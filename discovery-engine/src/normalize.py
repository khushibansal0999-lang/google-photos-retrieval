"""Unify raw scraped files into one records.jsonl with a common shape.

Each record: {id, source, url, author, date, title, text, score, parent_id}
Also applies a cheap keyword pre-filter so we don't pay to tag obviously
irrelevant items (storage/billing/etc). Everything that passes goes to Claude.
"""
import json, re, hashlib
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT = Path(__file__).resolve().parents[1] / "data" / "processed" / "records.jsonl"

# Broad on purpose — Claude does the real relevance judgement.
RETRIEVAL_HINTS = re.compile(
    r"\b(search|find|finding|found|look(ing)? for|locat|where (is|are|did)|can'?t see|"
    r"remember|old (photo|pic|picture|video)|from (last|a few|two|three|\d+) (year|month)|"
    r"screenshot|receipt|document|lens|face group|map view|album)",
    re.I,
)

def _id(*parts) -> str:
    return hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest()[:12]

def _rec(source, url, author, date, title, text, score=None, parent_id=None):
    text = (text or "").strip()
    title = (title or "").strip()
    if len(text) + len(title) < (25 if source.startswith("reddit") else 60):
        return None
    return {
        "id": _id(source, url, text[:80]), "source": source, "url": url, "author": author,
        "date": date, "title": title, "text": text, "score": score, "parent_id": parent_id,
    }

def load_reddit(path):
    items = json.loads(path.read_text())
    # index post titles so comments carry their thread context
    titles = {it.get("id") or it.get("postId"): it.get("title") for it in items if it.get("dataType") == "post"}
    titles.update({f"t3_{k}": v for k, v in list(titles.items()) if k and not str(k).startswith("t3_")})
    for it in items:
        if it.get("dataType") == "post":
            yield _rec("reddit_post", it.get("url") or it.get("postUrl"), it.get("authorName"), it.get("createdAt"),
                       it.get("title"), it.get("body"), it.get("upVotes"))
        else:
            ctx = titles.get(it.get("postId")) or titles.get(str(it.get("postId", "")).replace("t3_", "")) or ""
            yield _rec("reddit_comment", it.get("url"), it.get("authorName"), it.get("createdAt") or it.get("commentCreatedAt"),
                       f"[re: {ctx}]" if ctx else "", it.get("body"), it.get("upVotes"), it.get("postId"))

def load_playstore(path):
    for it in json.loads(path.read_text()):
        yield _rec("play_store", it.get("url") or it.get("reviewUrl"), it.get("userName") or it.get("name"),
                   it.get("date") or it.get("at"), "", it.get("text") or it.get("content"), it.get("score") or it.get("rating"))

def load_appstore(path):
    for it in json.loads(path.read_text()):
        yield _rec("app_store", it.get("url"), it.get("userName") or it.get("author"),
                   it.get("date") or it.get("updated"), it.get("title"), it.get("text") or it.get("review"),
                   it.get("score") or it.get("rating"))

LOADERS = {"reddit": load_reddit, "play_store": load_playstore, "app_store": load_appstore}

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    seen, kept, total = set(), 0, 0
    with OUT.open("w") as f:
        for path in sorted(RAW.glob("*.json")):
            key = next((k for k in LOADERS if path.stem.startswith(k)), None)
            if not key:
                print("skip", path.name); continue
            n_src = 0
            for r in LOADERS[key](path):
                total += 1
                if not r or r["id"] in seen: continue
                blob = r["title"] + " " + r["text"]
                if not RETRIEVAL_HINTS.search(blob): continue
                seen.add(r["id"]); kept += 1; n_src += 1
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"{path.name}: kept {n_src}")
    print(f"total {total} -> kept {kept} -> {OUT}")

if __name__ == "__main__":
    main()

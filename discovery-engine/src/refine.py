"""Second pass over relevant records: classify the *kind* of problem so the dashboard can
separate true vague-memory retrieval failures from UI regressions and data loss.
Adds tags.problem_class + tags.memory_index_gap. ~15 records/request.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from llm import generate_json

ROOT = Path(__file__).resolve().parents[1]
TAGGED = ROOT / "data" / "processed" / "tagged.jsonl"

PROBLEM_CLASSES = [
    "vague_memory_retrieval",   # user has a partial memory of a specific item and search/browse fails to bridge it
    "ui_navigation_regression", # layout/menus changed; can't find the search bar / folders / albums
    "data_missing_sync",        # photos genuinely absent: backup, deletion, device change
    "feature_request",          # wants a capability (manual face add, tags, filename search) - no concrete failed retrieval
    "general_praise_or_success",
    "other",
]
SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "string"},
    "problem_class": {"type": "string", "enum": PROBLEM_CLASSES},
    "memory_index_gap": {"type": "string", "description": "If vague_memory_retrieval: in <=15 words, what the user REMEMBERS vs what the app INDEXES/needs. e.g. 'remembers words in screenshot; OCR search returns nothing'. Else empty."},
}, "required": ["id", "problem_class", "memory_index_gap"]}}}, "required": ["items"]}

SYSTEM = """You classify user feedback about Google Photos. The research question is specifically about
VAGUE-MEMORY RETRIEVAL: the user knows a specific photo exists, remembers something about it, and the app fails
to bridge from their memory to the item. Distinguish that from: UI/navigation regressions (search bar moved,
endless scroll, folders hidden), genuine data loss/sync problems, and feature requests. Be strict."""

def main():
    rows = [json.loads(l) for l in TAGGED.open() if l.strip()]
    todo = [r for r in rows if r["tags"]["is_relevant"] and "problem_class" not in r["tags"]]
    print(f"{len(todo)} relevant records to refine")
    by_id = {r["id"]: r for r in rows}
    for i in range(0, len(todo), 15):
        chunk = todo[i:i+15]
        body = "\n\n".join(f"=== id={r['id']} ===\nTEXT: {r['text'][:1500]}\nEXTRACTED: fails_at={r['tags']['failure_stage']}; mechanism={r['tags']['failure_detail']}" for r in chunk)
        try:
            out = generate_json(SYSTEM, f"Classify each record.\n\n{body}", SCHEMA)
            for it in out["items"]:
                if it["id"] in by_id:
                    by_id[it["id"]]["tags"]["problem_class"] = it["problem_class"]
                    by_id[it["id"]]["tags"]["memory_index_gap"] = it["memory_index_gap"]
        except Exception as e:
            print("batch error", repr(e)[:200])
        print(f"  {min(i+15, len(todo))}/{len(todo)}", flush=True); time.sleep(4)
    TAGGED.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    from collections import Counter
    print(Counter(r["tags"].get("problem_class") for r in rows if r["tags"]["is_relevant"]))

if __name__ == "__main__":
    main()

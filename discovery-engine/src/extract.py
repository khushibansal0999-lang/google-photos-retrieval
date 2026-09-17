"""Tag every record with the extraction schema using Gemini structured output (free tier).

Records are sent in small batches (default 8) to stay inside the daily request quota.
Usage: python src/extract.py [--limit N] [--batch 8] [--sleep 4]
Resumable: ids already in data/processed/tagged.jsonl are skipped.
"""
import argparse, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from schema import EXTRACTION_SCHEMA, SYSTEM_PROMPT
from llm import generate_json

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "data" / "processed" / "records.jsonl"
TAGGED = ROOT / "data" / "processed" / "tagged.jsonl"

BATCH_SCHEMA = {
    "type": "object",
    "properties": {"items": {"type": "array", "items": {
        "type": "object",
        "properties": {"id": {"type": "string"}, **EXTRACTION_SCHEMA["properties"]},
        "required": ["id"] + EXTRACTION_SCHEMA["required"],
    }}},
    "required": ["items"],
}


def tag_batch(recs):
    body = "\n\n".join(f"=== RECORD id={r['id']} source={r['source']} ===\nTITLE: {r['title']}\nTEXT:\n{r['text'][:3500]}"
                       for r in recs)
    user = f"Tag each of the {len(recs)} records below. Return one item per record, in the same order, echoing its id.\n\n{body}"
    out = generate_json(SYSTEM_PROMPT, user, BATCH_SCHEMA)
    by_id = {it["id"]: it for it in out["items"]}
    return [{**r, "tags": {k: v for k, v in by_id[r["id"]].items() if k != "id"}} for r in recs if r["id"] in by_id]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--sleep", type=float, default=4.0, help="seconds between calls (free tier ~10-15 RPM)")
    args = ap.parse_args()

    done = {json.loads(l)["id"] for l in TAGGED.open() if l.strip()} if TAGGED.exists() else set()
    todo = [json.loads(l) for l in RECORDS.open() if l.strip()]
    todo = [r for r in todo if r["id"] not in done]
    if args.limit: todo = todo[: args.limit]
    print(f"{len(done)} already tagged, {len(todo)} to go, ~{-(-len(todo)//args.batch)} requests")

    n_ok = n_err = 0
    with TAGGED.open("a") as out:
        for i in range(0, len(todo), args.batch):
            chunk = todo[i:i + args.batch]
            try:
                for res in tag_batch(chunk):
                    out.write(json.dumps(res, ensure_ascii=False) + "\n"); n_ok += 1
                out.flush()
            except Exception as e:
                n_err += len(chunk); print("batch error", chunk[0]["id"], repr(e)[:200])
            if (i // args.batch) % 5 == 0:
                print(f"  tagged {n_ok}/{len(todo)}  (errors {n_err})")
            time.sleep(args.sleep)
    print(f"done: {n_ok} tagged, {n_err} errors -> {TAGGED}")


if __name__ == "__main__":
    main()

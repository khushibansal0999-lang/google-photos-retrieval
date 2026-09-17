"""Download Apify dataset results into data/raw/<source>.json.

Usage: python src/fetch_apify.py <source_name> <dataset_id>
Requires APIFY_TOKEN in .env (or pass datasets that are public).
"""
import json, os, sys
from pathlib import Path
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

def main(source: str, dataset_id: str):
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    items = list(client.dataset(dataset_id).iterate_items())
    out = RAW / f"{source}.json"
    out.write_text(json.dumps(items, ensure_ascii=False, indent=1))
    print(f"{source}: {len(items)} items -> {out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

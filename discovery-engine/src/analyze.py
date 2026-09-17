"""Quick pivots over tagged.jsonl -> prints tables + writes data/processed/summary.json"""
import json
from collections import Counter
from itertools import product
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TAGGED = ROOT / "data" / "processed" / "tagged.jsonl"

def load() -> pd.DataFrame:
    rows = []
    for l in TAGGED.open():
        if not l.strip(): continue
        r = json.loads(l); t = r.pop("tags")
        rows.append({**r, **{k: v for k, v in t.items() if not k.startswith("_")}})
    return pd.DataFrame(rows)

def main():
    df = load()
    rel = df[df.is_relevant]
    print(f"{len(df)} tagged, {len(rel)} relevant ({len(rel)/max(len(df),1):.0%})\n")
    print("== by source ==\n", rel.source.value_counts(), "\n")
    print("== failure stage ==\n", rel.failure_stage.value_counts(), "\n")
    print("== photo type ==\n", rel.photo_type.value_counts(), "\n")
    print("== cues remembered ==\n", Counter(c for cs in rel.cues_remembered for c in cs).most_common(), "\n")
    print("== cues forgotten ==\n", Counter(c for cs in rel.cues_forgotten for c in cs).most_common(), "\n")
    print("== workaround ==\n", rel.workaround.value_counts(), "\n")
    print("== photo type x failure stage ==")
    print(pd.crosstab(rel.photo_type, rel.failure_stage), "\n")
    summary = {
        "n_tagged": int(len(df)), "n_relevant": int(len(rel)),
        "failure_stage": rel.failure_stage.value_counts().to_dict(),
        "photo_type": rel.photo_type.value_counts().to_dict(),
        "cues_remembered": dict(Counter(c for cs in rel.cues_remembered for c in cs)),
        "cues_forgotten": dict(Counter(c for cs in rel.cues_forgotten for c in cs)),
        "workaround": rel.workaround.value_counts().to_dict(),
    }
    (ROOT / "data" / "processed" / "summary.json").write_text(json.dumps(summary, indent=1))

if __name__ == "__main__":
    main()

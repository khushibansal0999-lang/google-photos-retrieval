#!/bin/zsh
# Full pipeline. Run from discovery-engine/ after filling ../.env
set -e
cd "$(dirname "$0")"
.venv/bin/python src/fetch_apify.py reddit HWQcxjh34Kjx4qyy0   # 2,491 Reddit posts+comments
.venv/bin/python src/normalize.py
.venv/bin/python src/extract.py --limit 30                      # smoke test first
.venv/bin/python src/analyze.py

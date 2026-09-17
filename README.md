# Google Photos — Vague-Memory Photo Retrieval (Graduation Project)

Goal: increase the % of users who successfully retrieve a photo they remember but cannot precisely describe.

## Links
- **Discovery engine (live):** https://app-photos-retrieval-qvlu7ymwqfadwg3siqnqjb.streamlit.app/
- **Repo:** https://github.com/khushibansal0999-lang/google-photos-retrieval
- MVP (live): _coming_

## Structure
- `discovery-engine/` — Part 1. Scrape → Claude structured extraction → SQLite → Streamlit query UI
  - `data/raw/` scraped JSON (Reddit, Play Store, App Store, YouTube, support forums)
  - `data/processed/` tagged/extracted records
  - `src/` pipeline scripts
  - `app/` Streamlit discovery UI
- `research/` — Parts 3 & 6. Interview guide, notes, MVP test sessions
- `mvp/` — Part 5. AI-native retrieval prototype
- `deck/` — Final 10-slide deck

## Timeline
- Wk1 (Sep 16–22): engine + data + recruit
- Wk2 (Sep 23–29): interviews, synthesis, problem definition, MVP v0
- Wk3 (Sep 30–Oct 5): MVP deploy, user tests, metrics, deck
- Oct 6: buffer. Deadline Oct 7, 3:59 PM IST

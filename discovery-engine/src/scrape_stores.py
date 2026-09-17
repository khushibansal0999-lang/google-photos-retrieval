"""Scrape Google Play + App Store reviews for Google Photos without Apify.

Play Store: google-play-scraper (unofficial, free). Pulls newest + most-relevant for several countries.
App Store:  Apple's public RSS feed, 10 pages x 50 reviews per country.
Writes data/raw/play_store.json and data/raw/app_store.json
"""
import json, time
from pathlib import Path
import requests
from google_play_scraper import Sort, reviews

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
PLAY_ID = "com.google.android.apps.photos"
IOS_ID = "962194608"

def play_store(countries=("us", "in", "gb", "ca", "au"), per_country=1500):
    out, seen = [], set()
    for c in countries:
        for sort in (Sort.MOST_RELEVANT, Sort.NEWEST):
            token, got = None, 0
            while got < per_country:
                batch, token = reviews(PLAY_ID, lang="en", country=c, sort=sort, count=200, continuation_token=token)
                for r in batch:
                    if r["reviewId"] in seen: continue
                    seen.add(r["reviewId"])
                    out.append({"id": r["reviewId"], "userName": r["userName"], "score": r["score"], "text": r["content"],
                                "date": r["at"].isoformat(), "thumbsUp": r["thumbsUpCount"], "country": c,
                                "url": f"https://play.google.com/store/apps/details?id={PLAY_ID}&reviewId={r['reviewId']}"})
                got += len(batch)
                if not token or not batch: break
                time.sleep(0.5)
        print(f"play {c}: total so far {len(out)}")
    (RAW / "play_store.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return len(out)

def app_store(countries=("us", "in", "gb", "ca", "au")):
    out, seen = [], set()
    for c in countries:
        for page in range(1, 11):
            url = f"https://itunes.apple.com/{c}/rss/customerreviews/page={page}/id={IOS_ID}/sortby=mostrecent/json"
            try:
                r = requests.get(url, timeout=20); r.raise_for_status()
                entries = r.json().get("feed", {}).get("entry", [])
            except Exception as e:
                print("appstore", c, page, "err", e); break
            if isinstance(entries, dict): entries = [entries]
            if not entries: break
            for e in entries:
                rid = e["id"]["label"]
                if rid in seen: continue
                seen.add(rid)
                out.append({"id": rid, "userName": e["author"]["name"]["label"], "score": int(e["im:rating"]["label"]),
                            "title": e["title"]["label"], "text": e["content"]["label"], "date": e["updated"]["label"],
                            "country": c, "url": e["author"]["uri"]["label"]})
            time.sleep(0.3)
        print(f"appstore {c}: total so far {len(out)}")
    (RAW / "app_store.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return len(out)

if __name__ == "__main__":
    print("play store:", play_store())
    print("app store:", app_store())

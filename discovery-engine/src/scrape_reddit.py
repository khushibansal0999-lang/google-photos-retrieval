"""Scrape Reddit via public .json endpoints — no account, no cost.

Collects posts from retrieval-focused searches + r/googlephotos listings, then top-level
comments for each post. Writes data/raw/reddit.json in the same shape normalize.py expects.
Polite rate limiting (~1 req / 6.5s) to stay under Reddit's anonymous limit.
"""
import json, time, sys
from pathlib import Path
import requests

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT = RAW / "reddit_public.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
SLEEP = 3.0

SEARCHES = [
    "google photos can't find photo", "google photos search not finding", "google photos find old photo",
    "google photos search doesn't work", "google photos how to find a picture", "google photos looking for a photo from",
    "google photos search screenshot", "google photos search by description", "can't find a photo I know I took",
    "google photos remember photo", "google photos find photo from trip", "google photos search receipt document",
    "google photos gemini search", "google photos ask photos",
]
SUBREDDIT_LISTINGS = [
    ("googlephotos", "top", "all"), ("googlephotos", "top", "year"), ("googlephotos", "new", None),
]

def get(url, params=None, tries=4):
    for i in range(tries):
        r = requests.get(url, params=params, headers=UA, timeout=30)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 429:
            wait = 30 * (i + 1); print(f"  429, sleeping {wait}s", flush=True); time.sleep(wait); continue
        print("  http", r.status_code, url, flush=True); return None
    return None

def post_rec(d):
    return {"dataType": "post", "id": d["name"], "postId": d["name"], "title": d.get("title"), "body": d.get("selftext"),
            "url": "https://www.reddit.com" + d.get("permalink", ""), "authorName": d.get("author"),
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(d.get("created_utc", 0))),
            "upVotes": d.get("score"), "communityName": "r/" + d.get("subreddit", ""), "numComments": d.get("num_comments", 0)}

def collect_posts():
    posts = {}
    for q in SEARCHES:
        for sort in ("relevance", "top"):
            after = None
            for _ in range(2):  # 2 pages x 100
                data = get("https://old.reddit.com/search.json", {"q": q, "sort": sort, "t": "all", "limit": 100, "after": after})
                time.sleep(SLEEP)
                if not data: break
                kids = data["data"]["children"]
                for k in kids:
                    if k["kind"] == "t3": posts[k["data"]["name"]] = post_rec(k["data"])
                after = data["data"].get("after")
                if not after: break
        print(f"search '{q}': {len(posts)} posts so far", flush=True)
    for sub, sort, t in SUBREDDIT_LISTINGS:
        after = None
        for _ in range(5):  # up to 500 per listing
            params = {"limit": 100, "after": after}
            if t: params["t"] = t
            data = get(f"https://old.reddit.com/r/{sub}/{sort}.json", params)
            time.sleep(SLEEP)
            if not data: break
            for k in data["data"]["children"]:
                if k["kind"] == "t3": posts[k["data"]["name"]] = post_rec(k["data"])
            after = data["data"].get("after")
            if not after: break
        print(f"r/{sub}/{sort}: {len(posts)} posts so far", flush=True)
    return posts

def collect_comments(posts, max_per_post=15):
    comments = []
    todo = [p for p in posts.values() if p["numComments"] > 0]
    for i, p in enumerate(todo):
        data = get(p["url"].replace("www.reddit.com","old.reddit.com").rstrip("/") + ".json", {"limit": max_per_post, "depth": 1, "sort": "top"})
        time.sleep(SLEEP)
        if not data or len(data) < 2: continue
        for k in data[1]["data"]["children"]:
            if k["kind"] != "t1": continue
            d = k["data"]
            if d.get("body") in (None, "[deleted]", "[removed]"): continue
            comments.append({"dataType": "comment", "id": d["name"], "postId": p["postId"], "parentId": d.get("parent_id"),
                             "body": d["body"], "url": "https://www.reddit.com" + d.get("permalink", ""),
                             "authorName": d.get("author"), "upVotes": d.get("score"),
                             "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(d.get("created_utc", 0)))})
        if i % 25 == 0:
            print(f"comments: {i}/{len(todo)} posts, {len(comments)} comments", flush=True)
            OUT.write_text(json.dumps(list(posts.values()) + comments, ensure_ascii=False, indent=1))  # checkpoint
    return comments

if __name__ == "__main__":
    posts = collect_posts()
    OUT.write_text(json.dumps(list(posts.values()), ensure_ascii=False, indent=1))
    print(f"POSTS DONE: {len(posts)}", flush=True)
    comments = collect_comments(posts)
    OUT.write_text(json.dumps(list(posts.values()) + comments, ensure_ascii=False, indent=1))
    print(f"ALL DONE: {len(posts)} posts + {len(comments)} comments -> {OUT}", flush=True)

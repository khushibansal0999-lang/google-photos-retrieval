"""Bring the author's own images into the demo library.

Run once. Crops each to a square, writes it to mvp/scenes/<slug>/0.jpg where
thumbs.py already looks, and prints the library entries to paste in.

These are kept apart from the Openverse set in CREDITS.md on purpose: those are
CC0 and these were supplied by the author, whose provenance we have not
verified. Claiming one licence for both would be false.
"""
from pathlib import Path
import re
import sys

from PIL import Image, ImageOps

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = Path(__file__).resolve().parent.parent / "scenes"
PX = 320

# file -> (kind, title, tags, text-in-image, setting, tod)
# The kinds matter more than anything else here. The deck's whole finding is
# that paperwork and screenshots are what people fail to retrieve, so a demo
# library with real screenshots and real documents in it argues the case by
# existing.
ITEMS = [
    ("13.jpg", "photo", "Record on the turntable",
     ["vinyl", "record", "music", "turntable", "pink"],
     "Сияй, чёрт возьми · All Of A Sudden", "indoor", "evening"),
    ("14.jpg", "screenshot", "Saved: hot girls work hard",
     ["wallpaper", "quote", "saved", "gingham", "blue"],
     "HOT GIRLS WORK HARD", "indoor", ""),
    ("15.jpg", "screenshot", "Saved: study board",
     ["collage", "study", "motivation", "quote", "pinterest"],
     "Everything is hard, before it's easy", "indoor", ""),
    ("16.jpg", "photo", "Pink record, close up",
     ["vinyl", "record", "music", "pink", "turntable"],
     "All Of A Sudden", "indoor", "evening"),
    ("17.jpg", "screenshot", "Screenshot of a tweet",
     ["twitter", "social", "feed", "screenshot", "browser"],
     "Hiking High Dune · Montreal trends · Seinfeld", "indoor", ""),
    ("18.jpg", "screenshot", "Screenshot of a repo page",
     ["github", "code", "repo", "screenshot", "browser", "work"],
     "facebook / react · 134,638 stars", "indoor", ""),
    ("19.jpg", "photo", "Playing the AR game on the street",
     ["game", "phone", "street", "augmented reality", "walk"],
     "", "outdoor", "afternoon"),
    ("20.jpg", "photo", "Checking the chart at the desk",
     ["crypto", "chart", "phone", "desk", "finance", "screens"],
     "BTC-USD 63,198.00", "indoor", "afternoon"),
    ("21.jpg", "document", "Lecture slide on qubits",
     ["diagram", "slide", "quantum", "study", "notes", "paperwork"],
     "BIT · LINEAR · EXPONENTIAL · QUBIT · calculation", "indoor", ""),
    ("22.jpg", "photo", "Laptop running the profiler",
     ["laptop", "code", "work", "desk", "profiler"],
     "Memory allocation · 63.23 MB", "indoor", "afternoon"),
    ("23.jpg", "photo", "Laptop open on Slack",
     ["slack", "work", "laptop", "desk", "glasses", "messages"],
     "#social-media · Acme Inc", "indoor", "afternoon"),
    ("24.jpg", "screenshot", "Saved: dreams don't work",
     ["wallpaper", "quote", "flowers", "blue", "saved"],
     "dreams don't work unless you do", "indoor", ""),
    ("25.jpg", "screenshot", "Screenshot of the editor",
     ["code", "editor", "screenshot", "work", "javascript"],
     "Carousel.prototype · getItemForDirection", "indoor", "night"),
    ("26.jpg", "document", "Portfolio CV, one page",
     ["resume", "cv", "portfolio", "design", "paperwork", "official"],
     "Hello, I'm Han · Education · Experience · Technical skills", "indoor", ""),
    ("27.jpg", "screenshot", "Saved: what, like it's hard",
     ["wallpaper", "quote", "pink", "saved"],
     "WHAT, LIKE IT'S Hard?", "indoor", ""),
    ("28.jpg", "photo", "Castle under the moon",
     ["art", "wallpaper", "moon", "castle", "night", "fantasy"],
     "", "outdoor", "night"),
]


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for fn, kind, title, tags, text, setting, tod in ITEMS:
        src = SRC / fn
        if not src.exists():
            print(f"  !! missing {src}", file=sys.stderr)
            continue
        d = OUT / slug(title)
        d.mkdir(exist_ok=True)
        img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        ImageOps.fit(img, (PX, PX), Image.LANCZOS, centering=(0.5, 0.4)).save(
            d / "0.jpg", "JPEG", quality=80, optimize=True)
        rows.append((kind, title, tags, text, setting, tod))
        print(f"  {kind:11} {slug(title)}")
    print(f"\n{len(rows)} images written to {OUT.name}/")
    return rows


if __name__ == "__main__":
    main()

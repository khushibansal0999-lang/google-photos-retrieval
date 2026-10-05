"""Fetch one small, freely-licensed photo per scene in the demo library.

Run once, by hand, to populate mvp/scenes/. The app never calls this: the
images are committed, so the deployed link does not depend on anyone else's
server staying up or on a rate limit we do not control.

    python mvp/tools/fetch_scenes.py --dry     # show what would be fetched
    python mvp/tools/fetch_scenes.py           # actually fetch

Source is Openverse (openverse.org), Wikimedia's search over openly licensed
media, filtered to CC0 only. CC0 is a public-domain dedication: free to use,
modify and redistribute, no attribution required. We record attribution in
mvp/scenes/CREDITS.md anyway, because not being obliged to credit someone is
a poor reason not to.

Only PHOTO items get a real picture. Documents and screenshots keep their
drawn thumbnails on purpose -- a real photograph of a bill or an ID card is
someone's actual bill or ID card, and the drawn page and phone glyphs make
the kind of each result readable at a glance, which is doing real work in the
interface.
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "scenes"
API = "https://api.openverse.org/v1/images/"
UA = "nextleap-student-project/1.0 (portfolio prototype; contact via github)"

PX = 320          # square thumbnails; the grid never shows them larger
QUALITY = 78
VARIANTS = 4      # each repeating scene appears 4x in the library

# StockSnap only. Flickr's CC0 pool returns genuinely unrelated material (a
# search for bookshelves came back with a lingerie portrait) and Rawpixel's
# returns public-domain paintings and engravings filed as photographs, which
# made "kids playing cricket" an 18th-century oil. StockSnap is all modern
# photography, and this gets opened by people we do not know.
SOURCES = "stocksnap"

# Scene title -> the query that finds it, and how many variants we need.
# Queries lean towards places and objects rather than faces: a stranger's
# portrait captioned "my sister" would be a worse lie than an empty frame.
SCENES = {
    "Morning walk by the lake":          ("lake morning", VARIANTS),
    "Groceries laid out on the counter": ("groceries", VARIANTS),
    "Street dog asleep in the sun":      ("dog street", VARIANTS),
    "Dinner at home, plates from above": ("dinner table food", VARIANTS),
    "Concert, hands in the air":         ("concert crowd", VARIANTS),
    "Rain on the window from the bus":   ("rain window", VARIANTS),
    "Hill station viewpoint":            ("hills valley green", VARIANTS),
    "Birthday cake with candles lit":    ("birthday cake candles", VARIANTS),
    "Bookshelf, new arrangement":        ("bookshelf books", VARIANTS),
    "Beach at sunset":                   ("beach sunset", VARIANTS),
    "Office desk on a quiet day":        ("office desk", VARIANTS),
    "Temple corridor":                   ("temple", VARIANTS),
    "Cat on a parked scooter":           ("cat", VARIANTS),
    "Friends on a rooftop at night":     ("city night lights", VARIANTS),
    "Long queue outside the bank":       ("people walking street", VARIANTS),
    "Plant that finally flowered":       ("potted plant flower", VARIANTS),
    "Fog on the morning drive":          ("fog road", VARIANTS),
    "Snacks on the train table":         ("train window travel", VARIANTS),
    "New shoes, still in the box":       ("shoes", VARIANTS),
    "Kids playing cricket in the lane":  ("children playing", VARIANTS),
    "Market stall, vegetables stacked":  ("market vegetables", VARIANTS),
    # added after user testing, to thicken the library
    "Snow up north":                     ("snow mountains", VARIANTS),
    "Festival lights down the street":   ("festival lights", VARIANTS),
    "Boat on the backwaters":            ("boat river", VARIANTS),
    "Bridge at dusk":                    ("bridge dusk", VARIANTS),
    "Kitten behind the shop":            ("kitten", VARIANTS),
    "Breakfast at the hotel":            ("breakfast table", VARIANTS),
    "Cycling on the ring road":          ("bicycle", VARIANTS),
    "Leaves turning in the park":        ("autumn leaves park", VARIANTS),
    # planted items: these appear once each
    "Sister at the wedding, evening":    ("bride wedding", 1),
    "Group shot at the wedding":         ("wedding celebration", 1),
    "Small cafe on the Goa trip":        ("coffee shop", 1),
    "Waterfall, somewhere off the highway": ("waterfall forest", 1),
    "Roadside tea stall on the way back": ("tea", 1),
    "Medicine strip":                    ("pills medicine", 1),
    "Childhood photo, scanned":          ("kids bike", 1),
    "Childhood photo, birthday":         ("birthday cake candles", 1),
}


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _name(creator):
    """Decode a percent-encoded creator name for the credits table.

    These arrive as "Kai%20Oberh%E4user". The bytes are sometimes UTF-8 and
    sometimes Latin-1, and guessing wrong spells a real person's name with a
    replacement character, so try the former and fall back to the latter.
    """
    if not creator:
        return "unknown"
    raw = urllib.parse.unquote_to_bytes(creator)
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return creator


def search(query, want):
    """Ask Openverse for CC0 images, largest first, and return the candidates."""
    qs = urllib.parse.urlencode({
        "q": query, "license": "cc0", "page_size": max(8, want * 4),
        "mature": "false", "category": "photograph", "source": SOURCES,
    })
    req = urllib.request.Request(API + "?" + qs, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("results", [])


def square(raw):
    """Centre-crop to a square and shrink. ImageOps.fit does both in one pass."""
    img = Image.open(BytesIO(raw))
    img = ImageOps.exif_transpose(img).convert("RGB")
    return ImageOps.fit(img, (PX, PX), Image.LANCZOS, centering=(0.5, 0.45))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true",
                    help="list what would be fetched, download nothing")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    credits, total, failures = [], 0, []

    for title, (query, want) in SCENES.items():
        d = OUT / slug(title)
        try:
            hits = search(query, want)
        except Exception as e:                       # noqa: BLE001
            failures.append(f"{title}: search failed ({e})")
            continue
        if not hits:
            failures.append(f"{title}: no CC0 results for {query!r}")
            continue

        if args.dry:
            print(f"{title}\n  query {query!r} -> {len(hits)} hits, want {want}")
            for h in hits[:want]:
                print(f"    {h['license']}  {(h.get('title') or '?')[:52]!r}"
                      f"  {h.get('source')}")
            continue

        d.mkdir(exist_ok=True)
        got = 0
        for h in hits:
            if got >= want:
                break
            # Openverse's own thumbnail proxy, not h["url"]. The upstream CDNs
            # 403 anything without a browser User-Agent, and pretending to be a
            # browser to scrape someone's CDN is not a thing to build into a
            # portfolio project. The proxy is the documented way in, and its
            # output is already about the size we want.
            src = h.get("thumbnail") or h["url"]
            try:
                req = urllib.request.Request(src, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=40) as r:
                    raw = r.read()
                path = d / f"{got}.jpg"
                square(raw).save(path, "JPEG", quality=QUALITY, optimize=True)
            except Exception:                        # noqa: BLE001
                continue                             # a dead link is not fatal
            total += path.stat().st_size
            credits.append(
                f"| {title} | [{(h.get('title') or 'untitled')[:44]}]"
                f"({h.get('foreign_landing_url') or h['url']}) "
                f"| {_name(h.get('creator'))} | {h['license'].upper()} |")
            got += 1
        if got < want:
            failures.append(f"{title}: got {got} of {want}")
        print(f"{slug(title):38} {got}/{want}")

    if args.dry:
        return

    (OUT / "CREDITS.md").write_text(
        "# Photo credits\n\n"
        "Every image here is CC0 (public domain dedication), found through\n"
        "[Openverse](https://openverse.org). CC0 asks for no attribution.\n"
        "These are listed anyway.\n\n"
        "Regenerate with `python mvp/tools/fetch_scenes.py`.\n\n"
        "| scene | image | creator | licence |\n|---|---|---|---|\n"
        + "\n".join(credits) + "\n")

    print(f"\n{len(credits)} images, {total/1e6:.2f} MB total")
    for f in failures:
        print("  !! " + f, file=sys.stderr)


if __name__ == "__main__":
    main()

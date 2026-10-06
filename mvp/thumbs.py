"""Thumbnails: real photographs where we have one, drawn where we should not.

Photos come from mvp/scenes/, a small set of CC0 stock images fetched once by
tools/fetch_scenes.py and committed, so the deployed app depends on no one
else's server. A scene folder is found by slugifying the item's title, and
which of its variants an item gets is decided by a hash of the item id, so a
scene that repeats through the library does not repeat the same frame.

Documents and screenshots stay drawn, deliberately. A real photograph of a
bill or an ID card is someone's actual bill or ID card, and the drawn page and
phone glyphs let an evaluator see what kind each result is without reading the
label -- which the interface is relying on.

If mvp/scenes/ is missing or incomplete, every item falls back to the drawn
version and the app still runs. Nobody should meet a broken image.
"""
import base64
import hashlib
import re
from functools import lru_cache
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

SCENES = Path(__file__).resolve().parent / "scenes"

W = H = 300

# muted, colour-blind-safe field. No red/green pairing carries meaning here;
# colour is decoration, the kind glyph is the signal.
PALETTE = [
    ((208, 224, 247), (150, 185, 232)),
    ((247, 226, 214), (232, 186, 160)),
    ((223, 235, 222), (176, 205, 180)),
    ((234, 224, 241), (196, 176, 214)),
    ((246, 238, 210), (222, 205, 150)),
    ((214, 234, 236), (162, 202, 208)),
]


def _seed(item):
    return int(hashlib.md5(item["id"].encode()).hexdigest()[:8], 16)


def _gradient(draw, top, bottom):
    for y in range(H):
        f = y / H
        draw.line(
            [(0, y), (W, y)],
            fill=tuple(int(top[i] + (bottom[i] - top[i]) * f) for i in range(3)),
        )


def _photo(img, draw, s, item=None):
    a, b = PALETTE[s % len(PALETTE)]
    _gradient(draw, a, b)
    ink = tuple(max(0, c - 70) for c in b)
    # a horizon and a couple of shapes: enough to read as a scene, not a chart
    hz = 150 + (s % 60)
    draw.rectangle([0, hz, W, H], fill=tuple(max(0, c - 28) for c in b))
    r = 26 + (s % 30)
    draw.ellipse([W - 90 - r // 2, 40, W - 90 + r, 40 + r + r // 2], fill=(255, 255, 255, 90))
    for k in range(3):
        x = 20 + ((s >> (k * 3)) % 4) * 60
        pk = 40 + ((s >> (k * 2)) % 70)
        draw.polygon([(x, hz), (x + 55, hz - pk), (x + 110, hz)], fill=ink)


def _paper_kind(item):
    """Which shape of paperwork this is, read off the item's own tags.

    Falls back to a generic form, so a new document type still renders.
    """
    tags = set(item.get("tags", []))
    title = item.get("title", "").lower()
    if "boarding pass" in tags:                      return "pass"
    if "id" in tags or "identity" in tags:           return "card"
    if "invitation" in tags:                         return "invite"
    # a utility bill arrives as a letter; a cafe bill as a till slip
    if {"utility", "insurance", "policy", "prescription"} & tags: return "form"
    if {"receipt", "bill"} & tags:                   return "receipt"
    if "whiteboard" in tags:                         return "board"
    if {"password", "recovery", "codes"} & tags:     return "secret"
    if "screenshot" in tags or "screenshot" in title: return "rows"
    return "form"


# Paperwork is drawn, and the drawing has to earn its place in a grid of real
# photographs. The first version was pale grey on pale grey and ignored its own
# seed, so every bill came out pixel-identical and the grid read as a row of
# empty placeholders. Everything below is driven by the seed: paper tone, brand
# colour, how many lines, where they break. Two bills now look like two bills.
PAPER = (253, 252, 250)
DESK  = (228, 229, 233)
INK   = (62, 68, 78)
MID   = (126, 132, 142)
FAINT = (176, 181, 189)

# plausible letterhead colours. No red: red means "wrong" everywhere else here.
BRAND = [(38, 82, 148), (22, 104, 92), (86, 54, 122), (150, 92, 28),
         (40, 54, 74), (16, 92, 130), (112, 48, 70), (54, 86, 36)]


def _tone(s, n=4):
    """A slightly different paper white per item, so a stack is not one block."""
    k = (s >> 9) % n
    return tuple(c - k * 3 for c in PAPER)


def _rule(draw, x, y, w, widths, gap, h=7, dark=MID, light=FAINT, every=3):
    for i, f in enumerate(widths):
        draw.rectangle([x, y, x + int(w * f), y + h],
                       fill=dark if i % every == 0 else light)
        y += gap
    return y


def _widths(s, n):
    """Line lengths that differ per item but never look random."""
    out, v = [], s
    for _ in range(n):
        v = (v * 1103515245 + 12345) & 0x7FFFFFFF
        out.append(0.42 + (v % 60) / 100)
    return out


def _receipt(draw, s):
    """A till receipt: narrow, torn foot, a total that stands out."""
    brand = BRAND[s % len(BRAND)]
    draw.rectangle([0, 0, W, H], fill=DESK)
    x0, x1 = 74 + (s % 3) * 6, W - 74 - (s % 3) * 6
    draw.rectangle([x0, 8, x1, H - 24], fill=_tone(s))
    for i in range((x1 - x0) // 10 + 1):
        draw.polygon([(x0 + i * 10, H - 24), (x0 + i * 10 + 5, H - 11),
                      (x0 + i * 10 + 10, H - 24)], fill=_tone(s))
    draw.ellipse([(x0 + x1) // 2 - 13, 22, (x0 + x1) // 2 + 13, 48], fill=brand)
    n = 5 + (s >> 3) % 4
    y = _rule(draw, x0 + 18, 64, x1 - x0 - 36, _widths(s, n), gap=18, h=6)
    draw.line([x0 + 18, y + 5, x1 - 18, y + 5], fill=MID, width=2)
    draw.rectangle([x0 + 18, y + 16, x0 + 62, y + 29], fill=INK)
    draw.rectangle([x1 - 76, y + 16, x1 - 18, y + 29], fill=brand)


def _pass(draw, s):
    """A boarding pass: landscape, a tear-off stub, a barcode."""
    brand = BRAND[(s >> 2) % len(BRAND)]
    draw.rectangle([0, 0, W, H], fill=DESK)
    draw.rounded_rectangle([16, 70, W - 16, H - 70], radius=10, fill=_tone(s))
    draw.rectangle([16, 70, W - 16, 110], fill=brand)
    draw.ellipse([30, 80, 54, 104], fill=(255, 255, 255))
    cut = W - 100
    for y in range(76, H - 76, 12):
        draw.line([cut, y, cut, y + 6], fill=FAINT, width=2)
    _rule(draw, 40, 130, 150, _widths(s, 3), gap=22, h=8)
    draw.rectangle([40, 204, 118, 220], fill=brand)
    v = s
    for i in range(13):          # 13 bars is what fits between the stub and the
        v = (v * 48271) & 0x7FFFFFFF    # card edge; 24 ran off the side
        draw.rectangle([cut + 14 + i * 5, 134, cut + 16 + i * 5 + v % 3, 212],
                       fill=INK if v % 2 else MID)


def _card(draw, s):
    """An ID card: landscape, a portrait box, a chip. No face."""
    brand = BRAND[(s >> 4) % len(BRAND)]
    draw.rectangle([0, 0, W, H], fill=DESK)
    draw.rounded_rectangle([24, 66, W - 24, H - 66], radius=12, fill=_tone(s))
    draw.rectangle([24, 66, W - 24, 100], fill=brand)
    draw.rounded_rectangle([44, 116, 120, 212], radius=6, fill=(216, 219, 224))
    draw.ellipse([66, 134, 98, 166], fill=(178, 183, 190))
    draw.pieslice([56, 168, 108, 220], 180, 360, fill=(178, 183, 190))
    draw.rounded_rectangle([W - 90, 180, W - 48, 210], radius=4, fill=(206, 176, 92))
    _rule(draw, 138, 124, 118, _widths(s, 4), gap=22, h=8)


def _invite(draw, s):
    """An invitation: centred, bordered, nothing like a bill."""
    ink = [(176, 142, 96), (150, 110, 130), (110, 130, 150)][s % 3]
    draw.rectangle([0, 0, W, H], fill=DESK)
    draw.rectangle([50, 20, W - 50, H - 20], fill=(253, 250, 244))
    draw.rectangle([66, 36, W - 66, H - 36], outline=ink, width=2)
    cx = W // 2
    draw.ellipse([cx - 9, 60, cx + 9, 78], outline=ink, width=2)
    for i, (wd, h) in enumerate([(74, 9), (116, 14), (58, 8), (96, 9)]):
        y = 96 + i * 34
        draw.rectangle([cx - wd // 2, y, cx + wd // 2, y + h],
                       fill=ink if i == 1 else FAINT)


def _form(draw, s):
    """A dense official page: letterhead, two columns, a stamp."""
    brand = BRAND[(s >> 5) % len(BRAND)]
    draw.rectangle([0, 0, W, H], fill=DESK)
    draw.rectangle([28, 14, W - 28, H - 14], fill=_tone(s))
    draw.rectangle([28, 14, W - 28, 56], fill=brand)
    draw.rectangle([44, 28, 104, 42], fill=(255, 255, 255))
    draw.rectangle([46, 70, 150, 82], fill=INK)
    y, n = 96, 4 + (s >> 6) % 3
    for i, f in enumerate(_widths(s, n)):
        draw.rectangle([46, y, 118, y + 7], fill=MID)
        draw.rectangle([136, y, 136 + int(118 * f), y + 7], fill=FAINT)
        y += 22
    draw.ellipse([W - 104, H - 104, W - 48, H - 48], outline=brand, width=3)
    draw.line([46, H - 52, 140, H - 52], fill=MID, width=2)


def _document(img, draw, s, item):
    """A stock photo of a bill is some real person's bill, so these are drawn.
    Each kind gets its own shape, read off the item's own tags, so the sort of
    thing a result is reads before the caption does."""
    {"receipt": _receipt, "pass": _pass, "card": _card,
     "invite": _invite}.get(_paper_kind(item), _form)(draw, s)


def _phone(draw, s, body):
    brand = BRAND[(s >> 7) % len(BRAND)]
    draw.rectangle([0, 0, W, H], fill=(214, 217, 223))
    draw.rounded_rectangle([62, 6, W - 62, H - 6], radius=22, fill=(24, 26, 30))
    draw.rounded_rectangle([72, 20, W - 72, H - 20], radius=14, fill=_tone(s))
    draw.rectangle([72, 20, W - 72, 56], fill=brand)
    draw.rectangle([88, 31, 148, 45], fill=(255, 255, 255))
    body(draw, s, brand)


def _shot_rows(draw, s, brand):
    """A booking or a list: rows with a leading icon."""
    y = 74
    for i, f in enumerate(_widths(s, 5)):
        draw.rounded_rectangle([88, y, 108, y + 16], radius=4, fill=brand)
        draw.rectangle([118, y + 3, 118 + int(100 * f), y + 11], fill=FAINT)
        y += 30


def _shot_dialog(draw, s, brand):
    """A password or a code: a boxed value in the middle of the screen."""
    draw.rounded_rectangle([90, 100, W - 90, 200], radius=10, fill=(237, 240, 246))
    draw.rectangle([106, 116, 170, 127], fill=brand)
    v = s
    for r in range(3):
        for c in range(2):
            v = (v * 48271) & 0x7FFFFFFF
            draw.rectangle([106 + c * 62, 144 + r * 18,
                            106 + c * 62 + 38 + v % 14, 144 + r * 18 + 10],
                           fill=INK)


def _board(draw, s):
    """A whiteboard: landscape, sticky notes, not a phone at all."""
    draw.rectangle([0, 0, W, H], fill=(204, 207, 213))
    draw.rectangle([20, 42, W - 20, H - 42], fill=(252, 252, 252))
    draw.rectangle([20, 42, W - 20, H - 42], outline=(168, 172, 179), width=3)
    cols = ["#FDE293", "#AECBFA", "#F6AEA9", "#A8DAB5", "#D7AEFB"]
    v = s
    for x, y in [(50, 72), (130, 68), (208, 78), (60, 158), (148, 150), (214, 166)]:
        v = (v * 48271) & 0x7FFFFFFF
        draw.rectangle([x, y, x + 54, y + 48], fill=cols[v % len(cols)])
    draw.line([38, 134, W - 38, 134], fill=(198, 201, 207), width=2)


def _screenshot(img, draw, s, item):
    kind = _paper_kind(item)
    if kind == "board":
        return _board(draw, s)
    _phone(draw, s, _shot_dialog if kind == "secret" else _shot_rows)


# Google Photos' four brand colours, in the order they sit on the pinwheel.
GP_BLUE, GP_RED, GP_YELLOW, GP_GREEN = "#4285F4", "#EA4335", "#FBBC04", "#34A853"


def logo(px=128):
    """The four-blade pinwheel, drawn rather than shipped as a file.

    Each blade is a half-disc whose flat edge runs from the centre outwards,
    rotated a quarter turn from the one before it. Used for the browser tab;
    the header uses the SVG in app.py, which stays crisp at any size.
    """
    k = px / 48.0
    img = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    blades = [                                   # bbox in a 48pt frame, arc span
        ((14, 4, 34, 24), -90, 90, GP_BLUE),     # top, bulging right
        ((24, 14, 44, 34), 0, 180, GP_RED),      # right, bulging down
        ((14, 24, 34, 44), 90, 270, GP_YELLOW),  # bottom, bulging left
        ((4, 14, 24, 34), 180, 360, GP_GREEN),   # left, bulging up
    ]
    for (x0, y0, x1, y1), a, b, colour in blades:
        draw.pieslice([x0 * k, y0 * k, x1 * k, y1 * k], a, b, fill=colour)
    return img


def _slug(title):
    """Must match tools/fetch_scenes.py, which named the folders."""
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


@lru_cache(maxsize=64)
def _variants(slug):
    d = SCENES / slug
    return tuple(sorted(p for p in d.glob("*.jpg"))) if d.is_dir() else ()


def _scene(item):
    """The committed picture for this item, or None to fall back to drawing.

    Any kind can have a real picture now, not just photos. The generic filler
    documents and screenshots still have no file and so are still drawn, which
    is what keeps the kind readable at a glance; but where a real screenshot or
    a real scanned page exists, showing it beats showing a diagram of one.
    """
    files = _variants(_slug(item["title"]))
    if not files:
        return None
    # Indexed, not hashed. Hashing four items into four pictures collides most
    # of the time -- a tester saw "Hill station viewpoint" four times with the
    # same photo, and said it made them trust the whole library less.
    path = files[item.get("variant", 0) % len(files)]
    try:
        return Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)
    except Exception:                       # noqa: BLE001 -- a bad file is not fatal
        return None


def render(item):
    img = _scene(item)
    if img is None:
        img = Image.new("RGB", (W, H), (255, 255, 255))
        draw = ImageDraw.Draw(img, "RGBA")
        s = _seed(item)
        {"document": _document,
         "screenshot": _screenshot}.get(item["kind"], _photo)(img, draw, s, item)
    if item.get("bw"):
        img = img.convert("L").convert("RGB")
    return img


@lru_cache(maxsize=256)
def _png(key, kind, title, bw, variant):
    buf = BytesIO()
    render({"id": key, "kind": kind, "title": title, "bw": bw,
            "variant": variant}).save(
        buf, format="JPEG", quality=82, optimize=True)
    return buf.getvalue()


def png(item):
    # cached on the fields render actually reads, so the grid is cheap to redraw
    return _png(item["id"], item["kind"], item["title"], bool(item.get("bw")),
                item.get("variant", 0))


@lru_cache(maxsize=256)
def _small(key, kind, title, bw, variant, px):
    buf = BytesIO()
    render({"id": key, "kind": kind, "title": title, "bw": bw,
            "variant": variant}).resize((px, px), Image.LANCZOS).save(
        buf, format="JPEG", quality=74, optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def b64(item, px=150):
    """Base64 for embedding straight into a CSS grid.

    Rendered small on purpose. The home grid inlines two dozen of these into
    the HTML, and at full size that was 400KB before the page could paint --
    on a cold Streamlit boot a tester already sat through ten seconds of
    spinner, so this is not the place to spend bytes.
    """
    return _small(item["id"], item["kind"], item["title"],
                  bool(item.get("bw")), item.get("variant", 0), px)


if __name__ == "__main__":
    from library import LIBRARY
    total = 0
    for it in LIBRARY[:6] + [i for i in LIBRARY if i["kind"] != "photo"][:4]:
        b = png(it)
        total += len(b)
        print(f"{it['kind']:11} {len(b):6} bytes  {it['title'][:40]}")
    print(f"avg ~{total // 10} bytes per thumbnail")

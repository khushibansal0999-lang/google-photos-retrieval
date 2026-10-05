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


PAPER  = (252, 252, 252)
DESK   = (232, 233, 236)
INK    = (96, 102, 110)
FAINT  = (198, 201, 206)
MID    = (158, 162, 169)


def _lines(draw, x, y, w, widths, gap=20, h=8, dark=MID, light=FAINT):
    for i, f in enumerate(widths):
        draw.rectangle([x, y, x + int(w * f), y + h], fill=dark if i % 3 == 0 else light)
        y += gap
    return y


def _receipt(draw, s):
    """A till receipt: narrow, torn at the foot, with a total that stands out."""
    draw.rectangle([0, 0, W, H], fill=DESK)
    x0, x1 = 78, W - 78
    draw.rectangle([x0, 10, x1, H - 26], fill=PAPER)
    for i in range(0, (x1 - x0) // 10):       # torn edge along the bottom
        draw.polygon([(x0 + i * 10, H - 26), (x0 + i * 10 + 5, H - 14),
                      (x0 + i * 10 + 10, H - 26)], fill=PAPER)
    draw.rectangle([x0 + 24, 30, x1 - 24, 42], fill=INK)
    y = _lines(draw, x0 + 20, 62, x1 - x0 - 40, [.9, .62, .84, .55, .78, .46, .7], gap=19, h=7)
    draw.line([x0 + 20, y + 4, x1 - 20, y + 4], fill=MID, width=2)
    draw.rectangle([x0 + 20, y + 16, x0 + 70, y + 30], fill=INK)      # TOTAL
    draw.rectangle([x1 - 92, y + 16, x1 - 20, y + 30], fill=INK)


def _pass(draw, s):
    """A boarding pass: landscape, a tear-off stub, a barcode."""
    draw.rectangle([0, 0, W, H], fill=DESK)
    draw.rounded_rectangle([18, 74, W - 18, H - 74], radius=10, fill=PAPER)
    draw.rectangle([18, 74, W - 18, 112], fill=(66, 110, 180))
    cut = W - 104
    for y in range(80, H - 80, 12):           # perforation
        draw.line([cut, y, cut, y + 6], fill=FAINT, width=2)
    _lines(draw, 42, 134, 150, [.95, .6, .85], gap=22, h=8)
    draw.rectangle([42, 206, 118, 222], fill=INK)
    for i in range(26):                       # barcode on the stub
        draw.rectangle([cut + 16 + i * 5, 136, cut + 18 + i * 5 + (i % 3), 212],
                       fill=INK if i % 2 else MID)


def _card(draw, s):
    """An ID card: landscape, a portrait box, a couple of fields. No face."""
    draw.rectangle([0, 0, W, H], fill=DESK)
    draw.rounded_rectangle([26, 68, W - 26, H - 68], radius=12, fill=PAPER)
    draw.rectangle([26, 68, W - 26, 100], fill=(60, 120, 92))
    draw.rounded_rectangle([46, 118, 122, 212], radius=6, fill=(214, 217, 222))
    draw.ellipse([68, 136, 100, 168], fill=(186, 190, 196))          # head
    draw.pieslice([58, 170, 110, 220], 180, 360, fill=(186, 190, 196))  # shoulders
    _lines(draw, 140, 126, 120, [.95, .7, .9, .55], gap=22, h=8)


def _invite(draw, s):
    """An invitation: centred, bordered, nothing like a bill."""
    draw.rectangle([0, 0, W, H], fill=DESK)
    draw.rectangle([54, 24, W - 54, H - 24], fill=(253, 250, 244))
    draw.rectangle([70, 40, W - 70, H - 40], outline=(198, 170, 120), width=2)
    cx = W // 2
    for i, (wd, h) in enumerate([(70, 10), (112, 14), (54, 8), (92, 10)]):
        y = 96 + i * 34
        draw.rectangle([cx - wd // 2, y, cx + wd // 2, y + h],
                       fill=(176, 142, 96) if i == 1 else FAINT)


def _form(draw, s):
    """A dense official page: header block, two columns, a signature line."""
    draw.rectangle([0, 0, W, H], fill=DESK)
    draw.rectangle([30, 16, W - 30, H - 16], fill=PAPER)
    draw.rectangle([30, 16, W - 30, 58], fill=INK)
    draw.rectangle([48, 72, 150, 84], fill=MID)
    y = 100
    for row in range(5):
        draw.rectangle([48, y, 122, y + 7], fill=MID)
        draw.rectangle([140, y, 140 + int(110 * (0.9 - 0.12 * (row % 4))), y + 7], fill=FAINT)
        y += 22
    draw.line([48, H - 54, 140, H - 54], fill=MID, width=2)


def _document(img, draw, s, item):
    """Paperwork is drawn, not photographed: a stock photo of a bill is some
    real person's bill. Each kind gets its own shape so the thumbnail says
    what sort of thing it is before you read the caption."""
    {"receipt": _receipt, "pass": _pass, "card": _card,
     "invite": _invite}.get(_paper_kind(item), _form)(draw, s)


def _phone(draw, s, body):
    draw.rectangle([0, 0, W, H], fill=(216, 219, 224))
    draw.rounded_rectangle([64, 8, W - 64, H - 8], radius=22, fill=(26, 28, 32))
    draw.rounded_rectangle([74, 22, W - 74, H - 22], radius=14, fill=(250, 250, 251))
    draw.rectangle([74, 22, W - 74, 56], fill=(60, 110, 180))
    draw.rectangle([90, 33, 150, 45], fill=(226, 232, 242))
    body(draw)


def _shot_rows(draw):
    """A booking or a list: rows with a leading icon."""
    y = 74
    for i in range(5):
        draw.rounded_rectangle([90, y, 110, y + 16], radius=4, fill=(206, 212, 222))
        draw.rectangle([120, y + 3, 120 + int(96 * (0.95 - 0.14 * (i % 4))), y + 11], fill=FAINT)
        y += 30


def _shot_dialog(draw):
    """A password or a code: a boxed value in the middle of the screen."""
    draw.rounded_rectangle([92, 104, W - 92, 196], radius=10, fill=(238, 241, 246))
    draw.rectangle([108, 120, 168, 130], fill=MID)
    for r in range(3):
        for c in range(2):
            draw.rectangle([108 + c * 62, 146 + r * 18, 108 + c * 62 + 50, 146 + r * 18 + 10],
                           fill=(120, 126, 136))


def _board(draw, s):
    """A whiteboard: landscape, sticky notes, not a phone at all."""
    draw.rectangle([0, 0, W, H], fill=(206, 209, 214))
    draw.rectangle([22, 44, W - 22, H - 44], fill=(250, 250, 250))
    draw.rectangle([22, 44, W - 22, H - 44], outline=(170, 174, 180), width=3)
    notes = [(52, 74, "#FDE293"), (132, 70, "#AECBFA"), (210, 80, "#F6AEA9"),
             (62, 160, "#A8DAB5"), (150, 152, "#FDE293"), (216, 168, "#AECBFA")]
    for x, y, col in notes:
        draw.rectangle([x, y, x + 54, y + 48], fill=col)
    draw.line([40, 136, W - 40, 136], fill=(200, 203, 208), width=2)


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
    """The committed photo for this item, or None to fall back to drawing."""
    if item["kind"] != "photo":
        return None
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

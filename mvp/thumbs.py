"""Thumbnails, drawn at run time.

No image files ship with this repo, which keeps it small, free to host, and
free of anything that looks like a real person's photo library. Paperwork is
drawn as a page and screenshots as a phone, so an evaluator can tell at a
glance what kind of thing each result is without reading the label.
"""
import hashlib
from io import BytesIO

from PIL import Image, ImageDraw

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


def _photo(img, draw, s):
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


def _document(img, draw, s):
    draw.rectangle([0, 0, W, H], fill=(238, 238, 240))
    draw.rectangle([34, 22, W - 34, H - 22], fill=(255, 255, 255))
    draw.rectangle([34, 22, W - 34, 62], fill=(90, 96, 104))
    y = 84
    widths = [0.82, 0.64, 0.74, 0.43, 0.79, 0.58, 0.69, 0.36]
    for i, wfrac in enumerate(widths):
        if y > H - 46:
            break
        draw.rectangle([52, y, 52 + int((W - 104) * wfrac), y + 9],
                       fill=(196, 199, 204) if i % 3 else (150, 154, 160))
        y += 24
    draw.rectangle([52, H - 54, 122, H - 40], fill=(120, 126, 134))


def _screenshot(img, draw, s):
    draw.rectangle([0, 0, W, H], fill=(224, 226, 230))
    draw.rounded_rectangle([62, 14, W - 62, H - 14], radius=18, fill=(28, 30, 34))
    draw.rounded_rectangle([72, 26, W - 72, H - 26], radius=12, fill=(248, 249, 250))
    draw.rectangle([72, 26, W - 72, 58], fill=(58, 62, 68))
    y = 76
    for i, wfrac in enumerate([0.7, 0.5, 0.62, 0.34, 0.58]):
        if y > H - 50:
            break
        draw.rectangle([88, y, 88 + int((W - 176) * wfrac), y + 8],
                       fill=(178, 182, 188) if i % 2 else (140, 145, 152))
        y += 22


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


def render(item):
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    s = _seed(item)
    {"document": _document, "screenshot": _screenshot}.get(item["kind"], _photo)(img, draw, s)
    if item.get("bw"):
        img = img.convert("L").convert("RGB")
    return img


def png(item):
    buf = BytesIO()
    render(item).save(buf, format="PNG", optimize=True)
    return buf.getvalue()


if __name__ == "__main__":
    from library import LIBRARY
    total = 0
    for it in LIBRARY[:6] + [i for i in LIBRARY if i["kind"] != "photo"][:4]:
        b = png(it)
        total += len(b)
        print(f"{it['kind']:11} {len(b):6} bytes  {it['title'][:40]}")
    print(f"avg ~{total // 10} bytes per thumbnail")

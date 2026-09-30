import json
IN = 914400
def emu(v): return int(round(v*IN))

def hexc(h):
    h = h.lstrip("#")
    return {"red":int(h[0:2],16)/255,"green":int(h[2:4],16)/255,"blue":int(h[4:6],16)/255}

# ---- Google Material tokens, lifted from the design PDF ----
INK    = hexc("202124")   # grey 900, primary text
GREY   = hexc("5F6368")   # grey 700, secondary text
BLUE   = hexc("1A73E8")   # Google blue 600
RED    = hexc("D93025")   # Google red 600
YELLOW = hexc("F9AB00")   # Google yellow 700
GREEN  = hexc("188038")   # Google green 700
AMBER  = hexc("B45309")   # readable text on yellow tint
ORNG   = RED              # legacy alias used by existing slide scripts

F_NEUT = hexc("F8F9FA")
F_BLUE = hexc("E8F0FE")
F_RED  = hexc("FCE8E6")
F_YEL  = hexc("FEF7E0")
F_GRN  = hexc("E6F4EA")
F_ORNG = F_RED            # legacy alias
F_WHT  = hexc("FFFFFF")
F_DARK = hexc("202124")   # black emphasis card
BORDER = hexc("DADCE0")
O_BLUE = BLUE
O_ORNG = RED

TITLE_FONT = "Montserrat"
BODY_FONT  = "Roboto"

# ---- NextLeap hard rule: nothing on a slide may render below 14pt ----
# Everything on the slide is 14. Only the slide title is larger. Hierarchy is
# carried by weight and colour, never by size, which keeps the pages compact.
FLOOR = 14
SUB = LEAD = STAT = FLOOR   # kept as names so older scripts still resolve
TITLE = 24                  # slide title, the only thing above the floor

# card colour cycle: (tint fill, solid accent, readable text on that tint)
CYCLE = [(F_BLUE, BLUE, BLUE), (F_RED, RED, RED), (F_YEL, YELLOW, AMBER),
         (F_GRN, GREEN, GREEN), (F_DARK, INK, F_WHT)]

# char-width (chars per inch) and line height (inches) by pt size, Roboto body
CPI = {9:15.4,9.5:14.6,10:13.9,10.5:13.2,11:12.6,12:11.6,13:10.7,14:9.9,15:9.3,16:8.7,18:7.7,20:7.0,22:6.3,25:5.6,28:5.0,34:4.1,40:3.5}
LH  = {9:0.155,9.5:0.163,10:0.172,10.5:0.180,11:0.189,12:0.206,13:0.223,14:0.240,15:0.257,16:0.275,18:0.309,20:0.343,22:0.377,25:0.429,28:0.480,34:0.583,40:0.686}
# Montserrat Bold is wider than Roboto Slab: fewer chars per inch
CPI_TITLE = {18:6.8,20:6.1,22:5.5,23:5.3,25:4.9,28:4.3}

def _iv(tbl,size):
    ks=sorted(tbl)
    if size in tbl: return tbl[size]
    lo=max([k for k in ks if k<size], default=ks[0]); hi=min([k for k in ks if k>size], default=ks[-1])
    if lo==hi: return tbl[lo]
    f=(size-lo)/(hi-lo); return tbl[lo]+f*(tbl[hi]-tbl[lo])

def fit(parts, w_in, h_in, label="", tbl=None):
    """Runs that do not end in a newline flow on into the next run, so measure
    by paragraph rather than by run: width in inches, then wrap."""
    inner = w_in - 0.20
    paras, cur = [], []
    for t, size in parts:
        chunks = t.split("\n")
        for j, ch in enumerate(chunks):
            if ch: cur.append((ch, size))
            if j < len(chunks)-1:
                paras.append(cur); cur = []
    if cur: paras.append(cur)
    total = 0.0
    for p in paras:
        if not p:
            total += _iv(LH, FLOOR); continue
        w = sum(len(s)/_iv(tbl or CPI, sz) for s, sz in p)
        lines = max(1, -(-int(w*1000)//int(inner*1000)))
        total += lines * max(_iv(LH, sz) for _, sz in p)
    if total > h_in - 0.05:
        print(f"  !! OVERFLOW {label}: {total:.2f}in in {h_in:.2f}in box")
    return total

def shape(oid, page, x, y, w, h, stype="ROUND_RECTANGLE"):
    assert len(oid)>=5, f"object id too short: {oid}"
    return {"createShape":{"objectId":oid,"shapeType":stype,"elementProperties":{
        "pageObjectId":page,
        "size":{"width":{"magnitude":emu(w),"unit":"EMU"},"height":{"magnitude":emu(h),"unit":"EMU"}},
        "transform":{"scaleX":1,"scaleY":1,"translateX":emu(x),"translateY":emu(y),"unit":"EMU"}}}}

def fill(oid, color, outline=None, weight=25400):
    sp = {"shapeBackgroundFill":{"solidFill":{"alpha":1,"color":{"rgbColor":color}}}}
    f = "shapeBackgroundFill.solidFill.color"
    if outline:
        sp["outline"]={"dashStyle":"SOLID","weight":{"magnitude":weight,"unit":"EMU"},
                       "outlineFill":{"solidFill":{"alpha":1,"color":{"rgbColor":outline}}}}
        f += ",outline"
    else:
        sp["outline"]={"propertyState":"NOT_RENDERED"}
        f += ",outline.propertyState"
    return {"updateShapeProperties":{"objectId":oid,"shapeProperties":sp,"fields":f}}

def box(oid, page, x, y, w, h, parts, align=None, fam=None, spacing=None, tbl=None):
    """parts = [(text, size, color, bold)] ; returns request list"""
    fam = fam or BODY_FONT
    for t, size, _, _ in parts:
        assert size >= FLOOR, (
            f"{oid}: {size}pt is below the {FLOOR}pt floor -- {t[:40]!r}")
    reqs = [shape(oid, page, x, y, w, h, "TEXT_BOX")]
    full = "".join(p[0] for p in parts)
    reqs.append({"insertText":{"objectId":oid,"insertionIndex":0,"text":full}})
    i = 0
    for t, size, color, bold in parts:
        reqs.append({"updateTextStyle":{"objectId":oid,
            "textRange":{"type":"FIXED_RANGE","startIndex":i,"endIndex":i+len(t)},
            "style":{"bold":bold,"fontFamily":fam,
                     "fontSize":{"magnitude":size,"unit":"PT"},
                     "foregroundColor":{"opaqueColor":{"rgbColor":color}}},
            "fields":"bold,fontFamily,fontSize,foregroundColor"}})
        i += len(t)
    ps = {}; pf = []
    if align: ps["alignment"]=align; pf.append("alignment")
    if spacing: ps["lineSpacing"]=spacing; pf.append("lineSpacing")
    if ps:
        reqs.append({"updateParagraphStyle":{"objectId":oid,"textRange":{"type":"ALL"},
                     "style":ps,"fields":",".join(pf)}})
    fit([(t,s) for t,s,_,_ in parts], w, h, oid, tbl)
    return reqs

TOP = 1.02   # first content row starts here
BOT = 6.95   # nothing below this
PAD = 0.14   # inset from a card edge to its text

def title(oid, page, text, y=0.42, x=0.6, w=12.13, h=0.54, size=TITLE, col=None):
    """One line at 24pt. Over ~62 chars it wraps and eats the content row,
    so the fit check below is the signal to shorten the sentence."""
    return box(oid,page,x,y,w,h,[(text+"\n",size,col or INK,True)],
               fam=TITLE_FONT, tbl=CPI_TITLE)

def badge(oid, page, num, label, col=RED, txt=None, lab=None, y=0.12):
    """numbered pill + section label, top-left, as in the design"""
    r  = [shape(oid+"p",page,0.6,y,0.50,0.30), fill(oid+"p", col)]
    r += box(oid+"n",page,0.6,y+0.01,0.50,0.31,[(num+"\n",FLOOR,txt or F_WHT,True)],align="CENTER")
    r += box(oid+"l",page,1.20,y+0.01,7.6,0.31,[(label+"\n",FLOOR,lab or GREY,True)])
    return r

def card(oid, page, x, y, w, h, parts, tint=None, outline=None):
    """tinted panel plus its text, inset by PAD on every side"""
    r = [shape(oid+"b",page,x,y,w,h), fill(oid+"b", tint or F_NEUT, outline)]
    r += box(oid,page,x+PAD,y+PAD-0.02,w-2*PAD,h-2*PAD+0.04,parts)
    return r

def dots(oid, page, x=12.06, y=0.44, d=0.085, gap=0.055):
    """the four-dot Google motif, top-right"""
    r=[]
    for i,c in enumerate([BLUE,RED,YELLOW,GREEN]):
        r += [shape(f"{oid}{i}",page,x+i*(d+gap),y,d,d,"ELLIPSE"), fill(f"{oid}{i}",c)]
    return r

def dump(reqs, name):
    s = json.dumps(reqs, separators=(",",":"))
    open(f"/private/tmp/claude-501/-Users-khushibansal-Graduation-Project/c79cbd0a-9d24-48c2-a832-7bb9a63e4037/scratchpad/deck/{name}.json","w").write(s)
    print(f"{name}: {len(reqs)} requests, {len(s)} chars")

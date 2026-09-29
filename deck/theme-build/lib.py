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
    inner = w_in - 0.20
    total = 0.0
    for t, size in parts:
        for line in (t.split("\n")[:-1] if t.endswith("\n") else t.split("\n")):
            n = max(1, -(-len(line)//max(1,int(inner*_iv(tbl or CPI,size)))))
            total += n*_iv(LH,size)
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

def title(oid, page, text, y=0.50, x=0.6, w=12.13, h=0.74, size=21, col=None):
    return box(oid,page,x,y,w,h,[(text+"\n",size,col or INK,True)],
               fam=TITLE_FONT, tbl=CPI_TITLE)

def badge(oid, page, num, label, col=RED, txt=None, lab=None, y=0.20):
    """numbered pill + section label, top-left, as in the design"""
    r  = [shape(oid+"p",page,0.6,y,0.46,0.28), fill(oid+"p", col)]
    r += box(oid+"n",page,0.6,y+0.02,0.46,0.25,[(num+"\n",10,txt or F_WHT,True)],align="CENTER")
    r += box(oid+"l",page,1.17,y+0.02,7.6,0.25,[(label+"\n",10.5,lab or GREY,True)])
    return r

def dots(oid, page, x=12.06, y=0.50, d=0.085, gap=0.055):
    """the four-dot Google motif, top-right"""
    r=[]
    for i,c in enumerate([BLUE,RED,YELLOW,GREEN]):
        r += [shape(f"{oid}{i}",page,x+i*(d+gap),y,d,d,"ELLIPSE"), fill(f"{oid}{i}",c)]
    return r

def dump(reqs, name):
    s = json.dumps(reqs, separators=(",",":"))
    open(f"/private/tmp/claude-501/-Users-khushibansal-Graduation-Project/c79cbd0a-9d24-48c2-a832-7bb9a63e4037/scratchpad/deck/{name}.json","w").write(s)
    print(f"{name}: {len(reqs)} requests, {len(s)} chars")

import json,glob,collections
EMU=914400
# Roboto avg advance ~0.50 em for mixed-case prose; line height 1.20 em
CW, LH = 0.50, 1.20
def cap(w_in,h_in,pt):
    cw = CW*pt/72.0
    lh = LH*pt/72.0
    cols = max(1,int(w_in/cw))
    rows = max(1,int(h_in/lh))
    return cols,rows,cols*rows

rows=[]
for f in sorted(glob.glob('*_final.json')):
    reqs=json.load(open(f))
    box={}   # oid -> (w,h)
    txt=collections.defaultdict(str)
    for r in reqs:
        if 'createShape' in r:
            cs=r['createShape']
            if cs.get('shapeType')=='TEXT_BOX':
                sz=cs['elementProperties']['size']
                box[cs['objectId']]=(sz['width']['magnitude']/EMU, sz['height']['magnitude']/EMU)
        if 'insertText' in r:
            it=r['insertText']; txt[it['objectId']]+=it['text']
    for oid,(w,h) in box.items():
        t=txt.get(oid,'')
        n=len(t.rstrip('\n'))
        if n==0: continue
        # account for hard line breaks: each newline starts a new row
        hard=t.rstrip('\n').count('\n')
        cols,rws,c14=cap(w,h,14)
        # rows needed: sum over paragraphs of ceil(len/cols)
        need=0
        for para in t.rstrip('\n').split('\n'):
            need += max(1,-(-len(para)//cols))
        rows.append((f,oid,round(w,2),round(h,2),n,need,rws,need-rws))

rows.sort(key=lambda r:-r[7])
print(f"{'file':16}{'object':12}{'w':>6}{'h':>6}{'chars':>7}{'need':>6}{'have':>6}{'over':>6}")
bust=0
for f,o,w,h,n,need,have,over in rows:
    if over>0:
        bust+=1
        print(f"{f:16}{o:12}{w:6.2f}{h:6.2f}{n:7}{need:6}{have:6}{over:6}")
print(f"\n{bust} of {len(rows)} text boxes overflow at 14pt")

from lib import *
P="p5"; R=[]
for i in range(2,26): R.append({"deleteObject":{"objectId":f"p5_i{i}"}})
R += title("usr3t",P,"Talking to users broke the review-data story: most people never search. They scroll for a date they have forgotten")

W=2.845; G=0.25; Y=1.34; H=0.92
st=[("74%","scroll the timeline by date"),("61%","had forgotten the very date they were scrolling for"),
    ("48%","ever use search. 29% only ever scroll"),("52%","hit a failed retrieval monthly or more")]
for i,(n,l) in enumerate(st):
    x=0.6+i*(W+G)
    R += [shape(f"usr3s{i}b",P,x,Y,W,H), fill(f"usr3s{i}b",F_NEUT)]
    R += box(f"usr3s{i}",P,x+0.18,Y+0.08,W-0.36,H-0.16,[(n+"  ",20,BLUE,True),(l+"\n",10,GREY,False)])

# personas
PW=5.915; PY=2.42; PH=1.98
pers=[("PERSONA 1  ·  THE DEEP-LIBRARY KEEPER",
  "Four years in, about 75,000 items: camera photos, screenshots, WhatsApp images, downloads. Hits a failed retrieval weekly. Scrolls by date and searches only as a last resort, because search has burned them before. Describes a photo with four cues at once — “date / content of photo / with whom it was / why was it taken”.",
  "“I just wish someone / any agent find it for me what I need”"),
 ("PERSONA 2  ·  THE DOCUMENT KEEPER",
  "Photographs IDs, bills, receipts and tickets as a filing system; 77% of survey respondents do this often. Retrieval is time-pressured and high-stakes: at a counter, before a deadline. Abandons fast and re-creates the artefact rather than keep hunting, so the failure never shows up in telemetry.",
  "P1 gave up after two minutes and re-photographed their PAN card")]
for i,(hd,bd,q) in enumerate(pers):
    x=0.6+i*(PW+0.3)
    R += [shape(f"usr3p{i}b",P,x,PY,PW,PH), fill(f"usr3p{i}b",F_NEUT)]
    R += box(f"usr3p{i}",P,x+0.2,PY+0.14,PW-0.4,PH-0.28,[
      (hd+"\n",11,ORNG,True),(bd+"\n",10.5,INK,False),(q+"\n",10.5,BLUE,True)])

# observed tasks
TW=3.877; TY=4.54; TH=1.84
tk=[("P1  ·  a receipt, 2 years old",
     "Their correct brand name returned the appliance, not the receipt. The vendor name returned nothing. A generic “bill” found it on the third try.","The keyword matters, and it is luck"),
    ("P2  ·  a document, five steps",
     "Recalled a date, scrolled, failed, then used surrounding photos as landmarks to work out their own estimate was a month out, and scrolled again. Never gave the app a clue.","The app was never in the loop"),
    ("P2  ·  a childhood photo, ~20 years",
     "Face search failed: a 20-year-old face does not match the current cluster. Then, unprompted: “a feature to filter pictures based on non-recorded criteria (a picture with child / black and white picture) would certainly help”.","Face recognition breaks with age")]
for i,(hd,bd,tag) in enumerate(tk):
    x=0.6+i*(TW+0.25)
    hot = (i==2)
    R += [shape(f"usr3t{i}b",P,x,TY,TW,TH), fill(f"usr3t{i}b", F_ORNG if hot else F_NEUT)]
    R += box(f"usr3k{i}",P,x+0.2,TY+0.13,TW-0.4,TH-0.26,[
      (hd+"\n",11,INK,True),(bd+"\n",10,GREY,False),(tag+"\n",10,ORNG if hot else BLUE,True)])

R += box("usr3ft",P,0.6,6.5,12.13,0.42,[
  ("Method: contextual interviews with live retrieval tasks on participants’ own libraries, plus a Google Form survey (n=31). P3–P6 in progress. Participants anonymised.\n",9.5,GREY,False)])
dump(R,"s3")

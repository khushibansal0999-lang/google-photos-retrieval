from lib import *
P="p5"; R=[]
for i in range(2,26): R.append({"deleteObject":{"objectId":f"p5_i{i}"}})
R += title("res3t",P,"Four interviews and a survey broke the review-data story: most people never search at all")
R += badge("res3bg",P,"03","User research",YELLOW,txt=INK)
R += dots("res3dt",P)

W=2.845; G=0.25; Y=1.28; H=0.86
st=[("74%","scroll the timeline by date"),("61%","had forgotten the very date they were scrolling for"),
    ("48%","ever use search. 29% only ever scroll"),("52%","hit a failed retrieval monthly or more")]
for i,(n,l) in enumerate(st):
    x=0.6+i*(W+G)
    R += [shape(f"res3s{i}b",P,x,Y,W,H), fill(f"res3s{i}b",F_NEUT)]
    R += box(f"res3s{i}",P,x+0.18,Y+0.06,W-0.36,H-0.12,[(n+"  ",19,BLUE,True),(l+"\n",9.5,GREY,False)])

PW=3.877; PY=2.18; PH=1.90
pers=[("THE DEEP-LIBRARY KEEPER","Four years, about 75,000 items: camera photos, screenshots, WhatsApp images, downloads. Fails weekly. Scrolls by date and searches only as a last resort. Describes a photo with four cues at once.",
       "“I just wish someone / any agent find it for me what I need”"),
      ("THE UTILITY KEEPER","Photographs IDs, bills and receipts as a filing system; 77% of the survey do this often. Time-pressured and high-stakes. Two coping styles: re-create the artefact, or pre-file it somewhere else entirely.",
       "One participant now keeps documents in Drive, not in Photos"),
      ("THE CASUAL ACCUMULATOR","Around 3,000 photos over six years, one account, no system. Hits this rarely, so never builds a workaround, and gives up fastest of the four.",
       "“They eventually do show up, but not when I want em to”")]
for i,(hd,bd,q) in enumerate(pers):
    x=0.6+i*(PW+0.25)
    R += [shape(f"res3p{i}b",P,x,PY,PW,PH), fill(f"res3p{i}b",F_NEUT)]
    R += box(f"res3p{i}",P,x+0.2,PY+0.12,PW-0.4,PH-0.24,[
      (f"PERSONA {i+1}  ·  "+hd+"\n",10,ORNG,True),(bd+"\n",9.5,INK,False),(q+"\n",9.5,BLUE,True)])

CY=4.18; CH=1.88
conv=[("Documents fail for everyone","Three of four participants failed a document task: a PAN card, a recovery-password screenshot, and one who simply reported “given it was a document, I was unable to exactly locate it”. Documents are also the retrievals under the most time pressure.",True),
      ("Face search breaks as libraries deepen","It worked for the participant with 5,000 photos, who found a date-blind photo by face and sorted descending. It failed for the participant with 75,000, because a face from 20 years ago does not match the current cluster.",False),
      ("Four out of four route around the app","Re-photograph the document, file it in Drive instead, or give up and wait for it to surface by accident. None of this appears in telemetry as a failed search.",False)]
for i,(hd,bd,hot) in enumerate(conv):
    x=0.6+i*(PW+0.25)
    R += [shape(f"res3c{i}b",P,x,CY,PW,CH), fill(f"res3c{i}b", F_ORNG if hot else F_NEUT)]
    R += box(f"res3c{i}",P,x+0.2,CY+0.13,PW-0.4,CH-0.26,[
      (hd+"\n",11,ORNG if hot else INK,True),(bd+"\n",10,GREY,False)])

R += box("res3ft",P,0.6,6.18,12.13,0.9,[
  ("Method:",9.5,INK,True),
  ("  live retrieval tasks on participants’ own libraries, plus a Google Form survey (n=31). Four interviews complete, P5 and P6 in progress. Participants anonymised.\n",9.5,GREY,False),
  ("Hypothesis dropped:",9.5,ORNG,True),
  ("  multi-account fragmentation is 0 for 4. Every participant with several accounts said it has never made a photo harder to find, so it is out of the deck rather than presented as a theme on one data point.\n",9.5,GREY,False)])
dump(R,"s3b")

from lib import *
P="p5"; R=[]
R += title("res3t",P,"Most people never search. They scroll, and forget the date")
R += badge("res3bg",P,"03","User research",YELLOW,txt=INK)
R += dots("res3dt",P)

W=2.845; G=0.25; Y=TOP; H=0.80
st=[("74%","scroll by date"),("61%","forgot the date they were scrolling to"),
    ("48%","ever use search"),("52%","fail to find a photo monthly or more")]
for i,(n,l) in enumerate(st):
    R += card(f"res3s{i}",P,0.6+i*(W+G),Y,W,H,
        [(n+"  ",FLOOR,BLUE,True),(l+"\n",FLOOR,GREY,False)],F_NEUT)

PW=3.877; PY=1.90; PH=1.78
pers=[("THE BIG LIBRARY","Four years, 75,000 items. Fails weekly. Scrolls first, searches last.",
       "“I just wish any agent could find what I need”"),
      ("THE PAPERWORK KEEPER","Photographs IDs, bills and receipts instead of filing them. 77% do this.",
       "One now keeps documents in Drive, not Photos"),
      ("THE CASUAL ONE","3,000 photos, six years, no system. Hits this rarely, so gives up fastest.",
       "“They show up, but not when I want em to”")]
for i,(hd,bd,q) in enumerate(pers):
    R += card(f"res3p{i}",P,0.6+i*(PW+0.25),PY,PW,PH,
        [(hd+"\n",FLOOR,ORNG,True),(bd+"\n",FLOOR,INK,False),(q+"\n",FLOOR,BLUE,True)],F_NEUT)

CY=3.76; CH=1.50
conv=[("Paperwork fails for everyone","Three of four could not find a document they had photographed: an ID card, a password screenshot, a bill.",True),
      ("Face search fails as libraries grow","It worked at 5,000 photos and failed at 75,000: an old face no longer matches the person today.",False),
      ("All four work around the app","Take the photo again, file it in Drive, or wait and hope. None of this shows up as a failed search.",False)]
for i,(hd,bd,hot) in enumerate(conv):
    R += card(f"res3c{i}",P,0.6+i*(PW+0.25),CY,PW,CH,
        [(hd+"\n",FLOOR,ORNG if hot else INK,True),(bd+"\n",FLOOR,GREY,False)],
        F_ORNG if hot else F_NEUT)

R += box("res3ft",P,0.6,5.36,12.13,1.20,[
  ("How we ran it:",FLOOR,INK,True),
  ("  we gave people real retrieval tasks on their own libraries and watched, plus a survey of 31. Four interviews done, two more running. Names removed.\n",FLOOR,GREY,False),
  ("One idea we dropped:",FLOOR,ORNG,True),
  ("  we expected juggling several Google accounts to hurt. Nobody said it did. Out, rather than kept on one data point.\n",FLOOR,GREY,False)])
dump(R,"s3b")

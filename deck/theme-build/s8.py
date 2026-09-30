from lib import *
P="p9"; R=[]
R += title("mvp8t",P,"One box, a visible reading, one question when it matters")
R += badge("mvp8bg",P,"08","MVP and testing",GREEN)
R += dots("mvp8dt",P)
R += [shape("mvp8bdb",P,9.13,0.08,3.60,0.38), fill("mvp8bdb",F_ORNG,RED,12700)]
R += box("mvp8bd",P,9.13,0.11,3.60,0.32,[("STILL TO COME: MVP IN BUILD\n",FLOOR,ORNG,True)],align="CENTER")

W=3.877; G=0.25; Y=TOP; H=2.02
fl=[("FLOW 1  Several clues at once",
  "“restaurant bill, dinner with friends, about a year ago” becomes tags you can edit, and results come back saying why each one matched.",False),
 ("FLOW 2  The question  ← the one to watch",
  "“bill from last august”. The app sees photos in two different Augusts and asks: 2025 or 2026? One tap. This is the failure from our test, fixed in one turn.",True),
 ("FLOW 3  The near miss",
  "Nothing matches confidently. Instead of an empty screen: the closest few, plus one question about something nobody thinks to type — a child in frame, black and white, a document.",False)]
for i,(hd,bd,sel) in enumerate(fl):
    R += card(f"mvp8f{i}",P,0.6+i*(W+G),Y,W,H,
      [(hd+"\n",FLOOR,BLUE if sel else INK,True),(bd+"\n",FLOOR,GREY,False)],
      F_BLUE if sel else F_NEUT, O_BLUE if sel else None)

R += card("mvp8td",P,0.6,3.14,12.13,1.04,[
  ("How we will test it, decided before building:",FLOOR,INK,True),
  ("  three people from the interviews, each given their own real task from their own session. They try it in Google Photos first, then in the MVP. It works if at least two of three find it in fewer tries, and nobody asks for the plain grid back.\n",FLOOR,GREY,False)],F_NEUT)

TY=4.28; TH=1.26
for i in range(3):
    R += card(f"mvp8u{i}",P,0.6+i*(W+G),TY,W,TH,[
      (f"TESTER {i+1}\n",FLOOR,ORNG,True),
      ("Photos: tries / time / found?\nMVP: tries / time / found?\nWhat they said: …\n",FLOOR,GREY,False)],F_NEUT)

R += box("mvp8ft",P,0.6,5.64,12.13,0.96,[
  ("The demo library:",FLOOR,INK,True),
  ("  about 120 made-up items carrying the real failures from our research — a bill in a month that could be either year, an ID card, a password screenshot, childhood photos in black and white. Built with Python, Gemini and Streamlit Cloud, at no cost.\n",FLOOR,GREY,False)])
dump(R,"s8")

from lib import *
P="p9"; R=[]
for i in range(2,19): R.append({"deleteObject":{"objectId":f"p9_i{i}"}})

R += [shape("mvp8bg",P,9.98,0.10,2.75,0.34), fill("mvp8bg",{"red":1,"green":0.94509804,"blue":0.9098039},O_ORNG,12700)]
R += box("mvp8bd",P,10.06,0.13,2.6,0.30,[("TO COMPLETE: MVP in build\n",10,ORNG,True)],align="CENTER")

R += title("mvp8t",P,"The MVP: one box, an interpretation you can see, and one question only when it matters")
R += badge("mvp8bg",P,"08","MVP and user testing",GREEN)
R += dots("mvp8dt",P)

W=3.877; G=0.25; Y=1.28; H=2.22
flows=[("FLOW 1","Several cues at once",
  "“restaurant bill, dinner with friends, around a year ago” becomes chips: receipt · group · restaurant · about a year ago?  Ranked candidates come back, each saying why it matched.",False),
 ("FLOW 2","The ambiguity turn",
  "“bill from last august”. The app sees photos in two different Augusts and asks one question: 2025 or 2026? One tap resolves it. This is the control-test failure, fixed in a single turn.",True),
 ("FLOW 3","The near miss",
  "Nothing comes back with confidence. Instead of an empty grid: the closest candidates, plus one narrowing question drawn from attributes nobody recorded — a child in frame, black and white, a document.",False)]
for i,(lb,hd,bd,sel) in enumerate(flows):
    x=0.6+i*(W+G)
    R += [shape(f"mvp8f{i}b",P,x,Y,W,H), fill(f"mvp8f{i}b", F_BLUE if sel else F_NEUT, O_BLUE if sel else None)]
    R += box(f"mvp8f{i}",P,x+0.2,Y+0.13,W-0.4,H-0.26,[
      (lb+("   ← the money demo" if sel else "")+"\n",8.5,ORNG,True),
      (hd+"\n",12,BLUE if sel else INK,True),
      (bd+"\n",10,GREY,False)])

R += [shape("mvp8tdb",P,0.6,3.62,12.13,0.88), fill("mvp8tdb",F_NEUT)]
R += box("mvp8td",P,0.8,3.70,11.73,0.72,[
  ("Test design, fixed before building:",10.5,INK,True),
  ("  three users from the interview pool, each given their own real task from their own session. They attempt it in Google Photos first, recording attempts and time, then in the MVP. Success was defined in advance: at least two of three find it in fewer attempts, and nobody asks for the plain grid back.\n",10.5,GREY,False)])

TY=4.60; TH=1.62
for i in range(3):
    x=0.6+i*(W+G)
    R += [shape(f"mvp8t{i}b",P,x,TY,W,TH), fill(f"mvp8t{i}b",F_NEUT)]
    R += box(f"mvp8u{i}",P,x+0.2,TY+0.12,W-0.4,TH-0.24,[
      (f"TESTER {i+1}\n",9,ORNG,True),
      ("Task: ",9.5,INK,True),("their own, from their own session\n",9.5,GREY,False),
      ("Google Photos: ",9.5,INK,True),("attempts / time / found?\n",9.5,GREY,False),
      ("MVP: ",9.5,INK,True),("attempts / time / found?\n",9.5,GREY,False),
      ("What they said: ",10,INK,True),("…\n",10,GREY,False)])

R += box("mvp8ft",P,0.6,6.32,12.13,0.86,[
  ("Demo library:",9.5,INK,True),
  ("  about 120 seeded items carrying the real failures from the research, including a bill dated in an ambiguous month, an ID card, a recovery-password screenshot and childhood photos in black and white. The evaluator confirmed AI-generated images are acceptable. Built on Python + Gemini + Streamlit Cloud, with zero AI spend.\n",9.5,GREY,False)])
dump(R,"s8")

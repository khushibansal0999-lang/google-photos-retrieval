from lib import *
P="p8"; R=[]
for o in ["p8_i2","p8_i3","sol8title","sol8c1bx","sol8c1tx","sol8c2bx","sol8c2tx","sol8c3bx",
          "sol8c3tx","sol8d1bx","sol8d1tx","sol8d2bx","sol8d2tx","sol8d3bx","sol8d3tx",
          "sol8size","sol8tens2"]:
    R.append({"deleteObject":{"objectId":o}})

R += title("sol6t",P,"Three ways to enrich the prompt before the app commits to an interpretation")
R += badge("sol6bg",P,"06","Solution options",BLUE)
R += dots("sol6dt",P)

R += box("sol6fr",P,0.6,1.28,12.13,0.42,[
  ("All three attack stage 3,",10.5,INK,True),
  ("  because that is where the controlled test showed retrieval dies. They differ by what the user is actually able to give us.\n",10.5,GREY,False)])

W=3.877; G=0.25; Y=1.70; H=2.86
sols=[("A · THE COMPOSER","for when you can describe it",
  "Your sentence becomes editable cue chips, each with a confidence: sister · night · outdoors · wedding? · date unknown. A question mark means a preference, never a filter. The chips sit above the results as a receipt, so a wrong reading is visible and one tap fixes it.",
  "Reach 6   Impact 9\nConfidence 9   Effort 3","RICE 162",True),
 ("B · THE PROMPTER","for when you do not know what to say",
  "The box stops being blank. The app asks for the cues memory actually keeps, strongest first: who was there, indoors or outdoors, roughly where, what was happening. Every field optional. None of them a date.",
  "Reach 9   Impact 7\nConfidence 5   Effort 4","RICE 79",False),
 ("C · THE ANCHOR","for when you can only point",
  "“It is from the same trip as this one.” Point at any photo you can find and search relative to it: same day, same people, just before or just after. Words optional, and the anchor carries the context the words could not.",
  "Reach 6   Impact 8\nConfidence 8   Effort 5","RICE 77",False)]
for i,(hd,sub,bd,sc,rice,sel) in enumerate(sols):
    x=0.6+i*(W+G)
    R += [shape(f"sol6c{i}b",P,x,Y,W,H), fill(f"sol6c{i}b", F_BLUE if sel else F_NEUT, O_BLUE if sel else None)]
    R += box(f"sol6c{i}",P,x+0.2,Y+0.13,W-0.4,H-0.26,[
      (hd+"\n",13,BLUE if sel else INK,True),
      (sub+"\n\n",10,GREY,False),
      (bd+"\n\n",10,INK,False),
      (sc+"\n",10.5,INK,False),
      (rice+"\n",13,BLUE if sel else GREY,True)])

# how we scored
SY=4.64; SH=0.84; SW=2.845
crit=[("REACH","how many retrieval sessions it can fire in"),
      ("IMPACT","how much it moves a session that would otherwise fail"),
      ("CONFIDENCE","strength of our evidence, not our enthusiasm"),
      ("EFFORT","inverse: build cost against the existing index")]
for i,(h,d) in enumerate(crit):
    x=0.6+i*(SW+0.25)
    R += [shape(f"sol6k{i}b",P,x,SY,SW,SH), fill(f"sol6k{i}b",F_NEUT)]
    R += box(f"sol6k{i}",P,x+0.18,SY+0.1,SW-0.36,SH-0.2,[
      (h+"\n",9,ORNG,True),(d+"\n",9.5,GREY,False)])

R += box("sol6tn",P,0.6,5.56,12.13,1.40,[
  ("Why A wins, and why B is not the answer despite the widest reach.",10.5,INK,True),
  ("  B reaches the 74% who never type anything, which is the largest behaviour in our data, and it still loses. It scores 5 on confidence because no user asked for a form; it came from us and from desk research. A wins on evidence: a controlled test in which only the date phrasing changed, plus three unprompted requests from two participants for exactly this interaction. That is a legitimate reason to go first, and B is named as the next bet rather than dropped.\n",10.5,GREY,False),
  ("Deliberately out of this round:",10.5,ORNG,True),
  ("  the stage-5 recovery loop, which desk research rates the single biggest opportunity and we rate second. The MVP user test is designed to tell us whether that ordering is wrong.\n",10.5,GREY,False)])
dump(R,"s6")

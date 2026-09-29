from lib import *
P="chal7"; R=[]
R += title("chl7t",P,"We attacked all three. Here is what survived")
R += badge("chl7bg",P,"07","Solution selection",RED)
R += dots("chl7dt",P)

# At 14pt three cards give ~32 chars a line, so each card carries the objection
# and the answer only. "What would kill it" lives in the footer kill criteria.
W=3.877; G=0.25; Y=1.15; H=2.85
ch=[("A · THE COMPOSER",
  "A filter drawer with extra steps, and the research says nobody should build one.",
  "The chips come from the user's own sentence, never a menu. A receipt, not a control panel.",True),
 ("B · THE PROMPTER",
  "It is a form. Forms feel like work, and no user asked for one.",
  "True, hence 5 on confidence. Not the default: it appears after a blank result or a long pause.",False),
 ("C · THE ANCHOR",
  "Google already has “more from this day”. This is browsing renamed.",
  "Browsing from an anchor exists. Querying from one does not. P2 did this by hand to fix a date a month out.",False)]
for i,(hd,obj,ans,sel) in enumerate(ch):
    x=0.6+i*(W+G)
    R += [shape(f"chl7c{i}b",P,x,Y,W,H), fill(f"chl7c{i}b", F_BLUE if sel else F_NEUT, O_BLUE if sel else None)]
    R += box(f"chl7c{i}",P,x+0.2,Y+0.14,W-0.4,H-0.28,[
      (hd+"\n",LEAD,BLUE if sel else INK,True),
      ("THE STRONGEST OBJECTION\n",FLOOR,ORNG,True),(obj+"\n",FLOOR,INK,False),
      ("THE ANSWER\n",FLOOR,ORNG,True),(ans+"\n",FLOOR,GREY,False)])

DY=4.12; DH=1.88
R += [shape("chl7db",P,0.6,DY,12.13,DH), fill("chl7db",F_BLUE)]
R += box("chl7d",P,0.8,DY+0.14,11.73,DH-0.28,[
  ("Why A survives all three levels the evaluator scores\n",SUB,BLUE,True),
  ("Does it solve it?",FLOOR,INK,True),
  ("  “bill from last august” returned nothing; “bill from august 2025” returned an instant answer. Only the phrasing changed.  ",FLOOR,GREY,False),
  ("Differentiated?",FLOOR,INK,True),
  ("  Google, Apple and Immich resolve ambiguity silently. ChatGPT and Gemini ask, but cannot see your library.  ",FLOOR,GREY,False),
  ("What stops a copy?",FLOOR,INK,True),
  ("  Copyable in a week. The moat is underneath: judging whether “last August” is ambiguous needs that user's history.\n",FLOOR,GREY,False)])

R += box("chl7ft",P,0.6,6.12,12.13,0.80,[
  ("Sizing:",FLOOR,INK,True),
  ("  273M fail monthly × 82% misread clue ≈ 224M addressable; at a pessimistic one-in-five rescue rate, ~45M more retrievals a month, every figure an estimate.  ",FLOOR,GREY,False),
  ("Kill it if:",FLOOR,ORNG,True),
  ("  questions exceed 0.4 per session, or fewer than 2 of 3 testers beat their own baseline.\n",FLOOR,GREY,False)])
dump(R,"s7")

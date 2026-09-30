from lib import *
P="p8"; R=[]
R += title("sol6t",P,"Three ways to help people say more before we guess")
R += badge("sol6bg",P,"06","Solution options",BLUE)
R += dots("sol6dt",P)

R += box("sol6fr",P,0.6,TOP,12.13,0.30,[
  ("All three attack step 3, where the test showed retrieval dies. They differ by what the person can actually give us.\n",FLOOR,GREY,False)])

W=3.877; G=0.25; Y=1.40; H=2.96
sols=[("A · THE COMPOSER","when you can describe it",
  "Your sentence turns into small editable tags: sister · night · outdoors · wedding? · date unsure. A question mark means a preference, not a filter, and one tap fixes a wrong reading.",
  "Reach 6 · Impact 9 · Confidence 9 · Effort 3","RICE 162",True),
 ("B · THE PROMPTER","when you do not know what to say",
  "The box stops being empty. It asks for what memory actually keeps, strongest first: who was there, indoors or outdoors, roughly where, what was happening. All optional. None of them a date.",
  "Reach 9 · Impact 7 · Confidence 5 · Effort 4","RICE 79",False),
 ("C · THE ANCHOR","when you can only point",
  "“It is from the same trip as this one.” Point at any photo you can find and search around it: same day, same people, just before or after. Words optional.",
  "Reach 6 · Impact 8 · Confidence 8 · Effort 5","RICE 77",False)]
for i,(hd,sub,bd,sc,rice,sel) in enumerate(sols):
    R += card(f"sol6c{i}",P,0.6+i*(W+G),Y,W,H,[
      (hd+"  ",FLOOR,BLUE if sel else INK,True),(sub+"\n",FLOOR,GREY,False),
      (bd+"\n",FLOOR,INK,False),
      (sc+"\n",FLOOR,GREY,False),(rice+"\n",FLOOR,BLUE if sel else GREY,True)],
      F_BLUE if sel else F_NEUT, O_BLUE if sel else None)

SY=4.46; SH=0.78; SW=2.845
crit=[("REACH","how many searches it can fire in"),("IMPACT","how much it moves a failing search"),
      ("CONFIDENCE","how strong our evidence is"),("EFFORT","build cost, inverted")]
for i,(h,d) in enumerate(crit):
    R += card(f"sol6k{i}",P,0.6+i*(SW+0.25),SY,SW,SH,
      [(h+"  ",FLOOR,ORNG,True),(d+"\n",FLOOR,GREY,False)],F_NEUT)

R += box("sol6tn",P,0.6,5.32,12.13,1.62,[
  ("Why A wins, even though B reaches more people.",FLOOR,INK,True),
  ("  B reaches the 74% who never type anything, and it still loses. It scores 5 on confidence because no user asked for a form — the idea came from us. A wins on evidence: a test where only the date wording changed, plus three unprompted asks from two people for exactly this. B is next, not dropped.\n",FLOOR,GREY,False),
  ("Deliberately left out:",FLOOR,ORNG,True),
  ("  fixing the dead end at step 5, which outside research rates first and we rate second. The MVP test is built to tell us if that ordering is wrong.\n",FLOOR,GREY,False)])
dump(R,"s6")

from lib import *
P="risk10"; R=[]
R += title("rsk0t",P,"What could break this, and what we do not yet know")
R += badge("rsk0bg",P,"10","Risks and limits",RED)
R += dots("rsk0dt",P)

W=3.877; G=0.25; Y=TOP; H=2.70
risks=[("A confident wrong answer hurts more than an empty one",
  "People searching again within a day.",
  "Show why each photo matched, and keep the old results alongside. Costs screen space and a slower first load.",True),
 ("The questions turn into an interrogation",
  "More than 0.4 questions per search, or half of them skipped.",
  "Only ask when we are genuinely unsure, once per search. Cases we skip get a wider set instead.",False),
 ("Reading your words needs your history",
  "People opting out, and privacy complaints.",
  "Run on what is already on the phone, so nothing new leaves it. Costs accuracy if you change devices.",False)]
for i,(hd,det,mit,hot) in enumerate(risks):
    R += card(f"rsk0c{i}",P,0.6+i*(W+G),Y,W,H,[
      (hd+"\n",FLOOR,ORNG if hot else INK,True),
      ("THE WARNING SIGN\n",FLOOR,ORNG,True),(det+"\n",FLOOR,GREY,False),
      ("WHAT WE WOULD DO, AND ITS COST\n",FLOOR,ORNG,True),(mit+"\n",FLOOR,INK,False)],
      F_ORNG if hot else F_NEUT)

R += card("rsk0w",P,0.6,3.82,12.13,1.30,[
  ("What this research cannot tell you\n",FLOOR,INK,True),
  ("31 survey replies from people who volunteered. Four interviews, not twelve. The discovery engine reads public posts, so it hears the people annoyed enough to write one. A 120-item demo is not 75,000 photos, and things are easier to find in a small library. The sizing is a rough order of magnitude.\n",FLOOR,GREY,False)],F_NEUT)

R += box("rsk0ft",P,0.6,5.22,12.13,0.80,[
  ("Honestly:",FLOOR,ORNG,True),
  ("  the strongest thing here is one controlled test on one library, and the biggest number comes off a 31-person survey. Everything is sized so it can be proved wrong, rather than sized to impress.\n",FLOOR,GREY,False)])
dump(R,"s10")

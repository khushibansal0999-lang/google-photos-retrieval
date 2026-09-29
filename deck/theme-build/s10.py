from lib import *
P="risk10"; R=[]
R += title("rsk0t",P,"What could break this, and what we cannot yet know")
R += badge("rsk0bg",P,"10","Risks and limitations",RED)
R += dots("rsk0dt",P)

# three risks across. the fourth (a seeded library flatters the result) is a
# limitation of the method, not a risk in the product, so it moves below.
W=3.87; G=0.25; Y=1.18; H=2.90
risks=[("A confident wrong answer costs more trust than a blank one",
  "Re-search within 24 hours.",
  "Show why each result matched, and keep classic results alongside. Costs screen space and a slower first paint.",True),
 ("The clarifying question becomes an interrogation",
  "Over 0.4 questions per session, or a skip rate over 50%.",
  "Fire only below 0.75 confidence, one per session. Cases we skip return a wider set instead.",False),
 ("Interpretation needs history, and history is sensitive",
  "Opt-out rate and privacy complaints.",
  "Run on the existing on-device index, so nothing new leaves the phone. Costs accuracy for users who switch devices.",False)]
for i,(hd,det,mit,hot) in enumerate(risks):
    x=0.6+i*(W+G)
    R += [shape(f"rsk0c{i}b",P,x,Y,W,H), fill(f"rsk0c{i}b", F_ORNG if hot else F_NEUT)]
    R += box(f"rsk0c{i}",P,x+0.18,Y+0.14,W-0.36,H-0.28,[
      (hd+"\n",SUB,ORNG if hot else INK,True),
      ("THE SIGNAL\n",FLOOR,ORNG,True),(det+"\n",FLOOR,GREY,False),
      ("MITIGATION, AND ITS COST\n",FLOOR,ORNG,True),(mit+"\n",FLOOR,INK,False)])

BY=4.28; BH=1.62
R += [shape("rsk0wb",P,0.6,BY,12.13,BH), fill("rsk0wb",F_NEUT)]
R += box("rsk0w",P,0.8,BY+0.14,11.73,BH-0.28,[
  ("What this research cannot tell you\n",SUB,INK,True),
  ("Survey n=31, skewed to engaged users. Four interviews, not twelve. The discovery engine reads public posts, which over-represent the failures loud enough to complain about. A 120-item demo library is not 75,000, and ambiguity is rarer in a small one. Impact sizing is an order-of-magnitude estimate, labelled as one.\n",FLOOR,GREY,False)])

R += box("rsk0ft",P,0.6,6.06,12.13,0.80,[
  ("The honest summary:",FLOOR,ORNG,True),
  ("  the strongest evidence here is one controlled test on one library, and the largest number is an estimate off a 31-person survey. Everything is sized to be falsifiable rather than impressive.\n",FLOOR,GREY,False)])
dump(R,"s10")

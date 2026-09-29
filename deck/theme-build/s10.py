from lib import *
P="risk10"; R=[]
R += title("rsk0t",P,"What could make this fail, what we would watch, and what this research cannot tell you")
R += badge("rsk0bg",P,"10","Risks and limitations",RED)
R += dots("rsk0dt",P)

W=2.845; G=0.25; Y=1.30; H=2.72
risks=[("A confident wrong answer costs more trust than a blank one",
  "Google already lived this. Ask Photos was paused in 2026 after users said it found less than classic search.",
  "Re-search rate within 24 hours.",
  "Show why each result matched and keep classic results alongside. Costs us screen space and a slower first paint.",True),
 ("The clarifying question becomes an interrogation",
  "Confidence scoring treats an unambiguous phrase as ambiguous, so every query gets interrupted.",
  "Questions per session above 0.4, or a skip rate above 50%.",
  "Fire only below 0.75 confidence, hard cap one per session. Costs us some genuinely ambiguous cases, which return a wider set instead.",False),
 ("A seeded demo library flatters the result",
  "120 items is not 75,000. Ambiguity is rarer in a small library, which is what our P2 and P3 contrast showed.",
  "Testers reporting that it felt unrealistic.",
  "Seed from the real interview failures and state the limit on the MVP slide. Costs us the right to claim the result generalises.",False),
 ("Interpretation needs history, and history is sensitive",
  "Judging whether \u201clast August\u201d is ambiguous requires multi-year capture patterns for that person.",
  "Opt-out rate and privacy complaints.",
  "Run on the existing on-device index; nothing new leaves the device. Costs us cross-device accuracy for users who switch phones.",False)]
for i,(hd,why,det,mit,hot) in enumerate(risks):
    x=0.6+i*(W+G)
    R += [shape(f"rsk0c{i}b",P,x,Y,W,H), fill(f"rsk0c{i}b", F_ORNG if hot else F_NEUT)]
    R += box(f"rsk0c{i}",P,x+0.18,Y+0.12,W-0.36,H-0.24,[
      (hd+"\n",10.5,ORNG if hot else INK,True),
      ("WHY IT HAPPENS\n",8,ORNG,True),(why+"\n",9,GREY,False),
      ("THE SIGNAL\n",8,ORNG,True),(det+"\n",9,GREY,False),
      ("MITIGATION, AND WHAT IT COSTS\n",8,ORNG,True),(mit+"\n",9,INK,False)])

BW=5.915; BY=3.95; BH=1.78
wide=[("Limitations of this research",
  "Survey n=31, a convenience sample skewed to engaged users. Four interviews, not twelve. The discovery engine reads public posts, which over-represent failures loud enough to complain about and miss the silent ones entirely, which is the exact bias the survey caught. Impact sizing is an order-of-magnitude estimate and every figure is labelled as one."),
 ("Edge cases the MVP must not break",
  "Shared and group libraries, where “my sister” is ambiguous across accounts. Photos with no usable metadata at all. A user who genuinely does not have the photo: the app must be able to say so, which one participant could not determine for themselves. Non-English cue words. Faces that have aged past their own cluster, which breaks the one AI feature users currently trust.")]
for i,(hd,bd) in enumerate(wide):
    x=0.6+i*(BW+0.3)
    R += [shape(f"rsk0w{i}b",P,x,BY,BW,BH), fill(f"rsk0w{i}b",F_NEUT)]
    R += box(f"rsk0w{i}",P,x+0.2,BY+0.13,BW-0.4,BH-0.26,[
      (hd+"\n",11.5,INK,True),(bd+"\n",10,GREY,False)])

R += box("rsk0ft",P,0.6,5.88,12.13,1.0,[
  ("The honest summary:",10.5,ORNG,True),
  ("  the strongest evidence in this project is a single controlled test on one library, and the largest number in it is an estimate built on a 31-person survey. Everything here is sized to be falsifiable rather than impressive, and the kill criteria are written so that a failed MVP test reads as a result rather than as a failure of the project.\n",10.5,GREY,False)])
dump(R,"s10")

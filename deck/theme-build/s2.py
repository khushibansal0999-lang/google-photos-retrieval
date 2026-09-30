from lib import *
P="p2"; R=[]
OLD=["p2_i%d"%i for i in range(2,28)]
for o in OLD: R.append({"deleteObject":{"objectId":o}})

R += title("kpi2t",P,"Breaking the metric down: four behaviours decide whether a remembered photo is ever found")

# North star
R += [shape("kpi2nsb",P,0.6,1.42,12.13,0.92), fill("kpi2nsb",F_BLUE,O_BLUE)]
R += box("kpi2ns",P,0.8,1.52,11.73,0.74,[
  ("NORTH STAR  ",10.5,BLUE,True),
  ("Vague-memory retrieval success rate\n",13,INK,True),
  ("sessions that end with the photo opened  ÷  sessions where someone set out to find a specific photo at least a year old\n",11.5,GREY,False),
])
# formula strip
R += box("kpi2fx",P,0.6,2.40,12.13,0.48,[
  ("Success rate  =  Expression × Match × Recognition",12,INK,True),
  ("     +  the share of dead sessions that Recovery brings back\n",12,GREY,False),
], align="CENTER")

# four columns
W=2.846; GAP=0.25; Y=2.94; H=2.91
cols=[
 ("1 · EXPRESS","Expression rate","queries carrying at least one cue ÷ retrieval sessions",
  "Describes it from memory instead of scrolling to a date.",
  "One box takes several partial cues at once.",
  "74% scroll, only 48% ever search. 68% hold 2+ cues with nowhere to put them.",False),
 ("2 · MATCH   ← our bet","Match rate","sessions returning a relevant candidate ÷ queries",
  "Gives an approximate time without being punished for it.",
  "Time is a range with a confidence, never a silent hard filter.",
  "82% of failures were a fair clue misread. In the control test only the date phrasing changed.",True),
 ("3 · RECOGNISE","Recognition rate","sessions where the target is opened ÷ sessions with results",
  "Spots the photo in a short list rather than scanning a grid.",
  "Target in the top five, each result saying why it matched.",
  "One honest query did return the bill, buried in about 64 photos.",False),
 ("4 · RECOVER","Recovery rate","dead sessions rescued ÷ sessions with no usable result",
  "Narrows instead of giving up or re-creating the item.",
  "Every miss offers one narrowing question, never an empty grid.",
  "77% needed several tries. Both interviewees routed around the app.",False),
]
for i,(hd,met,defn,beh,out,ev,sel) in enumerate(cols):
    x = 0.6 + i*(W+GAP)
    R += [shape(f"kpi2c{i}b",P,x,Y,W,H),
          fill(f"kpi2c{i}b", F_BLUE if sel else F_NEUT, O_BLUE if sel else None)]
    R += box(f"kpi2c{i}",P,x+0.18,Y+0.14,W-0.36,H-0.28,[
      (hd+"\n",12.5,BLUE if sel else INK,True),
      (met+"\n",11.5,BLUE if sel else INK,True),
      (defn+"\n\n",9.5,GREY,False),
      ("USER BEHAVIOUR\n",8.5,ORNG,True),
      (beh+"\n",10,INK,False),
      ("PRODUCT OUTCOME\n",8.5,ORNG,True),
      (out+"\n",10,INK,False),
      ("WHAT HAPPENS TODAY\n",8.5,ORNG,True),
      (ev+"\n",10,GREY,False),
    ])

# bottom note
R += box("kpi2note",P,0.6,5.90,12.13,1.18,[
  ("A tree, not a funnel.",10.5,INK,True),
  ("  The four rates come from different samples (survey n=31 · 84 tagged failure reports · 2 task interviews · one controlled first-party test) so they are never multiplied together as evidence. They are the four places a session can die, and they agree on where the leak is: everything after the user remembers.\n",10.5,GREY,False),
  ("Counter-metrics:",10.5,ORNG,True),
  ("  clarifying questions per session ≤ 0.4  ·  zero-result rate on descriptive queries  ·  a document re-photographed within 10 minutes of a failed search, the “route around the app” signal.\n",10.5,GREY,False),
])
dump(R,"s2")

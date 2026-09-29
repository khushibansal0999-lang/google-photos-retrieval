from lib import *
P="p2"; R=[]
for o in ["kpi2t","kpi2nsb","kpi2ns","kpi2fx","kpi2c0b","kpi2c0","kpi2c1b","kpi2c1",
          "kpi2c2b","kpi2c2","kpi2c3b","kpi2c3","kpi2note"]:
    R.append({"deleteObject":{"objectId":o}})

R += title("met2t",P,"Breaking the metric down: five stages from memory to match, and three ways the last one ends")
R += badge("met2bg",P,"02","Business metric breakdown",RED)
R += dots("met2dt",P)

R += [shape("met2nb",P,0.6,1.26,12.13,0.72), fill("met2nb",F_BLUE,O_BLUE)]
R += box("met2ns",P,0.8,1.33,11.73,0.60,[
  ("NORTH STAR  ",9.5,BLUE,True),
  ("Vague-memory retrieval success rate  ",12,INK,True),
  ("—  sessions that end with the intended photo opened and used  ÷  sessions hunting a specific photo over a year old\n",10.5,GREY,False)])

W=2.282; G=0.18; Y=2.06; H=2.48
stg=[("1 · REMEMBER","Holds fragments of the moment: who, where, what was in frame, why it was taken.",
      "Cue recall rate","90% recall at least one cue. 68% recall two or more.",False),
     ("2 · EXPRESS","Turns that memory into a prompt, or gives up and scrolls instead.",
      "Expression rate","74% scroll. Only 48% ever search.",False),
     ("3 · UNDERSTAND","The app reads the prompt and decides what each clue means.",
      "Interpretation accuracy","82% of failures: a fair clue misread. “last august” silently became 2026.",True),
     ("4 · RETRIEVE","Fetches against the criteria it believes it understood.",
      "Target-in-top-N recall","Content matching works. “august 2025” returned it instantly.",False),
     ("5 · MATCH","Scans what came back and decides whether any of it is the photo.",
      "Recognition rate","One honest query returned it, buried in about 64 photos.",False)]
for i,(hd,beh,met,ev,sel) in enumerate(stg):
    x=0.6+i*(W+G)
    R += [shape(f"met2s{i}b",P,x,Y,W,H), fill(f"met2s{i}b", F_BLUE if sel else F_NEUT, O_BLUE if sel else None)]
    R += box(f"met2s{i}",P,x+0.16,Y+0.13,W-0.32,H-0.26,[
      (hd+("  ← our bet" if sel else "")+"\n",11,BLUE if sel else INK,True),
      (beh+"\n\n",9,INK,False),
      ("METRIC\n",8,ORNG,True),
      (met+"\n",9.5,BLUE if sel else INK,True),
      (ev+"\n",9,GREY,False)])
    if i<4:
        R += box(f"met2a{i}",P,x+W-0.02,Y+1.02,0.22,0.3,[("→",13,GREY,True)],align="CENTER")

OW=3.877; OY=4.62; OH=1.10
out=[("0 photos","A dead end with no way forward. 77% of users needed several tries.",F_ORNG,ORNG),
     ("Some photos, none of them right","The most useful moment in the whole journey: the user knows why it is wrong. One follow-up question narrows it and the loop repeats.",F_BLUE,BLUE),
     ("The photo, found","Opened and used, in time to matter. This is the north star.",F_NEUT,INK)]
for i,(hd,bd,bg,fg) in enumerate(out):
    x=0.6+i*(OW+0.25)
    R += [shape(f"met2o{i}b",P,x,OY,OW,OH), fill(f"met2o{i}b",bg)]
    R += box(f"met2o{i}",P,x+0.2,OY+0.11,OW-0.4,OH-0.22,[
      (hd+"\n",11.5,fg,True),(bd+"\n",10,GREY,False)])

R += box("met2note",P,0.6,5.80,12.13,1.34,[
  ("Where the biggest prize sits, and an honest disagreement.",10.5,INK,True),
  ("  Desk research puts it at the recovery loop in stage 5, where a near miss gives the most information for the least effort. Our own evidence puts it at stage 3: in a controlled test, changing only the date phrasing flipped total failure into an instant answer. The chosen solution does both, exposing its interpretation before it retrieves and asking one narrowing question after a near miss.\n",10.5,GREY,False),
  ("External corroboration:",10.5,ORNG,True),
  ("  across 83 free-recall photo descriptions, indoor/outdoor appeared 69 times, number of people 64, identity of people 56 and location 54, while exact date proved notably less useful than time of day or broad temporal context.\n",10.5,GREY,False)])
dump(R,"s2b")

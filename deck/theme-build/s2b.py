from lib import *
P="p2"; R=[]
R += title("met2t",P,"Five steps from memory to match. Step three breaks")
R += badge("met2bg",P,"02","Metric breakdown",RED)
R += dots("met2dt",P)

R += card("met2ns",P,0.6,TOP,12.13,0.62,[
  ("THE ONE NUMBER  ",FLOOR,BLUE,True),
  ("Of the times someone hunts a photo over a year old, how often do they end up opening it.\n",FLOOR,INK,False)],F_BLUE,O_BLUE)

RH=0.60; RY=1.76
rows=[("1  REMEMBER","They hold pieces: who, where, what was in it.","90% recall one thing. 68% recall two.",False),
      ("2  EXPRESS","They type something, or give up and scroll.","74% scroll. Only 48% ever search.",False),
      ("3  UNDERSTAND","The app decides what each word means.","82% of failures start here.",True),
      ("4  FETCH","It searches for what it thinks you said.","Works. “august 2025” returned it at once.",False),
      ("5  MATCH","They scan what came back for the photo.","One query returned it, buried in 64.",False)]
for i,(st,beh,ev,hot) in enumerate(rows):
    y=RY+i*(RH+0.06)
    R += [shape(f"met2r{i}b",P,0.6,y,12.13,RH), fill(f"met2r{i}b", F_ORNG if hot else F_NEUT)]
    R += box(f"met2r{i}a",P,0.74,y+0.13,2.30,0.36,[(st+"\n",FLOOR,ORNG if hot else INK,True)])
    R += box(f"met2r{i}b2",P,3.10,y+0.13,4.90,0.36,[(beh+"\n",FLOOR,GREY,False)])
    R += box(f"met2r{i}c",P,8.10,y+0.13,4.50,0.36,[(ev+"\n",FLOOR,ORNG if hot else BLUE,True)])

OY=5.10; OH=0.80; OW=3.877
out=[("Nothing came back","A dead end. 77% needed several tries.",F_ORNG,ORNG),
     ("Some, none right","The best moment: they know why.",F_BLUE,BLUE),
     ("Found it","Opened, in time to matter.",F_NEUT,INK)]
for i,(hd,bd,bg,fg) in enumerate(out):
    R += card(f"met2o{i}",P,0.6+i*(OW+0.25),OY,OW,OH,
        [(hd+"  ",FLOOR,fg,True),(bd+"\n",FLOOR,GREY,False)],bg)

R += box("met2note",P,0.6,5.98,12.13,0.54,[
  ("An honest disagreement:",FLOOR,ORNG,True),
  ("  outside research says step 5 is the bigger prize. Our own test says step 3. The MVP test will settle it.\n",FLOOR,GREY,False)])
dump(R,"s2b")

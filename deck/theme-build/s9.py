from lib import *
P="p10"; R=[]
R += title("mtr9t",P,"Every measure: formula, target, and the data it needs")
R += badge("mtr9bg",P,"09","Success metrics",BLUE)
R += dots("mtr9dt",P)

cols=[(0.74,2.40),(3.24,4.30),(7.64,1.30),(9.04,3.60)]
hdr=["MEASURE","HOW IT IS WORKED OUT","TARGET","DATA WE WOULD NEED"]
for c,(x,w) in enumerate(cols):
    R += box(f"mtr9h{c}",P,x,TOP,w,0.30,[(hdr[c]+"\n",FLOOR,ORNG,True)])

RH=0.76; RY=1.36
rows=[("The one number","photos found ÷ hunts for something over a year old","+15pts","hunt started, photo opened, how old it was",False),
 ("People who type something","searches with a clue in them ÷ all hunts","48→65%","what was typed, how many clues",False),
 ("Clues read correctly","clues kept loose ÷ clues that were vague","95%+","how each clue was read, and whether it filtered",True),
 ("Photo spotted in results","photo opened ÷ searches that returned something","70%+","what was shown, in what order, what was opened",False),
 ("Dead ends rescued","hunts saved ÷ hunts that returned nothing","30%+","empty result, question offered, question answered",False),
 ("Questions per search","questions asked ÷ hunts   (a limit, not a goal)","0.4 or less","question shown, answered, skipped",False)]
for i,(m,f,t,d,hot) in enumerate(rows):
    y=RY+i*(RH+0.02)
    R += [shape(f"mtr9b{i}",P,0.6,y,12.13,RH), fill(f"mtr9b{i}", F_ORNG if hot else (F_NEUT if i%2==0 else F_WHT))]
    vals=[m,f,t,d]
    for c,(x,w) in enumerate(cols):
        bold = (c==0 or c==2)
        col = (ORNG if hot else (INK if c==0 else BLUE)) if bold else GREY
        R += box(f"mtr9r{i}c{c}",P,x,y+0.10,w,0.56,[(vals[c]+"\n",FLOOR,col,bold)])

R += box("mtr9ft",P,0.6,6.12,12.13,0.82,[
  ("How to read this:",FLOOR,INK,True),
  ("  the first line is the one that matters on its own. “Clues read correctly” is what our fix moves directly, and the only one you cannot game by returning more photos.  ",FLOOR,GREY,False),
  ("None of it is built yet —",FLOOR,ORNG,True),
  ("  targets are set against the MVP test, not Google's real numbers, which we do not have.\n",FLOOR,GREY,False)])
dump(R,"s9")

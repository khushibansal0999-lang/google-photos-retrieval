from lib import *
P="p7"; R=[]
for o in ["cv7title","cv7navy","cv7prob","cv7whobx","cv7whoh","cv7whob","cv7qbox","cv7query",
          "cv7whyseg","cv7knowbx","cv7knowh","cv7evid","cv7nowbx","cv7nowh","cv7nowb",
          "cv7sizebx","cv7sizeh","cv7chain","cv7valu","cv7valuh","cv7valub","cv7valb",
          "cv7valbh","cv7valbb"]:
    R.append({"deleteObject":{"objectId":o}})

R += title("seg4t",P,"The segment is defined by library depth and elapsed time, not by demographics")
R += badge("seg4bg",P,"04","Target segment and sizing",GREEN)
R += dots("seg4dt",P)

R += [shape("seg4qb",P,0.6,1.28,5.20,2.28), fill("seg4qb",F_BLUE,O_BLUE)]
R += box("seg4q",P,0.8,1.40,4.80,2.04,[
  ("DEFINED AS A QUERY AN ANALYST COULD ACTUALLY RUN\n",8.5,BLUE,True),
  ("account_age ≥ 3 years\nAND library_size ≥ 2,000 items\nAND utility_share ≥ 15% of the last 12 months\nAND ≥ 1 retrieval attempt on an item older\n        than 365 days, in the last 30 days\n",11,INK,True)])

R += [shape("seg4wb",P,6.05,1.28,6.68,2.28), fill("seg4wb",F_NEUT)]
R += box("seg4w",P,6.25,1.40,6.28,2.04,[
  ("WHY THIS SEGMENT AND NOT A BROADER ONE\n",8.5,ORNG,True),
  ("Vague memory is a function of library depth and elapsed time. Someone with 400 recent photos scrolls and finds it. The problem only exists once the library outgrows recall, which is also the point at which the user is most invested and most likely to be paying for storage.\n\n",10.5,INK,False),
  ("Our own interviews carry the proof.",10.5,BLUE,True),
  ("  Face search found a date-blind photo in a 5,000-item library and failed on the same task in a 75,000-item one. The capability does not degrade with the feature. It degrades with the library.\n",10.5,GREY,False)])

SW=2.266; SY=3.70; SH=1.32
chain=[("1.5B","Google Photos monthly users, from Google’s own 10th-anniversary milestone, May 2025",False),
 ("× 35%","with deep, mixed libraries. Our survey said 68%; halved for sample bias",False),
 ("= 525M","the addressable segment",False),
 ("× 52%","hit a failed retrieval monthly or more often (survey)",False),
 ("= 273M","users failing to find a photo every single month",True)]
for i,(n,d,hot) in enumerate(chain):
    x=0.6+i*(SW+0.2)
    tint,acc,txt = CYCLE[i % len(CYCLE)]
    R += [shape(f"seg4s{i}b",P,x,SY,SW,SH), fill(f"seg4s{i}b",tint)]
    R += box(f"seg4s{i}",P,x+0.16,SY+0.12,SW-0.32,SH-0.24,[
      (n+"\n",17,F_WHT if i==4 else txt,True),(d+"\n",8.5,F_NEUT if i==4 else GREY,False)])

BW=5.915
R += [shape("seg4hb",P,0.6,5.18,BW,1.02), fill("seg4hb",F_BLUE)]
R += box("seg4h",P,0.8,5.28,BW-0.4,0.82,[
  ("≈ 96M high-stakes failures a month",12,BLUE,True),
  ("   35% of those who fail say it sometimes really matters.\n",10,GREY,False)])

R += [shape("seg4xb",P,6.81,5.18,BW,1.02), fill("seg4xb",F_NEUT)]
R += box("seg4x",P,7.01,5.28,BW-0.4,0.82,[
  ("Deliberately outside the segment\n",11,INK,True),
  ("Under three years or under 2,000 items: they scroll and they find it. Also out, anyone hunting a photo they never actually took.\n",10,GREY,False)])

R += box("seg4ft",P,0.6,6.32,12.13,0.72,[
  ("Every figure is an estimate and labelled as one.",9.5,ORNG,True),
  ("  The survey is a 31-person convenience sample, so the segment share is discounted by half. The purpose is order of magnitude, not precision: even at a tenth of this, the affected population is larger than most products ever reach.\n",9.5,GREY,False)])
dump(R,"s4")

from lib import *
P="p7"; R=[]
R += title("seg4t",P,"Who this is for: big libraries and old photos, not an age")
R += badge("seg4bg",P,"04","Target segment and size",GREEN)
R += dots("seg4dt",P)

R += card("seg4q",P,0.6,TOP,5.20,2.00,[
  ("WHO COUNTS, AS A QUERY YOU COULD ACTUALLY RUN\n",FLOOR,BLUE,True),
  ("Account 3 years or older\nAt least 2,000 items\nAt least 15% of them paperwork\nTried to find something over a year old, in the last month\n",FLOOR,INK,False)],F_BLUE,O_BLUE)

R += card("seg4w",P,6.05,TOP,6.68,2.00,[
  ("WHY NOT EVERYONE\n",FLOOR,ORNG,True),
  ("Forgetting is a function of how much you have and how long ago it was. Someone with 400 recent photos just scrolls and finds it. The problem starts when the library outgrows memory, which is also when people are paying for storage.\n",FLOOR,INK,False),
  ("Our interviews show it: ",FLOOR,BLUE,True),
  ("face search found a date-blind photo in a 5,000-item library and failed the same task at 75,000.\n",FLOOR,GREY,False)],F_NEUT)

SW=2.266; SY=3.12; SH=1.02
chain=[("1.5B","people use Google Photos each month",False),
 ("× 35%","have big, mixed libraries",False),
 ("= 525M","in this group",False),
 ("× 52%","fail to find a photo monthly",False),
 ("= 273M","people failing every month",True)]
for i,(n,d,hot) in enumerate(chain):
    tint,acc,txt = CYCLE[i % len(CYCLE)]
    R += card(f"seg4s{i}",P,0.6+i*(SW+0.2),SY,SW,SH,
      [(n+"\n",FLOOR,F_WHT if i==4 else txt,True),(d+"\n",FLOOR,F_NEUT if i==4 else GREY,False)],tint)

BW=5.915; BY=4.24
R += card("seg4h",P,0.6,BY,BW,0.78,[
  ("About 96M of those really matter  ",FLOOR,BLUE,True),
  ("— 35% of people who fail say it sometimes genuinely counts.\n",FLOOR,GREY,False)],F_BLUE)
R += card("seg4x",P,6.81,BY,BW,0.78,[
  ("Who we are not building for  ",FLOOR,INK,True),
  ("— under three years or under 2,000 items. They scroll and they find it.\n",FLOOR,GREY,False)],F_NEUT)

R += box("seg4ft",P,0.6,5.16,12.13,0.80,[
  ("These are estimates, and we say so.",FLOOR,ORNG,True),
  ("  The survey is 31 people who volunteered, so we halved the share it suggested. The point is the order of magnitude, not the exact number: even a tenth of this is a lot of people.\n",FLOOR,GREY,False)])
dump(R,"s4")

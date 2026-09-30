from lib import *
P="chal7"; R=[]
R += title("chl7t",P,"We attacked all three. Here is what survived")
R += badge("chl7bg",P,"07","Choosing one",RED)
R += dots("chl7dt",P)

W=3.877; G=0.25; Y=TOP; H=2.46
ch=[("A · THE COMPOSER",
  "A filter drawer with extra steps, and the research says nobody should build one.",
  "The tags come from the person's own words, never a menu. A receipt, not a control panel.",True),
 ("B · THE PROMPTER",
  "It is a form. Forms feel like work, and nobody asked for one.",
  "True, which is why it scores 5 on confidence. It only shows up after a blank result or a long pause.",False),
 ("C · THE ANCHOR",
  "Google already has “more from this day”. This is browsing renamed.",
  "Browsing from a photo exists. Searching from one does not. P2 did this by hand to fix a date a month out.",False)]
for i,(hd,obj,ans,sel) in enumerate(ch):
    R += card(f"chl7c{i}",P,0.6+i*(W+G),Y,W,H,[
      (hd+"\n",FLOOR,BLUE if sel else INK,True),
      ("THE BEST ARGUMENT AGAINST\n",FLOOR,ORNG,True),(obj+"\n",FLOOR,INK,False),
      ("OUR ANSWER\n",FLOOR,ORNG,True),(ans+"\n",FLOOR,GREY,False)],
      F_BLUE if sel else F_NEUT, O_BLUE if sel else None)

R += card("chl7d",P,0.6,3.58,12.13,1.72,[
  ("Why A holds up on all three things the brief asks about\n",FLOOR,BLUE,True),
  ("Does it solve it?",FLOOR,INK,True),
  ("  “bill from last august” returned nothing; “bill from august 2025” returned it at once. Only the wording changed.  ",FLOOR,GREY,False),
  ("Is it different?",FLOOR,INK,True),
  ("  Google, Apple and Immich all guess silently. ChatGPT and Gemini ask, but cannot see your photos.  ",FLOOR,GREY,False),
  ("What stops a copy?",FLOOR,INK,True),
  ("  The screen is copyable in a week. The hard part is knowing whether “last August” is ambiguous for you, which needs your own history.\n",FLOOR,GREY,False)],F_BLUE)

R += box("chl7ft",P,0.6,5.42,12.13,1.30,[
  ("How big:",FLOOR,INK,True),
  ("  273M fail monthly, 82% of those on a misread clue, so about 224M could be helped. If we rescue one in five, that is roughly 45M more photos found a month. Estimates, not measurements.\n",FLOOR,GREY,False),
  ("Drop the whole idea if:",FLOOR,ORNG,True),
  ("  we ask more than 0.4 questions per search, or fewer than 2 of 3 testers do better than they did on their own.\n",FLOOR,GREY,False)])
dump(R,"s7")

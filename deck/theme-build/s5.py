from lib import *
P="p6"; R=[]
R += title("root5t",P,"We reproduced it: the app guesses the date, and says nothing")
R += badge("root5bg",P,"05","Root cause",RED)
R += dots("root5dt",P)

# The four screenshots on this page were placed by hand (h542cb...*). They are
# never deleted and never moved; captions are aligned to where they actually sit.
IMG_X=[0.60, 3.547, 6.493, 9.438]; IMG_W=2.62
shots=[("“bill from last august”","FAILED — got Aug 2026",ORNG),
 ("“… last august at one8”","FAILED — venue hurt",ORNG),
 ("“bill from august 2025”","FOUND at once. Control.",BLUE),
 ("“… around a year ago”","FOUND, buried in 64",INK)]
for i,(q,verdict,col) in enumerate(shots):
    R += box(f"root5cap{i}",P,IMG_X[i],4.00,IMG_W,0.56,[
      (q+"\n",FLOOR,INK,True),(verdict+"\n",FLOOR,col,True)])

R += card("root5c",P,0.6,4.64,12.13,1.10,[
  ("Same photo. Same word, “bill”. Only the date wording changed.  ",FLOOR,INK,True),
  ("“Last August” was read as August 2026 and used as a hard filter; the bill was from August 2025. Reading the photo was never the problem — it could list the dishes. A fifth try, “bill from dinner last year”, worked, because “last year” cannot be misread.\n",FLOOR,GREY,False)],F_BLUE,O_BLUE)

R += box("root5ft",P,0.6,5.82,12.13,1.02,[
  ("Three ways people say when, and the middle one is the trap:",FLOOR,ORNG,True),
  ("  an exact date becomes an exact filter and works  ·  “last August” gets quietly pinned to one year and fails  ·  an openly vague phrase becomes a wide range, and works.\n",FLOOR,GREY,False),
  ("Tested on the live app with a control, 28 Sep 2026. Screenshots cropped to the reply text only. Full log in the research files.\n",FLOOR,GREY,False)])
dump(R,"s5")

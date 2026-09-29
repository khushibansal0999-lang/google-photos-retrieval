from lib import *
P="p6"; R=[]
for i in range(2,27): R.append({"deleteObject":{"objectId":f"p6_i{i}"}})
DARK={"red":0.09,"green":0.071,"blue":0.047}

R += title("root5t",P,"Root cause, reproduced on the live product: the app silently guesses the one thing users are least sure about")
R += badge("root5bg",P,"05","Root cause",RED)
R += dots("root5dt",P)

W=2.845; G=0.25; Y=1.30; FH=2.70
shots=[("q1_last_august_failed","“bill from last august”","✕  FAILED, then showed photos from August 2026",ORNG),
 ("q2_added_venue_failed","“… last august at one8”","✕  FAILED. Adding the correct venue returned less",ORNG),
 ("q4_august2025_control","“bill from august 2025”  ← control","✓  INSTANT. Only the date phrasing changed",BLUE),
 ("q5_around_a_year_ago","“… around a year ago”","⚠  FOUND, then buried in about 64 photos",INK)]
for i,(fn,q,verdict,col) in enumerate(shots):
    x=0.6+i*(W+G)
    R += [shape(f"root5f{i}",P,x,Y,W,FH), fill(f"root5f{i}",DARK)]
    R += box(f"root5cap{i}",P,x,Y+FH+0.06,W,0.66,[
      (q+"\n",10,INK,True),(verdict+"\n",9.5,col,True)])

R += [shape("root5cb",P,0.6,4.78,12.13,1.22), fill("root5cb",F_BLUE,O_BLUE)]
R += box("root5c",P,0.8,4.88,11.73,1.02,[
  ("Same photo. Same content word, “bill”. Only the date phrasing changed.",11.5,INK,True),
  ("  “Last August” was silently read as August 2026 and turned into a hard filter; the bill was from August 2025. Content matching was never broken — the app could read that bill down to the individual dish. A fifth query, “bill receipt of dinner last year”, also succeeded, because “last year” is unambiguous. ",11,GREY,False),
  ("Being honestly vague beat being confidently approximate.\n",11,BLUE,True)])

R += box("root5ft",P,0.6,6.10,12.13,0.78,[
  ("Three time behaviours, and the middle one is the trap:",9.5,ORNG,True),
  ("  explicit → exact filter, works  ·  ambiguous → silently resolved then hard-filtered, worst case  ·  openly vague → loose range, works but noisy.\n",9.5,GREY,False),
  ("First-party test with a control, 28 Sep 2026. Screenshots cropped to the assistant’s response text only; no personal photos published. Full log in the research repo.\n",9.5,GREY,False)])
dump(R,"s5")

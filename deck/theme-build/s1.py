from lib import *
P="p3"; R=[]
R += title("eng1t",P,"6,551 public posts, counted: one failure dominates")
R += badge("eng1bg",P,"01","AI discovery engine",BLUE)
R += dots("eng1dt",P)

W=2.25; G=0.22; Y=TOP; H=0.78
steps=[("1 COLLECT","6,551 posts"),("2 FILTER","1,196 kept"),("3 READ","15 fields each"),
       ("4 SORT","84 real cases"),("5 COMPARE","live tool")]
for i,(hd,met) in enumerate(steps):
    tint,acc,txt = CYCLE[i % len(CYCLE)]
    R += card(f"eng1s{i}",P,0.6+i*(W+G),Y,W,H,
        [(hd+"\n",FLOOR,txt,True),(met+"\n",FLOOR,F_WHT if i==4 else GREY,False)],tint)

R += box("eng1pipe",P,0.6,1.88,12.13,1.04,[
  ("How it works:",FLOOR,INK,True),
  ("  Reddit, Play Store and App Store posts from five countries. A keyword filter drops storage and billing complaints before any AI runs. Gemini then pulls the same 15 facts out of every post — what the photo was, what the person remembered, what they had forgotten, where the search broke, what they did instead — and a second pass separates real memory failures from bug reports.\n",FLOOR,GREY,False)])

Y2=2.96; H2=1.10; W2=2.845; G2=0.25
stats=[("82%","of failures were a fair clue the app read wrong",True),
       ("3 of 84","could not say what they were looking for",False),
       ("19","remembered words printed in the photo, and still missed",False),
       ("16","had forgotten only one thing: roughly when",False)]
for i,(n,lb,hot) in enumerate(stats):
    R += card(f"eng1f{i}",P,0.6+i*(W2+G2),Y2,W2,H2,
        [(n+"  ",FLOOR,ORNG if hot else BLUE,True),(lb+"\n",FLOOR,GREY,False)],
        F_ORNG if hot else F_NEUT)

R += box("eng1why",P,0.6,4.14,12.13,0.78,[
  ("Why this is not just review-reading:",FLOOR,INK,True),
  ("  each post is tagged to the point in the journey where it broke, so the failures can be counted and sliced by photo type, by what the person remembered, and by what they did next. Every number in this deck traces back to a quote.\n",FLOOR,GREY,False)])

Y3=5.00; H3=0.86; W3=3.877; G3=0.25
links=[("DISCOVERY ENGINE","Live and testable",True),("MVP","Link added on submission",False),
       ("RESEARCH FILES","Survey, interviews, full logs",False)]
for i,(hd,sub,hot) in enumerate(links):
    R += card(f"eng1l{i}",P,0.6+i*(W3+G3),Y3,W3,H3,
        [(hd+"\n",FLOOR,BLUE if hot else GREY,True),(sub+"\n",FLOOR,INK,False)],
        F_BLUE if hot else F_NEUT, O_BLUE if hot else None)

R += box("eng1ft",P,0.6,5.94,12.13,0.50,[
  ("Free tiers only: open-source scrapers → Python → Gemini → Streamlit Cloud. No spend.\n",FLOOR,GREY,False)])
dump(R,"s1")

from lib import *
P="p3"; R=[]
for i in range(2,36): R.append({"deleteObject":{"objectId":f"p3_i{i}"}})

R += title("eng1t",P,"An AI discovery engine turned 6,551 public posts into counted evidence, and named one dominant failure")
R += badge("eng1bg",P,"01","AI-powered discovery engine",BLUE)
R += dots("eng1dt",P)

# pipeline
W=2.25; G=0.22; Y=1.36; H=1.46
steps=[("1  Collect","6,551 posts","Reddit 2,002 · Play Store 3,249 · App Store 1,300 across US, IN, GB, CA, AU"),
       ("2  Filter","1,196 kept","A keyword gate drops storage, billing and praise-only posts before any AI spend"),
       ("3  Extract","15-field schema","Gemini structured output per post: photo type, cues held vs lost, failure stage, workaround, quote"),
       ("4  Classify","84 core cases","A second pass splits true vague-memory failures from UI regressions (95) and data loss (28)"),
       ("5  Compare","live tool","Cross-tab any segment, then ask a question and get an answer grounded in cited quotes")]
for i,(hd,met,d) in enumerate(steps):
    x=0.6+i*(W+G)
    tint,acc,txt = CYCLE[i % len(CYCLE)]
    R += [shape(f"eng1s{i}b",P,x,Y,W,H), fill(f"eng1s{i}b",tint)]
    R += box(f"eng1s{i}",P,x+0.16,Y+0.12,W-0.32,H-0.24,[
        (hd+"\n",12,txt,True),(met+"\n",10.5,F_WHT if i==4 else INK,True),(d+"\n",8.5,F_NEUT if i==4 else GREY,False)])

# findings
Y2=2.98; H2=1.5; W2=2.845; G2=0.25
stats=[("82%","of the 84 core failures were a fair clue the app misread",True),
       ("3","of 84 could not describe what they wanted. Expression is not the bottleneck",False),
       ("19","remembered words printed in the photo. None had forgotten them, and search still missed",False),
       ("16","had lost only one thing: roughly when. The most-forgotten cue is the one both paths need",False)]
for i,(n,lb,hot) in enumerate(stats):
    x=0.6+i*(W2+G2)
    R += [shape(f"eng1f{i}b",P,x,Y2,W2,H2), fill(f"eng1f{i}b", F_ORNG if hot else F_NEUT)]
    R += box(f"eng1f{i}",P,x+0.18,Y2+0.12,W2-0.36,H2-0.24,[
        (n+"\n",30,ORNG if hot else INK,True),(lb+"\n",10,GREY,False)])

R += box("eng1why",P,0.6,4.56,12.13,0.6,[
  ("Why this is more than sentiment analysis:",10.5,INK,True),
  ("  every post is tagged against the retrieval journey, so failure modes can be counted and cross-tabbed by photo type, cue and workaround. Every claim on the slides that follow traces back to a quote.\n",10.5,GREY,False)])

# deliverable links
Y3=5.22; H3=0.92; W3=3.877; G3=0.25
links=[("AI DISCOVERY ENGINE","Live and testable  →",True),
       ("AI-NATIVE MVP","Link added on submission",False),
       ("RESEARCH REPO","Problem definition, survey, interviews, execution plan  →",False)]
for i,(hd,sub,hot) in enumerate(links):
    x=0.6+i*(W3+G3)
    R += [shape(f"eng1l{i}b",P,x,Y3,W3,H3), fill(f"eng1l{i}b", F_BLUE if hot else F_NEUT, O_BLUE if hot else None)]
    R += box(f"eng1l{i}",P,x+0.2,Y3+0.14,W3-0.4,H3-0.28,[
        (hd+"\n",9,BLUE if hot else GREY,True),(sub+"\n",11.5,INK,False)])

R += box("eng1ft",P,0.6,6.32,12.13,0.45,[
  ("Built entirely on free tiers: open-source scrapers → Python → Gemini (JSON schema) → Streamlit Cloud. Zero spend on AI.\n",9.5,GREY,False)])
dump(R,"s1")

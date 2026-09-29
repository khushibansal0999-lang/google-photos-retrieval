from lib import *
P="p10"; R=[]
for i in range(2,26): R.append({"deleteObject":{"objectId":f"p10_i{i}"}})
R += title("mtr9t",P,"Every metric with its formula, its target, and the event data it needs")
R += badge("mtr9bg",P,"09","Success metrics",BLUE)
R += dots("mtr9dt",P)

COLS=[(0.6,2.75),(3.45,4.35),(7.90,1.45),(9.45,3.28)]
HDR=["METRIC","FORMULA","TARGET","EVENT DATA REQUIRED"]
HY=1.26
for j,(x,w) in enumerate(COLS):
    R += box(f"mtr9h{j}",P,x,HY,w,0.3,[(HDR[j]+"\n",8.5,ORNG,True)])

rows=[("North star · Vague-memory retrieval success rate","successful sessions ÷ sessions seeking an item over a year old","baseline +15pp","session_start · target_opened · item_age",True),
 ("Expression rate","sessions with at least one cue entered ÷ retrieval sessions","48% → 65%","query_submitted · cue_count",False),
 ("Interpretation accuracy","queries where no cue was silently hard-filtered ÷ queries containing a fuzzy cue","≥ 95%","cue_parsed{type, confidence} · filter_applied{hard|soft}",True),
 ("Recognition rate","target opened ÷ sessions that returned results","≥ 70%","result_shown{rank} · result_opened",False),
 ("Recovery rate","dead sessions rescued ÷ sessions with no usable result","≥ 30%","zero_result · narrowing_offered · narrowing_accepted",False),
 ("Clarifying questions per session   GUARDRAIL","questions asked ÷ retrieval sessions","≤ 0.4","clarify_shown · clarify_answered · clarify_skipped",False),
 ("Route-around rate   DIAGNOSTIC","documents re-photographed within 10 min of a failed search ÷ failed document searches","trending down","search_failed · capture{type} · timestamp",False)]
Y=1.62; RH=0.62
for i,(m,f,t,d,band) in enumerate(rows):
    y=Y+i*RH
    if band:
        R += [shape(f"mtr9b{i}",P,0.5,y-0.04,12.33,RH-0.06), fill(f"mtr9b{i}",F_NEUT)]
    vals=[(m,10,INK,True),(f,9.5,GREY,False),(t,10,BLUE,True),(d,9,GREY,False)]
    for j,(x,w) in enumerate(COLS):
        txt,sz,col,bd = vals[j]
        R += box(f"mtr9r{i}c{j}",P,x,y,w,RH-0.08,[(txt+"\n",sz,col,bd)])

R += box("mtr9ft",P,0.6,6.04,12.13,1.16,[
  ("How this gets read:",10.5,INK,True),
  ("  the north star is the only one that matters on its own. Interpretation accuracy is the metric the chosen solution moves directly, and the only one here that cannot be gamed by returning more results. Clarifying questions per session is a guardrail, not a goal.\n",10.5,GREY,False),
  ("Not yet instrumented:",10.5,ORNG,True),
  ("  every event above is a proposal. Targets are set against the MVP baseline measured in the user test, not against Google’s real telemetry, which we do not have.\n",10.5,GREY,False)])
dump(R,"s9")

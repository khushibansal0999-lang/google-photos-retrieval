from lib import *
P="chal7"; R=[]
R.append({"createSlide":{"objectId":P,"insertionIndex":6,
          "slideLayoutReference":{"predefinedLayout":"BLANK"}}})
R += title("chl7t",P,"We attacked all three before choosing one. Here is what survived")
R += badge("chl7bg",P,"07","Solution selection",RED)
R += dots("chl7dt",P)

W=3.877; G=0.25; Y=1.30; H=2.62
ch=[("A · THE COMPOSER",
  "This is a filter drawer with extra steps, and the research is explicit that nobody should build one.",
  "The chips are derived from the user’s own sentence, never offered as a menu, and they are capped. A chip the user did not imply is never created. It is a receipt, not a control panel.",
  "More than four chips on a median query, or an edit rate under 10%, which would mean nobody reads them.",True),
 ("B · THE PROMPTER",
  "It is a form. Forms feel like work, and no user asked for one.",
  "True, and it scores 5 on confidence for exactly that reason. It is not the default: it appears after a blank result or a long hesitation. The cue order is not guessed either, it follows free-recall research.",
  "Abandonment inside the prompter running higher than abandonment at the blank box.",False),
 ("C · THE ANCHOR",
  "Google already has “more from this day”. This is browsing with a new name.",
  "Browsing from an anchor exists. Querying from one does not. The unit here is “someone else from this trip, indoors”, an anchor plus a verbal cue. P2 performed exactly this by hand, using nearby photos to correct a date estimate that was a month out.",
  "Users cannot find an anchor either, which would mean the problem sits deeper than retrieval.",False)]
for i,(hd,obj,ans,kill,sel) in enumerate(ch):
    x=0.6+i*(W+G)
    R += [shape(f"chl7c{i}b",P,x,Y,W,H), fill(f"chl7c{i}b", F_BLUE if sel else F_NEUT, O_BLUE if sel else None)]
    R += box(f"chl7c{i}",P,x+0.2,Y+0.13,W-0.4,H-0.26,[
      (hd+"\n",12,BLUE if sel else INK,True),
      ("THE STRONGEST OBJECTION\n",8.5,ORNG,True),(obj+"\n",9.5,INK,False),
      ("THE ANSWER\n",8.5,ORNG,True),(ans+"\n",9.5,GREY,False),
      ("WHAT WOULD KILL IT\n",8.5,ORNG,True),(kill+"\n",9.5,GREY,False)])

R += box("chl7lb",P,0.6,4.00,12.13,0.36,[
  ("Why A survives all three levels the evaluator scores\n",12,INK,True)])

DY=4.40; DH=1.82
dfn=[("Does it solve the problem?","The control test settles it: “bill from last august” returned nothing, “bill from august 2025” returned an instant itemised answer. Same photo, same content word, only the date phrasing changed. Three unprompted requests from two participants describe this exact interaction.",F_BLUE,BLUE),
     ("Is it differentiated?","Google, Apple and Immich all resolve ambiguity silently. ChatGPT and Gemini ask, but cannot see your library. Screenshot apps read text only. Nothing shows you its interpretation and holds it loosely at the same time.",F_NEUT,INK),
     ("What stops a competitor copying it?","The interaction is copyable in a week, and we should say so. The moat is underneath: judging whether “last August” is ambiguous for this user needs their multi-year history, it runs on the existing index so nothing new leaves the device, and it ships where the failure happens.",F_ORNG,ORNG)]
for i,(hd,bd,bg,fg) in enumerate(dfn):
    x=0.6+i*(W+G)
    R += [shape(f"chl7d{i}b",P,x,DY,W,DH), fill(f"chl7d{i}b",bg)]
    R += box(f"chl7d{i}",P,x+0.2,DY+0.12,W-0.4,DH-0.24,[
      (hd+"\n",11,fg,True),(bd+"\n",10,GREY,False)])

R += box("chl7ft",P,0.6,6.30,12.13,0.98,[
  ("Sizing this bet:",10.5,INK,True),
  ("  273M users fail monthly × 82% of failures being a misread clue = ~224M addressable. At a deliberately pessimistic one-in-five rescue rate, about 45M more successful retrievals a month. Every figure is an estimate and labelled as one.\n",10.5,GREY,False),
  ("Kill the whole bet if:",10.5,ORNG,True),
  ("  clarifying questions exceed 0.4 per session, fewer than 2 of 3 testers beat their own Google Photos baseline, or anyone asks for the plain grid back.\n",10.5,GREY,False)])
dump(R,"s7")

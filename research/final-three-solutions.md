# The three solutions, combined and scored

Your three ideas and mine merged into three genuinely distinct options. Distinct means **different surface, different mechanism, different primary evidence** — not three flavours of one idea.

---

## Solution A · "Describe it the way you'd tell a friend"
**Surface:** the search / ask box · **Combines:** my time-disambiguation + attribute narrowing, your document text recognition

You type one sentence the way you'd say it to a person: *"the bill from that dinner with friends, sometime last year"*. The system:
- pulls out every cue it can — who, where, what was in frame, **words printed in the image**, roughly when
- treats time as a **range with a confidence**, never a silent filter. When it is genuinely torn it asks **one** question: *"August 2025 or August 2026?"*
- shows **why** each result matched, so a wrong answer is correctable instead of baffling
- on a miss, narrows by **attributes nobody recorded** — a child, black and white, a document — instead of returning an empty grid

**Evidence:** the controlled test (`"last august"` → nothing, `"august 2025"` → instant) · P2 Task B (wrong date by a month, five steps, app never in the loop) · 68% hold 2+ cues · 82% of review failures were a fair clue misread · **both of P2's unprompted wishes** — *"I just wish someone / any agent find it for me"* and *"a feature to filter pictures based on non-recorded criteria"*

---

## Solution B · "The things you saved, not the moments you lived"
**Surface:** a separate space, outside the memory timeline · **Combines:** your documents idea, your recognition idea redirected from faces to text and object type, my narrowing

Utility images stop living in the nostalgia timeline. The app detects them on capture — IDs, receipts, bills, tickets, prescriptions, screenshots — reads their text, and keeps them in their own indexed space, searchable by what is printed on them (*"PAN"*, *"ONE8"*, *"₹2760"*) and filterable by document type. Your holiday photos never dilute a search for your passport.

**Evidence:** 77% save utility photos often · P1's PAN card (gave up, re-photographed it) · **P2's recovery-password photo (five steps)** · your own ONE8 bill · Aadhaar, passport, marksheet in the survey · an entire category of screenshot-search apps exists because this gap is real

---

## Solution C · "Find it by what happened, not when"
**Surface:** the browse axis itself · **Combines:** your trip/occasion albums, my memory anchors

The timeline stops being months. The app derives landmarks from the library — trips from location clusters, events from density spikes, a house move from a change in home location, a new person who starts appearing — and you navigate by *"the Kodaikanal trip"* or *"around when we moved"* instead of scrolling through dates.

**Evidence:** 74% scroll by date, the widest behaviour we found · 61% had forgotten that date · **P2 Task B is a person manually using surrounding photos as landmarks to correct their own date estimate**, which is this feature done by hand

---

## Scoring

Confidence reflects evidence, not enthusiasm. Effort is inverse.

| | Reach | Impact | Confidence | Effort | **RICE** |
|---|---|---|---|---|---|
| **A · Describe it to a friend** | 7 | 9 | 9 | 3 | **189** |
| **B · Documents space** | 7 | 8 | 8 | 4 | **112** |
| **C · Landmark navigation** | **10** | 7 | 5 | 8 | **44** |

**Where each loses marks, honestly:**
- **A** — reach is capped because only 48% ever use search. A better box helps people who already type. (Counter: they stopped typing *because* it failed them, but that is a hypothesis, not evidence.)
- **B** — solves nothing for memory photos, which are 80% of a library. It owns the high-stakes moments and ignores the common ones.
- **C** — widest reach of anything we found, and still last, because nobody asked for it and it is the most expensive to build.

---

## Recommendation: A, with B's use case as the lead demo

Two reasons, and the second is the one that decides it.

**1. It wins on the numbers** — best evidence, lowest effort, addresses all three failure modes rather than one.

**2. The deck contradicts itself otherwise.** Slide 5 proves, with a control, that retrieval collapses because *the app silently guesses the date*. If the next slide proposes a documents folder, the first question any mentor asks is: *"you just showed the problem was the date, so why are you building a folder?"* The solution has to answer the root cause the deck spent three slides establishing. Only A does.

**Your documents idea is not lost — it becomes the lead scenario inside A.** The demo opens with the bill and the PAN card, because those are the retrievals that are time-pressured and high-stakes, and words printed in the image are a first-class cue in A's model. B's evidence carries straight into A's story.

**C is named on the slide as the next bet**, with its reach stated, so the deck shows we know the bigger prize and chose the provable one first.

**Deliberately out:** face-recognition enrichment. P2's Task C is the reason — a 20-year-old face does not match the current cluster, so it breaks on exactly the photos our segment is hunting.

---

## What gets built

**MVP: a conversational retrieval agent over a seeded library.**

Three flows, in build order:
1. **Multi-cue happy path** — one sentence with several cues returns ranked candidates, each showing why it matched.
2. **The ambiguity question** — an ambiguous date triggers one question, then resolves. *This is the money demo: it is your ONE8 failure, fixed in one turn.*
3. **The near-miss** — nothing confident returns closest candidates plus one narrowing question, including attributes nobody recorded (a child, black and white, a document).

**Demo library:** roughly 120 items with realistic metadata, seeded with the actual failures from research — a restaurant bill dated in an ambiguous month, a PAN-style ID card, a recovery-password screenshot, childhood photos in black and white, a trip, a wedding. The evaluator confirmed AI-generated images are acceptable.

**Stack, all free:** Python + Gemini for cue extraction and ranking, Streamlit Cloud for deployment, same pattern as the discovery engine.

---

## Update, 29 Sep: two more interviews and a desk-research pass

**Nothing changes the recommendation. Three things strengthen it and one thing needs answering.**

**1 · A third independent, unprompted request for Solution A.** P3, asked what they wished they could tell the app:
> "Probably describe the contents and specific details in the picture so that the app could filter and narrow down pics that suits the info from the description."

That is now P2 twice and P3 once, all unprompted, all describing A.

**2 · The best quote in the research for what A has to accept.** P4, asked how they'd describe the photo to a friend:
> "Bro I was roaming around there man. It's somewhere near a waterfall."

Vague, place-ish, entirely non-indexable, completely natural.

**3 · Dropping face recognition is now supported by a contrast, not an assertion.** P2 (~75,000 photos) failed a date-blind task because a 20-year-old face doesn't match the current cluster. P3 (~5,000 photos) succeeded at the same task with the same feature. **Face search degrades with library depth and elapsed time — precisely our segment.**

**4 · Documents are now 3 of 4.** A PAN card, a recovery-password screenshot, and P4's flat "given it was a document, I was unable to exactly locate it". This keeps documents as A's lead demo scenario and vindicates the B evidence being folded in.

**5 · A new failure mode.** P4 could not tell whether the photo was *missing* or merely *unfindable*: "I don't even know if it exists on this device or not." The archive's promise fails a level deeper than retrieval.

**6 · A new workaround class.** P3 keeps documents in Drive, never in Photos, and manually renames and folders everything important. The product lost the use case before a search ever happens. `WORKAROUNDS` needs **pre-emptive manual filing** and **store elsewhere**; both are invisible in telemetry.

### The one thing that needs answering

Desk research puts the largest opportunity at the **recovery loop** — turning "that's not it, but it's close" into the next search — on the grounds that a near miss is where users hand over the most information for the least effort. Our own evidence puts it at the **understanding step**, because the controlled test flipped total failure into an instant answer by changing only the date phrasing.

**Both are in A**, and the deck now names the disagreement rather than smoothing it: A exposes its interpretation before it retrieves, *and* asks one narrowing question after a near miss. The MVP build order reflects our own evidence first — disambiguation, then narrowing — and the user test is what settles which matters more.

### External corroboration worth citing

Across 83 free-recall photo descriptions, indoor/outdoor appeared 69 times, number of people 64, identity of people 56 and location 54, while **exact date proved notably less useful than time of day or broad temporal context**. Our survey found the same shape independently: 74% navigate by date, 61% had forgotten it.

### Concrete interaction for the MVP

The desk research names the mechanism better than we had: turn the sentence into **editable cue chips with confidence**, e.g. `Sister · Night · Outdoors · Wedding? · Date unknown`. The `?` marks a soft preference rather than a hard filter. That is Solution A's whole thesis made visible in one row of UI, and it is what the MVP should build.

---

# Reframe: the solutions now sit on the prompt, not on documents

Documents were a *use case*, not a mechanism. Leading with them made the solution set look like three unrelated products. The real territory is **stage 3 of the funnel — the moment the user's memory becomes a prompt and the app decides what it means.** All three options below attack that stage. They differ by what the user is actually able to give us.

## A · The Composer — *for when you can describe it*

The sentence becomes **editable cue chips, each carrying a confidence**: `sister · night · outdoors · wedding? · date unknown`. A question mark means a soft preference, never a hard filter. The chips sit above the results as a receipt of what the app understood, so a wrong reading is visible and one tap fixes it.

**Reach 6 · Impact 9 · Confidence 9 · Effort 3 → RICE 162**

- *Strongest objection:* "This is a filter drawer with extra steps, and the desk research explicitly says not to build one."
- *Answer:* the chips are derived from the user's own sentence, never offered as a menu, and they are capped. A chip the user did not imply is never created. It is a receipt, not a control panel.
- *What would kill it:* more than four chips on a median query, or an edit rate under 10%, meaning nobody reads them.

## B · The Prompter — *for when you don't know what to say*

The box stops being blank. The app asks for the cues memory actually keeps, strongest first: who was there, indoors or outdoors, roughly where, what was happening. Every field optional. **None of them a date.**

**Reach 9 · Impact 7 · Confidence 5 · Effort 4 → RICE 79**

- *Strongest objection:* "It's a form. Forms feel like work, and no user asked for one."
- *Answer:* true, and that is exactly why it scores 5 on confidence. It is not the default — it appears after a blank result or a long hesitation. The cue order is not guessed: free-recall research ranks indoor/outdoor, number of people, identity and location above exact date.
- *What would kill it:* abandonment inside the prompter running higher than abandonment at the blank box.

## C · The Anchor — *for when you can only point*

"It's from the same trip as this one." Point at any photo you *can* find and search relative to it: same day, same people, just before or just after. Words optional — the anchor carries the context the words could not.

**Reach 6 · Impact 8 · Confidence 8 · Effort 5 → RICE 77**

- *Strongest objection:* "Google already has 'more from this day'. This is browsing with a new name."
- *Answer:* browsing from an anchor exists; **querying** from one does not. The unit is "someone else from this trip, indoors" — an anchor plus a verbal cue. And **P2 performed exactly this operation by hand**, using nearby photos to correct a date estimate that was a month out.
- *What would kill it:* users cannot find an anchor either, which would mean the problem sits deeper than retrieval.

## Recommendation: A, and the reasoning is not the numbers

B has the widest reach in the entire project — the 74% who never type anything — and it still loses. It scores 5 on confidence because **no user asked for a form**; it came from us and from desk research. A wins on evidence: a controlled test where only the date phrasing changed, plus three unprompted requests from two participants describing this exact interaction. Going first on the provable bet is a legitimate choice, and **B is named as the next bet rather than dropped.**

**Deliberately out of this round:** the stage-5 recovery loop, which the desk research rates the single biggest opportunity and we rate second. The MVP user test is designed to tell us whether that ordering is wrong. Also still out: face-recognition enrichment, now disqualified by a contrast rather than an assertion — face search worked at 5,000 photos and failed at 75,000.

**Where documents went:** into the demo library as the lead scenario, and into the cue model as printed text. They are evidence for A, not a product of their own.

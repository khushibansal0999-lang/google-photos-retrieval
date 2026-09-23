# User Interview Guide — Vague-Memory Photo Retrieval

**Method:** Contextual inquiry with retrospective retrieval tasks (30–40 min, video call, participant shares their phone screen).
**Why this method:** Self-reported search behaviour is unreliable — people say "I just search for it" and then scroll for 4 minutes. Watching a real retrieval attempt on their *own* library surfaces the actual failure point, and each task doubles as an MVP test case later.

## What this round of interviews needs to settle

Two data sources disagree, and only watching real people will resolve it:

| Question | Reviews (n=84) say | Survey (n=31) says |
|---|---|---|
| Do people mostly search or scroll? | (reviews are 100% about failed search — selection bias) | 74% scroll by date; only 48% ever search |
| What's the weak cue? | time/place/date forgotten | **exact date forgotten by 61%** |
| Is the failure "can't describe it" or "app misunderstands"? | 69/84 = app misunderstood; only 3/84 = couldn't express | not asked |

Every interview should produce a direct answer to: **which method do they reach for first, unprompted, and where exactly does it break?** Don't ask them what they usually do — watch it happen.

Also test one finding the reviews never showed at all: **multi-account fragmentation** ("photos are distributed among multiple google ids, hard to remember which one I used" — one survey respondent). Probe for this explicitly; it's the kind of thing nobody writes a public review about.

**Recruit:** We already have 6 confirmed volunteers + 10 "maybe"s from the survey (contacts in `research/survey/responses_raw.csv`, local only). Pick for a *mix*, not just whoever answers first:
- At least one heavy utility-photo user (Q3 score 4-5: screenshots/receipts/documents)
- At least one person whose survey Q7 showed scroll-only behavior (no search attempted)
- The person who mentioned multi-account fragmentation, if they're reachable
- A spread of library sizes (not everyone at "more than 10,000")

---

## 0. Setup (2 min)
- Consent to record + screen share. Anonymous in write-up.
- "There are no wrong answers and this is not a test of you — it's a test of the app. I want to watch what actually happens, not what you think should happen."

## 1. Warm-up: library shape (5 min)
- How long have you used Google Photos (or your main app)? Roughly how many photos?
- What kinds of things end up in there besides "photos"? (screenshots, receipts, docs, WhatsApp forwards, labels)
- **Do you use more than one Google account, or has your photo library ever moved between phones/accounts?** (probe for fragmentation — if yes, ask whether that's ever caused a "which account was it in" problem)
- When was the last time you went looking for an *old* photo? What was it? Did you find it?

## 2. Retrieval tasks — THE CORE (20 min)
Run 3 tasks. Participant thinks aloud. **Do not help. Do not suggest search or scrolling — let them choose.** Note every action, every typed query, every scroll, every dead end, and the time.

**Task A — participant-generated (most important)**
"Think of a photo you know you have, from at least a year ago, that you'd struggle to find right now. Don't tell me where it is. Find it."
- Before they start, ask: *What do you remember about it?* (write down cues: time / place / people / what's in it / why you took it / how it got there)
- *What do you NOT remember?*
- **Watch their very first move** — do they open search, or start scrolling/swiping? Write down which, unprompted.

**Task B — utility photo**
"Find a photo you took of a document, receipt, label, bill, or screen — something you took to remember information, not for the memory."

**Task C — deliberately date-blind**
"Think of a photo where you have NO idea what year or even season it was taken — you just know it exists." *(This directly stress-tests whether losing the date cue is what breaks retrieval, per the survey's top finding.)* If they can't think of one, ask about a childhood/very old photo instead.

For each task record:
| Field | |
|---|---|
| Cues remembered | |
| Cues forgotten | |
| First action (search / scroll / album / map / people?) — **unprompted** | |
| Query typed (verbatim), if any | |
| What came back | |
| Second attempt | |
| Outcome (found / gave up / found by luck) | |
| Time to outcome | |
| Where it broke: couldn't express it / typed something reasonable and app got it wrong / scrolling had nothing to anchor to / too many results to scan / other | |

## 3. Reflection (8 min)
- You just [searched / scrolled] — is that what you usually do, or did today feel different? *(Cross-check against their survey answer if they took it.)*
- When it didn't work right away, what did you wish you could tell the app that you couldn't?
- If you could describe the photo to a friend who had your library, what would you say? (→ natural-language clue set)
- What do you do today when this happens — keep trying, ask someone, give up? Does it usually get resolved eventually, or do some photos just stay lost?
- How often does this happen — daily/weekly/monthly/rarely? Does it usually matter, or is it just mildly annoying? *(Compare to their survey Q10/Q11 answer if available.)*
- Have you ever given up on finding a photo you knew existed and never went back? What was it, and why did it matter (or not)?

## 4. Close (2 min)
- Would you be up for a 15-min follow-up in ~2 weeks to try a prototype? (→ MVP testers — separate from the survey's interview volunteer list)

---

## Synthesis template (fill after each session in `interviews/P<n>.md`)
- Participant profile (segment hints: library size, utility-photo habit, multi-account?)
- Per task: cues remembered / forgotten / first action / query / where it broke / outcome / time
- Top 3 verbatim quotes
- Did they search-first or scroll-first, unprompted? Does it match their survey answer?
- Did Task C (date-blind) actually break retrieval, or did another cue rescue it?
- Any mention of multi-account fragmentation?
- Surprises vs. the discovery-engine / survey findings

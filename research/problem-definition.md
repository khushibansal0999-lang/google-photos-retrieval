# Part 4 — Problem Definition

*Grounded in: 1,196 tagged public posts (84 genuine vague-memory failures) · survey n=31 · interviews P1–P2 (P3–P6 in progress).*

---

## The problem, in one paragraph

**People who have kept photos for years remember an old photo the way memory actually stores it — who was there, where it happened, what was in the frame, why they took it. Google Photos only accepts the two currencies memory doesn't keep: an exact date to scroll to, or the exact word the index happens to hold. When neither matches, there is no way to combine the fragments a person does have, and no way to narrow down after a near-miss. So the photo isn't lost — it's unreachable at the moment it's needed, and people quietly route around the app instead of through it.**

That last clause is the part that makes this worth solving: the failure is invisible in the product's own data, because users don't complain — they take the photo again, ask a friend, or wait to stumble on it weeks later.

---

## 1. Target user segment

**Long-tenure users with deep, mixed libraries.** Concretely: 3+ years of continuous backup, roughly 10,000+ items, and a library that holds *both* memory photos and utility photos — screenshots, bills, IDs, prescriptions, documents.

| Evidence | Source |
|---|---|
| 65% have 5+ years of photos; 68% have 2,000–10,000+ items | Survey n=31 |
| 77% save screenshots/bills/IDs often (4–5 on a 5-point scale) | Survey n=31 |
| P1: 15-year-old account. P2: ~75,000 photos in 4 years | Interviews |
| Failures cut across photo types — 70% of review cases fit no single photo-type niche | Discovery engine |

**Why this segment and not "everyone":** vague memory is a *function of library depth and elapsed time*. A user with 400 recent photos scrolls and finds it. The problem only exists once the library outgrows human recall — which is also the point at which the user is most committed to the product and most likely to be paying for storage.

## 2. The retrieval scenario we're solving for

A user needs **one specific photo they know exists**, taken **more than a year ago**, **right now**, for a concrete purpose — to prove something, complete a task, or show someone. They can describe the photo in human terms but cannot supply the two things the system wants: the date it was taken, or the word the index filed it under.

Not in scope: browsing for pleasure, rediscovering memories, curating albums. Those are *supply-driven* (the app decides what to show). This is *demand-driven* — the user arrives with an intent and a deadline.

## 3. Product outcome we intend to influence

> **The share of demand-driven retrieval sessions for photos ≥1 year old that end with the user opening and using the photo they came for — without having to guess a date or a keyword.**

Deliberately not "search success rate": most of these sessions never touch search (74% scroll). Measuring search alone would miss the majority of the problem.

## 4. Root cause

Both available paths into an old photo are keyed on information memory does not retain.

**The scroll path needs a date the user doesn't have.** The timeline is ordered by capture date; 61% of survey respondents had forgotten the exact date of the photo they were hunting. Worse, capture date is often not even the date they remember — a photo someone sent them files under *when it was originally taken*, not when they received it. As one reviewer put it: *"can't find family photos downloaded cause they end up being the year it was taken."* The user's memory anchor and the system's sort key are two different facts.

**The search path needs the word the index chose.** Remembering the content correctly isn't enough — you have to guess the term. In P1's session, the *correct* brand name returned photos of the appliance but not its receipt; the vendor name returned nothing; the generic word "bill" found it on the third try. His own summary: *"The keyword matters."* Across the review data, 82% of vague-memory failures were a reasonable clue the app misread — not a user who couldn't describe what they wanted.

**And neither path composes or recovers.** People hold several fragments at once — 68% recall two or more cues, and when P2 was asked how they'd describe a photo to a friend they listed four in one breath: *"date/content of photo/with whom it was/why was it taken."* But there is nowhere to put four partial cues together, and a failed query returns nothing rather than narrowing. Every attempt starts from zero.

**Why this is not "search is bad":** only 3 of 84 failures were users who couldn't express what they wanted, and 90% arrived holding at least one solid cue. The memory is present. The bridge from memory to photo is missing.

## 5. Existing workarounds

| Workaround | Evidence |
|---|---|
| Scroll month by month, hoping to recognise it | 74% of survey respondents; 29% never try anything else |
| Ask someone who was there | 19% of survey; P2 describes it as a normal step |
| **Re-do the task instead of finding the photo** | **2 of 2 interviews.** P1 gave up after ~2 min and re-photographed his PAN card; P2: *"I choose alternative path for that work."* |
| Wait for serendipity | P2: *"when randomly scrolling over my gallery later I find it"* — the photo surfaces, just too late to be useful |
| Abandon it | 77% have given up on a photo they were certain they had |

The third row is the most important and the least visible. **When someone re-photographs a document rather than finding the original, the need was met and the product failed — but nothing in the product's telemetry records a failure.** This is why review data under-counts the problem: people don't write reviews about a workaround that worked.

## 6. Why solving this creates meaningful user value

Three distinct costs, not one:

1. **Utility retrieval fails under time pressure.** The PAN card, the receipt, the prescription — needed at a counter, in a form, on a call. Failure means redoing work, and the user absorbs it as their own disorganisation.
2. **Moments arrive too late to matter.** P2 wanted a college photo *to post as a story* — a window measured in hours. Finding it a week later while scrolling is not success.
3. **The library's purpose quietly erodes.** People keep 15 years of photos in one place *because they expect to get back to them.* Every failed retrieval is evidence against that promise, and it compounds as the library grows — exactly as the user becomes more invested.

## 7. Why this makes business sense for Google Photos

- **Retrieval is the reason deep libraries stay put.** The switching cost of a photo library is the archive itself; if the archive isn't reachable, it's just storage — and storage is a commodity with cheaper competitors (Immich, Ente, OneDrive, which P1 already pays for and searches *in preference to* Google Photos).
- **Deep libraries are the paying libraries.** The segment with this problem is the segment on Google One. Retrieval failure attacks retention precisely where revenue is.
- **Google has already bet on this and been burned.** "Ask Photos" (Gemini-powered natural-language search) was paused in 2026 after users reported it found *less* than classic search; the fix was to show classic results alongside and let users disable Gemini entirely. The appetite is proven and the trust is damaged — which makes a *credible, explainable* version of this valuable rather than speculative.

## 8. How the thinking evolved

**Business metric** — increase successful retrieval of vaguely-remembered photos.
**↓ Product outcomes** — broke it into Remember → Express → Match → Recover. Asked which step actually leaks.
**↓ AI-powered discovery** — 1,196 posts tagged against that journey. Found the leak is *not* at "Remember" (users arrive with cues) but at Match: 82% of failures were reasonable clues misread. Also found Google's own Ask Photos rollback as external validation.
**↓ Observed user behaviour** — the survey broke the review-data framing: most people never search at all (74% scroll by date), and the cue they're scrolling for is the one 61% have forgotten. Interviews then showed *how* it fails in practice — keyword luck (P1), and that abandonment usually means routing around the app, not an unmet need (P1, P2).
**↓ Problem definition** — the statement at the top of this page.

The single biggest shift along that chain: we started expecting to find *"search misunderstands people"* and ended up finding *"most people never reach search, and neither path accepts what they actually remember."*

---

## What this implies for the MVP (to decide next)

The problem statement points at three requirements, in priority order:

1. **Accept several partial cues at once** — people arrive with 2+ fragments and nowhere to put them.
2. **Don't require a date or the index's exact word** — accept approximate time and human landmarks; match on meaning, not term.
3. **Recover from a near-miss** — narrow down instead of returning nothing, because today every retry restarts from zero.

**Open question for the MVP:** whether to build this as a conversational agent (directly answers P2's unprompted *"I just wish someone/any agent find it for me what I need"*) or as a structured multi-cue filter. To be decided once P3–P4 confirm the pattern.

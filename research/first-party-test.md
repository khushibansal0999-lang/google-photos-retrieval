# First-party retrieval test — Ask Photos, production Google Photos

**28 Sep 2026 · researcher's own library · Gemini "Ask Photos" enabled · Android**

A real retrieval task run against the shipping product, on a real library, for a real photo. This is the strongest single piece of evidence in the project: reproducible, first-party, and on the current production experience rather than a reconstructed review.

## What happened

| # | Query typed | Result |
|---|---|---|
| 1 | *"I need the photo of bill from last august"* | **Failed.** "I couldn't find any photos that matched your request for 'bill' from last August. However, I can show you photos from last August." Then displayed ~8 photos from **August 2026** — selfies, festival decorations, a book, a screenshot. No bills. |
| 2 | *"photo of bill from last august at one8"* (added the venue name) | **Failed again.** "I couldn't find any photos that matched your request for 'bill' from last August. It seems my search didn't turn up any relevant media." Nothing returned at all. |
| 3 | *"I want bill receipt of dinner last year"* | **Succeeded.** "I found two bills from One8 Commune dated August 3, 2025. The total amount was ₹2760.00" — with an itemised breakdown and both photos. |

The photo was in the library the whole time, and the product could ultimately read it in fine detail — itemised line items, total, venue, date. **This is a retrieval failure, not a data or capability failure.**

## What it proves

**1. The time reference was silently resolved to the wrong year — and that alone sank it.**
"Last August" is genuinely ambiguous a month after August 2026: it can mean Aug 2026 or Aug 2025. The bill was Aug 3, **2025**. Ask Photos resolved it to **2026** without saying so (the "Related" chips confirm: Aug 28 2026, Aug 15 2026), hard-filtered on that year, and searched inside a window the photo was never in. Query 3 succeeded largely because *"last year"* is unambiguous.

**A single clarifying question — "August 2025 or August 2026?" — would have solved this in one turn.** Instead the product guessed, failed, and never surfaced the ambiguity. This is requirement #3 from the problem definition ("recover from a near-miss") failing in the clearest possible way.

**2. Adding a more specific, correct cue made it worse, not better.**
Query 2 added the venue — *more* information, and accurate. It returned strictly less: zero results instead of a fallback grid. This reproduces P1's receipt task almost exactly (his correct brand name "Bosch" failed; generic "bill" worked). **Precision in the user's memory does not convert into precision in the result.** Two independent people, same pattern.

**3. When it fails, it discards the wrong cue.**
The fallback kept the *date* and threw away *"bill"* — then showed selfies and festival photos. The user was certain about exactly one thing (it's a bill) and unsure about exactly one thing (when). The product kept the thing they were unsure about and discarded the thing they were sure about. That's backwards, and it's the root cause made visible in one screen.

## Why this matters for the deck

It collapses the argument into something a reviewer can see in three screenshots:

- The photo exists · the AI can read it perfectly · the user described it correctly · **and it still took three attempts, with the successful one being vaguer than the failures.**
- It's first-party and reproducible — not a quote from someone else's review.
- It validates all three MVP requirements at once: accept multiple partial cues (2), don't hard-filter on a guessed date (1), ask one question instead of guessing (3).

## Privacy note before this goes in the deck

Screenshot 1 shows the researcher's personal photos (faces, family, home) and screenshot 3 shows real receipts with a transaction total. **Do not publish these uncropped** in a public deck or repo. For the deck, crop to the *text* of the Ask Photos response plus, at most, a blurred thumbnail strip — the argument lives entirely in the response text, not in the photos themselves.

## Follow-up worth running

1. Re-run query 1 as *"bill from August 2025"* — if that works, it isolates the failure to time resolution alone and makes the finding airtight.
2. Try a multi-cue query where all cues are correct but the date is approximate (*"restaurant bill, dinner with friends, around a year ago"*) — tests whether approximate time works when it isn't phrased as a specific month.

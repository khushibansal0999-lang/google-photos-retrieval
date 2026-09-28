# First-party retrieval test — Ask Photos, production Google Photos

**28 Sep 2026 · researcher's own library · Gemini "Ask Photos" enabled · Android**

A real retrieval task run against the shipping product, on a real library, for a real photo. This is the strongest single piece of evidence in the project: reproducible, first-party, and on the current production experience rather than a reconstructed review.

## What happened

| # | Query typed | Result |
|---|---|---|
| 1 | *"I need the photo of bill from last august"* | **Failed.** "I couldn't find any photos that matched your request for 'bill' from last August. However, I can show you photos from last August." Then displayed ~8 photos from **August 2026** — selfies, festival decorations, a book, a screenshot. No bills. |
| 2 | *"photo of bill from last august at one8"* (added the venue name) | **Failed again.** "I couldn't find any photos that matched your request for 'bill' from last August. It seems my search didn't turn up any relevant media." Nothing returned at all. |
| 3 | *"I want bill receipt of dinner last year"* | **Succeeded.** "I found two bills from One8 Commune dated August 3, 2025. The total amount was ₹2760.00" — with an itemised breakdown and both photos. |
| 4 | *"Bill from august 2025"* (control test) | **Succeeded instantly.** Same two bills, itemised to the dish — Cheese and Herb Polenta, Lemongrass Grilled Chicken, Burrata and Basil — *plus* related items it hadn't surfaced before: a table QR code, a ₹400 payment confirmation, a rewards screen. |
| 5 | *"Restaurant bill, dinner with friends, around a year ago"* (approximate time, multi-cue) | **Succeeded, then over-delivered.** Led with the right answer — "You have screenshots of two bills from ONE8 Commune dated August 3, 2025, totaling ₹2760.00" — but the grid then filled with ~64 items (+56 hidden): meals with friends across Bengaluru, Udaipur and Pushkar, Oct 2025 – Mar 2026. |

The photo was in the library the whole time, and the product could ultimately read it in fine detail — itemised line items, total, venue, date. **This is a retrieval failure, not a data or capability failure.**

## What it proves

**1. The time reference was silently resolved to the wrong year — and that alone sank it. Now proven by control test.**

Query 4 is the clincher: **identical content word ("bill"), identical photo, identical library — only the date phrasing changed from "last august" to "august 2025" — and it went from nothing to an instant, richer-than-asked-for answer.** Content matching was never the problem.

"Last August" is genuinely ambiguous a month after August 2026: it can mean Aug 2026 or Aug 2025. The bill was Aug 3, **2025**. Ask Photos resolved it to **2026** without saying so (the "Related" chips confirm: Aug 28 2026, Aug 15 2026), hard-filtered on that year, and searched inside a window the photo was never in. Query 3 succeeded largely because *"last year"* is unambiguous.

**A single clarifying question — "August 2025 or August 2026?" — would have solved this in one turn.** Instead the product guessed, failed, and never surfaced the ambiguity. This is requirement #3 from the problem definition ("recover from a near-miss") failing in the clearest possible way.

**2. Once the wrong window is locked in, every extra cue makes things worse.**
Query 2 added the venue — *more* information, and correct. It returned strictly *less*: zero results instead of a fallback grid. Read together with query 4, the cleanest explanation is not that the venue cue was misread, but that **the year filter was already wrong, so each additional cue simply narrowed an empty set further.** The user is punished for adding accurate detail.

*(Correction to an earlier draft of this note: I first framed query 2 as keyword luck, the same failure as P1's "Bosch" search. The control test shows that reading was wrong for this case — the time filter explains it. P1's keyword-luck finding still stands on its own evidence; it just isn't what happened here.)*

**3. When it fails, it discards the wrong cue.**
The fallback kept the *date* and threw away *"bill"* — then showed selfies and festival photos. The user was certain about exactly one thing (it's a bill) and unsure about exactly one thing (when). The product kept the thing they were unsure about and discarded the thing they were sure about. That's backwards, and it's the root cause made visible in one screen.

## Why this matters for the deck

It collapses the argument into something a reviewer can see in three screenshots:

- The photo exists · the AI can read it perfectly · the user described it correctly · **and it still took three attempts, with the successful one being vaguer than the failures.**
- It's first-party and reproducible — not a quote from someone else's review.
- It validates all three MVP requirements at once: accept multiple partial cues (2), don't hard-filter on a guessed date (1), ask one question instead of guessing (3).

**4. The system has three distinct time behaviours — and the middle one is the trap.**

| Time phrasing | How it's treated | Outcome |
|---|---|---|
| Explicit — *"august 2025"* | Exact filter | ✅ Best case: instant and precise |
| **Semi-specific but ambiguous — *"last august"*** | **Silently resolved to one reading, then hard-filtered** | ❌ **Worst case: zero results, no explanation** |
| Openly vague — *"around a year ago"* | Treated as a loose range | ⚠️ Target found and summarised first, but buried in ~64 loosely-related photos |

**The counter-intuitive headline: being *honestly vague* works better than being *confidently approximate*.** "Around a year ago" beat "last August". The failure zone is phrasing that *looks* resolvable to a parser but is genuinely ambiguous to a human — the system mistakes the user's approximation for precision and never checks.

That is exactly how people talk about old photos. "Last August", "last Diwali", "that summer" all read as specific and are not.

**5. Credit where due: the written answer carried it.**
In query 5 the grid was noisy, but the summary text led with the correct bill, the date, the total and the dishes. The language layer prioritised correctly even when the retrieval layer over-fetched — which points at an MVP shape: **lead with a confident written answer plus a handful of high-confidence matches, not a wall of thumbnails.** It also shows the `too_many_results` failure (only 4% of review cases) is real and observable in production.

## What this implies for the MVP — the sharpest requirement yet

**Never silently resolve an ambiguous time reference into a hard filter.** Either ask one question ("August 2025 or 2026?"), or search both windows and label which is which. Treat *every* time reference as a range with a confidence, never as a binary of exact-filter-or-ignore — because the evidence shows the product currently has only those two modes, and the gap between them is where real users' phrasing lands. This is now the single best-evidenced feature in the project: it is first-party, reproducible, has a clean control test, and would have turned a three-attempt failure into a one-turn success.

It also fits the rest of the evidence: 61% of survey respondents had forgotten the exact date, and the timeline is sorted by a date many don't have. Approximate time isn't an edge case — it is the normal condition.

## Privacy note before this goes in the deck

Screenshot 1 shows the researcher's personal photos (faces, family, home). Screenshot 3 shows real receipts with a transaction total. **Screenshot 4 shows a third party's full name and a ₹400 payment confirmation, plus a scannable QR code. Screenshot 5 shows the researcher's face clearly and reveals travel locations (Bengaluru, Udaipur, Pushkar) with dates.** **Do not publish any of these uncropped.** For the deck, crop to the *text* of the Ask Photos response only — the argument lives entirely in that text, not in the photos. If a thumbnail strip is needed for credibility, blur it.

## Status: micro-study complete

Five queries, one library, one target photo, three distinct system behaviours, with a clean control. Both planned follow-ups have now been run and both returned clear results. This is enough to carry the root-cause argument in the deck without further testing.

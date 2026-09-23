# Survey Findings — "How do you find old photos?"

**n = 31 responses** (as of 23 Sep 2026). Non-random convenience sample shared via WhatsApp/social — skews toward people I know, heavy usage (20/31 have 5+ years of library), and Google Photos users (21/31). Treat as **directional, not statistically representative** — its value is as a *second, independent* data source that triangulates against the 1,196 public reviews, not as a population estimate.

## Headline finding: the survey shows a different — and arguably more important — failure than the reviews do

| | Discovery engine (reviews, n=84 core cases) | Survey (n=31) |
|---|---|---|
| Top remembered cues | text-in-photo (23%), visual detail (19%) | **place (61%), people (52%)**, approx time (35%) |
| Top forgotten cues | approx time (19%), place (17%), exact date (10%) | **exact date (61%)**, text-in-photo (45%), approx time (39%) |
| Primary retrieval method | (typed a query — implicit, reviews are all about search) | **scrolled by date (74%)** |
| Used any search at all | (100% by definition — reviews are about search) | **only 48%** |
| Scrolling was their ONLY method (never touched search) | — | **29%** |

**These are not the same population talking about the same failure.** Public reviews are written by people who *tried to search, it failed, and they were frustrated enough to post about it* — that selection filter guarantees every review is a search failure. The survey instead asked "think of the last time you struggled" with no assumption about method, and it shows that **most people don't reach for search first at all** — nearly 3 in 4 scroll by date, and almost a third never try search.

**This reframes the root cause.** It's not only "the search engine misunderstands good queries" (though that's real and confirmed independently — see below). It's that **the default retrieval strategy most people actually use — scrolling, anchored on remembering roughly when something happened — breaks down exactly when the one cue it depends on (time) is the one people are least confident about.** Search failure is the loud, visible complaint; scroll failure is the silent, more common one.

## What the survey independently confirms from the reviews

Despite the different lens, the two sources agree on the core shape of the problem:
- **Exact date is the single most commonly forgotten thing** (61% survey / a top-3 forgotten cue in reviews) — nobody remembers precise dates, yet the dominant retrieval method (scrolling) depends entirely on it.
- **Text-in-photo is both commonly remembered by some (19%) and forgotten by others (45%)** — consistent with the reviews' finding that OCR/text search is a specific, unreliable weak point, not a strength people can lean on.
- Q9 (open text) independently surfaces the same failure mechanism reviews showed: *"Was sent in a Google drive, had to go back to it"* (source-channel confusion), *"had to search for month and date and then search manually one by one"* (date-dependent, effortful).

## A new failure mode the reviews never surfaced

One survey respondent: *"matter of time. sometime we hit it sometime dont. also **photos are distributed among multiple google ids**. hard to remember which one i used for those photos."*

**Multi-account fragmentation** — photos split across two+ Google accounts (personal, work, old accounts) — never appeared in any of the 1,196 tagged reviews. It's not in our `failure_stage` taxonomy. This is exactly the value of primary research beyond desk research: it surfaces failure modes no amount of review-mining would find, because it's not something people think to complain about publicly — it's a personal organizational habit, not a product bug. Worth probing for explicitly in interviews.

## Stakes & frequency (the gap reviews couldn't fill)

- **74% experience this at least "a few times a month."**
- **35% say it "sometimes really matters"** (needed for proof, a memory, a task) — this is not a trivial annoyance for a third of respondents.
- **77% have given up on a photo they knew existed** at some point (48% "forgot about it afterward," 26% "still think about it sometimes") — meaning most people quietly absorb this failure rather than reporting it, which is exactly why review data alone understates how common it is.

## Interview recruiting — a running start

**6 people said "Yes, contact me"; 10 said "Maybe."** Contact details are in [responses_raw.csv](responses_raw.csv) (Q14/Q15, not committed to the public repo — kept local only, see note below). That alone gets you most of the way to the 5-6 target — reach out to the 6 first, and 2-3 of the "Maybe"s as backup.

## Note on the raw data file

`responses_raw.csv` contains phone numbers and email addresses from consenting interview volunteers. **This file is excluded from the public GitHub repo** (added to `.gitignore`) — it stays local only.

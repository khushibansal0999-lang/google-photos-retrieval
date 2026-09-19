# User Segmentation & Impact Analysis

## Why segment by *usage behavior*, not by demographics or photo type

We first tried segmenting the 84 core vague-memory cases by photo type (screenshot owners, pet owners, travel photographers, etc.). Result: **70% fall into a general "content describer" bucket** — no single photo-type niche is big enough to be "the" segment. This is itself a finding: the failure isn't confined to one kind of photo, so the segment can't be defined by content type either.

Public reviews also don't reliably self-report demographics (only 79/243 relevant records mention any user trait at all, and most of those are throwaway — "subscriber," "long-time user"). So instead of forcing thin data to answer a question it can't, we built segments from what **is** well-evidenced — how deep/mixed a person's library is and what kind of content they accumulate — and marked what still needs interview validation (Part 3) before we commit to one.

## Segmentation framework: Library Composition × Retrieval Frequency

| Segment | Definition | Evidence it exists | Est. impact if unfixed |
|---|---|---|---|
| **A. Utility-photo accumulators** | People who use their camera as a scratchpad — screenshots, receipts, documents, labels, whiteboards, medical info — alongside memory photos | `content_not_indexed` + `text_in_image` clusters (10 core cases); corroborated externally by an entire micro-category of dedicated screenshot-search apps (ShotSeek, Screenshot Finder, Screenshot Hub) existing *specifically because* general photo apps fail this group | **High severity, narrow width.** These users hit the failure often (screenshots pile up weekly) but it's a subset of the base. Highest willingness-to-pay signal (people install a second app). |
| **B. Deep-library, multi-year users** | 3+ years of photos, tens of thousands of items, memory has degraded from "recent" to "vague" | Indirect: `time_since_photo` skews toward months/1-2yrs in the vague-memory subset; this is the population our whole research question presupposes ("photo I remember but can't precisely describe" only happens once a library is old/large) | **High severity, wide reach.** This is close to "most engaged Google Photos users" — a segment Google has strong business reason to retain. |
| **C. Occasional/shallow users** | Smaller libraries, mostly recent photos, rarely searches for anything old | Absence: almost no complaints in this shape in our dataset | **Low priority.** Vague-memory retrieval isn't yet a felt problem for this group. |
| **D. Multi-person/family archivists** | Search for a specific person combined with a fuzzy time/event ("photos of my dad," "my daughter last winter") | `person_face` segment, 100% `app_misunderstands` (n=7, small but the cleanest, most consistent failure rate of any segment) | **Medium-high severity**, cross-cuts A and B rather than standing alone. |

## Impact prioritization (reach × severity × business value)

Plotting the four segments:

```
severity (how badly retrieval breaks)
   high │  A: Utility-photo          B: Deep-library,
        │     accumulators              multi-year users
        │     (narrow, high pay-       (wide, high engagement
        │      willingness signal)      value to Google)
        │
        │  D: Family/person archivists (cross-cuts A & B)
        │
   low  │  C: Occasional/shallow users
        └───────────────────────────────────────────
           narrow                              wide
                        reach (% of user base)
```

**Recommended target: Segment B ∩ A/D** — deep-library users (3+ years, heavy usage) who *also* mix in utility photos and/or search for specific people. This isn't an artificial intersection: it's the same profile our discovery engine's raw evidence keeps surfacing (someone with years of mixed content trying to find one thing they only half-remember), and it's wide enough to matter to Google's retention metric while narrow enough to design a sharp interview screener and MVP around.

**This is the segment to recruit interviewees against** — the screener already reflects it (3+ years of library; ask about screenshot/document habits and searching for specific people during the session).

## Open questions for interviews (this segmentation is a hypothesis, not a conclusion)

Public review data can't tell us:
- How *often* this happens per user per month/year (frequency — needed for a real severity estimate)
- Whether the "gave up and it didn't matter" cases outnumber the "gave up and it mattered a lot" cases (emotional/practical stakes)
- Whether utility-photo accumulation (A) and deep-library depth (B) are actually correlated in real users, or two separate populations we've been merging

The interview guide (Part 3) is written to answer exactly these three questions in the reflection section.

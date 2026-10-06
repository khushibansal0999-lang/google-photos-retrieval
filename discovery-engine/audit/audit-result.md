# Hand audit — result

**12 of 20 agreed. 8 did not.** Twenty classifications drawn with a fixed seed
across three bands, read and judged by a person, 6 Oct 2026. Answers are in
`audit_sample.xlsx`; re-score with `python make_audit.py --score`.

| Band | What it tested | Agreed |
|---|---|---|
| A — 10 rows from the headline 84 | does this belong in the 84? | **5 / 10** |
| B — 5 rows judged relevant, classed otherwise | was this wrongly kept out? | **3 / 5** |
| C — 5 rows dropped before analysis | was a real case binned? | **4 / 5** |

## The disagreements are systematic, not noise

**Band A, five rejected.** Four of them (rows 1, 3, 7, 10) are post-update
complaints that never describe a photo — *"Worse with every update. Can't find
anything"* — and all four carry `cues_remembered` of `[]` or `none_stated`. The
problem class is someone who remembers something and cannot turn it into a
query; if the post never says what they remembered, it does not qualify. The
fifth (row 4) is different: searching by **filename**, which is precise memory,
not vague.

**Band B, two promoted.** Rows 11 and 13 were judged to belong in the 84 after
all. Both describe real retrieval failures underneath a UI complaint.

**Band C held up.** Four of five were correctly discarded, and the fifth was
moved to "relevant but not vague-memory", not into the 84. **Nothing in this
sample suggests the filter is throwing away genuine cases**, which is the
reassurance that matters most — 953 posts were dropped, and this is the only
check on them.

## What it does to the headline number

82% is 69 of the 84. Applying the rule behind most of the Band A rejections —
*no photo described and no cue stated* — removes 33 of the 84 and leaves 51,
of which 39 are `app_misunderstands`:

> **82% → 76%, on a base of 51 rather than 84.**

The deck keeps 82%, because that is what the classifier actually produced and
76% rests on a rule inferred from five judgements rather than a re-read of all
84. Slide 1 states both. The point is that **the direction survives the audit
and the precision does not** — either number says the same thing, which is that
most failures are a fair clue read wrongly.

## What we would do with more time

Re-read all 84 by hand against the stated rule, rather than extrapolating from
ten. The audit was designed to be honest about its own size: ten rows out of
84 gives a wide interval, and two rows out of 159 in band B gives a much wider
one. It is enough to say the classifier is noisy in both directions and that
the finding holds anyway. It is not enough to restate the number precisely.

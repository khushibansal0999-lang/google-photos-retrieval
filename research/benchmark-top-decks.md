# Benchmark: NextLeap top-fellow graduation decks

Two decks from NextLeap's official showcase, both 10 pages, both on the Claude brief:
- [Deck A](https://assets.nextleap.app/submissions/NL_Claude-37993987-e8e5-4d67-ac4d-bfe5a61c9945.pdf) — "Skill from Output" (Apr 2026 top fellow)
- [Deck B](https://assets.nextleap.app/submissions/NLClaude-22de754a-29fc-4d09-bb29-ef09d0e93590.pdf) — "Intent-Driven Skill Engine" (Apr 2026 top fellow)

## What both do that we currently don't

| Pattern | Deck A | Deck B | Us |
|---|---|---|---|
| **Wireframes / prototype screens on their own slide** | 10 screens + Figma link | 5 screens + link | ✗ placeholder |
| **RICE table with visible numeric scores** | Yes | Yes, full table with P1/P2/P3 | In a doc, not on a slide |
| **Alternatives considered, with "why deprioritised"** | Half a slide | Three options compared | One line |
| **Metrics with numeric targets** | Every metric has one (">50%", ">60%") | Yes | ✗ no targets at all |
| **North-star stated as a formula** | `(Confirmed Skill) / (Users shown chip) × 100`, target 25% in 30 days | Yes | Definition only |
| **Quantified business case with stated assumptions** | "1% free→Pro lift ≈ $3.4M ARR" | "+5-8% upgrade lift; assumption stated" | Qualitative only |
| **User personas** (name, age, city, role, tenure, quote) | 2 | 2 | Evidence rows, not personas |
| **Problem Framing Canvas** (6 boxes: true problem / who / how we know / value to user / value to business / why now) | Yes | Yes | Covered, but not as the recognisable canvas |
| **System architecture diagram** | Yes | Yes, layered | ✗ |
| **Go-to-market / rollout with phases and kill thresholds** | 3 phases, kill threshold "chip rejection >30%" | Revenue model + GTM | ✗ |
| **Market landscape / competitor table up front** | Slide 1 | Slide 1 | Buried in a doc, one box on slide 4 |
| **Ethics / privacy principles** | 4-principle table | Within risks | One risk row |

## Devices worth stealing

1. **Numbered hypotheses threaded through the deck.** Deck A labels research hypotheses H1–H6, then every solution says which it addresses ("Addresses H2, H3, H5, H6"). It makes the research→solution link auditable instead of asserted. It also ends the research slide with "THE THROUGH LINE CONNECTING ALL SIX" — one sentence chaining all six into a narrative.

2. **Kill thresholds, not just success criteria.** Deck A: *"Kill threshold: chip rejection rate exceeds 30%."* Stating when you'd stop is more convincing than stating when you'd celebrate.

3. **A one-line thesis in quotes on the solution slide.** Deck A: *"Every other approach asks users what they want before they have seen it. This one waits until they have seen it, then offers to save it."*

4. **Every metric answers "what it indicates."** Both use a three-column table: metric | what it tells you | target. The middle column is what makes it look considered.

## Where our deck is stronger

- **Evidence base is broader and better sourced.** 1,196 tagged public posts + n=31 survey + interviews. Deck B's survey is n=35 with no qualitative tagging; Deck A leans on 2 personas.
- **The first-party controlled test.** Neither reference deck has a controlled experiment on the live product. Our five-query micro-study with a control is a genuinely stronger piece of evidence than anything in either.
- **We have a deployed, testable AI discovery engine** — our brief requires it; theirs did not.
- **We report limitations honestly** (sample skew, the funnel-denominator correction). Neither reference deck flags a methodological limit.

## One conflict to be aware of

Both top decks use **category titles** ("User Personas", "Problem Framing Canvas", "Risks and Mitigations"). Our brief explicitly forbids that: *"don't write 'Problem' as the slide title, state the problem succinctly."* Our key-message titles follow our brief. **Keep ours** — the brief is explicit and is what this cohort is graded against.

Also: both reference decks are far denser than ours. "Crisp" shouldn't be taken so far that slides look thin next to these.

## Priority fixes, highest value first

1. **Wireframes/prototype slide** (slide 9) — the single biggest gap. Both top decks have one. Blocked on building the MVP.
2. **Numeric targets + north-star formula** (slide 10) — cheap, and its absence is conspicuous next to these.
3. **RICE table + rejected alternatives** (slide 8) — we did the work in `execution-plan.md`; it just isn't visible on a slide.
4. **Quantified business case with a stated assumption** (slide 7) — one line.
5. **System architecture strip** (slide 8 or 9) — shows the MVP is engineered, not hand-waved.
6. **Rollout phases with a kill threshold** — nice to have; hardest to fit in 10 slides.

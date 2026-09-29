# Six solution candidates, scored against the NextLeap marking criteria

Your three ideas plus the three from the earlier round, tested honestly. Creativity is scored the way the evaluator described it: **L1 does it address the identified problem · L2 is it differentiated in the market · L3 is there a competitive advantage a rival cannot copy next week.**

---

## First: what P2's completed tasks changed

The new answers are the most useful evidence in the project after the controlled test, and they move the scoring.

**Task B (a document, five steps):** the participant recalled a date, scrolled to it, failed, then **used surrounding photos as landmarks to work out that their own date estimate was wrong by a month**, and scrolled again. They never gave the app a clue at any point. The app was never in the loop.

**Task C (childhood photo):** face search **failed because a 20-year-old face does not match the current face cluster.** Then, unprompted: *"A feature to filter pictures based on non-recorded criteria like (a picture with child / black and white picture) would certainly help a lot."*

Two consequences:
1. **Face recognition degrades exactly as photos get old**, which is precisely our segment. Any solution built on enriching face recognition is building on the capability that breaks first.
2. A second unprompted feature request, this time for **narrowing by visual attributes nobody recorded**.

---

## The scoring

| Candidate | L1 · Solves our problem | L2 · Differentiated | L3 · Moat | Evidence | Verdict |
|---|---|---|---|---|---|
| **Yours 1 · Face + wardrobe recognition for better query** | **Weak.** Richer attributes help composition a little, but our proven root cause is time resolution. And P2 Task C shows face matching *fails* on old photos. | **No.** Google, Apple and Samsung all ship face grouping; Google already has some clothing search. | **Low.** Commodity capability. | Mixed, and partly contradicted by our own interview | ⛔ **Drop.** Also carries the heaviest privacy exposure (biometric regulation). |
| **Yours 2 · AI albums by day / place / trip / occasion** | **As written (nostalgia + share), no** — that is supply-driven rediscovery, a different job from demand-driven retrieval. **Reframed as "browse by trip and occasion instead of by date", yes** — it attacks the 74% scroll path. | Nostalgia framing duplicates Memories and auto-albums everywhere. Navigation framing is more novel. | Moderate. | P2 Task B *is* a person using surrounding photos as landmarks. Real support for the reframed version. | ⚠️ **Keep only if reframed.** Same as the earlier "memory anchors". |
| **Yours 3 · Documents space (IDs, receipts) via text recognition** | **Strong.** P1's PAN card, your ONE8 bill, **P2's recovery-password photo**, plus Aadhaar, passport and marksheet in the survey. 77% save utility photos often. | **Yes.** Apple has an OCR index but no documents surface; Google and Samsung have neither. An entire category of screenshot-search apps exists because of this gap. | **Moderate-high.** Needs the library, OCR at scale, and it ships where the failure happens. | Strong across all four sources | ✅ **Strongest of your three.** |
| Earlier 1 · Never guess silently (time disambiguation) | **Strongest.** The controlled test flips total failure to instant success, and P2 Task B is the same failure without search. | Real but subtle: everyone else guesses silently or cannot see your library. | Data + distribution. | Strongest evidence we have | ⚠️ Best evidenced, but **a mentor may read "add a clarifying question" as a UX fix rather than a product.** |
| Earlier 2 · Memory anchors | Attacks the widest behaviour. | Moderate. | Moderate. | No user asked for it | ⛔ Same as yours 2 |
| Earlier 3 · Narrow it down together | Solves the too-many-results case. | Moderate. | Low-moderate. | **Now much stronger: P2 asked for exactly this, unprompted.** | ⚠️ Promoted by the new evidence |

---

## The honest problem with picking any single one

- **Your S3 (documents)** has the clearest product shape and the best differentiation story, but it does not touch the time-resolution failure we actually proved.
- **Time disambiguation** has by far the best evidence, but reads small on its own. Arindam scores creativity partly on whether a competitor could ship it next week, and a clarifying question could be copied in a sprint.
- **Attribute narrowing** was just requested unprompted by a real user, but only solves the last step of the journey.

Each alone leaves a graded criterion exposed.

## Recommendation: one solution, three mechanisms

> **"Describe it the way you'd describe it to a friend."** A retrieval agent that takes several partial cues in one sentence, treats time as a range and asks one question when it is genuinely ambiguous, searches the words inside documents as a first-class cue, and lets you narrow by attributes nobody recorded — a child, black and white, a receipt.

This is **one** solution with a single interaction model, not three features bolted together. It earns each criterion:

| Criterion | How it is earned |
|---|---|
| **L1 · Solves the problem** | Time ambiguity (controlled test) · multi-cue composition (68% hold 2+) · no recovery from a miss (77% needed several tries) · documents under time pressure (P1, P2, your bill) |
| **L2 · Differentiated** | Google, Apple and Immich guess silently; ChatGPT and Gemini ask but cannot see your library; screenshot apps do text only. **Nothing accepts several fuzzy cues, admits uncertainty, and narrows on unrecorded attributes.** |
| **L3 · Moat** | Judging whether "last August" is ambiguous *for this user* needs their multi-year capture history. Runs on the existing index, so no new data leaves the device — the reason third-party apps stay niche. Ships where the failure happens. |
| **User pull** | Two unprompted requests from P2 alone: *"I just wish someone / any agent find it for me"* and *"a feature to filter pictures based on non-recorded criteria"*. |

**Your documents idea becomes the lead use case inside it**, not a separate product: the highest-stakes, most time-pressured retrievals are documents, so the demo leads with the bill and the PAN card.

**Deliberately still out:** face-recognition enrichment (breaks on old photos, heavy privacy cost) and the scroll-path redesign (74% reach, but too big for this iteration — named as the next bet).

---

## Deck structure: adopting yours

Your structure is better than what we have, for three reasons. Switching.

| # | Your structure | What changes vs. now |
|---|---|---|
| 1 | AI-powered engine: how the workflow works, in detail, with the link **and what we found** | Merges our current slides 3 and 4. Frees a slide. |
| 2 | Business metric decomposition into user behaviours and product outcomes, from engine evidence | Same as now |
| 3 | User research: survey, interviews, **personas**, observed retrieval tasks | Adds personas, which both top decks had and we lack |
| 4 | **Chosen target segment: market size, why this segment, impact** | **Its own slide.** Currently squeezed into the canvas. Directly serves the two criteria most submissions fail. |
| 5 | Root cause → what we found → problem definition | Merges our 6 and 7 |
| 6-7 | Solution rationale: three solutions, which one, selection criteria | Two slides, so the RICE table and the defence both get room |
| 8 | MVP: solution description, how it works, and user testing | Same |
| 9 | Success metrics: definition **and formulation** of each metric, and **data required** | **Its own slide.** Lets us add formulas, targets and event-level metrics. |
| 10 | Risks and limitations, guardrails, failure scenarios and edge cases | **Its own slide.** Fixes the one-line-risk pattern the evaluator calls out. |

**No title slide.** That is what frees the room, and the evaluator explicitly penalised a fellow for spending a slide on something that carried no new information. The deliverable links move to slide 1 alongside the engine.

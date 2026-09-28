# Evaluator feedback (Arindam, 19 Sep 2026) — what he asks for, and where we stand

Source: cohort feedback session, 139 min, 73-page transcript. Same brief family (Google Photos was one of the case studies). Evaluation: **3 mentors, blind, 15 criteria in 4 categories, normalised, 70% cutoff.**

---

## The ripple effect he describes

> "The segment definition is very broad, which is the very first signal that you have not thought deeply about it. Once the segment definition is very broad, the user research is also quite flawed… which means the insights are not deep enough, which means your problem definition is shallow, which means the solution you're coming up with is not very effective."

Segmentation → research → problem → solution. Everything downstream inherits the first mistake.

---

## Scorecard: his asks vs. our current state

| # | What he asks for | Us | Action |
|---|---|---|---|
| 1 | **Segment on objective, queryable criteria.** "If you write a data query feeding in this — give me a list of users who are X — would your data analyst be able to answer?" He rejected "wishlist users facing decision fatigue" as unqueryable. | ⚠️ Half-right. "3+ years, 10k+ items" is queryable. "Mixed libraries" is not yet operationalised. | Define the utility-photo criterion as a query, e.g. *≥15% of items are screenshots/documents in the last 12 months* |
| 2 | **Impact sizing / opportunity sizing.** Size the segment you chose and the potential gain. He explicitly rejected "67% of users face this difficulty" as *not* impact sizing. | ❌ **Missing entirely.** Named as one of the two most common failures. | **Add. Highest priority.** |
| 3 | **Problem definition must not be solution-led.** "No bundling suggestion exists" = defining the problem as the absence of your solution. Correct form: *"users are not able to log in with email and password because they are alien to these authentication mechanisms."* One problem, deep — not three. | ✅ Ours is behavioural and has the why. One problem. | Hold |
| 4 | **Metrics down to event level, mapped to your actual flow.** North star + guardrails alone is not enough. "Are there drop-offs from page 1 to page 2? Click-through rate on the buttons?" Plus data orientation: how would you compute it. "Think simply first" — start with how many people use it. | ❌ Ours is all high-level. No event metrics, no targets, no query logic. | **Add after the MVP flow exists** |
| 5 | **Risks with real depth.** "1-1 line for risks and mitigation. Three risks of one line, three mitigations of one line. That is what 90% of submissions are. That is not how you build products." Wants failure mode → root cause → detection signal → mitigation with trade-offs. | ❌ **We are exactly the pattern he criticises** — 4 risks, one line each. | **Rewrite to 4 columns** |
| 6 | **Creativity is scored at 3 levels:** (1) does it address the identified problem, (2) is it differentiated in market, (3) is there a competitive advantage a rival can't copy next week. | ⚠️ L1 ✅. L2 implied. L3 **not stated**. | **State the moat explicitly** |
| 7 | **Don't outsource thinking to AI.** "Evaluators are seasoned PMs working with AI day in and day out; it's very easy to figure out whether it is your work versus the AI's work." Expects 15-16+ days of effort. | ⚠️ Real exposure. | Own every number; be able to defend each slide unaided |
| 8 | **No leading/retrofitted survey questions.** "You've already introduced bias into your survey… you are retrofitting it." And: *"Users are 100% correct about the problem they're facing. They're mostly wrong about the solution."* | ✅ Survey was de-leaded. Better: our survey **contradicted** the review finding and we reported the contradiction rather than burying it. | Keep this visible — it is evidence of real research |
| 9 | **Presentation.** Don't waste a slide restating the given brief (he called it "a negative up front"). Define a term on the slide where it's used, not two slides later. Avoid text-heavy slides with no visual aid. Title = single message. | ✅ We restate nothing, titles are key messages, every slide has a visual. | Hold |
| 10 | **Discovery engine: ~1,000+ records, a couple of sources, must actually work when clicked.** One fellow's deployment errored live in the session and the evaluator got nothing from it. | ✅ 6,551 scraped, 3 sources, deployed. ⚠️ **Streamlit sleeps after inactivity.** | **Wake it before submitting; add a one-line note on the slide** |
| 11 | **MVP + usability test (new this cohort).** 3 users, task-based. Demo photos **may be AI-generated** (he confirmed). Summarise highlights on the slide, link to detail; don't make them watch long recordings. "What you'd change" = V2/V3 roadmap. | ⚠️ Planned, not built. | Per execution plan |
| 12 | Reassurance: usability testing **cannot lower your score** this cohort — "you can get brownie points for it, but it will not negatively impact your scores." | — | Removes the risk of experimenting |

---

## Three things to fix first

**1. Impact sizing — currently absent.** Something of this shape, with assumptions stated:

> Google Photos has ~1.5B MAU. If long-tenure deep-library users are ~20% (≈300M), and 52% of our survey hit this monthly or more, the affected population is ~150M users experiencing a failed retrieval each month. At even one prevented abandonment per user per month, this is the largest single reachable retrieval failure in the product.

Numbers must be labelled as estimates with the assumption shown. He is fine with assumptions; he is not fine with their absence.

**2. Risks — rewrite from one-liners to four columns.** For each: the failure mode, *why* it happens, **the signal that tells us it's happening**, and the mitigation including what it costs us. Example:

> **Risk:** The clarifying question fires when it shouldn't.
> **Root cause:** Confidence scoring treats an unambiguous phrase ("august 2025") as ambiguous, so every query gets interrupted.
> **Detection:** Clarifying questions per session >0.4, or skip rate on the question >50% — both visible from day one in the event log.
> **Mitigation and its cost:** Only fire below a 0.75 confidence threshold, hard cap one per session. Cost: we will miss some genuinely ambiguous cases and return a wider result set instead, which we accept because a false interruption is more damaging to trust than a wide result.

**3. State the competitive advantage.** Why Google and not a competitor:
- It queries the **existing index and on-device signals** — no new photo data leaves the device, which a third-party app cannot replicate because it doesn't have the library.
- The disambiguation improves from **longitudinal library data** (this user's own capture patterns) that only the host of a 15-year archive holds.
- It ships inside the surface where the failure already happens; a standalone app has to win distribution first (see the screenshot-search app category, which exists precisely because it can't).

---

## Two quotes worth keeping in mind

> "Your objective is not to get the top fellow badge. Your outcome is to break into a product role."

> "Research takes time. You ask people, do you buy? Do you wishlist? Yes, no. Okay, why not? One-line answer and end of user interview. That's not how user research works."

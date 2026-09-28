# Execution Plan — from problem statement to shipped MVP

*Written 28 Sep 2026. Deadline 7 Oct, 3:59 PM IST — so 6 Oct is the last full working day.*

---

## Step 0 — The problem we're solving (settled)

> People remember an old photo the way memory stores it — who, where, what was in frame, why they took it. Google Photos only accepts what memory doesn't keep: an exact date to scroll to, or the exact word the index holds. There's nowhere to put the fragments they *do* have, and no way to narrow after a miss — so the photo isn't lost, it's unreachable when needed, and people route around the app.

**Outcome we're moving:** share of demand-driven retrieval sessions (photo ≥ 1 year old) that end with the user opening the photo they came for, without guessing a date or a keyword.

---

## Step 1 — Opportunity mapping

Opportunities, straight from evidence — no invented ones.

| # | Opportunity | Evidence | Strength |
|---|---|---|---|
| **O1** | Ambiguous time is silently resolved to one reading, then hard-filtered | First-party test, **with control**: "last august" → 0 results; "august 2025" → instant | ★★★ Strongest |
| **O2** | Nowhere to put several partial cues at once | 68% hold 2+ cues; P2 named four in one breath | ★★★ |
| **O3** | A miss returns nothing instead of narrowing; every retry restarts | 77% needed several tries; 82% of review failures | ★★★ |
| **O4** | Scroll path is keyed on a date users don't have | 74% scroll first; 61% forgot the exact date | ★★★ (widest reach) |
| **O5** | Too many weakly-related results to evaluate | Query 5 returned ~64 items for one bill | ★★ |
| **O6** | Failure is invisible — users route around silently | 2 of 2 interviews re-did the task instead | ★★ (business case, not a feature) |

## Step 2 — Solution options, scored

RICE-style, honestly. Confidence reflects *evidence*, not enthusiasm.

| Solution | Reach | Impact | Confidence | Effort | Verdict |
|---|---|---|---|---|---|
| **S1 · Treat time as an uncertain range.** Never silently hard-filter. Ask one question, or search both windows and label them. | High | High | **Very high** — controlled first-party proof | Low | ✅ **Core of MVP** |
| **S2 · Compose multiple partial cues** (who + where + what + roughly when) into one query | High | High | High | Med | ✅ **Core of MVP** |
| **S3 · Recover from a near-miss** — narrow with one follow-up instead of returning zero | High | High | High | Med | ✅ **Core of MVP** |
| **S4 · Explain why each result matched** | All | Med | Med | Low | ✅ **Cheap add** — also repairs Ask Photos trust damage |
| **S5 · Life landmarks** ("around my sister's wedding") | ? | High? | **Low — no user asked for this; it was my idea** | High | ⛔ **Cut from MVP.** Honest call: unvalidated. Revisit only if P3–P6 raise it unprompted |
| **S6 · Fix the scroll path itself** (browse by something other than date) | **Highest — 74%** | High | Med | **High** | ⏭ **Next bet, not this one.** Too big for 9 days; named explicitly in the deck as the follow-on |

**The bet: S1 + S2 + S3 + S4.** One sentence: *let people describe the photo in their own words, treat time as fuzzy, say why things matched, and ask one question instead of giving up.*

> **Correction to the current deck:** slide 8 lists "swap dates for life landmarks" as a pillar. That's S5 — my invention, not user evidence. It comes out and is replaced by S1, which is the best-evidenced thing we have.

## Step 3 — Hypothesis and success criteria (fixed *before* building)

**Hypothesis**
> If people can describe a photo in natural language with partial cues, and the system treats time as a range, explains its matches, and asks one narrowing question instead of returning nothing — then users who previously failed to find a photo will find it in fewer attempts.

**Success criteria — set now so we can't move the goalposts later**

| | Pass | Fail |
|---|---|---|
| Retrieval | ≥ 2 of 3 testers find their target | ≤ 1 of 3 |
| Effort | Fewer attempts than their Google Photos baseline | Same or more |
| Perception | ≥ 2 of 3 say unprompted they'd use it | Mixed or negative |
| Trust | Nobody asks for the plain grid back | Anyone does → the "why matched" framing failed |

**What would falsify the bet:** testers still needing 3+ attempts, or the clarifying question reading as friction rather than help. Both are real possibilities and both get reported honestly in the deck.

## Step 4 — MVP scope (MoSCoW)

**Must**
- Natural-language input accepting several cues at once
- Time parsed into a *range with confidence*, never a silent filter
- Ambiguous time → **one** clarifying question, or both windows shown and labelled
- Ranked results, each with a plain-language "matched because…"
- Near-miss recovery: a narrowing follow-up instead of zero results
- A seeded demo library realistic enough to reproduce the real failure (including bills, IDs, screenshots)

**Should**
- Side-by-side "classic keyword search" toggle so the improvement is visible, not asserted
- Shareable public link, works on a phone

**Could**
- Confidence score shown per result
- Query history

**Won't (this iteration — and say so on the slide)**
- Real Google Photos integration (no API access; out of scope)
- Life landmarks (S5, unvalidated)
- Scroll-path redesign (S6, next bet)
- Face recognition / on-device ML

## Step 5 — Design the flows

1. **Happy path:** user types a multi-cue description → system shows 3–5 ranked matches, each with why → user opens the right one.
2. **Ambiguous-time path:** "bill from last August" → *"Do you mean August 2025 or August 2026?"* → one tap → results. **This is the money demo — it's the exact failure you reproduced.**
3. **Near-miss path:** nothing confident → system shows closest candidates *and* asks one narrowing question, never a dead end.

## Step 6 — Build (Sep 29 – Oct 2)

Stack, all free: Python + Gemini free tier for cue extraction and ranking, seeded photo metadata, Streamlit Cloud for deployment (same pattern as the discovery engine, which already works).

Approach: the demo library is metadata-rich synthetic data modelled on real interview tasks — P1's receipt, your ONE8 bill scenario, a PAN card, college photos. Every test task maps to something a real participant actually looked for.

## Step 7 — Test with users (Oct 3)

- 3 testers, drawn from the interview pool (P1 and P2 both already agreed to a follow-up)
- Each gets **their own real task** from their interview — not a generic one
- Baseline first: attempt in Google Photos, record attempts and time. Then the MVP. Same measures.
- Record: attempts, time, found?, where it broke, unprompted reactions
- **No leading questions** — the de-leaded script rules apply

## Step 8 — Decide, then report honestly (Oct 4)

Score against Step 3's criteria. Three outcomes, all reportable:
- **Pass** → deck reports the win with numbers
- **Partial** → report what worked and what didn't, and what changes next
- **Fail** → report it as a fail and explain what the evidence actually supports

A graduation deck that honestly reports a partial result is stronger than one that claims a win it didn't measure.

## Step 9 — Metrics framework (refined to what we built)

- **North star:** vague-memory retrieval success rate (photo ≥ 1 yr, opened and used)
- **Leading:** share of queries with 2+ cues · clarifying-question acceptance rate · near-miss recovery within 2 turns · median attempts to found
- **Diagnostic:** zero-result rate on descriptive queries · **new document photo within 10 min of a failed document search** (the "routing around" proxy, from P1 and P2) · scroll depth before searching
- **Guardrails:** latency · clarifying questions per session (friction ceiling) · opt-out rate · privacy complaints

## Step 10 — Risks

| Risk | Mitigation |
|---|---|
| Confident wrong matches erode trust further | "Matched because…" on every result; keep classic results available — Google's own fix after the Ask Photos pause |
| The clarifying question feels like friction | Hard cap: one question, only when confidence is genuinely split. Measured as a guardrail |
| Demo library makes it look easier than reality | Seed it with real failure cases from interviews; state the limitation plainly on the slide |
| Small, network-skewed sample (n=31, 2 interviews, all India, tech-adjacent) | State it as a limitation; propose a logged A/B on the north star as the real validation |
| Privacy — personal photos to an LLM | Design queries over the existing index and metadata; no new photo data leaves the device in the proposed production shape |

---

## Day-by-day

| Date | Focus | Done when |
|---|---|---|
| **Mon 29 Sep** | Lock the bet · PRD-lite · design 3 flows · seed data spec. P3/P4 interviews in parallel | Flows sketched, demo library spec'd |
| **Tue 30 Sep** | Build: cue extraction + ranked search over seeded library | Happy path works locally |
| **Wed 1 Oct** | Build: time disambiguation, near-miss recovery, "why matched" | All three flows work |
| **Thu 2 Oct** | Deploy to Streamlit · QA on phone · dry-run the tasks yourself | Public link works on mobile |
| **Fri 3 Oct** | Test with 3 users (baseline + MVP) | 3 sessions recorded |
| **Sat 4 Oct** | Synthesise results · quick fixes only | Verdict against Step 3 criteria |
| **Sun 5 Oct** | Rebuild deck around final narrative | All 10 slides real, no placeholders |
| **Mon 6 Oct** | Visual QA · font/contrast check · export PDF · verify every link in incognito | Submission-ready |
| **Tue 7 Oct** | Submit in the morning | Done before 3:59 PM IST |

**Biggest schedule risk:** user testing on Fri 3 Oct depends on three people being available. **Confirm those slots on Mon 29 Sep**, not later — it's the one thing that can't be compressed.

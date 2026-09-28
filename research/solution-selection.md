# Three solutions, one selected, and the defence

Root cause being solved: **the app silently guesses the one thing users are least sure about (when), turns that guess into a hard filter, and offers no way back.** Plus two supporting failures: no way to combine several partial cues, and no recovery from a near-miss.

---

## The three options

Deliberately attacking three *different* points in the journey, not three flavours of the same idea.

### Solution 1 — "Never guess silently"
**Where it acts: the query interpretation step.**

A layer over the existing search. When a query contains something the system is not confident about, most often a relative time reference, it stops resolving it silently. Instead it either asks one targeted question ("August 2025 or August 2026?") or returns both windows clearly labelled. It accepts several partial cues in one sentence, shows why each result matched, and on a miss offers one narrowing follow-up instead of an empty grid.

### Solution 2 — "Memory anchors"
**Where it acts: the browse path.**

Replaces the date axis entirely. The app derives a personal timeline of landmarks from the library itself (trips from location clusters, events from density spikes, a house move from a shift in home location, a new person who starts appearing) and lets people navigate by those instead of by month: "the Kodaikanal trip", "around when we moved", "when the baby arrived".

### Solution 3 — "Narrow it down together"
**Where it acts: the evaluate and recover steps.**

Takes a rich description, then instead of a flat grid returns a small set of high-signal candidates with structured differences surfaced, and lets the user eliminate by attribute: "not this person", "not indoors", "earlier than this". Twenty questions, played with images.

---

## Scoring

RICE. **Confidence reflects strength of evidence, not enthusiasm.** Effort is inverse (lower is better).

| | Reach | Impact | Confidence | Effort | **RICE** |
|---|---|---|---|---|---|
| **S1 · Never guess silently** | 8 — every search containing a fuzzy cue | 9 — control test flipped total failure to instant success | **9 — strongest evidence in the project** | 2 — rides the existing index | **324** |
| **S2 · Memory anchors** | **10 — reaches the 74% who scroll, the widest behaviour we found** | 7 — could replace the broken axis, unproven | **4 — nobody asked for this; it was our inference** | 8 — landmark detection, naming, a new browse surface | **35** |
| **S3 · Narrow it down together** | 6 — only fires when results come back ambiguous | 6 — solves the 64-result case, not the zero-result case | 6 — real but thin: "too many results" was 4% of tagged failures | 6 — new result UI plus attribute extraction | **36** |

### The tension worth naming

**S2 has the highest reach of anything we found and still loses decisively.** 74% of people scroll, and that path is the one truly broken at scale. It loses on confidence: no user asked for landmark navigation, it came from us. Scoring it honestly at 4 rather than flattering it is the difference between a real prioritisation and a rigged one.

S1 wins on **evidence and cheapness**, not on reach. That is a legitimate reason to go first, and it is the correct first bet precisely because it can be proven quickly. **S2 is named as the next bet**, not discarded.

---

## Defending S1

### Level 1 — Does it address the identified problem?

Directly, and it is the only option that addresses all three failures at once.

| Failure | How S1 answers it |
|---|---|
| Ambiguous time resolved silently, applied as a hard filter | It stops resolving silently. Asks, or shows both windows labelled. |
| Nowhere to put several partial cues | One sentence carries who, where, what and roughly when together. |
| No recovery from a near-miss | A miss produces a narrowing question, never an empty grid. |

**The proof already exists.** In our controlled test, `"bill from last august"` returned nothing while `"bill from august 2025"` returned an instant itemised answer. Same photo, same content word, only the date phrasing changed. One clarifying question would have converted that failure into a success in a single turn.

### Level 2 — Is it differentiated in the market?

| Product | Natural-language search | Handles time ambiguity | Asks before guessing | Has your library |
|---|---|---|---|---|
| Google Photos (Ask Photos) | Yes | **No — silently picks one** | No | Yes |
| Apple Photos | Yes | No | No | Yes |
| Immich / Ente (CLIP) | Yes | No time reasoning at all | No | Yes |
| Screenshot-search apps | Text only | No | No | Partial |
| ChatGPT / Gemini | Yes | Often asks | **Yes** | **No** |

The differentiation is not "AI search", which is table stakes and which Google already shipped. It is **treating uncertainty as something to surface rather than resolve.** Every product in that table either guesses silently or cannot see your photos. Nothing does both.

### Level 3 — What stops a competitor copying it next week?

**The interaction is copyable in a week, and we should say so rather than pretend otherwise.** The defensibility sits underneath it:

1. **Disambiguation needs the whole archive.** Deciding whether "last August" is ambiguous *for this user* requires knowing whether they have photos in both Augusts, whether there was a gap, whether they travelled. That judgement is computed from a 15-year capture history. Only the holder of the archive can make it; a competitor starting today has no history to reason over.
2. **It runs on the existing index, so nothing new leaves the device.** A third-party app has to ingest the library first, which is a privacy cost users refuse to pay. This is exactly why the screenshot-search app category stays niche despite solving a real need.
3. **Distribution at the moment of failure.** It lives on the surface where the retrieval already fails. Google's own Ask Photos reached a scale standalone tools never will, for this reason alone.

**The moat is data and distribution, not the feature.** That is the honest claim and it is the stronger one.

### Impact sizing for this specific solution

| Step | Figure |
|---|---|
| Users in segment hitting a failed retrieval monthly | **~273M** (see problem framing canvas) |
| Share of tagged failures where a fair clue was misread | **82%** (69 of 84) → the population S1 targets |
| = Addressable failures per month | **~224M** |
| Conservative conversion to success (assume S1 rescues 1 in 5) | **20%** |
| = **Additional successful retrievals per month** | **~45M** |

All figures are estimates with the assumption shown. The 20% conversion is deliberately pessimistic: the control test converted a total failure into an instant success, so the real question is what share of failures are time-driven, which the MVP test is designed to inform.

### What would make us kill it

- **Clarifying questions per session above 0.4**, or a skip rate on the question above 50%. That means we are interrupting people who were not actually ambiguous, and the cure is worse than the disease.
- **Fewer than 2 of 3 MVP testers** find their own photo in fewer attempts than their Google Photos baseline.
- **Anyone asking for the plain grid back.** That is the Ask Photos failure repeating, and it would mean the "why it matched" framing has not earned trust.

# Tip of My Tongue — AI-native MVP

Named for the state people arrive in: you are sure the photo exists, you can
half describe it, and the description will not resolve into the thing itself.

It wears Google Photos' colours and type deliberately. The argument is that
this behaviour belongs inside Photos, so it should be possible to mistake the
surface for Photos while reading the interaction as new.

One change to photo search: **show the person what you understood before you
search, hold the uncertain parts loosely, and ask once.**

```bash
pip install -r mvp/requirements.txt
streamlit run mvp/app.py
```

## Why it behaves this way

In a controlled test on the live Google Photos app:

| query | result |
|---|---|
| `bill from last august` | nothing, then photos from August 2026 |
| `bill from august 2025` | the bill, instantly, itemised down to the dishes |

Same photo. Same content word, `bill`. Only the date wording changed. "Last
August" was read as one specific year and turned into a hard filter, and the
bill was from the other one. Reading the photo was never the problem.

So the rule everything here is built around:

> A cue the app is confident about may narrow the results.
> A cue it is unsure about may only re-order them.
> It never filters on a guess.

## The three things to try

1. **Several clues at once** — `restaurant bill, dinner with friends, around a year ago`
   Every clue becomes a chip. The vague date is marked *maybe*, so it lifts the
   right bill to the top without excluding anything.

2. **The question** — `bill from last august`
   The library holds a bill in August 2025 *and* a different one in August 2026.
   Rather than picking one silently, it asks once. Answering turns the guess
   into a fact and the result becomes confident.

3. **A near miss** — `something from the trip`
   Nothing matches confidently, so you get the closest few plus one question
   about something people never think to type.

Then try the part that matters most: on any wrong result, hit **Not this one**
and say *why*. On the query above, rejecting the 2026 cafe bill as *wrong time*
puts the right bill first — a second, independent route to the same photo.

## Design decisions worth knowing

**It works with no API key.** The cue reader has two paths: Gemini when
`GEMINI_API_KEY` is set, and a deterministic built-in reader otherwise. The
built-in path is not a stub, it is the guaranteed one, so the deployed link
still works when the free quota runs out. Nobody should meet a dead app.

**At most one question that we start.** A second question the moment the first
is answered is an interrogation, which is the top risk on the risk slide, so the
cap is enforced in code rather than tuned. The near-miss loop is deliberately
exempt: a rejection is the person asking us to try again, so acting on it is
invited rather than imposed.

**Questions are ordered by what people actually recall.** Across 83 free-recall
photo descriptions in desk research, people volunteered indoor/outdoor 69 times,
how many people 64, who 56 and where 54, while an exact date proved notably less
useful than the time of day. The question asked is whichever of those best
splits the candidates currently on screen.

**Options come from the candidates, never the library.** A menu built from your
whole history is a filter drawer, which Google already has and people already do
not use. "Goa or Udaipur?" when those are the only two places among your near
misses is a narrowing question. The difference is the whole design.

**Real photos for photos, drawn glyphs for paperwork.** The 92 photo items use
CC0 stock images in `scenes/`, fetched once by `tools/fetch_scenes.py` and
committed, so the deployed app depends on nobody else's server. Documents and
screenshots stay drawn on purpose: a real photograph of a bill or an ID card is
someone's actual bill or ID card, and the page and phone glyphs let you see
what kind each result is without reading the label, which the interface leans
on. If `scenes/` is missing, everything falls back to the drawn version and the
app still runs.

**The library is seeded, and seeded honestly.** 132 items across 1998–2026,
carrying failures that came out of the research: two bills in different Augusts,
an ID card, a recovery-codes screenshot, black-and-white childhood photos with
no usable metadata, and a waterfall nobody wrote the location down for.

## Files

| file | what it does |
|---|---|
| `app.py` | the Streamlit interface |
| `cues.py` | sentence to cues with confidences. Gemini + rule-based fallback |
| `search.py` | scoring, the ambiguity check, narrowing questions, the near-miss loop |
| `library.py` | the 132-item demo library |
| `thumbs.py` | thumbnails: the CC0 photo if there is one, else drawn |
| `scenes/` | the CC0 photos, plus `CREDITS.md` |
| `tools/fetch_scenes.py` | refills `scenes/`. Run by hand, never by the app |

Each runs standalone for a quick sanity check:

```bash
python mvp/library.py
python mvp/thumbs.py
```

## Deploying

Streamlit Community Cloud, free tier:

1. Push to a public GitHub repo.
2. New app, pointed at `mvp/app.py`.
3. Optional: Settings, then Secrets, then `GEMINI_API_KEY = "..."`.
   Leave it out and it runs on the built-in reader.

`pillow` is now in both `requirements.txt` files. It has to be: Streamlit Cloud
reads the root one by default, and without Pillow the app cannot render a
single thumbnail and dies on boot.

The free tier sleeps after inactivity, so open the link once before sharing it.

## Limits, stated plainly

- A seeded 132-item library is not a real 75,000-item one. Ambiguity is rarer in
  a small library, which flatters these results. This is on the risk slide.
- Scoring is transparent keyword and metadata matching, not embeddings. That is
  deliberate for a prototype whose argument is about interaction rather than
  retrieval quality, and it means every result can explain itself.
- The clarifying question triggers on an unresolved year only. The same
  machinery extends to place and people; the year is where the research showed
  the failure.

"""The Composer — say what you remember, see what the app understood.

Run locally:  streamlit run mvp/app.py

The point of this prototype is one behaviour, not a feature list: the app shows
you its reading of your sentence before it searches, treats anything it is
unsure about as a preference rather than a filter, and asks exactly one question
when an unresolved detail is the only thing standing between you and the photo.
"""
import os
import sys
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# Streamlit Cloud keeps keys in st.secrets; mirror into env for llm.py
try:
    for _k in ("GEMINI_API_KEY", "GEMINI_MODELS"):
        if _k in st.secrets and not os.environ.get(_k):
            os.environ[_k] = st.secrets[_k]
except Exception:
    pass

import cues as cuemod          # noqa: E402
import search as searchmod     # noqa: E402
import thumbs                  # noqa: E402
from library import LIBRARY, TODAY  # noqa: E402

st.set_page_config(page_title="The Composer", page_icon="🔎", layout="wide")

BLUE, RED, INK, GREY = "#1a73e8", "#d93025", "#202124", "#5f6368"

st.markdown("""
<style>
  .block-container {padding-top: 2.2rem; max-width: 1180px;}
  .chip {display:inline-block; padding:4px 11px; margin:3px 5px 3px 0;
         border-radius:14px; font-size:13px; line-height:1.5;}
  .chip-hard {background:#e8f0fe; color:#1a73e8; border:1px solid #1a73e8;}
  .chip-soft {background:#f1f3f4; color:#5f6368; border:1px dashed #bdc1c6;}
  .why {display:inline-block; padding:2px 8px; margin:2px 4px 2px 0;
        border-radius:10px; background:#f1f3f4; color:#5f6368; font-size:11.5px;}
  .cap {font-size:13.5px; line-height:1.35; color:#202124; margin:6px 0 2px;}
  .meta {font-size:11.5px; color:#5f6368;}
  .ask {background:#e8f0fe; border:1px solid #1a73e8; border-radius:10px;
        padding:14px 16px; margin:6px 0 10px;}
  .lede {color:#5f6368; font-size:15px; margin-top:-8px;}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------- state --
S = st.session_state
S.setdefault("q", "")
S.setdefault("year", None)
S.setdefault("narrow", None)
S.setdefault("dropped", set())


def ask_query(text):
    """A fresh question clears anything we had previously resolved."""
    S.q, S.year, S.narrow, S.dropped = text, None, None, set()


# -------------------------------------------------------------------- head --
st.markdown("## The Composer")
st.markdown(
    '<p class="lede">Say what you remember. You will see what the app understood '
    'before it searches, and it will ask only when it genuinely cannot tell.</p>',
    unsafe_allow_html=True)

st.write("")
c1, c2, c3, _ = st.columns([1.5, 1.7, 1.6, 1.4])
with c1:
    if st.button("Several clues at once", use_container_width=True):
        ask_query("restaurant bill, dinner with friends, around a year ago")
with c2:
    if st.button("The question  ←  the one to watch", use_container_width=True):
        ask_query("bill from last august")
with c3:
    if st.button("A near miss", use_container_width=True):
        ask_query("something from the trip, cannot remember where")

q = st.text_input(
    "What are you looking for?",
    value=S.q,
    placeholder="the bill from that dinner, somewhere near a waterfall, my sister at the wedding…",
    label_visibility="collapsed",
)
if q != S.q:
    ask_query(q)

st.divider()

if not S.q.strip():
    st.caption(
        f"{len(LIBRARY)} items in this demo library, "
        f"{LIBRARY[-1]['date'][:4]}–{LIBRARY[0]['date'][:4]}. "
        "Seeded to carry the retrieval failures that came out of the research, "
        "so the things that break here are the things that broke for real people."
    )
    st.stop()

# ------------------------------------------------------------------ search --
use_llm = bool(os.environ.get("GEMINI_API_KEY"))
cues = cuemod.parse(S.q, use_llm=use_llm)

# Chips the user switched off stop contributing entirely.
chips = [c for c in cuemod.to_chips(cues) if c["label"] not in S.dropped]
live = dict(cues)
kept = {c["field"] for c in chips}
labels = {c["label"] for c in chips}
live["content"] = [w for w in cues["content"] if w in labels]
live["people"] = [p for p in cues["people"] if p in labels]
for f in ("place", "setting", "kind"):
    if f not in kept:
        live[f] = None
if "bw" not in kept:
    live["bw"] = False
if "date" not in kept:
    live["date"] = None

ans = searchmod.answer(LIBRARY, live, year_override=S.year, narrow=S.narrow)

# ------------------------------------------------------------------- chips --
left, right = st.columns([3, 1.15])
with left:
    st.markdown("**What the app understood**")
    row = st.columns(max(1, min(len(chips), 7)) or 1)
    html = "".join(
        f'<span class="chip chip-{"hard" if c["hard"] else "soft"}">{c["label"]}'
        f'{"" if c["hard"] else " ?"}</span>'
        for c in chips)
    st.markdown(html or '<span class="meta">nothing recognisable yet</span>',
                unsafe_allow_html=True)
    st.markdown(
        '<span class="meta">Solid = certain enough to narrow on. '
        'Dashed with a “?” = a preference only; it can lift a photo up the list, '
        'never push one off it.</span>', unsafe_allow_html=True)

    if chips:
        with st.expander("Change what it understood"):
            for c in cuemod.to_chips(cues):
                on = c["label"] not in S.dropped
                new = st.checkbox(f'{c["label"]}', value=on, key=f"chip_{c['label']}")
                if new != on:
                    if new:
                        S.dropped.discard(c["label"])
                    else:
                        S.dropped.add(c["label"])
                    st.rerun()

with right:
    st.markdown("**Reading**")
    st.markdown(
        f'<span class="meta">cues by {"Gemini" if cues.get("source") == "gemini" else "built-in reader"}'
        f'<br>{len(ans["results"])} of {len(LIBRARY)} items matched<br>'
        f'verdict: {ans["verdict"]}</span>', unsafe_allow_html=True)

# --------------------------------------------------------------- the question
if ans["ask"]:
    a = ans["ask"]
    st.markdown(
        f'<div class="ask"><b>{a["question"]}</b><br>'
        f'<span class="meta">{a["because"]}</span></div>', unsafe_allow_html=True)
    cols = st.columns(min(len(a["options"]), 4))
    for i, opt in enumerate(a["options"]):
        with cols[i % len(cols)]:
            if st.button(f'{opt["label"]}', key=f'opt{i}', use_container_width=True,
                         help=opt.get("hint")):
                if a["type"] == "year":
                    S.year = opt["value"]
                else:
                    S.narrow = (a["key"], opt["value"])
                st.rerun()
    st.caption("You can also just ignore this and look at the results below — "
               "the question never blocks the answer.")

if S.year or S.narrow:
    said = f"{S.year}" if S.year else f"“{S.narrow[1]}”"
    c_a, c_b = st.columns([4, 1])
    with c_a:
        st.success(f"Narrowed to {said}, because you told us.")
    with c_b:
        if st.button("Undo", use_container_width=True):
            S.year, S.narrow = None, None
            st.rerun()

# ----------------------------------------------------------------- results --
res = ans["results"]
if not res:
    st.warning("Nothing matched. Try one more detail — what was around it, "
               "who was there, or whether it was indoors.")
    st.stop()

if ans["verdict"] == "near":
    st.markdown(f"**Closest {min(len(res), 8)}** — nothing here is a confident match.")
else:
    st.markdown(f"**{min(len(res), 12)} best matches**")

show = res[: 8 if ans["verdict"] == "near" else 12]
for chunk_start in range(0, len(show), 4):
    cols = st.columns(4)
    for col, r in zip(cols, show[chunk_start:chunk_start + 4]):
        it = r["item"]
        with col:
            st.image(thumbs.png(it), use_container_width=True)
            st.markdown(f'<div class="cap">{it["title"]}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<span class="meta">{it["date"]} · {it["kind"]}</span>',
                unsafe_allow_html=True)
            st.markdown(
                "".join(f'<span class="why">{w}</span>' for w in r["why"][:3]),
                unsafe_allow_html=True)

# ----------------------------------------------------------------- sidebar --
with st.sidebar:
    st.markdown("### What this is")
    st.write(
        "A prototype of one change to photo search: show the person what you "
        "understood, hold the uncertain parts loosely, and ask one question "
        "when it is the only thing in the way."
    )
    st.markdown("### Why it behaves this way")
    st.write(
        "In a test on the live Google Photos app, “bill from last august” "
        "returned nothing, while “bill from august 2025” returned the bill "
        "instantly. Same photo, same word “bill” — only the date wording "
        "changed. “Last August” was quietly read as one year and turned into a "
        "hard filter. That is the failure this prototype is built to avoid."
    )
    st.markdown("### The rule")
    st.write(
        "A cue the app is confident about may narrow the results. A cue it is "
        "unsure about may only re-order them. It never filters on a guess."
    )
    st.markdown("### This library")
    kinds = {}
    for i in LIBRARY:
        kinds[i["kind"]] = kinds.get(i["kind"], 0) + 1
    st.write(
        f"{len(LIBRARY)} items · " + " · ".join(f"{v} {k}s" for k, v in kinds.items())
    )
    st.caption(
        "None of these are real photos. Each is a record with the metadata a "
        "photo app already holds; thumbnails are drawn at run time."
    )
    st.markdown("### Cue reading")
    st.caption(
        ("Gemini is connected." if use_llm else
         "Running on the built-in reader. Gemini is optional here on purpose — "
         "the app must still work when the free quota runs out.")
    )
    st.caption(f"Today, for this demo, is {TODAY.isoformat()}.")

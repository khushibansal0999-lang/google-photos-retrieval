"""The Composer — say what you remember, see what the app understood.

Run locally:  streamlit run mvp/app.py

Three behaviours, in the order they matter:

  1. Before it searches, the app shows its reading of your sentence. Anything
     it is unsure of is marked, and you can downgrade or drop any of it. This
     is the part that has to come first, because the failure we reproduced on
     the real product was invisible: it returned confident, wrong photos, and
     nothing on screen told the user a guess had been made.

  2. It asks one question, and only when an unresolved detail genuinely splits
     the candidates in front of you. Never a menu built from your whole
     library — that is a filter drawer, and people already do not use it.

  3. "Close, but not it" is treated as information rather than as a dead end.
     Telling us why a result is wrong is the fastest way to the right one.
"""
import os
import sys
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

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

st.markdown("""
<style>
  .block-container {padding-top: 1.6rem; max-width: 1200px;}
  .chip {display:inline-block; padding:3px 10px; margin:2px 4px 2px 0;
         border-radius:13px; font-size:13px;}
  .c-sure {background:#e8f0fe; color:#1a73e8; border:1px solid #1a73e8;}
  .c-maybe{background:#fef7e0; color:#b45309; border:1px dashed #f9ab00;}
  .why {display:inline-block; padding:2px 7px; margin:2px 3px 0 0; border-radius:9px;
        background:#f1f3f4; color:#5f6368; font-size:11px;}
  .cap {font-size:13px; line-height:1.3; color:#202124; margin:5px 0 1px;}
  .meta{font-size:11.5px; color:#5f6368;}
  .lede{color:#5f6368; font-size:15px; margin-top:-10px;}
  .ask {background:#e8f0fe; border:1px solid #1a73e8; border-radius:10px;
        padding:12px 15px; margin:4px 0 8px;}
  div[data-testid="stImage"] img {border-radius:8px;}
</style>
""", unsafe_allow_html=True)

S = st.session_state
S.setdefault("q", "")
S.setdefault("year", None)
S.setdefault("narrow", None)
S.setdefault("asked", [])       # dimensions already used, so we never repeat one
S.setdefault("level", {})       # cue label -> "sure" | "maybe" | "off"
S.setdefault("rejected", [])    # (item id, reason)
S.setdefault("note", "")


def ask_query(text):
    S.q, S.year, S.narrow = text, None, None
    S.asked, S.level, S.rejected, S.note = [], {}, [], ""


# ------------------------------------------------------------------- header -
st.markdown("### The Composer")
st.markdown('<p class="lede">Say what you remember. You will see what the app '
            'understood before it searches.</p>', unsafe_allow_html=True)

q = st.text_input("Search your photos", value=S.q,
                  placeholder="the bill from that dinner · somewhere near a waterfall · my sister at the wedding",
                  label_visibility="collapsed")
if q != S.q:
    ask_query(q)

e1, e2, e3, _ = st.columns([1.4, 1.7, 1.3, 2.0])
with e1:
    if st.button("Several clues", use_container_width=True):
        ask_query("restaurant bill, dinner with friends, around a year ago")
with e2:
    if st.button("The question  ←  watch this", use_container_width=True):
        ask_query("bill from last august")
with e3:
    if st.button("A near miss", use_container_width=True):
        ask_query("something from the trip")

# --------------------------------------------------------------- home page --
if not S.q.strip():
    st.divider()
    st.markdown("**Your photos**")
    st.caption(f"{len(LIBRARY)} items, {LIBRARY[-1]['date'][:4]}–{LIBRARY[0]['date'][:4]}. "
               "A demo library seeded with the retrieval failures that came out of the "
               "research, so the things that break here are things that broke for real people.")
    for start in range(0, 18, 6):
        for col, it in zip(st.columns(6), LIBRARY[start:start + 6]):
            with col:
                st.image(thumbs.png(it), use_container_width=True)
                st.markdown(f'<span class="meta">{it["date"]}</span>', unsafe_allow_html=True)
    st.stop()

# ------------------------------------------------------------------ search --
use_llm = bool(os.environ.get("GEMINI_API_KEY"))
cues = cuemod.parse(S.q, use_llm=use_llm)
all_chips = cuemod.to_chips(cues)

live = dict(cues)
kept = set()
for c in all_chips:
    lvl = S.level.get(c["label"], "sure" if c["conf"] >= 0.8 else "maybe")
    if lvl != "off":
        kept.add(c["field"])
labels_on = {c["label"] for c in all_chips
             if S.level.get(c["label"], "x") != "off"}
live["content"] = [w for w in cues["content"] if w in labels_on]
live["people"] = [p for p in cues["people"] if p in labels_on]
for f in ("place", "setting", "kind"):
    if f not in kept:
        live[f] = None
if "bw" not in kept:
    live["bw"] = False
if "date" not in kept:
    live["date"] = None

ans = searchmod.answer(LIBRARY, live, year_override=S.year, narrow=S.narrow)
res = ans["results"]
for rid, reason in S.rejected:
    item = next((i for i in LIBRARY if i["id"] == rid), None)
    if item:
        res, S.note = searchmod.reject(res, item, reason)

# ------------------------------------------------------------------- chips --
left, right = st.columns([3.1, 1])
with left:
    st.markdown("**What the app understood**")
    html = ""
    for c in all_chips:
        lvl = S.level.get(c["label"], "sure" if c["conf"] >= 0.8 else "maybe")
        if lvl == "off":
            continue
        cls = "c-sure" if lvl == "sure" else "c-maybe"
        html += f'<span class="chip {cls}">{c["label"]}{"" if lvl=="sure" else " ?"}</span>'
    st.markdown(html or '<span class="meta">nothing recognisable yet</span>',
                unsafe_allow_html=True)
    st.markdown('<span class="meta">Solid = certain enough to narrow on. '
                'Dashed = a preference only; it lifts a photo up the list, never '
                'pushes one off it.</span>', unsafe_allow_html=True)

    with st.expander("Change what it understood"):
        st.caption("Certain narrows the results. Maybe only re-orders them.")
        for c in all_chips:
            cur = S.level.get(c["label"], "sure" if c["conf"] >= 0.8 else "maybe")
            pick = st.radio(c["label"], ["Certain", "Maybe", "Not important"],
                            index=["sure", "maybe", "off"].index(cur),
                            key=f"lv_{c['label']}", horizontal=True)
            new = {"Certain": "sure", "Maybe": "maybe", "Not important": "off"}[pick]
            if new != cur:
                S.level[c["label"]] = new
                st.rerun()
with right:
    st.markdown("**Reading**")
    st.markdown(f'<span class="meta">cues by '
                f'{"Gemini" if cues.get("source")=="gemini" else "built-in reader"}<br>'
                f'{len(res)} of {len(LIBRARY)} matched<br>{ans["verdict"]}</span>',
                unsafe_allow_html=True)

# ---------------------------------------------------------- the one question -
ask = ans["ask"]
if ask and ask.get("key") in S.asked:
    ask = None
if ask and not S.rejected:
    st.markdown(f'<div class="ask"><b>{ask["question"]}</b><br>'
                f'<span class="meta">{ask["because"]}</span></div>',
                unsafe_allow_html=True)
    cols = st.columns(min(len(ask["options"]), 4))
    for i, opt in enumerate(ask["options"]):
        with cols[i % len(cols)]:
            if st.button(str(opt["label"]), key=f"opt{i}", use_container_width=True,
                         help=opt.get("hint")):
                if ask["type"] == "year":
                    S.year = opt["value"]
                else:
                    S.narrow = (ask["key"], opt["value"])
                    S.asked.append(ask["key"])
                st.rerun()
    st.caption("Ignoring this is fine — the results below are already there.")

if S.year or S.narrow or S.rejected:
    a, b = st.columns([4, 1])
    with a:
        bits = []
        if S.year:
            bits.append(f"narrowed to {S.year}")
        if S.narrow:
            bits.append(f"narrowed to “{S.narrow[1]}”")
        if S.rejected:
            bits.append(S.note or f"{len(S.rejected)} ruled out")
        st.success(" · ".join(bits).capitalize())
    with b:
        if st.button("Start over", use_container_width=True):
            S.year, S.narrow, S.asked, S.rejected, S.note = None, None, [], [], ""
            st.rerun()

# ----------------------------------------------------------------- results --
if not res:
    st.warning("Nothing left. Start over, or try one more detail — what was "
               "around it, who was there, whether it was indoors.")
    st.stop()

st.markdown(f'**{"Best matches" if ans["verdict"]=="confident" else "Closest to what you said"}** '
            f'<span class="meta">— tell me why one is wrong and I will use it</span>',
            unsafe_allow_html=True)

show = res[:12]
for start in range(0, len(show), 4):
    for col, r in zip(st.columns(4), show[start:start + 4]):
        it = r["item"]
        with col:
            st.image(thumbs.png(it), use_container_width=True)
            st.markdown(f'<div class="cap">{it["title"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="meta">{it["date"]} · {it["kind"]} · '
                        f'{it["tod"] or "—"}</span>', unsafe_allow_html=True)
            st.markdown("".join(f'<span class="why">{w}</span>' for w in r["why"][:3]),
                        unsafe_allow_html=True)
            with st.popover("Not this one", use_container_width=True):
                st.caption("Why not? This is the most useful thing you can tell me.")
                for code, label in searchmod.REJECTIONS:
                    if st.button(label, key=f"rj_{it['id']}_{code}",
                                 use_container_width=True):
                        S.rejected.append((it["id"], code))
                        st.rerun()

# ----------------------------------------------------------------- sidebar --
with st.sidebar:
    st.markdown("### What this is")
    st.write("A prototype of one change to photo search: show people what you "
             "understood, hold the uncertain parts loosely, and ask once.")
    st.markdown("### Why it behaves this way")
    st.write("On the live Google Photos app, “bill from last august” returned "
             "nothing, while “bill from august 2025” returned the bill instantly. "
             "Same photo, same word “bill” — only the date wording changed. "
             "“Last August” was quietly read as one year and turned into a hard "
             "filter. That is the failure this avoids.")
    st.markdown("### The rule")
    st.write("A cue it is confident about may narrow the results. A cue it is "
             "unsure about may only re-order them. It never filters on a guess.")
    st.markdown("### What it asks about")
    st.write("In the order people actually recall things: indoors or outdoors, "
             "how many people, who, where, time of day. Across 83 free-recall "
             "photo descriptions those beat an exact date every time.")
    st.markdown("### This library")
    kinds = {}
    for i in LIBRARY:
        kinds[i["kind"]] = kinds.get(i["kind"], 0) + 1
    st.write(f"{len(LIBRARY)} items · " + " · ".join(f"{v} {k}s" for k, v in kinds.items()))
    st.caption("None are real photos. Each is a record with the metadata a photo "
               "app already holds; thumbnails are drawn at run time.")
    st.caption("Gemini is connected." if use_llm else
               "Running on the built-in reader — Gemini is optional on purpose, so "
               "the link still works when the free quota runs out.")
    st.caption(f"Today, for this demo, is {TODAY.isoformat()}.")

"""Tip of My Tongue — say what you remember, see what the app understood.

The name is the cognitive phenomenon this product is built around: you are sure
the photo exists, you can half describe it, and the description will not
resolve into the thing itself. That is the state people arrive in.

It wears Google Photos' own colours and type on purpose. The argument is that
this behaviour belongs inside Photos, so it should be possible to mistake this
for Photos while reading the interaction as new.

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

st.set_page_config(page_title="Tip of My Tongue", page_icon=thumbs.logo(),
                   layout="wide")

# The pinwheel, inline so it stays crisp and costs no network request.
PINWHEEL = """<svg width="30" height="30" viewBox="0 0 48 48">
  <path d="M24 24 V4 A10 10 0 0 1 24 24 Z" fill="#4285F4"/>
  <path d="M24 24 H44 A10 10 0 0 1 24 24 Z" fill="#EA4335"/>
  <path d="M24 24 V44 A10 10 0 0 1 24 24 Z" fill="#FBBC04"/>
  <path d="M24 24 H4  A10 10 0 0 1 24 24 Z" fill="#34A853"/>
</svg>"""

# Google Photos' surface: Roboto, a pill search field, 8px thumbnails, and the
# four brand colours used only where they mean something.
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
  /* Streamlit sets Source Sans on almost everything, so this has to win. It
     deliberately leaves <span> alone: Streamlit's icons are ligature spans in
     an icon font, and overriding those prints "keyboard_double_arrow_right"
     where the arrow should be. Spans inherit from these parents anyway. */
  .stApp, .stApp div, .stApp p, .stApp li, .stApp label,
  .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5,
  .stApp button, .stApp input, .stApp textarea
        {font-family:'Roboto','Helvetica Neue',Arial,sans-serif !important;}
  .block-container {padding-top: 1.4rem; max-width: 1200px;}
  .brand {display:flex; align-items:center; gap:11px; margin-bottom:2px;}
  .brand h1 {font-size:21px; font-weight:500; color:#3c4043; margin:0;
             letter-spacing:.1px;}
  .chip {display:inline-block; padding:4px 12px; margin:2px 5px 2px 0;
         border-radius:16px; font-size:13px; font-weight:500;}
  .c-sure {background:#e8f0fe; color:#1967d2; border:1px solid #d2e3fc;}
  .c-maybe{background:#fef7e0; color:#b06000; border:1px dashed #fdd663;}
  .why {display:inline-block; padding:2px 8px; margin:3px 3px 0 0; border-radius:10px;
        background:#f1f3f4; color:#5f6368; font-size:11px;}
  .cap {font-size:13px; line-height:1.35; color:#202124; margin:6px 0 1px;}
  .meta{font-size:11.5px; color:#5f6368;}
  .lede{color:#5f6368; font-size:14px; margin:0 0 12px 41px;}
  .ask {background:#e8f0fe; border:1px solid #d2e3fc; border-radius:12px;
        padding:13px 16px; margin:4px 0 8px;}
  /* the Photos search field: a grey pill that turns white and lifts on focus */
  div[data-testid="stTextInput"] input {
        background:#f1f3f4; border:1px solid transparent; border-radius:24px;
        padding:11px 20px; font-size:15px; color:#202124;}
  div[data-testid="stTextInput"] input:focus {
        background:#fff; box-shadow:0 1px 6px rgba(32,33,36,.28);}
  div[data-testid="stImage"] img {border-radius:8px;}
  /* Cap the result thumbnails. Those still use st.columns because each card
     carries a "Not this one" control, and a stacked column would otherwise
     stretch a 300px drawing across the whole screen. Streamlit injects its own
     emotion styles after this block and sets max-width:100% on the image, so
     the cap goes on the container and needs !important or it loses the
     cascade. */
  div[data-testid="stImageContainer"],
  div[data-testid="stImageContainer"] > img {
        max-width:220px !important; margin-left:auto; margin-right:auto;}
  .grid {display:grid; gap:14px; margin-top:4px;
         grid-template-columns:repeat(auto-fill, minmax(118px, 1fr));}
  .grid figure {margin:0;}
  .grid img {width:100%; aspect-ratio:1; object-fit:cover; border-radius:8px;
             display:block;}
  .grid figcaption {font-size:11.5px; color:#5f6368; margin-top:4px;}
  .stButton button {border-radius:18px; font-size:13px; font-weight:500;
        border:1px solid #dadce0; color:#3c4043;}
  .stButton button:hover {background:#f1f3f4; border-color:#dadce0; color:#1967d2;}
  /* the per-result reject trigger sits under a caption, so it matches it */
  div[data-testid="stPopover"] button {font-size:13px; border-radius:18px;}
</style>
""", unsafe_allow_html=True)

S = st.session_state
S.setdefault("q", "")
S.setdefault("qbox", "")
S.setdefault("shown", 24)   # how much of the library the home grid is showing
S.setdefault("year", None)
S.setdefault("narrow", None)
S.setdefault("asked", [])       # dimensions already used, so we never repeat one
S.setdefault("level", {})       # cue label -> "sure" | "maybe" | "off"
S.setdefault("rejected", [])    # (item id, reason)
S.setdefault("note", "")


def ask_query(text):
    S.q, S.year, S.narrow = text, None, None
    S.asked, S.level, S.rejected, S.note = [], {}, [], ""


def use_example(text):
    """Load an example into the box.

    This has to run as an on_click callback, not inline after the button. The
    search box owns the key "qbox", and Streamlit refuses to let you write to a
    widget's key once that widget has been drawn this run. Callbacks fire
    before the script re-runs, which is the only moment the write is legal.

    Getting this wrong is what a tester hit: they clicked an example, typed
    their own search, pressed Enter, and watched their words vanish and the
    example come back. They assumed the app was broken, and they were right to.
    """
    S.qbox = text
    ask_query(text)


# ------------------------------------------------------------------- header -
st.markdown(f'<div class="brand">{PINWHEEL}<h1>Tip of My Tongue</h1></div>',
            unsafe_allow_html=True)
st.markdown('<p class="lede">The photo you can half remember. Say what you have '
            'got, and see what the app understood before it searches.</p>',
            unsafe_allow_html=True)

st.text_input("Search your photos", key="qbox",
              placeholder="the bill from that dinner · somewhere near a waterfall · my sister at the wedding",
              label_visibility="collapsed")
if S.qbox != S.q:
    ask_query(S.qbox)

e1, e2, e3, _ = st.columns([1.4, 1.7, 1.3, 2.0])
with e1:
    st.button("Several clues", use_container_width=True, on_click=use_example,
              args=("restaurant bill, dinner with friends, around a year ago",))
with e2:
    st.button("The question  ←  watch this", use_container_width=True,
              on_click=use_example, args=("bill from last august",))
with e3:
    st.button("A near miss", use_container_width=True, on_click=use_example,
              args=("something from the trip",))

# --------------------------------------------------------------- home page --
if not S.q.strip():
    st.divider()
    st.markdown("**Your photos**")
    shown = min(S.shown, len(LIBRARY))
    st.caption(f"Showing {shown} of {len(LIBRARY)} items, "
               f"{LIBRARY[-1]['date'][:4]}–{LIBRARY[0]['date'][:4]}. "
               "A demo library seeded with the retrieval failures that came out of the "
               "research, so the things that break here are things that broke for real people.")
    # One real CSS grid, not st.columns. Streamlit stacks columns below about
    # 640px, and a stacked column makes every thumbnail full-bleed -- a tester
    # saw a drawn phone blown up to the width of the screen, sitting in a field
    # of grey, and read it as empty space. auto-fill reflows instead: six across
    # on a laptop, two or three on a phone, never one enormous one.
    cells = "".join(
        f'<figure class="g-cell"><img src="data:image/jpeg;base64,{thumbs.b64(it)}" '
        f'alt="{it["title"]}"><figcaption>{it["date"]}</figcaption></figure>'
        for it in LIBRARY[:shown])
    st.markdown(f'<div class="grid">{cells}</div>', unsafe_allow_html=True)

    # Paged, not all at once. Every thumbnail is inlined into the HTML as
    # base64, so the whole library in one go is close to a megabyte before the
    # page can paint -- and a tester already sat through ten seconds of spinner
    # on a cold boot. Sixty at a time keeps the first paint cheap and still
    # lets anyone walk the whole library.
    if shown < len(LIBRARY):
        left = len(LIBRARY) - shown
        a, b, _ = st.columns([1.5, 1.5, 4])
        if a.button(f"Show {min(60, left)} more", use_container_width=True):
            S.shown = shown + 60
            st.rerun()
        if b.button(f"Show all {len(LIBRARY)}", use_container_width=True):
            S.shown = len(LIBRARY)
            st.rerun()
    elif len(LIBRARY) > 24:
        if st.button("Back to the top of the library"):
            S.shown = 24
            st.rerun()
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

# Re-label the chips from what the search actually ran on. When someone answers
# "which August?", the date stops being a guess, and the screen has to say so.
# Leaving it reading "year unknown" after they just told us the year is the
# precise failure this whole product is an argument against -- a tester caught
# us doing it, which was fair.
resolved = {c["field"]: c for c in cuemod.to_chips(ans["cues"])}
all_chips = [resolved.get(c["field"], c) if c["field"] == "date" else c
             for c in all_chips]

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

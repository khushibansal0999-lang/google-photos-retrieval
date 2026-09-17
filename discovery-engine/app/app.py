"""Discovery Engine UI — explore, compare and ask questions of tagged user evidence.

Run: streamlit run app/app.py
"""
import json, sys
from collections import Counter
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import streamlit as st
from dotenv import load_dotenv

# Streamlit Community Cloud stores keys in st.secrets; mirror them into env for llm.py
try:
    for _k in ("GEMINI_API_KEY", "GEMINI_MODELS"):
        if _k in st.secrets and not os.environ.get(_k):
            os.environ[_k] = st.secrets[_k]
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from schema import PHOTO_TYPES, MEMORY_CUES, FAILURE_STAGES, WORKAROUNDS  # noqa: E402
from llm import generate_json, generate_text_stream  # noqa: E402

load_dotenv(ROOT.parent / ".env")
TAGGED = ROOT / "data" / "processed" / "tagged.jsonl"

# Validated colour-blind-safe palette (dataviz reference instance)
BLUE, ORANGE, AQUA, YELLOW, MAGENTA = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"
SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

LABELS = {
    "cannot_express": "Can't express what they remember",
    "app_misunderstands": "App misunderstands the clue",
    "too_many_results": "Too many results to evaluate",
    "cannot_refine": "Can't refine a failed search",
    "wrong_metadata": "Date/location metadata wrong",
    "content_not_indexed": "Content type not indexed (text/docs/screenshots)",
    "gave_up": "Gave up",
    "succeeded": "Succeeded",
    "not_applicable": "N/A",
}

st.set_page_config(page_title="Photo Retrieval Discovery Engine", page_icon="🔍", layout="wide")


@st.cache_data
def load() -> pd.DataFrame:
    rows = []
    if not TAGGED.exists():
        return pd.DataFrame()
    for l in TAGGED.open():
        if not l.strip():
            continue
        r = json.loads(l); t = r.pop("tags")
        rows.append({**r, **{k: v for k, v in t.items() if not k.startswith("_")}})
    df = pd.DataFrame(rows)
    df["source_group"] = df.source.str.replace("reddit_.*", "reddit", regex=True)
    return df


def hbar(series: pd.Series, title: str, color=BLUE, labels=None):
    s = series.sort_values()
    names = [labels.get(i, i) if labels else i for i in s.index]
    fig = go.Figure(go.Bar(x=s.values, y=names, orientation="h", marker_color=color,
                           marker_line_width=0, text=s.values, textposition="outside"))
    fig.update_layout(title=title, height=max(260, 28 * len(s) + 80), margin=dict(l=10, r=40, t=40, b=10),
                      xaxis=dict(showgrid=True, gridcolor="#eee", zeroline=False), yaxis=dict(showgrid=False),
                      plot_bgcolor="white", paper_bgcolor="white", bargap=0.35)
    return fig


def cue_counts(df, col):
    return pd.Series(Counter(c for cs in df[col] for c in cs if c != "none_stated"))


df = load()
if df.empty:
    st.warning("No tagged data yet. Run `python src/extract.py` first.")
    st.stop()
rel_all = df[df.is_relevant].copy()
if "problem_class" not in rel_all.columns:
    rel_all["problem_class"] = "unclassified"
rel_all["problem_class"] = rel_all["problem_class"].fillna("unclassified")
PC_LABELS = {"vague_memory_retrieval": "Vague-memory retrieval (core)", "ui_navigation_regression": "UI / navigation regression",
             "data_missing_sync": "Data missing / sync", "feature_request": "Feature request",
             "general_praise_or_success": "Praise / success", "other": "Other", "unclassified": "Unclassified"}

SECTIONS = ["Overview", "Explore evidence", "Compare segments", "Ask the evidence", "How it works"]
with st.sidebar:
    st.header("Section")
    section = st.radio("Section", SECTIONS, label_visibility="collapsed")
    st.divider()
    st.header("Scope")
    pc_choice = st.multiselect("Problem class", list(PC_LABELS), default=["vague_memory_retrieval"],
                               format_func=lambda x: PC_LABELS.get(x, x),
                               help="A second AI pass separated genuine memory→index failures from UI regressions and data loss.")
    st.caption("Tip: add 'UI / navigation regression' to see how the layout changes broke *browsing* as a retrieval path.")
rel = rel_all[rel_all.problem_class.isin(pc_choice)].copy() if pc_choice else rel_all.copy()

st.title("🔍 Photo Retrieval Discovery Engine")
st.caption(
    f"{len(df):,} public posts/reviews analysed · {len(rel):,} about retrieving a specific photo · "
    "sources: Reddit, Google Play, App Store. Every record was tagged by Gemini along the retrieval journey: "
    "**Remember → Express → Understand → Evaluate → Refine**."
)


# ---------------------------------------------------------------- Overview
if section == "Overview":
    c0, c1, c2, c3, c4 = st.columns(5)
    c0.metric("Records analysed", f"{len(df):,}")
    c2.metric("Retrieval-relevant", f"{len(rel_all):,}", f"{len(rel_all)/len(df):.0%} of total")
    c1.metric("In current scope", f"{len(rel):,}")
    fails = rel[~rel.failure_stage.isin(["succeeded", "not_applicable"])]
    c3.metric("Describe a failure", f"{len(fails):,}")
    c4.metric("Frustrated", f"{(rel.sentiment=='frustrated').mean():.0%}")

    l, r = st.columns(2)
    with l:
        st.plotly_chart(hbar(fails.failure_stage.value_counts(), "Where retrieval breaks down", labels=LABELS),
                        use_container_width=True)
    with r:
        st.plotly_chart(hbar(rel.photo_type.value_counts().drop("not_specified", errors="ignore"),
                             "What kind of photo they were looking for"), use_container_width=True)

    st.subheader("What users remember vs. what they've forgotten")
    rem, forg = cue_counts(rel, "cues_remembered"), cue_counts(rel, "cues_forgotten")
    cues = sorted(set(rem.index) | set(forg.index), key=lambda c: -(rem.get(c, 0) + forg.get(c, 0)))
    fig = go.Figure()
    fig.add_bar(name="Remembered", x=cues, y=[rem.get(c, 0) for c in cues], marker_color=BLUE)
    fig.add_bar(name="Forgotten", x=cues, y=[forg.get(c, 0) for c in cues], marker_color=ORANGE)
    fig.update_layout(barmode="group", height=360, plot_bgcolor="white", paper_bgcolor="white",
                      margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1),
                      yaxis=dict(gridcolor="#eee"), bargap=0.3)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Photo type × failure stage")
    ct = pd.crosstab(fails.photo_type, fails.failure_stage)
    ct = ct.loc[ct.sum(1).sort_values(ascending=False).index]
    ct.columns = [LABELS.get(c, c) for c in ct.columns]
    fig = px.imshow(ct, text_auto=True, color_continuous_scale=SEQ_BLUE, aspect="auto")
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("What kind of problem is it? (all retrieval-relevant records)")
    st.plotly_chart(hbar(rel_all.problem_class.value_counts(), "", color=MAGENTA, labels=PC_LABELS), use_container_width=True)

    if "memory_index_gap" in rel.columns:
        gaps = rel[rel.memory_index_gap.fillna("") != ""]
        if len(gaps):
            st.subheader("Memory ↔ index gaps (what the user remembers vs. what the app needs)")
            for _, r in gaps.sort_values("score", ascending=False, na_position="last").head(40).iterrows():
                st.markdown(f"- **{r.photo_type}** — {r.memory_index_gap}")

    st.subheader("Workarounds people fall back on")
    st.plotly_chart(hbar(rel.workaround.value_counts().drop("none_mentioned", errors="ignore"), ""),
                    use_container_width=True)

# ---------------------------------------------------------------- Explore
if section == "Explore evidence":
    f1, f2, f3, f4 = st.columns(4)
    src = f1.multiselect("Source", sorted(rel.source_group.unique()))
    pt = f2.multiselect("Photo type", PHOTO_TYPES)
    fs = f3.multiselect("Failure stage", FAILURE_STAGES, format_func=lambda x: LABELS.get(x, x))
    cue = f4.multiselect("Remembered cue", MEMORY_CUES)
    q = st.text_input("Keyword in text / quote / scenario")
    sub = rel
    if src: sub = sub[sub.source_group.isin(src)]
    if pt: sub = sub[sub.photo_type.isin(pt)]
    if fs: sub = sub[sub.failure_stage.isin(fs)]
    if cue: sub = sub[sub.cues_remembered.apply(lambda cs: any(c in cs for c in cue))]
    if q: sub = sub[sub.apply(lambda r: q.lower() in (r.text + r.key_quote + r.retrieval_scenario).lower(), axis=1)]
    st.write(f"**{len(sub)} records**")
    for _, r in sub.head(200).iterrows():
        with st.container(border=True):
            st.markdown(f"**{r.retrieval_scenario or r.title or '(no scenario)'}**")
            st.markdown(f"> {r.key_quote}")
            meta = f"`{r.source}` · photo: `{r.photo_type}` · fails at: `{LABELS.get(r.failure_stage, r.failure_stage)}` · " \
                   f"remembers: `{', '.join(r.cues_remembered) or '—'}` · forgot: `{', '.join(r.cues_forgotten) or '—'}` · workaround: `{r.workaround}`"
            st.caption(meta)
            if r.failure_detail: st.caption(f"Mechanism: {r.failure_detail}")
            with st.expander("Full text"):
                st.write(r.text)
                if r.url: st.markdown(f"[source]({r.url})")

# ---------------------------------------------------------------- Compare
if section == "Compare segments":
    st.markdown("Pick two slices of the evidence and compare how retrieval fails for each.")
    dim = st.selectbox("Slice by", ["photo_type", "source_group", "time_since_photo", "query_style"])
    opts = sorted(rel[dim].dropna().unique())
    a, b = st.columns(2)
    A = a.selectbox("Segment A", opts, index=0)
    B = b.selectbox("Segment B", opts, index=min(1, len(opts) - 1))
    dA, dB = rel[rel[dim] == A], rel[rel[dim] == B]
    for col, d, name in ((a, dA, A), (b, dB, B)):
        col.metric(f"{name}", f"{len(d)} records")
        col.plotly_chart(hbar(d.failure_stage.value_counts(), "Failure stage", labels=LABELS), use_container_width=True)
        col.plotly_chart(hbar(cue_counts(d, "cues_remembered"), "Cues remembered", color=AQUA), use_container_width=True)
        col.plotly_chart(hbar(d.workaround.value_counts(), "Workaround", color=YELLOW), use_container_width=True)
        col.markdown("**Representative quotes**")
        for qt in d.key_quote.head(4): col.markdown(f"> {qt}")

# ---------------------------------------------------------------- Ask
if section == "Ask the evidence":
    st.markdown("Ask a research question. Gemini first decides which slice of the tagged evidence answers it, "
                "then writes a grounded answer citing real user quotes.")
    examples = ["What do users remember about photos they can't find, and what have they forgotten?",
                "How do screenshot retrieval failures differ from travel-photo failures?",
                "What do people type when they don't know how to describe the photo?",
                "Which failure stage is most common for photos older than a year?",
                "What workarounds do parents use to find kids' photos?"]
    question = st.text_area("Question", placeholder=examples[0])
    st.caption("Try: " + " · ".join(f"_{e}_" for e in examples))
    if st.button("Ask", type="primary") and question.strip():
        FILTER_SCHEMA = {
            "type": "object",
            "properties": {
                "photo_type": {"type": "array", "items": {"type": "string", "enum": PHOTO_TYPES}},
                "failure_stage": {"type": "array", "items": {"type": "string", "enum": FAILURE_STAGES}},
                "cues_remembered": {"type": "array", "items": {"type": "string", "enum": MEMORY_CUES}},
                "workaround": {"type": "array", "items": {"type": "string", "enum": WORKAROUNDS}},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "rationale": {"type": "string"},
            },
            "required": ["photo_type", "failure_stage", "cues_remembered", "workaround", "keywords", "rationale"],
            "additionalProperties": False,
        }
        with st.spinner("Selecting evidence…"):
            filt = generate_json(
                "You route research questions to slices of a tagged dataset of user feedback about finding photos. "
                "Return filters (empty arrays = no filter on that dimension). Keywords are substrings to match in text. "
                "Prefer broad filters; the answering step will read the records.",
                question, FILTER_SCHEMA)
        sub = rel
        if filt["photo_type"]: sub = sub[sub.photo_type.isin(filt["photo_type"])]
        if filt["failure_stage"]: sub = sub[sub.failure_stage.isin(filt["failure_stage"])]
        if filt["cues_remembered"]: sub = sub[sub.cues_remembered.apply(lambda cs: any(c in cs for c in filt["cues_remembered"]))]
        if filt["workaround"]: sub = sub[sub.workaround.isin(filt["workaround"])]
        if filt["keywords"]:
            kw = [k.lower() for k in filt["keywords"]]
            m = sub.apply(lambda r: any(k in (r.text + r.retrieval_scenario).lower() for k in kw), axis=1)
            if m.sum() >= 5: sub = sub[m]
        if len(sub) < 5: sub = rel
        sub = sub.sort_values("score", ascending=False, na_position="last").head(120)
        st.caption(f"Evidence slice: {len(sub)} records · {filt['rationale']}")

        evidence = "\n\n".join(
            f"[{r.id}] source={r.source} photo={r.photo_type} fail={r.failure_stage} remembers={r.cues_remembered} "
            f"forgot={r.cues_forgotten} workaround={r.workaround}\nscenario: {r.retrieval_scenario}\ntext: {r.text[:900]}"
            for _, r in sub.iterrows())
        stats = {
            "failure_stage": sub.failure_stage.value_counts().to_dict(),
            "photo_type": sub.photo_type.value_counts().to_dict(),
            "cues_remembered": cue_counts(sub, "cues_remembered").to_dict(),
            "cues_forgotten": cue_counts(sub, "cues_forgotten").to_dict(),
            "workaround": sub.workaround.value_counts().to_dict(),
        }
        with st.spinner("Synthesising…"):
            box = st.empty(); acc = ""
            for txt in generate_text_stream(
                "You are a product researcher answering questions ONLY from the evidence provided. "
                "Structure: 1) direct answer in 2-3 sentences, 2) 3-5 findings each backed by verbatim quotes with [id] citations, "
                "3) counts from the stats where useful, 4) what the evidence does NOT tell us. Never invent quotes.",
                f"QUESTION: {question}\n\nSTATS (this slice):\n{json.dumps(stats)}\n\nEVIDENCE:\n{evidence}"):
                acc += txt; box.markdown(acc)
        with st.expander("Records used"):
            st.dataframe(sub[["id", "source", "photo_type", "failure_stage", "key_quote", "url"]], use_container_width=True)

# ---------------------------------------------------------------- How it works
if section == "How it works":
    st.markdown("""
### Pipeline
1. **Collect** — Reddit (r/googlephotos + 10 retrieval-specific searches, posts + comments), Google Play (US/IN/GB/CA/AU), App Store (same countries).
2. **Pre-filter** — cheap regex drops reviews that are obviously about storage/billing/backup.
3. **Extract** — every remaining record is sent to Gemini (free tier) with a strict JSON schema. It decides *is this about retrieving a specific photo?* and, if so, tags:
   photo type · cues **remembered** vs **forgotten** · query style · failure stage · mechanism · workaround · time since photo · segment hint · key verbatim quote.
4. **Compare** — the tags map to the retrieval journey (Remember → Express → Understand → Evaluate → Refine), so failure modes can be counted and cross-tabbed instead of summarised.
5. **Ask** — a question is routed to an evidence slice, then answered with grounded, cited quotes.

### Why not sentiment analysis
Sentiment tells you people are unhappy. The schema tells you *which stage* of the retrieval journey broke, *for which photo types*, *given which memory cues* — which is what a decomposition of "successful vague-memory retrieval" needs.
""")
    st.code((ROOT / "src" / "schema.py").read_text()[:3000], language="python")

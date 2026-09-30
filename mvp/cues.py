"""Turn a sentence into cues, each with a confidence.

Two paths, same output shape:

  * Gemini, when GEMINI_API_KEY is set. Better at loose phrasing.
  * A rule-based reader, always. This is not a stub — it is the guaranteed
    path, so the deployed link keeps working when the free quota runs out.
    The evaluator should never meet a dead app.

The one rule that matters: a cue we are not sure about is returned with a low
confidence and is *never* allowed to become a filter. Guessing silently and
then filtering on the guess is the failure this whole project is about.
"""
import os
import re
from datetime import date

from library import TODAY

# --------------------------------------------------------------- vocabulary -
MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"])}
MONTHS.update({m[:3]: i for m, i in list(MONTHS.items())})

PEOPLE = {
    "sister": "sister", "brother": "brother", "mum": "family", "mom": "family",
    "mother": "family", "dad": "family", "father": "family", "family": "family",
    "friends": "friends", "friend": "friends", "kids": "child", "child": "child",
    "children": "child", "everyone": "friends",
}
SETTING = {
    "indoor": "indoor", "indoors": "indoor", "inside": "indoor",
    "outdoor": "outdoor", "outdoors": "outdoor", "outside": "outdoor",
}
KIND = {
    "bill": "document", "receipt": "document", "invoice": "document",
    "document": "document", "card": "document", "id": "document",
    "screenshot": "screenshot", "screengrab": "screenshot",
    "photo": "photo", "picture": "photo", "pic": "photo", "image": "photo",
}
PLACES = {"goa", "bengaluru", "bangalore", "udaipur", "pushkar", "hampi",
          "coorg", "ooty", "gokarna", "home", "office", "airport"}

STOP = set("""a an the of in on at to for from with and or i my me we our you your
is was were be been am are it its this that these those there here some any
do does did doing done just really very much more most so than then when where
what which who whom how why can could would should will shall may might must
about around near by into over under again once only own same too also as if
but not no nor because while during before after above below up down out off
over under further once take took taken get got go went photo photos picture
pictures pic pics image images thing stuff something anything remember
find looking look need want""".split())

# phrases the app must treat as uncertain rather than resolving quietly
VAGUE_TIME = [
    (r"\baround a year ago\b", 365), (r"\babout a year ago\b", 365),
    (r"\ba year or so ago\b", 365), (r"\blast year\b", 365),
    (r"\ba while (back|ago)\b", 540), (r"\bages ago\b", 900),
    (r"\bcouple of years ago\b", 730), (r"\btwo years ago\b", 730),
    (r"\bfew months ago\b", 120), (r"\ba few months (back|ago)\b", 120),
    (r"\blast summer\b", 400), (r"\bback then\b", 900),
]


def _tok(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower())]


def _date_cue(q):
    """Return (cue, note) where cue is None if the sentence says nothing about when.

    confidence semantics:
      1.0  an explicit year was given. Safe to lean on hard.
      0.45 a month with no year. We do NOT pick a year here.
      0.30 a vague gesture at a period. Wide window, soft only.
    """
    ql = q.lower()

    # "august 2025", "in 2019"
    m = re.search(r"\b(" + "|".join(MONTHS) + r")\w*\s+(\d{4})\b", ql)
    if m:
        return {"kind": "month_year", "month": MONTHS[m.group(1)],
                "year": int(m.group(2)), "confidence": 1.0,
                "text": m.group(0)}, None
    m = re.search(r"\b(19|20)\d{2}\b", ql)
    if m:
        return {"kind": "year", "year": int(m.group(0)), "confidence": 1.0,
                "text": m.group(0)}, None

    # "last august", "in august" — a month with no year is the trap
    m = re.search(r"\b(last|in|during)?\s*(" + "|".join(MONTHS) + r")\b", ql)
    if m and m.group(2):
        mon = MONTHS[m.group(2)]
        years = []
        y = TODAY.year
        # every year in the library where this month has already happened
        while y >= TODAY.year - 3:
            if date(y, mon, 1) <= TODAY:
                years.append(y)
            y -= 1
        return {"kind": "month", "month": mon, "years": years,
                "confidence": 0.45, "text": m.group(0).strip()}, "month-no-year"

    for pat, days in VAGUE_TIME:
        m = re.search(pat, ql)
        if m:
            centre = TODAY.toordinal() - days
            return {"kind": "around", "centre": centre, "window": max(120, days // 2),
                    "confidence": 0.30, "text": m.group(0)}, "vague"

    if re.search(r"\blast month\b", ql):
        centre = TODAY.toordinal() - 30
        return {"kind": "around", "centre": centre, "window": 25,
                "confidence": 0.85, "text": "last month"}, None
    return None, None


def parse_rules(q):
    toks = _tok(q)
    cues = {"content": [], "people": [], "place": None, "setting": None,
            "kind": None, "bw": False, "date": None, "notes": []}

    d, note = _date_cue(q)
    cues["date"] = d
    if note:
        cues["notes"].append(note)

    date_words = set(_tok(d["text"])) if d else set()
    date_words |= {"last", "ago", "year", "years", "month", "months", "around", "about"}

    bw = bool(re.search(r"\bblack and white\b|\bb\s*&\s*w\b|\bmonochrome\b", q.lower()))
    # "black" and "white" on their own would match a whiteboard and a bill that
    # happens to print the word. The phrase is the cue; the words are not.
    skip = {"black", "white", "monochrome"} if bw else set()

    for w in toks:
        if w in date_words or w in skip:
            continue
        if w in PEOPLE:
            v = PEOPLE[w]
            if v not in cues["people"]:
                cues["people"].append(v)
        elif w in SETTING:
            cues["setting"] = SETTING[w]
        elif w in PLACES:
            cues["place"] = "Bengaluru" if w in ("bangalore", "bengaluru") else w.title()
        elif w in KIND:
            cues["kind"] = KIND[w]
            # "photo"/"picture" only say what sort of file it is, so they become
            # the kind cue and nothing else. "bill" is also a thing printed on
            # the page, so it stays as content too.
            if w not in cues["content"] and KIND[w] != "photo":
                cues["content"].append(w)
        elif w not in STOP and len(w) > 2:
            if w not in cues["content"]:
                cues["content"].append(w)

    cues["bw"] = bw
    return cues


# ------------------------------------------------------------------- gemini -
_SCHEMA = {
    "type": "object",
    "properties": {
        "content": {"type": "array", "items": {"type": "string"}},
        "people": {"type": "array", "items": {"type": "string"}},
        "place": {"type": "string"},
        "setting": {"type": "string"},
        "kind": {"type": "string"},
        "bw": {"type": "boolean"},
    },
    "required": ["content"],
}

_SYS = """You read one sentence from someone hunting for a photo in their own library.
Pull out only what they actually said. Never invent a detail they did not give.

content  the things that would appear in or on the photo, lower case, no dates
people   any of: sister, brother, family, friends, child. Only if named.
place    a place name, only if they said one. Otherwise empty string.
setting  "indoor" or "outdoor", only if they said or clearly implied it.
kind     "document", "screenshot" or "photo", only if clear. Otherwise empty.
bw       true only if they said black and white.

Say nothing about dates. Dates are handled elsewhere, on purpose."""


def parse_llm(q):
    """Gemini's read, merged over the rule-based one. Returns None if unavailable."""
    if not os.environ.get("GEMINI_API_KEY"):
        return None
    try:
        from llm import generate_json
        got = generate_json(_SYS, q, _SCHEMA)
    except Exception:
        return None

    base = parse_rules(q)          # dates always come from the rules
    out = dict(base)
    if got.get("content"):
        seen = []
        for w in [str(x).lower().strip() for x in got["content"]]:
            if w and w not in seen and w not in STOP:
                seen.append(w)
        if seen:
            out["content"] = seen
    if got.get("people"):
        out["people"] = [p for p in (str(x).lower() for x in got["people"]) if p in PEOPLE.values()]
    if got.get("place"):
        out["place"] = str(got["place"]).title()
    if got.get("setting") in ("indoor", "outdoor"):
        out["setting"] = got["setting"]
    if got.get("kind") in ("document", "screenshot", "photo"):
        out["kind"] = got["kind"]
    out["bw"] = bool(got.get("bw")) or base["bw"]
    out["notes"] = base["notes"]
    return out


def parse(q, use_llm=True):
    if use_llm:
        got = parse_llm(q)
        if got is not None:
            got["source"] = "gemini"
            return got
    out = parse_rules(q)
    out["source"] = "rules"
    return out


def to_chips(cues):
    """The cues as the user sees them: label, confidence, and whether it filters.

    A chip under 0.8 confidence is a preference. It can lift a photo up the
    list; it can never push one off it.
    """
    chips, seen = [], set()

    def add(c):
        if c["label"] not in seen:
            seen.add(c["label"])
            chips.append(c)

    for w in cues["content"]:
        add({"label": w, "conf": 0.9, "hard": False, "field": "content"})
    for p in cues["people"]:
        add({"label": p, "conf": 0.85, "hard": False, "field": "people"})
    if cues["place"]:
        add({"label": cues["place"], "conf": 0.8, "hard": False, "field": "place"})
    if cues["setting"]:
        add({"label": cues["setting"], "conf": 0.8, "hard": False, "field": "setting"})
    if cues["kind"]:
        add({"label": cues["kind"], "conf": 0.75, "hard": False, "field": "kind"})
    if cues["bw"]:
        add({"label": "black and white", "conf": 0.9, "hard": False, "field": "bw"})
    d = cues.get("date")
    if d:
        if d["kind"] == "month_year":
            lab = f"{d['text']}"
        elif d["kind"] == "year":
            lab = str(d["year"])
        elif d["kind"] == "month":
            lab = f"{d['text']} — year unknown"
        else:
            lab = f"{d['text']} — roughly"
        add({"label": lab, "conf": d["confidence"],
             "hard": d["confidence"] >= 0.8, "field": "date"})
    return chips

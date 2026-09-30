"""Scoring, the ambiguity check, and the narrowing question.

The whole product argument lives in three rules:

  1. A cue we are confident about can filter. A cue we are not confident about
     can only lift. So "august 2025" narrows; "last august" does not.

  2. If an uncertain date could point at more than one year, and more than one
     of those years actually holds a decent match, we ask. Once. This is the
     failure we reproduced on the live app, and it is the whole demo.

  3. If nothing scores well, we do not show an empty screen. We show the
     closest few and ask about the attribute that best splits them.
"""
import re
from datetime import date

from library import TODAY


def _has(word, text):
    """Whole-word match. Without the boundaries, "trip" finds "strip"."""
    return re.search(rf"\b{re.escape(word)}\b", text) is not None

# how much each kind of agreement is worth
W_TEXT, W_TAG, W_TITLE = 3.0, 2.0, 2.5
W_PEOPLE, W_PLACE, W_SETTING, W_KIND, W_BW = 2.0, 2.0, 1.0, 1.5, 2.0
W_DATE_HARD, W_DATE_SOFT = 4.0, 1.5

GOOD = 6.0     # at or above this, we believe it
CLOSE = 2.5    # below GOOD but above this, it is a near miss worth showing
FLOOR = 2.0    # below this it is noise, and showing it is how you get 64 photos


def _hay(it):
    return " ".join([
        it["title"].lower(), it["desc"].lower(), it["text"].lower(),
        " ".join(it["tags"]).lower(), it["venue"].lower(),
        it["place"].lower(), it["event"].lower(),
    ])


def _date_score(it, d):
    """Return (points, in_window). in_window is only meaningful for hard cues."""
    if not d:
        return 0.0, True
    y, m, _ = (int(x) for x in it["date"].split("-"))

    if d["kind"] == "month_year":
        hit = (y == d["year"] and m == d["month"])
        return (W_DATE_HARD if hit else 0.0), hit
    if d["kind"] == "year":
        hit = (y == d["year"])
        return (W_DATE_HARD if hit else 0.0), hit
    if d["kind"] == "month":
        # the trap. Right month in any plausible year is a lift, never a filter.
        if m == d["month"] and y in d["years"]:
            # nearer years score a little higher, but all of them stay eligible
            rank = d["years"].index(y)
            return W_DATE_SOFT * (1.0 - 0.15 * rank), True
        return 0.0, True
    if d["kind"] == "around":
        delta = abs(date(y, m, 15).toordinal() - d["centre"])
        if delta <= d["window"]:
            return W_DATE_SOFT * (1.0 - delta / (d["window"] * 2.0)), True
        if delta <= d["window"] * 2:
            return W_DATE_SOFT * 0.25, True
        return 0.0, True
    return 0.0, True


def score(it, cues):
    hay = _hay(it)
    pts, why = 0.0, []

    for w in cues["content"]:
        if _has(w, it["text"].lower()):
            pts += W_TEXT; why.append(f"“{w}” is written in it")
        elif _has(w, it["title"].lower()):
            pts += W_TITLE; why.append(f"“{w}” in the title")
        elif _has(w, " ".join(it["tags"]).lower()):
            pts += W_TAG; why.append(f"tagged “{w}”")
        elif _has(w, hay):
            pts += 1.0; why.append(f"mentions “{w}”")

    for p in cues["people"]:
        if p in [x.lower() for x in it["people"]]:
            pts += W_PEOPLE; why.append(p)
    if cues["place"] and cues["place"].lower() in (it["place"] or "").lower():
        pts += W_PLACE; why.append(it["place"])
    if cues["setting"] and cues["setting"] == it["setting"]:
        pts += W_SETTING; why.append(it["setting"])
    if cues["kind"] and cues["kind"] == it["kind"]:
        pts += W_KIND; why.append(it["kind"])
    if cues["bw"] and it["bw"]:
        pts += W_BW; why.append("black and white")

    dp, in_win = _date_score(it, cues.get("date"))
    if dp > 0:
        pts += dp
        d = cues["date"]
        why.append(it["date"][:7] if d["confidence"] >= 0.8 else f"near {it['date'][:7]}")
    return pts, in_win, why


def run(items, cues, year_override=None, floor=None):
    """Rank the library. Only a confident date cue is ever allowed to exclude."""
    floor = FLOOR if floor is None else floor
    d = cues.get("date")
    hard_date = bool(d) and d["confidence"] >= 0.8

    out = []
    for it in items:
        pts, in_win, why = score(it, cues)
        if hard_date and not in_win:
            continue                      # confident date: a real filter
        if year_override is not None and not it["date"].startswith(str(year_override)):
            continue                      # the user answered our question
        if pts < floor:
            continue          # one weak brush against one word is not a result
        out.append({"item": it, "score": round(pts, 2), "why": why})
    # best first; ties broken by the newer photo, which is what people expect
    out.sort(key=lambda r: r["item"]["date"], reverse=True)
    out.sort(key=lambda r: -r["score"])
    return out


# ------------------------------------------------------------- the question -
def ambiguity(results, cues):
    """Is an unresolved year the thing standing between us and an answer?

    Only worth asking when the answer would actually change what we show:
    a month with no year, where two or more years each hold a decent match.
    """
    d = cues.get("date")
    if not d or d["kind"] != "month" or not results:
        return None

    by_year = {}
    for r in results:
        y = int(r["item"]["date"][:4])
        if y in d["years"] and int(r["item"]["date"][5:7]) == d["month"]:
            by_year.setdefault(y, []).append(r)

    # Only offer a year that is genuinely in contention. Listing every year that
    # happens to hold something would make the question look like a shrug.
    best = max((rs[0]["score"] for rs in by_year.values()), default=0)
    live = {y: rs for y, rs in by_year.items()
            if rs and rs[0]["score"] >= CLOSE and rs[0]["score"] >= 0.75 * best}
    if len(live) < 2:
        return None

    month_name = date(2000, d["month"], 1).strftime("%B")
    return {
        "type": "year",
        "question": f"Which {month_name} do you mean?",
        "because": f"You have photos from {month_name} in more than one year, "
                   f"and they are different photos.",
        "options": [
            {"value": y,
             "label": f"{month_name} {y}",
             "hint": live[y][0]["item"]["title"]}
            for y in sorted(live, reverse=True)
        ],
    }


def narrowing(results):
    """Nothing landed. Ask about whatever best splits the near misses.

    Deliberately drawn from attributes people do not think to type, which is
    where the remaining information actually is.
    """
    pool = [r for r in results[:12]]
    if not pool:
        return None

    def split(key, fn):
        vals = {}
        for r in pool:
            v = fn(r["item"])
            if v:
                vals.setdefault(v, 0)
                vals[v] += 1
        return vals if len(vals) >= 2 else None

    for label, key, fn, render in [
        ("Was anyone else in it?", "people",
         lambda i: "with people" if i["people"] else "just the thing itself",
         lambda v: v),
        ("Indoors or outdoors?", "setting", lambda i: i["setting"], lambda v: v),
        ("Is it a photo or something you photographed?", "kind",
         lambda i: {"photo": "a photo", "document": "paperwork",
                    "screenshot": "a screenshot"}.get(i["kind"]), lambda v: v),
        ("How old is it, roughly?", "era",
         lambda i: "older than five years" if i["date"] < "2021" else "recent",
         lambda v: v),
    ]:
        vals = split(key, fn)
        if vals:
            return {
                "type": "narrow", "key": key, "question": label,
                "because": "Nothing matched with any confidence, so here are the "
                           "closest few. One more detail would cut this down.",
                "options": [{"value": v, "label": render(v), "hint": f"{n} of these"}
                            for v, n in sorted(vals.items(), key=lambda kv: -kv[1])],
            }
    return None


def apply_narrowing(results, key, value):
    def keep(it):
        if key == "people":
            return ("with people" if it["people"] else "just the thing itself") == value
        if key == "setting":
            return it["setting"] == value
        if key == "kind":
            return {"photo": "a photo", "document": "paperwork",
                    "screenshot": "a screenshot"}.get(it["kind"]) == value
        if key == "era":
            return ("older than five years" if it["date"] < "2021" else "recent") == value
        return True
    return [r for r in results if keep(r["item"])]


def verdict(results):
    if not results:
        return "empty"
    if results[0]["score"] >= GOOD:
        return "confident"
    if results[0]["score"] >= CLOSE:
        return "near"
    return "empty"


def answer(items, cues, year_override=None, narrow=None):
    """One call, the whole behaviour.

    When we are confident we show a tight list. When we are not, we widen the
    net before giving up, because "here are the closest few, and one question"
    is worth far more to the user than an empty screen.

    At most one question per search, ever. A second question the moment the
    first is answered is the interrogation this design is supposed to avoid,
    and it is the thing the guardrail metric watches for.
    """
    answered = bool(year_override) or bool(narrow)

    if year_override and cues.get("date", {}) and cues["date"]["kind"] == "month":
        # The person just told us the year. That is now the best evidence we
        # have, so the cue stops being a guess and starts being a fact.
        cues = dict(cues)
        cues["date"] = {"kind": "month_year", "month": cues["date"]["month"],
                        "year": year_override, "confidence": 1.0,
                        "text": cues["date"]["text"]}

    res = run(items, cues)
    if verdict(res) != "confident":
        res = run(items, cues, floor=0.75)
    if narrow:
        res = apply_narrowing(res, *narrow)

    v = verdict(res)
    ask = None
    if not answered:
        ask = ambiguity(res, cues)
        if ask is None and v != "confident":
            ask = narrowing(res)
    return {"results": res, "verdict": v, "ask": ask}

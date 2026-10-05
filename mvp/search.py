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


def _starts(word, text):
    """Word-start match, so "water" reaches "waterfall" and "trip" reaches
    "trips" — but "trip" still cannot reach "strip"."""
    return re.search(rf"\b{re.escape(word)}\w+", text) is not None

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
        elif _starts(w, it["title"].lower()) or _starts(w, " ".join(it["tags"]).lower()):
            pts += 1.5; why.append(f"“{w}…” in it")
        elif _starts(w, hay):
            pts += 0.75; why.append(f"“{w}…” mentioned")

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

    other = pts          # everything the person said that was not about when
    hits = len(why)      # how many separate things they said this photo matches
    dp, in_win = _date_score(it, cues.get("date"))
    if dp > 0:
        pts += dp
        hits += 1
        d = cues["date"]
        why.append(it["date"][:7] if d["confidence"] >= 0.8 else f"near {it['date'][:7]}")
    return pts, in_win, why, other, hits


def _cue_count(cues):
    """How many separate things the person told us."""
    n = len(cues["content"]) + len(cues["people"])
    for f in ("place", "setting", "kind"):
        n += 1 if cues[f] else 0
    n += 1 if cues["bw"] else 0
    n += 1 if cues.get("date") else 0
    return n


def _non_date_cues(cues):
    """Did the person tell us anything other than when it was?"""
    return bool(cues["content"] or cues["people"] or cues["place"]
                or cues["setting"] or cues["kind"] or cues["bw"])


def run(items, cues, year_override=None, floor=None, need_hits=1):
    """Rank the library. Only a confident date cue is ever allowed to exclude.

    need_hits is how many of the person's cues a photo has to match. Asking for
    two is what stops "my sister at the wedding" returning thirty photos that
    merely have a sister in them. It is a preference, not a rule: answer() drops
    back to one when two leaves too little to look at.
    """
    floor = FLOOR if floor is None else floor
    d = cues.get("date")
    hard_date = bool(d) and d["confidence"] >= 0.8

    # A date that narrows must not become the only reason a photo is here. A
    # tester asked for a bill in August 2025 and got cricket and a vegetable
    # market, because landing in the right month scored enough on its own.
    # If the person told us anything besides when, that part has to match too.
    date_narrows = hard_date or year_override is not None
    needs_more = date_narrows and _non_date_cues(cues)

    out = []
    for it in items:
        pts, in_win, why, other, hits = score(it, cues)
        if hard_date and not in_win:
            continue                      # confident date: a real filter
        if year_override is not None and not it["date"].startswith(str(year_override)):
            continue                      # the user answered our question
        if needs_more and other <= 0:
            continue                      # in the right month, but nothing else
        if hits < need_hits:
            continue                      # matched less of the query than we want
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


# The order here is not arbitrary. Across 83 free-recall photo descriptions in
# desk research, people volunteered indoor/outdoor 69 times, how many people
# were there 64, who they were 56 and where 54 — while an exact date proved
# notably less useful than the time of day. So we ask in that order, and only
# ever about something the person did not already tell us.
DIMENSIONS = [
    ("setting", "Were you indoors or outdoors?",
     lambda i: i["setting"]),
    ("crowd", "How many people were in it?",
     lambda i: i["crowd"]),
    ("who", "Who was with you?",
     lambda i: ", ".join(i["people"]) if i["people"] else "nobody"),
    ("place", "Where was it?",
     lambda i: i["place"] or "somewhere not recorded"),
    ("tod", "What time of day?",
     lambda i: i["tod"]),
    ("event", "What was going on?",
     lambda i: i["event"] or "an ordinary day"),
    ("kind", "A photo, or something you photographed?",
     lambda i: {"photo": "a photo", "document": "paperwork",
                "screenshot": "a screenshot"}.get(i["kind"])),
    ("era", "Roughly how old is it?",
     lambda i: "more than five years" if i["date"] < "2021" else "fairly recent"),
]
_DIM = {k: fn for k, _, fn in DIMENSIONS}


def narrowing(results, cues=None, asked=()):
    """Ask about whatever best splits what is actually on screen.

    Two rules keep this from becoming a filter drawer. The options are computed
    from the candidates in front of the person, never from the whole library.
    And we never ask about something they already told us.
    """
    pool = results[:14]
    if len(pool) < 2:
        return None
    cues = cues or {}
    already = {
        "setting": bool(cues.get("setting")), "who": bool(cues.get("people")),
        "place": bool(cues.get("place")), "kind": bool(cues.get("kind")),
    }

    best = None
    for key, label, fn in DIMENSIONS:
        if key in asked or already.get(key):
            continue
        vals = {}
        for r in pool:
            v = fn(r["item"])
            if v:
                vals[v] = vals.get(v, 0) + 1
        if len(vals) < 2:
            continue
        # an even split removes the most candidates, so prefer it
        spread = min(vals.values()) / max(vals.values())
        cand = {
            "type": "narrow", "key": key, "question": label,
            "because": "Here are the closest few. One more detail cuts this down.",
            "options": [{"value": v, "label": v, "hint": f"{n} of these"}
                        for v, n in sorted(vals.items(), key=lambda kv: -kv[1])][:4],
        }
        if best is None or spread > best[0]:
            best = (spread, cand)
    return best[1] if best else None


def apply_narrowing(results, key, value):
    fn = _DIM.get(key)
    if not fn:
        return results
    return [r for r in results if fn(r["item"]) == value]


# ------------------------------------------------------- the near-miss loop -
# "Close, but not it" is the most informative thing a person can tell us, and
# the thing today's product throws away. Note the asymmetry with the question
# cap above: we cap the questions *we* start. A rejection is the person asking
# us to try again, so acting on it is invited rather than imposed.
REJECTIONS = [
    ("right_event", "Right occasion, wrong photo"),
    ("wrong_person", "Wrong people"),
    ("wrong_place", "Wrong place"),
    ("wrong_time", "Wrong time"),
    ("not_close", "Not close at all"),
]


def reject(results, item, reason):
    """Re-rank on what a rejected candidate tells us. Returns (results, note)."""
    out, notes = [], ""
    for r in results:
        it = r["item"]
        if it["id"] == item["id"]:
            continue                      # the rejected one always goes
        keep, bump = True, 0.0
        if reason == "right_event":
            # the strongest signal there is: same occasion, different frame
            same = (it["event"] and it["event"] == item["event"]) or \
                   it["date"][:7] == item["date"][:7]
            if same:
                bump = 5.0
            else:
                keep = False
            notes = "Kept the same occasion, dropped everything else."
        elif reason == "wrong_person":
            keep = set(it["people"]) != set(item["people"])
            notes = "Dropped anything with the same people in it."
        elif reason == "wrong_place":
            keep = (it["place"] or "") != (item["place"] or "")
            notes = "Dropped that place."
        elif reason == "wrong_time":
            keep = it["date"][:7] != item["date"][:7]
            notes = "Dropped that month."
        elif reason == "not_close":
            keep = not (set(it["tags"]) & set(item["tags"]))
            notes = "Dropped anything that looks like it."
        if keep:
            out.append({**r, "score": round(r["score"] + bump, 2)})
    out.sort(key=lambda r: -r["score"])
    return out, notes


def _clear_winner(results):
    """Is one photo plainly ahead of everything else?

    A tester searched "my sister at the wedding", got the right photo at the
    top, and was then asked whether they had been indoors or outdoors. The
    question was not wrong, it was late: they had already found it. A question
    earns its place by splitting a field of candidates, so when there is no
    real field left we say nothing.
    """
    if not results:
        return False
    if len(results) == 1:
        return True
    return results[0]["score"] >= max(GOOD * 0.75, results[1]["score"] * 1.5)


def verdict(results):
    """"empty" means we have nothing at all. Anything we do have is a near miss
    worth showing, because a screen with three wrong photos on it is still more
    use than a blank one — the person can tell us which way to go from there."""
    if not results:
        return "empty"
    return "confident" if results[0]["score"] >= GOOD else "near"


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

    # Widen in steps, and only as far as we have to. When the person gave us
    # two or more cues we first ask for photos that match at least two of them;
    # one cue out of three is a near miss, and thirty near misses is a wall.
    # Each step is only taken because the one before it came up short.
    want = 2 if _cue_count(cues) >= 2 else 1
    res = run(items, cues, need_hits=want)

    def top_up(pool, upto=8):
        """Add weaker matches underneath, but only enough to fill the screen.

        Topping up rather than replacing is the point. Two photos that match
        both of your cues are worth more than thirty that match one, so the
        two stay at the top and we borrow just enough to look at.
        """
        have = {r["item"]["id"] for r in res}
        return res + [r for r in pool if r["item"]["id"] not in have][:max(0, upto - len(res))]

    if len(res) < 8:
        res = top_up(run(items, cues, need_hits=1))
    if len(res) < 4 and verdict(res) != "confident":
        res = top_up(run(items, cues, floor=0.75, need_hits=1))
    if narrow:
        res = apply_narrowing(res, *narrow)

    v = verdict(res)
    ask = None
    if not answered:
        ask = ambiguity(res, cues)
        if ask is None and v != "confident" and not _clear_winner(res):
            ask = narrowing(res, cues)
    # cues goes back out because the person may have just resolved one of them,
    # and the screen has to say so. Showing "year unknown" after they told us
    # the year is the exact failure this product exists to argue against.
    return {"results": res, "verdict": v, "ask": ask, "cues": cues}

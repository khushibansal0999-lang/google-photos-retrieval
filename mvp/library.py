"""The demo library: ~120 items seeded to carry the real failures from research.

Nothing here is a real photo. Each item is a record with the metadata a photo
app would already hold, plus the text a photo would contain. Thumbnails are
drawn at runtime (see thumbs.py), so the repo carries no image files and the
app costs nothing to host.

The planted items exist so specific research findings can be reproduced live:

  * P1's bill        an itemised restaurant bill from August 2025, with a
                     second, different bill from August 2026 so that
                     "last august" is genuinely ambiguous rather than a trick.
  * P2's documents   an ID card and a recovery-password screenshot, the two
                     document tasks that failed in interviews.
  * P4's waterfall   "Bro I was roaming around there man. It's somewhere near
                     a waterfall." No date, no place name, one visual cue.
  * childhood B&W    scanned, decades old, no usable metadata. The case where
                     face search breaks because the face has aged out.
"""
from datetime import date, timedelta

TODAY = date(2026, 9, 30)

PHOTO, DOC, SHOT = "photo", "document", "screenshot"


def _i(id, d, kind, title, desc, *, people=(), place="", venue="", setting="",
       event="", text="", tags=(), bw=False, tod="", crowd=""):
    """tod and crowd exist because desk research found people recall the time of
    day and how many were in frame far more reliably than an exact date. They
    are the two highest-value narrowing questions we can ask."""
    return {
        "id": id, "date": d, "kind": kind, "title": title, "desc": desc,
        "people": list(people), "place": place, "venue": venue,
        "setting": setting, "event": event, "text": text,
        "tags": list(tags), "bw": bw,
        "tod": tod, "crowd": crowd or ("nobody" if not people else "a few"),
        # which stock photo of this scene to draw. Set per repeat in
        # _filler_items so four "Hill station viewpoint" items get four
        # different pictures instead of colliding on a hash.
        "variant": 0,
    }


# time of day and how many people, for the planted items
_TOD_CROWD = {
    "b001": ("evening", "a few"),    "b002": ("morning", "one other"),
    "d001": ("afternoon", "nobody"), "s001": ("night", "nobody"),
    "w001": ("afternoon", "a few"),  "w002": ("afternoon", "a few"),
    "c001": ("afternoon", "one other"), "c002": ("evening", "a crowd"),
    "g001": ("night", "one other"),  "g002": ("night", "a crowd"),
    "m001": ("morning", "nobody"),   "p001": ("afternoon", "a few"),
}


# ---------------------------------------------------------------- planted ---
# These reproduce findings from the research. Order matters to nobody, but the
# dates do: see the two August bills.
PLANTED = [
    _i("b001", "2025-08-03", DOC,
       "Restaurant bill, ONE8 Commune",
       "Itemised dinner bill for four. Cheese and Herb Polenta, Lemongrass "
       "Grilled Chicken, Burrata and Basil, Spicy Potato. Total 2,760.",
       people=["friends"], place="Bengaluru", venue="ONE8 Commune",
       setting="indoor", event="dinner",
       text="ONE8 COMMUNE  TABLE 12  CHEESE AND HERB POLENTA  LEMONGRASS "
            "GRILLED CHICKEN  BURRATA AND BASIL  SPICY POTATO  TOTAL 2760.00",
       tags=["bill", "receipt", "restaurant", "food", "dinner", "group", "paperwork"]),

    # The decoy. Same month name, different year. This is what makes
    # "bill from last august" ambiguous instead of merely underspecified.
    _i("b002", "2026-08-17", DOC,
       "Cafe bill, Third Wave Coffee",
       "Short cafe bill. Two flat whites and a croissant. Total 610.",
       people=["sister"], place="Bengaluru", venue="Third Wave Coffee",
       setting="indoor", event="coffee",
       text="THIRD WAVE COFFEE  FLAT WHITE X2  BUTTER CROISSANT  TOTAL 610.00",
       tags=["bill", "receipt", "cafe", "coffee", "paperwork"]),

    _i("d001", "2024-02-11", DOC,
       "ID card, front",
       "Photograph of an identity card taken to have it on hand. Glare across "
       "the lower third.",
       place="home", setting="indoor",
       text="PERMANENT ACCOUNT NUMBER  NAME  DATE OF BIRTH  SIGNATURE",
       tags=["id", "card", "identity", "document", "paperwork", "official"]),

    _i("s001", "2024-11-02", SHOT,
       "Recovery codes screenshot",
       "Screenshot of eight one-time backup codes shown once during account "
       "setup. Never opened since.",
       setting="indoor",
       text="SAVE YOUR BACKUP CODES  EACH CODE CAN BE USED ONCE  "
            "4F2A-9C11  7B03-DD52  1E9F-4A77",
       tags=["password", "recovery", "codes", "security", "screenshot", "paperwork"]),

    _i("w001", "2023-07-22", PHOTO,
       "Waterfall, somewhere off the highway",
       "Standing on wet rock in front of a wide waterfall. Nobody wrote down "
       "where this was. Green everywhere, overcast.",
       people=["friends"], setting="outdoor", event="road trip",
       tags=["waterfall", "water", "trip", "nature", "rocks", "green", "travel"]),
    _i("w002", "2023-07-22", PHOTO,
       "Roadside tea stall on the way back",
       "Plastic chairs, steel cups, rain starting. Same trip as the waterfall.",
       people=["friends"], setting="outdoor", event="road trip",
       tags=["tea", "roadside", "trip", "rain", "travel"]),

    _i("c001", "1998-06-14", PHOTO,
       "Childhood photo, scanned",
       "Black and white. A child on a bicycle in a courtyard. Scanned from a "
       "print, so the file date is the scan date, not the day it was taken.",
       people=["family", "child"], setting="outdoor",
       tags=["childhood", "black and white", "scanned", "old", "bicycle", "family"],
       bw=True),
    _i("c002", "1998-06-14", PHOTO,
       "Childhood photo, birthday",
       "Black and white. Cake on a table, several relatives leaning in.",
       people=["family", "child"], setting="indoor", event="birthday",
       tags=["childhood", "black and white", "scanned", "old", "birthday", "family"],
       bw=True),

    _i("g001", "2025-12-20", PHOTO,
       "Sister at the wedding, evening",
       "Outdoors after dark, string lights overhead. She is laughing at "
       "something off-frame.",
       people=["sister"], place="Udaipur", setting="outdoor", event="wedding",
       tags=["wedding", "night", "outdoors", "family", "lights", "celebration"]),
    _i("g002", "2025-12-20", PHOTO,
       "Group shot at the wedding",
       "Everyone squeezed into frame on the steps, mid-count-down.",
       people=["sister", "friends", "family"], place="Udaipur",
       setting="outdoor", event="wedding",
       tags=["wedding", "group", "night", "outdoors", "celebration"]),

    _i("m001", "2025-03-09", PHOTO,
       "Medicine strip",
       "Photograph of a strip of tablets taken so the name could be repeated "
       "to a pharmacist later.",
       setting="indoor",
       text="AZITHROMYCIN 500 MG  TABLETS  TAKE ONE DAILY AFTER FOOD",
       tags=["medicine", "tablets", "health", "paperwork", "pharmacy"]),

    _i("p001", "2024-09-05", PHOTO,
       "Small cafe on the Goa trip",
       "Blue shutters, handwritten menu board, two plastic tables outside. "
       "Nobody remembers the name.",
       people=["friends"], place="Goa", setting="outdoor", event="holiday",
       tags=["cafe", "goa", "trip", "travel", "holiday", "food"]),
]


# ----------------------------------------------------------------- filler ---
# Enough ordinary life that a query has to actually discriminate. Generated so
# the file stays readable, but every item is a plausible record.
_FILLER = [
    ("Morning walk by the lake", PHOTO, "outdoor", "walk",
     ["lake", "morning", "walk", "trees"], ["", "Bengaluru"]),
    ("Groceries laid out on the counter", PHOTO, "indoor", "",
     ["groceries", "kitchen", "food"], ["home"]),
    ("Whiteboard after the planning session", SHOT, "indoor", "work",
     ["whiteboard", "work", "notes", "screenshot"], ["office"]),
    ("Boarding pass", DOC, "indoor", "travel",
     ["boarding pass", "flight", "travel", "paperwork"], ["airport"]),
    ("Parking receipt", DOC, "outdoor", "",
     ["receipt", "parking", "paperwork"], [""]),
    ("Street dog asleep in the sun", PHOTO, "outdoor", "",
     ["dog", "street", "animal", "sun"], [""]),
    ("Dinner at home, plates from above", PHOTO, "indoor", "dinner",
     ["food", "dinner", "home", "plates"], ["home"]),
    ("Concert, hands in the air", PHOTO, "indoor", "concert",
     ["concert", "music", "crowd", "night", "lights"], [""]),
    ("Rain on the window from the bus", PHOTO, "indoor", "commute",
     ["rain", "window", "bus", "commute"], [""]),
    ("Electricity bill", DOC, "indoor", "",
     ["bill", "electricity", "utility", "paperwork"], ["home"]),
    ("Hill station viewpoint", PHOTO, "outdoor", "holiday",
     ["hills", "viewpoint", "trip", "travel", "green"], ["Coorg", "Ooty"]),
    ("Birthday cake with candles lit", PHOTO, "indoor", "birthday",
     ["birthday", "cake", "celebration", "candles"], ["home"]),
    ("Bookshelf, new arrangement", PHOTO, "indoor", "",
     ["books", "shelf", "home"], ["home"]),
    ("Screenshot of a train booking", SHOT, "indoor", "travel",
     ["train", "booking", "travel", "screenshot", "paperwork"], [""]),
    ("Beach at sunset", PHOTO, "outdoor", "holiday",
     ["beach", "sunset", "sea", "travel", "holiday"], ["Goa", "Gokarna"]),
    ("Office desk on a quiet day", PHOTO, "indoor", "work",
     ["desk", "work", "office"], ["office"]),
    ("Temple corridor", PHOTO, "outdoor", "holiday",
     ["temple", "stone", "travel", "architecture"], ["Hampi", "Pushkar"]),
    ("Cat on a parked scooter", PHOTO, "outdoor", "",
     ["cat", "animal", "street", "scooter"], [""]),
    ("Prescription slip", DOC, "indoor", "",
     ["prescription", "health", "paperwork", "doctor"], [""]),
    ("Friends on a rooftop at night", PHOTO, "outdoor", "party",
     ["rooftop", "night", "friends", "party", "lights"], ["Bengaluru"]),
    ("Long queue outside the bank", PHOTO, "outdoor", "",
     ["queue", "bank", "street", "people"], [""]),
    ("Plant that finally flowered", PHOTO, "indoor", "",
     ["plant", "flower", "home", "green"], ["home"]),
    ("Insurance policy, first page", DOC, "indoor", "",
     ["insurance", "policy", "paperwork", "official"], ["home"]),
    ("Fog on the morning drive", PHOTO, "outdoor", "road trip",
     ["fog", "road", "drive", "morning", "travel"], [""]),
    ("Wedding invitation card", DOC, "indoor", "wedding",
     ["invitation", "wedding", "card", "paperwork"], [""]),
    ("Snacks on the train table", PHOTO, "indoor", "travel",
     ["train", "food", "snacks", "travel"], [""]),
    ("New shoes, still in the box", PHOTO, "indoor", "",
     ["shoes", "shopping", "home"], ["home"]),
    ("Screenshot of a wifi password", SHOT, "indoor", "",
     ["wifi", "password", "screenshot", "paperwork"], [""]),
    ("Kids playing cricket in the lane", PHOTO, "outdoor", "",
     ["cricket", "children", "street", "play"], [""]),
    ("Market stall, vegetables stacked", PHOTO, "outdoor", "",
     ["market", "vegetables", "food", "street"], [""]),
    # Added after user testing: three testers all said the library felt thin,
    # and a thin library makes the retrieval problem look easier than it is.
    ("Snow up north", PHOTO, "outdoor", "holiday",
     ["snow", "mountains", "cold", "travel"], ["Manali", "Shimla"]),
    ("Festival lights down the street", PHOTO, "outdoor", "festival",
     ["festival", "lights", "diwali", "night", "street", "celebration"], [""]),
    ("Boat on the backwaters", PHOTO, "outdoor", "holiday",
     ["boat", "river", "water", "trip", "travel"], ["Kerala", "Goa"]),
    ("Bridge at dusk", PHOTO, "outdoor", "",
     ["bridge", "dusk", "river", "city", "evening"], ["Bengaluru"]),
    ("Kitten behind the shop", PHOTO, "outdoor", "",
     ["kitten", "cat", "animal", "street"], [""]),
    ("Breakfast at the hotel", PHOTO, "indoor", "holiday",
     ["breakfast", "food", "hotel", "travel", "morning"], ["Udaipur", "Goa"]),
    ("Cycling on the ring road", PHOTO, "outdoor", "",
     ["bicycle", "cycling", "road", "exercise"], ["Bengaluru"]),
    ("Leaves turning in the park", PHOTO, "outdoor", "",
     ["autumn", "leaves", "park", "trees", "green"], [""]),
]

_PEOPLE_CYCLE = [[], ["friends"], ["sister"], ["family"], ["friends", "sister"], []]


def _filler_items():
    out, n = [], 0
    # spread across four years so date questions have something to be wrong about
    d = TODAY - timedelta(days=1)
    for round_ in range(4):
        for j, (title, kind, setting, event, tags, places) in enumerate(_FILLER):
            n += 1
            d = d - timedelta(days=11 + (j % 7) + round_)

            # Keep August clear of other bills. The two planted August bills are
            # the point of the demo; a third would make the question we ask look
            # arbitrary rather than necessary.
            if d.month == 8 and ("bill" in tags or "receipt" in tags):
                d = d - timedelta(days=40)

            place = places[(round_ + j) % len(places)]
            # Paperwork does not have people in it. Only hand-authored items
            # (a shared restaurant bill) carry people, and they do it on purpose.
            people = [] if kind in (DOC, SHOT) else _PEOPLE_CYCLE[(round_ + j) % len(_PEOPLE_CYCLE)]
            it = _i(
                f"f{n:03d}", d.isoformat(), kind, title,
                f"{title}. Ordinary day, nothing written down about it.",
                people=people, place=place, setting=setting, event=event,
                tags=tags,
            )
            it["variant"] = round_      # a different picture on each repeat
            out.append(it)
    return out


_TODS = ["morning", "afternoon", "evening", "night"]
_CROWDS = ["nobody", "one other", "a few", "a crowd"]


def load():
    """Every item, newest first — the order a photo app would show them in."""
    items = PLANTED + _filler_items()
    for k, it in enumerate(items):
        if it["id"] in _TOD_CROWD:
            it["tod"], it["crowd"] = _TOD_CROWD[it["id"]]
        elif not it["tod"]:
            # spread the filler so a question about either actually splits it
            it["tod"] = _TODS[k % 4]
            it["crowd"] = "nobody" if not it["people"] else _CROWDS[1 + (k % 3)]
        # If the title already says when it was, that wins. A tester caught
        # "Fog on the morning drive" filed under night, and was right to stop
        # trusting the rest of the metadata after seeing it.
        for word in _TODS:
            if word in it["title"].lower():
                it["tod"] = word
                break
    items.sort(key=lambda x: x["date"], reverse=True)
    return items


LIBRARY = load()

if __name__ == "__main__":
    lib = load()
    print(f"{len(lib)} items, {lib[-1]['date']} to {lib[0]['date']}")
    from collections import Counter
    print(Counter(i["kind"] for i in lib))
    for y in ("2025-08", "2026-08"):
        hits = [i for i in lib if i["date"].startswith(y)]
        print(f"  {y}: {len(hits)} items -> {[i['id'] for i in hits]}")

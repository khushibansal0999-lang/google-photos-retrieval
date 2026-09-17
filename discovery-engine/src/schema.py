"""
Extraction schema for the discovery engine.

Every scraped post/review/comment is tagged along dimensions that map to the
retrieval journey:  REMEMBER -> EXPRESS -> UNDERSTAND -> EVALUATE -> REFINE.
This is what lets us compare failure modes instead of just summarising sentiment.
"""

PHOTO_TYPES = [
    "screenshot", "document_receipt_id", "medicine_label_product", "place_venue_travel",
    "person_face", "pet_animal", "event_celebration", "food_meal", "object_thing",
    "text_in_image", "video", "whatsapp_social_download", "other", "not_specified",
]

MEMORY_CUES = [
    "approx_time",          # "last year", "around Diwali", "a few months ago"
    "exact_date",           # knows the actual date
    "place_location",       # city / venue / GPS-able
    "people_present",       # who was in it / who they were with
    "visual_detail",        # colours, objects, composition, what is IN the photo
    "context_event",        # "when I was sick", "during the Goa trip", "at a wedding"
    "source_channel",       # "it was a WhatsApp forward", "a screenshot", "from my old phone"
    "text_content",         # words that appear inside the photo
    "emotion_significance", # why it mattered
    "none_stated",
]

FAILURE_STAGES = [
    "cannot_express",        # user doesn't know how to phrase what they remember
    "app_misunderstands",    # user gave a good clue, search returned wrong/no results
    "too_many_results",      # results returned but can't evaluate / scan them
    "cannot_refine",         # first attempt failed, no way to narrow further
    "wrong_metadata",        # date/location wrong so the clue doesn't match the index
    "content_not_indexed",   # photo type not recognised (text, screenshots, docs)
    "gave_up",               # abandoned
    "succeeded",             # found it (useful for what WORKS)
    "not_applicable",
]

WORKAROUNDS = [
    "scroll_by_date", "browse_albums", "ask_another_person", "check_other_app",
    "use_map_view", "use_face_groups", "search_multiple_terms", "use_lens_or_ocr",
    "gave_up", "third_party_tool", "none_mentioned",
]

QUERY_STYLES = [
    "single_keyword", "natural_language_sentence", "date_only", "location_only",
    "person_name", "category_word", "combined_filters", "not_mentioned",
]

# JSON schema passed to output_config.format — strict, additionalProperties: false.
EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "is_relevant": {
            "type": "boolean",
            "description": "True ONLY if the text is about finding/searching/retrieving/locating a photo or video the user already has. False for storage, billing, backup, sync, editing, UI complaints, or generic praise.",
        },
        "relevance_reason": {"type": "string"},
        "retrieval_scenario": {
            "type": "string",
            "description": "One-sentence paraphrase of what the user was trying to find, in their framing. Empty string if not relevant.",
        },
        "photo_type": {"type": "string", "enum": PHOTO_TYPES},
        "cues_remembered": {"type": "array", "items": {"type": "string", "enum": MEMORY_CUES}},
        "cues_forgotten": {"type": "array", "items": {"type": "string", "enum": MEMORY_CUES}},
        "query_style": {"type": "string", "enum": QUERY_STYLES},
        "query_verbatim": {
            "type": "string",
            "description": "Exact search text the user says they typed, if quoted. Else empty string.",
        },
        "failure_stage": {"type": "string", "enum": FAILURE_STAGES},
        "failure_detail": {
            "type": "string",
            "description": "Specific mechanism of failure in <=20 words. e.g. 'search for medicine returned pills stock photos not their label'",
        },
        "workaround": {"type": "string", "enum": WORKAROUNDS},
        "time_since_photo": {
            "type": "string",
            "enum": ["days", "weeks", "months", "1_2_years", "3plus_years", "unknown"],
        },
        "user_segment_hint": {
            "type": "string",
            "description": "Any hint about who the user is: parent, traveller, student, professional, elderly, heavy-screenshot user, etc. Empty if none.",
        },
        "sentiment": {"type": "string", "enum": ["frustrated", "neutral", "positive"]},
        "key_quote": {
            "type": "string",
            "description": "The single most evidence-bearing sentence from the text, verbatim, <=40 words.",
        },
    },
    "required": [
        "is_relevant", "relevance_reason", "retrieval_scenario", "photo_type",
        "cues_remembered", "cues_forgotten", "query_style", "query_verbatim",
        "failure_stage", "failure_detail", "workaround", "time_since_photo",
        "user_segment_hint", "sentiment", "key_quote",
    ],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """You are a product researcher on the Google Photos Core Experience team.
You are analysing public user feedback (app reviews, Reddit posts, forum threads) to understand
one specific problem: users trying to RETRIEVE a photo they remember but cannot precisely describe.

For each text you receive, extract structured fields according to the schema.

Rules:
- is_relevant is TRUE only when the user is trying to find, search for, locate, or re-discover a specific
  photo/video they already have in their library. Complaints about storage, backup, sync, deletion, editing,
  sharing, pricing, or the app being slow are NOT relevant.
- Distinguish carefully between cues the user REMEMBERS (they mention it as a known fact) and cues they have
  FORGOTTEN (they say they don't know / can't remember it). If the user gives a rough time like "last year",
  that is approx_time REMEMBERED, and exact_date FORGOTTEN.
- failure_stage: pick the stage where retrieval broke down. If they typed a good clue and the app returned
  nothing/wrong things -> app_misunderstands. If they say they didn't know what to type -> cannot_express.
  If the photo was a screenshot/document/text and search ignored it -> content_not_indexed.
- Be literal. Do not infer things that are not in the text. Use not_specified / not_mentioned / unknown freely.
- key_quote must be verbatim from the text."""

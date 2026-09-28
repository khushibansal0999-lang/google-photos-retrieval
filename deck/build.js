// Builds deck/NL_GooglePhotos.pptx — upload to Drive converts it to Google Slides.
// Rules from the brief: max 10 slides, no fellow name, key-message titles,
// every font >= 14pt, colour-blind-safe (blue/orange pair validated in the dataviz palette).
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.title = "NL_GooglePhotos";

const C = {
  ink: "1C2530", muted: "4E5A67", navy: "14213D", white: "FFFFFF",
  panel: "EEF2F6", line: "D5DCE4",
  blue: "2A78D6", blueDark: "1C5CAB", orange: "EB6834", orangeDark: "B04515",
};
const HEAD = "Roboto Slab", BODY = "Roboto";
const W = 13.333, M = 0.6, CW = W - 2 * M;
const LINKS = {
  engine: "https://app-photos-retrieval-qvlu7ymwqfadwg3siqnqjb.streamlit.app/",
  repo: "https://github.com/khushibansal0999-lang/google-photos-retrieval",
  survey: "https://github.com/khushibansal0999-lang/google-photos-retrieval/blob/main/research/survey/survey-findings.md",
  guide: "https://github.com/khushibansal0999-lang/google-photos-retrieval/blob/main/research/interview-guide.md",
  market: "https://github.com/khushibansal0999-lang/google-photos-retrieval/blob/main/research/market-research/competitive-landscape.md",
};

// ---------- helpers ----------
const txt = (s, t, o) => s.addText(t, { fontFace: BODY, fontSize: 15, color: C.ink, margin: 0, valign: "top", isTextBox: true, ...o });
function title(s, t, o = {}) {
  txt(s, t, { x: M, y: 0.42, w: CW, h: 1.05, fontFace: HEAD, fontSize: 26, bold: true, valign: "middle", ...o });
}
// evidence tag: encodes which data source a card rests on (the deck's one repeated motif)
function tag(s, label, x, y, color = C.blue) {
  const w = 0.16 + label.length * 0.095;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.32, rectRadius: 0.16, fill: { color }, line: { color } });
  txt(s, label, { x, y: y + 0.02, w, h: 0.28, fontSize: 14, bold: true, color: C.white, align: "center", valign: "middle" });
  return w;
}
function card(s, x, y, w, h, fill = C.panel) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: fill } });
}
function stat(s, num, label, x, y, w, color) {
  txt(s, num, { x, y, w, h: 0.85, fontFace: HEAD, fontSize: 48, bold: true, color });
  txt(s, label, { x, y: y + 0.85, w, h: 0.75, fontSize: 15, color: C.ink });
}
function footer(s, t, dark = false) {
  txt(s, t, { x: M, y: 6.95, w: CW, h: 0.35, fontSize: 14, color: dark ? "B8C4D6" : C.muted });
}
function draftBadge(s) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: W - M - 2.9, y: 0.12, w: 2.9, h: 0.34, rectRadius: 0.17, fill: { color: "FFF1E8" }, line: { color: C.orangeDark, width: 1 } });
  txt(s, "DRAFT — update after research", { x: W - M - 2.9, y: 0.14, w: 2.9, h: 0.3, fontSize: 14, bold: true, color: C.orangeDark, align: "center", valign: "middle" });
}

// ---------- 1. Title ----------
{
  const s = pres.addSlide(); s.background = { color: C.navy };
  txt(s, "Google Photos · Core Experience · Vague-memory retrieval", { x: M, y: 0.8, w: CW, h: 0.4, fontSize: 16, color: "9FB3CC", bold: true });
  txt(s, "People remember the moment,\nnot the metadata", { x: M, y: 1.4, w: 9.5, h: 2.1, fontFace: HEAD, fontSize: 44, bold: true, color: C.white });
  txt(s, "Why photos people know they have stay lost — and what to build so partial memories are enough to find them.", { x: M, y: 3.6, w: 8.6, h: 0.9, fontSize: 18, color: "D8E1EC" });
  const links = [
    ["AI Discovery Engine (live)", LINKS.engine],
    ["AI-native MVP (live)", null],
    ["All research artefacts (repo)", LINKS.repo],
  ];
  links.forEach(([label, url], i) => {
    const y = 4.85 + i * 0.5;
    s.addShape(pres.shapes.OVAL, { x: M, y: y + 0.1, w: 0.16, h: 0.16, fill: { color: i === 1 ? C.orange : C.blue }, line: { color: i === 1 ? C.orange : C.blue } });
    txt(s, url ? [{ text: label + "  →", options: { hyperlink: { url }, color: C.white, underline: { style: "sng" } } }]
               : [{ text: label + "  →  link added once deployed", options: { color: "9FB3CC" } }],
      { x: M + 0.35, y, w: 8, h: 0.38, fontSize: 16 });
  });
  footer(s, "NextLeap Product Management Fellowship · Graduation Project · October 2026", true);
  s.addNotes("Title slide. No fellow name per submission rules. Links: engine, MVP (pending), repo with survey, interview guide, market research.");
}

// ---------- 2. Metric decomposition ----------
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Memory isn't the bottleneck: 90% recall a cue, yet 77% need several tries — the leak is between remembering and finding");
  card(s, M, 1.6, CW, 0.75, C.navy);
  txt(s, [
    { text: "North-star: ", options: { bold: true, color: "9FB3CC" } },
    { text: "% of vague-memory retrieval sessions (target photo ≥ 1 yr old) that end with the user opening and using the intended photo", options: { color: C.white } },
  ], { x: M + 0.25, y: 1.72, w: CW - 0.5, h: 0.55, fontSize: 16, valign: "middle" });

  const steps = [
    ["1  Remember", "User holds partial cues", "90%", "recall ≥ 1 cue; 68% recall 2+", "Survey n=31", C.blue, false],
    ["2  Express", "Cues become a search or a browse path", "74%", "scroll by date first; only 48% ever search", "Survey n=31", C.orange, true],
    ["3  Match", "App maps the cue to the right photo", "82%", "of review failures: a reasonable clue, misread", "Reviews n=84", C.orange, true],
    ["4  Recognise", "User spots it among results", "4%", "of review failures: too many results", "Reviews n=84", C.blue, false],
    ["5  Refine", "User recovers from a near-miss", "77%", "needed several tries; 77% have given up before", "Survey n=31", C.orange, true],
  ];
  const gw = 0.18, bw = (CW - gw * 4) / 5;
  steps.forEach(([h, sub, n, lab, src, col, leak], i) => {
    const x = M + i * (bw + gw), y = 2.6;
    card(s, x, y, bw, 4.1, leak ? "FDEEE6" : C.panel);
    txt(s, h, { x: x + 0.18, y: y + 0.18, w: bw - 0.36, h: 0.4, fontFace: HEAD, fontSize: 18, bold: true });
    txt(s, sub, { x: x + 0.18, y: y + 0.62, w: bw - 0.36, h: 0.75, fontSize: 14, color: C.muted });
    txt(s, n, { x: x + 0.18, y: y + 1.45, w: bw - 0.36, h: 0.8, fontFace: HEAD, fontSize: 40, bold: true, color: col === C.orange ? C.orangeDark : C.blueDark });
    txt(s, lab, { x: x + 0.18, y: y + 2.3, w: bw - 0.36, h: 1.0, fontSize: 14 });
    tag(s, src, x + 0.18, y + 3.55, col === C.orange ? C.orangeDark : C.blueDark);
  });
  footer(s, "Orange = where success leaks. Metric tree, data definitions and raw counts: research repo (survey-findings.md, discovery engine).");
  s.addNotes("Decomposition: Remember -> Express -> Match -> Recognise -> Refine. Survey: 28/31 remembered at least one cue, 21/31 two or more; 23/31 scrolled by date; 15/31 used any search; 24/31 found only after several tries; 24/31 have given up on a known photo. Reviews: of 84 genuine vague-memory failures, 69 app_misunderstands, 3 too_many_results, 3 cannot_express.");
}

// ---------- 3. Discovery engine: how it works ----------
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "An AI discovery engine turned 6,551 public posts into comparable evidence on where retrieval breaks");
  const steps = [
    ["Collect", "6,551 posts & reviews", "Reddit 2,002 · Play Store 3,249 · App Store 1,300 (US, IN, GB, CA, AU)"],
    ["Filter", "1,196 kept", "Cheap keyword gate drops storage, billing and praise-only reviews before any AI cost"],
    ["Extract", "15-field schema", "Gemini structured output per post: photo type, cues remembered vs forgotten, failure stage, workaround, verbatim quote"],
    ["Classify", "84 core failures", "Second AI pass separates true vague-memory failures from UI regressions (95) and data loss (28)"],
    ["Compare & ask", "Live, testable", "Slice and compare segments; ask a question and get an answer grounded in cited user quotes"],
  ];
  const gw = 0.28, bw = (CW - gw * 4) / 5, y = 1.75;
  steps.forEach(([h, big, body], i) => {
    const x = M + i * (bw + gw);
    card(s, x, y, bw, 3.6);
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.22, w: 0.5, h: 0.5, fill: { color: C.blue }, line: { color: C.blue } });
    txt(s, String(i + 1), { x: x + 0.2, y: y + 0.26, w: 0.5, h: 0.42, fontSize: 18, bold: true, color: C.white, align: "center", valign: "middle" });
    txt(s, h, { x: x + 0.2, y: y + 0.85, w: bw - 0.4, h: 0.4, fontFace: HEAD, fontSize: 18, bold: true });
    txt(s, big, { x: x + 0.2, y: y + 1.3, w: bw - 0.4, h: 0.45, fontSize: 16, bold: true, color: C.blueDark });
    txt(s, body, { x: x + 0.2, y: y + 1.8, w: bw - 0.4, h: 1.7, fontSize: 14, color: C.muted });
    if (i < 4) s.addShape(pres.shapes.RIGHT_TRIANGLE, { x: x + bw + 0.07, y: y + 1.65, w: 0.14, h: 0.28, rotate: 0, fill: { color: C.line }, line: { color: C.line }, flipH: false });
  });
  card(s, M, 5.6, CW, 1.05, C.navy);
  txt(s, [
    { text: "Beyond sentiment: ", options: { bold: true, color: "9FB3CC" } },
    { text: "every post is tagged against the retrieval journey, so failure modes can be counted and cross-tabbed by photo type, cue and workaround.  ", options: { color: C.white } },
    { text: "Try it live →", options: { color: C.white, bold: true, underline: { style: "sng" }, hyperlink: { url: LINKS.engine } } },
  ], { x: M + 0.3, y: 5.72, w: CW - 0.6, h: 0.8, fontSize: 16, valign: "middle" });
  footer(s, "Stack: Apify + open-source scrapers → Python → Gemini (free tier, JSON schema) → Streamlit Cloud. Built at zero cost.");
  s.addNotes("One-slide workflow explanation required by the brief. Link: " + LINKS.engine);
}

// ---------- 4. Discovery findings ----------
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Reviews say people remember what's in the photo — words, objects, people — and search misreads exactly those clues");
  txt(s, "What 84 users with a vague-memory failure remembered vs. forgot", { x: M, y: 1.6, w: 6.6, h: 0.4, fontSize: 16, bold: true });
  s.addChart(pres.charts.BAR, [
    { name: "Remembered", labels: ["Words in photo", "Visual detail", "Rough time", "People", "Exact date", "Place"], values: [19, 16, 7, 6, 4, 3] },
    { name: "Forgot", labels: ["Words in photo", "Visual detail", "Rough time", "People", "Exact date", "Place"], values: [0, 4, 16, 1, 8, 14] },
  ], {
    x: M, y: 2.0, w: 6.6, h: 4.6, barDir: "bar", barGrouping: "clustered", barGapWidthPct: 60,
    chartColors: [C.blue, C.orange], showLegend: true, legendPos: "t", legendFontSize: 14, legendFontFace: BODY, legendColor: C.ink,
    catAxisLabelFontSize: 14, catAxisLabelFontFace: BODY, catAxisLabelColor: C.ink, catAxisOrientation: "maxMin",
    valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 14, dataLabelColor: C.ink, dataLabelFontFace: BODY,
  });
  const qx = M + 7.0, qw = CW - 7.0;
  const quotes = [
    ["“I know there's multiple screenshots with the words 'silver-blue eyes' in it and nothing is showing up”", "Play Store review"],
    ["“I switch back to Classic Search and put in same word and got all the pics I was expecting”", "Reddit, r/googlephotos"],
    ["“I have to attempt 3-4 different searches for other things that might be in the picture”", "Play Store review"],
  ];
  quotes.forEach(([q, src], i) => {
    const y = 1.65 + i * 1.28;
    card(s, qx, y, qw, 1.15);
    txt(s, q, { x: qx + 0.22, y: y + 0.12, w: qw - 0.44, h: 0.72, fontSize: 14, italic: true });
    txt(s, src, { x: qx + 0.22, y: y + 0.82, w: qw - 0.44, h: 0.3, fontSize: 14, color: C.muted });
  });
  card(s, qx, 5.55, qw, 1.1, C.navy);
  txt(s, [
    { text: "External validation: ", options: { bold: true, color: "9FB3CC" } },
    { text: "Google paused its Gemini 'Ask Photos' rollout in 2026 after users said it found less than classic search.", options: { color: C.white } },
  ], { x: qx + 0.22, y: 5.65, w: qw - 0.44, h: 0.9, fontSize: 14, valign: "middle" });
  footer(s, "Source: discovery engine, 84 genuine vague-memory failures (of 243 retrieval-related posts). TechCrunch, 10 Mar 2026.");
  s.addNotes("69 of 84 failures = app misunderstood a reasonable clue (82%). Remembered/forgot counts from Gemini tagging. Competitive landscape: " + LINKS.market);
}

// ---------- 5. User research ----------
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "But most people never search: 74% scroll by date — the very cue 61% of them had forgotten");
  const sx = M, sw = 3.7;
  [["74%", "scrolled the timeline by date to find it", C.orangeDark],
   ["48%", "used search at all; 29% only ever scrolled", C.blueDark],
   ["61%", "had forgotten the exact date they were scrolling for", C.orangeDark]]
    .forEach(([n, l, c], i) => stat(s, n, l, sx, 1.65 + i * 1.62, sw, c));
  tag(s, "Survey n=31", sx, 6.45, C.blueDark);

  const cx = M + 4.2, cw = CW - 4.2;
  txt(s, "Observed in a live retrieval task (interview P1)", { x: cx, y: 1.65, w: cw, h: 0.4, fontSize: 16, bold: true });
  const rows = [
    ["Receipt, 2 years old", "Typed the brand he remembered correctly → photos of the machine, not the receipt. Vendor name → nothing. Generic 'bill' → found.", "“The keyword matters.”"],
    ["Restaurant, unsure of year", "Typed the restaurant's name → found instantly, 8 years old. A proper noun rescued a missing date.", "Found first try"],
    ["PAN card photo (past attempt)", "Couldn't find it in Google Photos or OneDrive after ~2 minutes, so re-photographed the card instead.", "Workaround: recreate, not retrieve"],
  ];
  rows.forEach(([h, b, k], i) => {
    const y = 2.1 + i * 1.3;
    card(s, cx, y, cw, 1.18);
    txt(s, h, { x: cx + 0.22, y: y + 0.12, w: 2.3, h: 0.9, fontSize: 15, bold: true });
    txt(s, b, { x: cx + 2.6, y: y + 0.12, w: cw - 5.3, h: 0.95, fontSize: 14 });
    txt(s, k, { x: cx + cw - 2.5, y: y + 0.12, w: 2.3, h: 0.95, fontSize: 14, bold: true, color: C.blueDark });
  });
  txt(s, [
    { text: "Why sources disagree: ", options: { bold: true } },
    { text: "a public review exists only when search fails loudly; the survey also catches silent scroll failures. Interviews P2–P6 in progress.", options: {} },
  ], { x: cx, y: 6.05, w: cw, h: 0.65, fontSize: 14, color: C.muted });
  footer(s, "Methods: Google Form survey (n=31) · contextual interviews with live tasks on participants' own libraries. Findings & guide in research repo.");
  s.addNotes("Survey findings: " + LINKS.survey + "  Interview guide: " + LINKS.guide + "  UPDATE this slide once P2-P6 are synthesised.");
}

// ---------- 6. Target segment ----------
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Target: long-time users with deep, mixed libraries — they hit this monthly, and sometimes it really matters");
  // 2x2 reach x severity
  const px = M + 0.5, py = 1.75, pw = 5.6, ph = 4.6;
  s.addShape(pres.shapes.LINE, { x: px, y: py + ph, w: pw, h: 0, line: { color: C.muted, width: 1.5 } });
  s.addShape(pres.shapes.LINE, { x: px, y: py, w: 0, h: ph, line: { color: C.muted, width: 1.5 } });
  txt(s, "Reach (share of users) →", { x: px, y: py + ph + 0.08, w: pw, h: 0.35, fontSize: 14, color: C.muted, align: "right" });
  txt(s, "Severity →", { x: px - 0.55, y: py - 0.02, w: 1.2, h: 0.35, fontSize: 14, color: C.muted, rotate: 270 });
  const segs = [
    ["Deep-library users", "5+ yrs, 10k+ items", 3.3, 0.4, true],
    ["Utility-photo savers", "IDs, bills, labels", 0.35, 0.55, false],
    ["Family archivists", "search by person", 1.8, 2.05, false],
    ["Casual / new users", "small, recent libraries", 0.35, 3.5, false],
  ];
  segs.forEach(([h, sub, dx, dy, pick]) => {
    const x = px + dx, y = py + dy, w = 2.15, h2 = 0.95;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: h2, rectRadius: 0.1, fill: { color: pick ? C.blue : C.panel }, line: { color: pick ? C.blueDark : C.line, width: pick ? 2 : 1 } });
    txt(s, h, { x: x + 0.12, y: y + 0.1, w: w - 0.24, h: 0.4, fontSize: 15, bold: true, color: pick ? C.white : C.ink });
    txt(s, sub, { x: x + 0.12, y: y + 0.5, w: w - 0.24, h: 0.35, fontSize: 14, color: pick ? "E4EEFB" : C.muted });
  });
  txt(s, "Chosen: deep-library users who also save utility photos — the overlap of the top two boxes.", { x: px, y: py + ph + 0.4, w: pw + 0.4, h: 0.4, fontSize: 14, bold: true, color: C.blueDark });

  const rx = M + 6.8, rw = CW - 6.8;
  const facts = [
    ["65%", "of respondents have 5+ years of photos"],
    ["77%", "often save screenshots, bills, IDs (4–5 on a 5-point scale)"],
    ["52%", "struggle to find a known photo monthly or more"],
    ["35%", "say it sometimes really matters — proof, a task, a memory"],
  ];
  facts.forEach(([n, l], i) => {
    const y = 1.75 + i * 1.05;
    txt(s, n, { x: rx, y, w: 1.5, h: 0.7, fontFace: HEAD, fontSize: 34, bold: true, color: C.blueDark });
    txt(s, l, { x: rx + 1.6, y: y + 0.08, w: rw - 1.6, h: 0.8, fontSize: 15 });
  });
  tag(s, "Survey n=31", rx, 6.05, C.blueDark);
  footer(s, "Why this segment: vague memory only exists in deep libraries; utility photos are the time-pressured, high-stakes retrievals.");
  s.addNotes("Segmentation by usage behaviour, not demographics or photo type (70% of review failures didn't fit a single photo-type niche). Full doc: research/market-research/user-segmentation.md");
}

// ---------- 7. Root cause & problem ----------
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Root cause: both paths to an old photo run on what memory doesn't keep — exact dates and exact keywords");
  card(s, M, 1.6, CW, 1.2, C.navy);
  txt(s, "Long-time Google Photos users remember a photo by its context — who, where, what it showed, the words in it — but cannot turn those partial cues into the photo, because the timeline is ordered by a date they've forgotten and search rewards guessing the index's keyword, with no way to refine from a near-miss.",
    { x: M + 0.3, y: 1.7, w: CW - 0.6, h: 1.0, fontSize: 16, color: C.white, valign: "middle" });
  const colW = (CW - 0.4) / 2;
  [["Scroll path breaks", "Needs a date. 61% had forgotten the exact date; the timeline offers no other way in.", C.orange],
   ["Search path breaks", "Needs the right word. A correct brand name failed where a generic 'bill' worked; 82% of review failures were a reasonable clue misread.", C.orange]]
    .forEach(([h, b], i) => {
      const x = M + i * (colW + 0.4);
      card(s, x, 3.0, colW, 1.35, "FDEEE6");
      txt(s, h, { x: x + 0.25, y: 3.12, w: colW - 0.5, h: 0.4, fontFace: HEAD, fontSize: 18, bold: true, color: C.orangeDark });
      txt(s, b, { x: x + 0.25, y: 3.55, w: colW - 0.5, h: 0.75, fontSize: 14 });
    });
  const cols = [
    ["Workarounds today", ["Scroll month by month", "Ask someone who was there", "Re-photograph the document", "Give up — 77% have"]],
    ["Value to users", ["Minutes back per search", "Documents at the moment of need", "Memories that stop being 'lost'"]],
    ["Value to Google Photos", ["Retrieval is why people keep 15 years of photos here", "Protects Google One storage retention", "Rebuilds trust in AI search after the Ask Photos pause"]],
  ];
  const w3 = (CW - 0.6) / 3;
  cols.forEach(([h, items], i) => {
    const x = M + i * (w3 + 0.3);
    card(s, x, 4.55, w3, 2.2);
    txt(s, h, { x: x + 0.22, y: 4.67, w: w3 - 0.44, h: 0.4, fontSize: 16, bold: true, color: C.blueDark });
    txt(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1 } })),
      { x: x + 0.22, y: 5.1, w: w3 - 0.44, h: 1.6, fontSize: 14, paraSpaceAfter: 4 });
  });
  s.addNotes("Evolution: business metric -> decomposition (leak at Express/Match/Refine) -> discovery engine (82% misread clues) -> survey (74% scroll, 61% forget date) -> interview (keyword luck, recreate-not-retrieve) -> this problem statement.");
}

// ---------- 8. Solution rationale & MVP (draft) ----------
{
  const s = pres.addSlide(); s.background = { color: C.white };
  draftBadge(s);
  title(s, "Opportunity: let people search with the memory they have — any cue, in any order — and recover from near-misses");
  const items = [
    ["Understand fuzzy, multi-cue descriptions", "“My son, sprinkler, Delhi, a few summers ago” — people, place, activity and rough time together, not one keyword."],
    ["Swap dates for life landmarks", "“Around my sister's wedding”, “when we lived in Pune” — anchors people actually keep."],
    ["Explain the match, ask one question on a miss", "Show which cue matched; on low confidence ask a single narrowing question instead of returning nothing."],
  ];
  items.forEach(([h, b], i) => {
    const y = 1.7 + i * 1.5;
    s.addShape(pres.shapes.OVAL, { x: M, y: y + 0.05, w: 0.55, h: 0.55, fill: { color: C.blue }, line: { color: C.blue } });
    txt(s, String(i + 1), { x: M, y: y + 0.1, w: 0.55, h: 0.45, fontSize: 18, bold: true, color: C.white, align: "center", valign: "middle" });
    txt(s, h, { x: M + 0.8, y, w: 5.6, h: 0.45, fontSize: 17, bold: true });
    txt(s, b, { x: M + 0.8, y: y + 0.48, w: 5.6, h: 0.9, fontSize: 14, color: C.muted });
  });
  const mx = M + 6.9, mw = CW - 6.9;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: mx, y: 1.7, w: mw, h: 4.2, rectRadius: 0.12, fill: { color: C.panel }, line: { color: C.line, width: 1, dashType: "dash" } });
  txt(s, "MVP screenshot + live link\n(added once built)", { x: mx, y: 3.4, w: mw, h: 0.8, fontSize: 16, color: C.muted, align: "center", valign: "middle" });
  txt(s, "Why here: the research shows memory is present (90%) — intelligence is needed to interpret it and to recover from misses, not to help people remember.",
    { x: M, y: 6.1, w: CW, h: 0.65, fontSize: 15, bold: true, color: C.blueDark });
  s.addNotes("DRAFT. Direction follows from root cause; confirm with P2-P6 before building. Replace placeholder with MVP screenshot and link.");
}

// ---------- 9. MVP testing (placeholder) ----------
{
  const s = pres.addSlide(); s.background = { color: C.white };
  draftBadge(s);
  title(s, "[After testing] X of Y users found their own vague-memory photo with the MVP — and what we'd change next");
  const w3 = (CW - 0.6) / 3;
  ["Tester 1", "Tester 2", "Tester 3"].forEach((t, i) => {
    const x = M + i * (w3 + 0.3);
    card(s, x, 1.7, w3, 3.1);
    txt(s, t, { x: x + 0.22, y: 1.82, w: w3 - 0.44, h: 0.4, fontSize: 16, bold: true });
    txt(s, [
      { text: "Task: ", options: { bold: true } }, { text: "real photo from their interview", options: { breakLine: true } },
      { text: "Baseline (Google Photos): ", options: { bold: true } }, { text: "tries / time / found?", options: { breakLine: true } },
      { text: "With MVP: ", options: { bold: true } }, { text: "tries / time / found?", options: { breakLine: true } },
      { text: "Key quote: ", options: { bold: true } }, { text: "…", options: {} },
    ], { x: x + 0.22, y: 2.3, w: w3 - 0.44, h: 2.4, fontSize: 14, color: C.muted, paraSpaceAfter: 6 });
  });
  card(s, M, 5.0, CW, 1.7, C.panel);
  txt(s, "What we'd change in the next iteration", { x: M + 0.25, y: 5.12, w: CW - 0.5, h: 0.4, fontSize: 16, bold: true });
  txt(s, "1. …    2. …    3. …", { x: M + 0.25, y: 5.6, w: CW - 0.5, h: 0.9, fontSize: 14, color: C.muted });
  s.addNotes("PLACEHOLDER — fill after testing with at least 3 users on tasks from the interviews.");
}

// ---------- 10. Metrics & risks (draft) ----------
{
  const s = pres.addSlide(); s.background = { color: C.white };
  draftBadge(s);
  title(s, "Success = more vague-memory searches ending in the right photo, fewer retries and fewer 're-photographed' documents");
  const lw = 6.3;
  const groups = [
    ["North-star", ["Vague-memory retrieval success rate (photo ≥ 1 yr old opened and used)"], C.navy],
    ["Leading", ["Share of searches using 2+ cues or a life landmark", "Near-miss recovery: found within 2 turns after a miss", "Median time and tries to found"], C.blueDark],
    ["Diagnostic", ["Zero-result rate for descriptive queries", "Scroll depth before (or instead of) search", "New document photo within 10 min of a failed document search"], C.blueDark],
    ["Guardrails", ["Search latency · Gemini opt-out rate · privacy complaints"], C.muted],
  ];
  let y = 1.65;
  groups.forEach(([h, items, col]) => {
    txt(s, h, { x: M, y, w: 1.7, h: 0.35, fontSize: 15, bold: true, color: col });
    txt(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1 } })),
      { x: M + 1.75, y, w: lw - 1.75, h: 0.36 * items.length, fontSize: 14, paraSpaceAfter: 2 });
    y += 0.36 * items.length + 0.28;
  });
  const rx = M + lw + 0.4, rw = CW - lw - 0.4;
  txt(s, "Top risks → mitigations", { x: rx, y: 1.65, w: rw, h: 0.35, fontSize: 16, bold: true });
  const risks = [
    ["Confident wrong matches erode trust", "Show which cue matched; keep classic results alongside (Google's own Ask Photos fix)"],
    ["Personal photos sent to an LLM", "Query the existing index and on-device signals; no new photo data leaves"],
    ["Clarifying questions feel slow", "At most one question, only on low confidence"],
    ["Small, network-biased research sample", "Validate with a logged A/B on the north-star before rollout"],
  ];
  risks.forEach(([r, m], i) => {
    const yy = 2.1 + i * 1.12;
    card(s, rx, yy, rw, 1.0);
    txt(s, r, { x: rx + 0.2, y: yy + 0.08, w: rw - 0.4, h: 0.38, fontSize: 14, bold: true, color: C.orangeDark });
    txt(s, m, { x: rx + 0.2, y: yy + 0.46, w: rw - 0.4, h: 0.5, fontSize: 14 });
  });
  s.addNotes("DRAFT — metrics must reflect the MVP actually built. The re-photograph diagnostic comes from interview P1 (PAN card).");
}

pres.writeFile({ fileName: __dirname + "/NL_GooglePhotos.pptx" }).then(f => console.log("wrote", f));

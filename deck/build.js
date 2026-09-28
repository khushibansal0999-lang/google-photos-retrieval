// Builds deck/NL_GooglePhotos.pptx  →  upload to Drive → Open with Google Slides.
// Brief rules: 10 slides max (title counted), no fellow name, key-message titles,
// every font >= 14pt, colour-blind-safe (blue/orange), links to artefacts.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.title = "NL_GooglePhotos";

const C = {
  ink: "1C2530", muted: "4E5A67", navy: "14213D", white: "FFFFFF",
  panel: "EEF2F6", line: "D5DCE4", warmPanel: "FDEEE6",
  blue: "2A78D6", blueDark: "1C5CAB", orange: "EB6834", orangeDark: "B04515",
  green: "1B7A4B",
};
const HEAD = "Roboto Slab", BODY = "Roboto";
const W = 13.333, M = 0.6, CW = W - 2 * M;
const L = {
  engine: "https://app-photos-retrieval-qvlu7ymwqfadwg3siqnqjb.streamlit.app/",
  repo: "https://github.com/khushibansal0999-lang/google-photos-retrieval",
  problem: "https://github.com/khushibansal0999-lang/google-photos-retrieval/blob/main/research/problem-definition.md",
  test: "https://github.com/khushibansal0999-lang/google-photos-retrieval/blob/main/research/first-party-test.md",
  survey: "https://github.com/khushibansal0999-lang/google-photos-retrieval/blob/main/research/survey/survey-findings.md",
  market: "https://github.com/khushibansal0999-lang/google-photos-retrieval/blob/main/research/market-research/competitive-landscape.md",
  plan: "https://github.com/khushibansal0999-lang/google-photos-retrieval/blob/main/research/execution-plan.md",
  solution: "https://github.com/khushibansal0999-lang/google-photos-retrieval/blob/main/research/solution-selection.md",
};

const txt = (s, t, o) => s.addText(t, { fontFace: BODY, fontSize: 15, color: C.ink, margin: 0, valign: "top", isTextBox: true, ...o });
function title(s, t, o = {}) {
  txt(s, t, { x: M, y: 0.40, w: CW, h: 1.0, fontFace: HEAD, fontSize: 25, bold: true, valign: "middle", ...o });
}
function card(s, x, y, w, h, fill = C.panel, lineCol) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: lineCol || fill } });
}
function tag(s, label, x, y, color = C.blueDark) {
  const w = 0.2 + label.length * 0.093;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.3, rectRadius: 0.15, fill: { color }, line: { color } });
  txt(s, label, { x, y: y + 0.015, w, h: 0.27, fontSize: 14, bold: true, color: C.white, align: "center", valign: "middle" });
}
function footer(s, t, dark = false) {
  txt(s, t, { x: M, y: 6.98, w: CW, h: 0.33, fontSize: 14, color: dark ? "B8C4D6" : C.muted });
}
function draftBadge(s) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: W - M - 2.75, y: 0.1, w: 2.75, h: 0.32, rectRadius: 0.16, fill: { color: "FFF1E8" }, line: { color: C.orangeDark, width: 1 } });
  txt(s, "TO COMPLETE: MVP in build", { x: W - M - 2.75, y: 0.12, w: 2.75, h: 0.28, fontSize: 14, bold: true, color: C.orangeDark, align: "center", valign: "middle" });
}

/* ───────────────────────── 1 · Title ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.navy };
  txt(s, "Google Photos · Core Experience", { x: M, y: 0.85, w: CW, h: 0.35, fontSize: 16, color: "9FB3CC", bold: true });
  txt(s, "People remember the moment.\nThe app only accepts the metadata.", { x: M, y: 1.35, w: 10.5, h: 2.0, fontFace: HEAD, fontSize: 40, bold: true, color: C.white });
  txt(s, "Photos people know they have stay unreachable, because both ways in need what memory doesn't keep: an exact date, or the exact word.",
    { x: M, y: 3.5, w: 9.2, h: 0.9, fontSize: 18, color: "D8E1EC" });
  const links = [["AI Discovery Engine (live, testable)", L.engine], ["AI-native MVP: link on submission", null], ["Research artefacts: problem definition, survey, interviews, plan", L.repo]];
  links.forEach(([label, url], i) => {
    const y = 4.75 + i * 0.5;
    s.addShape(pres.shapes.OVAL, { x: M, y: y + 0.11, w: 0.14, h: 0.14, fill: { color: url ? C.blue : C.orange }, line: { color: url ? C.blue : C.orange } });
    txt(s, url ? [{ text: label + "  →", options: { hyperlink: { url }, color: C.white, underline: { style: "sng" } } }] : [{ text: label, options: { color: "9FB3CC" } }],
      { x: M + 0.33, y, w: 9.5, h: 0.38, fontSize: 16 });
  });
  footer(s, "NextLeap Product Management Fellowship · Graduation Project · October 2026", true);
  s.addNotes("Title. No fellow name. Evidence base: 1,196 tagged public posts, survey n=31, interviews P1-P2, first-party test on production Ask Photos.");
}

/* ───────────────────────── 2 · Metric decomposition ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Breaking the metric down: people arrive remembering plenty. Retrieval breaks when those memories meet the index");
  card(s, M, 1.5, CW, 0.7, C.navy);
  txt(s, [{ text: "North star:  ", options: { bold: true, color: "9FB3CC" } },
          { text: "% of sessions hunting a specific photo ≥1 year old that end with the user opening it, without guessing a date or a keyword", options: { color: C.white } }],
    { x: M + 0.25, y: 1.6, w: CW - 0.5, h: 0.5, fontSize: 16, valign: "middle" });

  const steps = [
    ["Remember", "Holds partial cues", "90% recall ≥1 cue\n68% recall 2 or more", false],
    ["Express", "Turns cues into a query or a browse path", "74% scroll by date\nonly 48% ever search", true],
    ["Match", "Index maps cue → photo", "82% of failures: a fair\nclue, misread", true],
    ["Evaluate", "Spots it among results", "one query returned\n64 items for one bill", true],
    ["Recover", "Narrows after a miss", "77% needed several tries\nnothing narrows for them", true],
  ];
  const gw = 0.2, bw = (CW - gw * 4) / 5;
  steps.forEach(([h, sub, stat, leak], i) => {
    const x = M + i * (bw + gw), y = 2.45;
    card(s, x, y, bw, 3.3, leak ? C.warmPanel : C.panel);
    txt(s, h, { x: x + 0.2, y: y + 0.18, w: bw - 0.4, h: 0.38, fontFace: HEAD, fontSize: 19, bold: true, color: leak ? C.orangeDark : C.blueDark });
    txt(s, sub, { x: x + 0.2, y: y + 0.62, w: bw - 0.4, h: 0.8, fontSize: 14, color: C.muted });
    txt(s, stat, { x: x + 0.2, y: y + 1.5, w: bw - 0.4, h: 1.5, fontSize: 15, bold: true, lineSpacingMultiple: 1.2 });
  });
  card(s, M, 5.95, CW, 0.9, C.panel);
  txt(s, [{ text: "Four independent lenses on one journey, not a funnel. ", options: { bold: true } },
          { text: "The percentages come from different samples (survey n=31 · tagged reviews n=84 · interviews) and are not multiplied. They agree on where the leak is: everything after Remember.", options: {} }],
    { x: M + 0.25, y: 6.06, w: CW - 0.5, h: 0.7, fontSize: 14, valign: "middle" });
  footer(s, "Orange = leaking. Full metric tree and raw counts in the research repo.");
  s.addNotes("Deliberately NOT a chained funnel: denominators differ. Survey: 28/31 one cue, 21/31 two+, 23/31 scroll, 15/31 search, 24/31 several tries. Reviews: 69/84 app misread the clue.");
}

/* ───────────────────────── 3 · Discovery engine (required workflow slide) ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "How the AI discovery engine works: 6,551 public posts turned into comparable, queryable evidence");
  const steps = [
    ["Collect", "6,551 posts", "Reddit 2,002 · Play Store 3,249 · App Store 1,300 across US, IN, GB, CA, AU"],
    ["Filter", "1,196 kept", "Keyword gate drops storage, billing and praise-only posts before any AI spend"],
    ["Extract", "15-field schema", "Gemini structured output per post: photo type, cues remembered vs forgotten, failure stage, workaround, verbatim quote"],
    ["Classify", "84 core cases", "Second pass separates true vague-memory failures from UI regressions (95) and data loss (28)"],
    ["Compare & ask", "Live tool", "Cross-tab any segment; ask a question, get an answer grounded in cited quotes"],
  ];
  const gw = 0.28, bw = (CW - gw * 4) / 5, y = 1.65;
  steps.forEach(([h, big, body], i) => {
    const x = M + i * (bw + gw);
    card(s, x, y, bw, 3.5);
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.22, w: 0.48, h: 0.48, fill: { color: C.blue }, line: { color: C.blue } });
    txt(s, String(i + 1), { x: x + 0.2, y: y + 0.25, w: 0.48, h: 0.42, fontSize: 18, bold: true, color: C.white, align: "center", valign: "middle" });
    txt(s, h, { x: x + 0.2, y: y + 0.82, w: bw - 0.4, h: 0.38, fontFace: HEAD, fontSize: 18, bold: true });
    txt(s, big, { x: x + 0.2, y: y + 1.24, w: bw - 0.4, h: 0.4, fontSize: 16, bold: true, color: C.blueDark });
    txt(s, body, { x: x + 0.2, y: y + 1.7, w: bw - 0.4, h: 1.7, fontSize: 14, color: C.muted });
  });
  card(s, M, 5.45, CW, 1.1, C.navy);
  txt(s, [{ text: "Why this is more than sentiment analysis:  ", options: { bold: true, color: "9FB3CC" } },
          { text: "every post is tagged against the retrieval journey, so failure modes can be counted and cross-tabbed by photo type, cue and workaround. Every claim traces back to a quote.   ", options: { color: C.white } },
          { text: "Try it live →", options: { color: C.white, bold: true, underline: { style: "sng" }, hyperlink: { url: L.engine } } }],
    { x: M + 0.3, y: 5.56, w: CW - 0.6, h: 0.9, fontSize: 16, valign: "middle" });
  footer(s, "Built entirely on free tiers: open-source scrapers → Python → Gemini (JSON schema) → Streamlit Cloud.");
  s.addNotes("This is the 1-slide workflow explanation the brief requires. Link: " + L.engine);
}

/* ───────────────────────── 4 · Discovery findings ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "The engine's verdict: 82% of failures were a fair clue the app misread");
  txt(s, "What 84 users with a genuine vague-memory failure remembered, and what they'd lost", { x: M, y: 1.42, w: 6.7, h: 0.35, fontSize: 15, bold: true });
  // Hand-drawn bars: native charts lose their category labels when converted to Google Slides.
  const LEG = [["Remembered", C.blue], ["Forgotten", C.orange]];
  LEG.forEach(([name, col], i) => {
    const lx = M + i * 1.75;
    s.addShape(pres.shapes.RECTANGLE, { x: lx, y: 1.88, w: 0.24, h: 0.16, fill: { color: col }, line: { color: col } });
    txt(s, name, { x: lx + 0.33, y: 1.83, w: 1.3, h: 0.28, fontSize: 14 });
  });
  const DATA = [
    ["Words in the photo", 19, 0], ["Visual detail", 16, 4], ["Roughly when", 7, 16],
    ["Who was there", 6, 1], ["Exact date", 4, 8], ["Where it was", 3, 14],
  ];
  const bx0 = M + 2.05, SC = 0.205, bh = 0.26;
  DATA.forEach(([label, rem, forg], i) => {
    const y = 2.28 + i * 0.73;
    txt(s, label, { x: M, y: y + 0.08, w: 1.95, h: 0.5, fontSize: 14 });
    [[rem, C.blue, 0], [forg, C.orange, bh + 0.05]].forEach(([v, col, dy]) => {
      if (v > 0) s.addShape(pres.shapes.RECTANGLE, { x: bx0, y: y + dy, w: v * SC, h: bh, fill: { color: col }, line: { color: col } });
      txt(s, String(v), { x: bx0 + (v > 0 ? v * SC : 0) + 0.08, y: y + dy - 0.02, w: 0.45, h: 0.3, fontSize: 14, bold: true, color: v > 0 ? C.ink : C.muted });
    });
  });
  const qx = M + 7.05, qw = CW - 7.05;
  txt(s, "In their words", { x: qx, y: 1.45, w: qw, h: 0.38, fontSize: 15, bold: true });
  [["“I know there's multiple screenshots with the words 'silver-blue eyes' in it and nothing is showing up”", "Play Store"],
   ["“I switch back to Classic Search and put in same word and got all the pics I was expecting”", "Reddit · r/googlephotos"],
   ["“I have to attempt 3-4 different searches for other things that might be in the picture”", "Play Store"]].forEach(([q, src], i) => {
    const y = 1.85 + i * 1.22;
    card(s, qx, y, qw, 1.1);
    txt(s, q, { x: qx + 0.22, y: y + 0.13, w: qw - 0.44, h: 0.7, fontSize: 14, italic: true });
    txt(s, src, { x: qx + 0.22, y: y + 0.8, w: qw - 0.44, h: 0.26, fontSize: 14, color: C.muted });
  });
  card(s, qx, 5.55, qw, 1.25, C.navy);
  txt(s, [{ text: "Google has already been burned here.  ", options: { bold: true, color: "9FB3CC" } },
          { text: "It paused the Gemini “Ask Photos” rollout in 2026 after users said it found less than classic search, then put classic results back alongside it.", options: { color: C.white } }],
    { x: qx + 0.22, y: 5.66, w: qw - 0.44, h: 1.05, fontSize: 14, valign: "middle" });
  footer(s, "84 genuine vague-memory failures of 243 retrieval-related posts. Only 3 of 84 were users who couldn't describe what they wanted.");
  s.addNotes("Key: the leak is at Match, not Remember. Competitive landscape: " + L.market);
}

/* ───────────────────────── 5 · User research ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Talking to users broke the review-data story: most people never search at all. They scroll for a date they've forgotten");
  [["74%", "scroll the timeline by date", C.orangeDark],
   ["48%", "ever use search; 29% only ever scroll", C.blueDark],
   ["61%", "had forgotten the very date they were scrolling for", C.orangeDark]].forEach(([n, l], i) => {
    const y = 1.5 + i * 1.5;
    txt(s, n, { x: M, y, w: 1.7, h: 0.8, fontFace: HEAD, fontSize: 44, bold: true, color: i === 1 ? C.blueDark : C.orangeDark });
    txt(s, l, { x: M, y: y + 0.82, w: 3.4, h: 0.62, fontSize: 15 });
  });
  tag(s, "Survey n=31", M, 6.15);

  const cx = M + 3.9, cw = CW - 3.9;
  txt(s, "Watched in live retrieval tasks on people's own libraries", { x: cx, y: 1.45, w: cw, h: 0.35, fontSize: 15, bold: true });
  [["P1 · a receipt, 2 years old", "The brand name he correctly remembered returned the appliance, not its receipt. The vendor name returned nothing. The generic word “bill” found it, third try.", "“The keyword matters.”"],
   ["P2 · 75,000 photos, 4 years", "Hits this weekly. Finds photos eventually, by accident. “When randomly scrolling over my gallery later I find it.”", "Late isn't found"],
   ["P1 and P2 · both, unprompted", "P1 gave up after 2 minutes and re-photographed his PAN card. P2: “I choose alternative path for that work.”", "They route around the app"]].forEach(([h, b, k], i) => {
    const y = 1.85 + i * 1.42;
    card(s, cx, y, cw, 1.3);
    txt(s, h, { x: cx + 0.22, y: y + 0.13, w: 2.55, h: 1.05, fontSize: 15, bold: true });
    txt(s, b, { x: cx + 2.95, y: y + 0.13, w: cw - 5.5, h: 1.1, fontSize: 14 });
    txt(s, k, { x: cx + cw - 2.35, y: y + 0.13, w: 2.15, h: 1.05, fontSize: 14, bold: true, color: C.blueDark });
  });
  txt(s, [{ text: "Why the sources disagreed: ", options: { bold: true } },
          { text: "a public review only exists when search fails loudly. The survey also catches the silent scroll failures. In both interviews, abandonment meant the job got done another way.", options: {} }],
    { x: cx, y: 6.15, w: cw, h: 0.6, fontSize: 14, color: C.muted });
  footer(s, "Method: contextual interviews with live tasks on participants' own libraries + Google Form survey. P3-P6 in progress.");
  s.addNotes("Survey: " + L.survey + " · Interview method deliberately task-based because self-report about search behaviour is unreliable.");
}

/* ───────────────────────── 6 · Root cause, proven ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Root cause, reproduced on the live product: the app silently guesses the one thing users are least sure about: when");
  txt(s, "One photo · one library · production Google Photos with Gemini “Ask Photos” · five queries", { x: M, y: 1.4, w: CW, h: 0.35, fontSize: 15, bold: true });

  const rows = [
    ["“bill from last august”", "Ambiguous", "Nothing found. Then showed unrelated photos from August 2026: selfies, decorations.", false],
    ["“…last august at one8”  (added the venue)", "Ambiguous", "Zero results. More accurate detail made it worse, not better.", false],
    ["“bill receipt of dinner last year”", "Unambiguous", "Found it.", true],
    ["“bill from august 2025”  ← control", "Explicit", "Instant. Itemised to the dish, with the total and related payment screenshots.", true],
    ["“restaurant bill, dinner with friends, around a year ago”", "Openly vague", "Found it and led with it, but buried in ~64 loosely-related photos.", true],
  ];
  const yTop = 1.85, rh = 0.72;
  rows.forEach(([q, kind, res, ok], i) => {
    const y = yTop + i * rh;
    card(s, M, y, CW, rh - 0.1, ok ? C.panel : C.warmPanel);
    txt(s, q, { x: M + 0.22, y: y + 0.11, w: 4.5, h: 0.45, fontSize: 14, bold: true });
    txt(s, kind, { x: M + 4.85, y: y + 0.11, w: 1.5, h: 0.45, fontSize: 14, color: C.muted });
    txt(s, (ok ? "✓  " : "✕  ") + res, { x: M + 6.45, y: y + 0.11, w: CW - 6.7, h: 0.45, fontSize: 14, color: ok ? C.green : C.orangeDark, bold: !ok });
  });

  card(s, M, 5.6, CW, 1.2, C.navy);
  txt(s, [{ text: "Same photo. Same word, “bill”. Only the date phrasing changed.  ", options: { bold: true, color: C.white } },
          { text: "“Last August” was silently read as August 2026 and turned into a hard filter. The bill was from August 2025. Content matching was never broken. ", options: { color: "D8E1EC" } },
          { text: "Being honestly vague (“around a year ago”) beat being confidently approximate (“last August”).", options: { color: C.white, bold: true } }],
    { x: M + 0.3, y: 5.72, w: CW - 0.6, h: 1.0, fontSize: 15, valign: "middle" });
  footer(s, "First-party test with a control, 28 Sep 2026. Full log and screenshots in the research repo.");
  s.addNotes("The strongest evidence in the project: first-party, reproducible, controlled. One clarifying question ('August 2025 or 2026?') would have solved it in one turn. Detail: " + L.test);
}

/* ───────────────────────── 7 · Problem framing canvas ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Memory is intact. What is missing is anywhere to put it, and any way back from a near-miss");

  card(s, M, 1.32, CW, 0.92, C.navy);
  txt(s, [{ text: "The true problem:  ", options: { bold: true, color: "9FB3CC" } },
          { text: "People who have kept photos for years remember an old photo the way memory stores it: who was there, where it was, what was in frame, why they took it. Google Photos accepts only what memory does not keep, an exact date to scroll to or the exact word the index holds. So the photo is not lost. It is unreachable at the moment it is needed.", options: { color: C.white } }],
    { x: M + 0.28, y: 1.4, w: CW - 0.56, h: 0.78, fontSize: 14, valign: "middle" });

  const w3 = (CW - 0.5) / 3, yA = 2.42, hA = 2.35;
  // WHO
  card(s, M, yA, w3, hA);
  txt(s, "Who faces it", { x: M + 0.2, y: yA + 0.12, w: w3 - 0.4, h: 0.3, fontSize: 15, bold: true, color: C.blueDark });
  txt(s, "Long-tenure users with deep, mixed libraries. Written so an analyst could query it:", { x: M + 0.2, y: yA + 0.46, w: w3 - 0.4, h: 0.5, fontSize: 14 });
  card(s, M + 0.2, yA + 0.98, w3 - 0.4, 0.92, "E4EAF1");
  txt(s, "account_age ≥ 3 yrs\nAND library_size ≥ 2,000\nAND utility_share ≥ 15%\nAND ≥1 retrieval of an item >365d old",
    { x: M + 0.32, y: yA + 1.06, w: w3 - 0.64, h: 0.8, fontSize: 14, fontFace: "Consolas", color: C.ink, lineSpacingMultiple: 0.95 });
  txt(s, "Vague memory is a function of library depth. A 400-photo user just scrolls and finds it.", { x: M + 0.2, y: yA + 1.98, w: w3 - 0.4, h: 0.4, fontSize: 14, color: C.muted });
  // HOW WE KNOW
  const bx = M + w3 + 0.25;
  card(s, bx, yA, w3, hA);
  txt(s, "How we know it is real", { x: bx + 0.2, y: yA + 0.12, w: w3 - 0.4, h: 0.3, fontSize: 15, bold: true, color: C.blueDark });
  [["6,551 posts → 84 core cases", "82% of failures: a fair clue misread"],
   ["Survey n=31", "74% scroll; 61% forgot that date"],
   ["2 live task interviews", "Both re-did the task instead of finding it"],
   ["Controlled test on the live app", "Same photo, same word. Only the date phrasing changed."]].forEach(([h, b], i) => {
    const y = yA + 0.5 + i * 0.47;
    txt(s, h, { x: bx + 0.2, y, w: w3 - 0.4, h: 0.22, fontSize: 14, bold: true });
    txt(s, b, { x: bx + 0.2, y: y + 0.21, w: w3 - 0.4, h: 0.24, fontSize: 14, color: C.muted });
  });
  // WHY NOW
  const cx = M + 2 * (w3 + 0.25);
  card(s, cx, yA, w3, hA);
  txt(s, "Why now", { x: cx + 0.2, y: yA + 0.12, w: w3 - 0.4, h: 0.3, fontSize: 15, bold: true, color: C.blueDark });
  txt(s, [{ text: "The capability already ships. ", options: { bold: true } }, { text: "“august 2025” returns an itemised answer instantly. This is a disambiguation fix, not new ML.", options: { breakLine: true } },
          { text: "The trust window is closing. ", options: { bold: true } }, { text: "Ask Photos was paused in 2026 and classic search restored beside it. Users are being taught the AI path is the unreliable one.", options: { breakLine: true } },
          { text: "Libraries only get deeper. ", options: { bold: true } }, { text: "The condition for the problem is elapsed time, so the segment grows every month.", options: {} }],
    { x: cx + 0.2, y: yA + 0.48, w: w3 - 0.4, h: 1.8, fontSize: 14, paraSpaceAfter: 5 });

  // IMPACT SIZING chain
  const yS = 4.95;
  card(s, M, yS, CW, 0.78, "E4EAF1");
  txt(s, "Impact sizing", { x: M + 0.22, y: yS + 0.24, w: 1.3, h: 0.3, fontSize: 14, bold: true, color: C.blueDark });
  const chain = [["1.5B", "monthly users"], ["× 35%", "deep, mixed libraries"], ["= 525M", "segment"], ["× 52%", "fail monthly+"], ["= 273M", "failing every month"]];
  chain.forEach(([n, l], i) => {
    const x = M + 1.65 + i * 2.18;
    txt(s, n, { x, y: yS + 0.1, w: 2.0, h: 0.34, fontSize: 17, bold: true, color: i === 4 ? C.orangeDark : C.ink });
    txt(s, l, { x, y: yS + 0.44, w: 2.0, h: 0.26, fontSize: 14, color: C.muted });
  });

  // VALUE
  const yV = 5.85, wv = (CW - 0.3) / 2;
  card(s, M, yV, wv, 1.0, C.warmPanel);
  txt(s, "Value for users", { x: M + 0.22, y: yV + 0.1, w: wv - 0.44, h: 0.26, fontSize: 14, bold: true, color: C.orangeDark });
  txt(s, "Documents arrive when they are needed · moments arrive while they still matter · the archive keeps the one promise it makes.", { x: M + 0.22, y: yV + 0.38, w: wv - 0.44, h: 0.55, fontSize: 14 });
  card(s, M + wv + 0.3, yV, wv, 1.0, C.panel);
  txt(s, "Value for Google Photos", { x: M + wv + 0.52, y: yV + 0.1, w: wv - 0.44, h: 0.26, fontSize: 14, bold: true, color: C.blueDark });
  txt(s, "Retrieval is the only reason a 15-year archive stays put, and deep libraries are the paying libraries. Today this failure is invisible in telemetry because people route around it.", { x: M + wv + 0.52, y: yV + 0.38, w: wv - 0.44, h: 0.55, fontSize: 14 });
  s.addNotes("Sizing: 1.5B MAU is Google's own 10th-anniversary figure (May 2025). Survey said 68% deep-library; halved to 35% because n=31 skews engaged. All figures labelled estimates. Full canvas: " + L.problem);
}

/* ───────────────────────── 8 · Three solutions, one bet ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  draftBadge(s);
  title(s, "The widest-reach idea scored lowest, because nobody asked for it. We bet on the one we can prove");

  const sols = [
    ["S1 · Never guess silently", "Stop resolving an ambiguous date in silence. Ask one question (“August 2025 or 2026?”) or show both windows labelled. Accept several cues at once, say why each result matched, and narrow on a miss instead of returning nothing.",
     ["Reach 8", "Impact 9", "Confidence 9", "Effort 2"], "324", true],
    ["S2 · Memory anchors", "Replace the date axis. Derive landmarks from the library itself (trips, a house move, a new face) and let people browse by “around when we moved” instead of by month.",
     ["Reach 10", "Impact 7", "Confidence 4", "Effort 8"], "35", false],
    ["S3 · Narrow it down together", "Return a few high-signal candidates instead of a grid, and let the user eliminate by attribute: not this person, not indoors, earlier than this.",
     ["Reach 6", "Impact 6", "Confidence 6", "Effort 6"], "36", false],
  ];
  const gw = 0.28, bw = (CW - gw * 2) / 3, y0 = 1.35;
  sols.forEach(([h, body, rice, score, win], i) => {
    const x = M + i * (bw + gw);
    card(s, x, y0, bw, 2.75, win ? "E8F0FB" : C.panel, win ? C.blue : C.panel);
    txt(s, h, { x: x + 0.2, y: y0 + 0.13, w: bw - 0.4, h: 0.3, fontSize: 15, bold: true, color: win ? C.blueDark : C.ink });
    txt(s, body, { x: x + 0.2, y: y0 + 0.48, w: bw - 0.4, h: 1.35, fontSize: 14, color: C.muted });
    rice.forEach((r, j) => txt(s, r, { x: x + 0.2 + (j % 2) * 1.75, y: y0 + 1.9 + Math.floor(j / 2) * 0.28, w: 1.7, h: 0.26, fontSize: 14 }));
    txt(s, "RICE " + score, { x: x + 0.2, y: y0 + 2.42, w: bw - 0.4, h: 0.28, fontSize: 15, bold: true, color: win ? C.blueDark : C.muted });
  });
  txt(s, [{ text: "The honest tension: ", options: { bold: true } },
          { text: "S2 reaches the 74% who scroll, the widest behaviour in our data, and still loses. It scores 4 on confidence because no user asked for it. We named it the next bet rather than dropping it.", options: {} }],
    { x: M, y: 4.2, w: CW, h: 0.4, fontSize: 14, color: C.muted });

  const dy = 4.68, dw = (CW - 0.5) / 3;
  [["Does it solve the problem?", "The control test already proves it. “bill from last august” returned nothing; “bill from august 2025” returned an instant itemised answer. One question closes that gap in a single turn.", C.blueDark],
   ["Is it differentiated?", "Google, Apple and Immich all guess silently. ChatGPT and Gemini ask, but cannot see your library. Nothing does both. The differentiator is surfacing uncertainty, not “AI search”.", C.blueDark],
   ["What stops a competitor copying it?", "The interaction is copyable in a week. The moat is underneath: judging ambiguity needs this user’s 15-year history, it runs on the existing index so no new data leaves, and it ships where the failure happens.", C.orangeDark]]
    .forEach(([h, b, col], i) => {
      const x = M + i * (dw + 0.25);
      card(s, x, dy, dw, 1.55);
      txt(s, h, { x: x + 0.2, y: dy + 0.11, w: dw - 0.4, h: 0.28, fontSize: 14, bold: true, color: col });
      txt(s, b, { x: x + 0.2, y: dy + 0.42, w: dw - 0.4, h: 1.05, fontSize: 14 });
    });
  txt(s, [{ text: "Sizing this bet: ", options: { bold: true } },
          { text: "273M users fail monthly × 82% of failures are a misread clue = ~224M addressable. At a deliberately pessimistic 1-in-5 rescue rate, ~45M more successful retrievals a month.", options: {} },
          { text: "   Kill it if: ", options: { bold: true, color: C.orangeDark } },
          { text: "clarifying questions exceed 0.4 per session, or anyone asks for the plain grid back.", options: { color: C.orangeDark } }],
    { x: M, y: 6.38, w: CW, h: 0.5, fontSize: 14 });
  s.addNotes("RICE scored with confidence = evidence, not enthusiasm. Full scoring and defence: " + L.solution);
}

/* ───────────────────────── 9 · MVP + testing ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  draftBadge(s);
  title(s, "[To complete] Tested against the tasks users actually failed: baseline first, then the MVP");
  card(s, M, 1.45, CW, 1.15, C.navy);
  txt(s, [{ text: "Test design, fixed before building:  ", options: { bold: true, color: "9FB3CC" } },
          { text: "3 users from the interview pool, each given their own real task from their own session. They attempt it in Google Photos first (attempts + time), then in the MVP. Success was defined in advance: ≥2 of 3 find it, in fewer attempts, and nobody asks for the plain grid back.", options: { color: C.white } }],
    { x: M + 0.3, y: 1.56, w: CW - 0.6, h: 0.95, fontSize: 15, valign: "middle" });
  const w3 = (CW - 0.6) / 3;
  ["Tester 1", "Tester 2", "Tester 3"].forEach((t, i) => {
    const x = M + i * (w3 + 0.3);
    card(s, x, 2.85, w3, 2.6);
    txt(s, t, { x: x + 0.22, y: 2.97, w: w3 - 0.44, h: 0.35, fontSize: 16, bold: true });
    txt(s, [{ text: "Their task: ", options: { bold: true } }, { text: "from their own interview", options: { breakLine: true } },
            { text: "In Google Photos: ", options: { bold: true } }, { text: "attempts / time / found?", options: { breakLine: true } },
            { text: "In the MVP: ", options: { bold: true } }, { text: "attempts / time / found?", options: { breakLine: true } },
            { text: "What they said: ", options: { bold: true } }, { text: "…", options: {} }],
      { x: x + 0.22, y: 3.4, w: w3 - 0.44, h: 2.0, fontSize: 14, color: C.muted, paraSpaceAfter: 6 });
  });
  card(s, M, 5.65, CW, 1.15, C.panel);
  txt(s, "What we'd change next", { x: M + 0.25, y: 5.76, w: CW - 0.5, h: 0.32, fontSize: 15, bold: true });
  txt(s, "Reported honestly against the criteria above, including a partial or failed result if that's what the testing shows.", { x: M + 0.25, y: 6.12, w: CW - 0.5, h: 0.55, fontSize: 14, color: C.muted });
  s.addNotes("Fill after testing on 3 Oct. Criteria are pre-registered so they can't move.");
}

/* ───────────────────────── 10 · Metrics + risks ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  draftBadge(s);
  title(s, "Success means fewer retries, fewer dead ends, and fewer documents photographed a second time");
  const lw = 6.4;
  let y = 1.45;
  [["North star", ["Vague-memory retrieval success rate: photo ≥1 yr old, opened and used"], C.navy],
   ["Leading", ["Share of queries carrying 2+ cues", "Clarifying question accepted, then found within 2 turns", "Median attempts and time to found"], C.blueDark],
   ["Diagnostic", ["Zero-result rate on descriptive queries", "Scroll depth before (or instead of) searching", "A document re-photographed within 10 min of a failed search: the “routing around” signal"], C.blueDark],
   ["Guardrails", ["Latency · clarifying questions per session · opt-out rate · privacy complaints"], C.muted],
  ].forEach(([h, items, col]) => {
    txt(s, h, { x: M, y, w: 1.55, h: 0.35, fontSize: 15, bold: true, color: col });
    txt(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1 } })),
      { x: M + 1.6, y, w: lw - 1.6, h: 0.42 * items.length, fontSize: 14, paraSpaceAfter: 3 });
    y += 0.42 * items.length + 0.32;
  });
  const rx = M + lw + 0.4, rw = CW - lw - 0.4;
  txt(s, "What could make this fail, and how we would see it coming", { x: rx, y: 1.45, w: rw, h: 0.3, fontSize: 15, bold: true });
  [["The question fires when it should not",
    "Cause: scoring treats an unambiguous phrase as ambiguous, so every query gets interrupted.",
    "Signal: >0.4 questions per session, or >50% skipped.",
    "Fix, and its cost: only fire below 0.75 confidence, hard cap one per session. We will miss some genuinely ambiguous cases and return a wider set instead. A false interruption costs more trust than a wide result."],
   ["A confident wrong answer",
    "Cause: the model resolves an ambiguity correctly for most users but wrongly for this one, and states it as fact.",
    "Signal: result opened then abandoned within 3s; re-query within 30s.",
    "Fix, and its cost: show which cue matched, keep classic results beside it. Costs screen space and some perceived simplicity. This is Google's own fix after the Ask Photos pause."],
   ["The demo library flatters the result",
    "Cause: a seeded library is smaller and cleaner than a real 75,000-item one, so retrieval looks easier than it is.",
    "Signal: testers find items faster than their own Google Photos baseline by an implausible margin.",
    "Fix, and its cost: seed it with the real failures from interviews, and state the limitation on the slide rather than burying it. We accept lower external validity in exchange for a testable MVP inside the deadline."]]
    .forEach(([r, cause, sig, fix], i) => {
      const yy = 1.82 + i * 1.66;
      card(s, rx, yy, rw, 1.55);
      txt(s, r, { x: rx + 0.18, y: yy + 0.09, w: rw - 0.36, h: 0.25, fontSize: 14, bold: true, color: C.orangeDark });
      txt(s, cause, { x: rx + 0.18, y: yy + 0.36, w: rw - 0.36, h: 0.36, fontSize: 14, color: C.muted });
      txt(s, sig, { x: rx + 0.18, y: yy + 0.72, w: rw - 0.36, h: 0.26, fontSize: 14, bold: true, color: C.blueDark });
      txt(s, fix, { x: rx + 0.18, y: yy + 0.98, w: rw - 0.36, h: 0.52, fontSize: 14 });
    });
  s.addNotes("Metrics must be re-checked against the MVP actually shipped. The re-photograph diagnostic comes from P1 and P2.");
}

pres.writeFile({ fileName: __dirname + "/NL_GooglePhotos.pptx" }).then(f => console.log("wrote", f));

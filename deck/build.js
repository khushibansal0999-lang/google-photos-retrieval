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
  txt(s, "TO COMPLETE — MVP in build", { x: W - M - 2.75, y: 0.12, w: 2.75, h: 0.28, fontSize: 14, bold: true, color: C.orangeDark, align: "center", valign: "middle" });
}

/* ───────────────────────── 1 · Title ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.navy };
  txt(s, "Google Photos · Core Experience", { x: M, y: 0.85, w: CW, h: 0.35, fontSize: 16, color: "9FB3CC", bold: true });
  txt(s, "People remember the moment.\nThe app only accepts the metadata.", { x: M, y: 1.35, w: 10.5, h: 2.0, fontFace: HEAD, fontSize: 40, bold: true, color: C.white });
  txt(s, "Photos people know they have stay unreachable — because the two ways in both need what memory doesn't keep: an exact date, or the exact word.",
    { x: M, y: 3.5, w: 9.2, h: 0.9, fontSize: 18, color: "D8E1EC" });
  const links = [["AI Discovery Engine — live, testable", L.engine], ["AI-native MVP — link on submission", null], ["Research artefacts: problem definition, survey, interviews, plan", L.repo]];
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
  title(s, "Breaking the metric down: people arrive remembering plenty — retrieval breaks when those memories meet the index");
  card(s, M, 1.5, CW, 0.7, C.navy);
  txt(s, [{ text: "North star:  ", options: { bold: true, color: "9FB3CC" } },
          { text: "% of sessions hunting a specific photo ≥1 year old that end with the user opening it — without guessing a date or a keyword", options: { color: C.white } }],
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
  txt(s, [{ text: "Read as four independent lenses on one journey, not a funnel — ", options: { bold: true } },
          { text: "the percentages come from different samples (survey n=31 · tagged reviews n=84 · interviews) and are not multiplied. They agree on where the leak is: everything after Remember.", options: {} }],
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
          { text: "every post is tagged against the retrieval journey, so failure modes can be counted, compared and cross-tabbed by photo type, cue and workaround — and every claim traces back to a quote.   ", options: { color: C.white } },
          { text: "Try it live →", options: { color: C.white, bold: true, underline: { style: "sng" }, hyperlink: { url: L.engine } } }],
    { x: M + 0.3, y: 5.56, w: CW - 0.6, h: 0.9, fontSize: 16, valign: "middle" });
  footer(s, "Built entirely on free tiers: open-source scrapers → Python → Gemini (JSON schema) → Streamlit Cloud.");
  s.addNotes("This is the 1-slide workflow explanation the brief requires. Link: " + L.engine);
}

/* ───────────────────────── 4 · Discovery findings ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "The engine's verdict: memory isn't the problem — 82% of failures were a fair clue the app misread");
  txt(s, "What 84 users with a genuine vague-memory failure remembered — and what they'd lost", { x: M, y: 1.42, w: 6.7, h: 0.35, fontSize: 15, bold: true });
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
          { text: "It paused the Gemini “Ask Photos” rollout in 2026 after users said it found less than classic search — then put classic results back alongside it.", options: { color: C.white } }],
    { x: qx + 0.22, y: 5.66, w: qw - 0.44, h: 1.05, fontSize: 14, valign: "middle" });
  footer(s, "84 genuine vague-memory failures of 243 retrieval-related posts. Only 3 of 84 were users who couldn't describe what they wanted.");
  s.addNotes("Key: the leak is at Match, not Remember. Competitive landscape: " + L.market);
}

/* ───────────────────────── 5 · User research ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Talking to users broke the review-data story: most people never search at all — they scroll for a date they've forgotten");
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
   ["P2 · 75,000 photos, 4 years", "Hits this weekly. Finds photos eventually — by accident. “When randomly scrolling over my gallery later I find it.”", "Late isn't found"],
   ["P1 and P2 · both, unprompted", "P1 gave up after 2 minutes and re-photographed his PAN card. P2: “I choose alternative path for that work.”", "They route around the app"]].forEach(([h, b, k], i) => {
    const y = 1.85 + i * 1.42;
    card(s, cx, y, cw, 1.3);
    txt(s, h, { x: cx + 0.22, y: y + 0.13, w: 2.55, h: 1.05, fontSize: 15, bold: true });
    txt(s, b, { x: cx + 2.95, y: y + 0.13, w: cw - 5.5, h: 1.1, fontSize: 14 });
    txt(s, k, { x: cx + cw - 2.35, y: y + 0.13, w: 2.15, h: 1.05, fontSize: 14, bold: true, color: C.blueDark });
  });
  txt(s, [{ text: "Why the sources disagreed: ", options: { bold: true } },
          { text: "a public review only exists when search fails loudly. The survey also catches the silent scroll failures — and both interviews show abandonment usually means the job got done another way, not that it went undone.", options: {} }],
    { x: cx, y: 6.15, w: cw, h: 0.6, fontSize: 14, color: C.muted });
  footer(s, "Method: contextual interviews with live tasks on participants' own libraries + Google Form survey. P3–P6 in progress.");
  s.addNotes("Survey: " + L.survey + " · Interview method deliberately task-based because self-report about search behaviour is unreliable.");
}

/* ───────────────────────── 6 · Root cause, proven ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Root cause, reproduced on the live product: the app silently guesses the one thing users are least sure about — when");
  txt(s, "One photo · one library · production Google Photos with Gemini “Ask Photos” · five queries", { x: M, y: 1.4, w: CW, h: 0.35, fontSize: 15, bold: true });

  const rows = [
    ["“bill from last august”", "Ambiguous", "Nothing found. Then showed unrelated photos from August 2026 — selfies, decorations.", false],
    ["“…last august at one8”  (added the venue)", "Ambiguous", "Zero results. More accurate detail made it worse, not better.", false],
    ["“bill receipt of dinner last year”", "Unambiguous", "Found it.", true],
    ["“bill from august 2025”  ← control", "Explicit", "Instant. Itemised to the dish, with the total and related payment screenshots.", true],
    ["“restaurant bill, dinner with friends, around a year ago”", "Openly vague", "Found it and led with it — but buried in ~64 loosely-related photos.", true],
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
          { text: "“Last August” was silently read as August 2026 and turned into a hard filter — the bill was from August 2025. Content matching was never broken. ", options: { color: "D8E1EC" } },
          { text: "Being honestly vague (“around a year ago”) beat being confidently approximate (“last August”).", options: { color: C.white, bold: true } }],
    { x: M + 0.3, y: 5.72, w: CW - 0.6, h: 1.0, fontSize: 15, valign: "middle" });
  footer(s, "First-party test with a control, 28 Sep 2026. Full log and screenshots in the research repo.");
  s.addNotes("The strongest evidence in the project: first-party, reproducible, controlled. One clarifying question — 'August 2025 or 2026?' — would have solved it in one turn. Detail: " + L.test);
}

/* ───────────────────────── 7 · Problem definition ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "The problem: memory is intact — there's just nowhere to put it, and no way back from a near-miss");
  card(s, M, 1.45, CW, 1.35, C.navy);
  txt(s, "People who have kept photos for years remember an old photo the way memory stores it — who was there, where it was, what was in frame, why they took it. Google Photos accepts only what memory doesn't keep: an exact date to scroll to, or the exact word the index holds. There is nowhere to put the fragments they do have, and no way to narrow after a miss — so the photo isn't lost, it's unreachable at the moment it's needed.",
    { x: M + 0.3, y: 1.56, w: CW - 0.6, h: 1.15, fontSize: 16, color: C.white, valign: "middle" });

  const w3 = (CW - 0.6) / 3;
  [["Who", "Long-tenure users with deep, mixed libraries: 3+ years, 10k+ items, memory photos sitting beside bills, IDs and screenshots.",
    "65% have 5+ years · 77% save utility photos often"],
   ["When it bites", "They need one specific photo, over a year old, right now — to prove something, finish a task, or show someone.", "52% hit this monthly or more · 35% say it sometimes really matters"],
   ["What they do instead", "Scroll month by month · ask someone who was there · re-do the task · wait to stumble on it · give up.", "2 of 2 interviews re-did the task rather than find the photo"]]
    .forEach(([h, b, stat], i) => {
      const x = M + i * (w3 + 0.3);
      card(s, x, 3.0, w3, 2.05);
      txt(s, h, { x: x + 0.22, y: 3.12, w: w3 - 0.44, h: 0.35, fontSize: 16, bold: true, color: C.blueDark });
      txt(s, b, { x: x + 0.22, y: 3.5, w: w3 - 0.44, h: 1.0, fontSize: 14 });
      txt(s, stat, { x: x + 0.22, y: 4.5, w: w3 - 0.44, h: 0.45, fontSize: 14, bold: true, color: C.muted });
    });

  card(s, M, 5.25, (CW - 0.3) / 2, 1.5, C.warmPanel);
  txt(s, "Why it matters to users", { x: M + 0.25, y: 5.37, w: (CW - 0.3) / 2 - 0.5, h: 0.35, fontSize: 15, bold: true, color: C.orangeDark });
  txt(s, "Documents fail under time pressure · moments arrive too late to use · and the library quietly stops delivering the one promise it makes — that you can get back to it.",
    { x: M + 0.25, y: 5.75, w: (CW - 0.3) / 2 - 0.5, h: 0.9, fontSize: 14 });
  const bx = M + (CW - 0.3) / 2 + 0.3;
  card(s, bx, 5.25, (CW - 0.3) / 2, 1.5, C.panel);
  txt(s, "Why it matters to Google Photos", { x: bx + 0.25, y: 5.37, w: (CW - 0.3) / 2 - 0.5, h: 0.35, fontSize: 15, bold: true, color: C.blueDark });
  txt(s, "Retrieval is the only reason a 15-year archive stays put. Deep libraries are the paying libraries — and this failure is invisible in telemetry, because people quietly route around it.",
    { x: bx + 0.25, y: 5.75, w: (CW - 0.3) / 2 - 0.5, h: 0.9, fontSize: 14 });
  s.addNotes("Full problem definition, incl. evolution chain: " + L.problem);
}

/* ───────────────────────── 8 · Solution rationale ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  draftBadge(s);
  title(s, "The bet: take the memory people actually have — fuzzy time included — and never guess silently");
  const items = [
    ["Treat time as a range, never a silent filter", "Ambiguous date? Ask one question — “August 2025 or 2026?” — or search both and label them. Proven by control test to flip a total failure into an instant find.", "Strongest evidence"],
    ["Accept several partial cues at once", "Who + where + what + roughly when, together. 68% of people hold two or more cues; P2 listed four in one breath.", "Survey + interviews"],
    ["Recover from a near-miss", "Narrow with one follow-up instead of returning nothing. Today every retry starts from zero — 77% needed several tries.", "Survey + reviews"],
    ["Say why each result matched", "Rebuilds the trust the Ask Photos pause cost, and makes a wrong answer correctable instead of baffling.", "Competitive"],
  ];
  items.forEach(([h, b, src], i) => {
    const y = 1.5 + i * 1.22;
    card(s, M, y, 7.4, 1.12);
    s.addShape(pres.shapes.OVAL, { x: M + 0.22, y: y + 0.3, w: 0.5, h: 0.5, fill: { color: i === 0 ? C.orange : C.blue }, line: { color: i === 0 ? C.orange : C.blue } });
    txt(s, String(i + 1), { x: M + 0.22, y: y + 0.34, w: 0.5, h: 0.42, fontSize: 18, bold: true, color: C.white, align: "center", valign: "middle" });
    txt(s, h, { x: M + 0.85, y: y + 0.12, w: 5.2, h: 0.35, fontSize: 16, bold: true });
    txt(s, b, { x: M + 0.85, y: y + 0.48, w: 6.3, h: 0.6, fontSize: 14, color: C.muted });
    txt(s, src, { x: M + 6.2, y: y + 0.12, w: 1.1, h: 0.3, fontSize: 14, color: C.blueDark, bold: true, align: "right" });
  });
  const mx = M + 7.7, mw = CW - 7.7;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: mx, y: 1.5, w: mw, h: 3.35, rectRadius: 0.12, fill: { color: C.panel }, line: { color: C.line, width: 1, dashType: "dash" } });
  txt(s, "MVP screenshot\n+ live link", { x: mx, y: 2.9, w: mw, h: 0.7, fontSize: 16, color: C.muted, align: "center", valign: "middle" });
  card(s, mx, 5.0, mw, 1.35, C.navy);
  txt(s, [{ text: "“I just wish someone / any agent find it for me what I need.”\n", options: { italic: true, color: C.white } },
          { text: "— P2, unprompted, 75,000-photo library", options: { color: "9FB3CC" } }],
    { x: mx + 0.22, y: 5.12, w: mw - 0.44, h: 1.1, fontSize: 14, valign: "middle" });
  txt(s, [{ text: "Deliberately not doing yet: ", options: { bold: true } },
          { text: "life-landmark anchoring (no user asked for it) and redesigning the scroll path (74% reach — the bigger prize, but too big for this iteration). Named as the next bet, not quietly dropped.", options: {} }],
    { x: M, y: 6.5, w: CW, h: 0.45, fontSize: 14, color: C.muted });
  s.addNotes("Prioritised RICE-style; confidence = evidence, not enthusiasm. Full scoring: " + L.plan);
}

/* ───────────────────────── 9 · MVP + testing ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  draftBadge(s);
  title(s, "[To complete] Tested against the tasks users actually failed — baseline first, then the MVP");
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
  txt(s, "Reported honestly against the criteria above — including a partial or failed result, if that's what the testing shows.", { x: M + 0.25, y: 6.12, w: CW - 0.5, h: 0.55, fontSize: 14, color: C.muted });
  s.addNotes("Fill after testing on 3 Oct. Criteria are pre-registered so they can't move.");
}

/* ───────────────────────── 10 · Metrics + risks ───────────────────────── */
{
  const s = pres.addSlide(); s.background = { color: C.white };
  draftBadge(s);
  title(s, "Success means fewer retries, fewer dead ends — and fewer documents photographed a second time");
  const lw = 6.4;
  let y = 1.45;
  [["North star", ["Vague-memory retrieval success rate: photo ≥1 yr old, opened and used"], C.navy],
   ["Leading", ["Share of queries carrying 2+ cues", "Clarifying question accepted, then found within 2 turns", "Median attempts and time to found"], C.blueDark],
   ["Diagnostic", ["Zero-result rate on descriptive queries", "Scroll depth before (or instead of) searching", "A document re-photographed within 10 min of a failed search — the “routing around” signal"], C.blueDark],
   ["Guardrails", ["Latency · clarifying questions per session · opt-out rate · privacy complaints"], C.muted],
  ].forEach(([h, items, col]) => {
    txt(s, h, { x: M, y, w: 1.55, h: 0.35, fontSize: 15, bold: true, color: col });
    txt(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1 } })),
      { x: M + 1.6, y, w: lw - 1.6, h: 0.42 * items.length, fontSize: 14, paraSpaceAfter: 3 });
    y += 0.42 * items.length + 0.32;
  });
  const rx = M + lw + 0.4, rw = CW - lw - 0.4;
  txt(s, "What could make this fail", { x: rx, y: 1.45, w: rw, h: 0.35, fontSize: 15, bold: true });
  [["A confident wrong answer costs more trust than a blank one", "Show why it matched; keep classic results beside it — Google's own fix after the Ask Photos pause"],
   ["The clarifying question becomes friction", "Hard cap of one, only when confidence is genuinely split — tracked as a guardrail"],
   ["A seeded demo library flatters the result", "Seeded with real failures from interviews; limitation stated on the slide, not buried"],
   ["Small, network-skewed sample: n=31, all India, tech-adjacent", "Stated plainly. Real validation is a logged A/B on the north star"]]
    .forEach(([r, m], i) => {
      const yy = 1.85 + i * 1.25;
      card(s, rx, yy, rw, 1.12);
      txt(s, r, { x: rx + 0.2, y: yy + 0.1, w: rw - 0.4, h: 0.5, fontSize: 14, bold: true, color: C.orangeDark });
      txt(s, m, { x: rx + 0.2, y: yy + 0.58, w: rw - 0.4, h: 0.48, fontSize: 14 });
    });
  s.addNotes("Metrics must be re-checked against the MVP actually shipped. The re-photograph diagnostic comes from P1 and P2.");
}

pres.writeFile({ fileName: __dirname + "/NL_GooglePhotos.pptx" }).then(f => console.log("wrote", f));

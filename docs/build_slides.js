// Two-slide summary deck: "What isomorphic means" and "How the code works".
// Run from the circuit-banks repo root:  NODE_PATH=<dir with pptxgenjs> node docs/build_slides.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const ROOT = path.resolve(__dirname, "..");
const BANKS = path.join(ROOT, "PHY II Electricity and Magnetism", "1_DC Circuits");
const B10 = path.join(BANKS, "PHY2-DC-SPRTC-10222026", "figures");
const B30 = path.join(BANKS, "PHY2-DC-SPRTC3-10232026", "figures");
const ONLY = process.env.ONLY;   // ONLY=2 builds just slide 2 (for Quick Look QA, which shows only the first slide)
const OUT = ONLY ? path.join(process.env.TMPDIR || "/tmp", `slide-${ONLY}.pptx`) : path.join(__dirname, "circuit-bank-2-slides.pptx");

const THEME = {
  name: "Circuit bank",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1E1E1E", lt1: "FFFFFF", dk2: "2F4858", lt2: "F3EFEA",
    accent1: "8A2A1B",   // brick (the PDF's accent)
    accent2: "2F4858",   // slate
    accent3: "C9A66B",   // copper
    accent4: "DCE6EE",   // pale slate  (Chen)
    accent5: "E2EEDC",   // pale green  (circuit skill)
    accent6: "F7E3D4",   // pale copper (glue)
    hlink: "8A2A1B", folHlink: "2F4858",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";            // 13.33 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Myrla Phillippe";
pres.title = "The circuit bank in two slides";
const C = pres.SchemeColor;

pres.defineSlideMaster({
  title: "content",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.8, fontSize: 32, bold: true, color: C.text1, margin: 0, valign: "top", align: "left" } } },
    { text: { text: "The circuit bank in two slides", options: { x: 0.6, y: 7.05, w: 8, h: 0.3, fontSize: 9, color: "8A8A8A", margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.05, w: 0.5, h: 0.3, fontSize: 9, color: "8A8A8A" },
});

pres.addSection({ title: "Summary" });

// ------------------------------------------------------------------ helpers
function card(slide, x, y, w, h, fill, title, body, opts = {}) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: fill }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: title + " card" });
  slide.addText(title, { x: x + 0.18, y: y + 0.12, w: w - 0.36, h: 0.4, fontSize: opts.titleSize || 14, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: title });
  slide.addText(body, { x: x + 0.18, y: y + 0.52, w: w - 0.36, h: h - 0.6, fontSize: opts.bodySize || 11.5, color: C.text2, margin: 0, isTextBox: true, valign: "top", objectName: title + " text" });
}
function img(slide, file, x, y, w, h, name) {
  slide.addImage({ path: file, x, y, w, h, sizing: { type: "contain", w, h }, objectName: name });
}

// ================================================================== SLIDE 1
if (ONLY !== "2") {
  const s = pres.addSlide({ masterName: "content", sectionTitle: "Summary" });
  s.addText("What “isomorphic” means — and why it is built for the student", { placeholder: "title" });

  // left: the three criteria as stacked cards
  const L = 0.6, W = 5.6;
  card(s, L, 1.35, W, 1.25, THEME.colors.lt2, "1  More than new numbers",
    "Same circuit with different values is not a variation — students pattern-match the one solution path.");
  card(s, L, 2.75, W, 1.25, THEME.colors.lt2, "2  A different solution",
    "At least one reduction step must differ. Redrawing, reordering or renaming parts changes nothing.");
  card(s, L, 4.15, W, 1.25, THEME.colors.lt2, "3  Same objective, same difficulty",
    "Same question, same number of steps. A 2-step and a 5-step circuit are not isomorphs.");
  s.addText([
    { text: "Why it matters.  ", options: { bold: true, color: C.accent1 } },
    { text: "Each student draws one random item for the same exam slot. Below the floor the draw is pointless; above the ceiling it is unfair. Isomorphic is the band where the draw is both meaningful and fair.", options: { color: C.text1 } },
  ], { x: L, y: 5.6, w: W, h: 1.25, fontSize: 12.5, margin: 0, isTextBox: true, valign: "top", objectName: "why it matters" });

  // right: three real isomorphs
  const R = 6.6, CW = 2.0, GAP = 0.15;
  s.addText("Three items from the bank — same question, three different reduction paths", { x: R, y: 1.35, w: 6.1, h: 0.35, fontSize: 12.5, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "figure heading" });
  const figs = [
    [path.join(B10, "q1.png"), "3 || 6 + 4", "parallel pair, then series"],
    [path.join(B10, "q2.png"), "(4 + 2) || 6 + 3", "series pair inside a parallel"],
    [path.join(B10, "q3.png"), "2 || 3 || 6 + 4", "three-way parallel, then series"],
  ];
  figs.forEach(([f, lingo, note], i) => {
    const x = R + i * (CW + GAP);
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.8, w: CW, h: 1.75, fill: { color: "FFFFFF" }, line: { color: "D8D2CA", width: 0.75 }, rectRadius: 0.06, objectName: "frame " + (i + 1) });
    img(s, f, x + 0.08, 1.88, CW - 0.16, 1.6, "circuit " + (i + 1));
    s.addText(lingo, { x, y: 3.6, w: CW, h: 0.3, fontSize: 11, fontFace: "Courier New", color: C.text1, align: "center", margin: 0, isTextBox: true, objectName: "lingo " + (i + 1) });
    s.addText(note, { x, y: 3.9, w: CW, h: 0.45, fontSize: 10, color: C.text2, align: "center", margin: 0, isTextBox: true, objectName: "note " + (i + 1) });
  });

  // right-bottom: student-facing guarantees
  const rows = [
    ["One difficulty per bank", "every item reduces in exactly 3 steps"],
    ["Every item a new path", "canonical-shape check: same shape = same problem"],
    ["Wrong answers are real mistakes", "each distractor is computed from one named error"],
    ["One drawing style, clean arithmetic", "the only thing that varies is the physics"],
  ];
  s.addText("Built with the student in mind", { x: R, y: 4.55, w: 6.1, h: 0.35, fontSize: 12.5, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "guarantees heading" });
  rows.forEach(([k, v], i) => {
    const y = 4.95 + i * 0.47;
    s.addShape(pres.ShapeType.ellipse, { x: R, y: y + 0.07, w: 0.22, h: 0.22, fill: { color: THEME.colors.accent1 }, line: { color: THEME.colors.accent1, width: 0 }, objectName: "dot " + (i + 1) });
    s.addText([{ text: k + "  ", options: { bold: true, color: C.text1 } }, { text: v, options: { color: C.text2 } }],
      { x: R + 0.35, y, w: 5.75, h: 0.4, fontSize: 11.5, margin: 0, isTextBox: true, valign: "middle", objectName: "guarantee " + (i + 1) });
  });

  s.addNotes("Isomorphic is Zhongzhou Chen's term: a bank of problems that test the same objective with variations that change the solution, not only the numbers. " +
    "The three criteria give a floor (more than numbers; a different solution) and a ceiling (same difficulty). " +
    "The use case is a random draw per student for one exam slot, which is only fair inside that band. " +
    "For resistor networks, an isomorph is a different series-parallel topology asked the same way at the same number of steps.");
}

// ================================================================== SLIDE 2
{
  const s = pres.addSlide({ masterName: "content", sectionTitle: "Summary" });
  s.addText("How the code works — every number computed, none guessed", { placeholder: "title" });

  // pipeline
  const stages = [
    ["Input scheme", "what circuits,\nhow many, difficulty", "accent4"],
    ["Chen's loop", "sidecar: target,\naccepted / rejected", "accent4"],
    ["Enumerate", "every shape in the\nband, values by seed", "accent6"],
    ["Critic (script)", "parse · solve · shape\n· steps · ranges", "accent6"],
    ["Circuit engine", "figure, numbers,\nworked solution", "accent5"],
    ["Bank + PDF", "computed distractors;\nChen's template", "accent6"],
  ];
  const PX = 0.6, PY = 1.35, BW = 1.9, BH = 1.15, PG = 0.14;
  stages.forEach(([t, n, c], i) => {
    const x = PX + i * (BW + PG);
    s.addShape(pres.ShapeType.roundRect, { x, y: PY, w: BW, h: BH, fill: { color: THEME.colors[c] }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: "stage " + (i + 1) });
    s.addText(t, { x: x + 0.1, y: PY + 0.1, w: BW - 0.2, h: 0.35, fontSize: 13, bold: true, color: C.text1, align: "center", margin: 0, isTextBox: true, objectName: "stage title " + (i + 1) });
    s.addText(n, { x: x + 0.1, y: PY + 0.47, w: BW - 0.2, h: 0.6, fontSize: 10, color: C.text2, align: "center", margin: 0, isTextBox: true, valign: "top", objectName: "stage note " + (i + 1) });
    if (i < stages.length - 1) {
      s.addShape(pres.ShapeType.rightArrow, { x: x + BW - 0.02, y: PY + BH / 2 - 0.1, w: PG + 0.04, h: 0.2, fill: { color: "9A9A9A" }, line: { color: "9A9A9A", width: 0 }, objectName: "arrow " + (i + 1) });
    }
  });
  // legend
  const legend = [["accent4", "Zhongzhou Chen's method and scripts, used in place"], ["accent5", "circuit-diagram-skill (deterministic engine)"], ["accent6", "circuit-bank glue (deterministic)"]];
  let lx = 0.6;
  legend.forEach(([c, t], i) => {
    s.addShape(pres.ShapeType.rect, { x: lx, y: 2.65, w: 0.22, h: 0.18, fill: { color: THEME.colors[c] }, line: { color: "FFFFFF", width: 0 }, objectName: "legend " + (i + 1) });
    s.addText(t, { x: lx + 0.3, y: 2.6, w: 4.0, h: 0.28, fontSize: 10, color: C.text2, margin: 0, isTextBox: true, valign: "middle", objectName: "legend text " + (i + 1) });
    lx += 4.2;
  });

  // stats row
  const stats = [["34", "distinct 3-step shapes\nwith 4–6 resistors"], ["30", "items in the bank —\n30 of those 34"], ["0", "rejections, one pass;\nno LLM anywhere"], ["=", "same input + seed →\nsame bank, byte for byte"]];
  stats.forEach(([n, l], i) => {
    const x = 0.6 + i * 3.08;
    s.addShape(pres.ShapeType.roundRect, { x, y: 3.1, w: 2.95, h: 1.3, fill: { color: THEME.colors.lt2 }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: "stat card " + (i + 1) });
    s.addText(n, { x: x + 0.15, y: 3.15, w: 1.0, h: 1.2, fontSize: 44, bold: true, color: C.accent1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "stat " + (i + 1) });
    s.addText(l, { x: x + 1.2, y: 3.2, w: 1.65, h: 1.1, fontSize: 11, color: C.text1, margin: 0, isTextBox: true, valign: "middle", objectName: "stat label " + (i + 1) });
  });

  // bottom left: one item with computed distractors
  s.addText("One item, four computed options", { x: 0.6, y: 4.65, w: 6.0, h: 0.35, fontSize: 12.5, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "item heading" });
  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 5.05, w: 2.6, h: 1.85, fill: { color: "FFFFFF" }, line: { color: "D8D2CA", width: 0.75 }, rectRadius: 0.06, objectName: "item frame" });
  img(s, path.join(B10, "q1.png"), 0.68, 5.12, 2.44, 1.7, "item figure");
  const opts = [
    ["0.92 A", "adds all resistors in series"],
    ["2.67 A", "sums reciprocals, forgets to invert"],
    ["1.33 A", "reports one branch current"],
    ["2.00 A", "correct: 3 ‖ 6 = 2 Ω; + 4 = 6 Ω; 12 / 6"],
  ];
  opts.forEach(([v, why], i) => {
    const y = 5.05 + i * 0.46;
    const ok = i === 3;
    s.addText([{ text: v + "   ", options: { bold: true, fontFace: "Courier New", color: ok ? C.accent1 : C.text1 } }, { text: why, options: { color: ok ? C.text1 : C.text2, italic: !ok } }],
      { x: 3.35, y, w: 3.3, h: 0.42, fontSize: 11, margin: 0, isTextBox: true, valign: "middle", objectName: "option " + (i + 1) });
  });

  // bottom right: the rejection reasons the critic writes
  s.addText("What the critic rejects (reasons written to Chen's sidecar)", { x: 6.95, y: 4.65, w: 5.8, h: 0.35, fontSize: 12.5, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "critic heading" });
  const rej = [
    ["does not parse / solve", "“The circuit line ends too early…”"],
    ["same canonical shape", "6 || 3 + 4 and 2 || 4 + 5 ≡ 3 || 6 + 4"],
    ["value out of range", "“R1 = 50 Ω is outside resistor_range [1, 24]”"],
    ["wrong difficulty", "“5 reduction steps; this bank wants 3”"],
  ];
  rej.forEach(([k, v], i) => {
    const y = 5.05 + i * 0.46;
    s.addShape(pres.ShapeType.ellipse, { x: 6.95, y: y + 0.1, w: 0.2, h: 0.2, fill: { color: THEME.colors.accent2 }, line: { color: THEME.colors.accent2, width: 0 }, objectName: "rdot " + (i + 1) });
    s.addText([{ text: k + "  ", options: { bold: true, color: C.text1 } }, { text: v, options: { color: C.text2, fontFace: i === 1 ? "Courier New" : undefined } }],
      { x: 7.3, y, w: 5.45, h: 0.42, fontSize: 11, margin: 0, isTextBox: true, valign: "middle", objectName: "reason " + (i + 1) });
  });

  s.addNotes("Chen's generate-critique-count loop runs unchanged (scenario_list.py). Two of his agents are replaced because circuits can be enumerated and verified: " +
    "the proposer is an enumerator over all series-parallel shapes in the difficulty band, and the critic is a script that parses, solves, canonicalises the shape, counts reduction steps and checks ranges. " +
    "The circuit engine (circuit-diagram-skill) produces every figure, number and worked solution; distractors are recomputed from named student mistakes. " +
    "34 shapes exist at 3 steps with 4-6 resistors; the bank uses 30 of them; same input and seed regenerate the identical bank.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log(OUT);
})();

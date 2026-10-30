// Full 12-slide deck: "How the circuit bank works".  Same theme and figures as the 2-slide version and the PDF.
// Run from the circuit-banks repo root:
//   NODE_PATH=<dir with pptxgenjs> PPTX_SKILL=<pptx skill dir> node docs/build_deck.js
// ONLY=n builds a one-slide file with slide n (Quick Look QA shows only a file's first slide).
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const ROOT = path.resolve(__dirname, "..");
const BANKS = path.join(ROOT, "PHY II Electricity and Magnetism", "1_DC Circuits");
const B10 = path.join(BANKS, "PHY2-DC-SPRTC-10222026", "figures");
const B30 = path.join(BANKS, "PHY2-DC-SPRTC3-10292026", "figures");
const ONLY = process.env.ONLY ? Number(process.env.ONLY) : null;
const OUT = ONLY ? path.join(process.env.TMPDIR || "/tmp", `deck-slide-${ONLY}.pptx`) : path.join(__dirname, "How-the-circuit-bank-works.pptx");

const THEME = {
  name: "Circuit bank",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1E1E1E", lt1: "FFFFFF", dk2: "2F4858", lt2: "F3EFEA",
    accent1: "8A2A1B", accent2: "2F4858", accent3: "C9A66B",
    accent4: "DCE6EE", accent5: "E2EEDC", accent6: "F7E3D4",
    hlink: "8A2A1B", folHlink: "2F4858",
  },
};
const K = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Myrla Phillippe";
pres.title = "How the circuit bank works";
const C = pres.SchemeColor;

pres.defineSlideMaster({
  title: "content",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.8, fontSize: 32, bold: true, color: C.text1, margin: 0, valign: "top", align: "left" } } },
    { text: { text: "How the circuit bank works", options: { x: 0.6, y: 7.05, w: 8, h: 0.3, fontSize: 9, color: "8A8A8A", margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.05, w: 0.5, h: 0.3, fontSize: 9, color: "8A8A8A" },
});
pres.defineSlideMaster({
  title: "dark",
  background: { color: K.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.9, y: 2.2, w: 11.5, h: 1.3, fontSize: 44, bold: true, color: C.background1, margin: 0, valign: "top", align: "left" } } },
    { placeholder: { options: { name: "body", type: "body", x: 0.9, y: 3.6, w: 11.0, h: 2.2, fontSize: 18, color: "DCE6EE", margin: 0, valign: "top" } } },
  ],
});

// ------------------------------------------------------------------ helpers
let n = 0;
function slide(masterName, sectionTitle) {
  n += 1;
  if (ONLY && n !== ONLY) return null;
  return pres.addSlide({ masterName, sectionTitle });
}
function card(s, x, y, w, h, fill, title, body, o = {}) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: fill }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: title + " card" });
  s.addText(title, { x: x + 0.18, y: y + 0.12, w: w - 0.36, h: 0.42, fontSize: o.titleSize || 15, bold: true, color: o.titleColor || C.text1, margin: 0, isTextBox: true, objectName: title });
  if (body) s.addText(body, { x: x + 0.18, y: y + 0.56, w: w - 0.36, h: h - 0.66, fontSize: o.bodySize || 12.5, color: C.text2, margin: 0, isTextBox: true, valign: "top", objectName: title + " text" });
}
function img(s, file, x, y, w, h, name) {
  s.addImage({ path: file, x, y, w, h, sizing: { type: "contain", w, h }, objectName: name });
}
function framed(s, file, x, y, w, h, name) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: "D8D2CA", width: 0.75 }, rectRadius: 0.06, objectName: name + " frame" });
  img(s, file, x + 0.08, y + 0.08, w - 0.16, h - 0.16, name);
}
function heading(s, text, x, y, w, name) {
  s.addText(text, { x, y, w, h: 0.38, fontSize: 14, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: name });
}
function dotRows(s, rows, x, y, w, step, color, name, fs = 12.5) {
  rows.forEach(([k, v], i) => {
    const yy = y + i * step;
    s.addShape(pres.ShapeType.ellipse, { x, y: yy + 0.1, w: 0.2, h: 0.2, fill: { color }, line: { color, width: 0 }, objectName: `${name} dot ${i + 1}` });
    s.addText([{ text: k + "  ", options: { bold: true, color: C.text1 } }, { text: v, options: { color: C.text2 } }],
      { x: x + 0.33, y: yy, w: w - 0.33, h: step - 0.04, fontSize: fs, margin: 0, isTextBox: true, valign: "middle", objectName: `${name} ${i + 1}` });
  });
}
function grid(s, rows, x, y, colW, rowH, o = {}) {
  // simple table from shapes: header row tinted, body rows alternate
  rows.forEach((r, i) => {
    const yy = y + i * rowH;
    let xx = x;
    r.forEach((cellText, j) => {
      const fill = i === 0 ? K.lt2 : (i % 2 === 0 ? "FAF8F5" : "FFFFFF");
      s.addShape(pres.ShapeType.rect, { x: xx, y: yy, w: colW[j], h: rowH, fill: { color: fill }, line: { color: "D8D2CA", width: 0.5 }, objectName: `cell ${i}-${j}` });
      s.addText(cellText, { x: xx + 0.1, y: yy, w: colW[j] - 0.2, h: rowH, fontSize: o.fs || 11.5, bold: i === 0, color: i === 0 ? C.text1 : (j === 0 ? C.text1 : C.text2), margin: 0, isTextBox: true, valign: "middle", objectName: `cell text ${i}-${j}` });
      xx += colW[j];
    });
  });
}

pres.addSection({ title: "How the circuit bank works" });
const SEC = "How the circuit bank works";

// ================================================================== 1 title
{
  const s = slide("dark", SEC);
  if (s) {
    s.addText("How the circuit bank works", { placeholder: "title" });
    s.addText([
      { text: "Isomorphic DC-circuit problem banks — what “isomorphic” means, why they are built for fairness to the student, and how the code produces 30 variations with every number computed, not guessed.", options: { breakLine: true } },
      { text: " ", options: { breakLine: true } },
      { text: "Myrla Phillippe · research group · October 2026", options: { fontSize: 14, color: "C9A66B" } },
    ], { placeholder: "body" });
    s.addNotes("Take Zhongzhou Chen's isomorphic-bank method, feed it a domain where the scenario is a circuit topology that a computer can enumerate and verify, and let a deterministic circuit engine do everything numerical. The result: every item has a different solution path, the same difficulty, computed wrong answers, and an answer key that regenerates byte for byte.");
  }
}

// ================================================================== 2 what isomorphic means
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("What “isomorphic” means here", { placeholder: "title" });
    const L = 0.6, W = 6.2;
    card(s, L, 1.4, W, 1.35, K.lt2, "1  More than new numbers", "“Same circuit, new values” is not a variation — students pattern-match the one solution path.");
    card(s, L, 2.9, W, 1.35, K.lt2, "2  A different solution", "At least one reduction step must differ. Redrawing, reordering or renaming parts changes nothing.");
    card(s, L, 4.4, W, 1.35, K.lt2, "3  Same objective, same difficulty", "Same question, same number of steps. A 2-step and a 5-step circuit are not isomorphs.");
    s.addText("Chen's repository: problems that test the same learning objectives “with variations that change the solution and not only the numbers”, drawn at random so no two students get the same item.",
      { x: L, y: 5.95, w: W, h: 0.9, fontSize: 11, italic: true, color: C.text2, margin: 0, isTextBox: true, valign: "top", objectName: "source quote" });
    // right: floor / band / ceiling
    const R = 7.3, RW = 5.4;
    heading(s, "A band with a floor and a ceiling", R, 1.4, RW, "band heading");
    const bands = [
      ["Below the floor", "same circuit, new numbers", "everyone has the same problem — the draw is pointless", "F3EFEA"],
      ["In the band", "different reduction path, same work", "the draw is meaningful and fair", "E2EEDC"],
      ["Above the ceiling", "different difficulty or objective", "one student's exam is harder — the draw is unfair", "F7E3D4"],
    ];
    bands.forEach(([t, ex, why, fill], i) => {
      const y = 1.9 + i * 1.45;
      s.addShape(pres.ShapeType.roundRect, { x: R, y, w: RW, h: 1.3, fill: { color: fill }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: `band ${i + 1}` });
      s.addText(t, { x: R + 0.2, y: y + 0.1, w: RW - 0.4, h: 0.35, fontSize: 14, bold: true, color: i === 1 ? C.accent1 : C.text1, margin: 0, isTextBox: true, objectName: `band title ${i + 1}` });
      s.addText([{ text: ex, options: { italic: true, color: C.text1, breakLine: true } }, { text: why, options: { color: C.text2 } }],
        { x: R + 0.2, y: y + 0.48, w: RW - 0.4, h: 0.75, fontSize: 12, margin: 0, isTextBox: true, valign: "top", objectName: `band text ${i + 1}` });
    });
    s.addText("Use case: each student draws one random item for the same exam slot.", { x: R, y: 6.3, w: RW, h: 0.5, fontSize: 12.5, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "use case" });
    s.addNotes("The word is Chen's. His three criteria give a floor (more than numbers; a different solution) and a ceiling (same difficulty). The use case is a random draw per student for one exam slot, which is only fair inside that band.");
  }
}

// ================================================================== 3 three real isomorphs
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("Three real isomorphs — same question, three reduction paths", { placeholder: "title" });
    const figs = [
      [path.join(B10, "q1.png"), "3 || 6 + 4", "parallel pair, then series", "12 V → 2.00 A"],
      [path.join(B10, "q2.png"), "(4 + 2) || 6 + 3", "series pair inside a parallel, then series", "18 V → 3.00 A"],
      [path.join(B10, "q3.png"), "2 || 3 || 6 + 4", "three-way parallel, then series", "20 V → 4.00 A"],
    ];
    const W = 3.9, G = 0.2, X0 = 0.6;
    figs.forEach(([f, lingo, note, ans], i) => {
      const x = X0 + i * (W + G);
      framed(s, f, x, 1.5, W, 2.9, `circuit ${i + 1}`);
      s.addText(lingo, { x, y: 4.55, w: W, h: 0.4, fontSize: 16, fontFace: "Courier New", color: C.text1, align: "center", margin: 0, isTextBox: true, objectName: `lingo ${i + 1}` });
      s.addText(note, { x, y: 5.0, w: W, h: 0.4, fontSize: 12.5, color: C.text2, align: "center", margin: 0, isTextBox: true, objectName: `note ${i + 1}` });
      s.addText(ans, { x, y: 5.4, w: W, h: 0.35, fontSize: 12, color: C.accent1, align: "center", margin: 0, isTextBox: true, objectName: `answer ${i + 1}` });
    });
    s.addText("For a resistor network, an isomorph is a different series-parallel topology — a different sequence of reductions — asked the same way. None of these can be solved by remembering another.",
      { x: 0.6, y: 6.0, w: 12.1, h: 0.8, fontSize: 13, color: C.text1, margin: 0, isTextBox: true, valign: "top", objectName: "takeaway" });
    s.addNotes("Three items from the first bank. The lingo line under each figure is the whole source of the item: parse it and you get the figure, the numbers and the worked solution. Three different reduction sequences; three different answers.");
  }
}

// ================================================================== 4 built for the student
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("Built with the student in mind", { placeholder: "title" });
    const rows = [
      ["Design choice", "What the student experiences", "How it is enforced"],
      ["One difficulty per bank", "Your drawn problem takes the same number of steps (3) with the same number of resistors (5–6) as your neighbour's.", "reduction_steps: 3, resistors 5–6 — the critic rejects anything else"],
      ["Every item a different path", "You cannot pass by memorising last year's problem.", "canonical-shape check: same shape = same problem"],
      ["Wrong answers are real mistakes", "Three options are the numbers one specific error each produces; a fifth sits near the largest so a lone big value is no giveaway.", "distractors.py re-solves the circuit as a mistaken student would, then adds a decoy near the largest"],
      ["Honest sizes", "A 144 A distractor is what the mistake really gives.", "deliberately not capped"],
      ["One drawing style", "The figure never changes style between items.", "layout: ladder for the whole bank"],
      ["Clean arithmetic", "Every intermediate resistance is a whole or half ohm.", "enumerator accepts only such value sets; pool ≤ 12 Ω"],
      ["A worked solution for every item", "Feedback shows every reduction step and a per-resistor table.", "written by the circuit engine into the bank"],
    ];
    grid(s, rows, 0.6, 1.45, [2.6, 4.9, 4.6], 0.66, { fs: 11.5 });
    s.addNotes("Every row is a guarantee the student gets, and the right column is where in the code it is enforced. None of them depends on an LLM behaving well.");
  }
}

// ================================================================== 5 computed distractors
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("Wrong answers are computed, not invented", { placeholder: "title" });
    framed(s, path.join(B10, "q1.png"), 0.6, 1.5, 5.2, 3.6, "item figure");
    s.addText("12 V battery · 3 || 6 + 4 · find the total current", { x: 0.6, y: 5.2, w: 5.2, h: 0.4, fontSize: 12.5, color: C.text2, align: "center", margin: 0, isTextBox: true, objectName: "item caption" });
    const opts = [
      ["0.92 A", "all_series", "adds every resistor as if in series: 12 / (3 + 6 + 4)"],
      ["2.67 A", "no_invert", "sums the reciprocals of the parallel pair but forgets to invert: 1/3 + 1/6 = 0.5 “Ω”"],
      ["1.33 A", "branch_current", "reports the current through R1 (one branch) instead of the total"],
      ["2.40 A", "decoy", "0.9 × the largest option — so the lone large value is not a giveaway by size"],
      ["2.00 A", "correct", "3 ‖ 6 = 2 Ω, + 4 = 6 Ω, 12 V / 6 Ω"],
    ];
    opts.forEach(([v, key, why], i) => {
      const y = 1.5 + i * 0.92, ok = key === "correct";
      s.addShape(pres.ShapeType.roundRect, { x: 6.3, y, w: 6.4, h: 0.82, fill: { color: ok ? K.accent5 : K.lt2 }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: `option card ${i + 1}` });
      s.addText(v, { x: 6.45, y: y + 0.06, w: 1.5, h: 0.7, fontSize: 20, bold: true, fontFace: "Courier New", color: ok ? C.accent1 : C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: `option ${i + 1}` });
      s.addText([{ text: key, options: { bold: true, fontFace: "Courier New", color: C.text1, breakLine: true } }, { text: why, options: { color: C.text2 } }],
        { x: 8.0, y: y + 0.06, w: 4.6, h: 0.7, fontSize: 11, margin: 0, isTextBox: true, valign: "middle", objectName: `option why ${i + 1}` });
    });
    s.addText("Fallbacks (series_as_parallel, all_parallel, first_only) are used only when a value collides. Option order rotates per item; the mistake behind each option is written into the answer key.",
      { x: 0.6, y: 6.05, w: 12.1, h: 0.7, fontSize: 11.5, color: C.text2, margin: 0, isTextBox: true, valign: "top", objectName: "fallback note" });
    s.addNotes("distractors.py re-walks the same circuit tree the way a mistaken student would. Each wrong option therefore names a misconception. The 'honest size' decision: a huge distractor is what the mistake gives, and its implausibility is itself feedback.");
  }
}

// ================================================================== 6 three pieces
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("The three pieces", { placeholder: "title" });
    const pieces = [
      ["Isomorphic-bank method", "Zhongzhou Chen", K.accent4,
        "The definition; an input scheme; a generate → critique → count loop with a target, accepted/rejected lists with reasons and a 5-pass cap (scenario_list.py); the bank YAML template and folder convention.",
        "AI inside: his critic and scenario writer are LLM agents. His docs: numbers, wording, figures “not generated yet”."],
      ["circuit-diagram-skill", "Myrla Phillippe", K.accent5,
        "A small language — circuit lingo: (4 + 2) || 6 + 3 — a parser, a series/parallel solver with worked steps, and a Schemdraw figure generator. Same text in → same figure, numbers and solution out.",
        "AI inside: none. An LLM may only translate an unreadable sentence into lingo; it never invents circuits."],
      ["circuit-bank skill", "this project", K.accent6,
        "Runs Chen's loop for circuits: an enumerator proposes every shape in the difficulty band; a script critic replaces his LLM critic; the circuit engine replaces his sympy stage; computed distractors; bank YAML + PDF.",
        "AI inside: none by default. An LLM proposer exists as an opt-in (generator: llm) for comparison."],
    ];
    pieces.forEach(([t, who, fill, what, ai], i) => {
      const x = 0.6 + i * 4.1, w = 3.9;
      s.addShape(pres.ShapeType.roundRect, { x, y: 1.45, w, h: 4.6, fill: { color: fill }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.1, objectName: `piece ${i + 1}` });
      s.addText(t, { x: x + 0.25, y: 1.6, w: w - 0.5, h: 0.45, fontSize: 17, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: `piece title ${i + 1}` });
      s.addText(who, { x: x + 0.25, y: 2.05, w: w - 0.5, h: 0.35, fontSize: 12, italic: true, color: C.text2, margin: 0, isTextBox: true, objectName: `piece who ${i + 1}` });
      s.addText(what, { x: x + 0.25, y: 2.5, w: w - 0.5, h: 2.5, fontSize: 12.5, color: C.text1, margin: 0, isTextBox: true, valign: "top", objectName: `piece what ${i + 1}` });
      s.addText(ai, { x: x + 0.25, y: 4.55, w: w - 0.5, h: 1.4, fontSize: 11.5, color: C.text2, margin: 0, isTextBox: true, valign: "top", objectName: `piece ai ${i + 1}` });
    });
    s.addNotes("Chen's repository separates tooling from banks. Our output follows his template and folder convention, so a circuit bank sits beside his mechanics banks without translation. The hand-off between creation and use is the bank YAML.");
  }
}

// ================================================================== 7 pipeline
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("The pipeline — whose work each stage is", { placeholder: "title" });
    const stages = [
      ["Input scheme", "what circuits, how many,\ndifficulty, ranges, seed", K.accent4],
      ["Chen's loop", "sidecar: target, pass count,\naccepted / rejected + reasons", K.accent4],
      ["Enumerate", "every shape in the band;\nvalues from a pool by seed", K.accent6],
      ["Critic (script)", "parse · solve · canonical shape\n· reduction steps · ranges", K.accent6],
      ["Circuit engine", "figure (Schemdraw), numbers,\nworked solution", K.accent5],
      ["Bank + PDF", "computed distractors;\nChen's YAML template; PDF", K.accent6],
    ];
    const PX = 0.6, PY = 1.7, BW = 1.9, BH = 1.5, PG = 0.14;
    stages.forEach(([t, note, fill], i) => {
      const x = PX + i * (BW + PG);
      s.addShape(pres.ShapeType.roundRect, { x, y: PY, w: BW, h: BH, fill: { color: fill }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: `stage ${i + 1}` });
      s.addText(t, { x: x + 0.1, y: PY + 0.12, w: BW - 0.2, h: 0.4, fontSize: 14, bold: true, color: C.text1, align: "center", margin: 0, isTextBox: true, objectName: `stage title ${i + 1}` });
      s.addText(note, { x: x + 0.1, y: PY + 0.55, w: BW - 0.2, h: 0.9, fontSize: 10.5, color: C.text2, align: "center", margin: 0, isTextBox: true, valign: "top", objectName: `stage note ${i + 1}` });
      if (i < stages.length - 1) s.addShape(pres.ShapeType.rightArrow, { x: x + BW - 0.02, y: PY + BH / 2 - 0.1, w: PG + 0.04, h: 0.2, fill: { color: "9A9A9A" }, line: { color: "9A9A9A", width: 0 }, objectName: `arrow ${i + 1}` });
    });
    const legend = [[K.accent4, "Zhongzhou Chen's method and scripts, run in place"], [K.accent5, "circuit-diagram-skill — deterministic engine"], [K.accent6, "circuit-bank glue — deterministic"]];
    let lx = 0.6;
    legend.forEach(([c, t], i) => {
      s.addShape(pres.ShapeType.rect, { x: lx, y: 3.45, w: 0.22, h: 0.18, fill: { color: c }, line: { color: "FFFFFF", width: 0 }, objectName: `legend ${i + 1}` });
      s.addText(t, { x: lx + 0.3, y: 3.4, w: 4.0, h: 0.28, fontSize: 11, color: C.text2, margin: 0, isTextBox: true, valign: "middle", objectName: `legend text ${i + 1}` });
      lx += 4.2;
    });
    heading(s, "What flows between the stages", 0.6, 4.05, 12, "flow heading");
    dotRows(s, [
      ["circuit-input.yaml", "the recipe — n_scenarios, difficulty band, value ranges, seed, bank id"],
      ["circuit-input.scenarios.yaml", "Chen's sidecar — the accepted lingo list, the source of truth the bank regenerates from"],
      ["agent2.json", "the candidates for one pass — the same JSON whether the enumerator or an LLM wrote them"],
      ["<bank_id>.yaml + figures/ + .pdf", "the product — importable bank, one figure per item, printable worksheet with answer key"],
    ], 0.6, 4.5, 12.1, 0.58, K.accent1, "flow", 12);
    s.addNotes("Colour shows whose work each stage is. The loop and the sidecar are Chen's scripts, unmodified. The proposer and critic are our scripts. The circuit engine is the circuit-diagram-skill. The LLM appears nowhere unless generator: llm is chosen.");
  }
}

// ================================================================== 8 one run
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("One run — the 30-item bank", { placeholder: "title" });
    const L = 0.6, LW = 5.6;
    heading(s, "Input (excerpt)", L, 1.4, LW, "input heading");
    s.addShape(pres.ShapeType.rect, { x: L, y: 1.8, w: LW, h: 2.3, fill: { color: "F6F4F0" }, line: { color: "FFFFFF", width: 0 }, objectName: "input box" });
    s.addText(["name: Series-parallel resistor networks: total current", "n_scenarios: 30", "bank_id: PHY2-DC-SPRTC3-10292026", "question_type: multiple_choice     layout: ladder",
      "resistor_range: [1, 24]     voltage_range: [6, 36]", "min_resistors: 5     max_resistors: 6", "reduction_steps: 3", "generator: enumerate     seed: 0"].join("\n"),
      { x: L + 0.15, y: 1.9, w: LW - 0.3, h: 2.1, fontSize: 11, fontFace: "Courier New", color: C.text1, margin: 0, isTextBox: true, valign: "top", objectName: "input text" });
    heading(s, "Enumerator output (one of 30)", L, 4.4, LW, "enum heading");
    s.addShape(pres.ShapeType.rect, { x: L, y: 4.8, w: LW, h: 1.2, fill: { color: "F6F4F0" }, line: { color: "FFFFFF", width: 0 }, objectName: "enum box" });
    s.addText("source: 9 V\ncircuit: (6 + 4) || (9 + 6)\nask: total current", { x: L + 0.15, y: 4.9, w: LW - 0.3, h: 1.0, fontSize: 12, fontFace: "Courier New", color: C.text1, margin: 0, isTextBox: true, valign: "top", objectName: "enum text" });
    const R = 6.7, RW = 6.0;
    heading(s, "What the critic checks, and the reason it writes", R, 1.4, RW, "critic heading");
    const rej = [
      ["parses and solves", "“circuit-diagram-skill rejects it: The circuit line ends too early…”"],
      ["new canonical shape (+ ask)", "“same solution path (S(P(R,R),R)) as an accepted scenario: 3 || 6 + 4”"],
      ["values in range", "“outside the input's ranges: R1 = 50 Ω is outside resistor_range [1, 24]”"],
      ["difficulty", "“5 reduction steps; this bank wants 3 (same difficulty for every item)”"],
    ];
    rej.forEach(([k, v], i) => {
      const y = 1.85 + i * 0.95;
      s.addShape(pres.ShapeType.roundRect, { x: R, y, w: RW, h: 0.85, fill: { color: K.lt2 }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.06, objectName: `check ${i + 1}` });
      s.addText([{ text: k, options: { bold: true, color: C.text1, breakLine: true } }, { text: v, options: { color: C.text2, italic: true } }],
        { x: R + 0.15, y: y + 0.06, w: RW - 0.3, h: 0.75, fontSize: 11.5, margin: 0, isTextBox: true, valign: "middle", objectName: `check text ${i + 1}` });
    });
    s.addText([{ text: "This run: ", options: { bold: true, color: C.text1 } }, { text: "Chen's validate_input.py ok · receive → needed 30 · enumerator wrote 30 · critic kept 30, rejected 0 · 30 items, 0 failures · PDF built.", options: { color: C.text2 } }],
      { x: R, y: 5.7, w: RW, h: 1.05, fontSize: 12, margin: 0, isTextBox: true, valign: "top", objectName: "run summary" });
    s.addNotes("The number of items lives in the input file, never in a chat message — one of Chen's rules we kept. The enumerator writes the same JSON an LLM proposer would, so add_lingo.py and the critic run unchanged. Because the enumerator never proposes a duplicate or an invalid circuit, the critic is a safety net here: 30 of 30 kept in one pass.");
  }
}

// ================================================================== 9 where the AI is
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("Where the AI is — and is not", { placeholder: "title" });
    grid(s, [
      ["Stage", "Chen's pipeline", "This pipeline"],
      ["Describe the problem family", "human writes the input", "human writes the input"],
      ["Propose variations", "LLM writes prose scenarios", "enumeration of every shape in the band (LLM opt-in)"],
      ["Judge variations", "LLM critic", "script: parse, solve, shape, steps, ranges"],
      ["Equations / numbers", "sympy from LaTeX; random numbers “not yet”", "circuit engine, deterministic"],
      ["Figures", "not generated", "Schemdraw, from the same lingo"],
      ["Wrong answers", "—", "computed from named mistakes"],
      ["Wording", "not generated", "fixed template from the engine"],
    ], 0.6, 1.45, [3.2, 4.2, 4.7], 0.56, { fs: 12 });
    s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 6.05, w: 12.1, h: 0.8, fill: { color: K.accent5 }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: "repro card" });
    s.addText([{ text: "Reproducibility.  ", options: { bold: true, color: C.text1 } }, { text: "Same input + same seed → the same 30 scenarios. Same sidecar → the same bank, byte for byte (verified). The sidecar is the source of truth; YAML, figures and PDF are derived.", options: { color: C.text1 } }],
      { x: 0.8, y: 6.1, w: 11.7, h: 0.7, fontSize: 12.5, margin: 0, isTextBox: true, valign: "middle", objectName: "repro text" });
    s.addNotes("When the LLM proposer is used, correctness is unchanged — the critic and the engine do not care who wrote the string — but the set of shapes differs from run to run and completeness is not assured. That mattered once we fixed one difficulty: finding all 30 shapes is a job for enumeration.");
  }
}

// ================================================================== 10 difficulty ceiling (native chart)
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("Difficulty has a ceiling", { placeholder: "title" });
    s.addChart(pres.ChartType.bar, [{ name: "Distinct shapes (3–6 resistors)", labels: ["1 step", "2 steps", "3 steps", "4 steps", "5 steps"], values: [8, 20, 34, 30, 12] }], {
      x: 0.6, y: 1.4, w: 7.2, h: 5.4, barDir: "col", chartColors: [K.accent1], invertedColors: [K.accent1],
      showTitle: true, title: "Distinct series-parallel shapes by number of reduction steps", titleFontSize: 13, titleFontFace: "+mn-lt", titleColor: K.dk1,
      showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 12, dataLabelFontFace: "+mn-lt", dataLabelColor: K.dk1,
      catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt", catAxisLabelColor: K.dk2, catGridLine: { style: "none" },
      valAxisLabelFontSize: 11, valAxisLabelFontFace: "+mn-lt", valAxisLabelColor: K.dk2, valGridLine: { color: "E3DED6", size: 0.5 }, valAxisMaxVal: 40,
      showLegend: false, objectName: "shape count chart",
    });
    const R = 8.2, RW = 4.5;
    s.addShape(pres.ShapeType.roundRect, { x: R, y: 1.4, w: RW, h: 1.5, fill: { color: K.lt2 }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: "stat card" });
    s.addText("30", { x: R + 0.15, y: 1.45, w: 1.4, h: 1.4, fontSize: 48, bold: true, color: C.accent1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "stat 30" });
    s.addText("distinct 3-step shapes with 5–6 resistors (34 with 4–6). The bank uses every one of the 30", { x: R + 1.6, y: 1.5, w: RW - 1.75, h: 1.3, fontSize: 12.5, color: C.text1, margin: 0, isTextBox: true, valign: "middle", objectName: "stat label" });
    dotRows(s, [
      ["Fixing difficulty = fixing the step count.", "one reduction step per group collapsed"],
      ["The set is finite and small.", "2, 4, 10, 24, 66 shapes for 2–6 resistors — the classic series-parallel sequence"],
      ["Wanting more at one difficulty", "means allowing more resistors, not inventing shapes — and that is a different difficulty"],
      ["Enumeration, not guessing.", "an LLM finding all 30 within 5 passes is unlikely; the enumerator lists every one"],
    ], R, 3.15, RW, 0.9, K.accent2, "ceiling", 11.5);
    s.addNotes("The counts come from enumerating series-parallel trees with alternating series/parallel nodes. At exactly three steps there are 34 shapes with four to six resistors and exactly 30 with five to six; the bank uses every one of those 30, so the arithmetic load is also held in a narrow band. The first bank mixed 2 to 5 steps — structurally isomorphic, but not fair as a random draw.");
  }
}

// ================================================================== 11 results
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("Results and verification", { placeholder: "title" });
    const banks = [
      ["PHY2-DC-SPRTC-10222026", "10 items", "mixed difficulty, 2–5 steps", "proposer: LLM", "0 rejections — 10 distinct shapes", "answers: several repeat", path.join(B10, "q5.png")],
      ["PHY2-DC-SPRTC3-10292026", "30 items", "one difficulty: exactly 3 steps, 5–6 resistors", "proposer: enumerator", "0 rejections — all 30 shapes", "answers: all distinct", path.join(B30, "q4.png")],
    ];
    banks.forEach(([id, items, diff, prop, rej, ans, f], i) => {
      const x = 0.6 + i * 6.2, w = 5.9;
      s.addShape(pres.ShapeType.roundRect, { x, y: 1.4, w, h: 3.55, fill: { color: i === 1 ? K.accent5 : K.lt2 }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.1, objectName: `bank card ${i + 1}` });
      s.addText(id, { x: x + 0.25, y: 1.5, w: w - 0.5, h: 0.4, fontSize: 15, bold: true, fontFace: "Courier New", color: C.text1, margin: 0, isTextBox: true, objectName: `bank id ${i + 1}` });
      s.addText(items, { x: x + 0.25, y: 1.9, w: 2.4, h: 0.6, fontSize: 26, bold: true, color: C.accent1, margin: 0, isTextBox: true, objectName: `bank items ${i + 1}` });
      s.addText([diff, prop, rej, ans].map((t, j) => ({ text: t, options: { breakLine: j < 3 } })), { x: x + 0.25, y: 2.55, w: 2.6, h: 2.3, fontSize: 11.5, color: C.text1, margin: 0, isTextBox: true, valign: "top", paraSpaceAfter: 4, objectName: `bank facts ${i + 1}` });
      framed(s, f, x + 3.0, 1.95, 2.7, 2.8, `bank figure ${i + 1}`);
    });
    heading(s, "Three independent checks", 0.6, 5.2, 12, "checks heading");
    dotRows(s, [
      ["Chen's own validate_input.py", "accepts the circuit input scheme — no missing fields"],
      ["Regeneration", "every item re-parsed and re-solved; the bank rebuilt from its sidecar is byte-identical"],
      ["Critic log", "every shape unique with exactly 3 steps — 30 kept, 0 rejected, in one pass"],
    ], 0.6, 5.6, 12.1, 0.45, K.accent2, "check", 12);
    s.addNotes("Both banks are published in Chen's folder convention in the circuit-banks repository with status: ready. The first bank is kept as a contrast: structurally isomorphic, mixed difficulty.");
  }
}

// ================================================================== 12 limits & next steps
{
  const s = slide("content", SEC);
  if (s) {
    s.addText("Limits and next steps", { placeholder: "title" });
    const rows = [
      ["Canvas import (QTI)", "Not produced. Chen's bank folders ship a QTI zip from an external converter. A deterministic QTI 2.1 exporter for multiple-choice-with-image is a well-scoped next step.", K.lt2],
      ["Varying the unknown", "Fixed to “total current”. Chen's input has unknown_rotation for this but it is not implemented yet; our critic already treats a different ask as a different problem.", K.lt2],
      ["Number randomisation per student", "Not done (also “not yet” in Chen's docs). Isomorphism is carried by the topology; numbers are fixed per item.", K.lt2],
      ["Distractor magnitude", "Left honest, no cap — one option can be 100× the answer. A documented design choice.", K.lt2],
      ["Licensing", "Chen's repo is CC BY-NC 4.0 and private; the skill that embeds one of his scripts is private too. The public circuit-banks repo holds only our output.", K.lt2],
    ];
    rows.forEach(([k, v, fill], i) => {
      const y = 1.45 + i * 1.08;
      s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: 0.96, fill: { color: fill }, line: { color: "FFFFFF", width: 0 }, rectRadius: 0.08, objectName: `limit ${i + 1}` });
      s.addText(k, { x: 0.8, y: y + 0.08, w: 3.0, h: 0.8, fontSize: 14, bold: true, color: C.text1, margin: 0, isTextBox: true, valign: "middle", objectName: `limit key ${i + 1}` });
      s.addText(v, { x: 3.9, y: y + 0.08, w: 8.6, h: 0.8, fontSize: 12, color: C.text2, margin: 0, isTextBox: true, valign: "middle", objectName: `limit text ${i + 1}` });
    });
    s.addNotes("The nearest next step is a QTI exporter, which would make this the only one of the three pieces that produces the Canvas file directly. Varying the unknown is an input-file change plus wording.");
  }
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log(OUT);
})();

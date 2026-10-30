#!/usr/bin/env python3
"""Build 'How the circuit bank works' - a report for the research group.  Run from the circuit-banks repo root with
the circuit-bank-skill venv (needs reportlab, PyYAML, and circuit-bank-skill + circuit-diagram-skill in ~/.claude/skills):
    ~/.claude/skills/circuit-bank-skill/.venv/bin/python docs/build_report.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle, Flowable)

ROOT = Path(__file__).resolve().parent.parent          # the circuit-banks repository
BANKS = ROOT / "PHY II Electricity and Magnetism" / "1_DC Circuits"
B10 = BANKS / "PHY2-DC-SPRTC-10222026"
B30 = BANKS / "PHY2-DC-SPRTC3-10292026"
SKILL = Path.home() / ".claude" / "skills" / "circuit-bank-skill" / "scripts"
sys.path.insert(0, str(SKILL))
import enumerate_lingo as EN  # noqa: E402

OUT = ROOT / "docs" / "How-the-circuit-bank-works.pdf"

# ------------------------------------------------------------------ fonts & styles
FONT = "Helvetica"
for cand in ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
    if Path(cand).is_file():
        pdfmetrics.registerFont(TTFont("Body", cand))
        FONT = "Body"
        break
ss = getSampleStyleSheet()
ACCENT = colors.HexColor("#8a2a1b")
INK = colors.HexColor("#1e1e1e")
MUTED = colors.HexColor("#555555")
body = ParagraphStyle("body", parent=ss["BodyText"], fontName=FONT, fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=6)
small = ParagraphStyle("small", parent=body, fontSize=9, leading=12, textColor=MUTED)
mono = ParagraphStyle("mono", parent=body, fontName="Courier", fontSize=9, leading=11.5, backColor=colors.HexColor("#f4f1ec"),
                      borderPadding=(4, 6, 4, 6), leftIndent=6, spaceBefore=4, spaceAfter=8)
cell = ParagraphStyle("cell", parent=body, fontSize=9, leading=11.5, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName=FONT)
title = ParagraphStyle("title", parent=ss["Title"], fontName=FONT, fontSize=26, leading=31, alignment=TA_LEFT, textColor=INK, spaceAfter=6)
subtitle = ParagraphStyle("subtitle", parent=body, fontSize=13, leading=18, textColor=MUTED, spaceAfter=18)
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName=FONT, fontSize=17, leading=21, textColor=ACCENT, spaceBefore=14, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName=FONT, fontSize=12.5, leading=16, textColor=INK, spaceBefore=10, spaceAfter=4)
callout = ParagraphStyle("callout", parent=body, fontSize=11.5, leading=16, textColor=INK, backColor=colors.HexColor("#fbf3ef"),
                         borderColor=ACCENT, borderWidth=0.8, borderPadding=(8, 10, 8, 10), leftIndent=4, rightIndent=4, spaceBefore=6, spaceAfter=12)
slide = ParagraphStyle("slide", parent=small, textColor=ACCENT, fontSize=8.5, spaceBefore=0, spaceAfter=2)


def P(t, st=body):
    return Paragraph(t, st)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table(rows, widths=None, header=True, zebra=True, fs=9):
    data = [[Paragraph(str(c), cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9c2b8")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#efe9e1"))]
    if zebra:
        for i in range(1 if header else 0, len(rows)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#faf8f5")))
    t.setStyle(TableStyle(st))
    return t


def fig(path, max_w=4.8 * inch, max_h=2.4 * inch, caption=None):
    img = Image(str(path))
    s = min(max_w / img.imageWidth, max_h / img.imageHeight)
    img.drawWidth, img.drawHeight = img.imageWidth * s, img.imageHeight * s
    img.hAlign = "LEFT"
    out = [img]
    if caption:
        out.append(P(caption, small))
    return out


class Pipeline(Flowable):
    """A simple left-to-right box diagram with a colour legend: who does each stage."""

    def __init__(self, stages, width=6.6 * inch):
        super().__init__()
        self.stages = stages
        self.width = width
        self.height = 1.55 * inch

    def draw(self):
        c = self.canv
        n = len(self.stages)
        gap = 8
        bw = (self.width - gap * (n - 1)) / n
        y, bh = 0.45 * inch, 0.95 * inch
        palette = {"chen": colors.HexColor("#dfe7f2"), "skill": colors.HexColor("#e3f0df"), "glue": colors.HexColor("#f6e7d8"),
                   "llm": colors.HexColor("#f3d9d9")}
        for i, (label, who, note) in enumerate(self.stages):
            x = i * (bw + gap)
            c.setFillColor(palette[who]); c.setStrokeColor(colors.HexColor("#888"))
            c.roundRect(x, y, bw, bh, 5, fill=1, stroke=1)
            c.setFillColor(INK); c.setFont(FONT, 8)
            lines = label.split("\n")
            for j, ln in enumerate(lines):
                c.drawCentredString(x + bw / 2, y + bh - 14 - j * 10, ln)
            c.setFont(FONT, 6.2); c.setFillColor(MUTED)
            for j, ln in enumerate(note.split("\n")):
                c.drawCentredString(x + bw / 2, y + 18 - j * 7.5, ln)
            if i < n - 1:
                c.setStrokeColor(colors.HexColor("#666")); c.setLineWidth(1)
                c.line(x + bw + 1, y + bh / 2, x + bw + gap - 1, y + bh / 2)
        lx = 0
        c.setFont(FONT, 7.5)
        for who, text in (("chen", "Zhongzhou Chen's method / scripts"), ("skill", "circuit-diagram-skill (deterministic)"),
                          ("glue", "circuit-bank glue (deterministic)"), ("llm", "LLM (optional)")):
            c.setFillColor(palette[who]); c.rect(lx, 4, 10, 10, fill=1, stroke=0)
            c.setFillColor(MUTED); c.drawString(lx + 14, 6, text)
            lx += 14 + pdfmetrics.stringWidth(text, FONT, 7.5) + 18


# ------------------------------------------------------------------ data from the real banks
def load_bank(path):
    d = yaml.safe_load((path / f"{path.name}.yaml").read_text(encoding="utf-8"))
    rows = []
    for q in d["questions"]:
        m = q["multiple_choice"]
        lingo = m["circuit_lingo"].strip().splitlines()
        src = lingo[0].split(":", 1)[1].strip(); circ = lingo[1].split(":", 1)[1].strip()
        opts = [(a["answer"]["text"], a["answer"].get("correct", False)) for a in m["answers"]]
        correct = next(t for t, c in opts if c)
        rows.append((m["id"], circ, src, correct, [t for t, c in opts if not c]))
    return d["bank_info"], rows


info10, rows10 = load_bank(B10)
info30, rows30 = load_bank(B30)
side30 = yaml.safe_load((B30 / "circuit-input.scenarios.yaml").read_text())
inp30 = (B30 / "circuit-input.yaml").read_text()

# shape catalogue for 3 steps, 4-6 resistors
cat = EN.all_shapes(5, 6, (3, 3))
cat_rows = [(EN.leaves_of(t), EN.render(t, [0] * EN.leaves_of(t)).replace("0", "R")) for t in cat]
counts = {}
for n in range(3, 7):
    for t in sorted(EN.shapes(n, "S") | EN.shapes(n, "P")):
        counts.setdefault(EN.steps_of(t), 0)
        counts[EN.steps_of(t)] += 1

# ------------------------------------------------------------------ the document
story = []
S = story.append

# ---- cover
S(Spacer(1, 1.2 * inch))
S(P("How the circuit bank works", title))
S(P("Isomorphic DC-circuit problem banks: what “isomorphic” means, why it is built for fairness to the student, "
    "and how the code produces 30 variations at one difficulty with every number computed, not guessed.", subtitle))
S(P("Myrla Phillippe · research-group presentation notes · October 2026", small))
S(Spacer(1, 0.3 * inch))
S(P("<b>In one sentence.</b> Take Zhongzhou Chen's isomorphic-bank method, feed it a domain where the “scenario” is a circuit "
    "topology that a computer can enumerate and verify, and let a deterministic circuit engine do everything numerical — "
    "the result is a bank where every item has a different solution path, the same difficulty (exactly three reduction steps, five or six resistors), computed wrong answers, "
    "and an answer key that regenerates byte-for-byte.", callout))
S(P("<b>Suggested slide order</b> (each section below is one or two slides): 1 What isomorphic means · 2 Built for the student · "
    "3 The three pieces · 4 Walk-through of one run · 5 Where the AI is and is not · 6 Difficulty has a ceiling · "
    "7 Results and verification · 8 Limits and next steps.", small))
S(PageBreak())

# ---- 1 isomorphic
S(P("SLIDE 1", slide)); S(P("1. What “isomorphic” means here", h1))
S(P("The word is Zhongzhou Chen's. His repository defines an isomorphic bank as problems that test the same learning objectives "
    "“with variations that change the solution and not only the numbers”, drawn at random so no two students get the same item. "
    "Spelled out, that is three criteria, and all three matter:"))
S(table([["", "Criterion", "What it rules out"],
         ["1", "The variation is <b>more than changing numbers</b> or swapping nouns.", "“Same circuit, new resistor values.” Students pattern-match the one solution path."],
         ["2", "It <b>changes the solution</b> — at least one step is different.", "Cosmetic changes: redrawing the figure, re-ordering parts, renaming R<sub>1</sub>→R<sub>2</sub>."],
         ["3", "It tests the <b>same learning objective at the same difficulty</b>.", "Mixing a 2-step circuit with a 5-step one, or asking for current in one item and power in another."]],
        widths=[0.3 * inch, 3.1 * inch, 3.2 * inch]))
S(Spacer(1, 6))
S(P("For a resistor network the natural reading is: <b>an isomorph is a different series-parallel topology</b> — a different "
    "sequence of reductions — asked the same way, at the same number of steps. Three real items from the 10-item bank:"))
tri = Table([[fig(B10 / "figures" / "q1.png", 2.1 * inch, 1.5 * inch)[0], fig(B10 / "figures" / "q2.png", 2.1 * inch, 1.5 * inch)[0],
              fig(B10 / "figures" / "q3.png", 2.1 * inch, 1.5 * inch)[0]],
             [P(f"<font face='Courier'>{esc(rows10[0][1])}</font><br/>parallel pair, then series", cell),
              P(f"<font face='Courier'>{esc(rows10[1][1])}</font><br/>series pair inside a parallel, then series", cell),
              P(f"<font face='Courier'>{esc(rows10[2][1])}</font><br/>three-way parallel, then series", cell)]],
            colWidths=[2.2 * inch] * 3, hAlign="LEFT")
tri.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 2)]))
S(tri)
S(Spacer(1, 6))
S(P("Same question (“find the total current”), same tools (series/parallel reduction + Ohm's law), but no two of them "
    "can be solved by remembering the other. That is the floor. The ceiling — same difficulty — is handled in section 6."))
S(P("<b>Why the word matters.</b> These banks exist for one use: each student draws <i>one</i> random item from the bank for the same "
    "exam slot. Below the floor the draw is pointless (everyone has the same problem). Above the ceiling the draw is unfair "
    "(one student's exam is harder). Isomorphic is exactly the band where a random draw is both meaningful and fair.", callout))
S(PageBreak())

# ---- 2 student
S(P("SLIDE 2", slide)); S(P("2. Built with the student in mind", h1))
S(table([["Design choice", "What the student experiences", "How it is enforced"],
         ["One difficulty per bank", "Whoever you are, your drawn problem takes the same number of reduction steps (3) with the same number of resistors (5–6) as your neighbour's.", "<font face='Courier'>reduction_steps: 3</font>, <font face='Courier'>min/max_resistors: 5/6</font> in the input; the critic rejects any candidate outside them. One step = one series run or parallel group collapsed into a single resistor."],
         ["Every item a different solution path", "You cannot pass by memorising last year's problem; you have to reduce the network you were given.", "Canonical-shape check: two circuits with the same tree shape are the same problem, whatever the numbers."],
         ["Wrong answers are real mistakes", "Three distractors are the numbers you get by making one specific error each; a fifth option sits near the largest value so a lone big number is not a giveaway by size.", "<font face='Courier'>distractors.py</font> recomputes the circuit as a mistaken student would (all-series, forgot-to-invert, branch current) and adds a decoy at 0.9 × the largest option."],
         ["Honest sizes", "A distractor of 144 A is what the mistake really gives; its implausibility is itself feedback.", "Deliberately not capped (a documented decision)."],
         ["One drawing style", "The figure never changes style between items, so the only thing that varies is the physics.", "<font face='Courier'>layout: ladder</font> for the whole bank; style is never a variation axis."],
         ["Clean arithmetic", "Every intermediate resistance is a whole or half ohm; answers have at most two decimals.", "The enumerator only accepts value sets that satisfy this; resistor pool ≤ 12 Ω."],
         ["Worked solution for every item", "After the exam, the feedback shows every reduction step and a per-resistor table.", "Produced by the circuit engine, stored in <font face='Courier'>feedback.general</font>."]],
        widths=[1.45 * inch, 2.75 * inch, 2.4 * inch]))
S(Spacer(1, 8))
S(P("Example of computed options — item q1 of the 10-item bank (12 V, <font face='Courier'>3 || 6 + 4</font>, correct 2.00 A):", h2))
S(table([["Option", "Where it comes from"],
         ["0.92 A", "adds every resistor as if in series: 12 / (3 + 6 + 4)"],
         ["2.67 A", "adds the reciprocals of the parallel pair but forgets to invert: R<sub>12</sub> = 1/3 + 1/6 = 0.5 “Ω”"],
         ["1.33 A", "reports the current through R<sub>1</sub> (one branch) instead of the total"],
         ["2.40 A", "decoy: 0.9 × the largest option, so the large value is not alone"],
         ["<b>2.00 A</b>", "<b>correct</b>: 3 ‖ 6 = 2 Ω, + 4 = 6 Ω, 12 V / 6 Ω"]], widths=[1.0 * inch, 5.6 * inch]))
S(PageBreak())

# ---- 3 pieces
S(P("SLIDE 3", slide)); S(P("3. The three pieces", h1))
S(table([["Piece", "Author", "What it contributes", "AI inside?"],
         ["<b>Isomorphic-bank method</b><br/><font size=8>isomorphic-bank-creation-skills</font>", "Zhongzhou Chen",
          "The definition of isomorphic; an input scheme; a <i>generate → critique → count</i> loop with a target, accepted/rejected lists with reasons and a 5-pass cap (<font face='Courier'>scenario_list.py</font>); the bank YAML format and its folder convention (bank id, QTI zip, figures).",
          "His critic and scenario writer are LLM agents. His docs state numbers, wording and figures are “not generated yet.”"],
         ["<b>circuit-diagram-skill</b>", "Myrla Phillippe",
          "A small language (“circuit lingo”: <font face='Courier'>(4 + 2) || 6 + 3</font>), a parser, a series/parallel solver with worked steps, and a Schemdraw figure generator. Same text in → same figure, numbers and solution out.",
          "None. An LLM may only translate an unreadable English sentence into lingo; it never invents circuits."],
         ["<b>circuit-bank skill</b>", "this project",
          "Runs Chen's loop for circuits: an <b>enumerator</b> proposes every shape in the difficulty band; a <b>script critic</b> replaces his LLM critic; the circuit engine replaces his sympy stage; computed distractors; bank YAML + PDF output.",
          "None by default. An LLM proposer exists as an opt-in (<font face='Courier'>generator: llm</font>) for comparison."]],
        widths=[1.35 * inch, 0.95 * inch, 2.75 * inch, 1.55 * inch]))
S(Spacer(1, 10))
S(P("Chen's repository separates the <i>tooling</i> (his two Cursor skills) from the <i>banks</i> (one folder per bank, in his YAML template). "
    "Our output follows the same template and folder convention, so a circuit bank sits beside his mechanics banks without translation.", small))
S(Spacer(1, 6))
S(Pipeline([("Input scheme\n(YAML)", "chen", "what circuits,\nhow many"),
            ("Sidecar\ninit / receive", "chen", "target, passes,\naccepted / rejected"),
            ("Propose\ncandidates", "glue", "enumerate shapes\n(or LLM, opt-in)"),
            ("Critic", "glue", "parse · solve · shape\nsteps · ranges"),
            ("Solve + draw", "skill", "numbers, figure,\nworked solution"),
            ("Distractors\n+ bank YAML", "glue", "named mistakes;\nChen's template"),
            ("Bank YAML\n+ PDF", "chen", "Chen's template;\nworksheet & key")]))
S(P("Figure: the pipeline, coloured by whose work each stage is.", small))
S(PageBreak())

# ---- 4 walk-through
S(P("SLIDE 4", slide)); S(P("4. Walk-through of one run (the 30-item bank)", h1))
S(P("4.1 The input scheme", h2))
S(P("Chen's format, plus a <font face='Courier'>bank:</font> block and a few machine-checkable ranges. The number of items lives here "
    "(<font face='Courier'>n_scenarios: 30</font>), never in a chat message — one of his rules we kept."))
inp_lines = [l for l in inp30.splitlines() if l.strip() and not l.strip().startswith("#")]
keep = [l for l in inp_lines if any(k in l for k in ("name:", "n_scenarios", "- Every", "- Between", "Ask for", "bank_id", "question_type", "layout",
                                                      "resistor_range", "voltage_range", "min_resistors", "max_resistors", "reduction_steps", "generator", "seed"))]
S(P("<br/>".join(esc(l.split("#")[0].rstrip()) for l in keep), mono))

S(P("4.2 Chen's loop opens the sidecar", h2))
S(P("<font face='Courier'>validate_input.py</font> (his Agent 1 check) passes the file; <font face='Courier'>scenario_list.py init</font> copies the "
    "target; <font face='Courier'>receive</font> starts pass 1 and reports <font face='Courier'>needed: 30</font>."))

S(P("4.3 Propose candidates — the enumerator", h2))
S(P("Every series-parallel network is a tree whose internal nodes alternate <i>series</i> and <i>parallel</i>. The enumerator generates all such "
    "trees with 5–6 resistors, keeps those with exactly 3 internal nodes (= 3 reduction steps), and skips shapes already accepted. "
    f"There are <b>{len(cat)}</b> of them (appendix A lists all) — so a 30-item bank uses every one. For each shape it then picks resistor values from a fixed pool "
    "(1–12 Ω) and a battery voltage, using a seed, until every intermediate resistance is a multiple of 0.5 Ω, the answer has ≤ 2 decimals, "
    "and no earlier item has the same answer. Output: 30 three-line lingo strings — the same JSON an LLM proposer would return."))
S(P("source: 9 V<br/>circuit: (6 + 4) || (9 + 6)<br/>ask: total current", mono))

S(P("4.4 The critic — a script, not an opinion", h2))
S(P("Each candidate is parsed and solved by the circuit engine; it is rejected, with a reason written into the sidecar, if any of these fail:"))
S(table([["Check", "Rejection reason as written to the sidecar"],
         ["parses and solves", "<i>circuit-diagram-skill rejects it: The circuit line ends too early…</i>"],
         ["new canonical shape (+ ask)", "<i>same solution path (S(P(R,R),R) ask total_current) as an accepted scenario: 3 || 6 + 4</i>"],
         ["values in range", "<i>outside the input's ranges: R1 = 50 Ω is outside resistor_range [1, 24]</i>"],
         ["difficulty", "<i>outside the input's ranges: 5 reduction steps; this bank wants 3 (same difficulty for every item)</i>"]],
        widths=[1.7 * inch, 4.9 * inch]))
S(P("The canonical shape ignores the order of siblings, so <font face='Courier'>3 || 6 + 4</font>, <font face='Courier'>6 || 3 + 4</font> and "
    "<font face='Courier'>2 || 4 + 5</font> all collapse to <font face='Courier'>S(P(R,R),R)</font> — one problem, not three. "
    "With the enumerator proposing, the critic is a safety net: in this run it kept 30 of 30 on the first pass.", small))

S(P("4.5 Numbers, figure, worked solution, distractors", h2))
S(P("For each accepted lingo the circuit engine draws the figure (ladder layout, US symbols) and writes the reduction steps, the per-part "
    "table and the answer. <font face='Courier'>distractors.py</font> re-walks the same tree three wrong ways and adds a decoy near the largest option. Everything is assembled into one "
    "bank YAML in Chen's template (so it can be imported wherever his banks are) and rendered to a PDF worksheet with an answer key."))
S(KeepTogether(fig(B30 / "figures" / "q2.png", 3.6 * inch, 1.9 * inch,
                   f"Item q2 of the 30-item bank: <font face='Courier'>{esc(rows30[1][1])}</font>, {rows30[1][2]} → {rows30[1][3]}. "
                   f"Distractors: {', '.join(rows30[1][4])}.")))
S(PageBreak())

# ---- 5 AI
S(P("SLIDE 5", slide)); S(P("5. Where the AI is — and is not", h1))
S(table([["Stage", "Chen's pipeline", "This pipeline"],
         ["Describe the problem family", "human writes the input", "human writes the input"],
         ["Propose variations", "LLM writes prose scenarios", "<b>enumeration</b> (all shapes in the band); LLM opt-in"],
         ["Judge variations", "LLM critic", "<b>script</b>: parse, solve, shape, steps, ranges"],
         ["Equations / numbers", "sympy from LaTeX formulas; random numbers “not generated yet”", "<b>circuit engine</b>, deterministic"],
         ["Figures", "not generated", "<b>Schemdraw</b> from the same lingo"],
         ["Wrong answers", "—", "<b>computed</b> from named mistakes"],
         ["Wording", "not generated", "fixed template from the engine"]],
        widths=[1.7 * inch, 2.3 * inch, 2.6 * inch]))
S(Spacer(1, 8))
S(P("<b>Reproducibility.</b> Same input + same seed → the same 30 scenarios. Same scenario sidecar → the same bank, byte for byte "
    "(verified: regenerating produced an identical SVG). The sidecar is the bank's source of truth; the PDF, the figures and the YAML "
    "are all derived from it.", callout))
S(P("When the LLM proposer <i>is</i> used (we ran it for the first 10-item bank), correctness is unchanged — the critic and the engine "
    "do not care who wrote the string — but two guarantees are lost: the set of shapes differs from run to run, and completeness is not "
    "assured. That mattered as soon as we fixed one difficulty (next section): finding all 30 possible shapes is a job for enumeration, not guessing.", small))

# ---- 6 difficulty
S(PageBreak())
S(P("SLIDE 6", slide)); S(P("6. Difficulty has a ceiling", h1))
S(P("Fixing one difficulty means fixing the number of reduction steps. The number of distinct series-parallel shapes is finite and small "
    "(the counts 2, 4, 10, 24, 66 for 2–6 resistors are the classic series-parallel network sequence):"))
S(table([["Reduction steps", "Distinct shapes with 3–6 resistors", "Largest one-difficulty bank"]] +
        [[str(k), str(v), str(v)] for k, v in sorted(counts.items())], widths=[1.6 * inch, 2.6 * inch, 2.2 * inch]))
S(P("At exactly 3 steps there are 34 shapes with 4–6 resistors; restricting to 5–6 resistors (so the arithmetic load is also held in a narrow band) leaves exactly 30 — the bank uses every one. "
    "Wanting more items at one difficulty means allowing more resistors, not inventing more shapes — and that is a different difficulty. The first bank (10 items, mixed 2–5 steps) is kept as a "
    "contrast: structurally isomorphic, but not fair as a random draw.", small))
S(PageBreak())

# ---- 7 results
S(P("SLIDE 7", slide)); S(P("7. Results and verification", h1))
S(table([["Bank", "Items", "Difficulty", "Proposer", "Critic rejections", "Answers"],
         [info10["bank_id"], "10", "mixed, 2–5 steps", "LLM", "0 (10 distinct shapes)", "several repeat"],
         [info30["bank_id"], "30", "exactly 3 steps, 5–6 resistors", "enumerator", "0 (all 30 shapes)", "all distinct"]],
        widths=[2.0 * inch, 0.5 * inch, 1.45 * inch, 0.8 * inch, 1.15 * inch, 0.7 * inch]))
S(Spacer(1, 8))
S(P("The 30-item bank", h2))
S(table([["id", "circuit (lingo)", "V", "answer"]] + [[r[0], f"<font face='Courier'>{esc(r[1])}</font>", r[2], r[3]] for r in rows30],
        widths=[0.5 * inch, 3.6 * inch, 0.7 * inch, 1.0 * inch], fs=8.5))
S(Spacer(1, 8))
S(P("Verification", h2))
S(P("Three independent checks were run. (1) Chen's own <font face='Courier'>validate_input.py</font> accepts the circuit input scheme with no "
    "missing fields. (2) Every accepted item was re-parsed and re-solved by the circuit engine, and the bank regenerated from its sidecar "
    "is byte-identical to the first build. (3) Each item's canonical shape is unique and has exactly three reduction steps — the critic's "
    "log shows 30 kept, 0 rejected, in a single pass. The banks are published in Chen's folder convention "
    "(<font face='Courier'>Subject-Unit-Abbreviation-date</font>, <font face='Courier'>status: ready</font>) in the <font face='Courier'>circuit-banks</font> repository."))

# ---- 8 limits
S(PageBreak())
S(P("SLIDE 8", slide)); S(P("8. Limits and next steps", h1))
S(table([["Topic", "Status"],
         ["Canvas import (QTI)", "Not produced. Chen's bank folders ship a QTI zip made by an external converter; his creation repo does not generate it. A deterministic QTI 2.1 exporter for multiple-choice-with-image is a well-scoped next step."],
         ["Varying the unknown", "Fixed to “total current”. Chen's input has <font face='Courier'>unknown_rotation</font> for this but his pipeline does not implement it yet; our critic already treats a different ask as a different problem, so this is an input-file change plus wording."],
         ["Number randomisation per student", "Not done (also “not yet” in Chen's docs). Isomorphism is carried by the topology; numbers are fixed per item."],
         ["Distractor magnitude", "Left honest (no cap); one option can be 100× the answer. Documented as a design choice."],
         ["Licensing", "Chen's repo is CC BY-NC 4.0 and is now private; the skill that embeds one of his scripts is kept private too. The public <font face='Courier'>circuit-banks</font> repo contains only our output."]],
        widths=[1.7 * inch, 4.9 * inch]))
S(PageBreak())

# ---- appendix A: catalogue
S(P("Appendix A — all 3-step shapes with 5–6 resistors (the 30-item bank uses every one)", h1))
half = (len(cat_rows) + 1) // 2
left = [["#", "R", "shape"]] + [[str(i + 1), str(n), f"<font face='Courier'>{esc(s)}</font>"] for i, (n, s) in enumerate(cat_rows[:half])]
right = [["#", "R", "shape"]] + [[str(i + 1 + half), str(n), f"<font face='Courier'>{esc(s)}</font>"] for i, (n, s) in enumerate(cat_rows[half:])]
two = Table([[table(left, [0.35 * inch, 0.3 * inch, 2.5 * inch], fs=8), table(right, [0.35 * inch, 0.3 * inch, 2.5 * inch], fs=8)]],
            colWidths=[3.3 * inch, 3.3 * inch], hAlign="LEFT")
two.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
S(two)
S(P("“R” = a resistor; <font face='Courier'>||</font> parallel, <font face='Courier'>+</font> series; sibling order is irrelevant. "
    "Each row is a different reduction sequence of exactly three steps.", small))

# ---- appendix B: commands & files
S(P("Appendix B — running it", h1))
S(P("In a chat with the skills installed: <i>“run the circuit bank workflow on circuit-input.yaml”</i>. Under the hood (repo root of the fork):"))
S(P("<br/>".join(esc(l) for l in [
    "PY=.venv/bin/python                            # repo venv",
    "P=.cursor/skills/problem-creation/scripts      # Chen's scripts",
    "S=.cursor/skills/circuit-bank/scripts          # circuit-bank scripts",
    "IN=BANK/circuit-input.yaml; SC=BANK/circuit-input.scenarios.yaml",
    "",
    "$PY $P/validate_input.py $IN                   # Agent 1 check (Chen)",
    "$PY $P/scenario_list.py init --input $IN       # sidecar, target (Chen)",
    "$PY $P/scenario_list.py receive --file $SC     # start a pass (Chen)",
    "$PY $S/enumerate_lingo.py --file $SC           # propose: every shape in the band",
    "$PY $S/add_lingo.py --file $SC --json BANK/agent2.json",
    "$PY $S/critic.py --file $SC --apply            # Agent 3 as a script",
    "$PY $S/assemble_bank.py --input $IN --file $SC --out BANK   # Agents 4+5 via circuit skill",
    "$PY $S/bank_to_pdf.py --bank BANK/<bank_id>.yaml"]), mono))
S(P("Files a bank folder contains (Chen's layout):", h2))
S(table([["File", "Role"],
         ["<font face='Courier'>circuit-input.yaml</font>", "the recipe: family, specs, count, ranges, difficulty, seed"],
         ["<font face='Courier'>circuit-input.scenarios.yaml</font>", "Chen's sidecar: accepted lingo (+ rejected with reasons) — the source of truth"],
         ["<font face='Courier'>&lt;bank_id&gt;.yaml</font>", "the bank in Chen's template: items, options, worked solutions — the importable product"],
         ["<font face='Courier'>figures/qN.png</font>", "one figure per item"],
         ["<font face='Courier'>&lt;bank_id&gt;.pdf</font>", "printable worksheet + answer key (for humans; students never see the whole bank)"]],
        widths=[2.3 * inch, 4.3 * inch]))
S(P("Repositories: <font face='Courier'>myrlaphil/circuit-diagram-skill</font> (public, the engine) · <font face='Courier'>myrlaphil/circuit-bank-skill</font> "
    "(private, standalone glue) · fork of <font face='Courier'>Zhongzhou/isomorphic-bank-creation-skills</font>, branch <font face='Courier'>circuit-bank</font> "
    "(private, glue installed beside his skills) · <font face='Courier'>myrlaphil/circuit-banks</font> (public, banks only).", small))


def on_page(canv, doc):
    canv.saveState()
    canv.setFont(FONT, 8); canv.setFillColor(MUTED)
    canv.drawString(0.9 * inch, 0.55 * inch, "How the circuit bank works · research-group notes")
    canv.drawRightString(letter[0] - 0.9 * inch, 0.55 * inch, str(doc.page))
    canv.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                        bottomMargin=0.85 * inch, title="How the circuit bank works", author="Myrla Phillippe")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(OUT)

#!/usr/bin/env python3
"""Top-to-bottom workflow charts for presentations.
    workflow-simple    - for someone hearing about the project for the first time (Goal + 6 steps)
    workflow-detailed  - for someone who knows problem banks and wants the mechanics (Goal + 7 steps)
Each exists as: light SVG/PNG, dark glossy SVG/PNG (keywords in amber), two half charts (-p1, -p2) for slides,
and four self-contained HTML pages:
    workflow-simple.html / workflow-detailed.html             the whole chart, fitted to the screen
    workflow-simple-slides.html / workflow-detailed-slides.html two screens (Goal..step 3 | the rest), arrow keys
The byline (photo, name, role) sits in the header of every chart, top right.
Colour = what kind of thing does the work: rule-based code, AI (language model), file / output.
    python3 docs/build_workflow_charts.py      (PNGs need rsvg-convert)
"""
import base64
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = "Helvetica, Arial, sans-serif"
MONO = "Menlo, Courier, monospace"
PHOTO = HERE / "myrla-phillippe.jpg"
NAME, ROLE = "Myrla Phillippe", "Physics Graduate Student"
FIG_Q1 = HERE.parent / "PHY II Electricity and Magnetism" / "1_DC Circuits" / "PHY2-DC-SPRTC3-10292026" / "figures" / "q1.png"

THEMES = {
    "light": dict(bg="#FFFFFF", code="#DCE6EE", ai="#F3D9D3", out="#E2EEDC", goal="#F3EFEA",
                  ink="#1E1E1E", muted="#555555", acc="#8A2A1B", edge="#D8D2CA", arrow="#555555",
                  mono="#1E1E1E", key="#8A2A1B", legend_edge="#C9C2B8", glossy=False),
    "dark": dict(bg="#0F141B", code="#2B4C7E", ai="#8C3550", out="#2F6B4F", goal="#3F4756",
                 ink="#FFFFFF", muted="#E3E8F0", acc="#FFD166", edge="rgba(255,255,255,0.28)", arrow="#F2F5F9",
                 mono="#BFE6FF", key="#FFD166", legend_edge="rgba(255,255,255,0.35)", glossy=True),
}
T = THEMES["light"]
CODE = AI = OUT = GOAL = INK = MUTED = ACC = EDGE = None


def use(theme):
    global T, CODE, AI, OUT, GOAL, INK, MUTED, ACC, EDGE
    T = THEMES[theme]
    CODE, AI, OUT, GOAL = T["code"], T["ai"], T["out"], T["goal"]
    INK, MUTED, ACC, EDGE = T["ink"], T["muted"], T["acc"], T["edge"]


# words that get the accent colour inside body text (longest first so "circuit lingo" wins over "lingo")
KEYWORDS = ["circuit lingo", "circuit-diagram engine", "3 reduction steps", "three reduction steps", "reduction step",
            "reduction steps", "Schemdraw", "lingo", "AI", "ESTELA", "enumerator", "critic", "distractors",
            "isomorphic", "canonical shape", "deterministic", "QTI", "YAML", "Canvas", "Fisher's exact test",
            "5–6 resistors", "30 distinct circuits", "exactly 30", "30 problems", "rule-based", "wrong options",
            "source: llm", "source: enumerate", "worked solution", "seed", "provenance", "difficulty"]
_KW = re.compile("(" + "|".join(re.escape(k) for k in sorted(KEYWORDS, key=len, reverse=True)) + r")(?![\w-])")


class Chart:
    def __init__(self, title, subtitle, box_x, box_w, side_x, side_w, left_x=None, left_w=0):
        self.p = []
        self.bx, self.bw, self.sx, self.sw = box_x, box_w, side_x, side_w
        self.lx, self.lw = left_x, left_w
        self.w = side_x + side_w + 30
        self.y = 136
        self.bottoms = {"main": 130, "right": 130, "left": 130}      # lowest drawn edge per column
        self.text(30, 46, title, 34, INK, weight="bold")
        self.text(30, 74, subtitle, 16)
        lx = 30
        for fill, t in ((CODE, "rule-based code (same input, same output, every time)"), (AI, "AI language model"),
                        (OUT, "file or output"), (GOAL, "goal / context")):
            self.p.append(f'<rect x="{lx}" y="92" width="20" height="15" fill="{fill}" stroke="{T["legend_edge"]}"/>')
            self.text(lx + 28, 104, t, 14)
            lx += 28 + 7.6 * len(t) + 32
        self.byline()

    # ---- bookkeeping
    def _col(self, x):
        if x < self.bx:
            return "left"
        if x > self.bx:
            return "right"
        return "main"

    def _touch(self, x, bottom):
        c = self._col(x)
        self.bottoms[c] = max(self.bottoms[c], bottom)

    @staticmethod
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def text(self, x, y, s, size=16, fill=None, anchor="start", weight="normal", family=F, keywords=False):
        fill = MUTED if fill is None else fill
        if keywords:
            # «…» forces a whole phrase into the accent colour; otherwise single keywords are matched
            def kw(seg):
                parts = _KW.split(seg)
                return "".join(f'<tspan fill="{T["key"]}" font-weight="bold">{self.esc(t)}</tspan>' if i % 2 else self.esc(t)
                               for i, t in enumerate(parts))
            body = "".join(f'<tspan fill="{T["key"]}" font-weight="bold">{self.esc(t)}</tspan>' if i % 2 else kw(t)
                           for i, t in enumerate(re.split("«(.*?)»", s)))
        else:
            body = self.esc(s)
        self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
                      f'font-weight="{weight}" font-family="{family}">{body}</text>')

    def panel(self, x, y, w, h, fill, at=None):
        """a rounded panel; glossy = one smooth gradient + shadow.  `at` inserts it earlier in the draw order."""
        if T["glossy"]:
            gid = f"g{len(self.p)}_{int(y)}"
            parts = [f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                     f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.16"/>'
                     f'<stop offset="0.6" stop-color="#FFFFFF" stop-opacity="0"/>'
                     f'<stop offset="1" stop-color="#000000" stop-opacity="0.12"/></linearGradient>',
                     f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" filter="url(#shadow)"/>',
                     f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="url(#{gid})" stroke="{EDGE}" stroke-width="1.5"/>']
        else:
            parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{EDGE}" stroke-width="1.5"/>']
        if at is None:
            self.p += parts
        else:
            self.p[at:at] = parts
        self._touch(x, y + h)

    def box(self, fill, title, lines, tag=None, gap=56, x=None, w=None, y=None, pad_bottom=18):
        """a stage box; returns (top, bottom). lines starting with '`' are set in monospace."""
        x = self.bx if x is None else x
        w = self.bw if w is None else w
        top = self.y if y is None else y
        h = 52 + 25 * len(lines) + pad_bottom
        self.panel(x, top, w, h, fill)
        self.text(x + 20, top + 34, title, 22, INK, weight="bold")
        for i, ln in enumerate(lines):
            if ln.startswith("`"):
                self.text(x + 32, top + 66 + i * 25, ln[1:], 15, T["mono"], family=MONO)
            else:
                self.text(x + 20, top + 66 + i * 25, ln, 16, keywords=True)
        if tag:
            self.text(x + w - 16, top + h - 12, tag, 14, ACC, anchor="end")
        if y is None:
            self.y = top + h + gap
        return top, top + h

    def file_(self, y, name, note):
        x, w = self.sx, self.sw
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="64" rx="8" fill="{OUT}" stroke="{T["legend_edge"]}" '
                      f'stroke-dasharray="4,3"{" filter=\"url(#shadow)\"" if T["glossy"] else ""}/>')
        self.text(x + w / 2, y + 27, name, 15, T["mono"], "middle", family=MONO)
        self.text(x + w / 2, y + 50, note, 13, MUTED, "middle")
        self._touch(x, y + 64)

    # ---- arrows
    def arrow(self, y1, y2, label=None):
        x = self.bx + self.bw / 2
        self.p.append(f'<path d="M{x},{y1} L{x},{y2}" stroke="{T["arrow"]}" stroke-width="7" stroke-linecap="round" fill="none" marker-end="url(#a)"/>')
        if label:
            self.text(x + 18, (y1 + y2) / 2 + 6, label, 16, MUTED)

    def side_arrow(self, y, label=None, dashed=True):
        dash = ' stroke-dasharray="8,6"' if dashed else ""
        a, b = self.bx + self.bw, self.sx
        self.p.append(f'<path d="M{a},{y} L{b},{y}" stroke="{T["arrow"]}" stroke-width="4" stroke-linecap="round" fill="none" marker-end="url(#a)"{dash}/>')
        if label:
            self.text((a + b) / 2, y - 10, label, 13, MUTED, "middle")

    def left_arrow(self, y):
        self.p.append(f'<path d="M{self.bx},{y} L{self.lx + self.lw},{y}" stroke="{T["arrow"]}" stroke-width="4" '
                      f'stroke-linecap="round" fill="none" marker-end="url(#a)"/>')

    def loop(self, y_from, y_to, label, x_gutter):
        """arrow leaving the box at y_from on the left, going up to y_to, re-entering on the left"""
        x0 = self.bx
        self.p.append(f'<path d="M{x0},{y_from} L{x_gutter},{y_from} L{x_gutter},{y_to} L{x0},{y_to}" '
                      f'stroke="{T["arrow"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none" marker-end="url(#a)"/>')
        for i, ln in enumerate(label.split("\n")):
            self.text(x_gutter - 10, (y_from + y_to) / 2 + i * 19, ln, 15, MUTED, "end")

    # ---- the live example panel
    def example(self, y, options, steps, x, w, title="In action: problem 1 of 30"):
        """lingo -> the figure the engine drew -> the five options -> the reduction steps; sized to its content"""
        img_w = w - 36
        img_h = int(img_w * 1212 / 1506)
        mark = len(self.p)
        self.text(x + 18, y + 34, title, 20, INK, weight="bold")
        cy = y + 66
        self.text(x + 18, cy, "lingo in", 13, T["key"], weight="bold")
        for ln in ("source: 20 V", "circuit: 12 || 4 || (10 || 10 + 1)", "ask: total current"):
            cy += 23
            self.text(x + 30, cy, ln, 15, T["mono"], family=MONO)
        cy += 34
        self.text(x + 18, cy, "figure out (Schemdraw)", 13, T["key"], weight="bold")
        cy += 10
        data = base64.b64encode(FIG_Q1.read_bytes()).decode("ascii")
        self.p.append(f'<rect x="{x + 18}" y="{cy}" width="{img_w}" height="{img_h}" rx="8" fill="#FFFFFF"/>')
        self.p.append(f'<image x="{x + 18}" y="{cy}" width="{img_w}" height="{img_h}" href="data:image/png;base64,{data}"/>')
        cy += img_h + 30
        self.text(x + 18, cy, "options out", 13, T["key"], weight="bold")
        for i, o in enumerate(options):
            cy += 24
            tick = "  ✓ correct" if i == 4 else ""
            self.text(x + 30, cy, f"({'ABCDE'[i]})  {o}{tick}", 15, INK if i == 4 else MUTED, weight="bold" if i == 4 else "normal")
        cy += 34
        self.text(x + 18, cy, "the 3 reduction steps", 13, T["key"], weight="bold")
        for st in steps:
            cy += 23
            self.text(x + 30, cy, st, 14)
        self.panel(x, y, w, cy + 26 - y, OUT, at=mark)

    # ---- byline: photo + name in the header, top right
    def byline(self):
        r = 40
        y, x_img = 18, self.w - 30 - 2 * r
        data = base64.b64encode(PHOTO.read_bytes()).decode("ascii")
        self.p.append(f'<clipPath id="clip"><circle cx="{x_img + r}" cy="{y + r}" r="{r}"/></clipPath>')
        self.p.append(f'<image x="{x_img}" y="{y}" width="{2 * r}" height="{2 * r}" preserveAspectRatio="xMidYMin slice" '
                      f'clip-path="url(#clip)" href="data:image/jpeg;base64,{data}"/>')
        self.p.append(f'<circle cx="{x_img + r}" cy="{y + r}" r="{r}" fill="none" stroke="{T["legend_edge"]}" stroke-width="2"/>')
        self.text(x_img - 16, y + 34, NAME, 20, INK, "end", weight="bold")
        self.text(x_img - 16, y + 58, ROLE, 15, MUTED, "end")

    def save(self, path):
        h = max(self.bottoms.values()) + 20
        head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w // 2}" height="{h // 2}" '
                f'viewBox="0 0 {self.w} {h}" font-family="{F}">',
                f'<rect width="{self.w}" height="{h}" fill="{T["bg"]}"/>',
                '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{T["arrow"]}"/></marker>'
                '<filter id="shadow" x="-5%" y="-5%" width="110%" height="120%">'
                '<feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="0.55"/></filter>'
                '</defs>']
        path.write_text("\n".join(head + self.p + ["</svg>"]), encoding="utf-8")
        if shutil.which("rsvg-convert"):
            subprocess.run(["rsvg-convert", "-z", "2", "-o", str(path.with_suffix(".png")), str(path)], check=True)
        return path


# ---------------------------------------------------------------- SIMPLE
def simple(part=None):
    """part None = whole chart; 1 = Goal + steps 1-3; 2 = steps 4-6"""
    sub = "Every arrow is a program step. AI appears in exactly one place."
    if part == 2:
        sub += "   (continued: steps 4–6)"
    c = Chart("From a one-page request to an exam-ready problem bank", sub, box_x=30, box_w=780, side_x=920, side_w=370)
    if part != 2:
        t, b = c.box(GOAL, "Goal", ["30 exam problems that all ask the same question (total current from the battery),",
                                    "each on a different circuit, all at one defendable difficulty,",
                                    "ready to load into an exam builder."], tag="problem to solve")
        c.arrow(b, c.y)
        t, b = c.box(GOAL, "1  Request", ["One short file written by the instructor:",
                                          "`how many: 30   voltage: 6–24 V   resistors: 1–12 Ω",
                                          "`difficulty: 3 reduction steps, 5–6 resistors per circuit"], tag="plain settings, no code")
        c.box(AI, "Where AI is used", ["Reads the request as written and",
                                       "fixes typos or wording.",
                                       "«It never invents circuits, numbers,»",
                                       "«answers or wrong options.»",
                                       "Only if the request needs a circuit",
                                       "type no rule can produce may AI",
                                       "propose one; such items are tagged",
                                       "and still checked in step 3."], x=c.sx, w=c.sw, y=t - 20, pad_bottom=14)
        c.side_arrow(t + 90, "reads it")
        c.arrow(b, c.y)
        t, b = c.box(CODE, "2  List every circuit that fits", [
            "Code enumerates all circuit shapes with exactly 3 reduction steps and 5–6 resistors.",
            "(A reduction step = merging one series run or one parallel group into a single resistor.)",
            "There are exactly 30 such shapes, so the bank has 30 distinct circuits.",
            "Each shape gets resistor and battery values, written in a tiny text notation, “circuit lingo”:",
            "`source: 20 V",
            "`circuit: 12 || 4 || (10 || 10 + 1)      ( || = parallel, + = series )",
            "`ask: total current"], tag="enumerator")
        c.arrow(b, c.y)
        t, b = c.box(CODE, "3  Check every circuit", [
            "Each lingo line is parsed and solved by the circuit code.",
            "Rejected if: it does not parse, values are outside the request, the step count is wrong,",
            "or the shape repeats one already accepted.  Accepted items are counted toward the 30."], tag="critic", gap=10 if part == 1 else 56)
        if part == 1:
            c.arrow(b, b + 44, "continued on the next page: steps 4–6")
            c.bottoms["main"] = b + 44
        else:
            c.arrow(b, c.y)
    if part != 1:
        if part == 2:
            c.y = 186
            c.arrow(124, c.y, "from step 3: the accepted circuits")
        t, b = c.box(CODE, "4  Build each problem", [
            "Solve it step by step (worked solution).",
            "Draw the circuit with Schemdraw (the figure).",
            "«Compute the wrong options from known student mistakes»: all resistors added in series,",
            "parallel group not inverted, a branch current reported, plus one decoy near the largest value.",
            "Shuffle the option order."], tag="circuit-diagram engine")
        c.example(t, ["0.54 A", "17.14 A", "5.00 A", "15.43 A", "10.00 A"],
                  ["1.  10 ‖ 10 → 5 Ω", "2.  5 + 1 → 6 Ω", "3.  12 ‖ 4 ‖ 6 → 2 Ω,  so I = 20 V / 2 Ω = 10 A"], x=c.sx, w=c.sw)
        c.side_arrow(t + 60, "example", dashed=False)
        c.arrow(b, c.y)
        t, b = c.box(OUT, "5  Output", ["One bank file (YAML) with 30 problems, «figures», «answers», wrong options and «solutions»,",
                                        "plus a «PDF» and an «HTML» worksheet, each with its answer key.",
                                        "Every item carries a tag saying whether code or AI proposed it (here: 30 code, 0 AI)."])
        c.arrow(b, c.y)
        t, b = c.box(OUT, "6  Use", ["The bank loads into the ESTELA exam builder straight from GitHub.",
                                     "Each exam version draws one of the 30 problems, so students get different circuits",
                                     "of the same difficulty.  Export to Canvas (QTI), PDF or LaTeX."], gap=0)
    return c.save(HERE / f"workflow-simple{PART}{SUFFIX}.svg")


# ---------------------------------------------------------------- DETAILED
def detailed(part=None):
    """part None = whole chart; 1 = Goal + steps 1-4 (the generate/critique loop); 2 = steps 5-7"""
    sub = "Generate → check → count loop from the isomorphic-bank-creation framework; every numerical stage is rule-based code."
    if part == 2:
        sub += "   (continued: steps 5–7)"
    if part == 1:
        c = Chart("Circuit problem-bank workflow — detailed", sub, box_x=230, box_w=820, side_x=1140, side_w=370)
        gutter = 150
    else:
        c = Chart("Circuit problem-bank workflow — detailed", sub, box_x=460, box_w=820, side_x=1370, side_w=370, left_x=30, left_w=370)
        gutter = 370
    if part != 2:
        t, b = c.box(GOAL, "Goal", ["An isomorphic bank: same objective, variation beyond numbers (the circuit topology changes),",
                                    "each variant has its own solution path, and difficulty is held constant and defined up front."])
        c.arrow(b, c.y)
        t, b = c.box(GOAL, "1  Input scheme", ["Bank metadata (id, title, learning objective, question type = multiple choice).",
                                               "Counts: n_scenarios 30.   Ranges: resistors 1–12 Ω, voltage 6–24 V.",
                                               "Difficulty: reduction_steps 3, min_resistors 5, max_resistors 6.",
                                               "Generator: auto (rules first, AI only as a tagged fallback), seed 0."], tag="validated by schema check")
        c.file_(t + 16, "circuit-input.yaml", "the recipe; the item count lives here, never in chat")
        c.side_arrow(t + 48)
        c.box(AI, "AI, step 1", ["Turns a plain-English request into",
                                 "this file; fixes typos. Nothing numerical."], x=c.sx, w=c.sw, y=t + 100, pad_bottom=10)
        c.arrow(b, c.y)
        t, b = c.box(CODE, "2  Scenario list", ["A sidecar file tracks the target (30), accepted / pending / rejected scenarios,",
                                                "reasons for rejection and the pass count (cap: 5 passes)."], tag="scenario_list.py")
        c.file_(t + 24, "circuit-input.scenarios.yaml", "source of truth for what is in the bank")
        c.side_arrow(t + 56)
        c.arrow(b, c.y)
        loop_top = c.y
        t, b = c.box(CODE, "3  Generate  (Agent 2)", [
            "Enumerator lists all series-parallel shapes in the band: 5 resistors → 10 shapes, 6 → 20; total 30.",
            "Canonical signature ignores sibling order, so 3 || 6 + 4 and 6 || 3 + 4 are one shape.",
            "Values from the pool {1,2,3,4,5,6,8,9,10,12} Ω with “clean arithmetic”: half-ohm intermediates,",
            "answers to ≤ 2 decimals, no repeated answers.  Deterministic: same seed → identical bank.",
            "`source: 20 V   circuit: 12 || 4 || (10 || 10 + 1)   ask: total current"], tag="enumerate_lingo.py")
        c.box(AI, "AI, fallback only", ["Used when the request asks for a",
                                        "family the enumerator has no rule for",
                                        "(capacitors, meters, other asks).",
                                        "Proposals go through step 4 like any",
                                        "other and are tagged source: llm.",
                                        "Enumerated items: source: enumerate."], x=c.sx, w=c.sw, y=t, pad_bottom=10)
        c.side_arrow(t + 100, "if no rule fits")
        c.arrow(b, c.y)
        t, b = c.box(CODE, "4  Critique  (Agent 3)", [
            "For every proposal: parse the lingo → solve → check ranges → count reduction steps → compare",
            "canonical shape with everything accepted so far.  Rejections carry a reason",
            "(does not parse / outside ranges / wrong step count / repeated shape / repeated answer).",
            "Accepted items are added via the framework's own add command; counts go back to the sidecar."],
            tag="critic.py --apply", gap=10 if part == 1 else 56)
        c.loop(b - 20, loop_top + 20, "fewer than 30\naccepted:\nnext pass\n(max 5)", x_gutter=gutter)
        if part == 1:
            c.arrow(b, b + 44, "continued on the next page: steps 5–7")
            c.bottoms["main"] = b + 44
        else:
            c.arrow(b, c.y)
    if part != 1:
        if part == 2:
            c.y = 186
            c.arrow(124, c.y, "from step 4: the 30 accepted circuits")
        t, b = c.box(CODE, "5  Assemble  (replaces Agents 4 & 5)", [
            "For each accepted lingo, the circuit-diagram engine:",
            "   • parses and solves, producing a numbered reduction (3 steps) and the total current;",
            "   • draws the figure with Schemdraw in the textbook (ladder) layout;",
            "   • computes distractors: all_series, no_invert, branch_current (+ fallbacks),",
            "     and decoy_near_largest = 0.9 × the largest option;",
            "   • rotates the correct answer's position (k = n mod 5) so it is not always the same letter;",
            "   • writes feedback naming the mistake behind each wrong option."], tag="assemble_bank.py + distractors.py")
        c.example(t, ["0.54 A   (all in series)", "17.14 A  (not inverted)", "5.00 A   (branch current)", "15.43 A  (decoy)", "10.00 A"],
                  ["1.  R3 ‖ R4:  10 ‖ 10 → 5 Ω", "2.  + R5:  5 + 1 → 6 Ω", "3.  R1 ‖ R2 ‖ R345:  12 ‖ 4 ‖ 6 → 2 Ω",
                   "     I = 20 V / 2 Ω = 10.00 A"], x=c.lx, w=c.lw)
        c.left_arrow(t + 60)
        c.arrow(b, c.y)
        t, b = c.box(OUT, "6  Bank file", ["Problem-bank YAML in the shared template: 30 multiple-choice items, 5 options each,",
                                           "figure paths, worked solutions, feedback, per-item source tag,",
                                           "a difficulty block (steps 3 ×30; resistors 5 ×10, 6 ×20; parallel groups 1 ×15, 2 ×15)",
                                           "and a provenance count (enumerate 30, llm 0).   PDF + HTML worksheet with key alongside."])
        c.file_(t + 16, "PHY2-DC-SPRTC3-10292026.yaml", "+ Figures/q1…q30.png + .pdf + .html")
        c.side_arrow(t + 48)
        c.arrow(b, c.y)
        t, b = c.box(OUT, "7  Delivery", ["Folder added to the ESTELA problem-bank repository (pull request).",
                                          "ESTELA Enhanced Exam Builder loads it from GitHub: each exam version draws one item,",
                                          "exports Canvas QTI, PDF or LaTeX.",
                                          "Planned validation: item-accuracy spread + extended Fisher's exact test on student data."], gap=0)
    return c.save(HERE / f"workflow-detailed{PART}{SUFFIX}.svg")


# ---------------------------------------------------------------- HTML
CSS = """
  :root { --bg:#0F141B; --fg:#E3E8F0; --btn:#2B4C7E; }
  html[data-theme="light"] { --bg:#FFFFFF; --fg:#1E1E1E; --btn:#DCE6EE; }
  html, body { margin:0; background:var(--bg); color:var(--fg); font-family:Helvetica, Arial, sans-serif; }
  .bar { position:fixed; top:10px; right:12px; display:flex; gap:8px; z-index:2; opacity:.35; transition:opacity .2s; }
  .bar:hover { opacity:1; }
  .bar button { background:var(--btn); color:var(--fg); border:1px solid rgba(128,128,128,.4); border-radius:8px;
                padding:5px 10px; font-size:13px; cursor:pointer; }
  .page { width:100vw; height:100vh; display:flex; align-items:center; justify-content:center; }
  .page svg { display:block; max-width:100vw; max-height:100vh; width:auto; height:100vh; }
  .dark { display:contents; } .light { display:none; }
  html[data-theme="light"] .dark { display:none; } html[data-theme="light"] .light { display:contents; }
  @media print { .bar { display:none; } .page { height:auto; } .page svg { height:auto; width:100%; } }
"""
PAGE_TPL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>{css}{extra_css}</style></head>
<body>
<div class="bar">{nav}<button onclick="toggle()">Light / dark</button><button onclick="document.documentElement.requestFullscreen()">Full screen</button></div>
{body}
<script>
function toggle(){{const h=document.documentElement;h.dataset.theme=h.dataset.theme==='light'?'':'light';}}
{script}
</script>
</body></html>
"""
SLIDES_CSS = """
  html { scroll-snap-type: y mandatory; overflow-y:scroll; }
  .page { scroll-snap-align:start; }
  .count { position:fixed; left:12px; bottom:10px; font-size:13px; opacity:.5; }
"""
SLIDES_JS = """
const pages=[...document.querySelectorAll('.page')];let i=0;const c=document.querySelector('.count');
function go(n){i=Math.max(0,Math.min(pages.length-1,n));pages[i].scrollIntoView({behavior:'smooth'});c.textContent=(i+1)+' / '+pages.length;}
document.addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();go(i+1);}
 if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();go(i-1);}});
document.addEventListener('scroll',()=>{const k=Math.round(window.scrollY/window.innerHeight);if(k!==i){i=k;c.textContent=(i+1)+' / '+pages.length;}});
c.textContent='1 / '+pages.length;
"""


def _svg(name):
    strip = lambda t: re.sub(r'<svg ([^>]*?)width="\d+" height="\d+" ', r'<svg \1', t, count=1)
    return (f'<div class="dark">{strip((HERE / f"{name}-dark.svg").read_text())}</div>'
            f'<div class="light">{strip((HERE / f"{name}.svg").read_text())}</div>')


def html_pages():
    for name, title in (("simple", "Circuit problem bank — workflow (simple)"),
                        ("detailed", "Circuit problem bank — workflow (detailed)")):
        out = HERE / f"workflow-{name}.html"
        out.write_text(PAGE_TPL.format(title=title, css=CSS, extra_css="", nav="", script="",
                                       body=f'<div class="page">{_svg(f"workflow-{name}")}</div>'), encoding="utf-8")
        print(out.name)
        out = HERE / f"workflow-{name}-slides.html"
        body = "".join(f'<div class="page">{_svg(f"workflow-{name}-p{k}")}</div>' for k in (1, 2)) + '<div class="count"></div>'
        nav = '<button onclick="go(i-1)">◀</button><button onclick="go(i+1)">▶</button>'
        out.write_text(PAGE_TPL.format(title=title + " — two pages", css=CSS, extra_css=SLIDES_CSS, nav=nav,
                                       script=SLIDES_JS, body=body), encoding="utf-8")
        print(out.name)


SUFFIX, PART = "", ""

if __name__ == "__main__":
    for theme, SUFFIX in (("light", ""), ("dark", "-dark")):
        use(theme)
        for part, PART in ((None, ""), (1, "-p1"), (2, "-p2")):
            for p in (simple(part), detailed(part)):
                print(p.name)
    html_pages()

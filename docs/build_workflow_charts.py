#!/usr/bin/env python3
"""Two top-to-bottom workflow charts for presentations (no author names):
    workflow-simple.svg    - for someone hearing about the project for the first time
    workflow-detailed.svg  - for someone who knows problem banks and wants the mechanics
Colour = what kind of thing does the work: rule-based code, AI (language model), file / output.
Written twice: light (print) and -dark (glossy, for screens; keywords in amber).
    python3 docs/build_workflow_charts.py      (also writes PNGs if rsvg-convert is installed)
"""
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = "Helvetica, Arial, sans-serif"
MONO = "Menlo, Courier, monospace"

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
    def __init__(self, w, title, subtitle, box_x, box_w, side_x=None, side_w=0):
        self.w, self.p = w, []
        self.bx, self.bw, self.sx, self.sw = box_x, box_w, side_x, side_w
        self.y = 170
        self.text(40, 56, title, 36, INK, weight="bold")
        self.text(40, 88, subtitle, 17)
        lx = 40
        for fill, t in ((CODE, "rule-based code (same input, same output, every time)"), (AI, "AI language model"),
                        (OUT, "file or output"), (GOAL, "goal / context")):
            self.p.append(f'<rect x="{lx}" y="110" width="22" height="16" fill="{fill}" stroke="{T["legend_edge"]}"/>')
            self.text(lx + 30, 123, t, 15)
            lx += 30 + 8.0 * len(t) + 36

    @staticmethod
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def text(self, x, y, s, size=16, fill=None, anchor="start", weight="normal", family=F, keywords=False):
        fill = MUTED if fill is None else fill
        if keywords:
            parts = _KW.split(s)
            body = "".join(f'<tspan fill="{T["key"]}" font-weight="bold">{self.esc(t)}</tspan>' if i % 2 else self.esc(t)
                           for i, t in enumerate(parts))
        else:
            body = self.esc(s)
        self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
                      f'font-weight="{weight}" font-family="{family}">{body}</text>')

    def box(self, fill, title, lines, tag=None, mono=(), gap=56, x=None, w=None, y=None, pad_bottom=18):
        """a stage box; returns its (top, bottom). lines starting with '`' are set in monospace."""
        x = self.bx if x is None else x
        w = self.bw if w is None else w
        top = self.y if y is None else y
        h = 52 + 25 * len(lines) + pad_bottom
        if T["glossy"]:
            gid = f"g{len(self.p)}"
            self.p.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                          f'<stop offset="0" stop-color="{fill}" stop-opacity="1"/>'
                          f'<stop offset="1" stop-color="#000000" stop-opacity="0.45"/></linearGradient>')
            self.p.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="16" fill="{fill}"/>')
            self.p.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="16" fill="url(#{gid})" '
                          f'stroke="{EDGE}" stroke-width="1.5" filter="url(#shadow)"/>')
            # the sheen: a soft white band across the top half
            self.p.append(f'<rect x="{x + 2}" y="{top + 2}" width="{w - 4}" height="{h * 0.48}" rx="14" fill="url(#sheen)"/>')
        else:
            self.p.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{EDGE}" stroke-width="1.5"/>')
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

    def arrow(self, y1, y2, label=None, x=None):
        x = (self.bx + self.bw / 2) if x is None else x
        self.p.append(f'<path d="M{x},{y1} L{x},{y2}" stroke="{T["arrow"]}" stroke-width="7" stroke-linecap="round" fill="none" marker-end="url(#a)"/>')
        if label:
            self.text(x + 14, (y1 + y2) / 2 + 5, label, 14)

    def side_arrow(self, y, label=None, dashed=True, to_main=False):
        dash = ' stroke-dasharray="8,6"' if dashed else ""
        a, b = (self.sx, self.bx + self.bw) if to_main else (self.bx + self.bw, self.sx)
        self.p.append(f'<path d="M{a},{y} L{b},{y}" stroke="{T["arrow"]}" stroke-width="4" stroke-linecap="round" fill="none" marker-end="url(#a)"{dash}/>')
        if label:
            self.text((a + b) / 2, y - 10, label, 13, MUTED, "middle")

    def loop(self, y_from, y_to, label, x_gutter):
        """arrow leaving the box at y_from on the left, going up to y_to, re-entering on the left"""
        x0 = self.bx
        self.p.append(f'<path d="M{x0},{y_from} L{x_gutter},{y_from} L{x_gutter},{y_to} L{x0},{y_to}" '
                      f'stroke="{T["arrow"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none" marker-end="url(#a)"/>')
        for i, ln in enumerate(label.split("\n")):
            self.text(x_gutter - 10, (y_from + y_to) / 2 + i * 19, ln, 15, MUTED, "end")

    def save(self, path):
        h = self.y + 10
        head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w // 2}" height="{h // 2}" '
                f'viewBox="0 0 {self.w} {h}" font-family="{F}">',
                f'<rect width="{self.w}" height="{h}" fill="{T["bg"]}"/>',
                '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{T["arrow"]}"/></marker>'
                '<filter id="shadow" x="-5%" y="-5%" width="110%" height="120%">'
                '<feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="0.55"/></filter>'
                '<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">'
                '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.22"/>'
                '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient></defs>']
        path.write_text("\n".join(head + self.p + ["</svg>"]), encoding="utf-8")
        if shutil.which("rsvg-convert"):
            subprocess.run(["rsvg-convert", "-z", "2", "-o", str(path.with_suffix(".png")), str(path)], check=True)
        return path


# ---------------------------------------------------------------- SIMPLE
def simple():
    c = Chart(1420, "From a one-page request to an exam-ready problem bank",
              "Every arrow is a program step. AI appears in exactly one place.", box_x=120, box_w=780, side_x=1010, side_w=370)
    t, b = c.box(GOAL, "Goal", ["30 exam problems that all ask the same question (total current from the battery),",
                                "each on a different circuit, all at one defendable difficulty,",
                                "ready to load into an exam builder."], tag="problem to solve")
    c.arrow(b, c.y)
    t, b = c.box(GOAL, "1  Request", ["One short file written by the instructor:",
                                      "`how many: 30   voltage: 6–24 V   resistors: 1–12 Ω",
                                      "`difficulty: 3 reduction steps, 5–6 resistors per circuit"], tag="plain settings, no code")
    # AI side box next to the request
    c.box(AI, "Where AI is used", ["Reads the request as written and",
                                   "fixes typos or wording.",
                                   "It never invents circuits, numbers,",
                                   "answers or wrong options.",
                                   "Only if the request needs a circuit",
                                   "type no rule can produce may AI",
                                   "propose one; such items are tagged",
                                   "and still checked in step 3."],
          x=c.sx, w=c.sw, y=t - 20, pad_bottom=14)
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
        "or the shape repeats one already accepted.  Accepted items are counted toward the 30."], tag="critic")
    c.arrow(b, c.y)
    t, b = c.box(CODE, "4  Build each problem", [
        "Solve it step by step (worked solution).",
        "Draw the circuit with Schemdraw (the figure).",
        "Compute the wrong options from known student mistakes: all resistors added in series,",
        "parallel group not inverted, a branch current reported, plus one decoy near the largest value.",
        "Shuffle the option order."], tag="circuit-diagram engine")
    c.arrow(b, c.y)
    t, b = c.box(OUT, "5  Output", ["One bank file (YAML) with 30 problems, figures, answers, wrong options and solutions,",
                                    "plus a PDF worksheet and answer key.",
                                    "Every item carries a tag saying whether code or AI proposed it (here: 30 code, 0 AI)."])
    c.arrow(b, c.y)
    t, b = c.box(OUT, "6  Use", ["The bank loads into the ESTELA exam builder straight from GitHub.",
                                 "Each exam version draws one of the 30 problems, so students get different circuits",
                                 "of the same difficulty.  Export to Canvas (QTI), PDF or LaTeX."], gap=10)
    return c.save(HERE / f"workflow-simple{SUFFIX}.svg")


# ---------------------------------------------------------------- DETAILED
def detailed():
    c = Chart(1600, "Circuit problem-bank workflow — detailed",
              "Generate → check → count loop from the isomorphic-bank-creation framework; every numerical stage is rule-based code.",
              box_x=280, box_w=820, side_x=1200, side_w=370)

    def file_(y, name, note):
        c.p.append(f'<rect x="{c.sx}" y="{y}" width="{c.sw}" height="64" rx="8" fill="{OUT}" stroke="{T["legend_edge"]}" stroke-dasharray="4,3"{" filter=\"url(#shadow)\"" if T["glossy"] else ""}/>')
        c.text(c.sx + c.sw / 2, y + 27, name, 15, T["mono"], "middle", family=MONO)
        c.text(c.sx + c.sw / 2, y + 50, note, 13, MUTED, "middle")

    t, b = c.box(GOAL, "Goal", ["An isomorphic bank: same objective, variation beyond numbers (the circuit topology changes),",
                                "each variant has its own solution path, and difficulty is held constant and defined up front."])
    c.arrow(b, c.y)

    t, b = c.box(GOAL, "1  Input scheme", ["Bank metadata (id, title, learning objective, question type = multiple choice).",
                                           "Counts: n_scenarios 30.   Ranges: resistors 1–12 Ω, voltage 6–24 V.",
                                           "Difficulty: reduction_steps 3, min_resistors 5, max_resistors 6.",
                                           "Generator: auto (rules first, AI only as a tagged fallback), seed 0."], tag="validated by schema check")
    file_(t + 16, "circuit-input.yaml", "the recipe; the item count lives here, never in chat")
    c.side_arrow(t + 48)
    c.box(AI, "AI, step 1", ["Turns a plain-English request into",
                             "this file; fixes typos. Nothing numerical."], x=c.sx, w=c.sw, y=t + 100, pad_bottom=10)
    c.arrow(b, c.y)

    t, b = c.box(CODE, "2  Scenario list", ["A sidecar file tracks the target (30), accepted / pending / rejected scenarios,",
                                            "reasons for rejection and the pass count (cap: 5 passes)."], tag="scenario_list.py")
    file_(t + 24, "circuit-input.scenarios.yaml", "source of truth for what is in the bank")
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
        "Accepted items are added via the framework's own add command; counts go back to the sidecar."], tag="critic.py --apply")
    c.loop(b - 20, loop_top + 20, "fewer than 30\naccepted:\nnext pass\n(max 5)", x_gutter=190)
    c.arrow(b, c.y)

    t, b = c.box(CODE, "5  Assemble  (replaces Agents 4 & 5)", [
        "For each accepted lingo, the circuit-diagram engine:",
        "   • parses and solves, producing a numbered reduction (3 steps) and the total current;",
        "   • draws the figure with Schemdraw in the textbook (ladder) layout;",
        "   • computes distractors: all_series, no_invert, branch_current (+ fallbacks),",
        "     and decoy_near_largest = 0.9 × the largest option;",
        "   • rotates the correct answer's position (k = n mod 5) so it is not always the same letter;",
        "   • writes feedback naming the mistake behind each wrong option."], tag="assemble_bank.py + distractors.py")
    c.arrow(b, c.y)

    t, b = c.box(OUT, "6  Bank file", ["Problem-bank YAML in the shared template: 30 multiple-choice items, 5 options each,",
                                       "figure paths, worked solutions, feedback, per-item source tag,",
                                       "a difficulty block (steps 3 ×30; resistors 5 ×10, 6 ×20; parallel groups 1 ×15, 2 ×15)",
                                       "and a provenance count (enumerate 30, llm 0).   PDF worksheet + key alongside."])
    file_(t + 16, "PHY2-DC-SPRTC3-10292026.yaml", "+ Figures/q1…q30.png + .pdf")
    c.side_arrow(t + 48)
    c.arrow(b, c.y)

    t, b = c.box(OUT, "7  Delivery", ["Folder added to the ESTELA problem-bank repository (pull request).",
                                      "ESTELA Enhanced Exam Builder loads it from GitHub: each exam version draws one item,",
                                      "exports Canvas QTI, PDF or LaTeX.",
                                      "Planned validation: item-accuracy spread + extended Fisher's exact test on student data."], gap=10)
    return c.save(HERE / f"workflow-detailed{SUFFIX}.svg")


SUFFIX = ""

if __name__ == "__main__":
    for theme, SUFFIX in (("light", ""), ("dark", "-dark")):
        use(theme)
        for p in (simple(), detailed()):
            print(p.name, "+", p.with_suffix(".png").name)

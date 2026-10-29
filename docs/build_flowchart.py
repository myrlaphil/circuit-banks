#!/usr/bin/env python3
"""Top-to-bottom flow chart of the forked circuit-bank workflow, as one SVG (drops into PowerPoint/Keynote).
Colour = whose work: blue Chen (unchanged, run in place), copper circuit-bank glue (new), green circuit-diagram-skill.
    python3 docs/build_flowchart.py   -> docs/circuit-bank-flowchart.svg
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "circuit-bank-flowchart.svg"
W, H = 1180, 1790
CHEN, SKILL, GLUE, FILE = "#DCE6EE", "#E2EEDC", "#F7E3D4", "#F3EFEA"
INK, MUTED, ACC = "#1E1E1E", "#555555", "#8A2A1B"
F = "Helvetica, Arial, sans-serif"
MONO = "Menlo, Courier, monospace"

P = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W // 2}" height="{H // 2}" viewBox="0 0 {W} {H}" font-family="{F}">',
     f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
     '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
     '<path d="M0,0 L10,5 L0,10 z" fill="#777"/></marker></defs>']

# column geometry
SX, SW = 230, 560          # stage boxes
FX, FW = 830, 310          # file boxes (right column)
LX = 60                    # left gutter for the loop arrow


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=14, fill=MUTED, anchor="start", weight="normal", family=F):
    P.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" font-family="{family}">{esc(s)}</text>')


def stage(y, h, fill, title, lines, who):
    P.append(f'<rect x="{SX}" y="{y}" width="{SW}" height="{h}" rx="12" fill="{fill}" stroke="#D8D2CA"/>')
    text(SX + 18, y + 32, title, 20, INK, weight="bold")
    for i, ln in enumerate(lines):
        text(SX + 18, y + 60 + i * 20, ln, 14)
    text(SX + SW - 14, y + h - 12, who, 12, ACC, anchor="end")
    return y + h


def file_(y, name, note, h=56):
    P.append(f'<rect x="{FX}" y="{y}" width="{FW}" height="{h}" rx="6" fill="{FILE}" stroke="#C9C2B8" stroke-dasharray="4,3"/>')
    text(FX + FW / 2, y + 24, name, 13, INK, "middle", family=MONO)
    text(FX + FW / 2, y + 43, note, 11, MUTED, "middle")


def down(y1, y2, label=None):
    x = SX + SW / 2
    P.append(f'<path d="M{x},{y1} L{x},{y2}" stroke="#777" stroke-width="2" fill="none" marker-end="url(#a)"/>')
    if label:
        text(x + 12, (y1 + y2) / 2 + 5, label, 12)


def side(y, label=None):
    """short dashed arrow from a stage to the file box beside it"""
    P.append(f'<path d="M{SX + SW},{y} L{FX},{y}" stroke="#777" stroke-width="1.5" fill="none" marker-end="url(#a)" stroke-dasharray="5,4"/>')
    if label:
        text((SX + SW + FX) / 2, y - 7, label, 11, MUTED, "middle")


# ---- title + legend
text(40, 50, "How the forked circuit-bank workflow works", 30, INK, weight="bold")
text(40, 78, "Chen's problem-creation loop, run unchanged; two agents replaced by scripts; the numerical stage done by circuit-diagram-skill", 14)
lx = 40
for fill, t in ((CHEN, "Zhongzhou Chen — unchanged, run in place"), (GLUE, "circuit-bank glue — new, deterministic"),
                (SKILL, "circuit-diagram-skill — deterministic engine"), (FILE, "file on disk")):
    P.append(f'<rect x="{lx}" y="98" width="18" height="14" fill="{fill}" stroke="#C9C2B8"/>')
    text(lx + 26, 110, t, 13)
    lx += 300 if fill != SKILL else 320

# ---- stages, top to bottom
y = 150
y1 = stage(y, 145, CHEN, "1  Input scheme", ["Chen's input YAML (name, context, specs, n_scenarios, formulas)",
                                              "+ bank: id, question type, drawing layout",
                                              "+ ranges: resistors, voltage, min/max resistors, reduction steps",
                                              "+ generator: enumerate | llm, seed"], "format: Chen")
file_(y + 35, "circuit-input.yaml", "the recipe — the item count lives here, never in chat"); side(y + 63)
down(y1, y1 + 40)

y = y1 + 40
y1 = stage(y, 105, CHEN, "2  Agent 1 check + confirmation", ["validate_input.py — required fields, warning if n > 10",
                                                            "the edited input is shown; nothing runs until the user confirms"], "Chen")
down(y1, y1 + 40)

y = y1 + 40
y1 = stage(y, 125, CHEN, "3  Sidecar + loop control", ["scenario_list.py  init → target copied from n_scenarios",
                                                       "receive → update_count + 1, needed = target − accepted",
                                                       "5-pass cap; accepted / pending / rejected (with reasons)"], "Chen")
file_(y + 35, "circuit-input.scenarios.yaml", "the source of truth — the bank regenerates from it"); side(y + 63)
loop_target = y1 - 20          # the loop arrow returns here (into stage 3)
down(y1, y1 + 40, "needed > 0")

# loop region (4 and 5)
y = y1 + 40
y1 = stage(y, 160, GLUE, "4  Propose candidates", ["enumerate_lingo.py (default, no AI): every series-parallel shape in the",
                                                   "difficulty band, skipping accepted shapes; values from a pool by seed",
                                                   "so every intermediate resistance is clean and no answer repeats",
                                                   "— or Agent 2 (LLM) writes lingo, opt-in (generator: llm)"], "replaces Chen's Agent 2")
file_(y + 40, "agent2.json", "the candidates — same JSON either way"); side(y + 68)
down(y1, y1 + 40, "add_lingo.py → pending")

y = y1 + 40
y1 = stage(y, 175, GLUE, "5  Critic — a script, not an opinion", ["critic.py, for each pending lingo:",
                                                                 "parse + solve with the circuit engine          → else reject",
                                                                 "canonical shape not already accepted           → else reject (same path)",
                                                                 "reduction steps = this bank's difficulty       → else reject",
                                                                 "resistor / voltage / count within the ranges   → else reject"], "replaces Chen's Agent 3")
loop_source = y1 - 30
side(y + 75, "remove: keep / reject + reason")
down(y1, y1 + 40, "complete")

# loop arrow on the left: from the critic back up into stage 3 (receive again)
P.append(f'<path d="M{SX},{loop_source} L{LX + 40},{loop_source} L{LX + 40},{loop_target} L{SX},{loop_target}" '
         f'stroke="#777" stroke-width="2" fill="none" stroke-dasharray="7,5" marker-end="url(#a)"/>')
mid = (loop_source + loop_target) / 2
text(LX + 30, mid - 10, "not complete:", 12, MUTED, "middle")
text(LX + 30, mid + 10, "receive again", 12, MUTED, "middle")
text(LX + 30, mid + 30, "(Chen's loop)", 12, MUTED, "middle")

y = y1 + 40
y1 = stage(y, 150, SKILL, "6  Circuit engine", ["circuit-diagram-skill, once per accepted lingo:",
                                                 "parse → solve (reduction steps, per-part current / voltage / power)",
                                                 "→ Schemdraw figure (one layout for the whole bank) → worked solution",
                                                 "same text in → same figure, numbers and solution out"], "replaces Chen's Agents 4 + 5")
file_(y + 35, "figures/qN.png", "one figure per item"); side(y + 63)
down(y1, y1 + 40)

y = y1 + 40
y1 = stage(y, 150, GLUE, "7  Assemble the bank", ["distractors.py — three wrong answers, each one named mistake",
                                                   "(all_series, no_invert, branch_current; fallbacks on collision)",
                                                   "assemble_bank.py → bank YAML in Chen's template, status ready",
                                                   "bank_to_pdf.py → printable worksheet + answer key"], "new")
file_(y + 5, "<id>.yaml", "the bank — Chen's template; importable"); side(y + 33)
file_(y + 68, "<id>.pdf", "worksheet + key — for humans, never students"); side(y + 96)

# ---- bottom: what's Chen's / what changed
y = y1 + 50
bw = (W - 80 - 20) / 2
P.append(f'<rect x="40" y="{y}" width="{bw}" height="290" rx="12" fill="{CHEN}" stroke="#D8D2CA"/>')
text(58, y + 32, "What is Chen's — used unchanged", 18, INK, weight="bold")
for i, ln in enumerate(["the definition of isomorphic (same objective, variation beyond", "   numbers, a changed solution, consistent difficulty)",
                        "the input scheme and its required fields", "Agent 1 check and the confirmation gate",
                        "scenario_list.py: sidecar, target, pass cap, accept / reject + reasons", "the bank YAML template and the folder convention",
                        "", "Nothing in his repository was edited: the skill is a sibling folder", "(.cursor/skills/circuit-bank/) and calls his script in place."]):
    text(58, y + 62 + i * 22, ln, 13.5, INK if ln.startswith(("Nothing", "(.cursor")) else MUTED)
P.append(f'<rect x="{60 + bw}" y="{y}" width="{bw}" height="290" rx="12" fill="{GLUE}" stroke="#D8D2CA"/>')
text(78 + bw, y + 32, "What changed — and why", 18, INK, weight="bold")
for i, ln in enumerate(["Agent 2 → enumerator: circuits are a finite set (34 shapes at", "   3 steps); list them instead of guessing",
                        "Agent 3 → script: a circuit can be parsed, solved and canonicalised,", "   so 'is this a new problem?' is computed, not judged",
                        "Agents 4 + 5 → circuit engine: his sympy stage expresses formulas,", "   not topologies; the engine also draws the figure",
                        "added: a difficulty band (reduction steps), computed distractors,", "   figures, PDF, and a 'no two answers repeat' rule",
                        "result: 30 items, one difficulty, 0 rejections, no LLM; same seed → same bank"]):
    text(78 + bw, y + 62 + i * 22, ln, 13.5, INK if ln.startswith("result") else MUTED)

P.append("</svg>")
OUT.write_text("\n".join(P), encoding="utf-8")
print(OUT, "height used:", y + 290)

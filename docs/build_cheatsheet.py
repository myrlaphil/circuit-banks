#!/usr/bin/env python3
"""One clean PDF: the plain-language version of the project with links into the GitHub repos.
    ~/.claude/skills/circuit-bank-skill/.venv/bin/python docs/build_cheatsheet.py
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = Path(__file__).resolve().parent / "circuit-bank-cheat-sheet.pdf"

FONT = "Helvetica"
for cand in ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
    if Path(cand).is_file():
        pdfmetrics.registerFont(TTFont("Body", cand)); FONT = "Body"; break

RED = colors.HexColor("#B3261E"); INK = colors.HexColor("#1E1E1E"); MUTED = colors.HexColor("#555555"); LINK = colors.HexColor("#1F4E79")
ss = getSampleStyleSheet()
body = ParagraphStyle("b", parent=ss["BodyText"], fontName=FONT, fontSize=11, leading=15, textColor=INK, spaceAfter=5)
small = ParagraphStyle("s", parent=body, fontSize=9.5, leading=13, textColor=MUTED)
title = ParagraphStyle("t", parent=ss["Title"], fontName=FONT, fontSize=22, leading=26, alignment=0, textColor=INK, spaceAfter=4)
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName=FONT, fontSize=15, leading=19, textColor=INK, spaceBefore=12, spaceAfter=4)
red = ParagraphStyle("r", parent=body, textColor=RED, fontSize=10.5, leading=14, spaceBefore=2, spaceAfter=6)
step = ParagraphStyle("st", parent=body, leftIndent=18, firstLineIndent=-18, spaceAfter=4)
quote = ParagraphStyle("q", parent=body, leftIndent=14, textColor=INK, fontSize=11.5, leading=16, spaceAfter=4)

GH = "https://github.com/myrlaphil"
B30 = f"{GH}/circuit-banks/blob/main/PHY%20II%20Electricity%20and%20Magnetism/1_DC%20Circuits/PHY2-DC-SPRTC3-10232026"
B10 = f"{GH}/circuit-banks/blob/main/PHY%20II%20Electricity%20and%20Magnetism/1_DC%20Circuits/PHY2-DC-SPRTC-10222026"
DOCS = f"{GH}/circuit-banks/blob/main/docs"
FORK = f"{GH}/isomorphic-bank-creation-skills/tree/circuit-bank"


def L(text, url):
    return f'<a href="{url}" color="#1F4E79"><u>{text}</u></a>'


def P(t, st=body):
    return Paragraph(t, st)


S = []
S.append(P("The circuit bank — the plain version, with links to the real thing", title))
S.append(P("Myrla Phillippe · October 2026 · every link opens the file on GitHub", small))
S.append(Spacer(1, 6))

# ---- repo links up top
links = [
    ["<b>No-AI version</b> — 30 items, one difficulty, enumerated", L("30-item bank folder", B30), L("circuit-banks repo", f"{GH}/circuit-banks")],
    ["<b>AI version</b> — 10 items, shapes proposed by an LLM (the “before” picture)", L("10-item bank folder", B10), L("circuit-banks repo", f"{GH}/circuit-banks")],
    ["<b>The code, inside Chen's repo</b> (fork, branch <font face='Courier'>circuit-bank</font>; private)", L("fork", FORK), L("the skill folder", f"{FORK}/.cursor/skills/circuit-bank")],
    ["<b>The engine</b> — circuit-diagram-skill (public)", L("circuit-diagram-skill", f"{GH}/circuit-diagram-skill"), L("standalone circuit-bank-skill (private)", f"{GH}/circuit-bank-skill")],
]
t = Table([[P(a, small), P(b, small), P(c, small)] for a, b, c in links], colWidths=[3.6 * inch, 1.6 * inch, 1.8 * inch], hAlign="LEFT")
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9C2B8")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FAF8F5")),
                       ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
S.append(t)

# ---- the problem / his way
S.append(P("The problem", h1))
S.append(P("<i>Distinction: this is the goal both versions share — it is Chen's definition, unchanged.</i>", red))
S.append(P("For a fair exam where every student gets a <i>different</i> question, you need a big pile of questions that are all "
           "“the same kind, same difficulty, but not the same.” Chen calls that an <b>isomorphic bank</b>: same objective, "
           "variation beyond numbers, a changed solution, same difficulty. " + L("Full definition and why it matters", f"{DOCS}/How-the-circuit-bank-works.pdf") + "."))

S.append(P("Chen's way", h1))
S.append(P("<i>Distinction: this is what the method looked like before circuits — two AI agents and a counting loop.</i>", red))
S.append(P("An AI invents variations, another AI judges them, and a loop keeps count until you have enough. Numbers, pictures and "
           "answers were not done yet. Because the AI has no seed, the same input gives different variations each run — the saved "
           "sidecar file is what makes a bank reproducible, not regeneration."))

# ---- your way (no AI)
S.append(P("Your way — the No-AI version (30 items)", h1))
S.append(P("<i>Distinction: Chen's loop is kept and run unchanged; his two AI agents are replaced by code; your circuit skill does every number.</i>", red))
S.append(P("Circuits are special: a computer can draw one, solve one, and tell if two are secretly the same. So:"))
steps = [
    ("1.", "<b>List</b> every possible circuit shape at one difficulty — there are only 34 three-step ones. No guessing.",
     L("why 34, and what changing the box does", f"{DOCS}/why-34.md")),
    ("2.", "<b>Check</b> each with a script: does it solve? is it really new? right number of steps? values sensible?",
     L("what “values sensible” means", f"{DOCS}/speaker-script-2-slides.md") + " · " + L("the four rejection reasons (report §4.4)", f"{DOCS}/How-the-circuit-bank-works.pdf")),
    ("3.", "<b>Solve and draw</b> each one with your circuit skill — exact numbers, a figure, a worked solution.",
     L("circuit-diagram-skill", f"{GH}/circuit-diagram-skill")),
    ("4.", "<b>Make the wrong answers</b> by deliberately making a common student mistake and computing what it gives.",
     L("worked example, q1 (report §2)", f"{DOCS}/How-the-circuit-bank-works.pdf")),
    ("5.", "<b>Package</b> it in Chen's format, plus a PDF with an answer key.",
     L("the whole pipeline as one chart", f"{DOCS}/circuit-bank-flowchart.svg")),
]
for n, txt, link in steps:
    S.append(P(f"{n}&nbsp;&nbsp;{txt}<br/><font size=9 color='#555555'>→ {link}</font>", step))
S.append(P("<b>What you got.</b> 30 questions, all three-step, all different, all correct, no AI anywhere — and running it again gives the exact same 30."))
S.append(KeepTogether([P("<b>The files:</b> " + L("PHY2-DC-SPRTC3-10232026.yaml — the bank and its answer key", f"{B30}/PHY2-DC-SPRTC3-10232026.yaml")
                         + " · " + L("PHY2-DC-SPRTC3-10232026.pdf — worksheet + worked solutions", f"{B30}/PHY2-DC-SPRTC3-10232026.pdf")
                         + " · " + L("figures/", f"{B30}/figures"), body)]))

# ---- the AI version
S.append(P("The AI version — the “before” picture (10 items)", h1))
S.append(P("<i>Distinction: identical to the No-AI version except for step 1 — here an LLM proposed the circuit shapes. Everything after it is the same code.</i>", red))
S.append(P("1.&nbsp;&nbsp;<b>Propose</b>: an LLM writes candidate circuits (Chen's Agent 2, adapted to write circuit lingo). "
           "Different shapes every run; mixed difficulty (2–5 steps) because the difficulty rule did not exist yet.", step))
S.append(P("2–5.&nbsp;&nbsp;The same script critic, the same circuit skill, the same computed distractors, the same packaging.", step))
S.append(P("<b>What you got.</b> 10 correct, distinct, reproducible-from-sidecar items — but not regenerable from the input alone, and not one difficulty. "
           "That is why the 30-item bank replaced the proposer with an enumerator."))
S.append(KeepTogether([P("<b>The files:</b> " + L("PHY2-DC-SPRTC-10222026.yaml", f"{B10}/PHY2-DC-SPRTC-10222026.yaml")
                         + " · " + L("PHY2-DC-SPRTC-10222026.pdf", f"{B10}/PHY2-DC-SPRTC-10222026.pdf")
                         + " · " + L("figures/", f"{B10}/figures"), body)]))

# ---- the forked version
S.append(P("The forked version — how it works inside Chen's repo", h1))
S.append(P("<i>Distinction: nothing of Chen's was edited. The fork's diff is additions only — one skill folder, one bank folder, one README section.</i>", red))
fork_steps = [
    ("1.", "<b>Installed the skill as a sibling of his.</b> <font face='Courier'>.cursor/skills/circuit-bank/</font> sits beside his "
           "<font face='Courier'>.cursor/skills/problem-creation/</font> — the same convention he uses.", L("the skill folder in the fork", f"{FORK}/.cursor/skills/circuit-bank")),
    ("2.", "<b>Called his script in place instead of copying it.</b> The forked scripts resolve "
           "<font face='Courier'>../problem-creation/scripts/scenario_list.py</font>, so the loop that runs is literally his file.", L("his loop script, unchanged", f"{FORK}/.cursor/skills/problem-creation/scripts/scenario_list.py")),
    ("3.", "<b>Pointed at your circuit skill wherever it lives</b> — a sibling folder, <font face='Courier'>~/.claude/skills</font>, "
           "<font face='Courier'>~/.cursor/skills</font>, or <font face='Courier'>CIRCUIT_SKILL=</font>. (The one thing that broke on the first fork run.)", L("circuit-diagram-skill", f"{GH}/circuit-diagram-skill")),
    ("4.", "<b>Used his venv and his folder layout.</b> One <font face='Courier'>.venv</font> at the repo root; the bank under "
           "<font face='Courier'>PHY II Electricity and Magnetism/1_DC Circuits/</font>, next to his <font face='Courier'>PHY I Mechanics/</font>.", L("the bank folder in the fork", f"{FORK}/PHY%20II%20Electricity%20and%20Magnetism/1_DC%20Circuits")),
]
for n, txt, link in fork_steps:
    S.append(P(f"{n}&nbsp;&nbsp;{txt}<br/><font size=9 color='#555555'>→ {link}</font>", step))
S.append(P("<b>The proof it worked as desired:</b> his own <font face='Courier'>validate_input.py</font> accepted the circuit input; his "
           "<font face='Courier'>scenario_list.py</font> ran the loop (target 30 → needed 30 → complete); the 30-item bank came out identical to the "
           "standalone run, because everything downstream of his loop is deterministic."))
S.append(KeepTogether([P("<b>The files (in the fork):</b> " + L("PHY2-DC-SPRTC3-10232026.yaml", f"{FORK}/PHY%20II%20Electricity%20and%20Magnetism/1_DC%20Circuits/PHY2-DC-SPRTC3-10232026/PHY2-DC-SPRTC3-10232026.yaml")
                         + " · " + L("PHY2-DC-SPRTC3-10232026.pdf", f"{FORK}/PHY%20II%20Electricity%20and%20Magnetism/1_DC%20Circuits/PHY2-DC-SPRTC3-10232026/PHY2-DC-SPRTC3-10232026.pdf")
                         + " · " + L("the 10-item bank", f"{FORK}/PHY%20II%20Electricity%20and%20Magnetism/1_DC%20Circuits/PHY2-DC-SPRTC-10222026")
                         + "  (private repo — opens for you)", body)]))

# ---- three sentences
S.append(P("Three sentences to say to anyone", h1))
for q in ["“Same difficulty, different solution, every time — that's what isomorphic means.”",
          "“I kept Chen's loop and swapped the two AI steps for code, because circuits can be counted and checked.”",
          "“Every number in the bank is calculated, including the wrong answers.”"]:
    S.append(P(q, quote))

S.append(Spacer(1, 8))
S.append(P("More: " + L("13-page report", f"{DOCS}/How-the-circuit-bank-works.pdf") + " · " + L("12-slide deck", f"{DOCS}/How-the-circuit-bank-works.pptx")
           + " · " + L("2-slide deck", f"{DOCS}/circuit-bank-2-slides.pptx") + " · " + L("speaker script", f"{DOCS}/speaker-script-2-slides.md")
           + " · " + L("flow chart", f"{DOCS}/circuit-bank-flowchart.svg") + " · " + L("why 34", f"{DOCS}/why-34.md"), small))


def on_page(c, d):
    c.saveState(); c.setFont(FONT, 8); c.setFillColor(MUTED)
    c.drawString(0.85 * inch, 0.5 * inch, "The circuit bank — plain version · github.com/myrlaphil/circuit-banks")
    c.drawRightString(letter[0] - 0.85 * inch, 0.5 * inch, str(d.page)); c.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.7 * inch, bottomMargin=0.8 * inch,
                        title="The circuit bank — plain version", author="Myrla Phillippe")
doc.build(S, onFirstPage=on_page, onLaterPages=on_page)
print(OUT)

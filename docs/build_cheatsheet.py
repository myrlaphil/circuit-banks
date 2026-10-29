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
    ["<b>Rules-only bank</b> — 30 items, one difficulty; every circuit proposed by the enumerator (<font face='Courier'>source: enumerate</font>)", L("30-item bank folder", B30), L("circuit-banks repo", f"{GH}/circuit-banks")],
    ["<b>LLM-proposed bank</b> — 10 items; shapes proposed by the LLM fallback, checked by the critic (<font face='Courier'>source: llm</font>)", L("10-item bank folder", B10), L("circuit-banks repo", f"{GH}/circuit-banks")],
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
S.append(P("Your way — rules first, the LLM only as a tagged fallback", h1))
S.append(P("<i>Distinction: the same principle as your circuit skill's English front door — rules first; the AI only where no rule exists; and when it is used, it says so (every item carries <font face='Courier'>source: enumerate</font> or <font face='Courier'>source: llm</font>). Chen's loop is kept unchanged; his two AI agents become code; your circuit skill does every number.</i>", red))
S.append(P("Circuits are special: a computer can draw one, solve one, and tell if two are secretly the same. So:"))
# ---- the simple run-through, verbatim, in a box
simple = [
    "1.  <b>List</b> every possible circuit shape at one difficulty — there are only 34 three-step ones. No guessing.",
    "2.  <b>Check</b> each with a script: does it solve? is it really new? right number of steps? values sensible?",
    "3.  <b>Solve and draw</b> each one with your circuit skill — exact numbers, a figure, a worked solution.",
    "4.  <b>Make the wrong answers</b> by deliberately making a common student mistake and computing what it gives.",
    "5.  <b>Package</b> it in Chen's format, plus a PDF with an answer key.",
]
boxed = Table([[P("<b>The simple run-through</b>", body)]] + [[P(t, step)] for t in simple], colWidths=[6.8 * inch], hAlign="LEFT")
boxed.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#8A2A1B")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FBF3EF")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
S.append(boxed)
S.append(Spacer(1, 8))
S.append(P("<b>The same five steps, with the details and the links:</b>", body))
steps = [
    ("1.", "<b>List</b> every possible circuit shape at one difficulty — there are only 34 three-step ones. No guessing. "
            "<b>Where the LLM comes in:</b> the list is exhaustive, so if you ask for more than exist the run stops and tells you to widen the box — an LLM cannot invent shapes that do not exist (tested: every fallback proposal came back as a duplicate). "
            "The LLM proposes only for families the enumerator does not cover (capacitors, switches, meters, other unknowns); step 2 checks those like any other, and each is tagged <font face='Courier'>source: llm</font>.",
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
S.append(P("<b>What you got (30-item bank).</b> 30 questions, all three-step, all different, all correct; the rules covered everything, so the fallback never fired — provenance: 30 enumerated, 0 from the LLM — and running it again gives the exact same 30."))
S.append(KeepTogether([P("<b>The files:</b> " + L("PHY2-DC-SPRTC3-10232026.yaml — the bank and its answer key", f"{B30}/PHY2-DC-SPRTC3-10232026.yaml")
                         + " · " + L("PHY2-DC-SPRTC3-10232026.pdf — worksheet + worked solutions", f"{B30}/PHY2-DC-SPRTC3-10232026.pdf")
                         + " · " + L("figures/", f"{B30}/figures"), body)]))

# ---- the AI version
S.append(P("The LLM-proposed bank — what the fallback looks like (10 items)", h1))
S.append(P("<i>Distinction: identical pipeline except step 1 — here the LLM proposed every circuit (it was the only proposer at the time). Everything after it is the same code, and every item is tagged source: llm.</i>", red))
S.append(P("1.&nbsp;&nbsp;<b>Propose</b>: an LLM writes candidate circuits (Chen's Agent 2, adapted to write circuit lingo). "
           "Different shapes every run; mixed difficulty (2–5 steps) because the difficulty rule did not exist yet.", step))
S.append(P("2–5.&nbsp;&nbsp;The same script critic, the same circuit skill, the same computed distractors, the same packaging.", step))
S.append(P("<b>What you got.</b> 10 correct, distinct items, reproducible from their sidecar — but not regenerable from the input alone, and not one difficulty. "
           "That is why the enumerator became the first choice and the LLM the fallback. Provenance: 0 enumerated, 10 from the LLM."))
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
          "“I kept Chen's loop; the rules propose and check the circuits, and the LLM only steps in when the rules run out — and says so.”",
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

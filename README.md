# circuit-banks

Isomorphic DC circuit problem banks produced by the circuit-bank workflow
(circuit-bank-skill + circuit-diagram-skill). Banks only - no tooling.

Each bank folder follows the isomorphic-bank-creation layout (`Subject-Unit-Abbreviation-date`, a bank YAML in
the problem-bank template, a `figures/` folder) so it can sit beside other banks in that format.

| Bank | Items | Contents |
|---|---|---|
| `PHY II Electricity and Magnetism/1_DC Circuits/PHY2-DC-SPRTC-10222026` | 10 multiple choice | mixed difficulty (2-5 reduction steps); bank YAML, `figures/`, printable PDF with answer key, input scheme and scenario sidecar |
| `PHY II Electricity and Magnetism/1_DC Circuits/PHY2-DC-SPRTC3-10232026` | 30 multiple choice | **one difficulty**: every circuit reduces in exactly 3 steps (30 of the 34 possible shapes with 4-6 resistors), enumerated deterministically - no LLM anywhere in this bank |

Every number, figure, worked solution and distractor is computed deterministically. In the 10-item bank an
LLM proposed the circuit topologies (each checked by a script for validity and non-isomorphism); in the
30-item bank even that step is a deterministic enumeration.

## How it works — presentation kit

All in [docs/](docs/):

| File | What it is |
|---|---|
| [How-the-circuit-bank-works.pdf](docs/How-the-circuit-bank-works.pdf) | the full report (13 pages): definition of isomorphic, student fairness, the three pieces, a walk-through, where the AI is and is not, the difficulty ceiling, results, limits; appendix lists all 34 three-step shapes |
| [How-the-circuit-bank-works.pptx](docs/How-the-circuit-bank-works.pptx) | 12-slide deck with speaker notes |
| [circuit-bank-2-slides.pptx](docs/circuit-bank-2-slides.pptx) | 2-slide summary deck |
| [speaker-script-2-slides.md](docs/speaker-script-2-slides.md) | what to say for the 2-slide version, with "check yourself" notes, Q&A and a glossary |
| [circuit-bank-flowchart.svg](docs/circuit-bank-flowchart.svg) | top-to-bottom chart of the forked workflow: what is Chen's, what changed and why |
| [why-34.md](docs/why-34.md) | why a one-difficulty bank has a ceiling (34 shapes at 3 steps) and what changing the box does |

The 30-item bank itself: [YAML](PHY%20II%20Electricity%20and%20Magnetism/1_DC%20Circuits/PHY2-DC-SPRTC3-10232026/PHY2-DC-SPRTC3-10232026.yaml) (the bank and its answer key) and
[PDF](PHY%20II%20Electricity%20and%20Magnetism/1_DC%20Circuits/PHY2-DC-SPRTC3-10232026/PHY2-DC-SPRTC3-10232026.pdf) (worksheet + worked solutions).

`build_report.py`, `build_deck.js`, `build_slides.js` and `build_flowchart.py` regenerate the documents from the banks in this repository.

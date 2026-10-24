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

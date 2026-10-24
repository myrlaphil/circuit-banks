# circuit-banks

Isomorphic DC circuit problem banks produced by the circuit-bank workflow
(circuit-bank-skill + circuit-diagram-skill). Banks only - no tooling.

Each bank folder follows the ESTELA layout and can be loaded in the
[ESTELA Exam Builder](https://zhongzhou.github.io/ESTELA-physics-problem-bank/standalone-enhanced.html)
via "Get Problem Banks" -> repo `myrlaphil/circuit-banks`, branch `main`:

| Bank | Items | Contents |
|---|---|---|
| `PHY II Electricity and Magnetism/1_DC Circuits/PHY2-DC-SPRTC-10222026` | 10 multiple choice | bank YAML, `figures/`, printable PDF with answer key, input scheme and scenario sidecar |

Every number, figure, worked solution and distractor is computed deterministically; the only
LLM step chose the circuit topologies, each checked by a script for validity and non-isomorphism.

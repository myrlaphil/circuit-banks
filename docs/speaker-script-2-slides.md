# Speaker script — the 2-slide version

Spoken, plain language. Each block is what to *say*; the indented notes are what it *means*, so you can check your own understanding first. Timing: about 4 minutes per slide, 8–10 total with a question or two.

---

## Before slide 1 — the one-sentence opener (say this first, standing on the title)

> "I took Zhongzhou's isomorphic-bank method and ran it on DC circuits — and because a circuit is something a computer can draw, solve and compare, I was able to replace the parts of his pipeline that guess with parts that compute. The result is a bank of 30 problems that are all the same difficulty, all different, with every number and every wrong answer calculated, not invented."

> *What this means:* Chen's method uses an AI to propose problem variations and another AI to judge them. For circuits I didn't need either, because the set of possible circuits is finite and each one can be solved exactly. That is the whole story; the two slides are the "why" and the "how".

---

## SLIDE 1 — What "isomorphic" means, and why it's built for the student

### Open with the word

> "Isomorphic is Zhongzhou's word. His definition is: problems that test the same learning objective, with variations that change the *solution* — not only the numbers. His newest paper phrases it as 'the same underlying concepts and solution structures, varying surface features and context'. Spelled out, that's three criteria."

> *Check yourself:* "iso" = same, "morph" = form. Same *form* of problem, different problem. The point is not variety for its own sake — it is that two students can get two different problems that are fair to compare.

### The three cards (left side)

Card 1 — **More than new numbers**

> "The weakest kind of variation is the same circuit with different resistor values. We don't count that. If a student has memorised 'parallel pair, then add the series resistor', new numbers don't test anything — they just re-run the recipe."

> *Why this is true:* Chi, Feltovich and Glaser showed in 1981 that novices sort physics problems by what they look like, experts by what principle solves them. New numbers only change what it looks like.

Card 2 — **A different solution**

> "So at least one step of the solution has to be different. Note what *doesn't* count: redrawing the figure, putting the resistors in a different order, renaming R1 to R2. Those are cosmetic. The solution is identical."

> *Concrete example to have ready:* `3 ‖ 6 + 4` and `6 ‖ 3 + 4` look different on paper and are the same problem. `(2 + 4) ‖ 3 + 1` is a different problem: you have to add first, then combine in parallel, then add.

Card 3 — **Same objective, same difficulty**

> "And the ceiling: it has to stay the same objective at the same difficulty. A 2-step circuit and a 5-step circuit both test series-parallel reduction, but they are not fair substitutes for each other on an exam."

> *Why "steps":* every time you collapse a group of resistors — a series run or a parallel group — into one, that's a step. Cognitive-load theory and the Minnesota difficulty study both tie difficulty to how many things you must hold and do at once; instructor difficulty ratings correlated about 0.84 with the number of equations needed.

### "Why it matters" (the red line)

> "Here's why the definition matters and isn't just taxonomy. These banks exist for one use: every student draws *one* random item from the bank for the same exam slot. If the items only differ by numbers, the draw is pointless — everyone effectively got the same problem. If the items differ in difficulty, the draw is unfair — one student's exam was harder. Isomorphic is exactly the band in between, where a random draw is both meaningful and fair."

> *If someone asks "why random draws at all?":* Chen's reason — it lets the whole bank be public for practice before the exam, allows asynchronous or multiple-attempt exams, and makes memorising answers pointless because there are too many. The bank is only fair if the items are isomorphic.

### The three circuits (right side, top)

> "Three real items from the bank. Same question each time — find the total current. Left: a parallel pair, then a series resistor. Middle: a series pair *inside* a parallel branch, then a series resistor. Right: a three-way parallel, then series. Nobody can solve the middle one by remembering the left one."

> *Have the lingo ready:* `3 ‖ 6 + 4`, `(4 + 2) ‖ 6 + 3`, `2 ‖ 3 ‖ 6 + 4`. The line under each figure is literally the whole source of the item — the figure, the numbers and the solution all come from that one line.

### "Built with the student in mind" (right side, bottom)

Go down the four dots:

> "One difficulty per bank — whoever you are, the item you drew takes the same number of steps as your neighbour's."
> "Every item a new path — you cannot pass by memorising last year's problem."
> "Wrong answers are real mistakes — each distractor is the number you get by making one specific error, not a random nearby value. I'll show that on the next slide."
> "One drawing style, clean arithmetic — the only thing that varies between items is the physics."

> *Check yourself on "clean arithmetic":* every intermediate resistance comes out a whole or half ohm and the answer has at most two decimals, so a student is never stuck on ugly fractions — the difficulty is in the reduction, not the arithmetic.

**Transition:** "So that's what we were trying to build. Here's how the code guarantees it."

---

## SLIDE 2 — How the code works: every number computed, none guessed

### The pipeline (top row) — walk left to right, pointing at the colours

> "Colour tells you whose work each stage is. Blue is Zhongzhou's, run unchanged. Copper is new glue I wrote. Green is my circuit engine."

1. **Input scheme** (blue)
   > "Everything starts from Zhongzhou's input file. I added a few lines to it: the bank id, the resistor and voltage ranges, and the difficulty — 'every circuit reduces in exactly three steps'. The number of items lives in this file, not in a chat message. That's one of his rules I kept."

2. **Chen's loop** (blue)
   > "His scenario script runs exactly as he wrote it. It keeps a 'sidecar' file: the target count, how many passes have run, and the list of accepted and rejected candidates with the reason for each rejection. That file is the source of truth — the whole bank regenerates from it."

   > *If asked "what's a sidecar?":* just a second file that sits beside the input and records the state of the loop. His word.

3. **Enumerate** (copper) — *this is the key substitution*
   > "In Zhongzhou's pipeline an AI proposes the variations. For circuits I don't need to guess, because a series-parallel circuit is a tree, and you can list every tree. With four to six resistors and exactly three reduction steps there are exactly 34 distinct shapes. So the proposer simply lists them, then assigns resistor values from a small pool using a seed, keeping only combinations where the arithmetic is clean and no two answers repeat."

   > *Check yourself on "shape":* a shape is the circuit with the numbers removed — 'a parallel pair, then series'. Two circuits with the same shape are the same problem. 34 is the count of such shapes at 3 steps with 4–6 resistors; it is a count, not a setting. **See [why-34.md](why-34.md)** for the table of what the count becomes if you allow more resistors or a band of steps, and the trade-off that goes with it.

   > *Check yourself on "seed":* a fixed starting value for the random number generator. Same seed, same choices — so the bank is reproducible.

4. **Critic** (copper) — *the second substitution*
   > "His critic is an AI judging prose. Mine is a script, because a circuit can be checked: does it parse and solve? Is its shape new, or is it a reorder of one we already have? Does it have exactly three steps? Are the values in range? Each failure is written back into Zhongzhou's sidecar as a reason, exactly where his AI critic would have written one."

   > *What "values in range / sensible" means — two different checks, both automatic:*
   > - **The critic's range check** — every resistor must be within `resistor_range` (1–24 Ω), the battery within `voltage_range` (6–36 V), and the resistor count within 4–6. A 50 Ω resistor or a 48 V battery gets rejected, with that reason written to the sidecar.
   > - **The enumerator's "clean arithmetic" rule** — when it picks values, it only accepts a set where every intermediate resistance comes out a whole or half ohm and the answer has at most two decimals, so no student is fighting ugly fractions. (Values come from a pool of 1–12 Ω.)
   > The first is a *rule you set* in the input file; the second is *built into the proposer*. Both are code, not judgement.

   > *If asked "then why keep the critic at all, if the enumerator never proposes duplicates?":* because the input also allows an AI proposer (one line: `generator: llm`), and because the critic is the guarantee — it doesn't matter who wrote the candidate.

5. **Circuit engine** (green)
   > "Every accepted item goes through my circuit skill: it parses the one-line description, solves the circuit step by step, draws the figure, and writes the worked solution. Same text in, same output out — no AI."

6. **Bank + PDF** (copper)
   > "Then the wrong answers are computed, and everything is written in Zhongzhou's bank format, plus a printable PDF with an answer key."

### The four numbers (middle row)

> "34 — the number of three-step shapes that exist. 30 — the bank uses 30 of them. 0 — rejections; the enumerator never proposes a bad one, so the critic kept all 30 in a single pass, and there is no AI anywhere in this bank. And 'equals' — same input and seed give the same bank, byte for byte."

### One item, four computed options (bottom left)

> "Here is why the wrong answers matter. Twelve volts, 3 ohm and 6 ohm in parallel, then 4 ohm. The right answer is 2 amps. The three wrong options aren't random: 0.92 A is what you get if you add all three resistors as if they were in series. 2.67 A is the classic mistake — you add the reciprocals of the parallel pair and forget to flip the sum back. 1.33 A is the current through just one branch, reported as the total. Each wrong option names a misconception, and the answer key records which."

> *Work the arithmetic once so you can do it live:*
> 3 ‖ 6 → 1/3 + 1/6 = 1/2 → 2 Ω. Plus 4 → 6 Ω. 12 V / 6 Ω = **2 A**.
> Wrong 1: 12 / (3+6+4) = 12/13 = 0.92 A. Wrong 2: "R = 1/3 + 1/6 = 0.5 Ω" then + 4 = 4.5 Ω → 12/4.5 = 2.67 A. Wrong 3: branch R1 has 4 V across the pair (2 A × 2 Ω) → 4/3 = 1.33 A.

### What the critic rejects (bottom right)

> "And these are the four reasons, in the words the script actually writes to the file: it doesn't parse; it's the same canonical shape as one we have — the reorder example; a value is out of range; or it's the wrong difficulty — 'five reduction steps, this bank wants three'."

### Close

> "So: Zhongzhou's loop, unchanged. Two of his agents replaced because circuits can be enumerated and verified rather than imagined and judged. A deterministic engine for every number, figure and solution. Thirty items, one difficulty, no AI anywhere in the final bank — and it regenerates from one file."

---

## Questions you may get, and short answers

**"Isn't this just a parameterised question generator?"**
No. A parameterised generator varies the numbers in one fixed solution. Here the numbers are almost incidental; what varies is the solution path, and the critic rejects anything that is only a renumbering.

**"Why not let the AI propose and just filter?"**
We did that first (the 10-item bank). It works, but at one fixed difficulty there are only 34 possible shapes, and an AI guessing shapes won't find 30 of 34 inside Zhongzhou's five-pass limit. Enumeration lists all 34 and is reproducible. The AI proposer is still there as an option.

**"How do you know the difficulty is really the same?"**
By construction, every item has exactly three reduction steps — that's a design guarantee Zhongzhou's method doesn't have. But it isn't validated by students yet. His group validates with student data: item-accuracy spread plus an extended Fisher's exact test; 15 of their 20 deployed banks came out homogeneous. Ours should be checked the same way after deployment.

**"Where's the AI, then?"**
Same policy as the circuit skill's English front door: rules first, the LLM only when the rules cannot, and it says so. The enumerator proposes; it is exhaustive, so if you ask for more than the band holds the run stops and says 'widen the band' — an LLM cannot invent shapes that do not exist (we tested: every fallback proposal was a duplicate). The LLM proposes only for families the enumerator does not cover; the critic checks those like any other, and each one is tagged `source: llm` in the sidecar and the bank. In the 30-item bank the rules covered everything (provenance: 30 enumerated, 0 LLM). In the 10-item bank the LLM proposed all ten. Never in a number, a figure, a solution or a distractor.

**"How is this different from what Zhongzhou's paper does?"**
His variation is mostly *contextual* — same solution structure, different story (traveler and backpack vs dog and sled). Mine is entirely *structural* — no story at all, different reduction path, held to one difficulty. Same definition, opposite end of it. Adding context on top is a wording layer and would be cheap.

**"Can it go into Canvas?"**
The bank is in his YAML format, which is what Canvas import is built from, but the QTI export step itself isn't done — his group uses an external converter for that.

---

## Glossary (for yourself)

- **Isomorphic**: same objective, variation beyond numbers, a changed solution, same difficulty.
- **Lingo**: the one-line circuit description, e.g. `(4 + 2) ‖ 6 + 3`. `+` series, `‖` parallel.
- **Shape / canonical shape**: the circuit with numbers removed and sibling order ignored. Same shape = same problem.
- **Reduction step**: collapsing one series run or one parallel group into a single resistor. The bank's difficulty = number of steps.
- **Sidecar**: Chen's state file — target, pass count, accepted / rejected with reasons. The bank regenerates from it.
- **Enumerator**: lists every shape in the difficulty band and assigns values by seed. Replaces the AI proposer.
- **Critic**: the script that parses, solves, canonicalises, counts steps and checks ranges. Replaces the AI critic.
- **Distractor**: a wrong multiple-choice option. Here, each is the result of one named mistake.
- **Seed**: fixed random starting point → the same choices every run.

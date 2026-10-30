# Why 34? — the ceiling on a one-difficulty bank

**34 is not a setting — it's a count.** It is how many distinct series-parallel circuit *shapes* exist with
**4 to 6 resistors** that reduce in **exactly 3 steps**. That number is a fact of combinatorics, like
"there are 4 suits in a deck."

A *shape* is a circuit with the numbers removed and the order of parts ignored: "a parallel pair, then a
series resistor" is one shape, whatever the values. Two circuits with the same shape are the same problem.
A *step* is collapsing one series run or one parallel group into a single resistor; the bank's difficulty
is the number of steps.

What *is* a setting is the box you count inside. Change the box, change the count (computed with
`enumerate_lingo.py --list`):

| Resistors allowed | Steps | Shapes available |
|---|---|---|
| 4–6 | exactly 3 | 34 |
| **5–6** | **exactly 3** | **30** ← the 30-item bank uses every one |
| 4–6 | exactly 2 | 18 |
| 4–6 | exactly 4 | 30 |
| 4–6 | 3 or 4 | 64 |
| 3–6 | exactly 3 | 34 (a 3-resistor circuit cannot take 3 steps) |
| 4–7 | exactly 3 | 66 |
| 4–7 | exactly 4 | 88 |
| 4–8 | exactly 3 | 114 |

The knobs live in the input file, `other (optional)`:

```yaml
min_resistors: 4
max_resistors: 6
reduction_steps: 3        # or [3, 4] for a band
```

So the ceiling can be raised — but notice the trade:

- **More resistors** → more shapes, but busier circuits, and the "same difficulty" claim gets softer: a
  7-resistor, 3-step circuit is more work than a 4-resistor one even at the same step count.
- **A band of steps** (3 or 4) → nearly doubles the pool, but now items differ in difficulty by one step —
  exactly what the one-difficulty rule was meant to avoid.

The bank uses the 5–6 resistor box: exactly 30 shapes at 3 steps, so both the structural difficulty (3 steps) and the arithmetic load (5–6 resistors) sit in a narrow band. Wanting 50
items at that difficulty is not a matter of trying harder — the shapes do not exist. Either widen the box
(and say so on the slide) or make a second bank at the next difficulty.

For reference, the total number of series-parallel shapes with *n* resistors, all step counts together, is
2, 4, 10, 24, 66 for n = 2…6 — the classic series-parallel network sequence.

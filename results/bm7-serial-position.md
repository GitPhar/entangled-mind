# Biomimetic (rev. 2 §3.5): serial-position weights from the archived O1–O4 chains

Pre-registered in `experiments/bm7-serial-position.md` (D41), committed before the archive was opened for this analysis. Anchor (a) only; 800 conversations, 40 items; item fixed effects; $0.

## In plain English

**The question.** When the model rates four of its own claims in a row and then answers the main question, which claim counts most: the first, the last, or the ones in between? A competing-accumulator account (the LCA) allows first-heavy, last-heavy or flat weighting, but never a U-shape where the first and last both count more than the middle.

**What we found.**
- **No U-shape**, so the LCA survives this test.
- **The weights are small.** Each position moves the final verdict by only 2–4 points per 50 points of the model's own sub-rating (4–9 points across its full range). Within a question, the verdict barely tracks the sub-ratings the model just gave.
- **No reliable slope with position.** The weights drift slightly downward, a faint first-heavy pattern (+2.3 [−1.6, +7.3]). That is the opposite of the last-heavy pattern experiment 5's fitted belief-adjustment model implies, but it is not reliable.

**What it means.** The shape of the weighting doesn't discriminate between accounts here. The notable result is how weakly the verdict depends on the model's own stated sub-ratings.

## Weight of each position on the final main rating

Evidence x = sign(lean) · (rating − 50)/50; weights in rating points per unit of evidence; 95% item-cluster bootstrap CIs.

| position | weight | BA5-implied weight (relative to position 4) |
|---|---|---|
| 1 | +4.3 [+0.1, +9.8] | 0.68 |
| 2 | +4.0 [+0.9, +7.8] | 0.77 |
| 3 | +3.2 [+0.4, +7.0] | 0.88 |
| 4 | +2.0 [-0.4, +4.8] | 1.00 |

- **U-shape contrasts:** u₁ = w₁ − (w₂ + w₃)/2 = +0.7 [-2.3, +4.3]; u₄ = w₄ − (w₂ + w₃)/2 = -1.6 [-4.7, +1.1].
- w₁ − w₄ = +2.3 [-1.6, +7.3]; linear trend over positions -0.77 [-2.35, +0.51] points per position.

## Pre-registered reading: **monotone or flat (flat): consistent with the LCA**

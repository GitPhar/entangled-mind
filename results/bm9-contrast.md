# Biomimetic (rev. 1 §3.9): contrast or assimilation on the single-scale QQ conversations

Pre-registered in `experiments/bm9-contrast.md` (D42), committed before the archive was opened for this analysis. Anchor (a) only; $0.

## In plain English

**The question.** When the model rates a sub-question and then the main question, does the main rating move toward the number it just gave (assimilation) or away from it (contrast)? The logical push of the claim's content is held fixed.

**What we found.** Assimilation.
- **Toward the number.** For every point by which the sub-question rating sits above the model's unprompted main rating, the main rating moves about a quarter-point toward it: +0.27 [+0.11, +0.43]. That is on top of the content's own push, +7.7 points.
- **Replication.** The single-scale run 2 gives the same figure, +0.27 [+0.05, +0.58].
- **Within the same question,** conversations where the model happened to rate the sub-question higher also tend to give a main rating that follows it in the content's direction (correlation +0.17 and +0.34).

**What it means.** The model's next judgment is pulled toward the number it just produced, beyond what the claim's content implies. That is the self-anchoring direction 2 found with planted numbers, now seen in unedited conversations. No contrast appears, so the reactance seen toward *another person's* numbers in run 3 does not extend to the model's own numbers. As revision 2 of the map notes, this does not test divisive normalization.

## d_M = α + β·L + γ·C across (item, claim) pairs

d_M: M after S minus M first; L: S level minus M-first level; C: yes-ward content push of the S rating. Secondary: within-pair correlation of S and the following M, signed by the claim's lean (positive = M follows S the way content implies). 95% item-cluster bootstrap CIs.

| set | pairs | β (level) | γ (content) | signed within-pair corr (pairs with variance) | reading |
|---|---|---|---|---|---|
| run 1, anchor (a), 40 items | 80 | +0.268 [+0.109, +0.427] | +7.7 [+0.8, +16.0] | +0.17 [+0.05, +0.29] (76) | assimilation |
| run 2, anchor (a), 10 items (replication) | 20 | +0.274 [+0.046, +0.584] | +7.7 [-8.4, +31.8] | +0.34 [+0.09, +0.56] (20) | assimilation |

## Pre-registered reading (primary set): **assimilation**

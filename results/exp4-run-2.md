# Experiment 4, run 2: graded order test

Pre-registration: `experiments/exp4-yearsley-trueblood.md`, Addendum — run 2 (DEVIATIONS.md, D17). Base model `claude-haiku-5-5`, thinking disabled, default temperature (1.0). 7 fallacy items from run 1, 4 two-turn cells × 20 repeats each, 1120 calls, **$0.04**.

Every order-effect number has the marginal-shift check beside it: OE_X and OE_Y are each conjunct's mean rating when rated second minus when rated first, and OSS = |OE_X| + |OE_Y|.

| item | P(X) | P(Y) | P(X∧Y) after X | P(X∧Y) after Y | o | f | o − o_rep (beyond anchoring) | anchor r | OE_X | OE_Y | OSS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| co01 | 0.85 | 0.05 | 0.05 | 0.03 | +0.023 [+0.021, +0.025] | -0.001 [-0.004, +0.000] | +0.000 [-0.000, +0.000] | 0.03 | +0.000 | +0.006 | 0.006 |
| co-lin06 | 0.85 | 0.07 | 0.16 | 0.04 | +0.118 [+0.103, +0.132] | +0.094 [+0.079, +0.108] | -0.002 [-0.005, +0.002] | 0.15 | -0.118 | +0.007 | 0.125 |
| co-lin08 | 0.56 | 0.04 | 0.02 | 0.03 | -0.005 [-0.009, -0.002] | -0.022 [-0.026, -0.018] | -0.005 [-0.009, -0.002] | 0.00 | +0.071 | -0.013 | 0.084 |
| co-lin09 | 0.70 | 0.44 | 0.40 | 0.32 | +0.080 [+0.053, +0.105] | -0.042 [-0.070, -0.016] | -0.009 [-0.018, +0.002] | 0.34 | -0.122 | -0.010 | 0.132 |
| co-lin10 | 0.85 | 0.04 | 0.13 | 0.03 | +0.103 [+0.093, +0.112] | +0.087 [+0.077, +0.096] | -0.000 [-0.000, +0.000] | 0.13 | -0.080 | +0.015 | 0.095 |
| co05 | 0.48 | 0.04 | 0.08 | 0.01 | +0.069 [+0.067, +0.072] | +0.041 [+0.038, +0.044] | +0.002 [-0.002, +0.005] | 0.15 | -0.230 | +0.024 | 0.255 |
| co06 | 0.47 | 0.10 | 0.08 | 0.04 | +0.039 [+0.033, +0.045] | -0.018 [-0.026, -0.011] | +0.001 [-0.001, +0.003] | 0.10 | +0.030 | -0.001 | 0.031 |

## Pre-registered rules

- Scored items (graded fallacy f reliably > 0): **3** of 7.
- R2, o ≥ f − 0.05: 3 of 3. Order effect beyond anchoring reliably > 0: 0 of 3.
- Static twin (o − o_rep interval contains 0): 3 of 3.

**Verdict: static classical twin (with anchoring) supported.**

## Reading

- **Graded ratings show order effects on the conjunction, which run 1's saturated binary joint could not show.** Rating the representative conjunct first raises the later conjunction rating. o is reliably positive on 6 of the 7 items, at about +0.10 for Bill (co-lin06), Marta (co-lin10) and co05. The marginal-shift check shows the representative conjunct is itself rated lower when rated second (OE_X = −0.12, −0.08, −0.23).
- **R2 holds where it applies.** On the 3 items with a reliable graded fallacy, o ≥ f − 0.05 in all 3. So the order effect is at least as large as the fallacy, as the quantum model (and a sequential-update classical model) requires.
- **The pre-registered verdict is "static twin with anchoring supported", but that rests on a flawed estimator (DEVIATIONS.md, D19).** The anchoring term was pre-registered as a regression of the second rating on the first across *both* cells pooled. The two cells differ mainly in their means (the high P(X) is rated first in one, the low P(Y) in the other). The fitted slope is therefore close to o / (P(X) − P(Y)), and o − o_rep ≈ 0 almost by construction, which is what the table shows on every item. The verdict stands as pre-registered, but it does not show that anchoring explains the effect.
- **The proper test is not possible on these data.** That test is within-cell anchoring, using repeat-to-repeat variation only. At the default temperature, the ratings barely vary across repeats: the standard deviation is 0.00–0.05 on the 0–1 scale, and exactly 0 in some cells. The within-cell slopes (`results/exp4-run-2-anchoring-diagnostic.json`, exploratory) range from 0.0 to 0.63 and cannot be estimated reliably.
- **Net:** the order effects are real and satisfy R2, but this design cannot tell a quantum account from simple anchoring on the first answer. A discriminating test needs a manipulation that moves the first rating independently of the item, for example a provided first rating to accept or revise.

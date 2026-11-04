# Second base model: claude-sonnet-5-5 (offline scoring of the hard pool)

Sonnet's own answers to the hard pool (pool run 4, `h101` excluded after a refusal, DEVIATIONS.md D21) were scored offline. Each item's archived claims and relation table go through the **already-fitted** v2 models, with frozen parameters from `results/v2-fit.json`. Nothing is refitted, and **no API call was made** during scoring (the client is blocked in code). The training-pool run stopped on a second refusal (D25), so only the hard pool is scored here. Arm G comes from 298 separate self-confidence calls to Sonnet, $0.88, with no refusal (D28).

Sonnet answered 298 items and got **30 wrong** (claim 0/60, science 18/120, simpleqa 12/118).

| model | Sonnet, hard pool (all 298) | Haiku, run-2 held-out (80), for reference |
|---|---|---|
| A2 learned quantum encoding | 0.90 [0.84, 0.95] | 0.82 [0.71, 0.91] |
| F2 learned classical twin | 0.82 [0.75, 0.88] | 0.71 [0.59, 0.82] |
| L relation-web features | 0.73 [0.64, 0.82] | 0.66 [0.53, 0.77] |
| H hedge baseline | 0.66 [0.56, 0.76] | 0.77 [0.66, 0.87] |
| G self-reported confidence | 0.91 [0.86, 0.95] | 0.82 [0.71, 0.90] |

Paired bootstrap on Sonnet's items: A2 − F2 = +0.078 [+0.018, +0.137]; L − H = +0.074 [-0.041, +0.205]; G − A2 = +0.008 [-0.061, +0.080]; G − L = +0.176 [+0.095, +0.257].

The two sets differ in composition: Sonnet's set is the whole hard pool, with 30 wrong of 298, while Haiku's held-out set is 40 wrong and 40 right. AUROC does not depend on that balance, but the intervals do.

## Reading

- **The frozen models transfer to a second base model's answers on the same hard-pool questions.** A2's edge over F2 is concentrated in the questions Haiku also got wrong (21 of Sonnet's 30 errors are in Haiku's run-2 held-out set; A2 − F2 is +0.21 there and −0.02 [−0.13, +0.06] on the other 220 questions), so it is not independent of Haiku's held-out edge. A2, F2 and L all score well above chance on Sonnet's hard-pool errors, in the same order as on Haiku's run-2 held-out set (A2 > F2 > L). The hedge baseline H is weaker on Sonnet (0.66 vs 0.77).
- **Self-report is again not detectably different from the best structural model.** Sonnet's own stated confidence, G, scores **0.91** [0.86, 0.95], level with A2 (G − A2 = +0.008 [−0.061, +0.080]). It beats the relation-web feature model L by +0.176 [+0.095, +0.257]. This is the same finding as on Haiku: nothing built from the deliberation structure detectably beats the model's self-report.
- **A2's edge over F2 (+0.078 [+0.018, +0.137]) is explained by the Addendum D ablation** (`results/sonnet-ablation.md`). It is single-claim readout geometry, and a classical twin carries it. Setting A2's couplings to exactly 0 changes nothing detectable, and F2 given A2's per-claim tilted-readout marginal (F2+) is not detectably different from A2. The edge is not entanglement and not quantum. The same holds on Haiku's run-2 held-out set (Addendum E): the frozen F2+ is not detectably different from A2 (−0.019 [−0.073, +0.029]) or A2.1 (−0.037 [−0.089, +0.012]). Each positive quantum-vs-classical difference tested (all on the same hard-pool questions) is statistically indistinguishable from F2+, which recovers the whole Sonnet edge and roughly two thirds (95% CI one fifth to all) of Haiku's held-out A2.1 edge.

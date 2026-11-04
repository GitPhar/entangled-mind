# Second base model: claude-sonnet-5-5 (offline scoring of the hard pool)

Sonnet's own answers to the hard pool (pool run 4, `h101` excluded after a refusal, DEVIATIONS.md D21) were scored offline. Each item's archived claims and relation table go through the **already-fitted** v2 models, with frozen parameters from `results/v2-fit.json`. Nothing is refitted, and **no API call was made** (the client is blocked in code). The training-pool run stopped on a second refusal (D25), so only the hard pool is scored here.

Sonnet answered 298 items and got **30 wrong** (claim 0/60, science 18/120, simpleqa 12/118).

| model | Sonnet, hard pool (all 298) | Haiku, run-2 held-out (80), for reference |
|---|---|---|
| A2 learned quantum encoding | 0.90 [0.84, 0.95] | 0.82 [0.71, 0.91] |
| F2 learned classical twin | 0.82 [0.75, 0.88] | 0.71 [0.59, 0.82] |
| L relation-web features | 0.73 [0.64, 0.82] | 0.66 [0.53, 0.77] |
| H hedge baseline | 0.66 [0.56, 0.76] | 0.77 [0.66, 0.87] |
| G self-reported confidence | **not scored** (needs Sonnet calls; halted, D25) | 0.82 [0.71, 0.90] |

Paired bootstrap on Sonnet's items: A2 − F2 = +0.078 [+0.018, +0.137]; L − H = +0.074 [-0.041, +0.205].

The two sets differ in composition: Sonnet's set is the whole hard pool, with 30 wrong of 298, while Haiku's held-out set is 40 wrong and 40 right. AUROC does not depend on that balance, but the intervals do.

## Reading

- **The error-prediction pattern largely replicates on a second base model.** The deliberation-structure models trained on Haiku's errors transfer to Sonnet's. A2, F2 and L all score well above chance on Sonnet's hard-pool errors, in the same order as on Haiku's run-2 held-out set (A2 > F2 > L). The hedge baseline H is weaker on Sonnet (0.66 vs 0.77).
- **A2 beats F2 on Sonnet's errors**, by +0.078 [+0.018, +0.137] (paired). This matches the direction of the secondary held-out results for Haiku (v2: +0.108; v2.1: +0.116). It is still a secondary comparison. On v2's primary test, the locked test set from the training-pool distribution, A2 and F2 tied (−0.007 [−0.079, +0.062]).
- **That edge is not entanglement.** A2's fitted couplings are near zero (k_sup = 0.12, k_con = 0.21, against 1 in v1), with one weak Trotter step. Its advantage over F2 comes from the learned single-claim geometry and the tilted readout basis (α = 0.40), which a classical model given the same readout freedom could in principle match. The robust part of the finding is that A2's parameterisation transfers across pools and base models better than F2's. It does not show that superposition or entanglement carry the error signal.
- **G, the base model's self-reported confidence, could not be scored on Sonnet** without new calls, and the replication was halted (D25). Whether self-report again matches the structural models on Sonnet's errors is therefore open.

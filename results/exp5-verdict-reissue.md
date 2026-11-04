# Experiment 5, run 1: verdict re-issued on the single-direction QQ statistic

DEVIATIONS.md D52. The frozen §7.3 and §7.5 rules of `experiments/exp5-sequential-judgment.md`, applied by the frozen code (`exp5_analyse.qq_check` and its verdict precedence) to run 1's anchor-(a) conversations: 0 = certainly false, 100 = certainly true. Nothing refitted; no API calls.

## In plain English

(Hand-written; excluded from reproduce.py's comparison.)

Experiment 5's verdict was first issued as a **tie**: the quantum model and its classical twin could not be told apart, and the quantum order-effect signature (the QQ equality) was neither present nor contradicted. That last part used a statistic averaged over two scale directions. In one direction the statistic is clearly negative; in the other it is clearly positive, so the average sat near zero. Run 2 had already called that average an artefact.

On the one scale direction the project uses everywhere else (0 = certainly false, 100 = certainly true), the statistic is −0.345 [−0.517, −0.181], well away from zero. The pre-registered rule calls that a contradicted signature, and a contradicted signature with a primary that is not a pass makes the verdict **classical**. Re-running the project's own frozen code on the same conversations gives the same answer (−0.339 [−0.510, −0.168]).

What changes is the label, not the conclusion: no quantum advantage and no quantum signature, in either reading. Using the single-direction subset is a choice made after the data, prompted by run 2 and the audit, so the original tie is kept in `results/exp5-run-1.md`, marked superseded.

## Inputs (§7.5)

- Primary (§7.2), unchanged: **TIE**, F5 − A5 = +67.0 [-34.1, +211.5] rating points².
- Kvam (§7.4), unchanged: signature present **False**, commitment **False**.

## QQ mean q on the large-order-effect pairs (§7.3)

| data | pairs with OE > 0.10, CI excluding 0 | mean q [95% CI] | contradicted (CI excludes 0) |
|---|---|---|---|
| both directions pooled (as issued) | 60 | +0.005 [-0.058, +0.065] | False |
| **anchor (a) only, the audit's recomputation (verdict basis)** | 32 | **-0.345 [-0.517, -0.181]** | **True** |
| anchor (a) only, frozen `qq_check` | 33 | -0.339 [-0.510, -0.168] | True |
| anchor (b) only, frozen `qq_check` (reported, not used) | 47 | +0.241 [+0.118, +0.370] | True |

## Verdict (§7.5)

- As issued on the pooled q (superseded): **TIE**.
- Re-issued on the single-direction q: **CLASSICAL** (the frozen-code recomputation gives **CLASSICAL**).
- Rule: "classical: primary classical, or a signature contradicted with the primary not a pass". The primary is a tie, not a pass, and the QQ signature is contradicted.

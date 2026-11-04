# Direction 3: six elicitation formats on the 160 chain claims

Pre-registered in `experiments/gm3b-format-invariance.md` (D38), committed before any call. `claude-haiku-5-5`, thinking disabled; one scale direction throughout. 9600 calls, **$0.41** of the $1 cap; no refusal.

## In plain English

**The question.** Does the model hold one degree of belief in a statement, which different ways of asking all read out, each with its own fixed distortion? We asked about the same 160 statements in six ways, ten times each:
- a 0–100 rating;
- yes/no;
- whether to buy a $100 ticket at a price;
- whether the statement is likelier than a coin landing heads;
- how many of 100 such statements would be true;
- a 7-point verbal scale.

All six use one scale direction. We then compared two descriptions:
- one belief per statement, read through a separate monotone "lens" for each format;
- a separate belief per statement for each format.

Each was scored on repeats it had not been fitted on.

**What we found.** There is no single belief to read out.
- **The separate-belief model predicts held-out answers far better** on 86% of the statements, by a wide margin: +19.4 log-likelihood units per statement [+16.5, +22.1].
- Taking any two formats, the order in which they rank the statements agrees only moderately (rank correlations 0.37–0.74). Overall agreement across all six is W = 0.56.
- **The rating and the other formats often order the same two statements differently.** For 12–25% of statement pairs (20–30% of the pairs both formats separate), the 0–100 rating and another format put them in opposite orders.
- **No fixed distortion explains that.** No one-to-one mapping can turn one ordering into another. "Statement A is likelier than B" in one format becomes "B is likelier than A" in another.
- **The coin comparison** is the most out of line: the model picks the statement over the coin 79% of the time, when its average 0–100 rating is 55.

**What it means.** On these statements, no single credence reproduces Haiku's answers in all six formats. This is the gold map's overturning direction, which it had put at 0.25 after Smolin & Wilder (2026), who found single beliefs fit other capable models well.

Two things could explain the difference:
- **The material.** Their statements were standalone cases. Ours are the model's own contested claims about hard questions, where it may simply have no settled view.
- **The model.** Claude was not among the models they tested.

**Noise baseline (computed after the run, not pre-registered).** Is the reordering more than repeat noise? Compare one half of a format's repeats with the other half of the same format: they put only 1–5% of statement pairs in opposite orders. Compare the 0–100 rating's even repeats with another format's odd repeats, the same amount of data, and the figure is 11–25%. The cross-format reordering is about five to ten times the noise. (An earlier version reported 4–8% and 21–35%; those are the (1 − τ_b)/2 index, not shares of pairs.)

**Caveats.**
- **Two different criteria.** The test compares on held-out *repeats*. Smolin & Wilder judged usefulness on held-out *framings*. Haiku's repeats vary little, so any reproducible statement-by-format deviation favours the separate-belief model, even if one belief would still predict a new format reasonably well. "No single credence" holds by the pre-registered rule. It does not show that a single latent is useless, and it does not contradict Smolin & Wilder. A like-for-like follow-up would predict each left-out format from the other five. That would need its own pre-registration. (Point raised by the literature session.)
- One model (Haiku), one context per statement.
- **The per-format table below comes from an under-converged L1 fit** (its objective is at least 9.5 below the optimum, per the audit), so the by-format ΔLL and slopes depend on the optimiser. The headline survives an independent refit (+19.6 [+16.1, +22.9], 87% of claims).
- Some formats, such as the coin comparison, may carry their own response biases. The per-format link absorbs any bias that is monotone, so a monotone bias is not the explanation. The ranking disagreements are.

## One credence (L1) against one credence per format (L6), held-out repeats

ΔLL = held-out log-likelihood of L6 minus L1, per claim, summed over 2 folds (even/odd repeats) and six formats. Positive favours format-specific credences.

- **Mean ΔLL per claim: +19.36 [+16.50, +22.08]** (item-bootstrap 95% CI).
- **Claims with ΔLL > 0: 86%** of 160.
- Total held-out LL: L1 -10438.3, L6 -7341.4.

| format | mean ΔLL per claim | L1 slope b_f (fold 0) |
|---|---|---|
| F1 rating 0-100 | +3.745 | 1.00 |
| F2 yes/no | +2.015 | 1.28 |
| F3 bet | +2.326 | 0.56 |
| F4 pairwise vs coin | +1.669 | 0.55 |
| F5 frequency /100 | +6.094 | 0.94 |
| F6 verbal 7-point | +3.506 | 3.23 |

## Agreement between formats (per-claim mean responses)

- Kendall's W across the six formats: **0.56**.

| pair | Spearman ρ |
|---|---|
| rating 0-100 – yes/no | +0.62 |
| rating 0-100 – bet | +0.59 |
| rating 0-100 – pairwise vs coin | +0.42 |
| rating 0-100 – frequency /100 | +0.62 |
| rating 0-100 – verbal 7-point | +0.74 |
| yes/no – bet | +0.62 |
| yes/no – pairwise vs coin | +0.42 |
| yes/no – frequency /100 | +0.42 |
| yes/no – verbal 7-point | +0.64 |
| bet – pairwise vs coin | +0.47 |
| bet – frequency /100 | +0.57 |
| bet – verbal 7-point | +0.66 |
| pairwise vs coin – frequency /100 | +0.37 |
| pairwise vs coin – verbal 7-point | +0.49 |
| frequency /100 – verbal 7-point | +0.52 |

| format | (1 − τ_b)/2 against the 0–100 rating (a discordance index, not a share of pairs) |
|---|---|
| yes/no | 26% |
| bet | 27% |
| pairwise vs coin | 34% |
| frequency /100 | 27% |
| verbal 7-point | 20% |

## Pre-registered reading: **no single credence: formats disagree beyond monotone links**

# Experiment 4, run 3: a manipulated first rating (pre-registration draft)

Written 2026-11-03, after run 2 (`results/exp4-run-2.md`, DEVIATIONS D19) and before any run-3 call. **Status: FROZEN 2026-11-03 22:59 MST with the amendment below, before any run-3 call (Sean's go-ahead; $2 cap).**

## 1. Why run 3

**What run 2 found.**
- Run 2 found real graded order effects, of about +0.10 on Bill (co-lin06), Marta (co-lin10) and co05.
- It met R2 on all 3 scored items.
- It could not say *why* the order effects occur. The pre-registered anchoring estimator regressed the second rating on the first across the X-first and Y-first cells pooled. Those cells differ mainly in their first-rating means, so the slope is about o / (P(X) − P(Y)), and o − o_rep ≈ 0 by construction (D19).
- A within-cell estimate was not possible either, because ratings barely vary between repeats (SD 0.00–0.05 on the 0–1 scale).

**The circularity runs deeper than the estimator.** Write r₁ for the first rating and r₂ for the conjunction rating that follows it.
- In a quantum model with **rank-one (non-degenerate) projectors** for X and Y, judging X first leaves the state on the X ray. So P(X then Y) = r₁·|⟨Y|X⟩|². By the law of reciprocity, |⟨Y|X⟩|² = |⟨X|Y⟩|² (the same law gives the QQ equality; Wang & Busemeyer 2013). The order effect is then o = c·(P(X) − P(Y)), with one item constant c.
- **Anchoring** (r₂ = r·r₁ + (1 − r)·fresh) gives o = r·(P(X) − P(Y)): exactly the same form.

With the first rating fixed by the item, nothing can separate the two. They separate only when **r₁ moves independently of the item**. Run 3 moves it.

## 2. The manipulation

Before rating the conjunction, the model is shown a **provided first rating** for one conjunct, set low or high. It must accept or revise it. Its stated first rating r₁ therefore varies across anchor conditions within the same item and order.

**Turn 1 (anchored cells), as structured output `{"decision": "accept" | "revise", "probability": <integer 0–100>}`:**

> *<context>*
>
> *Another person estimated, on a scale from 0 to 100, that the probability that <statement> is <A>. Do you accept this estimate, or would you revise it? Give the estimate you will use as a number from 0 to 100.*

**Turn 2 (every cell), as in run 2:** *"On a scale from 0 to 100, how likely is it that <X> and <Y>? Give only the number."*

**Provided values A.** For each statement, with m its own mean first-turn rating in percentage points (from run 2 for the 7 run-2 items, from run 1 phase 1 for the other 9):
- low: A_lo = max(2, m − 30)
- high: A_hi = min(98, m + 30)

These numbers are computed from archived means and fixed in the frozen commit.

**Settings.** Base model `claude-haiku-5-5`, thinking disabled, default temperature 1.0 (none sent; the API rejects one, D17), integer ratings as structured output. These are identical to run 2.

## 3. Cells and items

| cell | turn 1 | turn 2 | R |
|---|---|---|---|
| X-lo, X-hi | X with provided A_lo or A_hi, accepted or revised | X and Y | 40 each |
| Y-lo, Y-hi | Y with provided A_lo or A_hi, accepted or revised | X and Y | 40 each |
| X→XY, Y→XY | X (or Y) rated freely, as in run 2 | X and Y | 20 each |
| XY | X and Y rated alone (the "fresh" conjunction rating) | — | 20 |

- **Items:** all 16 items of experiment 4 (`experiments/exp4-items.json`). The 7 run-2 fallacy items are reported as their own family. The mechanism question does not need a fallacy, and 16 items give the item-level rules more power than 7.
- **Calls per item:** 4 × 40 × 2 + 2 × 20 × 2 + 20 = 420. That makes **6,720 calls** in all.

## 4. Predictions

Each prediction is for one item and one order, o ∈ {X-first, Y-first}. Fit r₂ = β₀ + β₁·r₁ + β₂·A over that order's 80 anchored conversations (r₁ and r₂ on the 0–1 scale). Because r₁ varies *within* an order through the manipulation, the slope is identified without pooling cells (the D19 lesson).

| account | intercept β₀ | slope β₁ by order | the provided number A, given r₁ (β₂) | ceiling |
|---|---|---|---|---|
| **Anchoring** on the first number | (1 − r)·fresh > 0: r₂ is pulled toward the fresh conjunction rating | the same r in both orders | may be ≠ 0 (pull toward the shown number) | r₂ can exceed r₁ when r₁ < fresh |
| **Classical sequential Bayes** (Jeffrey update of the first conjunct, then the conditional) | 0 (multiplicative) | P(Y∣X) after X-first, P(X∣Y) after Y-first, so **β₁(X-first)/β₁(Y-first) = P(Y)/P(X)** | 0 | r₂ ≤ r₁ |
| **Quantum, rank-one projectors** (Lüders, sequential conjunction) | 0 (multiplicative) | |⟨X|Y⟩|² in **both** orders (reciprocity), so **β₁(X-first)/β₁(Y-first) = 1** | 0 | r₂ ≤ r₁ |
| Quantum, degenerate projectors | 0 | unconstrained | 0 | r₂ ≤ r₁ |

**Reading the table.**
- The **intercept** separates numeric anchoring from content-driven sequential updating, whether quantum or Bayesian.
- The **slope ratio** separates rank-one quantum (ratio 1) from Bayes (ratio P(Y)/P(X)). On these items P(Y)/P(X) is far from 1: about 0.08 for Bill, 0.05 for Marta and 0.08 for co05 in run 2. So the two predictions are well apart.
- A quantum model with degenerate projectors predicts only the zero intercept and the ceiling. If the data are content-driven with a ratio far from 1, that excludes the rank-one quantum model, not quantum models in general. The write-up says so.

## 5. Pre-registered rule

**Manipulation check (per item and order).** The mean r₁ in the high cell minus the mean r₁ in the low cell must be at least 10 rating points. Item-orders that fail are reported, not scored. If fewer than 3 items pass in both orders, the run is **untestable**.

**Per scored item-order** (bootstrap 95% CIs from 1,000 resamples of conversations within cells):
- **Anchoring:** the β₀ CI excludes 0 **and** contains (1 − β₁)·fresh, where fresh is the XY-cell mean.
- **Content (multiplicative):** the β₀ CI contains 0 **and** excludes (1 − β₁)·fresh.
- **Undetermined:** anything else.

**Per scored item where both orders are "content":**
- **Reciprocity (rank-one quantum):** the CI of β₁(X-first)/β₁(Y-first) contains 1 **and** excludes P(Y)/P(X). P(Y) and P(X) are the free-rating means from the X→XY and Y→XY cells.
- **Bayes:** the reverse.
- **Undetermined:** anything else.

**Verdict, over scored items:**
1. **Anchoring explains the order effect** if at least half the scored item-orders classify as anchoring.
2. **Content-driven sequential updating** if at least half classify as content. Then, over the items with both orders content:
   - **rank-one quantum (reciprocity)** if at least half show reciprocity;
   - **classical Bayes** if at least half show the Bayes ratio;
   - **content, mechanism undetermined** otherwise.
3. **Undetermined** if neither 1 nor 2 holds.

**Reported alongside (not in the verdict):**
- β₂ (the pull of the shown number given r₁);
- violations of the ceiling, the share of conversations with r₂ > r₁;
- the accept rate and the mean revision toward the model's own value;
- the replication of run 2's o, from the X→XY and Y→XY cells;
- all results separately for the 7 run-2 fallacy items.

## 6. Repeats, power and the variance problem

- Run 2's free ratings barely varied (SD ≤ 0.05). The anchored cells do not depend on that variance: the manipulation creates the spread in r₁. R = 40 per anchored cell gives 80 points per regression, at two well-separated r₁ levels.
- **The risk** is that the model rejects every provided value and revises straight back to m, so the manipulation check fails. The check catches this before any mechanism is claimed. That outcome would itself be informative: the model's first ratings resist social anchors.

## 7. Cost

At run 2's measured rate (1,120 calls for $0.04, about $0.000036 per call), 6,720 calls cost about **$0.24**. Allowing 1.5× for the longer anchored prompt and the two-field output gives about **$0.35**. **Cap: $2.00, enforced in code.**

There is no QPU time, and wall-clock time is under 30 minutes at 8 workers.

## 8. What this run cannot do

- It tests the mechanism behind the order effect: numeric anchoring against content-driven updating, and within the latter, rank-one quantum against Bayes.
- It does not test R2 again, which run 2 already met on 3 of 3 items.
- It does not decide between degenerate quantum models and classical Bayes when the slope ratio is far from 1. Experiment 5 (`experiments/exp5-sequential-judgment.md`) is the broader test of sequential judgment.


## Amendment at freezing (2026-11-03 22:59 MST, DEVIATIONS.md D33)

1. **One scale direction.** Tonight's experiment-5 finding was that the model does not reliably reverse a flipped scale: recoded baseline means were 33.8 vs 71.3. So every rating prompt in run 3 states one direction explicitly, ", where 0 = certainly false and 100 = certainly true". It is added to the turn-1 anchored prompt, to the free first rating and to the conjunction rating. There is no counterbalanced reversal.
2. **Provided values A,** computed from archived means as §2 specifies and fixed here (also in `experiments/exp4-run-3-anchors.json`):

| item | source of m | m(X) | A_lo / A_hi for X | m(Y) | A_lo / A_hi for Y |
|---|---|---|---|---|---|
| co01 | run 2 first-turn means | 85.0 | 55 / 98 | 5.1 | 2 / 35 |
| co02 | run 1 phase-1 means | 97.0 | 67 / 98 | 8.2 | 2 / 38 |
| co03 | run 1 phase-1 means | 85.0 | 55 / 98 | 50.0 | 20 / 80 |
| co04 | run 1 phase-1 means | 78.0 | 48 / 98 | 27.0 | 2 / 57 |
| co-lin06 | run 2 first-turn means | 84.6 | 55 / 98 | 6.6 | 2 / 37 |
| co-lin08 | run 2 first-turn means | 56.4 | 26 / 86 | 4.2 | 2 / 34 |
| co-lin09 | run 2 first-turn means | 70.4 | 40 / 98 | 44.0 | 14 / 74 |
| co-lin10 | run 2 first-turn means | 85.0 | 55 / 98 | 4.3 | 2 / 34 |
| co05 | run 2 first-turn means | 47.9 | 18 / 78 | 4.1 | 2 / 34 |
| co06 | run 2 first-turn means | 47.0 | 17 / 77 | 10.0 | 2 / 40 |
| co07 | run 1 phase-1 means | 65.0 | 35 / 95 | 38.5 | 8 / 68 |
| co08 | run 1 phase-1 means | 80.0 | 50 / 98 | 15.0 | 2 / 45 |
| co09 | run 1 phase-1 means | 82.0 | 52 / 98 | 5.0 | 2 / 35 |
| co10 | run 1 phase-1 means | 78.2 | 48 / 98 | 4.2 | 2 / 34 |
| co11 | run 1 phase-1 means | 79.5 | 49 / 98 | 3.0 | 2 / 33 |
| co12 | run 1 phase-1 means | 54.8 | 25 / 85 | 48.8 | 19 / 79 |

3. **Collinearity.** If, within an order, r₁ equals A in every conversation (the model accepts every provided value), then r₁ and A are collinear and β₂ is not identified. That item-order is then fitted as r₂ = β₀ + β₁·r₁, and β₂ is reported as unidentified. More generally, the fit falls back to this two-parameter form whenever the design matrix's condition number exceeds 10⁶. The classification rules use β₀ and β₁ only, so they are unaffected.
4. **Point values in the rules.** In the anchoring and content tests, (1 − β₁)·fresh is evaluated at the point estimates. In the reciprocity test, P(Y)/P(X) is evaluated at the free-cell means. The bootstrap supplies the β₀ and slope-ratio intervals.

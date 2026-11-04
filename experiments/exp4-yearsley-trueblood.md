# Experiment 4 — Quantitative Yearsley & Trueblood test: pre-registration (not yet run)

Written 2026-11-03, before any experiment-4 call. **Status: pre-registered, queued last** (after the v2 steps and experiment 3). Budget: **$10**, enforced in code.

## Question

Yearsley & Trueblood (2018) argue that conjunction fallacies and order effects should co-occur, because both come from incompatible (non-commuting) events. Their prediction is qualitative.

A quantitative version follows from the Lüders rule (`items-borrowed.json → cooccurrence_rule`, R2). Write P(X then Y) for the probability of judging X true and then Y true, with X judged first. Quantum theory gives P(Y then X) ≤ P(Y). So if the model commits a fallacy, P(X then Y) > P(Y), then

**o = P(X then Y) − P(Y then X) ≥ f = P(X then Y) − P(Y).**

The order effect must be at least as large as the fallacy. This is a consequence of the quantum model, but an updating classical model, in which each judgment updates the state before the next, satisfies it too. Only the **static** classical twin is ruled out: with no updating between judgments it gives P(X then Y) = P(Y then X), so o = 0 apart from what simple repetition of the first answer produces.

## Items (fixed)

`experiments/exp4-items.json` holds 16 items, each with a context, a representative or likely conjunct X, and a less representative or unlikely conjunct Y:
- co01–co04 from `items-borrowed.json → cooccurrence_rule`
- Bill, Priya, the analytical-person item and the name-swapped Marta, converted from `linda_variants` (`co-lin06`, `co-lin08`, `co-lin09`, `co-lin10`)
- eight author-written items, co05–co12: people, fictional elections, weather, sport and markets

## Base model and calls

- **Model:** `claude-haiku-5-5` with thinking disabled. This follows the borrowed QQ protocol, which says to use "thinking off or display omitted, and nothing read from it".
- **One fresh call per sample.** No calls share a conversation except the scripted two-turn sequences.
- **Refusals:** a refusal stops the run at once, with the request ID recorded, and nothing is retried.

## Phase 1 — rating screen

1. **Ratings:** for each item, R = 20 fresh calls each for P(X), P(Y), P(X and Y) worded "X and Y", and P(Y and X) worded "Y and X". Each answer is an integer from 0 to 100, returned as structured output.
2. **Fallacy item:** mean P(X and Y) − mean P(Y) > 0, with the 95% bootstrap lower bound (1,000 resamples) above 0. That is the case where the model rates "A and B" above B alone.
3. **R3 (no double fallacy):** count the items where P(X and Y) exceeds both single ratings.

## Phase 2 — QQ audit on the fallacy items

This follows Kang (2026)'s committed multi-turn, forced-branch protocol, adapted for an API without log-probabilities (`items-borrowed.json → qq_order_protocol`).

- **System prompt:** "You are asked a series of judgment questions. For each question, answer with exactly one letter: "A" or "B". Do not explain." The answer is returned as structured output {"answer": "A" | "B"}.
- **Each question:** the context, then "Is it true that <X>?" (or <Y>), with a legend.
  - Mapping M1: A = yes, B = no.
  - Mapping M2: A = no, B = yes.
- **First position:** for each order (X first, Y first) and each mapping, R = 50 calls give the first-answer distribution p₁.
- **Second position, committed first answer:** for each order, each forced first answer (yes, no) and each of the **4 mapping combinations** (Q1 mapping × Q2 mapping), R = 25 calls. The forced first answer is written into the history as the assistant turn holding that label, and the call gives K(second | first).
- **Joint distribution:** p_order(α, β) = p₁(α) · K(β | α), at the content level (labels mapped back to yes/no), pooled over mappings. Independently measured marginals are never multiplied together.

## Statistics, each with a 95% bootstrap interval over calls (1,000 resamples)

- **Order effect:** o = p_XY(yes, yes) − p_YX(yes, yes).
- **Binary fallacy:** f = p_XY(yes, yes) − p₁(Y = yes | Y asked first). The phase-1 rating fallacy (in points / 100) is reported alongside.
- **Repetition (Kang 2026, Prop. 4):** fit the symmetric repetition model, in which the model repeats its first content answer with probability r and otherwise answers fresh from the first-position marginals. That model gives o_rep = r · (p_X − p_Y). The **order effect beyond repetition** is o − o_rep.
- **Letter-copying check:** ρ = P(same content answer | same mapping) − P(same content answer | crossed mapping). A content-driven model gives ρ ≈ 0. An item is flagged "repeating labels" if ρ > 0.10, and R2 is not scored on it.
- **Marginal-shift check, reported next to every number:**
  - OE_X = p(X = yes when second) − p(X = yes when first)
  - OE_Y, defined the same way
  - OSS = |OE_X| + |OE_Y|
  - q_QQ = the difference between orders in the probability of disagreeing answers
  - Γ = |q_QQ| − OSS. Γ ≤ 0 means non-contextual under rank-2 Contextuality-by-Default.
- **Saturation gate:** if the minority answer appears in fewer than 1 of R samples at more than half the positions, the item is "saturated" and no QQ or R2 conclusion is drawn from it.

## Predictions and pass rules

The scored items are the fallacy items that pass the saturation gate and the letter-copying check, and have f with a 95% lower bound above 0.

- **R2 is met (consistent with the quantum model or a sequential-update classical model; rules out the static twin)** if at least half of the scored items have o ≥ f − 0.05 (the borrowed 5-point tolerance), **and** at least half have o − o_rep with a 95% lower bound above 0.
- **The static classical twin (with repetition) is supported** if at least half of the scored items have an interval for o − o_rep that contains 0.
- **Neither is supported** if neither rule is met. A pass on R2 does not by itself select the quantum account over a sequential-update classical one. **Untestable** if there are fewer than 3 scored items, in which case everything is reported descriptively.
- **R1 is reported:** the share of fallacy items whose o is reliably different from 0.
- **R3 is reported:** the double-fallacy count. Any reliable double fallacy counts against the quantum account.

## Cost estimate

With thinking disabled, each call is about 200 input and about 10 output tokens, or about $0.00003.
- Phase 1: 16 items × 80 calls = 1,280 calls.
- Phase 2: at most 16 items × (200 first-position + 400 second-position) = 9,600 calls.
- **Total ≈ $0.35**, against the $10 cap. That is about 11,000 calls, roughly 30–45 minutes at 8 parallel workers.

## Addendum — run 2, graded form (pre-registered before run 2)

**Written 2026-11-03 19:06 MST, before any run-2 call.** Run 1's binary QQ phase was fully saturated (`results/exp4-run-1.md`): the model answered "Is it true that <Y>?" with "no" every time. Run 2 measures the same order test with graded ratings instead.

- **Items:** the 7 items with a reliable rating fallacy in run 1: co01, co-lin06, co-lin08, co-lin09, co-lin10, co05 and co06.
- **Calls:**
  - Base model `claude-haiku-5-5`, thinking disabled.
  - **Default sampling temperature, which is 1.0.** The current API rejects an explicit temperature parameter for this model, so none is sent.
  - Each answer is an integer from 0 to 100, as structured output, with the same rating wording as run 1's phase 1.
- **Cells:** each cell is a two-turn conversation. The first rating is committed, the second is asked in the same conversation, and each cell gets R = 20 repeats:
  1. **X → XY:** rate P(X), then P(X and Y).
  2. **Y → XY:** rate P(Y), then P(X and Y).
  3. **X → Y:** rate P(X), then P(Y), for the marginal-shift check.
  4. **Y → X:** rate P(Y), then P(X).

  That is 7 × 4 × 20 conversations, 1,120 calls.
- **Statistics, all on the 0–1 scale, each with a 95% bootstrap interval over repeats (1,000 resamples):**
  - Graded order effect: o = mean P(X and Y | X first) − mean P(X and Y | Y first).
  - Graded fallacy: f = mean P(X and Y | X first) − mean P(Y | Y rated first). The first-turn ratings of cells 2 and 4 are pooled for P(Y).
  - Anchoring on the first answer, the graded analogue of repetition. Fit second = r · first + (1 − r) · fresh by regressing the second rating on the first within cells 1–2, with fresh taken from the first-turn means. Then o_rep = r · (P(X) − P(Y)), and **o − o_rep** is the order effect beyond anchoring.
  - **Marginal-shift check, reported beside every number:** OE_X = mean P(X | rated second) − mean P(X | rated first), OE_Y defined the same way, and OSS = |OE_X| + |OE_Y|. (q_QQ and Γ are defined only for binary answers.)
- **Rules, unchanged from the pre-registration and the D11 addendum:**
  - Scored items are those with f's 95% lower bound above 0.
  - **R2 is met** (consistent with quantum or sequential-update classical; rules out the static twin) if at least half the scored items have o ≥ f − 0.05 **and** at least half have o − o_rep reliably > 0.
  - **The static twin is supported** if at least half have an o − o_rep interval that contains 0.
  - **Untestable** if fewer than 3 items are scored.
- **Budget:** $10, enforced in code. The estimate is about $0.05.

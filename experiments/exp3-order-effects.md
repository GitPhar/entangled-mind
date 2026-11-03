# Experiment 3 — Order effects: pre-registration (not yet run)

Written 2026-11-03, after Stage 2 runs 1–2 and before any order-effect data. **Status: designed, not run.** Running it needs Sean's go-ahead on the budget below.

## Question

Quantum-cognition models explain *question-order effects* (asking A then B gives different answers from B then A) through non-commuting operators. Arm A encodes a model's contentions as one entangled state. Does that state predict *which* pairs of contentions, when the model is asked about them first and in different orders, shift its final answer the most? And does it predict this better than its classical twin (arm F)?

## A correction to the obvious design

If "asking about contention *k*" is modelled as a projector on qubit *k*, two different contentions act on different qubits. Their projectors commute, even after conjugation by arm A's entangling evolution V, because V P_i V† and V P_j V† commute whenever P_i and P_j do. So the predicted order effect would be exactly zero for every pair. Asking is therefore modelled as a local evolution, not a projection.

## Models (fixed)

Let |ψ_A⟩ be arm A's noiseless pre-readout state, and let Π_yes be the readout's yes-projector (weighted X-basis vote m > 0, with m = 0 counted as half).

**Quantum prediction.** Considering contention *k* applies U_k = exp(−i γ₀ H_k), with γ₀ = 0.5 (the existing constant) and

H_k = −Σ_{j~k} J_kj X_k X_j − lean_k X_k − Z_k

This is *k*'s share of arm A's problem Hamiltonian plus its mixer term. U_i and U_j do not commute when contentions *i* and *j* are coupled, directly or through the mixer.

The predicted order effect is Δᴼ_ij = |⟨Π_yes⟩ after U_j U_i − ⟨Π_yes⟩ after U_i U_j|, computed exactly by statevector simulation (≤ 16 qubits).

**Classical-twin prediction (arm F).** Start from the product distribution with p_k(yes) = (1 + sin θ_k cos φ_k)/2, the same single-contention marginals as arm A's preparation. Considering contention *k* is one exact heat-bath (Glauber) update of spin *k* under arm F's energy E(x) at temperature T = 1. Sequential classical updates can depend on order too, so this is a fair comparator, not a strawman.

The predicted order effect is Δᶠ_ij = |P_yes(i then j) − P_yes(j then i)|, computed exactly over all 2^n configurations.

## Items and pairs

- **Items:** 40 items from the Stage 2 run-2 test set, 20 wrong and 20 right, drawn at random with seed 3.
- **Pairs per item:** the 2 related pairs with the largest Δᴼ and the 2 with the smallest Δᴼ, plus the largest-Δᶠ and smallest-Δᶠ pairs not already chosen. That is at most 6 pairs per item. Including arm F's extremes stops the selection from favouring the quantum model.

## Protocol

The base model is `claude-haiku-5-5`, at default effort with adaptive thinking.

1. **Conversation:** for each selected pair (*i*, *j*) and each order, one three-turn conversation:
   1. "Consider this statement: '<contention *i*>'. Do you think it is true? Answer in one sentence."
   2. The same for contention *j*.
   3. The original question with the standard base prompt, ending in `FINAL ANSWER: YES/NO`.
2. **Repeats:** R = 5 conversations per pair and order.
3. **Baseline:** R = 5 single-turn runs of the original question, to measure the model's own run-to-run variability.
4. **Thinking:** `display: "omitted"`. Each assistant turn's content is passed back unchanged within its own conversation, as the API requires. No thinking text is read, stored, or sent to any other call.
5. **Refusals:** as in the rest of the project, a refusal stops the run at once with the request ID recorded, and nothing is retried.

**Observed order effect** for a pair: |P̂_yes(i first) − P̂_yes(j first)|, from 5 + 5 conversations.

## Prediction and test

- **Primary:** across all item-pairs, Spearman ρ(Δᴼ, observed) > ρ(Δᶠ, observed). The difference ρᴼ − ρᶠ gets a 95% CI from 2,000 bootstrap resamples of *items* (pairs within an item move together). **Pass** if the CI excludes 0 on the positive side. **Fail** if it excludes 0 on the negative side. **Inconclusive** otherwise.
- **Secondary:**
  - Do order effects exist at all? Compare the mean observed order effect with the mean absolute difference between two random halves of the baseline runs, using a permutation test.
  - Do the 2 largest-Δᴼ pairs per item show larger observed effects than the 2 smallest? Paired Wilcoxon test over items.
- **Falsifying null for the quantum claim:** ρᴼ ≤ ρᶠ, meaning non-commutation adds nothing over classical sequential updating. If order effects are absent (secondary 1 fails), the experiment cannot discriminate the two models, and that is what gets reported.

## Cost estimate (Anthropic API; no QPU time)

These figures use pool run 3's measured Haiku base-call usage: 165 input and 846 output tokens on average. Prices are $0.10 in and $0.50 out per MTok.

| per three-turn conversation | input tokens | output tokens |
|---|---|---|
| turn 1 | ~150 | ~400 |
| turn 2 (turn 1 re-sent) | ~700 | ~400 |
| turn 3 (turns 1–2 re-sent) | ~1,300 | ~850 |
| **total** | **~2,150** | **~1,650** |

- One conversation costs about **$0.0010**.
- Per item: 6 pairs × 2 orders × 5 repeats = 60 conversations, plus 5 baseline runs at about $0.0004 each, which comes to **≈ $0.065**.
- **40 items ≈ $2.60 expected.** Wrong items run longer, at 1,246 output tokens on average, so with a 50% allowance for that and for longer thinking the cap would be set at **$4.00**, enforced in code.
- There are 2,600 conversations, or about 7,800 calls. At 4 parallel workers that is roughly 1–1.5 hours of wall-clock time.

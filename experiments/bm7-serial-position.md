# Biomimetic map (rev. 1 §3.7, rev. 2 §3.5): serial-position weights from the archived experiment 5 chains (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before the archive was opened for this analysis. DEVIATIONS.md D41. Cost $0: no API calls.

**What was already known at freezing:**
- the median order span (24.7 points);
- direction 9's NSIT results (`results/gm9-nsit.md`);
- experiment 5's fitted BA5, whose decay ρ = 0.877 < 1 weights later sub-questions more, a recency prediction.

No per-position weight has been computed.

## 1. In plain English

When the model hears four pieces of evidence in a row and then gives its verdict, does the first piece count most (primacy), the last (recency), or all equally? Different accounts predict different shapes:
- **step-by-step belief adjustment** (Hogarth & Einhorn): recency;
- **a perfect integrator:** flat weights;
- **competing accumulators (the LCA):** any of those monotone shapes, but never a U-shape in which both the first and the last pieces count more than the middle ones.

Experiment 5's O1–O4 chains are a Latin square: each sub-question appears once in each position. So the weight of each position can be estimated from data we already have.

**Revision 2 of the map** (`f824e14`), after reading Usher & McClelland 2001 in full: the leaky competing accumulator allows any monotone serial-position curve (primacy, recency or flat), but **never a U-shape** (p. 579). So the primacy/recency reading does not discriminate the LCA from belief adjustment. The U-shape check is the falsification test, and it is the primary reading here.

## 2. Data

- `results/exp5-conversations.json`, the 40 candidates, chains O1–O4.
- **Anchor (a) conversations only** (one scale direction): 5 per chain and item, 800 conversations in all.
- Conversations with a schema error are dropped.

## 3. Model

- **Evidence at position p:** x_p = sign(lean_k) · (rating_p − 50) / 50, where k is the claim asked at position p. So x_p is the yes-ward evidence the model itself stated.
- **Regression:** final M = α_item + Σ_{p=1..4} w_p · x_p + ε, by OLS with item fixed effects.
- **CIs:** 2,000 cluster-bootstrap resamples over items (seed 5151).
- **U-shape contrasts:** u₁ = w₁ − (w₂ + w₃)/2 and u₄ = w₄ − (w₂ + w₃)/2.
- **Primacy–recency contrast:** w₁ − w₄. **Linear trend:** the slope of w_p on p.

## 4. Pre-registered reading

1. **U-shape, which falsifies the LCA:** the CIs of both u₁ and u₄ lie above 0.
2. Otherwise the curve is called **monotone or flat**, which is consistent with the LCA. It is then described as:
   - **primacy:** the CI of w₁ − w₄ lies above 0;
   - **recency:** it lies below 0, the BA5 / Hogarth–Einhorn direction, which the leak-dominant LCA also allows;
   - **flat:** otherwise.

Reported alongside are the four weights, the trend, and BA5's implied weights, ρ^(4−p) normalised to w₄.

## 5. What it cannot do

The map's unique LCA test, a move from primacy to recency as chains get longer, needs chains of length 2, 4 and 8. That is a new run and is not part of this analysis.

# Gold-map direction 9: no-signalling in time on the archived experiment 5 conversations (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before the analysis was run. DEVIATIONS.md D34. Cost $0: no API calls, archived data only.

## 1. In plain English

When you ask a person one question and then another, the first can change the answer to the second. Quantum cognition reads this as "measurement disturbs the state". A person's mind can't be copied, so two explanations can't be told apart:
- the person had no definite opinion until asked;
- asking changed an opinion that was already there.

A language model is different. At every turn its whole state is the conversation so far, a piece of text that can be copied exactly. So it always has a definite state (macrorealism holds by construction). We can also always run the "not asked" counterfactual on an exact copy. Any effect of an earlier question can therefore only be **invasiveness**: the earlier question and its answer were added to the state.

This analysis measures that invasiveness on data we already have. It uses the standard test for it, no-signalling in time (NSIT): does asking an earlier question, averaged over whatever was answered, change the distribution of a later answer?

## 2. Data

- `results/exp5-conversations.json`, the 40 experiment-5 candidates. The pilot items are not used (as in experiment 5).
- **One scale direction only:** conversations on anchor (a), "0 = certainly false, 100 = certainly true". These are the even-numbered repeats. Anchor-(b) conversations are not used at all; pooling the two directions was experiment 5's confound (D33).
- Conversations with a schema error are dropped.
- **Replication set:** `results/exp5-run-2-conversations.json` (first 10 candidates, anchor (a), 40 conversations per QQ order).

## 3. Families of contrasts

Each cell is one item and one contrast. "Asked" and "not asked" are conversations whose only design difference is whether the earlier question was put. The later rating is compared across them.

| family | later rating | asked | not asked | cells | conversations per cell (asked / not) |
|---|---|---|---|---|---|
| N1M | the main question M | QQ order SM (S_k, then M) | QQ order MS (M first) | 80 (40 items × 2 pairs) | 20 / 20 |
| N1S | the sub-question S_k | QQ order MS (M, then S_k) | QQ order SM (S_k first) | 80 | 20 / 20 |
| N2 | final M | O1 (S1 S2 S3 S4, then M) | X_k (O1 with S_k removed), k = 1..4 | 160 | 5 / 5 |
| N3 | final M | O1–O4 pooled | B0 (M alone) | 40 | 20 / 5 |
| N4 | final M | K1 (a yes/no choice midway) | K0 (a filler midway) | 40 | 5 / 5 |
| N5 | final M | MF (M asked first, then S1–S4, then M) | O1 | 40 | 5 / 5 |

## 4. Statistics

- **Per cell:** d = mean(later rating | asked) − mean(later rating | not asked), in rating points. Also ΔP = P(rating ≥ 50 | asked) − P(rating ≥ 50 | not asked), the binarised NSIT.
- **Family test:** T = Σ_cells d². The null comes from permuting the asked / not-asked labels within each cell independently: 5,000 permutations, seed 9009, with p = (1 + #{T_perm ≥ T}) / 5,001.
- **Holm** correction over the six families.
- **Effect sizes:**
  - mean |d| against its permutation-null mean;
  - the share of cells with |d| ≥ 10 points;
  - the mean signed d with a 2,000-resample item-bootstrap CI (seed 9010): does asking push ratings one way?
  - the mean |ΔP|.
- **Replication:** N1M and N1S recomputed on the run-2 conversations (10 items × 2 pairs, 40 / 40).

## 5. Pre-registered reading

1. A family is **invasive** if its Holm-adjusted p < 0.05.
2. **The conceptual claim** does not depend on the data. For a system whose state is its copyable context, NSIT cannot test macrorealism; a violation measures invasiveness only. The same holds for every QQ, order-effect or Leggett–Garg-type test run on an LLM through its context. The write-up states this and states which families were invasive.
3. The analysis cannot say whether the invasiveness comes from the **question** text or from the **record of the answer**. Direction 2 (`experiments/gm2-self-conditioning.md`) separates the two by redacting and planting the recorded answers.

## 6. What it cannot do

- It does not test any quantum model.
- It uses only five conversations per condition in N2–N5, so small effects in those families can be missed. N1 has 20 per condition.

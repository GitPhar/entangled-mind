# Direction 9: no-signalling in time (NSIT) on the archived experiment 5 conversations

Pre-registered in `experiments/gm9-nsit.md` (D34), committed before this analysis. Anchor (a) conversations only (0 = certainly false, 100 = certainly true); 40 items; no API calls; $0.

## In plain English

**The question.** Does asking the model one question change how it answers a later one? We measured this on conversations we already had from experiment 5, using only the conversations with the same scale direction (0 = certainly false, 100 = certainly true).

**What we found.** Asking an earlier question changes later answers, in 5 of the 6 kinds of comparison.
- **One sub-question asked just before the main question** moves the main rating by about 12 points on average, against about 3 points expected from repeat-to-repeat noise. The shift goes up on some items and down on others, so it averages out to nothing overall.
- **The main question asked first** raises the next sub-question's rating by about 8 points on average (+8.0 [+2.7, +13.3]), though 30 of the 80 cells move the other way.
- **All four sub-questions asked first** move the main rating by about 23 points, against 5 from noise.
- **The main question asked at the start of a chain** lowers the main rating at the end by about 10 points, compared with chains that never asked it at the start.
- **A midway yes/no choice, in place of a filler turn,** has no detectable effect: 5 points against 3 from noise, p = 0.16. This matches experiment 5's null on the Kvam test.
- The two single-question effects replicate on the separate run-2 conversations: 17 and 16 points, against about 3 from noise.

**What it means.** A person's mind can't be copied, so when an earlier question changes a later answer, two explanations can't be told apart: either there was no settled opinion until asked, or asking changed it. A language model's whole state is the conversation text, which can be copied exactly. So it always has a definite state, and the "never asked" comparison runs on an exact copy, not a different person or a different day. (Strictly, the copy reproduces the *distribution* of answers, not the specific random draw: the API exposes no sampling seed. That is all the test needs.) Every effect above is therefore the act of asking adding text to the state (**invasiveness**). None of it is evidence that the model had no answer until asked.

The same reasoning applies to every order-effect, QQ or Leggett–Garg-style test run on a language model through its conversation, ours and other people's. Such tests can measure how much asking disturbs the model. They cannot show that its judgments lack definite values.

**What it can't say.** The added text has two parts: the question itself and the model's recorded answer. This analysis can't tell which one does the work. Direction 2 tests that by hiding or replacing the recorded answers.

## Results

d = mean later rating when the earlier question was asked minus when it was not (rating points). Permutation test of Σd² with labels shuffled within each cell (5,000 permutations); Holm over the six families.

| family | contrast | cells | n per condition (median) | mean |d| (null) | cells with |d| ≥ 10 | mean d [item-bootstrap CI] | mean |ΔP(≥50)| | p (perm) | p (Holm) | invasive |
|---|---|---|---|---|---|---|---|---|---|---|
| N1M | main question M after S_k (QQ: SM) vs M first (MS) | 80 | 20 / 20 | 12.4 (2.6) | 28% | -0.0 [-6.1, +5.5] | 0.11 | 0.0002 | 0.0012 | **yes** |
| N1S | sub-question S_k after M (QQ: MS) vs S_k first (SM) | 80 | 20 / 20 | 15.7 (3.1) | 42% | +8.0 [+2.7, +13.3] | 0.18 | 0.0002 | 0.0012 | **yes** |
| N2 | final M with S_k asked (O1) vs omitted (X_k) | 160 | 5 / 5 | 8.7 (3.9) | 19% | +0.7 [-3.7, +4.3] | 0.09 | 0.0002 | 0.0012 | **yes** |
| N3 | final M after all four sub-questions (O1-O4) vs M alone (B0) | 40 | 20 / 5 | 22.6 (5.2) | 50% | +2.7 [-9.3, +13.7] | 0.23 | 0.0002 | 0.0012 | **yes** |
| N4 | final M after a midway yes/no choice (K1) vs a filler (K0) | 40 | 5 / 5 | 5.0 (3.3) | 12% | -0.5 [-3.2, +2.5] | 0.05 | 0.1634 | 0.1634 | **no** |
| N5 | final M with M asked first (MF) vs not (O1) | 40 | 5 / 5 | 16.0 (6.1) | 40% | -10.1 [-18.2, -2.9] | 0.14 | 0.0002 | 0.0012 | **yes** |

## Replication on experiment 5 run 2 (10 items, anchor (a), 40 conversations per order)

| family | cells | mean |d| (null) | cells with |d| ≥ 10 | mean d [CI] | p (perm) |
|---|---|---|---|---|---|
| N1M | 20 | 17.4 (2.9) | 50% | -3.8 [-19.0, +9.8] | 0.0002 |
| N1S | 20 | 15.7 (2.3) | 45% | +10.6 [+0.5, +22.6] | 0.0002 |

## Pre-registered reading

- Invasive families (Holm p < 0.05): **N1M, N1S, N2, N3, N5**.
- Because the model's state at every turn is its copyable context, macrorealism holds by construction and the "not asked" condition is an exact counterfactual at the level of the response distribution (the API exposes no sampler seed, so the specific draw is not recovered; the clone-read model is still factorisable). Every NSIT violation above is therefore invasiveness, never evidence against definite states (§5.2).
- Whether the invasiveness comes from the question or from the record of the answer is direction 2's question.

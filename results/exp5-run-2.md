# Experiment 5, run 2: B0 and the QQ block with one scale direction

Pre-registered in the Addendum to `experiments/exp5-sequential-judgment.md` (D33). The first 10 candidates (h190, h101, h112, h191, h261, h058, h221, h279, h127, h238), with every conversation on anchor (a) (0 = certainly false, 100 = certainly true). Descriptive; no refitting. 1700 conversations, **$0.14**.

| measurement | pairs with OE > 0.10 (CI excl. 0) | mean q [95% item-bootstrap CI] | KS of z vs N(0,1) | B0 mean (SD across items) | B0 between-repeat SD (median) |
|---|---|---|---|---|---|
| run 2 (anchor a only) | 12 of 20 | -0.146 [-0.439, +0.137] | D = 0.46, p = 0.008 | 36.2 (34.2) | 7.1 |
| run 1, anchor a only | 12 of 20 | -0.154 [-0.423, +0.154] | D = 0.43, p = 0.017 | 36.6 (35.3) | 4.1 |
| run 1, both anchors pooled | 16 of 20 | +0.031 [-0.098, +0.166] | D = 0.44, p = 0.002 | 50.9 (29.5) | 20.6 |

## Per pair (run 2)

| pair | OE [95% CI] | OE_S | OE_M | q | z | run 1 OE (pooled) |
|---|---|---|---|---|---|---|
| h190:S2 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | +0.000 | +0.00 | 0.12 |
| h190:S5 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | +0.000 | +0.00 | 0.55 |
| h101:S3 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | +0.000 | +0.00 | 0.12 |
| h101:S2 | 0.05 [0.00, 0.12] | +0.05 | +0.00 | -0.050 | -1.43 | 0.12 |
| h112:S5 | 0.57 [0.38, 0.78] | +0.12 | +0.45 | +0.375 | +3.44 | 0.32 |
| h112:S2 | 0.32 [0.12, 0.55] | +0.15 | -0.17 | -0.075 | -1.77 | 0.15 |
| h191:S2 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | +0.000 | +0.00 | 0.45 |
| h191:S9 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | +0.000 | +0.00 | 0.03 |
| h261:S0 | 0.25 [0.12, 0.40] | +0.00 | -0.25 | +0.250 | +3.38 | 0.15 |
| h261:S6 | 0.88 [0.75, 0.97] | +0.00 | -0.88 | -0.875 | -7.83 | 1.05 |
| h058:S1 | 0.75 [0.58, 0.92] | -0.05 | -0.70 | +0.650 | +6.21 | 0.62 |
| h058:S3 | 0.23 [0.12, 0.45] | -0.05 | -0.18 | +0.225 | +3.18 | 0.10 |
| h221:S5 | 0.90 [0.70, 1.07] | +0.72 | -0.17 | -0.550 | -4.94 | 0.60 |
| h221:S2 | 0.28 [0.12, 0.43] | +0.10 | -0.17 | -0.225 | -3.18 | 0.45 |
| h279:S6 | 1.00 [1.00, 1.00] | +1.00 | +0.00 | -1.000 | -8.94 | 1.00 |
| h279:S3 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | +0.000 | +0.00 | 0.00 |
| h127:S0 | 2.00 [2.00, 2.00] | +1.00 | +1.00 | +0.000 | +0.00 | 0.82 |
| h127:S3 | 0.75 [0.62, 0.88] | +0.75 | +0.00 | -0.750 | -6.93 | 0.53 |
| h238:S3 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | +0.000 | +0.00 | 0.07 |
| h238:S5 | 0.47 [0.25, 0.70] | +0.35 | -0.12 | +0.225 | +2.92 | 0.30 |

## Pre-registered reading

- **Order effects survive** (at least half of run 1's large-OE pairs still large): **True**. 12 of 16 run-1 large-OE pairs are large in run 2.
- **Near-zero q survives** (run 2's mean-q CI contains 0): **True**. Run 1's QQ near-miss is resolved (the CI also lies within ±0.05): **False**.

## Reading

- **The order effects are not a scale artefact.** With every conversation on one scale direction, 12 of the 16 pairs that showed a large order effect in run 1 still do. Run 1's anchor-(a) subset has the same count (12 of 20).
- **Run 1's near-zero q was largely produced by pooling the two scale directions.**
  - On one scale, mean q is **−0.146** [−0.439, +0.137], almost exactly run 1's anchor-(a) subset (−0.154 [−0.423, +0.154]).
  - Run 1's pooled +0.031 came from averaging over the flipped scale, which pulled opposite-signed effects toward 0.
  - The CI still contains 0, so the pre-registered "survives" is met. But the estimate is imprecise and leans negative, the CI is far from ±0.05, and the per-pair z values are overdispersed (KS p = 0.008).
  - The QQ equality is therefore **not** supported on one scale. Run 1's near-miss should not be read as evidence for it.
- **The scale flip was also the main source of noise.** The median between-repeat SD of the baseline rating is 7.1 points on one scale, against 20.6 with both anchors pooled. Single-scale designs are much more sensitive.
- **This changes one line of run 1's reading:** the "near-zero q" there should be read as an artefact of anchor pooling, not as an approximate QQ equality. As first written here: "Run 1's verdict, a tie, does not use QQ beyond 'signature not present', so it is unchanged." That was wrong (superseded, D52): the tie's "not contradicted" leg used the pooled q. On run 1's anchor-(a) conversations the QQ signature is contradicted, so run 1's verdict is re-issued as **classical**.

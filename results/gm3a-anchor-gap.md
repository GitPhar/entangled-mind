# Direction 3, free look: does the scale-direction gap predict the model's errors?

Pre-registered in `experiments/gm3a-anchor-gap.md` (D35), committed before this analysis. 40 experiment-5 items (20 wrong, 20 right in the hard pool); no API calls; $0.

## In plain English

**The question.** In experiment 5 the model answered the same main question on two scale directions: "0 = certainly false" and "0 = certainly true". After recoding, the two averages should agree. They differed by 37 points overall. We asked whether the items with a large gap are the ones the model gets wrong.

**What we found.** No evidence either way. The gap shows no detectable relation to the model's errors, but 40 items can only detect a large one:
- **The gap:** AUROC 0.48 [0.28, 0.66]. That is not distinguishable from chance, and the same holds on the larger set of identical first turns, at 0.47. If anything the gap is slightly larger on items the model got right (41 points) than on items it got wrong (34).
- **The model's own stated confidence** on the same 40 items does predict errors, at 0.75 [0.58, 0.89].
- **How extreme its anchor-(a) rating is** also predicts errors, at 0.70.

**What it means.** The scale-direction gap looks like a reading slip in the reversed scale, not a sign of items where the model has no settled view. We could not detect the 37-point gap tracking whatever makes the model unsure of its answer. With 40 items it can only rule out a large effect. The six-format run (direction 3) is the real test.

## Results

| score (higher = predicted wrong) | AUROC for the model's errors [95% CI] |
|---|---|
| |gap| (B0) | 0.48 [0.28, 0.66] |
| signed gap (B0) | 0.53 [0.34, 0.72] |
| |gap| (B0-equivalent first turns) | 0.47 [0.28, 0.65] |
| 100 − G (arm-G self-confidence) | 0.75 [0.58, 0.89] |
| 50 − |mean_a − 50| (anchor-a B0 extremity) | 0.70 [0.52, 0.85] |

- Mean |gap|: 33.9 points on wrong items, 41.3 on right items.
- Paired difference AUROC(|gap|) − AUROC(100 − G): -0.27 [-0.49, -0.05].
- Spearman ρ(|gap|, G) = -0.16 (p = 0.327).

## Per item

| item | wrong | B0 mean, anchor a | B0 mean, anchor b (recoded) | gap | gap (B0-equivalent, n per direction) | G |
|---|---|---|---|---|---|---|
| h190 | yes | 3.2 | 8.2 | -5.0 | -12.2 (50) | 25 |
| h101 | yes | 3.2 | 43.4 | -40.2 | -43.9 (50) | 75 |
| h112 | yes | 22.4 | 60.0 | -37.6 | -42.6 (50) | 72 |
| h191 | yes | 2.8 | 85.6 | -82.8 | -82.9 (50) | 60 |
| h261 | yes | 90.8 | 95.8 | -5.0 | -3.9 (50) | 65 |
| h058 | yes | 78.2 | 99.2 | -21.0 | -18.5 (50) | 45 |
| h221 | yes | 32.0 | 60.0 | -28.0 | -23.9 (50) | 55 |
| h279 | yes | 25.0 | 50.0 | -25.0 | -24.4 (50) | 80 |
| h127 | yes | 12.8 | 53.0 | -40.2 | -41.1 (50) | 35 |
| h238 | yes | 95.6 | 96.2 | -0.6 | -0.2 (50) | 85 |
| h111 | yes | 95.2 | 94.4 | +0.8 | +0.7 (50) | 80 |
| h197 | yes | 25.0 | 53.0 | -28.0 | -31.4 (50) | 35 |
| h293 | yes | 3.0 | 40.0 | -37.0 | -30.0 (50) | 35 |
| h102 | yes | 15.0 | 50.0 | -35.0 | -36.5 (50) | 80 |
| h135 | yes | 2.8 | 80.8 | -78.0 | -72.9 (50) | 65 |
| h152 | yes | 3.2 | 45.0 | -41.8 | -37.5 (50) | 92 |
| h222 | yes | 22.0 | 56.0 | -34.0 | -33.8 (50) | 35 |
| h027 | yes | 27.0 | 50.0 | -23.0 | -24.7 (50) | 35 |
| h115 | yes | 9.0 | 82.0 | -73.0 | -70.2 (50) | 35 |
| h137 | yes | 8.6 | 50.0 | -41.4 | -32.7 (50) | 40 |
| h142 | no | 12.6 | 79.0 | -66.4 | -69.3 (50) | 62 |
| h214 | no | 10.2 | 81.0 | -70.8 | -66.6 (50) | 65 |
| h187 | no | 37.2 | 50.0 | -12.8 | -24.3 (50) | 55 |
| h019 | no | 6.0 | 83.0 | -77.0 | -74.3 (50) | 40 |
| h173 | no | 3.0 | 84.6 | -81.6 | -77.3 (50) | 55 |
| h149 | no | 13.0 | 51.0 | -38.0 | -40.3 (50) | 25 |
| h048 | no | 6.2 | 96.6 | -90.4 | -89.6 (50) | 85 |
| h291 | no | 2.8 | 60.6 | -57.8 | -89.7 (50) | 97 |
| h093 | no | 85.0 | 85.0 | +0.0 | +0.4 (50) | 62 |
| h183 | no | 1.0 | 39.6 | -38.6 | -34.9 (50) | 99 |
| h237 | no | 2.4 | 98.0 | -95.6 | -65.1 (50) | 55 |
| h080 | no | 99.8 | 100.0 | -0.2 | -0.4 (50) | 96 |
| h033 | no | 100.0 | 100.0 | +0.0 | +0.0 (50) | 99 |
| h090 | no | 95.0 | 96.4 | -1.4 | -1.2 (50) | 85 |
| h248 | no | 3.2 | 97.0 | -93.8 | -94.0 (50) | 96 |
| h158 | no | 97.0 | 98.8 | -1.8 | -1.8 (50) | 97 |
| h126 | no | 94.8 | 96.2 | -1.4 | -0.6 (50) | 85 |
| h043 | no | 3.0 | 88.4 | -85.4 | -82.9 (50) | 93 |
| h203 | no | 97.2 | 97.4 | -0.2 | -0.6 (50) | 85 |
| h294 | no | 5.8 | 18.0 | -12.2 | -13.5 (50) | 80 |

## Pre-registered reading: **no evidence either way**

# Stage 2 run 2: split analysis

Every arm re-scored on the run-2 test set (40 wrong + 40 right), split by item type and by whether the item's relation web had ≥ 3 contradictions. Thresholds are each arm's existing calibration thresholds; **nothing is fitted**. Arms F and G come from run 2b. Each cell: wrong flagged · right flagged · AUROC [95% bootstrap CI]. Small groups give wide intervals; read them as descriptive.

## type: simpleqa (22 wrong, 19 right)

| arm | wrong flagged | right flagged | AUROC [95% CI] |
|---|---|---|---|
| A | 5/22 | 4/19 | 0.53 [0.35, 0.71] |
| C | 18/22 | 7/19 | 0.72 [0.56, 0.86] |
| D | 10/22 | 6/19 | 0.61 [0.42, 0.77] |
| E | 10/22 | 7/19 | 0.58 [0.40, 0.75] |
| F | 0/22 | 0/19 | 0.50 [0.50, 0.50] |
| G | 17/22 | 10/19 | 0.74 [0.58, 0.88] |
| A0 | 3/22 | 4/19 | 0.52 [0.34, 0.70] |

## type: science (18 wrong, 16 right)

| arm | wrong flagged | right flagged | AUROC [95% CI] |
|---|---|---|---|
| A | 5/18 | 5/16 | 0.56 [0.37, 0.76] |
| C | 3/18 | 2/16 | 0.61 [0.42, 0.79] |
| D | 7/18 | 4/16 | 0.67 [0.47, 0.87] |
| E | 8/18 | 2/16 | 0.72 [0.54, 0.88] |
| F | 0/18 | 0/16 | 0.50 [0.50, 0.50] |
| G | 13/18 | 2/16 | 0.89 [0.76, 0.99] |
| A0 | 6/18 | 7/16 | 0.47 [0.28, 0.67] |

## type: claim (0 wrong, 5 right)

| arm | wrong flagged | right flagged | AUROC [95% CI] |
|---|---|---|---|
| A | 0/0 | 0/5 | undefined (no wrong or no right items) |
| C | 0/0 | 0/5 | undefined (no wrong or no right items) |
| D | 0/0 | 1/5 | undefined (no wrong or no right items) |
| E | 0/0 | 1/5 | undefined (no wrong or no right items) |
| F | 0/0 | 0/5 | undefined (no wrong or no right items) |
| G | 0/0 | 0/5 | undefined (no wrong or no right items) |
| A0 | 0/0 | 0/5 | undefined (no wrong or no right items) |

## contradictions >= 3 (29 wrong, 24 right)

| arm | wrong flagged | right flagged | AUROC [95% CI] |
|---|---|---|---|
| A | 8/29 | 5/24 | 0.52 [0.36, 0.66] |
| C | 19/29 | 8/24 | 0.65 [0.50, 0.79] |
| D | 17/29 | 6/24 | 0.68 [0.51, 0.82] |
| E | 18/29 | 10/24 | 0.63 [0.48, 0.77] |
| F | 0/29 | 0/24 | 0.50 [0.50, 0.50] |
| G | 22/29 | 11/24 | 0.75 [0.61, 0.87] |
| A0 | 6/29 | 5/24 | 0.50 [0.35, 0.65] |

## contradictions < 3 (11 wrong, 16 right)

| arm | wrong flagged | right flagged | AUROC [95% CI] |
|---|---|---|---|
| A | 2/11 | 4/16 | 0.63 [0.41, 0.84] |
| C | 2/11 | 1/16 | 0.75 [0.56, 0.92] |
| D | 0/11 | 5/16 | 0.58 [0.35, 0.82] |
| E | 0/11 | 0/16 | 0.68 [0.49, 0.86] |
| F | 0/11 | 0/16 | 0.50 [0.50, 0.50] |
| G | 8/11 | 1/16 | 0.93 [0.81, 1.00] |
| A0 | 3/11 | 6/16 | 0.48 [0.26, 0.70] |


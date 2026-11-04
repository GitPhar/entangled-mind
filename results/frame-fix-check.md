# Frame check (exploratory, run-2 data only)

Not pre-registered. The locked v2 test set is not touched. See DEVIATIONS.md, D15.

## Camp phases at encode (225 run-2 items with both a yes-leaning and a no-leaning claim)

Percentiles (10 / 25 / 50 / 75 / 90) of the confidence-weighted circular-mean phase of each camp.

| | yes camp: distance from 0° | no camp: distance from 180° | yes–no separation (ideal 180°) | yes camp > 30° off | separation < 90° |
|---|---|---|---|---|---|
| before (as run) | [0.0, 0.0, 0.0, 10.1, 127.0] | [0.0, 0.0, 0.0, 3.1, 36.0] | [0.0, 110.7, 180.0, 180.0, 180.0] | 20% | 20% |
| rigid pin (pin_frame) | [0.0, 0.0, 0.0, 9.1, 130.9] | [0.0, 0.0, 0.0, 2.2, 38.4] | [0.0, 110.7, 180.0, 180.0, 180.0] | 20% | 20% |
| anchors × λ (the correction) | [0.0, 0.0, 0.0, 0.0, 4.4] | [0.0, 0.0, 0.0, 0.0, 2.3] | [147.1, 180.0, 180.0, 180.0, 180.0] | 7% | 7% |
| anchors → ∞ (reference) | [0.0, 0.0, 0.0, 0.0, 0.0] | [0.0, 0.0, 0.0, 0.0, 0.0] | [180.0, 180.0, 180.0, 180.0, 180.0] | 0% | 0% |

A rigid rotation only fixes a frame that has *rotated*; it cannot change the separation, so camps the solver pulled together stay together. Scaling the lean anchors by λ = max(1, largest total coupling of any claim), in the phase solve only, is the correction (fixed before its AUROC was computed). The ∞ limit puts every leaning claim exactly on the axis and is shown for reference.

## Run-2 test set (40 wrong + 40 right): exact noiseless conflict scores

| arm | before (as run) | rigid pin | anchors × λ (the correction) | anchors → ∞ (reference) | archived run-2 (1,000 shots; C noisy) |
|---|---|---|---|---|---|
| A0 | 0.49 [0.35, 0.62] | 0.49 [0.36, 0.62] | 0.47 [0.34, 0.61] | 0.47 [0.33, 0.60] | 0.49 |
| C | 0.68 [0.56, 0.79] | 0.68 [0.56, 0.79] | 0.67 [0.55, 0.78] | 0.67 [0.54, 0.78] | 0.68 |

# Direction 3 follow-up: predict each format from the other five (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before the fit was run. DEVIATIONS.md D46. Cost $0: archived data only (`results/gm3b-calls.json`, last night's six-format run), no API calls.

**What was already known at freezing:** last night's held-out-*repeat* result (`results/gm3b-format-invariance.md`).
- Format-specific credences win on 86% of claims, with ΔLL +19.4 per claim.
- The fitted links.
- The rank correlations between formats (0.37–0.74).
- Split-half discordance of 4–8% within a format, against 21–35% across formats.

No held-out-format prediction has been computed.

## 1. In plain English

Last night's test asked whether one belief per statement explains every format's answers to within repeat noise, and it does not. A different question matters as much: is that one belief still *useful*? If we know how the model answers a statement in five formats, can we predict its answer in the sixth?

Smolin & Wilder (2026) used this criterion and found single beliefs useful for other capable models. Here, each format is predicted from the other five and compared with the best possible prediction, which is the same format's own other half of repeats.

## 2. Design

- **Folds:** the 40 items are split into 5 folds of 8 (`random.Random(4646)` shuffle of the sorted item list). Each item's 4 claims stay in its fold.
- **The fit, for each held-out format f and fold k:**
  - The one-credence model L1 is fitted exactly as specified in `experiments/gm3b-format-invariance.md` (§4, same code).
  - It uses the even repeats only.
  - The claims outside fold k contribute all six formats. The claims in fold k contribute the other five formats only.
  - So format f's link is learned from other claims, and each test claim's credence μ_c comes from its other five formats.
- **The prediction, for each test claim:**
  - The predicted mean response to format f on its **odd** repeats, from μ_c and format f's link, averaged over those repeats' prices and positions.
  - For F1 and F5 this is the expected rating, by 20-node Gauss–Hermite quadrature on the logit-normal link. For F2–F4 it is the predicted probability. For F6 it is the expected scale step.
- **The ceiling:** the claim's own mean response to format f on its **even** repeats, used as the prediction of the odd-repeat mean. That is format f's split-half reliability. It uses the same amount of data from the same repeats as the cross-format prediction.

## 3. Statistics

- **Per format f, across the 160 claims:**
  - R²_cross(f), the squared Pearson correlation between the cross-format prediction and the observed odd-repeat mean;
  - R²_ceil(f), the same for the ceiling;
  - Q_f = R²_cross(f) / R²_ceil(f).
  - Spearman versions are reported too.
- **Primary:** the mean Q over the six formats (Q can exceed 1, because five formats can predict a claim's mean with less noise than half of one format's repeats), with a 2,000-resample item-cluster bootstrap CI (seed 4647). Predictions are held fixed, and the correlations are recomputed on each resampled set of claims.
- **For comparison with Smolin & Wilder:** the absolute R²_cross per format and its mean. They reported held-out R² of 60–90%.

## 4. Pre-registered reading

- **A usable single belief:** the CI of mean Q lies wholly above 0.75. One credence recovers most of what is reproducible in each format. Last night's "no single credence" then means a belief that each format bends in its own reproducible way.
- **Little format-free belief:** the CI lies wholly below 0.5. Most of each format's reproducible answer cannot be recovered from the others. That is construction by format.
- **Partial:** otherwise.

## 5. What it cannot do

- **One model, one context per claim**, as before.
- **Monotone links only.** A held-out format with a non-monotone relation to the others would be missed by any one-credence model. That is part of what is being tested.

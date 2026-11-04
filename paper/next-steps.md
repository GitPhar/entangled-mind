# Next steps after version two

Written 2026-11-03. It reflects `main` at 92048fb. Numbers are copied from `results/`. Anything not yet in `results/` is marked [PENDING].

## 1. Where the project stands

**Version two failed its primary criterion. The learned quantum encoding ties its classical twin on error prediction.** Results on the locked test set (`results/v2-run-1.md`; 32 wrong, 177 right):

| model | AUROC [95% CI] |
|---|---|
| A2, learned quantum encoding (9 parameters) | 0.83 [0.75, 0.90] |
| F2, learned classical twin (9 parameters) | 0.84 [0.78, 0.89] |
| G, the model's self-reported confidence (no fitting) | 0.83 [0.78, 0.89] |
| L, relation-web features (linear) | 0.79 [0.70, 0.86] |
| H, hedge baseline | 0.67 [0.57, 0.76] |

- **The primary test failed.** The paired A2 − F2 difference is −0.007 [−0.079, +0.062]. The primary required A2's lower bound to exceed F2's upper bound.
- **A2's couplings fitted small.**
  - k_sup = 0.12 and k_con = 0.21, against 1 in version one, with a single Trotter step.
  - Zero couplings do as well as the fitted ones, and v1-strength couplings lower train AUROC from 0.82 to 0.61; the equally good candidates with large couplings read out near the Z axis, where couplings barely matter.
  - The plain statement is that **error prediction on this task shows no detectable dependence on the entangling structure.**
- **F2 fitted to a static model.** It chose zero sweeps, so it uses no dynamics.
- **The hard-pool held-out set (secondary) favours A2,** 0.82 against F2's 0.71. But G also scores 0.82 there, and with A2's couplings near zero the gain comes from A2's learned single-claim geometry, not from entanglement.

**Earlier results point the same way.**
- **Stage 2, run 2 (version one, pre-registered).** Test-set AUROC: entangled arm A 0.55, no-entangling arm C 0.68, shuffled web D 0.65, contradiction count E 0.64, noiseless A0 0.49 (`results/stage2-run-2.md`).
- **Exploratory stage-by-stage readout, not pre-registered** (`paper/window-vignettes.md`):
  - In the exact state, arm A's AUROC falls from 0.63 at encode to 0.49 after evolution.
  - The same circuit without entangling gates keeps 0.68.
  - The entangling and coupled-evolution steps lose the signal.
- **Witness on `ibm_fez`.** The belief states really are entangled on hardware, with negativity 0.147, 0.063 and 0.067 on 3 items, all certified. That shows the circuit does what it was built to do. It says nothing about whether entanglement models judgment.
- **Experiment 3 (order effects, yes/no answers): inconclusive.**
  - The base model gave the same answer in all 5 baseline runs for 85% of items.
  - Only 27 of 218 item-pairs differed between orders at all.
  - Order-label permutation test: p = 0.24.
- **Experiment 4, run 1 (Yearsley & Trueblood):**
  - 7 of 16 items show a reliable conjunction fallacy in 0–100 ratings, and there are no double fallacies.
  - The binary QQ phase saturated completely (the conjunct was answered "no" 100 times in 100), so R2 was untestable.

**Still running or prepared, but not yet in `results/`:**
- version 2.1, the honest-hedge encoding (Addendum B/C, D16): [PENDING]
- the claude-sonnet-5-5 replication (D18): [PENDING]
- experiment 4 run 2 (D17): [PENDING]

## 2. Why the project pivots to sequential judgment

**The data.**
- Two pre-registered tests, a fixed encoding and a learned one, agree.
- The error signal in the deliberation record is carried by single-claim quantities: confidence, lean and geometry. A classical score captures them as well as the quantum one, and so does the model's own stated confidence.
- When the fit was free to use coupling, it found no use for it.
- Further error-flagging variants (new readouts, new couplings, new pools) would be fishing in a pond the project has already drained. We stop here.

**The literature.** The evidence for quantum models of cognition was never about classifying a single judgment. It is about what one judgment does to the next. Each of these effects is predicted by the quantum account, and none is produced by the matched classical model in the papers that report them:
- Question-order effects that obey the parameter-free QQ equality: Wang & Busemeyer 2013; Wang et al. 2014, across 70 national surveys and 2 lab studies.
- Intermediate decisions that violate the law of total probability: a 10-point violation for narrow faces in Busemeyer, Wang & Lambert-Mogiliansky 2009; the disjunction effect in Pothos & Busemeyer 2009.
- Interference of a choice on later confidence: Kvam et al. 2015, interference coefficient −0.11 [−0.18, −0.04], with 7 of 9 participants favouring the quantum random walk.
- Evidence-order effects in inference: Trueblood & Busemeyer 2011.

Error flagging was the project's own extension, and it has now been tested and found to add nothing.

**The gap in work on language models.**
- Language models do show the raw phenomena:
  - recency in evidence order, and intermediate ratings that shift final ones (Bessis et al. 2026);
  - single but not double conjunction fallacies (Imannezhad, Pothos & Wills 2026; our experiment 4);
  - violations of total probability across partitions (Wolf et al. 2026).
- No published study gives a dispersed, counterbalanced test of the QQ equality or of choice-on-confidence interference in a language model. Kang (2026) ran into the same saturation we did.
- That gap is a test worth running whichever way it comes out.

**The measurement lesson.** Binary truth questions saturate in this model, while graded ratings move. Both remaining tests therefore use graded ratings, and they compute the binary constructs from a pre-registered cut.

## 3. The two remaining pre-registered tests

### 3.1 Experiment 4, run 2: graded QQ / R2 (`experiments/exp4-yearsley-trueblood.md`, Addendum; D17)

**Design.**
- Run 1's 7 fallacy items.
- Two-turn conversations with graded ratings in both orders: X → XY, Y → XY, X → Y and Y → X, with 20 repeats per cell.
- Default temperature: the API rejects an explicit one for this model.

**Tests.**
- The graded order effect o.
- The fallacy f.
- The order effect beyond anchoring, o − o_rep.
- The Yearsley & Trueblood rule R2.

**Cost.** About $0.05, with a $10 cap. Designed and not yet run.

**What it can and cannot show.**
- Meeting R2 is consistent with the quantum model **or** a sequential-update classical model, and rules out only the static classical twin (D11).
- It is cheap and quick, and it tells us whether graded ratings carry order structure at all before experiment 5 spends more.

### 3.2 Experiment 5: sequential, context-dependent judgment (`experiments/exp5-sequential-judgment.md`, draft on this branch)

**Design.**
- 40 hard-pool questions where the deliberation record has at least 4 competing claims.
- On each, the base model rates 4 of its own competing claims and then the main question, all on 0–100, in 12 chain types:
  - Latin-square orders;
  - each claim omitted in turn;
  - main question only;
  - main first and repeated;
  - an intermediate yes/no choice against a matched filler.
- Separate adjacent (claim, main) pairs test the QQ equality.

**Models.**
- **A5:** the existing encoder read as a dynamic belief state. One evolution step per question, and a Lüders update on each observed rating.
- **F5:** its commuting-limit Markov/Bayes twin, with the same 5 parameters and the same likelihood update.
- The two differ only in coherence and non-commutation.

**Primary test.** Held-out one-step-ahead prediction error, split by chain, with 8 items held out entirely. The verdict also needs one of two parameter-free signatures:
- QQ q ≈ 0 while order effects exceed 0.10;
- or Kvam-style interference: a less extreme final rating after a choice than after a filler. A commitment mechanism predicts the opposite sign.

**Gates and cost.** Pilot dispersion gates stop the run if the model's ratings do not move with sequence. Cost about $1.85, with a $4 cap. No QPU time.

## 4. What each outcome would mean, decided now

| outcome | what we write |
|---|---|
| Exp 5 **untestable** (pilot gate fails) | This model's graded judgments do not respond to sequence, so quantum probability has nothing to describe in them under these formats. Together with v2, the project's answer is a null on both the static and the sequential question for this model. |
| Exp 5 **tie** or **classical** | Quantum probability adds nothing over a matched classical updater, in sequential judgment as in error prediction. A clean, pre-registered negative result, worth publishing as such. |
| **Quantum fits better, no unique signature** | A modest positive. The quantum model is a better *description*, but nothing in the data excludes the classical family. |
| **Quantum supported** | The first dispersed, pre-registered evidence that a language model's sequential judgments show a quantum-probability signature. Only then would we request QPU time, for a separately pre-registered hardware follow-up. Even then, the claim concerns the probability model that describes the behaviour, not the network's physics. |

Experiment 4 run 2 is read alongside. Its R2 result can support "sequential, not static" but cannot by itself pick quantum over classical.

## 5. Order of work

1. Run experiment 4 run 2, which is already pre-registered (~$0.05).
2. Sean reviews the experiment 5 draft. Then it is frozen in a commit, together with `experiments/split-exp5.json`, before any call.
3. Run the experiment 5 pilot (~$0.20) and apply gates G1 and G2.
4. If G1 passes, make the full run (≈ $1.65 more, $4 cap in code).
5. Update the papers: version three of both drafts takes the verdicts from §4 as written. The v2 drafts' error-flagging results stay as the first, negative half of the story.

**Not planned:** more error-flagging encodings, new QPU runs before a signature exists, or any post-hoc analysis promoted to a claim. The exploratory hedge-count result in `paper/window-vignettes.md` was already tested as baseline H in v2: 0.67 on the locked test.

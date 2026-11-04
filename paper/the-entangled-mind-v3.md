# The Entangled Mind: Quantum Cognition as a Cognitive Architecture for Language Models

**Sean Pharris**
Independent Researcher, Colorado Springs, Colorado
Version 3, November 3, 2026, updated November 4 with the gold-map tests (version 2: November 3, 2026; version 1: October 25, 2026). Dates and times are local, America/Denver (MST, UTC−7).

**Author note.** Sean Pharris is an independent researcher with a background in psychology and philosophy and professional experience in prompt engineering and AI pipeline development.

**Versions.**
- Version 1 was a pre-registration-style proposal.
- Version 2 reported the first experiments.
- This version reports everything on the project's `main` branch as of the evening of November 3, 2026: the re-scoring of run 2, the split analysis, the learned encodings (v2 and v2.1), experiments 3 and 4, the IBM calibration at job time, and the second-model replication, which completed the hard pool and then stopped on a second refusal.
- It reports experiment 5, the pre-registered test of sequential, context-dependent judgment, and the two single-scale follow-ups: experiment 4 run 3 (untestable: the model resists provided first ratings) and experiment 5 run 2 (order effects survive; the QQ near-zero did not).
- The November 4 update adds the overnight gold-map tests (Section 5.13). Each was pre-registered before its analysis or first call, and each is reported as it landed.

**Number conventions.**
- **Results** are quoted verbatim from the files in `results/` of the project repository (https://github.com/GitPhar/entangled-mind).
- **Design constants** are cited to the pre-registration files, `DEVIATIONS.md` or the code.
- **Results that do not exist yet** are marked [NOT RUN], [RUNNING] or [NOT SCORED].
- **Reproducibility.** `experiments/reproduce.py` rebuilds every results table from the archived JSON with the network blocked, and its output matches the committed tables byte for byte above their Reading sections.
- **Exploratory** analyses (anything not pre-registered) are labelled as such wherever they appear.
- **Other people's numbers** come from the cited papers. Where we recomputed them, we say so.

Correspondence: seanm.pharris@gmail.com.

---

## Abstract

Do machines need quantum minds? Quantum-cognition models describe human judgment with amplitudes, interference and entanglement rather than classical probabilities. We built one into a machine that judges, and tested it against classical twins under pre-registered rules.

**Pipeline.**
- For each yes/no question, a language model (`claude-haiku-5-5`) answers and briefly explains its considerations for and against.
- The claims in that explanation are extracted, and every pair is judged to support, contradict or be unrelated to the other.
- The resulting web is encoded as one entangled state on 5–16 qubits, evolved briefly, and measured in a "yes"-oriented basis.

**Error prediction: negative, and robust.** The main question was whether the quantum state flags the model's wrong answers better than classical controls.
- **The fixed encoding fails.**
  - On an 80-item test set (40 wrong, 40 right), the entangled readout scored AUROC 0.55 [0.41, 0.67].
  - The same circuit without entangling gates scored 0.68, a shuffled relation web 0.65, and a plain contradiction count 0.64.
  - The model's own stated confidence scored 0.82 [0.71, 0.90], above every fixed structural arm (A–F).
  - The real relation web scored below 99% of 200 random webs of the same strengths.
- **The learned encodings tie their classical twins.**
  - Version 2: the learned encoding (9 parameters) scored 0.83 against 0.84 for a classical twin with the same parameters and fitting rule. Its couplings fitted small: strong couplings lowered the fit, and zero couplings did as well as the fitted ones.
  - Version 2.1, which stops forcing hedging claims into camps: 0.84 against 0.82. Both fits set the new hedge term's weight to 0, and simulated hardware noise changed nothing detectable (+0.000 [−0.020, +0.023]).
  - Self-reported confidence scored 0.83 on the same locked test set.
- **Secondary transfer to a second model.** The frozen v2 models were scored offline on `claude-sonnet-5-5`'s hard-pool errors. A2 scored 0.90 against F2's 0.82, a paired +0.078 [+0.018, +0.137].
  - **A pre-registered ablation identifies the edge** (Addendum D). It is single-claim readout geometry, and a classical model carries it.
    - Setting A2's couplings to exactly 0 changes nothing: −0.006 [−0.029, +0.013].
    - A classical twin given A2's per-claim tilted readout (F2+) matches A2: 0.90, and +0.004 [−0.032, +0.042].
  - **Sonnet's own stated confidence scores 0.91 [0.86, 0.95]**, level with A2. Self-report is again not detectably different from the best structural model (G − A2 = +0.008 [−0.061, +0.080]).
  - **The same holds for Haiku's earlier held-out edges** (Addendum E). The frozen F2+ is not detectably different from A2 and A2.1 there. No positive quantum-vs-classical difference in error prediction is significantly larger than a classical model with the same per-claim readout achieves (F2+ recovers 1.05 [0.73, 2.50] of the Sonnet edge and 0.68 [0.20, 1.21] of the held-out A2.1 edge).

**Hardware: positive, and narrow.**
- On IBM's `ibm_fez`, a pre-registered witness certified pairwise entanglement in the 3 most-entangled belief states (3 of 3 certified; one pair decoupled from its state), negativity 0.147, 0.063 and 0.067, in 44 QPU seconds.
- Calibration logged at job time shows median CZ error of about 2 × 10⁻³ and median T₁ of 134–146 µs.
- The device washed the states out more than its noise model predicts.

**Sequential judgment: real order effects, no quantum signature.** The evidence for quantum cognition is about one judgment changing the next.
- **Yes/no answers.** The model is near-deterministic: in experiment 3 it gave the same answer in all 5 runs on 85% of items, and experiment 3's design detected no order effect (p = 0.24). Experiment 4 run 1's yes/no audit did show order shifts in the first conjunct (OE_X up to +0.67).
- **Graded ratings.**
  - Experiment 4 found single conjunction fallacies (7 of 16 items) and no double fallacies.
  - Order effects of about +0.10 satisfied the Yearsley–Trueblood bound R2 on 3 of 3 scored items.
  - The pre-registered estimator meant to separate a quantum account from anchoring on the first answer turned out to be close to circular, so the mechanism is undetermined.
- **Experiment 5** (pre-registered, 12,600 conversations, $1.93). On 40 hard-pool questions the model rated chains of its own competing claims, in many orders.
  - Order effects are real: 40 of 80 claim–question pairs survive a Holm-corrected permutation test (60 exceed 0.10, about 27 by chance).
  - **The verdict is classical (re-issued, D52; first issued as a tie, now superseded).** The QQ signature is contradicted on the single scale direction (mean q −0.345 [−0.517, −0.181]), and a dynamic quantum belief state built from the encoder and a matched classical updater could not be told apart on the test chains (F5 − A5 = +67 [−34, +212] rating points²).
  - Neither parameter-free quantum signature appeared. The QQ statistic was near zero only when the two scale directions were pooled; on one scale it is not supported (q = −0.146 [−0.439, +0.137], run 2). A mid-chain choice did not detectably change later confidence (Δ_K = +0.29 [−1.12, +1.65]).
  - Where the quantum state predicted better (on 8 held-out items), a dephased version, which is a classical Markov chain, did equally well.

**What remains.** Experiment 4 run 3, the last test of the original programme, was untestable: the model resisted provided first ratings.

**After the programme: six gold-map tests on November 4,** each pre-registered before its analysis or first call; two reanalyse archived experiment-5 data (Section 5.13).
- **Asking is invasive.** Earlier questions change later ratings in 5 of 6 comparisons on the archived experiment 5 data. A midway yes/no choice is the exception: no effect was detected (p = 0.16).
  - The model's state is its copyable conversation, so it has a definite state at every turn. The effects therefore measure how asking disturbs it, not an absence of definite judgments (`paper/clonable-minds.md`).
- **Question and record both act.** The order effect survives hiding the model's earlier answers: on all 40 items the ratio is 1.23 [0.75, 2.02] against a bar of 0.5, though the order pattern under hiding is largely different from the shown one. Planted own answers pull later ratings. The model's consistency on a repeated question depends on seeing its answer (86% agreement shown, 36% hidden, against 77% between fresh first answers).
- **No privileged self-knowledge.** Authorship does not help a model judge its own errors: judge × author interaction −0.055 [−0.103, −0.007]. Sonnet judges Haiku's errors better than Haiku does.
- **No single credence.** Across six question formats, format-specific credences predict held-out answers better for 86% of claims. The formats rank the claims differently, four to six times beyond repeat noise (an exploratory baseline).
- **Evidence seeking is mixed.** The model's choice of which claim to check beats chance for informative and confirming checks alike; when they differ, whether it prefers either is undecided (the estimates lean confirmatory).
- **The scale gap shows no detectable error signal.** The 37-point scale-direction gap scores AUROC 0.48 [0.28, 0.66] for the model's errors: no evidence either way on 40 items.

**Keywords:** quantum cognition, entanglement, language models, error prediction, order effects, pre-registration, classical twin, entanglement witness

---

## 1. Introduction

Physics has a mathematics of states that cannot be decomposed into parts: entanglement. Psychology has three decades of evidence that human judgment departs from classical probability in ways that mathematics describes well (Busemeyer & Bruza, 2012; Pothos & Busemeyer, 2013; Bruza et al., 2015). Artificial intelligence has built machines that produce something like deliberation, and has built them on classical probability.

The first version of this project proposed putting the three in one room. Take the competing considerations behind a language model's answer, hold them as one entangled state rather than a list of weights, let the state evolve under their mutual support and contradiction, and read the answer from a measurement. It argued this could change how a machine judges, and could give quantum cognition its first working mechanism rather than a descriptive fit. It also said that "a clean negative result is still a contribution."

This version reports a clean negative result on the question the project was built to answer, and an open question in the place it should have looked first.

**The negative result.** As an error detector, the quantum state adds nothing detectable.
- With fixed constants, it is worse than every classical control.
- With learned constants, it ties a classical twin given the same parameters and fitting rule.
- In every comparison, the model's own one-line statement of confidence matches or beats both.

The search did not stop at the first failure. It went from fixed to learned encodings, then to an "honest hedge" encoding, then to a second base model. That replication collected the hard pool and then stopped on a second refusal. The frozen v2 models were later scored on its hard-pool records offline, without self-report (Section 5.11).

**The sequential question.** The places where quantum cognition has its evidence are sequences of judgments: question order, intermediate decisions and evidence order. Error flagging is not one of them. Our first sequential experiments were limited by the base model's near-deterministic yes/no answers and by one flawed estimator. Experiment 5 then tested sequential judgment with graded ratings. The order effects were real, and the quantum model did not detectably outpredict a matched classical one.

---

## 2. Related work

A fuller version, with every paper's design, numbers and limitations, is in `paper/related-work.md`. The sequential-judgment literature behind experiment 5 is summarised in `experiments/exp5-sequential-judgment.md`, §2.

**Order effects and the QQ equality.** Asking two questions in different orders changes people's answers.
- Wang and Busemeyer (2013) derived a parameter-free constraint that projective quantum models impose on questions asked back to back: the QQ equality. Four Gallup surveys satisfied it (Clinton/Gore q = −0.003, Gingrich/Dole −0.003, White/Black −0.019). Rose/Jackson, where background text intervenes, failed as predicted (q = +0.151).
- Wang, Solloway, Shiffrin and Busemeyer (2014) extended this to about 70 national surveys. Order effects were present, and q did not deviate from zero.
- Boyer-Kassem, Duchêne and Guerci (2016a) showed that the same datasets violate Grand Reciprocity, a stronger condition every non-degenerate quantum model must meet.
- Khrennikov, Basieva, Dzhafarov and Busemeyer (2014) showed that order effects combined with repeat-consistency are incompatible with projective measurement. Non-projective quantum instruments resolve this (Ozawa & Khrennikov, 2020, 2021; Fuyama, Khrennikov & Ozawa, 2025), but at the cost of the QQ equality's predictive edge.

**Sequences of judgments.** The strongest human evidence for quantum models is about what one judgment does to the next.
- **Intermediate decisions.** Asking for a categorisation first changed a later decision, and violated the law of total probability by 10 points for one face type (Busemeyer, Wang & Lambert-Mogiliansky, 2009).
- **The disjunction effect.** In the prisoner's dilemma, people defect less when the opponent's move is unknown than in either known condition. Any Markov model must treat the unknown case as a mixture of the known cases, so it cannot produce this (Pothos & Busemeyer, 2009).
- **Choice and confidence.** A choice made in the middle of random-dot evidence accumulation made later confidence less extreme (interference coefficient −0.11 [−0.18, −0.04]). The quantum random walk was favoured over a Markov random walk with the same parameters by a group log Bayes factor of 1,713 (Kvam, Pleskac, Yu & Busemeyer, 2015).
- **Evidence order.** Order effects in legal and medical inference fitted a quantum model as well as or better than parameter-matched belief-adjustment models (Trueblood & Busemeyer, 2011; Hogarth & Einhorn, 1992).
- **A counterpoint.** Busemeyer, Wang and Townsend (2006) found that a Markov random walk fitted response-time data better than its quantum counterpart.

**Conjunction fallacies and co-occurrence.** In probability formats, 85–90% of people rank "Linda is a bank teller and is active in the feminist movement" above "Linda is a bank teller" (Tversky & Kahneman, 1983). Frequency formats cut this to 0–25% (Fiedler, 1988; Hertwig & Gigerenzer, 1999).
- The quantum account explains single fallacies and forbids double ones (Busemeyer, Pothos, Franco & Trueblood, 2011).
- Yearsley and Trueblood (2018) predicted that order effects and fallacies should co-occur. In 1,200 participants they found recency effects in all 10 comparisons, single fallacies in 37 of 40, and no double fallacies.

**The flexibility critique.** The commentaries on Pothos and Busemeyer (2013) argued that the freedom to choose compatibility, dimension, state placement and processing order lets quantum models fit opposite patterns. We take this as the design constraint for our work. Our state is built from the model's claims before any outcome is seen, and every quantum arm has a classical twin.

**Language models.**
- **Bell-type values and coherence.**
  - Aerts et al. (2025/2026) report CHSH values up to 4 for chat models. We recomputed their tables (version 2 of this paper), and under Contextuality-by-Default every one of those datasets, human and model, is non-contextual.
  - LLM probability judgments break probability identities (Zhu & Griffiths, 2024) and the law of total probability (Wolf et al., 2026).
  - GPT-5 is nearly coherent, and its conjunction fallacies are almost all single (Imannezhad, Pothos & Wills, 2026).
- **Sequential effects.**
  - Evidence order and an intermediate rating shift final ratings in GPT-4o and GPT-5.2, though not in the human pattern (Bessis et al., 2026).
  - Earlier outputs left in context act as anchors (Echterhoff et al., 2024).
  - Measurement artefacts are large: answer-option position and label effects (Dominguez-Olmedo, Hardt & Mendler-Dünner, 2024; Rupprecht, Ahnert & Strohmaier, 2025), and dependence on presentation mode (Kreutner et al., 2025).
- **The closest precedent.** Kang (2026) audited an LLM's sequential answers against the QQ equality and found near-deterministic distributions on 17 of 18 pairs, which is the saturation that also limited our experiments 3 and 4.

**Where this leaves us.** No study we found gives a dispersed, counterbalanced test of the QQ equality or of choice-on-confidence interference in a language model.

---

## 3. Method as run

### 3.1 Items and base models

| pool | items | source | base model | wrong | file |
|---|---|---|---|---|---|
| standard (run 1) | 60 original + 75 computational extension (D4) | author-written puzzles and misconceptions; code-verified computations | `claude-sonnet-5-5`, effort `xhigh` | **0** of 117 answered | `results/pool-run-1.md` |
| standard (run 2) | 125 | as above | `claude-haiku-5-5`, default effort (D5) | **4** of 125 | `results/pool-run-2.md` |
| hard (run 3) | 300 (D6) | 120 SimpleQA, 120 MMLU-Pro physics/chemistry, 60 author-written claims | `claude-haiku-5-5` | **44** of 300 | `results/pool-run-3.md` |
| training, v2 (run 5) | 1,048 (D9) | SimpleQA, MMLU-Pro biology/engineering/physics/chemistry, computed puzzles, verified claims | `claude-haiku-5-5` | **158** of 1,048 | `results/pool-run-5.md` |
| hard, second model (run 4) | 300 planned (D18) | the hard pool | `claude-sonnet-5-5`, default effort | **30** of 298 answered (299 processed, `h101` excluded after a refusal, D20–D21; 1, h018, excluded when the extractor returned a single claim). L, H, A2 and F2 scored offline with frozen v2 parameters (D27); G scored with 298 Sonnet calls, $0.88, no refusal (D28) | `results/pool-run-4.md`, `results/sonnet-replication.md` |
| training, second model (run 6) | locked-test questions first (D18) | the training pool | `claude-sonnet-5-5` | [HALTED] after 82 items, 7 wrong, on a second refusal (D25) | `results/refusal-sonnet-replication-2.md` |

Every item records its source and licence. Anthropic API spend through the training pool was $16.19 (`results/api-usage.md`). Experiments 3 and 4 add $1.63, $0.23 and $0.04. The Sonnet replication cost $4.07 (hard pool, including the $1.39 spent before the first stop) and $1.10 (training pool, before the second stop). Experiment 5's pilot cost $0.21.

### 3.2 Pipeline

For every question:
1. **Base call** (`claude-haiku-5-5`, adaptive thinking). The model answers with a brief explanation of the main considerations for and against, ending in `FINAL ANSWER: YES/NO`. Thinking content is archived and never sent to any other call (D1–D3).
2. **Extractor** (`claude-sonnet-5-5`). The visible answer is presented as a document, and its distinct claims are listed as `{text, confidence, lean}`, with 5–16 claims kept.
3. **Relation judge** (`claude-haiku-5-5`). Each pair of claims is labelled `supports`, `contradicts` or `unrelated`, with a strength.

### 3.3 Encoding and readout (version one, pre-registered, fixed)

- **Qubits:** one per claim.
- **Preparation:** RY(θ) with θ = confidence · π/2, then RZ(φ). The phases φ minimise the XY energy E(φ) = −Σ J_ij cos(φ_i − φ_j) − Σ lean_k cos φ_k. Phase 0 is "yes".
- **Entangling:** RZZ(κ · J_ij) on every related pair, κ = π/4.
- **Evolution:** N = 2 Trotter steps of a problem Hamiltonian, −Σ J_ij X_i X_j − Σ lean_i X_i, plus a mixer, −Σ Z_i, with γ₀ = 0.5 and β₀ = 0.4.
- **Measurement:** X basis, 1,000 shots.
- **Readout:** a weighted vote m = Σ w_k x_k, with w_k ∝ |lean_k|.
  - Judgment = yes if P(m > 0) ≥ 0.5.
  - Conflict score = 2 · min(P(m ≥ 1/3), P(m ≤ −1/3)).

**A known defect (D15, found after Stage 2 and before v2's locked-test result).** The phase solve's lean anchors are weak against the relation couplings, so in 20% of the 225 run-2 items with both a yes and a no camp (44 of 300 items) the yes camp sits more than 30° off the readout axis.
- A stronger-anchor solve (`solve_phases_anchored`) fixes most of this.
- It leaves the error-detection AUROCs unchanged: arm A0 goes from 0.49 to 0.47 and arm C from 0.68 to 0.67 (exploratory, `results/frame-fix-check.md`).
- Every archived result uses the solver as run.

### 3.4 Arms

| arm | what runs | conflict / error score |
|---|---|---|
| **A** | entangled circuit, noisy Aer simulator built from `ibm_fez` | as above |
| **B** | the identical transpiled circuit on `ibm_fez` | as above (run only if the simulator gate opens) |
| **C** | A with every two-qubit term removed | as above |
| **D** | A built from a shuffled relation web (same strengths, random pairs) | as above; also a 200-shuffle null distribution |
| **E** | classical, no qubits | total contradiction strength |
| **A0** | A on a noiseless simulator | as above |
| **F** | classical Ising twin: same graph, couplings and fields, exact enumeration | share of the near-minimum energy landscape in strongly opposed camps |
| **G** | the base model's self-reported confidence (0–100) in its answer | 100 − confidence |

Every arm's flag threshold is the 75th percentile of its own scores on a calibration pool. Arms F and G, bootstrap intervals and the shuffle null were pre-registered in Addendum A, after run 2 and before any of those numbers existed.

### 3.5 Version two: learned encoding, and version 2.1

**Version two.**
- **The three models** (`experiments/preregistration-v2.md`, D12), with 9 parameters each including the flag threshold:
  - **A2:** a learned quantum encoding (angle scale, separate support and contradiction coupling scales, Trotter steps N ∈ {0,…,4}, two step scales, a readout-basis angle, the camp threshold τ).
  - **F2:** a learned classical twin (the same graph and priors, heat-bath dynamics, no amplitudes).
  - **L:** a linear score on 8 relation-web features.
- **Fitting:** the same rule for all three. 400 random draws, then hill-climbing of the 10 best for 60 steps on train AUROC, selection on validation AUROC, and a Youden threshold on train.
- **Split:** 60/20/20 with seed 2026. Train has 629 items (95 wrong), validation 210 (31 wrong) and the locked test set 209 (32 wrong). The split was locked before any fitting.
- **Pass criterion:** A2's lower 95% bound must exceed F2's upper 95% bound on the locked test set.
- **Held-out set:** the run-2 hard pool is scored once as a secondary, held-out set.

**Version 2.1, the "honest hedge"** (Addenda B and C, D14, D16).
- Claims with no lean (|lean| ≤ 0.1) are no longer pulled into a camp by the phase solve. They are fixed at phase π/2, are left out of the solve, and keep their couplings.
- A separate uncertainty term, the hedges' share of confidence weighted by a learned λ_h ∈ [0, 2], is added to both A2.1 and F2.1. They have 10 parameters each.
- **Fitting and scoring:** both are fitted noiseless. A2.1 is also scored on the noisy `ibm_fez` simulator. The pass criterion is the same as v2's.
- **H, a hedge baseline with no fitted parameters,** was pre-registered alongside v2.1.

### 3.6 Hardware

- **Backend:** IBM `ibm_fez` (Heron r2, 156 qubits), Open Plan, with a project hard stop at 420 QPU s.
- **Stage 1:** one circuit, to test the hardware path.
- **Entanglement witness** (`experiments/witness.md`, D8):
  - For each of 3 run-2 test items, take the most entangled related pair. Run two-qubit tomography (9 Pauli settings plus 4 readout-calibration circuits, 4,000 shots each) and compute negativity, with 500 bootstrap resamples.
  - An item is certified if the 95% lower bound is above 0; the run succeeds if at least 2 of 3 are certified.
- **Calibration at job time.** Read afterwards from `backend.properties(datetime=…)` for the physical qubits and CZ pairs each as-run circuit used (`results/ibm-calibration.md`). The exact as-run gate lists are exported from IBM's job records (`window/data/hardware/`).

### 3.7 Experiments 3 and 4

**Experiment 3: order effects in yes/no answers** (`experiments/exp3-order-effects.md`, D13).
- **Items and pairs:** 40 run-2 test items, with up to 6 claim pairs each.
- **Conversations:** three turns: consider claim *i*, consider claim *j*, answer the question. 5 conversations per pair and order, plus 5 baselines.
- **Predictions:**
  - Quantum: "considering" a claim is a local evolution, and the predicted order effect comes from non-commuting evolutions.
  - Classical: sequential heat-bath updates of the twin.
- **Primary test:** Spearman ρ(quantum prediction, observed) against ρ(classical prediction, observed).

**Experiment 4: the Yearsley–Trueblood test** (`experiments/exp4-yearsley-trueblood.md`, D11, D17).
- **Items:** 16 conjunction items: Linda and three variants, a name-swapped Linda, and 8 author-written items.
- **Run 1, in two phases:**
  - **Phase 1:** graded 0–100 ratings of P(X), P(Y) and P(X and Y) in both wordings.
  - **Phase 2:** on the items with a fallacy, a binary forced-branch QQ audit.
- **Run 2:** graded ratings in both orders (X → XY, Y → XY, X → Y, Y → X), with 20 repeats per cell.
- **Rules:** R1 (a fallacy needs an order effect); R2 (the order effect on the conjunction is at least the fallacy); R3 (no double fallacies).
- **Reading R2:** meeting R2 is consistent with the quantum model *or* a sequential-update classical model. It rules out only a static classical twin (D11).

### 3.8 Experiment 5: sequential, context-dependent judgment

The design is in `experiments/exp5-sequential-judgment.md`, frozen at D22 before any call. The implementation details (D23–D24) were fixed before any call; the model details (D26) were committed while the full run was collecting (606 of its conversations existed by then), before any fitting or result.

**Items and chains.**
- 40 hard-pool questions, each with at least 4 claims that contradict claims leaning the other way.
- In each chain the model rates 4 of its own competing claims, then the main question, all on 0–100, in 12 chain types:
  - four Latin-square orders;
  - each claim omitted in turn;
  - the main question alone;
  - the main question first and repeated at the end;
  - a mid-chain yes/no choice, against a matched one-word filler (the Kvam contrast).
- 10 conversations per chain, with the scale's anchor direction reversed in half.
- A separate block asks each of 2 (claim, main) pairs back to back, in both orders, 40 times each (the QQ test).

**Models**, with 5 parameters each:
- **A5:** the encoder's state (anchored phase solve, honest hedges), evolved one Trotter step before each question and updated by a Lüders POVM on each observed rating.
- **F5:** its commuting-limit Markov/Bayes twin.
- **Secondary comparators:**
  - D5, the dephased quantum model, which is a classical Markov chain;
  - BA5, a belief-adjustment model of the main ratings;
  - A5 with κ = 0.

**Primary test.** Held-out one-step-ahead mean squared error on 77 test chains, with the paired difference bootstrapped over items. 8 items are held out entirely.

**Parameter-free checks.**
- QQ on pairs whose order effect exceeds 0.10.
- Kvam interference: final folded confidence after a choice against after a filler.

---

## 4. Pre-registration and deviations

The pre-registrations were committed before the data they govern (`experiments/preregistration.md`, `preregistration-v2.md`, `exp3-order-effects.md`, `exp4-yearsley-trueblood.md`). `DEVIATIONS.md` records every change, with its date and reason.

| | what changed | why | effect on interpretation |
|---|---|---|---|
| **D1–D3** | Claims come from the model's *visible* explanation, not its hidden thinking. | The API's `reasoning_extraction` safeguard refused two designs. We redesigned rather than route around it. | Every result concerns the reasoning the model wrote down. |
| **D4–D6** | Computational extension; base model changed to `claude-haiku-5-5`; 300-item hard pool. | Sonnet made no errors, and Haiku few, on the standard pool. | Errors are mostly ignorance (SimpleQA) and multi-step science. |
| **D7** | Arms F and G, bootstrap intervals, the 200-shuffle null (Addendum A). | Added after run 2, before any F, G or null number existed. | Reported as run 2b. |
| **D8** | Witness readout calibration built on the measured physical qubits. | The transpiler could move calibration circuits elsewhere. | None. |
| **D9, D10** | 1,048-item training pool; QPU-seconds ledger fixed. | v2 needs separate training data; a parsing bug. | None. |
| **D11** | Experiment 4 pre-registered; R2 wording corrected before any call. | R2 is not unique to the quantum model. | R2 rules out only the static twin. |
| **D12** | Version two pre-registered; pass criterion read as non-overlapping intervals; fitting on exact noiseless scores. | Before any fitting. | The strongest version of the quantum model is tested. |
| **D13** | Experiment 3 implementation choices. | Logged before any result. | None. |
| **D14** | Hedge baseline H and the v2.1 honest hedge. | Prompted by an exploratory window observation (W4); added before any v2 test evaluation. | The run-2 held-out set is not independent of the suggestion; the locked test set is. |
| **D15** | The phase solver's frame drifts off axis; a stronger-anchor correction was characterised. | Found by inspecting the window. | Archived results keep the as-run solver; AUROCs are unchanged by the fix. |
| **D16** | v2.1 fitted noiseless, evaluated noiseless and on the noisy simulator. | Before any v2.1 fit. | The pass criterion uses the noiseless comparison. |
| **D17** | Experiment 4 run 2, graded, pre-registered; temperature cannot be set for this model. | Run 1's binary phase saturated. | Graded ratings at the default temperature of 1.0. |
| **D18** | Second base model (`claude-sonnet-5-5`) replication set up. | To test whether results depend on one base model. | — |
| **D19** | The pre-registered anchoring estimator in experiment 4 run 2 is near-tautological. | Logged after run 2's results. | The run's pre-registered verdict stands but does not show anchoring; the mechanism is undetermined. |
| **D20** | Sonnet replication stopped on a `reasoning_extraction` refusal of the extractor. | The project's rule: stop at once, reword nothing, retry nothing. | — |
| **D21** | Replication resumed with the refused item `h101` excluded; the extractor is unchanged, and a second refusal stops the run again. | Sean's decision after D20. | The Sonnet hard pool has 299 items. |
| **D22–D24** | Experiment 5 frozen; pilot items clarified (the 5-per-category cap left no further right items, so the next 2 in the uncapped ranking are used); split and runner committed; one pilot item's 4th chain slot filled. | Gaps in the draft's wording, found and fixed before any call. | None on the 40 scored items. |
| **D25** | Sonnet replication stopped on a second `reasoning_extraction` refusal (`t368`, training pool). The scorer was not run, because its arm-G step would make further Sonnet calls. | The project's rule and Sean's instruction. | Arm G cannot be scored on Sonnet. |
| **D27** | Sonnet's 298 hard-pool records scored offline (L, H, A2, F2) with frozen v2 parameters; every API client blocked in code; G not scored; the 82 training-pool records not scored. | Sean's request after D25. | A secondary transfer test, with nothing refitted. |
| **D28** | Addendum D, the coupling ablation A2(κ=0) and the classical twin F2+ with A2's per-claim readout, with its outcome rule fixed in advance; and arm G on Sonnet's hard pool. | To test what the Sonnet edge is. | Outcome 1: single-claim geometry, carried by a classical model (Section 5.11). |
| **D29** | Every date in the repository uses local America/Denver time. The frozen pre-registrations changed only in how the same instants are written. | Sean's instruction. | None. |
| **D30** | Addendum E: the frozen F2+ scored once on Haiku's run-2 held-out set. | To test whether Haiku's held-out edges are also readout geometry. | Outcome 1 (Section 5.11). |
| **D31** | Machine-written timestamps (IBM usage ledger, calibration, job-status log) switched to America/Denver; tables regenerated by their writers. | Sean's time-zone rule. | None; `reproduce.py` still matches byte for byte. |
| **D33** | Experiment 4 run 3 frozen with one stated scale direction; experiment 5 single-scale re-run pre-registered. | Experiment 5's anchor-direction artefact. | Both run once (Sections 5.9 and 5.12). |
| **D32** | Experiment 5's a priori QQ sub-test compared predicted non-commutativity with exact float inequality, so solver round-off ordered the pairs and gave a spurious 28–9. With a 10⁻⁶ tolerance it is 1–2 over 3 items. | Found after results. | The verdict does not use this sub-test and is unchanged. |
| **D34, D35** | Gold-map direction 9 (NSIT on archived experiment 5 data, anchor (a) only) and direction 3's free look (the scale-direction gap against errors) pre-registered, each in its own commit, before analysis. | Sean's overnight brief: six gold-map directions in order, one scale direction for every new design, stop on any refusal. | Section 5.13. |
| **D36** | Direction 1 pre-registered with a judge × author interaction as the primary statistic, matched framing in all four cells, and a recognition check for the paraphrase arm. | Changed from the gold map's sketch before freezing, after full-text reads (Xiao et al.; Panickssery et al.; Ashuach et al.). | Section 5.13. |
| **D36 amendments** | Direction 1's step order changed mid-run, before steps 3 and 4, when Sonnet calls cost more than assumed. A token-cap crash then lost up to $0.20 of calls; token-capped judge calls are recorded as no rating. | Budget. | The paraphrase arm covers 60 of 80 questions and Sonnet's recognition check did not run. The primary result is unaffected. Spend may have exceeded the $3 cap by up to $0.02. |
| **D37–D39** | Gold-map directions 2 (shown / redacted / planted transcripts), 3 (six formats) and 4 (evidence-seeking menus) pre-registered, each in its own commit, before any call. | The overnight brief. Changes from the gold map were made before freezing, after the full-text reads: plants ±15 rather than ±30 (Kumaran et al.); a 7-point verbal scale in place of the reversed scale; a most-uncertain baseline beside EIG. | Section 5.13. |
| **D26** | Experiment 5's model details left open by the frozen text, and the verdict's "contradicted" case, fixed in code. | Committed during full-run collection, before any fit or result. | — |

**On sequencing.** The analysis grew in stages:
- Addendum A came after run 2.
- Version two came after run 2b.
- v2.1 came after an exploratory observation.
- Experiment 4's graded run came after run 1 saturated.

Each addition was committed before it was scored, though some implementation details followed their first calls (D9, D13, D26, D28's code). Even so, every addition after run 2 was designed knowing that run 2 had failed.

---

## 5. Results

### 5.1 Stage 1: the hardware path works

From `results/stage1-run-1.md`.
- **The item:** `q01` (bat and ball), 9 qubits, 33 RZZ gates and N = 0.
- **The circuit:** transpiled for `ibm_fez` to depth 208 with 117 CZ gates. The exact as-run circuit, exported from the job record, has the same counts.
- **The job:** it waited 2 h 50 min in the queue and used 2 QPU s.

| run | P(yes) | judgment | conflict score | distinct bitstrings |
|---|---|---|---|---|
| ideal_sim | 0.294 | no | 0.276 | 235 |
| noisy_sim | 0.251 | no | 0.276 | 284 |
| hardware | 0.502 | yes | 0.666 | 336 |

Hardware washed the state out far more than the `ibm_fez` noise model predicts. Calibration at job time is in Section 5.7.

### 5.2 Stage 2, run 1: standard pool

From `results/stage2-run-1.md`, with 4 wrong and 10 hard-right items.
- **H1** passes (0.86).
- **H2** is underpowered, with only 4 wrong items.
- **H3** is too noisy to call (nominally falsified: A 0.45, C 0.51; dropping one item reverses it).
- **H4** is too noisy to call (nominally fails: A 0.45, D 0.42; dropping one item makes it pass, dropping others falsifies it).
- Contradiction strength E scored 0.69.

### 5.3 Stage 2, runs 2 and 2b: hard pool, 40 wrong + 40 right

From `results/stage2-run-2.md` and `results/stage2-run-2b.md`. The calibration pool has 220 items.

| arm | wrong flagged (of 40) | right flagged (of 40) | AUROC test [95% bootstrap CI] |
|---|---|---|---|
| A  entangled, noisy sim | 10 | 9 | 0.55 [0.41, 0.67] |
| B  entangled, real hardware | not run: simulator gate not met | | |
| C  no entangling gates | 21 | 9 | 0.68 [0.57, 0.79] |
| D  shuffled relation web (one shuffle) | 17 | 11 | 0.65 [0.52, 0.76] |
| E  classical contradiction strength | 18 | 10 | 0.64 [0.52, 0.75] |
| F  classical Ising twin | 0 | 0 | 0.50 [0.50, 0.50] |
| **G  self-reported confidence** | **30** | **12** | **0.82 [0.71, 0.90]** |
| A0 entangled, noiseless | 9 | 11 | 0.49 [0.36, 0.62] |

- **H2 fails**, both under its original controls and with F and G held to the same bar.
- **H3 and H4 are falsified.**
- **The model's own stated confidence is the best of the fixed arms** (its lead over C and D, +0.14 and +0.17, is significant only before a multiplicity correction).
- **The real relation web is worse than random ones.** 200 shuffles of each item's web (the same strengths on random pairs) give a null AUROC with mean 0.62 and central 95% range [0.57, 0.68]. Arm A's 0.55 is below 99% of them (p = 0.99).
- **Arm F is degenerate, as pre-registered.** Its near-minimum-energy window holds 1–16 configurations per item and never contains both camps, so every score is 0. It is reported as is. Redefining F after seeing this would be post hoc.

### 5.4 Split analysis (run 2, nothing refitted)

From `results/stage2-run-2-split.md`, using each arm's existing threshold. The groups are small, so read the intervals as descriptive.

| group (wrong / right) | A | C | D | E | G |
|---|---|---|---|---|---|
| SimpleQA (22 / 19) | 0.53 | 0.72 | 0.61 | 0.58 | **0.74** |
| science (18 / 16) | 0.56 | 0.61 | 0.67 | 0.72 | **0.89** |
| ≥ 3 contradictions (29 / 24) | 0.52 | 0.65 | 0.68 | 0.63 | **0.75** |
| < 3 contradictions (11 / 16) | 0.63 | 0.75 | 0.58 | 0.68 | **0.93** |

- Self-reported confidence has the highest point estimate in every group, tied with arm C in SimpleQA (0.74 vs 0.72).
- The entangled readout is near chance in every group.
- Items whose webs contain many contradictions, where an entangled representation should matter most, are not an exception.

### 5.5 Version two: learned encoding

From `results/v2-run-1.md`. Locked test set: 32 wrong, 177 right.

| model | locked test AUROC [95% CI] | run-2 held-out AUROC [95% CI] |
|---|---|---|
| A2 learned quantum encoding | 0.83 [0.75, 0.90] | 0.82 [0.71, 0.91] |
| F2 learned classical twin | 0.84 [0.78, 0.89] | 0.71 [0.59, 0.82] |
| L relation-web features (linear) | 0.79 [0.70, 0.86] | 0.66 [0.53, 0.77] |
| G self-reported confidence | 0.83 [0.78, 0.89] | 0.82 [0.71, 0.90] |
| H hedge baseline (no fitting) | 0.67 [0.57, 0.76] | 0.77 [0.66, 0.87] |

- **The primary criterion is not met. The learned quantum encoding ties its classical twin.** The paired A2 − F2 difference is −0.007 [−0.079, +0.062].
- **The fit chose weak couplings.** A2's coupling scales fitted to k_sup = 0.12 and k_con = 0.21, against 1 in version one, with one Trotter step. Setting the couplings to 0 costs nothing detectable (−0.009 [−0.029, +0.009]), while v1-strength couplings lower train AUROC from 0.82 to 0.61. Entanglement adds nothing detectable to error prediction here, and at v1 strength it degrades it.
- **F2 also fitted to a static model,** with zero sweeps.
- **The structure of the explanation does not beat the model's self-report.** L scores 0.79 and 0.66, against G's 0.83 and 0.82.
- **On the run-2 held-out set (secondary),** A2 beats F2 by +0.108 [+0.012, +0.215]. But G matches A2 there, and with A2's couplings near zero the gain cannot be credited to entanglement.

### 5.6 Version 2.1: the honest hedge

From `results/v2.1-run-1.md`.

| model | locked test AUROC [95% CI] | run-2 held-out AUROC [95% CI] |
|---|---|---|
| A2.1 honest-hedge quantum (noiseless) | 0.84 [0.75, 0.90] | 0.84 [0.74, 0.92] |
| A2.1 on the noisy `ibm_fez` simulator | 0.84 [0.75, 0.90] | — |
| F2.1 honest-hedge classical twin | 0.82 [0.76, 0.88] | 0.72 [0.60, 0.83] |

- **The primary criterion is not met. The honest-hedge encoding ties its classical twin.** The paired A2.1 − F2.1 difference is +0.017 [−0.064, +0.095].
- **The hedge change did nothing detectable.**
  - **Hedge term:** both fits set the hedge-uncertainty weight λ_h to **0**.
  - **Against v2:** A2.1 is indistinguishable from A2 (paired +0.002 [−0.042, +0.047]), and F2.1 is slightly worse than F2 (−0.021 [−0.044, −0.004]).
  - **The hedge baseline:** H, the exploratory observation that motivated v2.1, scores 0.67 on the locked test set.
- **No detectable effect of noise.** A2.1 noisy minus noiseless is +0.000 [−0.020, +0.023]. A2.1 chose N = 0 and small couplings, so its circuit is shallow and close to a product state.
- **On the held-out set, A2.1 beats F2.1** by +0.116 [+0.013, +0.225], almost all of it on SimpleQA (0.92 against 0.67). With no evolution and weak couplings, the quantum model's distinctive ingredient is its tilted readout basis, which belongs to single-claim geometry, not to entanglement. This set also motivated v2.1, so it is not an independent test (D14).

### 5.7 Entanglement witness, and calibration at job time

From `results/witness-run-1.md` and `results/ibm-calibration.md`. Job `dbl6e1d8mdtc73d5gesg`: 39 circuits × 4,000 shots, 44 QPU s.

| item | pair (physical qubits) | N ideal | N noisy sim [95% CI] | **N hardware [95% CI]** | certified |
|---|---|---|---|---|---|
| `h221` | (0, 6) on 10, 9 | 0.184 | 0.171 [0.157, 0.181] | **0.147 [0.134, 0.157]** | yes |
| `h088` | (5, 6) on 44, 37 | 0.175 | 0.149 [0.138, 0.162] | **0.063 [0.051, 0.075]** | yes |
| `h268` | (5, 6) on 4, 16 | 0.162 | 0.118 [0.105, 0.132] | **0.067 [0.055, 0.081]** | yes |

**3 of 3 items are certified,** and the result holds without readout mitigation.
- The `h221` pair's reduced state is pure, so that test is effectively a two-qubit entangling test.
- The `h088` and `h268` pairs are mixed, so they are entangled with the rest of their belief states.

**Calibration at each job's execution start.** The calibration snapshot is from 2026-11-03 15:31 MST; both jobs ran at 16:06 MST.

| job | qubits used | T₁ median [range] µs | T₂ median [range] µs | readout error median | √X error median | CZ error median [range] |
|---|---|---|---|---|---|---|
| Stage 1 | 9 | 133.5 [87.6, 203.5] | 114.1 [44.6, 191.1] | 6.35 × 10⁻³ | 2.79 × 10⁻⁴ | 2.06 × 10⁻³ [1.50, 2.43] × 10⁻³ |
| witness | 14 | 146.2 [23.0, 272.0] | 116.3 [18.6, 183.9] | 7.81 × 10⁻³ | 2.32 × 10⁻⁴ | 1.97 × 10⁻³ [1.58, 2.36] × 10⁻³ |

- **The device was not unusually bad on the day.** These are ordinary Heron-class numbers.
- **The measured witness qubits include one with T₂ = 33.3 µs.** It is qubit 9, one of the `h221` pair, which nonetheless gave the highest negativity.
- **A rough check of our own,** not a noise model: 117 CZ gates at the median CZ error logged at job time on Stage 1's 8 pairs (2.06 × 10⁻³, `results/ibm-calibration.md`) leave a product of CZ fidelities of 0.786. That ignores idle decoherence and crosstalk. Stage 1's washout to P(yes) 0.50 is far larger than this suggests, consistent with the noisy simulator underestimating the device.
- **Total QPU time:** 46 s.

### 5.8 Experiment 3: order effects in yes/no answers

From `results/exp3-run-1.md`: 2,380 conversations, $1.63.

**Primary: inconclusive.**
- Spearman ρ with the quantum prediction is −0.034; with the classical twin's prediction, +0.082.
- The difference has a 95% CI of [−0.284, +0.060].

**Why: the base model shows almost no order effects to predict.**
- Only 27 of 218 item-pairs show any difference between orders.
- The order-label permutation test gives p = 0.24.
- The model gives the same answer in all 5 baseline runs on 85% of items.

The point estimate leans slightly toward the classical twin.

### 5.9 Experiment 4: conjunction fallacies and order

**Run 1** (`results/exp4-run-1.md`; 5,480 calls, $0.23).
- **Phase 1, graded 0–100 ratings:**
  - 7 of 16 items show a reliable single fallacy: Linda +0.085, and the author-written co05 and co06 at +0.29 and +0.19.
  - **There are no double fallacies (R3).** That is what the quantum account requires, and it matches people.
- **Phase 2, binary:**
  - The QQ phase is fully saturated: the low-probability conjunct was answered "no" in every first-position sample.
  - So **0 items are scored and R2 is untestable.**

**Run 2, graded and in both orders** (`results/exp4-run-2.md`; 1,120 calls, $0.04).

| item | o (order effect) [95% CI] | f (fallacy) [95% CI] | OE_X |
|---|---|---|---|
| co-lin06 (Bill) | +0.118 [+0.103, +0.132] | +0.094 [+0.079, +0.108] | −0.118 |
| co-lin10 (Marta) | +0.103 [+0.093, +0.112] | +0.087 [+0.077, +0.096] | −0.080 |
| co05 | +0.069 [+0.067, +0.072] | +0.041 [+0.038, +0.044] | −0.230 |
| co-lin09 | +0.080 [+0.053, +0.105] | −0.042 | −0.122 |

- **The order effects are real.** Rating the representative conjunct first raises the later conjunction rating. o is reliably positive on 6 of 7 items, at about +0.10 on the largest.
- **R2 holds on 3 of 3 scored items.** Those are the items with a reliable graded fallacy, and on each o ≥ f − 0.05.
- **The pre-registered verdict is "static classical twin (with anchoring) supported". That verdict is not informative (D19).**
  - The anchoring term was pre-registered as a regression of the second rating on the first, across both cells pooled.
  - Those cells differ mainly in their first-rating means, so the slope is about o / (P(X) − P(Y)), and the "order effect beyond anchoring" is about 0 by construction.
  - A within-cell estimate cannot be made, because ratings barely vary between repeats (SD 0.00–0.05).
- **Net.** Graded order effects exist and satisfy R2. This design cannot tell a quantum account from anchoring on the first answer. It cannot tell either from a sequential-update classical model.

**Run 3, a manipulated first rating** (`results/exp4-run-3.md`, `de38306`; frozen with a one-scale amendment in D33, `fbc2fbf`; 6,720 calls, $0.30).
- **Design:** before rating the conjunction, the model was shown another person's estimate for one conjunct, low or high, and asked to accept or revise it. The aim was to move its first rating independently of the item.
- **Verdict: untestable.** The pre-registered manipulation check required the first rating to move at least 10 points between low and high estimates. Only 6 of 32 item-orders passed, and only 1 item (co06) passed in both orders, against the 3 required.
- **The model resists provided first ratings.**
  - Its accept rate is 0% in 17 of 32 item-orders, and its first rating moves toward the provided value by a median of only 9% of the gap.
  - In 5 item-orders, all on the three Linda-family vignettes, a *higher* provided estimate produced a reliably *lower* first rating, down to −0.50 on Marta (co-lin10); the mechanism is not identified.
  - **Followed up on November 4** (`results/bm1-serial-dependence.md`, D44; `results/bm0-source-distance-lag.md`, `e2c3b90`, D47). The same values planted as the model's *own* earlier answer pull its re-rating (slope +0.42 against +0.05 for another person's). Own beats other at 10, 30 and 60 points from the model's view (pooled +0.46 [+0.21, +0.84]), and uptake after three filler turns is not lower (lag 0 − lag 3 = −0.13 [−0.25, −0.00]). Another person's number is ignored rather than resisted (mean uptake +0.02). Run 3's resistance does not carry over to the own-answer framing, though the accept-or-revise wording also differs between the two conditions.
- **The ceiling held.** The conjunction rating almost never exceeded the first rating (at most 10% of conversations).
- **Run 2's order effects only partly replicate under the explicit scale wording.** Bill holds at +0.10, but Marta falls to +0.02 and co05 to +0.04.

### 5.10 Exploratory: what the window shows

These analyses are not pre-registered. They come from `paper/window-vignettes.md`, using exact statevectors on run 2.
- **The error signal is lost at the entangling step.** Reading the conflict score at each stage, arm A's test-set AUROC goes from 0.63 at encode to 0.60 after entangling and 0.49 after evolution. Without entangling gates it rises to 0.68.
- **Hedging claims are forced into camps** by the phase solve. That observation motivated v2.1, which then changed nothing detectable (Section 5.6).

### 5.11 Second base model: collected, then halted

The replication on `claude-sonnet-5-5` (D18) stopped at 102 of 300 hard-pool questions, with 12 wrong, at $1.39. The extractor call for `h101` was refused under `reasoning_extraction` (request `req_011Cgh7v49vVQNR6AgY3EDui`, D20). It is the first refusal since the D3 redesign, after 1,473 Haiku-based items and 102 Sonnet-based ones.

Following the project's rule, the run stopped at once, and nothing was reworded or retried. Sean then decided to drop `h101` and resume (D21).
- **The hard pool completed:** 299 items processed, 1 was excluded for a one-claim extraction, and Sonnet was wrong on **30** of 298 answered, for $4.07. Haiku was wrong on 44 of 300.
- **The training pool (run 6) then stopped** on a second extractor refusal, for question `t368` (request `req_011CghAdzJQ9nFBMocCLUMhf`, D25), after 82 items (7 wrong, $1.10).
- **Both refusals** came on SimpleQA items with Sonnet as the base model. Before them, 1,473 Haiku-based items and 381 Sonnet-based items had passed through the same extractor prompt without one.
- **Per Sean's rule,** the replication is halted, and nothing was retried. The scorer was **not run**, because its arm-G step would make further Sonnet calls.

**Offline scoring (D27, `results/sonnet-replication.md`).** At Sean's request, the already-fitted v2 models were run on Sonnet's 298 archived hard-pool records:
- the parameters were frozen from `results/v2-fit.json`, and nothing was refitted;
- every API client was blocked in code, so no call was made.

Arm G, Sonnet's own stated confidence, was then scored with 298 Sonnet calls under D28, for $0.88 and with no refusal.

| model | Sonnet, hard pool (30 wrong of 298) | Haiku, run-2 held-out (40 / 40), for reference |
|---|---|---|
| A2 learned quantum encoding | 0.90 [0.84, 0.95] | 0.82 [0.71, 0.91] |
| F2 learned classical twin | 0.82 [0.75, 0.88] | 0.71 [0.59, 0.82] |
| L relation-web features | 0.73 [0.64, 0.82] | 0.66 [0.53, 0.77] |
| H hedge baseline | 0.66 [0.56, 0.76] | 0.77 [0.66, 0.87] |
| G self-reported confidence | **0.91 [0.86, 0.95]** | 0.82 [0.71, 0.90] |

- **The models transfer.** Trained on Haiku's errors, they score well above chance on Sonnet's, in the same order as on Haiku's held-out set: A2 > F2 > L.
- **A2 beats F2 on Sonnet's errors.** The paired difference is +0.078 [+0.018, +0.137]. That matches the direction of Haiku's held-out results: v2 +0.108, v2.1 +0.116.
- **This is a secondary transfer result, not a reversal.** On v2's primary test, the locked test set, A2 and F2 tied (−0.007 [−0.079, +0.062]).
- **Self-report again matches the best structural model.** On Sonnet's errors:
  - G − A2 = +0.008 [−0.061, +0.080];
  - G beats the relation-web feature model L by +0.176 [+0.095, +0.257].

**What the Sonnet edge is: the test (Addendum D, D28; `results/sonnet-ablation.md`).** The question was whether A2's edge over F2 on Sonnet comes from its small couplings or from single-claim geometry: the tilted readout α acting on each claim's confidence angle θ and phase φ. The test was pre-registered at 21:03 MST (`f7afd8a`), before any score, with four outcomes fixed in advance. It used two models, with no API calls:
- **A2(κ=0):** A2's frozen parameters with both couplings set to exactly 0, so the state is a product of tilted single-claim qubits. It has 9 parameters, 7 effectively free.
- **F2+:** F2 whose single-claim prior is P(yes) = (1 + sin θ cos φ cos α + cos θ sin α)/2. That is exactly what an uncoupled qubit gives when measured along the tilted axis. F2+ was fitted on the v2 train split only and has 10 parameters.

| model | Haiku locked v2 test (209) | Sonnet hard pool (298) |
|---|---|---|
| A2 (frozen v2) | 0.83 [0.75, 0.90] | 0.90 [0.84, 0.95] |
| A2(κ=0), couplings set to 0 | 0.82 [0.74, 0.89] | 0.89 [0.83, 0.95] |
| F2 (frozen v2) | 0.84 [0.78, 0.89] | 0.82 [0.75, 0.88] |
| F2+, F2 with A2's per-claim readout | 0.85 [0.77, 0.91] | 0.90 [0.84, 0.95] |

| paired difference | Haiku locked v2 test | Sonnet hard pool |
|---|---|---|
| A2(κ=0) − A2 | −0.009 [−0.029, +0.009] | −0.006 [−0.029, +0.013] |
| F2+ − A2 | +0.015 [−0.042, +0.073] | +0.004 [−0.032, +0.042] |
| F2+ − F2 | +0.009 [−0.057, +0.065] | **+0.082 [+0.045, +0.120]** |

- **The pre-registered outcome is outcome 1: the edge is single-claim geometry, and a classical model carries it.** Removing the couplings changes nothing detectable on either set, and F2+ is not detectably different from A2 on both.
- **On Sonnet's items, the per-claim readout feature alone (F2+ − F2, +0.082) accounts for the whole A2 − F2 gap (+0.078).** On Haiku's locked test set it adds nothing detectable, and there A2 and F2 already tied.
- **What the geometry does.** The tilt mixes each claim's uncommitted component (cos θ, large when confidence is low) into its vote. It is a per-claim reweighting by confidence, with no superposition across claims, no interference between them and no entanglement.
**The Haiku held-out edges, tested next (Addendum E, D30; pre-registered in `52e80a0` at 21:49 MST, scored in `a9ab42c`).** The frozen F2+, never refitted and with no API calls, was scored once on Haiku's run-2 held-out set (40 wrong, 40 right).

| model or paired difference | AUROC or difference [95% CI] |
|---|---|
| F2+ (frozen) | 0.80 [0.69, 0.88] |
| F2+ − A2 | −0.019 [−0.073, +0.029] |
| F2+ − A2.1 | −0.037 [−0.089, +0.012] |
| F2+ − F2 | +0.088 [+0.014, +0.167] |
| A2 − F2 (the v2 edge, for reference) | +0.108 [+0.012, +0.215] |
| A2.1 − F2.1 (the v2.1 edge, for reference) | +0.116 [+0.013, +0.225] |

**The pre-registered outcome is outcome 1: the held-out edges are also single-claim readout geometry, carried by a classical model.** F2+ is not detectably different from A2 and A2.1 on this set (−0.019 [−0.073, +0.029] and −0.037 [−0.089, +0.012]), and the readout feature alone recovers most of the gap over plain F2.

### 5.12 Experiment 5: sequential, context-dependent judgment

From `results/exp5-run-1.md` (`75744dc`).
- **The run:** 12,600 conversations including the pilot, $1.93 against the $4 cap, no refusal, and no schema exclusions.
- **Encoder prediction, fixed before any data:** after the anchored phase solve, only 12 of 160 chain claims are off the yes/no axis (|sin Δφ| > 10⁻⁶, maximum 0.424). So for most claims the quantum model predicts no non-commutation with the main question. The pre-registration (§8.6) expected A5 and F5 to be close.

**Primary: tie.**

| model | test chains (77): MSE, all ratings | MSE, main ratings | held-out items (8): MSE, all ratings |
|---|---|---|---|
| A5 quantum belief state | 984.0 | 872.9 | 779.7 |
| F5 classical twin | 1050.9 | 919.5 | 987.0 |
| D5 dephased quantum (a classical Markov chain) | 987.8 | 851.5 | 768.4 |
| BA5 belief adjustment (main ratings only) | — | **827.1** | — |
| A5 with κ = 0 | 1008.4 | 896.5 | 812.9 |
| A5⁰ (a priori, unfitted) | 1088.3 | 920.4 | 922.5 |
| F5⁰ (a priori, unfitted) | 1739.7 | 1706.2 | 1642.6 |

Paired item-bootstrap differences (MSE in rating points²):

| difference | test chains | held-out items |
|---|---|---|
| **F5 − A5 (primary)** | **+67.0 [−34.1, +211.5]** | +207.3 [+52.0, +387.5] |
| D5 − A5 (does coherence matter?) | +3.8 [−21.8, +30.9] | −11.3 [−61.4, +44.9] |
| (A5, κ = 0) − A5 (does entanglement matter?) | +24.4 [−8.0, +60.5] | +33.2 [−23.6, +103.5] |
| BA5 − A5, main ratings | −45.8 [−94.1, +14.1] | +5.9 [−75.7, +103.6] |

- **The primary comparison is a tie.** A5 and F5 could not be told apart on the test chains.
- **On the 8 held-out items, outside the verdict, A5 beats F5.** But the dephased D5 is not detectably different from A5 there or on the test chains. D5 has no coherence: it is a classical Markov chain on the same states, with bit-flip dynamics between questions. Removing the couplings also costs nothing significant.
- **What F5 lacks is dynamics, not quantumness.** It fitted λ = 0, so it has no mixing between questions.
- **The best predictor of the main ratings on the test chains is the classical belief-adjustment model BA5** (827 against A5's 873).

**Parameter-free check 1, the QQ equality.**
- **Order effects are real.** 60 of 80 adjacent (claim, main) pairs have an order effect above 0.10 with an interval excluding 0 (about 27 expected by chance; 40 survive a Holm-corrected permutation test), and the main-rating means span a median of 24.7 points across orders and omissions (13.2 expected from repeat noise alone).
- **q was near zero only when the anchors were pooled; it is not supported on one scale.** On those 60 pairs the mean q is +0.005 [−0.058, +0.065], just wider than the pre-registered ±0.05. But that average pools the two scale directions, whose effects have opposite signs. The single-scale re-run (run 2, below) gives −0.146 [−0.439, +0.137].
- **The per-pair z values are overdispersed** against N(0, 1) (KS p < 0.001).
- **So the signature is not present. It is not contradicted on the pooled data, but on run 1's single-scale conversations (anchor a, not a pre-registered subset) mean q is −0.345 [−0.517, −0.181], which meets the contradiction rule; the verdict is re-issued on it as classical (D52).**
- **The encoder's a priori prediction of where order effects appear is not supported:** 1 win against 2 losses over the only 3 items with distinct predictions (p = 0.875, D32).

**Parameter-free check 2, Kvam-style interference.**
- **A mid-chain choice did not detectably move final confidence from where a matched filler leaves it:** Δ_K = +0.29 [−1.12, +1.65] points, with a total-probability residual of +0.58 points.
- **A5⁰'s predicted sign agrees on 53% of items,** about chance.
- **So neither interference nor a commitment effect was detected.**

**Also reported.**
- When the main question is asked first and again after the chain, the two ratings agree within 5 points in 84% of conversations.
- **A measurement artefact:** after recoding, baseline main ratings average 33.8 under one anchor direction ("0 = false") and 71.3 under the other ("0 = true"). The model does not reliably reverse the scale. That adds variance shared by every model, so the comparisons are fair but noisier than necessary.

**Verdict (§7.5): classical, re-issued in D52.** As first issued: tie, on the pooled q (superseded). On run 1's single-direction conversations the QQ signature is contradicted, and with a primary that is not a pass the frozen rule gives classical (`results/exp5-verdict-reissue.md`).

**Run 2: one scale direction** (`results/exp5-run-2.md`, `bffc4ab`; pre-registered in D33, `fbc2fbf`). The baseline and the QQ block were re-run on the first 10 candidates with every conversation on "0 = certainly false, 100 = certainly true": 1,700 conversations, $0.14, descriptive, with nothing refitted.

| measurement | pairs with OE > 0.10 | mean q [95% CI] | KS of z | baseline between-repeat SD (median) |
|---|---|---|---|---|
| run 2, one scale | 12 of 20 | −0.146 [−0.439, +0.137] | p = 0.008 | 7.1 |
| run 1, the same scale only | 12 of 20 | −0.154 [−0.423, +0.154] | p = 0.017 | 4.1 |
| run 1, both scales pooled | 16 of 20 | +0.031 [−0.098, +0.166] | p = 0.002 | 20.6 |

- **The order effects are not a scale artefact.** 12 of the 16 run-1 pairs with large order effects are still large on one scale.
- **Run 1's near-zero q was an anchor-pooling artefact.** On one scale the mean q leans negative, is far from the ±0.05 band, and the per-pair z values are overdispersed. **The QQ equality is not supported.** Run 1's verdict was first issued as a tie on the pooled q; re-issued on the single-direction q under the same rule, it is classical (D52).
- **The scale flip was the main noise source.** Baseline between-repeat SD is 7.1 points on one scale against 20.6 pooled.


### 5.13 After the pre-registered programme: the gold-map tests (November 4)

`paper/gold-map.md` ranked candidate directions after experiment 5. The overnight run on November 4 takes six of them in order. Each one is pre-registered in its own commit before its first call or analysis, every new design uses one scale direction, and every call stops on a refusal (D34 onward). The results are reported here as they land, whatever their outcome.

**Direction 9: does asking change later answers? No-signalling in time on the archived experiment 5 data** (`results/gm9-nsit.md`, `39a1a66`; pre-registered in `experiments/gm9-nsit.md`, `7f0dd3e`, D34; $0).
- **The contrasts.** In each family, conversations that differ only in whether an earlier question was put are compared on the later rating. Only anchor-(a) conversations are used. The test is a within-cell permutation test, with Holm correction over the six families.

| family | contrast | mean |d| (null) | p (Holm) | invasive |
|---|---|---|---|---|
| N1M | M after S_k vs M first | 12.4 (2.6) | 0.0012 | yes |
| N1S | S_k after M vs S_k first | 15.7 (3.1) | 0.0012 | yes |
| N2 | final M with S_k asked vs omitted | 8.7 (3.9) | 0.0012 | yes |
| N3 | final M after four sub-questions vs M alone | 22.6 (5.2) | 0.0012 | yes |
| N4 | final M after a midway yes/no choice vs a filler | 5.0 (3.3) | 0.1634 | **no** |
| N5 | final M with M asked first vs not | 16.0 (6.1) | 0.0012 | yes |

- **Asking is invasive in 5 of 6 families.**
  - Mostly the shifts go both ways across items: N1M's mean signed d is −0.0 [−6.1, +5.5].
  - Two families shift in one direction:
    - asking M first raises the next sub-question's rating by +8.0 [+2.7, +13.3];
    - asking M first and again at the end lowers the final M by −10.1 [−18.2, −2.9].
  - The N1 families replicate on the run-2 conversations: 17.4 against 2.9, and 15.7 against 2.3.
- **A midway choice shows no detectable effect beyond a filler** (N4, p = 0.16, 5 conversations per arm), consistent with experiment 5's Kvam null.
- **What it means.** By argument, the model's state at each turn is its copyable conversation, so it has a definite state by construction, and the "not asked" condition is an exact counterfactual at the level of the response distribution. Every one of these effects is therefore invasiveness: asking adds text to the state. None is evidence that a judgment lacked a definite value before it was asked. The same holds for every order-effect or QQ test run on a language model through its context, ours included (`paper/clonable-minds.md`).
- **What it cannot say.** This analysis cannot tell whether the question or the recorded answer does the work. That is direction 2.

**Direction 3, free look: does the scale-direction gap mark the model's errors?** (`results/gm3a-anchor-gap.md`, `43592e5`; pre-registered in `experiments/gm3a-anchor-gap.md`, `a1bc421`, D35; $0)
- **No evidence that the gap predicts errors.** The per-item gap between the "0 = false" and "0 = true" baseline ratings scores AUROC **0.48 [0.28, 0.66]** for the model's hard-pool errors, and 0.47 on the larger set of identical first turns.
- **The model's stated confidence does,** on the same 40 items: 0.75 [0.58, 0.89]. The paired difference is −0.27 [−0.49, −0.05].
- **The pre-registered reading is "no evidence either way".** The CI includes 0.5, and 40 items rule out only a large effect.
- **Direction.** If anything the gap is larger on the items the model got right (41.3 points) than on those it got wrong (33.9). The 37-point gap looks like a reading slip in the reversed scale, not a mark of items with no settled view. The six-format run is the real test of direction 3.


**Direction 1: does the model know its own errors better than another model reading the same answer?** (`results/gm1-self-knowledge.md`, `bc0f125`; pre-registered in `experiments/gm1-self-knowledge.md`, `28a20b2`, D36 with two amendments)
- **Design.** Both models rate their confidence in both models' answers on the 298 hard-pool questions both answered. All four cells use one matched prompt ("an answer another assistant gave"), so authorship is the only difference between cells.
- **Primary statistic.** The judge × author interaction I = HH + SS − SH − HS, which cancels each judge's overall skill. This replaced the gold map's per-author rule before freezing, because the full read of Xiao et al. showed capability dominating authorship.

| set | HH | SH | SS | HS | I [95% CI] |
|---|---|---|---|---|---|
| all 298 | 0.845 | 0.932 | 0.903 | 0.872 | **−0.055 [−0.103, −0.007]** |
| disagreement (authors' correctness differs, 26) | 0.432 | 0.850 | 0.865 | 0.583 | −0.135 [−0.496, +0.229] |
| paraphrased answers (subset) | 0.798 | 0.887 | 0.808 | 0.759 | −0.040 [−0.157, +0.075] |

(Cells read judge then author: SH is Sonnet judging Haiku's answers.)

- **No self-advantage.** The interaction is slightly negative, which comes from questions where the other model knew the answer. Sonnet judges Haiku's errors better than Haiku does: 0.93 against 0.85. On the 26 questions where exactly one model was right, Haiku is near chance on its own answers (0.43) while Sonnet scores 0.85 on them.
- **The framing makes no difference overall:** "an answer you gave" against "another assistant" changes the self cells by −0.011 (Haiku) and +0.007 (Sonnet) on all 298 questions.
- **Haiku does not recognise its own answers:** AUROC 0.51 [0.36, 0.67] on originals.
- **What was cut, and the cap.**
  - The run cost more per Sonnet call than planned, and a token-cap crash lost some calls (D36 amendments 1 and 2).
  - The paraphrase arm covers 60 of 80 planned questions, and Sonnet's recognition check did not run.
  - Recorded spend is $2.82. The lost calls add at most $0.20, so the run may have exceeded its $3 cap by up to $0.02.
  - The primary result uses all 298 questions and is not affected.
- **Reading.** The 0.82–0.91 self-report signal of Sections 5.3–5.11 carries no detectable authorship advantage: another model reading the same answer text matches or beats it. A stronger reader of the same text does better.


**Direction 2: is the order effect the question, or the model seeing its own answers?** (`results/gm2-self-conditioning.md`, `4c5c34f`; pre-registered in `experiments/gm2-self-conditioning.md`, `9e23b6f`, D37; 2,000 conversations, $0.55)
- **Design.** 10 experiment-5 items, chains O1–O4 and MF, on one scale direction. The model's earlier ratings were edited before each later turn:
  - **shown:** left as given;
  - **redacted:** replaced by "[rating recorded]";
  - **planted:** replaced by its usual rating ±15 points, placed in the model's own turn.

| condition | order effect across O1–O4 (points) | MF repeat agreement (within 5 points) |
|---|---|---|
| shown | 8.7 [4.1, 12.7] | 81% |
| redacted | 16.7 [8.0, 24.1] | 23% |
| planted high | 6.2 [3.6, 8.3] | 30% |
| planted low | 3.2 [2.2, 4.0] | 40% |

- **Pre-registered verdict: question-driven.** R = OE_redacted / OE_shown = **1.91 [0.92, 4.90]**, wholly above the 0.5 bar. With no record of its answers, the order of the questions still changes the final rating. In the gold map's terms this is the overturning direction, which it had put at P = 0.25.
- **The record also steers.** The final main rating follows a planted first main rating at 1.27 [0.70, 2.14] points per point. Planting higher earlier ratings raises the next ratings by 5.6 [3.4, 7.6] points and the final rating by 10.4 [4.2, 16.8].
- **The consistency depends on the visible answer.** The main question repeated after the chain agrees with the first answer 81% of the time when that answer is visible, and 23% when it is hidden. Experiment 5's 84% replicability depends on the visible first answer: without it, the intervening questions move the final rating.
- **Caveats, stated in the results file.**
  - There are only 10 items, and much of the redacted order effect comes from 2 of them (h191, h261).
  - "[rating recorded]" is itself an unusual turn. The redacted order effect is *larger* than the shown one, and the planted conditions, which keep a number in place, show smaller order effects than either. So the redaction placeholder may add variance of its own. The verdict that asking alone produces an order effect stands by the rule. The excess over the shown condition should not be read as the question's effect.
- **Reading.** Both parts of the measurement change the model's judgment: the questions put to it, and its own recorded answers, which it treats as evidence. In the terms of `paper/clonable-minds.md`, both the question channel and the record channel are invasive.
- **On all 40 items** (`results/gm2b-self-conditioning-40.md`, `758609a`; pre-registered at `4894bfc`, D45; 6,000 new conversations, $1.68, no refusal). The same design, with the other 30 experiment-5 items added.
  - **Still question-driven:** R = **1.23 [0.75, 2.02]**. Order effect 9.8 [5.8, 13.5] shown against 12.0 [7.3, 15.9] redacted.
  - **Not two items.** The 30 new items alone give 0.99 [0.51, 1.61]; all 40 without h191 and h261 give 0.99 [0.62, 1.49]. On 82% of 39 items the redacted order effect is at least half the shown one.
  - **No added noise from the placeholder.** The spread within one order is the same shown and redacted (SD 5.1 against 5.4); systematic placeholder effects are not excluded.
  - **The record still steers,** less than on the first 10: b_MF 0.85 [0.65, 1.13]; next-rating pull 5.2 [3.7, 6.5]; final-rating shift 9.0 [5.4, 12.6]. MF repeat agreement is 86% shown against 36% redacted (planted high 38%, low 45%).
  - **What changes.** The two-item caveat is resolved; the placeholder caveat is not. The redacted effect is no longer larger than the shown one: the first 10 items' R of 1.91 came mostly from h191 (0.4 points shown, 38 redacted). On these items hiding the record leaves an order effect of about the same size, but with a largely different pattern.


**Direction 3, six formats: does the model hold one credence per statement?** (`results/gm3b-format-invariance.md`, `1fd521d`; pre-registered in `experiments/gm3b-format-invariance.md`, `34eb191`, D38; 9,600 calls, $0.41)
- **Design.** The 160 experiment-5 chain claims, each asked 10 times in six single-turn formats on one scale direction:
  - a 0–100 rating;
  - yes/no;
  - a bet at a stated price;
  - "likelier than a fair coin landing heads?";
  - "how many of 100 such statements would be true";
  - a 7-point verbal scale. This replaced the gold map's reversed scale, under the one-direction rule.
- **The two models.** L1 has one latent credence per claim, read through a monotone link per format. L6 has a separate credence per claim and format. Both are scored on held-out repeats (2-fold, even against odd).
- **Pre-registered verdict: no single credence.** L6 beats L1 on held-out repeats for **86%** of claims. The mean ΔLL is **+19.4 [+16.5, +22.1]** per claim.
- **The formats rank the claims differently, which no monotone link can absorb:**
  - pairwise Spearman correlations between formats are 0.37–0.74, and Kendall's W across all six is 0.56;
  - 12–25% of claim pairs are in opposite order to the 0–100 rating ((1 − τ_b)/2 = 0.20–0.34);
  - the coin comparison is the most out of line, choosing the statement 79% of the time where the mean rating is 55.
- **Against the precedent.** Smolin & Wilder (2026) found one latent belief describes capable models well (concordance 0.8–0.95, held-out R² 60–90%). The gold map had lowered P from 0.45 to 0.25 for that reason. Their test and ours differ in three ways:
  - **The criterion.** They asked whether one latent *predicts* new framings usefully. Ours asks whether format-specific credences predict held-out *repeats* better. A latent can be useful by their criterion and still lose by ours whenever format deviations are reproducible, which is likely for a model whose repeats barely vary.
  - **The material.** Our statements are the model's own contested claims about hard questions.
  - **The model.** Claude was not in their set.
  So the two results need not conflict. Ours says this model's credences are not format-invariant on contested claims; it does not say a single latent is useless.
- **Noise baseline** (exploratory: computed after the run, not pre-registered). Two halves of the *same* format's repeats put only 1–5% of claim pairs in opposite order ((1 − τ_b)/2 = 4–8%). The 0–100 rating's even repeats against another format's odd repeats, the same amount of data, put 11–25% in opposite order ((1 − τ_b)/2 = 21–35%). So the cross-format reordering is four to six times the noise on that index, and larger on the count of reversed pairs.
- **The held-out-format follow-up** (`results/gm3c-heldout-format.md`, `52aedb6`; pre-registered at `1f2a837`, D46; $0) applies Smolin & Wilder's usefulness criterion (not their framings or items). One credence fitted on five formats predicts the sixth with mean R² 0.37 [0.28, 0.47], against split-half ceilings of 0.88–0.97.
  - It recovers **Q = 0.39 [0.30, 0.50]** of each format's reproducible answer, ranging from 0.17 for the coin comparison to 0.53 for the 0–100 rating.
  - The pre-registered reading is *little format-free belief*. The interval's upper end, 0.499, sits just under the 0.5 line.
  - Smolin & Wilder's 0.60–0.90 on other models is above every format here.
  - So the difference from their result is probably not only the criterion, though framings and items also differ. On this model and these statements, the format-free part of the answer is the smaller part.


**Direction 4: does the model seek the evidence that would settle its own conflict?** (`results/gm4-evidence-seeking.md`, `bc9e70d`; pre-registered in `experiments/gm4-evidence-seeking.md`, `e913227`, D39; 1,200 calls, $0.11)
- **Design.** For each of the 40 experiment-5 items, Haiku saw its own answer and a menu of four of its own claims, and said which it would check first. There were 3 menus per item and 10 repeats.
- **Scoring.** Choices were scored against four rules:
  - the expected-information-gain (EIG) choice under the frozen D5 and BA5 fits;
  - expected change in the main rating;
  - the confirmatory choice, the claim that most supports the model's own answer;
  - the most uncertain claim.
- **The choices are systematic.** The modal claim is picked 87% of the time.
- **The choices beat chance under every rule that weighs a claim's bearing on the answer.** The excess over chance is:
  - EIG under D5: +0.14 [+0.04, +0.25];
  - EIG under BA5: +0.21 [+0.11, +0.31];
  - confirmatory: +0.21 [+0.11, +0.31].
- **It avoids the most uncertain claim:** −0.13 [−0.21, −0.04].
- **Pre-registered verdict: mixed.** On the menus where the EIG and confirmatory choices differ, the model leans confirmatory, but neither difference is reliable: −0.24 [−0.52, +0.04] under D5 (46 menus) and −0.14 [−0.40, +0.14] under BA5 (26 menus). So neither "tracks EIG" nor "confirmatory" holds under either model.
- **Reading.** The model picks claims that bear strongly on its answer. When the informative and the confirming check come apart, it shows no detectable preference for the informative one, and the point estimates lean confirmatory. Active-inference-style evidence seeking is not shown, and neither is a clear confirmation bias.
- **Caveat.** EIG is computed from our fitted models of the model, which the chooser never sees. A miss may be a miss of those models: the D5 and BA5 argmax choices agree on only 41 of 120 menus.


---

## 6. Discussion

### 6.1 Error prediction: the answer is no

Four pre-registered comparisons agree:
- the fixed encoding against its controls (H2);
- the learned encoding against a matched classical twin (v2);
- the honest-hedge encoding against its twin (v2.1);
- and every structural arm against the model's self-report (run 2b).

In none of them does the quantum state add anything detectable to error prediction.

The data rule out the easy explanations.
- **It is not noise.** The noiseless state scores 0.49, and A2.1 noisy and noiseless differ by +0.000 [−0.020, +0.023].
- **It is not one flawed choice of constants.** Version two learned them; the fit chose weak couplings, because strong ones lowered train AUROC and weak ones did no better than none.
- **It is not the hedge encoding.** v2.1 removed that distortion, and the hedge term was fitted to zero.
- **It is not the frame bug.** Correcting it leaves the AUROCs unchanged (D15).

The window shows *where* the fixed encoding loses the signal: at the entangling and coupled-evolution steps. The learned encodings avoid the loss by switching those steps nearly off.

**The only positive differences between quantum and classical models are secondary, sit on the same hard-pool questions, and none survives against a classical twin with the same per-claim readout.**
- A2 and A2.1 beat their twins on Haiku's run-2 held-out set, which motivated v2.1.
- A2 beat F2 on Sonnet's hard-pool errors (+0.078).

In every case the learned quantum model has near-zero coupling. Two pre-registered tests settled what the edges are:
- **Addendum D:** setting the couplings to 0 changes nothing detectable.
- **Addenda D and E:** a classical twin with the same per-claim readout, F2+, is not detectably different from the quantum model on every set where the quantum model had led: Sonnet's hard pool and Haiku's run-2 held-out set.

**No positive quantum-vs-classical difference in error prediction is significantly larger than a classical model with the same per-claim readout achieves (F2+ recovers 1.05 [0.73, 2.50] of the Sonnet edge and 0.68 [0.20, 1.21] of the held-out A2.1 edge).** The one in sequential judgment does not survive either: on experiment 5's held-out items, D5, a dephased classical Markov chain, is not detectably different from A5 (D5 − A5 = −11.3 [−61.4, +44.9], Section 5.12). Where self-report was measured, on both base models, it was not detectably different from the best structural model.

### 6.2 What does predict the model's errors

**The model's own statement of confidence does.**
- AUROC 0.82 on the run-2 test set, and 0.83 on the locked test set.
- It has the highest point estimate in every subgroup of the split analysis, tied with arm C in SimpleQA (0.74 vs 0.72).

**The structure of the model's explanation adds nothing beyond that self-report.** Version 2 of this paper reported the contradiction signal (arm E, 0.64) as "a modest but real finding" and left open whether it adds to self-report. It does not:
- E scores 0.64 against G's 0.82;
- the learned 8-feature relation-web model L scores 0.79 and 0.66 against G's 0.83 and 0.82;
- the real relation web scores *below* 99% of random webs of the same strengths.

The relation judge's labels of *which* claims support or contradict which carry no error signal that survives encoding. The counts and strengths behave like noisy proxies for how unsure the model already says it is.

**The same holds on a second base model.** Sonnet's stated confidence scores 0.91 on its hard-pool errors, level with A2 (0.90), and 0.18 above the relation-web model L.

This is a plain negative for version one's hope that the quantum layer would expose conflicts the model cannot see. On both models, the model can see them, and says so when asked.

**But the self-report is not privileged.** Gold-map direction 1 (Section 5.13) had each model judge both models' answers with the same prompt. Authorship does not help: the judge × author interaction is −0.055 [−0.103, −0.007]. Sonnet judges Haiku's errors better than Haiku does (0.93 against 0.85). The error signal is available from the answer text to a capable reader, especially one that knows the answer.

### 6.3 Sequential judgment: real effects, classical account

**What the graded ratings show.**
- Single but not double conjunction fallacies, the pattern the quantum account predicts, which Imannezhad et al. (2026) also find in GPT-5.
- Order effects that satisfy R2 in experiment 4.
- Order effects in experiment 5, where 40 of 80 claim–question pairs survive a Holm-corrected permutation test.

The sequential phenomena that quantum cognition was built to explain are present in this model's graded judgments.

**None of them needs a quantum account.**
- **The prediction contest.** In experiment 5, the quantum belief state and its matched classical twin tie.
- **Coherence.** Where the quantum state predicts better, a dephased classical Markov chain with the same parameters is not detectably worse.
- **The QQ equality.** It is not supported: q looked near zero only when the two scale directions were pooled, and on one scale it leans negative with overdispersed per-pair values.
- **Kvam interference.** A mid-chain decision does not detectably change later confidence (Δ_K = +0.29 [−1.12, +1.65]), consistent with any read-out or Markov model.
- **Main ratings.** A classical belief-adjustment model predicts them best.

**Why the encoder could not do better here.** The anchored phase solve puts 148 of 160 chain claims exactly on the yes/no axis. Those claims commute with the main question at encode, so the quantum model's distinctive source of order effects is absent before any data. The pre-registration anticipated for this reason that A5 and F5 would be close (§8.6). The order effects the model shows must come from somewhere the encoder does not put non-commutation, and the classical dynamics capture them with no detectable loss against the quantum ones.

**What remains open.** Whether this model's order effect on conjunctions is numeric anchoring or content-driven updating. A rank-one quantum model and anchoring predict the same form, c · (P(X) − P(Y)), whenever the item fixes the first rating, so run 2 could not separate them (D19). Experiment 4 run 3 tried to move the first rating with a provided estimate, and was untestable, because the model resists such estimates (Section 5.9). The manipulation that remained was to set the first rating as the model's *own* earlier answer in the transcript. Gold-map direction 2 did that for experiment 5's chains (Section 5.13). Planted own answers do move later ratings, about 1.3 points per point. Hiding the answers does not remove the order effect. So in those chains, the question and the record both act. That run did not use experiment 4's conjunction items, so for conjunctions the mechanism remains open.

### 6.4 The hardware result

The witness separates two claims that behavioural Bell tests conflate: *the system holds an entangled state*, and *the outcomes shift with context*. For three of our belief states, selected as the most entangled, the first is certified on real hardware. The second, the claim that the entanglement helps judgment, has been answered negatively for error prediction.

At 5–16 qubits every state is exactly classically simulable, so the hardware's role was certification, and it played that role. The job-time calibration shows an ordinary device on an ordinary day. The gap between hardware and its noise model is therefore a property of the noise model, not of bad luck.

---

## 7. Implications

**Physics.** A real quantum processor held the entangled states of a language model's belief webs, with certified negativity on 3 of 3 items. That is a modest near-term use of hardware: certification, not speed. The device washed states out more than its own noise model and calibration predict. Any claim about "cognitive work" done by entanglement on current hardware should budget for that.

**Psychology.** Our results neither confirm nor refute quantum cognition, which models human aggregates. What we offer is a method: build the state per item from stated reasons, and compare it against a classical twin with the same inputs, parameter budget and fitting rule. The negative results show that method can return "no". Pointed at the effects the field rests on, sequential order and intermediate decisions, it finds the effects present in a language model's graded judgments, and finds a classical account of them that the quantum one does not detectably beat.

**Philosophy of mind.** A judgment layer built as an entangled whole (certified pairwise on three states) judged no better than one built as a list. When it was free to choose, it chose to be nearly a list. That does not settle anything about minds. It does show that being an indecomposable whole is not, by itself, an advantage for this kind of judgment.

**Artificial intelligence.** The practical finding is about self-report, not quantum structure. For this model, on hard factual and scientific questions, one call asking how confident it is predicts its errors as well as the best analysis of its written reasoning we built, quantum or classical. A pipeline that wants an error flag should ask for a confidence rating first, and should require any structural method to beat that baseline. Ours did not. The rating need not come from the model that wrote the answer: a stronger model reading the same answer did better than the author itself (direction 1, Section 5.13).

---

## 8. Limitations

- **One base model for the primary results.** Every pre-registered comparison uses `claude-haiku-5-5`. The second model, `claude-sonnet-5-5`, contributes a secondary transfer test on its hard pool: frozen parameters (D27), plus self-report and the Addendum D ablation (D28). It has no training-pool data, because the replication was halted by a second refusal (D25).
- **Visible explanations, not deliberation.** Claims come from what the model writes for the reader (D1–D3).
- **Models judging models.** The extractor and relation judge are language models, and their errors bound what any arm can find.
- **Error types.** The model's errors are mostly ignorance and multi-step science, not the judgment errors quantum cognition studies.
- **Moderate test sets.**
  - Run 2's test set has 80 items, and the locked v2 test set 209 items with 32 wrong. Intervals are reported throughout, and many overlap.
  - The only positive quantum-vs-classical differences are secondary: A2 and A2.1 on Haiku's held-out set, which motivated v2.1, and A2 on Sonnet's hard pool. None is significantly larger than a classical twin with the same per-claim readout achieves (Addenda D and E); the twin recovers all of the Sonnet edge and roughly two thirds (95% CI one fifth to all) of the held-out A2.1 edge. The F2+ comparisons are additional single scorings of frozen models on sets that had been scored before.
- **Analysis grew after the primary result.** Every addition was pre-registered before it was scored, but designed knowing run 2 had failed; four (D9, D13, D26, D28's code) were committed after their first calls had begun (Section 4).
- **Hardware scope.** The witness certified one pair in each of 3 items, and arm B never ran.
- **Sequential experiments are limited by the measurement.**
  - The yes/no answers saturate, and temperature cannot be raised.
  - One pre-registered estimator was circular (D19).
  - In experiment 5 the model did not reliably reverse a reversed rating scale (baseline means 33.8 against 71.3), which adds noise to every model's predictions.
  - Experiment 5's encoder predicted non-commutation for only 12 of 160 claims, so it tested the quantum model where that model had little to say.
- **Single author, no independent replication.** The code, data and decisions are public.

---

## 9. What comes next

**No pre-registered test of the original programme remains.**
- Experiment 4 run 3 was untestable, because the model resists provided first ratings.
- Experiment 5 and its single-scale re-run are complete.
- The six overnight gold-map tests (Section 5.13) are complete. Directions 5–8, 10 and 11 need new tooling or QPU time, and none is pre-registered.

**The readings fixed in advance.** `paper/next-steps.md` fixed the reading of a tie or classical verdict in experiment 5 before the run (the verdict is classical, re-issued in D52): no detectable advantage for quantum probability over a matched classical updater, in sequential judgment as in error prediction. That is a clean, pre-registered negative result, and we report it as one.

**The project's answer for this model** is a null on both the static question (error prediction) and the sequential one.
- Its primary verdicts are pre-registered.
- Every positive quantum-vs-classical difference along the way was traced to a classical mechanism.
- The one parameter-free quantum signature that looked close, the QQ equality, came from pooling two scale directions.

**What the gold-map tests settled.**
- The model's self-reported confidence shows no privileged self-knowledge: it has no authorship advantage over another model reading the same answer, which does as well or better.
- Its order effects survive hiding its recorded answers, though with a largely different pattern, while its recorded answers steer the level of later ratings.
- On contested claims, one credence per claim does not explain its answers across question formats.

**The follow-ups each result names.** Each would need its own pre-registration:
- a held-out-*format* test of a single credence, applying Smolin & Wilder's usefulness criterion (since run as D46, Section 5.13);
- a redaction placeholder that is less unusual than "[rating recorded]";
- direction 2's design on experiment 4's conjunction items, where the mechanism of the order effect is still open.

`paper/gold-map.md` ranks the remaining directions.

---

## References

Aerts, D. (2009). Quantum structure in cognition. *Journal of Mathematical Psychology, 53*(5), 314–348. https://doi.org/10.1016/j.jmp.2009.04.005

Aerts, D., Aerts Arguëlles, J., Beltran, L., Geriente, S., Leporini, R., Sassoli de Bianchi, M., & Sozzo, S. (2026). Identifying quantum structure in AI language: Evidence for evolutionary convergence of human and artificial cognition. *Entropy, 28*(6), 622. https://doi.org/10.3390/e28060622 (arXiv:2511.21731, 2025)

Aerts, D., & Sozzo, S. (2011). Quantum structure in cognition: Why and how concepts are entangled. In *Quantum Interaction 2011*, Lecture Notes in Computer Science 7052 (pp. 116–127). Springer. https://doi.org/10.1007/978-3-642-24971-6_12

Bessis, T. F., Wills, A. J., Wojciechowski, B. W., White, L. C., & Pothos, E. M. (2026). Legal decision biases in GPT: A comparison with human judgment. *Behavioral Sciences, 16*(3), 437. https://doi.org/10.3390/bs16030437

Beuria, J. (2026). Emergent non-classical probabilistic structure in large language models under contextual modulations. *Scientific Reports*. https://doi.org/10.1038/s41598-026-65824-7

Binz, M., & Schulz, E. (2023). Using cognitive psychology to understand GPT-3. *Proceedings of the National Academy of Sciences, 120*(6), e2218523120. https://doi.org/10.1073/pnas.2218523120

Boyer-Kassem, T., Duchêne, S., & Guerci, E. (2016a). Testing quantum-like models of judgment for question order effect. *Mathematical Social Sciences, 80*, 33–46. https://doi.org/10.1016/j.mathsocsci.2016.01.001

Bruza, P. D., Wang, Z., & Busemeyer, J. R. (2015). Quantum cognition: A new theoretical approach to psychology. *Trends in Cognitive Sciences, 19*(7), 383–393. https://doi.org/10.1016/j.tics.2015.05.001

Busemeyer, J. R., & Bruza, P. D. (2012). *Quantum models of cognition and decision*. Cambridge University Press. https://doi.org/10.1017/CBO9780511997716

Busemeyer, J. R., Pothos, E. M., Franco, R., & Trueblood, J. S. (2011). A quantum theoretical explanation for probability judgment errors. *Psychological Review, 118*(2), 193–218. https://doi.org/10.1037/a0022542

Busemeyer, J. R., Wang, Z., & Lambert-Mogiliansky, A. (2009). Empirical comparison of Markov and quantum models of decision making. *Journal of Mathematical Psychology, 53*(5), 423–433. https://doi.org/10.1016/j.jmp.2009.03.002

Busemeyer, J. R., Wang, Z., & Townsend, J. T. (2006). Quantum dynamics of human decision-making. *Journal of Mathematical Psychology, 50*(3), 220–241. https://doi.org/10.1016/j.jmp.2006.01.003

Dominguez-Olmedo, R., Hardt, M., & Mendler-Dünner, C. (2024). Questioning the survey responses of large language models. In *Advances in Neural Information Processing Systems 37*. arXiv:2306.07951

Dzhafarov, E. N., & Kujala, J. V. (2014). On selective influences, marginal selectivity, and Bell/CHSH inequalities. *Topics in Cognitive Science, 6*(1), 121–128. https://doi.org/10.1111/tops.12060

Echterhoff, J., Liu, Y., Alessa, A., McAuley, J., & He, Z. (2024). Cognitive bias in decision-making with LLMs. arXiv:2403.00811

Fiedler, K. (1988). The dependence of the conjunction fallacy on subtle linguistic factors. *Psychological Research, 50*(2), 123–129. https://doi.org/10.1007/BF00309212

Fuyama, M., Khrennikov, A., & Ozawa, M. (2025). Quantum-like cognition and decision-making in the light of quantum measurement theory. *Philosophical Transactions of the Royal Society A, 383*(2309), 20240372. https://doi.org/10.1098/rsta.2024.0372

Hertwig, R., & Gigerenzer, G. (1999). The 'conjunction fallacy' revisited: How intelligent inferences look like reasoning errors. *Journal of Behavioral Decision Making, 12*(4), 275–305. https://doi.org/10.1002/(SICI)1099-0771(199912)12:4<275::AID-BDM323>3.0.CO;2-M

Hogarth, R. M., & Einhorn, H. J. (1992). Order effects in belief updating: The belief-adjustment model. *Cognitive Psychology, 24*(1), 1–55. https://doi.org/10.1016/0010-0285(92)90002-J

Imannezhad, P., Pothos, E. M., & Wills, A. J. (2026). Divergent patterns of probabilistic reasoning in humans and GPT-5. *Frontiers in Psychology, 17*, 1782184. https://doi.org/10.3389/fpsyg.2026.1782184

Javadi-Abhari, A., Treinish, M., Krsulich, K., Wood, C. J., Lishman, J., Gacon, J., Martiel, S., Nation, P. D., Bishop, L. S., Cross, A. W., Johnson, B. R., & Gambetta, J. M. (2024). Quantum computing with Qiskit. arXiv:2405.08810. https://doi.org/10.48550/arXiv.2405.08810

Kang, P. (2026). Auditing question-order effects in large language models with the QQ equality: Mechanism characterization and a saturation caveat. arXiv:2607.17219

Khrennikov, A., Basieva, I., Dzhafarov, E. N., & Busemeyer, J. R. (2014). Quantum models for psychological measurements: An unsolved problem. *PLoS ONE, 9*(10), e110909. https://doi.org/10.1371/journal.pone.0110909

Kreutner, M., Rupprecht, J., Ahnert, G., Salem, A., & Strohmaier, M. (2025). QSTN: A modular framework for robust questionnaire inference with large language models. arXiv:2512.08646

Kujala, J. V., & Dzhafarov, E. N. (2016). Proof of a conjecture on contextuality in cyclic systems with binary variables. *Foundations of Physics, 46*(3), 282–299. https://doi.org/10.1007/s10701-015-9964-8

Kvam, P. D., Pleskac, T. J., Yu, S., & Busemeyer, J. R. (2015). Interference effects of choice on confidence: Quantum characteristics of evidence accumulation. *Proceedings of the National Academy of Sciences, 112*(34), 10645–10650. https://doi.org/10.1073/pnas.1500688112

McCoy, R. T., Yao, S., Friedman, D., Hardy, M. D., & Griffiths, T. L. (2024). Embers of autoregression show how large language models are shaped by the problem they are trained to solve. *Proceedings of the National Academy of Sciences, 121*(41), e2322420121. https://doi.org/10.1073/pnas.2322420121

Ozawa, M., & Khrennikov, A. (2020). Application of theory of quantum instruments to psychology: Combination of question order effect with response replicability effect. *Entropy, 22*(1), 37. https://doi.org/10.3390/e22010037

Ozawa, M., & Khrennikov, A. (2021). Modeling combination of question order effect, response replicability effect, and QQ-equality with quantum instruments. *Journal of Mathematical Psychology, 100*, 102491. https://doi.org/10.1016/j.jmp.2020.102491

Pothos, E. M., & Busemeyer, J. R. (2009). A quantum probability explanation for violations of 'rational' decision theory. *Proceedings of the Royal Society B, 276*(1665), 2171–2178. https://doi.org/10.1098/rspb.2009.0121

Pothos, E. M., & Busemeyer, J. R. (2013). Can quantum probability provide a new direction for cognitive modeling? *Behavioral and Brain Sciences, 36*(3), 255–274. https://doi.org/10.1017/S0140525X12001525

Rupprecht, J., Ahnert, G., & Strohmaier, M. (2025). Prompt perturbations reveal human-like biases in large language model survey responses. arXiv:2507.07188

Trueblood, J. S., & Busemeyer, J. R. (2011). A quantum probability account of order effects in inference. *Cognitive Science, 35*(8), 1518–1552. https://doi.org/10.1111/j.1551-6709.2011.01197.x

Tversky, A., & Kahneman, D. (1983). Extensional versus intuitive reasoning: The conjunction fallacy in probability judgment. *Psychological Review, 90*(4), 293–315. https://doi.org/10.1037/0033-295X.90.4.293

Wang, Z., & Busemeyer, J. R. (2013). A quantum question order model supported by empirical tests of an a priori and precise prediction. *Topics in Cognitive Science, 5*(4), 689–710. https://doi.org/10.1111/tops.12040

Wang, Z., Solloway, T., Shiffrin, R. M., & Busemeyer, J. R. (2014). Context effects produced by question orders reveal quantum nature of human judgments. *Proceedings of the National Academy of Sciences, 111*(26), 9431–9436. https://doi.org/10.1073/pnas.1407756111

Wolf, P., Kleine Buening, T., Krause, A., & Mendler-Dünner, C. (2026). Partition, prompt, aggregate: Statistical self-consistency in language models. arXiv:2607.15277

Yearsley, J. M., & Trueblood, J. S. (2018). A quantum theory account of order effects and conjunction fallacies in political judgments. *Psychonomic Bulletin & Review, 25*(4), 1517–1525. https://doi.org/10.3758/s13423-017-1371-z

Zhu, J.-Q., & Griffiths, T. L. (2024). Incoherent probability judgments in large language models. arXiv:2401.16646

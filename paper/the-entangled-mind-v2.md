# The Entangled Mind: Quantum Cognition as a Cognitive Architecture for Language Models

**Sean Pharris**
Independent Researcher, Colorado Springs, Colorado
Version 2, November 3, 2026 (version 1: October 25, 2026)

**Author note.** Sean Pharris is an independent researcher with a background in psychology and philosophy and professional experience in prompt engineering and AI pipeline development.

Version 1 was a pre-registration-style proposal. This version reports the experiments run so far and keeps the pending ones as placeholders with their pre-registered criteria.

Number conventions:
- **Results** are quoted verbatim from the files in `results/` of the project repository (https://github.com/GitPhar/entangled-mind).
- **Design constants** are cited to `experiments/preregistration.md`, `DEVIATIONS.md` or the code.
- **Any result not yet in `results/`** is marked [PENDING].
- Numbers about other people's work come from the cited papers. Where we recomputed them from published tables, we say so.

Correspondence: seanm.pharris@gmail.com.

---

## Abstract

Do machines need quantum minds? Quantum-cognition models describe human judgment with amplitudes, interference and entanglement rather than classical probabilities. They have explained order effects and conjunction fallacies in people, but they have been fitted to aggregate answer frequencies and never built into a machine that judges. We built one, and tested it.

**Pipeline.**
- For each yes/no question, a language model (`claude-haiku-5-5`) answers and briefly explains its considerations for and against.
- The claims in that explanation are extracted, and every pair is judged to support, contradict or be unrelated to the other.
- The resulting web is encoded as one entangled state on 5–16 qubits: one qubit per claim, confidence as amplitude, a solved phase as stance, and RZZ couplings for relations.
- The state evolves briefly under an Ising-style Hamiltonian and is measured in a "yes"-oriented basis.

**The test.** The pre-registered primary test (H2) asked whether the readout's conflict flag picks out the model's wrong answers better than three controls: the same circuit with no entanglement, the same circuit with a shuffled relation web, and plain classical contradiction-counting.

**Result.** It does not. On an 80-item test set (40 wrong, 40 right), the entangled readout separated wrong from right answers at AUROC 0.55. The controls did better:
- the unentangled circuit: 0.68
- the shuffled web: 0.65
- contradiction-counting: 0.64

The noiseless entangled state scored 0.49, so hardware noise is not the explanation. H2, H3 (entanglement carries information) and H4 (structure carries information) are falsified on this pool.

**Hardware.** A pre-registered entanglement witness certified, on IBM's `ibm_fez` processor, that the encoded belief states are physically entangled. The witness is two-qubit tomography with negativity as the criterion: 3 of 3 items certified, negativity 0.147, 0.063 and 0.067, lower 95% bounds all above zero, 44 QPU seconds. The entanglement is real; in this design it does not help.

**What the results say.** The error signal lives in the classical structure of the model's own explanation: how much its stated considerations contradict each other.

**What remains.** Three pre-registered follow-ups are pending:
- a learned "version two" encoding, compared against an equally tuned classical twin and a linear baseline;
- an order-effect experiment in which the quantum and classical-twin predictions differ;
- a conjunction/order co-occurrence test.

**Keywords:** quantum cognition, entanglement, language models, error prediction, pre-registration, classical twin, entanglement witness

---

## 1. Introduction

Physics has a mathematics of states that cannot be decomposed into parts: entanglement. Psychology has three decades of evidence that human judgment departs from classical probability in ways that mathematics describes well (Busemeyer & Bruza, 2012; Pothos & Busemeyer, 2013; Bruza et al., 2015). Artificial intelligence has built machines that produce something like deliberation, and has built them on classical probability. The first version of this project proposed putting the three in one room: take the competing considerations behind a language model's answer, hold them as one entangled state rather than a list of weights, let the state evolve under their mutual support and contradiction, and read the answer from a measurement.

Version 1 argued that this could change how a machine judges, and could give quantum cognition its first working mechanism rather than a descriptive fit. It also said that "a clean negative result is still a contribution." This version reports what happened when the idea met its own pre-registered test.

Three things changed between the proposal and the experiment.
- **The input.** Version 1 planned to split the model's hidden reasoning trace. The API's `reasoning_extraction` safeguard refused that design twice. We redesigned rather than route around it, so the claims now come from the model's *visible* explanation (Section 4, D1–D3).
- **The question.** Version 1's primary hypothesis asked whether the entangled layer flags conflict on known-wrong answers more often than two controls. The pre-registration sharpened this: the conflict flag must beat an unentangled circuit, a shuffled web *and* a plain classical contradiction count. The last control is the one that matters, because it asks whether the quantum state carries anything beyond the relation table it was built from.
- **The standard of comparison.** Every quantum component now has a classical twin with the same inputs. In version two of the encoding, the twin also has the same number of learned parameters and the same fitting rule. This answers the most persistent criticism of quantum-cognition models, that they are flexible enough to fit anything (Section 2).

The headline result is negative and robust. The entangled readout does not predict the model's errors as well as any control, and the information that does predict errors is classical. The hardware result is positive and narrow. A real quantum processor held the entangled states we built, which certifies the encoding and not its usefulness. We report both plainly. We then describe the pending experiments, which ask whether a learned encoding, or a test aimed where quantum and classical predictions actually differ, changes the picture.

---

## 2. Related work

A fuller version, with every paper's design, numbers and limitations, is in `paper/related-work.md`. We join a conversation that has run for about fifteen years, and we have borrowed from it freely.

**Order effects and the QQ equality.** Asking two questions in different orders changes people's answers. Wang and Busemeyer (2013) derived a parameter-free constraint that projective quantum models impose: the probability that the two answers disagree is the same in both orders (the QQ equality). Four Gallup surveys satisfied it: Clinton/Gore q = −0.003, Gingrich/Dole −0.003, White/Black −0.019. Rose/Jackson, where background text intervenes, failed as predicted: q = +0.151. Wang, Solloway, Shiffrin and Busemeyer (2014) extended this to about 70 national surveys.

Boyer-Kassem, Duchêne and Guerci (2016a) then showed that the same datasets violate a stronger condition, Grand Reciprocity, that every non-degenerate quantum model must meet. Only higher-dimensional models survive, and those need independent justification for their extra dimensions. Khrennikov, Basieva, Dzhafarov and Busemeyer (2014) showed that order effects plus the expectation that a repeated question gets the same answer are incompatible with projective measurement. The proposed resolution, non-projective quantum instruments (Ozawa & Khrennikov, 2020, 2021; Fuyama, Khrennikov & Ozawa, 2025), can both satisfy and violate QQ, at the cost of its predictive edge.

**Conjunction fallacies and co-occurrence.** In probability formats, 85–90% of people rank "Linda is a bank teller and is active in the feminist movement" above "Linda is a bank teller" (Tversky & Kahneman, 1983). Frequency formats cut this to 0–25% (Fiedler, 1988; Hertwig & Gigerenzer, 1999). The quantum account (Busemeyer, Pothos, Franco & Trueblood, 2011) explains single fallacies through incompatible events and forbids double fallacies. Yearsley and Trueblood (2018) predicted that order effects and conjunction fallacies should therefore co-occur. In 1,200 participants judging the 2016 primaries, they found recency order effects in all 10 comparisons, single fallacies in 37 of 40, and no double fallacies.

**Dynamic models.** Pothos and Busemeyer (2009) modelled the prisoner's dilemma with a Hamiltonian over a belief-and-action state. They proved that any Markov model must make the "unknown" case a mixture of the "known" cases, which the human data violate. Busemeyer, Wang and Townsend (2006) found, by contrast, that a Markov random walk fitted response-time data better than its quantum counterpart. Our encoding borrows the dynamic design, a problem Hamiltonian plus a mixer evolved for a fixed short time, and our classical twin plays the role of their Markov comparator.

**The flexibility critique.** The commentaries on Pothos and Busemeyer (2013) argued that the choice of compatibility, dimension, state placement and processing order leaves quantum models able to fit opposite patterns. Examples are Tentori and Crupi's "Russian woman" problem and Kaznatcheev and Shultz's point that the "more probable first" rule sits outside the formalism. We take this as the design constraint for our work. Our state is built from the model's claims before any outcome is seen, and every quantum arm has a classical twin.

**Quantum structure in LLMs.** Aerts and colleagues (Aerts & Sozzo, 2011) found that 81 people choosing exemplars of *The Animal Acts* gave a CHSH value of 2.42, above the classical bound of 2. Aerts et al. (2025) report CHSH values from 2.12 to 4 for ChatGPT and Gemini on the same items, and Bose–Einstein word statistics in LLM-written stories. They read this as convergence of human and artificial meaning structures.

We recomputed their published tables, and two things stand out.
- **The marginals move with context.** For example, P(Tiger) is 0.86 in one setting and 0.23 in another. Contextuality-by-Default (Kujala & Dzhafarov, 2016) allows CHSH values up to 2 + Δ, where Δ is the total marginal shift. Under that bound every Animal Acts dataset, human and LLM, is non-contextual: humans 2.42 against a bound of 5.78; ChatGPT 2.25 against 5.75; ChatGPT 3.53 against 6.50. This is the point Dzhafarov and Kujala (2014) made about the human data.
- **One table and its text disagree.** For the "neutral" ChatGPT prompt, the printed table implies CHSH 3.53 rather than the 3.09 stated in the text.

We offer these as a colleague's check, not a refutation. The Bose–Einstein result is a separate question that our work does not bear on.

**Classical-probability coherence in LLMs.**
- Binz and Schulz (2023) found GPT-3 human-like on 12 vignettes, including the Linda fallacy, but fragile under small perturbations and probably contaminated by training data.
- Zhu and Griffiths (2024) found human-like deviations from probability identities in four LLMs.
- Wolf, Kleine Buening, Krause and Mendler-Dünner (2026) found systematic violations of the law of total probability: estimates rebuilt from subgroups beat direct estimates. That is a classical, decomposition-based explanation of an LTP residual.
- Beuria (2026) tested six open-weight models and concluded that "the order data do not independently select a quantum account."
- Imannezhad, Pothos and Wills (2026) found GPT-5 nearly coherent: 18.8% of its conjunction judgments contained a fallacy, against 58.5% for humans, and only 0.5% of its fallacious judgments were double fallacies.

**The closest work to ours.** Kang (2026) audited an LLM's sequential answers against the QQ equality with a careful forced-branch protocol. The model's answer distributions were near-deterministic on 17 of 18 pairs. Swapping the labels changed the QQ verdict on 4 pairs, and no pair was certified contextual. Kang also proves that a classical "sometimes repeat your first answer" mechanism satisfies QQ exactly.

**Measurement critiques.** Dominguez-Olmedo, Hardt and Mendler-Dünner (2024), Tjuatja et al. (2024) and McCoy et al. (2024) show that LLM answer distributions shift with option labels, option order and output frequency. We adopt all of these critiques for our pending experiments.

**Where this leaves us.** The field has established robust human order effects and conjunction fallacies, the QQ regularity, and model-dependent probabilistic incoherence in LLMs. It has not established that any of these needs a quantum account: order data, QQ satisfaction and Bell-type values can each be met classically. Our contribution is a different kind of test.
- The state is built per item from the model's own stated considerations, so there is no state-placement freedom.
- The question is prediction of that model's errors on held-out items, against a classical twin with the same inputs.
- Hardware certifies separately that the entanglement is physically present.

---

## 3. Method as run

### 3.1 Items and base model

| pool | items | source | base model | wrong | file |
|---|---|---|---|---|---|
| standard (run 1) | 60 original + 75 computational extension (D4) | author-written puzzles and misconceptions; code-verified computations | `claude-sonnet-5-5`, effort `xhigh` | **0** of 117 answered (10 hit the 16,000-token cap) | `results/pool-run-1.md` |
| standard (run 2) | 125 | as above | `claude-haiku-5-5`, default effort (D5) | **4** of 125 | `results/pool-run-2.md` |
| hard (run 3) | 300 (D6) | 120 SimpleQA (MIT), 120 MMLU-Pro physics/chemistry (MIT), 60 author-written true/fabricated claims | `claude-haiku-5-5` | **44** of 300 | `results/pool-run-3.md` |
| training, v2 (run 5) | 1,048 (D9, D9b) | SimpleQA, MMLU-Pro biology/engineering/physics/chemistry, computed puzzles, verified claims | `claude-haiku-5-5` | [PENDING] | `results/pool-run-5.md` [PENDING] |

Every item records its source and licence. GPQA Diamond was not used, because its authors ask that items not be published in plain text.

### 3.2 Pipeline

For every question:

1. **Base call** (`claude-haiku-5-5`, adaptive thinking, `display: "summarized"`). The model answers with a brief explanation of the main considerations for and against, ending in `FINAL ANSWER: YES/NO`. The summarized thinking is archived and never sent to any other call (D1–D3).
2. **Extractor** (`claude-sonnet-5-5`). The visible answer is presented as a document, "a short written argument answering a yes/no question", and its distinct claims are listed as `{text, confidence, lean}`. Between 5 and 16 claims are kept.
3. **Relation judge** (`claude-haiku-5-5`). For every pair of claims: `supports`, `contradicts` or `unrelated`, with a strength.

### 3.3 Encoding and readout (pre-registered, fixed)

- **Qubits:** one per claim, 5–16 qubits.
- **Preparation:** RY(θ) with θ = confidence · π/2, then RZ(φ). The phases φ minimise the XY energy E(φ) = −Σ J_ij cos(φ_i − φ_j) − Σ lean_k cos φ_k, with J_ij = +strength for supports and −strength for contradicts. Phase 0 is "yes".
- **Entangling:** RZZ(κ · J_ij) for every related pair, κ = π/4.
- **Evolution:** N = 2 Trotter steps, with step k using s = k/(N+1).
  - Problem term exp(−iγ₀ s H_P), with H_P = −Σ J_ij X_i X_j − Σ lean_i X_i.
  - Mixer term exp(−iβ₀ (1−s) H_M), with H_M = −Σ Z_i.
  - γ₀ = 0.5, β₀ = 0.4.
- **Measurement:** X basis, 1,000 shots.
- **Readout:** each shot gives a weighted vote m = Σ w_k x_k, with w_k ∝ |lean_k|.
  - Judgment = yes if P(m > 0) ≥ 0.5.
  - Conflict score = 2 · min(P(m ≥ 1/3), P(m ≤ −1/3)), the mass on the weaker of two strongly opposed camps.

### 3.4 Arms

| arm | what runs | conflict / error score |
|---|---|---|
| **A** | entangled circuit, noisy Aer simulator built from `ibm_fez` | as above |
| **B** | the identical transpiled circuit on `ibm_fez` | as above, A's threshold (run only if the simulator gate opens) |
| **C** | A with every two-qubit term removed | as above |
| **D** | A built from a shuffled relation web (same number of relations and signed strengths, random pairs) | as above |
| **E** | classical, no qubits | total contradiction strength |
| **A0** | A on a noiseless simulator (supplementary) | as above |
| **F** | classical Ising twin: same graph, couplings and fields, exact enumeration over 2ⁿ configurations | share of the near-minimum energy landscape in strongly opposed camps |
| **G** | the base model's self-reported confidence (0–100) in its own visible answer | 100 − confidence |
| **L** | (version two) linear score on 8 relation-web features | fitted weights |

Every arm's flag threshold is the 75th percentile of its own scores on the calibration pool. This equalises *how much* each arm flags, so test-set differences reflect *where* the flags land. Arms F and G, bootstrap 95% intervals on every AUROC, and a 200-shuffle null distribution for arm D were pre-registered in Addendum A, after run 2 and before any F, G or null number existed.

### 3.5 Version two: learned encoding

The fixed constants above (κ, γ₀, β₀, N, the angle scale) were set a priori, not tuned. Version two asks whether learning them changes the result, under a rule that gives the quantum model no advantage (code: `src/entangled_mind/v2.py`).

- **A2, learned quantum encoding:**
  - a confidence-to-angle scale;
  - separate coupling scales for support and contradiction relations;
  - Trotter steps N ∈ {0,…,4};
  - two step scales;
  - a readout-basis angle;
  - the strong-camp threshold τ;
  - a flag threshold.
- **F2, learned classical twin:** the same graph, phases, priors and couplings, but a classical distribution evolved by N heat-bath sweeps (inverse-temperature schedule, independent-flip mixing). No amplitudes, no interference.
- **L, linear score:** eight relation-web features plus a bias:
  - contradiction count;
  - total contradiction strength;
  - total support strength;
  - number of claims;
  - mean confidence;
  - number of related pairs;
  - mean |lean|;
  - confidence mass leaning against the vote.
- **Same budget:** 9 parameters each, counting the flag threshold.
- **Same fitting rule:**
  - 400 uniform random parameter vectors;
  - hill-climb the 10 best on train AUROC, with 60 Gaussian perturbations each;
  - keep the climbed candidate with the highest validation AUROC;
  - set the flag threshold by Youden's J on train.
- **Discipline:**
  - The train/validation/test split (60/20/20, seed 2026, stratified by wrong/right × item type) is locked in `experiments/split-v2.json` before any fitting, and is never remade.
  - The run-2 hard pool, including its 80-item test set, stays a separate held-out set.
  - The v2 pass criteria are in `experiments/preregistration-v2.md` [PENDING: not yet committed].

### 3.6 Hardware

- **Backend:** IBM `ibm_fez` (Heron r2, 156 qubits), Open Plan (600 QPU s per month). The project's hard stop is 420 s.
- **Stage 1:** one circuit, as a test of the hardware path.
- **Entanglement witness** (`experiments/witness.md`, D8):
  - **Items:** for each of the 3 run-2 test items with the largest ideal pair negativity, take the related pair of claims whose two-qubit reduced state has the largest negativity N(ρ) = Σ|negative eigenvalues of ρ^{T_j}|. For two qubits, N > 0 if and only if the pair is entangled.
  - **Circuits:** 9 Pauli settings plus 4 readout-calibration circuits per item, built directly on the measured physical qubits. That is 39 circuits at 4,000 shots in one Batch.
  - **Analysis:** linear-inversion tomography, then 500 parametric bootstrap resamples.
  - **Rule fixed in advance:** an item is certified if the 95% lower bound on N is above 0; the run succeeds if at least 2 of 3 items are certified.

### 3.7 Experiments 3 and 4 (designed, not run)

**Experiment 3: order effects in the model's own contentions** (`experiments/exp3-order-effects.md`).

*The design.*
- The obvious design fails: projectors on different qubits commute, so the predicted order effect would be exactly zero. "Considering" contention k is therefore modelled as a local evolution U_k = exp(−iγ₀H_k), with H_k = −Σ_{j~k} J_kj X_k X_j − lean_k X_k − Z_k.
- The quantum prediction for pair (i, j) is Δᴼ_ij = |⟨Π_yes⟩ after U_jU_i − ⟨Π_yes⟩ after U_iU_j|.
- The classical twin's prediction Δᶠ_ij comes from sequential heat-bath updates of the same Ising model. Classical sequential updates can also depend on order, so the comparator is fair.

*The protocol.*
- Items: 40 run-2 test items (20 wrong, 20 right).
- Pairs: up to 6 per item, chosen at both models' extremes.
- Conversations: three-turn (consider *i*; consider *j*; answer the original question), 5 per pair and order, plus 5 single-turn baselines.
- Budget: capped at $4.00 [cost estimate from the pre-registration; actual spend PENDING].

**Experiment 4: conjunction/order co-occurrence** [PENDING: not yet pre-registered]. The candidate design is drafted in `experiments/items-borrowed.json → cooccurrence_rule`:
- elicit P(X), P(Y), P(X and Y) in both wordings, and both sequential orders;
- use classic, novel and fictional same-day event pairs;
- test the Yearsley–Trueblood rules (Section 6.3).

---

## 4. Pre-registration and deviations

The pre-registration (`experiments/preregistration.md`) was committed before any arm was run. The deviations log (`DEVIATIONS.md`) records every change, its date and its reason. In short:

| | what changed | why | effect on interpretation |
|---|---|---|---|
| **D1–D3** | Claims come from the model's *visible* explanation, not its hidden thinking. The extractor reads that explanation as a document. | The API's `reasoning_extraction` safeguard refused two designs. We redesigned per Anthropic's documented guidance rather than route around it. Sonnet 5.5 emitted no thinking block at low, medium or high effort on these items, and at `xhigh` only a one- or two-sentence summary. | Every result concerns the reasoning the model *wrote down*, which may be a tidied account of its deliberation. |
| **D4** | 75 code-verified computational items added. | Sonnet answered all 60 original items correctly. | Wrong items became mostly calculation slips. |
| **D5** | Base model changed from `claude-sonnet-5-5` (`xhigh`) to `claude-haiku-5-5` (default). | Sonnet answered all 117 checkable items correctly, so H2 could not be tested. | H2 criterion and arms unchanged. |
| **D6** | A 300-item hard pool (SimpleQA, MMLU-Pro, author-written claims). | Haiku got only 4 of 125 standard items wrong. | Errors are mostly ignorance-type and multi-step science, not conjunction- or order-type. |
| **D7** | Arms F and G, bootstrap intervals, 200-shuffle null for D (Addendum A). | Added after run 2, before any F/G/null number existed. | Reported alongside H2; H2 unchanged. |
| **D8** | Witness readout calibration built on the measured physical qubits. | The optimizing transpiler could move calibration circuits elsewhere. | Prediction recomputed; design otherwise as specified. |
| **D9, D9b** | 1,048-item training pool for v2; split locked before fitting. | v2 needs train/validation/test data separate from the run-2 test set. | The computed puzzles did not elicit errors from Haiku; its errors are SimpleQA and multi-step science. |
| **D10** | QPU-seconds parsing bug fixed and ledger repaired. | IBM Runtime reports `qpu_charge_time_seconds`. | Ledger now sums correctly. |

**From proposal to pre-registration.** Version 1 listed five hypotheses: divergence, entanglement signal, contextuality, emergence and human-likeness. The pre-registration replaced them with five that could be scored on the data the pipeline produces:
- H1, faithful encoding;
- H2, conflict detection, the primary;
- H3, entanglement carries information;
- H4, structure carries information;
- H5, hardware survives.

Version 1's contextuality, emergence and human-likeness questions are not abandoned. They return as Experiments 3 and 4 and as the borrowed items (`experiments/items-borrowed.json`).

**One note on sequencing.** The arms and statistics were added in stages (Addendum A after run 2; version two after run 2b). Each addition was committed before the data it governs existed, but readers should know the analysis grew after the primary result was in.

---

## 5. Results so far

### 5.1 Stage 1: the hardware path works

From `results/stage1-run-1.md`. Item `q01` (bat and ball) was encoded as 9 qubits with 33 RZZ gates and N = 0, and transpiled for `ibm_fez` to depth 208 with 117 CZ gates. The job waited 2 h 50 min in the queue and used 2 QPU seconds.

| run | P(yes) | judgment | conflict score | distinct bitstrings |
|---|---|---|---|---|
| ideal_sim | 0.294 | no | 0.276 | 235 |
| noisy_sim | 0.251 | no | 0.276 | 284 |
| hardware | 0.502 | yes | 0.666 | 336 |

Hardware washed the state out far more than the `ibm_fez` noise model predicts.

### 5.2 Stage 2, run 1: standard pool, 4 wrong + 10 hard-right items

From `results/stage2-run-1.md`. Under the D5 fallback rule, the right items are the 10 correct answers whose claims gave the model's answer the least support, so the right-item columns are biased upward.

| arm | threshold (from calibration) | calibration flag rate | wrong items flagged (of 4) | right items flagged (of 10) | AUROC test | judgment = model's answer (of 14) | judgment = truth (of 14) |
|---|---|---|---|---|---|---|---|
| A  entangled, noisy sim | 0.334 | 0.25 | 2 (50%) | 7 (70%) | 0.45 | 12 | 10 |
| B  entangled, real hardware | not run: simulator gate not met | | | | | | |
| C  no entangling gates | 0.008 | 0.21 | 4 (100%) | 10 (100%) | 0.51 | 12 | 10 |
| D  shuffled relation web | 0.193 | 0.25 | 1 (25%) | 6 (60%) | 0.42 | 11 | 9 |
| E  classical contradiction strength | 2.650 | 0.25 | 1 (25%) | 0 (0%) | 0.69 | 13 | 11 |
| A0 entangled, noiseless (supplementary) | 0.365 | 0.25 | 1 (25%) | 4 (40%) | 0.40 | 12 | 10 |

Hypotheses:
- **H1:** pass (0.86).
- **H2:** underpowered: only 4 known-wrong items (nominally fail).
- **H3:** falsified (A 0.45, C 0.51).
- **H4:** fail, not falsified (A 0.45, D 0.42).
- **H5:** untested.

### 5.3 Stage 2, run 2: hard pool, 40 wrong + 40 right items

From `results/stage2-run-2.md`. The calibration pool is 220 items, of which 4 are wrong.

| arm | threshold (from calibration) | calibration flag rate | wrong items flagged (of 40) | right items flagged (of 40) | AUROC test | AUROC calibration | judgment = model's answer (of 80) | judgment = truth (of 80) |
|---|---|---|---|---|---|---|---|---|
| A  entangled, noisy sim | 0.266 | 0.25 | 10 (25%) | 9 (22%) | 0.55 | 0.63 | 80 | 40 |
| B  entangled, real hardware | not run: simulator gate not met | | | | | | | |
| C  no entangling gates | 0.011 | 0.25 | 21 (52%) | 9 (22%) | 0.68 | 0.72 | 80 | 40 |
| D  shuffled relation web | 0.152 | 0.25 | 17 (42%) | 11 (28%) | 0.65 | 0.61 | 79 | 41 |
| E  classical contradiction strength | 2.325 | 0.25 | 18 (45%) | 10 (25%) | 0.64 | 0.68 | 80 | 40 |
| A0 entangled, noiseless (supplementary) | 0.279 | 0.25 | 9 (22%) | 11 (28%) | 0.49 | 0.50 | 80 | 40 |

Hypotheses:
- **H1:** pass (1.00).
- **H2:** **fail**. Wrong-item flag rates: A 0.25, C 0.53, D 0.42, E 0.45. The verdict is robust to any single item.
- **H3:** falsified (A 0.55, C 0.68).
- **H4:** falsified (A 0.55, D 0.65).
- **H5:** untested (simulator gate not met).

H1 passes trivially. The circuit's judgment tracks the model's answer because the claims are extracted from that answer.

**Pending re-scoring of run 2 (run 2b, Addendum A):**
- arm F AUROC [PENDING];
- arm G AUROC [PENDING];
- 95% bootstrap intervals for every arm [PENDING];
- arm A's position in the 200-shuffle arm-D null [PENDING];
- the second H2 line with F and G held to the same bar [PENDING].

### 5.4 Entanglement witness on real hardware

From `results/witness-run-1.md`. Job `dbl6e1d8mdtc73d5gesg` on `ibm_fez`: 39 circuits × 4,000 shots, **44 QPU seconds**.

| item | pair (physical qubits) | N ideal | N noisy sim [95% CI] | **N hardware [95% CI]** | hardware, unmitigated | certified |
|---|---|---|---|---|---|---|
| `h221` | (0, 6) on 10, 9 | 0.184 | 0.171 [0.157, 0.181] | **0.147 [0.134, 0.157]** | 0.140 | yes |
| `h088` | (5, 6) on 44, 37 | 0.175 | 0.149 [0.138, 0.162] | **0.063 [0.051, 0.075]** | 0.052 | yes |
| `h268` | (5, 6) on 4, 16 | 0.162 | 0.118 [0.105, 0.132] | **0.067 [0.055, 0.081]** | 0.058 | yes |

**3 of 3 items certified.** The pre-registered success rule (at least 2 of 3) is met, and the result holds without readout mitigation.

Two qualifications:
- For two items, hardware negativity is about half the noisy-simulator prediction. Together with Stage 1, this shows `ibm_fez` is noisier than its noise model.
- In `h221` the target pair's reduced state is pure (purity 1.000), so that pair is decoupled from the rest of its belief state and the test is effectively a two-qubit entangling test. The pairs in `h088` and `h268` are mixed (purity 0.746 and 0.819), so they are genuinely entangled with the rest of their belief states.

**QPU time used: 46 s** (Stage 1 2 s + witness 44 s; `results/ibm-usage.md`).

### 5.5 Pending experiments and their pre-registered criteria

**Version two** (A2, F2 and L on the locked v2 split).
- Test-set AUROC for each model, with 95% intervals [PENDING].
- Pass criteria: in `experiments/preregistration-v2.md` [PENDING: not yet committed].
- The comparison that matters is A2 against F2: the same graph, the same budget, the same fitting rule, with and without amplitudes and interference.

**Experiment 3** (order effects).
- **Primary:** across all item-pairs, the Spearman correlation ρ(Δᴼ, observed) exceeds ρ(Δᶠ, observed).
  - The 95% CI for ρᴼ − ρᶠ comes from 2,000 bootstrap resamples of items.
  - **Pass** if the CI excludes 0 on the positive side; **fail** if it excludes 0 on the negative side; otherwise **inconclusive**.
- **Secondary:**
  1. Do order effects exist at all? Mean observed order effect against the split-half baseline variability, by permutation test. If this fails, the experiment cannot discriminate the two models, and that is what is reported.
  2. Do the 2 largest-Δᴼ pairs per item show larger observed effects than the 2 smallest? Paired Wilcoxon test over items.
- **Falsifying null for the quantum claim:** ρᴼ ≤ ρᶠ.
- Results: [PENDING].

**Experiment 4** (co-occurrence).
- Pre-registration [PENDING].
- Results [PENDING].

---

## 6. Discussion

### 6.1 What the negative result on H2 means

The entangled readout does worse at finding the model's errors than every control, including the same circuit with its entangling gates removed. Three features of the result rule out the easy explanations.
- **It is not hardware noise.** The noiseless entangled state (A0) scored 0.49.
- **It is not a fluke of one item.** The H2 verdict is robust to any single item.
- **It is not a failure of the readout to track the model.** H1 passes, and the readout gives the model's own answer on 80 of 80 items.

What the entangling step seems to do is **spread** the signal. The unentangled circuit's conflict score (arm C, AUROC 0.68) reflects how the single-claim amplitudes are split between claims leaning yes and claims leaning no. The coupling and evolution then mix those amplitudes across the whole state, and the mixed state's split between opposed camps carries less information about errors than the unmixed one did.

The more interesting reading is about structure. Arm D, which places the same relation strengths on *random* pairs, scored 0.65 and beat the correctly wired circuit. Where the relations sit mattered less than how many contradictions there were and how strong.

What the result does not show:
- **It is not a verdict on quantum cognition.** That programme models human aggregate judgments; we tested one encoding of one model's written explanations as an error detector.
- **It is not a verdict on learned encodings.** The constants (κ, γ₀, β₀, N = 2) were set a priori, and version two asks whether learning them changes anything, against a classical twin given exactly the same chance.
- **It is not a verdict on all error types.** The model's errors on the hard pool are mostly ignorance (SimpleQA) and multi-step science (D6, D9b), not the order- and conjunction-type errors where quantum models have their best human evidence.

On this pool, with this encoding, the answer to "do machines need quantum minds?" is no.

### 6.2 What the classical contradiction signal means

Something does predict the model's errors: the classical structure of its own explanation.
- Total contradiction strength between its stated claims (arm E) gives AUROC 0.64.
- The unentangled per-claim spread (arm C) gives 0.68.

On items the model gets wrong, its brief explanation more often contains considerations that pull against each other. That is a modest but real finding about language-model self-explanations, and it needs no qubits. Two pending numbers decide how much it is worth:
- **The confidence intervals** [PENDING]. Most AUROCs here may overlap at n = 80.
- **Arm G, the model's own stated confidence** [PENDING]. If G matches E, the contradiction signal is just the uncertainty the model can already report. If E adds to G, the relation web carries information the model does not volunteer about itself.

This reframes the project's central question. Version 1 hoped the entangled state would let contradictions *cancel* and so expose conflicts the model cannot see. The data say that the conflicts are visible in plain bookkeeping: count the contradictions. The quantum layer has to beat that bookkeeping to earn its place, and so far it does not.

### 6.3 The sharp Yearsley–Trueblood test, and why the classical twin cannot fake it

Order effects alone cannot select a quantum account. Kang's classical repetition model satisfies the QQ equality exactly, and Beuria's order-invariant classical joint matches small QQ residuals. Experiment 4 is designed around a prediction with more bite, adapted from Yearsley and Trueblood (2018) and the quantum conjunction model of Busemeyer et al. (2011). In that model a conjunction is judged sequentially: P(X then Y) = ‖P_Y P_X ψ‖².

- **R1, necessity.** A single conjunction fallacy, P(X and Y) > P(Y), requires X and Y to be incompatible. Incompatible events predict an order effect for the same pair. A reliable fallacy with no order effect counts against the account.
- **R2, the bound.** Because ‖P_X P_Y ψ‖² ≤ ‖P_Y ψ‖², a fallacy relative to Y forces P(X then Y) − P(Y then X) ≥ P(X then Y) − P(Y). The order effect on the conjunction must be at least as large as the fallacy.
- **R3, no double fallacies.** P(X and Y) > max(P(X), P(Y)) is impossible.

**Why the classical twin cannot fake this.** Arm F reads every judgment from one joint distribution over configurations of the same claims. In any such model, P(X and Y) ≤ min(P(X), P(Y)) and P(X then Y) = P(Y then X) hold *identically*. No setting of F's couplings, fields or temperature produces a single fallacy or a conjunction-order effect. This is a structural zero, not a tuning failure, so a reliable fallacy-plus-bounded-order-effect pattern in the model's judgments is out of F's reach however F is fitted.

**What it does not rule out.** A classical model in which each judgment *updates* the state can produce fallacies and order effects, and it also satisfies R2, because for it too P(Y then X) ≤ P(Y). Our literature notes first overstated this point; it is corrected there. Experiment 3's sequential classical twin is such a model.

**The test against that rival** is numerical, per item, from a state fixed in advance. The quantum model and the sequential twin each predict, from the same claims and couplings and with no refitting, how large the fallacy and the order effect should be for each pair. The model's observed magnitudes then decide between them. That is the structure of Experiment 3, and the one Experiment 4 will follow when it is pre-registered.

### 6.4 What the hardware result means

The witness separates two claims that behavioural Bell tests conflate:
- *the system holds an entangled state*;
- *the outcomes shift with context*.

For our belief states the first is now certified on real hardware. The second, the claim that entanglement helps judgment, is answered negatively on the simulator. At 5–16 qubits every state is exactly classically simulable, so hardware offers no speed-up and no capability the simulator lacks. Its role is demonstration and certification, and it played that role.

---

## 7. Implications

Version 1 described what would follow if the hypotheses held. Most did not. What follows from what we found:

**Physics.** A real quantum processor held the entangled states of a language model's belief webs, with negativity well above zero on 3 of 3 items. That is a modest demonstration: a near-term use of hardware for certification rather than speed. The same runs show the device noisier than its published noise model, with two items reaching about half their simulated negativity. Any claim about "cognitive work" done by entanglement on current hardware should budget for that.

**Psychology.** Quantum cognition is a family of models fitted to human aggregates. Our results neither confirm nor refute it, because we did not test human data. What we offer the field is a method: build the state per item from stated reasons, then compare against a classical twin with the same inputs and parameter budget. The borrowed items (Animal Acts, Linda, QQ pairs, co-occurrence) let that method meet the classic effects directly. Our recomputations of published Bell-type data are offered in the same spirit.

**Philosophy of mind.** Version 1 hoped to give the intuition that a mind is a unity rather than a sum an experimental correlate. A machine judgment layer built as a genuine whole, certified entangled, turned out to judge no better than one built as a list, and slightly worse at knowing when it is wrong. That does not settle anything about minds. It does show that being an indecomposable whole is not, by itself, an advantage for this kind of judgment. Any argument from "unity" to function needs a mechanism, not just the mathematics.

**Artificial intelligence.** The useful component found so far is classical. The structure of a model's own stated considerations predicts its errors on a hard pool, before comparison with the model's self-reported confidence [PENDING]: how strongly they contradict each other gives AUROC 0.64, and how they split between yes and no gives 0.68. If that holds up, it is a cheap error flag that sits between a model's reasoning and its answer, which is what version 1 wanted the quantum layer to be. The window, which is designed but not yet built, remains the way to inspect *why* the quantum layer loses that signal.

---

## 8. Limitations

- **Visible explanations, not deliberation.** Claims come from a brief explanation the model writes for the reader (D1–D3), which may be a tidied account of how it reached the answer. A model whose internal deliberation could be accessed safely might give a different web.
- **One base model, mostly one error type.** All Stage 2 results use `claude-haiku-5-5`. Its errors on the hard pool are mostly gaps in knowledge and multi-step science, not the judgment errors quantum cognition studies.
- **Models judging models.** The extractor and relation judge are language models. Their errors enter every arm equally, but they bound what any arm can find.
- **Small test sets.** Run 1 had 4 wrong items. Run 2 had 80 items in all, where a single item is worth 2.5 percentage points of flag rate. Confidence intervals are [PENDING].
- **Fixed constants.** The version-one encoding was not tuned. Version two addresses this, under the same rules for the classical twin.
- **Analysis grew after the primary result.** Arms F, G and L and the shuffle null were each pre-registered before their data existed, but after run 2's result was known.
- **Hardware scope.** The witness certified one pair in each of 3 items, and one of those pairs is effectively a two-qubit test. Arm B never ran, so H5 is untested.
- **Borrowed items are not matched benchmarks.** Our yes/no versions of Linda differ from the original ranking and choice formats. Classic vignettes are probably in training data.
- **The window is not built.** Every run is archived as JSON, but the visual display that would let a reader watch a collapse does not yet exist.
- **Single author, no independent replication.** All code, data and decisions are public, but nobody else has yet run them.

---

## References

Aerts, D. (2009). Quantum structure in cognition. *Journal of Mathematical Psychology, 53*(5), 314–348. https://doi.org/10.1016/j.jmp.2009.04.005

Aerts, D., Aerts Arguëlles, J., Beltran, L., Geriente, S., Leporini, R., Sassoli de Bianchi, M., & Sozzo, S. (2026). Identifying quantum structure in AI language: Evidence for evolutionary convergence of human and artificial cognition. *Entropy, 28*(6), 622. https://doi.org/10.3390/e28060622 (arXiv:2511.21731, 2025)

Aerts, D., & Sozzo, S. (2011). Quantum structure in cognition: Why and how concepts are entangled. In *Quantum Interaction 2011*, Lecture Notes in Computer Science 7052 (pp. 116–127). Springer. https://doi.org/10.1007/978-3-642-24971-6_12

Beuria, J. (2026). Emergent non-classical probabilistic structure in large language models under contextual modulations. *Scientific Reports*. https://doi.org/10.1038/s41598-026-65824-7

Binz, M., & Schulz, E. (2023). Using cognitive psychology to understand GPT-3. *Proceedings of the National Academy of Sciences, 120*(6), e2218523120. https://doi.org/10.1073/pnas.2218523120

Boyer-Kassem, T., Duchêne, S., & Guerci, E. (2016a). Testing quantum-like models of judgment for question order effect. *Mathematical Social Sciences, 80*, 33–46. https://doi.org/10.1016/j.mathsocsci.2016.01.001

Bruza, P. D., Wang, Z., & Busemeyer, J. R. (2015). Quantum cognition: A new theoretical approach to psychology. *Trends in Cognitive Sciences, 19*(7), 383–393. https://doi.org/10.1016/j.tics.2015.05.001

Busemeyer, J. R., & Bruza, P. D. (2012). *Quantum models of cognition and decision*. Cambridge University Press. https://doi.org/10.1017/CBO9780511997716

Busemeyer, J. R., Pothos, E. M., Franco, R., & Trueblood, J. S. (2011). A quantum theoretical explanation for probability judgment errors. *Psychological Review, 118*(2), 193–218. https://doi.org/10.1037/a0022542

Busemeyer, J. R., Wang, Z., & Townsend, J. T. (2006). Quantum dynamics of human decision-making. *Journal of Mathematical Psychology, 50*(3), 220–241. https://doi.org/10.1016/j.jmp.2006.01.003

Dominguez-Olmedo, R., Hardt, M., & Mendler-Dünner, C. (2024). Questioning the survey responses of large language models. In *Advances in Neural Information Processing Systems 37*. arXiv:2306.07951

Dzhafarov, E. N., & Kujala, J. V. (2014). On selective influences, marginal selectivity, and Bell/CHSH inequalities. *Topics in Cognitive Science, 6*(1), 121–128. https://doi.org/10.1111/tops.12060

Fiedler, K. (1988). The dependence of the conjunction fallacy on subtle linguistic factors. *Psychological Research, 50*(2), 123–129. https://doi.org/10.1007/BF00309212

Fuyama, M., Khrennikov, A., & Ozawa, M. (2025). Quantum-like cognition and decision-making in the light of quantum measurement theory. *Philosophical Transactions of the Royal Society A, 383*(2309), 20240372. https://doi.org/10.1098/rsta.2024.0372

Hertwig, R., & Gigerenzer, G. (1999). The 'conjunction fallacy' revisited: How intelligent inferences look like reasoning errors. *Journal of Behavioral Decision Making, 12*(4), 275–305. https://doi.org/10.1002/(SICI)1099-0771(199912)12:4<275::AID-BDM323>3.0.CO;2-M

Imannezhad, P., Pothos, E. M., & Wills, A. J. (2026). Divergent patterns of probabilistic reasoning in humans and GPT-5. *Frontiers in Psychology, 17*, 1782184. https://doi.org/10.3389/fpsyg.2026.1782184

Javadi-Abhari, A., Treinish, M., Krsulich, K., Wood, C. J., Lishman, J., Gacon, J., Martiel, S., Nation, P. D., Bishop, L. S., Cross, A. W., Johnson, B. R., & Gambetta, J. M. (2024). Quantum computing with Qiskit. arXiv:2405.08810. https://doi.org/10.48550/arXiv.2405.08810

Kang, P. (2026). Auditing question-order effects in large language models with the QQ equality: Mechanism characterization and a saturation caveat. arXiv:2607.17219

Khrennikov, A., Basieva, I., Dzhafarov, E. N., & Busemeyer, J. R. (2014). Quantum models for psychological measurements: An unsolved problem. *PLoS ONE, 9*(10), e110909. https://doi.org/10.1371/journal.pone.0110909

Kujala, J. V., & Dzhafarov, E. N. (2016). Proof of a conjecture on contextuality in cyclic systems with binary variables. *Foundations of Physics, 46*(3), 282–299. https://doi.org/10.1007/s10701-015-9964-8

McCoy, R. T., Yao, S., Friedman, D., Hardy, M. D., & Griffiths, T. L. (2024). Embers of autoregression show how large language models are shaped by the problem they are trained to solve. *Proceedings of the National Academy of Sciences, 121*(41), e2322420121. https://doi.org/10.1073/pnas.2322420121

Ozawa, M., & Khrennikov, A. (2020). Application of theory of quantum instruments to psychology: Combination of question order effect with response replicability effect. *Entropy, 22*(1), 37. https://doi.org/10.3390/e22010037

Ozawa, M., & Khrennikov, A. (2021). Modeling combination of question order effect, response replicability effect, and QQ-equality with quantum instruments. *Journal of Mathematical Psychology, 100*, 102491. https://doi.org/10.1016/j.jmp.2020.102491

Pothos, E. M., & Busemeyer, J. R. (2009). A quantum probability explanation for violations of 'rational' decision theory. *Proceedings of the Royal Society B, 276*(1665), 2171–2178. https://doi.org/10.1098/rspb.2009.0121

Pothos, E. M., & Busemeyer, J. R. (2013). Can quantum probability provide a new direction for cognitive modeling? *Behavioral and Brain Sciences, 36*(3), 255–274. https://doi.org/10.1017/S0140525X12001525

Tjuatja, L., Chen, V., Wu, T., Talwalkar, A., & Neubig, G. (2024). Do LLMs exhibit human-like response biases? A case study in survey design. *Transactions of the Association for Computational Linguistics, 12*, 1011–1026. https://doi.org/10.1162/tacl_a_00685

Tversky, A., & Kahneman, D. (1983). Extensional versus intuitive reasoning: The conjunction fallacy in probability judgment. *Psychological Review, 90*(4), 293–315. https://doi.org/10.1037/0033-295X.90.4.293

Wang, Z., & Busemeyer, J. R. (2013). A quantum question order model supported by empirical tests of an a priori and precise prediction. *Topics in Cognitive Science, 5*(4), 689–710. https://doi.org/10.1111/tops.12040

Wang, Z., Solloway, T., Shiffrin, R. M., & Busemeyer, J. R. (2014). Context effects produced by question orders reveal quantum nature of human judgments. *Proceedings of the National Academy of Sciences, 111*(26), 9431–9436. https://doi.org/10.1073/pnas.1407756111

Wolf, P., Kleine Buening, T., Krause, A., & Mendler-Dünner, C. (2026). Partition, prompt, aggregate: Statistical self-consistency in language models. arXiv:2607.15277

Yearsley, J. M., & Trueblood, J. S. (2018). A quantum theory account of order effects and conjunction fallacies in political judgments. *Psychonomic Bulletin & Review, 25*(4), 1517–1525. https://doi.org/10.3758/s13423-017-1371-z

Zhu, J.-Q., & Griffiths, T. L. (2024). Incoherent probability judgments in large language models. arXiv:2401.16646

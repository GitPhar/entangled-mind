# The Entangled Mind: Quantum Cognition as a Cognitive Architecture for Language Models

**Sean Pharris**, independent researcher

> *Do machines need quantum minds?*

## Abstract

Quantum-cognition models describe human judgment with amplitudes, interference and entanglement rather than classical probabilities. This project asks whether the same idea is useful as an architecture around a language model. For each yes/no question, a language model answers and briefly explains the considerations for and against. Those claims are extracted, and every pair is judged to support, contradict, or be unrelated to the other. The resulting web becomes one entangled quantum state: one qubit per claim, with confidence setting the amplitude and a solved phase setting the stance. RZZ gates link related claims, and a short Ising-style evolution runs before measurement in a "yes"-oriented basis. The readout gives a judgment, a confidence, and a conflict flag for shots that split between strongly opposed configurations. The pre-registered test is whether that flag picks out the model's wrong answers better than three controls: the same circuit with no entanglement, the same circuit with a shuffled relation web, and plain classical contradiction-counting. The last is the control that matters most.

**Status:** every planned experiment has run.
- **No quantum advantage.** Every pre-registered test of a quantum advantage failed or tied: the entangled readout, the learned v2 and v2.1 encodings, sequential judgment (experiment 5), and the order-effect tests (experiments 3 and 4).
- **Every positive quantum-vs-classical difference is classical.** Each one, on held-out data and on a second base model, is matched by a classical model given the same per-claim readout.
- **Self-report does as well.** The base model's own stated confidence predicts its errors as well as anything here, for both Haiku and Sonnet.
- **Hardware.** The encoded belief states are certified entangled on real hardware (3 of 3 items, 44 QPU s).

## Hypotheses, and the null result that falsifies each

Full definitions are in [`experiments/preregistration.md`](experiments/preregistration.md).

| | hypothesis | falsified if |
|---|---|---|
| **H1** faithful encoding | Arm A's judgment matches the base model's own answer on ≥ 70% of test items | agreement ≤ 50% (no better than a coin flip) |
| **H2** conflict detection (primary) | A flags conflict on ≥ 10% of known-wrong items, while C, D and E each flag at no more than half of A's rate | A flags < 10% of wrong items, or any control reaches ≥ half of A's rate |
| **H3** entanglement carries information | A's AUROC (wrong vs right) exceeds C's by ≥ 0.10 | C's AUROC ≥ A's |
| **H4** structure carries information | A's AUROC exceeds D's by ≥ 0.10 | D's AUROC ≥ A's (a random web does as well) |
| **H5** hardware survives | B's conflict scores correlate with A's (Spearman ≥ 0.5), and B flags ≥ 10% of wrong items | correlation ≤ 0, or B flags no wrong item |

If arm E (plain contradiction-counting) flags wrong answers as well as arm A, the quantum state carries nothing beyond the relation table, and this README says so.

## The five arms

| arm | what runs |
|---|---|
| **A** | entangled circuit, N = 2 Trotter steps, Qiskit Aer noisy simulator built from the real backend (`AerSimulator.from_backend(ibm_fez)`) |
| **B** | the identical transpiled circuit on real IBM hardware (`ibm_fez`, Heron r2), all 20 test circuits as one job in a Batch |
| **C** | same circuit with every entangling term removed |
| **D** | same circuit built from a shuffled relation web (same number of relations and the same strengths, on random pairs) |
| **E** | classical control with no qubits: total contradiction strength, thresholded on the calibration pool |

Every arm uses 1,000 shots. Each arm's conflict threshold is set on the calibration pool so that it flags the top quartile there. This equalises how much each arm flags, so any difference on the test set reflects *where* the flags land. Every readout, including the raw counts, is archived as JSON in `results/`.

## Results

Each cell: wrong items flagged · right items flagged · test-set AUROC (wrong vs right; 0.5 = chance). Every arm's threshold flags the top quartile of its own calibration pool. Base model `claude-haiku-5-5`; full tables in [`results/stage2-run-1.md`](results/stage2-run-1.md) and [`results/stage2-run-2.md`](results/stage2-run-2.md).

| arm | run 1: standard pool (4 wrong + 10 hard-right) | run 2: hard pool (40 wrong + 40 right) |
|---|---|---|
| **A** entangled, noisy sim | 2/4 · 7/10 · 0.45 | 10/40 · 9/40 · 0.55 |
| **B** entangled, real hardware (`ibm_fez`) | not run | not run |
| **C** no entangling gates | 4/4 · 10/10 · 0.51 | 21/40 · 9/40 · 0.68 |
| **D** shuffled web | 1/4 · 6/10 · 0.42 | 17/40 · 11/40 · 0.65 |
| **E** classical contradiction strength | 1/4 · 0/10 · 0.69 | 18/40 · 10/40 · 0.64 |
| A0 entangled, noiseless (supplementary) | 1/4 · 4/10 · 0.40 | 9/40 · 11/40 · 0.49 |

| | run 1 | run 2 |
|---|---|---|
| H1 faithful encoding | pass | pass |
| **H2 conflict detection** | underpowered: only 4 known-wrong items (nominally fail) | **fail** |
| H3 entanglement carries information | falsified | falsified |
| H4 structure carries information | fail (not falsified) | falsified |
| H5 hardware survives | untested | untested |

**What this says.** On the hard pool, the pre-registered test H2 fails, and the result does not hinge on any single item. Arm A flags 25% of the known-wrong items and 22% of the right ones, which is barely better than chance (AUROC 0.55). Every control does better:
- **C**, the same circuit with the entanglement removed: AUROC 0.68
- **D**, a randomly shuffled relation web: 0.65
- **E**, plain contradiction-counting with no qubits: 0.64

The noiseless entangled state A0 scores 0.49. **Plain contradiction-counting (arm E) flags wrong answers better than the entangled quantum state, so in this design the quantum state carries no error signal beyond what is already in the relation table. If anything, the entangling step destroys signal that the unentangled circuit keeps.**

H1 passes trivially. The judgment readout tracks the model's own answer, because the claims are extracted from that answer, so it says nothing about whether the encoding adds anything.

**Hardware.**
- Backend: `ibm_fez` (Heron r2, 156 qubits). Noise models for arms A, C and D come from this backend.
- **Stage 1 (one circuit) returned real counts.** Job `dbl423dgg49c73dk0db0` encoded the bat-and-ball item as 9 qubits with 33 RZZ gates (117 CZ after transpiling). It waited 2 h 50 min in the Open Plan queue, then returned 1,000 shots across 336 distinct bitstrings, for **2 QPU seconds**. See [`results/stage1-run-1.md`](results/stage1-run-1.md). Real hardware washed the state out much more than the noise model predicts: P(yes) was 0.50 on hardware, against 0.25 on the noisy simulator and 0.29 ideal.
- Arm B (the 20-circuit hardware arm) was not submitted, because the simulator gate (A beating every control) was not met in either run.
- **QPU seconds used so far: 46** (Stage 1: 2 s; witness: 44 s) of the 600 s monthly allowance (ledger: [`results/ibm-usage.md`](results/ibm-usage.md)).

### Since run 2

**Run 2b: seven arms, with intervals** ([`results/stage2-run-2b.md`](results/stage2-run-2b.md)). This adds arms F and G and a 200-shuffle null for arm D, all pre-registered in Addendum A.
- **G, the base model's own self-reported confidence, reaches AUROC 0.82** [0.71, 0.90]. That beats every arm built from the deliberation structure.
- The real relation web (arm A, 0.55) scores **below 99% of 200 random webs** with the same strengths (null mean 0.62).
- Arm F, the exact classical Ising twin, is degenerate as pre-registered: every conflict score is 0, so its AUROC is 0.50. This is reported as is, not redefined.
- The split analysis ([`results/stage2-run-2-split.md`](results/stage2-run-2-split.md)) shows the same pattern within SimpleQA, within science, and within items with 3 or more contradictions.

**Version two: learned encodings** ([`results/v2-run-1.md`](results/v2-run-1.md), [`results/v2.1-run-1.md`](results/v2.1-run-1.md)). Each model has 9–10 parameters. All were fitted on a 629-item train split and selected on validation, and the locked 209-item test set was scored once.

| model (locked test: 32 wrong, 177 right) | AUROC [95% CI] |
|---|---|
| A2, learned quantum encoding | 0.83 [0.75, 0.90] |
| F2, learned classical twin | 0.84 [0.78, 0.89] |
| A2.1, honest-hedge quantum (noiseless / noisy `ibm_fez` simulator) | 0.84 [0.75, 0.90] / 0.84 [0.75, 0.90] |
| F2.1, honest-hedge classical twin | 0.82 [0.76, 0.88] |
| L, relation-web features | 0.79 [0.70, 0.86] |
| G, self-reported confidence (no fitting) | 0.83 [0.78, 0.89] |
| H, hedge count (no fitting) | 0.67 [0.57, 0.76] |

- **The learned quantum encoding ties its classical twin, in both v2 and v2.1. Both pre-registered pass criteria are not met.**
- A2's learned entangling couplings fitted **near zero** (0.12 and 0.21, against 1 in v1). Candidates with couplings anywhere from 0.06 to 1.5 scored the same on train, so the fit found that the quantum part adds nothing on this task.
- The honest-hedge uncertainty term fitted to weight 0 in both families.
- On the run-2 held-out set the quantum family beat its twin (A2.1 0.84 vs F2.1 0.72). That is a secondary comparison, mostly on SimpleQA, and it comes from the learned readout geometry, not entanglement. G scores the same 0.82 there.

**Experiment 3: order effects** ([`results/exp3-run-1.md`](results/exp3-run-1.md)). The result is inconclusive.
- The base model showed **no detectable order effects**. Only 27 of 218 item-pairs differ at all between orders (permutation p = 0.24), and on its own it gives the same answer in all 5 runs for 85% of items.
- The point estimate favours the classical twin (ρ = +0.08) over the quantum prediction (ρ = −0.03).

**Experiment 4: quantitative Yearsley & Trueblood** ([`results/exp4-run-1.md`](results/exp4-run-1.md)). The pre-registered test is untestable.
- Graded ratings show conjunction fallacies on 7 of 16 items, and no double fallacies.
- The binary QQ phase saturated completely: "Is it true that <Y>?" was answered "no" every time.
- A graded run 2 is pre-registered (D17).

**Experiment 4, run 2: graded order test** ([`results/exp4-run-2.md`](results/exp4-run-2.md)).
- Graded ratings show real order effects of about +0.10, and R2 holds on all 3 scored items.
- The pre-registered anchoring estimator turned out to be near-tautological (D19), so the mechanism is undetermined.

**What the secondary quantum edges are** ([`results/sonnet-ablation.md`](results/sonnet-ablation.md), Addenda D and E). Both outcomes are pre-registered outcome 1: single-claim readout geometry, carried by a classical model.
- Setting A2's couplings to exactly 0 changes nothing (−0.009 and −0.006).
- A classical twin given A2's per-claim tilted-readout marginal (F2+) matches A2 on all three sets:
  - Haiku's locked test set: +0.015 [−0.042, +0.073];
  - Sonnet's hard pool: +0.004 [−0.032, +0.042];
  - Haiku's run-2 held-out set: −0.019 [−0.073, +0.029].

**Second base model, `claude-sonnet-5-5`** ([`results/sonnet-replication.md`](results/sonnet-replication.md)). On Sonnet's 298 hard-pool answers (30 wrong), the frozen v2 models transfer:

| model | AUROC |
|---|---|
| A2 | 0.90 |
| F2 | 0.82 |
| L | 0.73 |
| H | 0.66 |
| Sonnet's own self-reported confidence | **0.91** |

- The training-pool replication was halted after two extractor refusals (D20, D25).

**Experiment 5: sequential judgment** ([`results/exp5-run-1.md`](results/exp5-run-1.md)). The verdict is a **tie**, as the pre-registration predicted (§8.6: "expect A5 and F5 to be close on most claims").
- Graded sequential ratings show large order effects: 60 of 80 adjacent pairs.
- The QQ equality is close (mean q = +0.005 [−0.058, +0.065]) but not certified.
- There is no Kvam interference (Δ_K = +0.29 [−1.12, +1.65]).
- A classical Markov chain (D5) does as well as the coherent quantum state, so coherence is not what any A5 advantage rests on.
- 12,600 conversations, $1.93.

## Related work

**Quantum cognition.** Quantum probability as a model of human judgment builds on the following:
- Aerts's work on quantum structure in concept combination (D. Aerts, "Quantum structure in cognition," *Journal of Mathematical Psychology* 53, 2009).
- The program set out by J. R. Busemeyer and P. D. Bruza in *Quantum Models of Cognition and Decision* (Cambridge University Press, 2012).
- E. M. Pothos and J. R. Busemeyer's review, "Can quantum probability provide a new direction for cognitive modeling?" (*Behavioral and Brain Sciences* 36, 2013).

Question-order effects are central to this project's experiment 3. The quantum account of them, and its parameter-free QQ-equality prediction, comes from:
- Z. Wang and J. R. Busemeyer, "A quantum question order model supported by empirical tests of an a priori and precise prediction" (*Topics in Cognitive Science* 5, 2013)
- Z. Wang, T. Solloway, R. M. Shiffrin and J. R. Busemeyer, "Context effects produced by question orders reveal quantum nature of human judgments" (*PNAS* 111, 2014)

The conjunction items in the question pool follow Tversky and Kahneman's "Linda" problem (*Psychological Review* 90, 1983).

**Quantum-like structure in language models.** Several recent studies put language models through the same tests:
- **Aerts and colleagues**, "Identifying Quantum Structure in AI Language: Evidence for Evolutionary Convergence of Human and Artificial Cognition" ([arXiv:2511.21731](https://arxiv.org/abs/2511.21731), 2025; also *Entropy* 28(6):622). They ran human concept-combination tests on ChatGPT and Gemini and found responses that violate the CHSH form of Bell's inequality. They also report Bose–Einstein-type statistics in the words the models produce, and read both as quantum structure emerging in conceptual-linguistic domains.
- **Beuria (2026)**, as summarised by Springer Nature (we could access only the summary). Six open-weight models systematically violated classical probability identities, but no single framework accounted for the departures, and question-order data alone did not select a quantum account.
- **P. Kang**, "Auditing Question-Order Effects in Large Language Models with the QQ Equality: Mechanism Characterization and a Saturation Caveat" ([arXiv:2607.17219](https://arxiv.org/abs/2607.17219), 2026). The paper shows that classical mechanisms, including simple repetition, can satisfy the QQ equality exactly. It pairs QQ with a Contextuality-by-Default bound, and in a one-model pilot it finds outputs too near-deterministic to certify any item as contextual. That caveat applies directly to experiment 3 here.
- **P. Wolf, T. Kleine Buening, A. Krause and C. Mendler-Dünner.** They show that LLMs systematically violate the law of total probability: prior-weighted conditional answers do not recompose into the model's marginal answer. Secondary sources differ on the paper's title, and we have not tied it to a quantum account; it is a test of classical coherence.

**What those works test, and what this project adds.** Those studies treat a language model as a *subject*. They give it human-style probes (Bell/CHSH tests, conjunction and order questions, total-probability decompositions) and ask whether its *answers* break classical probability. This project instead treats quantum structure as an *architecture* around the model, and tests whether it is useful. It adds four things:
1. **States built from the model's own deliberation.** Each belief state is built from the claims in the model's explanation of a specific answer, with confidences, leans and a judged relation web. It is not a generic probe.
2. **A practical target with strong classical controls.** The target is predicting the model's own errors. The controls include an exact classical Ising twin of the same graph (arm F), plain contradiction-counting (arm E) and the model's self-reported confidence (arm G). They are fixed before results exist, so a quantum encoding cannot win against a strawman.
3. **Hardware certification.** An entanglement witness on real IBM hardware shows that the encoded belief states are physically entangled, not just entangled on paper.
4. **The window.** This is the project's per-item visual display (`window/`). Each of the model's claims is a point whose brightness is its amplitude and whose hue is its phase, with relation edges between them. A timeline steps through encode, entangle, evolve and collapse, beside the as-run `ibm_fez` circuit. Quantum-cognition models are fitted to aggregate answer frequencies, and the LLM studies observe only answers. Here the state behind each judgment is constructed, simulable exactly at 5–16 qubits, recorded and inspectable item by item.

So far the answer is negative.
- The entangled readout predicted errors worse than its classical controls.
- Learned quantum encodings tied their classical twins.
- The model's own stated confidence was as good as anything built from its deliberation.
- The base model showed no detectable order effects in yes/no form.

That is consistent with the order-effect and probability-identity literature not yet selecting a quantum account for LLMs. The full literature notes, with what each study tested, on whom, and what we borrow, are in [`paper/related-work.md`](paper/related-work.md).

## What the hardware does and does not show

- **No speedup.** Every belief state here has 5–16 qubits, so it is exactly classically simulable. A laptop computes the same state exactly (arm A0) or under a device noise model (arm A). Running on a quantum processor provides **no computational advantage** at this size.
- **What hardware is for here: demonstration and certification.** It can confirm that a physical device held the entangled state the encoding describes, and that the effect survives real noise.
- **What it cannot show:** that the quantum structure helps the judgment. On the simulator, Stage 2 shows it does not.
- **Use of the QPU budget:** an **entanglement witness**, designed in [`experiments/witness.md`](experiments/witness.md). It is two-qubit tomography of the most strongly entangled pair of contentions in the belief state of 3 test items, with negativity as the witness. After Sean approved the budget it ran as job `dbl6e1d8mdtc73d5gesg` on `ibm_fez` (39 circuits, 44 QPU seconds).

  **Entanglement was certified on real hardware for 3 of 3 items**, meeting the pre-registered rule of at least 2 of 3. Hardware negativity was 0.147 [0.134, 0.157], 0.063 [0.051, 0.075] and 0.067 [0.055, 0.081]. It also clears zero without readout mitigation. Hardware loses more than the noise model predicts: two items reached about half their simulated negativity. One of the three pairs is decoupled from the rest of its belief state, so it is effectively a two-qubit test. Details: [`results/witness-run-1.md`](results/witness-run-1.md).

## Pre-registration deviations

The full record, with dates and reasons, is in [`DEVIATIONS.md`](DEVIATIONS.md). In short:

1. **D1–D3: claims come from the model's visible explanation, not its hidden thinking.** The original spec split the hidden thinking trace. The API's `reasoning_extraction` safeguard refused that design, and then a second design that still had the documented trigger shape. We redesigned rather than route around it, following [Anthropic's documented guidance](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks). The base model now gives an answer with a brief explanation of the considerations for and against. Its summarized thinking is archived but never sent to another call. The extractor reads the explanation as a document and lists its claims. Two findings along the way: Sonnet 5.5 emits **no thinking block at all** at low, medium or high effort on these items, and at `xhigh` the block is only a one- or two-sentence summary.
2. **D4: the pool was extended** with 75 computational items whose answers are computed by code. On the original 60 items the base model made no errors.
3. **D5: the base model was changed** from `claude-sonnet-5-5` at `xhigh` to `claude-haiku-5-5` at default effort. Sonnet answered all 117 checkable items correctly, which left no known-wrong items to test H2, so a weaker Claude model was used to obtain errors. The H2 criterion and the five arms are unchanged. Haiku still got only 4 of 125 standard items wrong, so Stage 2 run 1 is underpowered.
4. **D6: a second, harder pool** of 300 items:
   - 120 from SimpleQA (OpenAI simple-evals, MIT)
   - 120 MMLU-Pro physics and chemistry items (TIGER-Lab, MIT); GPQA Diamond was not used, because it is gated and its authors ask that items not be published in plain text
   - 60 author-written true or fabricated claims

   Every item records its source and license. Haiku got 44 wrong, which gives Stage 2 run 2 a 40-wrong / 40-right test set.
5. **D7–D18, later additions.** All were pre-registered or logged before the data they affect.
   - Arms F and G, bootstrap intervals, and the 200-shuffle null (D7).
   - Witness readout calibration pinned to the measured qubits (D8).
   - The v2 training pool and its one supplement (D9).
   - A QPU-seconds parsing bug, fixed (D10).
   - Experiment 4, with R2 reworded: it rules out only the *static* classical twin (D11).
   - The v2 pre-registration (D12) and experiment 3's implementation choices (D13).
   - The hedge baseline and v2.1 (D14), and v2.1's noisy evaluation (D16).
   - A frame correction (D15): the phase solver's camps drift off the yes/no axis on about 20% of items because the lean anchors are weak. Stronger anchors fix the geometry but leave error detection unchanged.
   - Experiment 4 run 2 in graded form (D17), and the Sonnet replication set-up (D18).

## How to run

```bash
python3.11 -m venv .venv && .venv/bin/pip install -e ".[test]"
cp .env.example .env        # then fill in ANTHROPIC_API_KEY and IBM_QUANTUM_TOKEN
.venv/bin/python experiments/run_pool.py 2      # base model + claim extractor + relation judge over the pool; fixes the split
.venv/bin/python experiments/stage1_pipe.py     # one circuit on the simulators and on real hardware
.venv/bin/python experiments/stage2_run.py      # all five arms; the hardware arm runs only if the gate opens
.venv/bin/python -m pytest -q                   # fast unit tests
.venv/bin/python experiments/reproduce.py       # rebuild every results table from archived JSON (no keys needed) and verify
```

IBM hardware is the scarce resource. The Open Plan gives 10 QPU minutes a month, and this project stops at 7. Every design decision is made on the simulator. Every hardware job is logged with its QPU seconds in [`results/ibm-usage.md`](results/ibm-usage.md), and Anthropic API spend per question is in [`results/api-usage.md`](results/api-usage.md).

## Repository

```
src/entangled_mind/   config (all pre-registered constants), llm, encoder, readout, backends
experiments/          questions, pre-registration, pool / Stage 1 / Stage 2 scripts
results/              one markdown + one JSON per run, usage ledgers
tests/                fast unit tests
paper/                proposal and plain-language companion (PDFs)
```

## License

MIT, see [`LICENSE`](LICENSE). To cite this work, see [`CITATION.cff`](CITATION.cff).

# The Entangled Mind: Quantum Cognition as a Cognitive Architecture for Language Models

**Sean Pharris**, independent researcher

> *Do machines need quantum minds?*

## Abstract

Quantum-cognition models describe human judgment with amplitudes, interference and entanglement rather than classical probabilities. This project asks whether the same idea is useful as an architecture around a language model. For each yes/no question, a language model answers and briefly explains the considerations for and against. Those claims are extracted, and every pair is judged to support, contradict, or be unrelated to the other. The resulting web becomes one entangled quantum state: one qubit per claim, with confidence setting the amplitude and a solved phase setting the stance. RZZ gates link related claims, and a short Ising-style evolution runs before measurement in a "yes"-oriented basis. The readout gives a judgment, a confidence, and a conflict flag for shots that split between strongly opposed configurations. The pre-registered test is whether that flag picks out the model's wrong answers better than three controls: the same circuit with no entanglement, the same circuit with a shuffled relation web, and plain classical contradiction-counting. The last is the control that matters most.

**Status:** Stage 2 runs 1–2 complete on the noisy simulator. **The primary hypothesis H2 failed:** the entangled readout flags the model's wrong answers worse than the non-quantum and unentangled controls. No hardware arm has run (the simulator gate was not met); the Stage 1 hardware job returned real counts after 2 h 50 min in the queue (2 QPU s).

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
- **QPU seconds used so far: 2** of the 600 s monthly allowance (ledger: [`results/ibm-usage.md`](results/ibm-usage.md)).

## What the hardware does and does not show

- **No speedup.** Every belief state here has 5–16 qubits, so it is exactly classically simulable. A laptop computes the same state exactly (arm A0) or under a device noise model (arm A). Running on a quantum processor provides **no computational advantage** at this size.
- **What hardware is for here: demonstration and certification.** It can confirm that a physical device held the entangled state the encoding describes, and that the effect survives real noise.
- **What it cannot show:** that the quantum structure helps the judgment. On the simulator, Stage 2 shows it does not.
- **Planned use of the QPU budget:** an **entanglement witness**. Two-qubit tomography of the most strongly entangled pair of contentions in the belief state of 3 test items, with negativity as the witness, is designed in [`experiments/witness.md`](experiments/witness.md). It is about 45 QPU seconds, and all three items pass on the noisy simulator. It has **not been submitted** and waits for budget approval.

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

## How to run

```bash
python3.11 -m venv .venv && .venv/bin/pip install -e ".[test]"
cp .env.example .env        # then fill in ANTHROPIC_API_KEY and IBM_QUANTUM_TOKEN
.venv/bin/python experiments/run_pool.py 2      # base model + claim extractor + relation judge over the pool; fixes the split
.venv/bin/python experiments/stage1_pipe.py     # one circuit on the simulators and on real hardware
.venv/bin/python experiments/stage2_run.py      # all five arms; the hardware arm runs only if the gate opens
.venv/bin/python -m pytest -q                   # fast unit tests
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

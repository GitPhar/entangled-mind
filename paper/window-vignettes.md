# Window vignettes: three items, stage by stage

*The Entangled Mind*, companion figures for the v2 paper. Written 2026-11-03.

These figures come from the window (`window/index.html`), the project's per-item display of the belief state.

**Data sources**
- **Stage values** are exact, noiseless statevectors rebuilt from the archived claims by `experiments/export_window.py`. They were checked against the full circuit, and against archived arm A0 (mean absolute difference 0.016 over 425 items).
- **Arm scores, thresholds and flags** are the archived results in `results/stage2-run-2.json`.

**Reproducing a panel.** Serve the folder (`python3 -m http.server -d window 8000`) and open `http://localhost:8000/?item=<id>&stage=<k>`, with k = 0 encode, 1 entangle, 2 evolve 1, 3 evolve 2, 4 collapse, 5 readout.

**How the three items were chosen.** All three are run-2 test items the base model (`claude-haiku-5-5`) answered wrongly, so a good error detector should flag all three. They were picked to show the three possible outcomes:
- flagged by the entangled arm but not by the contradiction count;
- flagged by the contradiction count alone;
- flagged by no arm.

They are illustrations, not evidence. The test-set statistics are in the paper, Section 5.3.

**Reading the conflict score.** The score is 2 · min(P(vote ≥ +1/3), P(vote ≤ −1/3)): the probability mass in the weaker of two strongly opposed yes/no camps. Arms flag an item when the score exceeds the 75th percentile of that arm's scores on the calibration pool.

| arm | what it is | threshold |
|---|---|---|
| A | entangled circuit, noisy simulator | 0.266 |
| A0 | entangled circuit, noiseless | 0.279 |
| C | circuit with no entangling gates | 0.011 |
| D | shuffled relation web | 0.152 |
| E | total contradiction strength (different units) | 2.325 |

---

## Figure W1. h046: a conflict the entangling step creates, and the count misses

**Caption.**
- **The item.** h046, a SimpleQA item: "In which month and year was Firozabad district first established from Agra district in India? Is the answer 'February 1989'?" The gold answer is yes; the model answered no.
- **Panel layout.** Each point is one of the 8 claims in the model's explanation. Brightness is amplitude, hue is phase (cyan yes, orange no, grey neither), and dashed links are entanglement, with opacity equal to pair negativity.
- **Panel a, encode** (`?item=h046&stage=0`). Two claims lean yes: claim 0, "carved out of Agra district in 1989", and claim 1, "the year 1989 matches", both at confidence 0.90. Five lean no (claims 2–5 and 7, on the month). One is neutral. The product state votes almost unanimously no: P(strong no) = 0.817, P(strong yes) = 0.001, conflict 0.003.
- **Panel b, entangle** (`stage=1`). After the RZZ gates, amplitudes dim and the pair negativity reaches 0.141. The vote splits into two camps, P(strong yes) 0.241 and P(strong no) 0.324, so the conflict score is 0.482.
- **Panels c–d, evolve 1 and 2.** Conflict settles at 0.291, then 0.281.
- **Readout.**

  | arm | score | flagged? |
  |---|---|---|
  | A | 0.310 | yes |
  | A0 | 0.260 | no (threshold 0.279) |
  | E | 0.5, from 2 weak contradictions | no |
  | C | 0.000 | no |
  | D | 0.066 | no |

**Narrative.** This is the case the original idea was built for. The model's explanation holds a real tension: the year is right, the month is wrong, and the question asks for both. Contradiction-counting cannot see it, because the relation judge marked most links between the year claims and the month claims as *supports*, not contradictions. Only two weak contradictions exist, with total strength 0.5.

Before entangling, the confident month claims outvote the year claims and the state is close to a unanimous "no". The entangling step pulls the year claims and the month claims into two opposed camps. That opposition is exactly what the conflict score measures, and it peaks at 0.48 straight after entangling.

Two cautions keep this from being more than an illustration.
- **The flag is marginal.** The noiseless score (0.260) sits just below its own threshold, so the noisy-simulator flag (0.310) depends partly on noise.
- **The same mechanism misfires elsewhere.** The entangling step manufactures opposed camps on items where the model was right, too (Figure W3 shows it doing so with no contradictions at all). On the 80-item test set it flagged 10 wrong items and 9 right ones.

---

## Figure W2. h135: a contradiction the count sees, and the vote cannot

**Caption.**
- **The item.** h135, an MMLU-Pro chemistry item: a radiocarbon-dating question, "Is the correct answer '6,225 years old'?" The gold answer is yes; the model answered no.
- **The claims.** There are 9. Two lean yes, both weakly: claim 0 at confidence 0.20 and claim 1 at 0.30. Five lean no. Claims 3, 4 and 5 lean no at confidence 0.80–0.85, and each computes a different age: about 6,760, 6,950 and 5,950 years. Two claims are neutral.
- **The relation web.** 29 related pairs, 11 of them contradictions, with total strength 4.4.
  - Of that, 2.3 is between the weak yes-claim 0 and the no-leaning claims.
  - 2.1 is among the no-leaning claims 3–6 themselves: the model's own calculations disagree with each other.
- **Panel b, entangle** (`?item=h135&stage=1`; this panel is `window/screenshot.png`). Pair negativity reaches 0.102, but the vote stays one-sided: P(strong no) 0.790, P(strong yes) 0.024, conflict 0.047.
- **Panels c–d, evolve 1 and 2.** Conflict 0.052, then 0.050.
- **Readout.**

  | arm | score | flagged? |
  |---|---|---|
  | E | 4.4 | **yes** (threshold 2.325) |
  | A | 0.104 | no |
  | A0 | 0.050 | no |
  | C | 0.000 | no |
  | D | 0.078 | no |

**Narrative.** Here the model's explanation shows a mind that does not agree with itself. It works the decay law three ways, gets three ages, and concludes against the proposed answer anyway. The contradiction count registers this directly: almost half its strength comes from claims that disagree with each other *while voting the same way*.

The conflict readout cannot register it, by construction. It measures opposition between a yes camp and a no camp, and here every confident claim is in the no camp. Entangling links the disagreeing calculations, and the negativity shows those links are physically real in the state, but entanglement among claims on the same side does not move probability into the opposite camp.

This is the clearest single picture of why plain counting beat the quantum readout on the test set. The useful signal was inconsistency, and the readout was built to detect opposition.

---

## Figure W3. h013: a confident, consistent error that no arm can see

**Caption.**
- **The item.** h013, an MMLU-Pro chemistry item: "Calculate the magnetic moment (μI) of a ¹³C nucleus. Is the correct answer '9.1445 × 10⁻²⁷ J T⁻¹'?" The gold answer is yes; the model answered no.
- **The claims.** All 9 lean no or are neutral, at confidence 0.80–0.95. The relation web has 25 related pairs, all *supports*; there are no contradictions.
- **Panel a, encode** (`?item=h013&stage=0`). A unanimous product state: P(strong no) 1.000, conflict 0.000.
- **Panel b, entangle.** Pair negativity reaches 0.129. A small yes camp appears from nowhere: P(strong yes) 0.078, conflict 0.155.
- **Panels c–d, evolve 1 and 2.** Conflict 0.171, then 0.202.
- **Readout.**

  | arm | score | flagged? |
  |---|---|---|
  | E | 0.0 | no |
  | A | 0.160 | no |
  | A0 | 0.182 | no |
  | C | 0.002 | no |
  | D | 0.102 | no |

  No arm flags it.

**Narrative.** The model is wrong, sure of itself, and internally consistent. Every claim points the same way, and every relation is a support. No method that reads conflict inside the explanation, quantum or classical, has anything to work with, and none flags the item. This is the blind spot of the whole approach. It is the case the pending comparison with the model's self-reported confidence (arm G) will speak to.

The window also shows something less welcome. With no contradictions anywhere, the entangling step still lifts the conflict score from 0 to 0.20. Mixing amplitudes across a web of supports creates a small yes camp that no claim asked for. Here it stays below threshold. On items the model got right, the same effect is one way the entangled arm produces false flags.

---

## Table W1. Where the signal goes: test-set AUROC of the exact conflict score, read at each stage

**Exploratory, not pre-registered.** These numbers were computed after the Stage 2 results were known, from the exact noiseless states in `window/data/index.json` (`stage_auroc_exploratory`). They are a diagnostic of the design, not a test of any hypothesis.

AUROC is the probability that a randomly chosen wrong item scores higher than a randomly chosen right one; 0.5 is chance. Arm C has no entangling gates, so its "entangle" stage is identical to "encode".

| stage | Run 2: A (entangled) | Run 2: C (no entangling) | Run 1: A | Run 1: C |
|---|---|---|---|---|
| encode | 0.630 | 0.630 | 0.675 | 0.675 |
| entangle | 0.596 | 0.630 | 0.575 | 0.675 |
| evolve 1 | 0.521 | 0.702 | 0.325 | 0.450 |
| evolve 2 (measured) | **0.486** | **0.683** | 0.375 | 0.425 |

Sample sizes and reference points:
- Run 2 is 40 wrong and 40 right items.
- Run 1 is 4 wrong and 10 hard-right items. It is far too small to read, and is shown only for completeness.
- The archived noiseless arm A0 scored 0.49 on run 2, matching the exact value. The archived noisy arm C scored 0.68.

**Reading.** On run 2, the error signal is present before any claim is linked to another: the unentangled product state already gives 0.63.
- Evolution *without* couplings (arm C) sharpens it to 0.68–0.70.
- The entangling gates lower it to 0.60.
- The coupled evolution takes it down to 0.49, which is chance.

The vignettes above show two of the mechanisms behind this.
- The entangling step creates opposed camps where the explanation has none (W3, and on right items generally).
- It cannot turn same-side inconsistency into opposition (W2).

The quantum layer does not merely fail to add information. On this pool it removes information that its own unentangled input already held.

---

## Note W4. Hedges are forced into camps: a candidate mechanism for the signal loss (flagged for version two)

**Exploratory, not pre-registered.** Everything in this note was found by looking at the window and then at the run-2 test set after the Stage 2 results were known. It is a hypothesis for the version-two design, not a finding.

**The observation (h046, claim 6).**
- **The claim.** "The writer relies on memory for the exact day and month, so is not fully certain." Confidence 0.80, lean 0: a *hedge*, a statement of uncertainty that takes no side.
- **The encoding commits it anyway.** Its confidence sets its tilt toward the equator (θ = 0.80 · π/2), so it starts with amplitude 0.951. That treats "confident that I am unsure" as "strongly committed".
- **One weak relation picks its side.** Its only relation is a weak contradiction (J = −0.2) with claim 3, "Firozabad became a separate district on 13 May 1989", which leans no. The phase solver therefore places the hedge opposite claim 3, on the yes side, at 43°.
- **The state keeps pushing it.** Across the stages its probability of a yes outcome goes 0.846 at encode, 0.865 after entangling, 0.966 after evolve 1, and **0.970** after evolve 2, with phase 43° → 39° → 9° → −6°.
- **The result.** In the measured state, the most strongly yes-committed claim is the model's remark about its own uncertain memory, at amplitude 0.945. The two claims that actually argue for yes (claims 0 and 1) have shrunk to amplitude 0.40 and 0.36.

In the window (`?item=h046&stage=0` to `stage=3`), the dotted gold ring marks the hedge, and the point can be watched rotating into the yes camp.

**Why it matters only indirectly.** The readout weights each claim's vote by |lean|, so a hedge has **weight zero** in the vote and cannot add to the conflict score directly. It acts through the dynamics instead. During the RZZ preparation and the Ising-style evolution it is a fully committed spin, coupled to its neighbours like any other claim. The encoding therefore does two things to a hedge, both plausibly harmful:
- **it discards** whatever the hedge says about the model's uncertainty, because the hedge carries no weight in the vote;
- **it distorts** the hedge's neighbours, by coupling them to a confident spin whose side was chosen by the phase solver rather than by the model.

**How common it is (run-2 test set, 40 wrong and 40 right items).**
- Hedges are 97 of the 697 claims, and appear in 52 of the 80 items.
- **The phase solver commits them at encode.** 99% of hedges sit at |2·P(yes) − 1| ≥ 0.5 before any evolution (mean 0.94). Evolution loosens them somewhat (mean 0.67 after evolve 2; 92% still ≥ 0.5). h046's claim 6, which evolution pushes further out, is the vivid case rather than the typical one. The forcing happens mainly in the phase solve.
- **Hedges track errors.** There are 72 hedges in the 40 wrong items against 25 in the 40 right items. 35 of 40 wrong items contain at least one hedge, against 17 of 40 right items.
- **A plain hedge count separates wrong from right items at AUROC 0.78** (hedge fraction: 0.77). That is better than any pre-registered arm on this set (best: C at 0.68). This number was computed on the test set after the fact. It must be treated as a hypothesis until it holds on held-out data.

**Candidate mechanism.** Part of the error signal in the model's explanations lives in its hedges: how often it says, in effect, "I am not sure". The version-one encoding gives hedges zero weight in the vote, turns their confidence into commitment, and lets one weak relation assign them a side. That loses the signal, and may corrupt neighbouring claims. It is consistent with Table W1, where the product state already scores 0.63 and the coupled steps take it down to 0.49. It has not been tested as a cause.

**Flagged for the version-two design (not yet pre-registered).**
1. **A pre-registered hedge baseline.** Add hedge count (or fraction) as a classical arm and test it on the locked v2 split, untouched by this analysis. If it beats the learned quantum encoding (A2), the quantum layer has more to answer for. The current linear baseline L does not include it, although its "mean |lean|" feature overlaps with it.
2. **An honest encoding of hedges.** In A2 *and* its classical twin F2 alike, map a hedge to an uncommitted state (amplitude near 0, or a separate "uncertainty" weight) instead of letting its confidence set its commitment and the phase solver set its side. Compare with the version-one treatment as a pre-registered ablation.
3. **Report it in the window.** The hedge ring stays on through every stage, so any version-two encoding can be checked by eye for the same forcing.

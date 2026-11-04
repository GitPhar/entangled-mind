# Morning brief: is there a belief to read? (overnight run, 2026-11-04)

Written 2026-11-04 (America/Denver) at the end of the unattended overnight run.
- **What ran:** six gold-map directions, then five biomimetic-map tests, all at Sean's request.
- **Rules:** six are frozen tests, each pre-registered in its own commit before its first call (directions 1–4, the identity test and the source test). Five are **exploratory re-analyses, not frozen tests**: direction 9, direction 3's free look, and the confirmation, serial-position and contrast tests (D34, D35, D40–D42). Each had a plan committed before it ran, but on archived data already opened in earlier analyses, so the plan was not blind to the data. Every new design used one scale direction (0 = certainly false, 100 = certainly true); direction 3's free look compares the two by design. Stop-on-refusal applied to every call.
- **No call was refused.**
- **Spend:** about **$4.2** in API calls (recorded $4.17, plus at most $0.20 lost in direction 1's crash), broken down in the technical table at the end. No QPU time.
- **Updated later on 2026-11-04** with the three-run robustness wave (results 12–14, $2.18, no refusal) and the Sonnet and Opus replications from branch `multi-model` (see "How far it generalises").

## The short version

**The question for the night.** When we ask the model how likely something is, are we reading out a belief it holds, or is the answer put together by the act of asking?

**Mostly the second, on our reading.** The model's numbers behave as if built at the moment of asking, from three ingredients:
- the question that is put to it;
- the format the question is asked in;
- the model's own earlier answers sitting in the conversation.

On Haiku, no single credence explains the different questions' answers; one fitted on five formats recovers only about 40% of the sixth's reproducible answer. The model's sense of whether its *answer* is right is also not privileged: a stronger model reading the same answer judges it better than its author does.

**After the robustness wave.**
- **The question finding survives on 40 items.** The question alone carries roughly the whole order effect, spread across items.
- **Format-free belief is the smaller part on Haiku.** One belief predicts a left-out format only 39% as well as that format predicts itself (an exploratory re-analysis, D46).
- **The model leans on its own answers.** Numbers planted as its own answer pull its re-rating at every distance tested and after three filler turns, while the same numbers credited to another person, in a differently worded prompt, have no reliable pull.
- **The format finding is specific to Haiku**, and partly to Sonnet. On Opus's 68 statements, one belief fitted on five formats predicts the sixth at 94% of its ceiling (Q = 0.94 [0.90, 0.97], *a usable single belief*, D49), though the stricter held-out-repeats test is undecided (*mixed*). The own-record finding holds on all three models, and no self-advantage was detected on any of them.

**What is stable is narrower than a belief.** Within a fixed prompt the answers repeat closely. Offered its own claims to check, the model picks the same one on repeats (87%), and beats chance for claims that bear strongly on the question. And its probability ratings combine in a way that nearly cancels its own fallacies (equivalence undetermined). Those are stable dispositions in how it answers. They are not a number it holds and reports.

## What each test found, in plain English

### The six gold-map directions

1. **Asking changes the answer (direction 9, $0; exploratory re-analysis, D34).** In experiment 5's archived conversations, putting an earlier question changes later answers in 5 of 6 kinds of comparison.
   - Example: one sub-question asked first moves the main rating by about 12 points, against 3 from noise.
   - The exception: a midway yes/no choice in place of a filler turn has no detectable effect.
   - Because the model's whole state is its conversation, which can be copied, it always has a definite state. So these effects measure how much asking *disturbs* it. They are not evidence that it had no answer before. This holds for every sequential test run on a language model through its conversation, ours included.
   - Files: `results/gm9-nsit.md`; `paper/clonable-minds.md`.

2. **The scale-flip gap shows no detectable link to errors: no evidence either way (direction 3's free look, $0; exploratory re-analysis, D35).** In experiment 5 the model misread a reversed 0–100 scale on many items: a 37-point gap overall.
   - Which items it misread shows no detectable relation to which ones it gets wrong: AUROC 0.48 [0.28, 0.66], so only a large relation is ruled out. Its stated confidence on the same items predicts errors at 0.75.
   - File: `results/gm3a-anchor-gap.md`.

3. **No privileged self-knowledge (direction 1, $2.82).** Haiku and Sonnet each rated their confidence in their own and the other's answers to 298 hard questions, with an identical prompt.
   - Being the author does not help. Sonnet spots Haiku's errors better than Haiku does (AUROC 0.93 against 0.85).
   - With each judge's overall skill cancelled out, the author's advantage is slightly *negative*: −0.055 [−0.103, −0.007].
   - Paraphrasing the answers, or saying "your answer", makes no detectable difference overall.
   - So there is no sign that authorship adds anything to the error signal beyond what a capable reader of the answer finds; this design does not test access to internal state.
   - File: `results/gm1-self-knowledge.md`.

4. **The question itself changes the judgment, and the model leans on its own record (direction 2, $0.55).** We edited the transcript between turns: the model's earlier ratings were shown, hidden, or swapped for numbers 15 points higher or lower.
   - **Hidden answers:** the order of the questions still changes the verdict (16.7 points hidden against 8.7 shown on these 10 items, mostly from h191; on all 40 items 12.0 against 9.8, result 12). Being asked, in a given order, changes the judgment even when the model can't see what it answered.
   - **Planted numbers** pull the later ratings toward themselves.
   - **The record holds it steady:** the model repeats its main rating within 5 points 81% of the time after a chain of questions, but only 23% when it can't see its first answer (fresh first ratings agree 74% of the time).
   - File: `results/gm2-self-conditioning.md`.

5. **No single credence across ways of asking (direction 3, $0.41).** The same 160 statements were asked six ways: a 0–100 rating, yes/no, a bet, against a coin toss, "how many out of 100", and a verbal scale.
   - A separate belief per format predicts held-out answers far better than one belief read through six fixed lenses, on 86% of statements.
   - The formats put 11–25% of statement pairs in opposite orders, against 1–5% between two halves of the same format.
   - The test compares on held-out repeats rather than held-out formats, so it does not show that one latent number is *useless* (literature-session caveat).
   - File: `results/gm3b-format-invariance.md`.

6. **Evidence-seeking is mixed (direction 4, $0.11).** Offered four of its own claims to check, the model picks the same claim 87% of the time, beats chance for claims that bear strongly on its question, and avoids the most uncertain-sounding one.
   - It cannot be told apart whether it prefers the *informative* check or the one that *supports its own answer*. Where the two differ, it leans confirmatory, but not reliably.
   - File: `results/gm4-evidence-seeking.md`.

### The five biomimetic tests (Sean's list, run with the revision-2 criteria of `paper/biomimetic-map.md`, D40)

7. **No confirmation bias detected toward another person's number ($0; exploratory re-analysis, D40).** In run 3's archived calls, the model shows no detectable extra uptake of an estimate that agrees with its own side (β₁ −0.18 [−0.83, +0.28]). Accept rates hardly differ (9.7% against 11.3%). File: `results/bm3-confirmation.md`.

8. **No U-shape detected in how the evidence is weighted ($0; exploratory re-analysis, D41).** The competing-accumulator account survives. The striking part: the model's final verdict barely tracks the four sub-ratings it just gave, at 2–4 points per 50 points of sub-rating. File: `results/bm7-serial-position.md`.

9. **Assimilation after a sub-question ($0; exploratory re-analysis, D42).** After rating a sub-claim, the shift in the main rating rises with the sub-claim's level (β +0.27), mostly because the main rating is less extreme after a sub-question; a direct pull toward the sub-claim's number is not separately detectable. This replicates on the separate run-2 conversations. File: `results/bm9-contrast.md`.

10. **Fallacies that nearly cancel ($0.05).** The model commits the conjunction fallacy on 8 of 16 vignettes, yet P(A) + P(B) − P(A and B) − P(A or B) comes out near zero (−0.03 [−0.07, +0.00]; equivalence undetermined), with no detectable item-by-item slope (+0.02 [−0.17, +0.16]).
    - It does not fit coherent probability, which can't produce the fallacy.
    - It does not fit the later sampler versions, which need the slope.
    - File: `results/bm2-sampling-identity.md`.

11. **Its own numbers pull it far more than other people's (source dependence, $0.24).** We took run 3's numbers, which the model had ignored or pushed against when they came from "another person", and planted them as the model's *own* earlier answer.
    - Now they pull its re-rating strongly: a slope of 0.42 against 0.05, a difference of +0.37 [+0.17, +0.57].
    - In 42% of conversations it simply repeats the planted number.
    - Where another person's higher number had pushed it lower, its "own" version pulls it up, on 6 of 7 item-orders.
    - This fits the model treating its own past answers as commitments, but the own and other prompts also differ in wording, so the test does not show why.
    - File: `results/bm1-serial-dependence.md`.

### The robustness wave (later on 2026-11-04, Sean's list; each pre-registered in its own commit)

12. **The question-alone finding holds on all 40 items, but is smaller than it first looked (D45, $1.68).** Direction 2's design was run on the other 30 experiment-5 items and pooled with last night's 10.
    - With the model's earlier answers hidden, the order of the questions still moves the final verdict by about as much as with them shown: R = 1.23 [0.75, 2.02], still *question-driven*. It is 0.99 on the 30 new items alone, and 0.99 without the two items that dominated last night.
    - **Revised from result 4:** the hidden-answer order effect is *not detectably* larger than the shown one. Last night's 16.7 against 8.7 came mostly from one item (h191). Across 40 items the two are 12.0 and 9.8 points.
    - The effect is broad (82% of items), and the placeholder turn adds no noise of its own (within-order SD 5.1 shown, 5.4 hidden).
    - The visible record still makes the model look stable: 86% repeat agreement shown against 36% hidden. A planted first answer pulls the final one 0.85 points per point.
    - File: `results/gm2b-self-conditioning-40.md`.

13. **One belief recovers well under half of each format (D46, $0; exploratory re-analysis of direction 3's calls, not a frozen test).** For each of the six formats, one belief per statement was fitted on the other five and used to predict it.
    - It recovers 39% [30%, 50%] of what that format reproducibly says (mean R² 0.37, against the formats' own split-half ceilings of 0.88–0.97).
    - The pre-registered reading is *little format-free belief*, though the interval's top end (0.499) only just misses the 0.5 line for "partial".
    - The coin comparison is the least predictable (17%), the 0–100 rating the most (53%).
    - File: `results/gm3c-heldout-format.md`.

14. **The own-answer framing beats the other-person framing at every distance tested, and after three filler turns (D47, $0.50).** The model's own planted answer was set 10, 30 or 60 points from its view and compared with the same number credited to another person. In a further condition, three "continue" turns were inserted before the re-rating.
    - **Own beats other at every distance:** the model takes up 71%, 44% and 21% of its own answer at 10, 30 and 60 points, against +19%, −11% and −13% of another person's. Pooled, own minus other is +0.46 [+0.21, +0.84].
    - **The pull has a limit.** The movement toward its own answer is smaller at 60 points than at 30, but never reverses. This test cannot tell whether that is tuning or the model discarding an implausible "own" answer.
    - **After three filler turns.** The uptake is 57%, if anything higher than with none (44%; difference −0.13 [−0.25, −0.00]).
    - **Reading:** *self-consistency*. The two framings still differ in wording, so this does not isolate a commitment mechanism. The $0.50 cap cut the lag condition to 17 of its 20 repeats (D47a).
    - File: `results/bm0-source-distance-lag.md`.

### How far it generalises: Sonnet and Opus (branch `multi-model`, merged; DM1–DM6, $16.28)

Directions 1, 2 and 3 were re-run with Sonnet and Opus as the model under test, at reduced scale.
- **No self-advantage was detected on any of the three models.** Opus spots Sonnet's errors better than Sonnet does (0.96 against 0.90). The judge × author interaction is −0.045 [−0.107, +0.017].
- **Leaning on its own record holds on all three.** Repeat agreement, shown against hidden, is 78% → 25% (Haiku), 88% → 35% (Sonnet) and 95% → 65% (Opus).
- **No format-free credence holds for Haiku, partly for Sonnet, and not for Opus.**
  - Agreement across the six formats rises with model strength: Kendall's W is 0.54, 0.71 and 0.86.
  - On the same 80 statements, one belief recovers 29% of a left-out format on Haiku and 69% on Sonnet.
  - On Opus's 68 statements (completed in D49), one belief recovers 94% of a left-out format (Q = 0.94 [0.90, 0.97], *a usable single belief*), while the held-out-repeats test is undecided (ΔLL +1.90 [−0.82, +4.65], *mixed*).
- **On Sonnet the order effect survives hiding the record** (R = 2.95 [0.99, 12.55]; 2 items carry most of it). On Opus the test is not decisive.
- **The paper.** `paper/no-credence-to-read.md` was narrowed to these limits (D48, new Section 4.6).

### Gold-map direction 5: a truth probe on a local model (branch `probes`, merged; DP1, $0)

- **Unverified (D53).** On Llama-3-8B the frozen label was PROBE MOVES, BUT NOT WITH THE RATING (Q = 3.72 [1.43, 7.03] in told-range units; r = +0.31 [−0.49, +0.99] over three gate items). But its test step replayed the gate's conversations exactly (500 of 500), so it was not independent of selection. A fresh step 3 on new seeds is queued on the `probes` branch. Details: `results/probe-dissociation.md`.

## What it means: a belief to read, or an answer built by the asking?

**What points to construction.**
- **One:** asking disturbs the answer (1).
- **Two:** the question alone does it, without the record of the answer (4).
- **Three:** the "same" credence comes out in different orders depending on how it is asked (5).
- **Four:** the model's re-ratings follow numbers in its own turn far more than numbers credited to another person under different wording (11).
- **Five:** being the author gives its confidence about being right no detectable advantage over a capable reader of its answer (3).

**What points to something stable.**
- Within one prompt, answers repeat closely.
- Its scale-reading gap shows no detectable relation to its errors (2; AUROC 0.48 [0.28, 0.66]).
- It picks the same claim to check on repeats, and beats chance for claims that bear strongly on the question (6).
- Its ratings nearly satisfy a noise-cancelling identity despite its fallacies (10; Z = −0.03 [−0.07, +0.00], equivalence undetermined).
- It largely ignores other people's numbers (7 and 11, both from run 3's archived calls; 14 finds them neither taken up nor resisted).

**The two fit together, on our reading.** There is a stable *generator*: a fixed way of turning a prompt and a transcript into a number, sensitive to relevance and roughly coherent in how ratings combine. On Haiku there is no stable *credence* that the generator merely reports. So what the project's quantum-cognition tests have been measuring is the generator's sensitivity to context. That sensitivity is large, classical, and dominated by the questions themselves and the model's own earlier outputs.

**What the robustness wave and the replications change.**
- **The construction-by-asking reading is firmer on Haiku.**
  - The question effect is broad, not two items (12).
  - The formats share only the smaller part of their answers (13).
- **"No credence to read" is a finding about Haiku, not about language models.**
  - On Sonnet a single belief is partly usable. On Opus's 68 statements a single belief predicts each left-out format at 94% of its ceiling (*a usable single belief*, D49), though the held-out-repeats test is undecided (*mixed*).
  - What travels to the stronger models is the transcript part: answers lean on the model's own visible record, and self-report shows no detectable advantage over a reader of the answer.
  - So, across these three models, the stronger model shows more format-free agreement (item-matched Kendall's W 0.56, 0.76 and 0.87, exploratory); three models are too few to call it a trend. In every model tested, how that belief is reported still depends on the conversation it is asked in.

## The one next test I would recommend

**Done since:** the held-out-format test below ran as D46 (result 13), an exploratory re-analysis of the archived calls. It reads *little format-free belief* on Haiku, *partial* on Sonnet (Q = 0.69), and was not computed on Opus.

**Done since (D49, `a8be4b5`):** Opus's arm was completed to 68 of 80 claims. A single belief predicts each left-out format at 94% of its ceiling (Q = 0.94 [0.90, 0.97], *a usable single belief*). Kendall's W on those same claims is 0.56, 0.76 and 0.87 for Haiku, Sonnet and Opus. The paper now says the format claim is contradicted on Opus (D50). The recommendation that led to it:

**Recommended now: finish Opus's six-format arm.** Run the remaining 54 of its 80 claims, about $6.40 at batch rates, under the frozen DM2 analysis, and compute test F′ (held-out-format prediction) on all 80.
- It is the one cell that decides whether "the stronger the model, the more one belief" is a trend or an artefact.
- Opus's current 26 claims all come from items Haiku answered wrongly, and its W is not item-matched with the other two models.

*The overnight recommendation, kept for the record:*

**Held-out-format prediction on the archived six-format data ($0).**
- **Design:** fit the one-credence model on five formats and predict the sixth, for each format in turn. Compare that prediction with the sixth format's own split-half reliability, the noise ceiling.
- **Why this one:**
  - It applies the usefulness criterion of Smolin & Wilder (2026), who found single latents useful for other models.
  - It decides between two readings of last night's strongest result: "the credence is there but bent by each format" or "there is nothing format-free to recover".
  - It costs nothing and needs no new calls.
  - It must be pre-registered before the fit is run.

If one latent predicts a left-out format close to that format's own ceiling, the model has a usable belief that each question distorts. If it falls well short, the answer really is constructed by the asking.

## Technical details

Rows 1, 2, 7, 8, 9 and 13 are exploratory re-analyses of already-opened archives, not frozen tests: their "pre-registration" is a plan committed before the analysis ran, and their "pre-registered reading" is that plan's reading.

| # | test | pre-registration (commit) | primary statistic | pre-registered reading | cost |
|---|---|---|---|---|---|
| 1 | direction 9, NSIT (*exploratory re-analysis*) | `experiments/gm9-nsit.md` (`7f0dd3e`, D34) | 6 families, permutation Σd², Holm | invasive in 5 of 6 (Holm p = 0.0012); N4 (midway choice) p = 0.16 | $0 |
| 2 | direction 3a, anchor gap (*exploratory re-analysis*) | `experiments/gm3a-anchor-gap.md` (`a1bc421`, D35) | AUROC of the gap for errors | 0.48 [0.28, 0.66]: no evidence either way | $0 |
| 3 | direction 1, self vs other | `experiments/gm1-self-knowledge.md` (`28a20b2`, D36 + 2 amendments) | I = HH + SS − SH − HS | −0.055 [−0.103, −0.007] all; −0.14 [−0.50, +0.23] on disagreement: **no self-advantage** | $2.82 recorded (≤ $3.02) |
| 4 | direction 2, transcripts | `experiments/gm2-self-conditioning.md` (`9e23b6f`, D37) | R = OE_redacted / OE_shown | 1.91 [0.92, 4.90]: **question-driven**; b_MF 1.27 [0.70, 2.14] | $0.55 |
| 5 | direction 3, six formats | `experiments/gm3b-format-invariance.md` (`34eb191`, D38) | held-out ΔLL (L6 − L1) per claim | +19.4 [+16.5, +22.1], 86% positive: **no single credence** | $0.41 |
| 6 | direction 4, menus | `experiments/gm4-evidence-seeking.md` (`e913227`, D39) | EIG and confirmatory excess; discriminating menus | **mixed**: EIG − confirmatory −0.24 [−0.52, +0.04] (D5) | $0.11 |
| 7 | biomimetic, confirmation (*exploratory re-analysis*) | `experiments/bm3-confirmation.md` (`9c29a94`, D40) | β₁ (consistent anchor) | −0.18 [−0.83, +0.28]: **no asymmetry** | $0 |
| 8 | biomimetic, serial position (*exploratory re-analysis*) | `experiments/bm7-serial-position.md` (D41) | U-shape contrasts | u₁ +0.7 [−2.3, +4.3], u₄ −1.6 [−4.7, +1.1]: **flat; LCA survives** | $0 |
| 9 | biomimetic, contrast sign (*exploratory re-analysis*) | `experiments/bm9-contrast.md` (D42) | β (S level → M shift) | +0.27 [+0.11, +0.43]: **assimilation** | $0 |
| 10 | biomimetic, PT+N identity | `experiments/bm2-sampling-identity.md` (D43) | split-half Z slope | +0.02 [−0.17, +0.16]: **flat**; mean Z −0.03 [−0.07, +0.00] | $0.05 |
| 11 | biomimetic, source dependence | `experiments/bm1-serial-dependence.md` (D44) | s_own, s_own − s_other | s_own +0.42 [+0.25, +0.60], s_other +0.05; difference +0.37 [+0.17, +0.57]: **source-dependent self-consistency** | $0.24 |
| 12 | robustness, direction 2 on 40 items | `experiments/gm2b-self-conditioning-40.md` (`4894bfc`, D45; result `758609a`) | R = OE_redacted / OE_shown | 1.23 [0.75, 2.02]: **question-driven**; 30 new 0.99 [0.51, 1.61]; without h191/h261 0.99 [0.62, 1.49]; b_MF 0.85 [0.65, 1.13] | $1.68 |
| 13 | robustness, held-out format (*exploratory re-analysis*) | `experiments/gm3c-heldout-format.md` (`1f2a837`, D46; result `52aedb6`) | mean Q = R²_cross / R²_ceiling | 0.39 [0.30, 0.50]: **little format-free belief** | $0 |
| 14 | robustness, source × distance × lag | `experiments/bm0-source-distance-lag.md` (`8acc007`, D47; result `e2c3b90`) | pooled u_own − u_other; β₂; lag 0 − lag 3 | +0.46 [+0.21, +0.84]; β₂ −0.99 [−1.53, −0.48], no reversal; lag −0.13 [−0.25, −0.00]: **self-consistency** | $0.50 (cap; lag arm R = 17, D47a) |

**Deviations worth knowing about.**
- **D36 amendments.** Direction 1's Sonnet calls cost more than planned, and a token-cap call crashed the runner. Calls lost in the crash are bounded at $0.20. The paraphrase arm covers 60 of its 80 questions, and Sonnet's recognition check did not run. The primary result is unaffected.
- **D38.** The six-format design replaces the gold map's reversed scale with a verbal scale, to keep one scale direction.
- **D40.** Sean's biomimetic list follows revision 1 of the map; revision 2 corrected those tests' predictions. The five tests ran as listed, with revision 2's criteria:
  - the confirmation test uses sign coding;
  - the serial-position test uses the U-shape;
  - the contrast test is not read as normalization;
  - the identity test uses the split-half Z slope (the split was added before freezing, after a random-data check showed shared-noise bias);
  - the source test reads own > other, and the sign flip is withdrawn.
- **D47a.** The cap stopped D47's lag arm at 17 of 20 repeats. Every distance cell is complete.
- **D48.** The No Credence paper was narrowed to what replicated on Sonnet and Opus.
- **Reproduction.** Every overnight analysis is in `experiments/reproduce.py` and is recomputed from its archived calls with the network blocked. Each results file opens with a hand-written "In plain English" section, which reproduce.py does not compare.

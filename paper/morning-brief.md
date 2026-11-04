# Morning brief: is there a belief to read? (overnight run, 2026-11-04)

Written 2026-11-04 (America/Denver) at the end of the unattended overnight run.
- **What ran:** six gold-map directions, then five biomimetic-map tests, all at Sean's request.
- **Rules:** each was pre-registered in its own commit before its archive was opened or its first call. Every design used one scale direction (0 = certainly false, 100 = certainly true). Stop-on-refusal applied to every call.
- **No call was refused.**
- **Spend:** about **$4.2** in API calls (recorded $4.17, plus at most $0.20 lost in direction 1's crash), broken down in the technical table at the end. No QPU time.

## The short version

**The question for the night.** When we ask the model how likely something is, are we reading out a belief it holds, or is the answer put together by the act of asking?

**Mostly the second.** The model's numbers are built at the moment of asking, from three ingredients:
- the question that is put to it;
- the format the question is asked in;
- the model's own earlier answers sitting in the conversation.

There is no stored, format-free credence behind them that the different questions all read out. The model's sense of whether its *answer* is right is also not privileged: a stronger model reading the same answer judges it better than its author does.

**What is stable is narrower than a belief.** Within a fixed prompt the answers repeat closely. The model reliably picks out which of its claims bear on a question. And its probability ratings combine in a way that cancels its own fallacies. Those are stable dispositions in how it answers. They are not a number it holds and reports.

## What each test found, in plain English

### The six gold-map directions

1. **Asking changes the answer (direction 9, $0).** In experiment 5's archived conversations, putting an earlier question changes later answers in 5 of 6 kinds of comparison.
   - Example: one sub-question asked first moves the main rating by about 12 points, against 3 from noise.
   - The exception: a midway yes/no choice in place of a filler turn has no detectable effect.
   - Because the model's whole state is its conversation, which can be copied, it always has a definite state. So these effects measure how much asking *disturbs* it. They are not evidence that it had no answer before. This holds for every quantum-cognition test run on a language model, ours included.
   - Files: `results/gm9-nsit.md`; `paper/clonable-minds.md`.

2. **The scale-flip slip is just a slip (direction 3's free look, $0).** In experiment 5 the model misread a reversed 0–100 scale on many items: a 37-point gap overall.
   - Which items it misread tells us nothing about which ones it gets wrong: AUROC 0.48, chance. Its stated confidence on the same items predicts errors at 0.75.
   - File: `results/gm3a-anchor-gap.md`.

3. **No privileged self-knowledge (direction 1, $2.82).** Haiku and Sonnet each rated their confidence in their own and the other's answers to 298 hard questions, with an identical prompt.
   - Being the author does not help. Sonnet spots Haiku's errors better than Haiku does (AUROC 0.93 against 0.85).
   - With each judge's overall skill cancelled out, the author's advantage is slightly *negative*: −0.055 [−0.103, −0.007].
   - Paraphrasing the answers, or saying "your answer", changes nothing.
   - So the model's best error signal is good reading of the answer text, not access to anything inside.
   - File: `results/gm1-self-knowledge.md`.

4. **The question itself changes the judgment, and the model leans on its own record (direction 2, $0.55).** We edited the transcript between turns: the model's earlier ratings were shown, hidden, or swapped for numbers 15 points higher or lower.
   - **Hidden answers:** the order of the questions still changes the verdict, and the order effect gets larger, not smaller: 16.7 points against 8.7. Being asked, in a given order, changes the judgment even when the model can't see what it answered.
   - **Planted numbers** pull the later ratings toward themselves.
   - **Memory, not stability:** the model's famous consistency (repeating its main rating within 5 points 81% of the time) drops to 23% when it can't see its first answer.
   - File: `results/gm2-self-conditioning.md`.

5. **No single credence across ways of asking (direction 3, $0.41).** The same 160 statements were asked six ways: a 0–100 rating, yes/no, a bet, against a coin toss, "how many out of 100", and a verbal scale.
   - A separate belief per format predicts held-out answers far better than one belief read through six fixed lenses, on 86% of statements.
   - The formats put pairs of statements in opposite orders 21–35% of the time, against 4–8% between two halves of the same format.
   - The test compares on held-out repeats rather than held-out formats, so it does not show that one latent number is *useless* (literature-session caveat).
   - File: `results/gm3b-format-invariance.md`.

6. **Evidence-seeking is mixed (direction 4, $0.11).** Offered four of its own claims to check, the model consistently (87%) picks ones that bear strongly on its question, and avoids the most uncertain-sounding one.
   - It cannot be told apart whether it prefers the *informative* check or the one that *supports its own answer*. Where the two differ, it leans confirmatory, but not reliably.
   - File: `results/gm4-evidence-seeking.md`.

### The five biomimetic tests (Sean's list, run with the revision-2 criteria of `paper/biomimetic-map.md`, D40)

7. **No confirmation bias toward another person's number ($0).** In run 3's archived calls, the model takes up an estimate no more when it agrees with its own side. It *accepts* agreeing estimates less often. File: `results/bm3-confirmation.md`.

8. **No U-shape in how the evidence is weighted ($0).** The competing-accumulator account survives. The striking part: the model's final verdict barely tracks the four sub-ratings it just gave, at 2–4 points each. File: `results/bm7-serial-position.md`.

9. **Assimilation to its own last number ($0).** After rating a claim, the model's main rating moves about a quarter of the way toward the number it just gave, beyond what the claim's content implies. This replicates on the separate run-2 conversations. File: `results/bm9-contrast.md`.

10. **Fallacies that cancel ($0.05).** The model commits the conjunction fallacy on 8 of 16 vignettes, yet P(A) + P(B) − P(A and B) − P(A or B) comes out near zero (−0.03), with no item-by-item slope.
    - That is the signature of the original "probability theory plus noise" model.
    - It does not fit coherent probability, which can't produce the fallacy.
    - It does not fit the later sampler versions, which need the slope.
    - File: `results/bm2-sampling-identity.md`.

11. **Its own numbers bind it; other people's don't (source dependence, $0.24).** We took run 3's numbers, which the model had ignored or pushed against when they came from "another person", and planted them as the model's *own* earlier answer.
    - Now they pull its re-rating strongly: a slope of 0.42 against 0.05, a difference of +0.37 [+0.17, +0.57].
    - In 42% of conversations it simply repeats the planted number.
    - Where another person's higher number had pushed it lower, its "own" version pulls it up, on 6 of 7 item-orders.
    - The model treats its own past answers as commitments.
    - File: `results/bm1-serial-dependence.md`.

## What it means: a belief to read, or an answer built by the asking?

**What points to construction.**
- **One:** asking disturbs the answer (1).
- **Two:** the question alone does it, without the record of the answer (4).
- **Three:** the "same" credence comes out in different orders depending on how it is asked (5).
- **Four:** the model pulls each new number toward the last one it gave (4, 9), and binds itself to its own earlier answers far more than to anyone else's (11). Its apparent stability is consistency with its own transcript (4).
- **Five:** its confidence about being right carries nothing that a reader of its answer lacks (3).

**What points to something stable.**
- Within one prompt, answers repeat closely.
- Its scale-reading slips are noise, unrelated to its errors (2).
- It consistently picks the claims that matter to a question (6).
- Its ratings obey a noise-cancelling identity despite its fallacies (10).
- It resists other people's numbers rather than absorbing them (7, 11).

**The two fit together.** There is a stable *generator*: a fixed way of turning a prompt and a transcript into a number, sensitive to relevance and roughly coherent in how ratings combine. There is no stable *credence* that the generator merely reports. So what the project's quantum-cognition tests have been measuring is the generator's sensitivity to context. That sensitivity is large, classical, and dominated by the questions themselves and the model's own earlier outputs.

## The one next test I would recommend

**Held-out-format prediction on the archived six-format data ($0).**
- **Design:** fit the one-credence model on five formats and predict the sixth, for each format in turn. Compare that prediction with the sixth format's own split-half reliability, the noise ceiling.
- **Why this one:**
  - It is the like-for-like comparison with Smolin & Wilder (2026), who found single latents useful for other models.
  - It decides between two readings of last night's strongest result: "the credence is there but bent by each format" or "there is nothing format-free to recover".
  - It costs nothing and needs no new calls.
  - It must be pre-registered before the fit is run.

If one latent predicts a left-out format close to that format's own ceiling, the model has a usable belief that each question distorts. If it falls well short, the answer really is constructed by the asking.

## Technical details

| # | test | pre-registration (commit) | primary statistic | pre-registered reading | cost |
|---|---|---|---|---|---|
| 1 | direction 9, NSIT | `experiments/gm9-nsit.md` (`7f0dd3e`, D34) | 6 families, permutation Σd², Holm | invasive in 5 of 6 (Holm p = 0.0012); N4 (midway choice) p = 0.16 | $0 |
| 2 | direction 3a, anchor gap | `experiments/gm3a-anchor-gap.md` (`a1bc421`, D35) | AUROC of the gap for errors | 0.48 [0.28, 0.66]: no evidence either way | $0 |
| 3 | direction 1, self vs other | `experiments/gm1-self-knowledge.md` (`28a20b2`, D36 + 2 amendments) | I = HH + SS − SH − HS | −0.055 [−0.103, −0.007] all; −0.14 [−0.50, +0.23] on disagreement: **no self-advantage** | $2.82 recorded (≤ $3.02) |
| 4 | direction 2, transcripts | `experiments/gm2-self-conditioning.md` (`9e23b6f`, D37) | R = OE_redacted / OE_shown | 1.91 [0.92, 4.90]: **question-driven**; b_MF 1.27 [0.70, 2.14] | $0.55 |
| 5 | direction 3, six formats | `experiments/gm3b-format-invariance.md` (`34eb191`, D38) | held-out ΔLL (L6 − L1) per claim | +19.4 [+16.5, +22.1], 86% positive: **no single credence** | $0.41 |
| 6 | direction 4, menus | `experiments/gm4-evidence-seeking.md` (`e913227`, D39) | EIG and confirmatory excess; discriminating menus | **mixed**: EIG − confirmatory −0.24 [−0.52, +0.04] (D5) | $0.11 |
| 7 | biomimetic, confirmation | `experiments/bm3-confirmation.md` (`9c29a94`, D40) | β₁ (consistent anchor) | −0.18 [−0.83, +0.28]: **no asymmetry** | $0 |
| 8 | biomimetic, serial position | `experiments/bm7-serial-position.md` (D41) | U-shape contrasts | u₁ +0.7 [−2.3, +4.3], u₄ −1.6 [−4.7, +1.1]: **flat; LCA survives** | $0 |
| 9 | biomimetic, contrast sign | `experiments/bm9-contrast.md` (D42) | β (S level → M shift) | +0.27 [+0.11, +0.43]: **assimilation** | $0 |
| 10 | biomimetic, PT+N identity | `experiments/bm2-sampling-identity.md` (D43) | split-half Z slope | +0.02 [−0.17, +0.16]: **flat**; mean Z −0.03 [−0.07, +0.00] | $0.05 |
| 11 | biomimetic, source dependence | `experiments/bm1-serial-dependence.md` (D44) | s_own, s_own − s_other | s_own +0.42 [+0.25, +0.60], s_other +0.05; difference +0.37 [+0.17, +0.57]: **source-dependent self-consistency** | $0.24 |

**Deviations worth knowing about.**
- **D36 amendments.** Direction 1's Sonnet calls cost more than planned, and a token-cap call crashed the runner. Calls lost in the crash are bounded at $0.20. The paraphrase arm covers 60 of its 80 questions, and Sonnet's recognition check did not run. The primary result is unaffected.
- **D38.** The six-format design replaces the gold map's reversed scale with a verbal scale, to keep one scale direction.
- **D40.** Sean's biomimetic list follows revision 1 of the map; revision 2 corrected those tests' predictions. The five tests ran as listed, with revision 2's criteria:
  - the confirmation test uses sign coding;
  - the serial-position test uses the U-shape;
  - the contrast test is not read as normalization;
  - the identity test uses the split-half Z slope (the split was added before freezing, after a random-data check showed shared-noise bias);
  - the source test reads own > other, and the sign flip is withdrawn.
- **Reproduction.** Every overnight analysis is in `experiments/reproduce.py` and is recomputed from its archived calls with the network blocked. Each results file opens with a hand-written "In plain English" section, which reproduce.py does not compare.

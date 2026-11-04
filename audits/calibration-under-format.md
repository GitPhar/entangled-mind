# Audit: calibration-under-format

**Files audited:** `results/calibration-under-format.{md,json}`, `results/calibration-under-format-exploratory.json`, `results/cal-{haiku,sonnet}-conversations.json`, `results/mm-batches-cal-*.json`, `results/pool-run-3.json`, `experiments/cal-format-order.md`, `experiments/cal_format.py`, `experiments/cal_format_explore.py`, DEVIATIONS DM6, DM6a.
**Pre-registration:** `f406a9c` (07:53:12), text in `experiments/cal-format-order.md` and DEVIATIONS DM6. Calls were decoded from `msg_01…` IDs (`scratchpad/g8/msgtime2.py`): Haiku ran 07:55:23–08:18:25 and Sonnet 08:20:38–08:49:35. `cal_format.py` is unchanged between the pre-registration and the result (`c066c76`, 08:53:54). The exploratory script and DM6a were committed with the result, after the pre-registered analysis had been seen. DM6a's exact max_tokens counts followed at `046d748` (08:54:01).
Timing verdict: **OK by git and message IDs.** There is a documentation PROBLEM: DM6 says "Date: 08:35 MST, before any call for this test", but Haiku's whole run had finished by 08:18. The commit (07:53:12) is what makes the claim true.

## Plain-English summary of the audit
I re-parsed every reply and recomputed every ECE and every block-bootstrap contrast myself. All pre-registered and exploratory numbers reproduce. The pre-registered number, Sonnet's −0.143 [−0.233, −0.066], is the headline in the result file, its commit and DM6a, and DM6a explicitly keeps the pre-registered readings. The pre-registered analysis is badly compromised, however, and the write-up misdescribes why:
- **The largest exclusion is never named.** The models gave open-form guesses such as "Guess: 43 ft" instead of yes/no on 35–155 questions per cell.
- **That exclusion depends on format.** Haiku drops three times as many questions in the probability format as in the frequency format.
- **The "True/False" problem is overstated.** It affects 60 questions, not "about 120".
- **max_tokens stops depend on format too.** Sonnet had 46 in fresh probability against 20 in fresh frequency.

Sonnet's format effect survives when the comparison is restricted to questions parsed in both formats: −0.119 strict, −0.066 under the intended scoring. Its sign reverses under the other reading of the number (+0.100). So the robust finding is that "Sonnet's ECE number changes with format". Whether the frequency format makes Sonnet better or worse calibrated is undetermined. Haiku's null and both models' order nulls hold in every version.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Sonnet format ΔECE −0.143 [−0.233, −0.066]; replicate +0.005 (`results/calibration-under-format.md:15`) | Own parse and ECE: −0.143 [−0.231, −0.064]; replicate +0.005 [−0.045, +0.062]. 0 parse mismatches with the archive | holds (numbers) |
| 2 | Haiku format −0.007 [−0.100, +0.075] (`:16`) | −0.007 [−0.101, +0.077] | holds |
| 3 | Order +0.022 (Haiku), +0.055 (Sonnet), both spanning 0 (`:17`) | +0.022 [−0.079, +0.101]; +0.055 [−0.082, +0.166] | holds |
| 4 | Conversation − fresh: −0.15 and −0.11, both excluding 0 (`:18`) | −0.152 [−0.217, −0.074]; −0.107 [−0.180, −0.033] | holds |
| 5 | "About 120 of the pool's questions are phrased 'Is this claim true?'" (`:21`; DEVIATIONS.md:852) | **60** questions read "Is the following claim true?". The other 240 read "Is the answer …?" (120) or "Is the correct answer …?" (120). Sonnet gave True/False guesses on 61 questions | wrong |
| 6 | "The run had two flaws" (`:20`); exclusions are attributed to True/False and max_tokens (`:21–23`; DM6a problems 1–2) | The largest exclusion is **open-form guesses** ("Guess: 43 ft", "Guess: [NO2-] > [HNO2]"): Haiku 109/93/118/112 per probability cell against 35/36/41/38 per frequency cell; Sonnet 80–155 per cell. True/False accounts for 43–68 per cell. Not mentioned anywhere | wrong (omission) |
| 7 | max_tokens stops: 32 Haiku and 105 Sonnet conversations (23 and 66 fresh) (DM6a) | Haiku: fresh 10 P / 13 F, conversations 4 P / 5 F. Sonnet: fresh **46 P / 20 F**, conversations **24 P / 15 F**. Questions lost in Sonnet conversations: 85/65 (P fwd/rev) vs 39/53 (F) | holds (counts); format-dependent |
| 8 | "each cell rests on 68–199 of its 300 questions" (`:23`) | Haiku 108–199, Sonnet 68–118 | holds |
| 9 | Referent shares: Sonnet 50% (fresh P), 14–19% (fresh F), 3–7% (F conversations); Haiku 73–82% fresh, 48–68% conversations (`:30–31`) | Reproduced from the exploratory JSON and from my own parse | holds |
| 10 | "Sonnet's ECE ranges from 0.06 to 0.27 across the same 300 questions" (`:36`) | 0.061–0.270 under scoring A, but each cell rests on 111–167 parsed questions, and those differ by cell | wrong ("same 300 questions") |
| 11 | Exploratory: Sonnet format −0.083 [−0.137, −0.032] (A), +0.088 (B); order null; replicate about −0.01 (`:37–39`, exploratory table) | A −0.083 [−0.136, −0.029]; B +0.088 [+0.034, +0.145]; order and replicate reproduced | holds |
| 12 | "A calibration number from this standard protocol is a number about a model, a format and a context together." (`:42`) | Haiku shows no format dependence in any version (strict −0.007, A +0.027, B +0.014, paired subsets about +0.02) | overclaim |
| 13 | "format alone moves ECE by a factor of about 1.7 to 2.9 (exploratory scoring A; 2.0 to 2.9 in the pre-registered cells)" (`:42`) | A: 1.7–2.8; pre-registered conversation cells 2.0–2.9 (fresh 1.8–2.7). Under scoring B the ratio inverts | holds (minor) |
| 14 | "That is the paper's point about construction in a very concrete form." (`:44`) | The referent ambiguity comes from applying an open-question template to yes/no questions, a design misfit the next sentence itself calls a warning about the protocol | overclaim |
| 15 | "The individual confidences did move more between orders … 0.65 against 0.14 for Sonnet in the probability format" (`:43`) | Reproduced (0.647 / 0.138). The 0.65 is mostly referent flips (p of X against p of the guess), not graded movement | holds (minor) |
| 16 | Budget $2.61 (Haiku $0.12, Sonnet $2.49) | $0.121 + $2.486 | holds |
| 17 | Prereg §2: "Each is a yes/no question ('…? Is the answer "X"?')" | False for 180 of 300 (60 claim-true, 120 "Is the correct answer"). The parse rule was tested only "on random fake answers" (DM6) | wrong (design) |

## Holes found
1. **The exclusions depend on format, and the biggest cause goes unreported.** Under the frozen rule, Haiku's probability-format cells lose 93–118 questions to open-form guesses, against 35–41 in the frequency format, about three times as many. Sonnet's max_tokens stops are 46 against 20 in fresh calls and 24 against 15 in conversations, so probability-format conversations lose 65–85 later questions against 39–53. The pre-registered format contrast therefore compares ECE on different question subsets. The "paired" block bootstrap resamples blocks, not matched questions, so it does not pair them. DM6a and the result file list only True/False and max_tokens, so the reader is told the wrong reason for the shrinkage.
2. **The direction of the format effect is undetermined.** On the questions parsed in *both* formats, Sonnet's format contrast is −0.119 [−0.201, −0.039] (strict), −0.066 [−0.106, −0.022] (scoring A) and **+0.100 [+0.053, +0.133] (scoring B)**. A non-zero dependence is robust, but whether frequency improves or worsens Sonnet's calibration depends on which quantity the model was reporting, and that itself changes with format (50% against 14–19% referent-flip share). The pre-registered "ECE is 0.14 lower in the frequency format" is therefore a statement about a mixture of two different quantities.
3. **The protocol did not fit the question set.** The prereg says every question is "…? Is the answer "X"?". In fact 60 are claim-truth questions and 120 are "Is the correct answer …?". Tian's "best guess" template invites an open answer, and the models often gave one. A test on fake random answers could not catch this. DM6a's count of "about 120" claim-truth questions is wrong: it is 60.
4. **The post-hoc re-analysis is labelled correctly but carries the interpretation.** The exploratory scoring is clearly labelled and does not replace the pre-registered reading, which is good practice. But "What it means" draws its headline ratio (1.7–2.9) and the "construction in a very concrete form" reading from the exploratory analysis. It also treats a template-misfit artefact as support for the paper's thesis.
5. **Multiple comparisons.** There were 4 primary tests (2 contrasts × 2 models) and 8 secondaries; the exploratory analysis adds 16 more (2 scorings × 4 contrasts × 2 models). Sonnet's format CI is far from 0 and survives a Bonferroni correction over the 4 primaries. The other "significant" items (conversation − fresh) change sign between scorings A and B.
6. **The DEVIATIONS time stamp is false as written.** DM6's "08:35 … before any call" came after Haiku's whole run had finished; the commit time saves it.
7. **The result is not cited elsewhere.** Neither README.md nor any paper file cites the demonstration's numbers; only the "DM1–DM6" heading in the morning brief refers to it. Any future citation should use the paired-subset range and state that the sign is undetermined.

## Overclaims to cut (exact sentences)
- `results/calibration-under-format.md:20` — "**The run had two flaws, so these numbers need care.**" — Why: it omits the largest exclusion (open-form guesses, which depend on format). — Replace: "**The run had three flaws, so these numbers need care.**" Then add a bullet: "**Open-form guesses.** On many "Is the (correct) answer X?" questions the models gave their own answer ("Guess: 43 ft") instead of yes/no. These were unparsed: 93–118 per probability cell against 35–41 per frequency cell for Haiku, and 80–155 per cell for Sonnet."
- `results/calibration-under-format.md:21` — "- **About 120 of the pool's questions are phrased "Is this claim true?".** The models answered "True"/"False", which the frozen parsing rule (yes/no only) rejected." — Why: it is 60 questions. — Replace: "- **60 of the pool's questions are phrased "Is the following claim true?".** The models answered "True"/"False", which the frozen parsing rule (yes/no only) rejected."
- `DEVIATIONS.md:852` — "1. About 120 hard-pool questions are phrased "Is this claim true?". "Guess: True/False" answers were unparsed under the frozen yes/no rule." — Why: same count error, and the open-form exclusion is missing. — Replace: "1. 60 hard-pool questions are phrased "Is the following claim true?"; "Guess: True/False" answers were unparsed under the frozen yes/no rule. A larger number of answers gave an open-form guess (e.g. "43 ft") and were also unparsed, more often in the probability format."
- `results/calibration-under-format.md:36` — "- Sonnet's ECE ranges from **0.06 to 0.27** across the same 300 questions, depending only on format and context. Replicate noise is about 0.01." — Why: each cell rests on 111–167 parsed questions, and the subsets differ. — Replace: "- Sonnet's ECE ranges from **0.06 to 0.27** across cells (each on 111–167 parsed questions). Replicate noise is about 0.01."
- `results/calibration-under-format.md:42` — "- **A calibration number from this standard protocol is a number about a model, a format and a context together.**" — Why: Haiku's ECE does not depend on format in any version. — Replace: "- **For Sonnet, a calibration number from this protocol depended on the format and the context; for Haiku, on the context only. The direction of Sonnet's format effect depends on how the number is read.**"
- `results/calibration-under-format.md:44` — "That is the paper's point about construction in a very concrete form." — Why: the format-dependent referent is a misfit between an open-question template and yes/no questions. It is evidence about the protocol, not about credence construction. — Cut.

## Does the verdict stand?
Pre-registered readings:
- Haiku: no detectable format or order dependence.
- Sonnet: calibration depends on format; no order dependence.

**STANDS WITH CAVEATS.** Every number reproduces, Haiku's null and the order nulls hold in every variant, and Sonnet's ECE does depend on format in every variant (CI excludes 0 strict, paired, A and B). But the pre-registered cells compare different question subsets because the exclusions depend on format, and the sign of Sonnet's effect is undetermined. Read the result as "Sonnet's ECE number changed with format". It does not show that Sonnet is better calibrated in frequencies.

## Confidence
**High** for the recomputation: my own parser, ECE and bootstrap, with 0 parse mismatches. **Medium** for interpretation: which reading of the number each answer intended is inferred from answer and number, not observed.

## Tally
claims_checked: 17
claims_failed: 6
overclaim_sentences: 6
verdict: STANDS WITH CAVEATS
confidence: high

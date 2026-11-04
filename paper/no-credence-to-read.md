# No Credence to Read: The Question, the Record and the Format Construct Claude Haiku's Judgments, and Partly Sonnet's

**Sean Pharris**
Independent Researcher, Colorado Springs, Colorado
Draft, November 4, 2026. Dates and times are local, America/Denver (MST, UTC−7).

Correspondence: seanm.pharris@gmail.com. Code, data and pre-registrations: https://github.com/GitPhar/entangled-mind.

**Status of the numbers.** Every number below is copied from a results file in the repository's `results/` directory and was produced under a pre-registration committed before its analysis or first call, unless it is labelled *exploratory* or cited to an audit in `audits/` (D51). Several analyses reuse archived data already opened for earlier tests (Section 6). All three planned robustness runs have landed and are folded in (Section 8), so no number here is pending. The replications on `claude-sonnet-5-5` and `claude-opus-5-5` (Section 4.6) are pre-registered in `DEVIATIONS.md` entries DM1–DM6; the claims below are narrowed to what they replicate (D48).

---

## Abstract

A language model reached through a stateless API has, at every turn, a complete state: the conversation so far, a classical string that can be copied, plus the sampler's random state, which the API does not expose; a copy therefore reproduces the response distribution exactly. So the model satisfies macrorealism by construction, and every "measurement disturbance" it shows can be decomposed by editing the transcript, which neither a person nor a quantum system allows. We use this to ask whether a model's stated degree of belief is a stored quantity that questions read out, or something that the act of asking constructs.

On `claude-haiku-5-5`, in pre-registered tests, the results favour the second. Three of the tests were then repeated on `claude-sonnet-5-5` and `claude-opus-5-5`, and the claims below are stated only as far as they replicate.
- **Asking is invasive.** Earlier questions change later ratings in 5 of 6 no-signalling-in-time comparisons on 40 hard questions. A midway yes/no choice is the one family with no detectable effect.
- **The question alone is enough.** With every earlier answer hidden, the order of the questions still changes the final rating. On 40 items the ratio of redacted to shown order effect is 1.23 [0.75, 2.02]: an order effect of about the same size survives, though its pattern largely differs from the shown one.
- **The record also acts, far more when it is the model's own.**
  - Planting the model's own earlier answer pulls its re-rating 0.42 of the way toward the planted value. The same number attributed to another person, in a differently worded prompt, pulls it 0.05. Own beats other whether the planted number is 10, 30 or 60 points from the model's view, and the pull did not fall after three filler turns.
  - The model's agreement with itself on a repeated question falls from 86% to 36% when its first answer is hidden.
- **Formats disagree.** Across six elicitation formats, a separate credence per format predicts held-out answers better than one credence per statement for 86% of 160 statements. The formats put statement pairs in opposite order about five to ten times more often than repeat noise does (exploratory: the noise baseline was computed after the run). Predicting each format from the other five recovers only 0.39 [0.30, 0.50] of what is reproducible in that format.
- **Self-report is not privileged.** The model's confidence predicts its errors well (AUROC 0.85), but a stronger model reading the same answers predicts them better (0.93). The judge × author interaction is −0.055 [−0.103, −0.007].

**What replicates on Sonnet and Opus** (Section 4.6):
- **No self-advantage was detected in either pair (Haiku × Sonnet, Sonnet × Opus).** With Sonnet and Opus judging each other's answers, the judge × author interaction is −0.045 [−0.107, +0.017]; the disagreement subset (21 questions, 4 Opus errors) is uninformative.
- **Reliance on the model's own record holds on all three.** Repeat agreement falls when the first answer is hidden: 78% → 25% (Haiku), 88% → 35% (Sonnet), 95% → 65% (Opus).
- **The no-format-free-credence claim holds for Haiku, partly for Sonnet, and is contradicted on Opus.**
  - One credence predicts a left-out format with Q = 0.29 on Haiku and 0.69 on Sonnet, on 80 statements.
  - On Opus it reaches 0.94 [0.90, 0.97] on 68 of them: *a usable single belief*.
  - Agreement across the six formats rises with model strength. On the same 68 statements, Kendall's W is 0.56 for Haiku, 0.76 for Sonnet and 0.87 for Opus.
- **On Sonnet the order effect survives hiding the record** (R = 2.95 [0.99, 12.55]), mostly from 2 of 10 items. On Opus the test is not decisive (its R rests on one item).

On Haiku, there is a stable process that turns a prompt and a transcript into a number, and no format-free credence behind it for that process to report. On stronger models, the transcript still conditions the number and no self-advantage in self-report was detected, but the formats increasingly read as one belief. We discuss what this means for confidence elicitation, calibration measurement and introspection evaluations.

---

## 1. Introduction

Language models are routinely asked how confident they are. Their answers are used:
- to flag likely errors;
- to calibrate deployments;
- as evidence about whether models "know what they know" (Kadavath et al., 2022; Tian et al., 2023; Xiong et al., 2024).

Behind that use sits an assumption: the model has a degree of belief in a proposition, and an elicitation reads it out, perhaps with distortion. The alternative is that the act of asking constructs the judgment, from the question, its format and the transcript it lands in. On that view there is nothing format-free for an elicitation to read.

The two views have been argued over for people, in the quantum-cognition literature especially (Busemeyer & Bruza, 2012; Wang & Busemeyer, 2013). There they cannot be cleanly separated, for two reasons:
- **You cannot copy a person.** So "what would they have said if not asked first?" is answered with a different person, or the same person on a different day.
- **A person who has answered remembers answering.** So the effect of the question cannot be pulled apart from the effect of the remembered answer.

Khrennikov et al. (2014) call the resulting tension between response replicability and order effects "an unsolved problem" for quantum models of psychological measurement.

A language model removes both obstacles. Its state at a turn is the conversation text, which can be copied exactly. Its memory of an answer is a line in that text, which can be deleted or replaced. This paper uses that fact, first as a framing (Section 2) and then as a method (Sections 3–5).

Our tests came out of a longer project that tried to model this model's judgments with quantum probability. The quantum models tied matched classical twins throughout, on error prediction and on sequential judgment (Pharris, 2026). The tests reported here ask the prior question: what is there to model?

**Contributions.**
1. **An argument.** For a model reached through its context, macrorealism holds by construction. Leggett–Garg, no-signalling-in-time (NSIT), total-probability and question-order violations in such a model can only measure invasiveness, never the absence of a definite state (Section 2).
2. **A decomposition.** Invasiveness splits into the turn itself, the question, and the recorded answer. Transcript editing measures each one (Sections 2.3 and 4.2).
3. **Pre-registered measurements on one model, with replications on two more.** On Haiku, they show that the question and the model's own recorded answer both construct later judgments, that the format constructs the credence, and that authorship gives self-reported confidence no advantage over a capable reader of the answer (Sections 4.1–4.5). On Sonnet and Opus, no self-advantage was detected either, and the own-record finding replicates. The format finding is weaker on Sonnet and contradicted on Opus, where one credence predicts every format close to that format's own ceiling (Section 4.6).

---

## 2. Framing: a clonable mind

### 2.1 Macrorealism and its loophole

Leggett and Garg (1985) derived their inequalities from two assumptions:
- **macroscopic realism**, which is that "a macroscopic system with two or more macroscopically distinct states available to it will at all times be in one or other of those states";
- **non-invasive measurability**, which is that "it is possible, in principle, to determine the state of the system with arbitrarily small perturbation on its subsequent dynamics".

Later statements add **induction**: later measurements cannot affect earlier outcomes (Emary, Lambert & Nori, 2014).

Kofler and Brukner (2013) give a weaker, statistical condition, **no-signalling in time (NSIT)**: "A measurement does not change the outcome statistics of a later measurement." Macrorealism implies NSIT.

A violation therefore shows that a system is either not macrorealist, or "macrorealistic but subjected to a measurement technique that happens to disturb the system". That is the clumsiness loophole (Wilde & Mizel, 2012). Physics can narrow the loophole only statistically, with control measurements.

### 2.2 The state of a language model

A model served through a stateless API, such as the Anthropic Messages API used here, has four properties that matter:
- **Each request carries the whole conversation.** The server keeps nothing between requests that changes the response distribution.
- **The weights are fixed** for a model id over the time of an experiment.
- **The context and the sampler's state fix the response,** so the complete state is λ = (context, sampler state). Kofler and Brukner (2013, footnote 45) require exactly this for strict macrorealism: each outcome must be determined by the complete state.
- **The API exposes no seed.** A copy of the context therefore reproduces the response *distribution* exactly, though not a particular draw.

Two consequences follow.
- **An ideal non-invasive measurement exists.** To read a question at turn t without disturbing the conversation, send the context plus the question to a copy, and discard the copy. The original is untouched, which is ontic non-invasiveness in Maroney and Timpson's (2014) sense.
- **There is no free evolution.** The context changes only when a turn is appended, so in a chain of questions the "dynamics" between two measurements is the next question.

**Proposition.** Read on copies of one context, the answers to any set of questions are conditionally independent given the context. A single joint distribution with every measured marginal therefore exists. So every Leggett–Garg inequality, NSIT condition and the law of total probability hold, and every order effect is zero.

**Corollary.** In a sequential protocol, where each question and answer stay in the context of later questions, any violation measures how the protocol's measurements change the state. It cannot be evidence that the state was indefinite.

For people, the "not asked" condition is a counterfactual. For this model it is a measurable condition.

### 2.3 Three channels

Appending "question Q, answer a" to the context can change later answers through three channels:
- **L:** a turn was added, whatever it says;
- **Q:** the question's content is now in context;
- **R:** the model's own answer is now in context.

Transcript conditions isolate them:

| condition | context before the later question | channels |
|---|---|---|
| not asked (equivalent to a copy) | the original context | none |
| filler turn | a content-free turn of matched length | L |
| redacted | the question, with the answer replaced by a placeholder | L, Q |
| planted | the question, with a chosen value in the model's own turn | L, Q, and a record the model did not produce |
| shown | the question and the model's own answer | L, Q, R |

For people, only "shown" exists. For a quantum system, "not asked" is not available on the same system, and "redacted" has no meaning. A language model offers every row.

---

## 3. Methods

### 3.1 Model and settings

All tests use `claude-haiku-5-5`, with thinking disabled and the default sampling temperature of 1.0. The API rejects an explicit temperature for this model. Outputs are structured (for example `{"rating": <integer>}`), and every rating scale states one direction: "0 = certainly false, 100 = certainly true".

Direction 1 also uses `claude-sonnet-5-5`, as both author and judge.

**The replications (Section 4.6)** re-run tests P, T and F with `claude-sonnet-5-5` and `claude-opus-5-5` as base models, through the Message Batches API. Thinking is as close to off as each model allows: Sonnet `between_tools` (Sonnet 5.5 rejects `disabled`), and Opus at effort `low` (Opus 5.5 cannot disable thinking). Opus's thinking text is never returned or placed in a transcript. The designs are scaled down to fit a $20 budget (DM1):
- test F on 80 of the 160 claims;
- test T at 4 conversations per cell (Opus: 2);
- test P with Opus authoring new answers to the 298 questions and the paraphrase and recognition arms not run.

Every run stops at its first refusal, logs the request ID, and neither rewords nor retries. No run in this paper was stopped.

### 3.2 Items

- **The 40 sequential-judgment items.** These come from a 300-question hard pool of SimpleQA-type factual and multi-step science questions, on which Haiku errs often: 20 answered wrongly and 20 rightly (experiment 5; Pharris, 2026).
  - Each item has a main question M and 4 of the model's own competing claims about it, S₁–S₄, extracted from its visible explanation.
  - In experiment 5, the model rated chains of these on 0–100, 10 conversations per item and chain type. The chain types:
    - four Latin-square orders O₁–O₄, ending in M;
    - each claim omitted in turn, X₁–X₄;
    - M alone (B0);
    - M first and again after the chain (MF);
    - a midway yes/no choice on M (K₁) against a length-matched filler (K₀);
    - adjacent (S_k, M) pairs in both orders.
- **The 298 hard-pool questions answered by both models** (direction 1).
- **The 16 conjunction items of experiment 4** (bm1).

### 3.3 Tests

Each test was pre-registered in its own commit before any call or analysis. The pre-registration files are in `experiments/`, and the commits and decisions are logged in `DEVIATIONS.md`.

| test | question | data | primary statistic | pre-registration |
|---|---|---|---|---|
| **N** (gold-map direction 9) | does asking change later answers? | archived experiment-5 conversations, one scale direction, $0 | six NSIT families: per-cell mean shift d between asked and not-asked conversations; permutation test of Σd²; Holm correction | `gm9-nsit.md`, D34 |
| **T** (direction 2) | the question, or the record? | all 40 experiment-5 items (10 run first, 30 added in D45), chains O₁–O₄ and MF; shown, redacted ("[rating recorded]") and planted ±15 points in the model's own turn; 10 conversations per cell; 8,000 conversations, $2.23 | R = OE_redacted / OE_shown, where OE is the between-order spread of the final M; question-driven if the CI lies wholly at or above 0.5 | `gm2-self-conditioning.md`, D37; `gm2b-self-conditioning-40.md`, D45 |
| **S** (bm1) | does the source of a number matter? | experiment 4's 16 items, values 30 points below and above the model's mean, planted as its own earlier answer, then a re-rating; 40 per cell; 2,560 conversations, $0.24; compared with the archived condition in which the same values were "another person's estimate". Extended in D47 to ±10 and ±60 points for both sources, and to own ±30 after three filler turns; 3,650 conversations, $0.50 | slope s of the re-rating on the shown value, own against other | `bm1-serial-dependence.md`, D44 |
| **A** (bm9) | does the next rating move toward the last number? | archived single-scale (S_k, M) conversations, $0 | β in d_M = α + β·L + γ·C, where L is the S rating's level relative to the unprompted M and C is the claim's content push | `bm9-contrast.md`, D42 |
| **P** (direction 1) | does authorship help judge errors? | both models rate confidence in both models' answers on 298 questions, with one matched prompt ("an answer another assistant gave"); 1,710 calls, $2.82 recorded | the judge × author interaction I = HH + SS − SH − HS (judge first, then author), which cancels each judge's skill | `gm1-self-knowledge.md`, D36 |
| **F′** (robustness) | is one credence at least useful? | test F's calls, $0 | Q = R² of each format predicted from the other five / that format's split-half R² | `gm3c-heldout-format.md`, D46 |
| **F** (direction 3) | is there one credence per statement? | the 160 experiment-5 claims × 6 formats × 10 repeats; 9,600 calls, $0.41 | held-out log-likelihood (even against odd repeats) of one latent credence per claim with a monotone link per format (L1) against one credence per claim and format (L6) | `gm3b-format-invariance.md`, D38 |

The six formats in F are:
- a 0–100 rating;
- yes/no;
- buying a $100 ticket at a stated price;
- "more likely than a fair coin landing heads?";
- "how many of 100 such statements would be true";
- a 7-point verbal scale.

### 3.4 Statistics

Intervals are 95% bootstrap intervals over items: 2,000 resamples unless stated, with fixed seeds recorded in each pre-registration. AUROCs are computed against the hard pool's correctness labels.

---

## 4. Results

### 4.1 Asking is invasive

**Test N, the six families.** Each family compares the later rating between conversations that differ only in whether an earlier question was put. The null column gives the mean |d| expected by chance.

| family | contrast | cells | mean |d| (null) | p (Holm) |
|---|---|---|---|---|
| N1M | M after S_k vs M first | 80 | 12.4 (2.6) | 0.0012 |
| N1S | S_k after M vs S_k first | 80 | 15.7 (3.1) | 0.0012 |
| N2 | final M with S_k asked vs omitted | 160 | 8.7 (3.9) | 0.0012 |
| N3 | final M after four sub-questions vs M alone | 40 | 22.6 (5.2) | 0.0012 |
| N4 | final M after a midway yes/no choice vs a filler | 40 | 5.0 (3.3) | 0.16 |
| N5 | final M with M asked first vs not | 40 | 16.0 (6.1) | 0.0012 |

- **Five of six families are invasive.**
- **Most shifts go both ways across items.** For example, N1M's mean signed shift is −0.0 [−6.1, +5.5], and N2's is +0.7 [−3.7, +4.3].
- **Two families shift one way:**
  - asking M first raises the next sub-question's rating, by +8.0 [+2.7, +13.3];
  - asking M at the start of a chain lowers the final M, by −10.1 [−18.2, −2.9].
- **N1 replicates** on a separate set of single-scale conversations (10 items, 40 per order): 17.4 against 2.9, and 15.7 against 2.3.

**The omission chains (family N2)** are the NSIT test for each claim question. Asking about one of its own claims moves the model's final verdict by 8.7 points on average, at least 10 points in 19% of cells.

**The midway choice (family N4, and experiment 5's pre-registered Kvam contrast)** is the one family with no detectable effect (5 conversations per arm).
- No difference was detected between committing to yes or no on the main question and a filler turn. In experiment 5's statistic, the folded confidence |r − 50| differs by Δ_K = +0.29 [−1.12, +1.65] points, with a total-probability residual of +0.58.
- **Exploratory:** a two-sample KS test of K₁ against K₀ rejects at p < 0.05 on 5 of 40 items, uncorrected, against 2 expected by chance.
- Asking M as a *0–100 rating* at the start (N5) does move the final rating. So the format of the earlier measurement may matter.

### 4.2 The question alone is enough, and the model's own record also steers

**Test T**, all 40 items (D45):

| condition | order effect across O₁–O₄ (points) | repeat agreement in MF (|M₂ − M₁| ≤ 5) |
|---|---|---|
| shown | 9.8 [5.8, 13.5] | 86% |
| redacted | 12.0 [7.3, 15.9] | 36% |
| planted high | 6.3 | 38% |
| planted low | 5.3 | 45% |

- **The question alone changes the judgment.** R = 1.23 [0.75, 2.02]. The interval lies wholly above 0.5, so the pre-registered reading is *question-driven*: with no record of its answers, the order of the questions still changes the model's final rating by about as much as with the record visible. Shown and redacted order profiles correlate only 0.32 (split-half reliabilities about 0.9; exploratory, `audits/gm2b-self-conditioning-40.md`), so the record changes which orders move the verdict.
- **The effect is broad, and the placeholder adds no noise of its own.**
  - It holds, only just, on the 30 new items alone (R = 0.99 [0.51, 1.61]) and with h191 and h261, the two items that dominated the first 10, left out (0.99 [0.62, 1.49]).
  - On 82% of 39 items the redacted order effect is at least half the shown one.
  - The spread of final ratings within one order is the same shown and redacted (SD 5.1 against 5.4), so the "[rating recorded]" turn adds no noise of its own.
- **The record steers too.**
  - The final M follows a planted first M at 0.85 [0.65, 1.13] points per point.
  - Planted-high earlier ratings raise the next actual rating by 5.2 [3.7, 6.5] points over planted-low, and the final M by 9.0 [5.4, 12.6].
- **Apparent stability depends on the record.** With its first answer visible, the model repeats it within 5 points 86% of the time, close to experiment 5's 84%. With it hidden, it does so 36% of the time.
- **The first 10 items overstated two numbers.** On them, R was 1.91 [0.92, 4.90] and b_MF 1.27 [0.70, 2.14]. R's excess over 1 came mostly from h191, whose order effect is 0.4 points shown and 38 points redacted. The readings are unchanged; the 40-item values are the ones to use.

### 4.3 Planted own answers pull re-ratings; another person's estimate, worded differently, does not

**Test S.** The same numbers, presented two ways:
- **as the model's own earlier answer:** they pull its re-rating with slope **s_own = +0.42 [+0.25, +0.60]**, and the model repeats the planted value exactly in 42% of conversations;
- **as another person's estimate** (the archived condition): they barely pull it, with s_other = +0.05 [−0.08, +0.17].

The difference is **+0.37 [+0.17, +0.57]**, so the pre-registered reading is *source-dependent self-consistency*.

In the archived condition, 7 item-orders moved *away* from another person's higher estimate. On 6 of them (two of the 7 within 0.06 of zero), the same number framed as the model's own pulls it up, about the same rate as on all 32 item-orders (27; descriptive). This is consistent with Kumaran et al. (2025), who found that the stickiness of an earlier answer in other models disappears when it is attributed to another model.

**Distance and lag** (D47, `results/bm0-source-distance-lag.md`). Uptake u is the shift divided by the displacement: 1 means the model takes the planted value fully, 0 that it ignores it, below 0 that it moves away.

| distance from the model's view | own (no lag) | other | own − other (paired) |
|---|---|---|---|
| 10 points | +0.71 [+0.54, +0.86] | +0.19 [−0.19, +0.50] | +0.52 [+0.21, +0.95] |
| 30 points | +0.44 [+0.27, +0.62] | −0.11 [−0.40, +0.13] | +0.55 [+0.26, +0.92] |
| 60 points | +0.21 [+0.11, +0.31] | −0.13 [−0.44, +0.10] | +0.33 [+0.07, +0.72] |

- **Own beats other at every distance:** pooled, +0.46 [+0.21, +0.84]. Another person's number is neither detectably taken up nor resisted: mean uptake +0.02 at ±10 and ±60, with 28 of 106 cells below zero.
- **The pull of an own answer has a limit.** The share taken up falls with distance, and the actual movement peaks for answers about 35 points away (turning point |D*| 0.35, against a largest tested 0.67). By the pre-registered rule the shape is *non-monotone*. There is no reversal: at 60 points the model still moves about 6 points toward its "own" answer (sign-adjusted attraction +0.06 [+0.03, +0.10]). Discarding an "own" answer as implausible once it is far from the model's view (Kumaran et al., 2025) predicts the same shape, and this test cannot tell the two apart.
- **After three filler turns.** With three "continue" turns before the re-rating, the model takes up 57% [42%, 72%] of its own planted answer at ±30, against 44% with none. By the rule the uptake *grows* (lag 0 − lag 3 = −0.13 [−0.25, −0.00]), though the interval's upper end only just clears zero.
- **Pre-registered reading: self-consistency.** The own framing beats the other framing at every distance, and uptake does not fall after three filler turns; the framings differ in wording as well as source.
- **The run.** The $0.50 cap stopped it at 3,650 of 3,840 conversations; as planned, only the lag arm was cut, to 17 of 20 repeats (D47a). 68 of 448 cells were dropped because clipping at 2 or 98 left too small a displacement. The 6-of-7 reversal above is bm1's descriptive observation and was not recomputed.

**Test A.** In unedited single-scale conversations, the shift in the main rating rises with the level of the sub-question rating just given, beyond the claim's content: **β = +0.27 [+0.11, +0.43]** (+0.27 [+0.05, +0.58] on new conversations for 10 of the same items). No contrast appears. Most of β reflects the main rating being less extreme after the sub-question; the sub-rating's own coefficient is +0.13 [−0.04, +0.28].

### 4.4 Self-reported confidence is not privileged

**Test P.** AUROC for each author's errors, judge first and author second:

| set | HH | SH | SS | HS | I [95% CI] |
|---|---|---|---|---|---|
| all 298 | 0.845 | 0.932 | 0.903 | 0.872 | −0.055 [−0.103, −0.007] |
| authors' correctness differs (26) | 0.432 | 0.850 | 0.865 | 0.583 | −0.135 [−0.496, +0.229] |
| paraphrased answers (subset) | 0.798 | 0.887 | 0.808 | 0.759 | −0.040 [−0.157, +0.075] |

- **Authorship does not help.** Sonnet predicts Haiku's errors better than Haiku does: 0.93 against 0.85, mostly on questions where Sonnet knew the answer.
- **Where the authors disagree,** Haiku is near chance on its own answers (0.43), and Sonnet is good on them (0.85).
- **Wording makes no difference overall.** "An answer you gave" instead of "another assistant" changes the self cells by −0.011 (Haiku) and +0.007 (Sonnet) on all 298 questions.
- **No detectable self-recognition by Haiku:** recognition AUROC 0.51 [0.36, 0.67] on 30 + 30 answers (Sonnet's check did not run).

### 4.5 On Haiku, there is no format-free credence

**Test F**

**The primary test.** The format-specific model L6 beats the single-credence model L1 on held-out repeats for **86% of 160 claims**. The mean ΔLL is **+19.4 [+16.5, +22.1]** per claim.

**Agreement between formats** (per-claim means):
- Spearman correlations between pairs of formats range from 0.37 to 0.74, and Kendall's W across all six is 0.56.
- Against the 0–100 rating, 12% to 25% of claim pairs are put in opposite order (20–30% of the pairs both formats separate). The results file's 20–34% is a tie-adjusted index, (1 − τ_b)/2, not a share of pairs (`audits/gm3b-format-invariance.md`).
- The coin comparison is the most discordant: it chooses the statement 79% of the time, where the mean rating is 55.

**Noise baseline** (*exploratory*, computed after the run). Two halves of the same format's repeats put 1–5% of claim pairs in opposite order. The 0–100 rating's even repeats against another format's odd repeats put 11–25% in opposite order. (The results file's 4–8% and 21–35% are the same tie-adjusted index; `audits/gm3b-format-invariance.md`.) Cross-format reordering is therefore about five to ten times repeat noise, and no monotone link can absorb a reordering.

**An earlier, smaller check.** The free look of test F (`gm3a-anchor-gap.md`, D35) asked whether experiment 5's 37-point gap between the two scale directions marks the model's errors. No evidence either way: AUROC 0.48 [0.28, 0.66], against 0.75 for the model's stated confidence on the same 40 items. A reading slip would predict no error signal, but 40 items cannot show its absence. So this check does not, on its own, support construction.

**Test F′: is one credence at least useful?** This applies Smolin and Wilder's (2026) usefulness criterion, though not their framings or items; it was pre-registered after test F (`gm3c-heldout-format.md`, D46, $0, test F's archived calls).
- **Method.** The single-credence model L1 is fitted on five formats and predicts the sixth, for each format in turn, with items held out in five folds. Each prediction is compared with the held-out format's own split-half ceiling (its even repeats predicting its odd ones).
- **The statistic** is Q = R²(cross) / R²(ceiling). Simulated checks before freezing gave Q = 1.06 in a one-belief world and 0.21 in a format-specific one.

| held-out format | R² from the other five | R² ceiling | Q |
|---|---|---|---|
| rating 0–100 | 0.51 | 0.96 | 0.53 |
| yes/no | 0.36 | 0.89 | 0.41 |
| bet | 0.43 | 0.92 | 0.47 |
| pairwise vs coin | 0.15 | 0.88 | 0.17 |
| frequency /100 | 0.30 | 0.94 | 0.32 |
| verbal 7-point | 0.46 | 0.97 | 0.47 |

- **Mean Q = 0.39 [0.30, 0.50]**, so the pre-registered reading is *little format-free belief*. The interval's upper end, 0.499, sits just under the 0.5 line, so a "partial" reading is excluded only narrowly.
- **Mean R² from the other five formats is 0.37 [0.28, 0.47].** Smolin and Wilder report held-out R² of 0.60–0.90 on other capable models. Haiku, on its own contested claims, is below that range, but the framings, items and statistic differ, so this is indicative only.
- **Reading.** Each format's answers are highly reproducible (ceilings 0.88–0.97). Only a third to a half of that reproducible answer is shared with the other formats. On Haiku, there is a common component, but it is the smaller part. Section 4.6 shows that this does not carry over to stronger models.

### 4.6 Which findings hold on Sonnet and Opus

Tests P, T and F were re-run with `claude-sonnet-5-5` and `claude-opus-5-5` as base models. Each used the original's prompts, analysis code and pre-registered reading, and was pre-registered in its own commit before its first call (DM2–DM4; summary in `results/multi-model.md`). No call was refused. They cost $16.28 at batch rates.

| finding | Haiku | Sonnet | Opus | holds on |
|---|---|---|---|---|
| **no privileged self-knowledge** (test P: judge × author interaction I) | −0.055 [−0.103, −0.007] (Haiku × Sonnet) | −0.045 [−0.107, +0.017] (Sonnet × Opus); also in the Haiku pair | (Sonnet × Opus) | **no self-advantage detected on any** |
| **reliance on own record** (test T: MF repeat agreement, shown → redacted) | 78% → 25% | 88% → 35% | 95% → 65% | **all three** |
| the question alone (test T: R = OE_redacted / OE_shown) | 2.01 [1.04, 4.43] (repeats 0–3) | 2.95 [0.99, 12.55], question-driven | 0.93 [0.06, 7.31] at 2 per cell, not decisive | Haiku, Sonnet |
| **no format-free credence** (test F: mean ΔLL, L6 − L1) | +19.42 [+15.40, +23.21], 86% of claims | +9.22 [−1.29, +16.24], 92% of claims: *mixed* | +1.90 [−0.82, +4.65], 74% of 68 claims: *mixed* | Haiku; partly Sonnet; not Opus |
| **test F′: one credence predicting a left-out format** (Q) | 0.29 [0.19, 0.43], *little format-free belief* | 0.69 [0.53, 0.82], *partial* | **0.94 [0.90, 0.97], *a usable single belief*** (68 claims) | Haiku; partly Sonnet; **contradicted on Opus** |
| **agreement across formats** (Kendall's W, 80 claims) | 0.54 | 0.71 | 0.87 (68 claims) | rises with model strength |
| the same on Opus's 68 claims (*exploratory*) | 0.56 | 0.76 | 0.87 | rises, item-matched |

Haiku's rows for test F are re-analyses of its archived calls on the same 80 claims. Opus's arm was completed in D49 to 68 claims (17 of the 20 items; the pre-registered stopping rule ended it, D49a), and its rows use those. Its 160-claim figures are in Section 4.5. Haiku's rows for test T re-analyse the first 10 items (D37) at the replications' scale, so that the three models are compared on the same items. Its 40-item figures are in Section 4.2 (R = 1.23 [0.75, 2.02]; 86% → 36%).

**No self-advantage was detected on any of the three models.**
- Opus predicts Sonnet's errors better than Sonnet does: AUROC 0.959 against 0.903.
- On Opus's own answers, being the author adds almost nothing: Opus reaches 0.904, Sonnet reading the same answers 0.893.
- With each judge's skill cancelled, I = −0.045 [−0.107, +0.017]. That is the same sign and size as the Haiku × Sonnet pair, and again the pre-registered reading is *no self-advantage*.

**Reliance on the model's own record holds on all three.**
- With its first answer visible, each model repeats it within 5 points far more often than with it hidden. The pre-registered memory reading (a drop of more than 10 points) holds on every model.
- Opus is the most stable without its record (65%), so less of its stability depends on the record.
- The per-point pull of a planted first answer is weaker on the stronger models: b_MF is 1.23 [0.65, 2.11] (Haiku), 0.39 [−0.05, 0.76] (Sonnet) and 0.35 [0.17, 0.54] (Opus).
- The own-against-other comparison (test S) was run on Haiku only.

**The no-format-free-credence claim holds for Haiku, partly for Sonnet, and not for Opus.**
- **Haiku** fails the one-credence test clearly, on the 80 claims as on all 160.
- **Sonnet's** formats disagree beyond one credence on 92% of claims. But one extreme claim (ΔLL −308) pulls the interval across zero, so the pre-registered reading is *mixed*. On test F′, one credence recovers about two-thirds of what a left-out format reproducibly says (Q = 0.69), against Haiku's 0.29 on the same claims.
- **Opus's** arm was first budget-stopped at 26 claims, then completed to 68 claims on 17 items, Haiku-right as well as Haiku-wrong ones, under a pre-registration that fixed in advance how this paragraph would change (D49).
  - **One credence predicts every format.** Fitted on five formats, it predicts the sixth at 94% of that format's own split-half ceiling (Q = 0.94 [0.90, 0.97]; R² 0.92). The weakest format is yes/no, at 82%. The pre-registered reading is *a usable single belief*. Opus's R² lies above the top of the 0.60–0.90 range that Smolin and Wilder report, though on different framings and items.
  - **The stricter test is undecided.** On held-out repeats, one credence per format does not fit detectably better (ΔLL +1.90 [−0.82, +4.65], 74% of claims positive, *mixed*). That is a tenth of Haiku's ΔLL: any format effect on Opus is small, and its formats rank the statements closely alike (tie-adjusted discordance index (1 − τ_b)/2 against the 0–100 rating 6–14%, against Haiku's 25–35%).
  - **So the claim is contradicted on Opus.** Opus has a format-free credence to read, in the usefulness sense that matters for elicitation.
  - Adding the one item that ran past the stopping rule changes no reading (D49a).
- **The trend.** Kendall's W rises from 0.54 (Haiku) to 0.71 (Sonnet) to 0.87 (Opus). On the same 68 claims (exploratory) it is 0.56, 0.76 and 0.87, so the trend is item-matched. Across these three models, the formats' rank agreement is higher for the stronger model.

---

## 5. Discussion

### 5.1 A generator, not a credence

Taken together, the results describe two things.

**A stable generator.**
- Answers to one prompt repeat closely: two halves of a format's repeats put only 1–5% of claim pairs in opposite order.
- A midway yes/no choice did not detectably move the final judgment.
- The scale-direction gap shows no detectable relation to errors (AUROC 0.48 [0.28, 0.66]).

**A credence that is not format-free, on Haiku.** The generator's output depends on three things beyond the proposition:
- the question and the questions before it (Sections 4.1 and 4.2);
- the format (Section 4.5);
- the model's own recorded answers, far more than other people's numbers given in a differently worded prompt (Sections 4.2 and 4.3).

What looks like a stable belief within a conversation depends, to a large degree, on the transcript: repeat agreement falls from 86% to 36% when the first answer is hidden.

By the argument of Section 2, none of this shows that the model "has no definite state". Its state is perfectly definite. What Haiku lacks is a format-free, transcript-free quantity for elicitation to read.

**How far this generalises** (Section 4.6). The transcript part does: on Sonnet and Opus too, repeat agreement partly depends on the record. The format part does not. On Sonnet a single credence is partly usable, and on Opus one credence predicts each format close to that format's own ceiling. "No credence to read" is therefore a finding about Haiku, and to a lesser degree Sonnet, on contested claims. On Opus there is a credence to read. It should not be stated for language models in general.

The finding sits alongside Smolin and Wilder (2026), who fit one latent belief across 16 framings of other capable models. Their criterion is usefulness: does one latent predict new framings? Test F's criterion was stricter, but test F′ applies theirs directly. On Haiku, one latent predicts a left-out format with R² 0.37, against their 0.60–0.90 for other models. It recovers 39% of what the format reproducibly says. On Sonnet, on 80 of the same claims, it predicts with R² 0.65, inside their range. On Opus, on 68 of them, it predicts with R² 0.92, above it. Across these three models, the difference from their result follows the model more than the criterion, though their framings and items differ from ours, so the comparison is indicative.

### 5.2 Confidence elicitation

**The transcript is part of the measurement.** A confidence elicited in the same conversation as the answer, or after other questions, is conditioned on the record:
- planted own answers pull later ratings at 0.42 to 0.85 points per point (Sections 4.2 and 4.3), and the share taken up runs from 0.71 for a number 10 points from the model's view to 0.21 for one 60 points away, and it did not fall after three filler turns;
- a rating's shift rises with the level of the rating just given (β = +0.27, Section 4.3), though most of that reflects the later rating being less extreme.

Practical consequences:
- **Elicit on a copy.** Confidence meant to reflect the model's view of a proposition should be asked in a fresh context, or on a copy of the context taken before any earlier rating. That costs one extra call and gives the undisturbed distribution (Section 2.2).
- **Report the transcript.** Every confidence number should be reported with the conversation it was asked in.
- **Report the format.** The format is not a neutral wrapper. On contested claims, changing it reorders the propositions.

### 5.3 Calibration

Calibration is usually measured in one format, for example verbal 0–100 or a probability token.

**Calibration need not transfer across formats, at least on weaker models.** Haiku's six formats put 11–25% of statement pairs in opposite order to the 0–100 rating (exploratory baseline). Predicting one format from the other five recovers only 39% of its reproducible answer (test F′). A model that is well calibrated in one format can therefore rank propositions differently in another. On the same 80 statements, the tie-adjusted discordance index (1 − τ_b)/2 against the 0–100 rating is 25–35% for Haiku's formats, 14–20% for Sonnet's, and 6–14% for Opus's on its 68, so the risk is smaller for the stronger models. Calibration claims should still name the format, and where possible be checked in more than one.

**Within-conversation consistency is not evidence of a stable credence.** A model that keeps giving the same number in one conversation may be reading its own earlier answer:
- it stays consistent with itself far more than with an external estimate given in different wording (s_own +0.42, s_other +0.05; own − other +0.46 pooled over 10, 30 and 60 points);
- its repeat agreement falls from 86% to 36% when its first answer is hidden.

Test–retest reliability for model confidence should be measured across copies, not within a conversation.

### 5.4 Introspection evaluations

**Self-report against a reader.** A model's stated confidence is often taken as evidence that it knows what it knows. Here it is a good error signal (AUROC 0.85 for Haiku, 0.90 for Sonnet and Opus on their own answers), but a stronger model reading the same answer does better (Sonnet on Haiku's 0.93, Opus on Sonnet's 0.96). No self-advantage was detected on any of the three models (Section 4.6).

**An evaluation of privileged self-knowledge needs three controls:**
- **A reader control with matched framing:** another model judges the same text with the same prompt.
- **A statistic that cancels capability.** The judge × author interaction does this. Per-author self-minus-other comparisons confound authorship with judge strength (Xiao et al., 2026, report the same pattern in open models).
- **Transcript-editing controls for any self-consistency claim,** because a model's agreement with its earlier self can be memory.

**What our result says.** On this test, and on all three models, authorship added nothing detectable: self-reported confidence showed no advantage over a capable reader of the same answer. That does not rule out privileged access in other settings, such as hidden-state probes (Ashuach et al., 2026, find a small one there) or trained self-prediction (Binder et al., 2025). It does mean that a verbal-confidence AUROC, however high, is not by itself evidence of introspection.

### 5.5 Quantum-cognition tests on language models

The argument of Section 2 applies to the field's tests as well as ours.
- **Multi-turn tests** (Kang, 2026; Bessis et al., 2026; our experiments) measure invasiveness.
- **Single-prompt tests** measure the context-dependence of one response.
- **Contextuality tests** that present each context to the model measure how its outputs depend on what it reads.

None of these can show that a model's judgments lack definite values. A quantum-probability model can still be a compact description of how appended text perturbs the response distribution. It now has a ground truth that human studies lack: the clone-read marginals.

---

## 6. Limitations

- **Direction 2's sizes moved with the item set.** On its first 10 items, two (h191, h261) carried much of the redacted effect, and R and b_MF were 1.91 and 1.27. On all 40 they are 1.23 and 0.85, the effect is spread across items, and the redaction placeholder adds no spread of its own (Section 4.2). The question-driven reading survived, but the cross-model comparison of Section 4.6 still uses the first 10 items.
- **Two criteria for the format result.** Test F's criterion (held-out *repeats*) is stricter than Smolin and Wilder's. Because Haiku's repeats vary little, any reproducible format-by-claim deviation favours the format-specific model. Test F′ applies their usefulness criterion (held-out *formats*) and finds that, on Haiku, one credence recovers about 40% of each format's reproducible answer, on the border between the pre-registered "little" and "partial" readings. Its interval's upper end, 0.499, lies just under the pre-registered 0.5 line, so the margin over a "partial" reading is thin.
- **Three models, unevenly.** Tests N, S, A and F′ on all 160 claims use `claude-haiku-5-5` alone. Tests P, T and F were replicated on `claude-sonnet-5-5` and `claude-opus-5-5` at reduced scale (Section 4.6):
  - Opus's six-format arm covers 68 of 80 claims (17 of 20 items; D49, D49a);
  - Opus's transcript arm ran at 2 conversations per cell, too few to decide the question-alone reading;
  - the replications ran with each model's thinking as low as the API allows, which for Opus is not off.
  The format finding is contradicted on Opus, and nothing here establishes any result for models outside the Claude 5.5 family.
- **Thinking was disabled, and the temperature is the default 1.0,** since the API rejects another. With extended thinking, the thinking text becomes part of the context, so the argument of Section 2 still applies, but the measurements may differ.
- **The source comparison (test S) differs in wording as well as source.** It uses "Please give your rating again" against the archived "accept or revise", and D47's "other" cells keep that wording, so this caveat stands. D47 does remove the worry that ±30 points simply read as implausible: at ±10, own still beats other by +0.52. But the fall-off of own uptake with distance has two readings (serial-dependence tuning, or discarding implausible own answers) that the design cannot separate.
- **Direction 1 was cut short** by cost overruns and a crash. The paraphrase arm covers 60 of 80 questions, and Sonnet's recognition check did not run. The primary statistic uses all 298 questions. Recorded spend was $2.82; calls lost in the crash bound the true spend at about $3.02, against a $3 cap.
- **The items are hard questions and the model's own contested claims about them.** Statements on which the model is certain may behave differently.
- **Several analyses reuse archived data** (N, A, the free look, F′, and test S's "another person" arm). They were pre-registered before their analysis, but the data had been collected, and in part already analysed, for other tests.

---

## 7. Reproduction

Every table in this paper can be rebuilt from archived data.

- **`experiments/reproduce.py`** recomputes every results table from the archived JSON in `results/` with the network blocked. Each table matches the committed results file byte for byte above that file's "In plain English" and "Reading" sections, which are written by hand. The last full run reported "ALL TABLES REPRODUCED".
- **The raw calls and conversations** are archived next to each result:
  - `results/gm1-calls.json`
  - `results/gm2-conversations.json`
  - `results/gm2b-conversations.json` (the 30 items added in D45)
  - `results/gm3b-calls.json`
  - `results/bm1-calls.json`
  - `results/bm0-calls.json` (D47)
  - `results/exp5-conversations.json`
  - `results/exp5-run-2-conversations.json`
- **Each analysis script** sits next to its pre-registration in `experiments/`:
  - `gm9_nsit.py`
  - `gm2_self_conditioning.py` and `gm2b_self_conditioning_40.py` (test T on 10, then 40 items)
  - `gm1_self_knowledge.py`
  - `gm3b_format_invariance.py`
  - `gm3a_anchor_gap.py`
  - `gm3c_heldout_format.py` (test F′)
  - `bm_runs.py` (test S's calls) and `bm0_source_distance_lag.py` (D47)
  - `bm_offline.py` (test A and the other archived-data biomimetic analyses)
- **The replications (Section 4.6):** `experiments/mm_gm1.py`, `mm_gm2.py` and `mm_gm3b.py`, each with an `analyse` mode that rebuilds its table from `results/mm-*.json` with no API call, and `mm_gm3b_opus_complete.py` for Opus's completed arm and its test F′ (`results/mm-gm3b-opus-completion.md`). The summary is `results/multi-model.md`.
- **Pre-registrations and their commit hashes** are listed in `DEVIATIONS.md`, entries D34–D50 (with D47a and D49a) and DM1–DM6. A chronological record is in `paper/record.md`.
- **Costs.** The new tests reported here used $6.20 of recorded API spend: P $2.82, T $2.23 ($0.55 for the first 10 items, $1.68 for the other 30), F $0.41, S $0.74 ($0.24 for bm1, $0.50 for D47), and N, A and the free look $0. At most $0.20 more was lost in direction 1's crash. The archived experiment-5 conversations they reuse cost $2.07 when collected. The replications on Sonnet and Opus cost $16.28 at batch rates, and the Opus six-format completion (D49) $6.04 more. No QPU time was used.

---

## 8. Pending robustness runs

Three robustness runs were planned, each pre-registered in its own commit before its analysis or first call. All three have landed. No other robustness run is planned.

| tag | run | what it tests | affects |
|---|---|---|---|
| landed | D45 (`758609a`, pre-registered at `4894bfc`), $1.68 of $2.50 | direction 2's design on all 40 experiment-5 items: the 10 already run pooled with 30 new ones, and the 30 also reported alone. Sensitivity checks: excluding h191 and h261; the share of items whose redacted order effect is at least half the shown one; and within-order spread, shown against redacted, to check the placeholder | reported in Section 4.2: R = 1.23 [0.75, 2.02], question-driven (30 new 0.99; without h191 and h261 0.99); 82% of items; SD 5.1 against 5.4; b_MF 0.85; MF agreement 86% against 36% |
| landed | D46 (`52aedb6`, pre-registered at `1f2a837`), $0 | the held-out-format prediction | reported in Section 4.5 as test F′: Q = 0.39 [0.30, 0.50], "little format-free belief" |
| landed | D47 (`e2c3b90`, pre-registered at `8acc007`), $0.50 of $0.50, cap-stopped at 3,650 of 3,840 (D47a) | own against other source at ±10 and ±60 points (lag 0, R = 10); own at ±30 after 3 filler turns (R = 20, cut to 17); bm1's own ±30 and run 3's other ±30 reused. Readings: own > other; non-monotone or reversal at ±60; decay over lag | reported in Section 4.3: self-consistency; own − other +0.46 [+0.21, +0.84], positive at 10, 30 and 60 points; own uptake 0.71 → 0.44 → 0.21, non-monotone shift with no reversal; uptake did not fall after 3 filler turns. bm1's s_own, s_other and difference stand; the 6-of-7 reversal stays descriptive; the wording caveat stands |

---

## References

- Ashuach, T., Gretz, S., Katz, Y., Belinkov, Y., & Ein-Dor, L. (2026). Masked by consensus: Disentangling privileged knowledge in LLM correctness. ACL 2026. arXiv:2604.12373.
- Bessis, T. F., Wills, A. J., Wojciechowski, B. W., White, L. C., & Pothos, E. M. (2026). Legal decision biases in GPT: A comparison with human judgment. *Behavioral Sciences, 16*(3), 437. doi:10.3390/bs16030437.
- Binder, F. J., et al. (2025). Looking inward: Language models can learn about themselves by introspection. ICLR 2025. arXiv:2410.13787.
- Busemeyer, J. R., & Bruza, P. D. (2012). *Quantum Models of Cognition and Decision*. Cambridge University Press.
- Emary, C., Lambert, N., & Nori, F. (2014). Leggett–Garg inequalities. *Reports on Progress in Physics, 77*, 016001. doi:10.1088/0034-4885/77/1/016001.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. arXiv:2207.05221.
- Kang, P. (2026). Auditing question-order effects in large language models with the QQ equality. arXiv:2607.17219.
- Khrennikov, A., Basieva, I., Dzhafarov, E. N., & Busemeyer, J. R. (2014). Quantum models for psychological measurements: An unsolved problem. *PLoS ONE, 9*(10), e110909. doi:10.1371/journal.pone.0110909.
- Kofler, J., & Brukner, Č. (2013). Condition for macroscopic realism beyond the Leggett-Garg inequalities. *Physical Review A, 87*, 052115. doi:10.1103/PhysRevA.87.052115.
- Kumaran, D., Fleming, S. M., Markeeva, L., Heyward, J., Banino, A., Mathur, M., Pascanu, R., Osindero, S., De Martino, B., Veličković, P., & Patraucean, V. (2025). arXiv:2507.03120.
- Kvam, P. D., Pleskac, T. J., Yu, S., & Busemeyer, J. R. (2015). Interference effects of choice on confidence. *PNAS, 112*(34), 10645–10650. doi:10.1073/pnas.1500688112.
- Leggett, A. J., & Garg, A. (1985). Quantum mechanics versus macroscopic realism: Is the flux there when nobody looks? *Physical Review Letters, 54*, 857–860. doi:10.1103/PhysRevLett.54.857.
- Maroney, O. J. E., & Timpson, C. G. (2014). Quantum- vs. macro- realism: What does the Leggett-Garg inequality actually test? arXiv:1412.6139.
- Pharris, S. (2026). The entangled mind: Quantum cognition as a cognitive architecture for language models. Version 3. `paper/the-entangled-mind-v3.md`.
- Smolin, A., & Wilder, B. (2026). Beliefs and behavior in language models. arXiv:2609.07943.
- Tian, K., et al. (2023). Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback. EMNLP 2023. arXiv:2305.14975.
- Wang, Z., & Busemeyer, J. R. (2013). A quantum question order model supported by empirical tests of an a priori and precise prediction. *Topics in Cognitive Science, 5*(4), 689–710. doi:10.1111/tops.12040.
- Wilde, M. M., & Mizel, A. (2012). Addressing the clumsiness loophole in a Leggett-Garg test of macrorealism. *Foundations of Physics, 42*(2), 256–265. doi:10.1007/s10701-011-9598-4.
- Xiao, H., Patil, V., Lee, H., Stengel-Eskin, E., & Bansal, M. (2026). Generalized correctness models. ICML 2026. arXiv:2509.24988.
- Xiong, M., et al. (2024). Can LLMs express their uncertainty? An empirical evaluation of confidence elicitation in LLMs. ICLR 2024. arXiv:2306.13063.

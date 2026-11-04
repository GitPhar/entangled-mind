# Audit: synthesis-claims

**Files audited:**
- `README.md` (Status bullets lines 11–17; "Overnight, 2026-11-04" lines 19–34; "What those works test, and what this project adds" lines 185–189; "So far the answer is negative" lines 191–197).
- `paper/morning-brief.md` (whole).
- `paper/no-credence-to-read.md` (title, status note, abstract, introduction, §4.6 summary table, §5.1, §6).
- `paper/clonable-minds.md` (§§1, 3, 5, 6, 9).
- `paper/the-entangled-mind-paper.md` (abstract, introduction, §§3.3, 4.1, 5).
- `paper/the-entangled-mind-v3.md` (abstract; §§6.1, 6.4, 7, 8, 9).

Every aggregate claim was traced to the results files it rests on, and each was checked against those files' own tables: `stage2-run-2b`, `v2-run-1`, `v2.1-run-1`, `sonnet-replication`, `sonnet-ablation`, `exp3-run-1`, `exp4-run-1/2/3`, `exp5-run-1/2`, `witness-run-1`, `gm9`, `gm3a`, `gm1`, `gm2`, `gm2b`, `gm3b`, `gm3c`, `gm4`, `bm0`, `bm1`, `bm2`, `bm3`, `bm7`, `bm9`, `multi-model`, `api-usage`.
**Pre-registration:** not applicable (synthesis layer). Where a synthesis claim says "pre-registered before its data", it was checked against git and the decoded first calls (see `audits/record-accuracy.md`). First call: see that file.
Timing verdict: PROBLEM for the "pre-registered before its data" wording in the papers. Five of the eleven overnight tests are archival, and four earlier additions were committed after their first calls.

## Plain-English summary of the audit
**The negative quantum result holds.** Every primary pre-registered quantum-versus-classical comparison tied or lost. Each of the three secondary quantum edges is matched by a classical model with the same per-claim readout. Self-report matches the best structural model on both base models.

**Where the summaries go wrong.**
- **Headlines say more than the results.** "No quantum advantage: every pre-registered test failed or tied" counts experiments 3 and 4 (inconclusive or untestable) as failures. It also ignores two pre-registered secondary edges that the next bullet itself admits.
- **README's overnight section is stale.** It was last edited at 05:41. It still quotes R = 1.91 (superseded by 1.23) and "six separate credences" (narrowed by D46 and by Opus). It never says the construction findings are Haiku-only.
- **Mechanism words outrun behavioural contrasts.** "Self-knowledge is text-reading", "binds itself", "treats its own past answers as commitments", "a noise-cancelling identity", "just a slip".
- **The own-versus-other contrast is confounded with wording** ("give your rating again" against "accept or revise"). The headline sentences leave this out.

**Several syntheses count the same data twice.**
- bm3 and bm1's "other" arm are the same run-3 calls.
- bm0 reuses bm1's and run 3's ±30 cells.
- gm2b contains gm2.
- bm9 and direction 9's N1 families share the QQ block.
- D46 reanalyses D38's calls.
- The "holds on all three models" self-knowledge row reuses D36's Sonnet self-judgement cell.

**What the overnight evidence rests on.** About five independent data collections, all from one model and two item sets.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | rests on → evidence | status |
|---|---|---|---|
| 1 | "**No quantum advantage.** Every pre-registered test of a quantum advantage failed or tied: ... and the order-effect tests (experiments 3 and 4)" (README.md:12) | H2 fail (0.55 vs C 0.68); v2 0.83 vs 0.84; v2.1 0.84 vs 0.82; exp 5 tie (+67.0 [−34.1, +211.5]) ✓. But exp 3 is *inconclusive* (CI [−0.284, +0.060], model near-deterministic), exp 4 run 1 and run 3 are *untestable*, and exp 4 run 2's mechanism is *undetermined* (D19). The pre-registered secondary transfer A2 − F2 = +0.078 [+0.018, +0.137] (Sonnet), and the held-out edges +0.108 and +0.116, are quantum wins over the matched twin | overclaim |
| 2 | "**Every positive quantum-vs-classical difference has a classical account.**" (README.md:13; v3 abstract; v3:880) | Sonnet: F2+ − A2 +0.004 [−0.032, +0.042], κ = 0 −0.006. Haiku held-out: F2+ − A2 −0.019 [−0.073, +0.029], F2+ − A2.1 −0.037 (CI contains 0). Exp 5: D5 = A5. Three edges and three matches. Caveat: F2+ was designed after the Sonnet edge was seen (f7afd8a, 5 min after b584386), then applied frozen to Haiku's set (Addendum E, 73 s, archival) | holds (minor) |
| 3 | "**Self-report does as well.** ... as well as anything here, for both Haiku and Sonnet" (README.md:16) | Run 2b G 0.82 [0.71, 0.90] > every arm. Locked test G 0.83 vs F2 0.84, A2.1 0.84. Run-2 held-out G 0.82. Sonnet G − A2 +0.008 [−0.061, +0.080] | holds |
| 4 | "The encoded belief states are certified entangled on real hardware (3 of 3 items, 44 QPU s)" (README.md:17; paper:22; v3 abstract, :829–833) | witness-run-1: N = 0.147, 0.063, 0.067, lower bounds > 0, also without mitigation; rule ≥ 2 of 3. One two-qubit pair per item, and one pair is decoupled from its state ("effectively a two-qubit test"). Hardware N is about half the simulated value on two items. An entangled pair does imply a non-separable state, so the logic holds | holds (minor) |
| 5 | "Eleven pre-registered tests, six ... and five ..." (README.md:21; brief:4) | Six gold-map (9, 3a, 1, 2, 3, 4) plus five biomimetic (bm3, bm7, bm9, bm2, bm1) = 11 ✓. Five are archival, and only six collected new data | holds (count) |
| 6 | "about $4.2 in all, with no refusals" (README.md:21; brief:6–7) | Archived cost_usd sum $4.1695; ≤ $4.37 with the crash bound. Every file says no refusal; the archives store no stop_reason. api-usage.md records none of it | holds |
| 7 | "**The answer is mostly constructed by the asking.**" (README.md:23; brief:14 "Mostly the second") | Rests on D34, D37/D45, D38/D46, D44/D47 (README bullets). All Haiku; 40 exp-5 items and 16 exp-4 vignettes. "Mostly" has quantitative support only in D46 (Q = 0.39, so about 61% of the reproducible format-specific answer is not shared) and D45 (R ≈ 1). On Opus the format leg fails (26 claims, ΔLL +0.42 [−1.83, +2.69]) and the question leg is undecided (R 0.93 [0.06, 7.31]). README gives no model scope; the brief (line 144) does | overclaim (README) |
| 8 | "Asking earlier questions is invasive (NSIT, 5 of 6 families)" (README.md:24; brief:33; NC:18) | gm9: Holm p 0.0012 on 5 families, N4 p 0.16 ✓ | holds |
| 9 | "Order effects survive hiding the model's own earlier answers (R = 1.91 [0.92, 4.90])" (README.md:25) | Superseded by D45: R = 1.23 [0.75, 2.02] on 40 items. 1.91 came mostly from h191 (gm2b:15) | wrong (stale) |
| 10 | "Six ways of asking the same 160 statements need six separate credences (86% of claims; formats reorder statement pairs 21–35% of the time, against 4–8% noise)" (README.md:26) | gm3b: 86%, +19.36 [+16.50, +22.08] ✓. 21–35% and 4–8% are from the "noise baseline (computed after the run, not pre-registered)" (gm3b:34). gm3b's own caveat: the test "does not show that a single latent is useless". D46: one credence recovers 39%. Opus: one credence fits as well. "Need" overstates it | overclaim |
| 11 | "The model binds itself to its *own* earlier numbers but not to another person's identical numbers (slope +0.42 against +0.05)" (README.md:27) | bm1: +0.42 [+0.25, +0.60] vs +0.05 [−0.08, +0.17] ✓. But the two arms differ in wording ("give your rating again" against "accept or revise"; bm1:20, bm0:27), and the "other" arm is run 3's archive from another session. Uptake 0.42 is not binding; at 60 points it is 0.21 (bm0) | overclaim |
| 12 | "**Self-knowledge is text-reading.** Each model judges its own answers no better than the other model does" (README.md:29) | gm1: I = −0.055 [−0.103, −0.007] ✓. But Δ_S = SS − HS = +0.031 [−0.009, +0.073]: Sonnet's point estimate *is* better on its own answers. "Text-reading" is a mechanism inferred from a behavioural null, with 2 judges and AUROC additivity assumed by I | overclaim |
| 13 | "Ratings that commit the conjunction fallacy yet cancel in the Costello–Watts identity (Z = −0.03, flat slope)" (README.md:34); "Its ratings obey a noise-cancelling identity despite its fallacies (10)" (brief:134) | bm2: mean Z −0.034 [−0.071, +0.002], equivalence band ±0.05 → **undetermined** (bm2:26); slope +0.015 [−0.165, +0.164] | overclaim |
| 14 | "A consistent choice of relevant claims to check" (README.md:33; brief:62, :133) | gm4: modal share 87%; EIG and confirmatory both beat chance; discriminating menus CI include 0 ✓ | holds |
| 15 | Controls "are fixed before results exist, so a quantum encoding cannot win against a strawman" (README.md:187) | F and G added 49 s after run 2's result (see record-accuracy #36) | wrong |
| 16 | "the LLM studies observe only answers" (README.md:189) | clonable-minds:141 and related-work: Kang uses next-token probabilities; Lo et al. use BERT masked-token outputs | wrong (internal inconsistency, minor) |
| 17 | Beuria "as summarised by Springer Nature (we could access only the summary)" (README.md:181) | related-work.md:320 "[partial: published abstract and appendices; full v1 preprint]"; clonable-minds:137 "the Research Square preprint and the author's public code were read". Clonable-minds:143 says "four 7–8B open models", README and related-work say six | wrong (internal inconsistency) |
| 18 | Wolf et al.: "Secondary sources differ on the paper's title" (README.md:183) | related-work.md:300 gives the title and arXiv:2607.15277, read in full | wrong (stale, internal inconsistency) |
| 19 | "So far the answer is negative" bullets (README.md:192–195) | 0.55 < C/D/E ✓; ties ✓; G as good as anything ✓; exp 3 27/218, p 0.24 ✓ | holds |
| 20 | "There is no stored, format-free credence behind them that the different questions all read out" (brief:19) | D38 + D46 on Haiku; brief:25 then restricts it to Haiku. Holds as a Haiku statement inside a Haiku brief | holds (minor) |
| 21 | "a stronger model reading the same answer judges it better than its author does" (brief:19) | SH 0.932 > HH 0.845; OS 0.959 > SS 0.903 ✓ | holds |
| 22 | "Its own planted answers bind it at every distance and after intervening turns, while another person's are ignored" (brief:24) | bm0 own 0.71/0.44/0.21, lag 3 0.57 ✓; other +0.19 [−0.19, +0.50] at 10 points, mean +0.02 ✓. Wording confound as in #11; "bind" against uptake of 0.21–0.71 | overclaim |
| 23 | "Opus's formats agree closely enough to read as one belief" (brief:25); "On Opus the six formats read as one" (brief:145) | Opus: 26 of 80 claims, all from items Haiku got wrong; pre-registered reading *mixed*, not *single credence*; D48: "not supported on Opus, not ... refuted"; W not item-matched | overclaim |
| 24 | "This holds for every quantum-cognition test run on a language model, ours included" (brief:36) | clonable-minds' corollary (§3.2) covers *sequential* protocols only; §6 puts single-prompt and contextuality studies (Beuria, Wolf, Kumar, Lo) in other classes | overclaim |
| 25 | "The scale-flip slip is just a slip" (brief:39); "Its scale-reading slips are noise, unrelated to its errors (2)" (brief:132); "The scale-direction slip is unrelated to errors" (NC:339) | gm3a: AUROC 0.48 [0.28, 0.66]; pre-registered reading "**no evidence either way**"; gm3a itself says "With 40 items it can only rule out a large effect". The gap is a systematic 37 points, not noise | overclaim |
| 26 | "So the model's best error signal is good reading of the answer text, not access to anything inside" (brief:47) | gm1 shows no authorship advantage. It does not test the incremental value of the self-signal over a reader's signal | overclaim |
| 27 | "the order effect gets larger, not smaller: 16.7 points against 8.7" (brief:51) | gm2 ✓ for 10 items. gm2b:28: "'The redacted effect is larger than the shown' should no longer be said"; brief:91 revises it, but line 51 stands unmarked | overclaim (stale) |
| 28 | "The model treats its own past answers as commitments" (brief:84; bm1:15; bm0:24; record:57) | bm1/bm0 behavioural contrast with a wording confound; the distance fall-off has two readings (bm0:17) | overclaim |
| 29 | "It resists other people's numbers rather than absorbing them (7, 11)" (brief:135) | 7 (bm3) and 11's s_other (bm1) are **the same run-3 archive**. bm0:12: other's number "is not resisted either: about a quarter of cells move away, and no more" | wrong (double count, contradicted by bm0) |
| 30 | "the model pulls each new number toward the last one it gave (4, 9)" (brief:127) | gm2 planted pull 5.6 [3.4, 7.6] ✓; bm9 β +0.27 [+0.11, +0.43] ✓. bm9 uses exp 5's QQ block, the same conversations as gm9's N1M/N1S, which brief:124 ("One") also counts | holds (minor; shared data) |
| 31 | "So the stronger the model, the more there is a belief to read" (brief:147) | Three models. Opus's arm is incomplete, its W is not item-matched, and F′ was not computed on Opus. brief:154 itself calls this "trend or ... artefact" undecided | overclaim |
| 32 | "No privileged self-knowledge holds on all three models" (brief:112; NC:27; NC:302) | Two tests: Haiku×Sonnet I = −0.055 [−0.103, −0.007]; Sonnet×Opus I = −0.045 [−0.107, +0.017]. DM3 reuses D36's SS cell (multi-model:68), so Sonnet's self cell is the same data in both. The disagreement subset is +0.184 [−0.296, +0.812] | holds (minor; one cell shared) |
| 33 | "Leaning on its own record holds on all three" (brief:113; NC:28) | multi-model: 78→25, 88→35, 95→65 ✓. Haiku row = D37 repeats 0–3, not new data | holds |
| 34 | "The question alone constructs the judgment on Sonnet (R = 2.95)" (brief:118; NC:30) | R = 2.95 [0.99, 12.55] at R = 4; "much of it comes from 2 of the 10 items, one of them ... h191" (multi-model:20) — the concentration D45 showed inflates Haiku's 10-item R | holds (minor) |
| 35 | Title: "No Credence to Read: ... Construct a Language Model's Judgments" (NC:1) | NC:350: "It should not be stated for language models in general"; D48 left the title unchanged | overclaim |
| 36 | "Every number below ... was produced under a pre-registration committed before its data, unless it is labelled *exploratory*" (NC:9) | Archival N, A, free look, F′, and S's comparator. The unlabelled post-hoc noise baseline at NC:23 and NC:337 ("computed after the run, not pre-registered", gm3b:34) | wrong |
| 37 | "a complete state that is a classical string: the conversation so far, plus the sampler's random state. That string can be copied." (NC:15) | NC §2.2 (line 82) and gm9:17: "The API exposes no seed"; only the context can be copied | wrong (self-contradiction) |
| 38 | "Formats disagree ... four to six times more often than repeat noise" (NC:23; v3:78) | post-hoc baseline, not labelled exploratory | overclaim |
| 39 | "self-reported confidence carries no information a capable reader of the answer lacks" (NC:58) | gm1 tests the authorship advantage (I), not the incremental information of HH over SH. On Sonnet's answers the weaker reader (HS 0.872) trails the author (SS 0.903) | overclaim |
| 40 | "the model's own recorded answers, but not other people's" (NC:344); "The R channel is source-specific: it carries the model's own record, not any number in the context" (clonable:133) | wording confound (NC:409 limitation itself says "this caveat stands") | overclaim |
| 41 | "the weaker the model, the less of a format-free belief there is to find" (NC:352) | F′ on two models (Haiku 0.29, Sonnet 0.69); Opus not computed | overclaim |
| 42 | Macrorealism "holds by construction"; "every violation is invasiveness" in sequential protocols (clonable:10–11, §3.1–3.2; NC:15, :56) | A valid argument *given* λ = (context, sampler state) and a stateless server. It is definitional: any context change counts as invasiveness. No data in the repository test it, and the server's statelessness is assumed (clonable:38, :189 "None of these applies") | holds (as argument; not an empirical result) |
| 43 | "None of these applies to the runs in this project" (clonable:189) | Server-side state and weight stability cannot be checked from the client; asserted, not tested | overclaim (minor) |
| 44 | Short paper: G "predicted its errors better than every structural reading of its explanation (0.82). And the one edge the learned quantum model ever showed, on a second base model's errors, ... a classical model with the same angle reproduces exactly" (paper:23) | Better than every arm only in run 2b. On the locked test G 0.83 < F2 0.84, A2.1 0.84. There were three edges (Sonnet +0.078, Haiku held-out +0.108 and +0.116), not one. F2+ − A2 = +0.004 [−0.032, +0.042] is a tie, not "exactly" | wrong |
| 45 | "Every pre-registered comparison against a matched classical model was a tie or a loss" (paper:41) | Sonnet A2 − F2 +0.078 [+0.018, +0.137] (pre-registered secondary transfer, frozen parameters) is a win | wrong |
| 46 | "One call asking the model how confident it is outperforms every structural analysis of its reasoning ... 0.83 on the locked test set" (paper:176–177) | Locked test: F2 0.84, A2.1 0.84, A2 0.83, G 0.83 | wrong |
| 47 | "A classical Markov chain describes them as well as the quantum state does" (paper:224), where "them" includes the conjunction fallacies | D5 was fitted only to exp 5's sequential ratings; no Markov model was fitted to exp 4's fallacies | overclaim (minor) |
| 48 | v3 abstract: "six gold-map tests on November 4, each pre-registered before its data" (v3:73) | D34 and D35 are archival, with 89 s and 47 s gaps and analysis code committed with the result | overclaim |
| 49 | "Every addition was pre-registered before its data" (v3:858); "That answer is pre-registered throughout" (v3:879) | D13 committed 6 s after first call; D26 after full-run calls began; D28 code after calls began; D9 after pool calls began. Primary verdicts were pre-registered | overclaim |
| 50 | "The model's self-reported confidence is text-reading, not privileged self-knowledge" (v3:884; record:78) | as #12 | overclaim |
| 51 | "Its order effects come from both the question and its own recorded answers" (v3:885) | D45 (v3's own abstract, line 76): the question carries roughly all of the order effect, and the record adds little to it | wrong (stale) |
| 52 | v3 §9: "Directions 5–8, 10 and 11 ... none is pre-registered"; follow-ups listed include "a held-out-*format* test" and a less unusual placeholder (v3:874, :889–890) | Direction 5 pre-registered on `probes` (9ef909d 07:39). The held-out-format test ran as D46; the placeholder check passed in D45 | wrong (stale) |
| 53 | v3 §6.1 / paper §5: "Four pre-registered comparisons ... In none of them does the quantum state add anything to error prediction" (v3:764–770) | H2, v2, v2.1, run 2b ✓ (all primary) | holds |
| 54 | v3 §7 AI: one confidence call "predicts its errors better than any analysis of its written reasoning we built" (v3:845) | Locked test: G 0.83 vs F2 0.84 and A2.1 0.84 (ties). "Better" holds only for run 2's fixed-encoding arms | overclaim (minor) |

## Holes found
1. **The same data are counted as independent support.**
   - **Run 3's "another person" calls (exp4-run-3, 23:01–23:16)** are the data for bm3 (D40), for bm1's s_other (D44) and for bm0's ±30 "other" cell (D47). The brief's "It resists other people's numbers rather than absorbing them (7, 11)" cites two results that are one archive. bm0:12 then says the other-person number "is not resisted either".
   - **bm0's ±30 own lag-0 cell is bm1's data.** The pooled own − other of +0.46 is therefore not independent of bm1's +0.37. "Own beats other" has one independent replication, at ±10 and ±60, not two.
   - **gm2b (D45) pools gm2's (D37) 10 items and conversations.** The 30-new-items row (0.99 [0.51, 1.61]) is the only independent replication.
   - **D46 reanalyses D38's 9,600 calls.** NC:23 lists them as one bullet, which is fine. The brief counts them as results 5 and 13.
   - **gm9's N1M/N1S and bm9 use the same exp-5 QQ conversations.** brief:124 "One" and brief:127 "Four" both draw on them.
   - **DM3 reuses D36's SS cell,** so the "holds on all three models" self-knowledge claim shares Sonnet's self-judgement data across its two tests.
   - **The multi-model Haiku rows** (78→25, R 2.01, W 0.54, Q 0.29) are re-analyses of D37 and D38, not new Haiku data.
2. **Independent tests behind each synthesis claim:**

   | claim | independent data | tests |
   |---|---|---|
   | "constructed by the asking" | exp 5 archive (D34); gm2 + gm2b transcripts (D37/D45); gm3b calls (D38/D46); bm1 + bm0 calls with run 3 as comparator (D44/D47) | 4 collections; one model; 2 item sets (40 hard-pool items, 16 vignettes) |
   | "self-knowledge is text-reading / not privileged" | D36 | 1 on Haiku; plus DM3 (shares SS) on Sonnet×Opus |
   | "no single credence" | gm3b | 1 on Haiku (D38, with D46 re-analysing it); Sonnet *mixed* and *partial*; Opus *mixed*, pointing the other way |
   | "binds itself to its own numbers" | bm1 + bm0 | 2 collections sharing cells, both against an archived, differently worded comparator |
   | "every positive difference has a classical account" | three edges, each matched | 3 matches, two on sets already scored |
   | "no quantum advantage" | H2, v2, v2.1, exp 5 | 4 primary; exp 3/4 do not count as failures |
3. **README's overnight section is stale and has no model scope.**
   - **When it was last touched.** 2d49fcf, 05:41.
   - **What it still says.** R = 1.91 (now 1.23); "need six separate credences" (now Q = 0.39 on Haiku, *partial* on Sonnet, not supported on Opus).
   - **What it never mentions.** The robustness wave, the multi-model replications and D48.
   - **Why that matters.** It is the most-read summary, and it states the construction finding without "on Haiku". The No Credence paper (NC:350) says this "should not be stated for language models in general".
4. **The no-quantum-advantage headline contradicts its own next bullet.**
   - **The headline.** README:12 says every pre-registered test of a quantum advantage "failed or tied".
   - **The next bullet.** README:13–15 lists positive differences that needed a classical account.
   - **What the short paper does.** It goes further: "Every pre-registered comparison against a matched classical model was a tie or a loss" (paper:41) and "the one edge the learned quantum model ever showed" (paper:23).
   - **The record.** The Sonnet transfer (+0.078 [+0.018, +0.137]) and Haiku's held-out edges (+0.108, +0.116) were pre-registered comparisons against the matched twin, and the quantum model won them. The negative conclusion survives only once F2+ explains them; the summaries erase that step.
   - **Experiments 3 and 4.** Calling them "failed or tied" is wrong. They were inconclusive or untestable.
5. **The source effect is confounded with wording in every headline that states it.**
   - **The confound.** The own condition says "Please give your rating again". The other condition, archived from run 3 and re-used in D47, says "accept or revise".
   - **Where the authors admit it.** bm1:20, bm0:27 and NC:409 all state the caveat ("this caveat stands").
   - **Where it is left out.** README:27, brief:24, brief:84, NC:21, NC:344 and clonable:133.
   - **What follows.** "Source-specific" and "commitments" cannot be separated from a prompt-wording effect.
6. **Mechanism words from behavioural nulls.**
   - **"Text-reading"** (README:29, v3:884, record:78, brief:47): the test shows no authorship advantage with 2 judges. It does not show that the self-signal is fully redundant with a reader's.
   - **"Carries no information a capable reader lacks"** (NC:58): an incremental-validity claim that was never tested.
   - **"Noise-cancelling identity"**: the equivalence test was undetermined.
   - **"Just a slip" / "noise"**: the pre-registered reading was "no evidence either way", with CI [0.28, 0.66].
7. **Post-hoc numbers presented as pre-registered.**
   - **The baseline.** gm3b's 4–8% repeat-noise baseline is explicitly "computed after the run, not pre-registered".
   - **Where it appears unlabelled.** NC:23 and v3:78 put it in their abstracts ("four to six times"), and NC:337 uses it again. NC:9 says every unlabelled number was pre-registered.
   - **Another post-hoc reading.** bm2's "PT+N 2014 fits best" reading (brief:75) was written 18 s after the result (605fa97), replacing "the sampling account ... is not supported".
8. **Self-contradictions inside documents.**
   - NC:15 ("plus the sampler's random state. That string can be copied") against NC:82 ("The API exposes no seed").
   - The NC title against NC:350.
   - brief:147 (trend asserted) against brief:154 (trend undecided).
   - v3:885 (both channels) against v3:76 (question carries roughly all).
   - README:181/183 against related-work.md and clonable-minds on the Beuria and Wolf readings, including the model count, four against six.
9. **Scope of the clonable-minds argument.**
   - **What is careful.** The note limits its corollary to sequential protocols and sorts other studies into separate classes.
   - **What is not.** The brief (line 36) generalises it to "every quantum-cognition test run on a language model".
   - **What it rests on.** Its premise that the server keeps no state (clonable:38, :189) is an assumption about the provider, not a measured fact.
   - **What it is.** The "macrorealism holds by construction" result is a definitional argument. It is sound, but no experiment tests it, and the record (record:48) presents it as a "diagnosis" of D34.

## Overclaims to cut (exact sentences)
- `README.md:12` — "- **No quantum advantage.** Every pre-registered test of a quantum advantage failed or tied: the entangled readout, the learned v2 and v2.1 encodings, sequential judgment (experiment 5), and the order-effect tests (experiments 3 and 4)." — exps 3 and 4 were inconclusive or untestable, and secondary pre-registered edges existed. — "- **No quantum advantage.** Every primary pre-registered test of a quantum advantage failed or tied: the entangled readout, the learned v2 and v2.1 encodings, and sequential judgment (experiment 5). The order-effect tests (experiments 3 and 4) were inconclusive or untestable."
- `README.md:23` — "**The answer is mostly constructed by the asking.**" — Haiku only; Opus's formats are not shown to differ. — "**On Haiku, the answer is largely constructed by the asking** (on Sonnet partly; on Opus the format finding does not hold: `results/multi-model.md`)."
- `README.md:25` — "- Order effects survive hiding the model's own earlier answers (R = 1.91 [0.92, 4.90])." — superseded. — "- Order effects survive hiding the model's own earlier answers (R = 1.23 [0.75, 2.02] on all 40 items; 0.99 on the 30 new ones)."
- `README.md:26` — "- Six ways of asking the same 160 statements need six separate credences (86% of claims; formats reorder statement pairs 21–35% of the time, against 4–8% noise)." — "need" outruns a held-out-repeats test, and the noise baseline is post hoc. — "- On Haiku, six ways of asking the same 160 statements fit held-out repeats better with six separate credences (86% of claims), and one credence recovers only 39% [30%, 50%] of a left-out format (formats reorder statement pairs 21–35% of the time, against 4–8% between halves of one format, a baseline computed after the run)."
- `README.md:27` — "- The model binds itself to its *own* earlier numbers but not to another person's identical numbers (slope +0.42 against +0.05)." — wording confound; 0.42 is not binding. — "- A number planted as the model's own earlier answer pulls its re-rating (slope +0.42) far more than the same number credited to another person under different wording (+0.05)."
- `README.md:29` — "**Self-knowledge is text-reading.** Each model judges its own answers no better than the other model does; the judge × author interaction is −0.055 [−0.103, −0.007]." — mechanism claim; Δ_S is +0.031. — "**No privileged self-knowledge.** With each judge's overall skill cancelled, authorship gives no advantage: the judge × author interaction is −0.055 [−0.103, −0.007]."
- `README.md:34` — "- Ratings that commit the conjunction fallacy yet cancel in the Costello–Watts identity (Z = −0.03, flat slope)." — the equivalence test is undetermined. — "- Ratings that commit the conjunction fallacy yet nearly cancel in the Costello–Watts identity (Z = −0.03 [−0.07, +0.00], short of the ±0.05 equivalence band; flat slope)."
- `README.md:181` — "- **Beuria (2026)**, as summarised by Springer Nature (we could access only the summary)." — contradicts related-work.md:320 and clonable-minds:137. — "- **Beuria (2026)**, read from the published abstract and appendices and the v1 preprint (`paper/related-work.md`)."
- `README.md:183` — "Secondary sources differ on the paper's title, and we have not tied it to a quantum account; it is a test of classical coherence." — related-work.md:300 has the title and arXiv id. — "\"Partition, Prompt, Aggregate: Statistical Self-Consistency in Language Models\" (arXiv:2607.15277); it is a test of classical coherence, not tied to a quantum account."
- `README.md:189` — "Quantum-cognition models are fitted to aggregate answer frequencies, and the LLM studies observe only answers." — Kang uses next-token probabilities, and Lo et al. use BERT outputs. — "Quantum-cognition models are fitted to aggregate answer frequencies, and the LLM studies observe outputs (answers or token probabilities)."
- `paper/morning-brief.md:24` — "- **The model is bound to its own answers.** Its own planted answers bind it at every distance and after intervening turns, while another person's are ignored." — wording confound; uptake 0.21–0.71. — "- **The model leans on its own answers.** Numbers planted as its own answer pull its re-rating at every distance tested and after three filler turns, while the same numbers credited to another person, in a differently worded prompt, have no reliable pull."
- `paper/morning-brief.md:25` — "Opus's formats agree closely enough to read as one belief." — pre-registered reading *mixed*; 26 claims. — "On Opus's 26 statements, one credence fits as well as six (pre-registered reading *mixed*)."
- `paper/morning-brief.md:36` — "This holds for every quantum-cognition test run on a language model, ours included." — the corollary covers sequential protocols only. — "This holds for every sequential test run on a language model through its conversation, ours included."
- `paper/morning-brief.md:39` — "2. **The scale-flip slip is just a slip (direction 3's free look, $0).**" — the pre-registered reading was "no evidence either way". — "2. **The scale-flip gap shows no detectable link to errors (direction 3's free look, $0).**"
- `paper/morning-brief.md:47` — "   - So the model's best error signal is good reading of the answer text, not access to anything inside." — mechanism inferred from a null. — "   - So there is no sign that authorship adds anything to the error signal beyond what a capable reader of the answer finds."
- `paper/morning-brief.md:51` — "   - **Hidden answers:** the order of the questions still changes the verdict, and the order effect gets larger, not smaller: 16.7 points against 8.7." — gm2b says this should no longer be said. — "   - **Hidden answers:** the order of the questions still changes the verdict (16.7 points hidden against 8.7 shown on these 10 items, mostly from h191; on all 40 items 12.0 against 9.8, result 12)."
- `paper/morning-brief.md:84` — "    - The model treats its own past answers as commitments." — behavioural contrast with a wording confound. — "    - This fits the model treating its own past answers as commitments, though the own and other prompts also differ in wording."
- `paper/morning-brief.md:132` — "- Its scale-reading slips are noise, unrelated to its errors (2)." — CI [0.28, 0.66]; the gap is systematic. — "- Its scale-reading gap shows no detectable relation to its errors (2; AUROC 0.48 [0.28, 0.66])."
- `paper/morning-brief.md:134` — "- Its ratings obey a noise-cancelling identity despite its fallacies (10)." — equivalence undetermined. — "- Its ratings nearly satisfy a noise-cancelling identity despite its fallacies (10; Z = −0.03 [−0.07, +0.00])."
- `paper/morning-brief.md:135` — "- It resists other people's numbers rather than absorbing them (7, 11)." — 7 and 11 are one archive, and bm0 finds it "not resisted either". — "- It does not take up other people's numbers (7 and 11, both from run 3's archived calls; 14 finds them neither taken up nor resisted)."
- `paper/morning-brief.md:145` — "  - On Sonnet a single belief is partly usable. On Opus the six formats read as one." — as above. — "  - On Sonnet a single belief is partly usable. On Opus's 26 statements one belief fits as well as six (reading *mixed*)."
- `paper/morning-brief.md:147` — "  - So the stronger the model, the more there is a belief to read." — the brief itself (line 154) says this is undecided. — "  - The three models are ordered that way, but Opus's arm is incomplete and not item-matched, so whether it is a trend is open (see below)."
- `paper/no-credence-to-read.md:1` — "# No Credence to Read: The Question, the Record and the Format Construct a Language Model's Judgments" — NC:350 says it should not be stated for language models in general. — "# No Credence to Read: The Question, the Record and the Format Construct Claude Haiku's Judgments"
- `paper/no-credence-to-read.md:9` — "Every number below is copied from a results file in the repository's `results/` directory and was produced under a pre-registration committed before its data, unless it is labelled *exploratory*." — archival analyses; an unlabelled post-hoc baseline. — "Every number below is copied from a results file in the repository's `results/` directory and was produced under a pre-registration committed before its analysis or first call, unless it is labelled *exploratory*. Several analyses reuse archived data already opened for earlier tests (Section 6)."
- `paper/no-credence-to-read.md:15` — "A language model reached through a stateless API has, at every turn, a complete state that is a classical string: the conversation so far, plus the sampler's random state. That string can be copied." — contradicts §2.2's "The API exposes no seed". — "A language model reached through a stateless API has, at every turn, a complete state: the conversation so far, a classical string that can be copied, plus the sampler's random state, which the API does not expose; a copy therefore reproduces the response distribution exactly."
- `paper/no-credence-to-read.md:23` — "The formats rank the statements differently four to six times more often than repeat noise does." — post-hoc baseline, unlabelled. — "The formats rank the statements differently four to six times more often than repeat noise does (exploratory: the noise baseline was computed after the run)."
- `paper/no-credence-to-read.md:58` — "On Haiku, they show that the question and the model's own recorded answer both construct later judgments, that the format constructs the credence, and that self-reported confidence carries no information a capable reader of the answer lacks (Sections 4.1–4.5)." — incremental information not tested. — "On Haiku, they show that the question and the model's own recorded answer both construct later judgments, that the format constructs the credence, and that authorship gives self-reported confidence no advantage over a capable reader of the answer (Sections 4.1–4.5)."
- `paper/no-credence-to-read.md:339` — "- The scale-direction slip is unrelated to errors." — "no evidence either way". — "- The scale-direction gap shows no detectable relation to errors (AUROC 0.48 [0.28, 0.66])."
- `paper/no-credence-to-read.md:344` — "- the model's own recorded answers, but not other people's (Sections 4.2 and 4.3)." — wording confound. — "- the model's own recorded answers, far more than other people's numbers given in a differently worded prompt (Sections 4.2 and 4.3)."
- `paper/no-credence-to-read.md:352` — "So the difference from their result is mostly the model, not the criterion: the weaker the model, the less of a format-free belief there is to find." — two models; Opus F′ not computed. — "On the two models where F′ was computed, the difference from their result follows the model more than the criterion; Opus's F′ would show whether it is a trend."
- `paper/clonable-minds.md:133` — "The R channel is source-specific: it carries the model's own record, not any number in the context." — wording confound. — "The R channel looks source-specific: a number in the model's own turn pulls the re-rating, while the same number credited to another person, under different wording, does not."
- `paper/clonable-minds.md:189` — "None of these applies to the runs in this project." — server state cannot be checked from the client. — "None of these is known to apply to the runs in this project; the server's statelessness is taken from the API's documented behaviour, not tested."
- `paper/the-entangled-mind-paper.md:23` — "The model's own stated confidence predicted its errors better than every structural reading of its explanation (0.82). And the one edge the learned quantum model ever showed, on a second base model's errors, was a per-claim readout angle that a classical model with the same angle reproduces exactly." — locked test G 0.83 < F2 0.84; three edges; a tie is not "exactly". — "The model's own stated confidence predicted its errors better than every fixed-encoding arm (0.82) and as well as the learned models. And the learned quantum model's edges, on a second base model's errors and on Haiku's held-out set, came from a per-claim readout angle that a classical model with the same angle matches."
- `paper/the-entangled-mind-paper.md:41` — "Every pre-registered comparison against a matched classical model was a tie or a loss." — Sonnet transfer +0.078 [+0.018, +0.137]. — "Every primary pre-registered comparison against a matched classical model was a tie or a loss, and each secondary edge was matched by a classical model with the same readout."
- `paper/the-entangled-mind-paper.md:176` — "**One call asking the model how confident it is outperforms every structural analysis of its reasoning**, quantum or classical:" — on the locked test 0.83 against 0.84. — "**One call asking the model how confident it is matches or beats every structural analysis of its reasoning**, quantum or classical:"
- `paper/the-entangled-mind-paper.md:224` — "A classical Markov chain describes them as well as the quantum state does." — D5 was not fitted to the fallacies. — "In experiment 5, a classical Markov chain describes the order effects as well as the quantum state does."
- `paper/the-entangled-mind-v3.md:73` — "**After the programme: six gold-map tests on November 4,** each pre-registered before its data (Section 5.13)." — two are archival. — "**After the programme: six gold-map tests on November 4,** each pre-registered before its analysis or first call; two reanalyse archived experiment-5 data (Section 5.13)."
- `paper/the-entangled-mind-v3.md:78` — "The formats rank the claims differently, four to six times beyond repeat noise." — post-hoc baseline. — "The formats rank the claims differently, four to six times beyond repeat noise (an exploratory baseline)."
- `paper/the-entangled-mind-v3.md:858` — "Every addition was pre-registered before its data, but designed knowing run 2 had failed (Section 4)." — D9, D13, D26 and D28's code followed their first calls. — "Every addition was pre-registered before it was scored, but designed knowing run 2 had failed; four (D9, D13, D26, D28's code) were committed after their first calls had begun (Section 4)."
- `paper/the-entangled-mind-v3.md:879` — "- That answer is pre-registered throughout." — as above. — "- Its primary verdicts are pre-registered."
- `paper/the-entangled-mind-v3.md:884` — "- The model's self-reported confidence is text-reading, not privileged self-knowledge." — mechanism from a null. — "- The model's self-reported confidence shows no privileged self-knowledge: a capable reader of its answer does as well or better."
- `paper/the-entangled-mind-v3.md:885` — "- Its order effects come from both the question and its own recorded answers." — contradicts D45 and v3's own abstract. — "- Its order effects survive hiding its recorded answers (the question carries roughly all of them), while its recorded answers steer the level of later ratings."
- `paper/record.md:78` — "  - self-report is text-reading, not privileged access (direction 1);" — as #12. — "  - self-report shows no privileged access (direction 1);"

## Does the verdict stand?
The documents' overall conclusions:
- **Quantum structure adds nothing over matched classical models for this model's judgments: STANDS.** All four primary comparisons tie or lose. Each of the three secondary edges is matched by F2+ or D5. Self-report matches the best structural arm.
- **On Haiku, the asking constructs much of the answer: STANDS WITH CAVEATS.** The supporting tests do hold on their own numbers. But they rest on about four independent data collections from one model and two item sets. The source leg is confounded with prompt wording. The format leg weakens on Sonnet and is not supported on Opus.
- **The summaries themselves (README's overnight section in particular) overstate it.** They drop the model scope, quote superseded numbers, count shared data twice, and use mechanism words ("text-reading", "binds", "commitments") that the behavioural contrasts do not establish.

Overall: STANDS WITH CAVEATS.

## Confidence
Medium.
- **What I checked.** Every aggregate claim against the results files' own tables, and the data overlaps through each result's stated design (cells reused, archives named).
- **What I did not recompute.** Raw statistics, per the assignment.
- **What I could not verify.** Whether F2+ or the archival analyses were tried before their pre-registration commits. The server statelessness that clonable-minds assumes. The external papers behind the README's related-work characterisations: I checked those only for consistency with `paper/related-work.md` and `paper/clonable-minds.md`.

## Tally
claims_checked: 54
claims_failed: 38
overclaim_sentences: 43
verdict: STANDS WITH CAVEATS
confidence: medium

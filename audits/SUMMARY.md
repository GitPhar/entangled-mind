# Independent audit: summary

Branch `audit`, 2026-11-04. Scope: every result in `results/` plus the unmerged `probes` branch. That is 39 per-result audits, plus two cross-cutting audits: `record-accuracy.md` (the record as a ledger) and `synthesis-claims.md` (README, morning brief and paper-level claims). No API calls were made, and nothing outside `audits/` was changed.

## In plain English

**The numbers are sound; the words are not.**
- Every headline statistic was recomputed from the archived JSON with independent code. All of them reproduce, apart from a handful of miscounts listed below.
- No pre-registered verdict is reversed outright. The project's central negative finding survives every check: no quantum advantage, and every quantum-vs-classical edge has a classical match.
- The problem is the prose around the numbers. **38 of the 39 results (97%) carry at least one sentence that says more than the data show, and 30% of the 560 claims checked fail.** Most of the failures (about three in four) are in the README and the paper files rather than the results files. The prose gets stronger the further it travels from the table.

**The common failure patterns:**
1. **Nulls written as findings.** An interval that includes zero becomes "no decay", "carries no error signal", "does not prefer", "not invasive" or "holds on all three models".
2. **Mechanism words a behavioural contrast cannot carry.** Examples: "text-reading", "consistency is memory", "binds itself to its own numbers", "treats its answers as commitments", "reactance".
3. **Point estimates read as rankings.** "Every control does better" and "self-report outperforms every structural analysis" are point-estimate statements; the second is false at the point estimate too (F2 0.84 against G 0.83).
4. **The same data counted twice** in the overnight synthesis. It rests on about four independent data collections, all on Haiku and two item sets, not eleven.
5. **Results driven by one or two items, presented as general.**

**The verdicts are robust only in direction, not in label.**
- None of the 39 is reversed.
- Two are UNDETERMINED (5%):
  - experiment 4 run 2, whose frozen rule could only ever return one answer;
  - gm3c, whose "little" label beats "partial" by 0.0012 and flips under a refit.
- In 9 of 39 (23%), counting those two, a pre-registered label fails under one defensible check: a single dropped item, another bootstrap seed, a multiple-comparison correction, or the authors' own reasoning from a later run.
- The most consequential is experiment 5. Its "tie" depends on pooling two scale directions that the authors themselves later called an artefact. On run 1's own single-direction data, the pre-registered contradiction condition is met, which would make the label "classical".

**The pre-registration record is mostly honest, with some soft spots.**
- Anthropic request and message IDs embed a millisecond timestamp. Decoding them dates every archived call independently of git.
- Every pre-registration predates its first call, except for small slips, all disclosed or harmless:
  - experiment 3's implementation choices: 6 s after its first call;
  - direction 1's runner: 3.5 min after its first call;
  - the D9 training pool: 23 min after its calls began;
  - experiment 5's D26 model details: after full-run calls began;
  - the witness D8 commit: after the hardware job.
- But 5 of the 11 overnight tests (6 of 14 with the robustness wave) re-analysed data the authors had already opened. The README's "frozen … before its data were opened" is false for them.
- The probe study's selection/test separation was never achieved. Its "new" step-3 ratings are an exact replay of the gate conversations (500 of 500 identical).

## Headline rates (39 per-result audits)

| measure | value |
|---|---|
| results with at least one overclaim sentence to cut | **38 / 39 (97%)** (the exception is `exp5-pilot`) |
| claims checked / claims failed (overclaim or wrong) | 560 / 166 (**30%**) |
| overclaim sentences listed | 303 in result audits + 53 in the two cross-cutting audits = 356; 309 distinct file:line targets (29 targeted by more than one audit) |
| where the overclaims sit (320 parsed entries) | 238 (74%) in README / paper / DEVIATIONS; 82 (26%) in `results/*.md` |
| quoted sentences confirmed verbatim at the cited location | 320 / 320 (lead auditor's own check) |
| **verdict reversal rate (strict: verdict REVERSED)** | **0 / 39 (0%)** |
| verdict UNDETERMINED after audit | 2 / 39 (5%): `exp4-run-2`, `gm3c-heldout-format` |
| a pre-registered label fails under one defensible check (includes the 2 above) | **9 / 39 (23%)**, listed below |
| verdict STANDS / STANDS WITH CAVEATS | 12 / 25 |
| auditor confidence high / medium | 34 / 5 |

**Fragile labels** (the overall verdict survives, but the label flips under one check):

| result | the check that flips it |
|---|---|
| `exp4-run-2` | The frozen anchoring rule could only ever return "static twin", and the README drops that verdict without saying so. |
| `gm3c-heldout-format` | The CI upper end is 0.4988 against a 0.5 bar. A refit and 5 of 6 bootstrap seeds give "partial". |
| `exp5-run-1` | Anchor (a) alone: q = −0.345 [−0.517, −0.181] (verified by the lead auditor). That meets the §7.5 contradiction condition, so the label is "classical", not "tie". One item (h183) supplies +55.8 of the +67 primary difference. |
| `stage2-run-1` | H3 and H4 flip on dropping one item. The pre-registration's own rule calls such verdicts "too noisy to call", but the rule was applied to H2 only. |
| `probe-dissociation` | The gate passes only uncorrected: under Holm it is 2 of 10, a fail. "Not with the rating" rests on three items, one of them (h191) opposing, and the probe moves only about 6% of its true–false gap. |
| `mm-gm3b-format-invariance` | Sonnet's "mixed" is one claim (h058 c8; without it, "no single credence"). The Opus row sits one claim from "one credence suffices", on a degenerate fit. |
| `mm-gm2-self-conditioning` | Without h058, Opus's "leaning question-driven" becomes "self-anchoring" (R = 0.14 [0.00, 0.46]). |
| `gm2b-self-conditioning-40` | The independent 30-item replication passes the frozen bar by 0.012 and fails it on 7 of 30 single-item drops. |
| `bm2-sampling-identity` | The 18-second "corrected reading" (PT+N 2014 fits best) is wrong by the map's own §3.4. The frozen verdict (flat slope) stands. |

## Pre-registration timing

Call times decoded from `req_01…` / `msg_01…` IDs (first 6 bytes are Unix ms). This was validated on the two refusals, which decode to 19:44:19 and 20:20:02, a minute before their commits. The decoder is `audits/tools/ridtime.py`.

| test | frozen | first call | gap | note |
|---|---|---|---|---|
| pool run 1 / pre-registration | `afe1c1b` 12:54:30 | 12:56:06 | +1.6 min | |
| D4 extension rules | `2248e54` 14:17:24 | 13:27 (extension calls) | **after** | rules reached git after all 67 extension calls |
| run 2b arm G (Addendum A) | `dd81f4f` 15:15:39 | 15:15:52 | +13 s | committed 49 s after run 2's H2 failure; G's code was in `3204d10` |
| witness (D8 calibration) | `f5f306b` 15:39:59 | job ran 16:06–16:07 | design OK | D8 committed 16:07:46, after the job, though its circuits were in the submitted job |
| D9 training pool | `930730c` 16:26:03 | 16:02:45 | **−23 min** | supplement chosen on interim error rates, before the split |
| experiment 3 (D13) | `de9c536` 15:39 / `958d9db` 17:23:10 | 17:23:04 | **−6 s** | D13 changed the budget and both secondary tests |
| experiment 4 | `54cfa1f` 16:52 | 18:10:21 | OK | |
| v2 locked test, arm G | `8a4faa2` 17:20:53 | 18:46:23 | OK | |
| experiment 4 run 2 | `cb4e96e` 19:05:10 | 19:34:11 | OK | |
| Sonnet arm G (Addendum D) | `f7afd8a` 21:03:08 | 21:03:26 | +18 s | its runner code was committed at 21:04:16 |
| experiment 5 pilot | `2c2ef6c` 20:15:54 | 20:18:49 | OK | |
| experiment 5 full run (D26) | `2251693` 20:32:21 / `1155dde` 20:34:48 | 20:30:12 | **−2 to −4.6 min** | 1,958 calls made before the analysis commit; partial data on disk |
| experiment 4 run 3 / experiment 5 run 2 (D33) | `fbc2fbf` 23:00:01 | 23:01:01 / 23:01:44 | OK | |
| D34 gm9 · D35 gm3a | 03:48:17 · 03:50:31 | archival | 89 s · 47 s to result | analysis code committed with the result: text-only freeze |
| D36 gm1 | `28a20b2` 03:52:51 | 03:54:55 | OK | runner entered git at 03:58:25; amendments made mid-run |
| D37 gm2 · D38 gm3b · D39 gm4 | 03:58 · 04:02 · 04:05 | 04:15 · 04:41 · 05:02 | OK | |
| D40 bm3 · D41 bm7 · D42 bm9 | 05:08:07 · 05:08:33 · 05:08:50 | archival | 15–16 s | code frozen in `9c29a94` before all three |
| D43 bm2 · D44 bm1 | 05:09:07 · 05:11:41 | 05:09:10 · 05:11:44 | +3 s each | |
| D45 gm2b · D46 gm3c · D47 bm0 | 06:30:14 · 06:33:43 · 06:37:52 | 06:30:19 · archival · 09:16:17 | OK | |
| direction 5 (probes) | `9ef909d` 07:39:41 | local, no IDs | not checkable | |
| DM2 · DM3 · DM4 · DM6 | 07:44:03 · 07:47:58 · 07:48:27 · 07:53:12 | 07:45:58 · 07:49:06 · 07:50:47 · 07:55:23 | OK | the DM "Date" fields in DEVIATIONS are 6–51 min later than their own commits |

**Verdict on timing.** No result was analysed before its pre-registration. The slips listed above are small, and most are disclosed. The weak spot is the archival tests:
- A freeze 15–90 s before the result, on data already analysed in neighbouring ways, protects the statistic from being changed afterwards.
- It does not protect the choice of contrast or bar from knowledge of the data (for example, gm3c's bars were set with the pairwise ρ and split-half reliabilities already known).

## Numbers found wrong

The arithmetic otherwise reproduces. These are miscounts, mislabels and misstatements:

| file | as stated | correct |
|---|---|---|
| `results/exp4-run-3.md:56` and five other documents | 5 of 32 item-orders pass the manipulation check | 6 (the file's own table) |
| same | accept rate 0% in 15 of 32 | 17 |
| same | "higher anchor gave lower rating in 6" | 5 reliable |
| `gm3b` | "20–34%" (record) and "21–35% of statement pairs" (README) | both are (1 − τ_b)/2, not shares of pairs; the actual share ordered oppositely is 12–25%, against a 1–5% noise baseline |
| `gm3b` | archived L1 fit | under-converged (objective at least 9.5 below optimum); the by-format table depends on the optimiser |
| `bm7` | "2–4 points across the full range" | 4–9 points (the weights are per 50 points) |
| `DEVIATIONS.md:376`, v3:153 and 507 | h018 "hit the token cap" | archived reason: "extractor returned 1 claims" |
| `frame-fix-check` | "20% of run-2 items" | 20% of the 225 items with both camps (44 of 300 = 15%) |
| `stage2-run-2b` | arm F window "1–6" configurations | 1–16 |
| `sonnet-ablation` / Addenda D and E | 2,000 bootstrap resamples | the code used 1,000 (no rule outcome changes) |
| `paper/the-entangled-mind-paper.md:176` | self-report "outperforms every structural analysis" | F2 0.84 and A2.1 0.84 against G 0.83 on the locked test |
| `paper/the-entangled-mind-v3.md:67` | A5 and F5 "do not differ in predicting held-out ratings" | they do: +207 [+52, +388] |
| `results/calibration-under-format.md` | "about 120" True/False questions | 60 |
| `results/api-usage.md` / README:244 | per-question spend ledger for all runs | the ledger stops at pool run 6 |

## Cross-cutting holes

1. **README:21 and morning-brief:5** say each overnight test was frozen "before its data were opened". This is false for D34, D35, D40, D41 and D42, and D35 is not single-scale either.
2. **Double counting.** The overnight synthesis reuses data across tests:
   - bm3 and bm1's "other" arm are the same run-3 archive.
   - bm0 reuses bm1's ±30 cells, and gm2b contains gm2's 10 items.
   - gm3c re-analyses gm3b, and bm9 shares experiment 5's question-order block with gm9.
   - The "three models" self-knowledge claim reuses D36's Sonnet cell.
   - The independent support is about four data collections on one model.
3. **Own vs other is confounded with wording.** It differs in instruction, output schema and turn position, not only in whose number it is. The authors' own caveat says so, but every headline drops it: README:27, brief:24/84, No Credence:344, clonable-minds:133. 42% of own re-ratings repeat the planted number exactly.
4. **A response-direction confound in v1 error prediction.** 36 of 40 wrong test items are "no" answers, against 22 of 40 right ones. A one-bit "model said no" predictor scores AUROC 0.675, level with arms C, D and E (verified by the lead auditor).
5. **The v2 pool enrichment makes item type predictive.** Type alone scores AUROC 0.71 on the locked test, and mean claim confidence 0.77.
6. **The three "positive quantum edges" are one item set.** 21 of Sonnet's 30 errors are in Haiku's held-out wrong set. Outside it, Sonnet's A2 − F2 is −0.018 [−0.125, +0.064].
7. **The mechanism claims in gm1 are largely built into the design.** Every rating, the archived self-report included, is a fresh call that sees only the answer text, so "not privileged access" is not something the test could show. The interaction's negative sign comes from judge knowledge, not authorship.
8. **D48 is two different entries.** It is direction 5 on `probes` (07:39) and the No Credence narrowing on `main` (09:18), so the two will collide on merge. Main's narrowing also turns Opus's undecided 26-claim format arm into "does not hold" / "points the other way".
9. **`reproduce.py` has gaps.**
   - It never checks the hand-written Reading / plain-English prose, where most failures are.
   - It cannot rebuild the multi-model replications or the calibration demonstration, and it skips the Sonnet ablation.
   - It runs the authors' own code.
10. **The record is stale.**
    - Its "Standing" section is dated 05:05 while its rows run to 09:36.
    - It omits DM2–DM6, D48 and direction 5.
    - It says the gold-map full-read corrections came "before the run"; they came after D34's and D35's results.

## Per-result table

Overclaims = sentences listed for cutting. Verdict key: S = STANDS, SC = STANDS WITH CAVEATS, U = UNDETERMINED.

| audit | verdict | overclaims | conf. | most serious hole |
|---|---|---|---|---|
| pool-runs | S | 2 | high | h018's exclusion reason misstated; D4 rules committed after the extension calls |
| stage1-run-1 | S | 1 | high | "decoheres" is a mechanism guess from one circuit; some qubits overshoot 50/50 |
| stage2-run-1 | SC | 5 | high | the one-item "too noisy" rule was applied to H2 only; H3 and H4 flip on one item |
| stage2-run-2 | S | 4 | high | "every control does better" holds for point estimates only (C − A +0.14 [−0.01, +0.29]) |
| stage2-run-2-split | SC | 2 | high | "same pattern" has no significant within-group contrast |
| stage2-run-2b | SC | 10 | high | "G beats every structural arm by a wide margin" is not pre-registered, and fails under Holm against C and D |
| witness-run-1 | S | 9 | high | certifies pairwise entanglement in 3 of 80 states (one a decoupled pair), not "the belief states" |
| frame-fix-check | S | 2 | high | "found after all pre-registered runs" is false; 20% is really 15% |
| v2-run-1 | SC | 12 | high | the coupling-spread argument is wrong (8 of 10 candidates read out near the Z axis); no equivalence margin (the minimum detectable effect is about 0.10) |
| v2.1-run-1 | SC | 1 | high | λ_h = 0 for F2.1 is a scale artefact |
| sonnet-replication | SC | 5 | high | same questions as Haiku's hard pool, so not an independent replication |
| sonnet-ablation | SC | 10 | high | "matches" means only that the interval includes 0; the three edges are one item set |
| exp3-run-1 | SC | 7 | high | "no order effects in yes/no form" is contradicted by experiment 4's yes/no data; the test could not separate the two models |
| exp4-run-1 | S | 2 | high | two of the 7 fallacies drop under correction for 16 tests |
| exp4-run-2 | **U** | 4 | high | the frozen rule could only return "static twin"; README drops that verdict |
| exp4-run-3 | S | 15 | high | three counts wrong in six documents; "reactance" is interpretation |
| exp5-pilot | SC | 0 | high | gate G1 was nearly certain to pass by noise (P ≈ 0.98–1.00 per item) |
| exp5-run-1 | SC | 25 | medium | "tie" rests on the pooled q; single-scale q meets the contradiction condition; h183 drives the primary |
| exp5-run-2 | SC | 2 | high | "run 1's tie is unchanged" is wrong: its "not contradicted" leg used the artefact q |
| gm9-nsit | SC | 10 | high | text-only freeze; N4's underpowered null promoted to "non-invasive"; "macrorealism by construction" filed as a result |
| gm3a-anchor-gap | S | 14 | high | a 40-item null written up as "no error signal"; the gap mostly tracks the verdict direction (ρ = −0.82) |
| gm1-self-knowledge | SC | 20 | high | "text-reading" is built into the design; README wrong for Sonnet (+0.28 [+0.07, +0.51]); recognition check dropped |
| gm4-evidence-seeking | S | 5 | high | EIG's above-chance rate is carried entirely by overlap with confirmatory targets; the record states a null |
| gm2-self-conditioning | SC | 10 | high | "consistency is memory" is not supported (redaction shifts the final rating systematically) |
| gm2b-self-conditioning-40 | SC | 16 | high | shown and redacted order patterns correlate only 0.32; "question carries all" is wrong; 30-item replication fragile |
| gm3b-format-invariance | S | 11 | high | the "% of pairs" figures are mislabelled τ; under-converged L1; mechanism wording |
| gm3c-heldout-format | **U** | 10 | medium | "little" vs "partial" is decided by 0.0012 and flips on refit; the Smolin & Wilder comparison is not like-for-like |
| bm3-confirmation | S | 3 | high | the headline secondary (−0.29) is 1 of 15 coefficients and driven by one item-order |
| bm7-serial-position | S | 3 | high | "2–4 points" is off by a factor of 2 |
| bm9-contrast | SC | 7 | medium | β > 0 mostly reflects M-first regression; the S-level coefficient alone includes 0 |
| bm2-sampling-identity | SC | 6 | high | the 18-second "corrected reading" is wrong; "cancel" overclaims an undetermined equivalence |
| bm1-serial-dependence | SC | 9 | high | own vs other differs in four ways at once; "binds itself" is causal |
| bm0-source-distance-lag | SC | 15 | high | "no decay" is forbidden by its own pre-registration (line 77); "grows" rests on a CI bound of −0.00002 |
| mm-gm3b-format-invariance | SC | 11 | high | Sonnet's label is one claim; Opus's fit is degenerate |
| mm-gm1-self-knowledge | SC | 5 | high | the disagreement subset has 4 Opus errors; "holds on all three" is a non-detection |
| mm-gm2-self-conditioning | SC | 2 | high | Opus's label is one item deep |
| multi-model | SC | 7 | high | D48's narrowing overclaims Opus; "Opus barely shows an order effect" contradicts its gate (p = 0.004) |
| calibration-under-format | SC | 6 | high | format-dependent exclusions never mentioned; the sign on jointly parsed questions is undetermined |
| probe-dissociation | SC | 15 | medium | step 3 replays the gate (500 of 500 identical); Q > 1 is a scaling artefact (about 0.6–0.7 on true–false gaps) |
| *record-accuracy* (cross-cutting) | SC | 10 | high | archival tests called "frozen before opened"; stale Standing section |
| *synthesis-claims* (cross-cutting) | SC | 43 | medium | double counting; one model; "every pre-registered test failed or tied" ignores secondary wins |

## What the main session should cut first

1. Every "no decay", "no error signal", "not invasive", "does not prefer", "holds on all three models", "matches"/"equals" that rests on an interval including 0. Replace each with the interval, or "not detected".
2. The mechanism words: "text-reading", "memory", "binds itself", "commitments", "reactance", "contrast", "macrorealism holds" (as a result), "constructed by the asking" (as a finding rather than a reading).
3. README:21 ("before its data were opened"), README:12 ("every pre-registered test failed or tied"), README:27, README:29, and the stale R = 1.91 and "six separate credences" in the overnight section.
4. The miscounts in the "Numbers found wrong" table above.
5. Experiment 5's "tie" should read "tie on the pooled pre-registered analysis; the single-scale data meet the contradiction condition, so tie versus classical is unsettled". It should no longer be described as the outcome the pre-registration predicted.
6. Renumber one of the two D48s before merging `probes`.

## How this audit was done, and its limits

- **How the work was split.**
  - Ten auditors worked in parallel, each with a written brief.
  - The lead auditor did the timing analysis, ran `reproduce.py`, and wrote this summary.
  - The lead auditor independently re-verified every claim with the power to change a verdict or a headline, or to embarrass a published sentence:
    - the 500-of-500 probe replay;
    - the experiment 4 run 3 counts (6 and 17);
    - experiment 5's anchor-(a) q;
    - the bm0 "no decay" rule;
    - G 0.83 against F2 0.84;
    - the h018 exclusion reason;
    - gm3c's 0.4988;
    - the yes/no confound (AUROC 0.675);
    - the message-ID time decoding;
    - all 320 quoted sentences.
- **What was not recomputed:**
  - no model was re-run, and no local LM was re-run, so the probe projections are taken as archived;
  - experiment 5's BA5 and A5⁰ sign agreement;
  - the timing of local runs.
- **Where per-audit counts are subjective.** "Claims checked" counts are each auditor's own granularity, so the 30% failure rate is indicative, not exact. The 97% result-level overclaim rate and the reversal counts do not depend on that granularity.
- **Recomputation scripts** are in the session scratchpad (`g1/`–`g10/`), not in the repository. The request-ID decoder behind every timing claim is committed as `audits/tools/ridtime.py` (`python audits/tools/ridtime.py results/*.json`).

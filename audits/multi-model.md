# Audit: multi-model

**Files audited:** `results/multi-model.md` (summary), `results/mm-pilot-calls.json`, `results/mm-gm2-opus-cap.json`, all `results/mm-*` call archives (for spend), DEVIATIONS DM1, DM2a, DM4a, DM5, D48 (`2ae4d19`, 09:18:13), the D48 diff to `paper/no-credence-to-read.md`, and `paper/morning-brief.md` (section "How far it generalises"). The per-test recomputations are in `audits/mm-gm3b-format-invariance.md`, `audits/mm-gm1-self-knowledge.md` and `audits/mm-gm2-self-conditioning.md`; this file checks the summary's prose and the D48 narrowing against them.
**Pre-registration:** DM1 set-up and pilot committed with DM2 in `86e7c56` (07:44:03). DM3 `207c9b6` (07:47:58), DM4 `dea966b` (07:48:27), amendment DM4a `a9e1e7b` (07:49:52), amendment DM2a `e65a384` (07:59:51). First calls, decoded from request and message IDs:
- pilot sync calls 07:33:17–07:33:38;
- pilot batch 07:36:48–52;
- DM2 07:45:58;
- DM3 07:49:06;
- DM4 Sonnet 07:50:47;
- DM4 Opus 08:26:43.

`msg_01…` IDs carry the same millisecond timestamp layout as `req_01…` IDs. Decoder: `scratchpad/g8/msgtime.py`, `msgtime2.py`. Summary `a863d66` (08:45:04); merge `22bdcef` (09:16:27); D48 `2ae4d19` (09:18:13). Between pre-registration and results, the multi-model branch carries only DM4a (Opus cap code), the DM4a analysis restriction in `mm_gm3b.py` (inside `f406a9c`, 07:53:12) and DM2a (chunk size). No imported analysis module changed.
Timing verdict: **OK by git and message IDs.** There is a documentation PROBLEM: every DM entry's self-stated "Date" is later than its commit, by 6–51 minutes. DM1 says 07:45 (commit 07:44:03), DM2 07:50, DM3 08:05, DM4 08:10, DM4a 08:20, DM6 08:35 and DM2a 08:50. Read at face value, DM3, DM4, DM4a and DM6's "before any call" statements would be false, because their calls had already started or finished by the stated times.

## Plain-English summary of the audit
The summary's numbers are all correct: every table entry and spend figure reproduces from the archives. Its plain-English section, and the D48 narrowing of the paper, mostly state honestly what replicated, but three statements outrun the evidence.
- **Opus's format result is presented as a positive finding.** The summary says one credence "does as well as" six there, and that "the evidence points the other way". The pre-registered reading on its 26 claims is *mixed*, the fit behind it is degenerate, and the label is one claim away from flipping. That arm is undecided.
- **Opus's order effect is misdescribed.** "Opus barely shows an order effect at all" contradicts its own gate (p = 0.004).
- **Non-detections are written as findings.** "No privileged self-knowledge holds on all three models" turns a non-detection into a positive claim; the confirmatory subset had 4 Opus errors.

D48's own text says the paper calls the format claim "not supported" on Opus, "not refuted", yet the paper it edited says "does not hold on Opus" twice.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | "Every test used the same design and the same pre-registered criteria as the Haiku original…" (`results/multi-model.md:8`) | The criteria are the same; the designs are not. R is 4 (Opus 2) rather than 10, F has 80/26 claims rather than 160, F′ uses 3 folds rather than 5, P dropped its paraphrase and recognition arms, max_tokens is 1,000 rather than 100/200, and Opus's thinking is not off | overclaim |
| 2 | "…each was pre-registered in its own commit before its first call. No call was refused." (`:8`) | Verified by decoded message IDs (see the pre-registration line); 0 refusals in every archive | holds |
| 3 | Self-knowledge bullets (`:12–17`) | Recomputed (`audits/mm-gm1-self-knowledge.md`). Numbers hold; "still not privileged" is a non-detection | holds (minor) |
| 4 | "Sonnet's order effect survives hiding … 2.95 [0.99, 12.55] … much of it comes from 2 of the 10 items … (h191)" (`:20`) | Holds; h191 42.4, h112 30.0 | holds |
| 5 | "Opus barely shows an order effect at all: 4.4 points, against Sonnet's 6.1 and Haiku's 9.3." (`:21`) | Opus gate p = 0.004 (stronger than Sonnet's 0.031); the OE CIs overlap | overclaim |
| 6 | "…its ratio of 0.93 has an interval from 0.06 to 7.3. It is read as *leaning question-driven, not decisive*." (`:22`) | Holds. Omitted: without h058, R = 0.14 [0.00, 0.46], the *self-anchoring* side | holds (minor) |
| 7 | MF agreement 78/88/95% → 25/35/65%; "partly memory in every model. Opus is the most stable without it" (`:24–27`) | Reproduced; the drop's CIs exclude 0 on all three | holds |
| 8 | "The 'no format-free credence' finding weakens sharply as the model gets stronger." (`:29`) | On the primary statistic Sonnet has *more* claims positive than Haiku (92% vs 86%), and its CI crosses 0 because of one claim; without it, +13.2 [+9.8, +17.0]. The weakening shows in F′ (0.29 → 0.69) and in W | overclaim (moderate) |
| 9 | Sonnet bullets (`:31–32`): 92%, one extreme statement, Q 0.69 [0.53, 0.82], Haiku 0.29 | Reproduced independently | holds |
| 10 | "On those, one credence per statement does as well as one per format (ΔLL +0.42 [−1.83, +2.69]), and its formats agree closely (Kendall's W 0.86, against 0.71 for Sonnet and 0.54 for Haiku)." (`:33`) | The pre-registered reading is *mixed*; L1 slopes diverged (b_F4 ≈ 2–5.6 × 10⁴); ΔLL is 0.16–0.42 depending on the optimiser; 14–16/26 positive against the 13/26 line. W reproduces | overclaim |
| 11 | "So the stronger the model, the more its different ways of answering look like readings of one belief. That matches Smolin & Wilder's (2026) finding…" (`:34`) | Three models, one on a partial arm. Item-matched W (exploratory) 0.50 / 0.76 / 0.84 supports a trend in rank agreement, but the belief test is *mixed* on both stronger models | overclaim (moderate) |
| 12 | "Its claim about self-report (Section 4.4) holds on all three models." (`:37`) | Non-detection; see `audits/mm-gm1-self-knowledge.md` | holds (minor) |
| 13 | "Its claim that the record conditions later answers (Section 4.2's memory result) holds on all three." (`:38`) | The memory criterion holds; the planted-value pull is null on Sonnet, and Opus's final M moves away from the plant | holds (minor) |
| 14 | "Its claim that the question alone constructs the judgment holds on Sonnet. On Opus it is untested at useful power." (`:39`) | Holds by the rule (2-item concentration) | holds (minor) |
| 15 | "…On Opus, the evidence available points the other way." (`:40`) | See claim 10; the pre-registered reading is *mixed* | overclaim |
| 16 | Budget table and the $16.28 total; Opus cap $8.51 | $0.030 + 2.045 + 3.099 + 4.030 + 2.189 + 4.889 = $16.28; cap file $20 − $11.393 − $0.10 = $8.5069 | holds |
| 17 | "The full designs would have cost about $65 at list price, so each was scaled down without changing its structure (DM1)" (`:44`) | DM3 dropped two arms, and F′'s fold structure changed (3 folds) | overclaim (minor; same as claim 1) |
| 18 | DM1 pilot: 12 sync calls plus a 2-request batch, $0.031, on h002 (not a DM2 or DM4 item); Opus ≈ $0.0016 single-turn; thinking in later turns | 12 sync records plus the batch; $0.0301; h002 is not in `split-exp5` candidates; Opus later-turn outputs of 71 and 58 tokens against 9–11 | holds |
| 19 | DM4a: Opus ≈ 120 thinking tokens per call ($3.10 for 1,600) | $0.00194 per call at batch rate. With about 330 input tokens, that implies about 128 output tokens, against about 9 visible | holds |
| 20 | DM5: after wave 1, projection $8.74 at R = 3 > $8.51; R = 3 would have fitted | My reconstruction: about $8.68 projected; about $6.5 actual at R = 3 | holds |
| 21 | D48: "No new data or analysis. Every number is copied from …" (DEVIATIONS D48) | Every number in the D48 diff matches the result files | holds |
| 22 | D48: "the paper says the claim is 'not supported' on Opus, not that it is refuted" | The paper says "does not hold on Opus" (`no-credence-to-read.md:58`, `:407`) and "the evidence that exists points the other way" (`:325`) | wrong (D48 misdescribes its own edit) |

## Holes found
1. **D48's narrowing is inconsistent with itself on Opus.** D48 states that Opus's reading is *mixed* and that the paper therefore says "not supported", "not refuted". The edited paper nonetheless says the format finding "does not hold on Opus" (lines 58 and 407), that "one credence per statement fits as well as one per format" (lines 29, 325, 350), and that "the evidence that exists points the other way" (line 325). The Opus arm is budget-stopped at 26 non-random claims, near-deterministic, with a degenerate L1 fit, and one claim from the opposite pre-registered label (`audits/mm-gm3b-format-invariance.md`, hole 2). "Narrowed to what replicated" should have narrowed the Opus row to "untested / undecided".
2. **The non-detections are written as replications.** "No privileged self-knowledge holds on all three models" and "Self-report is still not privileged" are each a non-detection in a pairwise test. The confirmatory disagreement subset in the Sonnet × Opus pair had 4 Opus errors (CI [−0.30, +0.81], point estimate +0.18). The all-question bound (+0.017) is informative, but it is the confounded statistic.
3. **Opus's order effect is mis-summarised.** "Opus barely shows an order effect at all" contradicts gate p = 0.004. And "leaning question-driven" is carried by one item: without h058 the rule reads *self-anchoring*. The summary reports the h058 concentration in its Notes but not its consequence.
4. **"Weakens sharply" does not match the primary statistic.** Sonnet's share of claims favouring six credences (92%) is higher than Haiku's (86%), and its mean drops below Haiku's partly because of one −308 claim. The evidence for weakening is F′ and W, which the summary does give. The heading still overstates what the pre-registered test shows.
5. **The DEVIATIONS time stamps are fabricated or estimated.** Every DM "Date" is later than its own commit (see the timing verdict). The ordering is rescued by git and by the message-ID timestamps, which the authors did not use. The brief's assumption that batch timing is unrecoverable is wrong for these archives.
6. **"Same design" is not accurate.** The scaled designs changed power substantially, from R = 10 to 4 or 2 and from 160 claims to 80 or 26. Fold counts changed (F′ 3 folds) and arms were dropped (P paraphrase and recognition). The summary's Budget section lists these, but line 8's "same design" contradicts it.

## Overclaims to cut (exact sentences)
- `results/multi-model.md:8` — "Every test used the same design and the same pre-registered criteria as the Haiku original, one scale direction and stop-on-refusal, and each was pre-registered in its own commit before its first call." — Why: the designs were scaled and arms were dropped. — Replace: "Every test used the Haiku original's prompts, analysis code and pre-registered criteria, at reduced scale (see Budget), with one scale direction and stop-on-refusal, and each was pre-registered in its own commit before its first call."
- `results/multi-model.md:21` — "- Opus barely shows an order effect at all: 4.4 points, against Sonnet's 6.1 and Haiku's 9.3." — Why: the gate is p = 0.004 and the intervals overlap. — Replace: "- Opus shows a smaller order effect (4.4 points [0.8, 6.9], gate p = 0.004), against Sonnet's 6.1 and Haiku's 9.3; with the record hidden it comes from one item (h058)."
- `results/multi-model.md:29` — "**The "no format-free credence" finding weakens sharply as the model gets stronger.**" — Why: the primary statistic does not show a sharp weakening on Sonnet (92% of claims positive; *mixed* from one claim). — Replace: "**On Sonnet, one credence is partly usable (F′); on Opus the test is undecided.**"
- `results/multi-model.md:33` — "- Opus's run was stopped by its budget after 26 statements. On those, one credence per statement does as well as one per format (ΔLL +0.42 [−1.83, +2.69]), and its formats agree closely (Kendall's W 0.86, against 0.71 for Sonnet and 0.54 for Haiku)." — Why: *mixed*, a degenerate fit, and a knife-edge share. — Replace: "- Opus's run was stopped by its budget after 26 statements. On those, the test is undecided (ΔLL +0.42 [−1.83, +2.69], *mixed*), though its formats rank the statements closely alike (Kendall's W 0.86, against 0.71 for Sonnet and 0.54 for Haiku)."
- `results/multi-model.md:34` — "- So the stronger the model, the more its different ways of answering look like readings of one belief." — Why: a three-model trend in rank agreement; the belief test is *mixed* on both stronger models. — Replace: "- Across these three models, the formats agree more for the stronger models (W; and F′ on Sonnet against Haiku)."
- `results/multi-model.md:40` — "On Opus, the evidence available points the other way." — Why: the pre-registered reading is *mixed*. — Replace: "On Opus, the test is undecided on the 26 claims run."
- `results/multi-model.md:12` — "**Self-report is still not privileged.** This is the finding that travels best." — Why: this is a non-detection, and the confirmatory subset had 4 Opus errors. — Replace: "**No self-advantage was detected on the Sonnet × Opus pair either.**"

(The paper and brief sentences repeating these claims are listed in `audits/mm-gm3b-format-invariance.md`, `audits/mm-gm1-self-knowledge.md` and `audits/mm-gm2-self-conditioning.md`.)

## Does the verdict stand?
DM5 and D48's readings:
- self-knowledge: *no self-advantage*;
- transcripts: Sonnet *question-driven*, Opus *leaning*;
- six formats: Sonnet *mixed*, Opus *mixed*.

**STANDS WITH CAVEATS.** Every number and every pre-registered label reproduces. Three things fail in the prose and in D48's edits to the paper:
- the Opus format row is converted from "undecided" into "does not hold" or "fits as well";
- non-detections are converted into "holds on all three";
- Opus's order effect is described as nearly absent despite p = 0.004.

## Confidence
**High.** All the underlying statistics were recomputed independently in the three companion audits, the spend was summed from the archives, and the timing was verified with decoded message IDs.

## Tally
claims_checked: 22
claims_failed: 8
overclaim_sentences: 7
verdict: STANDS WITH CAVEATS
confidence: high

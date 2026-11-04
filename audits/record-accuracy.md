# Audit: record-accuracy

**Files audited:** `paper/record.md` (all 82 lines); the commit, time, pre-registration, cost and refusal claims in `README.md` and `paper/morning-brief.md`; cross-checked against `git log --all`, `scratchpad/gitlog.txt`, decoded request-ID times (`scratchpad/first_calls.txt`, `ridtime.py -k`), `DEVIATIONS.md`, `results/api-usage.md` and the headline tables of every `results/*.md` the record cites.
**Pre-registration:** not applicable (this audits the record of all pre-registrations). Every pre-registration the record names was checked against git and, where request IDs exist, against the first call. Scratch script: `scratchpad/g10/hashes.py`.
Timing verdict: PROBLEM. Every hash exists and every time is correctly transcribed, but the record leaves out six timing problems, two statements in it are false, and the "standing" summary is four and a half hours out of date.

## Plain-English summary of the audit
As a ledger of hashes and times, the record is accurate. All 92 commit citations resolve, every one is on `main`, and every quoted time matches git to the minute. Every result number I checked against its results table matches. The record goes wrong in what it says about order and in what it leaves out.
- "Before the run" is false for the gold-map full-read corrections: they were committed after the first two overnight results.
- Five of the eleven overnight tests (45%) reanalyse data the authors had already opened. Yet README and the morning brief say each was frozen "before its data were opened".
- README and the brief say every overnight design used one scale direction. Direction 3's free look (D35) is by definition the gap between two directions, and `DEVIATIONS.md` D35 says so.
- The record never says that several "pre-registered" items were committed after their calls had begun: experiment 3's choices, experiment 5's models and analysis, the Addendum D code, and the direction 1 runner.
- The "Standing" section is dated 05:05 while the table runs to 09:36. It ignores the biomimetic tests, the robustness wave, the merged Sonnet/Opus replications (DM1–DM6) and D48.
- The `probes` branch reuses the label D48 for a different entry. Its pre-registration (07:39) is earlier than main's D48 (09:18).

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Every backticked hash in record.md is a short id on `main` with the time shown (record.md:4–5, all rows) | 92 citations, 76 distinct hashes: all resolve, all reachable from `main`, every quoted hh:mm matches `git show -s --date=format` (script output in scratchpad/g10) | holds |
| 2 | Row times equal the result commit's time (record.md:23–57) | All 30 row times match the cited result commit (e.g. 14:17 = 2248e54 14:17:24; 09:36 = e2c3b90 09:36:15) | holds |
| 3 | Proposal dated 2026-10-25, added as PDFs in `f09175d` (11-03 16:53) (record.md:8) | f09175d = 11-03 16:53:20 ✓; the 10-25 date has no git or file evidence | holds (minor); date not checkable |
| 4 | Pre-registration `afe1c1b` 12:54 and redesign `f37e4a8` 12:55 precede pool run 1 (record.md:10–17, 23) | first call 12:56:06, 9 s after f37e4a8 | holds |
| 5 | Stage 2 run 2 pre-registered in afe1c1b; hard pool D6 `f5649da` 14:35 (record.md:24–25) | pool-run-3 first call 14:35:39, 1 s after f5649da | holds |
| 6 | Run 2b (arms F, G, shuffle null) "pre-registered `dd81f4f` (15:15)" (record.md:32) | dd81f4f 15:15:39 is **49 s after** run 2's failing result 3204d10 (15:14:50). Arm G calls 15:15:52–15:17:29 come after it | holds (minor): true before arm G's calls, but the record does not say that Addendum A was written after H2 had failed |
| 7 | Witness design `f5f306b` (15:39) before witness result 655a8f8 (16:08) (record.md:27) | ✓ by git; no request-ID timing for IBM jobs | holds |
| 8 | Experiment 3: "`de9c536` (15:39); choices `958d9db` (D13)" listed as pre-registered (record.md:29) | exp3 first call **17:23:04**; 958d9db 17:23:10 is **6 s after** it | overclaim (timing omitted) |
| 9 | Experiment 4: `54cfa1f` 16:52, R2 corrected `3fe936e` 17:04 (record.md:30) | exp4 first call 18:10:21 | holds |
| 10 | v2: split `a142d10`, models `8a4faa2` (17:20) (record.md:31) | v2 arm-G first call 18:46:23 ✓. But the training pool (pool run 5) began **16:02:45**, 23 min before the D9 pool commit 930730c (16:26:03) | holds (minor) |
| 11 | v2.1: `775042f` 17:45, `fe3c411` 18:36 before a531b36 19:32 (record.md:33) | ✓ | holds |
| 12 | Exp 4 run 2: `cb4e96e` 19:05 (record.md:34) | first call 19:34:11 | holds |
| 13 | Sonnet replication set up `c98bdf7` 19:07 (record.md:35) | pool-run-4 first call 19:37:08 ✓; $4.07 = api-usage run 4 $4.0667 ✓; 82 training items = pool-run-6 n = 82 ✓ | holds |
| 14 | Exp 5: frozen `2c2ef6c` 20:15, D23 `2ad710c`, D24 `97dde55` before the pilot (record.md:36) | pilot first call 20:18:49, 12 s after 97dde55 | holds |
| 15 | "models `2251693` and analysis `1155dde` (D26) committed before any full-run result" (record.md:36) | Full-run calls began **20:30:12** (h190 group), before 2251693 (20:32:21) and 1155dde (20:34:48) | overclaim: literally true for *results*, but the full run's calls were already under way |
| 16 | Addendum D and Sonnet arm G "pre-registered" `f7afd8a` (21:03, D28) (record.md:38) | Sonnet arm-G first call 21:03:26, 18 s after f7afd8a, but the code that made those calls (69722c7) is 21:04:16, **50 s after the calls began**. Addendum D was designed after the +0.078 edge (b584386, 20:58) | overclaim (timing omitted) |
| 17 | Addendum E `52e80a0` (21:49, D30) before a9ab42c (record.md:39) | 73 s gap; the run-2 held-out set had already been scored by A2 and A2.1 | holds (archival; disclosed as "no API calls") |
| 18 | Exp 5 run 2 and exp 4 run 3 frozen in `fbc2fbf` 23:00 (record.md:41–42) | first calls 23:01:44 and 23:01:01; runners acd1d9c 23:00:58 and 37ce49b 23:01:41, each committed seconds before its first call | holds |
| 19 | "Before the run, the gold map's abstract-only citations for directions 1–4 were read in full and corrected (`01b1ce9`...)" (record.md:44) | 01b1ce9 = **03:53:38**: after D34's result (03:49:46), D35's result (03:51:18) and D36's pre-registration (03:52:51). Before direction 1's first call (03:54:55) only | wrong |
| 20 | Overnight: "Each is pre-registered in its own commit before its first call or analysis" (record.md:44) | All six pre-registration commits come before their first call or result commit. But direction 1's runner `gm1_self_knowledge.py` first enters git at 954b4da **03:58:25**, after its first call (03:54:55) | holds (minor) |
| 21 | D34 `7f0dd3e` 03:48 → 39a1a66 03:49 (record.md:48) | 89 s; archival; analysis code `gm9_nsit.py` first committed *with the result*, so the pre-registration froze text only | holds (archival, code not frozen) |
| 22 | D35 `a1bc421` 03:50 → 43592e5 03:51 (record.md:49) | 47 s; archival; `gm3a_anchor_gap.py` first committed with the result; the 33.8 vs 71.3 gap it tests was already reported in the exp 5 result (22:24) | holds (archival, code not frozen) |
| 23 | D36 `28a20b2` (03:52; amended 03:58 and 04:07) (record.md:50) | Both amendments (954b4da 03:58:25, 2e2ab39 04:07:05) fall inside the call window 03:54:55–04:07:56; the runner itself was first committed in the first amendment | overclaim (the record gives the times but not that they are mid-run) |
| 24 | D37 `9e23b6f` 03:58, D38 `34eb191` 04:02, D39 `e913227` 04:05 (record.md:51–53) | first calls 04:15:33, 04:41:04, 05:02:12; each runner is in its pre-registration commit | holds |
| 25 | "D40–D44, each in its own commit before its data" (record.md:54) | D40→result 16 s, D41 16 s, D42 15 s, all on archives already analysed (run 3 at 23:17, exp 5 at 22:24). bm7 and bm9's analysis code was committed in D40's commit (05:08:07), **before** the D41 and D42 texts. D43 and D44 are new calls, 3 s after their commits. bm2's reading was rewritten 18 s after its result (605fa97, "corrected reading") | overclaim for D40–D42 ("before its data") |
| 26 | D46 `1f2a837` (06:33) → 52aedb6 06:35; D45 `4894bfc` (06:30); D47 `8acc007` (06:37) (record.md:55–57) | D46 111 s, archival (D38's calls, opened 05:02), code frozen with it ✓; gm2b first call 06:30:19 (5 s after) ✓; bm0 first call 09:16:17 ✓ | holds |
| 27 | Result numbers, Nov 3 rows (record.md:23–42) | Spot-checked against tables: 0 of 117; 0.86/0.45/0.51; 0.55/0.68/0.65/0.64/0.49; 0.50 vs 0.25; N 0.147/0.063/0.067, 44 s; 20%/30°; [−0.284, +0.060], 85%, 27/218, $1.63; 7/16, 5,480, $0.23; 0.83/0.84, k 0.12/0.21; G 0.82 [0.71, 0.90]; 0.84/0.82; 1,120, $0.04; 30 of 298; pilot 1,400, $0.21, 5/5, 10/10; A2 0.90 F2 0.82 L 0.73 H 0.66, +0.078 [+0.018, +0.137]; −0.006, +0.004, +0.082, G 0.91 (+0.008), $0.88; 0.80, −0.019, −0.037, +0.088; F5 − A5 +67.0 [−34.1, +211.5], 60/80, q +0.005 [−0.058, +0.065], Δ_K +0.29 [−1.12, +1.65], 12/160, 33.8/71.3, 12,600, $1.93; q −0.146 [−0.439, +0.137], +0.031, KS 0.008, 12/16, 1,700, $0.14; 6,720, $0.30, 15 of 32 | holds (all present in the cited tables) |
| 28 | Result numbers, Nov 4 rows (record.md:48–57) | All match: 5/6, Holm 0.0012, 12.4 vs 2.6, p 0.16; 0.48 [0.28, 0.66], 0.75; −0.055 [−0.103, −0.007], 0.93/0.85, −0.14 [−0.50, +0.23], 0.51, 1,710, $2.82, $3.02; R 1.91 [0.92, 4.90], b_MF 1.27 [0.70, 2.14], 81/23%; 86%, +19.4 [+16.5, +22.1], W 0.56, 20–34%, 9,600, $0.41; +0.14/+0.21/+0.21/−0.13, −0.24 [−0.52, +0.04], −0.14 [−0.40, +0.14], 1,200, $0.11; s_own 0.42/0.05, β 0.27; Q 0.39 [0.30, 0.50], 0.37, 0.88–0.97; R 1.23 [0.75, 2.02], 0.99 [0.51, 1.61], 0.99 [0.62, 1.49], 82%, 5.1/5.4, 0.85 [0.65, 1.13], 86/36%, 6,000, $1.68; +0.46 [+0.21, +0.84], +0.52/+0.55/+0.33, 0.71/0.44/0.21, 0.57 vs 0.44, +0.02, 3,650/3,840, $0.50 | holds |
| 29 | "Standing at the end of the record (`bc9e70d`, 2026-11-04 05:05)" (record.md:69) | Table rows run to 09:36 (e2c3b90). The standing bullets leave out D40–D47, DM1–DM6 (merged 22bdcef 09:16) and D48. "There is no single credence across formats" is not qualified by the later Opus/Sonnet narrowing | wrong (stale) |
| 30 | "This is a chronological record of each question the project tested" (record.md:3) | Omits four pre-registered tests merged into main: DM2 (86e7c56), DM3 (207c9b6), DM4 (dea966b), DM6 (f406a9c). Also omits D48 (2ae4d19), and direction 5 on `probes` (9ef909d 07:39, result 8685008 09:18) | wrong (incomplete) |
| 31 | Decision labels are from DEVIATIONS.md (record.md:6) | `probes:DEVIATIONS.md:700` defines D48 as "Gold map direction 5 ... pre-registered" (07:39). `main:DEVIATIONS.md:866` defines D48 as "The No Credence paper's claims narrowed" (09:18). The morning brief (lines 119, 198) uses main's meaning | wrong (label collision on merge) |
| 32 | README:21: "Eleven pre-registered tests ... each frozen in its own commit before its data were opened or its first call" | 5 of 11 (D34, D35, D40, D41, D42) reanalyse archives the authors had already opened and analysed. Their pre-registration-to-result gaps are 89, 47, 16, 16 and 15 s. D44's comparison arm (s_other) is also archival run-3 data. Counting the robustness wave, 6 of 14 are archival (D46 too) | wrong |
| 33 | README:21: "All used one scale direction" | D35 (gm3a) *is* the gap between the two directions; DEVIATIONS D35: "the only overnight analysis that uses both scale directions" | wrong |
| 34 | README:21: "about $4.2 in all, with no refusals" | Sum of archived `cost_usd`: 2.8153 + 0.5468 + 0.4084 + 0.1109 + 0.0459 + 0.2422 = **$4.1695**, plus at most $0.20 lost in the D36 crash, so ≤ $4.37. Every results file says "no refusal"; the call archives store no stop_reason, so this rests on the runners' stop-on-refusal rule | holds |
| 35 | README:244: "Anthropic API spend per question is in `results/api-usage.md`" | api-usage.md stops at pool run 6 ("Session total: $21.36"). It has none of exp 3–5, arm G, Sonnet G, the overnight $4.17, robustness $2.18 or multi-model $16.28 | wrong (ledger incomplete) |
| 36 | README:187: controls "are fixed before results exist, so a quantum encoding cannot win against a strawman" | Arms F and G were fixed in dd81f4f, 49 s after run 2's result | wrong for F and G |
| 37 | README:221: "D7–D18 ... All were pre-registered or logged before the data they affect" | D9 logged 23 min after pool-run-5 calls began; D13 logged 6 s after exp 3's first call; D7 after run 2's result | overclaim (minor) |
| 38 | morning-brief:5: "each was pre-registered in its own commit before its archive was opened or its first call. Every design used one scale direction" | Same as #32 and #33 | wrong |
| 39 | morning-brief:7: "recorded $4.17, plus at most $0.20 lost" | $4.1695 ✓ | holds |
| 40 | morning-brief:8: robustness "$2.18, no refusal"; multi-model "$16.28" | 1.6827 + 0 + 0.5019 = $2.1846 ✓; multi-model.md total $16.28 ✓ | holds |
| 41 | morning-brief technical table hashes and D labels (lines 173–186) | All ten cited hashes match their D entries and times ✓. Rows 8–11 cite no hash | holds |

## Holes found
1. **"Before its data were opened" is false for 5 of the 11 overnight tests, and for 2 of them the pre-registration froze no code.**
   - **Which tests.** D34 (NSIT on exp 5), D35 (gap on exp 5 B0), D40 (run 3), D41 (exp 5 O-chains) and D42 (exp 5 QQ block) all reanalyse archives the authors had already opened. Exp 5 was analysed at 22:24 on Nov 3, and its 33.8 vs 71.3 scale-direction gap, D35's subject, was already reported then. Run 3 was analysed at 23:17.
   - **Gaps.** Pre-registration to result: 89, 47, 16, 16 and 15 s.
   - **Code.** For D34 and D35, the analysis script was first committed together with the result, so the frozen object was prose only. For D41 and D42, the analysis code (`bm_offline.py`) was committed in D40's commit at 05:08:07, before their own pre-registration texts (05:08:33, 05:08:50). The code even prints "committed before the archive was opened" for registrations that did not yet exist.
   - **What this means.** These analyses were written, then committed in a staged sequence. The pre-registration can guard against changing the statistic after seeing *that specific* output. It cannot guard against designs chosen with knowledge of the data.
   - **Where the claim appears.** README:21 and morning-brief:5 state "before its data were opened" without exception. `paper/no-credence-to-read.md` §6 does name the archival analyses (N, A, free look), but it leaves out F′ and test S's comparison arm.
2. **The one-scale claim is false for D35.** README:21 and morning-brief:5 say every overnight design used one scale direction. D35's statistic is the gap between the two directions, and `DEVIATIONS.md:489` says so.
3. **The record omits timing problems it could see.**
   - **Experiment 3.** D13's implementation choices were committed 6 s after the first call.
   - **Experiment 5.** The models and analysis (D26) were committed 2 and 4.5 min after the full run's first call (20:30:12).
   - **Addendum D.** Its Sonnet arm-G code (69722c7, 21:04:16) was committed after the calls began (21:03:26).
   - **Direction 1.** Its runner was first committed at 03:58:25, after its first call (03:54:55). Both D36 amendments fall inside the call window.
   - **Addendum A** was written 49 s after H2 failed.
   - **What the record says instead.** It lists all of these under "pre-registered" with no qualifier. For experiment 5 it says the models were committed "before any full-run result", which is true of results and silent about calls.
4. **"Before the run" is wrong (record.md:44).** The full-read corrections (01b1ce9, 03:53:38) came after directions 9 and 3a had produced results. The same commit revised the gold map's stated probabilities ("P revised (1: 0.30->0.15 ..."), before direction 1's first call, so the "against the stated probabilities" scoring (89d5b4b) uses priors revised mid-run.
5. **The "Standing" section is stale and dated wrong (record.md:69–82).**
   - **Dating.** It is anchored at bc9e70d (05:05), but the table and the file run to e2c3b90 (09:36).
   - **What is missing.** The biomimetic findings, the robustness wave, the multi-model replications (Opus formats "read as one", the Sonnet F′ partial) and D48's narrowing.
   - **What is overstated.** "There is no single credence across formats" is stated without the Haiku-only scope that D48 imposed on the paper.
6. **The record is not the complete record it claims to be.**
   - **Not on main.** Direction 5 (probes branch) is unmerged, and the record says hashes are on `main`, so leaving it out is defensible if stated.
   - **Merged but missing.** DM2, DM3, DM4 and DM6 (pre-registered tests, merged at 22bdcef, 09:16) and D48 are on main but absent.
   - **Label collision.** D48 names two different entries on the two branches; the probes entry is 1 h 39 min earlier. Merging `probes` will make "D48" ambiguous in every document that cites it (morning-brief:119, :198; no-credence-to-read:9).
7. **The cost ledger is incomplete.** `results/api-usage.md` covers pool runs 1–6 only ($21.36). Every other run's cost exists only in its own results file, so no single file gives project spend. README:244 says otherwise.
8. **"No refusals" cannot be confirmed from the archives.** The overnight call JSONs store values, costs and request IDs, but no `stop_reason`. The claim rests on the runners' stop-on-refusal logic and on every run completing.

## Overclaims to cut (exact sentences)
- `paper/record.md:44` — "Before the run, the gold map's abstract-only citations for directions 1–4 were read in full and corrected (`01b1ce9`, on `related-work`)." — 01b1ce9 (03:53:38) is after the first two results. — "After directions 9 and 3a had run, and before direction 1's first call, the gold map's abstract-only citations for directions 1–4 were read in full and corrected, and their stated probabilities revised (`01b1ce9`, 03:53, on `related-work`)."
- `paper/record.md:54` — "D40–D44, each in its own commit before its data" — D40–D42 reuse archives already analysed (gaps 15–16 s). — "D40–D44, each in its own commit before its analysis or first call; D40–D42 reanalyse run-3 and experiment-5 archives already opened in earlier analyses"
- `paper/record.md:69` — "**Standing at the end of the record (`bc9e70d`, 2026-11-04 05:05).**" — the table runs to 09:36, and the standing ignores D40–D48 and DM1–DM6. — "**Standing at the end of the record (`e2c3b90`, 2026-11-04 09:36).**", with the bullets brought up to date (biomimetic, robustness wave, multi-model narrowing).
- `paper/record.md:79` — "  - there is no single credence across formats (direction 3);" — Haiku-only. Sonnet is *mixed* or *partial*; Opus's 26 claims fit one credence as well as six. — "  - on Haiku there is no single credence across formats (direction 3; partial on Sonnet, not supported on Opus, DM2);"
- `paper/record.md:3` — "This is a chronological record of each question the project tested: its pre-registration, the test, the result, the diagnosis, and the redirect it led to." — omits DM2–DM6, D48 and direction 5. — Append: "It covers `main` up to 09:36 on 2026-11-04. It does not include the multi-model replications (DM1–DM6, `results/multi-model.md`) or the unmerged `probes` branch."
- `README.md:21` — "Eleven pre-registered tests, six from `paper/gold-map.md` and five from `paper/biomimetic-map.md`, each frozen in its own commit before its data were opened or its first call. All used one scale direction, about $4.2 in all, with no refusals." — 5 of 11 reuse archives already opened; D35 uses both directions. — "Eleven pre-registered tests, six from `paper/gold-map.md` and five from `paper/biomimetic-map.md`, each frozen in its own commit before its analysis or first call. Five of them (D34, D35, D40–D42) reanalyse archived data that earlier analyses had already opened. Every new design used one scale direction (D35 compares the two by design). About $4.2 in all, with no refusals."
- `README.md:187` — "They are fixed before results exist, so a quantum encoding cannot win against a strawman." — Arms F and G were added 49 s after run 2's failing result. — "Arm E was fixed before any results. Arms F and G were added after run 2 failed, but before they were scored, so a quantum encoding cannot win against a strawman."
- `README.md:221` — "All were pre-registered or logged before the data they affect." — D9 was logged after its pool calls began, and D13 6 s after exp 3's first call. — "All were pre-registered or logged before their data were analysed; D9 and D13 were committed after their first calls had begun."
- `README.md:244` — "Every hardware job is logged with its QPU seconds in [`results/ibm-usage.md`](results/ibm-usage.md), and Anthropic API spend per question is in [`results/api-usage.md`](results/api-usage.md)." — the ledger stops at pool run 6. — "Every hardware job is logged with its QPU seconds in [`results/ibm-usage.md`](results/ibm-usage.md). Anthropic API spend per question for the pool runs is in [`results/api-usage.md`](results/api-usage.md); every other run's cost is in its own results file."
- `paper/morning-brief.md:5` — "- **Rules:** each was pre-registered in its own commit before its archive was opened or its first call. Every design used one scale direction (0 = certainly false, 100 = certainly true). Stop-on-refusal applied to every call." — same as README:21. — "- **Rules:** each was pre-registered in its own commit before its analysis or first call; five reanalyse archives already opened in earlier analyses. Every new design used one scale direction (0 = certainly false, 100 = certainly true); direction 3's free look compares the two by design. Stop-on-refusal applied to every call."

## Does the verdict stand?
For a ledger, the "verdict" is whether the record can be trusted as a factual timeline: STANDS WITH CAVEATS.
- **What holds.** Every hash, time and copied number checks out.
- **What needs correcting.** One sentence is false ("Before the run"). The "Standing" is stale and mis-dated. The record omits four merged pre-registered tests. It does not flag six cases where a "pre-registration" or its code followed the first calls or the primary result.
- **README and the brief.** Their "before its data were opened" and "all used one scale direction" claims are wrong as stated. Five of the eleven overnight tests are archival, and one uses both scale directions.

## Confidence
High.
- **What I verified mechanically.** Every hash and time against git. First calls via decoded request IDs. Costs from the archived `cost_usd` fields. Table values by matching numbers in the results files.
- **What I could not check.** The 2026-10-25 proposal date. Whether archival analyses were run before their pre-registration commit (git records only the commit, so the 15–90 s gaps fit pre-written code run once, but cannot prove it). Refusals, because the archives store no stop_reason. Timing for batch-API (`mm-*`) and local-model (probes) runs, which rests on git order alone.

## Tally
claims_checked: 41
claims_failed: 15
overclaim_sentences: 10
verdict: STANDS WITH CAVEATS
confidence: high

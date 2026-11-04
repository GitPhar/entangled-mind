# Audit: gm4-evidence-seeking

**Files audited:** `results/gm4-evidence-seeking.md`, `results/gm4-evidence-seeking.json`, `results/gm4-calls.json`, `experiments/gm4-evidence-seeking.md`, `experiments/gm4_evidence_seeking.py`, `experiments/gm4_menus.py`, `experiments/gm4-menus.json`, DEVIATIONS D39, `results/pool-run-3.json`; citations in README.md, paper/record.md, paper/morning-brief.md, paper/the-entangled-mind-v3.md, paper/gold-map.md. Recomputation: `scratchpad/g5/gm4.py`.
**Pre-registration:** `e913227` (2026-11-04 04:05:19), text in `experiments/gm4-evidence-seeking.md` + DEVIATIONS D39. The runner, analysis code, menu builder and frozen menus/scores (`gm4-menus.json`) are all in the same commit. First call 05:02:12, last 05:04:32 (decoded, 1,200 calls). Result `bc9e70d` 05:05:06.
Timing verdict: OK. Everything was frozen 57 min before the first call, and none of the four gm4 files has changed since (`git diff e913227 HEAD` on them is empty). The shared `gm_common.py` caller was changed at 04:07 (amendment 2 of D36: save frequency and error stop). That touches run plumbing only, not scoring.

## Plain-English summary of the audit
The numbers are right and the pre-registered verdict, "mixed or at chance", stands. I recomputed every hit rate, chance rate, excess, CI and discriminating-menu contrast from the raw choices and the frozen menu scores. The README's "undecided" is the accurate summary. The record's and v3's "does not prefer the informative check" goes slightly beyond intervals whose upper ends are +0.04 and +0.14, and v3's "prefers neither" asserts a null. A post-hoc look sharpens the picture in a way the summaries miss. The above-chance score for the "informative" (EIG) rule comes entirely from menus where the informative claim is also the confirming one. On menus where they differ, EIG picks are exactly at chance (−0.002 and 0.000), while confirmatory picks stay above chance under D5 (+0.20 [+0.04, +0.36]). So "+14 and +21 points over chance for the informative check" should not be read as evidence of any informativeness-seeking.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | EIG D5 hit 39%, chance 25%, +0.141 [+0.042, +0.245] (`results/gm4-evidence-seeking.md:26`) | 0.391 / 0.250 / +0.141 [+0.042, +0.241]; LOO range +0.125 to +0.151 | holds |
| 2 | EIG BA5 55% / 34% / +0.210 [+0.113, +0.310] (`:27`) | 0.550 / 0.340 / +0.210 [+0.116, +0.310] | holds |
| 3 | dM D5 +0.196, dM BA5 +0.166 (`:28-29`) | +0.196 [+0.103, +0.293]; +0.166 [+0.084, +0.248] | holds |
| 4 | confirmatory 52% / 32% / +0.207 [+0.109, +0.313] (`:30`) | 0.523 / 0.317 / +0.207 [+0.107, +0.314]; LOO +0.193 to +0.223 | holds |
| 5 | most-uncertain 21% / 34% / −0.128 [−0.205, −0.043] (`:31`) | 0.214 / 0.342 / −0.128 [−0.203, −0.045] | holds |
| 6 | discriminating menus: D5 46 menus −0.237 [−0.523, +0.044]; BA5 26 menus −0.135 [−0.403, +0.142] (`:16,37-38`) | −0.237 [−0.521, +0.050] on 46 menus from 23 items; −0.135 [−0.406, +0.140] on 26 menus from 14 items | holds |
| 7 | modal share 87%; positions 27/26/26/21%; D5–BA5 argmax agree on 41 of 120 (`:10,40-42`) | 0.868; 26.8 / 26.3 / 26.0 / 20.8%; 41. The screen-position mapping (i + r) mod 4 was verified on all 1,200 calls. | holds |
| 8 | "Its picks beat chance under every rule that scores a claim by how much it bears on the answer" (`:11-14`) | True for all 5 rules. But the rules overlap heavily: the EIG targets share a claim with the confirmatory target on 74 (D5) and 94 (BA5) of 120 menus. Post hoc, on the disjoint menus, EIG excess is −0.002 [−0.139, +0.134] (D5) and 0.000 [−0.155, +0.180] (BA5). All of EIG's excess lies on overlap menus (+0.23, +0.27). | holds (minor: non-specific) |
| 9 | "The decisive comparison is undecided … Under the pre-registered rule the verdict is **mixed**." (`:16`); README:33 "Whether it prefers informative or confirmatory checks is undecided." | matches the rule: per model "neither", verdict "mixed or at chance" | holds |
| 10 | "It does not prefer the informative check over the confirmatory one when they come apart" (`:18`); record:53; v3:754 | Point estimates are negative, but the CIs reach +0.04 (D5) and +0.14 (BA5). "No detectable preference" is supported; "does not prefer" states a null. | overclaim (minor) |
| 11 | "prefers neither when they differ" (`paper/the-entangled-mind-v3.md:79`) | Both point estimates lean confirmatory, and post hoc the confirmatory excess on D5-disjoint menus is +0.197 [+0.043, +0.360]. "Neither" asserts a symmetric null the data do not show. | overclaim |
| 12 | "the model consistently (87%) picks ones that bear strongly on its question" (`paper/morning-brief.md:62`) | 87% is the mean modal-choice share (consistency of repeats), not the share of picks that bear strongly on the question. The rule hit rates are 39–61%. | overclaim (minor) |
| 13 | number of tests | 6 excess CIs + 2 paired contrasts, uncorrected. The verdict uses a pre-registered conjunction of 4 of them, and nothing post hoc is reported as confirmatory. | holds |

## Holes found
1. **The EIG "hit above chance" is non-specific.** EIG's target overlaps the confirmatory target on 62% (D5) and 78% (BA5) of menus. Where they do not overlap, EIG picks are at chance (−0.002, 0.000) while confirmatory picks remain above chance (D5-disjoint +0.20 [+0.04, +0.36]; BA5-disjoint +0.14 [−0.07, +0.34]). This is post hoc, but it means the "+14 and +21 points over chance" for the informative rule (`:12`; record:53; v3:749) is carried by confirmatory/relevance overlap. A post-hoc |lean|-only rule also beats chance (69% against 54%).
2. **"Does not prefer informative" and "prefers neither" are stronger than "undecided".** The pre-registered contrasts have upper bounds of +0.04 and +0.14, so a small informative preference is not excluded (BA5 especially). v3:79's "prefers neither" also ignores that both point estimates and the post-hoc disjoint-menu excess lean confirmatory. The README's "undecided" is the correct summary. The record's sentence is the less accurate of the two the lead flagged.
3. **The discriminating sets are small and clustered.** 46 menus from 23 items (D5) and 26 from 14 items (BA5), which explains the wide CIs. The test of the gold map's central question rests on 14–23 items.
4. **The "87%" figure is consistency, not relevance** (morning-brief:62). Minor wording.
5. **The scope caveat is stated in the results file.** EIG is defined by the experiment-5 fits, which the chooser never sees, and c_k is an extracted confidence (prereg §7).

## Overclaims to cut (exact sentences)
- `results/gm4-evidence-seeking.md:18` — "It does not prefer the informative check over the confirmatory one when they come apart; if anything it leans confirmatory, as Jhaveri et al. found for hypothesis testing." — CIs [−0.52, +0.04] and [−0.40, +0.14] do not exclude a small informative preference. — Replace with: "When they come apart it shows no detectable preference for the informative check; if anything it leans confirmatory, as Jhaveri et al. found for hypothesis testing."
- `paper/the-entangled-mind-v3.md:754` — "When the informative and the confirming check come apart, it does not prefer the informative one." — Replace with: "When the informative and the confirming check come apart, it shows no detectable preference for the informative one, and the point estimates lean confirmatory."
- `paper/the-entangled-mind-v3.md:79` — "- **Evidence seeking is mixed.** The model's choice of which claim to check beats chance for informative and confirming checks alike, and prefers neither when they differ." — Replace with: "- **Evidence seeking is mixed.** The model's choice of which claim to check beats chance for informative and confirming checks alike; when they differ, whether it prefers either is undecided (the estimates lean confirmatory)."
- `paper/record.md:53` — "it chooses claims that bear on its answer, but does not prefer the informative check over the confirming one" — Replace with: "it chooses claims that bear on its answer; whether it prefers the informative or the confirming check is undecided (estimates lean confirmatory)".
- `paper/morning-brief.md:62` — "6. **Evidence-seeking is mixed (direction 4, $0.11).** Offered four of its own claims to check, the model consistently (87%) picks ones that bear strongly on its question, and avoids the most uncertain-sounding one." — 87% is repeat consistency, not relevance. — Replace with: "6. **Evidence-seeking is mixed (direction 4, $0.11).** Offered four of its own claims to check, the model picks the same claim 87% of the time, beats chance for claims that bear strongly on its question, and avoids the most uncertain-sounding one."

## Does the verdict stand?
Pre-registered verdict: **mixed or at chance**, with "neither" under both D5 and BA5. **STANDS.** All inputs recompute exactly from the raw choices and the frozen scores, and everything was frozen before the calls. The only changes needed are to the summary wording. A post-hoc analysis suggests that EIG's above-chance rate is carried entirely by overlap with confirmatory targets. It should be reported as exploratory and does not change the verdict.

## Confidence
High. Everything was recomputed from `gm4-calls.json` and `gm4-menus.json` with my own tie handling, chance correction and item bootstrap. The timing is fully verified from decoded request IDs and git. The menu scores themselves (EIG under the D5/BA5 fits) were taken as frozen inputs and not re-derived from the fits.

## Tally
claims_checked: 13
claims_failed: 3
overclaim_sentences: 5
verdict: STANDS
confidence: high

# Do the paper's three main findings hold on Sonnet and Opus?

Written 2026-11-04 (America/Denver) after the multi-model runs on branch `multi-model`. The three tests of *No Credence to Read* that make its main claims are:
- direction 1, self-knowledge (test P);
- direction 2, edited transcripts (test T);
- direction 3, six formats (test F).

Each was re-run with `claude-sonnet-5-5` and `claude-opus-5-5` as the base model. Every test used the Haiku original's prompts, analysis code and pre-registered criteria, at reduced scale (see Budget), with one scale direction and stop-on-refusal, and each was pre-registered in its own commit before its first call. No call was refused.

## In plain English

**No self-advantage was detected on the Sonnet × Opus pair either.**
- Sonnet and Opus each rated how likely each other's answers were to be right, and how likely their own were, with an identical prompt.
- Opus spots Sonnet's mistakes better than Sonnet does: AUROC 0.96 against 0.90.
- On Opus's own answers, no advantage from being the author was detected: Opus reaches 0.90, Sonnet reading the same answers 0.89 (+0.011 [−0.056, +0.072]).
- With each judge's overall skill cancelled out, the authorship effect is −0.045 [−0.107, +0.017]. That is the same sign and about the same size as for Haiku and Sonnet (−0.055), though that interval excluded 0 and this one does not.
- The pre-registered reading is again **no self-advantage**.

**The question alone still changes the judgment on Sonnet. On Opus the effect is small and the test is not decisive.**
- Sonnet's order effect survives hiding its earlier answers. The ratio is 2.95 [0.99, 12.55], read as *question-driven*. As with Haiku, much of it comes from 2 of the 10 items, one of them the item that dominated Haiku's result (h191).
- Opus shows a smaller order effect (4.4 points [0.8, 6.9], gate p = 0.004), against Sonnet's 6.1 and Haiku's 9.3; with the record hidden it comes from one item (h058).
- With only 2 conversations per cell for Opus (a budget fallback), its ratio of 0.93 has an interval from 0.06 to 7.3. It is read as *leaning question-driven, not decisive*.

**All three models lean on their own record.**
- When the model can see its first answer, it repeats it within 5 points 78% (Haiku), 88% (Sonnet) and 95% (Opus) of the time.
- When the first answer is hidden, the shares fall to 25%, 35% and 65%.
- So in every model, the repeated answer leans partly on the visible first answer. Opus is the most stable without it.

**On Sonnet, one credence is partly usable (F′); on Opus, once its arm was completed (D49), one credence is usable by F′, though on both the held-out-repeats test is undecided.**
- Haiku, re-analysed on the same 80 statements, clearly fails the one-credence test.
- Sonnet's formats disagree beyond what one credence can absorb on 92% of statements. But one extreme statement pulls the interval across zero, so the pre-registered reading is *mixed*.
- On test F′, one credence predicts a left-out format from the other five about two-thirds as well as that format predicts itself (Q = 0.69 [0.53, 0.82], *partial*). Haiku's Q on the same 80 statements is 0.29.
- Opus's run was stopped by its budget after 26 statements. On those, the test was undecided (ΔLL +0.42 [−1.83, +2.69], *mixed*), though its formats ranked the statements closely alike (Kendall's W 0.86, against 0.71 for Sonnet and 0.54 for Haiku).
- **Update (D49, after this summary was written):** Opus's arm was completed to 68 of 80 statements (`results/mm-gm3b-opus-completion.md`). The held-out-repeats test is still *mixed* (ΔLL +1.90 [−0.82, +4.65]), and test F′ gives Q = 0.94 [0.90, 0.97], *a usable single belief*.
- Across these three models, the formats agree more for the stronger models (item-matched Kendall's W on Opus's 68 statements: 0.56, 0.76 and 0.87, exploratory; F′ Q 0.29 and 0.69 on 80 statements, 0.94 on Opus's 68). That matches Smolin & Wilder's (2026) finding for other capable models.

**What this means for the paper.**
- On its claim about self-report (Section 4.4), no self-advantage was detected on any of the three models.
- Its claim that the record conditions later answers (Section 4.2) holds on all three: hiding the first answer lowers repeat agreement on every model.
- Its claim that the question alone changes the judgment holds on Sonnet (*question-driven*). On Opus it is untested at useful power.
- Its strongest claim, that there is no format-free credence (Section 4.5), is a claim about Haiku, and to a lesser degree Sonnet. It should not be stated for language models in general. On Opus the held-out-repeats test is undecided, on the 26 claims run here and on the 68 of the completion (D49); by D49's frozen F′ rule the claim is contradicted there (D50).

## Budget

Sean set **$20** for the three replications. All calls went through the Message Batches API, at half of list price. The full designs would have cost about $65 at list price, so each was scaled down without changing its structure (DM1).

| run | design as run | cap | spent | status |
|---|---|---|---|---|
| pilot (DM1) | 12 sync calls + 2-request batch, on a non-test item | — | $0.03 | |
| six formats, Sonnet (DM2) | 80 claims × 6 formats × 10 repeats | $2.20 | $2.04 | complete (resumed in smaller chunks, DM2a) |
| six formats, Opus (DM2) | 26 of 80 claims | $4.30 | $3.10 | **budget-stopped** at 1,600 of 4,800 calls (DM4a) |
| self-knowledge, Sonnet × Opus (DM3) | Opus answers 298 questions; 3 new judge cells × 298 | $4.60 | $4.03 | complete; paraphrase and recognition arms not run |
| transcripts, Sonnet (DM4) | 10 items × 5 chains × 4 conditions × R = 4 | $2.40 | $2.19 | complete |
| transcripts, Opus (DM4) | same, at **R = 2** after the per-wave fallback | $8.51 (DM4a) | $4.89 | complete at R = 2 |
| **total** | | | **$16.28** | $3.72 unspent |

**Why Opus cost more than planned, and why money was left over.**
- Opus 5.5 cannot turn thinking off. At its lowest effort it still thought for about 120 tokens per call on these contested statements; in the pilot's easy single-turn calls it had not thought at all. That doubled its cost per call and stopped its six-format arm.
- The transcript arm's cap was then re-set, before any transcript call, to whatever remained of the $20 (DM4a).
- After its first wave, the pre-registered projection, which assumed costs grow 12% per turn, predicted $8.74 at R = 3 against an $8.51 cap. The fallback therefore dropped to R = 2.
- In fact Opus's later turns cost less per call than its first, so R = 3 would have fitted. The rule makes the drop irreversible. That is why $3.72 was left unspent.

## Results

### Self-knowledge (direction 1; `results/mm-gm1-self-knowledge.md`)

**Accuracy on the 298 questions:** Sonnet 89.9% (30 wrong); Opus 94.3% (17 wrong).

AUROC for each author's errors (judge first, then author; SS is D36's archived cell):

| set | SS | OS | OO | SO | I = SS + OO − OS − SO |
|---|---|---|---|---|---|
| all 298 | 0.903 | 0.959 | 0.904 | 0.893 | **−0.045 [−0.107, +0.017]** |
| authors' correctness differs (21) | 0.551 | 0.522 | 0.684 | 0.529 | +0.184 [−0.296, +0.812] |
| *Haiku × Sonnet, D36, all 298* | | | | | *−0.055 [−0.103, −0.007]* |

**Per-author self advantages.**
- Δ_S = SS − OS = −0.056 [−0.089, −0.025]: Sonnet is worse on its own answers than Opus is.
- Δ_O = OO − SO = +0.011 [−0.056, +0.072].

**Pre-registered reading: no self-advantage.**

### Transcripts (direction 2; `results/mm-gm2-self-conditioning.md`)

| model | R per cell | gate p | OE shown | OE redacted | R = OE_redacted / OE_shown | reading |
|---|---|---|---|---|---|---|
| Haiku (D37 archive, repeats 0–3) | 4 | 0.0008 | 9.3 | 18.7 | 2.01 [1.04, 4.43] | question-driven |
| Sonnet | 4 | 0.031 | 6.1 | 17.9 | **2.95 [0.99, 12.55]** | **question-driven** |
| Opus | 2 | 0.004 | 4.4 | 4.1 | **0.93 [0.06, 7.31]** | **leaning question-driven (not decisive)** |

| model | b_MF (final M follows planted first M) | next-rating pull | MF agreement, shown → redacted |
|---|---|---|---|
| Haiku (R = 4) | 1.23 [0.65, 2.11] | +5.4 [3.1, 7.5] | 78% → 25% |
| Sonnet | 0.39 [−0.05, 0.76] | +2.5 [−0.5, 5.5] | 88% → 35% |
| Opus | 0.35 [0.17, 0.54] | +0.8 [−1.5, 2.9] | 95% → 65% |

**Notes.**
- **Concentration.** Sonnet's redacted order effect comes mostly from h191 (42 points) and h112 (30 points); the other 8 items are at 0–17. h191 also carried Haiku's effect (43 points). Opus's redacted effect is one item, h058 (13 points).
- **Memory.** The memory reading (agreement falls by more than 10 points when the first answer is hidden) holds on all three models.
- **Opus's final M.** It moves *away* from the planted values in O1–O4 (high minus low −10.0 [−17.1, −3.1]), while its MF re-rating follows them (b_MF +0.35).

### Six formats (direction 3; `results/mm-gm3b-format-invariance.md`)

| model | claims (items) | mean ΔLL per claim (L6 − L1) | claims with ΔLL > 0 | reading | Kendall's W | discordant pairs vs 0–100 | test F′ Q |
|---|---|---|---|---|---|---|---|
| Haiku (D38 archive, same 80) | 80 (20) | +19.42 [+15.40, +23.21] | 86% | no single credence | 0.54 | 25–35% | 0.29 [0.19, 0.43] |
| Sonnet | 80 (20) | +9.22 [−1.29, +16.24] | 92% | **mixed** | 0.71 | 14–20% | **0.69 [0.53, 0.82], partial** |
| Opus (budget-stopped) | 26 (7) | +0.42 [−1.83, +2.69] | 58% | **mixed** | 0.86 | 3–14% | not computed (arm incomplete) |

**Exploratory note** (computed after the analysis; it changes no reading):
- Sonnet's interval reaches below 0 because of one claim, h058 claim 8, with ΔLL −308. The next lowest are −90 and −77. The median claim is +11.0.
- A claim like this is one where the even and odd repeats of a format disagree more than any fitted per-format latent allows. Test F's even/odd design is sensitive to such claims.
- Opus's 26 claims all come from items Haiku answered wrongly, so its row is not comparable item for item with the others.

## Deviations, in one place

These are recorded in `DEVIATIONS.md`, entries DM1–DM6.
- **DM1, thinking.** Thinking is "off" per model: Haiku `disabled`, Sonnet `between_tools` (Sonnet 5.5 rejects `disabled`), Opus effort `low` (Opus 5.5 cannot disable thinking). Opus's thinking text is never returned and never placed in a transcript.
- **DM1, batches.** All calls use the Batches API, which records a message ID per call rather than an HTTP request ID.
- **Scaled designs.**
  - Six formats: 80 of 160 claims.
  - Transcripts: R = 4 rather than 10, with planted values from each model's own first-turn ratings.
  - Self-knowledge: Opus authors new answers; Sonnet's self cell is D36's archive; paraphrase and recognition arms not run.
- **DM2a.** The runner's 1.25 safety factor refused Sonnet's last six-format chunk at a projected $2.21 against $2.20. The chunk was submitted in quarters under the same cap and finished at $2.04.
- **DM4a.** Opus's six-format arm was budget-stopped as pre-registered. Opus's transcript cap was re-set from cost alone, before its first call.

## Files

- **Pre-registrations:**
  - `experiments/mm-gm3b-format-invariance.md`
  - `experiments/mm-gm1-self-knowledge.md`
  - `experiments/mm-gm2-self-conditioning.md`
- **Code:** `experiments/mm_common.py` (batch runner and stop rules), `mm_gm3b.py`, `mm_gm1.py`, `mm_gm2.py`. Each imports the original test's prompts and analysis unchanged.
- **Raw calls:**
  - `results/mm-gm3b-{sonnet,opus}-calls.json`
  - `results/mm-gm1-calls.json`
  - `results/mm-gm2-{sonnet,opus}-conversations.json`, with planted values in `results/mm-gm2-{sonnet,opus}-planted.json`
  - batch IDs in `results/mm-batches-*.json`
  - the pilot in `results/mm-pilot-calls.json`
- **Rebuilding the tables:** `python experiments/mm_gm3b.py analyse`, `mm_gm1.py analyse`, `mm_gm2.py analyse` rebuild every table from the archived calls with no API call.

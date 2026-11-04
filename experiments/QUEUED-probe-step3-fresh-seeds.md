# Queued: probe study step 3 on fresh seeds (not yet pre-registered)

**Status:** QUEUED on 2026-11-04 (America/Denver) by the main session, after the audit (`audits/probe-dissociation.md`, hole 1). It has not been run or frozen. Before its first conversation, whoever runs it must:
1. turn this file into a pre-registration, `experiments/probe-dissociation-step3-fresh.md`;
2. log it as **DP2** in `DEVIATIONS.md`, under the probes section;
3. commit both in a commit of their own.

## Why

DP1's step 3 was meant to test on conversations different from the gate's. The pre-registration says "Selection and test therefore use different conversations" (`experiments/probe-dissociation.md` §3). But both `cmd_gate` and `cmd_run` seed each conversation with `local_lm.seed_for(f"{lm.name}|{qid}|{cell}|{rep}")`, so the same key gives the same seed. As a result, step 3's verbal ratings for O1–O4 and B0 are an exact replay of the gate's: 500 of 500 identical.

Three things follow:
- validity check V4 tested nothing;
- the gate items' order effects in step 3 carry the selection's winner's curse;
- the result is marked **unverified** on main (D53).

## The design to freeze

Everything from DP1 is unchanged except the seed namespace and the output file:
- the model (Llama-3-8B-Instruct, 4-bit, MLX);
- the gate items G (h190, h101, h191);
- the probe file `results/probe-dissociation-llama3-8b-theta.npz` and its layer (13);
- the cells (O1–O4, B0, T+, T−) and R = 10;
- the prompts, the M-prompt readout, the statistics, the bootstrap and the frozen verdict rule.

**The change: fresh seeds.** Each conversation's sampler seed is `seed_for(f"{lm.name}|step3-fresh|{qid}|{cell}|{rep}")`. The new namespace `step3-fresh` makes the seeds disjoint from the gate's and from DP1's step 3. Add the namespace to `collect`/`converse` as a parameter that defaults to the old behaviour, so DP1 still reproduces.

**Before running, check** that no fresh-seed O1–O4/B0 rating sequence matches its gate counterpart exactly. Report the share that do. It should be near the chance rate of exact repeats at temperature, not 100%.

**Output:** `results/probe-dissociation-llama3-8b-run-fresh.json`, with the analysis written to `results/probe-dissociation-fresh.{json,md}`. DP1's files are untouched.

**Report alongside**, with these as pre-registered secondaries:
- the gate rule re-applied to the fresh verbal data (span ≥ 5 and order permutation p < 0.05 on each of G), uncorrected and under Holm;
- Q in the two alternative scalings the audit proposed, in units of the held-out true–false gap and the probe's B0 SD;
- r with h191 dropped.

**Reading:**
- If the fresh run returns DP1's label, DP1 is verified on independent conversations.
- If it returns a different label, DP1's label is withdrawn and the fresh one is reported in its place.
- If the gate items lose their order effect on fresh seeds, the label is "gate not replicated".

**Cost:** $0 API, local only. About as long as DP1's step 3.

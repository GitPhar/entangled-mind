"""Gold-map direction 2: shown / redacted / planted-high / planted-low transcripts, as pre-registered
in experiments/gm2-self-conditioning.md (D37). $1 cap; any refusal stops the run.

    python experiments/gm2_self_conditioning.py            # run (cached), then analyse
    python experiments/gm2_self_conditioning.py --analyse  # analysis only

Calls cached in results/gm2-conversations.json. Writes results/gm2-self-conditioning.{json,md}."""

import json
import sys

import numpy as np

import exp5_run as er
from entangled_mind import config
from gm_common import PLAIN, Caller, structured

CACHE = config.RESULTS / "gm2-conversations.json"
PLANTED = config.EXPERIMENTS / "gm2-planted-values.json"
OUT_JSON, OUT_MD = config.RESULTS / "gm2-self-conditioning.json", config.RESULTS / "gm2-self-conditioning.md"
CHAINS, CONDS, R, CAP = ["O1", "O2", "O3", "O4", "MF"], ["shown", "redacted", "high", "low"], 10, 1.0
N_PERM, PERM_SEED, BOOT_SEED = 5000, 2002, 2003


def converse(job, recs, planted):
    key, q, chain, cond = job
    rec = recs[q]
    turns = er.turns_for(chain, planted[q]["chain_claims"])
    msgs, out, cost, rids = [], [], 0.0, []
    for t, (kind, k) in enumerate(turns):
        text = er.question(rec, kind, k)
        if t == 0:
            text = er.opening(rec, "a") + "\n\n" + text
        msgs.append({"role": "user", "content": text})
        d, raw, c, rid = structured(er.MODEL, msgs, er.RATING, "gm2", max_tokens=200)
        r = min(100, max(0, int(d["rating"])))
        out.append({"kind": kind, "claim": k, "rating": r})
        cost += c
        rids.append(rid)
        if cond == "shown":
            hist = raw
        elif cond == "redacted":
            hist = "[rating recorded]"
        else:
            v = planted[q]["M"] if kind == "M" else planted[q]["S"][str(k)]
            hist = json.dumps({"rating": v[cond]})
        msgs.append({"role": "assistant", "content": hist})
    return {"turns": out, "cost": cost, "request_ids": rids}


def run():
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    planted = json.loads(PLANTED.read_text())["items"]
    c = Caller(CACHE, CAP, "direction 2")
    jobs = [(f"{q}|{ch}|{cond}|{r}", q, ch, cond) for q in planted for ch in CHAINS for cond in CONDS for r in range(R)]
    c.run(jobs, lambda j: converse(j, recs, planted), workers=8)


# --- analysis -----------------------------------------------------------------

def finals(conv, q, ch, cond):
    return [conv[f"{q}|{ch}|{cond}|{r}"]["turns"][-1]["rating"] for r in range(R) if f"{q}|{ch}|{cond}|{r}" in conv]


def vc(groups):
    groups = [np.asarray(g, float) for g in groups if len(g)]
    n = np.mean([len(g) for g in groups])
    allv = np.concatenate(groups)
    msb = sum(len(g) * (g.mean() - allv.mean()) ** 2 for g in groups) / (len(groups) - 1)
    msw = sum(((g - g.mean()) ** 2).sum() for g in groups) / (len(allv) - len(groups))
    return max(0.0, (msb - msw) / n), msb


def oe(conv, items, cond):
    return float(np.sqrt(np.mean([vc([finals(conv, q, f"O{i}", cond) for i in (1, 2, 3, 4)])[0] for q in items])))


def item_boot(items, fn, seed, n=2000):
    rng = np.random.default_rng(seed)
    vals = [fn(list(rng.choice(items, len(items)))) for _ in range(n)]
    vals = [v for v in vals if v == v]
    return [fn(items), *map(float, np.percentile(vals, [2.5, 97.5]))]


def analyse():
    conv = json.loads(CACHE.read_text())
    planted = json.loads(PLANTED.read_text())["items"]
    res = compute(conv, planted, list(planted))
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)


def compute(conv, planted, items):
    # gate: permutation test of sum MS_between in the shown condition
    rng = np.random.default_rng(PERM_SEED)
    data = {q: [finals(conv, q, f"O{i}", "shown") for i in (1, 2, 3, 4)] for q in items}
    T = sum(vc(g)[1] for g in data.values())
    null = []
    for _ in range(N_PERM):
        t = 0.0
        for g in data.values():
            allv = rng.permutation(np.concatenate(g))
            sizes = np.cumsum([len(x) for x in g])[:-1]
            t += vc(np.split(allv, sizes))[1]
        null.append(t)
    p_gate = (1 + sum(x >= T for x in null)) / (N_PERM + 1)
    res = {"n_conversations": len(conv), "cost_usd": sum(v["cost"] for v in conv.values()), "gate_p": float(p_gate),
           "OE": {cond: oe(conv, items, cond) for cond in CONDS},
           "OE_ci": {cond: item_boot(items, lambda s, c=cond: oe(conv, s, c), BOOT_SEED + i) for i, cond in enumerate(CONDS)}}
    ratio = lambda s: oe(conv, s, "redacted") / oe(conv, s, "shown") if oe(conv, s, "shown") > 0 else float("nan")
    res["R"] = item_boot(items, ratio, BOOT_SEED)
    # planted effects
    dM = {q: planted[q]["M"]["high"] - planted[q]["M"]["low"] for q in items}
    b_mf = lambda s: float(np.mean([(np.mean(finals(conv, q, "MF", "high")) - np.mean(finals(conv, q, "MF", "low"))) / dM[q] for q in s]))
    res["b_MF"] = item_boot(items, b_mf, BOOT_SEED + 10)

    def pull_item(q):
        diffs = []
        for ch in CHAINS:
            for pos in range(1, 6 if ch == "MF" else 5):
                hi = [conv[f"{q}|{ch}|high|{r}"]["turns"][pos]["rating"] for r in range(R) if f"{q}|{ch}|high|{r}" in conv]
                lo = [conv[f"{q}|{ch}|low|{r}"]["turns"][pos]["rating"] for r in range(R) if f"{q}|{ch}|low|{r}" in conv]
                if hi and lo:
                    diffs.append(np.mean(hi) - np.mean(lo))
        return float(np.mean(diffs))
    pulls = {q: pull_item(q) for q in items}
    res["next_rating_pull"] = item_boot(items, lambda s: float(np.mean([pulls[q] for q in s])), BOOT_SEED + 11)
    fm = {q: float(np.mean([np.mean(finals(conv, q, f"O{i}", "high")) - np.mean(finals(conv, q, f"O{i}", "low")) for i in (1, 2, 3, 4)]))
          for q in items}
    res["final_M_shift_O"] = item_boot(items, lambda s: float(np.mean([fm[q] for q in s])), BOOT_SEED + 12)

    def agree(cond):
        v = []
        for q in items:
            for r in range(R):
                c = conv.get(f"{q}|MF|{cond}|{r}")
                if c:
                    ms = [t["rating"] for t in c["turns"] if t["kind"] == "M"]
                    v.append(abs(ms[1] - ms[0]) <= 5)
        return float(np.mean(v))
    res["MF_agreement"] = {cond: agree(cond) for cond in CONDS}
    res["per_item"] = {q: {"OE_shown": float(np.sqrt(vc(data[q])[0])),
                           "OE_redacted": float(np.sqrt(vc([finals(conv, q, f"O{i}", "redacted") for i in (1, 2, 3, 4)])[0])),
                           "M_means": {cond: [float(np.mean(finals(conv, q, f"O{i}", cond))) for i in (1, 2, 3, 4)] for cond in CONDS},
                           "MF_M2": {cond: float(np.mean(finals(conv, q, "MF", cond))) for cond in CONDS},
                           "planted_M": planted[q]["M"], "next_rating_pull": pulls[q]} for q in items}
    if p_gate >= 0.05:
        reading = "untestable (no order effect in the shown condition)"
    elif res["R"][1] >= 0.5:
        reading = "question-driven: the order effect survives redaction (a measurement effect in the strict sense)"
    elif res["R"][2] < 0.5:
        reading = "self-anchoring: redaction removes most of the order effect"
    else:
        reading = f"leaning {'question-driven' if res['R'][0] >= 0.5 else 'self-anchoring'} (CI straddles 0.5; not decisive)"
    res["reading"] = reading
    return res


def write_md(r):
    f = lambda d, p=2: f"{d[0]:.{p}f} [{d[1]:.{p}f}, {d[2]:.{p}f}]"
    lines = ["# Direction 2: measurement as self-conditioning (shown, redacted, planted transcripts)", "",
             "Pre-registered in `experiments/gm2-self-conditioning.md` (D37), committed before any call. 10 experiment-5 items, chains "
             "O1–O4 and MF, anchor (a) only (0 = certainly false, 100 = certainly true), 10 conversations per item × chain × condition. "
             f"{r['n_conversations']} conversations, **${r['cost_usd']:.2f}** of the $1 cap; no refusal.", "", PLAIN,
             "## Order effect across O1–O4 (final main rating)", "",
             "OE = √(mean over items of the between-order variance component), in rating points; 95% item-bootstrap CIs.", "",
             "| condition | OE (points) |", "|---|---|"]
    for cond in CONDS:
        lines.append(f"| {cond} | {f(r['OE_ci'][cond], 1)} |")
    lines += ["", f"- Gate (shown order effect, permutation p): **{r['gate_p']:.4f}**.",
              f"- **R = OE_redacted / OE_shown: {f(r['R'])}**.", "",
              "## Planted values", "",
              f"- Self-anchoring in MF, b_MF (final M follows the planted first M): {f(r['b_MF'])}.",
              f"- Next-rating pull (actual ratings at positions 2+, planted high minus low): {f(r['next_rating_pull'], 1)} points.",
              f"- Final M shift in O1–O4, planted high minus low: {f(r['final_M_shift_O'], 1)} points.", "",
              "## Replicability in MF (|M₂ − M₁| ≤ 5)", "", "| condition | agreement |", "|---|---|"]
    for cond, v in r["MF_agreement"].items():
        lines.append(f"| {cond} | {v:.0%} |")
    lines += ["", "## Per item", "", "| item | OE shown | OE redacted | final M by order O1–O4: shown | redacted | MF M₂: shown / redacted / high / low | planted M low / high |",
              "|---|---|---|---|---|---|---|"]
    for q, v in r["per_item"].items():
        mm = v["M_means"]
        lines.append(f"| {q} | {v['OE_shown']:.1f} | {v['OE_redacted']:.1f} | {', '.join(f'{x:.0f}' for x in mm['shown'])} | "
                     f"{', '.join(f'{x:.0f}' for x in mm['redacted'])} | "
                     f"{' / '.join(f'{v['MF_M2'][c]:.0f}' for c in CONDS)} | {v['planted_M']['low']} / {v['planted_M']['high']} |")
    lines += ["", f"## Pre-registered reading: **{r['reading']}**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        write_md(json.loads(OUT_JSON.read_text()))
    else:
        if "--analyse" not in sys.argv:
            run()
        analyse()

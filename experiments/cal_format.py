"""Consequence demonstration: a standard verbalized-confidence calibration protocol (Tian et al., 2023, "Verb. 1S top-1")
under two formats and two question orders, as pre-registered in experiments/cal-format-order.md (DM6). $3 budget.

    python experiments/cal_format.py run haiku|sonnet
    python experiments/cal_format.py analyse

Calls cached in results/cal-<model>-conversations.json; writes results/calibration-under-format.{json,md}."""

import json
import random
import re
import sys

import numpy as np

import mm_common as mc
from entangled_mind import config

MODELS = {"haiku": mc.H, "sonnet": mc.S}
CAPS = {"haiku": 0.30, "sonnet": 2.60}
EST = {"haiku": 0.00003, "sonnet": 0.0006}
BLOCK_SEED, BOOT_SEED, BLOCK, NBOOT, BINS = 4041, 4042, 10, 2000, 10
OUT_JSON, OUT_MD = config.RESULTS / "calibration-under-format.json", config.RESULTS / "calibration-under-format.md"

# Tian et al. (2023), Table 6, "Verb. 1S top-1", verbatim ("\n" rendered as newlines).
TIAN_P = ("Provide your best guess and the probability that it is correct (0.0 to 1.0) for the following question. Give ONLY the "
          "guess and probability, no other words or explanation. For example:\n\nGuess: <most likely guess, as short as possible; "
          "not a complete sentence, just the guess!>\n Probability: <the probability between 0.0 and 1.0 that your guess is correct, "
          "without any extra commentary whatsoever; just the probability!>\n\nThe question is: {q}")
# The same template with the probability replaced by a frequency (the paper's format F5), every other word unchanged.
TIAN_F = ("Provide your best guess and the number of questions, out of 100 questions like this one on each of which you have the "
          "same evidence as on this one, on which your guess would be correct (0 to 100) for the following question. Give ONLY the "
          "guess and number, no other words or explanation. For example:\n\nGuess: <most likely guess, as short as possible; "
          "not a complete sentence, just the guess!>\n Frequency: <the number between 0 and 100 of such questions on which your "
          "guess would be correct, without any extra commentary whatsoever; just the number!>\n\nThe question is: {q}")
TEMPLATES = {"P": TIAN_P, "F": TIAN_F}


def pool():
    recs = json.loads((config.RESULTS / "pool-run-3.json").read_text())["records"]
    return {r["id"]: {"question": r["question"], "gold": r["answer"]} for r in recs}


def blocks():
    ids = sorted(pool())
    random.Random(BLOCK_SEED).shuffle(ids)
    return [ids[i:i + BLOCK] for i in range(0, len(ids), BLOCK)]


def design():
    """Conversation key -> ordered question ids."""
    conv = {}
    for b, qs in enumerate(blocks()):
        for f in "PF":
            conv[f"seq|{f}|fwd|{b}"] = qs
            conv[f"seq|{f}|rev|{b}"] = qs[::-1]
            for q in qs:
                for rep in (0, 1):
                    conv[f"fresh|{f}|r{rep}|{q}"] = [q]
    return conv


def parse(text, fmt):
    """Guess -> yes/no; confidence in [0, 1]. Returns (guess, conf) with None where unparseable."""
    g = re.search(r"Guess:\s*\**\s*([A-Za-z]+)", text or "")
    guess = g.group(1).lower() if g and g.group(1).lower() in ("yes", "no") else None
    if fmt == "P":
        m = re.search(r"Probability:\s*\**\s*([0-9]*\.?[0-9]+)\s*(%?)", text or "")
        conf = None
        if m:
            v = float(m.group(1))
            conf = v / 100 if m.group(2) == "%" else v
    else:
        m = re.search(r"Frequency:\s*\**\s*([0-9]*\.?[0-9]+)", text or "")
        conf = float(m.group(1)) / 100 if m else None
    if conf is not None and not 0 <= conf <= 1:
        conf = None
    return guess, conf


def path(m):
    return config.RESULTS / f"cal-{m}-conversations.json"


def run(m):
    model, P = MODELS[m], pool()
    D = design()
    cache = json.loads(path(m).read_text()) if path(m).exists() else {}
    for k in D:
        cache.setdefault(k, {"turns": [], "cost": 0.0})
    save = lambda: path(m).write_text(json.dumps(cache))
    spent = lambda: sum(c["cost"] for c in cache.values())
    est = EST[m]
    for t in range(BLOCK):
        live = [k for k in D if len(D[k]) > t and len(cache[k]["turns"]) == t and not cache[k].get("abandoned")]
        if not live:
            continue
        reqs = {}
        for k in live:
            fmt = k.split("|")[1]
            msgs = []
            for u, q in enumerate(D[k][:t + 1]):
                msgs.append({"role": "user", "content": TEMPLATES[fmt].format(q=P[q]["question"])})
                if u < t:
                    msgs.append({"role": "assistant", "content": cache[k]["turns"][u]["raw"]})   # shown: the reply as given
            reqs[k] = mc.params(model, msgs, None, max_tokens=300)

        def store(k, rec):
            c = cache[k]
            c["cost"] += rec["cost"]
            if "raw" not in rec:
                c["abandoned"] = rec.get("error", "refused")
                return
            q = D[k][len(c["turns"])]
            guess, conf = parse(rec["raw"], k.split("|")[1])
            c["turns"].append({"q": q, "raw": rec["raw"], "guess": guess, "conf": conf, "msg_id": rec.get("msg_id"),
                               "batch": rec.get("batch")})
        br = mc.BatchRunner(f"cal-{m}-turn{t + 1}", CAPS[m], spent, chunk=1500)
        est = br.run(reqs, lambda k, msg: {"raw": mc.text_of(msg)}, store, save, est * (1.15 if t else 1.0))
        print(f"{m}: turn {t + 1} done, ${spent():.3f}", flush=True)


# --- analysis -------------------------------------------------------------------------------

def ece(conf, corr, bins=BINS):
    conf, corr = np.asarray(conf, float), np.asarray(corr, float)
    idx = np.minimum((conf * bins).astype(int), bins - 1)
    return float(sum(abs(corr[idx == b].mean() - conf[idx == b].mean()) * (idx == b).mean() for b in range(bins) if (idx == b).any()))


def auroc(pos, neg):
    from gm_common import auroc as a
    return a(pos, neg) if len(pos) and len(neg) else float("nan")


CELLS = [("seq", f, o) for f in "PF" for o in ("fwd", "rev")] + [("fresh", f, r) for f in "PF" for r in ("r0", "r1")]


def records(cache, P):
    """cell -> {q: (conf, correct)} for parsed answers; plus unparsed counts and position-wise confidence."""
    out, unparsed = {c: {} for c in CELLS}, {c: 0 for c in CELLS}
    for k, c in cache.items():
        kind, f, o = k.split("|")[:3]
        for pos, t in enumerate(c["turns"]):
            if t["guess"] is None or t["conf"] is None:
                unparsed[(kind, f, o)] += 1
                continue
            out[(kind, f, o)][t["q"]] = (t["conf"], t["guess"] == P[t["q"]]["gold"], pos)
    return out, unparsed


def stats(cell, qs):
    v = [cell[q] for q in qs if q in cell]
    if not v:
        return dict(ece=np.nan)
    conf, corr = np.array([x[0] for x in v]), np.array([x[1] for x in v], float)
    return dict(ece=ece(conf, corr), acc=float(corr.mean()), conf=float(conf.mean()), over=float(conf.mean() - corr.mean()),
                brier=float(np.mean((conf - corr) ** 2)), n=len(v),
                auroc=auroc(conf[corr == 1], conf[corr == 0]))


def contrasts(R, qs):
    e = {c: stats(R[c], qs)["ece"] for c in CELLS}
    return {"format": np.mean([e[("seq", "F", o)] - e[("seq", "P", o)] for o in ("fwd", "rev")]),
            "order": np.mean([e[("seq", f, "rev")] - e[("seq", f, "fwd")] for f in "PF"]),
            "replicate": np.mean([e[("fresh", f, "r1")] - e[("fresh", f, "r0")] for f in "PF"]),
            "sequential_minus_fresh": np.mean([np.mean([e[("seq", f, o)] for o in ("fwd", "rev")]) - e[("fresh", f, "r0")] for f in "PF"]),
            **{f"format_{o}": e[("seq", "F", o)] - e[("seq", "P", o)] for o in ("fwd", "rev")},
            **{f"order_{f}": e[("seq", f, "rev")] - e[("seq", f, "fwd")] for f in "PF"}}


def analyse():
    P, B = pool(), blocks()
    out = {"blocks": len(B), "block_size": BLOCK, "models": {}}
    for m in MODELS:
        if not path(m).exists():
            continue
        cache = json.loads(path(m).read_text())
        R, unparsed = records(cache, P)
        allq = [q for b in B for q in b]
        point = contrasts(R, allq)
        rng = np.random.default_rng(BOOT_SEED)
        boots = {k: [] for k in point}
        for _ in range(NBOOT):
            qs = [q for bi in rng.integers(0, len(B), len(B)) for q in B[bi]]
            for k, v in contrasts(R, qs).items():
                boots[k].append(v)
        ci = {k: [float(point[k]), *map(float, np.nanpercentile(boots[k], [2.5, 97.5]))] for k in point}
        # per-question confidence movement: order (fwd vs rev) against resampling (fresh r0 vs r1), per format
        move = {}
        for f in "PF":
            a, b = R[("seq", f, "fwd")], R[("seq", f, "rev")]
            c, d = R[("fresh", f, "r0")], R[("fresh", f, "r1")]
            move[f] = {"order_mean_abs": float(np.mean([abs(a[q][0] - b[q][0]) for q in a if q in b])),
                       "replicate_mean_abs": float(np.mean([abs(c[q][0] - d[q][0]) for q in c if q in d])),
                       "guess_flip_order": float(np.mean([a[q][1] != b[q][1] for q in a if q in b])),
                       "guess_flip_replicate": float(np.mean([c[q][1] != d[q][1] for q in c if q in d]))}
        pos = {f"{f}": [float(np.mean([v[0] for k in (("seq", f, "fwd"), ("seq", f, "rev")) for v in R[k].values() if v[2] == p]))
                        for p in range(BLOCK)] for f in "PF"}
        reading = []
        reading.append("calibration depends on format" if ci["format"][1] > 0 or ci["format"][2] < 0 else "no detectable format dependence")
        reading.append("calibration depends on question order" if ci["order"][1] > 0 or ci["order"][2] < 0
                       else "no detectable order dependence")
        out["models"][m] = {"cells": {"|".join(c): stats(R[c], allq) for c in CELLS}, "unparsed": {"|".join(c): v for c, v in unparsed.items()},
                            "contrasts": ci, "movement": move, "confidence_by_position": pos, "reading": "; ".join(reading),
                            "cost_usd": sum(c["cost"] for c in cache.values()),
                            "abandoned": sum(1 for c in cache.values() if c.get("abandoned"))}
    ms = list(out["models"])
    if len(ms) == 2:
        sign = {"|".join(c): np.sign(out["models"]["haiku"]["cells"]["|".join(c)]["ece"] - out["models"]["sonnet"]["cells"]["|".join(c)]["ece"])
                for c in CELLS if c[0] == "seq"}
        out["model_ranking_same_in_all_sequential_cells"] = bool(len(set(sign.values())) == 1)
        out["ece_sign_haiku_minus_sonnet"] = {k: float(v) for k, v in sign.items()}
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float))
    write_md(out)


NAMES = {"P": "probability 0.0–1.0 (Tian, verbatim)", "F": "frequency out of 100"}


def write_md(o):
    f3 = lambda d: f"{d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]"
    L = ["# Calibration under format and question order", "",
         "Pre-registered in `experiments/cal-format-order.md` (DM6), committed before any call. Tian et al.'s (2023) Verb. 1S top-1 "
         "protocol on the 300-question hard pool, in two formats; each question asked alone (two independent replicates) and inside "
         f"{o['blocks']} ten-question conversations in a forward and a reversed order. ECE: 10 equal-width bins, |accuracy − confidence| "
         "weighted by bin share (Guo et al., 2017). 95% CIs from 2,000 block-bootstrap resamples, paired across conditions. Costs at the batch rate.", "",
         "## In plain English", "", "(Hand-written after the run; excluded from reproduce.py's comparison.)", ""]
    for m, r in o["models"].items():
        L += [f"## {m}", "", f"Cost ${r['cost_usd']:.2f}; abandoned conversations: {r['abandoned']}.", "",
              "| context | format | order / replicate | n | accuracy | mean confidence | ECE | Brier | AUROC | unparsed |", "|---|---|---|---|---|---|---|---|---|---|"]
        for c in CELLS:
            s = r["cells"]["|".join(c)]
            L.append(f"| {'conversation' if c[0] == 'seq' else 'fresh'} | {NAMES[c[1]]} | {c[2]} | {s['n']} | {s['acc']:.3f} | {s['conf']:.3f} | "
                     f"**{s['ece']:.3f}** | {s['brier']:.3f} | {s['auroc']:.3f} | {r['unparsed']['|'.join(c)]} |")
        k = r["contrasts"]
        L += ["", "| contrast | ΔECE [95% CI] |", "|---|---|",
              f"| **format** (frequency − probability), mean of both orders | **{f3(k['format'])}** |",
              f"| **order** (reversed − forward), mean of both formats | **{f3(k['order'])}** |",
              f"| noise baseline: fresh replicate 2 − replicate 1, mean of both formats | {f3(k['replicate'])} |",
              f"| conversation (mean of both orders) − fresh, mean of both formats | {f3(k['sequential_minus_fresh'])} |",
              f"| format, forward only / reversed only | {f3(k['format_fwd'])} / {f3(k['format_rev'])} |",
              f"| order, probability only / frequency only | {f3(k['order_P'])} / {f3(k['order_F'])} |", "",
              "| format | mean per-question |Δconfidence|, forward vs reversed | same, fresh replicate 1 vs 2 | correctness flips, order / replicate |",
              "|---|---|---|---|"]
        for fm, v in r["movement"].items():
            L.append(f"| {NAMES[fm]} | {v['order_mean_abs']:.3f} | {v['replicate_mean_abs']:.3f} | {v['guess_flip_order']:.1%} / {v['guess_flip_replicate']:.1%} |")
        L += ["", "Mean confidence by position in the conversation (1–10): " + "; ".join(
            f"{fm}: " + ", ".join(f"{x:.2f}" for x in v) for fm, v in r["confidence_by_position"].items()), "",
              f"**Pre-registered reading, {m}: {r['reading']}.**", ""]
    if "model_ranking_same_in_all_sequential_cells" in o:
        L.append(f"Which model has the lower ECE is the same in all four conversation cells: **{o['model_ranking_same_in_all_sequential_cells']}**.")
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    if sys.argv[1] == "run":
        mc.main_guard(lambda: run(sys.argv[2]))
    else:
        analyse()

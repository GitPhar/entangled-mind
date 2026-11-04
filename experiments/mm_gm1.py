"""Multi-model replication of direction 1 (self versus other confidence), as pre-registered in
experiments/mm-gm1-self-knowledge.md (DM3). Pair: Sonnet (S) and Opus (O).

    python experiments/mm_gm1.py run       # Opus answers the 298 questions, then the three new judge cells (batches, capped)
    python experiments/mm_gm1.py analyse

The judge prompt, schema, settings, AUROC cells, bootstrap and reading rule are gm1_self_knowledge's, imported unchanged.
The SS cell is direction 1's archived matched-framing cell. Calls cached in results/mm-gm1-calls.json;
writes results/mm-gm1-self-knowledge.{json,md}."""

import json
import re
import sys

import numpy as np

import gm1_self_knowledge as g1
import mm_common as mc
from entangled_mind import config, llm

CACHE = config.RESULTS / "mm-gm1-calls.json"
OUT_JSON, OUT_MD = config.RESULTS / "mm-gm1-self-knowledge.json", config.RESULTS / "mm-gm1-self-knowledge.md"
CAP, EST_BASE, EST_JUDGE = 4.60, 0.009, 0.0019
JUDGES = {"S": mc.S, "O": mc.O}


def load_cache():
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


def opus_authors(cache, ids, s):
    """Opus records in direction 1's author format; answered questions only."""
    out = {}
    for i in ids:
        v = cache.get(f"base|O|{i}")
        if v and v.get("answer") in ("yes", "no"):
            out[i] = {"question": s[i]["question"], "correct": v["answer"] == s[i]["answer"],
                      "deliberation_record": {"visible_answer": v["text"]}}
    return out


def run():
    authors, ids, _, _ = g1.load()
    s = authors["S"]
    cache = load_cache()
    save = lambda: CACHE.write_text(json.dumps(cache))
    spent = lambda: sum(v["cost"] for v in cache.values())
    # step A: Opus as author, exactly as llm.ask_base (adaptive thinking, model default effort, max_tokens 16000)
    reqs = {f"base|O|{i}": {"model": mc.O, "max_tokens": 16000, "thinking": {"type": "adaptive", "display": "summarized"},
                            "messages": [{"role": "user", "content": llm.BASE_PROMPT.format(question=s[i]["question"])}]}
            for i in ids if f"base|O|{i}" not in cache}

    def on_base(k, m):
        text = "\n".join(b.text for b in m.content if b.type == "text").strip()
        f = re.findall(r"FINAL ANSWER:\s*(YES|NO)", text, flags=re.I)
        return {"text": text, "answer": f[-1].lower() if f else None,
                "thinking_summary": "\n".join(b.thinking for b in m.content if b.type == "thinking").strip()}
    br = mc.BatchRunner("gm1-base", CAP, spent, chunk=300)
    br.run(reqs, on_base, cache.__setitem__, save, EST_BASE)
    print(f"step A done, ${spent():.3f}", flush=True)
    o = opus_authors(cache, ids, s)
    both = [i for i in ids if i in o]
    auth = {"S": s, "O": o}
    # step B: judge cells SO, OS, OO with the matched prompt and llm.self_confidence's settings (no thinking parameter)
    reqs = {}
    for i in both:
        for j, a in (("S", "O"), ("O", "S"), ("O", "O")):
            k = f"orig|{j}|{a}|{i}"
            if k not in cache:
                prompt = g1.MATCHED.format(question=auth[a][i]["question"], answer=auth[a][i]["deliberation_record"]["visible_answer"])
                reqs[k] = {"model": JUDGES[j], "max_tokens": 4000, "messages": [{"role": "user", "content": prompt}],
                           "output_config": {"format": {"type": "json_schema", "schema": g1.CONF}}}
    br = mc.BatchRunner("gm1-judge", CAP, spent, chunk=900)
    br.run(reqs, lambda k, m: {"confidence": int(min(100, max(0, json.loads(mc.text_of(m))["confidence"])))},
           cache.__setitem__, save, EST_JUDGE)
    print(f"step B done, ${spent():.3f}", flush=True)


def analyse():
    authors, ids, _, _ = g1.load()
    s = authors["S"]
    cache = load_cache()
    arch = json.loads(g1.CACHE.read_text())
    o = opus_authors(cache, ids, s)
    items = [i for i in ids if i in o]
    auth = {"S": s, "O": o}
    ok = lambda d, k: k in d and d[k].get("confidence") is not None
    conf = {("S", "S"): {i: arch[f"orig|S|S|{i}"]["confidence"] for i in items if ok(arch, f"orig|S|S|{i}")}}
    for j, a in (("S", "O"), ("O", "S"), ("O", "O")):
        conf[(j, a)] = {i: cache[f"orig|{j}|{a}|{i}"]["confidence"] for i in items if ok(cache, f"orig|{j}|{a}|{i}")}
    complete = [i for i in items if all(i in d for d in conf.values())]
    dis = [i for i in complete if s[i]["correct"] != o[i]["correct"]]
    inter = lambda c: c[("O", "O")] + c[("S", "S")] - c[("S", "O")] - c[("O", "S")]
    dS = lambda c: c[("S", "S")] - c[("O", "S")]
    dO = lambda c: c[("O", "O")] - c[("S", "O")]
    res = {"n": {"questions": len(ids), "opus_answered": len(items), "complete": len(complete), "disagreement": len(dis)},
           "accuracy": {"sonnet": float(np.mean([s[i]["correct"] for i in complete])),
                        "opus": float(np.mean([o[i]["correct"] for i in complete]))},
           "errors": {"sonnet": int(sum(not s[i]["correct"] for i in complete)), "opus": int(sum(not o[i]["correct"] for i in complete))},
           "opus_unanswered": [i for i in ids if i not in o],
           "refusals": sum(1 for v in cache.values() if v.get("refused")),
           "max_tokens": sum(1 for v in cache.values() if v.get("error") == "max_tokens"),
           "cost_usd": sum(v["cost"] for v in cache.values()), "n_calls": len(cache)}
    seeds = iter(range(g1.SEED_BOOT, g1.SEED_BOOT + 100))
    for name, its in (("all", complete), ("disagreement", dis)):
        if not its:
            continue
        cells = g1.cells_auroc(conf, auth, its)
        res[name] = {"cells": {f"{j}{a}": v for (j, a), v in cells.items()},
                     "I": g1.boot(conf, auth, its, inter, next(seeds)),
                     "delta_S": g1.boot(conf, auth, its, dS, next(seeds)),
                     "delta_O": g1.boot(conf, auth, its, dO, next(seeds))}
    m_all, m_dis = res["all"]["I"], res.get("disagreement", {}).get("I", [float("nan")] * 3)
    if m_all[0] > 0 and m_dis[1] > 0:
        reading = "self-advantage (paraphrase control not run; see DM3)"
    elif m_dis[2] < 0:
        reading = "other-advantage"
    else:
        reading = "no self-advantage"
    res["reading"] = reading
    ref = json.loads((config.RESULTS / "gm1-self-knowledge.json").read_text())
    res["haiku_sonnet_reference"] = {"I_all": ref["matched, all"]["I"], "I_disagreement": ref["matched, disagreement"]["I"],
                                     "cells_all": ref["matched, all"]["cells"]}
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)


def write_md(r):
    f = lambda d: f"{d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]"
    L = ["# Multi-model replication of direction 1: self versus other confidence, Sonnet × Opus", "",
         "Pre-registered in `experiments/mm-gm1-self-knowledge.md` (DM3), committed before any call. Authors: Sonnet's archived "
         f"hard-pool answers and Opus's new ones, on the {r['n']['complete']} of direction 1's {r['n']['questions']} questions "
         f"that both answered; disagreement subset (authors' correctness differs): {r['n']['disagreement']}. "
         f"{r['n_calls']} new calls, **${r['cost_usd']:.2f}** of the ${CAP:.2f} cap (batch rate); refusals: {r['refusals']}.", "",
         "## In plain English", "", "(Hand-written after the run; excluded from reproduce.py's comparison.)", "",
         f"Accuracy on the complete set: Sonnet {r['accuracy']['sonnet']:.1%} ({r['errors']['sonnet']} wrong), "
         f"Opus {r['accuracy']['opus']:.1%} ({r['errors']['opus']} wrong).", "",
         "## AUROC of each judge for each author's errors", "",
         "Cells: judge then author (OS = Opus judging Sonnet's answers). I = SS + OO − OS − SO; Δ_S = SS − OS; Δ_O = OO − SO. "
         "95% CIs from 2,000 question-level resamples. SS is direction 1's archived cell.", "",
         "| set | SS | OS | OO | SO | **I** | Δ_S | Δ_O |", "|---|---|---|---|---|---|---|---|"]
    for name in ("all", "disagreement"):
        if name in r:
            c, v = r[name]["cells"], r[name]
            L.append(f"| {name} | {c['SS']:.3f} | {c['OS']:.3f} | {c['OO']:.3f} | {c['SO']:.3f} | **{f(v['I'])}** | "
                     f"{f(v['delta_S'])} | {f(v['delta_O'])} |")
    h = r["haiku_sonnet_reference"]
    L += ["", f"Reference, Haiku × Sonnet (D36): I = {f(h['I_all'])} on all 298; {f(h['I_disagreement'])} on the disagreement subset.", "",
          f"## Pre-registered reading: **{r['reading']}**"]
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    if sys.argv[1] == "run":
        mc.main_guard(run)
    else:
        analyse()

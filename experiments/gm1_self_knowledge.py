"""Gold-map direction 1: privileged self-knowledge, as pre-registered in
experiments/gm1-self-knowledge.md (D36). $3 cap; any refusal stops the run.

    python experiments/gm1_self_knowledge.py            # run steps 1-4 (cached), then analyse
    python experiments/gm1_self_knowledge.py --analyse  # analysis only, from the cache

Calls cached in results/gm1-calls.json. Writes results/gm1-self-knowledge.{json,md}."""

import json
import random
import re
import sys

import numpy as np

from entangled_mind import config, llm
from gm_common import PLAIN, Caller, auroc, structured

CACHE = config.RESULTS / "gm1-calls.json"
OUT_JSON, OUT_MD = config.RESULTS / "gm1-self-knowledge.json", config.RESULTS / "gm1-self-knowledge.md"
H, S = "claude-haiku-5-5", "claude-sonnet-5-5"
JUDGES = {"H": H, "S": S}
# D36 amendment 2: the recorded-spend cap is $3 minus an upper bound of $0.20 on calls lost uncached in the crash
CAP, SEED_SUB, SEED_REC, SEED_BOOT, SEED_RBOOT = 2.80, 1001, 1002, 1001, 1003
MATCHED = """Here is a yes/no question and an answer another assistant gave to it.

Question: {question}

The assistant's answer:
{answer}

How confident are you, from 0 to 100, that this final answer is correct? Give only the number."""
PARA_SYSTEM = ("Rewrite the following answer to a yes/no question in your own words. Keep every consideration, the reasoning "
               "and the conclusion exactly as they are; do not add, remove or correct anything. Keep the final line exactly "
               "as it is.")
RECOG = """Here is a yes/no question and an answer to it.

Question: {question}

Answer:
{answer}

How likely is it, from 0 to 100, that you wrote this answer? Give only the number."""
CONF = {"type": "object", "properties": {"confidence": {"type": "integer"}}, "required": ["confidence"], "additionalProperties": False}
LIKE = {"type": "object", "properties": {"likelihood": {"type": "integer"}}, "required": ["likelihood"], "additionalProperties": False}
TEXT = {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"], "additionalProperties": False}


def final(text):
    m = re.findall(r"FINAL ANSWER:\s*(YES|NO)", text or "", flags=re.I)
    return m[-1].lower() if m else None


def load():
    h = {r["id"]: r for r in json.loads((config.RESULTS / "pool-run-3.json").read_text())["records"]}
    s = {r["id"]: r for r in json.loads((config.RESULTS / "pool-run-4.json").read_text())["records"] if r["correct"] is not None}
    ids = sorted(set(h) & set(s))
    authors = {"H": h, "S": s}
    union_wrong = [q for q in ids if not h[q]["correct"] or not s[q]["correct"]]
    both_right = [q for q in ids if q not in union_wrong]
    sub = sorted(union_wrong + random.Random(SEED_SUB).sample(both_right, 80 - len(union_wrong)))
    rec = sub[:]
    random.Random(SEED_REC).shuffle(rec)
    return authors, ids, sub, sorted(rec[:30])


def judge_call(judge, prompt, schema, field):
    # identical settings to llm.self_confidence: no thinking parameter (model default), max_tokens 4000
    resp = llm.client().messages.create(model=JUDGES[judge], max_tokens=4000, messages=[{"role": "user", "content": prompt}],
                                        output_config={"format": {"type": "json_schema", "schema": schema}})
    if resp.stop_reason == "max_tokens":     # D36 amendment 2: recorded as no rating, as with earlier token-cap answers
        return {field: None, "error": "max_tokens", "cost": llm._usage(resp).cost,
                "request_id": getattr(resp, "_request_id", None)}
    llm._check_stop(resp, f"gm1 judge {judge}")
    text = next(b.text for b in resp.content if b.type == "text")
    return {field: int(min(100, max(0, json.loads(text)[field]))), "cost": llm._usage(resp).cost,
            "request_id": getattr(resp, "_request_id", None)}


def run() -> None:
    authors, ids, sub, rec = load()
    c = Caller(CACHE, CAP, "direction 1")
    q = lambda a, i: authors[a][i]["question"]
    vis = lambda a, i: authors[a][i]["deliberation_record"]["visible_answer"]
    # step 1: matched-framing 2x2 on originals
    jobs = [(f"orig|{j}|{a}|{i}", j, a, i) for i in ids for a in "HS" for j in "HS"]
    c.run(jobs, lambda jb: judge_call(jb[1], MATCHED.format(question=q(jb[2], jb[3]), answer=vis(jb[2], jb[3])), CONF, "confidence"))
    print("step 1 done", f"${c.spent():.3f}", flush=True)

    # step 2: paraphrases by Haiku, thinking disabled
    def para(jb):
        _, a, i = jb
        d, _, cost, rid = structured(H, [{"role": "user", "content": vis(a, i)}], TEXT, "gm1 paraphrase", max_tokens=3000,
                                     system=PARA_SYSTEM)
        return {"text": d["text"], "cost": cost, "request_id": rid}
    c.run([(f"para|{a}|{i}", a, i) for i in sub for a in "HS"], para)
    print("step 2 done", f"${c.spent():.3f}", flush=True)
    ok = lambda a, i: final(c.cache[f"para|{a}|{i}"]["text"]) == final(vis(a, i)) and final(vis(a, i)) is not None
    ptext = lambda a, i: c.cache[f"para|{a}|{i}"]["text"]
    # D36 amendment (before steps 3-4 ran): Haiku's recognition calls first, then step 3, then Sonnet's recognition
    rec_jobs = lambda judge: [(f"recog|{v}|{judge}|{a}|{i}", v, judge, a, i) for i in rec for a in "HS" for v in ("orig", "para")
                              if v == "orig" or ok(a, i)]
    rec_fn = lambda jb: judge_call(jb[2], RECOG.format(question=q(jb[3], jb[4]),
                                                       answer=vis(jb[3], jb[4]) if jb[1] == "orig" else ptext(jb[3], jb[4])),
                                   LIKE, "likelihood")
    c.run(rec_jobs("H"), rec_fn)
    print("step 4 (Haiku judge) done", f"${c.spent():.3f}", flush=True)
    # step 3: paraphrase 2x2
    jobs = [(f"pjud|{j}|{a}|{i}", j, a, i) for i in sub for a in "HS" for j in "HS" if ok(a, i)]
    c.run(jobs, lambda jb: judge_call(jb[1], MATCHED.format(question=q(jb[2], jb[3]), answer=ptext(jb[2], jb[3])), CONF, "confidence"))
    print("step 3 done", f"${c.spent():.3f}", flush=True)
    # step 4, Sonnet judge, as far as the cap allows
    c.run(rec_jobs("S"), rec_fn)
    print("step 4 done", f"${c.spent():.3f}", flush=True)


# --- analysis -----------------------------------------------------------------

def A(scores, wrong):
    s, w = np.asarray(scores, float), np.asarray(wrong, bool)
    return auroc(s[w], s[~w]) if w.any() and (~w).any() else float("nan")


def cells_auroc(conf, authors, items):
    """conf[(judge, author)][item] = confidence; returns A(J, X) on items."""
    out = {}
    for (j, a), d in conf.items():
        its = [i for i in items if i in d]
        out[(j, a)] = A([100 - d[i] for i in its], [not authors[a][i]["correct"] for i in its])
    return out


def interaction(cell):
    return cell[("H", "H")] + cell[("S", "S")] - cell[("S", "H")] - cell[("H", "S")]


def boot(conf, authors, items, fn, seed, n=2000):
    rng = np.random.default_rng(seed)
    point = fn(cells_auroc(conf, authors, items))
    vals = []
    for _ in range(n):
        smp = list(rng.choice(items, len(items)))
        keys = [f"{i}#{t}" for t, i in enumerate(smp)]          # resampled items may repeat: expand by position
        conf_b = {k: {f"{i}#{t}": d[i] for t, i in enumerate(smp) if i in d} for k, d in conf.items()}
        auth_b = {a: {f"{i}#{t}": authors[a][i] for t, i in enumerate(smp)} for a in authors}
        v = fn(cells_auroc(conf_b, auth_b, keys))
        if v == v:
            vals.append(v)
    return [point, *map(float, np.percentile(vals, [2.5, 97.5]))]


def analyse() -> None:
    authors, ids, sub, rec = load()
    cache = json.loads(CACHE.read_text())
    dis = [i for i in ids if authors["H"][i]["correct"] != authors["S"][i]["correct"]]
    ok_ = lambda k: k in cache and cache[k].get("confidence", cache[k].get("likelihood")) is not None
    orig = {(j, a): {i: cache[f"orig|{j}|{a}|{i}"]["confidence"] for i in ids if ok_(f"orig|{j}|{a}|{i}")}
            for j in "HS" for a in "HS"}
    g_h = json.loads((config.RESULTS / "arm-g-confidence.json").read_text())
    g_s = json.loads((config.RESULTS / "sonnet-arm-g-confidence.json").read_text())
    you = dict(orig)
    you[("H", "H")] = {i: g_h[i]["confidence"] for i in ids}
    you[("S", "S")] = {i: g_s[i]["confidence"] for i in ids}
    para = {(j, a): {i: cache[f"pjud|{j}|{a}|{i}"]["confidence"] for i in sub if ok_(f"pjud|{j}|{a}|{i}")}
            for j in "HS" for a in "HS"}
    para_drop = {a: [i for i in sub if f"para|{a}|{i}" in cache and final(cache[f"para|{a}|{i}"]["text"])
                     != final(authors[a][i]["deliberation_record"]["visible_answer"])] for a in "HS"}
    dH = lambda c: c[("H", "H")] - c[("S", "H")]
    dS = lambda c: c[("S", "S")] - c[("H", "S")]
    res = {"n": {"all": len(ids), "disagreement": len(dis), "subset": len(sub), "recognition": len(rec)},
           "complete": {"orig": all(len(v) == len(ids) for v in orig.values()), "para": all(len(v) > 0 for v in para.values())}}
    seeds = iter(range(SEED_BOOT, SEED_BOOT + 100))
    for name, conf, items in (("matched, all", orig, ids), ("matched, disagreement", orig, dis),
                              ("matched, paraphrase subset (originals)", orig, sub),
                              ("you-gave self cells, all", you, ids), ("you-gave self cells, disagreement", you, dis),
                              ("paraphrased, subset", para, sub), ("paraphrased, disagreement", para, [i for i in dis if i in sub])):
        if not all(len(v) for v in conf.values()):
            continue
        res[name] = {"cells": {f"{j}{a}": v for (j, a), v in cells_auroc(conf, authors, items).items()},
                     "I": boot(conf, authors, items, interaction, next(seeds)),
                     "delta_H": boot(conf, authors, items, dH, next(seeds)),
                     "delta_S": boot(conf, authors, items, dS, next(seeds))}
    res["framing_effect"] = {j: cells_auroc(you, authors, ids)[(j, j)] - cells_auroc(orig, authors, ids)[(j, j)] for j in "HS"}
    # recognition: AUROC of "I wrote it" for own vs other answers
    rng = np.random.default_rng(SEED_RBOOT)
    recog = {}
    for v in ("orig", "para"):
        for j in "HS":
            own = [cache[k]["likelihood"] for i in rec for k in [f"recog|{v}|{j}|{j}|{i}"] if ok_(k)]
            oth = [cache[k]["likelihood"] for i in rec for a in "HS" if a != j for k in [f"recog|{v}|{j}|{a}|{i}"] if ok_(k)]
            if own and oth:
                bs = [auroc(rng.choice(own, len(own)), rng.choice(oth, len(oth))) for _ in range(2000)]
                recog[f"{v}|{j}"] = [auroc(own, oth), *map(float, np.percentile(bs, [2.5, 97.5])), float(np.mean(own)), float(np.mean(oth)), len(own), len(oth)]
    res["recognition"] = recog
    res["paraphrase_drops"] = para_drop
    m_all, m_dis = res["matched, all"]["I"], res["matched, disagreement"]["I"]
    if m_all[0] > 0 and m_dis[1] > 0:
        reading = "self-advantage"
    elif m_dis[2] < 0:
        reading = "other-advantage"
    else:
        reading = "no self-advantage"
    res["reading"] = reading
    if reading == "self-advantage" and "paraphrased, subset" in res:
        ip, io = res["paraphrased, subset"]["I"][0], res["matched, paraphrase subset (originals)"]["I"][0]
        res["paraphrase_reading"] = "survives paraphrase" if ip > 0 and ip >= io / 2 else "does not survive paraphrase"
        if any(recog.get(f"para|{j}", [0.5, 0, 0])[1] > 0.5 for j in "HS"):
            res["paraphrase_reading"] += " (control incomplete: paraphrases still recognised)"
    res["cost_usd"] = sum(v["cost"] for v in cache.values())
    res["n_calls"] = len(cache)
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)


def write_md(r) -> None:
    f = lambda d: f"{d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]"
    lines = ["# Direction 1: privileged self-knowledge (2×2 self-versus-other confidence)", "",
             "Pre-registered in `experiments/gm1-self-knowledge.md` (D36), committed before any call. Authors: Haiku and Sonnet hard-pool "
             f"answers on the {r['n']['all']} questions both answered; disagreement subset (authors' correctness differs): "
             f"{r['n']['disagreement']} questions. {r['n_calls']} calls, **${r['cost_usd']:.2f}** of the $3 cap; no refusal.", "", PLAIN,
             "## AUROC of each judge for each author's errors", "",
             "Cells: judge then author (HS = Haiku judging Sonnet's answers). I = HH + SS − SH − HS (each judge's overall skill cancels); "
             "Δ_H = HH − SH; Δ_S = SS − HS. 95% CIs from 2,000 question-level resamples.", "",
             "| set | HH | SH | SS | HS | **I** | Δ_H | Δ_S |", "|---|---|---|---|---|---|---|---|"]
    for k, v in r.items():
        if isinstance(v, dict) and "cells" in v:
            c = v["cells"]
            lines.append(f"| {k} | {c['HH']:.3f} | {c['SH']:.3f} | {c['SS']:.3f} | {c['HS']:.3f} | **{f(v['I'])}** | {f(v['delta_H'])} | {f(v['delta_S'])} |")
    fe = r["framing_effect"]
    lines += ["", f"Framing effect on the self cells (\"an answer you gave\" minus \"another assistant\"), all questions: "
              f"Haiku {fe['H']:+.3f}, Sonnet {fe['S']:+.3f}.", "",
              "## Recognition check (\"how likely is it that you wrote this answer?\")", "",
              "| text | judge | AUROC own vs other [95% CI] | mean likelihood, own | mean likelihood, other | n own / other |", "|---|---|---|---|---|---|"]
    for k, v in r["recognition"].items():
        t, j = k.split("|")
        lines.append(f"| {'original' if t == 'orig' else 'paraphrase'} | {'Haiku' if j == 'H' else 'Sonnet'} | {v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}] | {v[3]:.1f} | {v[4]:.1f} | {v[5]} / {v[6]} |")
    lines += ["", f"Paraphrases dropped for a changed or missing final answer: Haiku-authored {len(r['paraphrase_drops']['H'])}, "
              f"Sonnet-authored {len(r['paraphrase_drops']['S'])}.", "",
              f"## Pre-registered reading: **{r['reading']}**"]
    if "paraphrase_reading" in r:
        lines.append(f"\nParaphrase control: **{r['paraphrase_reading']}**")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        write_md(json.loads(OUT_JSON.read_text()))
    else:
        if "--analyse" not in sys.argv:
            run()
        analyse()

"""Experiment 4, run 1: quantitative Yearsley & Trueblood test, as pre-registered in
experiments/exp4-yearsley-trueblood.md (with the D11 addendum on rule R2).

    python experiments/exp4_run.py

Phase 1 rates P(X), P(Y), P(X and Y), P(Y and X) (0-100, R=20 each) and screens for
fallacy items. Phase 2 runs the committed forced-branch QQ audit on the fallacy items
(R=50 first-position calls per order x mapping; R=25 second-position calls per order x
forced first answer x 4 mapping combinations). Calls are cached in
results/exp4-calls.json. On any refusal the run stops and records the request ID.

Writes results/exp4-run-1.{json,md}."""

import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from dotenv import load_dotenv

from entangled_mind import config, llm

load_dotenv(config.ROOT / ".env")
ITEMS = config.EXPERIMENTS / "exp4-items.json"
CALLS = config.RESULTS / "exp4-calls.json"
OUT_JSON = config.RESULTS / "exp4-run-1.json"
OUT_MD = config.RESULTS / "exp4-run-1.md"
MODEL = "claude-haiku-5-5"
BUDGET_USD = 10.0
R_RATE, R_FIRST, R_SECOND, N_BOOT = 20, 50, 25, 1000
SYSTEM = 'You are asked a series of judgment questions. For each question, answer with exactly one letter: "A" or "B". Do not explain.'
RATE_SCHEMA = {"type": "object", "properties": {"probability": {"type": "integer"}}, "required": ["probability"],
               "additionalProperties": False}
AB_SCHEMA = {"type": "object", "properties": {"answer": {"type": "string", "enum": ["A", "B"]}}, "required": ["answer"],
             "additionalProperties": False}
MAPS = {"M1": {"A": "yes", "B": "no"}, "M2": {"A": "no", "B": "yes"}}

_cache, _lock, _stop, _refusal = {}, threading.Lock(), threading.Event(), {}


def call(key, **kw):
    if key in _cache:
        return _cache[key]["out"]
    if _stop.is_set():
        return None
    with _lock:
        if sum(v["cost"] for v in _cache.values()) >= BUDGET_USD:
            _stop.set()
            return None
    try:
        resp = llm.client().messages.create(model=MODEL, max_tokens=200, thinking={"type": "disabled"}, **kw)
        llm._check_stop(resp, "exp4")
    except llm.RefusalError as e:
        _refusal.setdefault("e", (key, e))
        _stop.set()
        return None
    out = json.loads(next(b.text for b in resp.content if b.type == "text"))
    with _lock:
        _cache[key] = {"out": out, "cost": llm._usage(resp).cost, "request_id": getattr(resp, "_request_id", None)}
    return out


def rate(item, statement, rep):
    q = f"{item['context']}\n\nOn a scale from 0 to 100, how likely is it that {statement}? Give only the number."
    out = call(f"{item['id']}|rate|{statement}|{rep}", output_config={"format": {"type": "json_schema", "schema": RATE_SCHEMA}},
               messages=[{"role": "user", "content": q}])
    return None if out is None else min(100, max(0, int(out["probability"]))) / 100


def ab_question(item, which, mapping):
    m = MAPS[mapping]
    inv = {v: k for k, v in m.items()}
    return (f"{item['context']}\n\nIs it true that {item[which]}?\nA = {m['A']}\nB = {m['B']}"), inv


def ask_first(item, order, mapping, rep):
    first = order[0]
    q, _ = ab_question(item, first, mapping)
    out = call(f"{item['id']}|first|{order}|{mapping}|{rep}", system=SYSTEM,
               output_config={"format": {"type": "json_schema", "schema": AB_SCHEMA}},
               messages=[{"role": "user", "content": q}])
    return None if out is None else MAPS[mapping][out["answer"]]


def ask_second(item, order, forced, m1, m2, rep):
    q1, inv1 = ab_question(item, order[0], m1)
    q2, _ = ab_question(item, order[1], m2)
    msgs = [{"role": "user", "content": q1},
            {"role": "assistant", "content": json.dumps({"answer": inv1[forced]})},
            {"role": "user", "content": q2}]
    out = call(f"{item['id']}|second|{order}|{forced}|{m1}{m2}|{rep}", system=SYSTEM,
               output_config={"format": {"type": "json_schema", "schema": AB_SCHEMA}}, messages=msgs)
    return None if out is None else MAPS[m2][out["answer"]]


def run_parallel(fns):
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(lambda f: f(), fns))
    CALLS.write_text(json.dumps(_cache))
    if _refusal:
        key, e = _refusal["e"]
        (config.RESULTS / "refusal.md").write_text(
            f"# Pipeline stopped on a refusal\n\nExperiment 4, call `{key}`\n\nRefused call: **{e.call}**\n\nRequest ID: "
            f"`{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\nNothing was reworded or retried.\n")
        sys.exit(f"STOPPED: {e}")
    if _stop.is_set():
        sys.exit("budget stop")
    return res


# --- statistics on raw samples (bootstrap resamples within each position) -----

def qq_stats(S):
    """S: dict position -> array of 'yes'/'no' content answers. Returns all pre-registered statistics."""
    py = lambda a: float(np.mean(np.asarray(a) == "yes"))
    first = {o: np.concatenate([S[("first", o, m)] for m in MAPS]) for o in ("XY", "YX")}
    K = {(o, f): np.concatenate([S[("second", o, f, a + b)] for a in MAPS for b in MAPS])
         for o in ("XY", "YX") for f in ("yes", "no")}
    pX, pY = py(first["XY"]), py(first["YX"])          # each asked first
    p1 = {"XY": pX, "YX": pY}
    joint = {o: {(a, b): (p1[o] if a == "yes" else 1 - p1[o]) * (py(K[(o, a)]) if b == "yes" else 1 - py(K[(o, a)]))
                 for a in ("yes", "no") for b in ("yes", "no")} for o in ("XY", "YX")}
    o_eff = joint["XY"][("yes", "yes")] - joint["YX"][("yes", "yes")]
    f_bin = joint["XY"][("yes", "yes")] - pY
    # symmetric repetition fit: agreement = r + (1 - r) * p_fresh(second answer matches first)
    est = []
    for o in ("XY", "YX"):
        p_fresh_second = pY if o == "XY" else pX
        for a in ("yes", "no"):
            agree = float(np.mean(K[(o, a)] == a))
            pm = p_fresh_second if a == "yes" else 1 - p_fresh_second
            if pm < 1:
                est.append((agree - pm) / (1 - pm))
    r = float(np.clip(np.mean(est), 0, 1)) if est else 0.0
    o_rep = r * (pX - pY)
    # letter copying: content agreement under same vs crossed mappings
    same = np.concatenate([S[("second", o, f, m + m)] == f for o in ("XY", "YX") for f in ("yes", "no") for m in MAPS])
    cross = np.concatenate([S[("second", o, f, a + b)] == f for o in ("XY", "YX") for f in ("yes", "no")
                            for a in MAPS for b in MAPS if a != b])
    rho = float(same.mean() - cross.mean())
    # marginal shifts and QQ
    x_second = sum((p1["YX"] if a == "yes" else 1 - p1["YX"]) * py(K[("YX", a)]) for a in ("yes", "no"))
    y_second = sum((p1["XY"] if a == "yes" else 1 - p1["XY"]) * py(K[("XY", a)]) for a in ("yes", "no"))
    oe_x, oe_y = x_second - pX, y_second - pY
    disagree = lambda o: joint[o][("yes", "no")] + joint[o][("no", "yes")]
    q = disagree("XY") - disagree("YX")
    oss = abs(oe_x) + abs(oe_y)
    return {"pX_first": pX, "pY_first": pY, "P_X_then_Y": joint["XY"][("yes", "yes")], "P_Y_then_X": joint["YX"][("yes", "yes")],
            "o": o_eff, "f_binary": f_bin, "r_repeat": r, "o_rep": o_rep, "o_beyond_rep": o_eff - o_rep,
            "rho_letter": rho, "OE_X": oe_x, "OE_Y": oe_y, "OSS": oss, "q_QQ": q, "Gamma": abs(q) - oss}


def boot(S, rng):
    pts = qq_stats(S)
    draws = [qq_stats({k: rng.choice(v, len(v)) for k, v in S.items()}) for _ in range(N_BOOT)]
    return {k: {"value": v, "ci95": [float(np.percentile([d[k] for d in draws], 2.5)),
                                     float(np.percentile([d[k] for d in draws], 97.5))]} for k, v in pts.items()}


def saturated(S):
    """Minority answer in fewer than 1 of R samples (i.e. absent) at more than half the positions."""
    flags = [min(np.sum(v == "yes"), np.sum(v == "no")) < 1 for v in S.values()]
    return sum(flags) > len(flags) / 2


def main() -> None:
    global _cache
    items = json.loads(ITEMS.read_text())
    _cache = json.loads(CALLS.read_text()) if CALLS.exists() else {}
    rng = np.random.default_rng(4)
    # phase 1
    jobs = [(it, s, k) for it in items for s in ("X", "Y", "XY", "YX") for k in range(R_RATE)]
    stmt = lambda it, s: {"X": it["X"], "Y": it["Y"], "XY": f"{it['X']} and {it['Y']}", "YX": f"{it['Y']} and {it['X']}"}[s]
    vals = run_parallel([lambda it=it, s=s, k=k: rate(it, stmt(it, s), k) for it, s, k in jobs])
    ratings = {}
    for (it, s, k), v in zip(jobs, vals):
        ratings.setdefault(it["id"], {}).setdefault(s, []).append(v)
    phase1 = {}
    for it in items:
        rr = {s: np.array(v, float) for s, v in ratings[it["id"]].items()}
        def stat(fn):
            d = [fn({s: rng.choice(a, len(a)) for s, a in rr.items()}) for _ in range(N_BOOT)]
            return {"value": fn(rr), "ci95": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))]}
        phase1[it["id"]] = {
            "mean": {s: float(a.mean()) for s, a in rr.items()},
            "fallacy": stat(lambda d: d["XY"].mean() - d["Y"].mean()),
            "double_fallacy": stat(lambda d: d["XY"].mean() - max(d["X"].mean(), d["Y"].mean())),
            "wording_XY_minus_YX": stat(lambda d: d["XY"].mean() - d["YX"].mean())}
    fallacy_items = [it for it in items if phase1[it["id"]]["fallacy"]["ci95"][0] > 0]
    # phase 2
    fns, keys = [], []
    for it in fallacy_items:
        for o in ("XY", "YX"):
            order = ("X", "Y") if o == "XY" else ("Y", "X")
            for m in MAPS:
                for k in range(R_FIRST):
                    keys.append((it["id"], ("first", o, m)))
                    fns.append(lambda it=it, order=order, o=o, m=m, k=k: ask_first(it, order, m, k))
            for f in ("yes", "no"):
                for a in MAPS:
                    for b in MAPS:
                        for k in range(R_SECOND):
                            keys.append((it["id"], ("second", o, f, a + b)))
                            fns.append(lambda it=it, order=order, f=f, a=a, b=b, k=k: ask_second(it, order, f, a, b, k))
    answers = run_parallel(fns)
    samples = {}
    for (qid, pos), ans in zip(keys, answers):
        samples.setdefault(qid, {}).setdefault(pos, []).append(ans)
    phase2 = {}
    for it in fallacy_items:
        S = {k: np.array(v) for k, v in samples[it["id"]].items()}
        st = boot(S, rng)
        sat = saturated(S)
        phase2[it["id"]] = {"stats": st, "saturated": bool(sat), "repeating_labels": st["rho_letter"]["value"] > 0.10}
    scored = [q for q, v in phase2.items() if not v["saturated"] and not v["repeating_labels"]
              and v["stats"]["f_binary"]["ci95"][0] > 0]
    n = len(scored)
    r2_ok = sum(phase2[q]["stats"]["o"]["value"] >= phase2[q]["stats"]["f_binary"]["value"] - 0.05 for q in scored)
    beyond = sum(phase2[q]["stats"]["o_beyond_rep"]["ci95"][0] > 0 for q in scored)
    static_ok = sum(phase2[q]["stats"]["o_beyond_rep"]["ci95"][0] <= 0 <= phase2[q]["stats"]["o_beyond_rep"]["ci95"][1] for q in scored)
    r1 = sum(not (v["stats"]["o"]["ci95"][0] <= 0 <= v["stats"]["o"]["ci95"][1]) for v in phase2.values())
    r3 = sum(v["double_fallacy"]["ci95"][0] > 0 for v in phase1.values())
    if n < 3:
        verdict = f"untestable ({n} scored items; reported descriptively)"
    else:
        r2_met = r2_ok >= n / 2 and beyond >= n / 2
        static_met = static_ok >= n / 2
        verdict = ("R2 met: consistent with the quantum model or a sequential-update classical model; rules out the static twin"
                   if r2_met else "static classical twin (with repetition) supported" if static_met else "neither rule met")
    cost = sum(v["cost"] for v in _cache.values())
    OUT_JSON.write_text(json.dumps({"phase1": phase1, "phase2": phase2, "fallacy_items": [i["id"] for i in fallacy_items],
                                    "scored": scored, "r2_ok": r2_ok, "beyond_rep": beyond, "static_ok": static_ok,
                                    "R1_order_effect_items": r1, "R3_double_fallacies": r3, "verdict": verdict,
                                    "n_calls": len(_cache), "cost_usd": cost}, indent=1))
    write_md(items, phase1, phase2, fallacy_items, scored, r2_ok, beyond, static_ok, r1, r3, verdict, cost)


def write_md(items, phase1, phase2, fallacy_items, scored, r2_ok, beyond, static_ok, r1, r3, verdict, cost):
    c = lambda d: f"{d['value']:+.3f} [{d['ci95'][0]:+.3f}, {d['ci95'][1]:+.3f}]"
    lines = ["# Experiment 4, run 1: quantitative Yearsley & Trueblood test", "",
             "Pre-registration: `experiments/exp4-yearsley-trueblood.md` (with the D11 addendum: meeting R2 is consistent "
             "with the quantum model *or* a sequential-update classical model; it rules out only the static twin). "
             f"Base model `{MODEL}`, thinking disabled. {len(_cache)} calls, **${cost:.2f}**.", "",
             "## Phase 1: ratings (0–1)", "",
             "| item | P(X) | P(Y) | P(X and Y) | P(Y and X) | fallacy P(X and Y) − P(Y) [95% CI] | double fallacy [95% CI] |",
             "|---|---|---|---|---|---|---|"]
    for it in items:
        p = phase1[it["id"]]
        m = p["mean"]
        lines.append(f"| {it['id']} | {m['X']:.2f} | {m['Y']:.2f} | {m['XY']:.2f} | {m['YX']:.2f} | {c(p['fallacy'])} | {c(p['double_fallacy'])} |")
    lines += ["", f"**{len(fallacy_items)} of {len(items)} items show a reliable fallacy** (lower bound > 0) and go to phase 2. "
              f"Reliable double fallacies (R3): **{r3}**.", "",
              "## Phase 2: committed forced-branch QQ audit (fallacy items)", "",
              "Every order-effect number is shown with the marginal-shift check next to it: OE_X and OE_Y (each question's yes-rate "
              "when asked second minus first), OSS = |OE_X| + |OE_Y|, q_QQ and Γ = |q_QQ| − OSS (Γ ≤ 0: non-contextual under "
              "rank-2 Contextuality-by-Default).", "",
              "| item | o = P(X then Y) − P(Y then X) | binary fallacy f | o − o_rep (beyond repetition) | repeat r | letter-copy ρ | OE_X | OE_Y | OSS | q_QQ | Γ | saturated |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for q, v in phase2.items():
        s = v["stats"]
        lines.append(f"| {q} | {c(s['o'])} | {c(s['f_binary'])} | {c(s['o_beyond_rep'])} | {s['r_repeat']['value']:.2f} | "
                     f"{s['rho_letter']['value']:+.2f} | {s['OE_X']['value']:+.3f} | {s['OE_Y']['value']:+.3f} | {s['OSS']['value']:.3f} | "
                     f"{s['q_QQ']['value']:+.3f} | {s['Gamma']['value']:+.3f} | {'yes' if v['saturated'] else ''} |")
    lines += ["", "## Pre-registered rules", "",
              f"- Scored items (fallacy item, not saturated, no letter copying, binary fallacy reliably > 0): **{len(scored)}**.",
              f"- R2, o ≥ f − 0.05: {r2_ok} of {len(scored)}. Order effect beyond repetition reliably > 0: {beyond} of {len(scored)}.",
              f"- Static twin (o − o_rep interval contains 0): {static_ok} of {len(scored)}.",
              f"- R1, fallacy items with an order effect reliably ≠ 0: {r1} of {len(phase2)}.",
              f"- R3, reliable double fallacies: {r3} of {len(items)}.", "",
              f"**Verdict: {verdict}.**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

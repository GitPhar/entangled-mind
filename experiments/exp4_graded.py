"""Experiment 4, run 2: graded order test on run 1's fallacy items, as pre-registered in
experiments/exp4-yearsley-trueblood.md ("Addendum - run 2").

    python experiments/exp4_graded.py

Four two-turn cells per item (X->XY, Y->XY, X->Y, Y->X), R = 20 repeats, ratings 0-100,
default temperature (1.0), thinking disabled. Calls cached in results/exp4-run-2-calls.json;
on any refusal the run stops and records the request ID. Writes results/exp4-run-2.{json,md}."""

import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from dotenv import load_dotenv

from entangled_mind import config, llm

load_dotenv(config.ROOT / ".env")
ITEMS = config.EXPERIMENTS / "exp4-items.json"
RUN1 = config.RESULTS / "exp4-run-1.json"
CALLS = config.RESULTS / "exp4-run-2-calls.json"
OUT_JSON = config.RESULTS / "exp4-run-2.json"
OUT_MD = config.RESULTS / "exp4-run-2.md"
MODEL, BUDGET_USD, R, N_BOOT = "claude-haiku-5-5", 10.0, 20, 1000
SCHEMA = {"type": "object", "properties": {"probability": {"type": "integer"}}, "required": ["probability"],
          "additionalProperties": False}
CELLS = {"X_XY": ("X", "XY"), "Y_XY": ("Y", "XY"), "X_Y": ("X", "Y"), "Y_X": ("Y", "X")}

_cache, _lock, _stop, _refusal = {}, threading.Lock(), threading.Event(), {}


def statement(it, s):
    return {"X": it["X"], "Y": it["Y"], "XY": f"{it['X']} and {it['Y']}"}[s]


def prompt(it, s, first):
    lead = f"{it['context']}\n\n" if first else ""
    return f"{lead}On a scale from 0 to 100, how likely is it that {statement(it, s)}? Give only the number."


def run_cell(it, cell, rep):
    key = f"{it['id']}|{cell}|{rep}"
    if key in _cache:
        return _cache[key]["ratings"]
    if _stop.is_set():
        return None
    with _lock:
        if sum(v["cost"] for v in _cache.values()) >= BUDGET_USD:
            _stop.set()
            return None
    a, b = CELLS[cell]
    msgs, ratings, cost, rids = [], [], 0.0, []
    try:
        for k, s in enumerate((a, b)):
            msgs.append({"role": "user", "content": prompt(it, s, k == 0)})
            resp = llm.client().messages.create(model=MODEL, max_tokens=200, thinking={"type": "disabled"},
                                                output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
                                                messages=msgs)
            llm._check_stop(resp, "exp4-graded")
            text = next(x.text for x in resp.content if x.type == "text")
            msgs.append({"role": "assistant", "content": text})
            ratings.append(min(100, max(0, int(json.loads(text)["probability"]))) / 100)
            cost += llm._usage(resp).cost
            rids.append(getattr(resp, "_request_id", None))
    except llm.RefusalError as e:
        _refusal.setdefault("e", (key, e))
        _stop.set()
        return None
    with _lock:
        _cache[key] = {"ratings": ratings, "cost": cost, "request_ids": rids}
    return ratings


def stats(c):
    """c: cell -> array (R, 2) of (first, second) ratings."""
    pX = np.concatenate([c["X_XY"][:, 0], c["X_Y"][:, 0]]).mean()
    pY = np.concatenate([c["Y_XY"][:, 0], c["Y_X"][:, 0]]).mean()
    both_x, both_y = c["X_XY"][:, 1].mean(), c["Y_XY"][:, 1].mean()
    o, f = both_x - both_y, both_x - pY
    first = np.concatenate([c["X_XY"][:, 0], c["Y_XY"][:, 0]])
    second = np.concatenate([c["X_XY"][:, 1], c["Y_XY"][:, 1]])
    fresh = np.concatenate([np.full(len(c["X_XY"]), both_x), np.full(len(c["Y_XY"]), both_y)]).mean()
    dx, dy = first - first.mean(), second - fresh
    r = float(np.clip(np.dot(dx, dy) / np.dot(dx, dx), 0, 1)) if np.dot(dx, dx) > 0 else 0.0
    o_rep = r * (pX - pY)
    oe_x = c["Y_X"][:, 1].mean() - pX
    oe_y = c["X_Y"][:, 1].mean() - pY
    return {"P_X_first": pX, "P_Y_first": pY, "P_XY_after_X": both_x, "P_XY_after_Y": both_y, "o": o, "f": f,
            "r_anchor": r, "o_rep": o_rep, "o_beyond_anchor": o - o_rep, "OE_X": oe_x, "OE_Y": oe_y,
            "OSS": abs(oe_x) + abs(oe_y)}


def main() -> None:
    global _cache
    run1 = json.loads(RUN1.read_text())
    items = [it for it in json.loads(ITEMS.read_text()) if it["id"] in run1["fallacy_items"]]
    _cache = json.loads(CALLS.read_text()) if CALLS.exists() else {}
    jobs = [(it, cell, k) for it in items for cell in CELLS for k in range(R)]
    with ThreadPoolExecutor(max_workers=8) as ex:
        out = list(ex.map(lambda j: run_cell(*j), jobs))
    CALLS.write_text(json.dumps(_cache))
    if _refusal:
        key, e = _refusal["e"]
        (config.RESULTS / "refusal.md").write_text(
            f"# Pipeline stopped on a refusal\n\nExperiment 4 run 2, call `{key}`\n\nRefused call: **{e.call}**\n\nRequest ID: "
            f"`{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\nNothing was reworded or retried.\n")
        sys.exit(f"STOPPED: {e}")
    if _stop.is_set():
        sys.exit("budget stop")
    analyse(items)


def analyse(items) -> None:
    rng = np.random.default_rng(42)
    res = {}
    for it in items:
        c = {cell: np.array([_cache[f"{it['id']}|{cell}|{k}"]["ratings"] for k in range(R)]) for cell in CELLS}
        pt = stats(c)
        draws = [stats({cell: a[rng.integers(0, R, R)] for cell, a in c.items()}) for _ in range(N_BOOT)]
        res[it["id"]] = {k: {"value": float(v), "ci95": [float(np.percentile([d[k] for d in draws], 2.5)),
                                                         float(np.percentile([d[k] for d in draws], 97.5))]}
                         for k, v in pt.items()}
        res[it["id"]]["zero_variance_cells"] = [cell for cell, a in c.items() if a[:, 1].std() == 0]
    scored = [q for q, s in res.items() if s["f"]["ci95"][0] > 0]
    n = len(scored)
    r2_ok = sum(res[q]["o"]["value"] >= res[q]["f"]["value"] - 0.05 for q in scored)
    beyond = sum(res[q]["o_beyond_anchor"]["ci95"][0] > 0 for q in scored)
    static_ok = sum(res[q]["o_beyond_anchor"]["ci95"][0] <= 0 <= res[q]["o_beyond_anchor"]["ci95"][1] for q in scored)
    if n < 3:
        verdict = f"untestable ({n} scored items; reported descriptively)"
    elif r2_ok >= n / 2 and beyond >= n / 2:
        verdict = "R2 met: consistent with the quantum model or a sequential-update classical model; rules out the static twin"
    elif static_ok >= n / 2:
        verdict = "static classical twin (with anchoring) supported"
    else:
        verdict = "neither rule met"
    cost = sum(v["cost"] for v in _cache.values())
    OUT_JSON.write_text(json.dumps({"items": res, "scored": scored, "r2_ok": r2_ok, "beyond_anchor": beyond,
                                    "static_ok": static_ok, "verdict": verdict, "n_calls": 2 * len(_cache),
                                    "cost_usd": cost}, indent=1))
    c = lambda d: f"{d['value']:+.3f} [{d['ci95'][0]:+.3f}, {d['ci95'][1]:+.3f}]"
    lines = ["# Experiment 4, run 2: graded order test", "",
             "Pre-registration: `experiments/exp4-yearsley-trueblood.md`, Addendum — run 2 (DEVIATIONS.md, D17). "
             f"Base model `{MODEL}`, thinking disabled, default temperature (1.0). {len(items)} fallacy items from run 1, "
             f"4 two-turn cells × {R} repeats each, {2 * len(_cache)} calls, **${cost:.2f}**.", "",
             "Every order-effect number has the marginal-shift check beside it: OE_X and OE_Y are each conjunct's mean "
             "rating when rated second minus when rated first, and OSS = |OE_X| + |OE_Y|.", "",
             "| item | P(X) | P(Y) | P(X∧Y) after X | P(X∧Y) after Y | o | f | o − o_rep (beyond anchoring) | anchor r | OE_X | OE_Y | OSS |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for q, s in res.items():
        lines.append(f"| {q} | {s['P_X_first']['value']:.2f} | {s['P_Y_first']['value']:.2f} | {s['P_XY_after_X']['value']:.2f} | "
                     f"{s['P_XY_after_Y']['value']:.2f} | {c(s['o'])} | {c(s['f'])} | {c(s['o_beyond_anchor'])} | "
                     f"{s['r_anchor']['value']:.2f} | {s['OE_X']['value']:+.3f} | {s['OE_Y']['value']:+.3f} | {s['OSS']['value']:.3f} |")
    lines += ["", "## Pre-registered rules", "",
              f"- Scored items (graded fallacy f reliably > 0): **{n}** of {len(items)}.",
              f"- R2, o ≥ f − 0.05: {r2_ok} of {n}. Order effect beyond anchoring reliably > 0: {beyond} of {n}.",
              f"- Static twin (o − o_rep interval contains 0): {static_ok} of {n}.", "",
              f"**Verdict: {verdict}.**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

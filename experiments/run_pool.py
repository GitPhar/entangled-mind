"""Run the base model, claim extractor and relation judge on the question pool,
then fix the test / calibration split.

    python experiments/run_pool.py 1   # base claude-sonnet-5-5, effort xhigh (archived; 0 wrong)
    python experiments/run_pool.py 2   # base claude-haiku-5-5, default effort (DEVIATIONS.md, D5)
    python experiments/run_pool.py 3   # hard pool, base claude-haiku-5-5 (D6)
    python experiments/run_pool.py 4   # hard pool, base claude-sonnet-5-5, default effort (D6)
    python experiments/run_pool.py 5   # v2 training pool, base claude-haiku-5-5 (D9)
    python experiments/run_pool.py 6   # v2 training pool, base claude-sonnet-5-5, locked-test items first (D18)

Questions run on 4 worker threads sharing a stop flag. If any API call is
refused, no new call starts (calls already in flight may finish), the refused
call, request ID and exact refusal go to results/refusal.md, and the run exits;
nothing is reworded or retried. Finished questions are cached in the run's JSON,
so a crash never pays twice."""

import json
import random
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from dotenv import load_dotenv

from entangled_mind import config, llm

load_dotenv(config.ROOT / ".env")
USAGE_MD = config.RESULTS / "api-usage.md"
# Calls made outside this script this session (pilots, two refused designs, one
# capped extension call before truncation handling existed); see api-usage.md.
UNITEMISED_USD = 0.25
SPEND_STOP_USD = 8.50                 # DEVIATIONS.md, D4
HARD_BUDGET_USD = 15.0                # D6: runs 3 + 4 together
TRAIN_BUDGET_USD = 20.0               # D9: run 5
SONNET_BUDGET_USD = 12.0              # D18: runs 4 + 6 (of the $15 replication budget; the rest is for arm G)
STANDARD = ("questions.json", "questions_extension.json")
HARD = ("questions-hard.json",)
RUNS = {
    1: {"base_model": "claude-sonnet-5-5", "base_effort": "xhigh", "extension_stop_wrong": 13, "pool": STANDARD},
    2: {"base_model": "claude-haiku-5-5", "base_effort": None, "extension_stop_wrong": None, "pool": STANDARD},
    3: {"base_model": "claude-haiku-5-5", "base_effort": None, "extension_stop_wrong": None, "pool": HARD},
    4: {"base_model": "claude-sonnet-5-5", "base_effort": None, "extension_stop_wrong": None, "pool": HARD},
    5: {"base_model": "claude-haiku-5-5", "base_effort": None, "extension_stop_wrong": None, "pool": ("questions-train.json",)},
    6: {"base_model": "claude-sonnet-5-5", "base_effort": None, "extension_stop_wrong": None, "pool": ("questions-train.json",)},
}
# Items dropped after an API refusal (never reworded or retried); see DEVIATIONS.md.
REFUSAL_EXCLUDED = {4: {"h101": "req_011Cgh7v49vVQNR6AgY3EDui"}}   # D21
BUDGET_GROUP = {1: "standard", 2: "standard", 3: "hard", 4: "sonnet", 5: "train", 6: "sonnet"}


def paths(run: int):
    return config.RESULTS / f"pool-run-{run}.json", config.RESULTS / f"pool-run-{run}.md"


def load(run: int) -> dict:
    p, _ = paths(run)
    return json.loads(p.read_text()) if p.exists() else {"records": []}


def process(q: dict) -> dict:
    base = llm.ask_base(q["question"])
    if base.truncated:
        print(f"{q['id']} truncated at max_tokens ${base.usage.cost:.4f}", flush=True)
        return {**q, "model_answer": None, "correct": None, "truncated": True,
                "thinking_tokens": base.thinking_tokens, "request_ids": {"base": base.request_id},
                "usage": {"base": base.usage.as_dict()}, "cost_usd": round(base.usage.cost, 6)}
    # an answer with no parseable FINAL ANSWER line is excluded, not counted as wrong
    rec = {**q, "model_answer": base.answer, "correct": None if base.answer is None else base.answer == q["answer"],
           # deliberation record: archived here, never sent to another call
           "deliberation_record": {"thinking_summary": base.thinking_summary, "visible_answer": base.text},
           "thinking_tokens": base.thinking_tokens,
           "request_ids": {"base": base.request_id},
           "usage": {"base": base.usage.as_dict()}}
    try:
        cs, u = llm.extract_contentions(q["question"], base)
    except llm.RefusalError:
        raise
    except RuntimeError as e:   # e.g. fewer than 5 claims after one retry: excluded, never counted as wrong
        print(f"{q['id']} excluded: {e}", flush=True)
        return {**rec, "correct": None, "excluded_reason": str(e), "cost_usd": round(base.usage.cost, 6)}
    rec["contentions"], rec["usage"]["extract"] = cs, u.as_dict()
    pairs, u, missing = llm.judge_relations(q["question"], cs)
    rec["pairs"], rec["judge_missing_pairs"], rec["usage"]["judge"] = pairs, missing, u.as_dict()
    rec["cost_usd"] = round(sum(v["cost_usd"] for v in rec["usage"].values()), 6)
    print(f"{q['id']} truth={q['answer']} model={base.answer} think_tok={base.thinking_tokens} n={len(cs)} "
          f"rel={sum(p['relation'] != 'unrelated' for p in pairs)} ${rec['cost_usd']:.4f}", flush=True)
    return rec


def session_spend() -> float:
    return UNITEMISED_USD + sum(r["cost_usd"] for run in RUNS for r in load(run)["records"])


def session_spend_with(done: dict, current: int) -> float:
    """Spend counted against the run's cap, using in-memory records for the run in progress.
    Runs 1-2 count against SPEND_STOP_USD (with unitemised calls); runs 3-4 against HARD_BUDGET_USD."""
    group = [r for r in RUNS if BUDGET_GROUP[r] == BUDGET_GROUP[current]]
    other = sum(r["cost_usd"] for run in group if run != current for r in load(run)["records"])
    base = UNITEMISED_USD if BUDGET_GROUP[current] == "standard" else 0
    return base + other + sum(r["cost_usd"] for r in done.values())


def cap(run: int) -> float:
    return {"standard": SPEND_STOP_USD, "hard": HARD_BUDGET_USD, "train": TRAIN_BUDGET_USD,
            "sonnet": SONNET_BUDGET_USD}[BUDGET_GROUP[run]]


def write_usage() -> None:
    lines = ["# Anthropic API usage", "",
             "Prices per MTok: " + ", ".join(f"`{m}` ${a:.2f} in / ${b:.2f} out" for m, (a, b) in config.PRICES.items())
             + ". Thinking tokens bill as output. Extractor `claude-sonnet-5-5`, judge `claude-haiku-5-5` in every run."
             + " This ledger covers the pool runs only; every later run's API cost is stated in its own results file."]
    for run, spec in RUNS.items():
        recs = load(run)["records"]
        if not recs:
            continue
        lines += ["", f"## Pool run {run}: base `{spec['base_model']}`, effort {spec['base_effort'] or 'default'}", "",
                  "| question | base in | base out | extract in | extract out | judge in | judge out | cost USD |",
                  "|---|---|---|---|---|---|---|---|"]
        for r in sorted(recs, key=lambda r: r["id"]):
            u = r["usage"]
            g = lambda step, k: u[step][k] if step in u else "—"
            lines.append(f"| {r['id']}{' (truncated)' if r.get('truncated') else ''} | {g('base', 'input_tokens')} | "
                         f"{g('base', 'output_tokens')} | {g('extract', 'input_tokens')} | {g('extract', 'output_tokens')} | "
                         f"{g('judge', 'input_tokens')} | {g('judge', 'output_tokens')} | {r['cost_usd']:.4f} |")
        lines += ["", f"Run {run} itemised total: ${sum(r['cost_usd'] for r in recs):.4f}"]
    lines += ["", f"Not itemised, about ${UNITEMISED_USD:.2f}: pilot calls made while choosing the base effort level "
              "(8 short calls), the base + refused extractor calls of the two abandoned designs (see DEVIATIONS.md), "
              "and one extension base call that hit the 16,000-token cap before truncation was handled.",
              "", f"**Standard pool, runs 1-2 (incl. unitemised): ${UNITEMISED_USD + sum(r['cost_usd'] for run in (1, 2) for r in load(run)['records']):.2f}** of the ${config.API_BUDGET_USD:.2f} budget.",
              f"**Hard pool, runs 3-4: ${sum(r['cost_usd'] for run in (3, 4) for r in load(run)['records']):.2f}** of the ${HARD_BUDGET_USD:.2f} budget (D6).",
              f"**v2 training pool, run 5: ${sum(r['cost_usd'] for r in load(5)['records']):.2f}** of the ${TRAIN_BUDGET_USD:.2f} budget (D9).",
              f"**Sonnet replication, runs 4 + 6: ${sum(r['cost_usd'] for run in (4, 6) for r in load(run)['records']):.2f}** of the ${SONNET_BUDGET_USD:.2f} pool budget (D18).",
              f"**Session total: ${session_spend():.2f}.**"]
    USAGE_MD.write_text("\n".join(lines) + "\n")


def answer_support(r: dict) -> float:
    """Net support the extracted claims give the model's own answer, in [-1, 1]:
    sum(conf * lean) / sum(conf), signed toward the answer given. Used only by the
    D5 fallback to pick the lowest-confidence correct items."""
    c = np.array([x["confidence"] for x in r["contentions"]])
    l = np.array([x["lean"] for x in r["contentions"]])
    v = float(np.dot(c, l) / c.sum()) if c.sum() else 0.0
    return v if r["model_answer"] == "yes" else -v


def split(records: list[dict], run: int) -> dict:
    wrong = sorted(r["id"] for r in records if r["correct"] is False)
    right = sorted(r["id"] for r in records if r["correct"] is True)
    rng = random.Random(config.SPLIT_SEED)
    if run in (5, 6):   # D9 / D18: the v2 split is made separately (experiments/lock_split_v2.py), not here
        return {"rule": "none (v2 split locked separately in experiments/split-v2.json)", "test_wrong": [],
                "test_right": [], "calibration": [], "excluded_truncated": sorted(r["id"] for r in records if r["correct"] is None)}
    if run >= 3:   # D6: all wrong items (at most 40) + as many right items, both at random
        rule = "D6: all wrong items (at most 40, at random) + an equal number of right items at random (seed 2026)"
        test_wrong = sorted(rng.sample(wrong, min(40, len(wrong))))
        test_right = sorted(rng.sample(right, len(test_wrong)))
    elif len(wrong) >= config.N_TEST_WRONG:
        rule = "random 10 wrong + random 10 right (seed 2026)"
        test_wrong = sorted(rng.sample(wrong, config.N_TEST_WRONG))
        test_right = sorted(rng.sample(right, config.N_TEST_RIGHT))
    else:
        rule = (f"fallback (D5): all {len(wrong)} wrong items + the 10 correct items whose extracted claims "
                "give the model's answer the least net support")
        by_id = {r["id"]: r for r in records}
        test_wrong = wrong
        test_right = sorted(sorted(right, key=lambda q: (answer_support(by_id[q]), q))[: config.N_TEST_RIGHT])
    test = set(test_wrong + test_right)
    return {"rule": rule, "test_wrong": test_wrong, "test_right": test_right,
            "calibration": sorted(r["id"] for r in records if r["id"] not in test and r["correct"] is not None),
            "excluded_truncated": sorted(r["id"] for r in records if r["correct"] is None)}


def main(run: int) -> None:
    spec = RUNS[run]
    config.BASE_MODEL, config.BASE_EFFORT = spec["base_model"], spec["base_effort"]
    out, md = paths(run)
    questions = [q for f in spec["pool"] for q in json.loads((config.EXPERIMENTS / f).read_text())]   # D4, D6
    if run in REFUSAL_EXCLUDED:   # D21: dropped on a refusal, not retried
        questions = [q for q in questions if q["id"] not in REFUSAL_EXCLUDED[run]]
    if run == 6:   # D18: locked v2 test items first, so a budget stop still covers them
        test = set(json.loads((config.EXPERIMENTS / "split-v2.json").read_text())["test"])
        questions = sorted(questions, key=lambda q: (q["id"] not in test, q["id"]))
    if run == 2:   # items that hit the token cap in run 1 are excluded (D5)
        capped = {r["id"] for r in load(1)["records"] if r.get("truncated")}
        questions = [q for q in questions if q["id"] not in capped]
    done = {r["id"]: r for r in load(run)["records"]}
    stop, lock, refusal = threading.Event(), threading.Lock(), {}

    def work(q):
        with lock:
            n_wrong = sum(r["correct"] is False for r in done.values())
            spent = session_spend_with(done, run)
        stop_wrong = spec["extension_stop_wrong"]
        if stop.is_set() or (q["id"].startswith("x") and stop_wrong and n_wrong >= stop_wrong) \
                or spent >= cap(run):
            return
        try:
            rec = process(q)
        except llm.RefusalError as e:
            refusal.setdefault("first", (q, e))
            stop.set()
            return
        with lock:
            done[q["id"]] = rec
            out.write_text(json.dumps({"records": sorted(done.values(), key=lambda r: r["id"])}, indent=1))

    # run 1 is archived: finalise its files from the cache, make no further calls
    todo = [] if run == 1 else [q for q in questions if q["id"] not in done]
    with ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(work, todo))
    if refusal:
        q, e = refusal["first"]
        (config.RESULTS / "refusal.md").write_text(
            f"# Pipeline stopped on a refusal\n\nPool run {run}, question `{q['id']}`: {q['question']}\n\n"
            f"Refused call: **{e.call}**\n\nRequest ID: `{e.request_id}`\n\nExact stop details:\n\n"
            f"```\n{e.stop_details}\n```\n\n{len(done)} questions had completed. Nothing was reworded or "
            "retried; the next step is a support ticket with the request ID.\n")
        print(f"STOPPED: {e}")
        sys.exit(3)
    if session_spend_with(done, run) >= cap(run):
        print(f"spend stop: ${session_spend_with(done, run):.2f}")
    records = sorted(done.values(), key=lambda r: r["id"])
    write_usage()
    n_wrong = sum(r["correct"] is False for r in records)
    n_trunc = sum(r["correct"] is None for r in records)
    s = split(records, run) if n_wrong else None
    out.write_text(json.dumps({"base_model": spec["base_model"], "base_effort": spec["base_effort"],
                               "split": s, "records": records}, indent=1))
    lines = [f"# Pool run {run}: base `{spec['base_model']}` (effort {spec['base_effort'] or 'default'}, adaptive thinking)", "",
             f"{len(records)} questions processed; {n_trunc} hit the 16,000-token cap, gave no FINAL ANSWER or failed claim extraction, and are excluded; "
             f"base model wrong on **{n_wrong}** of {len(records) - n_trunc} answered. "
             f"API cost ${sum(r['cost_usd'] for r in records):.4f}. "
             "Contentions are the claims in the visible answer (DEVIATIONS.md, D1–D3).", ""]
    if s:
        lines += [f"Test set rule: {s['rule']}. Test set: {len(s['test_wrong'])} wrong + {len(s['test_right'])} right. "
                  f"Calibration pool: {len(s['calibration'])} items.", ""]
    else:
        lines += ["No wrong items, so no test set can be formed from this run.", ""]
    lines += ["| id | category | truth | model | correct | set | contentions | related pairs | contradictions |",
              "|---|---|---|---|---|---|---|---|---|"]
    for r in records:
        if r["correct"] is None:
            why = "truncated" if r.get("truncated") else (r.get("excluded_reason") or "no FINAL ANSWER")
            lines.append(f"| {r['id']} | {r['category']} | {r['answer']} | ({why}) | — | excluded | | | |")
            continue
        st = "—" if not s else ("test" if r["id"] in s["test_wrong"] + s["test_right"] else "calib")
        lines.append(f"| {r['id']} | {r['category']} | {r['answer']} | {r['model_answer']} | "
                     f"{'yes' if r['correct'] else '**no**'} | {st} | {len(r['contentions'])} | "
                     f"{sum(p['relation'] != 'unrelated' for p in r['pairs'])} | "
                     f"{sum(p['relation'] == 'contradicts' for p in r['pairs'])} |")
    if n_wrong:
        by_cat = {}
        for r in records:
            if r["correct"] is not None:
                c = by_cat.setdefault(r["category"], [0, 0])
                c[0] += r["correct"] is False
                c[1] += 1
        lines += ["", "Wrong by category: " + ", ".join(f"{k} {w}/{n}" for k, (w, n) in sorted(by_cat.items())), ""]
        lines += ["", "Wrong items:", ""]
        lines += [f"- {r['id']}: {r['question']} (truth {r['answer']}, model {r['model_answer']})"
                  for r in records if r["correct"] is False]
    md.write_text("\n".join(lines) + "\n")
    print(f"run {run}: {len(records)} processed, {n_trunc} truncated, {n_wrong} wrong, session ${session_spend():.2f}")


if __name__ == "__main__":
    main(int(sys.argv[1]))

"""Run the base model, contention extractor and relation judge on the whole
question pool, then fix the test / calibration split.

Questions run one at a time. If any API call is refused, the run stops at once,
records which call and the exact refusal in results/refusal.md, and exits;
nothing is reworded or retried.

Writes results/pool-run-1.json (every trace, contention and pair table),
results/pool-run-1.md, and results/api-usage.md. Re-running skips questions
already processed, so a crash never pays twice."""

import json
import random
import sys

from dotenv import load_dotenv

from entangled_mind import config, llm

load_dotenv(config.ROOT / ".env")
OUT = config.RESULTS / "pool-run-1.json"
MD = config.RESULTS / "pool-run-1.md"
USAGE_MD = config.RESULTS / "api-usage.md"


def process(q: dict) -> dict:
    base = llm.ask_base(q["question"])
    rec = {**q, "model_answer": base.answer, "correct": base.answer == q["answer"],
           "response": base.text, "thinking_tokens": base.thinking_tokens,
           "usage": {"base": base.usage.as_dict()}}
    cs, u = llm.extract_contentions(q["question"], base)
    rec["contentions"], rec["usage"]["extract"] = cs, u.as_dict()
    pairs, u, missing = llm.judge_relations(q["question"], cs)
    rec["pairs"], rec["judge_missing_pairs"], rec["usage"]["judge"] = pairs, missing, u.as_dict()
    rec["cost_usd"] = round(sum(v["cost_usd"] for v in rec["usage"].values()), 6)
    print(f"{q['id']} truth={q['answer']} model={base.answer} think_tok={base.thinking_tokens} n={len(cs)} "
          f"rel={sum(p['relation'] != 'unrelated' for p in pairs)} ${rec['cost_usd']:.4f}", flush=True)
    return rec


def write_usage(records: list[dict]) -> None:
    lines = ["# Anthropic API usage", "",
             f"Base `{config.BASE_MODEL}` (effort {config.BASE_EFFORT}, adaptive thinking), extractor "
             f"`{config.EXTRACTOR_MODEL}`, judge `{config.JUDGE_MODEL}`. Prices per MTok: "
             + ", ".join(f"{m} ${a:.2f} in / ${b:.2f} out" for m, (a, b) in config.PRICES.items())
             + ". Thinking tokens bill as output.", "",
             "| question | base in | base out | extract in | extract out | judge in | judge out | cost USD |",
             "|---|---|---|---|---|---|---|---|"]
    total = 0.0
    for r in sorted(records, key=lambda r: r["id"]):
        u = r["usage"]
        total += r["cost_usd"]
        lines.append(f"| {r['id']} | {u['base']['input_tokens']} | {u['base']['output_tokens']} | "
                     f"{u['extract']['input_tokens']} | {u['extract']['output_tokens']} | "
                     f"{u['judge']['input_tokens']} | {u['judge']['output_tokens']} | {r['cost_usd']:.4f} |")
    lines += ["", f"**Total: ${total:.4f}** of the ${config.API_BUDGET_USD:.2f} session budget.",
              "", "Not itemised: pilot calls made while choosing the base effort level (8 short calls, about $0.03), "
              "and one refused extractor call from the abandoned thinking-trace design (see DEVIATIONS.md)."]
    USAGE_MD.write_text("\n".join(lines) + "\n")


def split(records: list[dict]) -> dict:
    wrong = sorted(r["id"] for r in records if not r["correct"])
    right = sorted(r["id"] for r in records if r["correct"])
    rng = random.Random(config.SPLIT_SEED)
    test_wrong = sorted(rng.sample(wrong, min(config.N_TEST_WRONG, len(wrong))))
    test_right = sorted(rng.sample(right, config.N_TEST_RIGHT))
    test = set(test_wrong + test_right)
    return {"test_wrong": test_wrong, "test_right": test_right,
            "calibration": sorted(r["id"] for r in records if r["id"] not in test)}


def main() -> None:
    questions = json.loads((config.EXPERIMENTS / "questions.json").read_text())
    done = {r["id"]: r for r in json.loads(OUT.read_text())["records"]} if OUT.exists() else {}
    todo = [q for q in questions if q["id"] not in done]
    for q in todo:
        try:
            rec = process(q)
        except llm.RefusalError as e:
            (config.RESULTS / "refusal.md").write_text(
                f"# Pipeline stopped on a refusal\n\nQuestion `{q['id']}`: {q['question']}\n\n"
                f"Refused call: **{e.call}**\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\n"
                f"{len(done)} questions had completed. Nothing was reworded or retried.\n")
            print(f"STOPPED: {e}")
            sys.exit(3)
        done[rec["id"]] = rec
        OUT.write_text(json.dumps({"records": sorted(done.values(), key=lambda r: r["id"])}, indent=1))
    records = sorted(done.values(), key=lambda r: r["id"])
    write_usage(records)
    n_wrong = sum(not r["correct"] for r in records)
    print(f"{len(records)} processed, {n_wrong} wrong")
    if n_wrong < config.N_TEST_WRONG:
        print("not enough wrong items for the test set; pool must be extended")
        OUT.write_text(json.dumps({"records": records}, indent=1))
        sys.exit(2)
    s = split(records)
    OUT.write_text(json.dumps({"split": s, "records": records}, indent=1))
    total = sum(r["cost_usd"] for r in records)
    lines = ["# Pool run 1: base model on the question pool", "",
             f"{len(records)} questions; base model wrong on {n_wrong}. API cost ${total:.4f}. "
             f"Contentions come from the visible written response only (see DEVIATIONS.md).", "",
             f"Test set: {len(s['test_wrong'])} wrong + {len(s['test_right'])} right, drawn with seed {config.SPLIT_SEED}. "
             f"Calibration pool: {len(s['calibration'])} items.", "",
             "| id | category | truth | model | correct | set | contentions | related pairs | contradictions |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in records:
        st = "test" if r["id"] in s["test_wrong"] + s["test_right"] else "calib"
        lines.append(f"| {r['id']} | {r['category']} | {r['answer']} | {r['model_answer']} | "
                     f"{'yes' if r['correct'] else '**no**'} | {st} | {len(r['contentions'])} | "
                     f"{sum(p['relation'] != 'unrelated' for p in r['pairs'])} | "
                     f"{sum(p['relation'] == 'contradicts' for p in r['pairs'])} |")
    lines += ["", "Wrong items:", ""]
    lines += [f"- {r['id']}: {r['question']} (truth {r['answer']}, model {r['model_answer']})"
              for r in records if not r["correct"]]
    MD.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

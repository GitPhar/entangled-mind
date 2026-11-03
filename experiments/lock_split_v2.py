"""Lock the v2 train / validation / test split (60 / 20 / 20, seed 2026),
stratified by wrong/right x item type, from pool run 5. Run once, before any
fitting; refuses to overwrite an existing split (never re-split).

    python experiments/lock_split_v2.py

Writes experiments/split-v2.json. The run-2 80-item test set (pool run 3) stays
a separate held-out set and is listed in the file for reference."""

import json
import random
import sys

from entangled_mind import config

POOL = config.RESULTS / "pool-run-5.json"
RUN2_POOL = config.RESULTS / "pool-run-3.json"
OUT = config.EXPERIMENTS / "split-v2.json"


def kind(cat: str) -> str:
    return "science" if cat.startswith("science") else cat.split("-")[0]


def main() -> None:
    if OUT.exists():
        sys.exit(f"{OUT} already exists; the v2 split is locked and is never re-made.")
    recs = [r for r in json.loads(POOL.read_text())["records"] if r["correct"] is not None]
    strata: dict[tuple, list[str]] = {}
    for r in recs:
        strata.setdefault((r["correct"] is False, kind(r["category"])), []).append(r["id"])
    rng = random.Random(config.SPLIT_SEED)
    split = {"train": [], "validation": [], "test": []}
    table = []
    for key in sorted(strata):
        ids = sorted(strata[key])
        rng.shuffle(ids)
        n = len(ids)
        n_tr, n_va = round(0.6 * n), round(0.2 * n)
        split["train"] += ids[:n_tr]
        split["validation"] += ids[n_tr:n_tr + n_va]
        split["test"] += ids[n_tr + n_va:]
        table.append({"wrong": key[0], "type": key[1], "n": n, "train": n_tr, "validation": n_va,
                      "test": n - n_tr - n_va})
    run2 = json.loads(RUN2_POOL.read_text())["split"]
    out = {"seed": config.SPLIT_SEED, "source": "results/pool-run-5.json", "strata": table,
           **{k: sorted(v) for k, v in split.items()},
           "excluded_no_answer": sorted(r["id"] for r in json.loads(POOL.read_text())["records"] if r["correct"] is None),
           "run2_heldout": {"test_wrong": run2["test_wrong"], "test_right": run2["test_right"],
                            "source": "results/pool-run-3.json (never used for fitting)"}}
    OUT.write_text(json.dumps(out, indent=1))
    for t in table:
        print(t)
    print({k: len(v) for k, v in split.items()})


if __name__ == "__main__":
    main()

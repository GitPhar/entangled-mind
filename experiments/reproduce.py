"""Regenerate every results table from the archived JSON, with no API key and no IBM token,
and verify it matches the committed files.

    python experiments/reproduce.py [--emit DIR]   # --emit keeps the regenerated tables in DIR

1. Snapshots results/ and experiments/ at git HEAD into a temporary directory, so runs in
   progress in the working tree cannot leak in.
2. Blocks every network client: llm.client() and backends.service() raise. Any table that
   would need a live call fails loudly instead of silently re-querying.
3. Points the package at the snapshot and runs each table's writer from its archived JSON
   (caches for the conversation-based experiments; exact recomputation for the
   simulation-only checks).
4. Compares each regenerated file with the committed one. Hand-written "## Reading" sections
   (analysis prose appended after a run) are not generated and are excluded from the
   comparison; everything above them must match byte for byte.

Exit status 0 if every table matches. Pool runs still in progress (Sonnet runs 4 and 6) and
plain logs (job status, refusals) are listed and skipped."""

import difflib
import importlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "experiments")]
for k in ("ANTHROPIC_API_KEY", "IBM_QUANTUM_TOKEN"):
    os.environ.pop(k, None)

from entangled_mind import backends, config, llm  # noqa: E402

READING = "\n## Reading"
SKIPPED = {
    "pool-run-6.md": "Sonnet training-pool run halted on a refusal (D25); no table written",
    "sonnet-ablation.md": "assembled by two writers (Addenda D and E) with a hand-written Reading between them",
    "refusal-sonnet-replication-2.md": "log of a refused call",
    "ibm-job-status-log.md": "log of status checks, not a table",
    "refusal-attempt-2.md": "log of a refused call",
    "refusal.md": "log of a refused call",
    "multi-model.md": "hand-written summary of the multi-model replications (DM5)",
    "probe-dissociation.md": "hand-written write-up (DP1); its numbers are in probe-dissociation.json, which the probe step recomputes",
    "refusal-sonnet-replication.md": "log of a refused call",
}


def blocked(*_, **__):
    raise RuntimeError("reproduce.py: network access is blocked (tables must come from archived JSON)")


def snapshot() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="entangled-mind-reproduce-"))
    data = subprocess.run(["git", "-C", str(ROOT), "archive", "HEAD", "results", "experiments"],
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        tf.extractall(tmp, filter="data")
    return tmp


PLAIN = "\n## In plain English\n"
EXPLORATORY = "\n# Exploratory re-analysis"


def generated_part(text: str) -> str:
    text = text.split(READING, 1)[0]
    text = text.split(EXPLORATORY, 1)[0]   # hand-written exploratory tail (calibration-under-format.md, DM6a)
    if PLAIN in text:                   # hand-written plain-English section (overnight gold-map runs, D34)
        head, rest = text.split(PLAIN, 1)
        text = head + PLAIN + ("\n## " + rest.split("\n## ", 1)[1] if "\n## " in rest else "")
    return text.rstrip("\n")


def main() -> int:
    emit = Path(sys.argv[sys.argv.index("--emit") + 1]) if "--emit" in sys.argv else None
    tmp = snapshot()
    committed = {p.name: p.read_text() for p in (tmp / "results").glob("*.md")}
    config.RESULTS, config.EXPERIMENTS = tmp / "results", tmp / "experiments"
    backends.USAGE_MD, backends.USAGE_JSON = config.RESULTS / "ibm-usage.md", config.RESULTS / "ibm-usage.json"
    llm.client = blocked
    backends.service = blocked
    for name in list(committed):
        if name not in SKIPPED:
            (config.RESULTS / name).unlink()     # every table is rebuilt from scratch
    load = lambda f: json.loads((config.RESULTS / f).read_text())
    steps = []

    def step(name, fn):
        steps.append((name, fn))

    def pools():
        rp = importlib.import_module("run_pool")
        for run in (1, 2, 3, 4, 5):
            rp.main(run)
        rp.write_usage()
    step("pool runs 1-5 and api-usage.md", pools)
    step("ibm-usage.md", lambda: backends.render_usage_md(load("ibm-usage.json")))
    step("stage1-run-1.md", lambda: importlib.import_module("stage1_pipe").write_md(load("stage1-run-1.json")))

    def stage2():
        for run in (1, 2):
            sys.argv = ["stage2_run.py", str(run), "--md-only"]
            importlib.reload(importlib.import_module("stage2_run")).md_only()
    step("stage2-run-1.md, stage2-run-2.md", stage2)
    step("stage2-run-2b.md", lambda: importlib.import_module("stage2_rescore").main())
    step("stage2-run-2-split.md", lambda: importlib.import_module("split_analysis").main())
    step("frame-fix-check.md", lambda: importlib.import_module("frame_fix_check").main())
    step("witness-run-1.md", lambda: importlib.import_module("witness_run").write_md(load("witness-run-1.json")))
    step("ibm-calibration.md", lambda: importlib.import_module("ibm_calibration").write_md(load("ibm-calibration.json")))
    step("exp3-run-1.md", lambda: importlib.import_module("exp3_run").main())
    step("exp4-run-1.md", lambda: importlib.import_module("exp4_run").main())
    step("exp4-run-2.md", lambda: importlib.import_module("exp4_graded").main())

    step("exp5-pilot.md", lambda: importlib.import_module("exp5_run").cmd_pilot())
    step("exp5-run-1.md", lambda: importlib.import_module("exp5_analyse").md_only())
    step("exp4-run-3.md", lambda: importlib.import_module("exp4_run3").main())          # all calls cached: no API use
    step("exp5-run-2.md", lambda: importlib.import_module("exp5_rerun").main())          # all calls cached: no API use
    if "exp5-verdict-reissue.md" in committed:     # D52: run 1's verdict on the single-direction q
        step("exp5-verdict-reissue.md", lambda: importlib.import_module("exp5_reissue").main())
    step("gm9-nsit.md", lambda: importlib.import_module("gm9_nsit").main())
    if "gm3c-heldout-format.md" in committed:
        step("gm3c-heldout-format.md", lambda: importlib.import_module("gm3c_heldout_format").main())
    step("gm3a-anchor-gap.md", lambda: importlib.import_module("gm3a_anchor_gap").main())
    for mod, md in (("gm1_self_knowledge", "gm1-self-knowledge.md"), ("gm2_self_conditioning", "gm2-self-conditioning.md"),
                    ("gm3b_format_invariance", "gm3b-format-invariance.md"), ("gm4_evidence_seeking", "gm4-evidence-seeking.md"),
                    ("gm2b_self_conditioning_40", "gm2b-self-conditioning-40.md")):
        if md in committed:          # overnight runs: analysis recomputed from the call caches
            step(md, lambda mod=mod: importlib.import_module(mod).analyse())
    for fn, md in (("bm3", "bm3-confirmation.md"), ("bm7", "bm7-serial-position.md"), ("bm9", "bm9-contrast.md")):
        if md in committed:          # biomimetic $0 analyses (D40-D42)
            step(md, lambda fn=fn: getattr(importlib.import_module("bm_offline"), fn)())
    for fn, md in (("bm2_analyse", "bm2-sampling-identity.md"), ("bm1_analyse", "bm1-serial-dependence.md")):
        if md in committed:          # biomimetic runs (D43-D44), from their call caches
            step(md, lambda fn=fn: getattr(importlib.import_module("bm_runs"), fn)())
    if "bm0-source-distance-lag.md" in committed:     # D47, from its call cache
        step("bm0-source-distance-lag.md", lambda: importlib.import_module("bm0_source_distance_lag").analyse())
    for mod, md in (("mm_gm1", "mm-gm1-self-knowledge.md"), ("mm_gm2", "mm-gm2-self-conditioning.md"),
                    ("mm_gm3b", "mm-gm3b-format-invariance.md"), ("cal_format", "calibration-under-format.md"),
                    ("mm_gm3b_opus_complete", "mm-gm3b-opus-completion.md")):
        if md in committed:          # multi-model replications (DM1-DM6, D49), from their batch caches
            step(md, lambda mod=mod: importlib.import_module(mod).analyse())
    if "probe-dissociation.md" in committed:     # DP1: the verdict from the archived probe runs (no model needed)
        step("probe-dissociation.json", lambda: importlib.import_module("probe_dissociation").cmd_analyse("llama3-8b"))
    if "mm-gm3b-opus-completion-with-h291.md" in committed:     # D49a sensitivity
        step("mm-gm3b-opus-completion-with-h291.md", lambda: importlib.import_module("mm_gm3b_opus_complete").analyse_with_h291())

    def sonnet():
        sys.argv = ["sonnet_replication.py", "--offline"]
        importlib.import_module("sonnet_replication").offline()
    step("sonnet-replication.md", sonnet)

    def v2():
        vf = importlib.import_module("v2_fit")
        d = load("v2-run-1.json")
        vf.write_md(d["fit"], d["results"], d["primary_pass"])
        d = load("v2.1-run-1.json")
        vf.write21_md(d["fit"], d["results"], d["primary_pass"])
    step("v2-run-1.md, v2.1-run-1.md", v2)

    failures = []
    for name, fn in steps:
        try:
            with redirect_stdout(io.StringIO()):
                fn()
            print(f"  ran   {name}")
        except Exception as e:  # noqa: BLE001
            failures.append(f"{name}: {type(e).__name__}: {e}")
            print(f"  FAIL  {name}: {e}")
    ok = True
    print("\nComparison with the committed tables (generated part, above any '## Reading'):")
    for name in sorted(committed):
        if name in SKIPPED:
            print(f"  skip  {name}  ({SKIPPED[name]})")
            continue
        new = config.RESULTS / name
        if not new.exists():
            print(f"  MISSING {name}")
            ok = False
            continue
        same = generated_part(new.read_text()) == generated_part(committed[name])
        has_reading = READING in committed[name]
        print(f"  {'match' if same else 'DIFF '} {name}{'  (+ hand-written Reading, not compared)' if has_reading else ''}")
        if not same:
            d = difflib.unified_diff(generated_part(committed[name]).splitlines(), generated_part(new.read_text()).splitlines(),
                                     "committed", "regenerated", n=0, lineterm="")
            print("        " + "\n        ".join(list(d)[2:10]))
        ok &= same
    if emit:                            # keep the regenerated tables for inspection
        emit.mkdir(parents=True, exist_ok=True)
        for p in (config.RESULTS).glob("*.md"):
            shutil.copy(p, emit / p.name)
    shutil.rmtree(tmp)
    if failures:
        print("\nFailed steps:\n  " + "\n  ".join(failures))
    print("\nALL TABLES REPRODUCED" if ok and not failures else "\nREPRODUCTION INCOMPLETE")
    return 0 if ok and not failures else 1


if __name__ == "__main__":
    sys.exit(main())

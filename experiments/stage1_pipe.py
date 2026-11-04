"""Stage 1 gate: one real IBM circuit returning counts.

Takes the first pool item (q01; the pipe test does not depend on the split), encodes it with entangling gates and N=0
evolution (the smoke test), and runs the identical transpiled circuit on the
noisy simulator, the ideal simulator, and once on real hardware."""

import json

from entangled_mind import backends, config, encoder, readout

POOL = config.RESULTS / "pool-run-1.json"


def main() -> None:
    pool = json.loads(POOL.read_text())
    recs = {r["id"]: r for r in pool["records"]}
    rec = recs["q01"]
    web = encoder.build_web(rec["contentions"], rec["pairs"])
    qc = encoder.build_circuit(web, entangle=True, n_trotter=0)
    isa = backends.transpile(qc)
    ops = dict(isa.count_ops())

    ideal = backends.run_ideal(qc)
    noisy = backends.run_noisy(isa)
    hw_counts, usage = backends.run_hardware([isa], purpose="Stage 1 pipe test (1 circuit)")
    hw = hw_counts[0]

    out = {
        "item": {k: rec[k] for k in ("id", "question", "answer", "model_answer", "correct")},
        "n_qubits": web.n, "n_edges": len(web.edges), "transpiled_ops": ops, "depth": isa.depth(),
        "arms": {name: {"counts": c, "readout": readout.quantum_readout(c, web)}
                 for name, c in (("ideal_sim", ideal), ("noisy_sim", noisy), ("hardware", hw))},
        "ibm_usage": usage,
    }
    (config.RESULTS / "stage1-run-1.json").write_text(json.dumps(out, indent=1))
    write_md(out)


def write_md(out: dict) -> None:
    """Stage 1 markdown, from the archived JSON alone."""
    usage, item = out["ibm_usage"], out["item"]
    hw = out["arms"]["hardware"]["counts"]
    qsec = float((usage.get("job_metrics_usage") or {}).get("qpu_charge_time_seconds", usage["quantum_seconds"]))
    top = sorted(hw.items(), key=lambda kv: -kv[1])[:8]
    lines = ["# Stage 1, run 1: the pipe", "",
             f"Item `{item['id']}`: {item['question']}", "",
             f"Encoded as {out['n_qubits']} qubits with {out['n_edges']} entangling RZZ gates and N=0 evolution. "
             f"Transpiled for `{usage['backend']}`: depth {out['depth']}, {out['transpiled_ops'].get('cz', 0)} CZ gates.", "",
             f"**Hardware job `{usage['job_id']}` on `{usage['backend']}` returned {sum(hw.values())} shots "
             f"across {len(hw)} distinct bitstrings. QPU time: {qsec:g} s (IBM `qpu_charge_time_seconds`).**", "",
             "| run | P(yes) | judgment | conflict score | distinct bitstrings |", "|---|---|---|---|---|"]
    for name, a in out["arms"].items():
        r = a["readout"]
        lines.append(f"| {name} | {r['p_yes']:.3f} | {r['judgment']} | {r['conflict_score']:.3f} | {len(a['counts'])} |")
    lines += ["", "Most frequent hardware bitstrings (qubit 0 rightmost; 0 = yes-aligned):", ""]
    lines += [f"- `{b}`: {c}" for b, c in top]
    (config.RESULTS / "stage1-run-1.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

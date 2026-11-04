"""Experiment 5, run 1: the §7.5 verdict re-issued on the single-direction QQ statistic (DEVIATIONS.md D52).

    python experiments/exp5_reissue.py

Run 1's verdict, TIE, used the QQ mean q pooled over both scale directions (anchors a and b). Run 2 (D33) and the
audit (audits/exp5-run-1.md) show that pooled value is the cancellation of two opposite-signed directions. This
re-applies the frozen §7.3/§7.5 rules, and the frozen code (exp5_analyse.qq_check and the verdict precedence of
exp5_analyse.main), to run 1's anchor-(a) conversations only: 0 = certainly false, 100 = certainly true, the
project's one scale direction. Nothing is refitted: the primary (§7.2) and the Kvam check are read from
results/exp5-run-1.json. Anchor (b) is reported alongside. Writes results/exp5-verdict-reissue.{json,md}. No API calls."""

import json

import exp5_analyse as a
import exp5_run as er
from entangled_mind import config

OUT_JSON, OUT_MD = config.RESULTS / "exp5-verdict-reissue.json", config.RESULTS / "exp5-verdict-reissue.md"
# The single-direction q the audit recomputed with independent code (audits/exp5-run-1.md, claims row 10; SUMMARY.md)
AUDIT_Q = {"anchor": "a", "n_large_OE": 32, "mean_q": -0.345, "mean_q_ci95": [-0.517, -0.181]}


def verdict(primary, contradicted):
    """exp5_analyse.main's §7.5 precedence, for a primary that is not a pass."""
    if primary == "tie" and not contradicted:
        return "tie"
    if primary == "classical" or contradicted:
        return "classical"
    return "tie"


def main():
    run1 = json.loads(a.OUT_JSON.read_text())
    split = json.loads(er.SPLIT.read_text())
    recs = {r["id"]: r for r in json.loads(a.POOL.read_text())["records"]}
    conv = json.loads(a.CONV.read_text())
    keep = lambda d: {k: d[k] for k in ("n_pairs", "n_large_OE", "mean_q", "mean_q_ci95", "KS_D", "KS_p",
                                        "signature_present", "signature_contradicted")}
    by_anchor = {an: keep(a.qq_check(split["candidates"], recs, {k: v for k, v in conv.items() if v.get("anchor") == an},
                                     split)) for an in ("a", "b")}
    audit_contra = AUDIT_Q["mean_q_ci95"][0] > 0 or AUDIT_Q["mean_q_ci95"][1] < 0
    contra = audit_contra or run1["kvam"]["commitment"]          # D26 addendum: Kvam commitment also counts
    out = {"primary": run1["primary"], "primary_delta_F5_minus_A5": run1["evals"]["test"]["delta_F5_minus_A5"],
           "kvam_commitment": run1["kvam"]["commitment"], "kvam_signature_present": run1["kvam"]["signature_present"],
           "pooled_qq": keep(run1["qq"]), "verdict_as_issued": run1["verdict"],
           "audit_single_direction_q": AUDIT_Q, "audit_q_contradicted": audit_contra,
           "frozen_code_by_anchor": by_anchor,
           "verdict_reissued": verdict(run1["primary"], contra),
           "verdict_reissued_frozen_code_check": verdict(run1["primary"],
                                                         by_anchor["a"]["signature_contradicted"] or run1["kvam"]["commitment"])}
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float))
    write_md(out)


def ci(c):
    return f"[{c[0]:+.3f}, {c[1]:+.3f}]"


def write_md(o):
    p, aq, fa, fb = o["pooled_qq"], o["audit_single_direction_q"], o["frozen_code_by_anchor"]["a"], o["frozen_code_by_anchor"]["b"]
    d = o["primary_delta_F5_minus_A5"]
    L = ["# Experiment 5, run 1: verdict re-issued on the single-direction QQ statistic", "",
         "DEVIATIONS.md D52. The frozen §7.3 and §7.5 rules of `experiments/exp5-sequential-judgment.md`, applied by the frozen "
         "code (`exp5_analyse.qq_check` and its verdict precedence) to run 1's anchor-(a) conversations: 0 = certainly false, "
         "100 = certainly true. Nothing refitted; no API calls.", "",
         "## In plain English", "",
         "(Hand-written; excluded from reproduce.py's comparison.)", "",
         "## Inputs (§7.5)", "",
         f"- Primary (§7.2), unchanged: **{o['primary'].upper()}**, F5 − A5 = {d[0]:+.1f} [{d[1]:+.1f}, {d[2]:+.1f}] rating points².",
         f"- Kvam (§7.4), unchanged: signature present **{o['kvam_signature_present']}**, commitment **{o['kvam_commitment']}**.",
         "", "## QQ mean q on the large-order-effect pairs (§7.3)", "",
         "| data | pairs with OE > 0.10, CI excluding 0 | mean q [95% CI] | contradicted (CI excludes 0) |", "|---|---|---|---|",
         f"| both directions pooled (as issued) | {p['n_large_OE']} | {p['mean_q']:+.3f} {ci(p['mean_q_ci95'])} | {p['signature_contradicted']} |",
         f"| **anchor (a) only, the audit's recomputation (verdict basis)** | {aq['n_large_OE']} | **{aq['mean_q']:+.3f} {ci(aq['mean_q_ci95'])}** | **{o['audit_q_contradicted']}** |",
         f"| anchor (a) only, frozen `qq_check` | {fa['n_large_OE']} | {fa['mean_q']:+.3f} {ci(fa['mean_q_ci95'])} | {fa['signature_contradicted']} |",
         f"| anchor (b) only, frozen `qq_check` (reported, not used) | {fb['n_large_OE']} | {fb['mean_q']:+.3f} {ci(fb['mean_q_ci95'])} | {fb['signature_contradicted']} |",
         "", "## Verdict (§7.5)", "",
         f"- As issued on the pooled q (superseded): **{o['verdict_as_issued'].upper()}**.",
         f"- Re-issued on the single-direction q: **{o['verdict_reissued'].upper()}** "
         f"(the frozen-code recomputation gives **{o['verdict_reissued_frozen_code_check'].upper()}**).",
         "- Rule: \"classical: primary classical, or a signature contradicted with the primary not a pass\". The primary is a "
         "tie, not a pass, and the QQ signature is contradicted."]
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()

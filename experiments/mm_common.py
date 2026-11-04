"""Shared pieces for the multi-model replications (DEVIATIONS.md, DM1-DM5) and the calibration demonstration (DM6).

All calls go through the Message Batches API (50% of list price). The stopping rules of the overnight Caller are kept:
- a budget cap per run, enforced in code before every batch is submitted (projected cost of the batch must fit);
- the run stops at the first refusal: the batch containing it is archived, nothing further is submitted, the refused request
  is written to results/refusal-<label>.md with its message ID, and nothing is reworded or retried;
- a request that comes back errored or expired (an API failure, not a model output) is resubmitted unchanged, at most twice;
- a response that hits max_tokens is recorded as no answer (as in D36 amendment 2).

Batch results carry a message ID (msg_...) and the batch ID rather than an HTTP request ID; both are archived per call.

Model settings ("off" = the paper's thinking-off setting, as close as each model allows; "default" = no thinking parameter):
- claude-haiku-5-5:  off = thinking disabled (as in every overnight run)
- claude-sonnet-5-5: off = thinking {"type": "between_tools"} (Sonnet 5.5 rejects "disabled"; between_tools is its thinking-off mode)
- claude-opus-5-5:   off = effort "low" (Opus 5.5 cannot disable thinking; low effort is the minimum; thinking text is never returned
                     and never placed in any later turn)
"""

import json
import sys
import time

from dotenv import load_dotenv

from entangled_mind import config, llm

load_dotenv(config.ROOT / ".env")
H, S, O = "claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"
SHORT = {H: "haiku", S: "sonnet", O: "opus"}
DISCOUNT = 0.5
OFF = {H: {"thinking": {"type": "disabled"}}, S: {"thinking": {"type": "between_tools"}}, O: {"output_config": {"effort": "low"}}}


def params(model, messages, schema=None, max_tokens=1000, mode="off", system=None):
    p = {"model": model, "max_tokens": max_tokens, "messages": messages}
    extra = json.loads(json.dumps(OFF[model])) if mode == "off" else {}
    oc = extra.pop("output_config", {})
    if schema is not None:
        oc["format"] = {"type": "json_schema", "schema": schema}
    if oc:
        p["output_config"] = oc
    if system:
        p["system"] = system
    p.update(extra)
    return p


def cost_of(msg) -> float:
    pin, pout = config.PRICES[llm._model_of(msg)]
    return DISCOUNT * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6


def text_of(msg) -> str:
    return "".join(b.text for b in msg.content if b.type == "text")


class Stop(Exception):
    pass


class BatchRunner:
    """Submits {key: params} through the Batches API in chunks, with the cap and refusal rules above.
    on_result(key, msg) -> dict parses a successful, non-refused message into the record that is stored."""

    def __init__(self, label, cap_usd, spent_fn, chunk=1500, poll=20):
        self.label, self.cap, self.spent_fn, self.chunk, self.poll = label, cap_usd, spent_fn, chunk, poll
        self.log_path = config.RESULTS / f"mm-batches-{label}.json"
        self.log = json.loads(self.log_path.read_text()) if self.log_path.exists() else []

    def _submit_wait(self, reqs):
        idmap = {f"r{n}": k for n, k in enumerate(reqs)}
        b = llm.client().messages.batches.create(requests=[{"custom_id": c, "params": reqs[k]} for c, k in idmap.items()])
        t0 = time.time()
        print(f"{self.label}: batch {b.id} submitted, {len(reqs)} requests", flush=True)
        while True:
            b = llm.client().messages.batches.retrieve(b.id)
            if b.processing_status == "ended":
                break
            time.sleep(self.poll)
        print(f"{self.label}: batch {b.id} ended after {time.time() - t0:.0f}s: {b.request_counts}", flush=True)
        out = {}
        for r in llm.client().messages.batches.results(b.id):
            out[idmap[r.custom_id]] = r.result
        self.log.append({"batch": b.id, "n": len(reqs), "seconds": round(time.time() - t0)})
        self.log_path.write_text(json.dumps(self.log, indent=1))
        return b.id, out

    def run(self, reqs, on_result, store, save, est_per_req):
        """reqs: {key: params}; store(key, record); save() persists. Returns the observed mean cost per request."""
        keys, costs, refusal = list(reqs), [], None
        for start in range(0, len(keys), self.chunk):
            part = {k: reqs[k] for k in keys[start:start + self.chunk]}
            for attempt in range(3):
                est = len(part) * (max(est_per_req, (sum(costs) / len(costs)) if costs else 0) * 1.25)
                if self.spent_fn() + est > self.cap:
                    save()
                    raise Stop(f"{self.label}: budget cap ${self.cap} would be exceeded "
                               f"(spent ${self.spent_fn():.3f} + projected ${est:.3f}); stopped before submitting")
                bid, res = self._submit_wait(part)
                retry = {}
                for k, r in res.items():
                    if r.type != "succeeded":
                        retry[k] = part[k]
                        continue
                    m = r.message
                    c = cost_of(m)
                    costs.append(c)
                    if m.stop_reason == "refusal":
                        refusal = refusal or (k, m, bid)
                        store(k, {"refused": True, "cost": c, "msg_id": m.id, "batch": bid})
                    elif m.stop_reason == "max_tokens":
                        store(k, {"value": None, "error": "max_tokens", "cost": c, "msg_id": m.id, "batch": bid})
                    else:
                        rec = on_result(k, m)
                        rec.update(cost=c, msg_id=m.id, batch=bid)
                        store(k, rec)
                save()
                if refusal:
                    k, m, bid = refusal
                    (config.RESULTS / f"refusal-mm-{self.label}.md").write_text(
                        f"# Run stopped on a refusal\n\n{self.label}, job `{k}`\n\nBatch `{bid}`, message ID `{m.id}`, "
                        f"model `{m.model}`\n\nExact stop details:\n\n```\n{m.stop_details}\n```\n\n"
                        "Nothing was reworded or retried, and no further batch was submitted.\n")
                    raise Stop(f"{self.label}: STOPPED on a refusal ({k}, {m.id})")
                if not retry:
                    break
                print(f"{self.label}: {len(retry)} errored/expired requests resubmitted unchanged", flush=True)
                part = retry
            else:
                save()
                raise Stop(f"{self.label}: requests still failing after two resubmissions: {list(part)[:3]}")
        return (sum(costs) / len(costs)) if costs else est_per_req


def main_guard(fn):
    try:
        fn()
    except Stop as e:
        sys.exit(str(e))

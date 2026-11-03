"""Language-model side of the pipeline: base answer, contention extraction,
pairwise relation judging. Every call returns its token usage so callers can
log cost per question."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

import anthropic

from . import config

_client: anthropic.Anthropic | None = None


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(max_retries=4)
    return _client


@dataclass
class Usage:
    model: str
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def cost(self) -> float:
        pin, pout = config.PRICES[self.model]
        return (self.input_tokens * pin + self.output_tokens * pout) / 1e6

    def as_dict(self) -> dict:
        return {"model": self.model, "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens, "cost_usd": round(self.cost, 6)}


def _usage(resp) -> Usage:
    return Usage(_model_of(resp), resp.usage.input_tokens, resp.usage.output_tokens)


def _model_of(resp) -> str:
    for m in config.PRICES:
        if resp.model.startswith(m):
            return m
    raise ValueError(f"no price for {resp.model}")


class RefusalError(RuntimeError):
    """Raised when the API refuses a call. The pipeline stops on this; it never rewords or retries."""

    def __init__(self, call: str, resp):
        self.call, self.stop_details = call, resp.stop_details
        super().__init__(f"{call} call refused (model {resp.model}): {resp.stop_details}")


def _check_stop(resp, call: str) -> None:
    if resp.stop_reason == "refusal":
        raise RefusalError(call, resp)
    if resp.stop_reason == "max_tokens":
        raise RuntimeError(f"{call} call hit max_tokens")


# --- 1. base model ---------------------------------------------------------

BASE_PROMPT = """Answer the following yes/no question.
In your response, reason step by step in writing: lay out the considerations on each side, work through any calculation, and say which considerations you accept or reject and why. Then give your answer.
End your response with a final line that is exactly "FINAL ANSWER: YES" or "FINAL ANSWER: NO".

Question: {question}"""


@dataclass
class BaseAnswer:
    text: str                   # the visible written response - the only text used downstream
    answer: str | None          # "yes" / "no" / None if unparseable
    thinking_tokens: int        # thinking stays on; its content is never requested or stored
    usage: Usage


def ask_base(question: str) -> BaseAnswer:
    resp = client().messages.create(
        model=config.BASE_MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive", "display": "omitted"},
        output_config={"effort": config.BASE_EFFORT},
        messages=[{"role": "user", "content": BASE_PROMPT.format(question=question)}],
    )
    _check_stop(resp, "base")
    text = "\n".join(b.text for b in resp.content if b.type == "text").strip()
    m = re.findall(r"FINAL ANSWER:\s*(YES|NO)", text, flags=re.I)
    details = getattr(resp.usage, "output_tokens_details", None)
    return BaseAnswer(text, m[-1].lower() if m else None,
                      int(getattr(details, "thinking_tokens", 0) or 0), _usage(resp))


# --- 2. contention extraction ---------------------------------------------

EXTRACT_SYSTEM = """You decompose a written answer to a yes/no question into discrete contentions.
A contention is one distinct claim, consideration, intuition, or sub-conclusion stated in the written reasoning - including ones the writer raised and then rejected.
For each contention give:
- text: one short sentence stating it.
- confidence: 0 to 1, how strongly the writer endorsed it in the end (a rejected idea gets a low value).
- lean: -1 to 1, which way the contention pushes the answer if it is taken as true: positive toward YES, negative toward NO, 0 if it bears on neither.
Report only what is in the reasoning. Do not add your own considerations and do not judge whether the writer was correct.
Return between 5 and 16 contentions."""

EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "contentions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "confidence": {"type": "number"},
                    "lean": {"type": "number"},
                },
                "required": ["text", "confidence", "lean"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["contentions"],
    "additionalProperties": False,
}


def _json_call(model: str, effort: str, system: str, user: str, schema: dict, call: str):
    resp = client().messages.create(
        model=model,
        max_tokens=16000,
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    _check_stop(resp, call)
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text), _usage(resp)


def _clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, float(x)))


def extract_contentions(question: str, base: BaseAnswer) -> tuple[list[dict], Usage]:
    # Only the visible written response is passed on; thinking content never is.
    user = f"Question: {question}\n\n<response>\n{base.text}\n</response>"
    total = Usage(config.EXTRACTOR_MODEL)
    for _ in range(2):
        data, u = _json_call(config.EXTRACTOR_MODEL, config.EXTRACTOR_EFFORT,
                             EXTRACT_SYSTEM, user, EXTRACT_SCHEMA, "extractor")
        total.input_tokens += u.input_tokens
        total.output_tokens += u.output_tokens
        cs = [{"text": c["text"].strip(),
               "confidence": _clip(c["confidence"], 0, 1),
               "lean": _clip(c["lean"], -1, 1)} for c in data["contentions"] if c["text"].strip()]
        if len(cs) >= config.MIN_CONTENTIONS:
            return cs[: config.MAX_CONTENTIONS], total
    raise RuntimeError(f"extractor returned {len(cs)} contentions")


# --- 3. pairwise relation judge -------------------------------------------

JUDGE_SYSTEM = """You judge how pairs of contentions from one written answer relate to each other.
For every pair (i, j) with i < j, decide:
- "supports": if one is true, the other becomes more plausible, or they push toward the same conclusion for linked reasons.
- "contradicts": they cannot both be fully true, or one undercuts the other.
- "unrelated": neither.
strength: 0 to 1, how strong the relation is (use 0 for unrelated).
Return every pair exactly once."""

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "pairs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "i": {"type": "integer"},
                    "j": {"type": "integer"},
                    "relation": {"type": "string", "enum": ["supports", "contradicts", "unrelated"]},
                    "strength": {"type": "number"},
                },
                "required": ["i", "j", "relation", "strength"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["pairs"],
    "additionalProperties": False,
}


def judge_relations(question: str, contentions: list[dict]) -> tuple[list[dict], Usage, int]:
    """Returns the full i<j pair table, usage, and how many pairs the judge omitted
    (filled in as unrelated)."""
    n = len(contentions)
    listing = "\n".join(f"{k}: {c['text']}" for k, c in enumerate(contentions))
    user = (f"Question being reasoned about: {question}\n\nContentions:\n{listing}\n\n"
            f"There are {n} contentions, so {n * (n - 1) // 2} pairs.")
    data, usage = _json_call(config.JUDGE_MODEL, config.JUDGE_EFFORT, JUDGE_SYSTEM, user, JUDGE_SCHEMA, "judge")
    table: dict[tuple[int, int], dict] = {}
    for p in data["pairs"]:
        i, j = sorted((int(p["i"]), int(p["j"])))
        if 0 <= i < j < n:
            s = _clip(p["strength"], 0, 1) if p["relation"] != "unrelated" else 0.0
            table[(i, j)] = {"i": i, "j": j, "relation": p["relation"], "strength": s}
    missing = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) not in table:
                missing += 1
                table[(i, j)] = {"i": i, "j": j, "relation": "unrelated", "strength": 0.0}
    return [table[k] for k in sorted(table)], usage, missing

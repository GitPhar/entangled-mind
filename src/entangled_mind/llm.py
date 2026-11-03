"""Language-model side of the pipeline: base answer, claim extraction,
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
        self.request_id = getattr(resp, "_request_id", None)
        super().__init__(f"{call} call refused (model {resp.model}, request {self.request_id}): {resp.stop_details}")


def _check_stop(resp, call: str) -> None:
    if resp.stop_reason == "refusal":
        raise RefusalError(call, resp)
    if resp.stop_reason == "max_tokens":
        raise RuntimeError(f"{call} call hit max_tokens")


# --- 1. base model ---------------------------------------------------------

BASE_PROMPT = """Answer the following yes/no question. Give a brief explanation of the main considerations for and against, and say which of them decide the matter.
End your response with a final line that is exactly "FINAL ANSWER: YES" or "FINAL ANSWER: NO".

Question: {question}"""


@dataclass
class BaseAnswer:
    text: str                   # the visible answer - the only text sent to any later call
    answer: str | None          # "yes" / "no" / None if unparseable
    thinking_summary: str       # summarized thinking blocks; archived locally, never sent anywhere
    thinking_tokens: int
    usage: Usage
    request_id: str | None
    truncated: bool = False     # hit max_tokens: recorded as no answer, excluded from the split


def ask_base(question: str) -> BaseAnswer:
    resp = client().messages.create(
        model=config.BASE_MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive", "display": "summarized"},
        **({"output_config": {"effort": config.BASE_EFFORT}} if config.BASE_EFFORT else {}),
        messages=[{"role": "user", "content": BASE_PROMPT.format(question=question)}],
    )
    truncated = resp.stop_reason == "max_tokens"
    if not truncated:
        _check_stop(resp, "base")
    text = "\n".join(b.text for b in resp.content if b.type == "text").strip()
    summary = "\n".join(b.thinking for b in resp.content if b.type == "thinking").strip()
    m = re.findall(r"FINAL ANSWER:\s*(YES|NO)", text, flags=re.I)
    details = getattr(resp.usage, "output_tokens_details", None)
    return BaseAnswer(text, None if truncated or not m else m[-1].lower(), summary,
                      int(getattr(details, "thinking_tokens", 0) or 0), _usage(resp),
                      getattr(resp, "_request_id", None), truncated)


# --- 2. claim extraction (claims become 'contentions', one qubit each) ---------------------------------------------

EXTRACT_SYSTEM = """Below is a short written argument answering a yes/no question.
List the distinct claims the document makes, including claims it raises and then dismisses.
For each claim give:
- text: one short sentence stating the claim.
- confidence: 0 to 1, the writer's apparent confidence in the claim (a dismissed claim gets a low value).
- lean: -1 to 1, which way the claim pushes the answer if it is true: positive toward YES, negative toward NO, 0 if it bears on neither.
Report only claims the document makes. Do not add claims of your own and do not assess whether the writer is right.
List between 5 and 16 claims."""

EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "claims": {
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
    "required": ["claims"],
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
    # Only the visible answer is passed on; thinking content never is.
    user = f"Question: {question}\n\nDocument:\n{base.text}"
    total = Usage(config.EXTRACTOR_MODEL)
    for _ in range(2):
        data, u = _json_call(config.EXTRACTOR_MODEL, config.EXTRACTOR_EFFORT,
                             EXTRACT_SYSTEM, user, EXTRACT_SCHEMA, "extractor")
        total.input_tokens += u.input_tokens
        total.output_tokens += u.output_tokens
        cs = [{"text": c["text"].strip(),
               "confidence": _clip(c["confidence"], 0, 1),
               "lean": _clip(c["lean"], -1, 1)} for c in data["claims"] if c["text"].strip()]
        if len(cs) >= config.MIN_CONTENTIONS:
            return cs[: config.MAX_CONTENTIONS], total
    raise RuntimeError(f"extractor returned {len(cs)} claims")


# --- 3. pairwise relation judge -------------------------------------------

JUDGE_SYSTEM = """You are given a yes/no question and a numbered list of claims made about it.
For every pair of claims (i, j) with i < j, decide:
- "supports": if one is true, the other becomes more plausible, or one backs the other toward the same answer.
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
    user = (f"Question: {question}\n\nClaims:\n{listing}\n\n"
            f"There are {n} claims, so {n * (n - 1) // 2} pairs.")
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


# --- 4. arm G: self-reported confidence -----------------------------------

CONFIDENCE_PROMPT = """Here is a yes/no question and an answer you gave to it.

Question: {question}

Your answer:
{answer}

How confident are you, from 0 to 100, that this final answer is correct? Give only the number."""

CONFIDENCE_SCHEMA = {
    "type": "object",
    "properties": {"confidence": {"type": "integer"}},
    "required": ["confidence"],
    "additionalProperties": False,
}


def self_confidence(question: str, visible_answer: str) -> tuple[int, Usage, str | None]:
    """One call to the base model; only its visible answer is shown back to it."""
    resp = client().messages.create(
        model=config.BASE_MODEL,
        max_tokens=4000,
        output_config={"format": {"type": "json_schema", "schema": CONFIDENCE_SCHEMA}},
        messages=[{"role": "user", "content": CONFIDENCE_PROMPT.format(question=question, answer=visible_answer)}],
    )
    _check_stop(resp, "self_confidence")
    text = next(b.text for b in resp.content if b.type == "text")
    return int(_clip(json.loads(text)["confidence"], 0, 100)), _usage(resp), getattr(resp, "_request_id", None)

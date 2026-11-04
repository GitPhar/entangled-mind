"""Local open-weight model backend for the probe-dissociation test (D48), on Apple silicon via MLX.

One `Chat` is one conversation held in a KV cache. It does three things:
- `rate(user_text)`: append a user turn and sample a 0-100 rating as the assistant turn
  `{"rating": N}`. Decoding is constrained the way experiment 5's JSON schema constrained Haiku:
  the prefix `{"rating": ` is forced, then digit tokens are sampled at temperature 1.0 from the
  model's own distribution, restricted to integers 0-100 without leading zeros, then `}`.
- `probe(user_text, needle)`: a side branch. Append a user turn, run it, return the residual
  stream at the last token of `needle` (the statement) at every layer, then trim the cache back
  so the conversation continues as if the branch had never happened.
- the residual at the last prompt token before the rating digits is kept on every `rate` call
  (`last_rate_hidden`, exploratory readout position).

Residuals are the outputs of each transformer block (index 0 = embeddings, L = last block,
before the final norm), as in Marks & Tegmark's residual-stream probes.
"""

from __future__ import annotations

import hashlib

import mlx.core as mx
import numpy as np
from mlx_lm import load
from mlx_lm.models.cache import make_prompt_cache, trim_prompt_cache

MODELS = {"llama3-8b": "mlx-community/Meta-Llama-3-8B-Instruct-4bit",
          "qwen2.5-7b": "mlx-community/Qwen2.5-7B-Instruct-4bit"}
PREFIX = '{"rating": '


class _Rec:
    """Wraps one transformer block and keeps its output at the last position."""

    def __init__(self, block, store, idx):
        self.block, self.store, self.idx = block, store, idx

    def __call__(self, h, *a, **k):
        out = self.block(h, *a, **k)
        if self.store.get("on"):
            self.store[self.idx] = out[0, -1]
        return out

    def __getattr__(self, name):   # pass through attributes such as use_sliding
        return getattr(self.block, name)


class LM:
    def __init__(self, name: str):
        self.name = name
        mx.set_cache_limit(256 * 2**20)   # keep MLX's freed-buffer cache small: the Mac is memory-bound
        mx.set_wired_limit(mx.device_info()["max_recommended_working_set_size"])   # as mlx_lm.generate does
        self.model, self.tok = load(MODELS[name])
        inner = self.model.model
        self.store: dict = {}
        self.n_layers = len(inner.layers)
        emb = inner.embed_tokens
        store = self.store

        def embed(x, _e=emb):
            out = _e(x)
            if store.get("on"):
                store[0] = out[0, -1]
            return out
        inner.embed_tokens = embed
        inner.layers = [_Rec(b, self.store, i + 1) for i, b in enumerate(inner.layers)]
        self._digits()

    def _digits(self):
        """Token ids whose text is 1-3 ASCII digits, and ids whose text starts with '}'."""
        dig, end = {}, []
        for t in range(len(self.tok.vocab) if hasattr(self.tok, "vocab") else self.tok.vocab_size):
            s = self.tok.decode([t])
            if 1 <= len(s) <= 3 and s.isascii() and s.isdigit():
                dig[t] = s
            elif s.startswith("}"):
                end.append(t)
        self.dig, self.end = dig, np.array(end)

    def render(self, messages, gen=False) -> str:
        return self.tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=gen)

    def encode(self, text: str) -> list[int]:
        return self.tok.encode(text, add_special_tokens=False)

    def hidden_of(self, text: str) -> np.ndarray:
        """Residuals at the last token of `text`, a fresh forward pass (probe training)."""
        self.store.clear()
        self.store["on"] = True
        self.model(mx.array([self.encode(text)]))
        h = np.stack([np.array(self.store[i].astype(mx.float32)) for i in range(self.n_layers + 1)])
        self.store["on"] = False
        return h

    def statement_text(self, statement: str) -> str:
        """A statement as its own user turn, cut at its last character (training format)."""
        full = self.render([{"role": "user", "content": statement}])
        return full[: full.rindex(statement) + len(statement)]


def seed_for(key: str) -> int:
    return int(hashlib.sha256(key.encode()).hexdigest()[:8], 16)


class Chat:
    def __init__(self, lm: LM, key: str):
        self.lm, self.msgs, self.toks = lm, [], []
        self.cache = make_prompt_cache(lm.model)
        self.rng = np.random.default_rng(seed_for(f"{lm.name}|{key}"))
        self.last_rate_hidden = None
        self.stats = {"fed": 0}

    def _sync(self, target: list[int], record=False):
        """Bring the cache to exactly `target` tokens; return logits at the last one."""
        n = 0
        for a, b in zip(self.toks, target):
            if a != b:
                break
            n += 1
        if n == len(target):   # nothing new: re-run the last token so we have its logits
            n -= 1
        if n < len(self.toks):
            trim_prompt_cache(self.cache, len(self.toks) - n)
        self.toks = list(target[:n])
        new = target[n:]
        self.lm.store.clear()
        self.lm.store["on"] = record
        logits = self.lm.model(mx.array([new]), cache=self.cache)[0, -1]
        self.lm.store["on"] = False
        mx.eval(logits)
        self.toks = list(target)
        self.stats["fed"] += len(new)
        return logits

    def _hidden(self):
        return np.stack([np.array(self.lm.store[i].astype(mx.float32)) for i in range(self.lm.n_layers + 1)])

    def rate(self, user_text: str) -> int:
        lm = self.lm
        self.msgs.append({"role": "user", "content": user_text})
        prompt = lm.encode(lm.render(self.msgs, gen=True) + PREFIX)
        logits = self._sync(prompt, record=True)
        self.last_rate_hidden = self._hidden()
        digits = ""
        while True:
            lp = np.array((logits - mx.logsumexp(logits)).astype(mx.float32))
            opts, mass = [], []
            if digits and int(digits) <= 100:
                opts.append(None)
                mass.append(np.exp(lp[lm.end]).sum())
            for t, s in lm.dig.items():
                d = digits + s
                if len(d) <= 3 and not (len(d) > 1 and d[0] == "0") and int(d) <= 100:
                    opts.append(t)
                    mass.append(np.exp(lp[t]))
            mass = np.array(mass, dtype=np.float64)
            pick = opts[self.rng.choice(len(opts), p=mass / mass.sum())]
            if pick is None:
                break
            digits += lm.dig[pick]
            if len(digits) == 3:
                break
            logits = self._sync(self.toks + [pick])
        r = int(digits)
        self.msgs.append({"role": "assistant", "content": f'{PREFIX}{r}}}'})
        return r

    def probe(self, user_text: str, needle: str) -> np.ndarray:
        lm = self.lm
        full = lm.render(self.msgs + [{"role": "user", "content": user_text}])
        cut = full.rindex(needle) + len(needle)
        keep = len(self.toks)
        self._sync(lm.encode(full[:cut]), record=True)
        h = self._hidden()
        trim_prompt_cache(self.cache, len(self.toks) - keep)
        self.toks = self.toks[:keep]
        return h

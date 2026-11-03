"""Pool extension (DEVIATIONS.md, D4): 75 yes/no items whose answers are
computed here, not hand-labelled, so a 'wrong' model answer cannot be a
labelling error. Deterministic (seed 404)."""

import datetime as dt
import json
import random

from entangled_mind import config

rng = random.Random(404)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def rand_prime(lo, hi):
    while True:
        n = rng.randrange(lo, hi)
        if is_prime(n):
            return n


def fmt(n):
    return f"{n:,}"


items = []
# primality: 8 primes, 7 semiprimes of two 4-digit primes (no small factors)
for k in range(15):
    n = rand_prime(10_000_000, 99_000_000) if k % 2 == 0 else rand_prime(1000, 9999) * rand_prime(1000, 9999)
    items.append(("computation", f"Is {fmt(n)} a prime number?", is_prime(n)))
# weekdays
for k in range(15):
    d = dt.date(1600, 1, 1) + dt.timedelta(days=rng.randrange(0, 365 * 800))
    day = d.weekday() if k % 2 == 0 else (d.weekday() + rng.choice([1, 2, 3, 4, 5, 6])) % 7
    items.append(("calendar", f"Was {d.strftime('%B')} {d.day}, {d.year} a {DAYS[day]} (in the Gregorian calendar)?", day == d.weekday()))
# letter counts in real sentences
SENTENCES = [
    "Peter Piper picked a peck of pickled peppers from the pepper patch",
    "She sells seashells by the seashore while the seagulls screech overhead",
    "Never underestimate the patience of a determined beekeeper in September",
    "The committee reconvened to reconsider the necessary preparations",
    "Interstellar travelers rarely remember the terrible turbulence there",
    "Assessing successive assistants is a necessary business process",
    "Lollipops and gumballs fill the small yellow balloon stall",
    "Mammals in the Amazon commonly communicate at dawn and dusk",
    "Tattered banners fluttered atop the battered fortress tower",
    "Eleven elegant elephants entered the evergreen enclosure every evening",
]
LETTER = ["p", "s", "e", "e", "r", "s", "l", "m", "t", "e"]
for k in range(15):
    i = k % len(SENTENCES)
    s, ch = SENTENCES[i], LETTER[i]
    true = s.lower().count(ch)
    claim = true if k % 2 == 0 else true + rng.choice([-1, 1])
    items.append(("words", f"Does the sentence \"{s}\" contain exactly {claim} occurrences of the letter '{ch}' (ignoring case)?", claim == true))
# digit sums of powers of 2
for k in range(10):
    e = rng.randrange(60, 160)
    true = sum(map(int, str(2 ** e)))
    claim = true if k % 2 == 0 else true + rng.choice([-9, -3, 3, 9])
    items.append(("computation", f"Is the sum of the decimal digits of 2^{e} equal to {claim}?", claim == true))
# 5-digit multiplications with near misses
for k in range(10):
    a, b = rng.randrange(10_000, 99_999), rng.randrange(10_000, 99_999)
    true = a * b
    claim = true if k % 2 == 0 else true + rng.choice([-1, 1]) * rng.choice([10, 100, 1000, 9000])
    items.append(("computation", f"Is {fmt(a)} × {fmt(b)} equal to {fmt(claim)}?", claim == true))
# prime counts in an interval
for k in range(10):
    lo = rng.randrange(1000, 20000)
    true = sum(is_prime(n) for n in range(lo, lo + 100))
    claim = true if k % 2 == 0 else true + rng.choice([-1, 1])
    items.append(("computation", f"Are there exactly {claim} prime numbers between {fmt(lo)} and {fmt(lo + 99)} inclusive?", claim == true))

rng.shuffle(items)   # interleave categories so an early stop still leaves a mix
out = [{"id": f"x{k + 1:02d}", "category": c, "question": q,
        "answer": "yes" if a else "no", "answer_source": "computed"} for k, (c, q, a) in enumerate(items)]
(config.EXPERIMENTS / "questions_extension.json").write_text(json.dumps(out, indent=2))
print(len(out), sum(o["answer"] == "yes" for o in out), "yes")

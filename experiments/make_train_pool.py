"""Build experiments/questions-train.json: ~600 yes/no items for the v2 learned
encoding (DEVIATIONS.md, D9). No item overlaps the run-2 hard pool, which stays a
separate held-out set.

    python experiments/make_train_pool.py <simpleqa_csv> <mmlupro_dir>

(a) 150 SimpleQA (OpenAI simple-evals, MIT): gold answer for half, the gold answer of
    a different question with the same topic and answer type for the other half.
(b) 200 MMLU-Pro (TIGER-Lab, MIT): 50 each biology, engineering, physics, chemistry;
    correct option for half, a random wrong option for the other half.
(c) 150 two-sided computed puzzles: base rates, sampling without replacement,
    birthday problems, expected values, dice, conditional coins, combinations,
    average speed, compound growth, power comparisons. Each claim sits 3-15% above or
    below the exact value (computed with fractions), so either answer is plausible.
(d) 100 code-verified claims: element number/symbol facts with near-miss false
    versions, and computed numeric facts with off-by-small false versions.
Every answer is from the source dataset or computed here. Deterministic (seed 2718)."""

import ast
import csv
import glob
import json
import math
import random
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rng = random.Random(2718)
SQA = ("OpenAI SimpleQA (openai/simple-evals, simple_qa_test_set.csv)", "MIT")
MMLU = ("TIGER-Lab/MMLU-Pro, test split", "MIT")
OWN = ("generated and verified by code in experiments/make_train_pool.py", "MIT")

ELEMENTS = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr "
            "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb "
            "Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn").split()
NAMES = ("hydrogen helium lithium beryllium boron carbon nitrogen oxygen fluorine neon sodium magnesium aluminium "
         "silicon phosphorus sulfur chlorine argon potassium calcium scandium titanium vanadium chromium manganese "
         "iron cobalt nickel copper zinc gallium germanium arsenic selenium bromine krypton rubidium strontium yttrium "
         "zirconium niobium molybdenum technetium ruthenium rhodium palladium silver cadmium indium tin antimony "
         "tellurium iodine xenon caesium barium lanthanum cerium praseodymium neodymium promethium samarium europium "
         "gadolinium terbium dysprosium holmium erbium thulium ytterbium lutetium hafnium tantalum tungsten rhenium "
         "osmium iridium platinum gold mercury thallium lead bismuth polonium astatine radon").split()
assert len(ELEMENTS) == len(NAMES) == 86


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def stem(q):
    """Question text without the candidate answer, for leakage checks against the held-out pool."""
    return norm(re.split(r' Is the answer "|\nIs the correct answer "', q)[0])


def norm(s):
    return re.sub(r"\W+", " ", s.lower()).strip()


def item(cat, q, ans, src, ref):
    return {"category": cat, "question": q, "answer": "yes" if ans else "no", "source": src[0],
            "license": src[1], "source_ref": ref}


# --- (a) SimpleQA ----------------------------------------------------------

def simpleqa(path, exclude_rows, n=150):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f)):
            meta = ast.literal_eval(r["metadata"])
            rows.append({"row": i, "problem": r["problem"].strip(), "answer": r["answer"].strip(),
                         "key": (meta["topic"], meta["answer_type"])})
    avail = [r for r in rows if r["row"] not in exclude_rows]
    out = []
    for k, r in enumerate(rng.sample(avail, n)):
        yes = k % 2 == 0
        if yes:
            cand = r["answer"]
        else:
            pool = [x for x in rows if x["key"] == r["key"] and norm(x["answer"]) != norm(r["answer"])
                    and norm(x["answer"]) not in norm(r["answer"]) and norm(r["answer"]) not in norm(x["answer"])]
            cand = rng.choice(pool)["answer"]
        out.append(item("simpleqa", f"{r['problem']} Is the answer \"{cand}\"?", yes, SQA,
                        f"row {r['row']}; gold answer: {r['answer']}"))
    return out


# --- (b) MMLU-Pro ----------------------------------------------------------

OPTION_DEPENDENT = re.compile(r"\b(following|these|below|above|options?|choices?)\b", re.I)


def mmlu(paths, exclude_ids, per=50):
    rows, seen = [], set()
    for p in sorted(paths):
        d = json.loads(Path(p).read_text())
        for r in d.get("rows", []):
            r = r["row"]
            if r["question_id"] in seen or r["question_id"] in exclude_ids:
                continue
            seen.add(r["question_id"])
            if r["category"] in ("biology", "engineering", "physics", "chemistry") \
                    and not OPTION_DEPENDENT.search(r["question"]) and len(r["question"]) < 900:
                rows.append(r)
    out = []
    for cat in ("biology", "engineering", "physics", "chemistry"):
        for k, r in enumerate(rng.sample([r for r in rows if r["category"] == cat], per)):
            yes = k % 2 == 0
            correct = r["options"][r["answer_index"]].strip()
            cand = correct if yes else rng.choice([o.strip() for o in r["options"] if norm(o) != norm(correct)])
            out.append(item(f"science-{cat}", f"{r['question'].strip()}\nIs the correct answer \"{cand}\"?", yes, MMLU,
                            f"question_id {r['question_id']} ({r['src']}); correct option: {correct}"))
    return out


# --- (c) two-sided computed puzzles ---------------------------------------

def near(value, yes):
    """A threshold 3-15% below the value (so 'greater than' is yes) or above it (no)."""
    d = Fr(rng.randint(3, 15), 100)
    return value * (1 - d) if yes else value * (1 + d)


def pct(x):
    return f"{float(x) * 100:.1f}%"


def puzzles(n_each=15):
    out = []
    for k in range(n_each):                                   # without replacement
        r, b, draw = rng.randint(4, 9), rng.randint(3, 8), rng.randint(2, 3)
        p = Fr(math.comb(r, draw), math.comb(r + b, draw))
        yes = k % 2 == 0
        out.append(item("puzzle-computed", f"A bag holds {r} red and {b} blue marbles. You draw {draw} at random without "
                        f"replacement. Is the probability that all {draw} are red greater than {pct(near(p, yes))}?",
                        yes, OWN, f"exact {p} = {pct(p)}"))
    for k in range(n_each):                                   # base rates
        prev, sens, fpr = Fr(1, rng.choice([50, 100, 200, 500])), Fr(rng.randint(80, 99), 100), Fr(rng.randint(2, 15), 100)
        post = prev * sens / (prev * sens + (1 - prev) * fpr)
        yes = k % 2 == 0
        out.append(item("puzzle-computed", f"A condition affects 1 in {prev.denominator} people. A test detects it "
                        f"{pct(sens)} of the time when present and gives a false positive {pct(fpr)} of the time when "
                        f"absent. A randomly chosen person tests positive. Is the probability they have the condition "
                        f"greater than {pct(near(post, yes))}?", yes, OWN, f"exact {float(post):.5f}"))
    for k in range(n_each):                                   # birthday
        days = rng.choice([100, 200, 365, 500, 1000])
        people = rng.randint(8, 45)
        p_none = Fr(1)
        for i in range(people):
            p_none *= Fr(days - i, days)
        p = 1 - p_none
        yes = k % 2 == 0
        out.append(item("puzzle-computed", f"{people} people each pick one of {days} equally likely days at random, "
                        f"independently. Is the probability that at least two pick the same day greater than "
                        f"{pct(near(p, yes))}?", yes, OWN, f"exact {float(p):.5f}"))
    for k in range(n_each):                                   # expected value
        a, pa = rng.randint(20, 200), Fr(rng.randint(5, 60), 100)
        ev_a = a * pa
        sure = round(float(near(ev_a, k % 2 == 0)), 2)        # even k: sure amount below EV(A)
        yes = ev_a > Fr(str(sure))
        out.append(item("puzzle-computed", f"Game A pays ${a} with probability {pct(pa)} and nothing otherwise. Game B "
                        f"pays ${sure:.2f} for sure. Does game A have the higher expected payout?", yes, OWN,
                        f"EV(A) = {float(ev_a):.4f}"))
    for k in range(n_each):                                   # three dice
        counts = {}
        for x in range(1, 7):
            for y in range(1, 7):
                for z in range(1, 7):
                    counts[x + y + z] = counts.get(x + y + z, 0) + 1
        while True:
            s1, s2 = rng.sample(range(4, 18), 2)
            if counts[s1] != counts[s2]:
                break
        out.append(item("puzzle-computed", f"When three fair six-sided dice are rolled, is a total of {s1} more likely "
                        f"than a total of {s2}?", counts[s1] > counts[s2], OWN,
                        f"ways: {s1} -> {counts[s1]}, {s2} -> {counts[s2]} (of 216)"))
    for k in range(n_each):                                   # conditional coin
        heads = rng.randint(1, 5)
        p = Fr(2 ** heads, 2 ** heads + 1)                    # P(double-headed | `heads` heads)
        yes = k % 2 == 0
        out.append(item("puzzle-computed", f"A box holds one fair coin and one coin with heads on both sides. You pick one "
                        f"at random and flip it {heads} times; every flip is heads. Is the probability you picked the "
                        f"two-headed coin greater than {pct(near(p, yes))}?", yes, OWN, f"exact {p}"))
    for k in range(n_each):                                   # combinations
        nn, kk = rng.randint(12, 30), rng.randint(3, 7)
        c = math.comb(nn, kk)
        yes = k % 2 == 0
        thr = int(near(Fr(c), yes))
        out.append(item("puzzle-computed", f"Are there more than {thr:,} ways to choose a team of {kk} from {nn} people "
                        f"(order does not matter)?", c > thr, OWN, f"C({nn},{kk}) = {c}"))
    for k in range(n_each):                                   # average speed (harmonic-mean trap)
        d = rng.choice([60, 90, 120])
        v1, v2 = rng.sample([20, 30, 40, 45, 50, 60, 75, 80, 90], 2)
        avg = Fr(2 * d, 1) / (Fr(d, v1) + Fr(d, v2))
        yes = k % 2 == 0
        out.append(item("puzzle-computed", f"A car drives {d} km at {v1} km/h and then another {d} km at {v2} km/h. Is "
                        f"its average speed for the whole trip greater than {float(near(avg, yes)):.1f} km/h?", yes, OWN,
                        f"exact {float(avg):.4f}"))
    for k in range(n_each):                                   # compound growth
        p0, r, yrs = rng.choice([1000, 2500, 5000]), Fr(rng.randint(3, 12), 100), rng.randint(5, 25)
        fv = p0 * (1 + r) ** yrs
        yes = k % 2 == 0
        thr = round(float(near(fv, yes)))
        out.append(item("puzzle-computed", f"${p0:,} grows at {pct(r)} per year, compounded annually, for {yrs} years. "
                        f"Does it end above ${thr:,}?", fv > thr, OWN, f"exact {float(fv):.2f}"))
    for k in range(n_each):                                   # power comparison
        while True:
            a, c = rng.randint(2, 9), rng.randint(2, 9)
            if a == c:
                continue
            b = rng.randint(10, 60)
            d = round(b * math.log(a) / math.log(c)) + rng.choice([-1, 0, 1])
            if d > 1 and a ** b != c ** d:
                break
        out.append(item("puzzle-computed", f"Is {a}^{b} greater than {c}^{d}?", a ** b > c ** d, OWN,
                        f"log10: {b * math.log10(a):.4f} vs {d * math.log10(c):.4f}"))
    return out


# --- (d) code-verified claims ---------------------------------------------

def primes(n):
    ps, x = [], 2
    while len(ps) < n:
        if all(x % p for p in ps if p * p <= x):
            ps.append(x)
        x += 1
    return ps


def claims():
    out = []
    for k in range(50):
        z = rng.randint(1, 86)
        yes = k % 2 == 0
        if k % 4 < 2:
            step = -1 if z == 86 else (1 if z == 1 else rng.choice([-1, 1]))
            name = NAMES[z - 1] if yes else NAMES[z - 1 + step]
            c = f"The element with atomic number {z} is {name}."
        else:
            sym = ELEMENTS[z - 1] if yes else rng.choice([s for s in ELEMENTS if s != ELEMENTS[z - 1] and s[0] == ELEMENTS[z - 1][0]]
                                                          or [s for s in ELEMENTS if s != ELEMENTS[z - 1]])
            c = f"The chemical symbol for {NAMES[z - 1]} is {sym}."
        out.append(item("claim-verified", f"Is the following claim true? {c}", yes, OWN,
                        f"Z={z}: {NAMES[z - 1]} ({ELEMENTS[z - 1]})"))
    for k in range(50):
        yes = k % 2 == 0
        kind = k % 5
        if kind == 0:
            n = rng.randint(10, 40); v = sum(primes(n)); c = "The sum of the first {} prime numbers is {:,}."
            args, true = (n,), v
        elif kind == 1:
            n = rng.randint(15, 60); v = len(str(math.factorial(n))); c = "{}! (factorial) has {} digits."
            args, true = (n,), v
        elif kind == 2:
            n = rng.randint(30, 200); v = len(str(2 ** n)); c = "2^{} has {} digits."
            args, true = (n,), v
        elif kind == 3:
            n = rng.randint(20, 150); v = n * (n + 1) // 2; c = "The {} triangular number is {:,}."
            args, true = (ordinal(n),), v
        else:
            n = rng.randint(20, 40); a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            v = a; c = "The {} Fibonacci number (with F1 = F2 = 1) is {:,}."
            args, true = (ordinal(n),), v
        shown = true if yes else true + rng.choice([-1, 1]) * (1 if kind in (1, 2) else rng.choice([1, 2, 10]))
        out.append(item("claim-verified", "Is the following claim true? " + c.format(*args, shown), yes, OWN,
                        f"true value {true}"))
    return out


def main(sqa_csv, mmlu_dir):
    hard = json.loads((ROOT / "experiments" / "questions-hard.json").read_text())
    ex_rows = {int(h["source_ref"].split(";")[0].split()[1]) for h in hard if h["category"] == "simpleqa"}
    ex_ids = {int(h["source_ref"].split()[1]) for h in hard if h["category"].startswith("science")}
    items = simpleqa(sqa_csv, ex_rows) + mmlu(glob.glob(str(Path(mmlu_dir) / "mmlupro_*.json")), ex_ids) + puzzles() + claims()
    held_out = {stem(h["question"]) for h in hard}
    leaked = [it for it in items if stem(it["question"]) in held_out]
    items = [it for it in items if stem(it["question"]) not in held_out]
    print(f"dropped {len(leaked)} items whose question stem also appears in the held-out hard pool")
    rng.shuffle(items)
    out = [{"id": f"t{k + 1:03d}", **it} for k, it in enumerate(items)]
    (ROOT / "experiments" / "questions-train.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    from collections import Counter
    print(len(out), Counter(o["category"] for o in out), Counter(o["answer"] for o in out))


if __name__ == "__main__" and len(sys.argv) == 3:
    main(sys.argv[1], sys.argv[2])


def supplement(sqa_csv, mmlu_dir):
    """D9b: one supplement, appended as t599+, from the categories that produced errors in pool run 5
    (MMLU-Pro engineering / physics / chemistry, and SimpleQA). Excludes every existing train item and
    the held-out hard pool."""
    global rng
    rng = random.Random(2719)
    path = ROOT / "experiments" / "questions-train.json"
    existing = json.loads(path.read_text())
    hard = json.loads((ROOT / "experiments" / "questions-hard.json").read_text())
    taken = existing + hard
    ex_rows = {int(h["source_ref"].split(";")[0].split()[1]) for h in taken if h["category"] == "simpleqa"}
    ex_ids = {int(h["source_ref"].split()[1]) for h in taken if h["category"].startswith("science")}
    held = {stem(h["question"]) for h in taken}
    rows, seen = [], set()
    for p in sorted(glob.glob(str(Path(mmlu_dir) / "mmlupro_*.json"))):
        for r in json.loads(Path(p).read_text()).get("rows", []):
            r = r["row"]
            if r["question_id"] in seen or r["question_id"] in ex_ids:
                continue
            seen.add(r["question_id"])
            if r["category"] in ("engineering", "physics", "chemistry") \
                    and not OPTION_DEPENDENT.search(r["question"]) and len(r["question"]) < 900:
                rows.append(r)
    new = []
    for cat in ("engineering", "physics", "chemistry"):
        for k, r in enumerate(rng.sample([r for r in rows if r["category"] == cat], 100)):
            yes = k % 2 == 0
            correct = r["options"][r["answer_index"]].strip()
            cand = correct if yes else rng.choice([o.strip() for o in r["options"] if norm(o) != norm(correct)])
            new.append(item(f"science-{cat}", f"{r['question'].strip()}\nIs the correct answer \"{cand}\"?", yes, MMLU,
                            f"question_id {r['question_id']} ({r['src']}); correct option: {correct}"))
    new += simpleqa(sqa_csv, ex_rows, n=150)
    new = [it for it in new if stem(it["question"]) not in held]
    rng.shuffle(new)
    start = len(existing)
    out = existing + [{"id": f"t{start + k + 1:03d}", **it} for k, it in enumerate(new)]
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    from collections import Counter
    print(f"supplement: {len(new)} items (t{start + 1:03d}-t{len(out):03d})", Counter(i["category"] for i in new))


if __name__ == "__main__" and len(sys.argv) > 3 and sys.argv[3] == "--supplement":
    supplement(sys.argv[1], sys.argv[2])

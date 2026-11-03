"""Build experiments/questions-hard.json: ~300 harder yes/no items with known
answers and per-item source and license (DEVIATIONS.md, D6).

    python experiments/make_hard_pool.py <data_dir>

<data_dir> must hold the public source files, downloaded unchanged:
  simple_qa_test_set.csv  https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv
                          (openai/simple-evals, MIT)
  mmlupro_*.json          TIGER-Lab/MMLU-Pro test rows via the HF datasets-server /rows API (MIT)

(a) 120 SimpleQA items. "yes" items pair the question with its gold answer; "no" items
    pair it with the gold answer of a different SimpleQA question with the same topic
    and answer type (plausible, certainly wrong).
(b) 120 MMLU-Pro physics + chemistry items (GPQA Diamond is gated and its authors ask
    that items not be published in plain text, so it is not used). "yes" items pair the
    stem with the correct option, "no" items with a random wrong option. Stems that
    depend on seeing the option list are dropped.
(c) 60 author-written claims, 30 true and 30 plausible fabrications.
Deterministic (seed 1729)."""

import ast
import csv
import glob
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rng = random.Random(1729)
SQA_SRC = ("OpenAI SimpleQA (openai/simple-evals, simple_qa_test_set.csv)", "MIT")
MMLU_SRC = ("TIGER-Lab/MMLU-Pro, test split", "MIT")
OWN_SRC = ("author-written for this project; verified by the author", "MIT")

TRUE_CLAIMS = [
    "The Peace of Westphalia was signed in 1648.",
    "The element with atomic number 74 is tungsten.",
    "The Hubble Space Telescope was launched in 1990.",
    "The chemical symbol for antimony is Sb.",
    "The Rosetta Stone is held in the British Museum.",
    "Marie Curie was born in Warsaw.",
    "The Suez Canal opened in 1869.",
    "The capital of Kazakhstan is Astana.",
    "Venus has no natural moons.",
    "The SI base unit of luminous intensity is the candela.",
    "Kurt Gödel published his incompleteness theorems in 1931.",
    "The Danube flows into the Black Sea.",
    "Mount Kilimanjaro is in Tanzania.",
    "The first transatlantic telegraph cable was completed in 1858.",
    "Neptune was discovered in 1846.",
    "Watson and Crick published the double-helix structure of DNA in 1953.",
    "The atomic number of gold is 79.",
    "Ulaanbaatar is the capital of Mongolia.",
    "Saturn's largest moon is Titan.",
    "The Battle of Hastings took place in 1066.",
    "Lake Titicaca lies on the border between Peru and Bolivia.",
    "Johannes Kepler published Astronomia Nova in 1609.",
    "The speed of sound in dry air at 20 °C is about 343 metres per second.",
    "Alan Turing's paper 'On Computable Numbers' was published in the 1930s.",
    "Pluto was discovered by Clyde Tombaugh.",
    "The Eiffel Tower was completed in 1889.",
    "Penicillin was discovered by Alexander Fleming.",
    "The Berlin Wall fell in 1989.",
    "Insulin was first isolated at the University of Toronto.",
    "The Magna Carta was sealed in 1215.",
]
FALSE_CLAIMS = [
    "The Treaty of Utrecht was signed in 1648.",
    "The element with atomic number 74 is molybdenum.",
    "The Hubble Space Telescope was launched in 1986.",
    "The chemical symbol for antimony is An.",
    "The Rosetta Stone is held in the Louvre.",
    "Marie Curie was born in Kraków.",
    "The Suez Canal opened in 1859.",
    "The capital of Kazakhstan is Almaty.",
    "Mars has no natural moons.",
    "The SI base unit of luminous intensity is the lumen.",
    "Kurt Gödel published his incompleteness theorems in 1921.",
    "The Danube flows into the Adriatic Sea.",
    "Mount Kilimanjaro is in Kenya.",
    "The first transatlantic telegraph cable was completed in 1838.",
    "Neptune was discovered in 1781.",
    "Watson and Crick published the double-helix structure of DNA in 1949.",
    "The atomic number of gold is 78.",
    "Ulaanbaatar is the capital of Kyrgyzstan.",
    "Saturn's largest moon is Enceladus.",
    "The Battle of Agincourt took place in 1066.",
    "Lake Titicaca lies on the border between Chile and Bolivia.",
    "Johannes Kepler published Astronomia Nova in 1619.",
    "The speed of sound in dry air at 20 °C is about 443 metres per second.",
    "Alan Turing's paper 'On Computable Numbers' was published in 1946.",
    "Pluto was discovered by Edwin Hubble.",
    "The Eiffel Tower was completed in 1899.",
    "Penicillin was discovered by Louis Pasteur.",
    "The Berlin Wall fell in 1991.",
    "Insulin was first isolated at the University of Edinburgh.",
    "The chemical formula of table salt is KCl.",
]


def norm(s: str) -> str:
    return re.sub(r"\W+", " ", s.lower()).strip()


def simpleqa(path: Path, n: int = 120) -> list[dict]:
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f)):
            meta = ast.literal_eval(r["metadata"])
            rows.append({"row": i, "problem": r["problem"].strip(), "answer": r["answer"].strip(),
                         "key": (meta["topic"], meta["answer_type"])})
    picked = rng.sample(rows, n)
    out = []
    for k, r in enumerate(picked):
        yes = k % 2 == 0
        if yes:
            cand = r["answer"]
        else:
            pool = [x for x in rows if x["key"] == r["key"] and norm(x["answer"]) != norm(r["answer"])
                    and norm(x["answer"]) not in norm(r["answer"]) and norm(r["answer"]) not in norm(x["answer"])]
            cand = rng.choice(pool)["answer"]
        out.append({"category": "simpleqa", "question": f"{r['problem']} Is the answer \"{cand}\"?",
                    "answer": "yes" if yes else "no", "source": SQA_SRC[0], "license": SQA_SRC[1],
                    "source_ref": f"row {r['row']}; gold answer: {r['answer']}"})
    return out


OPTION_DEPENDENT = re.compile(r"\b(following|these|below|above|options?|choices?)\b", re.I)


def mmlu_pro(paths: list[str], per_category: int = 60) -> list[dict]:
    rows = []
    for p in sorted(paths):
        for r in json.loads(Path(p).read_text()).get("rows", []):   # failed downloads hold only an error
            r = r["row"]
            if r["category"] in ("physics", "chemistry") and not OPTION_DEPENDENT.search(r["question"]) \
                    and len(r["question"]) < 900:
                rows.append(r)
    out = []
    for cat in ("physics", "chemistry"):
        picked = rng.sample([r for r in rows if r["category"] == cat], per_category)
        for k, r in enumerate(picked):
            yes = k % 2 == 0
            correct = r["options"][r["answer_index"]].strip()
            if yes:
                cand = correct
            else:
                cand = rng.choice([o.strip() for o in r["options"] if norm(o) != norm(correct)])
            out.append({"category": f"science-{cat}",
                        "question": f"{r['question'].strip()}\nIs the correct answer \"{cand}\"?",
                        "answer": "yes" if yes else "no", "source": MMLU_SRC[0], "license": MMLU_SRC[1],
                        "source_ref": f"question_id {r['question_id']} ({r['src']}); correct option: {correct}"})
    return out


def claims() -> list[dict]:
    items = [(c, "yes") for c in TRUE_CLAIMS] + [(c, "no") for c in FALSE_CLAIMS]
    rng.shuffle(items)
    return [{"category": "claim", "question": f"Is the following claim true? {c}", "answer": a,
             "source": OWN_SRC[0], "license": OWN_SRC[1], "source_ref": "true claim" if a == "yes" else "fabrication"}
            for c, a in items]


def main(data_dir: str) -> None:
    d = Path(data_dir)
    items = simpleqa(d / "simple_qa_test_set.csv") + mmlu_pro(glob.glob(str(d / "mmlupro_*.json"))) + claims()
    rng.shuffle(items)
    out = [{"id": f"h{k + 1:03d}", **it} for k, it in enumerate(items)]
    (ROOT / "experiments" / "questions-hard.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    from collections import Counter
    print(len(out), Counter(o["category"] for o in out), Counter(o["answer"] for o in out))


if __name__ == "__main__":
    main(sys.argv[1])

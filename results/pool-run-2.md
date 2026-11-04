# Pool run 2: base `claude-haiku-5-5` (effort default, adaptive thinking)

125 questions processed; 0 hit the 16,000-token cap, gave no FINAL ANSWER or failed claim extraction, and are excluded; base model wrong on **4** of 125 answered. API cost $1.0334. Contentions are the claims in the visible answer (DEVIATIONS.md, D1–D3).

Test set rule: fallback (D5): all 4 wrong items + the 10 correct items whose extracted claims give the model's answer the least net support. Test set: 4 wrong + 10 right. Calibration pool: 111 items.

| id | category | truth | model | correct | set | contentions | related pairs | contradictions |
|---|---|---|---|---|---|---|---|---|
| q01 | puzzle | no | no | yes | calib | 9 | 27 | 10 |
| q02 | puzzle | yes | yes | yes | calib | 9 | 24 | 8 |
| q03 | puzzle | no | no | yes | calib | 9 | 34 | 12 |
| q04 | puzzle | no | no | yes | calib | 8 | 23 | 7 |
| q05 | puzzle | no | no | yes | calib | 8 | 20 | 2 |
| q06 | puzzle | no | no | yes | calib | 9 | 27 | 1 |
| q07 | puzzle | no | no | yes | calib | 7 | 15 | 5 |
| q08 | puzzle | yes | yes | yes | calib | 11 | 34 | 7 |
| q09 | puzzle | no | no | yes | calib | 8 | 28 | 7 |
| q10 | puzzle | no | no | yes | calib | 8 | 23 | 6 |
| q11 | puzzle | no | no | yes | calib | 9 | 18 | 0 |
| q12 | puzzle | no | no | yes | calib | 8 | 17 | 6 |
| q13 | puzzle | yes | yes | yes | calib | 9 | 22 | 5 |
| q14 | probability | no | no | yes | calib | 9 | 22 | 1 |
| q15 | probability | no | no | yes | test | 9 | 27 | 0 |
| q16 | probability | yes | yes | yes | calib | 9 | 23 | 5 |
| q17 | probability | no | no | yes | calib | 9 | 19 | 1 |
| q18 | probability | no | no | yes | calib | 9 | 33 | 7 |
| q19 | probability | no | no | yes | calib | 10 | 38 | 14 |
| q20 | probability | no | no | yes | calib | 7 | 11 | 4 |
| q21 | probability | yes | yes | yes | calib | 9 | 17 | 0 |
| q22 | linda | no | no | yes | calib | 10 | 25 | 3 |
| q23 | linda | no | no | yes | calib | 9 | 31 | 15 |
| q24 | linda | yes | yes | yes | test | 8 | 16 | 5 |
| q25 | linda | yes | yes | yes | calib | 10 | 24 | 4 |
| q26 | linda | no | no | yes | calib | 9 | 25 | 5 |
| q27 | logic | no | no | yes | calib | 10 | 29 | 5 |
| q28 | logic | yes | yes | yes | calib | 8 | 12 | 0 |
| q29 | logic | no | no | yes | calib | 8 | 20 | 0 |
| q30 | logic | yes | yes | yes | calib | 10 | 45 | 16 |
| q31 | math | no | no | yes | test | 9 | 14 | 3 |
| q32 | math | no | no | yes | calib | 9 | 19 | 0 |
| q33 | math | yes | yes | yes | calib | 9 | 15 | 0 |
| q34 | math | no | no | yes | test | 8 | 15 | 0 |
| q35 | math | no | no | yes | calib | 8 | 28 | 0 |
| q36 | math | no | no | yes | calib | 9 | 17 | 0 |
| q37 | math | no | no | yes | calib | 10 | 31 | 0 |
| q38 | math | yes | yes | yes | calib | 8 | 20 | 0 |
| q39 | math | yes | yes | yes | calib | 8 | 22 | 6 |
| q40 | math | yes | yes | yes | calib | 10 | 45 | 0 |
| q41 | math | no | no | yes | calib | 8 | 20 | 7 |
| q42 | math | yes | yes | yes | calib | 8 | 21 | 5 |
| q43 | math | yes | yes | yes | calib | 7 | 16 | 5 |
| q44 | math | yes | yes | yes | calib | 8 | 28 | 11 |
| q45 | words | yes | yes | yes | calib | 7 | 15 | 0 |
| q46 | words | no | no | yes | calib | 8 | 12 | 6 |
| q47 | calendar | no | no | yes | calib | 11 | 25 | 3 |
| q48 | fact | yes | yes | yes | calib | 9 | 28 | 5 |
| q49 | fact | yes | yes | yes | calib | 10 | 25 | 0 |
| q50 | fact | yes | yes | yes | calib | 9 | 28 | 8 |
| q51 | fact | yes | yes | yes | calib | 10 | 34 | 7 |
| q52 | fact | no | no | yes | calib | 10 | 29 | 8 |
| q53 | fact | no | no | yes | calib | 10 | 25 | 2 |
| q54 | fact | no | no | yes | calib | 10 | 24 | 0 |
| q55 | fact | yes | yes | yes | calib | 8 | 12 | 2 |
| q56 | fact | yes | yes | yes | calib | 9 | 21 | 2 |
| q57 | fact | yes | yes | yes | calib | 8 | 23 | 0 |
| q58 | fact | yes | yes | yes | calib | 11 | 27 | 7 |
| q59 | fact | yes | yes | yes | calib | 10 | 45 | 9 |
| q60 | fact | no | no | yes | calib | 9 | 22 | 1 |
| x01 | computation | no | no | yes | calib | 10 | 26 | 0 |
| x02 | computation | yes | yes | yes | calib | 9 | 36 | 0 |
| x03 | calendar | no | no | yes | calib | 8 | 12 | 0 |
| x05 | calendar | no | no | yes | calib | 10 | 19 | 6 |
| x07 | words | yes | yes | yes | calib | 11 | 55 | 0 |
| x08 | computation | no | no | yes | calib | 10 | 30 | 9 |
| x10 | computation | yes | yes | yes | calib | 8 | 28 | 0 |
| x11 | computation | no | no | yes | calib | 9 | 21 | 3 |
| x12 | calendar | no | no | yes | calib | 10 | 30 | 0 |
| x13 | computation | no | no | yes | calib | 10 | 26 | 5 |
| x14 | computation | yes | yes | yes | calib | 9 | 18 | 2 |
| x15 | computation | no | no | yes | calib | 9 | 17 | 4 |
| x16 | words | no | no | yes | calib | 9 | 29 | 0 |
| x17 | computation | no | no | yes | test | 10 | 19 | 5 |
| x18 | computation | no | no | yes | calib | 10 | 31 | 3 |
| x19 | calendar | no | no | yes | calib | 9 | 34 | 0 |
| x20 | words | yes | yes | yes | calib | 11 | 21 | 0 |
| x21 | calendar | no | no | yes | test | 8 | 12 | 0 |
| x22 | calendar | no | no | yes | calib | 8 | 16 | 0 |
| x23 | computation | yes | yes | yes | calib | 9 | 22 | 0 |
| x24 | computation | yes | yes | yes | calib | 9 | 21 | 0 |
| x25 | words | yes | yes | yes | calib | 9 | 29 | 0 |
| x26 | calendar | no | no | yes | calib | 9 | 21 | 0 |
| x28 | computation | yes | yes | yes | calib | 8 | 16 | 1 |
| x29 | calendar | yes | yes | yes | calib | 10 | 20 | 4 |
| x31 | computation | yes | no | **no** | test | 9 | 7 | 2 |
| x32 | computation | yes | yes | yes | calib | 9 | 17 | 2 |
| x33 | words | yes | yes | yes | calib | 10 | 30 | 20 |
| x34 | calendar | yes | yes | yes | calib | 9 | 31 | 0 |
| x35 | computation | yes | yes | yes | calib | 9 | 14 | 5 |
| x36 | computation | yes | yes | yes | calib | 10 | 29 | 0 |
| x39 | computation | yes | yes | yes | calib | 10 | 22 | 1 |
| x40 | computation | yes | yes | yes | calib | 9 | 23 | 0 |
| x41 | computation | yes | yes | yes | calib | 8 | 15 | 1 |
| x42 | words | yes | yes | yes | calib | 10 | 34 | 2 |
| x43 | words | no | no | yes | calib | 11 | 17 | 0 |
| x44 | words | yes | yes | yes | calib | 12 | 66 | 0 |
| x45 | words | no | no | yes | test | 11 | 11 | 0 |
| x47 | computation | no | no | yes | calib | 8 | 13 | 0 |
| x48 | computation | no | no | yes | calib | 10 | 20 | 2 |
| x49 | computation | yes | yes | yes | calib | 8 | 17 | 2 |
| x50 | words | no | no | yes | calib | 11 | 17 | 0 |
| x51 | calendar | yes | yes | yes | calib | 9 | 24 | 0 |
| x52 | computation | yes | yes | yes | calib | 11 | 28 | 0 |
| x53 | words | yes | yes | yes | calib | 9 | 36 | 0 |
| x56 | calendar | yes | yes | yes | calib | 9 | 10 | 0 |
| x57 | computation | no | no | yes | calib | 9 | 13 | 4 |
| x58 | calendar | yes | yes | yes | calib | 9 | 23 | 3 |
| x59 | words | no | no | yes | calib | 11 | 24 | 21 |
| x60 | computation | no | no | yes | calib | 9 | 20 | 0 |
| x61 | computation | no | no | yes | calib | 10 | 26 | 5 |
| x62 | computation | no | yes | **no** | test | 9 | 15 | 3 |
| x63 | words | no | no | yes | test | 10 | 15 | 0 |
| x64 | words | no | no | yes | calib | 11 | 20 | 0 |
| x65 | calendar | yes | yes | yes | calib | 8 | 16 | 2 |
| x66 | computation | no | no | yes | calib | 11 | 27 | 0 |
| x67 | calendar | yes | yes | yes | calib | 8 | 16 | 4 |
| x68 | words | yes | no | **no** | test | 9 | 27 | 13 |
| x69 | computation | no | no | yes | calib | 9 | 17 | 0 |
| x70 | calendar | yes | yes | yes | calib | 10 | 21 | 0 |
| x71 | computation | no | no | yes | test | 10 | 23 | 2 |
| x72 | computation | no | no | yes | test | 10 | 23 | 0 |
| x73 | computation | no | no | yes | calib | 9 | 24 | 7 |
| x74 | computation | yes | yes | yes | calib | 8 | 22 | 1 |
| x75 | computation | yes | no | **no** | test | 9 | 15 | 0 |

Wrong by category: calendar 0/16, computation 3/35, fact 0/13, linda 0/5, logic 0/4, math 0/14, probability 0/8, puzzle 0/13, words 1/17


Wrong items:

- x31: Is 11,503,259 a prime number? (truth yes, model no)
- x62: Is 9,236,891 a prime number? (truth no, model yes)
- x68: Does the sentence "Never underestimate the patience of a determined beekeeper in September" contain exactly 19 occurrences of the letter 'e' (ignoring case)? (truth yes, model no)
- x75: Is 58,881,457 a prime number? (truth yes, model no)

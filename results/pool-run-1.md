# Pool run 1: base `claude-sonnet-5-5` (effort xhigh, adaptive thinking)

127 questions processed; 10 hit the 16,000-token cap, gave no FINAL ANSWER or failed claim extraction, and are excluded; base model wrong on **0** of 117 answered. API cost $4.2440. Contentions are the claims in the visible answer (DEVIATIONS.md, D1–D3).

No wrong items, so no test set can be formed from this run.

| id | category | truth | model | correct | set | contentions | related pairs | contradictions |
|---|---|---|---|---|---|---|---|---|
| q01 | puzzle | no | no | yes | — | 9 | 33 | 7 |
| q02 | puzzle | yes | yes | yes | — | 9 | 21 | 2 |
| q03 | puzzle | no | no | yes | — | 10 | 24 | 9 |
| q04 | puzzle | no | no | yes | — | 8 | 16 | 0 |
| q05 | puzzle | no | no | yes | — | 9 | 29 | 6 |
| q06 | puzzle | no | no | yes | — | 8 | 23 | 9 |
| q07 | puzzle | no | no | yes | — | 8 | 13 | 4 |
| q08 | puzzle | yes | yes | yes | — | 9 | 22 | 4 |
| q09 | puzzle | no | no | yes | — | 8 | 26 | 7 |
| q10 | puzzle | no | no | yes | — | 9 | 31 | 6 |
| q11 | puzzle | no | no | yes | — | 10 | 40 | 6 |
| q12 | puzzle | no | no | yes | — | 8 | 26 | 6 |
| q13 | puzzle | yes | yes | yes | — | 8 | 14 | 4 |
| q14 | probability | no | no | yes | — | 10 | 31 | 10 |
| q15 | probability | no | no | yes | — | 10 | 24 | 1 |
| q16 | probability | yes | yes | yes | — | 10 | 20 | 5 |
| q17 | probability | no | no | yes | — | 9 | 25 | 3 |
| q18 | probability | no | no | yes | — | 9 | 35 | 7 |
| q19 | probability | no | no | yes | — | 8 | 18 | 5 |
| q20 | probability | no | no | yes | — | 9 | 18 | 0 |
| q21 | probability | yes | yes | yes | — | 9 | 26 | 6 |
| q22 | linda | no | no | yes | — | 9 | 20 | 2 |
| q23 | linda | no | no | yes | — | 10 | 21 | 6 |
| q24 | linda | yes | yes | yes | — | 9 | 24 | 6 |
| q25 | linda | yes | yes | yes | — | 8 | 28 | 7 |
| q26 | linda | no | no | yes | — | 9 | 32 | 12 |
| q27 | logic | no | no | yes | — | 10 | 31 | 6 |
| q28 | logic | yes | yes | yes | — | 9 | 27 | 3 |
| q29 | logic | no | no | yes | — | 9 | 24 | 2 |
| q30 | logic | yes | yes | yes | — | 10 | 24 | 1 |
| q31 | math | no | no | yes | — | 10 | 21 | 3 |
| q32 | math | no | no | yes | — | 10 | 24 | 0 |
| q33 | math | yes | yes | yes | — | 10 | 16 | 0 |
| q34 | math | no | no | yes | — | 9 | 16 | 0 |
| q35 | math | no | no | yes | — | 9 | 31 | 0 |
| q36 | math | no | no | yes | — | 10 | 23 | 4 |
| q37 | math | no | no | yes | — | 9 | 36 | 8 |
| q38 | math | yes | yes | yes | — | 8 | 12 | 1 |
| q39 | math | yes | yes | yes | — | 8 | 15 | 4 |
| q40 | math | yes | yes | yes | — | 10 | 30 | 9 |
| q41 | math | no | no | yes | — | 9 | 24 | 1 |
| q42 | math | yes | yes | yes | — | 9 | 36 | 0 |
| q43 | math | yes | yes | yes | — | 9 | 28 | 0 |
| q44 | math | yes | yes | yes | — | 9 | 25 | 7 |
| q45 | words | yes | yes | yes | — | 8 | 16 | 6 |
| q46 | words | no | no | yes | — | 8 | 22 | 0 |
| q47 | calendar | no | no | yes | — | 8 | 13 | 1 |
| q48 | fact | yes | yes | yes | — | 10 | 30 | 12 |
| q49 | fact | yes | yes | yes | — | 11 | 28 | 2 |
| q50 | fact | yes | yes | yes | — | 10 | 35 | 14 |
| q51 | fact | yes | yes | yes | — | 10 | 37 | 0 |
| q52 | fact | no | no | yes | — | 9 | 19 | 3 |
| q53 | fact | no | no | yes | — | 11 | 42 | 8 |
| q54 | fact | no | no | yes | — | 10 | 26 | 9 |
| q55 | fact | yes | yes | yes | — | 9 | 19 | 3 |
| q56 | fact | yes | yes | yes | — | 9 | 27 | 0 |
| q57 | fact | yes | yes | yes | — | 10 | 37 | 11 |
| q58 | fact | yes | yes | yes | — | 8 | 13 | 0 |
| q59 | fact | yes | yes | yes | — | 11 | 19 | 5 |
| q60 | fact | no | no | yes | — | 10 | 33 | 13 |
| x01 | computation | no | no | yes | — | 9 | 23 | 0 |
| x02 | computation | yes | yes | yes | — | 10 | 23 | 0 |
| x03 | calendar | no | no | yes | — | 10 | 15 | 1 |
| x04 | computation | yes | (truncated) | — | excluded | | | |
| x05 | calendar | no | no | yes | — | 10 | 18 | 1 |
| x06 | computation | yes | (truncated) | — | excluded | | | |
| x07 | words | yes | yes | yes | — | 10 | 9 | 6 |
| x08 | computation | no | no | yes | — | 9 | 15 | 0 |
| x09 | computation | yes | (truncated) | — | excluded | | | |
| x10 | computation | yes | yes | yes | — | 9 | 25 | 0 |
| x11 | computation | no | no | yes | — | 8 | 13 | 2 |
| x12 | calendar | no | no | yes | — | 10 | 25 | 0 |
| x13 | computation | no | no | yes | — | 8 | 10 | 0 |
| x14 | computation | yes | yes | yes | — | 8 | 18 | 3 |
| x15 | computation | no | no | yes | — | 9 | 30 | 0 |
| x16 | words | no | no | yes | — | 9 | 26 | 0 |
| x17 | computation | no | no | yes | — | 10 | 23 | 5 |
| x18 | computation | no | no | yes | — | 9 | 22 | 6 |
| x19 | calendar | no | no | yes | — | 9 | 15 | 0 |
| x20 | words | yes | yes | yes | — | 10 | 15 | 0 |
| x21 | calendar | no | no | yes | — | 8 | 14 | 0 |
| x22 | calendar | no | no | yes | — | 9 | 25 | 0 |
| x23 | computation | yes | yes | yes | — | 8 | 21 | 0 |
| x24 | computation | yes | yes | yes | — | 10 | 31 | 0 |
| x25 | words | yes | yes | yes | — | 11 | 45 | 0 |
| x26 | calendar | no | no | yes | — | 8 | 16 | 0 |
| x27 | computation | yes | (truncated) | — | excluded | | | |
| x28 | computation | yes | yes | yes | — | 10 | 26 | 0 |
| x29 | calendar | yes | yes | yes | — | 9 | 27 | 0 |
| x30 | computation | no | (truncated) | — | excluded | | | |
| x31 | computation | yes | yes | yes | — | 11 | 20 | 3 |
| x32 | computation | yes | yes | yes | — | 9 | 16 | 1 |
| x33 | words | yes | yes | yes | — | 11 | 19 | 0 |
| x34 | calendar | yes | yes | yes | — | 9 | 26 | 3 |
| x35 | computation | yes | yes | yes | — | 8 | 20 | 0 |
| x36 | computation | yes | yes | yes | — | 9 | 29 | 0 |
| x37 | computation | no | (truncated) | — | excluded | | | |
| x38 | computation | yes | (truncated) | — | excluded | | | |
| x39 | computation | yes | yes | yes | — | 8 | 21 | 4 |
| x40 | computation | yes | yes | yes | — | 9 | 22 | 0 |
| x41 | computation | yes | yes | yes | — | 8 | 21 | 0 |
| x42 | words | yes | yes | yes | — | 10 | 38 | 0 |
| x43 | words | no | no | yes | — | 8 | 14 | 7 |
| x44 | words | yes | yes | yes | — | 9 | 26 | 0 |
| x45 | words | no | no | yes | — | 10 | 16 | 13 |
| x46 | computation | no | (truncated) | — | excluded | | | |
| x47 | computation | no | no | yes | — | 8 | 19 | 0 |
| x48 | computation | no | no | yes | — | 10 | 34 | 6 |
| x49 | computation | yes | yes | yes | — | 10 | 20 | 0 |
| x50 | words | no | no | yes | — | 10 | 8 | 0 |
| x51 | calendar | yes | yes | yes | — | 10 | 36 | 0 |
| x52 | computation | yes | yes | yes | — | 9 | 26 | 0 |
| x53 | words | yes | yes | yes | — | 9 | 36 | 0 |
| x54 | computation | yes | (truncated) | — | excluded | | | |
| x55 | computation | no | (truncated) | — | excluded | | | |
| x56 | calendar | yes | yes | yes | — | 9 | 16 | 0 |
| x57 | computation | no | no | yes | — | 8 | 14 | 0 |
| x58 | calendar | yes | yes | yes | — | 9 | 15 | 2 |
| x59 | words | no | no | yes | — | 11 | 3 | 0 |
| x60 | computation | no | no | yes | — | 10 | 22 | 2 |
| x61 | computation | no | no | yes | — | 9 | 20 | 0 |
| x62 | computation | no | no | yes | — | 9 | 12 | 4 |
| x63 | words | no | no | yes | — | 9 | 18 | 0 |
| x64 | words | no | no | yes | — | 10 | 18 | 0 |
| x65 | calendar | yes | yes | yes | — | 9 | 25 | 0 |
| x66 | computation | no | no | yes | — | 10 | 27 | 5 |
| x67 | calendar | yes | yes | yes | — | 8 | 14 | 2 |

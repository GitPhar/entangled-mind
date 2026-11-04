# Multi-model replication of direction 2: shown, redacted and planted transcripts

Pre-registered in `experiments/mm-gm2-self-conditioning.md` (DM4), committed before any call. D37's 10 items, chains O1–O4 and MF, four conditions, one scale direction, **R = 4** conversations per cell. Haiku's row is D37's archive restricted to repeats 0–3. Costs at the batch rate.

## In plain English

(Hand-written after the run; excluded from reproduce.py's comparison.)

## Primary: the order effect with and without the record

| model | complete conversations | cost | gate p | OE shown | OE redacted | **R = OE_redacted / OE_shown** | reading |
|---|---|---|---|---|---|---|---|
| haiku | 800 | archived | 0.0008 | 9.3 [4.4, 13.2] | 18.7 [7.4, 27.5] | **2.01 [1.04, 4.43]** | **question-driven: the order effect survives redaction (a measurement effect in the strict sense)** |
| sonnet | 800 / 800 | $2.19 | 0.0306 | 6.1 [1.7, 8.9] | 17.9 [5.5, 26.2] | **2.95 [0.99, 12.55]** | **question-driven: the order effect survives redaction (a measurement effect in the strict sense)** |
| opus | 400 / 800 | $4.89 | 0.0040 | 4.4 [0.8, 6.9] | 4.1 [0.0, 7.1] | **0.93 [0.06, 7.31]** | **leaning question-driven (CI straddles 0.5; not decisive)** |

## Planted values and repeat agreement

| model | b_MF | next-rating pull (points) | final-M shift, high − low | OE planted high / low | MF agreement shown / redacted / high / low |
|---|---|---|---|---|---|
| haiku | 1.23 [0.65, 2.11] | 5.4 [3.1, 7.5] | 10.9 [4.8, 17.1] | 6.7 / 3.7 | 78% / 25% / 35% / 40% |
| sonnet | 0.39 [-0.05, 0.76] | 2.5 [-0.5, 5.5] | -4.8 [-13.0, 3.6] | 4.6 / 7.0 | 88% / 35% / 20% / 52% |
| opus | 0.35 [0.17, 0.54] | 0.8 [-1.5, 2.9] | -10.0 [-17.1, -3.1] | 4.6 / 0.5 | 95% / 65% / 35% / 65% |

### Per item, haiku

| item | OE shown | OE redacted | final M by order, shown | redacted | MF M₂ shown / redacted / high / low |
|---|---|---|---|---|---|
| h190 | 4.2 | 3.8 | 18, 10, 18, 10 | 15, 12, 15, 22 | 5 / 15 / 17 / 5 |
| h101 | 2.0 | 9.8 | 5, 9, 4, 6 | 34, 4, 6, 13 | 3 / 19 / 16 / 2 |
| h112 | 19.7 | 21.2 | 81, 38, 66, 82 | 45, 0, 46, 25 | 40 / 26 / 45 / 14 |
| h191 | 0.0 | 43.1 | 4, 3, 4, 4 | 89, 3, 3, 3 | 3 / 3 / 18 / 2 |
| h261 | 16.5 | 30.1 | 50, 8, 10, 6 | 75, 25, 4, 10 | 49 / 68 / 3 / 3 |
| h058 | 8.7 | 8.4 | 41, 22, 54, 42 | 56, 35, 41, 36 | 70 / 15 / 92 / 39 |
| h221 | 2.7 | 8.1 | 32, 31, 38, 36 | 25, 45, 30, 32 | 29 / 34 / 40 / 11 |
| h279 | 7.7 | 2.9 | 34, 29, 18, 39 | 35, 28, 35, 35 | 22 / 42 / 42 / 12 |
| h127 | 4.4 | 3.3 | 22, 35, 28, 30 | 18, 26, 20, 16 | 13 / 28 / 16 / 8 |
| h238 | 4.9 | 4.7 | 14, 4, 4, 3 | 15, 4, 12, 13 | 29 / 10 / 97 / 20 |

### Per item, sonnet

| item | OE shown | OE redacted | final M by order, shown | redacted | MF M₂ shown / redacted / high / low |
|---|---|---|---|---|---|
| h190 | 2.7 | 0.0 | 10, 12, 13, 6 | 10, 12, 10, 11 | 4 / 8 / 16 / 3 |
| h101 | 0.0 | 1.9 | 4, 5, 4, 4 | 8, 10, 6, 10 | 3 / 8 / 14 / 2 |
| h112 | 1.6 | 30.0 | 3, 3, 7, 4 | 70, 6, 4, 8 | 3 / 10 / 17 / 2 |
| h191 | 0.0 | 42.4 | 2, 3, 3, 3 | 6, 72, 91, 8 | 3 / 90 / 17 / 2 |
| h261 | 12.3 | 3.1 | 85, 48, 85, 68 | 88, 86, 89, 81 | 89 / 86 / 86 / 96 |
| h058 | 13.8 | 14.7 | 62, 64, 35, 67 | 34, 36, 28, 62 | 92 / 32 / 90 / 72 |
| h221 | 2.7 | 16.5 | 48, 44, 36, 41 | 40, 12, 20, 50 | 51 / 27 / 30 / 40 |
| h279 | 0.0 | 0.0 | 38, 38, 36, 38 | 29, 26, 25, 26 | 24 / 32 / 32 / 22 |
| h127 | 2.7 | 0.0 | 30, 33, 38, 35 | 24, 22, 23, 23 | 13 / 20 / 25 / 5 |
| h238 | 1.8 | 2.5 | 12, 8, 10, 12 | 12, 11, 15, 18 | 33 / 15 / 7 / 22 |

### Per item, opus

| item | OE shown | OE redacted | final M by order, shown | redacted | MF M₂ shown / redacted / high / low |
|---|---|---|---|---|---|
| h190 | 0.3 | 0.0 | 4, 4, 5, 5 | 6, 4, 4, 4 | 4 / 6 / 8 / 2 |
| h101 | 0.0 | 0.0 | 4, 3, 4, 3 | 5, 4, 5, 4 | 4 / 5 / 16 / 2 |
| h112 | 0.0 | 0.0 | 2, 2, 2, 2 | 3, 2, 2, 2 | 2 / 2 / 12 / 2 |
| h191 | 0.0 | 0.0 | 2, 2, 2, 2 | 2, 2, 2, 2 | 2 / 2 / 4 / 2 |
| h261 | 0.0 | 0.9 | 90, 88, 89, 90 | 84, 86, 90, 88 | 89 / 80 / 92 / 91 |
| h058 | 0.0 | 12.9 | 67, 71, 62, 67 | 71, 61, 38, 52 | 64 / 67 / 88 / 70 |
| h221 | 1.2 | 0.0 | 85, 86, 88, 85 | 82, 84, 86, 82 | 86 / 80 / 94 / 88 |
| h279 | 10.0 | 1.8 | 49, 59, 39, 32 | 32, 38, 28, 24 | 32 / 32 / 32 / 24 |
| h127 | 2.5 | 0.0 | 78, 82, 84, 78 | 80, 78, 76, 81 | 82 / 78 / 88 / 89 |
| h238 | 9.5 | 0.0 | 32, 22, 22, 42 | 26, 24, 15, 17 | 50 / 25 / 44 / 36 |

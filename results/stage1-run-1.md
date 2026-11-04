# Stage 1, run 1: the pipe

Item `q01`: A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. Does the ball cost 10 cents?

Encoded as 9 qubits with 33 entangling RZZ gates and N=0 evolution. Transpiled for `ibm_fez`: depth 208, 117 CZ gates.

**Hardware job `dbl423dgg49c73dk0db0` on `ibm_fez` returned 1000 shots across 336 distinct bitstrings. QPU time: 2 s (IBM `qpu_charge_time_seconds`).**

| run | P(yes) | judgment | conflict score | distinct bitstrings |
|---|---|---|---|---|
| ideal_sim | 0.294 | no | 0.276 | 235 |
| noisy_sim | 0.251 | no | 0.276 | 284 |
| hardware | 0.502 | yes | 0.666 | 336 |

Most frequent hardware bitstrings (qubit 0 rightmost; 0 = yes-aligned):

- `101111101`: 24
- `010001000`: 20
- `111111101`: 19
- `101111111`: 17
- `000001000`: 16
- `000001001`: 12
- `011101101`: 11
- `000000000`: 11

## Reading

- The job waited in the Open Plan queue from 13:16 to 16:06 MST (2 h 50 min).
- On this one circuit, hardware departs from the `ibm_fez` noise model far beyond shot noise: P(yes) 0.50 on hardware vs 0.25 on the noisy simulator and 0.29 ideal (z = 12), with 336 distinct bitstrings out of 1,000 shots. Some qubits overshoot 50/50 (qubit 1: 0.25 ideal, 0.70 hardware), so this is not decoherence alone.
- The QPU time was first logged as 0.0 s by a parsing bug (DEVIATIONS.md, D10), since repaired.

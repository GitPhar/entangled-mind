# ibm_fez calibration at job time

Calibration data are read from `backend.properties(datetime=...)` at each job's execution start. They cover the physical qubits and CZ pairs that the as-run circuits used (`window/data/hardware/`). T1 and T2 are in µs; errors are probabilities.

## Stage 1 pipe test: job `dbl423dgg49c73dk0db0`

Job ran at 2026-11-03 16:06 MST. Calibration snapshot: 2026-11-03 15:31:18-07:00. 9 physical qubits used (9 measured), 8 CZ pairs.

| quantity | median | min | max |
|---|---|---|---|
| T1_us | 133.5 | 87.6 | 203.5 |
| T2_us | 114.1 | 44.6 | 191.1 |
| readout_error | 6.35e-03 | 3.42e-03 | 2.10e-02 |
| sx_error | 2.79e-04 | 1.85e-04 | 4.58e-04 |
| cz_error | 2.06e-03 | 1.50e-03 | 2.43e-03 |

Measured qubits:

| qubit | T1 µs | T2 µs | readout error | sx error |
|---|---|---|---|---|
| 117 | 87.6 | 92.3 | 8.30e-03 | 3.10e-04 |
| 123 | 100.8 | 114.1 | 1.07e-02 | 2.46e-04 |
| 124 | 110.2 | 144.1 | 5.86e-03 | 2.85e-04 |
| 125 | 143.4 | 44.6 | 2.10e-02 | 2.05e-04 |
| 136 | 98.9 | 86.2 | 6.35e-03 | 2.28e-04 |
| 141 | 156.2 | 111.0 | 1.56e-02 | 1.85e-04 |
| 142 | 133.5 | 134.0 | 4.39e-03 | 4.58e-04 |
| 143 | 203.5 | 191.1 | 6.35e-03 | 2.79e-04 |
| 144 | 140.7 | 181.7 | 3.42e-03 | 3.14e-04 |

## Entanglement witness run 1: job `dbl6e1d8mdtc73d5gesg`

Job ran at 2026-11-03 16:06 MST. Calibration snapshot: 2026-11-03 15:31:18-07:00. 14 physical qubits used (6 measured), 12 CZ pairs.

| quantity | median | min | max |
|---|---|---|---|
| T1_us | 146.2 | 23.0 | 272.0 |
| T2_us | 116.3 | 18.6 | 183.9 |
| readout_error | 7.81e-03 | 2.44e-03 | 3.17e-02 |
| sx_error | 2.32e-04 | 9.43e-05 | 4.24e-04 |
| cz_error | 1.97e-03 | 1.58e-03 | 2.36e-03 |

Measured qubits:

| qubit | T1 µs | T2 µs | readout error | sx error |
|---|---|---|---|---|
| 4 | 140.9 | 104.8 | 4.88e-03 | 2.72e-04 |
| 9 | 147.1 | 33.3 | 2.44e-03 | 2.33e-04 |
| 10 | 145.2 | 103.2 | 6.84e-03 | 1.76e-04 |
| 16 | 158.5 | 120.8 | 8.79e-03 | 3.19e-04 |
| 37 | 115.0 | 127.2 | 2.93e-03 | 2.30e-04 |
| 44 | 156.5 | 113.4 | 8.30e-03 | 4.24e-04 |


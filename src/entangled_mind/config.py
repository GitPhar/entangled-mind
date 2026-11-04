"""Pre-registered constants. Changing any of these after test-set results exist
invalidates the run; see experiments/preregistration.md."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
EXPERIMENTS = ROOT / "experiments"

# --- language models -------------------------------------------------------
BASE_MODEL = "claude-haiku-5-5"   # DEVIATIONS.md, D5 (run 1 used claude-sonnet-5-5 at xhigh)
EXTRACTOR_MODEL = "claude-sonnet-5-5"
JUDGE_MODEL = "claude-haiku-5-5"
BASE_EFFORT = None            # model default; run 1 used "xhigh"
EXTRACTOR_EFFORT = "low"
JUDGE_EFFORT = "low"

# USD per million tokens (input, output); thinking tokens bill as output.
PRICES = {
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-opus-5-5": (4.00, 20.00),   # multi-model branch (DM1)
}
API_BUDGET_USD = 10.0

MIN_CONTENTIONS = 5
MAX_CONTENTIONS = 16

# --- encoding --------------------------------------------------------------
KAPPA = 0.25 * 3.141592653589793   # RZZ angle = KAPPA * strength * sign
N_TROTTER = 2                      # default evolution depth for entangled arms
GAMMA0 = 0.5                       # problem-Hamiltonian step scale
BETA0 = 0.4                        # mixer step scale
SHOTS = 1000

# --- readout ---------------------------------------------------------------
STRONG_TAU = 1.0 / 3.0             # |m| >= tau counts as a strongly committed configuration
CALIBRATION_FLAG_FRACTION = 0.25   # each arm's threshold flags the top quartile of the calibration pool

# --- data split ------------------------------------------------------------
SPLIT_SEED = 2026
N_TEST_WRONG = 10
N_TEST_RIGHT = 10
SHUFFLE_SEED = 7

# --- IBM -------------------------------------------------------------------
IBM_CHANNEL = "ibm_quantum_platform"
IBM_INSTANCE = "open-instance"
IBM_BACKEND = "ibm_fez"
QPU_MONTHLY_SECONDS = 600
QPU_STOP_SECONDS = 420             # hard stop at 7 minutes cumulative

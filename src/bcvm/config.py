"""Global constants. Anything that changes the token stream bumps FORMAT_VERSION."""
import os
import sys

# Bytecode changes between minor versions; data and checkpoints are only valid
# for this one. 3.14 rather than 3.15 because torch ships no cp315 wheels yet,
# and the runner needs compile() and torch in the same interpreter.
PYTHON_VERSION = (3, 14)

FORMAT_VERSION = 1

INT_BOUND = 999          # every int in the state must satisfy |v| <= INT_BOUND
MAX_STEPS = 2000         # instruction budget per script during data generation
MAX_STR_LEN = 48         # longest string value allowed in the state
MAX_STACK = 24
MAX_GLOBALS = 32         # user names -> N0..N31
MAX_LOCALS = 16          # fast locals -> L0..L15 (phase E)
MAX_INSTRS = 999         # instruction indices are three address digits
CONTEXT = 2048           # model context; listing + one step must fit
MAX_LISTING_TOKENS = 1408
MAX_STEP_TOKENS = CONTEXT - MAX_LISTING_TOKENS

DATA_DIR = os.environ.get("BCVM_DATA", os.path.expanduser("~/work/pythonlm-data"))


def require_pinned_python():
    if sys.version_info[:2] != PYTHON_VERSION:
        want = ".".join(map(str, PYTHON_VERSION))
        raise SystemExit(f"bcvm needs Python {want}; running {sys.version.split()[0]}")

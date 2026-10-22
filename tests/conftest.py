import glob
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(__file__))


def natural_files(phase):
    return sorted(glob.glob(os.path.join(ROOT, "natural", f"phase{phase}", "*.py")))


@pytest.fixture(scope="session")
def natural_sample():
    out = []
    for p in "ABC":
        files = natural_files(p)
        out += [(p, f) for f in files[:: max(1, len(files) // 25)]]
    return out

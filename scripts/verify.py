"""Cross-platform environment check — the equivalent of `make verify`.

For students on Windows (or anyone without ``make``). Runs the smoke test and,
if it passes, prints one clear OK line.

Usage:
    python scripts/verify.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
OK_LINE = "Environment OK — the agent can read the repo and run the tests."


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_smoke.py", "-q"],
        cwd=_REPO_ROOT,
    )
    if result.returncode != 0:
        print(
            "\nEnvironment check FAILED. Make sure you installed the "
            "requirements (`pip install -r requirements.txt`) and generated the "
            "fixture (`python scripts/generate_synthetic_fixture.py`).",
            file=sys.stderr,
        )
        return result.returncode

    print(OK_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

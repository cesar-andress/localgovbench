#!/usr/bin/env python3
"""Clean-room style reproducibility check for the active tip.

Distinguishes git-alone vs corpus-dependent vs intentionally unavailable Results.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=check,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument(
        "--require-corpus",
        action="store_true",
        help="Fail if corpus verification fails (default: report only).",
    )
    args = parser.parse_args()

    failures: list[str] = []
    notes: list[str] = []

    # Import / version
    try:
        import localgovbench
        import tomllib

        pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        expected = pyproject["project"]["version"]
        if localgovbench.__version__ != expected:
            failures.append(
                f"version mismatch runtime={localgovbench.__version__} pyproject={expected}"
            )
        else:
            notes.append(f"PASS version={localgovbench.__version__} (git-alone)")
    except Exception as exc:  # noqa: BLE001
        failures.append(f"import/version failed: {exc}")

    # Repository validation
    proc = run([sys.executable, "scripts/validate_repository.py"], check=False)
    if proc.returncode != 0:
        failures.append("validate_repository failed:\n" + proc.stdout + proc.stderr)
    else:
        notes.append("PASS validate_repository (git-alone)")

    # Corpus
    corp = run([sys.executable, "scripts/verify_pilot_corpus.py"], check=False)
    if corp.returncode == 0:
        notes.append("PASS corpus verification (external corpus present)")
    else:
        msg = "Corpus not verified (expected without local CSV). See corpus_acquisition.md."
        if args.require_corpus:
            failures.append(msg + "\n" + corp.stderr)
        else:
            notes.append("WARN " + msg)

    if not args.skip_tests:
        proc = run(
            [
                sys.executable,
                "-m",
                "pytest",
                "localgovbench_measurement_validation/affordance",
                "tests/test_active_documentation_claims.py",
                "tests/test_version_consistency.py",
                "tests/test_legacy_notices.py",
                "-q",
            ],
            check=False,
        )
        if proc.returncode != 0:
            failures.append("pytest failed:\n" + proc.stdout + proc.stderr)
        else:
            notes.append("PASS active pytest suites (git-alone)")

        packet = (
            ROOT
            / "localgovbench_measurement_validation/affordance/coding/pilot_round_01/"
            "coder_packets/pilot_round_01_coder_A.csv"
        )
        proc = run(
            [
                sys.executable,
                "scripts/validate_pilot_packet.py",
                str(packet),
                "--mode",
                "pre",
            ],
            check=False,
        )
        if proc.returncode != 0:
            failures.append("pilot pre-validation failed:\n" + proc.stdout + proc.stderr)
        else:
            notes.append("PASS blank pilot packet validation (git-alone)")

    notes.append(
        "NOTE intentionally unavailable: human coding Results, IRR, realization, gaps"
    )

    for line in notes:
        print(line)
    if failures:
        print("FAILURES:")
        for f in failures:
            print(f)
        return 1
    print("CLEAN_ROOM_CHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

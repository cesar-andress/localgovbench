#!/usr/bin/env python3
"""Validate blank or completed pilot_round_01 coder packets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from localgovbench_measurement_validation.affordance.coding.pilot_launch import (
    PILOT_ROUND_ROOT,
    validate_blank_packet,
    validate_completed_packet,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate pilot_round_01 packets")
    parser.add_argument("path", type=Path, help="CSV packet path")
    parser.add_argument(
        "--mode",
        choices=["pre", "post"],
        default="pre",
        help="pre=blank packet; post=completed packet",
    )
    parser.add_argument(
        "--blank-packet",
        type=Path,
        default=None,
        help="Blank packet for post-mode frozen-context comparison",
    )
    args = parser.parse_args(argv)

    if args.mode == "pre":
        errors = validate_blank_packet(args.path)
    else:
        blank = args.blank_packet
        if blank is None:
            slot = "coder_A" if "coder_A" in args.path.name else "coder_B"
            blank = (
                PILOT_ROUND_ROOT
                / "coder_packets"
                / f"pilot_round_01_{slot}.csv"
            )
        errors = validate_completed_packet(args.path, blank)

    if errors:
        print(f"FAIL ({len(errors)} errors)")
        for e in errors:
            print(f"- {e}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

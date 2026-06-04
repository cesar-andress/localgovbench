#!/usr/bin/env python3
"""Discriminant validity: verify benchmark cases differentiate maturity profiles."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.validation.discriminant import (
    run_discriminant_analysis,
    verify_discriminant_ordering,
)

DEFAULT_CASES = ROOT / "validation" / "benchmark_cases"
DEFAULT_REPORT = ROOT / "validation" / "reports" / "discriminant_validity.md"


def render_report(results: list, errors: list[str]) -> str:
    lines = [
        "# Discriminant Validity Report (Synthetic Cases)",
        "",
        "> Demonstrates that LocalGovBench v0.1 scoring **differentiates** governance maturity profiles.",
        "",
        "| Case | Overall (0–4) | Readiness | Band | Expected band | Match |",
        "|------|---------------|-----------|------|---------------|-------|",
    ]
    for r in results:
        lines.append(
            f"| `{r.case_id}` | {r.overall_maturity} | {r.readiness_index} | "
            f"{r.readiness_band} | {r.expected_band} | {r.band_match} |"
        )
    lines.append("")
    if errors:
        lines.append("## Verification errors")
        for err in errors:
            lines.append(f"- {err}")
    else:
        lines.append("## Verification")
        lines.append("")
        lines.append("All discriminant ordering checks **passed**.")
        lines.append("")
        lines.append("- low < medium < high ≤ sovereign_ready")
        lines.append("- compliance_gap < high (documentation without oversight depth)")
    lines.append("")
    lines.append("---")
    lines.append("*Synthetic data — not empirical validation.*")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run discriminant validity checks.")
    parser.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    results = run_discriminant_analysis(args.cases_dir)
    errors = verify_discriminant_ordering(results)
    report = render_report(results, errors)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")

    print("Discriminant validity analysis")
    print("=" * 40)
    for r in results:
        print(f"  {r.case_id}: maturity={r.overall_maturity}, readiness={r.readiness_index}")
    if errors:
        print("FAILED:")
        for e in errors:
            print(f"  - {e}")
        print(f"Report: {args.output}")
        return 1
    print("All checks passed.")
    print(f"Report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

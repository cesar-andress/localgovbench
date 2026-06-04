#!/usr/bin/env python3
"""Run Governance Readiness Benchmark (GRB) assessment and export Markdown report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.grb.scoring import compute_grb_assessment, render_markdown_report
from localgovbench.grb.specification import GRB_SPEC_VERSION, load_indicator_specification
from localgovbench.utils.io import load_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Run GRB assessment on a municipality YAML file.")
    parser.add_argument(
        "assessment",
        type=Path,
        nargs="?",
        default=ROOT / "examples" / "grb" / "medium_readiness_municipality.yaml",
        help="Path to assessment YAML (default: medium synthetic profile)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Markdown report path (default: reports/<profile>_grb_report.md)",
    )
    args = parser.parse_args()

    assessment_path = args.assessment.resolve()
    if not assessment_path.exists():
        print(f"Assessment file not found: {assessment_path}", file=sys.stderr)
        return 1

    _ = load_indicator_specification()
    payload = load_yaml(assessment_path)
    result = compute_grb_assessment(payload)

    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    profile = payload.get("metadata", {}).get("profile", assessment_path.stem)
    output_path = args.output or (reports_dir / f"{profile}_grb_report.md")
    output_path.write_text(render_markdown_report(result), encoding="utf-8")

    print("GRB Assessment — synthetic validation experiment")
    print("=" * 50)
    print(f"Specification: {GRB_SPEC_VERSION}")
    print(f"Input: {assessment_path.name}")
    print(f"Municipality: {result.municipality}")
    print(f"Overall maturity: {result.overall_maturity} (0–4)")
    print(f"Readiness (raw): {result.readiness_raw}")
    print(f"Readiness (final): {result.readiness_final} — {result.readiness_band}")
    if result.safeguard_applied:
        print(f"Safeguard: {result.safeguard_reason}")
    print(f"Evidence issues: {len(result.evidence_issues)}")
    print(f"Report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

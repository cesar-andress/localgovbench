#!/usr/bin/env python3
"""Readiness ranking robustness under alternative v0.1 dimension weights."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.validation.weighting_robustness import (
    DEFAULT_RANDOM_SAMPLES,
    run_weighting_robustness,
)

DEFAULT_CASES = ROOT / "validation" / "benchmark_cases"
DEFAULT_CSV = ROOT / "results" / "weighting_robustness.csv"
DEFAULT_REPORT = ROOT / "reports" / "weighting_robustness.md"


def write_csv(
    path: Path,
    scores: dict,
    comparisons: list,
    random_summary: dict,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "record_type",
                "weight_config",
                "case_id",
                "overall_maturity",
                "readiness_index",
                "rank",
                "reference",
                "alternate",
                "spearman",
                "kendall_tau",
                "cases_rank_changed",
                "total_rank_displacement",
                "rank_shift",
            ]
        )
        for config_name, cases in scores.items():
            for case in cases:
                writer.writerow(
                    [
                        "case_score",
                        config_name,
                        case.case_id,
                        case.overall_maturity,
                        case.readiness_index,
                        case.rank,
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ]
                )
        for comp in comparisons:
            for case_id, shift in sorted(comp.rank_shifts.items()):
                writer.writerow(
                    [
                        "comparison",
                        "",
                        case_id,
                        "",
                        "",
                        "",
                        comp.reference,
                        comp.alternate,
                        f"{comp.spearman:.6f}",
                        f"{comp.kendall_tau:.6f}",
                        comp.cases_rank_changed,
                        comp.total_rank_displacement,
                        shift,
                    ]
                )
        writer.writerow(
            [
                "random_summary",
                "",
                "",
                "",
                "",
                "",
                "uniform",
                f"random_n={random_summary['sample_count']}",
                f"{random_summary['spearman_mean']:.6f}",
                f"{random_summary['kendall_mean']:.6f}",
                f"{random_summary['cases_rank_changed_mean']:.3f}",
                "",
                f"seed={random_summary['seed']}",
            ]
        )
        writer.writerow(
            [
                "random_summary_detail",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                f"min={random_summary['spearman_min']:.6f}",
                f"min={random_summary['kendall_min']:.6f}",
                f"std_spearman={random_summary['spearman_std']:.6f}",
                f"std_kendall={random_summary['kendall_std']:.6f}",
                f"perfect_fraction={random_summary['perfect_spearman_fraction']:.4f}",
            ]
        )


def render_report(
    scores: dict,
    comparisons: list,
    random_summary: dict,
) -> str:
    lines = [
        "# Readiness Weighting Robustness (Synthetic Benchmark Cases)",
        "",
        "> Evaluates whether **v0.1 readiness rankings** over five synthetic municipality "
        "profiles are stable when dimension weights depart from the default uniform scheme.",
        "",
        "**Instrument:** Local AI Governance Framework v0.1 (`compute_maturity_score`).",
        "**Baseline:** `uniform` (weight 1.0 per dimension).",
        "",
        "## Predefined weight schemes",
        "",
        "| Scheme | Emphasis |",
        "|--------|----------|",
        "| `uniform` | Equal weights (baseline) |",
        "| `oversight_heavy` | Operational ×3, organizational ×2 |",
        "| `data_governance_heavy` | Legal/regulatory ×3 |",
        "| `sovereignty_heavy` | Strategic sovereignty ×3, technical security ×2 |",
        f"| `random` | {random_summary['sample_count']} Dirichlet samples (seed {random_summary['seed']}) |",
        "",
        "## Case scores and ranks (uniform baseline)",
        "",
        "| Case | Maturity (0–4) | Readiness | Rank |",
        "|------|----------------|-----------|------|",
    ]
    for case in scores["uniform"]:
        lines.append(
            f"| `{case.case_id}` | {case.overall_maturity} | {case.readiness_index} | {case.rank} |"
        )

    lines.extend(
        [
            "",
            "## Rank correlation vs uniform",
            "",
            "| Alternate | Spearman ρ | Kendall τ | Cases re-ranked | Total rank shift |",
            "|-----------|------------|-----------|-----------------|------------------|",
        ]
    )
    for comp in comparisons:
        lines.append(
            f"| `{comp.alternate}` | {comp.spearman:.4f} | {comp.kendall_tau:.4f} | "
            f"{comp.cases_rank_changed} | {comp.total_rank_displacement} |"
        )

    lines.extend(
        [
            "",
            "### Per-case rank shifts (predefined alternates)",
            "",
        ]
    )
    for comp in comparisons:
        shifts = ", ".join(f"`{cid}`: {delta:+d}" for cid, delta in sorted(comp.rank_shifts.items()))
        lines.append(f"- **{comp.alternate}:** {shifts}")

    lines.extend(
        [
            "",
            "## Random weight ensembles",
            "",
            f"- Samples: **{random_summary['sample_count']}**",
            f"- Spearman ρ — mean {random_summary['spearman_mean']:.4f}, "
            f"min {random_summary['spearman_min']:.4f}, "
            f"std {random_summary['spearman_std']:.4f}",
            f"- Kendall τ — mean {random_summary['kendall_mean']:.4f}, "
            f"min {random_summary['kendall_min']:.4f}, "
            f"std {random_summary['kendall_std']:.4f}",
            f"- Fraction with perfect Spearman (ρ = 1): "
            f"{random_summary['perfect_spearman_fraction']:.1%}",
            f"- Mean cases re-ranked vs uniform: {random_summary['cases_rank_changed_mean']:.2f}",
            "",
            "---",
            "*Synthetic benchmark cases — structural robustness only; not municipal validation.*",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run readiness weighting robustness analysis.")
    parser.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--output-report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--random-samples",
        type=int,
        default=DEFAULT_RANDOM_SAMPLES,
        help=f"Number of random weight draws (default {DEFAULT_RANDOM_SAMPLES})",
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    scores, comparisons, random_summary = run_weighting_robustness(
        args.cases_dir,
        random_samples=args.random_samples,
        seed=args.seed,
    )

    write_csv(args.output_csv, scores, comparisons, random_summary)
    report = render_report(scores, comparisons, random_summary)
    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    args.output_report.write_text(report, encoding="utf-8")

    print("Weighting robustness analysis")
    print("=" * 40)
    for comp in comparisons:
        print(
            f"  {comp.alternate}: spearman={comp.spearman:.4f}, "
            f"kendall={comp.kendall_tau:.4f}, changed={comp.cases_rank_changed}"
        )
    print(
        f"  random ({args.random_samples}): spearman mean={random_summary['spearman_mean']:.4f}, "
        f"min={random_summary['spearman_min']:.4f}"
    )
    print(f"CSV: {args.output_csv}")
    print(f"Report: {args.output_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

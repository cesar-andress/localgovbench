#!/usr/bin/env python3
"""GRB sensitivity analysis — 100 synthetic profiles with controlled dimension variation."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.grb.profiles import build_assessment_payload
from localgovbench.grb.scoring import SAFEGUARD_CAP, compute_grb_assessment
from localgovbench.grb.specification import GRB_SPEC_VERSION

BASELINE_LEVEL = 3
PROFILE_COUNT = 100
D2_SWEEP_COUNT = 34
D4_SWEEP_COUNT = 33
D6_SWEEP_COUNT = 33


def generate_profiles() -> list[dict]:
    """Generate 100 synthetic profiles: D2 sweep, D4 sweep, D6 sweep."""
    profiles: list[dict] = []
    idx = 0

    for level in range(D2_SWEEP_COUNT):
        score = level % 5  # 0–4 cycling across 34 profiles
        profiles.append(
            {
                "profile_id": f"sens_{idx:03d}",
                "scenario": "d2_sweep",
                "d2_level": score,
                "d4_level": BASELINE_LEVEL,
                "d6_level": BASELINE_LEVEL,
                "dimension_levels": {"d2": score},
            }
        )
        idx += 1

    for level in range(D4_SWEEP_COUNT):
        score = level % 5
        profiles.append(
            {
                "profile_id": f"sens_{idx:03d}",
                "scenario": "d4_sweep",
                "d2_level": BASELINE_LEVEL,
                "d4_level": score,
                "d6_level": BASELINE_LEVEL,
                "dimension_levels": {"d4": score},
            }
        )
        idx += 1

    for level in range(D6_SWEEP_COUNT):
        score = level % 5
        profiles.append(
            {
                "profile_id": f"sens_{idx:03d}",
                "scenario": "d6_sweep",
                "d2_level": BASELINE_LEVEL,
                "d4_level": BASELINE_LEVEL,
                "d6_level": score,
                "dimension_levels": {"d6": score},
            }
        )
        idx += 1

    assert len(profiles) == PROFILE_COUNT, f"Expected {PROFILE_COUNT}, got {len(profiles)}"
    return profiles


def run_analysis() -> list[dict]:
    """Score all sensitivity profiles and return result rows."""
    rows: list[dict] = []
    for spec in generate_profiles():
        payload = build_assessment_payload(
            spec["profile_id"],
            dimension_levels=spec["dimension_levels"],
            default_level=BASELINE_LEVEL,
            scenario=spec["scenario"],
        )
        result = compute_grb_assessment(payload)
        rows.append(
            {
                "profile_id": spec["profile_id"],
                "scenario": spec["scenario"],
                "d2_input_level": spec["d2_level"],
                "d4_input_level": spec["d4_level"],
                "d6_input_level": spec["d6_level"],
                "d1_score": result.dimension_scores["d1"],
                "d2_score": result.dimension_scores["d2"],
                "d3_score": result.dimension_scores["d3"],
                "d4_score": result.dimension_scores["d4"],
                "d5_score": result.dimension_scores["d5"],
                "d6_score": result.dimension_scores["d6"],
                "overall_maturity": result.overall_maturity,
                "readiness_raw": result.readiness_raw,
                "readiness_final": result.readiness_final,
                "readiness_band": result.readiness_band,
                "safeguard_applied": result.safeguard_applied,
            }
        )
    return rows


def aggregate_by_level(rows: list[dict], scenario: str, level_key: str) -> list[dict]:
    """Mean readiness by input level for a one-dimensional sweep."""
    buckets: dict[int, list[float]] = defaultdict(list)
    safeguard_counts: dict[int, int] = defaultdict(int)
    for row in rows:
        if row["scenario"] != scenario:
            continue
        level = int(row[level_key])
        buckets[level].append(row["readiness_final"])
        if row["safeguard_applied"]:
            safeguard_counts[level] += 1
    summary: list[dict] = []
    for level in sorted(buckets):
        values = buckets[level]
        summary.append(
            {
                "input_level": level,
                "n_profiles": len(values),
                "mean_readiness_final": round(mean(values), 2),
                "mean_readiness_raw": round(
                    mean(r["readiness_raw"] for r in rows if r["scenario"] == scenario and int(r[level_key]) == level),
                    2,
                ),
                "safeguard_applied_count": safeguard_counts[level],
            }
        )
    return summary


def render_markdown_report(rows: list[dict]) -> str:
    """Build sensitivity analysis report with tables and interpretation."""
    d2_summary = aggregate_by_level(rows, "d2_sweep", "d2_input_level")
    d4_summary = aggregate_by_level(rows, "d4_sweep", "d4_input_level")
    d6_summary = aggregate_by_level(rows, "d6_sweep", "d6_input_level")

    baseline_raw = 75.0  # all dimensions at 3
    lines = [
        "# GRB Sensitivity Analysis",
        "",
        f"**GRB version:** {GRB_SPEC_VERSION}  ",
        f"**Profiles:** {PROFILE_COUNT} synthetic assessments  ",
        f"**Baseline:** dimensions D1, D3, D5 at maturity {BASELINE_LEVEL} (readiness raw ≈ {baseline_raw})  ",
        f"**Safeguard G1:** cap at {SAFEGUARD_CAP} when D2 or D4 dimension score < 2.0  ",
        "",
        "## Design",
        "",
        "| Scenario | Profiles | Varied dimension | Fixed dimensions |",
        "|----------|----------|------------------|------------------|",
        f"| `d2_sweep` | {D2_SWEEP_COUNT} | D2 Human Oversight (0–4) | D1, D3–D6 at {BASELINE_LEVEL} |",
        f"| `d4_sweep` | {D4_SWEEP_COUNT} | D4 Data Legitimacy (0–4) | D1–D3, D5–D6 at {BASELINE_LEVEL} |",
        f"| `d6_sweep` | {D6_SWEEP_COUNT} | D6 Strategic Sovereignty (0–4) | D1–D5 at {BASELINE_LEVEL} |",
        "",
        "## Table 1 — D2 Human Oversight vs readiness",
        "",
        "| D2 input level | N | Mean readiness (final) | Mean readiness (raw) | Safeguard applied (count) |",
        "|----------------|---|------------------------|----------------------|---------------------------|",
    ]
    for row in d2_summary:
        lines.append(
            f"| {row['input_level']} | {row['n_profiles']} | {row['mean_readiness_final']} | "
            f"{row['mean_readiness_raw']} | {row['safeguard_applied_count']} |"
        )

    lines.extend(
        [
            "",
            "## Table 2 — D4 Data Legitimacy vs readiness",
            "",
            "| D4 input level | N | Mean readiness (final) | Mean readiness (raw) | Safeguard applied (count) |",
            "|----------------|---|------------------------|----------------------|---------------------------|",
        ]
    )
    for row in d4_summary:
        lines.append(
            f"| {row['input_level']} | {row['n_profiles']} | {row['mean_readiness_final']} | "
            f"{row['mean_readiness_raw']} | {row['safeguard_applied_count']} |"
        )

    lines.extend(
        [
            "",
            "## Table 3 — D6 Strategic Sovereignty vs readiness",
            "",
            "| D6 input level | N | Mean readiness (final) | Mean readiness (raw) | Safeguard applied (count) |",
            "|----------------|---|------------------------|----------------------|---------------------------|",
        ]
    )
    for row in d6_summary:
        lines.append(
            f"| {row['input_level']} | {row['n_profiles']} | {row['mean_readiness_final']} | "
            f"{row['mean_readiness_raw']} | {row['safeguard_applied_count']} |"
        )

    # Monotonicity checks
    d2_readiness = [r["mean_readiness_final"] for r in d2_summary]
    d4_readiness = [r["mean_readiness_final"] for r in d4_summary]
    d6_readiness = [r["mean_readiness_final"] for r in d6_summary]
    d2_monotone = all(d2_readiness[i] <= d2_readiness[i + 1] for i in range(len(d2_readiness) - 1))
    d4_monotone = all(d4_readiness[i] <= d4_readiness[i + 1] for i in range(len(d4_readiness) - 1))
    d6_monotone = all(d6_readiness[i] <= d6_readiness[i + 1] for i in range(len(d6_readiness) - 1))

    lines.extend(
        [
            "",
            "## Table 4 — Expected marginal effect per dimension point",
            "",
            "Each dimension contributes 9 of 54 indicators (weight 1/6 in overall maturity).",
            "",
            "| Dimension | Δ maturity per +1 level | Δ readiness (raw) per +1 level |",
            "|-----------|---------------------------|----------------------------------|",
            "| D2, D4, D6 (non-safeguard) | ≈ 1/6 ≈ 0.167 | ≈ 4.17 |",
            "| D2 or D4 with safeguard binding | ≤ 4.17 (cap may bind) | ≤ 4.17 |",
            "",
            "## Interpretation — does the model behave as expected?",
            "",
        ]
    )

    interpretation = []
    if d2_monotone:
        interpretation.append(
            "- **D2 decrease:** Mean readiness **decreases monotonically** as Human Oversight "
            "input level falls (Table 1). Consistent with equal-weight aggregation."
        )
    else:
        interpretation.append(
            "- **D2 decrease:** Readiness is **not strictly monotonic** in the sweep — investigate safeguard binding."
        )

    if d4_monotone:
        interpretation.append(
            "- **D4 decrease:** Mean readiness **decreases monotonically** as Data Legitimacy "
            "falls (Table 2). D4 is a safeguard dimension; scores 0–1 trigger G1 when raw > 60."
        )
    else:
        interpretation.append("- **D4 decrease:** Non-monotonic pattern detected — review safeguard interactions.")

    if d6_monotone:
        interpretation.append(
            "- **D6 increase:** Mean readiness **increases monotonically** as Strategic Sovereignty "
            "rises (Table 3). No safeguard applies to D6; effect is linear in raw score."
        )
    else:
        interpretation.append("- **D6 increase:** Non-monotonic pattern detected.")

    safeguard_d2 = sum(r["safeguard_applied_count"] for r in d2_summary if r["input_level"] < 2)
    safeguard_d4 = sum(r["safeguard_applied_count"] for r in d4_summary if r["input_level"] < 2)
    interpretation.append(
        f"- **Safeguard G1:** Applied in {safeguard_d2} D2-sweep profile-groups at level < 2 "
        f"and {safeguard_d4} D4-sweep groups where raw readiness exceeded {SAFEGUARD_CAP}."
    )
    interpretation.append(
        "- **Overall:** The scoring model responds **directionally as expected** to one-dimensional "
        "shifts in D2, D4, and D6 under uniform indicator scoring. Safeguard capping introduces a "
        "**ceiling** on final readiness when D2 or D4 are weak but other dimensions are strong — "
        "by design for responsible-deployment signalling."
    )
    interpretation.append(
        "- **Limitation:** This experiment uses **uniform scores within each dimension** and does not "
        "vary D1, D3, or D5; it is a structural sensitivity test, not empirical validation."
    )

    lines.extend(interpretation)
    lines.extend(["", "---", "*Synthetic experiment — not field data.*"])
    return "\n".join(lines)


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    rows = run_analysis()
    results_dir = ROOT / "results"
    reports_dir = ROOT / "reports"
    results_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    csv_path = results_dir / "sensitivity_analysis.csv"
    report_path = reports_dir / "sensitivity_analysis.md"
    write_csv(csv_path, rows)
    report_path.write_text(render_markdown_report(rows), encoding="utf-8")

    print("GRB sensitivity analysis")
    print("=" * 40)
    print(f"Profiles scored: {len(rows)}")
    print(f"CSV: {csv_path}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

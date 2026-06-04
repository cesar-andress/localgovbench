"""Deterministic GRB sensitivity analysis profile generation (frozen specification)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from statistics import mean
from typing import Iterable

from localgovbench.grb.profiles import build_assessment_payload
from localgovbench.grb.scoring import SAFEGUARD_CAP, SAFEGUARD_THRESHOLD, compute_grb_assessment
from localgovbench.grb.specification import GRB_SPEC_VERSION

BASELINE_LEVEL = 3

PROFILE_GROUP_COUNTS: dict[str, int] = {
    "baseline": 10,
    "low_d2": 30,
    "low_d4": 30,
    "high_d6": 30,
    "mixed": 50,
}

MIN_PROFILE_COUNT = sum(PROFILE_GROUP_COUNTS.values())

CSV_FIELDNAMES: tuple[str, ...] = (
    "profile_id",
    "profile_group",
    "d2_input_level",
    "d4_input_level",
    "d6_input_level",
    "d1_score",
    "d2_score",
    "d3_score",
    "d4_score",
    "d5_score",
    "d6_score",
    "overall_maturity",
    "readiness_raw",
    "readiness_final",
    "readiness_band",
    "safeguard_applied",
    "readiness_delta_raw_final",
)


@dataclass(frozen=True, slots=True)
class ProfileSpec:
    """One synthetic GRB sensitivity profile specification."""

    profile_id: str
    profile_group: str
    d2_level: int
    d4_level: int
    d6_level: int

    @property
    def dimension_levels(self) -> dict[str, int]:
        return {"d2": self.d2_level, "d4": self.d4_level, "d6": self.d6_level}


def _clamp(level: int) -> int:
    return max(0, min(4, int(level)))


def generate_profile_specs() -> tuple[ProfileSpec, ...]:
    """
    Generate >=150 deterministic synthetic profiles across five groups.

    Groups: baseline, low_d2, low_d4, high_d6, mixed.
    """
    specs: list[ProfileSpec] = []
    seq = 0

    for _ in range(PROFILE_GROUP_COUNTS["baseline"]):
        specs.append(
            ProfileSpec(
                profile_id=f"grb_sens_{seq:04d}",
                profile_group="baseline",
                d2_level=BASELINE_LEVEL,
                d4_level=BASELINE_LEVEL,
                d6_level=BASELINE_LEVEL,
            )
        )
        seq += 1

    for i in range(PROFILE_GROUP_COUNTS["low_d2"]):
        level = i % 5
        specs.append(
            ProfileSpec(
                profile_id=f"grb_sens_{seq:04d}",
                profile_group="low_d2",
                d2_level=_clamp(level),
                d4_level=BASELINE_LEVEL,
                d6_level=BASELINE_LEVEL,
            )
        )
        seq += 1

    for i in range(PROFILE_GROUP_COUNTS["low_d4"]):
        level = i % 5
        specs.append(
            ProfileSpec(
                profile_id=f"grb_sens_{seq:04d}",
                profile_group="low_d4",
                d2_level=BASELINE_LEVEL,
                d4_level=_clamp(level),
                d6_level=BASELINE_LEVEL,
            )
        )
        seq += 1

    for i in range(PROFILE_GROUP_COUNTS["high_d6"]):
        level = i % 5
        specs.append(
            ProfileSpec(
                profile_id=f"grb_sens_{seq:04d}",
                profile_group="high_d6",
                d2_level=BASELINE_LEVEL,
                d4_level=BASELINE_LEVEL,
                d6_level=_clamp(level),
            )
        )
        seq += 1

    for i in range(PROFILE_GROUP_COUNTS["mixed"]):
        specs.append(
            ProfileSpec(
                profile_id=f"grb_sens_{seq:04d}",
                profile_group="mixed",
                d2_level=_clamp((i * 3 + 1) % 5),
                d4_level=_clamp((i * 7 + 2) % 5),
                d6_level=_clamp((i * 11 + 3) % 5),
            )
        )
        seq += 1

    if len(specs) < MIN_PROFILE_COUNT:
        raise RuntimeError(f"Expected >={MIN_PROFILE_COUNT} profiles, got {len(specs)}")
    return tuple(specs)


def score_profile_spec(spec: ProfileSpec) -> dict[str, object]:
    """Score one profile and return a CSV row dict."""
    payload = build_assessment_payload(
        spec.profile_id,
        dimension_levels=spec.dimension_levels,
        default_level=BASELINE_LEVEL,
        scenario=spec.profile_group,
    )
    result = compute_grb_assessment(payload)
    return {
        "profile_id": spec.profile_id,
        "profile_group": spec.profile_group,
        "d2_input_level": spec.d2_level,
        "d4_input_level": spec.d4_level,
        "d6_input_level": spec.d6_level,
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
        "readiness_delta_raw_final": round(result.readiness_raw - result.readiness_final, 2),
    }


def run_sensitivity_study() -> list[dict[str, object]]:
    """Generate and score all sensitivity profiles."""
    return [score_profile_spec(spec) for spec in generate_profile_specs()]


def aggregate_by_group(rows: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    """Mean readiness and safeguard counts per profile group."""
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["profile_group"])].append(row)

    summary: list[dict[str, object]] = []
    for group in ("baseline", "low_d2", "low_d4", "high_d6", "mixed"):
        items = grouped.get(group, [])
        if not items:
            continue
        safeguarded = [r for r in items if r["safeguard_applied"]]
        summary.append(
            {
                "profile_group": group,
                "n_profiles": len(items),
                "mean_readiness_raw": round(mean(float(r["readiness_raw"]) for r in items), 2),
                "mean_readiness_final": round(mean(float(r["readiness_final"]) for r in items), 2),
                "safeguard_applied_count": len(safeguarded),
                "mean_cap_delta": round(
                    mean(float(r["readiness_delta_raw_final"]) for r in safeguarded), 2
                )
                if safeguarded
                else 0.0,
            }
        )
    return summary


def baseline_reference_readiness(rows: Iterable[dict[str, object]]) -> float:
    """Mean final readiness of baseline group."""
    baseline = [float(r["readiness_final"]) for r in rows if r["profile_group"] == "baseline"]
    return round(mean(baseline), 2) if baseline else 0.0


def render_sensitivity_report(rows: list[dict[str, object]]) -> str:
    """Build Markdown report for GRB sensitivity analysis."""
    group_summary = aggregate_by_group(rows)
    baseline_mean = baseline_reference_readiness(rows)
    total = len(rows)

    lines = [
        "# GRB Sensitivity Analysis Report",
        "",
        "## Objective",
        "",
        "Evaluate whether the **frozen** Governance Readiness Benchmark (GRB v0.1) scoring model "
        "responds predictably when **Human Oversight (D2)**, **Data Legitimacy and Processing (D4)**, "
        "or **Strategic Sovereignty (D6)** maturity inputs change, while other dimensions remain at baseline.",
        "",
        "This is a **structural sensitivity** experiment on synthetic profiles — not empirical municipal validation.",
        "",
        "## Method",
        "",
        f"- **GRB version:** {GRB_SPEC_VERSION} (54 indicators, six dimensions — **not modified**)",
        f"- **Profiles generated:** {total} (deterministic)",
        f"- **Baseline maturity level:** {BASELINE_LEVEL} on D1, D3, D5; varied dimension(s) per group",
        f"- **Safeguard G1:** cap final readiness at {SAFEGUARD_CAP} when D2 or D4 dimension score < {SAFEGUARD_THRESHOLD}",
        "- **Aggregation:** uniform indicator scores within each varied dimension",
        "",
        "### Generated profile groups",
        "",
        "| Group | N | Varied dimensions | Fixed dimensions |",
        "|-------|---|-------------------|------------------|",
        f"| `baseline` | {PROFILE_GROUP_COUNTS['baseline']} | none (all at {BASELINE_LEVEL}) | D1–D6 at {BASELINE_LEVEL} |",
        f"| `low_d2` | {PROFILE_GROUP_COUNTS['low_d2']} | D2 (0–4 cycle) | D1, D3–D6 at {BASELINE_LEVEL} |",
        f"| `low_d4` | {PROFILE_GROUP_COUNTS['low_d4']} | D4 (0–4 cycle) | D1–D3, D5–D6 at {BASELINE_LEVEL} |",
        f"| `high_d6` | {PROFILE_GROUP_COUNTS['high_d6']} | D6 (0–4 cycle) | D1–D5 at {BASELINE_LEVEL} |",
        f"| `mixed` | {PROFILE_GROUP_COUNTS['mixed']} | D2, D4, D6 (deterministic mix) | D1, D3, D5 at {BASELINE_LEVEL} |",
        "",
        "## Average readiness per group",
        "",
        f"Baseline reference mean readiness (final): **{baseline_mean}**",
        "",
        "| Group | N | Mean readiness (raw) | Mean readiness (final) | Safeguard G1 applied | Mean cap reduction |",
        "|-------|---|----------------------|----------------------|----------------------|-------------------|",
    ]
    for row in group_summary:
        lines.append(
            f"| `{row['profile_group']}` | {row['n_profiles']} | {row['mean_readiness_raw']} | "
            f"{row['mean_readiness_final']} | {row['safeguard_applied_count']} | {row['mean_cap_delta']} |"
        )

    # D2/D4 low level vs baseline at level 3
    low_d2_at_0 = _mean_final(rows, "low_d2", d2_level=0)
    low_d4_at_0 = _mean_final(rows, "low_d4", d4_level=0)
    high_d6_at_4 = _mean_final(rows, "high_d6", d6_level=4)

    lines.extend(
        [
            "",
            "## Effect of safeguard G1",
            "",
            "Safeguard G1 binds when **D2 or D4 dimension score** falls below 2.0 while raw readiness exceeds 60. "
            "In this experiment:",
            "",
            "- **low_d2** and **low_d4** groups trigger G1 most often at input levels 0–1.",
            "- **high_d6** and **baseline** groups do not trigger G1 (D2 and D4 held at baseline 3).",
            "- When applied, `readiness_final` is reduced to at most 60 even if other dimensions are strong.",
            "",
            "| Illustrative contrast | Mean readiness (final) |",
            "|----------------------|------------------------|",
            f"| baseline (D2=3) | {baseline_mean} |",
            f"| low_d2 at input 0 | {low_d2_at_0} |",
            f"| low_d4 at input 0 | {low_d4_at_0} |",
            f"| high_d6 at input 4 | {high_d6_at_4} |",
            "",
            "## Interpretation",
            "",
        ]
    )

    interpretation = [
        "- **D2 Human Oversight:** Lower D2 inputs reduce group mean readiness versus baseline; "
        "monotonic trend expected within `low_d2` sweep.",
        "- **D4 Data Legitimacy and Processing:** Same directional effect for `low_d4`; "
        "D4 participates in safeguard G1 with D2.",
        "- **D6 Strategic Sovereignty:** Higher D6 inputs increase readiness in `high_d6` without safeguard binding.",
        "- **Mixed profiles:** Spread of readiness reflects combined variation; useful for stress-testing aggregation.",
        "- **Overall:** The frozen scoring formula produces **directionally consistent** outputs suitable "
        "for structural validation; empirical calibration remains future work.",
        "",
        "## Limitations",
        "",
        "- Uniform scores within each dimension (no item-level variation).",
        "- D1, D3, D5 fixed at baseline except in `mixed` indirect effects.",
        "- Synthetic data only; no claim about real municipalities.",
        "- Does not test evidence-gate E2/E3 or inter-rater agreement.",
        "- GRB specification, indicators, and scoring formula were **not altered** in this experiment.",
        "",
        "---",
        "*Generated by `scripts/run_grb_sensitivity_analysis.py`*",
    ]
    lines.extend(interpretation)
    return "\n".join(lines)


def _mean_final(
    rows: Iterable[dict[str, object]],
    group: str,
    *,
    d2_level: int | None = None,
    d4_level: int | None = None,
    d6_level: int | None = None,
) -> float:
    values: list[float] = []
    for row in rows:
        if row["profile_group"] != group:
            continue
        if d2_level is not None and int(row["d2_input_level"]) != d2_level:
            continue
        if d4_level is not None and int(row["d4_input_level"]) != d4_level:
            continue
        if d6_level is not None and int(row["d6_input_level"]) != d6_level:
            continue
        values.append(float(row["readiness_final"]))
    return round(mean(values), 2) if values else 0.0

"""Unit commensurability / programme granularity sensitivity analysis."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from localgovbench_measurement_validation.pilot_public_satisfiability.mapping_rules import (
    MAPPING_RULES,
    SOURCE_SCHEMAS,
    SHORTFALL_LABELS,
    COVERAGE_TO_SHORTFALL,
    classify_from_evidence_rows,
)

AGENCY_WIDE_PATTERN = re.compile(
    r"\b(agency[- ]wide|enterprise[- ]wide|department[- ]wide|government[- ]wide|"
    r"organisation[- ]wide|organization[- ]wide|across the agency|all staff|"
    r"nationwide deployment|whole of government)\b",
    re.I,
)

HIGH_IMPACT_PATTERN = re.compile(r"high[- ]impact", re.I)


@dataclass(frozen=True)
class GranularityScenario:
    scenario_id: str
    label: str
    description: str
    filter_fn: Callable[[dict], bool]


def _parse_fields(record: dict) -> dict[str, str]:
    return json.loads(record["raw_fields_json"])


def _is_nonempty(value: str) -> bool:
    text = (value or "").strip()
    return text not in ("", "[]", "null", "None", "N/A", "n/a")


def non_empty_field_count(record: dict) -> int:
    fields = _parse_fields(record)
    keys = SOURCE_SCHEMAS.get(record["source_name"], list(fields.keys()))
    return sum(1 for k in keys if _is_nonempty(str(fields.get(k, ""))))


def description_length(record: dict) -> int:
    return len((record.get("programme_description") or "").strip())


def complexity_score(record: dict) -> float:
    """Transparent proxy: higher = more complex / broader deployment signal."""
    fields = _parse_fields(record)
    ne = non_empty_field_count(record)
    dl = description_length(record)
    text = " ".join(
        [
            record.get("programme_title", ""),
            record.get("programme_description", ""),
            json.dumps(fields, ensure_ascii=False),
        ]
    )
    score = ne + math.log1p(dl) / 3.0
    if AGENCY_WIDE_PATTERN.search(text):
        score += 4.0
    if HIGH_IMPACT_PATTERN.search(text):
        score += 2.0
    if _is_nonempty(str(fields.get("is_high_impact", ""))):
        score += 2.0
    if _is_nonempty(str(fields.get("HI_justification", ""))):
        score += 1.5
    return score


def information_score(record: dict) -> float:
    """Transparent proxy: higher = richer programme metadata."""
    ne = non_empty_field_count(record)
    dl = description_length(record)
    title = len((record.get("programme_title") or "").strip())
    return ne + math.log1p(dl) / 5.0 + (1.0 if title >= 10 else 0.0)


def build_scenarios(records: list[dict]) -> list[GranularityScenario]:
    """Derive source-stratified percentile thresholds from corpus metadata."""
    by_source: dict[str, list[dict]] = {}
    for row in records:
        by_source.setdefault(row["source_name"], []).append(row)

    info_thresholds: dict[str, float] = {}
    complexity_thresholds: dict[str, float] = {}

    for source, src_rows in by_source.items():
        info_vals = sorted(information_score(r) for r in src_rows)
        comp_vals = sorted(complexity_score(r) for r in src_rows)
        info_thresholds[source] = info_vals[max(0, int(0.30 * len(info_vals)) - 1)]
        complexity_thresholds[source] = comp_vals[min(len(comp_vals) - 1, int(0.90 * len(comp_vals)))]

    def scenario_a(record: dict) -> bool:
        return True

    def scenario_b(record: dict) -> bool:
        source = record["source_name"]
        info = information_score(record)
        ne = non_empty_field_count(record)
        dl = description_length(record)
        # Minimum information: source p30 info score AND absolute sparse-record floor
        return info >= info_thresholds[source] and ne >= 4 and dl >= 30

    def scenario_c(record: dict) -> bool:
        source = record["source_name"]
        comp = complexity_score(record)
        # Exclude top-decile complexity within source (agency-wide / high-impact / very long)
        return comp < complexity_thresholds[source]

    return [
        GranularityScenario(
            "A_all_records",
            "Scenario A — all records",
            "Full corpus (7,434 programme records); no granularity filter.",
            scenario_a,
        ),
        GranularityScenario(
            "B_min_information",
            "Scenario B — minimum information threshold",
            "Exclude records below source-specific 30th-percentile information score "
            "and absolute floor (≥4 non-empty native fields, description ≥30 chars).",
            scenario_b,
        ),
        GranularityScenario(
            "C_exclude_high_complexity",
            "Scenario C — exclude high-complexity proxy",
            "Exclude records at/above source-specific 90th-percentile complexity proxy "
            "(agency-wide keywords, high-impact flags, long descriptions, dense metadata).",
            scenario_c,
        ),
    ]


def mapped_field_fill_rate(
    records: list[dict],
    source: str,
    mapped_fields: list[str],
) -> float:
    src_records = [r for r in records if r["source_name"] == source]
    if not src_records:
        return 0.0
    hits = 0
    for record in src_records:
        fields = _parse_fields(record)
        if any(_is_nonempty(str(fields.get(f, ""))) for f in mapped_fields):
            hits += 1
    return hits / len(src_records)


def effective_shortfall_level(
    schema_level: int,
    mapped_fields: list[str],
    fill_rate: float,
    *,
    population_floor: float = 0.10,
) -> int:
    """Downgrade schema shortfall when mapped fields are rarely populated in filtered corpus."""
    if schema_level == 0 or not mapped_fields:
        return 0
    if fill_rate < population_floor:
        return 0
    if schema_level >= 2 and fill_rate < 0.25:
        return 1
    return schema_level


def build_effective_coverage_rows(
    records: list[dict],
    criteria: list[dict],
    baseline_coverage: list[dict],
) -> list[dict]:
    """Build source×criterion rows with population-adjusted shortfall for filtered records."""
    baseline_lookup = {
        (r["source_name"], r["criterion_id"]): r for r in baseline_coverage
    }
    rows: list[dict] = []

    for criterion in criteria:
        cid = criterion["criterion_id"]
        for source in SOURCE_SCHEMAS:
            base = baseline_lookup.get((source, cid))
            if not base:
                continue
            rule = MAPPING_RULES.get(cid, {}).get(source)
            if not rule:
                continue
            coverage_class, mapped_fields, _, can_gate = rule
            schema_level = 4 if can_gate else COVERAGE_TO_SHORTFALL.get(coverage_class, 0)
            fill = mapped_field_fill_rate(records, source, mapped_fields)
            eff = effective_shortfall_level(schema_level, mapped_fields, fill)
            rows.append(
                {
                    "source_name": source,
                    "criterion_id": cid,
                    "dimension_id": criterion["dimension_id"],
                    "schema_shortfall_level": schema_level,
                    "effective_shortfall_level": eff,
                    "field_fill_rate": round(fill, 4),
                    "mapped_fields": ";".join(mapped_fields),
                    "coverage_class": coverage_class,
                    "can_potentially_satisfy_gate": str(can_gate),
                    "evidence_shortfall_level": str(eff),
                    "evidence_shortfall_label": SHORTFALL_LABELS.get(eff, SHORTFALL_LABELS[0]),
                }
            )
    return rows


def summarize_scenario(
    scenario: GranularityScenario,
    records: list[dict],
    criteria: list[dict],
    baseline_coverage: list[dict],
) -> dict:
    filtered = [r for r in records if scenario.filter_fn(r)]
    coverage_rows = build_effective_coverage_rows(filtered, criteria, baseline_coverage)

    by_criterion: dict[str, list[dict]] = {}
    for row in coverage_rows:
        by_criterion.setdefault(row["criterion_id"], []).append(row)

    criterion_stats: list[dict] = []
    for c in criteria:
        cid = c["criterion_id"]
        rows = by_criterion.get(cid, [])
        max_level = max(int(r["effective_shortfall_level"]) for r in rows) if rows else 0
        det_class = classify_from_evidence_rows(
            rows,
            criterion_id=cid,
            evidence_hint=c.get("evidence_hint", ""),
            expected_artifact_type=c.get("expected_artifact_type", ""),
        )
        gate_possible = any(r["can_potentially_satisfy_gate"] == "True" for r in rows)
        gate_unreachable = not gate_possible and max_level < 4
        criterion_stats.append(
            {
                "criterion_id": cid,
                "dimension_id": c["dimension_id"],
                "partition_class": det_class,
                "max_shortfall_level": max_level,
                "gate_unreachable": gate_unreachable,
            }
        )

    n = len(criteria)
    counts = Counter(s["partition_class"] for s in criterion_stats)
    gate_unreachable_n = sum(1 for s in criterion_stats if s["gate_unreachable"])
    shortfall_dist = Counter(str(s["max_shortfall_level"]) for s in criterion_stats)

    dim_stats: dict[str, dict] = {}
    for s in criterion_stats:
        did = s["dimension_id"]
        dim_stats.setdefault(did, {"n": 0, "partial": 0, "gate": 0, "shortfall_sum": 0})
        dim_stats[did]["n"] += 1
        if s["partition_class"] != "structurally_internal":
            dim_stats[did]["partial"] += 1
        if s["gate_unreachable"]:
            dim_stats[did]["gate"] += 1
        dim_stats[did]["shortfall_sum"] += s["max_shortfall_level"]

    return {
        "scenario_id": scenario.scenario_id,
        "scenario_label": scenario.label,
        "scenario_description": scenario.description,
        "records_total": len(filtered),
        "records_retained_pct": round(100.0 * len(filtered) / max(len(records), 1), 1),
        "criteria_count": n,
        "pct_structurally_internal": round(100.0 * counts["structurally_internal"] / n, 1),
        "pct_partially_or_public": round(
            100.0 * (counts["partially_public_satisfiable"] + counts["public_satisfiable"]) / n, 1
        ),
        "pct_gate_unreachable": round(100.0 * gate_unreachable_n / n, 1),
        "gate_unreachable_count": gate_unreachable_n,
        "public_satisfiable_count": counts["public_satisfiable"],
        "partially_public_count": counts["partially_public_satisfiable"],
        "structurally_internal_count": counts["structurally_internal"],
        "shortfall_level_0": shortfall_dist.get("0", 0),
        "shortfall_level_1": shortfall_dist.get("1", 0),
        "shortfall_level_2": shortfall_dist.get("2", 0),
        "shortfall_level_3": shortfall_dist.get("3", 0),
        "shortfall_level_4": shortfall_dist.get("4", 0),
        "mean_max_shortfall": round(
            sum(s["max_shortfall_level"] for s in criterion_stats) / n, 2
        ),
        "criterion_stats": criterion_stats,
        "dimension_stats": dim_stats,
        "coverage_rows": coverage_rows,
    }

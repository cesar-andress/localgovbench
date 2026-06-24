#!/usr/bin/env python3
"""Sensitivity analysis: conservative vs liberal partition scenarios."""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench_measurement_validation.pilot_public_satisfiability.mapping_rules import (  # noqa: E402
    classify_from_evidence_rows,
)
from localgovbench_measurement_validation.pilot_public_satisfiability.pilot_paths import (  # noqa: E402
    CONFIG_CRITERIA,
    FIELD_COVERAGE_MATRIX,
    OUTPUTS,
    SENSITIVITY_MAIN,
    SENSITIVITY_SCENARIOS,
)


def load_coverage() -> list[dict]:
    with FIELD_COVERAGE_MATRIX.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_criteria() -> list[dict]:
    data = yaml.safe_load(CONFIG_CRITERIA.read_text(encoding="utf-8"))
    return data["criteria"]


def baseline_class(rows: list[dict], prelim: str, meta: dict) -> str:
    return classify_from_evidence_rows(
        rows,
        criterion_id=meta["criterion_id"],
        evidence_hint=meta.get("evidence_hint", ""),
        expected_artifact_type=meta.get("expected_artifact_type", ""),
    )


def conservative_class(rows: list[dict], prelim: str, meta: dict) -> str:
    """Downgrade borderline partial criteria to structurally_internal."""
    base = baseline_class(rows, prelim, meta)
    max_level = max(int(r["evidence_shortfall_level"]) for r in rows)
    has_direct = any(r["coverage_class"] == "direct_field" for r in rows)
    if base == "partially_public_satisfiable" and max_level <= 1 and not has_direct:
        return "structurally_internal"
    if base == "public_satisfiable" and max_level < 3:
        return "partially_public_satisfiable"
    return base


def liberal_class(rows: list[dict], prelim: str, meta: dict) -> str:
    """Upgrade borderline internal criteria when any source shows level ≥2."""
    max_level = max(int(r["evidence_shortfall_level"]) for r in rows)
    if max_level >= 2:
        if meta["criterion_id"] == "operational_lifecycle_management":
            return "public_satisfiable"
        return "partially_public_satisfiable"
    if any(int(r["evidence_shortfall_level"]) >= 1 for r in rows):
        return "partially_public_satisfiable"
    return "structurally_internal"


def gate_unreachable(rows: list[dict]) -> bool:
    return not any(r["can_potentially_satisfy_gate"] == "True" for r in rows) and all(
        int(r["evidence_shortfall_level"]) < 4 for r in rows
    )


def summarize(scenario: str, classes: dict[str, str], gate_flags: dict[str, bool], criteria: list[dict]) -> dict:
    n = len(criteria)
    counts = Counter(classes.values())
    pct_internal = 100.0 * counts.get("structurally_internal", 0) / n
    pct_partial = 100.0 * (
        counts.get("partially_public_satisfiable", 0) + counts.get("public_satisfiable", 0)
    ) / n
    pct_gate = 100.0 * sum(1 for v in gate_flags.values() if v) / n

    dim_stats: dict[str, dict] = defaultdict(lambda: {"partial": 0, "n": 0, "gate": 0})
    for c in criteria:
        cid = c["criterion_id"]
        did = c["dimension_id"]
        dim_stats[did]["n"] += 1
        if classes[cid] != "structurally_internal":
            dim_stats[did]["partial"] += 1
        if gate_flags[cid]:
            dim_stats[did]["gate"] += 1

    dim_ceiling = {
        did: round(100.0 * s["partial"] / s["n"], 1) for did, s in dim_stats.items()
    }
    dim_gate = {did: round(100.0 * s["gate"] / s["n"], 1) for did, s in dim_stats.items()}

    return {
        "scenario": scenario,
        "pct_structurally_internal": round(pct_internal, 1),
        "pct_partially_or_public_satisfiable": round(pct_partial, 1),
        "pct_gate_unreachable": round(pct_gate, 1),
        "structurally_internal_count": counts.get("structurally_internal", 0),
        "partially_public_count": counts.get("partially_public_satisfiable", 0),
        "public_satisfiable_count": counts.get("public_satisfiable", 0),
        "dimension_ceiling_json": str(dim_ceiling),
        "dimension_gate_unreachable_json": str(dim_gate),
    }


def main() -> int:
    coverage = load_coverage()
    criteria = load_criteria()
    by_criterion: dict[str, list[dict]] = defaultdict(list)
    for row in coverage:
        by_criterion[row["criterion_id"]].append(row)

    scenario_defs = {
        "baseline": baseline_class,
        "conservative": conservative_class,
        "liberal": liberal_class,
    }

    scenario_rows: list[dict] = []
    main_rows: list[dict] = []

    for scenario_name, classifier in scenario_defs.items():
        classes: dict[str, str] = {}
        gate_flags: dict[str, bool] = {}
        for c in criteria:
            cid = c["criterion_id"]
            rows = by_criterion[cid]
            classes[cid] = classifier(rows, c["preliminary_public_satisfiability_class"], c)
            gate_flags[cid] = gate_unreachable(rows)
            scenario_rows.append(
                {
                    "scenario": scenario_name,
                    "criterion_id": cid,
                    "dimension_id": c["dimension_id"],
                    "assigned_class": classes[cid],
                    "gate_unreachable": str(gate_flags[cid]),
                    "max_shortfall_level": max(int(r["evidence_shortfall_level"]) for r in rows),
                }
            )

        main_rows.append(summarize(scenario_name, classes, gate_flags, criteria))

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    with SENSITIVITY_SCENARIOS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scenario_rows[0].keys()))
        writer.writeheader()
        writer.writerows(scenario_rows)

    with SENSITIVITY_MAIN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(main_rows[0].keys()))
        writer.writeheader()
        writer.writerows(main_rows)

    print(f"Wrote {SENSITIVITY_SCENARIOS.relative_to(ROOT)}")
    print(f"Wrote {SENSITIVITY_MAIN.relative_to(ROOT)}")
    for row in main_rows:
        print(
            f"  {row['scenario']}: internal={row['pct_structurally_internal']}% "
            f"partial+={row['pct_partially_or_public_satisfiable']}% "
            f"gate_unreachable={row['pct_gate_unreachable']}%"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

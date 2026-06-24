#!/usr/bin/env python3
"""Derive minimum non-public evidence set for gate-unreachable criteria."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench_measurement_validation.pilot_public_satisfiability.pilot_paths import (  # noqa: E402
    CONFIG_CRITERIA,
    FIELD_COVERAGE_MATRIX,
    MINIMUM_INTERNAL,
    OUTPUTS,
)

INTERNAL_SOURCE_TYPES: dict[str, str] = {
    "legal_regulatory": "compliance_records / legal register",
    "technical_security": "security_operations / architecture repository",
    "organizational": "governance_charter / procurement_file / HR_role_matrix",
    "operational": "MLOps_runbook / monitoring_dashboard / IR_playbook",
    "strategic_sovereignty": "infrastructure_design / vendor_exit_plan / data_residency_memo",
}


def load_coverage() -> list[dict]:
    with FIELD_COVERAGE_MATRIX.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_criteria() -> dict[str, dict]:
    data = yaml.safe_load(CONFIG_CRITERIA.read_text(encoding="utf-8"))
    return {c["criterion_id"]: c for c in data["criteria"]}


def main() -> int:
    coverage = load_coverage()
    criteria = load_criteria()
    by_criterion: dict[str, list[dict]] = defaultdict(list)
    for row in coverage:
        by_criterion[row["criterion_id"]].append(row)

    rows: list[dict] = []
    for cid, meta in criteria.items():
        src_rows = by_criterion[cid]
        max_level = max(int(r["evidence_shortfall_level"]) for r in src_rows)
        gate_possible = any(r["can_potentially_satisfy_gate"] == "True" for r in src_rows)
        if gate_possible or max_level >= 4:
            continue

        best = max(src_rows, key=lambda r: int(r["evidence_shortfall_level"]))
        why_parts = sorted({r["reason_gate_not_reachable"] for r in src_rows if r["reason_gate_not_reachable"]})
        why = why_parts[0] if len(why_parts) == 1 else (
            f"Across {len(src_rows)} sources max shortfall level {max_level}; "
            f"best public signal from {best['source_name']} ({best['evidence_shortfall_label']})."
        )

        rows.append(
            {
                "criterion_id": cid,
                "dimension": meta["dimension_name"],
                "dimension_id": meta["dimension_id"],
                "evidence_hint": meta.get("evidence_hint", ""),
                "required_internal_artifact": meta.get("expected_artifact_type", ""),
                "why_public_inventory_is_insufficient": why,
                "recommended_internal_source_type": INTERNAL_SOURCE_TYPES.get(
                    meta["dimension_id"], "programme_dossier"
                ),
                "max_public_shortfall_level": max_level,
                "best_public_source": best["source_name"],
            }
        )

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "criterion_id",
        "dimension",
        "dimension_id",
        "evidence_hint",
        "required_internal_artifact",
        "why_public_inventory_is_insufficient",
        "recommended_internal_source_type",
        "max_public_shortfall_level",
        "best_public_source",
    ]
    with MINIMUM_INTERNAL.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {MINIMUM_INTERNAL.relative_to(ROOT)} ({len(rows)} criteria)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

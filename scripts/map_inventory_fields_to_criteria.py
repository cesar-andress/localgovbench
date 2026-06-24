#!/usr/bin/env python3
"""Map native inventory fields to LocalGovBench criteria (coverage + shortfall matrix)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench_measurement_validation.pilot_public_satisfiability.mapping_rules import (  # noqa: E402
    MAPPING_RULES,
    SOURCE_SCHEMAS,
    compute_shortfall,
)
from localgovbench_measurement_validation.pilot_public_satisfiability.pilot_paths import (  # noqa: E402
    CONFIG_CRITERIA,
    FIELD_COVERAGE_MATRIX,
    OUTPUTS,
)


def load_criteria_meta() -> dict[str, dict]:
    data = yaml.safe_load(CONFIG_CRITERIA.read_text(encoding="utf-8"))
    return {c["criterion_id"]: c for c in data["criteria"]}


def main() -> int:
    if not CONFIG_CRITERIA.is_file():
        print("Run: python3.12 scripts/generate_localgovbench_criteria_config.py", file=sys.stderr)
        return 1

    criteria_meta = load_criteria_meta()
    criterion_ids = list(criteria_meta.keys())
    sources = sorted(SOURCE_SCHEMAS.keys())
    rows: list[dict[str, str]] = []

    for source in sources:
        all_fields = SOURCE_SCHEMAS[source]
        for cid in criterion_ids:
            rule = MAPPING_RULES.get(cid, {}).get(
                source,
                ("no_public_field", [], "No mapping defined.", False),
            )
            coverage, fields, rationale, can_gate = rule
            meta = criteria_meta[cid]
            level, label, reason = compute_shortfall(
                coverage,
                can_gate,
                meta.get("expected_artifact_type", "primary artefact"),
            )
            rows.append(
                {
                    "source_name": source,
                    "criterion_id": cid,
                    "dimension_id": meta["dimension_id"],
                    "native_fields_available": ";".join(all_fields),
                    "mapped_fields": ";".join(fields),
                    "can_potentially_satisfy_gate": str(can_gate),
                    "coverage_class": coverage,
                    "mapping_rationale": rationale,
                    "evidence_shortfall_level": str(level),
                    "evidence_shortfall_label": label,
                    "reason_gate_not_reachable": reason,
                }
            )

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source_name",
        "criterion_id",
        "dimension_id",
        "native_fields_available",
        "mapped_fields",
        "can_potentially_satisfy_gate",
        "coverage_class",
        "mapping_rationale",
        "evidence_shortfall_level",
        "evidence_shortfall_label",
        "reason_gate_not_reachable",
    ]
    with FIELD_COVERAGE_MATRIX.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {FIELD_COVERAGE_MATRIX.relative_to(ROOT)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

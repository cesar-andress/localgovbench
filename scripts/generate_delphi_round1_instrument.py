#!/usr/bin/env python3
"""Generate Delphi Round 1 instrument from frozen LocalGovBench v0.1 criteria."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.framework.dimensions import FRAMEWORK_VERSION, GOVERNANCE_DIMENSIONS
from localgovbench.framework.scoring import MATURITY_LEVELS, MATURITY_LABELS

OUTPUT = ROOT / "validation" / "content_validity" / "delphi" / "delphi_round1_instrument.yaml"
TRACEABILITY_CSV = ROOT / "data" / "traceability" / "indicator_mapping.csv"

STUDY_FRAMING = {
    "construct": "Programme-Level Governance Readiness",
    "evidence_layer": "confidential programme dossier",
    "forbidden_basis": "public-document observability",
    "instruction": (
        "Rate each criterion for assessing a bounded municipal AI/LLM programme dossier "
        "using evidence-gated assessor review. Do not rate public AI registers, transparency "
        "portals, or open-web documentary observability. Do not assign maturity scores for "
        "any municipality in Round 1."
    ),
}


def load_traceability() -> dict[str, list[dict[str, str]]]:
    """Group traceability rows by full criterion indicator_id."""
    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    if not TRACEABILITY_CSV.is_file():
        return by_id
    with TRACEABILITY_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            cid = row["indicator_id"].strip()
            by_id[cid].append(
                {
                    "governance_requirement": row["governance_requirement"].strip(),
                    "source_framework": row["source_framework"].strip(),
                    "source_concept": row["source_concept"].strip(),
                    "rationale": row["rationale"].strip(),
                }
            )
    return dict(by_id)


def build_assessment_question(statement: str) -> str:
    return (
        "For a bounded municipal AI/LLM programme dossier, is the following criterion "
        f"relevant and clearly worded for programme-level governance readiness assessment? "
        f"Criterion: {statement}"
    )


def build_criteria(traceability: dict[str, list[dict[str, str]]]) -> tuple[list[dict], list[str]]:
    items: list[dict] = []
    missing_trace: list[str] = []
    for dimension in GOVERNANCE_DIMENSIONS:
        for criterion in dimension.criteria:
            criterion_id = f"{dimension.id}_{criterion.id}"
            refs = traceability.get(criterion_id, [])
            if not refs:
                missing_trace.append(criterion_id)
            items.append(
                {
                    "criterion_id": criterion_id,
                    "dimension_id": dimension.id,
                    "dimension_name": dimension.name,
                    "assessment_question": build_assessment_question(criterion.statement),
                    "criterion_statement": criterion.statement,
                    "documentation_hint": criterion.suggested_evidence,
                    "risk_if_missing": criterion.risk_if_missing,
                    "traceability_references": refs,
                    "synthetic": False,
                    "response": {
                        "relevance_1_5": None,
                        "clarity_1_5": None,
                        "essential_yes_no": None,
                        "suggested_revision": None,
                        "comment": None,
                    },
                }
            )
    return items, missing_trace


def build_document() -> dict:
    traceability = load_traceability()
    criteria, missing_trace = build_criteria(traceability)
    maturity_reference = {
        str(level): {"label": MATURITY_LABELS[level], "description": desc}
        for level, (_, desc) in sorted(MATURITY_LEVELS.items())
    }
    return {
        "schema_version": "1.1",
        "generated_by": "scripts/generate_delphi_round1_instrument.py",
        "generated_on": date.today().isoformat(),
        "study_label": "localgovbench_instrument_validation_redevelop",
        "instrument_version": "v0.1.0",
        "instrument_id": "localgovbench-v0.1",
        "framework_version": FRAMEWORK_VERSION,
        "round": 1,
        "synthetic": False,
        "study_framing": STUDY_FRAMING,
        "validation_scope_guard": {
            "study_type": "instrument_content_validity",
            "unit_of_evaluation": "criterion_definitions",
            "evidence_basis": "confidential programme dossier",
            "forbidden_primary_evidence": [
                "public_document_observability",
                "public_ai_registers",
                "transparency_portals",
                "open_pilot",
            ],
        },
        "scales": {
            "relevance_1_5": {
                "range": [1, 5],
                "labels": {
                    1: "not relevant",
                    2: "somewhat relevant",
                    3: "moderately relevant",
                    4: "relevant",
                    5: "highly relevant",
                },
            },
            "clarity_1_5": {
                "range": [1, 5],
                "labels": {1: "very unclear", 5: "very clear"},
            },
            "essential_yes_no": {
                "type": "boolean",
                "note": "Lawshe essentiality for programme-level dossier assessment",
            },
        },
        "maturity_scale_reference": maturity_reference,
        "criteria": criteria,
        "analysis_thresholds": {
            "icvi_minimum": 0.78,
            "target_s_cvi_ave": 0.90,
        },
        "response_storage": {
            "path": "validation/content_validity/delphi/responses/",
            "gitignore": True,
        },
        "generation_report": {
            "criteria_count": len(criteria),
            "dimensions_count": len(GOVERNANCE_DIMENSIONS),
            "missing_traceability_mappings": missing_trace,
        },
    }


def main() -> int:
    try:
        import yaml
    except ImportError:
        print("PyYAML required: pip install pyyaml (or pip install -e '.[dev]')", file=sys.stderr)
        return 1

    doc = build_document()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "# Delphi Round 1 — generated from LocalGovBench v0.1 (25 criteria)\n"
        "# Regenerate: python3.12 scripts/generate_delphi_round1_instrument.py\n"
        "# NOT a public-document observability study.\n\n"
    )
    body = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100)
    OUTPUT.write_text(header + body, encoding="utf-8")

    report = doc["generation_report"]
    dims = sorted({c["dimension_id"] for c in doc["criteria"]})
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    print(f"  Criteria: {report['criteria_count']}")
    print(f"  Dimensions ({len(dims)}): {', '.join(dims)}")
    if report["missing_traceability_mappings"]:
        print(f"  Missing traceability: {len(report['missing_traceability_mappings'])}")
        for cid in report["missing_traceability_mappings"]:
            print(f"    - {cid}")
    else:
        print("  Missing traceability: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

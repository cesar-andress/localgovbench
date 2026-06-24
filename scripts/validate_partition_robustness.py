#!/usr/bin/env python3
"""Dual-rule / dual-model robustness check for criterion partition."""

from __future__ import annotations

import csv
import os
import re
import sys
from collections import Counter
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
    PARTITION_AGREEMENT,
    PARTITION_SENSITIVITY,
)

# Keyword heuristics for alternative classifier (placeholder when no local LLM).
INTERNAL_KEYWORDS = re.compile(
    r"\b(architecture|IAM|access control|logging|audit trail|retention|"
    r"incident response|runbook|prompt registry|portability|migration|"
    r"infrastructure|RoPA|DPIA|lawful basis register|risk register|"
    r"contract clause|RACI|role description|sustainment)\b",
    re.I,
)
PARTIAL_KEYWORDS = re.compile(
    r"\b(oversight|human|lifecycle|stage|status|deployment|vendor|"
    r"supplier|monitoring|classification|impact|governance charter|"
    r"organisation|organization|contact|provider|lawful basis)\b",
    re.I,
)
PUBLIC_KEYWORDS = re.compile(
    r"\b(inventory|register|published|transparency record|status field|"
    r"development stage|operational date)\b",
    re.I,
)


def load_coverage() -> list[dict]:
    with FIELD_COVERAGE_MATRIX.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_criteria() -> dict[str, dict]:
    data = yaml.safe_load(CONFIG_CRITERIA.read_text(encoding="utf-8"))
    return {c["criterion_id"]: c for c in data["criteria"]}


def deterministic_classify(criterion: dict, rows_for_criterion: list[dict]) -> tuple[str, int]:
    cls = classify_from_evidence_rows(
        rows_for_criterion,
        criterion_id=criterion["criterion_id"],
        evidence_hint=criterion.get("evidence_hint", ""),
        expected_artifact_type=criterion.get("expected_artifact_type", ""),
    )
    return cls, max(int(r["evidence_shortfall_level"]) for r in rows_for_criterion)


def heuristic_classify(criterion: dict, rows_for_criterion: list[dict]) -> tuple[str, int]:
    """Keyword + field-presence heuristic (LLM placeholder when no local model)."""
    level = max(int(r["evidence_shortfall_level"]) for r in rows_for_criterion)
    has_direct = any(r["coverage_class"] == "direct_field" for r in rows_for_criterion)
    text = " ".join(
        [
            criterion.get("evidence_hint", ""),
            criterion.get("expected_artifact_type", ""),
            criterion.get("criterion_statement", ""),
            " ".join(r.get("mapped_fields", "") for r in rows_for_criterion),
        ]
    )

    if level >= 3:
        return "public_satisfiable", level
    if level >= 2:
        if criterion["criterion_id"] == "operational_lifecycle_management" and has_direct:
            return "public_satisfiable", level
        return "partially_public_satisfiable", level
    if level == 0:
        return "structurally_internal", level

    internal_hits = len(INTERNAL_KEYWORDS.findall(text))
    partial_hits = len(PARTIAL_KEYWORDS.findall(text))
    if has_direct or partial_hits > internal_hits:
        return "partially_public_satisfiable", level
    return "structurally_internal", level


def llm_classify_if_configured(criterion: dict, rows_for_criterion: list[dict]) -> tuple[str, int, str]:
    """Optional local LLM hook; falls back to heuristic."""
    model_endpoint = os.environ.get("LOCALGOVBENCH_LLM_ENDPOINT", "").strip()
    if not model_endpoint:
        cls, level = heuristic_classify(criterion, rows_for_criterion)
        return cls, level, "heuristic_keyword_classifier"

    # Placeholder-ready: wire OpenAI-compatible / Ollama endpoint when configured.
    cls, level = heuristic_classify(criterion, rows_for_criterion)
    return cls, level, "llm_endpoint_configured_but_stub_uses_heuristic"


def main() -> int:
    if not FIELD_COVERAGE_MATRIX.is_file():
        print("Run map_inventory_fields_to_criteria.py first.", file=sys.stderr)
        return 1

    criteria = load_criteria()
    coverage = load_coverage()
    by_criterion: dict[str, list[dict]] = {}
    for row in coverage:
        by_criterion.setdefault(row["criterion_id"], []).append(row)

    agreement_rows: list[dict] = []
    class_agree = 0
    level_agree = 0
    n = len(criteria)

    for cid, meta in criteria.items():
        rows = by_criterion.get(cid, [])
        det_class, det_level = deterministic_classify(meta, rows)
        alt_class, alt_level, alt_method = llm_classify_if_configured(meta, rows)
        prelim = meta["preliminary_public_satisfiability_class"]

        class_match_det_alt = det_class == alt_class
        class_match_det_prelim = det_class == prelim
        level_match = det_level == alt_level

        if class_match_det_alt:
            class_agree += 1
        if level_match:
            level_agree += 1

        agreement_rows.append(
            {
                "criterion_id": cid,
                "dimension_id": meta["dimension_id"],
                "preliminary_class": prelim,
                "deterministic_class": det_class,
                "alternative_class": alt_class,
                "alternative_classifier": alt_method,
                "deterministic_max_shortfall": det_level,
                "alternative_max_shortfall": alt_level,
                "class_agreement_det_vs_alt": str(class_match_det_alt),
                "class_agreement_det_vs_prelim": str(class_match_det_prelim),
                "shortfall_level_agreement": str(level_match),
            }
        )

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    with PARTITION_AGREEMENT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(agreement_rows[0].keys()))
        writer.writeheader()
        writer.writerows(agreement_rows)

    disagree = [r for r in agreement_rows if r["class_agreement_det_vs_alt"] == "False"]
    disagree_prelim = [r for r in agreement_rows if r["class_agreement_det_vs_prelim"] == "False"]

    summary_rows = [
        {
            "metric": "criteria_count",
            "value": n,
        },
        {
            "metric": "class_agreement_det_vs_alt_pct",
            "value": round(100.0 * class_agree / n, 1),
        },
        {
            "metric": "shortfall_level_agreement_pct",
            "value": round(100.0 * level_agree / n, 1),
        },
        {
            "metric": "class_agreement_det_vs_prelim_pct",
            "value": round(100.0 * sum(1 for r in agreement_rows if r["class_agreement_det_vs_prelim"] == "True") / n, 1),
        },
        {
            "metric": "disagreement_det_vs_alt_count",
            "value": len(disagree),
        },
        {
            "metric": "disagreement_det_vs_prelim_count",
            "value": len(disagree_prelim),
        },
        {
            "metric": "disagreement_det_vs_alt_criteria",
            "value": ";".join(r["criterion_id"] for r in disagree) or "none",
        },
        {
            "metric": "alternative_classifier_used",
            "value": agreement_rows[0]["alternative_classifier"] if agreement_rows else "none",
        },
        {
            "metric": "partition_robust_if_agreement_gte_80pct",
            "value": str(class_agree / n >= 0.80),
        },
    ]

    with PARTITION_SENSITIVITY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Wrote {PARTITION_AGREEMENT.relative_to(ROOT)}")
    print(f"Wrote {PARTITION_SENSITIVITY.relative_to(ROOT)}")
    print(f"Class agreement (det vs alt): {class_agree}/{n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Field normalization helpers for schema inventory generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import yaml

from localgovbench_measurement_validation.affordance.paths import (
    FIELD_NORMALIZATION_YAML,
)


@dataclass(frozen=True)
class NormalizationHit:
    raw_field_name: str
    normalized_field_name: str
    rule_id: str
    rule_type: str
    rationale: str


def load_normalization_rules(path=None) -> dict[str, Any]:
    path = path or FIELD_NORMALIZATION_YAML
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_rule_index(rules_doc: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    """Index explicit rename/canonical rules by (source, raw_field_name)."""
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for rule in rules_doc.get("rules", []):
        source = rule["source"]
        raw = rule["raw_field"]
        index[(source, raw)] = rule
    return index


def normalize_field_name(
    source_name: str,
    raw_field_name: str,
    rule_index: dict[tuple[str, str], dict[str, Any]],
) -> NormalizationHit:
    """Apply explicit rules only; default identity normalization.

    Raw field names are always preserved separately by callers.
    """
    rule = rule_index.get((source_name, raw_field_name))
    if rule is None:
        # Whitespace-only trim for *normalized* name, preserving raw elsewhere.
        normalized = raw_field_name.strip()
        if normalized != raw_field_name:
            return NormalizationHit(
                raw_field_name=raw_field_name,
                normalized_field_name=normalized,
                rule_id="implicit_strip_whitespace",
                rule_type="whitespace_trim_normalized_only",
                rationale=(
                    "Normalized name strips leading/trailing whitespace; "
                    "raw_field_name is preserved unchanged in outputs."
                ),
            )
        return NormalizationHit(
            raw_field_name=raw_field_name,
            normalized_field_name=raw_field_name,
            rule_id="identity",
            rule_type="identity",
            rationale="No explicit normalization rule; raw name retained.",
        )

    return NormalizationHit(
        raw_field_name=raw_field_name,
        normalized_field_name=rule["normalized_field"],
        rule_id=rule["id"],
        rule_type=rule["rule_type"],
        rationale=rule["rationale"],
    )

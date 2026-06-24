"""Hide-field / recover-field evaluation for detector reliability."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass(frozen=True)
class DetectorFieldSpec:
    field_name: str
    recovery_mode: str  # substring | categorical | token_set | boolean
    notes: str = ""
    categorical_values: tuple[str, ...] = ()


# Native structured fields directly exposed by each source (mapping-relevant subset).
DETECTOR_TARGET_FIELDS: dict[str, list[DetectorFieldSpec]] = {
    "US-OMB-2025": [
        DetectorFieldSpec("development_stage", "categorical", "Lifecycle stage (direct inventory field)."),
        DetectorFieldSpec("is_high_impact", "categorical", "High-impact flag."),
        DetectorFieldSpec("human_roles", "token_set", "Human roles narrative."),
        DetectorFieldSpec("vendor_name", "substring", "Vendor/supplier name."),
        DetectorFieldSpec("agency_name", "substring", "Agency attribution."),
        DetectorFieldSpec("use_case_name", "substring", "Programme title in schema."),
        DetectorFieldSpec("have_ato", "boolean", "Authorization-to-operate flag."),
        DetectorFieldSpec("classification", "categorical", "Technology classification."),
    ],
    "CA-GC-AI-REG": [
        DetectorFieldSpec("ai_system_status_en", "categorical", "System lifecycle status."),
        DetectorFieldSpec("involves_personal_information", "boolean", "Personal information flag."),
        DetectorFieldSpec("government_organization", "substring", "Owning organization."),
        DetectorFieldSpec("vendor_information", "substring", "Vendor disclosure."),
        DetectorFieldSpec("data_sources_en", "token_set", "Data source narrative."),
        DetectorFieldSpec("name_ai_system_en", "substring", "System name."),
    ],
    "NL-ALGO-REG": [
        DetectorFieldSpec("status", "categorical", "Algorithm lifecycle status."),
        DetectorFieldSpec("lawful_basis", "token_set", "Lawful basis field (Dutch standard)."),
        DetectorFieldSpec("human_intervention", "token_set", "Human intervention description."),
        DetectorFieldSpec("organization", "substring", "Publishing organization."),
        DetectorFieldSpec("provider", "substring", "Technology provider."),
        DetectorFieldSpec("risks", "token_set", "Risk narrative."),
        DetectorFieldSpec("name", "substring", "Algorithm name."),
    ],
    "EU-PSTW": [
        DetectorFieldSpec("Status", "categorical", "Case status."),
        DetectorFieldSpec("Primary Technology", "categorical", "Primary technology label."),
        DetectorFieldSpec("Responsible organisation", "substring", "Responsible organisation."),
        DetectorFieldSpec("Name", "substring", "Case name."),
        DetectorFieldSpec("Application type", "categorical", "Application type."),
    ],
    "UK-ATRS": [
        DetectorFieldSpec("title", "substring", "Record title."),
        DetectorFieldSpec("organisation_title", "substring", "Publishing organisation."),
        DetectorFieldSpec("description", "token_set", "Record summary."),
    ],
}

US_STAGE_VALUES = (
    "Deployed",
    "Pre-deployment",
    "Pilot",
    "Research",
    "Development",
    "Planned",
    "Retired",
)
US_IMPACT_VALUES = ("High-impact", "Not high-impact", "High Impact", "Not High Impact")
CA_STATUS_VALUES = (
    "Active",
    "Inactive",
    "In development",
    "Decommissioned",
    "Pilot",
    "Production",
)
NL_STATUS_VALUES = ("Active", "Inactive", "In development", "Concept", "Phased out")
PSTW_STATUS_VALUES = ("Ongoing", "Completed", "Planned", "Discontinued", "Pilot")
BOOL_VALUES = ("yes", "no", "true", "false", "y", "n", "1", "0")


def normalize_text(value: str) -> str:
    text = (value or "").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def is_empty(value: str) -> bool:
    return normalize_text(value) in ("", "[]", "null", "none", "n/a", "na")


def build_context(raw_fields: dict[str, str], hidden_field: str) -> str:
    parts: list[str] = []
    for key, value in raw_fields.items():
        if key == hidden_field or is_empty(str(value)):
            continue
        parts.append(f"{key}: {value}")
    return "\n".join(parts)


def _ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def recover_substring(original: str, context: str, min_len: int = 3) -> str:
    orig_norm = normalize_text(original)
    ctx_norm = normalize_text(context)
    if len(orig_norm) < min_len:
        return ""
    if orig_norm in ctx_norm:
        return original.strip()
    # Try longest token run for partial organization names
    tokens = [t for t in re.split(r"[^\w]+", orig_norm) if len(t) >= 4]
    if tokens and all(t in ctx_norm for t in tokens[:3]):
        return original.strip()
    return ""


def recover_categorical(
    original: str,
    context: str,
    allowed: tuple[str, ...] | None = None,
) -> str:
    ctx_norm = normalize_text(context)
    candidates = allowed or (original.strip(),)
    best = ""
    best_score = 0.0
    for candidate in candidates:
        cand_norm = normalize_text(candidate)
        if not cand_norm:
            continue
        if cand_norm in ctx_norm:
            score = len(cand_norm)
            if score > best_score:
                best_score = score
                best = candidate
    if best:
        return best
    orig_norm = normalize_text(original)
    if orig_norm and orig_norm in ctx_norm:
        return original.strip()
    return ""


def recover_token_set(original: str, context: str, min_token_len: int = 5) -> str:
    orig_norm = normalize_text(original)
    ctx_norm = normalize_text(context)
    if orig_norm and orig_norm in ctx_norm:
        return original.strip()
    tokens = [t for t in re.split(r"[^\w]+", orig_norm) if len(t) >= min_token_len]
    if len(tokens) >= 2 and all(t in ctx_norm for t in tokens[:6]):
        return original.strip()
    if len(tokens) == 1 and tokens[0] in ctx_norm:
        return original.strip()
    return ""


def recover_boolean(original: str, context: str) -> str:
    orig_norm = normalize_text(original)
    ctx_norm = normalize_text(context)
    if is_empty(original):
        return ""
    if orig_norm in ctx_norm:
        return original.strip()
    for token in BOOL_VALUES:
        if token == orig_norm and re.search(rf"\b{re.escape(token)}\b", ctx_norm):
            return original.strip()
    return ""


def recover_field(
    spec: DetectorFieldSpec,
    original: str,
    context: str,
    allowed_values: tuple[str, ...] = (),
) -> str:
    if spec.recovery_mode == "substring":
        return recover_substring(original, context)
    if spec.recovery_mode == "categorical":
        allowed = spec.categorical_values or allowed_values or (original.strip(),)
        return recover_categorical(original, context, allowed)
    if spec.recovery_mode == "token_set":
        return recover_token_set(original, context)
    if spec.recovery_mode == "boolean":
        return recover_boolean(original, context)
    return recover_substring(original, context)


def values_match(original: str, predicted: str, *, fuzzy_threshold: float = 0.92) -> bool:
    if is_empty(original) and is_empty(predicted):
        return True
    if is_empty(original) != is_empty(predicted):
        return False
    o = normalize_text(original)
    p = normalize_text(predicted)
    if o == p:
        return True
    return _ratio(o, p) >= fuzzy_threshold


def collect_allowed_values(records: list[dict], field_name: str, limit: int = 40) -> tuple[str, ...]:
    seen: dict[str, int] = {}
    for record in records:
        fields = json.loads(record["raw_fields_json"])
        val = str(fields.get(field_name, "")).strip()
        if not is_empty(val) and len(val) <= 80:
            key = normalize_text(val)
            seen[key] = seen.get(key, 0) + 1
    ordered = sorted(seen.items(), key=lambda x: (-x[1], x[0]))
    return tuple(v for v, _ in ordered[:limit])


FAILURE_MODES: dict[str, str] = {
    "empty_field_high": "High empty rate: recovery metrics dominated by absence, not extraction noise.",
    "verbatim_leakage": "Recovered via verbatim duplication in another schema field (inflates F1).",
    "categorical_alias": "Synonym or label variant not present in remaining text (false negative).",
    "long_narrative": "Long free-text field: token-set recovery misses paraphrases.",
    "search_metadata_only": "UK ATRS evaluation uses Search API metadata, not full HTML record body.",
    "cross_field_redundancy": "Structured inventories duplicate key values across fields (conservative F1).",
}

UNCERTAINTY_NOTES: list[str] = [
    "Hide-field evaluation uses deterministic substring/categorical heuristics as a conservative "
    "proxy for automated extraction; no generative LLM recovery is applied unless configured.",
    "Context excludes the hidden field and empty values only; derived normalised columns "
    "(programme_title, agency_or_owner) are not used to avoid label leakage.",
    "Boolean and categorical fields use corpus-derived allowed values where applicable.",
    "UK ATRS sample (n=133) yields wider confidence intervals than US/NL/EU sources.",
    "High recovery F1 indicates structured access is reliable; low F1 on narrative fields "
    "does not inflate public-satisfiability ceilings because mapping uses native schema fields.",
]

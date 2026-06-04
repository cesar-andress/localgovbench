"""GRB assessment evidence log schema and I/O."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from localgovbench.grb.specification import GRB_SPEC_VERSION, all_indicator_ids
from localgovbench.utils.io import load_yaml, save_yaml

EVIDENCE_LOG_FILENAME = "evidence_log.yaml"


@dataclass
class EvidenceEntry:
    """One candidate evidence record for an indicator."""

    entry_id: str
    source_document: str
    candidate_evidence: str
    quoted_text_span: str = ""
    confidence_level: str = "low"
    extracted_by: str = "human"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "source_document": self.source_document,
            "candidate_evidence": self.candidate_evidence,
            "quoted_text_span": self.quoted_text_span,
            "confidence_level": self.confidence_level,
            "extracted_by": self.extracted_by,
            "notes": self.notes,
        }


def new_evidence_log(
    case_id: str,
    *,
    documents_reviewed: list[str] | None = None,
    ollama_used: bool = False,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    """Create an empty evidence log with all GRB indicators."""
    indicators: dict[str, Any] = {ind_id: {"entries": []} for ind_id in all_indicator_ids()}
    return {
        "metadata": {
            "case_id": case_id,
            "grb_version": GRB_SPEC_VERSION,
            "documents_reviewed": documents_reviewed or [],
            "ollama_used": ollama_used,
            "warnings": warnings or [],
        },
        "indicators": indicators,
    }


def append_evidence_entry(
    log: dict[str, Any],
    indicator_id: str,
    entry: EvidenceEntry,
) -> None:
    """Append one evidence entry to an indicator (supports multiple per indicator)."""
    if indicator_id not in log.get("indicators", {}):
        raise KeyError(f"Unknown indicator in evidence log: {indicator_id}")
    log["indicators"][indicator_id]["entries"].append(entry.to_dict())


def validate_evidence_log(log: dict[str, Any]) -> list[str]:
    """Return validation errors; empty list means valid."""
    errors: list[str] = []
    if "metadata" not in log:
        errors.append("missing metadata section")
    if "indicators" not in log:
        errors.append("missing indicators section")
        return errors

    expected = set(all_indicator_ids())
    found = set(log["indicators"].keys())
    missing = expected - found
    extra = found - expected
    if missing:
        errors.append(f"missing {len(missing)} indicators")
    if extra:
        errors.append(f"unknown indicator ids: {sorted(extra)[:3]}")

    for ind_id, block in log["indicators"].items():
        if not isinstance(block, dict):
            errors.append(f"{ind_id}: indicator block must be a mapping")
            continue
        entries = block.get("entries")
        if not isinstance(entries, list):
            errors.append(f"{ind_id}: entries must be a list")
            continue
        for idx, entry in enumerate(entries):
            if not isinstance(entry, dict):
                errors.append(f"{ind_id}: entry {idx} must be a mapping")
                continue
            for key in ("entry_id", "source_document", "candidate_evidence"):
                if key not in entry:
                    errors.append(f"{ind_id}: entry {idx} missing {key}")
    return errors


def evidence_refs_for_scoring(log: dict[str, Any]) -> dict[str, list[str]]:
    """Map indicator ids to evidence reference ids for GRB E2/E3 checks."""
    refs: dict[str, list[str]] = {}
    for ind_id, block in log.get("indicators", {}).items():
        entries = block.get("entries") or []
        refs[ind_id] = [
            str(e.get("entry_id") or e.get("source_document", "ref"))
            for e in entries
            if isinstance(e, dict)
        ]
    return refs


def save_evidence_log(path: Path, log: dict[str, Any]) -> None:
    errors = validate_evidence_log(log)
    if errors:
        raise ValueError(f"Invalid evidence log: {errors[0]}")
    path.parent.mkdir(parents=True, exist_ok=True)
    save_yaml(path, log)


def load_evidence_log(path: Path) -> dict[str, Any]:
    log = load_yaml(path)
    errors = validate_evidence_log(log)
    if errors:
        raise ValueError(f"Invalid evidence log at {path}: {errors[0]}")
    return log

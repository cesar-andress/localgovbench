"""Synthetic demo score filler — not for real municipal assessments."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from localgovbench.grb.specification import all_indicator_ids
from localgovbench.utils.io import load_yaml, save_yaml
from localgovbench.workflows.evidence_log import load_evidence_log
from localgovbench.workflows.scoring_template import validate_scoring_template

SYNTHETIC_DEMO_BANNER = (
    "SYNTHETIC DEMO ONLY — scores are deterministic placeholders for workflow walkthrough. "
    "Do not use for real assessments or publication claims."
)

DIMENSION_BASE_LEVEL = 3


def indicator_dimension(indicator_id: str) -> str:
    return indicator_id.split("_", 1)[0]


def deterministic_demo_score(indicator_id: str) -> int:
    """
    Deterministic maturity score centred on level 3 per dimension.

    Offset in {-1, 0, +1} from a stable hash of the indicator id.
    """
    base = DIMENSION_BASE_LEVEL
    offset = (sum(ord(c) for c in indicator_id) % 3) - 1
    return max(0, min(4, base + offset))


def _evidence_refs_for_indicator(
    indicator_id: str,
    score: int,
    evidence_log: dict[str, Any] | None,
) -> list[str]:
    """Build evidence reference ids for E2/E3-style documentation in the completed YAML."""
    refs: list[str] = []
    if evidence_log:
        entries = evidence_log.get("indicators", {}).get(indicator_id, {}).get("entries") or []
        for entry in entries:
            if isinstance(entry, dict) and entry.get("entry_id"):
                refs.append(str(entry["entry_id"]))
    if score >= 3 and not refs:
        refs.append(f"{indicator_id}_synthetic_demo_ref_01")
    if score >= 4:
        second = f"{indicator_id}_synthetic_demo_ref_02"
        if second not in refs:
            refs.append(second)
    return refs


def fill_synthetic_demo_scores(
    template: dict[str, Any],
    *,
    evidence_log: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Return a copy of *template* with all null responses filled with demo scores.

    Adds ``evidence_refs`` for indicators with score >= 3 when supported.
    """
    errors = validate_scoring_template(template)
    if errors:
        raise ValueError(f"Invalid scoring template: {errors[0]}")

    completed = {
        "metadata": dict(template.get("metadata") or {}),
        "responses": dict(template.get("responses") or {}),
        "notes": SYNTHETIC_DEMO_BANNER,
    }
    meta = completed["metadata"]
    meta["synthetic"] = True
    meta["synthetic_demo_scores"] = True
    meta["scoring_status"] = "synthetic_demo_completed"
    meta["demo_scores_warning"] = SYNTHETIC_DEMO_BANNER

    evidence_refs: dict[str, list[str]] = {}
    for indicator_id in all_indicator_ids():
        raw = completed["responses"].get(indicator_id)
        if raw is None:
            score = deterministic_demo_score(indicator_id)
            completed["responses"][indicator_id] = score
        else:
            score = int(raw)
        refs = _evidence_refs_for_indicator(indicator_id, score, evidence_log)
        if refs:
            evidence_refs[indicator_id] = refs

    if evidence_refs:
        completed["evidence_refs"] = evidence_refs

    remaining_null = [k for k, v in completed["responses"].items() if v is None]
    if remaining_null:
        raise RuntimeError(f"Demo fill left {len(remaining_null)} null scores")

    return completed


def fill_demo_scores_file(
    input_path: Path,
    output_path: Path,
    *,
    evidence_log_path: Path | None = None,
) -> dict[str, Any]:
    """Load template, fill demo scores, save completed YAML."""
    template = load_yaml(input_path)
    evidence_log = None
    if evidence_log_path and evidence_log_path.exists():
        evidence_log = load_evidence_log(evidence_log_path)
    elif input_path.parent.joinpath("evidence_log.yaml").exists():
        evidence_log = load_evidence_log(input_path.parent / "evidence_log.yaml")

    completed = fill_synthetic_demo_scores(template, evidence_log=evidence_log)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_yaml(output_path, completed)
    return completed

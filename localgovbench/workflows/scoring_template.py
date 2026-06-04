"""Human GRB scoring template generation and loading."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from localgovbench.grb.scoring import validate_indicator_score
from localgovbench.grb.specification import GRB_SPEC_VERSION, all_indicator_ids
from localgovbench.utils.io import load_yaml, save_yaml

SCORING_TEMPLATE_FILENAME = "assessor_scoring_template.yaml"


def build_scoring_template(
    case_id: str,
    *,
    evidence_log_file: str = "evidence_log.yaml",
    municipality_label: str | None = None,
) -> dict[str, Any]:
    """
    Build a YAML template with all GRB indicators and null scores.

    Ollama and other tools must never pre-fill maturity scores.
    """
    responses = {ind_id: None for ind_id in all_indicator_ids()}
    return {
        "metadata": {
            "case_id": case_id,
            "municipality": municipality_label or case_id.replace("_", " ").title(),
            "instrument": "grb-0.1-experiment",
            "grb_version": GRB_SPEC_VERSION,
            "scoring_status": "awaiting_human_input",
            "synthetic": False,
            "evidence_log": evidence_log_file,
        },
        "responses": responses,
        "notes": "Assign integer scores 0–4 per indicator. Do not use LLM-generated scores.",
    }


def validate_scoring_template(template: dict[str, Any]) -> list[str]:
    """Validate template structure; scores may be null."""
    errors: list[str] = []
    responses = template.get("responses")
    if not isinstance(responses, dict):
        return ["missing responses mapping"]

    expected = set(all_indicator_ids())
    found = set(responses.keys())
    if expected != found:
        missing = expected - found
        extra = found - expected
        if missing:
            errors.append(f"missing {len(missing)} indicator slots")
        if extra:
            errors.append(f"unknown indicators: {sorted(extra)[:3]}")

    for ind_id, raw in responses.items():
        if raw is None:
            continue
        try:
            validate_indicator_score(raw)
        except (TypeError, ValueError) as exc:
            errors.append(f"{ind_id}: {exc}")
    return errors


def assert_no_llm_scores(template: dict[str, Any]) -> None:
    """Ensure no indicator was auto-scored (all must remain null before human coding)."""
    responses = template.get("responses") or {}
    filled = [k for k, v in responses.items() if v is not None]
    if filled:
        raise ValueError(
            f"Scoring template must not contain LLM-assigned scores; found {len(filled)} filled indicators"
        )


def load_human_scores(path: Path) -> dict[str, int]:
    """Load completed human scores from assessor YAML."""
    data = load_yaml(path)
    errors = validate_scoring_template(data)
    if errors:
        raise ValueError(f"Invalid scoring template at {path}: {errors[0]}")

    responses = data["responses"]
    missing = [k for k, v in responses.items() if v is None]
    if missing:
        raise ValueError(
            f"{len(missing)} indicators still unscored (null). Complete human scoring before compute."
        )

    return {k: validate_indicator_score(v) for k, v in responses.items()}


def save_scoring_template(path: Path, template: dict[str, Any], *, allow_prescore: bool = False) -> None:
    if not allow_prescore:
        assert_no_llm_scores(template)
    errors = validate_scoring_template(template)
    if errors:
        raise ValueError(f"Invalid scoring template: {errors[0]}")
    path.parent.mkdir(parents=True, exist_ok=True)
    save_yaml(path, template)

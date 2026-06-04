"""Synthetic GRB profile builders for experiments."""

from __future__ import annotations

from localgovbench.grb.specification import GRB_DIMENSIONS, all_indicator_ids


def build_responses(
    *,
    dimension_levels: dict[str, int],
    default_level: int = 3,
) -> dict[str, int]:
    """Set all indicators in each dimension to the given maturity level (0–4)."""
    level_map = {dim.id: dimension_levels.get(dim.id, default_level) for dim in GRB_DIMENSIONS}
    responses: dict[str, int] = {}
    for dimension in GRB_DIMENSIONS:
        level = max(0, min(4, int(level_map[dimension.id])))
        for subdimension in dimension.subdimensions:
            for indicator in subdimension.indicators:
                responses[indicator.id] = level
    missing = set(all_indicator_ids()) - set(responses.keys())
    if missing:
        raise RuntimeError(f"Incomplete profile: missing {len(missing)} indicators")
    return responses


def build_assessment_payload(
    profile_id: str,
    *,
    dimension_levels: dict[str, int],
    default_level: int = 3,
    scenario: str,
) -> dict:
    """Build a minimal assessment payload for ``compute_grb_assessment``."""
    return {
        "metadata": {
            "municipality": f"Synthetic Sensitivity {profile_id}",
            "profile": profile_id,
            "scenario": scenario,
            "synthetic": True,
        },
        "responses": build_responses(dimension_levels=dimension_levels, default_level=default_level),
        "evidence": {},
    }

"""Tests for GRB dimension ablation study."""

from __future__ import annotations

from localgovbench.grb.ablation import (
    ABLATION_CONFIGS,
    active_dimensions,
    compute_ablated_readiness,
    run_ablation_study,
    score_profile_ablation,
)
from localgovbench.grb.profiles import build_assessment_payload, build_responses
from localgovbench.grb.scoring import SAFEGUARD_CAP, compute_grb_assessment
from localgovbench.grb.sensitivity import ProfileSpec, generate_profile_specs


def test_ablation_configs() -> None:
    assert set(ABLATION_CONFIGS) == {"full", "without_d2", "without_d4", "without_d6"}
    assert active_dimensions(ABLATION_CONFIGS["without_d2"]) == ("d1", "d3", "d4", "d5", "d6")


def test_without_d2_disables_d2_safeguard_trigger() -> None:
    """Weak D2 with strong baseline triggers G1 in full model but not when D2 is excluded."""
    responses = build_responses(dimension_levels={"d2": 1}, default_level=4)
    full = compute_grb_assessment({"metadata": {}, "responses": responses})
    assert full.safeguard_applied is True

    _, _, final_ablated, applied, _ = compute_ablated_readiness(
        full.dimension_scores,
        excluded_dimensions=ABLATION_CONFIGS["without_d2"],
    )
    assert applied is False
    assert final_ablated > SAFEGUARD_CAP


def test_without_d6_changes_readiness_not_safeguard_dims() -> None:
    responses = build_responses(dimension_levels={"d6": 0}, default_level=3)
    full = compute_grb_assessment({"metadata": {}, "responses": responses})
    overall_full, raw_full, final_full, _, _ = compute_ablated_readiness(
        full.dimension_scores,
        excluded_dimensions=frozenset(),
    )
    overall_no_d6, _, final_no_d6, _, _ = compute_ablated_readiness(
        full.dimension_scores,
        excluded_dimensions=ABLATION_CONFIGS["without_d6"],
    )
    assert overall_no_d6 > overall_full
    assert final_no_d6 > final_full
    assert raw_full == full.readiness_raw


def test_run_ablation_study_small_sample() -> None:
    specs = generate_profile_specs()[:20]
    scores, comparisons, summary = run_ablation_study(specs)
    assert len(scores["full"]) == 20
    assert len(comparisons) == 3
    assert summary["profile_count"] == 20
    for comp in comparisons:
        assert comp.reference == "full"
        assert -1.0 <= comp.spearman <= 1.0


def test_score_profile_ablation_matches_full_config() -> None:
    spec = generate_profile_specs()[0]
    ablated = score_profile_ablation(spec, "full", frozenset())
    payload = build_assessment_payload(
        spec.profile_id,
        dimension_levels=spec.dimension_levels,
        scenario=spec.profile_group,
    )
    full = compute_grb_assessment(payload)
    assert ablated.readiness_final == full.readiness_final
    assert ablated.safeguard_applied == full.safeguard_applied


def test_enriched_deltas_on_alternate_configs() -> None:
    scores, _, _ = run_ablation_study(generate_profile_specs()[:5])
    for config in ("without_d2", "without_d4", "without_d6"):
        for row in scores[config]:
            assert isinstance(row.readiness_delta_vs_full, float)

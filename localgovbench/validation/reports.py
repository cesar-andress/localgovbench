"""Validation study report generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from localgovbench.validation.irr import InterRaterStudyResult, run_inter_rater_study
from localgovbench.utils.io import load_yaml


@dataclass(frozen=True, slots=True)
class ValidationPackageSummary:
    """Summary counts for the validation package."""

    content_validity_template: Path
    expert_questionnaire_template: Path
    inter_rater_cases: int
    inter_rater_rating_files: int
    irr_study: InterRaterStudyResult | None


def _count_yaml(directory: Path) -> int:
    if not directory.exists():
        return 0
    return len(list(directory.glob("*.yaml")))


def render_validation_report(
    *,
    validation_root: Path,
    irr_result: InterRaterStudyResult | None = None,
    content_validity_path: Path | None = None,
) -> str:
    """Render a Markdown validation benchmark report."""
    templates = validation_root / "templates"
    cases_dir = validation_root / "cases"
    ratings_dir = validation_root / "ratings"

    if irr_result is None and ratings_dir.exists():
        irr_result = run_inter_rater_study(ratings_dir)

    cv_path = content_validity_path or (templates / "content_validity_study.yaml")
    cv_status = "Template (not yet fielded)"
    if cv_path.exists():
        cv_data = load_yaml(cv_path)
        reviews = cv_data.get("criterion_reviews") or []
        completed = sum(1 for r in reviews if r.get("clarity_score"))
        cv_status = f"{completed}/{len(reviews)} criterion reviews completed (synthetic template)"

    lines = [
        "# LocalGovBench Scientific Validation Report",
        "",
        "> Research-grade validation package for empirical studies. "
        "Bundled IRR data are **synthetic** for pipeline demonstration.",
        "",
        "## 1. Package components",
        "",
        "| Component | Location | Status |",
        "|-----------|----------|--------|",
        f"| Content validity study | `validation/templates/content_validity_study.yaml` | {cv_status} |",
        "| Expert review questionnaire | `validation/templates/expert_review_questionnaire.yaml` | Template |",
        "| Inter-rater codebook | `validation/templates/inter_rater_codebook.yaml` | Template |",
        f"| Synthetic benchmark cases | `validation/cases/` | {_count_yaml(cases_dir)} cases |",
        f"| Rater sheets | `validation/ratings/` | {_count_yaml(ratings_dir)} files |",
        "",
        "## 2. Instrument",
        "",
        "- **ID:** `localgovbench-v0.1`",
        "- **Criteria:** 25 (five dimensions, unchanged)",
        "- **Scale:** 0–4 maturity per criterion",
        "- **Scoring:** Human assessors only; LLM evidence extraction is auxiliary",
        "",
    ]

    if irr_result:
        lines.extend(
            [
                "## 3. Inter-rater reliability (synthetic pilot)",
                "",
                f"**Study ID:** {irr_result.study_id}  ",
                f"**Instrument:** {irr_result.instrument_id}",
                "",
                "### Overall metrics",
                "",
                "| Metric | Value | Interpretation (guidance) |",
                "|--------|-------|---------------------------|",
                f"| Cohen's Kappa | {irr_result.overall_kappa} | {irr_result.overall_kappa_label} |",
                f"| Krippendorff's Alpha | {irr_result.overall_alpha} | {irr_result.overall_alpha_label} |",
                "",
                "### Per-case results",
                "",
                "| Case | Disagreements | Cohen's Kappa | Krippendorff's Alpha |",
                "|------|---------------|---------------|----------------------|",
            ]
        )
        for case in irr_result.cases:
            lines.append(
                f"| `{case.case_id}` | {case.disagreement_count}/{case.n_criteria} | "
                f"{case.cohens_kappa} | {case.krippendorff_alpha} |"
            )
        lines.append("")

    lines.extend(
        [
            "## 4. Content validity (planned workflow)",
            "",
            "1. Recruit 6–8 experts (public administration, law/DPO, IT security).",
            "2. Complete `content_validity_study.yaml` per criterion.",
            "3. Aggregate relevance and clarity scores; revise criteria with CV ratio / I-CVI targets.",
            "4. Document changes in instrument version log.",
            "",
            "## 5. Recommendations for field deployment",
            "",
            "- Run dual independent coding with `inter_rater_rating_sheet.yaml`.",
            "- Adjudicate discrepancies >1 point using `adjudication_record.yaml`.",
            "- Report κ and α per case and pooled, with raw disagreement tables.",
            "- Do not publish municipality rankings without consent.",
            "",
            "## 6. Limitations",
            "",
            "- Synthetic IRR bundled data are **not** empirical validation results.",
            "- Threshold labels are guidance only, not normative standards.",
            "- GRB 54-indicator extension validated separately if adopted.",
            "",
            "---",
            "*Generated by LocalGovBench validation package.*",
        ]
    )
    return "\n".join(lines)

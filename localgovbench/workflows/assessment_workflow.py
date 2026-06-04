"""End-to-end GRB assessment workflow: documents → evidence → human scores → readiness."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from localgovbench.grb.scoring import GRBAssessmentResult, compute_grb_assessment
from localgovbench.grb.specification import GRB_SPEC_VERSION, all_indicator_ids
from localgovbench.llm.evidence_extraction import (
    DEFAULT_OLLAMA_BASE_URL,
    DEFAULT_OLLAMA_MODEL,
    OllamaClient,
    extract_evidence,
)
from localgovbench.utils.io import save_yaml
from localgovbench.workflows.evidence_log import (
    EVIDENCE_LOG_FILENAME,
    EvidenceEntry,
    append_evidence_entry,
    evidence_refs_for_scoring,
    load_evidence_log,
    new_evidence_log,
    save_evidence_log,
)
from localgovbench.workflows.scoring_template import (
    SCORING_TEMPLATE_FILENAME,
    build_scoring_template,
    load_human_scores,
    save_scoring_template,
)

DOCUMENT_SUFFIXES = (".md", ".txt", ".markdown")
READINESS_REPORT_FILENAME = "readiness_report.md"
RESULTS_JSON_FILENAME = "machine_readable_results.json"


@dataclass
class WorkflowConfig:
    """Configuration for one municipality assessment run."""

    case_id: str
    documents_dir: Path
    output_dir: Path
    use_ollama: bool = False
    ollama_model: str = DEFAULT_OLLAMA_MODEL
    ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL
    municipality_label: str | None = None


@dataclass
class WorkflowResult:
    """Paths and warnings produced by a workflow phase."""

    case_id: str
    output_dir: Path
    warnings: list[str] = field(default_factory=list)
    evidence_log_path: Path | None = None
    scoring_template_path: Path | None = None
    readiness_report_path: Path | None = None
    results_json_path: Path | None = None
    assessment_result: GRBAssessmentResult | None = None


def discover_documents(documents_dir: Path) -> list[Path]:
    """List readable governance documents in *documents_dir*."""
    if not documents_dir.is_dir():
        raise FileNotFoundError(f"Documents directory not found: {documents_dir}")
    files = sorted(
        p
        for p in documents_dir.iterdir()
        if p.is_file() and p.suffix.lower() in DOCUMENT_SUFFIXES
    )
    if not files:
        raise ValueError(f"No documents ({DOCUMENT_SUFFIXES}) found in {documents_dir}")
    return files


def load_document_corpus(paths: list[Path]) -> tuple[str, list[str]]:
    """Concatenate documents with source headers; return corpus and filenames."""
    parts: list[str] = []
    names: list[str] = []
    for path in paths:
        names.append(path.name)
        parts.append(f"--- DOCUMENT: {path.name} ---\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(parts), names


def _try_ollama_extract(
    corpus: str,
    indicator_id: str,
    *,
    model: str,
    base_url: str,
    warnings: list[str],
) -> EvidenceEntry | None:
    try:
        client = OllamaClient(base_url=base_url, model=model, timeout_seconds=90.0)
        result = extract_evidence(corpus, indicator_id, client=client)
    except (ConnectionError, RuntimeError, ValueError, OSError) as exc:
        warnings.append(f"Ollama skipped for {indicator_id}: {exc}")
        return None

    return EvidenceEntry(
        entry_id=f"{indicator_id}_ollama_01",
        source_document="corpus",
        candidate_evidence=result.candidate_evidence,
        quoted_text_span=result.quoted_text_span,
        confidence_level=result.confidence_level,
        extracted_by="ollama",
        notes=result.insufficient_evidence_warning or "",
    )


def run_prepare_phase(config: WorkflowConfig) -> WorkflowResult:
    """
    Load documents, optionally extract candidate evidence, write evidence log and template.

    Never writes maturity scores — template responses remain null.
    """
    config.output_dir.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []
    doc_paths = discover_documents(config.documents_dir)
    corpus, doc_names = load_document_corpus(doc_paths)

    log = new_evidence_log(
        config.case_id,
        documents_reviewed=doc_names,
        ollama_used=config.use_ollama,
        warnings=[],
    )

    if config.use_ollama:
        import urllib.error
        import urllib.request

        try:
            urllib.request.urlopen(
                f"{config.ollama_base_url.rstrip('/')}/api/tags",
                timeout=3,
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            warnings.append(
                f"Ollama unavailable at {config.ollama_base_url}: {exc}. "
                "Continuing without LLM evidence extraction."
            )
            log["metadata"]["ollama_used"] = False
        else:
            for idx, indicator_id in enumerate(all_indicator_ids(), start=1):
                entry = _try_ollama_extract(
                    corpus,
                    indicator_id,
                    model=config.ollama_model,
                    base_url=config.ollama_base_url,
                    warnings=warnings,
                )
                if entry:
                    append_evidence_entry(log, indicator_id, entry)
    else:
        doc_list = ", ".join(doc_names)
        for indicator_id in all_indicator_ids():
            append_evidence_entry(
                log,
                indicator_id,
                EvidenceEntry(
                    entry_id=f"{indicator_id}_pending_01",
                    source_document=doc_names[0] if doc_names else "corpus",
                    candidate_evidence=(
                        "Pending human review — documents indexed without LLM extraction. "
                        f"Sources: {doc_list}"
                    ),
                    quoted_text_span="",
                    confidence_level="low",
                    extracted_by="workflow_index",
                    notes="Add further entries per indicator as needed.",
                ),
            )

    log["metadata"]["warnings"] = warnings
    evidence_path = config.output_dir / EVIDENCE_LOG_FILENAME
    save_evidence_log(evidence_path, log)

    template = build_scoring_template(
        config.case_id,
        evidence_log_file=EVIDENCE_LOG_FILENAME,
        municipality_label=config.municipality_label,
    )
    template_path = config.output_dir / SCORING_TEMPLATE_FILENAME
    save_scoring_template(template_path, template)

    results_path = config.output_dir / RESULTS_JSON_FILENAME
    _write_results_json(
        results_path,
        case_id=config.case_id,
        evidence_log_path=evidence_path,
        scoring_template_path=template_path,
        assessment_result=None,
        warnings=warnings,
        phase="prepare",
    )

    return WorkflowResult(
        case_id=config.case_id,
        output_dir=config.output_dir,
        warnings=warnings,
        evidence_log_path=evidence_path,
        scoring_template_path=template_path,
        results_json_path=results_path,
    )


def run_compute_phase(config: WorkflowConfig, scores_path: Path) -> WorkflowResult:
    """Load human scores and evidence log; compute readiness and reports."""
    config.output_dir.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []

    evidence_path = config.output_dir / EVIDENCE_LOG_FILENAME
    if not evidence_path.exists():
        raise FileNotFoundError(f"Evidence log not found: {evidence_path}. Run prepare phase first.")

    log = load_evidence_log(evidence_path)
    warnings.extend(log.get("metadata", {}).get("warnings") or [])

    scores = load_human_scores(scores_path)
    evidence = evidence_refs_for_scoring(log)

    payload = {
        "metadata": {
            "municipality": config.municipality_label or config.case_id.replace("_", " ").title(),
            "case_id": config.case_id,
            "profile": config.case_id,
            "grb_version": GRB_SPEC_VERSION,
            "synthetic": False,
            "scoring_source": "human",
        },
        "responses": scores,
        "evidence": evidence,
    }
    result = compute_grb_assessment(payload)

    report_path = config.output_dir / READINESS_REPORT_FILENAME
    report_path.write_text(
        render_workflow_readiness_report(
            config.case_id,
            log=log,
            human_scores=scores,
            assessment=result,
            documents_dir=config.documents_dir,
        ),
        encoding="utf-8",
    )

    results_path = config.output_dir / RESULTS_JSON_FILENAME
    _write_results_json(
        results_path,
        case_id=config.case_id,
        evidence_log_path=evidence_path,
        scoring_template_path=scores_path,
        assessment_result=result,
        warnings=warnings,
        phase="compute",
        human_scores=scores,
    )

    return WorkflowResult(
        case_id=config.case_id,
        output_dir=config.output_dir,
        warnings=warnings,
        evidence_log_path=evidence_path,
        scoring_template_path=scores_path,
        readiness_report_path=report_path,
        results_json_path=results_path,
        assessment_result=result,
    )


def render_workflow_readiness_report(
    case_id: str,
    *,
    log: dict[str, Any],
    human_scores: dict[str, int],
    assessment: GRBAssessmentResult,
    documents_dir: Path,
) -> str:
    """Markdown report distinguishing evidence, human scores, and computed readiness."""
    meta = log.get("metadata", {})
    indicators_with_evidence = sum(
        1 for block in log.get("indicators", {}).values() if block.get("entries")
    )
    sample_evidence: list[str] = []
    for ind_id in sorted(log.get("indicators", {}))[:5]:
        entries = log["indicators"][ind_id].get("entries") or []
        if entries:
            sample_evidence.append(
                f"- `{ind_id}`: {entries[0].get('candidate_evidence', '')[:120]}..."
            )

    lines = [
        "# GRB Readiness Report — End-to-End Workflow",
        "",
        f"**Case id:** `{case_id}`",
        f"**GRB version:** {assessment.framework_version}",
        f"**Documents folder:** `{documents_dir}`",
        "",
        "> This report separates **candidate evidence** (document/LLM indexing), "
        "**human-assigned maturity scores**, and **computed readiness** from the frozen GRB engine.",
        "",
        "## 1. Candidate evidence (not scores)",
        "",
        f"- Documents reviewed: {', '.join(meta.get('documents_reviewed', [])) or 'none'}",
        f"- Ollama used in prepare phase: **{meta.get('ollama_used', False)}**",
        f"- Indicators with ≥1 evidence entry: **{indicators_with_evidence}** / {len(all_indicator_ids())}",
        "",
        "Sample candidate evidence (first indicators with entries):",
        "",
    ]
    lines.extend(sample_evidence or ["- *(no entries)*"])
    lines.extend(
        [
            "",
            "Full log: `evidence_log.yaml` (multiple entries per indicator supported).",
            "",
            "## 2. Human-assigned scores (authoritative)",
            "",
            f"- Scoring source: **human** ({len(human_scores)} indicators)",
            "- Maturity scale: **0–4** per frozen GRB indicator",
            "- LLM did **not** assign these scores",
            "",
            "| Sample indicator | Human score |",
            "|------------------|-------------|",
        ]
    )
    for ind_id in sorted(human_scores)[:6]:
        lines.append(f"| `{ind_id}` | {human_scores[ind_id]} |")
    lines.append("| ... | ... |")
    lines.extend(
        [
            "",
            "## 3. Computed readiness (GRB engine)",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Overall maturity (0–4) | {assessment.overall_maturity} |",
            f"| Readiness (raw, 0–100) | {assessment.readiness_raw} |",
            f"| Readiness (final, 0–100) | {assessment.readiness_final} |",
            f"| Readiness band | {assessment.readiness_band} |",
            f"| Safeguard G1 applied | {assessment.safeguard_applied} |",
            "",
        ]
    )
    if assessment.safeguard_reason:
        lines.extend([f"> {assessment.safeguard_reason}", ""])

    lines.extend(["### Dimension scores (computed)", "", "| Dimension | Score |", "|-----------|-------|"])
    for dim_id in sorted(assessment.dimension_scores):
        lines.append(f"| `{dim_id}` | {assessment.dimension_scores[dim_id]} |")

    if assessment.evidence_issues:
        lines.extend(["", "### Evidence gate issues (E2/E3)", ""])
        for issue in assessment.evidence_issues[:10]:
            lines.append(f"- `{issue.indicator_id}` (score {issue.score}): {issue.message}")
        if len(assessment.evidence_issues) > 10:
            lines.append(f"- ... and {len(assessment.evidence_issues) - 10} more")
    else:
        lines.extend(["", "### Evidence gate issues (E2/E3)", "", "None detected.", ""])

    warnings = meta.get("warnings") or []
    if warnings:
        lines.extend(["## Workflow warnings", ""])
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    lines.extend(["---", "*Generated by `scripts/run_assessment_workflow.py`*"])
    return "\n".join(lines)


def _write_results_json(
    path: Path,
    *,
    case_id: str,
    evidence_log_path: Path,
    scoring_template_path: Path,
    assessment_result: GRBAssessmentResult | None,
    warnings: list[str],
    phase: str,
    human_scores: dict[str, int] | None = None,
) -> None:
    payload: dict[str, Any] = {
        "case_id": case_id,
        "grb_version": GRB_SPEC_VERSION,
        "phase": phase,
        "evidence_log": str(evidence_log_path.name),
        "scoring_template": str(scoring_template_path.name),
        "warnings": warnings,
        "human_scores": human_scores,
        "computed_readiness": None,
    }
    if assessment_result is not None:
        payload["computed_readiness"] = {
            "overall_maturity": assessment_result.overall_maturity,
            "readiness_raw": assessment_result.readiness_raw,
            "readiness_final": assessment_result.readiness_final,
            "readiness_band": assessment_result.readiness_band,
            "safeguard_applied": assessment_result.safeguard_applied,
            "dimension_scores": assessment_result.dimension_scores,
            "evidence_issue_count": len(assessment_result.evidence_issues),
        }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

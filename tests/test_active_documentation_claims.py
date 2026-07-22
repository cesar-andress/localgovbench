"""Fail if active public docs make unqualified legacy measurement claims."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

# Active surfaces that must not claim GRB/readiness as current measurement.
ACTIVE_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "CITATION.cff",
    REPO_ROOT / "pyproject.toml",
    REPO_ROOT / "localgovbench_measurement_validation" / "affordance" / "README.md",
    REPO_ROOT / "docs" / "releases" / "github_release_v0.2.0.md",
    REPO_ROOT / "docs" / "releases" / "zenodo_metadata_v0.2.0.md",
]

# Phrases that are forbidden as *current* claims unless clearly historical.
FORBIDDEN_CURRENT_PATTERNS = [
    re.compile(r"(?i)currently measures?\s+governance readiness"),
    re.compile(r"(?i)active analytical framework.*governance readiness"),
    re.compile(r"(?i)LocalGovBench is an? open research artifact for studying\s+\*\*local and on-premise"),
    re.compile(r"(?i)provides:\n\n- A version \*\*0\.1\.0\*\* governance framework"),
]


def _strip_historical_blocks(text: str) -> str:
    """Remove clearly marked historical/v0.1.0 paragraphs for scanning."""
    # Drop fenced historical bibtex / tables that mention v0.1.0 DOI context
    text = re.sub(
        r"(?is)```bibtex.*?localgovbench_v010.*?```",
        "",
        text,
    )
    text = re.sub(
        r"(?im)^> \*\*Historical notice\.\*\*.*$",
        "",
        text,
    )
    text = re.sub(
        r"(?is)\| v0\.1\.0 \(historical\).*?\n\n",
        "\n\n",
        text,
    )
    return text


@pytest.mark.parametrize("path", ACTIVE_FILES, ids=lambda p: p.name)
def test_active_docs_exist(path: Path):
    assert path.is_file(), f"Missing active doc: {path}"


def test_readme_states_active_framework_is_disclosure_functions():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "Disclosure Functions" in text
    assert "not** the active analytical framework" in text or "not the active analytical framework" in text
    assert "10.5281/zenodo.20543779" in text


def test_citation_cff_version_and_historical_doi():
    doc = yaml.safe_load((REPO_ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert str(doc.get("version")).startswith("0.2")
    assert "readiness" not in doc.get("abstract", "").lower() or "not" in doc.get("abstract", "").lower()
    abstract = doc["abstract"].lower()
    assert "disclosure" in abstract
    assert "10.5281/zenodo.20543779" in str(doc)
    # Must not set current doi to the historical version DOI
    assert doc.get("doi") in (None, "")


def test_pyproject_version():
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "0.2.0"' in text
    assert "disclosure" in text.lower()


def test_active_docs_avoid_unqualified_readiness_claims():
    for path in ACTIVE_FILES:
        raw = path.read_text(encoding="utf-8")
        scan = _strip_historical_blocks(raw)
        for pat in FORBIDDEN_CURRENT_PATTERNS:
            assert not pat.search(scan), f"{path} matched forbidden current claim: {pat.pattern}"


def test_legacy_banner_present_on_benchmark_spec():
    text = (REPO_ROOT / "docs" / "benchmark_specification.md").read_text(encoding="utf-8")
    assert "Status: LEGACY — v0.1.0" in text


def test_zenodo_draft_json_parses():
    path = REPO_ROOT / "docs" / "releases" / "zenodo_v0.2.0.draft.json"
    import json

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["version"] == "0.2.0"
    assert "Governance Readiness Benchmark" not in data["title"]
    assert "Disclosure" in data["title"]

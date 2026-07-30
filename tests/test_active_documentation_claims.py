"""Fail if active public docs make unqualified legacy measurement claims."""

from __future__ import annotations

import json
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
    REPO_ROOT / "CONTRIBUTING.md",
    REPO_ROOT / "localgovbench_measurement_validation" / "affordance" / "README.md",
    REPO_ROOT / "docs" / "releases" / "public_positioning_v0.2.0.md",
    REPO_ROOT / "docs" / "releases" / "github_release_v0.2.0.md",
    REPO_ROOT / "docs" / "releases" / "zenodo_metadata_v0.2.0.md",
    REPO_ROOT / "docs" / "releases" / "release_readiness_v0.2.0.md",
    REPO_ROOT / "docs" / "releases" / "NEXT_RELEASE.md",
    REPO_ROOT / "docs" / "releases" / "README.md",
]

LEGACY_STATUS_MARKERS = (
    "Status: LEGACY — v0.1.0",
    "Status: DEPRECATED",
    "Status: HISTORICAL REFERENCE",
    "Status: SUPERSEDED",
)

# Unqualified *current* framing — historical contrast tables/notices are stripped first.
FORBIDDEN_CURRENT_PATTERNS = [
    re.compile(r"(?i)\bLocalGovBench is (?:an? )?(?:open )?(?:research )?(?:artifact|instrument|benchmark) for (?:studying )?(?:local and )?on-premise"),
    re.compile(r"(?i)\bprovides:\s*\n\s*- A version \*\*0\.1\.0\*\* governance framework"),
    re.compile(r"(?i)\bcurrently measures?\b.{0,80}\bgovernance readiness\b"),
    re.compile(r"(?i)\bcurrently measures?\b.{0,80}\bgovernance maturity\b"),
    re.compile(r"(?i)\bactive (?:analytical )?framework\b.{0,60}\bgovernance readiness\b"),
    re.compile(r"(?i)\bLocalGovBench (?:currently )?(?:is|provides|implements) .{0,40}\bshortfall (?:score|scoring)\b"),
    re.compile(r"(?i)\bLocalGovBench (?:currently )?(?:is|provides|implements) .{0,40}\bjurisdiction ranking"),
    re.compile(r"(?i)\bLocalGovBench (?:currently )?(?:is|provides|implements) .{0,40}\bcompliance score"),
    re.compile(r"(?i)\bLocalGovBench (?:currently )?(?:is|provides|implements) .{0,40}\bcomposite (?:readiness|governance) (?:score|index)\b"),
    re.compile(r"(?i)\bsovereign LLM (?:deployment )?readiness\b(?!.{0,80}\b(?:historical|legacy|v0\.1\.0|not the active)\b)"),
]


def _strip_historical_blocks(text: str) -> str:
    """Remove clearly marked historical/v0.1.0 paragraphs for scanning."""
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
    text = re.sub(
        r"(?im)^.*\b(?:historical|legacy|v0\.1\.0|previous version)\b.*$",
        "",
        text,
    )
    return text


def _is_legacy_labelled(path: Path) -> bool:
    head = path.read_text(encoding="utf-8")[:800]
    return any(m in head for m in LEGACY_STATUS_MARKERS)


@pytest.mark.parametrize("path", ACTIVE_FILES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_active_docs_exist(path: Path):
    assert path.is_file(), f"Missing active doc: {path}"


def test_readme_states_active_framework_is_disclosure_functions():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "Disclosure Functions" in text
    assert "not the active analytical framework" in text
    assert "10.5281/zenodo.20543779" in text
    assert "10.5281/zenodo.21500899" in text
    assert "7,434" in text or "7434" in text
    assert "aa8ea3d" in text
    assert "ac2669c" in text


def test_positioning_doc_exists_and_restrained():
    text = (REPO_ROOT / "docs" / "releases" / "public_positioning_v0.2.0.md").read_text(
        encoding="utf-8"
    )
    assert "Disclosure Affordances in Public AI and Algorithm Registers" in text
    assert "Non-claims" in text or "non-claims" in text.lower()
    assert "not" in text.lower() and "completed" in text.lower()


def test_citation_cff_version_and_historical_doi():
    doc = yaml.safe_load((REPO_ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert str(doc.get("version")) == "1.0.0"
    abstract = doc["abstract"].lower()
    assert "disclosure" in abstract or "documentary evidence" in abstract
    assert "10.5281/zenodo.20543779" in str(doc)
    assert "10.5281/zenodo.21500899" in str(doc)


def test_readme_canonical_doi():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "10.5281/zenodo.21500899" in text
    assert "Disclosure Functions" in text or "Disclosure Affordance" in text
    assert "10.5281/zenodo.20543779" in text
    assert "Historical" in text or "historical" in text
    assert "v1.0.0" in text


def test_pyproject_version():
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "1.0.0"' in text
    assert "disclosure" in text.lower() or "documentary" in text.lower()


def test_active_docs_avoid_unqualified_readiness_claims():
    for path in ACTIVE_FILES:
        if _is_legacy_labelled(path):
            continue
        raw = path.read_text(encoding="utf-8")
        scan = _strip_historical_blocks(raw)
        for pat in FORBIDDEN_CURRENT_PATTERNS:
            assert not pat.search(scan), f"{path} matched forbidden current claim: {pat.pattern}"


def test_legacy_banner_present_on_key_docs():
    required = [
        REPO_ROOT / "docs" / "benchmark_specification.md",
        REPO_ROOT / "docs" / "demo_walkthrough.md",
        REPO_ROOT / "data" / "benchmark" / "README.md",
        REPO_ROOT / "validation" / "README.md",
        REPO_ROOT / "validation" / "docs" / "content_validity_guide.md",
    ]
    for path in required:
        text = path.read_text(encoding="utf-8")
        assert "Status: LEGACY — v0.1.0" in text
        assert "Do not use" in text and "current analytical specification" in text


def test_zenodo_draft_json_parses():
    path = REPO_ROOT / "docs" / "releases" / "zenodo_v0.2.0.draft.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["version"] == "0.2.0"
    assert "Governance Readiness Benchmark" not in data["title"]
    assert "Disclosure" in data["title"]
    assert data.get("doi") == "10.5281/zenodo.21500899"


def test_root_zenodo_json_active_doi():
    data = json.loads((REPO_ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    assert data["version"] == "1.0.0"
    assert "21500899" in json.dumps(data)
    assert "20543779" in json.dumps(data)


def test_release_docs_distinguish_published_and_unreleased():
    readiness = (REPO_ROOT / "docs/releases/release_readiness_v0.2.0.md").read_text(
        encoding="utf-8"
    )
    nxt = (REPO_ROOT / "docs/releases/NEXT_RELEASE.md").read_text(encoding="utf-8")
    index = (REPO_ROOT / "docs/releases/README.md").read_text(encoding="utf-8")
    assert "Published" in readiness
    assert "does **not** include" in readiness.lower() or "does not include" in readiness.lower()
    assert "NEXT_DOI_TBD" in nxt
    assert "v1.0.0" in nxt
    assert "v1.0.0" in index
    assert "10.5281/zenodo.21500899" in index


def test_github_release_notes_list_milestones():
    text = (REPO_ROOT / "docs" / "releases" / "github_release_v0.2.0.md").read_text(
        encoding="utf-8"
    )
    assert "aa8ea3d" in text
    assert "ac2669c" in text
    assert "framework transition" in text.lower()
    assert "10.5281/zenodo.21500899" in text

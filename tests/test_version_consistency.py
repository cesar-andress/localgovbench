"""Runtime / metadata version consistency."""

from __future__ import annotations

from pathlib import Path

import localgovbench
import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]


def _pyproject_version() -> str:
    text = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("version"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise AssertionError("version missing in pyproject.toml")


def test_runtime_matches_pyproject():
    assert localgovbench.__version__ == _pyproject_version()
    assert localgovbench.__version__ == "1.0.0"


def test_citation_cff_tracks_v100():
    doc = yaml.safe_load((REPO / "CITATION.cff").read_text(encoding="utf-8"))
    assert str(doc["version"]) == "1.0.0"
    blob = str(doc)
    assert "10.5281/zenodo.21500899" in blob
    assert "10.5281/zenodo.20543779" in blob
    assert "v1.0.0" in blob or "1.0.0" in blob


def test_zenodo_json_tracks_v100():
    import json

    data = json.loads((REPO / ".zenodo.json").read_text(encoding="utf-8"))
    assert data["version"] == "1.0.0"
    assert "21500899" in json.dumps(data)
    assert "20543779" in json.dumps(data)


def test_next_release_has_doi_placeholder_not_invented():
    text = (REPO / "docs/releases/NEXT_RELEASE.md").read_text(encoding="utf-8")
    assert "NEXT_DOI_TBD" in text
    assert "10.5281/zenodo.21500899" in text
    assert "unchanged" in text.lower()
    assert "v1.0.0" in text

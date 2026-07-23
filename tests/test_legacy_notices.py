"""Legacy / non-DF notices on results-looking surfaces."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

REQUIRED = [
    REPO / "reports" / "README.md",
    REPO / "results" / "README.md",
    REPO / "localgovbench_measurement_validation" / "pilot_public_satisfiability" / "README.md",
    REPO / "data" / "README.md",
    REPO / "prompts" / "README.md",
]

MARKERS = (
    "not Disclosure Functions v1 empirical results",
    "not the active Disclosure Functions",
)


@pytest.mark.parametrize("path", REQUIRED, ids=lambda p: str(p.relative_to(REPO)))
def test_legacy_notice_present(path: Path):
    text = path.read_text(encoding="utf-8")
    assert any(m in text for m in MARKERS), path
    assert "readiness" in text.lower() or "LEGACY" in text or "legacy" in text.lower()

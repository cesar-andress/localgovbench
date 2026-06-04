#!/usr/bin/env python3
"""Validate repository structure and key metadata for publication readiness."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "pyproject.toml",
    ".gitignore",
    "docs/framework.md",
    "docs/methodology.md",
    "docs/governance_dimensions.md",
    "docs/ai_act_mapping.md",
    "docs/gdpr_mapping.md",
    "docs/zenodo_release.md",
    "localgovbench/__init__.py",
    "localgovbench/framework/dimensions.py",
    "localgovbench/framework/scoring.py",
    "localgovbench/framework/checklist.py",
    "localgovbench/evaluation/rubric.py",
    "localgovbench/evaluation/validators.py",
    "localgovbench/utils/io.py",
    "data/README.md",
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "data/templates/README.md",
    "prompts/README.md",
    "examples/example_assessment.yaml",
    "examples/README.md",
    "tests/test_dimensions.py",
    "tests/test_scoring.py",
    "tests/test_checklist.py",
    "scripts/run_example_assessment.py",
]


def main() -> int:
    missing = [p for p in REQUIRED_PATHS if not (ROOT / p).exists()]
    if missing:
        print("Missing required paths:")
        for path in missing:
            print(f"  - {path}")
        return 1

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if "LocalGovBench" not in citation:
        print("CITATION.cff does not mention LocalGovBench.")
        return 1

    example = (ROOT / "examples" / "example_assessment.yaml").read_text(encoding="utf-8")
    if "synthetic: true" not in example:
        print("example_assessment.yaml must declare synthetic: true")
        return 1

    print("Repository structure validation passed.")
    print(f"Checked {len(REQUIRED_PATHS)} required paths under {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run the synthetic example assessment bundled with LocalGovBench."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.evaluation.rubric import describe_maturity
from localgovbench.evaluation.validators import validate_assessment
from localgovbench.framework.dimensions import FRAMEWORK_VERSION
from localgovbench.framework.scoring import compute_maturity_score
from localgovbench.utils.io import load_yaml


def main() -> int:
    example_path = ROOT / "examples" / "example_assessment.yaml"
    payload = load_yaml(example_path)

    issues = validate_assessment(payload)
    if issues:
        print("Validation failed:")
        for issue in issues:
            print(f"  - {issue.field}: {issue.message}")
        return 1

    responses = payload["responses"]
    result = compute_maturity_score(responses)

    fw_version = payload["metadata"].get("framework_version", FRAMEWORK_VERSION)
    print("LocalGovBench — synthetic example assessment")
    print("=" * 48)
    print(f"Framework version: {fw_version}")
    print(f"Source: {example_path.name}")
    print(f"Title: {payload['metadata'].get('title', 'N/A')}")
    print(f"Deployment: {payload['metadata'].get('deployment_model', 'N/A')}")
    print(f"Synthetic: {payload['metadata'].get('synthetic')}")
    print()
    print(f"Overall maturity: {result.overall} ({describe_maturity(result.overall)})")
    print("Per dimension:")
    for dim_id, score in sorted(result.by_dimension.items()):
        print(f"  - {dim_id}: {score} ({describe_maturity(score)})")
    print()
    print("WARNING: This output is based on synthetic demonstration data only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

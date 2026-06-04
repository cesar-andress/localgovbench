#!/usr/bin/env python3
"""Compute I-CVI, S-CVI/Ave, and Lawshe CVR from expert relevance survey results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.validation.content_validity import (
    ICVI_THRESHOLD,
    compute_lawshe_cvr,
    compute_scale_cvi_ave,
    load_relevance_survey,
)

DEFAULT_INPUT = ROOT / "validation" / "content_validity" / "indicator_relevance_survey_results.yaml"
DEFAULT_OUTPUT = ROOT / "validation" / "reports" / "content_validity_analysis.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Content validity analysis (CVI, CVR).")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if not args.input.exists():
        print(
            f"Input not found: {args.input}\n"
            "Copy indicator_relevance_survey_results.example.yaml and complete expert ratings.",
            file=sys.stderr,
        )
        return 1

    item_ratings = load_relevance_survey(args.input)
    scale = compute_scale_cvi_ave(item_ratings)

    from localgovbench.utils.io import load_yaml

    cvr_results = []
    raw = load_yaml(args.input)
    for item in raw.get("essential_ratings") or []:
        cvr = compute_lawshe_cvr(item["criterion_id"], item["essential_flags"])
        cvr_results.append(
            {
                "criterion_id": cvr.item_id,
                "cvr": cvr.cvr,
                "n_essential": cvr.n_essential,
                "n_experts": cvr.n_experts,
                "passes_minimum": cvr.passes_minimum,
            }
        )

    payload = {
        "instrument": "localgovbench-v0.1",
        "icvi_threshold": ICVI_THRESHOLD,
        "s_cvi_ave": scale.s_cvi_ave,
        "items_below_icvi_threshold": list(scale.items_below_threshold),
        "item_cvi": [
            {
                "criterion_id": i.item_id,
                "i_cvi": i.i_cvi,
                "n_experts": i.n_experts,
                "passes": i.passes_threshold,
            }
            for i in scale.items
        ],
        "lawshe_cvr": cvr_results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("Content validity analysis")
    print(f"S-CVI/Ave: {scale.s_cvi_ave}")
    print(f"Items below I-CVI {ICVI_THRESHOLD}: {len(scale.items_below_threshold)}")
    print(f"Output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate blank expert Delphi response YAML files from Round 1 instrument."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

INSTRUMENT = ROOT / "validation" / "content_validity" / "delphi" / "delphi_round1_instrument.yaml"
RESPONSES_DIR = ROOT / "validation" / "content_validity" / "delphi" / "responses"
DEFAULT_EXPERT_IDS = [f"exp_{i:03d}" for i in range(1, 13)]


def load_instrument(path: Path) -> dict:
    from localgovbench.utils.io import load_yaml

    if not path.is_file():
        raise SystemExit(f"Instrument not found: {path}")
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise SystemExit("Instrument root must be a mapping")
    criteria = data.get("criteria")
    if not isinstance(criteria, list) or len(criteria) != 25:
        raise SystemExit(f"Expected 25 criteria in instrument, found {len(criteria or [])}")
    return data


def build_response_file(instrument: dict, expert_id: str) -> dict:
    framing = instrument.get("study_framing") or {}
    criteria = instrument["criteria"]
    return {
        "schema_version": "1.0",
        "confidential": True,
        "gitignored": True,
        "synthetic": False,
        "expert_id": expert_id,
        "round": instrument.get("round", 1),
        "instrument_ref": INSTRUMENT.name,
        "instrument_version": instrument.get("instrument_version", "v0.1.0"),
        "generated_on": date.today().isoformat(),
        "submitted_at": None,
        "expert_domain_code": None,
        "study_framing": {
            "construct": framing.get("construct", "Programme-Level Governance Readiness"),
            "evidence_layer": framing.get("evidence_layer", "confidential programme dossier"),
            "forbidden_basis": framing.get("forbidden_basis", "public-document observability"),
            "instruction": framing.get("instruction", "").strip(),
        },
        "responses": [
            {
                "criterion_id": c["criterion_id"],
                "dimension_id": c["dimension_id"],
                "relevance_1_5": None,
                "clarity_1_5": None,
                "essential_yes_no": None,
                "suggested_revision": None,
                "comment": None,
            }
            for c in criteria
            if isinstance(c, dict) and c.get("criterion_id")
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate blank Delphi expert response templates.")
    parser.add_argument("--instrument", type=Path, default=INSTRUMENT)
    parser.add_argument("--output-dir", type=Path, default=RESPONSES_DIR)
    parser.add_argument(
        "--expert-ids",
        nargs="+",
        default=DEFAULT_EXPERT_IDS,
        help="Pseudonymous expert IDs (default: exp_001 … exp_012)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing response files",
    )
    args = parser.parse_args()

    instrument = load_instrument(args.instrument)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    from localgovbench.utils.io import save_yaml

    created = 0
    skipped = 0
    for expert_id in args.expert_ids:
        out_path = args.output_dir / f"{expert_id}_round1.yaml"
        if out_path.exists() and not args.force:
            skipped += 1
            continue
        payload = build_response_file(instrument, expert_id)
        save_yaml(out_path, payload)
        created += 1

    print(f"Expert response templates: {created} created, {skipped} skipped (use --force to overwrite)")
    print(f"Output directory: {args.output_dir}")
    print(f"Criteria per file: 25")
    print(f"Confidential / gitignored: yes (see .gitignore)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

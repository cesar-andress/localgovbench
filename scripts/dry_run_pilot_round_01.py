#!/usr/bin/env python3
"""Technical dry run for pilot_round_01 using NON_SUBSTANTIVE_TEST_FIXTURE only.

Does not write into coder_packets/ or completed_inputs/.
Deletes temporary outputs after verification unless --keep is set.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from localgovbench_measurement_validation.affordance.coding.pilot_launch import (
    PILOT_ROUND_ROOT,
    build_coder_packet_rows,
    validate_blank_packet,
    write_coder_packet,
)
from localgovbench_measurement_validation.affordance.coding.validate import (
    create_adjudication_input,
    export_disagreements,
)
from localgovbench_measurement_validation.affordance.experiments.pipeline import (
    run_affordance_experiment,
)


def _fill_nonsubstantive(rows: list[dict[str, str]], coder: str, *, flip: bool) -> list[dict[str, str]]:
    """Fill minimal valid judgments clearly marked as NON_SUBSTANTIVE_TEST_FIXTURE."""
    out = []
    for i, row in enumerate(rows):
        r = dict(row)
        r["coder_id"] = f"NON_SUBSTANTIVE_TEST_FIXTURE_{coder}"
        r["coding_timestamp"] = "2026-07-23T00:00:00+00:00"
        # Use frozen default as applicability label for fixture only
        appl = r.get("frozen_default_applicability") or "universal"
        r["applicability_label"] = appl
        r["applicability_rationale"] = "NON_SUBSTANTIVE_TEST_FIXTURE"
        if appl == "catalogue_inapplicable":
            support = "absent"
            encoding = "not_applicable"
            linkage = "not_applicable"
        elif flip and i == 0:
            # Force one disagreement for disagreement-export testing
            support = "indirect"
            encoding = "free_text"
            linkage = "none"
            # need an indirect field if any candidates exist
            cand = (r.get("candidate_observed_fields") or "").split("|")
            cand = [c for c in cand if c.strip()]
            r["indirect_supporting_fields"] = cand[0] if cand else "NON_SUBSTANTIVE_FIELD"
        else:
            support = "absent"
            encoding = "not_applicable"
            linkage = "none"
        r["support_level"] = support
        r["encoding_type"] = encoding
        r["documentary_linkage_layer"] = linkage
        r["coder_confidence"] = "low"
        r["coder_rationale"] = "NON_SUBSTANTIVE_TEST_FIXTURE"
        r["anti_overcredit_check"] = "NON_SUBSTANTIVE_TEST_FIXTURE"
        r["adjudication_status"] = "pending"
        r["adjudicated_value"] = ""
        r["notes"] = "NON_SUBSTANTIVE_TEST_FIXTURE — not study data"
        out.append(r)
    return out


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv)

    # Pre-coding blank validation on real packets
    for name in ("pilot_round_01_coder_A.csv", "pilot_round_01_coder_B.csv"):
        path = PILOT_ROUND_ROOT / "coder_packets" / name
        errs = validate_blank_packet(path)
        if errs:
            print("Blank packet validation failed:", errs[:10])
            return 1

    tmp = Path(tempfile.mkdtemp(prefix="pilot_round_01_NON_SUBSTANTIVE_"))
    try:
        rows_a = _fill_nonsubstantive(build_coder_packet_rows("coder_A"), "A", flip=False)
        rows_b = _fill_nonsubstantive(build_coder_packet_rows("coder_B"), "B", flip=True)
        a_path = tmp / "NON_SUBSTANTIVE_TEST_FIXTURE_coder_A.csv"
        b_path = tmp / "NON_SUBSTANTIVE_TEST_FIXTURE_coder_B.csv"
        _write_csv(a_path, rows_a)
        _write_csv(b_path, rows_b)

        disagree = tmp / "NON_SUBSTANTIVE_TEST_FIXTURE_disagreements.csv"
        export_disagreements(a_path, b_path, disagree)
        adj_in = tmp / "NON_SUBSTANTIVE_TEST_FIXTURE_adjudication_input.csv"
        create_adjudication_input(disagree, adj_in)

        # Resolve the forced disagreement so pipeline merge can succeed
        with adj_in.open(encoding="utf-8", newline="") as handle:
            adj_rows = list(csv.DictReader(handle))
        if adj_rows:
            adj_rows[0]["adjudicator_decision"] = (
                "support_level=absent;encoding_type=not_applicable;"
                "documentary_linkage_layer=none;indirect_supporting_fields="
            )
            adj_rows[0]["resolution_status"] = "resolved"
            adj_rows[0]["adjudicator_rationale"] = "NON_SUBSTANTIVE_TEST_FIXTURE"
            fieldnames = list(adj_rows[0].keys())
            with adj_in.open("w", encoding="utf-8", newline="") as handle:
                w = csv.DictWriter(handle, fieldnames=fieldnames)
                w.writeheader()
                w.writerows(adj_rows)

        expected = {r["coding_unit_id"] for r in rows_a}
        out_root = tmp / "pipeline_out"
        result = run_affordance_experiment(
            experiment_id="NON_SUBSTANTIVE_TEST_FIXTURE_pilot",
            coder_a=a_path,
            coder_b=b_path,
            adjudication=adj_in,
            operator="NON_SUBSTANTIVE_TEST_FIXTURE",
            require_complete=True,
            expected_units=expected,
            output_root=out_root,
        )
        assert Path(result["manifest_path"]).is_file()
        assert Path(result["provenance_path"]).is_file()
        assert result["matrix_row_count"] == 33
        print("DRY_RUN_OK")
        print(json.dumps({k: str(v) for k, v in result.items()}, indent=2, sort_keys=True))
        return 0
    finally:
        if not args.keep:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build and validate the Disclosure Functions v1 specification layer.

Regenerates:
  - corpus_lock_v1.json / corpus_lock_v1.md
  - schema_inventory_v1.csv / schema_inventory_v1.json

Validates hand-authored frozen specifications under affordance/config/.

Does not run human coding, realization outputs, gap analysis, figures,
or manuscript rewriting.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench_measurement_validation.affordance.corpus_lock import (  # noqa: E402
    build_corpus_lock,
    write_corpus_lock,
)
from localgovbench_measurement_validation.affordance.paths import (  # noqa: E402
    CORPUS_LOCK_JSON,
    SCHEMA_INVENTORY_CSV,
    SCHEMA_INVENTORY_JSON,
)
from localgovbench_measurement_validation.affordance.schema_inventory import (  # noqa: E402
    build_schema_inventory,
    write_schema_inventory,
)
from localgovbench_measurement_validation.affordance.validate_specs import (  # noqa: E402
    validate_all_hand_authored,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate hand-authored specs and existing generated artefacts only.",
    )
    args = parser.parse_args()

    errors = validate_all_hand_authored()
    if errors:
        print("Hand-authored specification validation FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("Hand-authored specifications: OK")

    if args.validate_only:
        if not CORPUS_LOCK_JSON.is_file() or not SCHEMA_INVENTORY_CSV.is_file():
            print("Generated artefacts missing; run without --validate-only", file=sys.stderr)
            return 1
        print("Validate-only mode complete.")
        return 0

    lock = build_corpus_lock()
    write_corpus_lock(lock)
    inventory = build_schema_inventory(corpus_lock=lock)
    write_schema_inventory(inventory)

    # Determinism check: rebuild inventory and compare CSV bytes
    inventory2 = build_schema_inventory(corpus_lock=lock)
    write_schema_inventory(inventory2)
    csv_bytes_1 = SCHEMA_INVENTORY_CSV.read_bytes()
    inventory3 = build_schema_inventory(corpus_lock=lock)
    write_schema_inventory(inventory3)
    csv_bytes_2 = SCHEMA_INVENTORY_CSV.read_bytes()
    if csv_bytes_1 != csv_bytes_2:
        print("Non-deterministic schema inventory CSV", file=sys.stderr)
        return 1

    by_source: dict[str, int] = {}
    for row in inventory:
        by_source[row["source_name"]] = by_source.get(row["source_name"], 0) + 1

    print(f"Wrote {CORPUS_LOCK_JSON}")
    print(f"  sha256={lock['sha256']}")
    print(f"  total_records={lock['total_record_count']}")
    print(f"  counts={lock['record_count_per_source']}")
    print(f"Wrote {SCHEMA_INVENTORY_CSV} and {SCHEMA_INVENTORY_JSON}")
    print(f"  inventory_rows={len(inventory)}")
    print(f"  fields_per_source={json.dumps(by_source, sort_keys=True)}")
    print("Specification layer build complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

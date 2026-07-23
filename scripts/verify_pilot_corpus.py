#!/usr/bin/env python3
"""Verify the pilot corpus file against the frozen Disclosure Functions corpus lock.

Does not download data. Does not invent bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = (
    ROOT
    / "localgovbench_measurement_validation"
    / "affordance"
    / "locks"
    / "corpus_lock_v1.json"
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lock-only",
        action="store_true",
        help="Validate lock metadata only; do not require corpus bytes.",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=None,
        help="Override corpus path (default: lock canonical/portable path).",
    )
    args = parser.parse_args()

    if not LOCK_PATH.is_file():
        print(f"ERROR: missing corpus lock: {LOCK_PATH}", file=sys.stderr)
        return 2

    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    expected_sha = lock["sha256"]
    expected_n = lock["total_record_count"]
    portable = lock.get("portable_path") or lock.get("canonical_path")
    if not portable:
        print("ERROR: lock missing canonical_path/portable_path", file=sys.stderr)
        return 2

    print(f"lock_version={lock.get('corpus_lock_version')}")
    print(f"expected_records={expected_n}")
    print(f"expected_sha256={expected_sha}")
    print(f"portable_path={portable}")
    if lock.get("absolute_path"):
        print(
            "note: historical absolute_path present in lock; "
            "use portable_path/canonical_path for verification"
        )

    if args.lock_only:
        print("OK (lock-only)")
        return 0

    corpus = args.corpus or (ROOT / portable)
    if not corpus.is_file():
        print(f"ERROR: corpus file missing: {corpus}", file=sys.stderr)
        print(
            "See docs/reproducibility/corpus_acquisition.md for acquisition options.",
            file=sys.stderr,
        )
        return 1

    observed = sha256_file(corpus)
    if observed != expected_sha:
        print("ERROR: SHA-256 mismatch", file=sys.stderr)
        print(f"  expected: {expected_sha}", file=sys.stderr)
        print(f"  observed: {observed}", file=sys.stderr)
        return 1

    # Count logical CSV records (fields may contain embedded newlines).
    import csv

    with corpus.open(encoding="utf-8", newline="") as handle:
        n = sum(1 for _ in csv.DictReader(handle))
    if n != expected_n:
        print(
            f"ERROR: record count mismatch expected={expected_n} observed={n}",
            file=sys.stderr,
        )
        return 1

    print(f"OK corpus verified at {corpus} (n={n})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

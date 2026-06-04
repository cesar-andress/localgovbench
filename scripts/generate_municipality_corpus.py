#!/usr/bin/env python3
"""Generate synthetic municipality document corpus."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.synthetic.municipality_corpus import (
    DEFAULT_MUNICIPALITY_COUNT,
    DEFAULT_SEED,
    generate_municipality_corpus,
)

DEFAULT_OUTPUT = ROOT / "data" / "synthetic" / "municipality_corpus"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic municipality corpus.")
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_MUNICIPALITY_COUNT,
        help=f"Number of municipalities (default {DEFAULT_MUNICIPALITY_COUNT})",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    metadata = generate_municipality_corpus(
        args.output_dir,
        count=args.count,
        seed=args.seed,
    )

    print("Synthetic municipality corpus")
    print("=" * 40)
    print(f"Municipalities: {metadata['municipality_count']}")
    print(f"Seed: {metadata['seed']}")
    print(f"Tier distribution: {metadata['maturity_tier_distribution']}")
    print(f"Output: {args.output_dir}")
    print(f"Metadata: {args.output_dir / 'metadata.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

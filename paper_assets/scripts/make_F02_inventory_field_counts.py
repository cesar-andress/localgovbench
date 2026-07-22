#!/usr/bin/env python3
"""Generate F02_inventory_field_counts from repository artefacts. No invented findings."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "paper_assets" / "figures" / "F02_inventory_field_counts" / "F02_inventory_field_counts.png"
import csv

def main() -> None:
    path = (
        REPO
        / "localgovbench_measurement_validation/affordance/outputs/schema_inventory_v1.csv"
    )
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    from collections import Counter

    counts = Counter(r["source_name"] for r in rows)
    sources = sorted(counts)
    values = [counts[s] for s in sources]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(sources, values, color="#55A868")
    ax.set_ylabel("Distinct observed fields")
    ax.set_title("Observed schema inventory field counts by source")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300)
    print(OUT)

if __name__ == "__main__":
    main()

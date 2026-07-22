#!/usr/bin/env python3
"""Generate F01_corpus_record_counts from repository artefacts. No invented findings."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "paper_assets" / "figures" / "F01_corpus_record_counts" / "F01_corpus_record_counts.png"
def main() -> None:
    lock = json.loads(
        (
            REPO
            / "localgovbench_measurement_validation/affordance/locks/corpus_lock_v1.json"
        ).read_text(encoding="utf-8")
    )
    counts = lock["record_count_per_source"]
    sources = sorted(counts)
    values = [counts[s] for s in sources]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(sources, values, color="#4C72B0")
    ax.set_ylabel("Records (n)")
    ax.set_title("Locked corpus record counts by source")
    ax.tick_params(axis="x", rotation=30)
    ax.set_ylim(0, max(values) * 1.15)
    for i, v in enumerate(values):
        ax.text(i, v, str(v), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300)
    print(OUT)

if __name__ == "__main__":
    main()

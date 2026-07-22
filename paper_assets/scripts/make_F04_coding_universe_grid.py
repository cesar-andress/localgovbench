#!/usr/bin/env python3
"""Generate F04_coding_universe_grid from repository artefacts. No invented findings."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "paper_assets" / "figures" / "F04_coding_universe_grid" / "F04_coding_universe_grid.png"
import csv
import numpy as np

def main() -> None:
    path = (
        REPO
        / "localgovbench_measurement_validation/affordance/coding/templates/schema_coding_template_v1.csv"
    )
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    sources = sorted({r["source_name"] for r in rows})
    funcs = sorted({r["disclosure_function_id"] for r in rows})
    pilot_path = (
        REPO
        / "localgovbench_measurement_validation/affordance/coding/templates/pilot_coding_manifest_v1.csv"
    )
    with pilot_path.open(encoding="utf-8", newline="") as handle:
        pilot = {
            (r["source_name"], r["disclosure_function_id"])
            for r in csv.DictReader(handle)
        }
    grid = np.zeros((len(funcs), len(sources)))
    for i, f in enumerate(funcs):
        for j, s in enumerate(sources):
            if (s, f) in {(r["source_name"], r["disclosure_function_id"]) for r in rows}:
                grid[i, j] = 2 if (s, f) in pilot else 1
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(grid, aspect="auto", cmap="Blues", vmin=0, vmax=2)
    ax.set_xticks(range(len(sources)))
    ax.set_xticklabels(sources, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(funcs)))
    ax.set_yticklabels(funcs, fontsize=8)
    ax.set_title("Coding universe (1=full template; 2=pilot subset)")
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2])
    cbar.ax.set_yticklabels(["absent", "template", "pilot"])
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300)
    print(OUT)

if __name__ == "__main__":
    main()

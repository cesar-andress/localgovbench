#!/usr/bin/env python3
"""Generate F03_disclosure_functions_tiers from repository artefacts. No invented findings."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "paper_assets" / "figures" / "F03_disclosure_functions_tiers" / "F03_disclosure_functions_tiers.png"
import yaml

def main() -> None:
    path = (
        REPO
        / "localgovbench_measurement_validation/affordance/config/disclosure_functions_v1.yaml"
    )
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    core = [f["id"] for f in data.get("core_functions", [])]
    mods = [f["id"] for f in data.get("modules", [])]
    fig, ax = plt.subplots(figsize=(8, 5))
    y = list(range(len(core + mods)))
    labels = core + mods
    colors = ["#4C72B0"] * len(core) + ["#DD8452"] * len(mods)
    ax.barh(y, [1] * len(labels), color=colors)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xticks([])
    ax.set_xlim(0, 1.5)
    ax.set_title("Disclosure Functions v1 (core vs module)")
    ax.invert_yaxis()
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300)
    print(OUT)

if __name__ == "__main__":
    main()

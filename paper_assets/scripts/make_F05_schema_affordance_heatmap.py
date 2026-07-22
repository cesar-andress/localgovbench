#!/usr/bin/env python3
"""Stub for F05_schema_affordance_heatmap. Refuses to invent findings."""
import sys
print(
    "F05_schema_affordance_heatmap: required study inputs are not present. "
    "Do not invent results. Needed: affordance/experiments/outputs/*_schema_affordance_matrix.csv (future)",
    file=sys.stderr,
)
sys.exit(2)

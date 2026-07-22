#!/usr/bin/env python3
"""Analyze Delphi Round 1 expert responses: I-CVI, S-CVI/Ave, Lawshe CVR."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.validation.content_validity import (
    ICVI_THRESHOLD,
    compute_item_cvi,
    compute_lawshe_cvr,
    compute_scale_cvi_ave,
)

RESPONSES_DIR = ROOT / "validation" / "content_validity" / "delphi" / "responses"
INSTRUMENT = ROOT / "validation" / "content_validity" / "delphi" / "delphi_round1_instrument.yaml"
SUMMARY_JSON = ROOT / "exports" / "validation" / "content_validity_round1_summary.json"
ITEMS_CSV = ROOT / "exports" / "validation" / "content_validity_round1_items.csv"
REPORT_MD = ROOT / "validation" / "content_validity" / "delphi" / "delphi_round1_report.md"

SCVI_AVE_THRESHOLD = 0.90
AGREE_MINIMUM = 4

# Lawshe (1975) minimum CVR by panel size (two-tailed, p=0.05).
LAWSHE_MIN_CVR: dict[int, float] = {
    5: 0.99,
    6: 0.99,
    7: 0.99,
    8: 0.75,
    9: 0.78,
    10: 0.62,
    11: 0.59,
    12: 0.62,
    13: 0.54,
    14: 0.51,
    15: 0.49,
    16: 0.47,
    17: 0.45,
    18: 0.42,
    19: 0.40,
    20: 0.38,
}


def lawshe_minimum_cvr(n_experts: int) -> float:
    if n_experts in LAWSHE_MIN_CVR:
        return LAWSHE_MIN_CVR[n_experts]
    if n_experts < 5:
        return 0.99
    if n_experts > 20:
        return 0.37
    return LAWSHE_MIN_CVR.get(n_experts, 0.50)


def load_instrument_criteria() -> list[dict]:
    from localgovbench.utils.io import load_yaml

    data = load_yaml(INSTRUMENT)
    return [c for c in (data.get("criteria") or []) if isinstance(c, dict)]


def load_responses(responses_dir: Path) -> list[dict]:
    from localgovbench.utils.io import load_yaml

    files = sorted(responses_dir.glob("*.yaml"))
    payloads: list[dict] = []
    for path in files:
        data = load_yaml(path)
        if isinstance(data, dict):
            data["_source_file"] = path.name
            payloads.append(data)
    return payloads


def aggregate_ratings(
    responses: list[dict],
) -> tuple[dict[str, list[int]], dict[str, list[int]], dict[str, list[bool]], dict[str, str]]:
    relevance: dict[str, list[int]] = defaultdict(list)
    clarity: dict[str, list[int]] = defaultdict(list)
    essential: dict[str, list[bool]] = defaultdict(list)
    dimensions: dict[str, str] = {}

    for payload in responses:
        for item in payload.get("responses") or []:
            if not isinstance(item, dict):
                continue
            cid = item.get("criterion_id")
            if not cid:
                continue
            dimensions[cid] = item.get("dimension_id") or dimensions.get(cid, "")
            rel = item.get("relevance_1_5")
            if isinstance(rel, int):
                relevance[cid].append(rel)
            clr = item.get("clarity_1_5")
            if isinstance(clr, int):
                clarity[cid].append(clr)
            ess = item.get("essential_yes_no")
            if isinstance(ess, bool):
                essential[cid].append(ess)

    return relevance, clarity, essential, dimensions


def safe_item_cvi(item_id: str, ratings: list[int]) -> dict | None:
    if not ratings:
        return None
    result = compute_item_cvi(item_id, ratings, agree_minimum=AGREE_MINIMUM)
    return {
        "criterion_id": result.item_id,
        "i_cvi": result.i_cvi,
        "n_experts": result.n_experts,
        "n_agree": result.n_agree,
        "passes_threshold": result.passes_threshold,
    }


def safe_scale_cvi(item_ratings: dict[str, list[int]]) -> dict | None:
    filtered = {k: v for k, v in item_ratings.items() if v}
    if not filtered:
        return None
    scale = compute_scale_cvi_ave(filtered, agree_minimum=AGREE_MINIMUM)
    return {
        "s_cvi_ave": scale.s_cvi_ave,
        "passes_threshold": scale.s_cvi_ave >= SCVI_AVE_THRESHOLD,
        "items_below_threshold": list(scale.items_below_threshold),
        "items": [
            {
                "criterion_id": i.item_id,
                "i_cvi": i.i_cvi,
                "n_experts": i.n_experts,
                "passes_threshold": i.passes_threshold,
            }
            for i in scale.items
        ],
    }


def dimension_averages(
    item_results: dict[str, dict | None],
    dimensions: dict[str, str],
) -> dict[str, float | None]:
    by_dim: dict[str, list[float]] = defaultdict(list)
    for cid, result in item_results.items():
        if result is None:
            continue
        dim = dimensions.get(cid, "unknown")
        by_dim[dim].append(result["i_cvi"])
    return {
        dim: (round(sum(vals) / len(vals), 4) if vals else None)
        for dim, vals in sorted(by_dim.items())
    }


def items_failing(
    relevance_items: dict[str, dict | None],
    clarity_items: dict[str, dict | None],
    cvr_items: dict[str, dict | None],
) -> list[str]:
    failing: set[str] = set()
    for cid, r in relevance_items.items():
        if r is not None and not r["passes_threshold"]:
            failing.add(cid)
    for cid, c in clarity_items.items():
        if c is not None and not c["passes_threshold"]:
            failing.add(cid)
    for cid, e in cvr_items.items():
        if e is not None and not e["passes_minimum"]:
            failing.add(cid)
    return sorted(failing)


def build_report(
    *,
    n_files: int,
    n_experts_rated: int,
    lawshe_min: float,
    relevance_scale: dict | None,
    clarity_scale: dict | None,
    dimension_rel: dict[str, float | None],
    dimension_clr: dict[str, float | None],
    failing: list[str],
    criteria_order: list[str],
) -> str:
    lines = [
        "# Delphi Round 1 — content validity report",
        "",
        f"- Expert response files: **{n_files}**",
        f"- Experts contributing ≥1 rating: **{n_experts_rated}**",
        f"- I-CVI threshold: **{ICVI_THRESHOLD}** (ratings ≥ {AGREE_MINIMUM})",
        f"- S-CVI/Ave threshold: **{SCVI_AVE_THRESHOLD}**",
        f"- Lawshe CVR minimum (n={n_experts_rated or n_files}): **{lawshe_min}**",
        "",
    ]

    if relevance_scale is None and clarity_scale is None:
        lines.extend(
            [
                "## Status",
                "",
                "Awaiting expert responses — no non-null relevance or clarity ratings yet.",
                "",
            ]
        )
    else:
        rel_ave = relevance_scale["s_cvi_ave"] if relevance_scale else "N/A"
        clr_ave = clarity_scale["s_cvi_ave"] if clarity_scale else "N/A"
        lines.extend(
            [
                "## Scale-level summary",
                "",
                f"- S-CVI/Ave (relevance): **{rel_ave}**",
                f"- S-CVI/Ave (clarity): **{clr_ave}**",
                "",
                "## Per-dimension I-CVI averages",
                "",
                "| Dimension | Relevance I-CVI avg | Clarity I-CVI avg |",
                "|-----------|--------------------:|------------------:|",
            ]
        )
        all_dims = sorted(set(dimension_rel) | set(dimension_clr))
        for dim in all_dims:
            rel = dimension_rel.get(dim)
            clr = dimension_clr.get(dim)
            rel_s = f"{rel:.4f}" if rel is not None else "—"
            clr_s = f"{clr:.4f}" if clr is not None else "—"
            lines.append(f"| {dim} | {rel_s} | {clr_s} |")
        lines.append("")

    lines.extend(
        [
            "## Items failing thresholds",
            "",
        ]
    )
    if failing:
        for cid in failing:
            lines.append(f"- `{cid}`")
    else:
        lines.append("- None (or insufficient ratings to evaluate).")
    lines.extend(
        [
            "",
            "## Criterion order",
            "",
            ", ".join(f"`{c}`" for c in criteria_order),
            "",
            "_Generated by scripts/analyze_delphi_round1.py_",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Delphi Round 1 expert responses.")
    parser.add_argument("--responses-dir", type=Path, default=RESPONSES_DIR)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--items-csv", type=Path, default=ITEMS_CSV)
    parser.add_argument("--report-md", type=Path, default=REPORT_MD)
    args = parser.parse_args()

    if not args.responses_dir.is_dir():
        print(f"Responses directory not found: {args.responses_dir}", file=sys.stderr)
        return 1

    criteria = load_instrument_criteria()
    criteria_order = [c["criterion_id"] for c in criteria if c.get("criterion_id")]
    responses = load_responses(args.responses_dir)
    relevance, clarity, essential, dimensions = aggregate_ratings(responses)

    n_files = len(responses)
    rating_counts = [
        len(v) for v in relevance.values()
    ] + [
        len(v) for v in clarity.values()
    ] + [
        len(v) for v in essential.values()
    ]
    n_experts_rated = max(rating_counts) if rating_counts else 0
    panel_n = n_experts_rated or n_files
    lawshe_min = lawshe_minimum_cvr(panel_n)

    relevance_items: dict[str, dict | None] = {}
    clarity_items: dict[str, dict | None] = {}
    cvr_items: dict[str, dict | None] = {}

    for cid in criteria_order:
        relevance_items[cid] = safe_item_cvi(cid, relevance.get(cid, []))
        clarity_items[cid] = safe_item_cvi(cid, clarity.get(cid, []))
        ess = essential.get(cid, [])
        if ess:
            cvr = compute_lawshe_cvr(cid, ess, minimum_cvr=lawshe_min)
            cvr_items[cid] = {
                "criterion_id": cvr.item_id,
                "cvr": cvr.cvr,
                "n_essential": cvr.n_essential,
                "n_experts": cvr.n_experts,
                "passes_minimum": cvr.passes_minimum,
            }
        else:
            cvr_items[cid] = None

    relevance_scale = safe_scale_cvi(relevance)
    clarity_scale = safe_scale_cvi(clarity)

    dim_rel = dimension_averages(relevance_items, dimensions)
    dim_clr = dimension_averages(clarity_items, dimensions)
    failing = items_failing(relevance_items, clarity_items, cvr_items)

    summary = {
        "instrument": "localgovbench-v0.1",
        "round": 1,
        "n_expert_files": n_files,
        "n_experts_with_ratings": n_experts_rated,
        "thresholds": {
            "i_cvi": ICVI_THRESHOLD,
            "s_cvi_ave": SCVI_AVE_THRESHOLD,
            "lawshe_cvr_minimum": lawshe_min,
            "agree_minimum_likert": AGREE_MINIMUM,
        },
        "s_cvi_ave_relevance": relevance_scale["s_cvi_ave"] if relevance_scale else None,
        "s_cvi_ave_clarity": clarity_scale["s_cvi_ave"] if clarity_scale else None,
        "passes_s_cvi_ave_relevance": relevance_scale["passes_threshold"] if relevance_scale else None,
        "passes_s_cvi_ave_clarity": clarity_scale["passes_threshold"] if clarity_scale else None,
        "per_dimension_i_cvi_average_relevance": dim_rel,
        "per_dimension_i_cvi_average_clarity": dim_clr,
        "items_failing_any_threshold": failing,
        "analysis_status": "complete" if n_experts_rated else "awaiting_expert_responses",
    }

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    args.items_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.items_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "criterion_id",
                "dimension_id",
                "n_relevance",
                "i_cvi_relevance",
                "passes_i_cvi_relevance",
                "n_clarity",
                "i_cvi_clarity",
                "passes_i_cvi_clarity",
                "n_essential",
                "cvr",
                "passes_cvr",
            ],
        )
        writer.writeheader()
        for cid in criteria_order:
            rel = relevance_items[cid]
            clr = clarity_items[cid]
            cvr = cvr_items[cid]
            writer.writerow(
                {
                    "criterion_id": cid,
                    "dimension_id": dimensions.get(cid, ""),
                    "n_relevance": rel["n_experts"] if rel else 0,
                    "i_cvi_relevance": rel["i_cvi"] if rel else "",
                    "passes_i_cvi_relevance": rel["passes_threshold"] if rel else "",
                    "n_clarity": clr["n_experts"] if clr else 0,
                    "i_cvi_clarity": clr["i_cvi"] if clr else "",
                    "passes_i_cvi_clarity": clr["passes_threshold"] if clr else "",
                    "n_essential": cvr["n_experts"] if cvr else 0,
                    "cvr": cvr["cvr"] if cvr else "",
                    "passes_cvr": cvr["passes_minimum"] if cvr else "",
                }
            )

    report = build_report(
        n_files=n_files,
        n_experts_rated=n_experts_rated,
        lawshe_min=lawshe_min,
        relevance_scale=relevance_scale,
        clarity_scale=clarity_scale,
        dimension_rel=dim_rel,
        dimension_clr=dim_clr,
        failing=failing,
        criteria_order=criteria_order,
    )
    args.report_md.write_text(report, encoding="utf-8")

    print("Delphi Round 1 analysis")
    print(f"Expert files: {n_files}")
    print(f"Experts with ratings: {n_experts_rated}")
    print(f"Status: {summary['analysis_status']}")
    if relevance_scale:
        print(f"S-CVI/Ave (relevance): {relevance_scale['s_cvi_ave']}")
    if clarity_scale:
        print(f"S-CVI/Ave (clarity): {clarity_scale['s_cvi_ave']}")
    print(f"Items failing any threshold: {len(failing)}")
    print(f"Summary: {args.summary_json}")
    print(f"Items CSV: {args.items_csv}")
    print(f"Report: {args.report_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

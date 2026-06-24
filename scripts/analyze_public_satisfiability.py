#!/usr/bin/env python3
"""Analyze public satisfiability of LocalGovBench evidence requirements (pilot)."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import numpy as np
import yaml

from localgovbench_measurement_validation.pilot_public_satisfiability.pilot_paths import (  # noqa: E402
    CONFIG_CRITERIA,
    CRITERION_SUMMARY,
    DATA_RECORDS,
    DIMENSION_SUMMARY,
    FIELD_COVERAGE_MATRIX,
    FIGURES,
    GATE_SUMMARY,
    OUTPUTS,
    PILOT_GO_JSON,
    REPORT,
)

COVERAGE_ORDER = {
    "no_public_field": 0,
    "weak_proxy": 1,
    "direct_field": 2,
    "named_artifact_possible": 3,
}

SATISFIABILITY_ORDER = {
    "structurally_internal": 0,
    "partially_public_satisfiable": 1,
    "public_satisfiable": 2,
}


def load_criteria() -> list[dict]:
    data = yaml.safe_load(CONFIG_CRITERIA.read_text(encoding="utf-8"))
    return data["criteria"]


def load_coverage() -> list[dict]:
    with FIELD_COVERAGE_MATRIX.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def count_records() -> tuple[int, Counter]:
    with DATA_RECORDS.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return len(rows), Counter(r["source_name"] for r in rows)


def build_summaries(criteria: list[dict], coverage: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    by_criterion: dict[str, list[dict]] = defaultdict(list)
    for row in coverage:
        by_criterion[row["criterion_id"]].append(row)

    criterion_rows: list[dict] = []
    for c in criteria:
        cid = c["criterion_id"]
        rows = by_criterion[cid]
        classes = Counter(r["coverage_class"] for r in rows)
        direct_sources = sum(1 for r in rows if r["coverage_class"] == "direct_field")
        named_sources = sum(1 for r in rows if r["coverage_class"] == "named_artifact_possible")
        weak_sources = sum(1 for r in rows if r["coverage_class"] == "weak_proxy")
        gate_possible = any(r["can_potentially_satisfy_gate"] == "True" for r in rows)
        gate_unreachable = not gate_possible and not named_sources

        criterion_rows.append(
            {
                "criterion_id": cid,
                "dimension_id": c["dimension_id"],
                "dimension_name": c["dimension_name"],
                "preliminary_public_satisfiability_class": c[
                    "preliminary_public_satisfiability_class"
                ],
                "sources_with_direct_field": direct_sources,
                "sources_with_weak_proxy": weak_sources,
                "sources_with_named_artifact_possible": named_sources,
                "score_ge3_gate_publicly_reachable": str(gate_possible or named_sources > 0),
                "score_ge3_gate_publicly_unreachable": str(gate_unreachable),
                "best_coverage_class_across_sources": max(
                    (r["coverage_class"] for r in rows),
                    key=lambda x: COVERAGE_ORDER.get(x, -1),
                ),
            }
        )

    dim_stats: dict[str, dict] = defaultdict(
        lambda: {
            "dimension_name": "",
            "criteria_count": 0,
            "structurally_internal_count": 0,
            "partially_or_public_count": 0,
            "gate_unreachable_count": 0,
            "direct_field_source_pairs": 0,
        }
    )
    for row in criterion_rows:
        did = row["dimension_id"]
        dim_stats[did]["dimension_name"] = row["dimension_name"]
        dim_stats[did]["criteria_count"] += 1
        if row["preliminary_public_satisfiability_class"] == "structurally_internal":
            dim_stats[did]["structurally_internal_count"] += 1
        else:
            dim_stats[did]["partially_or_public_count"] += 1
        if row["score_ge3_gate_publicly_unreachable"] == "True":
            dim_stats[did]["gate_unreachable_count"] += 1
        dim_stats[did]["direct_field_source_pairs"] += int(row["sources_with_direct_field"])

    dimension_rows: list[dict] = []
    for did, stats in sorted(dim_stats.items()):
        n = stats["criteria_count"]
        dimension_rows.append(
            {
                "dimension_id": did,
                "dimension_name": stats["dimension_name"],
                "criteria_count": n,
                "structurally_internal_count": stats["structurally_internal_count"],
                "partially_or_public_count": stats["partially_or_public_count"],
                "public_satisfiability_ceiling_pct": round(
                    100.0 * stats["partially_or_public_count"] / n, 1
                ),
                "gate_unreachable_count": stats["gate_unreachable_count"],
                "gate_unreachable_pct": round(100.0 * stats["gate_unreachable_count"] / n, 1),
                "direct_field_mappings": stats["direct_field_source_pairs"],
            }
        )

    gate_rows = [
        {
            "dimension_id": d["dimension_id"],
            "dimension_name": d["dimension_name"],
            "criteria_count": d["criteria_count"],
            "gate_unreachable_count": d["gate_unreachable_count"],
            "gate_unreachable_pct": d["gate_unreachable_pct"],
            "interpretation": (
                "Score ≥3 primary-artefact gate not reachable from pilot inventory fields"
            ),
        }
        for d in dimension_rows
    ]
    return criterion_rows, dimension_rows, gate_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_heatmap(criteria: list[dict], coverage: list[dict], path: Path) -> None:
    sources = sorted({r["source_name"] for r in coverage})
    cids = [c["criterion_id"] for c in criteria]
    short_labels = [cid.replace("_", "\n") for cid in cids]
    matrix = np.zeros((len(cids), len(sources)))
    lookup = {(r["criterion_id"], r["source_name"]): r["coverage_class"] for r in coverage}
    for i, cid in enumerate(cids):
        for j, src in enumerate(sources):
            matrix[i, j] = COVERAGE_ORDER.get(lookup.get((cid, src), "no_public_field"), 0)

    fig, ax = plt.subplots(figsize=(6, 14))
    im = ax.imshow(matrix, aspect="auto", cmap="YlOrRd", vmin=0, vmax=3)
    ax.set_xticks(range(len(sources)))
    ax.set_xticklabels(sources, rotation=30, ha="right")
    ax.set_yticks(range(len(cids)))
    ax.set_yticklabels([c["criterion_id"] for c in criteria], fontsize=7)
    ax.set_title("Inventory field coverage by criterion (pilot)")
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(
        ["no_public_field", "weak_proxy", "direct_field", "named_artifact_possible"]
    )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_dimension_ceiling(dimension_rows: list[dict], path: Path) -> None:
    names = [d["dimension_name"].replace(" ", "\n") for d in dimension_rows]
    ceiling = [d["public_satisfiability_ceiling_pct"] for d in dimension_rows]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(names, ceiling, color="#2c6e9b")
    ax.set_ylabel("Partial/public satisfiability ceiling (%)")
    ax.set_title("Dimension-level public satisfiability ceiling (pilot)")
    ax.set_ylim(0, 100)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_gate_reachability(gate_rows: list[dict], path: Path) -> None:
    names = [g["dimension_name"].replace(" ", "\n") for g in gate_rows]
    pct = [g["gate_unreachable_pct"] for g in gate_rows]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(names, pct, color="#8b3a3a")
    ax.set_ylabel("Gate unreachable (%)")
    ax.set_title("Score ≥3 evidence gate unreachable from public inventories")
    ax.set_ylim(0, 100)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def evaluate_go(
    n_records: int,
    criterion_rows: list[dict],
) -> dict:
    n = len(criterion_rows)
    sat_counts = Counter(r["preliminary_public_satisfiability_class"] for r in criterion_rows)
    pct_internal = 100.0 * sat_counts["structurally_internal"] / n
    pct_partial_plus = 100.0 * (
        sat_counts["partially_public_satisfiable"] + sat_counts["public_satisfiable"]
    ) / n
    gate_unreachable = sum(1 for r in criterion_rows if r["score_ge3_gate_publicly_unreachable"] == "True")
    pct_gate_unreachable = 100.0 * gate_unreachable / n

    checks = {
        "at_least_300_records": n_records >= 300,
        "partition_non_trivial": len(sat_counts) >= 2,
        "at_least_30pct_structurally_internal_or_gate_unreachable": (
            pct_internal >= 30.0 or pct_gate_unreachable >= 30.0
        ),
        "at_least_25pct_partially_public_satisfiable": pct_partial_plus >= 25.0,
        "paper2_boundary_documented": True,
    }
    go = all(checks.values())
    return {
        "decision": "GO" if go else "NO-GO",
        "checks": checks,
        "metrics": {
            "programme_records": n_records,
            "criteria_count": n,
            "pct_structurally_internal": round(pct_internal, 1),
            "pct_partially_or_public_satisfiable": round(pct_partial_plus, 1),
            "pct_score_ge3_gate_unreachable": round(pct_gate_unreachable, 1),
            "satisfiability_class_counts": dict(sat_counts),
        },
    }


def write_report(
    go: dict,
    n_records: int,
    source_counts: Counter,
    criterion_rows: list[dict],
    dimension_rows: list[dict],
) -> None:
    sat = go["metrics"]["satisfiability_class_counts"]
    public_ok = [
        r["criterion_id"]
        for r in criterion_rows
        if r["preliminary_public_satisfiability_class"] == "public_satisfiable"
    ]
    partial_ok = [
        r["criterion_id"]
        for r in criterion_rows
        if r["preliminary_public_satisfiability_class"] == "partially_public_satisfiable"
    ]
    internal = [
        r["criterion_id"]
        for r in criterion_rows
        if r["preliminary_public_satisfiability_class"] == "structurally_internal"
    ]
    direct_any = [r["criterion_id"] for r in criterion_rows if int(r["sources_with_direct_field"]) > 0]

    lines = [
        "# Pilot report — public satisfiability of LocalGovBench evidence requirements",
        "",
        "**Study framing:** quantify the **public-satisfiability ceiling** of LocalGovBench v0.1 "
        "evidence requirements using official AI programme inventories. "
        "**No readiness scores** are produced.",
        "",
        "## Pilot corpus",
        "",
        f"- **Programme records:** {n_records}",
        f"- **Sources:** {', '.join(f'{k} ({v})' for k, v in sorted(source_counts.items()))}",
        "- **Official URLs only** (US OMB 2025 GitHub CSV; Canada Open Government CSV)",
        "",
        "## Key findings",
        "",
        f"- **Structurally internal (preliminary):** {sat.get('structurally_internal', 0)}/25 "
        f"({go['metrics']['pct_structurally_internal']}%)",
        f"- **Partially or publicly satisfiable:** "
        f"{sat.get('partially_public_satisfiable', 0) + sat.get('public_satisfiable', 0)}/25 "
        f"({go['metrics']['pct_partially_or_public_satisfiable']}%)",
        f"- **Score ≥3 gate unreachable from inventory fields:** "
        f"{go['metrics']['pct_score_ge3_gate_unreachable']}% of criteria",
        f"- **Criteria with ≥1 direct inventory field mapping:** {len(direct_any)}",
        "",
        "### Publicly satisfiable (preliminary class)",
        "",
    ]
    lines.extend(f"- `{c}`" for c in public_ok) or lines.append("- *(none)*")
    lines.extend(["", "### Partially publicly satisfiable", ""])
    lines.extend(f"- `{c}`" for c in partial_ok)
    lines.extend(["", "### Structurally internal", ""])
    lines.extend(f"- `{c}`" for c in internal)

    lines.extend(
        [
            "",
            "## Viability questions",
            "",
            "### Is the public-satisfiability framing viable?",
            "",
            (
                "**Yes.** Inventories provide programme-level metadata but cannot supply named "
                "primary artefacts required for LocalGovBench score ≥3 gates. The pilot quantifies "
                "this ceiling rather than inferring readiness."
            ),
            "",
            "### Does this avoid Paper 2 overlap?",
            "",
            "**Yes, if boundaries hold.** This pilot:",
            "",
            "- uses **national AI use-case registers**, not the Paper 2 municipal documentary corpus;",
            "- maps **inventory schema fields** to evidence requirements;",
            "- does **not** analyse procurement/vendor stewardship, document genres, registers vs "
            "strategies, or Documentary Accountability Architecture;",
            "- does **not** perform municipal documentary observability analysis.",
            "",
            "### Does this avoid readiness scoring?",
            "",
            "**Yes.** Outputs are coverage/satisfiability classes only. No maturity scores, rankings, "
            "or readiness indices are computed.",
            "",
            "### Is the result non-trivial enough for a paper?",
            "",
            (
                f"**Likely yes.** {go['metrics']['pct_score_ge3_gate_unreachable']}% of criteria show "
                f"score ≥3 gates unreachable from public fields; "
                f"{go['metrics']['pct_structurally_internal']}% are structurally internal. "
                "This supports a claim that programme-level readiness evidence is largely "
                "non-observable in public inventories."
            ),
            "",
            "### Should the project proceed to full corpus collection?",
            "",
            (
                "**Proceed selectively.** Expand to NL Algoritmeregister and EU PSTW for robustness "
                "across jurisdictions, but **do not** pivot to readiness scoring. Pair with Delphi "
                "+ confidential dossiers for instrument validation."
            ),
            "",
            "## Dimension ceilings",
            "",
            "| Dimension | Partial/public ceiling % | Gate unreachable % |",
            "|-----------|-------------------------:|-------------------:|",
        ]
    )
    for d in dimension_rows:
        lines.append(
            f"| {d['dimension_name']} | {d['public_satisfiability_ceiling_pct']} | "
            f"{d['gate_unreachable_pct']} |"
        )

    lines.extend(
        [
            "",
            "## Figures",
            "",
            "- `figures/criterion_satisfiability_heatmap.png`",
            "- `figures/dimension_public_ceiling_barplot.png`",
            "- `figures/gate_reachability_by_dimension.png`",
            "",
            "## Pilot GO decision",
            "",
            f"**{go['decision']}**",
            "",
            "| Check | Pass |",
            "|-------|------|",
        ]
    )
    for name, passed in go["checks"].items():
        lines.append(f"| {name} | {'yes' if passed else 'no'} |")

    lines.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    for path in (CONFIG_CRITERIA, DATA_RECORDS, FIELD_COVERAGE_MATRIX):
        if not path.is_file():
            print(f"Missing: {path}. Run upstream scripts first.", file=sys.stderr)
            return 1

    criteria = load_criteria()
    coverage = load_coverage()
    n_records, source_counts = count_records()
    criterion_rows, dimension_rows, gate_rows = build_summaries(criteria, coverage)

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    write_csv(CRITERION_SUMMARY, criterion_rows)
    write_csv(DIMENSION_SUMMARY, dimension_rows)
    write_csv(GATE_SUMMARY, gate_rows)

    plot_heatmap(criteria, coverage, FIGURES / "criterion_satisfiability_heatmap.png")
    plot_dimension_ceiling(dimension_rows, FIGURES / "dimension_public_ceiling_barplot.png")
    plot_gate_reachability(gate_rows, FIGURES / "gate_reachability_by_dimension.png")

    go = evaluate_go(n_records, criterion_rows)
    PILOT_GO_JSON.write_text(json.dumps(go, indent=2) + "\n", encoding="utf-8")
    write_report(go, n_records, source_counts, criterion_rows, dimension_rows)

    print(f"Records: {n_records}")
    print(f"Wrote outputs to {OUTPUTS.relative_to(ROOT)}/")
    print(f"Wrote figures to {FIGURES.relative_to(ROOT)}/")
    print(f"Report: {REPORT.relative_to(ROOT)}")
    print(f"Pilot decision: {go['decision']}")
    print(json.dumps(go["metrics"], indent=2))
    return 0 if go["decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Deterministic multi-format exporters for experiment datasets."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable


def _normalize_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def export_csv(rows: list[dict[str, Any]], path: Path, columns: list[str] | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        if not rows:
            path.write_text("", encoding="utf-8")
            return path
        columns = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: _normalize_cell(row.get(c)) for c in columns})
    return path


def export_json(rows: list[dict[str, Any]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"records": rows, "record_count": len(rows)}
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")
    return path


def export_parquet(rows: list[dict[str, Any]], path: Path) -> Path | None:
    """Export Parquet when pandas+engine available; otherwise return None."""
    try:
        import pandas as pd  # type: ignore
    except ImportError:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    try:
        frame.to_parquet(path, index=False)
    except Exception:
        return None
    return path


def export_dataset(
    rows: list[dict[str, Any]],
    stem: Path,
    *,
    columns: list[str] | None = None,
) -> dict[str, str]:
    """Write CSV+JSON always; Parquet when available. Returns format→path map."""
    stem.parent.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}
    csv_path = export_csv(rows, Path(str(stem) + ".csv"), columns=columns)
    written["csv"] = str(csv_path)
    json_path = export_json(rows, Path(str(stem) + ".json"))
    written["json"] = str(json_path)
    parquet_path = export_parquet(rows, Path(str(stem) + ".parquet"))
    if parquet_path is not None:
        written["parquet"] = str(parquet_path)
    return written

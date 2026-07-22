"""Generate corpus_lock_v1 artefacts from the frozen pilot corpus."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from localgovbench_measurement_validation.affordance.paths import (
    CORPUS_LOCK_JSON,
    CORPUS_LOCK_MD,
    CORPUS_LOCK_VERSION,
    CORPUS_PATH,
    OBJECT_LAYER_BY_SOURCE,
    REPO_ROOT,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit_hash() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=REPO_ROOT,
                text=True,
            )
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNKNOWN"


def build_corpus_lock(corpus_path: Path | None = None) -> dict[str, Any]:
    corpus_path = corpus_path or CORPUS_PATH
    if not corpus_path.is_file():
        raise FileNotFoundError(f"Corpus not found: {corpus_path}")

    with corpus_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if "raw_fields_json" not in fieldnames:
        raise ValueError("Corpus missing required column raw_fields_json")

    source_counts = Counter(row["source_name"] for row in rows)
    collection_dates = sorted({row.get("collection_date", "") for row in rows})

    relative = corpus_path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    lock = {
        "corpus_lock_version": CORPUS_LOCK_VERSION,
        "corpus_filename": corpus_path.name,
        "canonical_path": relative,
        "absolute_path": str(corpus_path.resolve()),
        "sha256": sha256_file(corpus_path),
        "total_record_count": len(rows),
        "source_names": sorted(source_counts.keys()),
        "record_count_per_source": dict(sorted(source_counts.items())),
        "object_layer_per_source": {
            source: OBJECT_LAYER_BY_SOURCE.get(source, "unknown")
            for source in sorted(source_counts.keys())
        },
        "collection_dates_observed": collection_dates,
        "collection_date": collection_dates[0] if len(collection_dates) == 1 else None,
        "generation_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit_hash_at_generation": git_commit_hash(),
        "columns": fieldnames,
        "raw_fields_json_column_confirmed": "raw_fields_json" in fieldnames,
        "notes": [
            "Observed schema fields must be derived only from raw_fields_json.",
            "SOURCE_SCHEMAS is not evidence of field existence.",
            "UK-ATRS object_layer is search_api_slim, not full ATRS.",
            "EU-PSTW object_layer is case_catalogue (contrast stratum).",
        ],
    }
    if sum(source_counts.values()) != len(rows):
        raise AssertionError("Source counts do not sum to total records")
    return lock


def write_corpus_lock(lock: dict[str, Any] | None = None) -> tuple[Path, Path]:
    lock = lock or build_corpus_lock()
    CORPUS_LOCK_JSON.parent.mkdir(parents=True, exist_ok=True)
    CORPUS_LOCK_JSON.write_text(
        json.dumps(lock, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Corpus lock v1",
        "",
        f"- **Version:** `{lock['corpus_lock_version']}`",
        f"- **Filename:** `{lock['corpus_filename']}`",
        f"- **Canonical path:** `{lock['canonical_path']}`",
        f"- **SHA-256:** `{lock['sha256']}`",
        f"- **Total records:** {lock['total_record_count']}",
        f"- **Collection date:** `{lock.get('collection_date')}`",
        f"- **Generated (UTC):** `{lock['generation_timestamp_utc']}`",
        f"- **Git commit at generation:** `{lock['git_commit_hash_at_generation']}`",
        f"- **raw_fields_json present:** `{lock['raw_fields_json_column_confirmed']}`",
        "",
        "## Record counts by source",
        "",
        "| Source | Records | Object layer |",
        "|--------|--------:|--------------|",
    ]
    for source, count in sorted(lock["record_count_per_source"].items()):
        layer = lock["object_layer_per_source"].get(source, "unknown")
        lines.append(f"| {source} | {count} | `{layer}` |")
    lines.extend(
        [
            "",
            "## Columns",
            "",
            ", ".join(f"`{c}`" for c in lock["columns"]),
            "",
            "## Notes",
            "",
        ]
    )
    for note in lock["notes"]:
        lines.append(f"- {note}")
    lines.append("")
    CORPUS_LOCK_MD.write_text("\n".join(lines), encoding="utf-8")
    return CORPUS_LOCK_JSON, CORPUS_LOCK_MD

"""Provenance and experiment manifest helpers (deterministic fields)."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from localgovbench_measurement_validation.affordance.coding.paths import (
    CODING_LAYER_VERSION,
    SPECIFICATION_VERSION,
)
from localgovbench_measurement_validation.affordance.coding.template import load_corpus_lock
from localgovbench_measurement_validation.affordance.experiments.paths import (
    EXPERIMENT_PIPELINE_VERSION,
)
from localgovbench_measurement_validation.affordance.paths import SCHEMA_INVENTORY_VERSION


def git_commit_hash(repo_root: Path | None = None) -> str:
    """Return HEAD commit hash, or 'UNKNOWN' if unavailable."""
    cwd = repo_root or Path(__file__).resolve().parents[3]
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(cwd),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "UNKNOWN"


def software_version(repo_root: Path | None = None) -> str:
    root = repo_root or Path(__file__).resolve().parents[3]
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        for line in pyproject.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("version"):
                # version = "0.2.0"
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return "UNKNOWN"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_provenance(
    *,
    experiment_id: str,
    generator_script: str,
    input_paths: list[str],
    output_paths: list[str],
    operator: str = "local",
    random_seed: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    lock = load_corpus_lock()
    payload: dict[str, Any] = {
        "experiment_id": experiment_id,
        "creation_timestamp_utc": utc_now_iso(),
        "generator_script": generator_script,
        "software_version": software_version(),
        "git_commit": git_commit_hash(),
        "specification_version": SPECIFICATION_VERSION,
        "coding_version": CODING_LAYER_VERSION,
        "pipeline_version": EXPERIMENT_PIPELINE_VERSION,
        "corpus_lock_sha256": lock["sha256"],
        "schema_inventory_version": SCHEMA_INVENTORY_VERSION,
        "operator": operator,
        "random_seed": random_seed,
        "input_paths": sorted(input_paths),
        "output_paths": sorted(output_paths),
    }
    if extra:
        payload["extra"] = extra
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Deterministic JSON: sorted keys, stable separators, trailing newline.
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")
    return path


def build_experiment_manifest(
    *,
    experiment_id: str,
    operator: str = "local",
    random_seed: str | None = None,
    notes: str = "",
) -> dict[str, Any]:
    lock = load_corpus_lock()
    return {
        "experiment_id": experiment_id,
        "date_utc": utc_now_iso()[:10],
        "creation_timestamp_utc": utc_now_iso(),
        "git_commit": git_commit_hash(),
        "specification_version": SPECIFICATION_VERSION,
        "coding_version": CODING_LAYER_VERSION,
        "pipeline_version": EXPERIMENT_PIPELINE_VERSION,
        "corpus_hash": lock["sha256"],
        "software_version": software_version(),
        "operator": operator,
        "random_seed": random_seed,
        "notes": notes,
    }

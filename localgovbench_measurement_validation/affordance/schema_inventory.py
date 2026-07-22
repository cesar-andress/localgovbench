"""Deterministic schema inventory generator from raw_fields_json."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from localgovbench_measurement_validation.affordance.corpus_lock import (
    build_corpus_lock,
    write_corpus_lock,
)
from localgovbench_measurement_validation.affordance.nonempty import (
    classify_value,
    infer_data_type,
    is_nonempty_for_population,
)
from localgovbench_measurement_validation.affordance.normalize import (
    build_rule_index,
    load_normalization_rules,
    normalize_field_name,
)
from localgovbench_measurement_validation.affordance.paths import (
    CORPUS_PATH,
    OBJECT_LAYER_BY_SOURCE,
    SCHEMA_INVENTORY_CSV,
    SCHEMA_INVENTORY_JSON,
    SCHEMA_INVENTORY_VERSION,
)


INVENTORY_COLUMNS = [
    "source_name",
    "raw_field_name",
    "normalized_field_name",
    "observed_record_count",
    "source_record_count",
    "presence_rate",
    "nonempty_count",
    "nonempty_rate",
    "inferred_data_type",
    "object_layer",
    "normalization_rule_applied",
    "normalization_rule_type",
    "value_class_counts_json",
    "schema_inventory_version",
    "corpus_lock_reference",
]


def _load_rows(corpus_path: Path) -> list[dict[str, str]]:
    with corpus_path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_schema_inventory(
    corpus_path: Path | None = None,
    corpus_lock: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    corpus_path = corpus_path or CORPUS_PATH
    corpus_lock = corpus_lock or build_corpus_lock(corpus_path)
    rows = _load_rows(corpus_path)

    rules_doc = load_normalization_rules()
    rule_index = build_rule_index(rules_doc)

    source_totals = Counter(row["source_name"] for row in rows)
    # source -> field -> list of values (only when key present)
    field_values: dict[str, dict[str, list[Any]]] = defaultdict(lambda: defaultdict(list))
    field_present: dict[str, Counter] = defaultdict(Counter)

    for row in rows:
        source = row["source_name"]
        raw = json.loads(row["raw_fields_json"])
        if not isinstance(raw, dict):
            raise ValueError(f"raw_fields_json is not an object for {row.get('record_id')}")
        for key, value in raw.items():
            field_present[source][key] += 1
            field_values[source][key].append(value)

    inventory: list[dict[str, Any]] = []
    lock_ref = corpus_lock["sha256"]

    for source in sorted(field_values.keys()):
        source_n = source_totals[source]
        object_layer = OBJECT_LAYER_BY_SOURCE.get(source, "unknown")
        for raw_field in sorted(field_values[source].keys(), key=lambda x: (x.strip().lower(), x)):
            values = field_values[source][raw_field]
            present = field_present[source][raw_field]
            class_counts: Counter[str] = Counter()
            nonempty = 0
            for value in values:
                cls = classify_value(value)
                class_counts[cls] += 1
                if is_nonempty_for_population(value):
                    nonempty += 1
            # Values only stored when key present; absent keys are source_n - present
            if present < source_n:
                class_counts["key_absent"] += source_n - present

            hit = normalize_field_name(source, raw_field, rule_index)
            inventory.append(
                {
                    "source_name": source,
                    "raw_field_name": raw_field,
                    "normalized_field_name": hit.normalized_field_name,
                    "observed_record_count": present,
                    "source_record_count": source_n,
                    "presence_rate": round(present / source_n, 6),
                    "nonempty_count": nonempty,
                    "nonempty_rate": round(nonempty / source_n, 6),
                    "inferred_data_type": infer_data_type(values),
                    "object_layer": object_layer,
                    "normalization_rule_applied": hit.rule_id,
                    "normalization_rule_type": hit.rule_type,
                    "value_class_counts_json": json.dumps(
                        dict(sorted(class_counts.items())),
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    "schema_inventory_version": SCHEMA_INVENTORY_VERSION,
                    "corpus_lock_reference": lock_ref,
                }
            )

    inventory.sort(key=lambda r: (r["source_name"], r["raw_field_name"]))
    return inventory


def write_schema_inventory(inventory: list[dict[str, Any]] | None = None) -> tuple[Path, Path]:
    if inventory is None:
        lock = build_corpus_lock()
        write_corpus_lock(lock)
        inventory = build_schema_inventory(corpus_lock=lock)

    SCHEMA_INVENTORY_CSV.parent.mkdir(parents=True, exist_ok=True)
    with SCHEMA_INVENTORY_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=INVENTORY_COLUMNS)
        writer.writeheader()
        for row in inventory:
            writer.writerow({k: row[k] for k in INVENTORY_COLUMNS})

    payload = {
        "schema_inventory_version": SCHEMA_INVENTORY_VERSION,
        "corpus_lock_reference": inventory[0]["corpus_lock_reference"] if inventory else None,
        "n_rows": len(inventory),
        "fields": inventory,
    }
    SCHEMA_INVENTORY_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return SCHEMA_INVENTORY_CSV, SCHEMA_INVENTORY_JSON

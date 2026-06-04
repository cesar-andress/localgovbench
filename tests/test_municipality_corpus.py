"""Tests for synthetic municipality corpus generator."""

from __future__ import annotations

import json
from pathlib import Path

from localgovbench.synthetic.municipality_corpus import (
    CORPUS_DOCUMENT_TYPES,
    DEFAULT_MUNICIPALITY_COUNT,
    generate_municipality_corpus,
)


def test_generates_fifty_municipalities_with_six_documents(tmp_path: Path) -> None:
    metadata = generate_municipality_corpus(tmp_path, count=50, seed=42)
    assert metadata["municipality_count"] == 50
    assert metadata["synthetic"] is True
    assert len(metadata["municipalities"]) == 50

    for record in metadata["municipalities"]:
        mun_dir = tmp_path / "municipalities" / record["municipality_id"]
        assert mun_dir.is_dir()
        for doc_type in CORPUS_DOCUMENT_TYPES:
            path = mun_dir / f"{doc_type}.md"
            assert path.is_file()
            text = path.read_text(encoding="utf-8")
            assert "SYNTHETIC" in text
            assert record["municipality_id"] in text


def test_metadata_file_written(tmp_path: Path) -> None:
    generate_municipality_corpus(tmp_path, count=5, seed=1)
    meta_path = tmp_path / "metadata.json"
    assert meta_path.is_file()
    loaded = json.loads(meta_path.read_text(encoding="utf-8"))
    assert loaded["seed"] == 1
    assert set(loaded["document_types"]) == set(CORPUS_DOCUMENT_TYPES)


def test_reproducible_with_same_seed(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    meta_a = generate_municipality_corpus(a, count=10, seed=99)
    meta_b = generate_municipality_corpus(b, count=10, seed=99)
    ids_a = [m["municipality_id"] for m in meta_a["municipalities"]]
    ids_b = [m["municipality_id"] for m in meta_b["municipalities"]]
    assert ids_a == ids_b


def test_default_count_constant() -> None:
    assert DEFAULT_MUNICIPALITY_COUNT == 50

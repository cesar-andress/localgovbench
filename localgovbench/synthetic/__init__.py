"""Synthetic data generators for LocalGovBench experiments."""

from localgovbench.synthetic.municipality_corpus import (
    CORPUS_DOCUMENT_TYPES,
    DEFAULT_MUNICIPALITY_COUNT,
    MunicipalityRecord,
    generate_municipality_corpus,
)

__all__ = [
    "CORPUS_DOCUMENT_TYPES",
    "DEFAULT_MUNICIPALITY_COUNT",
    "MunicipalityRecord",
    "generate_municipality_corpus",
]

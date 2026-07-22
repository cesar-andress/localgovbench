# Supplement A — Corpus

## Purpose

Document the **frozen public inventory corpus** used as the observational base for Disclosure Functions v1 schema analysis: which sources are included, how many records are locked, which columns are authoritative, and how schema fields must be derived.

This supplement supports Methods statements about the empirical corpus. It does **not** report schema-coding outcomes or realization rates.

## Inputs

| Input | Role |
|-------|------|
| Official public AI / algorithm inventory exports (five sources) | Upstream records normalised into the pilot corpus |
| `localgovbench_measurement_validation/pilot_public_satisfiability/data/pilot_programme_records.csv` | Canonical corpus file (filename in lock) |
| `localgovbench_measurement_validation/pilot_public_satisfiability/data/source_registry_expanded.csv` | Source registry metadata (companion file in the same data directory) |
| Builder: `localgovbench_measurement_validation/affordance/corpus_lock.py` via `scripts/build_affordance_specification.py` | Computes SHA-256 and writes the lock |

**Derivation rule (normative):** observed schema fields must be taken only from `raw_fields_json`. `SOURCE_SCHEMAS` (or similar declared schemas) is **not** evidence of field existence.

## Outputs

| Output | Path |
|--------|------|
| Machine-readable corpus lock | `affordance/locks/corpus_lock_v1.json` |
| Human-readable corpus lock | `affordance/locks/corpus_lock_v1.md` |

### Table A1 — Locked corpus summary (from corpus lock v1.0.0)

Values copied from the frozen lock artefact (not recalculated here as new science).

| Property | Value |
|----------|------:|
| Corpus lock version | 1.0.0 |
| Filename | `pilot_programme_records.csv` |
| Canonical path | `localgovbench_measurement_validation/pilot_public_satisfiability/data/pilot_programme_records.csv` |
| SHA-256 | `12ea6282efcf338d362c8eb91a9beffe8dd7eae9f70aa2805723b386c9c8d693` |
| Total records | 7 434 |
| Collection date | 2026-06-24 |
| `raw_fields_json` column confirmed | True |

### Table A2 — Record counts by source and object layer

| Source | Records | Object layer |
|--------|--------:|--------------|
| CA-GC-AI-REG | 412 | `ai_system_register` |
| EU-PSTW | 1 794 | `case_catalogue` |
| NL-ALGO-REG | 1 484 | `algorithm_register` |
| UK-ATRS | 133 | `search_api_slim` |
| US-OMB-2025 | 3 611 | `use_case_inventory` |

**Source:** `affordance/locks/corpus_lock_v1.md`.

### Corpus columns (locked)

`record_id`, `jurisdiction`, `source_name`, `source_url`, `programme_title`, `programme_description`, `agency_or_owner`, `raw_fields_json`, `collection_date`

## Figures

None. No corpus map figure is shipped as a Disclosure Functions v1 result graphic in this package.

## Limitations

1. **Distribution:** the CSV may be absent from a bare Git clone (repository `.gitignore` policy for `*.csv`). Third parties must obtain the file via the Zenodo/data distribution path used for the cited software version, or rebuild from official sources and **verify SHA-256** against Table A1.  
2. **Object-layer caveats (from lock notes):** UK-ATRS is `search_api_slim`, not a claim of full ATRS coverage; EU-PSTW is a `case_catalogue` contrast stratum.  
3. **Machine-local metadata:** `corpus_lock_v1.json` may contain an `absolute_path` field reflecting the generating machine; use `canonical_path` + SHA-256 for portability.  
4. **Not a coding result:** record counts are corpus description only.

## Cross references

| Topic | See |
|-------|-----|
| Schema fields observed in this corpus | [Supplement B](B_observed_schema_inventory.md) |
| Functions applied to schema objects | [Supplement C](C_disclosure_functions_v1.md) |
| Regeneration / verification commands | [Supplement G](G_reproducibility.md) |
| Affordance package overview | `affordance/README.md` |
| Lock notes (authoritative) | `affordance/locks/corpus_lock_v1.md` |

# Corpus lock v1

- **Version:** `1.0.0`
- **Filename:** `pilot_programme_records.csv`
- **Canonical path:** `localgovbench_measurement_validation/pilot_public_satisfiability/data/pilot_programme_records.csv`
- **SHA-256:** `12ea6282efcf338d362c8eb91a9beffe8dd7eae9f70aa2805723b386c9c8d693`
- **Total records:** 7434
- **Collection date:** `2026-06-24`
- **Generated (UTC):** `2026-07-22T23:11:30.807519+00:00`
- **Git commit at generation:** `95f3de8f1a2da7da81f195dcfc1297ec8e8a2512`
- **raw_fields_json present:** `True`

## Record counts by source

| Source | Records | Object layer |
|--------|--------:|--------------|
| CA-GC-AI-REG | 412 | `ai_system_register` |
| EU-PSTW | 1794 | `case_catalogue` |
| NL-ALGO-REG | 1484 | `algorithm_register` |
| UK-ATRS | 133 | `search_api_slim` |
| US-OMB-2025 | 3611 | `use_case_inventory` |

## Columns

`record_id`, `jurisdiction`, `source_name`, `source_url`, `programme_title`, `programme_description`, `agency_or_owner`, `raw_fields_json`, `collection_date`

## Notes

- Observed schema fields must be derived only from raw_fields_json.
- SOURCE_SCHEMAS is not evidence of field existence.
- UK-ATRS object_layer is search_api_slim, not full ATRS.
- EU-PSTW object_layer is case_catalogue (contrast stratum).

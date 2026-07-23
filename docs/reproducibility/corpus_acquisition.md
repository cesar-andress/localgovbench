# Corpus acquisition and verification

**Status:** ACTIVE — Disclosure Functions v1 reproducibility  
**Does not:** invent licensing conclusions; fabricate corpus bytes; claim automated redistribution rights.

## Decision summary

| Option | Status |
|--------|--------|
| A. Safely commit aggregated CSV to git | **BLOCKED — HUMAN DECISION** (redistribution/licensing of multi-source aggregate not affirmed in-repo) |
| B. Separate public archive (Zenodo data deposit) | **Supported as planned path**; not yet published as a dedicated data DOI |
| C. Reconstruct from public source exports | **Technically supported** via `scripts/build_pilot_corpus.py` + official URLs in the source registry |
| D. External deposit only | Acceptable interim if A/B unresolved |

Default CI and clean-room checks **verify** a user-supplied corpus when present; they do **not** require network fetches.

## Present in git

| Artefact | Path |
|----------|------|
| Corpus lock (JSON) | `localgovbench_measurement_validation/affordance/locks/corpus_lock_v1.json` |
| Corpus lock (Markdown) | `localgovbench_measurement_validation/affordance/locks/corpus_lock_v1.md` |
| Schema inventory | `localgovbench_measurement_validation/affordance/outputs/schema_inventory_v1.*` |
| Source registry (tracked CSV exception / local) | `.../pilot_public_satisfiability/data/source_registry_expanded.csv` (may be gitignored by `*.csv` unless allowlisted) |
| Builder script | `scripts/build_pilot_corpus.py` |

## Absent from a clean clone (typical)

| Artefact | Expected path |
|----------|----------------|
| Aggregated programme corpus | `localgovbench_measurement_validation/pilot_public_satisfiability/data/pilot_programme_records.csv` |

**Why absent:** repository `.gitignore` ignores `*.csv` broadly; the aggregate file is large (~27 MB) and multi-source. Committing it requires an explicit human redistribution decision (Option A) that this repository does **not** invent.

## Expected identity (frozen)

| Property | Value |
|----------|------|
| Filename | `pilot_programme_records.csv` |
| Portable / canonical path | `localgovbench_measurement_validation/pilot_public_satisfiability/data/pilot_programme_records.csv` |
| Record count | **7434** |
| SHA-256 | `12ea6282efcf338d362c8eb91a9beffe8dd7eae9f70aa2805723b386c9c8d693` |
| Collection date | `2026-06-24` |
| Lock version | `1.0.0` |

The lock JSON may also contain a historical machine-local `absolute_path` from generation time. Prefer `canonical_path` / `portable_path` for all new documentation and scripts.

## Source registry references

Official access URLs and filters are listed in:

`localgovbench_measurement_validation/pilot_public_satisfiability/data/source_registry_expanded.csv`

Sources: US-OMB-2025, CA-GC-AI-REG, NL-ALGO-REG, EU-PSTW, UK-ATRS.

## Verification commands

```bash
# From repository root — fails clearly if missing or hash mismatch
python3.12 scripts/verify_pilot_corpus.py

# Optional: print lock identity only
python3.12 scripts/verify_pilot_corpus.py --lock-only
```

## Reconstruction procedure (Option C — network required)

If licensing and upstream availability permit **in your jurisdiction**, rebuild then verify:

```bash
python3.12 scripts/build_pilot_corpus.py
python3.12 scripts/verify_pilot_corpus.py
```

**Caveats:**

- Upstream URLs and schemas can change; a rebuild may not match the frozen SHA.
- Matching the frozen lock is required for Disclosure Functions Phase 1 regeneration claims.
- This repository does **not** assert that every upstream licence permits every form of redistribution.

## Unresolved decisions (human)

1. Whether to allowlist and commit the aggregate CSV.  
2. Whether to publish a dedicated Zenodo **data** deposit with its own DOI.  
3. Whether CI should ever run live corpus rebuilds (default: **no**).

## Failure behaviour

| Condition | Behaviour |
|-----------|-----------|
| File missing | `verify_pilot_corpus.py` exits non-zero with path + expected SHA |
| Hash mismatch | Non-zero exit; prints expected vs observed |
| Lock-only mode | Succeeds if lock JSON present and well-formed |

Phase 1 inventory/lock **regeneration** without a verified corpus must be treated as **not yet reproducible from git alone**.

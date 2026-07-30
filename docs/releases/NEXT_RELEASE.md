# Next release candidate — after **v1.0.0**

**Status:** Placeholder for future work after the canonical **v1.0.0** release.  
**Do not** invent a DOI.

## Published baseline (canonical)

| Item | Value |
|------|-------|
| **Canonical stable release** | **v1.0.0** — DOI `10.5281/zenodo.21701861` |
| GitHub release | https://github.com/cesar-andress/localgovbench/releases/tag/v1.0.0 |
| Historical prior DF deposit | v0.2.0 — DOI `10.5281/zenodo.21500899` (**unchanged**; not canonical) |
| Historical GRB archive | v0.1.0 — DOI `10.5281/zenodo.20543779` (**unchanged**; not canonical) |
| Future DOI placeholder | `NEXT_DOI_TBD` |

**Exact statement:** Published software **v1.0.0** (DOI `10.5281/zenodo.21701861`) is the **only** canonical citation. Historical **v0.2.0** and **v0.1.0** deposits remain unchanged for provenance.

## Possible future scope (not committed)

- Human DF pilot coding → IRR  
- Record-level realization / gap tables  
- Commit or separately deposit the aggregate corpus CSV if licensing allows  

## Validation commands

```bash
pip install -e ".[dev]"
python3.12 scripts/validate_repository.py
python3.12 scripts/verify_pilot_corpus.py --lock-only
pytest -m "not integration" -q
```

## Validation of this document

This file retains the `NEXT_DOI_TBD` placeholder until a post-v1.0.0 DOI exists.

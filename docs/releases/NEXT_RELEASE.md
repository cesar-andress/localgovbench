# Next release candidate — after **v1.0.0**

**Status:** Placeholder for future work after the manuscript-stable **v1.0.0** tag.  
**Do not** invent a DOI.

## Published baseline

| Item | Value |
|------|-------|
| Current stable tag | **v1.0.0** |
| Prior Disclosure Functions deposit | v0.2.0 — DOI `10.5281/zenodo.21500899` (**unchanged**) |
| Historical GRB archive | v0.1.0 — DOI `10.5281/zenodo.20543779` (**unchanged**) |
| Future DOI placeholder | `NEXT_DOI_TBD` |

**Exact statement:** Published software **v0.2.0** remains historical and **unchanged**. The **v1.0.0** Git tag is the manuscript-accompanying archive; its Zenodo version DOI is minted on deposit.

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

# LocalGovBench measurement-validation study (Day 1)

Working folder for **Paper 1 rescue feasibility**: empirical measurement-validation of
LocalGovBench v0.1 using **official public programme/use-case inventories** — **not** the
Paper 2 (*Vendor Stewardship in the Public Record*) corpus or methods.

## Hard exclusions (Paper 2 firewall)

- No `paper/data/open_pilot/` or Paper 2 municipal documentary corpus
- No documentary observability as primary design
- No procurement/vendor stewardship as central finding
- No document-genre comparisons (strategies vs registers/portals)
- No Documentary Accountability Architecture

## Affordance specification layer (active paper path)

Canonical Disclosure Functions v1 specification (schema disclosure affordance):

See `affordance/README.md` and regenerate with:

`python3.12 scripts/build_affordance_specification.py`

LocalGovBench criteria YAML is **not** the analytical framework for this path.

## Day 1 outputs

| Artifact | Path |
|----------|------|
| Corpus verification report | `reports/corpus_verification_day1.md` |
| Candidate source inventory | `data/corpus_candidates_day1.csv` |

## Regenerate

Day 1 verification is manual/source-audit based. Re-run counts from official URLs
listed in the CSV before field work.

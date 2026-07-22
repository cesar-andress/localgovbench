# Release readiness — LocalGovBench v0.2.0

**Date:** 2026-07-23  
**Tag / GitHub release / Zenodo publish:** **not performed** in this task

## Documentation audited

Yes — see [`public_documentation_audit_v0.2.0.md`](public_documentation_audit_v0.2.0.md).

## Active files updated

- Root `README.md` (12-point visitor guide)
- `CITATION.cff`, `pyproject.toml`, `CHANGELOG.md`, `CONTRIBUTING.md`
- `docs/releases/public_positioning_v0.2.0.md` (frozen positioning)
- Zenodo + GitHub drafts, manifest, readiness

## Legacy files labelled

Yes — benchmark specification, demo walkthrough, validation package, GRB-related docs, examples, data/benchmark, citation/reproducibility guides, etc. Banners state retention reason, replacement path, and **do not use as current analytical specification**.

## Metadata updated

| Item | Status |
|------|--------|
| `CITATION.cff` version 0.2.0 + DF abstract | Updated |
| Historical DOI 10.5281/zenodo.20543779 | Preserved as v0.1.0 only |
| New Zenodo version DOI | **Not set** (correct) |
| `date-released` | **Unset** until publish |
| Concept DOI | **USER CONFIRMATION** — not verified in-repo |
| Companion paper DOI / venue | **USER CONFIRMATION** |
| Communities on Zenodo | **USER CONFIRMATION** |
| Archive breadth (full tree vs DF-focused) | **USER CONFIRMATION** |
| Root `.zenodo.json` / `codemeta.json` | Absent; drafts under `docs/releases/` |

## Tests executed

See preparation run log (local):

- Phase 1 affordance tests  
- Phase 2 coding tests  
- Active-documentation claim validation  
- Draft Zenodo JSON parse  
- CITATION.cff YAML parse  

## Validators

| Validator | Result |
|-----------|--------|
| `pytest -m "not integration"` | **200 passed**, 2 deselected |
| Active-documentation claim tests | Passed |
| `cffconvert --validate` (CFF 1.2.0) | **Valid** (after removing invalid `related-identifiers`; relations live in Zenodo draft) |
| Zenodo draft JSON parse | Passed |
| Online Zenodo API / DOI minting | **Skipped** — intentionally not publishing |
| Offline Codemeta validator | **Skipped** — no root `codemeta.json` |
| GitHub About description update | **Skipped** — remote UI; requires user |

## Unresolved metadata / confirmations

1. Publication date for v0.2.0  
2. Whether a Zenodo **concept DOI** exists and should be listed  
3. Companion manuscript DOI / journal (if any)  
4. Zenodo communities  
5. Exact Zenodo file set (full repo vs affordance-focused subset)  
6. Confirmation that author/affiliation/ORCID/email remain as in `docs/author_identity.md` (already used; confirm no funder/grant to add)  
7. GitHub repository About / topics text  

## Concept DOI status

**Unverified.** No repository evidence confirms a concept DOI distinct from `10.5281/zenodo.20543779`. Flagged for user confirmation; not invented.

## Proposed archive content / exclusions

See [`release_manifest_v0.2.0.md`](release_manifest_v0.2.0.md).

## Risks

- Remote GitHub description may still advertise readiness if not updated manually  
- Mixing GRB outputs with DF coding if consumers ignore LEGACY banners  
- Publishing before human coding completes (mitigated by explicit non-claims)  

## GitHub tagging safe?

**Not yet** — wait for user metadata confirmation and explicit tag decision.

## GitHub release publication safe?

**Not yet** — drafts only; no tag.

## Zenodo publication safe?

**Not yet** — no tag, no version DOI, draft metadata only. Do not edit the historical v0.1.0 Zenodo record.

---

## Final status

**B. Ready after user confirms metadata.**

Rationale: public positioning, legacy labelling, and draft release packs are in place; formal tag / GitHub / Zenodo still require user confirmation of the metadata checklist above and an explicit publish decision.

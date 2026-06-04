# LocalGovBench v0.1.0 — Pre-release checklist

Use this checklist before publishing the repository on **GitHub** and depositing on **Zenodo**. Mark each item `[x]` when complete.

Related documents: [artifact_description.md](artifact_description.md), [reproducibility.md](reproducibility.md), [zenodo_release.md](zenodo_release.md).

---

## README completeness

- [ ] **Project purpose** stated (local/on-premise LLM governance in European public sector)
- [ ] **Version v0.1.0** visible at top of [README.md](../README.md)
- [ ] **Empirical validation pending** stated explicitly
- [ ] Links to artifact description, reproducibility guide, and this checklist
- [ ] Quick start commands present and tested
- [ ] Scope tables (included / excluded) accurate
- [ ] GIQ paper relation described without bundling manuscript
- [ ] Ethical and legal disclaimer present

---

## License

- [ ] [LICENSE](../LICENSE) file present (MIT)
- [ ] License badge in README
- [ ] `CITATION.cff` `license: MIT` matches repository

---

## Citation metadata

- [ ] [CITATION.cff](../CITATION.cff) `title: LocalGovBench`
- [ ] `version: 0.1.0` aligned with `pyproject.toml`
- [x] Citation message: *"If you use LocalGovBench, please cite this research artifact."*
- [x] Zenodo DOI `10.5281/zenodo.20543779` in `CITATION.cff` and README
- [x] Repository URL `https://github.com/cesar-andress/localgovbench`
- [x] Author identity standardized — **César Andrés**, ORCID `0009-0001-8968-3404`, `cesar.andress@ucjc.edu` (see [author_identity.md](author_identity.md))
- [ ] Companion paper DOI added when published (optional `related-identifiers`)

---

## Synthetic data labeling

- [ ] `examples/example_assessment.yaml` contains `synthetic: true`
- [ ] `examples/README.md` warns that bundled scores are synthetic
- [ ] `data/README.md` states no real municipal data in v0.1.0
- [ ] GRB examples and `examples/grb/inter_rater/` marked synthetic in metadata/YAML
- [ ] `validation/ratings/` and `validation/benchmark_cases/` documented as synthetic pilots
- [ ] Generated CSV/MD under `results/` and `reports/` reproducible from scripts (not hand-edited secrets)

---

## No personal data

- [ ] No names, emails, or citizen identifiers in committed files
- [ ] No procurement documents with supplier PII
- [ ] `.env` and credentials excluded via `.gitignore`
- [ ] `data/raw/` and `data/processed/` contain only `.gitkeep` or anonymised templates

---

## No manuscript drafts

- [ ] No PDF, LaTeX, or Word manuscript in repository
- [ ] No `paper/`, `manuscript/`, or `submission/` directories with drafts
- [ ] GIQ positioning in `docs/manuscript_positioning.md` is descriptive only (no full paper)

---

## No reviewer correspondence

- [ ] No peer-review reports, rebuttals, or editorial letters
- [ ] No anonymous review files or decision letters

---

## Reproducible commands

- [ ] [docs/reproducibility.md](reproducibility.md) lists exact install and run commands
- [ ] All commands succeed on a clean Python 3.11+ environment from tagged commit
- [ ] GRB scripts documented separately from LocalGovBench v0.1 validation scripts
- [ ] Ollama prototype documented as optional (local LLM required)

---

## Tests passing

- [ ] `pip install -e ".[dev]"` succeeds
- [ ] `pytest -m "not integration"` — all unit tests pass (no Ollama required)
- [ ] `python scripts/validate_repository.py` — required paths OK
- [ ] No changes to frozen scoring formulas, indicators, or validation metric implementations in this release prep commit

---

## Zenodo metadata

- [ ] Upload type: **Software**
- [ ] Title matches `CITATION.cff` (*LocalGovBench*)
- [ ] Version **0.1.0**
- [ ] Description/abstract aligned with [artifact_description.md](artifact_description.md)
- [ ] Keywords: AI governance, public sector, EU, LLM, benchmark, reproducibility
- [ ] License: MIT
- [ ] GitHub–Zenodo integration configured (or manual upload of tag archive)
- [ ] Related identifier for companion paper when available

---

## Version tag

- [ ] Working tree clean on release commit
- [ ] Annotated tag created: `git tag -a v0.1.0 -m "LocalGovBench v0.1.0 pre-release"`
- [ ] Tag pushed to GitHub: `git push origin v0.1.0`
- [ ] GitHub Release created from tag with release notes (see [CHANGELOG.md](../CHANGELOG.md))

---

## Archive checksum

Record checksums for the **exact** archive cited in publications.

### GitHub source archive (example)

```bash
# After downloading GitHub-generated Source code (zip) for tag v0.1.0:
sha256sum localgovbench-0.1.0.zip
```

### Git checkout archive (example)

```bash
git archive --format=tar.gz --prefix=localgovbench-0.1.0/ v0.1.0 \
  | tee localgovbench-0.1.0.tar.gz | sha256sum
```

- [ ] SHA-256 checksum recorded in GitHub Release body
- [ ] Same checksum (or Zenodo file hash) noted in Zenodo record description
- [ ] Optional: add checksum line to `CHANGELOG.md` under v0.1.0 release notes after deposit

**Placeholder (fill at release):**

| Archive | SHA-256 |
|---------|---------|
| Git tag `v0.1.0` tarball | `TBD` |
| Zenodo record file | `TBD` |

---

## Post-deposit updates

- [x] Replace placeholder DOI in `CITATION.cff` with `10.5281/zenodo.20543779`
- [x] Update README citation section with Zenodo DOI and [citation.md](citation.md)
- [x] Zenodo DOI badge in README

---

*LocalGovBench v0.1.0 pre-release checklist — research artifact only*

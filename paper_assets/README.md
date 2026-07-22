# Paper assets (Disclosure Functions v1)

Reproducible manuscript ingredients generated from repository artefacts.

**Does not write Results. Does not invent findings.**

```
paper_assets/
  paper_asset_manifest.md
  tables/           # T01–T13 (CSV + MD + TeX)
  figures/          # F01–F08 (caption, placeholder, script, meta)
  appendices/       # wrappers to docs/supplements
  methods_assets/   # Methods drafting pointers
  latex/            # collected includes
  scripts/          # generators
```

```bash
python3.12 paper_assets/scripts/generate_all_paper_assets.py
python3.12 paper_assets/scripts/make_F01_corpus_record_counts.py
python3.12 paper_assets/scripts/make_F02_inventory_field_counts.py
python3.12 paper_assets/scripts/make_F03_disclosure_functions_tiers.py
python3.12 paper_assets/scripts/make_F04_coding_universe_grid.py
```

See `paper_asset_manifest.md` for generation order and future inputs.

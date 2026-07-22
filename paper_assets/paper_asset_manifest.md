# Paper asset manifest

**Construct:** Disclosure Functions v1 / schema disclosure affordance  
**Generator:** `paper_assets/scripts/generate_all_paper_assets.py`  
**Rule:** Do **not** invent Results. Placeholders stay empty until real inputs exist.

## Dependencies

| Dependency | Role |
|------------|------|
| Python ≥ 3.11 | Generator + figure scripts |
| PyYAML | Function catalogue |
| matplotlib | Figure scripts F01–F04 |
| Frozen corpus lock + inventory | Methods tables/figures |
| Source registry CSV | Corpus metadata columns |
| Coding templates / pilot manifest | Unit design tables/figures |
| Completed human coding (future) | T09–T11, F05–F06 |
| Realization stage outputs (future) | T12–T13, F07–F08 |

Install (from repo root):

```bash
pip install -e ".[dev]"
```

## Generation order

1. Ensure Phase 1–2 freezes exist (`affordance/locks`, `outputs`, `coding/templates`).  
2. Run:

   ```bash
   python3.12 paper_assets/scripts/generate_all_paper_assets.py
   ```

3. Generate auto figures:

   ```bash
   python3.12 paper_assets/scripts/make_F01_corpus_record_counts.py
   python3.12 paper_assets/scripts/make_F02_inventory_field_counts.py
   python3.12 paper_assets/scripts/make_F03_disclosure_functions_tiers.py
   python3.12 paper_assets/scripts/make_F04_coding_universe_grid.py
   ```

4. Leave F05–F08 / T09–T13 placeholders until study inputs exist.  
5. Do **not** run legacy shortfall figure pipelines as DF Results.

## Files generated automatically (methods / descriptive)

### Tables (CSV + Markdown + LaTeX)

| ID | Content |
|----|---------|
| T01 | Corpus composition |
| T02 | Object layers |
| T03 | Disclosure Functions catalogue |
| T04 | Schema inventory summary |
| T05 | Full coding universe (55) |
| T06 | Pilot unit selection (33) |
| T07 | Coding label enumerations |
| T08 | Field–function candidate summary |

### Figures (scripts + placeholders; PNG when scripts succeed)

| ID | Content |
|----|---------|
| F01 | Corpus record counts |
| F02 | Inventory field counts |
| F03 | Function tier overview |
| F04 | Coding universe / pilot grid |

### Other

- `appendices/` wrappers → `docs/supplements/`  
- `methods_assets/` checklists  
- `latex/tables/*.tex`, `latex/figures/*.tex` include stubs  

## Files requiring future inputs (manual / empirical interpretation)

| ID | Required future input | Manual interpretation? |
|----|----------------------|-------------------------|
| T09 schema affordance matrix | Completed coding + adjudication + Phase 3 matrix | Yes — Methods/Results framing of support levels |
| T10 coder disagreements | Dual completed sheets + disagreement export | Yes — qualitative disagreement themes optional |
| T11 IRR summary | IRR computation per plan | Yes — coefficient choice/reporting |
| T12 realization rates | Future realization measurement | Yes |
| T13 affordance–realization gap | T09 + T12 | Yes |
| F05–F08 | Same as related tables | Yes |

## Required future inputs (checklist)

- [ ] `pilot_round_01_coder_A_completed.csv` / `_B_completed.csv` (human)  
- [ ] Disagreement export + adjudication completed sheet  
- [ ] Phase 3 affordance matrix for cited `experiment_id`  
- [ ] IRR statistics computed per `irr_analysis_plan_v1.md`  
- [ ] Realization inputs filled (not templates alone)  
- [ ] Gap analysis notebook/script (not yet a DF Results claim)

## Explicitly out of scope for this asset pack

Legacy public-satisfiability / shortfall outputs under
`pilot_public_satisfiability/outputs/` and `figures/` are **not**
copied into `paper_assets/` as Disclosure Functions Results.
They belong to a different construct (v0.1 ceiling/shortfall pilot).

## Cross references

- Supplements A–J: `docs/supplements/`  
- Affordance package: `localgovbench_measurement_validation/affordance/`  
- Software citation: `CITATION.cff` / Supplement I  

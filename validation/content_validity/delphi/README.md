# Delphi content validity — Round 1 workflow

Expert panel review of LocalGovBench v0.1 criterion definitions for **programme-level governance readiness** assessment on **confidential programme dossiers**. Public-document observability is forbidden as primary evidence for this round.

## Files

| File | Purpose | Git |
|------|---------|-----|
| `delphi_round1_instrument.yaml` | Round 1 instrument (25 criteria, scales, framing) | tracked |
| `panel_roster_template.yaml` | Pseudonymous panel slot template | tracked |
| `expert_response_template.yaml` | Single-expert response schema reference | tracked |
| `responses/exp_*_round1.yaml` | Completed expert ratings | **gitignored** |
| `responses/README.md` | Local storage note | tracked |
| `delphi_round1_report.md` | Analysis report (generated) | tracked after analysis |

## Workflow

1. **Generate instrument** (if criteria change):
   ```bash
   python3.12 scripts/generate_delphi_round1_instrument.py
   python3.12 scripts/validate_delphi_round1_instrument.py
   ```

2. **Generate blank response templates** (default: `exp_001` … `exp_012`):
   ```bash
   python3.12 scripts/generate_expert_response_templates.py
   ```

3. **Distribute** `delphi_round1_instrument.yaml` and blank response files to panel members via secure channel. Maintain real identities only in `panel_roster.yaml` **outside** this repository.

4. **Validate responses** before analysis:
   ```bash
   python3.12 scripts/validate_delphi_responses.py
   ```

5. **Analyze Round 1**:
   ```bash
   python3.12 scripts/analyze_delphi_round1.py
   ```

   Exports:
   - `exports/validation/content_validity_round1_summary.json`
   - `exports/validation/content_validity_round1_items.csv`
   - `delphi_round1_report.md`

## Response fields (per criterion)

- `relevance_1_5` — 1 (not relevant) to 5 (highly relevant); I-CVI uses proportion rating ≥ 4
- `clarity_1_5` — 1 (very unclear) to 5 (very clear); I-CVI uses proportion rating ≥ 4
- `essential_yes_no` — Lawshe essentiality (boolean)
- `suggested_revision` — optional wording change (no PII)
- `comment` — optional free text (no PII)

## Thresholds

| Metric | Threshold |
|--------|-----------|
| I-CVI (relevance, clarity) | ≥ 0.78 |
| S-CVI/Ave (relevance, clarity) | ≥ 0.90 |
| Lawshe CVR | panel-size critical value (Lawshe 1975) |

## Confidentiality

- Response YAML files under `responses/` are marked `confidential: true` and excluded from git.
- Use pseudonymous IDs only (`exp_001`, …).
- Do not record names, emails, employers, or municipality identifiers in response files.

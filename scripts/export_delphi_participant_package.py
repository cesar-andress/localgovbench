#!/usr/bin/env python3
"""Export Delphi Round 1 participant package from frozen LocalGovBench v0.1 criteria."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_delphi_round1_instrument import (  # noqa: E402
    STUDY_FRAMING,
    build_criteria,
    load_traceability,
)
from localgovbench.framework.dimensions import FRAMEWORK_VERSION, GOVERNANCE_DIMENSIONS  # noqa: E402

OUTPUT_DIR = ROOT / "exports" / "delphi_round1"
VALIDATION_JSON = ROOT / "exports" / "validation" / "delphi_package_validation.json"

CATALOG_COLUMNS = [
    "criterion_id",
    "dimension_id",
    "dimension_name",
    "assessment_question",
    "criterion_description",
    "documentation_hint",
    "risk_if_missing",
    "traceability_references",
    "relevance_1_5",
    "clarity_1_5",
    "essential_yes_no",
    "suggested_revision",
    "comment",
]

RELEVANCE_LABELS = {
    1: "Not relevant",
    2: "Somewhat relevant",
    3: "Moderately relevant",
    4: "Relevant",
    5: "Highly relevant",
}

CLARITY_LABELS = {
    1: "Very unclear",
    2: "Unclear",
    3: "Moderately clear",
    4: "Clear",
    5: "Very clear",
}


def format_traceability(refs: list[dict[str, str]]) -> str:
    parts: list[str] = []
    for ref in refs:
        parts.append(
            f"{ref['source_framework']} / {ref['source_concept']}: "
            f"{ref['governance_requirement']} — {ref['rationale']}"
        )
    return " | ".join(parts)


def build_catalog_rows(criteria: list[dict]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in criteria:
        rows.append(
            {
                "criterion_id": item["criterion_id"],
                "dimension_id": item["dimension_id"],
                "dimension_name": item["dimension_name"],
                "assessment_question": item["assessment_question"],
                "criterion_description": item["criterion_statement"],
                "documentation_hint": item["documentation_hint"],
                "risk_if_missing": item["risk_if_missing"],
                "traceability_references": format_traceability(item["traceability_references"]),
                "relevance_1_5": "",
                "clarity_1_5": "",
                "essential_yes_no": "",
                "suggested_revision": "",
                "comment": "",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CATALOG_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _xlsx_cell(ref: str, value: str, *, style: str = "s") -> str:
    text = escape(value)
    return f'<c r="{ref}" t="inlineStr"><is><t>{text}</t></is></c>'


def write_xlsx(path: Path, rows: list[dict[str, str]]) -> None:
    """Write a minimal Office Open XML workbook (stdlib only)."""
    sheet_rows: list[str] = []
    header_cells = "".join(
        _xlsx_cell(f"{chr(65 + idx)}1", col) for idx, col in enumerate(CATALOG_COLUMNS)
    )
    sheet_rows.append(f"<row r=\"1\">{header_cells}</row>")

    for row_idx, row in enumerate(rows, start=2):
        cells = "".join(
            _xlsx_cell(
                f"{chr(65 + col_idx)}{row_idx}",
                row[col],
            )
            for col_idx, col in enumerate(CATALOG_COLUMNS)
        )
        sheet_rows.append(f'<row r="{row_idx}">{cells}</row>')

    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f"<sheetData>{''.join(sheet_rows)}</sheetData></worksheet>"
    )
    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="criterion_catalog" sheetId="1" r:id="rId1"/></sheets></workbook>'
    )
    rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", rels_xml)
        archive.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def render_consent_information() -> str:
    return f"""# Delphi Round 1 — expert panel consent information

**Study:** LocalGovBench v0.1 instrument content validity  
**Instrument version:** v0.1.0 (framework {FRAMEWORK_VERSION})  
**Round:** 1  
**Generated:** {date.today().isoformat()}

## Purpose

You are invited to review criterion definitions for **Programme-Level Governance Readiness**
assessment of **bounded municipal AI/LLM programmes** using **confidential programme dossiers**
and **evidence-gated assessor review**.

This Round 1 Delphi study evaluates **content validity only**. You will **not** score any
municipality, review real dossiers, or assign maturity levels in this round.

## What participation involves

- Review **25 criteria** across **5 dimensions**.
- Rate each criterion for **relevance** (1–5), **clarity** (1–5), and **essentiality** (yes/no).
- Optionally suggest wording revisions and provide comments.
- Estimated time: **45–60 minutes** for Round 1.

## Voluntary participation

Participation is voluntary. You may skip any item or withdraw without penalty.

## Confidentiality

- Do **not** include personal data, employer identifiers, or municipality names in free-text fields.
- Responses are stored under pseudonymous expert IDs.
- Aggregated results may appear in a peer-reviewed publication; individual responses will not be
  attributed without separate written consent.

## Data protection

Responses are processed for research purposes under applicable data protection law. Contact the
principal investigator named in the invitation letter for questions about retention, access, or
erasure.

## Scope limits

This study does **not** request:

- public AI registers or transparency portals as assessment evidence;
- public-document observability analysis;
- legal compliance certification or municipal ranking.

## Consent statement

By returning a completed response, you confirm that:

1. You have read this information sheet.
2. You understand the purpose and limits of Round 1.
3. You agree to participate voluntarily.
4. You will not include identifying information in free-text responses.

---

*LocalGovBench instrument-validation study — Delphi Round 1 consent information*
"""


def render_participant_instructions() -> str:
    return f"""# Delphi Round 1 — participant instructions

**Instrument:** LocalGovBench v0.1  
**Framework version:** {FRAMEWORK_VERSION}  
**Round:** 1  
**Generated:** {date.today().isoformat()}

## Study framing

{STUDY_FRAMING["instruction"]}

**Construct under review:** {STUDY_FRAMING["construct"]}  
**Evidence layer for the eventual field study:** {STUDY_FRAMING["evidence_layer"]}  
**Not in scope for this round:** {STUDY_FRAMING["forbidden_basis"]}

## Your task

For each of the **25 criteria**, provide:

| Field | Scale / format | Guidance |
|-------|----------------|----------|
| **Relevance** | 1–5 | How relevant is this criterion for assessing programme-level governance readiness from a confidential dossier? |
| **Clarity** | 1–5 | How clear and operable is the criterion wording for independent assessors? |
| **Essentiality** | Yes / No | Lawshe essentiality: is the item **essential** for the instrument to comprehensively represent the construct? |
| **Suggested revision** | Free text (optional) | Proposed wording change only; no PII. |
| **Comment** | Free text (optional) | Rationale, overlap concerns, missing elements; no PII. |

### Relevance scale (1–5)

| Score | Label |
|-------|-------|
| 1 | {RELEVANCE_LABELS[1]} |
| 2 | {RELEVANCE_LABELS[2]} |
| 3 | {RELEVANCE_LABELS[3]} |
| 4 | {RELEVANCE_LABELS[4]} |
| 5 | {RELEVANCE_LABELS[5]} |

### Clarity scale (1–5)

| Score | Label |
|-------|-------|
| 1 | {CLARITY_LABELS[1]} |
| 2 | {CLARITY_LABELS[2]} |
| 3 | {CLARITY_LABELS[3]} |
| 4 | {CLARITY_LABELS[4]} |
| 5 | {CLARITY_LABELS[5]} |

### Essentiality (Lawshe)

Answer **Yes** if the item should remain in the instrument for comprehensive coverage; **No** if
the construct could be represented adequately without it.

## How to respond

You may complete either:

1. **`criterion_catalog.xlsx`** or **`criterion_catalog.csv`** — fill the response columns; or
2. **`participant_questionnaire.md`** — for reference; return ratings via the spreadsheet if preferred.

Return completed files through the **secure channel** indicated in your invitation email.

## Important rules

- Rate **criterion definitions**, not any specific municipality or vendor.
- Do **not** infer legal compliance from relevance ratings.
- Flag redundant or overlapping criteria in comments — Round 2 may revise failed items.
- If a criterion is outside your expertise, rate to the best of your knowledge and note uncertainty
  in the comment field.

## Analysis thresholds (for transparency)

| Metric | Threshold |
|--------|-----------|
| I-CVI (relevance, clarity) | ≥ 0.78 (proportion rating 4–5) |
| S-CVI/Ave | ≥ 0.90 target |
| Lawshe CVR | panel-size critical value |

---

*LocalGovBench instrument-validation study — Delphi Round 1 participant instructions*
"""


def render_participant_questionnaire(criteria: list[dict]) -> str:
    lines: list[str] = [
        "# LocalGovBench v0.1 — Delphi Round 1 participant questionnaire",
        "",
        f"**Framework version:** {FRAMEWORK_VERSION}  ",
        f"**Round:** 1  ",
        f"**Generated:** {date.today().isoformat()}  ",
        f"**Criteria:** {len(criteria)}  ",
        "",
        "Complete one block per criterion. See `participant_instructions.md` for scales.",
        "",
        "---",
        "",
    ]

    current_dimension: str | None = None
    item_no = 0
    for item in criteria:
        if item["dimension_id"] != current_dimension:
            current_dimension = item["dimension_id"]
            lines.extend(
                [
                    f"## {item['dimension_name']} (`{item['dimension_id']}`)",
                    "",
                ]
            )

        item_no += 1
        lines.extend(
            [
                f"### {item_no}. `{item['criterion_id']}`",
                "",
                f"**Assessment question:** {item['assessment_question']}",
                "",
                f"**Criterion description:** {item['criterion_statement']}",
                "",
                "**Documentation hint (for field study context only; not rated in Round 1):**  ",
                f"{item['documentation_hint']}",
                "",
                "**Risk if missing (indicative):**  ",
                f"{item['risk_if_missing']}",
                "",
                "**Traceability references:**",
                "",
            ]
        )
        if item["traceability_references"]:
            for ref in item["traceability_references"]:
                lines.append(
                    f"- **{ref['source_framework']}** — {ref['source_concept']}: "
                    f"{ref['governance_requirement']}. {ref['rationale']}"
                )
        else:
            lines.append("- *(none mapped)*")
        lines.extend(
            [
                "",
                "**Your ratings**",
                "",
                "| Field | Your response |",
                "|-------|---------------|",
                "| Relevance (1–5) | |",
                "| Clarity (1–5) | |",
                "| Essential? (Yes/No) | |",
                "",
                "**Suggested revision (optional):**",
                "",
                "",
                "**Comment (optional):**",
                "",
                "",
                "---",
                "",
            ]
        )

    lines.append(
        "*End of questionnaire — LocalGovBench v0.1 Delphi Round 1 "
        "(programme dossier / evidence-gated validation study)*"
    )
    return "\n".join(lines)


def _markdown_to_html(md_text: str) -> str:
    import markdown

    body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    return (
        "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
        "<style>body{font-family:Helvetica,Arial,sans-serif;font-size:11pt;"
        "line-height:1.45;margin:2.2cm;} h1,h2,h3{page-break-after:avoid;}"
        "table{border-collapse:collapse;width:100%;} th,td{border:1px solid #ccc;"
        "padding:4px;vertical-align:top;} hr{margin:1.2em 0;}</style></head>"
        f"<body>{body}</body></html>"
    )


def try_write_pdf(md_path: Path, pdf_path: Path) -> tuple[bool, str]:
    pandoc = shutil.which("pandoc")
    if pandoc:
        result = subprocess.run(
            [
                pandoc,
                str(md_path),
                "-o",
                str(pdf_path),
                "--pdf-engine=pdflatex",
                "-V",
                "geometry:margin=2.5cm",
                "-V",
                "fontsize=11pt",
            ],
            capture_output=True,
            text=True,
            check=False,
            cwd=ROOT,
        )
        if result.returncode != 0:
            result = subprocess.run(
                [pandoc, str(md_path), "-o", str(pdf_path)],
                capture_output=True,
                text=True,
                check=False,
                cwd=ROOT,
            )
        if result.returncode == 0 and pdf_path.is_file():
            return True, "generated via pandoc"

    wkhtml = shutil.which("wkhtmltopdf")
    if not wkhtml:
        return False, "pandoc and wkhtmltopdf not available on PATH"

    html_path = pdf_path.with_suffix(".html")
    html_path.write_text(_markdown_to_html(md_path.read_text(encoding="utf-8")), encoding="utf-8")
    result = subprocess.run(
        [wkhtml, "--quiet", str(html_path), str(pdf_path)],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    html_path.unlink(missing_ok=True)
    if result.returncode != 0 or not pdf_path.is_file():
        detail = (result.stderr or result.stdout or "wkhtmltopdf failed").strip()
        return False, detail[:500]
    return True, "generated via wkhtmltopdf"


def write_package_manifest(
    path: Path,
    *,
    criteria_count: int,
    pdf_written: bool,
    pdf_note: str,
) -> None:
    manifest = {
        "package": "delphi_round1_participant",
        "generated_on": date.today().isoformat(),
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "instrument_version": "v0.1.0",
        "framework_version": FRAMEWORK_VERSION,
        "round": 1,
        "criteria_count": criteria_count,
        "dimensions_count": len(GOVERNANCE_DIMENSIONS),
        "source_of_truth": [
            "localgovbench/framework/dimensions.py",
            "data/traceability/indicator_mapping.csv",
        ],
        "files": [
            "participant_questionnaire.md",
            "participant_questionnaire.pdf",
            "criterion_catalog.csv",
            "criterion_catalog.xlsx",
            "participant_instructions.md",
            "consent_information.md",
        ],
        "pdf_status": {"written": pdf_written, "note": pdf_note},
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    traceability = load_traceability()
    criteria, missing_trace = build_criteria(traceability)
    if missing_trace:
        print("ERROR: missing traceability mappings:", file=sys.stderr)
        for cid in missing_trace:
            print(f"  - {cid}", file=sys.stderr)
        return 1

    rows = build_catalog_rows(criteria)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)

    files_written: list[str] = []

    questionnaire_md = OUTPUT_DIR / "participant_questionnaire.md"
    questionnaire_md.write_text(render_participant_questionnaire(criteria), encoding="utf-8")
    files_written.append(questionnaire_md.name)

    instructions = OUTPUT_DIR / "participant_instructions.md"
    instructions.write_text(render_participant_instructions(), encoding="utf-8")
    files_written.append(instructions.name)

    consent = OUTPUT_DIR / "consent_information.md"
    consent.write_text(render_consent_information(), encoding="utf-8")
    files_written.append(consent.name)

    catalog_csv = OUTPUT_DIR / "criterion_catalog.csv"
    write_csv(catalog_csv, rows)
    files_written.append(catalog_csv.name)

    catalog_xlsx = OUTPUT_DIR / "criterion_catalog.xlsx"
    write_xlsx(catalog_xlsx, rows)
    files_written.append(catalog_xlsx.name)

    pdf_path = OUTPUT_DIR / "participant_questionnaire.pdf"
    pdf_ok, pdf_note = try_write_pdf(questionnaire_md, pdf_path)
    if pdf_ok:
        files_written.append(pdf_path.name)
    else:
        pdf_note = f"PDF not generated: {pdf_note}"

    manifest_path = OUTPUT_DIR / "package_manifest.json"
    write_package_manifest(
        manifest_path,
        criteria_count=len(criteria),
        pdf_written=pdf_ok,
        pdf_note=pdf_note,
    )

    print(f"Wrote Delphi Round 1 participant package → {OUTPUT_DIR.relative_to(ROOT)}/")
    for name in sorted(files_written):
        print(f"  - {name}")
    if not pdf_ok:
        print(f"  - participant_questionnaire.pdf (skipped: {pdf_note})")
    print(f"  - package_manifest.json")
    print(f"  Criteria: {len(criteria)}")
    print(f"  Dimensions: {len(GOVERNANCE_DIMENSIONS)}")
    print("\nRun: python3.12 scripts/validate_delphi_package.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

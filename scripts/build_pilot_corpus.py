#!/usr/bin/env python3
"""Build expanded programme corpus from official public AI inventories (5 sources)."""

from __future__ import annotations

import csv
import io
import json
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench_measurement_validation.pilot_public_satisfiability.pilot_paths import (  # noqa: E402
    DATA_RECORDS,
    SOURCE_REGISTRY,
)
from localgovbench_measurement_validation.pilot_public_satisfiability.source_registry import (  # noqa: E402
    COLLECTION_DATE,
    EXPANDED_SOURCES,
)

US_CSV_URL = EXPANDED_SOURCES[0]["url"]
CA_CSV_URL = EXPANDED_SOURCES[1]["url"]
NL_CSV_URL = EXPANDED_SOURCES[2]["url"]
PSTW_CSV_URL = EXPANDED_SOURCES[3]["url"]
UK_SEARCH_URL = EXPANDED_SOURCES[4]["url"]


def fetch_bytes(url: str, timeout: int = 120) -> bytes:
    return urllib.request.urlopen(url, timeout=timeout).read()


def fetch_csv(url: str, delimiter: str = ",") -> list[dict[str, str]]:
    raw = fetch_bytes(url)
    text = raw.decode("utf-8-sig", errors="replace")
    return list(csv.DictReader(io.StringIO(text), delimiter=delimiter))


def fetch_csv_latin1(url: str, delimiter: str = ";") -> list[dict[str, str]]:
    raw = fetch_bytes(url)
    text = raw.decode("latin-1", errors="replace")
    return list(csv.DictReader(io.StringIO(text), delimiter=delimiter))


def fetch_uk_atrs() -> list[dict]:
    results: list[dict] = []
    start = 0
    batch = 100
    while True:
        params = urllib.parse.urlencode(
            {
                "filter_document_type": "algorithmic_transparency_record",
                "count": batch,
                "start": start,
            }
        )
        url = f"https://www.gov.uk/api/search.json?{params}"
        payload = json.loads(fetch_bytes(url, timeout=60))
        batch_results = payload.get("results", [])
        if not batch_results:
            break
        results.extend(batch_results)
        if len(results) >= payload.get("total", len(results)):
            break
        start += batch
    return results


def normalize_us(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        rid = row.get("id") or row.get("use_case_name") or ""
        out.append(
            {
                "record_id": f"us-omb-2025-{rid}",
                "jurisdiction": "United States (federal)",
                "source_name": "US-OMB-2025",
                "source_url": US_CSV_URL,
                "programme_title": (row.get("use_case_name") or "").strip(),
                "programme_description": " | ".join(
                    p
                    for p in [
                        (row.get("problem_solved") or "").strip(),
                        (row.get("benefits") or "").strip(),
                        (row.get("system_outputs") or "").strip(),
                    ]
                    if p
                ),
                "agency_or_owner": (row.get("agency_name") or row.get("agency") or "").strip(),
                "raw_fields_json": json.dumps(row, ensure_ascii=False),
                "collection_date": COLLECTION_DATE,
            }
        )
    return out


def normalize_ca(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        rid = row.get("ai_register_id") or row.get("name_ai_system_en") or ""
        desc_en = (row.get("description_ai_system_en") or "").strip()
        desc_fr = (row.get("description_ai_system_fr") or "").strip()
        out.append(
            {
                "record_id": f"ca-gc-ai-{rid}",
                "jurisdiction": "Canada (federal)",
                "source_name": "CA-GC-AI-REG",
                "source_url": CA_CSV_URL,
                "programme_title": (row.get("name_ai_system_en") or row.get("name_ai_system_fr") or "").strip(),
                "programme_description": desc_en or desc_fr,
                "agency_or_owner": (row.get("government_organization") or "").strip(),
                "raw_fields_json": json.dumps(row, ensure_ascii=False),
                "collection_date": COLLECTION_DATE,
            }
        )
    return out


def normalize_nl(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        rid = (row.get("source_id") or row.get("url") or row.get("name") or "").strip()
        out.append(
            {
                "record_id": f"nl-algo-{rid}",
                "jurisdiction": "Netherlands (national + local bodies)",
                "source_name": "NL-ALGO-REG",
                "source_url": NL_CSV_URL,
                "programme_title": (row.get("name") or "").strip(),
                "programme_description": (row.get("description_short") or row.get("goal") or "").strip(),
                "agency_or_owner": (row.get("organization") or "").strip(),
                "raw_fields_json": json.dumps(row, ensure_ascii=False),
                "collection_date": COLLECTION_DATE,
            }
        )
    return out


def normalize_pstw(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    ai_rows = [
        r
        for r in rows
        if (r.get("Primary Technology") or "").strip() == "Artificial Intelligence"
    ]
    out: list[dict[str, str]] = []
    for row in ai_rows:
        rid = (row.get("PSTW ID") or row.get("Name") or "").strip()
        out.append(
            {
                "record_id": f"eu-pstw-{rid}",
                "jurisdiction": row.get("Geographical coverage (country)", "European Union").strip()
                or "European Union (multi-country)",
                "source_name": "EU-PSTW",
                "source_url": PSTW_CSV_URL,
                "programme_title": (row.get("Name") or "").strip(),
                "programme_description": (row.get("Description") or "").strip(),
                "agency_or_owner": (row.get("Responsible organisation") or "").strip(),
                "raw_fields_json": json.dumps(row, ensure_ascii=False),
                "collection_date": COLLECTION_DATE,
            }
        )
    return out


def normalize_uk(rows: list[dict]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        link = (row.get("link") or "").strip()
        rid = link.strip("/").replace("/", "-") or str(row.get("index", ""))
        orgs = row.get("organisations") or []
        org_title = orgs[0].get("title", "") if orgs else ""
        slim = {
            "title": row.get("title", ""),
            "description": row.get("description", ""),
            "link": link,
            "organisation_title": org_title,
            "format": row.get("format", ""),
            "index": row.get("index", ""),
            "public_timestamp": row.get("public_timestamp", ""),
        }
        out.append(
            {
                "record_id": f"uk-atrs-{rid}",
                "jurisdiction": "United Kingdom",
                "source_name": "UK-ATRS",
                "source_url": f"https://www.gov.uk{link}" if link else UK_SEARCH_URL,
                "programme_title": (row.get("title") or "").strip(),
                "programme_description": (row.get("description") or "").strip(),
                "agency_or_owner": org_title.strip(),
                "raw_fields_json": json.dumps(slim, ensure_ascii=False),
                "collection_date": COLLECTION_DATE,
            }
        )
    return out


def write_source_registry(counts: dict[str, int]) -> None:
    fieldnames = [
        "source_id",
        "source_name",
        "jurisdiction",
        "url",
        "access_method",
        "machine_readable",
        "filter_applied",
        "programme_level_unit",
        "overlap_paper2_risk",
        "record_count",
        "collection_date",
    ]
    SOURCE_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with SOURCE_REGISTRY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for src in EXPANDED_SOURCES:
            writer.writerow(
                {
                    **src,
                    "record_count": counts.get(src["source_id"], 0),
                    "collection_date": COLLECTION_DATE,
                }
            )


def main() -> int:
    print("Fetching US OMB 2025 inventory...")
    us_rows = fetch_csv(US_CSV_URL)
    print(f"  {len(us_rows)} records")

    print("Fetching Canada GC AI Register...")
    ca_rows = fetch_csv(CA_CSV_URL)
    print(f"  {len(ca_rows)} records")

    print("Fetching Dutch Algoritmeregister bulk CSV...")
    nl_rows = fetch_csv(NL_CSV_URL)
    print(f"  {len(nl_rows)} records")

    print("Fetching EU PSTW dataset (AI-primary filter)...")
    pstw_all = fetch_csv_latin1(PSTW_CSV_URL)
    pstw_norm = normalize_pstw(pstw_all)
    print(f"  {len(pstw_all)} total PSTW rows; {len(pstw_norm)} AI-primary retained")

    print("Fetching UK ATRS via GOV.UK Search API...")
    uk_raw = fetch_uk_atrs()
    print(f"  {len(uk_raw)} records")

    records = (
        normalize_us(us_rows)
        + normalize_ca(ca_rows)
        + normalize_nl(nl_rows)
        + pstw_norm
        + normalize_uk(uk_raw)
    )

    counts = {
        "US-OMB-2025": len(us_rows),
        "CA-GC-AI-REG": len(ca_rows),
        "NL-ALGO-REG": len(nl_rows),
        "EU-PSTW": len(pstw_norm),
        "UK-ATRS": len(uk_raw),
    }
    write_source_registry(counts)

    fieldnames = [
        "record_id",
        "jurisdiction",
        "source_name",
        "source_url",
        "programme_title",
        "programme_description",
        "agency_or_owner",
        "raw_fields_json",
        "collection_date",
    ]
    DATA_RECORDS.parent.mkdir(parents=True, exist_ok=True)
    with DATA_RECORDS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Wrote {DATA_RECORDS.relative_to(ROOT)} — {len(records)} programme records")
    print(f"Wrote {SOURCE_REGISTRY.relative_to(ROOT)}")
    for src, n in counts.items():
        print(f"  {src}: {n}")

    if len(records) < 300:
        print("WARNING: fewer than 300 records", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

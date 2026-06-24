"""Expanded source registry metadata for validation upgrade."""

from __future__ import annotations

from datetime import date

COLLECTION_DATE = date.today().isoformat()

EXPANDED_SOURCES: list[dict[str, str]] = [
    {
        "source_id": "US-OMB-2025",
        "source_name": "2025 U.S. Federal Agency AI Use Case Inventory (OMB)",
        "jurisdiction": "United States (federal)",
        "url": (
            "https://raw.githubusercontent.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory/"
            "main/Data/2025_individually_reported_AI_use_cases.csv"
        ),
        "access_method": "direct_csv_download",
        "machine_readable": "yes",
        "filter_applied": "none",
        "programme_level_unit": "federal_ai_use_case",
        "overlap_paper2_risk": "low",
    },
    {
        "source_id": "CA-GC-AI-REG",
        "source_name": "Government of Canada AI Register (MVP)",
        "jurisdiction": "Canada (federal)",
        "url": (
            "https://open.canada.ca/data/dataset/fcbc0200-79ba-4fa4-94a6-00e32facea6b/"
            "resource/369f6f34-148a-42ed-b581-8c164e941a89/download/"
            "gc-ai-register-mvp-registre-de-lia-du-gc-pmv-04-26.csv"
        ),
        "access_method": "direct_csv_download",
        "machine_readable": "yes",
        "filter_applied": "none",
        "programme_level_unit": "federal_ai_system",
        "overlap_paper2_risk": "low",
    },
    {
        "source_id": "NL-ALGO-REG",
        "source_name": "Dutch national Algorithm Register (Algoritmeregister)",
        "jurisdiction": "Netherlands (national + local bodies)",
        "url": "https://algoritmes.overheid.nl/api/downloads/ENG?filetype=csv",
        "access_method": "official_api_bulk_csv",
        "machine_readable": "yes",
        "filter_applied": "none",
        "programme_level_unit": "algorithm_description",
        "overlap_paper2_risk": "medium",
    },
    {
        "source_id": "EU-PSTW",
        "source_name": "EU Public Sector Tech Watch (JRC) cases dataset",
        "jurisdiction": "European Union (multi-country)",
        "url": (
            "https://interoperable-europe.ec.europa.eu/sites/default/files/"
            "custom-page/attachment/2026-06/pstw_dataset.csv"
        ),
        "access_method": "direct_csv_download",
        "machine_readable": "yes",
        "filter_applied": "Primary Technology == Artificial Intelligence",
        "programme_level_unit": "public_sector_ai_case",
        "overlap_paper2_risk": "medium",
    },
    {
        "source_id": "UK-ATRS",
        "source_name": "UK Algorithmic Transparency Recording Standard (GOV.UK records)",
        "jurisdiction": "United Kingdom",
        "url": (
            "https://www.gov.uk/api/search.json?"
            "filter_document_type=algorithmic_transparency_record"
        ),
        "access_method": "govuk_search_api_pagination",
        "machine_readable": "yes_partial",
        "filter_applied": "document_type=algorithmic_transparency_record",
        "programme_level_unit": "transparency_record",
        "overlap_paper2_risk": "medium",
    },
]

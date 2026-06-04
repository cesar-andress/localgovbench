"""Synthetic municipality document corpus generator."""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any, Sequence

CORPUS_VERSION = "1.0"
DEFAULT_MUNICIPALITY_COUNT = 50
DEFAULT_SEED = 42

CORPUS_DOCUMENT_TYPES: tuple[str, ...] = (
    "governance_policy",
    "ai_strategy",
    "oversight_procedure",
    "risk_register",
    "procurement_note",
    "architecture_note",
)

MATURITY_TIERS: tuple[str, ...] = ("low", "emerging", "managed")

FICTIONAL_NAMES: tuple[str, ...] = (
    "Nordvale",
    "Estuarywick",
    "Montelake",
    "Riverford",
    "Highmere",
    "Stonehaven",
    "Greenwich Bay",
    "Ashford Vale",
    "Silverbrook",
    "Cedarford",
    "Windmere",
    "Oakridge",
    "Fairmont",
    "Briarcliff",
    "Westholm",
    "Eastbarrow",
    "Summit Dale",
    "Lowfield",
    "Clearwater",
    "Ironwood",
    "Meadowgate",
    "Pinehurst",
    "Redcliff",
    "Bluehaven",
    "Goldmere",
    "Whitecliff",
    "Blackwood",
    "Springvale",
    "Winterford",
    "Autumn Bay",
    "Northgate",
    "Southwick",
    "Centralia",
    "Lakeshore",
    "Hillcrest",
    "Valleyview",
    "Coastmere",
    "Borderwick",
    "Crossfield",
    "Milltown",
    "Bridgeport",
    "Harbourton",
    "Dockside",
    "Marketford",
    "Guildmere",
    "Crafton",
    "Scholarsgate",
    "Library Bay",
    "Archive Vale",
    "Registry Ford",
)

REGIONS: tuple[str, ...] = (
    "Northern Arc Region",
    "Central Estuary Belt",
    "Western Uplands",
    "Southern Coastal Alliance",
    "Inland Metropolitan Ring",
)

USE_CASES: tuple[str, ...] = (
    "internal policy drafting",
    "citizen enquiry triage (advisory only)",
    "procurement specification review",
    "meeting minute summarisation",
    "multilingual intranet search",
)


@dataclass(frozen=True, slots=True)
class MunicipalityRecord:
    """Metadata for one synthetic municipality."""

    municipality_id: str
    display_name: str
    slug: str
    region: str
    population_band: str
    maturity_tier: str
    primary_use_case: str
    service_owner_role: str
    documents: tuple[str, ...]


def generate_municipality_corpus(
    output_dir: Path,
    *,
    count: int = DEFAULT_MUNICIPALITY_COUNT,
    seed: int = DEFAULT_SEED,
) -> dict[str, Any]:
    """
    Generate *count* synthetic municipalities under *output_dir*.

    Layout::

        output_dir/
          metadata.json
          municipalities/<municipality_id>/*.md
    """
    if count < 1:
        raise ValueError("count must be >= 1")
    if count > len(FICTIONAL_NAMES):
        raise ValueError(f"count must be <= {len(FICTIONAL_NAMES)} unique names")

    rng = random.Random(seed)
    output_dir = Path(output_dir)
    municipalities_dir = output_dir / "municipalities"
    municipalities_dir.mkdir(parents=True, exist_ok=True)

    names = rng.sample(list(FICTIONAL_NAMES), count)
    tiers = [rng.choice(MATURITY_TIERS) for _ in range(count)]
    records: list[MunicipalityRecord] = []

    for index, (name, tier) in enumerate(zip(names, tiers, strict=True)):
        municipality_id = f"mun_{index + 1:03d}_{_slugify(name)}"
        slug = _slugify(name)
        population = rng.choice(
            ("15k–40k", "41k–120k", "121k–250k", "251k–450k")
        )
        region = rng.choice(REGIONS)
        use_case = rng.choice(USE_CASES)
        owner = rng.choice(
            (
                "Director of Digital Services",
                "Chief Information Officer",
                "Head of Innovation and Smart City",
                "Deputy Mayor for Digital Transformation",
            )
        )

        record = MunicipalityRecord(
            municipality_id=municipality_id,
            display_name=f"Municipality of {name}",
            slug=slug,
            region=region,
            population_band=population,
            maturity_tier=tier,
            primary_use_case=use_case,
            service_owner_role=owner,
            documents=CORPUS_DOCUMENT_TYPES,
        )
        records.append(record)

        mun_dir = municipalities_dir / municipality_id
        mun_dir.mkdir(parents=True, exist_ok=True)
        context = _MunicipalityContext(record=record, rng=rng)
        for doc_type in CORPUS_DOCUMENT_TYPES:
            content = _render_document(doc_type, context)
            (mun_dir / f"{doc_type}.md").write_text(content, encoding="utf-8")

    metadata = build_metadata(records, seed=seed, output_dir=output_dir)
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return metadata


def build_metadata(
    records: Sequence[MunicipalityRecord],
    *,
    seed: int,
    output_dir: Path,
) -> dict[str, Any]:
    """Build corpus-level metadata JSON structure."""
    tier_counts = {tier: 0 for tier in MATURITY_TIERS}
    for record in records:
        tier_counts[record.maturity_tier] += 1

    return {
        "corpus_version": CORPUS_VERSION,
        "synthetic": True,
        "generated_on": date.today().isoformat(),
        "generator": "localgovbench.synthetic.municipality_corpus",
        "seed": seed,
        "municipality_count": len(records),
        "document_types": list(CORPUS_DOCUMENT_TYPES),
        "maturity_tier_distribution": tier_counts,
        "output_path": str(output_dir.as_posix()),
        "assumptions_doc": "docs/synthetic_municipality_corpus.md",
        "municipalities": [asdict(record) for record in records],
        "disclaimer": (
            "Fictional municipalities for workflow and evidence-extraction experiments only. "
            "Not empirical field data; no real persons or organizations."
        ),
    }


@dataclass
class _MunicipalityContext:
    record: MunicipalityRecord
    rng: random.Random

    @property
    def name(self) -> str:
        return self.record.display_name

    @property
    def tier(self) -> str:
        return self.record.maturity_tier

    @property
    def owner(self) -> str:
        return self.record.service_owner_role

    @property
    def use_case(self) -> str:
        return self.record.primary_use_case

    def policy_status(self) -> str:
        return {
            "low": "Draft — pending council adoption",
            "emerging": "Approved with conditions (2025-09)",
            "managed": "Approved and reviewed annually (2025-11)",
        }[self.tier]

    def oversight_cadence(self) -> str:
        return {
            "low": "ad hoc when incidents arise",
            "emerging": "monthly sampling of 5% of outputs",
            "managed": "weekly sampling of 10% with quarterly audit",
        }[self.tier]


def _slugify(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")


def _render_document(doc_type: str, ctx: _MunicipalityContext) -> str:
    renderers = {
        "governance_policy": _governance_policy,
        "ai_strategy": _ai_strategy,
        "oversight_procedure": _oversight_procedure,
        "risk_register": _risk_register,
        "procurement_note": _procurement_note,
        "architecture_note": _architecture_note,
    }
    return renderers[doc_type](ctx)


def _header(ctx: _MunicipalityContext, title: str) -> str:
    return (
        f"# {title}\n\n"
        f"**SYNTHETIC DOCUMENT — NOT A REAL MUNICIPALITY**\n\n"
        f"**Organization:** {ctx.name}  \n"
        f"**Region:** {ctx.record.region}  \n"
        f"**Population band:** {ctx.record.population_band}  \n"
        f"**Maturity tier (generator):** {ctx.tier}  \n"
        f"**Municipality ID:** `{ctx.record.municipality_id}`\n\n"
    )


def _footer() -> str:
    return "\n---\n*Synthetic document generated for LocalGovBench municipality corpus.*\n"


def _governance_policy(ctx: _MunicipalityContext) -> str:
    return (
        _header(ctx, "Municipal AI Governance Policy")
        + f"**Status:** {ctx.policy_status()}\n\n"
        "## Purpose\n\n"
        f"This policy governs the municipality's on-premise large language model programme "
        f"supporting **{ctx.use_case}**. Model outputs are **advisory**; accountable decisions "
        f"remain with designated service owners.\n\n"
        "## Accountability\n\n"
        f"- Service owner: {ctx.owner}\n"
        "- AI oversight committee meets quarterly; minutes filed under ref GOV-AI-MIN\n"
        "- Complaint and correction procedure published on intranet (ref GOV-AI-CP-01)\n\n"
        "## Data protection\n\n"
        "- Personal data in prompts requires RoPA entry and documented lawful basis\n"
        "- Inference logs retained per municipal retention schedule (tier-dependent)\n"
        "- DPIA reference: synthetic placeholder DPIA-AI-2026\n\n"
        "## Human oversight\n\n"
        f"- Review cadence: {ctx.oversight_cadence()}\n"
        "- High-risk topics (legal, budget, personal data) require named officer sign-off\n\n"
        + _footer()
    )


def _ai_strategy(ctx: _MunicipalityContext) -> str:
    horizon = {
        "low": "2027",
        "emerging": "2028",
        "managed": "2030",
    }[ctx.tier]
    return (
        _header(ctx, "Municipal AI Strategy — Sovereign LLM Programme")
        + "## Vision\n\n"
        f"By {horizon}, {ctx.name} will operate a **sovereign, on-premise** LLM capability "
        f"aligned with public values, GDPR accountability, and EU AI Act deployer duties "
        f"(operational themes only — not legal certification).\n\n"
        "## Priority use case\n\n"
        f"- Primary: {ctx.use_case}\n"
        "- Secondary pilots: internal knowledge search; translation assist for caseworkers\n\n"
        "## Roadmap\n\n"
        "| Phase | Focus |\n|-------|-------|\n"
        "| 1 | Policy, architecture, procurement guardrails |\n"
        "| 2 | Controlled pilot with oversight sampling |\n"
        "| 3 | Scale with vendor-independence test and skills plan |\n\n"
        "## Success measures\n\n"
        "- Documented oversight samples and incident response drills\n"
        "- No uncatalogued cross-border inference paths\n"
        "- Annual strategy review led by "
        f"{ctx.owner}\n\n"
        + _footer()
    )


def _oversight_procedure(ctx: _MunicipalityContext) -> str:
    sla = {"low": "48 hours", "emerging": "24 hours", "managed": "4 hours"}[ctx.tier]
    return (
        _header(ctx, "Human Oversight Procedure — LLM Outputs")
        + "## Scope\n\n"
        "Applies to all staff using the municipal sovereign LLM for draft or advisory content.\n\n"
        "## Review thresholds\n\n"
        "- **Tier A (low sensitivity):** peer review optional; log prompt ID\n"
        "- **Tier B (operational):** named reviewer within one business day\n"
        "- **Tier C (high sensitivity):** policy officer sign-off; no external circulation without approval\n\n"
        "## Intervention\n\n"
        f"- Supervisors may override or block outputs; overrides logged in case system\n"
        f"- Escalation SLA for Tier C: {sla}\n"
        f"- Sampling: {ctx.oversight_cadence()}\n\n"
        "## Traceability\n\n"
        "- Prompt registry entry required before production use\n"
        "- Review samples linked to case IDs in oversight log\n\n"
        + _footer()
    )


def _risk_register(ctx: _MunicipalityContext) -> str:
    base_score = {"low": 12, "emerging": 9, "managed": 6}[ctx.tier]
    risks = [
        ("R-01", "Inadequate human review of high-impact drafts", base_score),
        ("R-02", "Personal data in prompts without RoPA entry", base_score + 1),
        ("R-03", "Vendor lock-in on model weights", base_score - 1),
        ("R-04", "Undocumented cross-border API egress", base_score),
        ("R-05", "Insufficient incident response playbooks", base_score + 2),
    ]
    rows = "\n".join(
        f"| {rid} | {desc} | {score} | {'Open' if score >= 10 else 'Mitigated'} |"
        for rid, desc, score in risks
    )
    return (
        _header(ctx, "AI Programme Risk Register")
        + "## Register (synthetic)\n\n"
        "| ID | Risk | Score (1–16) | Status |\n|----|------|--------------|--------|\n"
        f"{rows}\n\n"
        "**Scoring note:** Higher scores indicate residual risk in this synthetic tier.\n\n"
        + _footer()
    )


def _procurement_note(ctx: _MunicipalityContext) -> str:
    vendor = ctx.rng.choice(
        ("OpenGov Models Ltd", "Sovereign Stack Cooperative", "Municipal AI Partners GmbH")
    )
    exit_clause = {
        "low": "exit terms under negotiation",
        "emerging": "30-day notice for model weight changes",
        "managed": "30-day notice; annual portability test mandatory",
    }[ctx.tier]
    return (
        _header(ctx, "Procurement Note — LLM Platform")
        + "## Contract summary\n\n"
        f"- Supplier: {vendor} (fictional)\n"
        "- Deployment: on-premise appliance in municipal data centre\n"
        f"- Service owner signatory: {ctx.owner}\n\n"
        "## Governance clauses\n\n"
        f"- Data processing: EU hosting only; subprocessors listed in Annex C\n"
        f"- Model change: {exit_clause}\n"
        "- Audit rights: annual security and logging review\n"
        "- Open-weights export format specified in Schedule 4\n\n"
        "## Value band\n\n"
        "Synthetic placeholder — not a real financial commitment.\n\n"
        + _footer()
    )


def _architecture_note(ctx: _MunicipalityContext) -> str:
    logging = {
        "low": "basic application logs; retention TBD",
        "emerging": "SIEM forwarding; 90-day prompt redaction",
        "managed": "SIEM + immutable audit trail; 90-day redaction; annual pen-test",
    }[ctx.tier]
    return (
        _header(ctx, "Technical Architecture — On-Premise LLM")
        + "## Deployment\n\n"
        "- Inference cluster in municipal data centre (EU jurisdiction)\n"
        "- No default public-cloud inference; egress deny-by-default firewall\n"
        "- RBAC with MFA for operators and break-glass procedure\n\n"
        "## Logging and monitoring\n\n"
        f"- {logging}\n"
        "- Capacity alerts to platform operations\n\n"
        "## Change management\n\n"
        "- Model updates require change advisory board (CAB) approval\n"
        "- Rollback runbook: ARCH-LLM-ROLLBACK-01\n"
        "- Disaster recovery RPO 24h / RTO 8h (synthetic targets)\n\n"
        + _footer()
    )

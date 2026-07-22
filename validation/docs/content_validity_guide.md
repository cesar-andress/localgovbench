> **Status: LEGACY — v0.1.0**  
> Historical validation guidance for the v0.1 instrument.  
> **Active framework:** [`../../localgovbench_measurement_validation/affordance/README.md`](../../localgovbench_measurement_validation/affordance/README.md).


# Content Validity Study Guide

## Purpose

Assess whether each of the **25 criteria** in LocalGovBench v0.1 is **clear**, **relevant**, and **sufficient** for evaluating governance readiness for sovereign municipal LLM deployments.

## Materials

- Template: `validation/templates/content_validity_study.yaml`
- Criterion definitions: `localgovbench/framework/dimensions.py`
- Benchmark specification: `docs/benchmark_specification.md`

## Procedure

1. Brief experts with scope (on-premise LLM, EU public sector, no legal compliance scoring).
2. For each criterion, experts rate:
   - **Clarity** (1–5): wording understandable and operable
   - **Relevance** (1–5): contributes to governance readiness construct
   - **Sovereign LLM fit** (1–5): applicable to local/sovereign deployment context
3. Collect free-text revision suggestions.
4. Aggregate; discuss in consensus workshop.
5. Revise instrument; record changes.

## Analysis (field study)

| Metric | Typical use |
|--------|-------------|
| I-CVI | Proportion of experts rating relevant (4–5) per item |
| S-CVI/Ave | Mean CVI across items |
| CV ratio | Comprehensiveness of dimension sets |

## Repository template status

The bundled YAML contains **empty scores** (`null`) — ready for empirical collection. Do not treat as study results.

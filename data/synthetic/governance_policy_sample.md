# SYNTHETIC DOCUMENT — NOT A REAL MUNICIPALITY

# Internal AI Governance Policy (Draft v0.3)

**Organization:** Fictional Borough of North Estuary  
**Scope:** On-premise large language model for internal policy drafting  
**Status:** Synthetic sample for LocalGovBench evidence extraction experiments

## 1. Purpose

This policy defines governance expectations for the borough's sovereign LLM deployment
hosted in the municipal data centre. The system must not process citizen-facing requests
without a separate public transparency review.

## 2. Human oversight

Section 4.2 requires that any LLM-generated draft circulated beyond the originating team
must be reviewed by a named policy officer. Review triggers include references to
personal data, legal commitments, or budget figures.

The oversight procedure (Appendix B) states: *"Automated outputs are advisory; accountable
decisions remain with the designated service owner."* Sampling of 10% of weekly outputs
is mandated for quality review.

## 3. Data protection

Personal data must not be entered into prompts unless recorded in the RoPA entry
**AI-DRAFT-2026-01** with documented lawful basis (public task, Article 6(1)(e)).

Prompt and inference logs are retained for 90 days, then deleted from primary storage.
Backups expire after 180 days.

## 4. Architecture and sovereignty

The LLM inference stack runs on borough-owned hardware in the EU. Egress to external
APIs is blocked by default at the network firewall except for approved security updates.

Vendor contracts require 30-day notice before model weight changes. Migration test T-2026-03
demonstrated export of prompt registry YAML to an alternate open-weights runtime.

## 5. Risk and incidents

AI-related risks are entered in the corporate risk register (reference R-447). Incidents
including harmful hallucinations must be reported to the IT security desk within 4 hours.

## 6. Limitations of this sample

This document is **fabricated** for software testing. It does not represent real
governance maturity or legal compliance.

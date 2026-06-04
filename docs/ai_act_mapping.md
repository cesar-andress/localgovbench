# EU AI Act Mapping (Indicative)

> **Disclaimer:** This mapping supports research and self-assessment. It is **not** legal advice. Consult qualified counsel for compliance decisions.

LocalGovBench dimensions are **indicatively** related to themes in Regulation (EU) 2024/1689 (AI Act). Exact obligations depend on system classification, role (provider/deployer), and use case.

## High-level mapping

| LocalGovBench dimension (v0.1) | AI Act themes (indicative) |
|--------------------------------|----------------------------|
| `legal_regulatory` | Classification documentation, deployer duties, data governance |
| `technical_security` | Technical documentation, logging, change control |
| `organizational` | Governance, human oversight assignments, risk management |
| `operational` | Monitoring, serious incidents, post-deployment practices |
| `strategic_sovereignty` | Supply chain transparency, independence from providers |

## Public sector relevance

Public authorities may act as **deployers** of AI systems procured from vendors. Local governance practices should document:

- System purpose and affected populations
- Classification rationale (e.g., limited vs high-risk)
- Human oversight arrangements
- Incident and serious event reporting pathways (where applicable)

## Placeholder for future work

A machine-readable mapping table (`data/templates/ai_act_mapping.csv`) may be added in a later release. This release documents relationships in prose only.

## References

- Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence
- European Commission AI Act implementation resources (check for updates at release time)

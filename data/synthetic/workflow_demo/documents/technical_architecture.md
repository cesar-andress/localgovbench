# Technical Architecture — On-Premise LLM (Synthetic Demo)

## Deployment

- Inference cluster in municipal data centre (EU hosting)
- No public cloud inference; egress firewall blocks outbound model APIs
- RBAC with MFA for operators

## Logging

- Security events to SIEM; prompts redacted after 90 days per retention schedule

## Change management

- Model updates require CAB approval and rollback runbook TEST-LLM-ROLLBACK

*Synthetic document for LocalGovBench workflow demo.*

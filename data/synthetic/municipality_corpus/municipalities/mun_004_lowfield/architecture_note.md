# Technical Architecture — On-Premise LLM

**SYNTHETIC DOCUMENT — NOT A REAL MUNICIPALITY**

**Organization:** Municipality of Lowfield  
**Region:** Central Estuary Belt  
**Population band:** 41k–120k  
**Maturity tier (generator):** emerging  
**Municipality ID:** `mun_004_lowfield`

## Deployment

- Inference cluster in municipal data centre (EU jurisdiction)
- No default public-cloud inference; egress deny-by-default firewall
- RBAC with MFA for operators and break-glass procedure

## Logging and monitoring

- SIEM forwarding; 90-day prompt redaction
- Capacity alerts to platform operations

## Change management

- Model updates require change advisory board (CAB) approval
- Rollback runbook: ARCH-LLM-ROLLBACK-01
- Disaster recovery RPO 24h / RTO 8h (synthetic targets)


---
*Synthetic document generated for LocalGovBench municipality corpus.*

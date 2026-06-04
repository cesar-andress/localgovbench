# Case Alpha — Evidence Pack (Synthetic)

**Municipality profile:** Mid-size city piloting an on-premise citizen Q&A assistant.  
**Deployment:** Single GPU cluster; no public cloud inference.  
**Study use:** GRB IRR pilot — **synthetic** artefacts.

---

## Artefacts reviewed

| ID | Type | Summary |
|----|------|---------|
| A-01 | AI governance memo (draft) | States intent for human review; not yet council-approved |
| A-02 | DPIA excerpt | Personal data in logs; retention 90 days; lawful basis cited as public task |
| A-03 | Ops runbook | Restart procedures; **no** model rollback or intervention thresholds |
| A-04 | Committee minutes | IT security update; **no** standing AI oversight body |
| A-05 | Architecture diagram | On-prem stack; vendor LLM weights hosted locally |

---

## Dimension highlights (for coding)

- **D1 Accountability:** Named IT lead but no elected-officer sign-off for AI decisions.
- **D2 Human Oversight:** Runbook lacks human-in-the-loop triggers; monitoring is uptime-only.
- **D3 Transparency:** Internal FAQ on AI use; no citizen-facing model card.
- **D4 Data Legitimacy:** DPIA exists; minimization and purpose limitation partially documented.
- **D5 Risk:** Generic cyber risk register; AI-specific harms not scored.
- **D6 Sovereignty:** On-prem emphasized; portability plan absent.

---

## Coding notes

Assessors should expect **low D2** and **low D4** relative to D1/D3. Scores ≥ 3 require citing artefact IDs above.

*Synthetic pack for `case_alpha` — not a real municipality.*

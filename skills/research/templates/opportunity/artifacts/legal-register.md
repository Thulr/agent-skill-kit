# Legal Register — <opportunity-slug>

> Filled by `investigate` on `legal` surface, using
> `references/opportunity/playbooks/legal.md`. **This is an inventory of legal
> questions to escalate to counsel. It is NOT legal advice.
> Jurisdiction-dependent. Counsel review required before commitments.**

## Opportunity statement

<one-line>

## Jurisdictions in scope

| Jurisdiction | Why in scope | Counsel identified? |
|---|---|---|
| US-Federal | <baseline> | <yes/no> |
| US-California | <CCPA + privacy + employment + sales tax> | <…> |
| US-New York | <employment + DFS + tax> | <…> |
| EU (general + member states) | <GDPR + product liability + tax> | <…> |
| UK | <UK-GDPR + sanctions + tax> | <…> |
| Other: <country> | <reason> | <…> |

## Entity / contract structure

| Question | Status | To escalate |
|---|---|---|
| Entity formed? | <yes / no — pending> | <jurisdiction choice> |
| Founder agreements signed (IP assignment, vesting)? | <yes / no> | <…> |
| Contractor agreements with IP assignment + classification? | <yes / no> | <…> |
| Customer contract (terms of service, MSA, DPA) drafted? | <yes / no> | <draft + counsel review> |
| Vendor / partner agreements reviewed? | <…> | <…> |

## IP

| Question | Status | To escalate |
|---|---|---|
| Trademark search done for product name? | <…> | <USPTO + EU + UK> |
| Domain holdings? | <…> | <…> |
| Patent landscape scan? | <…> | <freedom-to-operate review> |
| Copyright posture on training / content data? | <…> | <fair-use / license / consent> |
| Open-source license audit (deps)? | <…> | <copyleft / attribution / patent grants> |
| Trade secrets identified + protected? | <…> | <NDA + access controls> |

## Privacy (GDPR / CCPA / sectoral)

| Data kind | PII? | Consent basis | Retention | DSR rights supported | Audit log | Residency |
|---|---|---|---|---|---|---|
| <kind> | <yes/no> | <consent / contract / legitimate interest / legal obligation> | <duration> | <yes/no — mechanism> | <yes/no> | <region> |
| <…> | <…> | <…> | <…> | <…> | <…> | <…> |

**Privacy policy drafted?** <yes/no — link, last counsel review date>

**Data processing agreement (DPA) template ready?** <yes/no — link>

**Data Protection Officer / Privacy lead designated?** <yes/no — name>

## Security compliance

| Certification | Required by | Timeline | Cost estimate |
|---|---|---|---|
| SOC 2 Type I | <enterprise pilot> | <month 6> | $<X> + ongoing |
| SOC 2 Type II | <enterprise GA> | <month 12> | $<X> |
| HIPAA | <health customers> | <month <N>> | $<X> + BAA |
| PCI-DSS | <handling cards> | <pre-launch> | $<X> |
| ISO 27001 | <international enterprise> | <month <N>> | $<X> |

## Industry-specific regulation

| Regulation | Jurisdiction | Applicability | Status |
|---|---|---|---|
| <e.g., HIPAA> | US | <if health PHI handled> | <…> |
| <e.g., FINRA> | US | <if securities> | <…> |
| <e.g., DSA / DMA> | EU | <if platform> | <…> |
| <e.g., FDA> | US | <if medical / device> | <…> |
| <e.g., AML / KYC> | global | <if financial> | <…> |
| <…> | <…> | <…> | <…> |

## Claims-we-cannot-make list

Marketing copy reviewed against regulatory limits.

| Claim risk | Source domain | Action |
|---|---|---|
| Health benefit claims | FDA / FTC | <route copy to counsel before launch> |
| Financial return claims | SEC / FINRA | <…> |
| Automated-decisioning claims | EU AI Act / state laws | <…> |
| Biometric / facial recognition | state laws | <…> |
| Comparative ad claims | FTC | <…> |
| AI capability guarantees | FTC | <…> |

## Employment / contractor classification

| Person | Role | Classification | Risk |
|---|---|---|---|
| <name> | <role> | <employee / contractor / international> | <misclass risk per jurisdiction> |

## Tax exposure

| Tax | Jurisdiction | Trigger | Status |
|---|---|---|---|
| Sales tax | US states | <nexus per state> | <…> |
| VAT | EU | <€10k turnover threshold> | <…> |
| Corp income tax | <entity HQ + nexus> | <…> | <…> |
| Marketplace facilitator obligations | various | <if platform> | <…> |

## Severity / kill-criterion candidates

Legal findings with severity 4 (existential):

- <e.g., "regulatory ruling that prohibits the core mechanic in target
  jurisdiction — severity 4, kill criterion if no carve-out>

## F/A/D/R

### Facts

- <e.g., "EU AI Act Article 5 prohibits real-time biometric ID in
  public spaces; product not subject because feature is opt-in
  workplace use; source: AI Act + counsel memo dated 2026-04-01">

### Assumptions

- <e.g., "assume current SOC 2 path completes by month 6; test:
  monthly milestone review with auditor">

### Decisions

- <e.g., "defer EU launch until DPO designated and DPA template
  reviewed by counsel">

### Risks

- <e.g., "severity-3: contractor classification in California —
  mitigation: convert top contractors to W-2 by month 3">

## Next test

<one falsifiable action — usually scheduling counsel review on the
highest-leverage open question, or starting the SOC 2 readiness
assessment>

## Sources

| # | Source | Type | Confidence |
|---|---|---|---|
| 1 | <…> | <…> | <H/M/L> |

## Disclaimers

**This register is not legal advice. Every "we believe" or "we are
not subject to" claim requires counsel verification. Outputs are
jurisdiction-dependent and the legal landscape changes.**

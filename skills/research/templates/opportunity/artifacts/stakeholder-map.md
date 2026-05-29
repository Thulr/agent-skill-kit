# Stakeholder Map — <opportunity-slug>

> Filled by `investigate` on `stakeholder` surface, using
> `references/playbooks/stakeholder.md`. **B2B / enterprise / internal
> tools.** Collapse to "user = buyer = approver" for consumer / SMB.

## Opportunity statement

<one-line>

## Target buyer org type

- **Org size:** <SMB / mid-market / enterprise>
- **Industry:** <…>
- **Reference accounts targeted:** <named accounts in pipeline>

## Five roles (mapped for the target deal)

### User(s)

| Field | Value |
|---|---|
| Role / title | <e.g., individual contributor analyst> |
| Daily touch | <high / med / low> |
| Optimizes for | <productivity / quality / autonomy> |
| Says yes when | <e.g., reduces tedious work> |
| Says no when | <e.g., adds compliance burden> |

### Buyer (controls budget)

| Field | Value |
|---|---|
| Role / title | <e.g., VP of Operations> |
| Authority level | <can sign $<X> / requires CFO> |
| Optimizes for | <ROI / risk / team productivity> |
| Decision criteria (top 3) | <…> |
| Says yes when | <…> |
| Says no when | <…> |

### Approver(s)

| Field | Value |
|---|---|
| Role / title | <e.g., CTO + CFO + Legal> |
| Approval triggers | <$ threshold / risk class / data type> |
| Typical approval duration | <days / weeks> |
| Common reasons for rejection | <…> |

### Champion (pushes internally)

| Field | Value |
|---|---|
| Name (or "to identify") | <…> |
| Role / title | <…> |
| Power level | <H/M/L — formal authority + influence> |
| Aligned because | <…> |
| Reciprocal value we offer the champion | <career / outcome / story> |
| Risk if champion leaves | <…> |

If champion is aspirational ("we hope to find one"), the deal is at
risk; flag as severity ≥ 3.

### Blockers

| Function | Concern | What they need to NOT block | Status |
|---|---|---|---|
| Security | <SOC 2 / data handling / vendor risk> | <SOC 2 cert + responses to vendor questionnaire + DPA> | <…> |
| Legal | <DPA / IP / liability> | <DPA template + indemnity terms + MSA review> | <…> |
| Procurement | <vendor onboarding> | <questionnaire + insurance + 30 / 60 / 90 payment terms> | <…> |
| IT | <provisioning / SSO / data flows> | <SSO support + standard provisioning + audit log> | <…> |
| Finance | <budget / contracting structure> | <annual prepay option + multi-year discount> | <…> |
| Leadership skeptic | <strategic fit> | <reference customers + ROI story> | <…> |

## Power dynamics

Where formal authority and actual influence diverge:

| Person | Formal authority | Actual influence | Notes |
|---|---|---|---|
| <name> | <title can sign $X> | <…> | <e.g., "CFO has formal authority but defers to VP-Ops on stack choices"> |

## Procurement path (step by step)

| Step | Trigger | Owner | Duration (typical) | Drop-off (%) |
|---|---|---|---|---|
| 1 | Initial demo | <buyer> | 1 day | <…> |
| 2 | Pilot scoping | <buyer + user> | 1 week | <…> |
| 3 | Security review | <security> | 2–4 weeks | <…> |
| 4 | Legal review (MSA + DPA) | <legal> | 2–6 weeks | <…> |
| 5 | Procurement onboarding | <procurement> | 2–4 weeks | <…> |
| 6 | Final approval | <approver chain> | 1–2 weeks | <…> |
| 7 | PO + signature | <buyer> | 1 week | <…> |
| 8 | Provisioning | <IT> | 1–2 weeks | <…> |
| 9 | Activation | <user> | week 1 | <…> |

Total typical timeline: <weeks / months> from first demo to activation.

## Change-friction score

Replacing an existing tool:

| Friction source | Cost | Mitigation |
|---|---|---|
| Training | <hrs × people × $/hr> | <…> |
| Migration | <data, integrations> | <…> |
| Internal politics | <champion-vs-blocker tension> | <…> |
| Switching cost (existing contract) | $<X> | <…> |
| **Total change-friction** | **<$X> + <N person-weeks>** | |

Compare to status-quo benefit. If switching cost > 12 months of
value, hard sell.

## Vendor onboarding scope

| Requirement | Status | Owner | Time |
|---|---|---|---|
| Vendor security questionnaire | <e.g., not started> | <…> | <…> |
| Insurance certificate (E&O, cyber) | <…> | <…> | <…> |
| W-9 / tax forms | <…> | <…> | <…> |
| Subprocessor list | <…> | <…> | <…> |
| References (3–5) | <…> | <…> | <…> |
| Financial statements (if requested) | <…> | <…> | <…> |

## Reference customer status

| Account | Role | Reference status | Public / private |
|---|---|---|---|
| <name> | <…> | <willing to take 1 call/quarter> | <private> |
| <name> | <…> | <case study + quote> | <public> |

## F/A/D/R

### Facts

- <e.g., "target buyer org has 3-month avg procurement timeline; security review
  is the longest single step at 6 weeks; source: <interview / public docs>">

### Assumptions

- <e.g., "assume we can complete SOC 2 Type I by month 6, enabling
  enterprise deals; test: monthly auditor milestone review">

### Decisions

- <e.g., "build security collateral first (SOC 2, DPA, vendor
  questionnaire responses); defer field sales until 3 reference
  customers signed">

### Risks

- <e.g., "severity-3: aspirational champion at target account 1 has
  no formal authority; mitigation: identify champion in 2 other
  accounts in parallel">

## Next test

<one falsifiable experiment — usually a procurement-path interview
with a comparable customer, or a vendor-questionnaire dry-run against
the target's known security policy>

## Sources

| # | Source | Type | Confidence |
|---|---|---|---|
| 1 | <…> | <…> | <H/M/L> |

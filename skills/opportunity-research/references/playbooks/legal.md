# Legal / Regulatory / Compliance Playbook

> **This playbook produces an inventory of legal questions to escalate
> to counsel. It is NOT legal advice. Outputs are jurisdiction-dependent
> and legal review is required before commitments.**

## Scope

What you are allowed to do, what constraints you inherit, where the
landmines are. Legal research is the discipline that prevents
"launched, then hit by a regulator / lawsuit / takedown / fine."

- In: entity / contract structure, IP (ownership, trademarks,
  patents, copyright risk), licensing (open-source, vendor,
  content, data), privacy (GDPR, CCPA, PII handling, retention,
  DSR), security compliance (SOC 2, HIPAA, PCI, ISO 27001),
  industry-specific regulation (financial, health, education,
  labor, automotive), advertising and claims, employment /
  contractor classification, tax (sales tax, marketplace
  obligations, international).
- Out: legal *advice* (escalate to counsel), product-internal
  security architecture (`technical.md`), partnership contracts'
  business terms (`channel.md`, `stakeholder.md`), operational
  staffing (`operational.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **GDPR / CCPA / HIPAA / PCI-DSS primary sources** — the rule
  texts themselves are the authoritative reference for privacy and
  payment compliance.
- **Stripe Atlas Guides** — operational legal patterns for
  early-stage businesses (entity formation, sales tax, international
  expansion, contracts, IP).
- **Privacy by Design (Ann Cavoukian 2009)** — privacy as a system
  constraint rather than a launch blocker. Embed privacy now or
  retrofit at 10× cost.
- **Convo.txt** — "This is often ignored early, then becomes a giant
  fire later." Legal is a guardrail topic; the playbook produces
  the inventory of questions to escalate, not the answers.

## Good signals

- Output is framed as **questions to escalate**, not answers.
  Every claim that resembles "we are not subject to X" carries
  "verify with counsel."
- All applicable regulations are named with jurisdiction (US-Fed,
  EU, UK, California, target country).
- PII handling is inventoried: what data, what consent basis, what
  retention, what DSR rights, what audit trail.
- IP ownership is unambiguous — founder agreements, contractor
  agreements, open-source license compatibility, third-party
  content rights.
- Marketing / product claims have a "claims-we-cannot-make" list
  (especially in regulated domains: health, finance, automated
  decisioning).
- Compliance certifications needed by customer segment are named
  (SOC 2 for enterprise, HIPAA for health, PCI for payments).
- Employment / contractor classification per jurisdiction is named.

## Common failures

- **Treating legal as a launch-blocker rather than a design
  constraint.** Privacy retrofitted at scale is one of the most
  expensive fixes in software. Mitigation: surface privacy / IP /
  claims requirements at design time.
- **GDPR / CCPA blind spot.** "We don't have EU users" — until
  marketing puts the URL in front of EU users, or a user travels.
  Geo-blocking is harder than it looks.
- **Open-source license incompatibility.** GPL contamination,
  attribution misses, or dual-license terms that force open-sourcing
  proprietary work. Audit dependencies for licenses, not just CVEs.
- **Contractor as employee.** Misclassification risk varies by
  jurisdiction; California, New York, several EU states are
  aggressive. Tax + benefit + IP-assignment exposure.
- **Claims regulator scrutinizes.** Health benefits, financial
  returns, automated decisioning, AI capability — regulators have
  active interest. Marketing copy review by counsel before launch.
- **Data residency assumed.** Customer data crossing borders may
  violate residency requirements (UK NHS, EU public-sector, China,
  Russia). Cloud-region choice matters.
- **Sales tax / marketplace obligations.** Nexus thresholds per
  US state; EU VAT; marketplace responsibilities for collecting tax
  on platform sales. Often missed in v1.
- **IP from prior employer.** Founders' work-product clauses can
  attach to startup IP if not cleanly assigned. Cleaner now than
  in due diligence.

## Heuristics

- **(scope, investigate)** *Inventory not advice.* The output is a
  list of questions to escalate to counsel, with the risk severity
  attached. Every "we believe" / "we are not subject to" has
  "verify with counsel" stapled on.
- **(investigate)** *Jurisdiction-by-jurisdiction.* US-Fed, state
  (esp. CA, NY, TX), EU (esp. GDPR), UK, target countries. Don't
  treat "US-only" as risk-free.
- **(investigate, decide)** *PII inventory by 6 axes.* Data kind,
  consent basis, retention, DSR rights, audit trail, residency.
- **(investigate)** *Claims-we-cannot-make list.* In regulated
  domains: health benefits, financial returns / outcomes,
  automated-decisioning capabilities, biometric uses, AI behavior
  guarantees. Marketing reviewed against this list.
- **(investigate, decide)** *Compliance certifications by segment.*
  SOC 2 for enterprise, HIPAA for health, PCI for payments, ISO 27001
  for international enterprise. Timelines and costs scoped.
- **(investigate)** *Contracts inventory.* Founder, contractor,
  customer, vendor, partner. IP assignment, confidentiality,
  liability, indemnity, termination.
- **(investigate)** *Open-source license audit.* All deps with
  license; flag copyleft (GPL/AGPL), attribution requirements,
  patent grants.
- **(decide)** *Pre-launch counsel review.* Before commitments —
  marketing site, customer contracts, partnership terms — counsel
  review is non-optional in regulated domains.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is output framed as escalation questions, not answers? | Output reads as advice | Re-frame; staple "verify with counsel." |
| Are applicable jurisdictions enumerated? | US-only assumed | Enumerate; check geo-block reality. |
| Is PII inventoried by 6 axes? | Partial | Complete inventory; tag retention + consent + DSR. |
| Is the claims-we-cannot-make list present? | Marketing not constrained | Build the list per regulated domain. |
| Are compliance certifications scoped by segment? | "SOC 2 later" | Spec timeline + cost; confirm with enterprise segment buyer. |
| Are contracts inventoried with IP assignment? | Loose contracts | Catalogue; tighten IP assignment; counsel review. |
| Is the OSS license audit done? | Untracked deps | Audit; flag copyleft, attribution, patent grants. |
| Is counsel review scheduled for pre-launch artifacts? | Self-served | Schedule; budget; allow time for revisions. |

## Cross-references

- → `references/playbooks/technical.md` — for security threat model
  feeding compliance requirements.
- → `references/playbooks/data.md` — for the data-side of privacy
  / consent / retention.
- → `references/playbooks/operational.md` — for the ongoing
  compliance operations.
- → `references/playbooks/gtm.md` — for marketing claims review.
- → `references/playbooks/risk.md` — where legal severity-4
  risks become kill criteria.
- → `references/core/severity-rubric.md` — for legal-risk scoring.
- → `references/core/fadr-framework.md` — for the F/A/D/R fold.
- → `templates/artifacts/legal-register.md` — the artifact this
  playbook produces under `investigate`. **Carries the "not legal
  advice" marker.**

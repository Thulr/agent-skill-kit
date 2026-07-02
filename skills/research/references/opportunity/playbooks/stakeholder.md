# Stakeholder / Organizational Playbook

## Scope

Who actually drives the decision in B2B / enterprise / internal-tools
contexts: users, buyers, approvers, champions, blockers. Many products
fail because the team optimized for the user and ignored the buyer,
or vice versa. This playbook produces the decision-maker map for the
sale (or the adoption decision, for internal tools).

Collapse to "user = buyer = approver = champion" for consumer / SMB;
the full playbook is for B2B, enterprise, regulated, or internal-tooling
contexts.

- In: user / buyer / approver / champion / blocker mapping;
  per-actor incentives; power dynamics; change-friction; procurement
  path; what each actor needs to say yes; what each blocker needs
  to NOT say no.
- Out: domain glossary / workflow (`domain.md`), gtm messaging
  (`gtm.md`), channel discovery (`channel.md`), pure user-research
  personas (`customer.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **John Kotter — *Leading Change* (1996)** — change-friction in
  organizations; coalitions and champions; the cost of skipping
  the urgency / coalition / vision steps.
- **Geoffrey Moore — *Crossing the Chasm* (2014)** — the difference
  between innovator and pragmatist buyers; pragmatists buy in
  herds and need peer references.
- **Patrick Lencioni — *The Five Dysfunctions of a Team* (2002)** —
  team-level commitment-vs-buy-in dynamics; trust as a prerequisite.
- **Convo.txt** — stakeholder research covers users / buyers /
  approvers / champions / blockers / incentives / power /
  change-friction / procurement — and "many products fail because
  teams optimize for the user but ignore the buyer."

## Good signals

- Roles are explicit and may be the same or different people:
  user (touches it daily), buyer (controls budget), approver
  (signs off), champion (pushes internally), blocker (security /
  procurement / legal / leadership skeptic).
- Each actor has incentive + success metric + "what would make
  them say yes" + "what would make them say no."
- Power dynamics named: who actually has influence, who has formal
  authority, where they diverge.
- Procurement path mapped step-by-step: interest → demo → pilot →
  security review → legal review → MSA → PO → activate. Each
  step has typical duration + drop-off rate.
- Champion identification is real, not aspirational: named person
  with named title + named org + reason they're aligned.
- Blockers named with what they'd need to NOT block: security
  needs SOC 2; procurement needs vendor onboarding; legal needs
  data-processing agreement.
- Change-friction acknowledged: replacement of existing tool
  involves training, migration, internal politics. None are free.

## Common failures

- **Optimizing for user, ignoring buyer.** Free product that users
  love and budget owners won't fund. Mitigation: buyer in the loop
  from week 1 in B2B.
- **Optimizing for buyer, ignoring user.** Top-down purchase that
  users sabotage. Adoption falls; renewal at risk.
- **Champion that doesn't have enough power.** Excited director
  who can't push past the VP's skepticism. Champion identification
  needs power assessment, not enthusiasm assessment.
- **Procurement / security / legal as afterthought.** All three are
  blockers more often than budget. Discover their requirements
  before the buyer says yes.
- **Approver path discovered mid-deal.** "We need a VP-level
  signature for that." Mapping approval paths in advance saves
  weeks per deal.
- **Single stakeholder for an enterprise opportunity.** One person's
  championship doesn't move enterprise procurement. Need 3–5
  named relationships across user / buyer / approver / champion.
- **Treating change-friction as zero.** Replacement of an existing
  tool involves training, migration, internal politics, time
  investment by champion. The "switching cost" is real.
- **Vendor-onboarding friction.** Enterprise vendor onboarding is
  a 4–12 week process before a single dollar moves. Spec it before
  the close.

## Heuristics

- **(scope, investigate)** *Map five roles explicitly: user, buyer,
  approver, champion, blocker.* For each: name, title, role,
  incentive, what makes them say yes, what makes them say no.
- **(investigate)** *Power dynamics named.* Who has formal
  authority? Who has actual influence? Where do they diverge?
  Where does authority require influence to act?
- **(investigate, decide)** *Procurement path step-by-step.*
  Demo → pilot → security → legal → MSA → PO → activate. Typical
  duration + drop-off per step.
- **(investigate)** *Champion check.* Named person + title + org +
  why they're aligned + how much power they have. Aspirational
  champions don't move deals.
- **(investigate)** *Blocker requirements inventory.* Security
  needs / legal needs / procurement needs / IT needs. Spec these
  before the buyer says yes.
- **(investigate)** *Approver path mapped in advance.* What level
  of approval is required for this dollar amount; what evidence
  does that level need; how long does it take.
- **(investigate, decide)** *Change-friction scored.* Replacement
  cost: training, migration, internal politics, switching cost.
  Compare to status quo benefit.
- **(decide)** *Vendor onboarding scoped.* If enterprise:
  vendor questionnaire, security review, data-processing agreement,
  procurement timeline. 4–12 weeks before money moves.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are all 5 roles (user / buyer / approver / champion / blocker) mapped? | Partial map | Complete. |
| Are power dynamics (formal authority vs influence) named? | Title-only map | Re-do with influence overlay. |
| Is the procurement path mapped step-by-step with duration / drop-off? | "Long" / "complex" | Spec each step; typical duration. |
| Are champions named, with power + alignment? | Aspirational champion | Identify real champion (or note absence). |
| Are blocker requirements inventoried (security / legal / IT / procurement)? | Discovered mid-deal | Spec in advance. |
| Is the approver path known for this deal size? | Discovered during close | Map; verify with reference customer. |
| Is change-friction scored? | Assumed zero | Score: training + migration + political cost. |
| Is vendor onboarding scoped (enterprise)? | Skipped | Scope; spec timeline. |

## Cross-references

- → `references/opportunity/playbooks/domain.md` — for the underlying actor
  map (often shared structure).
- → `references/opportunity/playbooks/gtm.md` — for buyer-vs-user message
  segmentation.
- → `references/opportunity/playbooks/channel.md` — for where each actor
  lives.
- → `references/opportunity/playbooks/legal.md` — for contracts, MSAs, DPAs.
- → `references/opportunity/playbooks/risk.md` — where stakeholder
  concentration becomes a tracked risk.
- → `references/opportunity/core/fadr-framework.md` — for the F/A/D/R fold.
- → `templates/opportunity/artifacts/stakeholder-map.md` — the artifact this
  playbook produces under `investigate`.

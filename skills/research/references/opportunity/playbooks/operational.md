# Operational Playbook

## Scope

Whether the business can actually be run — delivery, support,
escalation, runbooks, staffing, vendor handoffs, monitoring, failure
modes. The product can be marketable and technically feasible and
still be a terrible business because it's painful to operate.

- In: delivery / fulfillment flow, support model and escalation
  paths, runbooks / SOPs, QA and review steps, staffing assumptions,
  training requirements, vendor ops and handoffs, monitoring and
  observability of the *business* (not the system — see
  `perf-critique` / `perf-design`), failure-mode analysis.
- Out: technical architecture (`technical.md`), unit economics
  (`financial.md`), production / SRE perf (`perf-critique` / `perf-design`),
  legal contracts (`legal.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **Eliyahu Goldratt — *The Goal* (1984)** — theory of constraints;
  the system's throughput is set by its bottleneck, not its average
  capacity.
- **Womack / Jones — *Lean Thinking* (1996)** — value stream;
  eliminate waste; pull rather than push; flow.
- **Stripe Atlas Guides** — operational patterns for early-stage
  businesses (entity, contracts, support, payments, international).
- **Convo.txt** — operational research covers delivery, support,
  escalation, runbooks, QA, staffing, training, vendor ops,
  monitoring, failure modes — and "a product that is marketable and
  technically feasible can still be a terrible business if it is
  painful to operate."

## Good signals

- Delivery / fulfillment is traced end-to-end with who does what,
  when, in what queue.
- Support model is named (self-serve / async / synchronous /
  white-glove) with the escalation path for each tier.
- Runbooks exist for the top-5 recurring operational events (or
  are explicitly planned as launch-blockers).
- Staffing is sized to predicted volume, not current. Hidden labor
  is named (the marketing site needs updates; the contracts need
  signatures; the legal cases need attention).
- Vendor handoffs are named: which third party does what, with
  what SLA, with what fallback if they fail.
- Monitoring is **business-level** (orders / day, support ticket
  rate, churn cadence) not just system-level.
- Failure modes are inventoried before launch with severity ×
  likelihood.

## Common failures

- **"We could run it once" = "we can run it 1000 times".** Single-run
  feasibility ≠ operational feasibility. The 1000th run reveals
  bottlenecks, hidden labor, and edge cases the first run hid.
- **Hidden labor.** Products that quietly need humans for
  onboarding, QA, support, content moderation, payments
  reconciliation. Staffing models that ignore them lie.
- **Support model unspecified.** Self-serve assumed by default;
  reality is async-by-email; reality at scale is synchronous
  multi-tier. The mismatch is operational debt.
- **Vendor SLAs taken at face.** "Their uptime is 99.9%" without
  a fallback for the 8.76 hours of unavailability per year. Vendor
  failure modes belong in your operational plan.
- **No runbooks at launch.** Operational events that happen weekly
  (refund, escalation, dispute, outage) without a documented
  process burn senior staff time forever.
- **Business monitoring confused with system monitoring.** System
  monitoring tells you the server is up; business monitoring tells
  you the orders are still flowing. Both matter, separately.
- **Failure modes deferred.** "We'll figure it out when it happens"
  works for week 1 and not for week 4.

## Heuristics

- **(scope, investigate)** *Trace delivery end-to-end with handoffs.*
  Who does what, when, in what queue, with what typical delay. Each
  handoff is a potential bottleneck.
- **(investigate)** *Support model named with escalation tiers.*
  Self-serve / async / synchronous / white-glove + escalation path
  for each. The model implies a cost structure (route to
  `financial.md`).
- **(investigate, decide)** *Top-5 runbook inventory.* What
  operational events do we predict will happen ≥weekly? Each gets a
  named runbook (or is launched without one as known debt).
- **(investigate)** *Staff to predicted volume, not current.* Map
  load × labor coefficient × month for the next 12 months. Hidden
  labor (legal, finance, content, support) belongs in the model.
- **(investigate)** *Vendor SLAs + fallbacks.* For each vendor: SLA,
  fallback procedure, cost of fallback, switching cost / time.
- **(investigate)** *Business monitoring separate from system
  monitoring.* What 3–5 business metrics tell you the business is
  healthy regardless of whether the servers are up?
- **(investigate, decide)** *Failure-mode pre-mortem.* List ≥5
  operational failure modes you expect; estimate severity ×
  likelihood; name mitigation. Severity-4 → kill criterion or
  pre-launch fix.
- **(decide)** *Bottleneck-aware sequencing.* The throughput of the
  operational system equals its bottleneck. Don't add capacity
  upstream of a bottleneck — it just inflates queues.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is delivery traced end-to-end with handoffs and queues? | Happy-path flow only | Re-trace including handoffs / queues / delays. |
| Is the support model named with escalation tiers? | Self-serve assumed | Spec support tiers; map cost. |
| Are runbooks named for top-5 predicted weekly events? | None | Inventory; spec each (or accept as known debt). |
| Is staffing modeled to 12-month volume, not current? | Current-state staffing | Project volume; map labor; surface hidden labor. |
| Are vendor SLAs + fallbacks named? | Vendor SLAs taken at face | Spec fallback per vendor; cost out fallback execution. |
| Is business monitoring spec'd separately from system monitoring? | "Monitoring" = uptime | Spec business metrics; alert thresholds. |
| Are ≥5 failure modes pre-mortemed? | "We'll figure it out" | Pre-mortem; severity-4 → kill criterion or fix. |

## Cross-references

- → `references/playbooks/technical.md` — for system architecture
  side of operational concerns.
- → `references/playbooks/financial.md` — for the cost side of
  staffing and ops.
- → `references/playbooks/legal.md` — for contracts, employment,
  vendor agreements.
- → `references/playbooks/risk.md` — where operational
  severity-4 risks become kill criteria.
- → `references/core/severity-rubric.md` — for failure-mode scoring.
- → `references/core/fadr-framework.md` — for the F/A/D/R fold.
- → `templates/artifacts/operating-model.md` — the artifact this
  playbook produces under `investigate`.

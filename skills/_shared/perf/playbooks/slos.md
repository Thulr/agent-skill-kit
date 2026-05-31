# SLOs Playbook

## Scope

Service Level Indicators (SLIs), Service Level Objectives (SLOs),
error-budget policy, and the alerting that derives from them. Covers
SLI selection (latency, availability, correctness, freshness, durability,
throughput), SLO target setting, error-budget calculation, burn-rate
alerting, and the program-level governance that keeps SLOs aligned
with user experience.

## Grounding

- **SRE book (eds. 2016)** — the SLI / SLO / SLA framing; the Four
  Golden Signals as the minimum-coverage SLI set; error budgets as the
  bridge between reliability and feature velocity.
- **The Site Reliability Workbook (eds. 2018)** — practical SLI
  selection patterns, multi-window multi-burn-rate alerting, the
  governance of error-budget policy across teams.

## Good signals

- SLIs are chosen to reflect user-experienced outcomes (request
  success ratio at the user boundary, request latency at the user
  boundary), not internal-hop proxies.
- SLO targets are realistic — derived from measured baseline, not
  aspirational; matched to user expectations (and to the SLA, if
  one exists).
- Error budgets are explicit, calculated continuously, and visible to
  product and engineering both.
- Burn-rate alerting follows the multi-window multi-burn-rate pattern
  (catch fast and slow burn separately; suppress noise).
- Error-budget policy is written down: what happens when the budget
  is exhausted (feature freeze, reliability work prioritization,
  rollback default).
- SLOs are reviewed periodically; SLIs that drifted from user
  experience are replaced, not patched.
- Each SLO has a named owner.

## Common failures

- SLIs are chosen for what is easy to measure ("response 200 OK")
  rather than what the user experiences (request actually succeeded,
  latency at the user boundary).
- SLO targets are aspirational; the system has never met them, so the
  budget is always exhausted; the budget loses signal.
- Burn-rate alerting is single-threshold and fires on noise; on-call
  is paged for problems that resolve before anyone can act.
- Error-budget policy is implicit; budget exhaustion has no
  consequence, so the budget is not load-bearing.
- SLOs are set once and never reviewed; the SLI no longer reflects user
  experience but no one updates it.
- SLOs are an engineering-only artifact; product cannot see them, so
  reliability work is deprioritized.
- A surface has no SLO owner; nobody is accountable for the budget.

## Heuristics

- **SLI at the user boundary** *(design, audit, strategize)* — SLIs
  are measured where the user experiences the service, not at an
  internal hop. Success means the user got a valid result in time.
- **Realistic SLO target** *(design, strategize)* — SLO target is
  derived from measured baseline plus achievable improvement, not
  pulled from a slide.
- **Explicit, visible error budget** *(design, audit, strategize)* —
  the budget is calculated continuously and visible to product and
  engineering; this is the lever that makes reliability work
  prioritizable.
- **Multi-window multi-burn-rate alerting** *(design, audit, optimize)*
  — alert on fast burn (e.g., 14.4× over 1 hour) and slow burn (e.g.,
  3× over 6 hours) separately; suppress noise by requiring both a
  short-window and long-window threshold to trip.
- **Written error-budget policy** *(design, strategize)* — when the
  budget is exhausted, the policy specifies the consequence (feature
  freeze, reliability work prioritization, rollback default). The
  policy is signed off, not implied.
- **Periodic SLI / SLO review** *(strategize, audit)* — SLIs are
  reviewed (e.g., quarterly) against user experience; outdated
  indicators are replaced.
- **Named owner per SLO** *(design, audit)* — every SLO has a person
  or team accountable; orphan SLOs are unacceptable.
- **Avoid SLO ladder traps** *(design, strategize)* — do not set
  separate SLOs for every dependency hop; the user-facing SLO is the
  one that matters and others are diagnostic.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are SLIs measured at the user boundary? | Budget burn does not match user pain | Re-derive SLIs from user-experienced outcomes |
| Are SLO targets derived from measured baseline? | Targets are aspirational, budget is meaningless | Re-base SLOs on measured baseline + achievable improvement |
| Is the error budget visible to product and engineering? | Reliability has no lever | Surface the budget in product reviews |
| Is alerting multi-window multi-burn-rate? | Alerts fire on noise or miss real burn | Adopt the multi-window multi-burn-rate pattern |
| Is error-budget policy written down? | Budget exhaustion has no consequence | Draft the policy; sign off with product |
| Are SLOs reviewed periodically? | Indicators drift from user experience | Schedule quarterly SLI / SLO review |
| Does every SLO have a named owner? | Accountability is missing | Assign owners; orphan SLOs are findings |

## Cross-references

- → `latency.md` for latency SLI sourcing.
- → `metrics.md` for SLI source quality.
- → `tracing.md` for cross-service SLI attribution.
- → `logs.md` for event-derived SLI sources.

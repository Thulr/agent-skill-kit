# Operating Model — <opportunity-slug>

> Filled by `investigate` on `operational` surface, using
> `references/playbooks/operational.md`. **Delivery flow, support
> model, runbooks, staffing, vendor handoffs, monitoring, failure
> modes.**

## Opportunity statement

<one-line>

## Delivery / fulfillment flow

End-to-end, with handoffs and queues.

```
[Customer signs up]
    ↓
[Step 2: Activity X by role Y, queue depth Z, typical delay D]
    ↓
[Step 3: ...]
    ↓
[Value delivered]
```

| Step | Activity | Role / system | Queue depth | Typical delay | Edge cases |
|---|---|---|---|---|---|
| 1 | <…> | <…> | <…> | <…> | <…> |
| 2 | <…> | <…> | <…> | <…> | <…> |

## Support model

| Tier | Channel | SLA (response / resolution) | Cost / interaction | Trigger for escalation |
|---|---|---|---|---|
| T0 (self-serve) | <docs / FAQ / community> | <n/a> | $<X> | <bug / payment issue> |
| T1 (async) | <email / ticket> | <24h / 72h> | $<X> | <T0 fail / high-value account> |
| T2 (synchronous) | <chat / phone> | <1h / 24h> | $<X> | <T1 escalation / outage> |
| T3 (engineering) | <internal> | <on-call> | $<X> | <severity-1 outage> |

## Top-5 runbook inventory

| Event | Frequency | Has runbook? | Owner | Notes |
|---|---|---|---|---|
| Refund | <weekly?> | <yes/no — link> | <…> | <…> |
| Account dispute | <…> | <…> | <…> | <…> |
| Outage / incident | <…> | <…> | <…> | <…> |
| Privacy / DSR request | <…> | <…> | <…> | <…> |
| Payment failure | <…> | <…> | <…> | <…> |

## Staffing projection (12 months)

| Role | M0 | M3 | M6 | M9 | M12 | Notes |
|---|---|---|---|---|---|---|
| Engineering | <N> | <N> | <N> | <N> | <N> | <…> |
| Support | <…> | <…> | <…> | <…> | <…> | <…> |
| Sales | <…> | <…> | <…> | <…> | <…> | <…> |
| Customer success | <…> | <…> | <…> | <…> | <…> | <…> |
| Finance / ops | <…> | <…> | <…> | <…> | <…> | <…> |
| Hidden labor (content / legal / compliance) | <…> | <…> | <…> | <…> | <…> | <…> |

## Vendor handoffs

| Vendor | Role | SLA | Fallback procedure | Switching cost / time |
|---|---|---|---|---|
| <e.g., payment provider> | <…> | <99.9% / 24h> | <…> | <high / 3mo> |
| <e.g., email delivery> | <…> | <…> | <…> | <…> |
| <e.g., cloud provider> | <…> | <…> | <…> | <…> |

## Business monitoring (separate from system monitoring)

| Metric | Target | Alert threshold | Channel |
|---|---|---|---|
| Orders / day | <…> | <±20%> | <slack / pagerduty> |
| Support tickets / day | <…> | <…> | <…> |
| Churn cohort signal | <…> | <…> | <…> |
| Refund rate | <…> | <…> | <…> |
| Time-to-activation | <…> | <…> | <…> |

(System monitoring — uptime, latency, errors — is out of scope for this
artifact.)

## Failure modes (≥5 pre-mortemed)

| Failure | Severity | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| <e.g., support backlog blows out> | <…> | <…> | <…> | <…> |
| <e.g., vendor X has multi-day outage> | <…> | <…> | <…> | <…> |
| <e.g., content moderation event> | <…> | <…> | <…> | <…> |
| <e.g., onboarding regression after migration> | <…> | <…> | <…> | <…> |
| <e.g., compliance audit miss> | <…> | <…> | <…> | <…> |

## Bottleneck analysis

What's the throughput-limiting bottleneck at projected volume?

- **At month 6 volume:** <bottleneck>
- **Mitigation:** <hire / automate / vendor / reduce scope>
- **At month 12 volume:** <bottleneck>
- **Mitigation:** <…>

## F/A/D/R

### Facts

- <e.g., "comparable ops team at company X runs at 1 ops / 200
  customers for tier-2 support, source: <interview>">

### Assumptions

- <e.g., "assume self-serve handles 70% of tier-1 questions; test:
  measure deflection rate in first 30 days of beta">

### Decisions

- <e.g., "launch with async-only support; spec synchronous tier
  for month-6 if enterprise pipeline materializes">

### Risks

- <e.g., "severity-3: hidden labor underestimated; mitigation:
  monthly labor audit; kill criterion: ops labor / revenue > 30%">

## Next test

<one falsifiable experiment — usually a load-test of the planned
support model or a runbook tabletop exercise>

## Sources

| # | Source | Type | Confidence |
|---|---|---|---|
| 1 | <…> | <…> | <H/M/L> |

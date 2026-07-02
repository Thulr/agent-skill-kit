# Technical Feasibility — <opportunity-slug>

> Filled by `investigate` on `technical` surface, using
> `references/opportunity/playbooks/technical.md`. **Three architecture options
> with named tradeoffs minimum.**

## Opportunity statement

<one-line>

## Functional scope (what must the system do)

- Capability 1: <e.g., "ingest documents from 5 storage backends">
- Capability 2: <e.g., "extract structured fields with confidence">
- Capability 3: <…>

## Non-functional requirements

| Attribute | Target | Critical? |
|---|---|---|
| p50 latency | <…> | <yes/no> |
| p95 latency | <…> | <yes/no> |
| p99 latency | <…> | <yes/no> |
| Throughput | <…> | <yes/no> |
| Availability | <99.9% / 99.99%> | <…> |
| Cost ceiling | $<X> per <unit> | <…> |
| Data residency | <…> | <…> |
| Compliance | <SOC 2 / HIPAA / PCI / GDPR> | <…> |

## Architecture options (≥3)

### Option A: <name>

- **Approach:** <description>
- **Components (build vs buy):** | Component | Build / Buy | Reason |
- **Pros:** <…>
- **Cons:** <…>
- **Estimated cost:** <…>
- **Estimated time to ship MVP:** <weeks>
- **Estimated maintenance burden at 12mo:** <hrs/wk>

### Option B: <name>

- **Approach:** <…>
- **Components:** <…>
- **Pros:** <…>
- **Cons:** <…>
- **Estimated cost:** <…>
- **Time to MVP:** <…>
- **Maintenance at 12mo:** <…>

### Option C: <name>

- **Approach:** <…>
- ...

## Build-vs-buy decisions (per component)

| Component | Decision | Reason | Vendor (if buy) | Switching cost |
|---|---|---|---|---|
| Authentication | Buy | Commodity | Auth0 / Clerk / WorkOS | Med |
| Payments | Buy | Commodity + regulatory | Stripe / Adyen | High |
| Core <differentiator> | Build | Load-bearing differentiator | n/a | n/a |
| Observability | Buy | Commodity | Honeycomb / Datadog | Low |
| <component> | <…> | <…> | <…> | <…> |

## Spike plan (riskiest assumption)

The technical risk that, if it fails, kills the bet:

- **Risk:** <e.g., "third-party API rate limits cap throughput at
  1k/hr; we need 100k/hr">
- **Spike:** <one-week prototype to test feasibility>
- **Success threshold:** <e.g., "sustain 100 req/sec for 5 min in
  a synthetic test">
- **Owner / deadline:** <…>

## Performance budget (percentile not average)

| Path | p50 target | p95 target | p99 target | Source of estimate |
|---|---|---|---|---|
| <critical path 1> | <…> | <…> | <…> | <load test / benchmark> |
| <…> | <…> | <…> | <…> | <…> |

## Security threat model (attacker × asset × surface)

| Attacker | Asset | Surface | Mitigation |
|---|---|---|---|
| <e.g., curious user> | <PII> | <web> | <e.g., row-level auth> |
| <e.g., malicious user> | <other users' data> | <API> | <…> |
| <e.g., compromised peer> | <internal services> | <internal API> | <…> |
| <e.g., nation-state> | <crown-jewels> | <all> | <…> |

## Maintenance projection (6 / 12 / 18 months)

| Aspect | At 6mo | At 12mo | At 18mo |
|---|---|---|---|
| Engineering hours / week | <…> | <…> | <…> |
| Open-source dep update burden | <…> | <…> | <…> |
| Vendor SLA management | <…> | <…> | <…> |
| Technical debt added | <…> | <…> | <…> |
| Compatibility / version skew | <…> | <…> | <…> |

## Scalability path

What changes when load hits 10× / 100× / 1000×.

| Multiplier | What breaks first | Required change | Estimated lead time |
|---|---|---|---|
| 10× | <…> | <…> | <…> |
| 100× | <…> | <…> | <…> |
| 1000× | <…> | <…> | <…> |

## Recommendation

**Picked:** Option <A/B/C>.

Reason (in 3 sentences): <…>.

## F/A/D/R

### Facts

- <e.g., "third-party API has documented 1k req/hr free-tier limit;
  paid tier $X/mo for 100k/hr; source: vendor docs">

### Assumptions

- <e.g., "vendor rate limit will not drop in next 12mo; test: track
  vendor announcements quarterly + maintain fallback adapter">

### Decisions

- <e.g., "build proprietary <component> in-house; buy everything
  else; spike vendor X for 1 week before committing">

### Risks

- <e.g., "severity-4: spike fails — fall back to Option B which is
  slower and costlier; kill criterion: if Options A and B both fail
  spike, bet is technically infeasible">

## Next test

<the spike planned above; or another <1-week experiment that closes
the top technical assumption>

## Sources

| # | Source | Type | Confidence |
|---|---|---|---|
| 1 | <…> | <…> | <H/M/L> |

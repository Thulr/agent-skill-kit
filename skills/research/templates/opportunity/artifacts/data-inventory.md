# Data Inventory — <opportunity-slug>

> Filled by `investigate` on `data` surface, using
> `references/opportunity/playbooks/data.md`. **9-axis inventory required: source
> / access / ownership / quality / coverage / freshness / labels /
> governance / instrumentation gaps.**

## Opportunity statement

<one-line>

## Use case

What the data is for: <e.g., "train churn-prediction model" / "power
recommendation feed" / "feed compliance dashboard" / "drive billing
calculation">

## Data inventory (per source)

### Source 1: <name>

| Axis | Detail |
|---|---|
| **Source** | <vendor / internal / public / partner / scraped> |
| **Access** | <API / file dump / partnership / scrape / purchase> |
| **Access established?** | <yes — contract, link / no — pending> |
| **Ownership** | <who controls it; revocation risk> |
| **Quality (completeness, accuracy, consistency)** | <H/M/L per dim> |
| **Coverage** | <represents which population — and what's missing> |
| **Freshness** | <real-time / batch <freq> / monthly / yearly / stale> |
| **Labels / ground truth** | <yes/no; if yes, freshness + quality> |
| **Schema** | <usable as-is / needs transformation; link to schema> |
| **Governance (PII / consent / retention / DSR / lineage / audit)** | <details> |
| **Instrumentation gaps** | <what's missing that we'd need to add> |
| **Concentration share** | <% of total data we'd depend on from this source> |
| **Confidence** | <H/M/L> |

### Source 2: <name>

| Axis | Detail |
|---|---|
| **Source** | <…> |
| **Access** | <…> |
| ...same 12 rows...

### Source 3: <name>

(repeat)

## Coverage / representativeness check

Does the union of sources represent the population we'll predict /
serve / report on?

- **Population we serve:** <description>
- **Population our data represents:** <description>
- **Selection bias risk:** <how trained-only-on-X distorts predictions
  about non-X>
- **Mitigation:** <re-sample / re-weight / collect more / acknowledge
  scope>

## Label freshness × domain change rate

- **Domain change rate:** <how fast underlying truth shifts — slow /
  med / fast>
- **Label age:** <weeks / months / years>
- **Label quality given age:** <H / M / L>
- **Re-label plan if L:** <approach + cost + timeline>

## Privacy / governance

| Data kind | PII? | Consent basis | Retention | DSR rights | Audit trail | Residency |
|---|---|---|---|---|---|---|
| <kind> | <yes/no> | <consent / contract / legitimate interest / legal> | <e.g., 3 yrs> | <yes/no> | <yes/no> | <region> |
| <…> | <…> | <…> | <…> | <…> | <…> | <…> |

(Route to `legal.md` for compliance verification.)

## Concentration risk

- **>50% from one source?** <yes/no — name source>
- **Failure scenarios:**
  - Source rate-limits: <consequence + fallback>
  - Source raises price: <consequence + fallback>
  - Source changes terms: <consequence + fallback>
  - Source disappears: <consequence + fallback>

## Instrumentation plan (for gaps)

What's missing that we need to start collecting?

| Gap | Why needed | Collection approach | Lead time | Cost |
|---|---|---|---|---|
| <gap> | <use case> | <event log / form / API call> | <weeks> | <eng-weeks / $> |

## F/A/D/R

### Facts

- <e.g., "Source X has 5M rows, last refreshed 2026-04-01, schema
  documented at <link>">

### Assumptions

- <e.g., "assume vendor Y maintains current free-tier access; test:
  re-confirm quarterly via API behavior + vendor comms">

### Decisions

- <e.g., "use Source A as primary; instrument event Z to reduce
  Source B dependency; defer Source C until labels improve">

### Risks

- <e.g., "severity-3: Source A concentration >60% — mitigation: build
  Source B adapter in parallel; owner: <…>">

## Next test

<the highest-leverage data assumption — usually a quality / coverage
audit on one source or a re-labeling pilot>

## Sources

| # | Source | Type | Confidence |
|---|---|---|---|
| 1 | <…> | <…> | <H/M/L> |

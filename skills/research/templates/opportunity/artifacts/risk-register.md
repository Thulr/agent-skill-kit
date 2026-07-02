# Risk Register — <opportunity-slug>

> Filled by `investigate` on `risk` surface, using
> `references/opportunity/playbooks/risk.md`. **Categorize by source. Score
> severity × likelihood × confidence. Mitigations have success
> thresholds. Severity-4 risks become kill criteria or have mitigations
> with thresholds.**

## Opportunity statement

<one-line>

## Pre-mortem narrative

> Imagine it's 18 months from now. The opportunity failed. Working
> backwards, what happened?

<2–5 sentence narrative tying together the most plausible failure
path. Each plausible cause maps to a row in the register below.>

## Outside-view base rates

What's the base rate for comparable bets reaching scale?

| Comparable category | % reaching <threshold> | Median time | Source |
|---|---|---|---|
| <e.g., B2B SaaS in this segment> | <%> | <years> | <…> |
| <e.g., consumer marketplace> | <%> | <years> | <…> |

Inside-view forecasts that exceed base rates by 2× need outside-view
justification.

## Risk register

ID format: `OR-risk-NNN`. Each row:

| ID | Risk | Category | Severity (0–4) | Likelihood (L/M/H) | Confidence in assessment | Mitigation (with threshold) | Owner | Status | Last review |
|---|---|---|---|---|---|---|---|---|---|
| OR-risk-001 | <…> | <assumption / market / execution / technical / operational / financial / legal / platform / fraud / reputation / concentration> | <0–4> | <L/M/H> | <H/M/L> | <e.g., "Customer A renewal rate above 80% by month 12; otherwise pivot ICP"> | <@founder> | <open / in-progress / mitigated / kill-criterion> | <date> |
| OR-risk-002 | <…> | <…> | <…> | <…> | <…> | <…> | <…> | <…> | <…> |
| OR-risk-003 | <…> | <…> | <…> | <…> | <…> | <…> | <…> | <…> | <…> |

(Aim for 10+ rows for a serious investigation; 5+ minimum.)

## Concentration risks (first-class category)

Any single customer / channel / vendor / data source / regulatory
regime contributing > 30% — surface explicitly even if other
indicators are green.

| Concentration | % of total | Severity | Mitigation |
|---|---|---|---|
| <e.g., Customer X> | <%> | <…> | <…> |
| <e.g., Channel Y> | <%> | <…> | <…> |
| <e.g., Vendor Z> | <%> | <…> | <…> |

Concentration > 50% on any axis → severity ≥ 3.

## Severity-4 disposition

Every severity-4 risk MUST be one of:

| ID | Risk | Disposition | Detail |
|---|---|---|---|
| <id> | <…> | <resolved> | <how + evidence> |
| <id> | <…> | <mitigated to threshold> | <threshold + monitoring> |
| <id> | <…> | <kill criterion> | <observable + date + witness> |

No severity-4 risk is allowed to "hang" — that's the named failure
mode.

## Antifragile structural changes

Beyond mitigating each risk, can the structure be changed so the same
external event helps rather than hurts?

| Risk | Antifragile change | Mechanism |
|---|---|---|
| <e.g., vendor lock-in> | <multi-vendor adapter from day 1> | <optionality> |
| <e.g., channel concentration> | <invest in asset layer> | <diversification> |
| <e.g., regulatory shift> | <reversible pricing / packaging> | <reversibility> |

## F/A/D/R

### Facts

- <e.g., "comparable category base rate for reaching $1M ARR: 30%
  in 24 months, source: <…>; we project month 18">

### Assumptions

- <e.g., "assume vendor X maintains current terms for 18 months;
  test: quarterly vendor health check">

### Decisions

- <e.g., "build channel diversification before scale; commit to SOC 2
  Type I by month 6; cap customer concentration at 30%">

### Risks

- (this entire artifact is the risk inventory)

## Next test

<one falsifiable risk-mitigation experiment — usually testing the
top severity assumption or stress-testing a key mitigation>

## Sources

| # | Source | Type | Confidence |
|---|---|---|---|
| 1 | <…> | <…> | <H/M/L> |

## Cross-references

- All other area artifacts surface risks; this register catalogs them.
- Severity-4 rows feed `fadr-memo.md`'s kill criteria.
- For deep backwards-from-failure analysis: hand off to the
  `premortem` skill.

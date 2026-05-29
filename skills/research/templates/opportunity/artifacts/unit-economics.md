# Unit Economics — <opportunity-slug>

> Filled by `investigate` on `financial` surface, using
> `references/playbooks/financial.md`. **Not investment advice. Not
> audited figures. Best / base / worst-case modeling only.**

## Opportunity statement

<one-line>

## Business model

| Field | Value |
|---|---|
| Revenue model | <subscription / usage / transaction / marketplace / license / one-time> |
| Pricing model | <per-seat / per-usage / per-transaction / tiered / bundled / freemium> |
| Average revenue per unit (ARPU) | $<X> / <period> |
| Pricing tiers | <list with "best for" criteria> |
| Sales motion | <PLG / inside sales / field sales / partnership> |

## COGS itemized

Cost to deliver one unit of the product.

| Cost component | Per-unit cost | Notes |
|---|---|---|
| Infrastructure | $<X> | <e.g., compute + storage + bandwidth> |
| Third-party APIs | $<X> | <e.g., LLM tokens, payments, identity> |
| Labor (delivery) | $<X> | <support hours × rate / unit> |
| Payment processing | $<X> | <e.g., 2.9% + $0.30> |
| Refunds / chargebacks | $<X> | <% × refund rate> |
| Other | $<X> | <…> |
| **Total COGS** | **$<X>** | |
| **Gross margin** | **<%>** | (revenue − COGS) / revenue |

## CAC (blended)

| Cost | Amount per month | Notes |
|---|---|---|
| Ad spend | $<X> | <…> |
| Marketing labor | $<X> | <salaries + content> |
| Sales labor | $<X> | <…> |
| Tooling | $<X> | <…> |
| Content production | $<X> | <…> |
| **Total acquisition cost / mo** | **$<X>** | |
| New customers / mo | <N> | <…> |
| **CAC** | **$<X>** | total / new customers |

## Retention / churn

| Metric | Value | Source / confidence |
|---|---|---|
| Monthly churn (gross) | <%> | <cohort data / benchmark / estimate, H/M/L> |
| Monthly churn (net of expansion) | <%> | <…> |
| Net revenue retention | <%> | <…> |

## LTV

- **Method:** LTV = ARPU × gross margin / monthly churn (SaaS).
  Adapt per model.
- **Calc:** $<ARPU> × <margin%> / <churn%> = **$<LTV>**
- **Confidence:** <H/M/L> based on churn anchor

## Payback period

- **Months until CAC recovered from gross margin:** <N>
- **Benchmark:** SaaS base < 12mo. Capital-intensive / enterprise: up to 24mo.

## LTV / CAC ratio

- **Ratio:** $<LTV> / $<CAC> = **<X>x**
- **Benchmark:** > 3 in base case.
- **If < 3:** diagnose — price, CAC, churn, margin (named fix).

## 24-month cash flow (monthly)

| Month | Revenue | COGS | Gross profit | Opex (incl. CAC) | Net | Cumulative cash |
|---|---|---|---|---|---|---|
| M0 | <…> | <…> | <…> | <…> | <…> | <starting capital> |
| M1 | <…> | <…> | <…> | <…> | <…> | <…> |
| M6 | <…> | <…> | <…> | <…> | <…> | <…> |
| M12 | <…> | <…> | <…> | <…> | <…> | <…> |
| M18 | <…> | <…> | <…> | <…> | <…> | <…> |
| M24 | <…> | <…> | <…> | <…> | <…> | <…> |

- **Cash runway:** <N> months
- **Break-even at:** month <N>

## Scenarios

### Best case

- ARPU + <X>%, Churn − <Y>%, CAC − <Z>%
- LTV/CAC: <X>x. Payback: <N>mo.
- Drivers: <what would have to be true>

### Base case (above)

- LTV/CAC: <X>x. Payback: <N>mo. Runway: <N>mo.

### Worst case

- ARPU − <X>%, Churn + <Y>%, CAC + <Z>%
- LTV/CAC: <X>x. Payback: <N>mo. Runway: <N>mo (may be negative).
- Drivers (what would land us here): <…>

## Sensitivity to downside

Which 1–2 variables, if they move adversely, push us to worst case?

| Variable | Movement | Effect |
|---|---|---|
| <e.g., churn> | <+50%> | <LTV halves; LTV/CAC drops to 1.5x — broken> |
| <e.g., CAC> | <+30%> | <payback to 22mo; cash flow worsens; runway shortens> |

## Scale break-points

What changes at 1× / 10× / 100×?

| Scale | New cost | Reason |
|---|---|---|
| 1× | <baseline> | <…> |
| 10× | + sales team + CRO + SOC 2 audit | <…> |
| 100× | + regional expansion + finance / legal hires | <…> |

## F/A/D/R

### Facts

- <e.g., "comparable SaaS in this segment: ARPU $X, churn Y%, gross
  margin Z%, source: public 10-K">

### Assumptions

- <e.g., "assume churn = 5% / month (benchmark); test: cohort
  retention in first 90 days of paid pilots">

### Decisions

- <e.g., "price at $99/mo per seat (tier 1); $499/mo team tier;
  enterprise custom>

### Risks

- <e.g., "severity-3: churn underestimated; mitigation: cohort
  analysis monthly; kill criterion: 6-mo churn > 10%">

## Next test

<one falsifiable experiment — usually a paid pilot with measured
retention, a price-ladder test, or a CAC measurement on one channel>

## Sources

| # | Source | Type | Confidence |
|---|---|---|---|
| 1 | <…> | <…> | <H/M/L> |

## Disclaimers

This is best/base/worst-case modeling, not audited figures. Not
investment advice. Numbers carry their listed confidence and source.

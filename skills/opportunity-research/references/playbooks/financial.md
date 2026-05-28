# Financial Playbook

## Scope

Whether the economics make sense — pricing, costs, margins, CAC, LTV,
payback period, cash flow, scenarios. Financial research is what
separates "people will use it" from "this can be a business." The
playbook produces best / base / worst-case modeling, not audited
figures. It is **not** investment advice.

- In: revenue model, pricing model, cost structure, COGS, gross
  margin, CAC, retention / churn, LTV, payback period, cash flow
  shape, scenario analysis (best / base / worst).
- Out: market sizing (`market.md`), legal / tax implications
  (`legal.md`), operational staffing cost detail (`operational.md`),
  channel acquisition mechanics (`channel.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **David Skok — *SaaS Metrics 2.0* (2013, forEntrepreneurs.com)** —
  canonical SaaS unit-economics framing: CAC, LTV, payback,
  gross margin, magic number, with the LTV/CAC > 3 and
  payback < 12mo benchmarks.
- **Brian Balfour — *Four Fits for $100M+ Growth* (2017)** — the
  model / market fit (LTV must support paid acquisition) and the
  channel / model fit (channel cost must support price tier).
- **Aswath Damodaran's published unit-economics frameworks** —
  scenario analysis (best / base / worst) and sensitivity to
  downside as a discipline.
- **Convo.txt** — "What you want out of this: a business that can
  survive reality. Not just 'people like it,' but 'this makes
  economic sense'."

## Good signals

- Revenue model is named (subscription / usage / transaction /
  marketplace / license / one-time) with the pricing model under
  it (per-seat / per-usage / per-transaction / tiered / bundled).
- COGS is itemized — infra, third-party, labor to deliver, payment
  processing, refunds / chargebacks. Gross margin = (revenue −
  COGS) / revenue.
- CAC is computed *blended* (all-in costs of acquiring an average
  customer, including marketing salaries + content + ads).
- LTV is computed with churn assumptions explicit. (LTV =
  ARPU × gross margin / monthly churn — for SaaS; adapt per model.)
- Payback period < 12 months in base case for SaaS; longer is OK
  for capital-intensive / enterprise / sticky.
- LTV / CAC > 3 in the base case. < 3 = something is broken.
- Cash flow is modeled monthly for at least 24 months, with cash
  runway named.
- Best / base / worst-case scenarios are present, with named
  drivers between them.
- "Sensitivity to downside" is named: which 1–2 variables would
  cause base → worst, and what would have to be true to land
  there.

## Common failures

- **Pricing chosen by feel.** No comparable benchmark, no
  willingness-to-pay test, no value anchor. Mitigation: anchor on
  comparables AND on customer value (savings vs cost).
- **CAC omits salaries and content.** A "we'll do content marketing"
  CAC that ignores the marketing salary is a fantasy. Blended CAC
  includes all costs.
- **LTV computed at zero churn.** LTV = ARPU × gross margin / churn;
  churn → 0 = LTV → infinity. Mitigation: use a credible churn
  assumption (cohort data, comparable benchmark, expert estimate)
  and tag confidence.
- **Best-case-only modeling.** Forward models that show
  hockey-stick growth without naming what would make them break.
  Mitigation: name 1–2 sensitivity drivers; show worst case.
- **Ignoring payback period.** LTV/CAC > 3 with payback > 24mo
  means capital-intensive, even if the long-run economics work.
  Cash kills before unit economics fix it.
- **Confusing GMV with revenue.** Marketplace / payments / take-rate
  businesses are paid the take, not the GMV. Top-line vanity inflates
  perceived size.
- **Missing recurring costs.** Sales commission, customer success
  staffing, refunds, compliance fees, certification renewal,
  insurance — all of these compound and many are missed in v1
  models.
- **Cost model omits scale break-points.** What changes when you
  hit 1× / 10× / 100×: do you need a sales team, a CRO, a finance
  hire, SOC2 audit, regional expansion.

## Heuristics

- **(scope, investigate)** *Pick the revenue + pricing model
  explicitly.* Subscription / usage / transaction / marketplace /
  license / one-time. Pricing under it: per-seat / per-usage /
  tiered / bundled / freemium.
- **(investigate)** *Itemize COGS.* Infra, third-party, labor to
  deliver, payment processing, refunds / chargebacks. Compute
  gross margin per unit.
- **(investigate)** *Blended CAC.* All-in: ads, marketing labor,
  content, sales labor (if applicable), tooling. Avoid
  paid-spend-only CAC.
- **(investigate, decide)** *LTV with explicit churn.* (LTV =
  ARPU × gross margin / monthly churn for SaaS; adapt for other
  models). Churn anchored to cohort data, comparable benchmark, or
  expert estimate — tagged H / M / L confidence.
- **(investigate, decide)** *Payback period named.* Months until
  CAC is recovered from gross margin. Benchmark: < 12mo for SaaS
  base; longer OK for capital-intensive / enterprise.
- **(investigate, decide)** *LTV / CAC > 3 in base case.* Below
  that, something is broken (price too low, CAC too high, churn
  too high, gross margin too thin).
- **(investigate)** *24-month cash-flow model.* Monthly, with cash
  runway and break-even named. Negative cash cures slowly.
- **(investigate, decide)** *Best / base / worst with named
  drivers.* What 1–2 variables move base to worst? What would
  have to be true?
- **(decide)** *Sensitivity to downside.* If the downside is
  existential and likely, the unit economics don't yet support the
  bet.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are revenue and pricing models named explicitly? | "We'll figure out pricing" | Pick; benchmark; anchor on value. |
| Is COGS itemized with gross margin computed? | Lump-sum cost | Itemize; compute gross margin per unit. |
| Is CAC blended (all-in)? | Paid-spend-only CAC | Re-compute with labor + content + tooling. |
| Is LTV computed with explicit, anchored churn? | LTV at zero churn | Anchor churn; tag confidence; recompute. |
| Is payback period named (< 12mo base for SaaS)? | Silent on payback | Compute; if > 24mo, mark as capital-intensive. |
| Is LTV / CAC > 3 in base case? | < 3 | Diagnose: price / CAC / churn / margin. Don't proceed without naming the fix. |
| Is the 24-month cash-flow model present? | Annualized only | Re-do monthly; surface runway and break-even. |
| Are best / base / worst scenarios with named drivers? | Best-case only | Add worst; name 1–2 sensitivity drivers. |

## Cross-references

- → `references/playbooks/market.md` — for the SAM / SOM the
  revenue model is sized against.
- → `references/playbooks/channel.md` — for CAC by channel and
  channel / model fit.
- → `references/playbooks/operational.md` — for the labor side of
  COGS.
- → `references/playbooks/risk.md` — where financial severity-4
  risks (runway, concentration) become kill criteria.
- → `references/core/severity-rubric.md` — for risk scoring.
- → `references/core/fadr-framework.md` — for the F/A/D/R fold.
- → `templates/artifacts/unit-economics.md` — the artifact this
  playbook produces under `investigate`. **Note:** the artifact
  carries the "not investment advice / not audited figures" marker.

# Data Playbook

## Scope

Whether the data needed for the opportunity exists, is reachable, is
clean enough, and represents the problem fully. Especially load-bearing
for AI / ML / analytics opportunities — many "AI ideas" are really
data-availability problems wearing AI clothing.

- In: data inventory by source, access rights, ownership, quality,
  coverage, freshness, labels / ground truth, schema, governance
  (privacy, retention, lineage, audit), instrumentation gaps.
- Out: data-system architecture (`technical.md`), data privacy
  /  compliance regulation (`legal.md`), operational data
  monitoring (`operational.md`), AI model behavior /  product
  feasibility (`technical.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **Cathy O'Neil — *Weapons of Math Destruction* (2016)** — data
  encodes the world it was collected from, including its biases.
  Quality includes representativeness.
- **The DAMA Body of Knowledge (DMBOK)** — data quality dimensions
  (completeness, accuracy, consistency, freshness, validity,
  uniqueness) as a structured assessment frame.
- **Convo.txt** — "A lot of 'AI ideas' are really just data
  availability problems in disguise" — the load-bearing principle
  this playbook enforces.
- **Privacy by Design (Ann Cavoukian 2009)** — privacy as a
  data-system constraint, not a launch-blocker; embed it.

## Good signals

- Data is inventoried by source × access × ownership × quality ×
  coverage × freshness × labels × governance × instrumentation gaps.
  Each row has a confidence tag.
- Access is established (not assumed) — written down with the
  contract / agreement / API key / scrape policy.
- Labels exist and are recent. "We'll label later" is a data
  problem in disguise.
- Coverage is named explicitly: does the data represent the full
  problem space, or only the slice we have access to.
- Freshness is appropriate to the use case: real-time / batch /
  monthly / yearly. Mismatch is a silent failure mode.
- Governance is named: PII present? Retention rules? Lineage
  traceable? Audit log? Privacy policy compatible with this use?
- Concentration: a single source providing >50% of the data is a
  risk class (rate-limit, terms change, vendor disappears).

## Common failures

- **AI idea that's actually a data idea.** "We'll train a model" without
  knowing if the labeled data exists. Mitigation: data inventory
  before model architecture.
- **Stale labels treated as ground truth.** Two-year-old labels in a
  fast-changing domain are nearly indistinguishable from no labels.
- **Coverage gap silently inherited.** Training only on customers
  who used feature X then predicting for those who didn't =
  selection bias.
- **Access by assumption.** "We can scrape this" / "we can buy
  this" / "we can ask for this" without checking. Each is a
  legal / commercial / technical question, not a given.
- **Concentration ignored.** All training data from one source =
  one rate-limit or terms change kills the product.
- **Privacy / compliance retrofit.** Building on data that turns
  out to need consent / DSR / retention controls you don't have.
- **Instrumentation gaps treated as data quality issues.** "Our data
  is messy" is sometimes "we don't collect what we need" — these
  need different fixes.

## Heuristics

- **(scope, investigate)** *Inventory by 9 axes.* Source / access /
  ownership / quality / coverage / freshness / labels / governance
  / instrumentation gaps. One row per data source. Confidence on
  every cell.
- **(investigate)** *Access is a contract, not a claim.* For each
  source: how do we have access (purchase, API, scrape, partnership,
  internal), under what terms, with what revocation risk.
- **(investigate, decide)** *Label freshness has a half-life.*
  Domain change-rate × label-age = label quality. Old labels in
  fast-changing domains are L-confidence by default.
- **(investigate)** *Coverage = representativeness.* Does the data
  represent the full population we're predicting for, or only the
  trained-on slice? Selection bias is silent until it bites.
- **(investigate)** *Freshness matched to use case.* Real-time
  decisioning needs real-time data; quarterly insight is fine
  weekly. Mismatch on either side is a silent failure.
- **(investigate, decide)** *Concentration risk.* If one source is
  >50% of the data, model 30% loss (rate limit, terms change,
  outage) in the risk register.
- **(investigate)** *Governance up front.* PII, consent, retention,
  DSR rights, lineage, audit log. Retrofits cost 10×.
- **(decide)** *Instrumentation plan.* What's missing now that we
  need to start collecting? Time-to-data is a real project cost.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the data inventoried across 9 axes per source? | Partial inventory | Complete; confidence on each cell. |
| Is access established (contract / API / agreement), not assumed? | "We can get it" | Establish; document; revocation risk noted. |
| Are labels recent enough for the domain's change rate? | Old labels | Re-label or downgrade confidence to L. |
| Is coverage representative of the prediction population? | Trained-only-on-slice | Quantify gap; flag as Assumption + test. |
| Is freshness matched to the use case? | Mismatch | Re-spec the freshness; model the gap. |
| Is concentration risk modeled (>50% single source)? | Silent concentration | Add to risk register; severity ≥3. |
| Is governance (PII / consent / retention / lineage) named? | Retrofit pending | Spec now; estimate retrofit cost if late. |
| Is the instrumentation plan named for what's missing? | "Our data is messy" | Separate quality from instrumentation; spec collection. |

## Cross-references

- → `references/opportunity/playbooks/technical.md` — for data-system
  architecture and feasibility.
- → `references/opportunity/playbooks/legal.md` — for privacy / consent /
  retention / compliance.
- → `references/opportunity/playbooks/operational.md` — for ongoing data
  monitoring and quality.
- → `references/opportunity/playbooks/risk.md` — where data concentration
  becomes a tracked risk.
- → `references/opportunity/core/confidence-rubric.md` — for labeling claim
  confidence (and the auto-promotion of L).
- → `references/opportunity/core/fadr-framework.md` — for the F/A/D/R fold.
- → `templates/opportunity/artifacts/data-inventory.md` — the artifact this
  playbook produces under `investigate`.

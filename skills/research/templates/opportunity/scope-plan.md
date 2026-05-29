# Scope Plan — <opportunity-slug>

> Output of the `scope` intent. Saved when the user accepts the
> scoping. Subsequent `investigate` runs consume this plan.

## Opportunity statement

<one-line statement: "build a <product/service> for <segment> that
solves <job> via <approach>">

## Stage

<one of: pre-idea | idea | validation | build | launch | scale>

Reason: <why this stage; what's already known vs unknown>

## Audience for this plan

<who reads this — founder, board, team, investor, internal review>

## Recommended area subset (in priority order)

For each area in scope, name the rationale and the depth.

| # | Area | Why now | Depth (light / standard / deep) | Lead persona |
|---|---|---|---|---|
| 1 | <area> | <rationale> | <depth> | <founder / operator / investor / skeptic> |
| 2 | … |  |  |  |
| 3 | … |  |  |  |

Default first-pass at each stage (from `references/subagent-dispatch.md`):

- **Pre-idea:** customer, domain, trend
- **Idea:** customer, market, competitive, domain
- **Validation:** + technical, financial
- **Build:** + operational, data, risk
- **Launch:** + channel, gtm, legal, stakeholder
- **Scale:** all 14

## Areas explicitly deferred (out of scope for this iteration)

| Area | Reason deferred | When to revisit |
|---|---|---|
| <area> | <reason> | <stage / milestone> |

## Sequence of intents

Recommended order:

1. `investigate` with surface = <chosen> or `all` over the subset above
   (fans out one sub-agent per area).
2. `synthesize` row = `bundle` (or `by-stage` / `investor-brief`).
3. `decide` row = `go-no-go` (or `kill-criteria` / `pivot`).

## Persona lenses

Default: <founder + skeptic / all four / operator + investor>. Reason:
<why this lens combination for this opportunity / stage>.

## Time & cost estimate

| Step | Effort | Notes |
|---|---|---|
| Investigate subset above | <hrs / days> | <parallel via sub-agents> |
| Synthesize | <hrs> | <after artifacts exist> |
| Decide | <hrs> | <when ready for the call> |

## F/A/D/R fold (scope-level)

### Facts (what we know about the scope)

- <fact, confidence H/M/L, source>

### Assumptions (about the scope itself, not the opportunity)

- <assumption, leverage, test>

### Decisions (what this plan commits to)

- <decision: include area X, defer area Y, sequence Z>

### Risks (of mis-scoping)

- <risk that we under-scoped some area; severity, mitigation>

## Next test

<one falsifiable next action that closes the highest-leverage scope
assumption — typically the first area to investigate or the first
customer / user interview>

## Sources

- <source name, link, contribution to this scoping decision>

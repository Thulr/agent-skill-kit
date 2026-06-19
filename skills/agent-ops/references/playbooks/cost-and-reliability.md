# Cost and Reliability Playbook

## Scope

Operating the reliability and cost of an agent system already in production: keeping a multi-step agent's end-to-end success rate above the floor its per-step quality implies, holding token and iteration spend inside enforced budgets, gating releases on decomposed per-slice scoring rather than one aggregate number, and degrading gracefully when load or budget pressure hits instead of failing hard or silently overspending.

- **In:** end-to-end success-rate math (the march of nines), cost/iteration circuit-breakers and token budgets, release gates decomposed by failure mode (guardrail vs north-star), per-slice scoring against a baseline with a rollback threshold, graceful degradation under load/budget pressure.
- **Out:** designing the eval suites and LLM judges those gates consume (see `agent-test`); building the SDK that emits the spans and exposes the budget knobs (see `agent-dx`); writing the agent-native docs (see `agent-docs`); scaffolding repo gates and hooks (see `harden-repo-for-coding-agents`).
- **Intents this surface answers:** do, review, design.

## Grounding

- **Per-step quality compounds multiplicatively across a trajectory.** A step that passes 95% of the time, repeated across a multi-step agent, lands end-to-end success far below 95% — a 20-step run at 0.95/step is roughly 0.36. Reliability is a product, not an average; this is the operator's "march of nines."
- **An aggregate pass-rate is a lossy summary.** A single number can hold steady while a specific slice collapses, and it conflates two regressions with opposite ship decisions: a guardrail breach (safety, cost, side-effects) must block, while a north-star/capability dip is report-only. Operators decompose by failure mode before reading a release verdict.
- **Cost and latency are reliability dimensions, not afterthoughts.** Token spend and iteration count are runtime resources an agent can exhaust the way it exhausts a retry budget; uncapped loops are an availability and a billing incident at once. Circuit-breakers belong in the harness (the L3 rail), not in the prompt.
- **Degradation is a designed behavior or it is an outage.** Under load or budget pressure an agent either sheds work in a defined order (cheaper model, fewer steps, queued, refused-with-reason) or it fails unpredictably. The order is an operational decision made before the pressure arrives.

## Good signals

- The release dashboard reports success per slice (task type, tool, model, customer tier) against a stored baseline, not one global pass-rate.
- Every gated metric is tagged guardrail or north-star; guardrail regressions block ship, north-star dips are reported with a delta and a human call.
- A hard token budget and a max-iteration cap exist per run, enforced in harness code; hitting either terminates the run with a typed, logged reason.
- End-to-end success is measured on full trajectories, and the per-step bar is set from the trajectory target backward (the march-of-nines math is written down, not assumed).
- A rollback threshold is defined numerically per slice ("block if slice X drops >3pts vs baseline") and wired to revert, not just to alert.
- Cost per successful task — not cost per call — is tracked, so a cheaper model that fails more is correctly read as more expensive.
- Degradation tiers are explicit and ordered (full → cheaper model → fewer steps → queue → refuse-with-reason), and which tier is active is observable.
- Budget and iteration breaches surface as first-class events in the trace, not as a stuck run a human notices hours later.

## Common failures

- **God Gate.** One aggregate pass-rate is the release gate; it hides which slice broke and lets a guardrail breach ship because the average held.
- **Guardrail/north-star conflation.** A safety or cost regression and a capability dip are scored on the same scale, so either a real breach ships or a harmless dip blocks a release.
- **March-of-nines denial.** Per-step quality is treated as the end-to-end number; a 0.95/step agent is shipped as "95% reliable" and underperforms badly in production.
- **Uncapped loops.** No iteration cap or token budget, so a confused agent spins until it times out or until the bill spikes — an availability and billing incident at once.
- **Cost-per-call tunnel vision.** Spend is tracked per call, so a cheaper model that doubles the failure (and retry) rate looks like a saving.
- **Alert-only rollback.** A threshold fires a notification but nothing reverts; the regression stays live until a human wakes up.
- **Hard-fail under pressure.** With no degradation tiers, load or budget exhaustion turns into 500s or silent overspend rather than a defined, cheaper service level.
- **Baseline drift.** Slices are scored against last week instead of a pinned baseline, so a slow multi-release decline never trips any single gate.

## Heuristics

- **(review, design) Decompose the gate by failure mode.** Replace the single pass-rate with per-slice scores against a baseline; a release verdict reads as a vector, not a scalar. The God Gate is a reporting choice, and you can choose otherwise.
- **(design) Tag every metric guardrail or north-star.** Guardrail regressions (safety, cost, side-effects) block ship; north-star/capability dips report a delta for a human call. Encode the two different ship decisions in the data, not in a reviewer's head.
- **(do, review) Do the march-of-nines math explicitly.** Multiply the per-step bar across the trajectory length before quoting an end-to-end number; set the per-step target by working backward from the end-to-end floor you actually need.
- **(do, design) Put cost and iteration circuit-breakers in the harness.** A hard token budget and a max-iteration cap live in L3 harness code, not the prompt; breaching either terminates with a typed, logged reason. Permissions, costs, and side-effects are harness rails, not prompt text.
- **(review) Measure cost per successful task.** Normalize spend by successful outcomes so a cheaper-but-flakier model is read as more expensive when its retries cost more than it saved.
- **(design) Define degradation tiers before the pressure.** Order the fallbacks (cheaper model → fewer steps → queue → refuse-with-reason) and make the active tier observable; a defined cheaper service level beats an undefined outage.
- **(design, review) Wire the rollback threshold to revert, not just alert.** State the numeric drop per slice that triggers rollback and connect it to an automatic revert; an alert nobody actions is Dashboard Theater for reliability.
- **(do) Emit budget and iteration breaches as trace events.** A run that hit its cap should say so in the trajectory, so the loop's failure mode is reconstructable instead of looking like a hang.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the release gate decomposed per slice against a pinned baseline? | One number hides which slice broke | Replace the aggregate gate with per-slice scoring vs baseline |
| Is every gated metric tagged guardrail vs north-star? | A breach ships or a dip blocks | Tag metrics; block on guardrail, report on north-star |
| Is the per-step bar derived from the end-to-end trajectory target? | The march of nines bites in prod | Write the multiplicative math down; reset the per-step bar |
| Are token budgets and iteration caps enforced in harness code? | A loop becomes a billing/availability incident | Add circuit-breakers in the L3 harness; terminate with a typed reason |
| Is cost tracked per successful task, not per call? | A flaky cheap model reads as a saving | Normalize spend by successful outcomes |
| Are degradation tiers defined and the active tier observable? | Pressure turns into a hard outage | Order the fallbacks and make the active tier visible |
| Does the rollback threshold revert, not just alert? | The regression stays live until a human acts | Wire the numeric per-slice threshold to an automatic revert |

## Cross-references

- `optimization-loop.md` — scoring the six-field loop and confirming observed emission before any gate is trusted.
- `autonomous-controller.md` — the controller that reverts on failed gates uses these per-slice thresholds and budgets as its stop/rollback rails.
- → `agent-test` for designing the eval suites, judges, and per-slice fixtures these gates score against.
- → `agent-dx` for building the SDK budget knobs, iteration caps, and the spans this surface consumes.
- → `harden-repo-for-coding-agents` for scaffolding the CI release-gate and rollback wiring as repo files.
- finding IDs `AGENT-OPS-REL-NNN`.
- `references/intents/{do,review,design}.csv` row `cost-and-reliability` — the entry points.

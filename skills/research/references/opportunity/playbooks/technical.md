# Technical Playbook

## Scope

Whether the system can be built, on what architecture, at what cost,
and with what risk. This playbook strips wishful thinking — most
"it's just an API call" / "it's just a CRUD app" claims survive
30 seconds of structured questioning.

- In: feasibility, architecture options, build-vs-buy per component,
  integration complexity, performance / latency / throughput budget,
  security threat model at a high level, reliability and recovery,
  maintainability over 6–18 months, scalability path.
- Out: pure code-architecture audit of an existing system
  (`minimal-modular-code`), DX of the resulting API
  (`dx-audit` / `dx-design`), data quality and instrumentation (`data.md`),
  ops / SRE runbooks (`operational.md`), perf observability.
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **Architecture Tradeoff Analysis Method (ATAM, SEI)** —
  quality-attribute tradeoffs as named scenarios; sensitivity
  points; risk themes. Used here to frame build-vs-buy and
  architecture-option decisions.
- **John Ousterhout — *A Philosophy of Software Design* (2018)** —
  deep modules with simple interfaces; defining errors out of
  existence; complexity-budget framing.
- **Martin Kleppmann — *Designing Data-Intensive Applications*
  (2017)** — latency / consistency / partition tradeoffs;
  percentile-not-average framing for performance.
- **Hyrum's Law (Hyrum Wright)** — every observable behavior of an
  interface is depended on; stable-contract reasoning.

## Good signals

- Build-vs-buy is decided per component, not per project. Commodity
  components default-buy; the load-bearing differentiator
  default-builds.
- Architecture is described in 1–3 named options with explicit
  tradeoffs (latency vs cost; consistency vs availability;
  ergonomics vs flexibility). Single-option presentations are
  usually un-stress-tested.
- A spike / prototype has been run (or is planned) on the riskiest
  technical assumption — usually the integration, scale, or
  latency claim that "of course will work."
- Performance budget is named with percentiles (p50, p95, p99), not
  averages.
- Security threat model is named at the level of attacker, asset,
  attack surface — not "we'll add auth."
- Maintenance burden is named honestly — what does this look like at
  6, 12, 18 months under turnover and growth.
- Risks are scored 0–4 with named mitigations and owners.

## Common failures

- **"We can build it" treated as "we should build it".** Capability
  is not strategy. The build-vs-buy frame restores the second
  question.
- **Skipping the spike.** A one-week prototype kills more bad bets
  than any architecture review. Mitigation: the riskiest assumption
  gets a spike before the build commits.
- **Performance modeled at average, not at percentile.** Means hide
  tail risk; p99 latency is what users feel.
- **Integration complexity hand-waved.** "We'll use their API" is
  one integration; the third-party also has rate limits, downtime,
  versioning, and breaking changes. Hyrum's-law surfaces always.
- **Security as a phase-three concern.** Auth, secrets handling,
  PII storage, audit logging chosen as afterthoughts cost 10× to
  retrofit.
- **Maintenance ignored.** The architecture that ships fastest at
  month 1 often costs the most at month 12. Maintenance burden
  belongs in the decision.
- **Single-option architecture.** If only one path was considered,
  the alternatives weren't ruled out — they were skipped.

## Heuristics

- **(scope, investigate)** *Decompose feasibility into named
  attributes.* Functionality, performance, integration, security,
  reliability, maintainability, cost. Score each on the chosen
  architecture.
- **(investigate)** *Run the riskiest spike first.* A one-week
  prototype on the load-bearing technical assumption (integration,
  scale, novel mechanic). Treat the spike result as evidence, not
  morale.
- **(investigate, decide)** *Build-vs-buy per component.*
  Commodity = buy (auth, payments, observability, queues).
  Differentiator = build. Edge cases that are *not* the
  differentiator = buy. Never build commodity infrastructure.
- **(investigate)** *Three architecture options, each with named
  tradeoffs.* Latency vs cost; consistency vs availability;
  ergonomics vs control. If you have one option, you have a
  recommendation, not an analysis.
- **(investigate)** *Percentile latency budget.* p50 / p95 / p99 at
  named load. Average latency is a vanity metric.
- **(investigate, decide)** *Threat model at attacker × asset ×
  surface.* Not "we'll add auth"; "the attacker is a curious user
  / malicious user / compromised peer / nation-state, the asset is
  X, the surface is Y."
- **(investigate, decide)** *Maintenance honesty.* What does this
  cost at 6, 12, 18 months under turnover and growth? Architectures
  that win at month 1 lose at month 12.
- **(decide)** *Risk score with kill criteria.* 0–4 with named
  mitigation and owner; severity-4 technical risks become kill
  criteria.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are 2–3 named architecture options with tradeoffs documented? | One-option presentation | Generate alternatives; name tradeoffs. |
| Is build-vs-buy decided per component? | Project-level "we'll build" | Re-do per-component; default-buy commodity. |
| Has the riskiest assumption been spiked? | Spike skipped | Run a 1-week spike on the load-bearing claim. |
| Is performance budget at p95 / p99, not average? | Average-only | Re-spec with percentiles + named load. |
| Is the threat model at attacker × asset × surface? | "We'll add auth" | Spec the threat model formally. |
| Is maintenance burden named at 6 / 12 / 18 months? | Silent on maintenance | Project maintenance under turnover + growth. |
| Are technical risks scored 0–4 with mitigations? | Vague risks | Score each; name mitigations; severity-4 → kill criterion. |

## Cross-references

- → `references/opportunity/playbooks/data.md` — for data side of feasibility
  (sources, access, quality).
- → `references/opportunity/playbooks/operational.md` — for the run-it side
  (delivery, support, recovery).
- → `references/opportunity/playbooks/financial.md` — for the cost side of
  build-vs-buy (infra + labor).
- → `references/opportunity/playbooks/risk.md` — where technical severity-4
  risks become kill criteria.
- → `references/opportunity/core/severity-rubric.md` — for risk scoring.
- → `references/opportunity/core/fadr-framework.md` — for the F/A/D/R fold.
- → `templates/opportunity/artifacts/technical-feasibility.md` — the artifact
  this playbook produces under `investigate`.

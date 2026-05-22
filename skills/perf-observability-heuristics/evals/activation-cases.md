# activation-cases.md — perf-observability-heuristics

Behavioral cases the skill is expected to handle. Each section is
machine-readable enough for future activation eval runners; today the
file is human-graded.

## Positive — should activate

- "Our p99 latency just doubled and we don't know why. Help me diagnose."
  → `diagnose/latency`. Hypothesis-ranking before naming root causes;
  measurement method must be named in the runbook output.
- "Design the SLO program for our new payments service."
  → `design/slos`. SLI selection, SLO target setting, error-budget
  policy, alerting thresholds.
- "Audit our existing observability stack for gaps before next quarter's
  reliability push." → `audit/all`. Multi-surface fan-out (one sub-agent
  per playbook), per-surface score, project-wide path-to-10.
- "Plan a tail-latency optimization pass for the checkout API."
  → `optimize/latency`. Profile-first; sequenced safe improvements with
  measured before/after gates.
- "Strategize our observability roadmap across logs, metrics, and traces."
  → `strategize/slos` (SLO program is the natural anchor; logs / metrics /
  traces fall out of "what do we need to measure to defend the SLO?").
  Program scope, adoption sequence, instrumentation budget.
- "Review our distributed tracing setup for cardinality and sampling."
  → `audit/tracing`. Three lenses against a single playbook.
- "We're seeing connection-pool exhaustion and slow queries; help us think
  through it." → `diagnose/resources` (resource-saturation framing) with
  cross-link to the DB-tier slice of `latency` and `resources`.
- "Run a USE-method pass on the API tier."
  → `audit/resources`.
- "Add error-budget alerting that doesn't page on noise."
  → `design/slos`.
- "Reduce p99 on the homepage; the median is fine."
  → `optimize/latency`. Tail-tolerant patterns.

## Negative — should NOT activate

- "Pick a good name for this React component." → naming, not perf.
- "Refactor this CRUD endpoint to use the repository pattern." →
  `clean-architecture`, not perf.
- "Review our developer onboarding docs for first-time integrator
  friction." → `dx-heuristics`.
- "Audit this test suite for false-pass risk and flakiness." →
  `test-heuristics`.
- "Design a database schema with proper normalization and foreign keys."
  → future `data-modeling-heuristics`, not perf-observability. (DB
  *performance* is in scope; schema *design* is not.)
- "Critique this user persona for evidence backing." → `persona-critique`.
- "Stress-test this PRD adversarially." → `spec-red-team`.

## Edge — boundary or ambiguous

- "Our CI build farm is saturated and the test stage runtime doubled —
  investigate the pipeline workers." → Activates at `diagnose/latency`.
  Per the README boundary, **CI / build-farm runtime is a production
  system** (owned by an infra / platform team) and stays here; developer
  inner-loop perf on a single workstation (install, cold start, own
  edit-test cycle) routes to `dx-heuristics`. The "investigate the
  pipeline workers" framing is unambiguously the production-system case.
- "First Contentful Paint regressed after the bundler upgrade; investigate
  the browser tier." → `diagnose/latency` (browser-tier slice).
- "We have RED metrics on the gateway but nothing on workers — what to
  add and why?" → `design/metrics`. The "why" framing pulls the
  three-pillars critique from the playbook's grounding.
- "Should we switch from Postgres to a columnar store for analytics?" →
  Not this skill; that's a data-modeling / architecture call. If the
  question reframes as "our OLAP queries are slow, what should we
  measure first?", then `diagnose/latency` (DB-tier slice).
- "How do we keep our observability bill from doubling?" → Could be
  `strategize` (instrumentation budget) or `audit/tracing` (sampling).
  Ask one disambiguation question.
- "Investigate this incident." → Too vague. Ask whether the user wants
  diagnosis (symptom → root cause) or an audit of why detection was slow.

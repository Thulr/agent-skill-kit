---
name: perf-observability-heuristics
description: Use when reviewing, designing, diagnosing, optimizing, or strategizing systems performance and observability — latency budgets, throughput and scalability, resource utilization, distributed tracing, structured logs, metrics, and SLO / error-budget programs across backend, browser / network, and database tiers. Trigger for p99 audits, profiling discipline, capacity planning, tail-latency investigations, instrumentation strategy, and observability program reviews. Database content is performance-only (index strategy, query plans, lock contention); route schema design and migration safety to a future data-modeling skill.
license: MIT
---

# Perf and Observability Heuristics

Review, design, diagnosis, optimization, and program-level strategy for
performance and observability across backend services, distributed systems,
the browser / network tier, and database performance internals. Provenance
lives in `skill.json`; this file is runtime routing only.

**Produces:** intent-specific report — `audit-report.md` / `design-doc.md` / `diagnose-runbook.md` / `optimize-plan.md` / `strategy-doc.md`; tracked audits also emit `perf-observability-heuristics-findings-ledger-<date>-<slug>.md` + `perf-observability-heuristics-workflow-state-<date>-<slug>.json`.

## Core principle

**Measure before optimizing; instrument for diagnosis, not just dashboards.**
A perf claim without a profile is a guess. A dashboard that does not let an
on-call engineer answer "why is this slow right now" is decoration. Tail
percentiles (p95, p99, max) tell the truth that medians hide.

## Activation

- **Bare invocation** (`"perf review"`, `"observability audit"`,
  `"start"`): load `references/starter-scenarios.csv` and
  `references/intent-router.csv`, then show the intent menu with named
  starter scenarios on top and offer the mode choice. Wait. No file
  inspection, network calls, or writes.
- **Concrete invocation** with intent and surface inferable: skip to
  step 3.
- **Ambiguous concrete invocation**: ask one blocker question identifying
  intent or surface before inspecting private systems.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Route to one of:
   `audit`, `design`, `diagnose`, `optimize`, `strategize`. Ambiguous → ask
   once.
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Route to one or more surfaces, or
   `all` (audit only) for multi-surface fan-out — see "Subagent dispatch"
   below. Ambiguous → ask once with the CSV menu, adding `all` as an
   option for audit intent.
3. **Load grounded context.** Load only the files listed in the chosen CSV
   row: one playbook from `references/playbooks/<surface>.md` plus the
   `core_refs` listed. Do not load other playbooks. Skip this step when
   surface = `all` — each spawned surface agent loads its own playbook.
4. **Identify the target persona** from `references/core/personas.md`.
5. **Spawn sub-agents in parallel (default for `audit`, `diagnose`, and
   `optimize`).** Single-surface: delegate one lens per agent — on-call /
   SRE, profiler / workload, capacity-planner. Audit + `all`: delegate one
   surface per agent; each runs the three lenses sequentially inside
   itself. See "Subagent dispatch" below.
6. **Apply the playbook.** Use the playbook's heuristics tagged for this
   intent. `audit` scores the surface 0–10 via
   `references/core/score-rubric.md`; `design` names the good-shaped
   pattern; `diagnose` ranks hypotheses before naming root causes;
   `optimize` sequences safe improvements with measured before / after
   gates; `strategize` defines the SLO / error-budget program and
   instrumentation roadmap.
7. **Apply severity and IDs** from `references/core/severity-rubric.md`
   and `references/trackable-findings.md` to every audit / diagnose /
   optimize finding. Use stable IDs like `PO-<surface>-NNN`.
8. **Emit output.** Audit → `templates/audit-report.md` (or
   `audit-report-multi.md` for surface = `all`). Design →
   `templates/design-doc.md`. Diagnose → `templates/diagnose-runbook.md`.
   Optimize → `templates/optimize-plan.md`. Strategize →
   `templates/strategy-doc.md`.
9. **Create, resume, or close tracking state.** For audit / diagnose /
   optimize outputs with 7+ findings, any severity 3–4, or a save / track /
   closeout request, load `references/trackable-findings.md`. If the
   request names an existing ledger, workflow-state, PR, branch, or `PO-*`
   ID, read saved state first; update statuses only after each
   verification rule passes. Otherwise write both artifacts now at
   `docs/audits/perf-observability-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and
   `docs/audits/perf-observability-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to
   `audit-artifacts/perf-observability-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and
   `audit-artifacts/perf-observability-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps,
   issues, and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output includes: target persona; playbook(s) applied; intent-specific
load-bearing section (findings for audit / diagnose / optimize, acceptance
criteria for design, program scope and adoption sequence for strategize);
verification with the measurement method named (not just "metric went
down"); grounding sources applied from `skill.json.inspired_by`.

## Subagent dispatch

**Default for `audit`, `diagnose`, and `optimize`;** preferred for
`design`; optional for `strategize`; skip tiny deterministic or
secret-bound work. Spawn three lenses in parallel — **on-call / SRE**,
**profiler / workload**, **capacity-planner** — per
`references/subagent-dispatch.md`. Without delegation, run the three
lenses sequentially and preserve disagreements as open questions.

## Reference map

- `references/intent-router.csv`, `references/intents/<intent>.csv` —
  routing.
- `references/playbooks/<surface>.md` — surface playbooks (latency,
  throughput, resources, tracing, logs, metrics, slos).
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/trackable-findings.md` — ledger, workflow-state, closeout.
- `references/modes.md`, `references/starter-scenarios.csv` — modes and
  worked examples.
- `references/core/{severity,score}-rubric.md`, `personas.md` — rubrics
  and persona list.
- `templates/*.md` — five intent-specific outputs plus tracking artifacts.
- `evals/*` and `skill.json` — activation / static checks and provenance.

---
name: perf-audit
description: Use to AUDIT the performance and observability posture of a production or runtime system — audit an existing service, distributed system, browser/network tier, or database tier for latency, throughput, resource saturation, tracing, logs, metrics, and SLO/error-budget gaps and score it, or diagnose a specific live incident or regression. Covers p99/tail-latency spikes, throughput cliffs, resource exhaustion, missing spans, log-volume blowups, cardinality blowups, and error-budget burn. Triggers on "perf audit", "observability review", "why did p99 double", "trace this throughput cliff", "are our SLOs/alerts right", "USE-method pass". Do NOT use to DESIGN instrumentation/SLOs or optimize a known-slow path (use perf-design), for developer-facing or local build/inner-loop performance (use dx-audit), or for end-user product UX (use ux-audit).
license: MIT
---

# Perf Critique

Performance and observability audit and incident-diagnosis for any production
system — backend services, distributed systems, the browser/network tier, and
the database tier. Provenance lives in `skill.json`; this file is runtime
routing only.

**Produces:** an intent-specific report — `audit-report.md` (or
`audit-report-multi.md` for surface = `all`) / `diagnose-runbook.md`; tracked
audits also emit `perf-audit-findings-ledger-<date>-<slug>.md` +
`perf-audit-workflow-state-<date>-<slug>.json`.

## Core principle

**Measure where the user feels it, and never trust a number you cannot
defend.** If on-call cannot answer "why is this slow or unreliable right now"
from the existing instrumentation — or the numbers hide the tail — that is a
finding worth recording.

## Activation

- **Bare invocation** (`"use perf-audit"`, `"perf audit"`, `"start"`): load
  `references/starter-scenarios.csv` and `references/intent-router.csv`, then
  show the intent menu with named starter scenarios on top and offer the mode
  choice. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and surface inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying intent or surface; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to one
   of: `audit`, `diagnose`. Ambiguous → ask once. (Designing instrumentation or
   optimizing a known-slow path instead? That is `perf-design`.)
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match to one or more surfaces, or `all`
   (audit only) for a multi-surface fan-out — see `references/subagent-dispatch.md`.
   Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen CSV row's files: one playbook
   from `references/playbooks/<surface>.md` plus its `core_refs`. Do not load
   other playbooks. Skip for surface = `all` — each spawned surface agent loads
   its own playbook in step 5.
4. **Identify the target persona** from `references/core/personas.md`.
5. **Spawn sub-agents in parallel (default for `audit`).** Single-surface: one
   lens per agent — capacity planner, on-call diagnostician, instrumentation
   reviewer. Audit + `all`: one surface per agent, each running the lenses
   sequentially. See "Subagent dispatch"; fall back to sequential only if the
   host has no delegation primitive.
6. **Apply the playbook.** Use the heuristics tagged for this intent. For
   `audit`, score the surface 0–10 using `references/core/score-rubric.md`; for
   `diagnose`, rank hypotheses before naming fixes and name the disconfirming
   measurement for each. If sub-agents ran, synthesize their findings here.
7. **Apply severity and IDs** from `references/core/severity-rubric.md` and
   `references/trackable-findings.md` to every audit finding or risk. Use stable
   IDs like `PERF-<surface>-NNN`.
8. **Emit output.** Audit → `templates/audit-report.md` (or
   `audit-report-multi.md` for `all`). Diagnose → `templates/diagnose-runbook.md`.
   Every output names the measurement method, not just the metric.
9. **Create, resume, or close tracking state.** For audit outputs with 7+
   findings, any severity 3–4, or a save/track/closeout request, load
   `references/trackable-findings.md`. If the request names an existing ledger,
   workflow-state, PR, branch, or `PERF-*` ID, read saved state first; update
   statuses only after each verification rule passes. Otherwise write both
   artifacts now at
   `docs/audits/perf-audit-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/perf-audit-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to `audit-artifacts/perf-audit-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps, issues,
   and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target persona, the playbook(s) applied, the
intent-specific load-bearing section (findings / root cause), the measurement
method per finding or hypothesis, and the grounding sources from
`skill.json.inspired_by`.

## Subagent dispatch

**Default for `audit`;** optional for `diagnose`; skip tiny deterministic or
secret-bound work. Spawn three lenses in parallel — **capacity planner**,
**on-call diagnostician**, **instrumentation reviewer** — per
`references/subagent-dispatch.md`.

## Reference map

- `references/intent-router.csv` — router (audit / diagnose).
- `references/intents/<intent>.csv` — surface router per intent.
- `references/playbooks/<surface>.md` — surface playbooks (shared with perf-design).
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/trackable-findings.md` — ledger, workflow-state, closeout rules.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/core/{severity,score}-rubric.md` — the 0–4 and 0–10 scales.
- `references/core/personas.md` — target persona list.
- `templates/*.md` — audit / diagnose outputs plus tracking artifacts.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.

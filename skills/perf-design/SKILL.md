---
name: perf-design
description: Use to DESIGN or optimize the performance and observability of a production or runtime system — design instrumentation, SLOs/error-budget policy, tracing topology, latency budgets, or metric selection up-front for a new or expanding system; plan a profile-first optimization pass on a known-slow path with before/after measurement gates; or shape a program-level observability and reliability strategy across logs, metrics, and traces. Triggers on "design our SLOs", "what spans/metrics should we emit", "plan a tail-latency optimization", "cut our log bill without losing recovery value", "observability roadmap". Emits a design doc, optimization plan, or strategy doc with concrete good-shaped patterns and acceptance criteria. Do NOT use to AUDIT or diagnose an existing system (use perf-audit), for developer-facing or local build/inner-loop performance (use dx-design), or for end-user product UX (use ui-design to build it, ux-audit to audit it), or for agent-system observability and tracing (use agent-ops).
license: MIT
---

# Perf Design

Performance and observability design, optimization, and program-level strategy
for any production or runtime system — applied *before* a problem ships, or
*ahead of* a measured optimization pass, so the instrumentation and budgets are
right the first time. Provenance lives in `skill.json`; this file is runtime
routing only.

**Produces:** a `design-doc.md` (instrumentation / SLO / tracing / budget
design), `optimize-plan.md` (profile-first, before/after-gated reductions to a
known-slow path), or `strategy-doc.md` (cross-surface program roadmap) — each a
concrete good-shaped pattern with testable acceptance criteria.

## Core principle

**Design the measurement before you need it, and never optimize a path you have
not profiled.** The cheapest time to fix a perf or observability gap is before
the symptom — name the SLI, the span attribute, the latency budget, or the
profile-gated change concretely rather than describing principles abstractly.

## Activation

- **Bare invocation** (`"use perf-design"`, `"design our observability"`,
  `"start"`): load `references/starter-scenarios.csv` and
  `references/intent-router.csv`, show the intent menu, offer the mode choice.
  Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying intent or surface; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to one
   of: `design`, `optimize`, `strategize`. Ambiguous → ask once. (Auditing or
   diagnosing an *existing* system instead? Route to `perf-audit`.)
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match the prompt to one surface (or a
   small set). Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen row's playbook
   `references/playbooks/<surface>.md` plus its `core_refs`. Do not load other
   playbooks.
4. **Identify the target persona** from `references/core/personas.md` — the
   design or optimization is *for* a specific operator and outcome.
5. **Name the good-shaped pattern.** Apply the playbook heuristics tagged for
   the intent. Produce the concrete shape — sample SLI/SLO, paste-ready alert
   rule, span-attribute schema, latency-budget table, or a profile-gated change
   sequence — not abstract advice. For `optimize`, sequence the work
   profile-first with a before/after measurement gate per step. For a wide
   design space, optionally dispatch parallel sketches and synthesize the
   strongest.
6. **Emit output.** `design` → `templates/design-doc.md`; `optimize` →
   `templates/optimize-plan.md`; `strategize` → `templates/strategy-doc.md`.
   Each names the measurement method and testable acceptance criteria.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target persona, the playbook(s) applied, the concrete
good-shaped pattern, the grounding sources from `skill.json.inspired_by`, and
acceptance criteria checkable by reading the artifact or running a measurement.

## Reference map

- `references/intent-router.csv` — level-1 router (design / optimize / strategize).
- `references/intents/<intent>.csv` — level-2 router (surface) per intent.
- `references/playbooks/<surface>.md` — surface playbooks (shared with perf-audit).
- `references/core/personas.md` — target persona list.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `templates/{design-doc,optimize-plan,strategy-doc}.md` — the output shapes.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.

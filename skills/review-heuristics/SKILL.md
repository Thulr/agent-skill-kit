---
name: review-heuristics
description: Heuristic review, design, and debugging across seven domains — pick the domain, the skill routes the rest. Use for DEVELOPER EXPERIENCE (APIs, SDKs, CLIs, dev docs, setup, errors, auth, IDE, plugins, telemetry); DOCUMENTATION experience (README/quickstarts, API refs, help centers, error copy, OpenAPI/MCP tool contracts, human-vs-agent audience conflicts); systems PERFORMANCE & observability (latency, p99/tail, throughput, SLOs, tracing, profiling, capacity); TEST-suite quality (unit/integration/e2e/property/contract/snapshot/mutation, flakiness, brittleness, pruning, test-pyramid); user-facing UX & ACCESSIBILITY (usability, forms, navigation/IA, error/recovery, onboarding, checkout/signup friction, WCAG/keyboard/screen-reader); UI DESIGN CRAFT (mockups, dashboards, design systems, prototypes, motion, decks, visual polish, anti-slop); and clean ARCHITECTURE (dependency rule, layering, ports/adapters, DDD, bounded contexts, refactors). Triggers on "DX review", "audit our docs", "p99 latency audit", "is our test suite flaky", "usability audit", "design a dashboard", "layer-violation audit", and similar. Use ui-craft to CREATE/polish a UI and ux to AUDIT one. Do not use for validating a product/market opportunity (use research), hardening a repo for coding agents (use project-agentification), or agent experience — designing/reviewing agent-readable docs, AI/Agent SDKs, or repo agent-readiness (use agent-experience).
license: MIT
---

# Review Heuristics

Source-grounded heuristic review across seven domains, routed **domain →
intent → surface**. Provenance lives in `skill.json`; this file is runtime
routing only.

**Produces:** an intent-specific report for the chosen domain (audit / design /
debug / edge-pass and the domain's equivalents); audits over threshold also
emit a findings-ledger + workflow-state pair for tracking.

## Core principle

**Make the good-shaped path obvious and every finding actionable.** Across all
seven domains the job is the same: bring independent expert lenses to a
surface, ground each finding in a cited heuristic, rate it by severity, and
hand back something the owner can act on — not a vibe. The domain decides
*which* heuristics; the engine is shared.

## Activation

- **Bare invocation** (`"review heuristics"`, `"start"`): load
  [`references/domain-router.csv`](./references/domain-router.csv), show the
  seven-domain menu, wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with the domain inferable from the prompt: pick the
  domain and go to step 2.
- **Concrete invocation with ambiguous domain**: ask one question naming the
  two or three candidate domains (e.g. "developer-facing API friction → `dx`,
  or end-user product usability → `ux`?"). Do not inspect private systems
  first.

## Workflow

1. **Pick domain.** Load [`references/domain-router.csv`](./references/domain-router.csv).
   Match the prompt to one of `dx`, `docs`, `perf`, `test`, `ux`, `ui-craft`,
   `architecture`. Disambiguation hints: developer integrating your
   product → `dx`; docs as the product → `docs`; production runtime/SLOs →
   `perf`; the developer's own machine inner-loop → `dx`; creating a UI →
   `ui-craft`; auditing a UI's usability → `ux`; internal code structure →
   `architecture`. Ambiguous → ask once.
2. **Run the shared workflow.** Load
   [`references/review-workflow.md`](./references/review-workflow.md) and follow
   it against the chosen domain `D` — it routes intent → surface inside
   `references/D/`, dispatches `D`'s reviewer lenses, applies `D`'s rubrics, and
   emits `D`'s output template under `templates/D/`. Load only the chosen
   domain's files.

## Modes

Guided Draft (default), Autopilot, Grill Me — see the chosen domain's
`references/<domain>/modes.md` (all sourced from `skills/_shared/modes.md`).
Offer the mode at bare invocation; default to Guided Draft otherwise.

## Reference map

- [`references/domain-router.csv`](./references/domain-router.csv) — top-level
  router (domain → domain directory).
- [`references/review-workflow.md`](./references/review-workflow.md) — the
  shared intent → surface → lenses → severity → emit → track workflow.
- `references/<domain>/` — per-domain routers, playbooks, rubrics, personas,
  lens identities (`dx`, `docs`, `perf`, `test`, `ux`, `ui-craft`,
  `architecture`).
- `templates/<domain>/` — the intent-specific outputs each domain emits.
- `evals/{activation-cases.md,run-static-checks.sh,trigger-evals.json}` — gates.
- `skill.json` — provenance (122 grounding sources across the seven domains),
  version, status.

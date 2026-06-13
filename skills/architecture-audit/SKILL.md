---
name: architecture-audit
description: Use to AUDIT an existing codebase or module for clean-architecture concerns — audit it for dependency-rule violations, layer/port/adapter boundary leakage, anemic domain models, bounded-context seams, and cross-cutting concerns, then score it. Triggers on "architecture review", "layer-violation audit", "is our domain anemic", "audit dependency direction", "DDD / bounded context review", "are our ports and adapters right". Do NOT use to DESIGN, refactor toward, or explain a target architecture (use architecture-design), for developer-facing API/SDK/CLI surfaces (use dx-audit), or for product UX / forms / navigation / accessibility (use ux-audit).
license: MIT
---

# Architecture Audit

Clean-architecture audit for an existing codebase or module — dependency
direction, layer/port/adapter boundaries, domain modeling, bounded-context
seams, and cross-cutting concerns. Provenance lives in `skill.json`; this file
is runtime routing only.

**Produces:** an `audit-report.md` (or `audit-report-multi.md` for `all`) plus a
findings-ledger + workflow-state file when tracked.

## Core principle

**The dependency rule is the load-bearing invariant.** Source-code dependencies
point inward, toward more abstract code. If an outer concern (framework, ORM,
HTTP, message broker) has reached into the domain or application core, that is a
finding worth its severity — verify it against the structural graph, do not
guess from names.

## Activation

- **Bare invocation** (`"use architecture-audit"`, `"architecture review"`,
  `"start"`): load `references/starter-scenarios.csv` and
  `references/intent-router.csv`, then show the intent menu with named starter
  scenarios on top and offer the mode choice. Wait. No file inspection, no
  network calls, no writes.
- **Concrete invocation** with the surface inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying the surface; do not inspect private systems first.

## Workflow

1. **Confirm intent = audit.** Load `references/intent-router.csv`. This skill
   is single-intent (`audit`). If the ask is to design a target shape, sequence
   a refactor, or explain a principle, route to `architecture-design` instead.
2. **Pick surface.** Load `references/intents/audit.csv`. Match to one or more
   of: `dependency-rule`, `boundaries`, `domain-model`, `bounded-context`,
   `cross-cutting`, or `all` for a multi-surface fan-out — see
   `references/subagent-dispatch.md`. Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen CSV row's files: one playbook
   from `references/playbooks/<surface>.md` plus its `core_refs`. Do not load
   other playbooks. Skip for `all` — each surface agent loads its own playbook.
4. **Identify the target persona** from `references/core/personas.md`.
   Then **calibrate to project scale** per `references/calibration.md`: below
   Load-bearing, narrow scope, collapse same-mechanism gaps into one systemic
   finding, and split fixes Now vs Later.
5. **Spawn sub-agents in parallel (default when permitted).** Single-surface:
   one lens per agent; audit + `all`: one surface per agent running the lenses
   sequentially. See "Subagent dispatch"; fall back to sequential only if the
   host lacks a delegation primitive.
6. **Apply the playbook.** Use the heuristics tagged `(audit)`. Score the
   surface 0–10 using `references/core/score-rubric.md`. If sub-agents ran,
   synthesize their findings here, preserving disagreements as open questions.
7. **Apply severity and IDs** from `references/core/severity-rubric.md` and
   `references/audit-mechanics.md` to every finding. Use stable IDs with the
   canonical surface prefixes: `CA-DEP`, `CA-BOUNDARY`, `CA-DOMAIN`,
   `CA-CONTEXT`, `CA-CROSS` (`CA-<surface>-NNN`).
8. **Emit output.** Audit → `templates/audit-report.md` (or
   `audit-report-multi.md` for `all`).
9. **Create, resume, or close tracking state.** For audits with 7+ findings,
   any severity 3–4, or a save/track/closeout request, load
   `references/audit-mechanics.md` and `references/trackable-findings.md`. If the
   request names an existing ledger, workflow-state, PR, branch, or `CA-*` ID,
   read saved state first; update statuses only after each verification rule
   passes. Otherwise write both artifacts now at
   `docs/audits/architecture-audit-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/architecture-audit-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to `audit-artifacts/architecture-audit-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps, issues,
   and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target persona, the playbook(s) applied, the findings
with severity and verification, and the grounding sources from
`skill.json.inspired_by`. Surface school disagreements explicitly rather than
flattening them.

## Subagent dispatch

**Default for `audit` when delegation is permitted;** skip tiny deterministic or
secret-bound work. Spawn three lenses in parallel — **dependency-auditor**,
**boundary-designer**, **refactor-pragmatist** — per
`references/subagent-dispatch.md`, then synthesize.

## Reference map

- `references/intent-router.csv` — single-intent router (`audit`).
- `references/intents/audit.csv` — surface router (dependency-rule / boundaries /
  domain-model / bounded-context / cross-cutting / all).
- `references/playbooks/<surface>.md` — surface playbooks (shared with architecture-design).
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/audit-mechanics.md` — finding IDs, scoring, closeout mechanics.
- `references/trackable-findings.md` — ledger, workflow-state, closeout rules.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/calibration.md` — project-scale tiers + every-X collapse rule (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/core/{severity,score}-rubric.md` — the 0–4 and 0–10 scales.
- `references/core/{personas,glossary}.md` — target persona list and terms.
- `templates/*.md` — audit outputs plus tracking artifacts.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.

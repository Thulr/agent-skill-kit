---
name: docs-audit
description: "Use to AUDIT existing documentation — score a docs/help/agent-readable surface for friction, drift, accessibility, retrieval, or audience conflict, or debug a docs failure. Owns every doc a human reads: README, CHANGELOG, quickstart, onboarding, samples. Triggers on 'docs review', 'audit our docs/README/help', 'our quickstart fails'. Do NOT use for API/SDK/CLI friction beyond the docs (dx-audit) or standalone agent-native docs (agent-docs) — cross-audience conflicts spanning llms.txt stay here."
license: MIT
---

# Docs Audit

Documentation-experience audit and debugging for any surface someone reads to
learn, integrate, recover, or retrieve — developer docs, end-user help, and
agent-readable docs. Provenance lives in `skill.json`; this file is runtime
routing only.

**Produces:** an intent-specific report — `audit-report.md` (friction findings,
score, audience conflicts) or `debug-runbook.md` (ranked hypotheses, fix path,
prevention).

## Boundaries

Do NOT use to DESIGN new docs (use docs-design), for line-level prose tightening (use writing-audit), for end-user product UX outside help (use ux-audit), for repo agent hardening (use harden-repo-for-coding-agents), for API/SDK/CLI friction beyond the docs (use dx-audit), or for standalone agent-native docs (use agent-docs).

## Core principle

**Match the page to the audience's job and keep it true.** If a competent
reader has to guess the page type, hunt for the canonical fact, copy a stale
example, or fight prose that fits no audience, that is a docs problem worth a
finding.

## Activation

- **Bare invocation** ("use docs-audit", "docs review", "start"): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and surface inferable: skip to step 3.
- **Ambiguous invocation**: ask one — e.g., *"Are you auditing developer docs, end-user help, or agent-readable surfaces?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to one
   of: `audit`, `debug`. Ambiguous → ask once. (Designing or measuring new docs
   instead? That is `docs-design`.)
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match to one or more surfaces, or `all`
   (audit only) for a multi-surface fan-out — see `references/subagent-dispatch.md`.
   Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen CSV row's files: one playbook
   from `references/playbooks/<surface>.md` plus its `core_refs`. Do not load
   other playbooks. Skip per-surface loads for `all` — each spawned surface agent
   loads its own playbook in step 5.
4. **Identify the target audience** from `references/core/personas.md` and the
   shared `references/core/audience-matrix.md` — developer, end user, or agent.
   Then **calibrate to project scale** per `references/calibration.md`: infer the
   tier (Prototype / Growing / Load-bearing) — ask once only if unclear. Below
   Load-bearing, narrow scope and collapse same-mechanism gaps of severity ≤ 3
   into one systemic finding (severity 4: explicit, never deferred), and split
   fixes Now vs Later; tier reshapes emission,
   not the severity rubric.
5. **Spawn sub-agents in parallel (default for broad audits).** One lens per
   agent — see "Subagent dispatch" below for the four. Fall back to sequential
   only if the host has no delegation primitive; mark the review single-threaded.
6. **Apply the playbook.** Use the heuristics tagged for this intent. For
   `audit`, score the surface 0–10 using `references/core/score-rubric.md`; for
   `debug`, rank hypotheses by mechanism (absence, findability, ambiguity,
   staleness, conflict) before naming fixes. If sub-agents ran, synthesize and
   preserve audience disagreements.
7. **Apply severity and IDs** from `references/core/severity-rubric.md` to every
   audit finding. Use stable IDs like `DOC-<surface>-NNN`.
8. **Emit output.** Audit → `templates/audit-report.md`. Debug →
   `templates/debug-runbook.md`. Name the playbook(s) applied, the target
   audience, and the grounding sources.

> **Wrong direction?** If the user says this isn't what they meant, go back to step 1 (Pick intent) — do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer at bare invocation;
concrete invocations default to Guided Draft.

## Output requirements

Every output names the target audience, the playbook(s) applied, the
intent-specific load-bearing section (findings / hypotheses-and-prevention),
verification per finding, and the grounding sources from
`skill.json.inspired_by`.

## Subagent dispatch

**Default for broad audits;** optional for narrow `debug`; skip tiny
deterministic or secret-bound work. Spawn the four lenses in parallel —
**developer-docs**, **end-user help**, **agent-retrieval**, and
**content-operations** — per `references/subagent-dispatch.md`, then synthesize.

## Reference map

- `references/intent-router.csv` — level-1 router (audit / debug).
- `references/intents/<intent>.csv` — level-2 router (surface) per intent.
- `references/playbooks/<surface>.md` — surface playbooks (shared with docs-design).
- `references/subagent-dispatch.md` — the four lens prompts and merge rules.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/calibration.md` — project-scale tiers + every-X collapse rule (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/core/{severity,score}-rubric.md` — the 0–4 and 0–10 scales.
- `references/core/personas.md`, `references/core/audience-matrix.md` — audiences.
- `templates/*.md` — audit / debug outputs.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.

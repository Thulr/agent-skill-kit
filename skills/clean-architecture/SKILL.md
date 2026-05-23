---
name: clean-architecture
description: Audit, design, refactor toward, or explain clean-architecture concerns — dependency rule, layered/hexagonal/onion boundaries, DDD tactical and strategic patterns, cross-cutting concerns. Use for architecture review, layer-violation audits, bounded-context design, anemic-domain detection, refactor sequencing toward ports and adapters, or explaining principles like the dependency rule, aggregate vs entity, or anti-corruption layers. Opinionated terrain; surfaces school disagreements explicitly. Language-agnostic, full-stack-friendly for code architecture; route product UX, forms, navigation, and accessibility to ux-accessibility-heuristics.
license: MIT
---

# Clean Architecture

Architecture review, design, refactor, and explanation grounded in the
clean-architecture family. Provenance and citations live in `skill.json`;
this file is runtime routing only.

Frontend scope is code-architecture only: component boundaries, dependency
direction, state/effect isolation, and feature/module structure. User-facing
visual UX, forms, navigation, and accessibility route to
`ux-accessibility-heuristics`.

**Produces:** intent-specific report — `audit-report.md` / `design-doc.md` / `refactor-runbook.md` / `explanation.md`; tracked audits also emit `clean-architecture-findings-ledger-<date>-<slug>.md` + `workflow-state-<date>-<slug>.json`.

## Core principle

**Dependency direction is load-bearing.** Inner, more abstract code never
depends on outer, more concrete code. Layered, hexagonal, onion, or
concentric diagrams differ; inward arrows still mean a leak.

## Activation

- **Bare invocation** (`"use clean-architecture"`, `"architecture review"`,
  `"start"`): load `references/starter-scenarios.csv` and
  `references/intent-router.csv`, then show the intent menu with named
  starter scenarios on top and offer the mode choice. Wait. No file
  inspection, network calls, or writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Ambiguous concrete invocation**: ask one blocker question identifying
  intent or surface before inspecting private systems.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`; route to `audit`,
   `design`, `refactor`, or `explain`. Ambiguous -> ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`; route to one or
   more surfaces, or `all` for audit fan-out. Follow-through prompts use
   `audit/tracking` or `audit/closeout` pseudo-routes and skip surface
   loading. Ambiguous -> ask once.
3. **Load context.** Load only the CSV row's playbook plus `core_refs`. For
   audit `all`, each surface pass loads its own row. Audit rows load
   `references/audit-mechanics.md` for ID prefixes, synthesis rules, and
   template mapping.
4. **Set vocabulary.** Identify persona from `references/core/personas.md`
   and load `references/core/glossary.md`.
5. **Apply the three-lens plan.** Load `references/subagent-dispatch.md`.
   Try parallel sub-agents whenever the host supports delegation and the
   user, project, session, or host policy permits it. If the host requires
   fresh explicit opt-in and none exists, ask once before dispatch. Fall
   back to sequential lens or surface passes only when dispatch is blocked,
   declined, unsafe, or unavailable.
6. **Apply playbook.** Audit scores 0-10; design names the pattern; refactor
   sequences safe steps; explain uses the playbook grounding. Synthesize
   sub-agent findings and preserve disagreements.
7. **Apply severity and IDs.** Every finding gets severity 0-4. Audit
   findings also get stable IDs from `references/trackable-findings.md`.
   Use `CA-DEP`, `CA-BOUNDARY`, `CA-DOMAIN`, `CA-CONTEXT`, or `CA-CROSS`
   prefixes by surface.
8. **Emit output.** Audit -> `templates/audit-report.md` or
   `templates/audit-report-multi.md`; design -> `templates/design-doc.md`;
   refactor -> `templates/refactor-runbook.md`; explain ->
   `templates/explanation.md`.
9. **Create tracking state.** For audit outputs with 7+ findings or any
   severity 3-4 finding, load `references/trackable-findings.md` and write both
   tracking artifacts immediately: the Markdown ledger at
   `docs/audits/clean-architecture-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and workflow state at
   `docs/audits/clean-architecture-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`
   (create the directory if needed). If the target is not a repo or
   `docs/audits/` is not writable, use
   `audit-artifacts/clean-architecture-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`.
   Populate them from `templates/findings-ledger.md` and
   `templates/workflow-state.json`, report both saved paths, and do not merely
   inline or offer them. Roadmaps and GitHub issues require explicit user
   request; never create external issues without confirmation. Check boxes only
   after verification.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output includes persona, playbook(s), intent-specific payload, severity,
verification, and grounding sources applied from `skill.json.inspired_by`.
Audit outputs include finding IDs and, when triggered, the saved ledger and
workflow-state paths or closeout result.

## Subagent dispatch

Use the three lenses for audit, prefer them for design trade-off checks, and
skip them for tiny explanations, deterministic checks, or work requiring
secrets/live production context.

Always try dispatch when the host supports delegation and user, project,
session, or host policy permits it. If policy requires an explicit user
request and none is present, ask once: "Use parallel sub-agents for this
clean-architecture work?" A yes unlocks dispatch; no or ambiguity means
sequential passes.

For audit `all`, try to dispatch one agent per audit CSV surface; each runs
the three lenses sequentially. Otherwise use one agent per lens.

## Reference map

- `references/intent-router.csv` and `references/intents/<intent>.csv` -
  routing.
- `references/playbooks/<surface>.md` - surface playbooks.
- `references/subagent-dispatch.md` - three lenses and synthesis.
- `references/audit-mechanics.md` - audit ID namespace, host synthesis,
  closeout extraction, and template source-of-truth rules.
- `references/core/{severity,score}-rubric.md`, `personas.md`,
  `glossary.md` - shared rubrics and terms.
- `references/trackable-findings.md` - ledger, roadmap, issues, workflow
  state, and verification closeout.
- `references/modes.md` - Guided Draft / Autopilot / Grill Me contract (shared).
- `references/starter-scenarios.csv` - named worked examples for bare invocation.
- `templates/*.md` - output and tracking templates.
- `evals/*` and `skill.json` - activation/static checks and provenance.

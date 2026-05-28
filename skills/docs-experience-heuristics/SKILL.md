---
name: docs-experience-heuristics
description: "Use when auditing, designing, debugging, or measuring documentation experience across developer docs, end-user help, and agent-readable docs, including README/quickstarts, API references, examples, error copy, help centers, onboarding help, llms.txt/AGENTS.md/SKILL.md/MCP/OpenAPI descriptions, RAG-friendly structure, documentation telemetry, and audience conflicts. Do not use for pure developer-surface DX outside docs (use dx-heuristics), pure product UX/accessibility inspection (use ux-accessibility-heuristics), or repo agent-readiness gates/hooks (use project-agentification)."
license: MIT
---

# Docs Experience Heuristics

Cross-audience documentation review, design, debugging, and measurement for
surfaces that must serve humans and agents. Provenance lives in `skill.json`;
this file is runtime routing only.

**Produces:** intent-specific output — `audit-report.md`, `design-doc.md`,
`debug-runbook.md`, or `measurement-plan.md`.

## Core principle

**Make the needed explanation findable, current, actionable, and audience-fit.**
Documentation fails when readers cannot tell which page applies, examples rot,
errors dead-end, help arrives in the wrong place, or agents cannot retrieve and
act on the contract.

## Activation

- **Bare invocation** (`"use docs-experience-heuristics"`, `"docs review"`,
  `"make our docs better"`): load `references/starter-scenarios.csv` and
  `references/intent-router.csv`, show the intent menu, then wait. Do not read
  target docs, inspect repos, or write files yet.
- **Concrete invocation** with intent and surface inferable: skip to workflow
  step 3.
- **Ambiguous audience or surface:** ask one blocker question: developer docs,
  end-user help, agent-readable docs, API/tool contracts, cross-audience
  conflict, or all.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to
   `audit`, `design`, `debug`, or `measure`. Ambiguous → ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`. Match one or more
   surfaces: `foundations`, `dx-docs`, `ux-help`, `ax-docs`, `api-contracts`,
   `audience-conflicts`. For broad audits or measurement plans, allow `all`.
3. **Load only routed context.** Read the selected playbook(s) plus the listed
   core references. Do not load unrelated playbooks.
4. **Name the audience mix.** Use `references/core/personas.md` and
   `references/core/audience-matrix.md` to identify primary, secondary, and
   harmed audiences before recommending changes.
5. **Apply heuristics by intent.** Use only heuristics tagged for the chosen
   intent. Audit scores use `references/core/score-rubric.md`; findings and
   risks use `references/core/severity-rubric.md`.
6. **Resolve conflicts explicitly.** When human and agent needs diverge, use
   `audience-conflicts.md` instead of averaging the audiences together.
7. **Emit the template.** Audit → `templates/audit-report.md`; design →
   `templates/design-doc.md`; debug → `templates/debug-runbook.md`; measure →
   `templates/measurement-plan.md`.

## Output requirements

Every output names the audience mix, intent, surface playbook(s), top risks,
recommended verification, and grounding sources from `skill.json.inspired_by`.
Do not invent telemetry, eval results, or user-research findings; mark them as
needed evidence when unavailable.

## Subagent dispatch

Default for broad `audit`, `design`, and `measure`; optional for focused
`debug`. Spawn four lenses in parallel when the host supports delegation:
developer-docs reviewer, end-user help reviewer, agent-retrieval reviewer, and
content-operations reviewer. Use `references/subagent-dispatch.md`; fall back
to the lenses sequentially when delegation is unavailable.

## Reference map

- `references/intent-router.csv` — level-1 router by intent.
- `references/intents/<intent>.csv` — level-2 router by surface.
- `references/playbooks/<surface>.md` — surface playbooks.
- `references/core/{severity,score}-rubric.md` — shared scales.
- `references/core/{personas,audience-matrix}.md` — audience vocabulary.
- `references/subagent-dispatch.md` — multi-lens review prompts.
- `references/starter-scenarios.csv` — starter menu for bare invocation.
- `templates/*.md` — output skeletons.
- `evals/activation-cases.md` and `evals/trigger-evals.json` — routing cases.

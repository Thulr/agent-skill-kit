# Docs Experience Heuristics Activation Cases

## Positive

- "Audit our docs site across developers, end users, and coding agents." -> routes to `audit` and `foundations`, may fan out to all playbooks, emits `templates/audit-report.md`.
- "Design a docs IA with tutorials, how-tos, reference, explanation, versioning, accessibility, and feedback loops." -> routes to `design` and `foundations`, loads `references/playbooks/foundations.md`, emits `templates/design-doc.md`.
- "Our README buries install instructions and the quickstart does not reach hello world." -> routes to `audit` and `dx-docs`, loads `references/playbooks/dx-docs.md`, emits `templates/audit-report.md`.
- "Developers copy our example and it fails because imports and environment setup are missing." -> routes to `debug` and `dx-docs`, loads `references/playbooks/dx-docs.md`, emits `templates/debug-runbook.md`.
- "Users read a help article after an error and still open support tickets." -> routes to `debug` and `ux-help`, loads `references/playbooks/ux-help.md`, emits `templates/debug-runbook.md`.
- "Design in-product help for empty states, tooltips, onboarding, and user-facing error recovery." -> routes to `design` and `ux-help`, loads `references/playbooks/ux-help.md`, emits `templates/design-doc.md`.
- "Add llms.txt, markdown docs, stable anchors, and RAG-friendly summaries for our docs site." -> routes to `design` and `ax-docs`, loads `references/playbooks/ax-docs.md`, emits `templates/design-doc.md`.
- "Agents under-trigger the right skill and retrieve chunks that say 'see above'; diagnose the agent docs." -> routes to `debug` and `ax-docs`, loads `references/playbooks/ax-docs.md`, emits `templates/debug-runbook.md`.
- "Review our OpenAPI schema and MCP tool descriptions for examples, errors, constraints, and retry semantics." -> routes to `audit` and `api-contracts`, loads `references/playbooks/api-contracts.md`, emits `templates/audit-report.md`.
- "Define an eval for tool-call success from schema descriptions and stable error codes." -> routes to `measure` and `api-contracts`, loads `references/playbooks/api-contracts.md`, emits `templates/measurement-plan.md`.
- "Our tooltips are good UX but the instructions disappear for agents and screen readers." -> routes to `debug` and `audience-conflicts`, loads `references/playbooks/audience-conflicts.md`, emits `templates/debug-runbook.md`.
- "Make one source of truth render as human docs, agent markdown, and in-product help without drift." -> routes to `design` and `audience-conflicts`, loads `references/playbooks/audience-conflicts.md`, emits `templates/design-doc.md`.

## Negative

- "Audit the checkout form for keyboard traps, focus order, contrast, and ARIA labels." -> use `ux-accessibility-heuristics` instead, because this is product accessibility rather than documentation/help strategy.
- "Make this dashboard visually polished and build a Tailwind component system." -> use `ui-design-craft` instead, because visual UI creation is not a docs-experience task.
- "Review the SDK API design, naming, auth flow, and developer onboarding; docs are out of scope." -> use `dx-heuristics` instead, because the requested surface is the developer product/API, not documentation.
- "Assess this repository's AGENTS.md, hooks, sandbox, and CI for coding-agent readiness." -> use `project-agentification` instead, because repo agent-readiness and gates are the primary task.
- "Record this agent failure in a reflection log and decide whether it should become a rule." -> use `evidence-driven-agent-rules` instead, because failure-log governance is the task.
- "Investigate why p99 latency increased and whether our tracing coverage is sufficient." -> use `perf-observability-heuristics` instead, because system performance and observability are primary.
- "Review our unit, integration, and e2e tests for brittleness and false-pass risk." -> use `test-heuristics` instead, because the request is test-suite quality.
- "Research the history of documentation frameworks and give me a cited primer." -> use `topic-research` instead, because the output is an open-ended research report, not a docs-experience intervention.

## Boundary / edge

- "Make our docs better." -> activates only if the user confirms a documentation/help/agent-docs surface; otherwise ask whether they mean developer DX (`dx-heuristics`), product UX (`ux-accessibility-heuristics`), repo agent-readiness (`project-agentification`), or cross-audience docs (`docs-experience-heuristics`).
- "Improve our AGENTS.md." -> activates only when the task is about documentation strategy or always-loaded vs load-on-demand docs; otherwise prefer `project-agentification` for repo context files and enforcement.
- "Fix this error message." -> activates if the error is part of docs/help/API contract design; otherwise prefer `dx-heuristics` for developer-facing runtime errors or `ux-accessibility-heuristics` for product form recovery.

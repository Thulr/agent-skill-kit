# Candidate Plan — docs-experience-heuristics

## Candidate

- **Name:** `docs-experience-heuristics`
- **Dossier ref:** `.agents/state/source-dossiers/docs-experience-heuristics-2026-05-27.md`
- **Audience ref:** intake brief in `.agents/state/intake-briefs/docs-experience-heuristics-2026-05-27.md`
- **Public path:** `skills/docs-experience-heuristics/`
- **Action:** create skill plus cross-reference updates to neighboring skills and repo indexes.

## Shape decision

- **Shape:** two-level routing.
- **Rubric evidence:** two orthogonal axes are doing real work: intent (`audit`, `design`, `debug`, `measure`) and documentation surface (`foundations`, `dx-docs`, `ux-help`, `ax-docs`, `api-contracts`, `audience-conflicts`). Each leaf loads distinct playbook content and shared audience/severity rubrics.
- **Anti-pattern check:** no collapsed axis (4 intents, 6 surfaces); not a registry pointing to identical files; not projected bloat because playbooks are 400–1500 words; not a substitute for unrelated skills because all leaves share the docs-experience audience matrix.

## Playbook outline

- `foundations`: mode purity, docs-as-code, IA, accessibility, versioning, feedback loops; failure: telemetry without closure.
- `dx-docs`: first-success ladder, mode split, copy-paste proof, example CI; failure: snippet rot.
- `ux-help`: moment-of-need help, empty states, recovery copy, accessible help media; failure: tooltip dependency.
- `ax-docs`: retrieval entrypoint, load-budget split, chunk-survivability, trigger descriptions; failure: context hoarding.
- `api-contracts`: six-part descriptions, error envelope, retry safety, operational metadata; failure: unstable message branching.
- `audience-conflicts`: visible plus machine-readable, one source/many renderings, precision with explanation; failure: average-audience compromise.

## Registry sketch

- `references/intent-router.csv` routes 4 intents to intent-specific CSVs and templates.
- `references/intents/*.csv` route each intent to surface playbooks plus shared core references.
- Leaves are `references/playbooks/*.md`; shared scales live in `references/core/`.

## Activation case seeds

- Positive: cross-audience audit, README quickstart, help-center deflection, llms.txt/RAG docs, OpenAPI/MCP descriptions, tooltips-vs-agents conflict, docs telemetry.
- Negative siblings: `dx-heuristics`, `ux-accessibility-heuristics`, `ui-design-craft`, `project-agentification`, `agent-rules`, `perf-observability-heuristics`, `test-heuristics`, `topic-research`.
- Edge: ambiguous "make our docs better" and AGENTS.md/error-message boundary prompts.

## Grounding map

See `skills/docs-experience-heuristics/skill.json` `inspired_by[].playbooks` for per-source mapping.

## Review handoff

- **Draft paths:** `skills/docs-experience-heuristics/`, README index updates, neighboring cross-reference edits.
- **Validation report:** `.agents/state/validation-reports/docs-experience-heuristics-2026-05-27.md` (`validate-generated-skill`: note-only; per-skill static check passed).
- **Known risks:** new skill overlaps with `dx-heuristics` docs and `project-agentification` AX surfaces; activation cases and README routing must make boundaries explicit.
- **Suggested reviewer focus:** skill activation specificity, playbook usefulness, and whether cross-skill routing avoids over-triggering.

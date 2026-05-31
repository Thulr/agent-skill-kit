# Source Dossier — docs-experience-heuristics

- **Dossier ID:** docs-experience-heuristics-2026-05-27
- **Primary source:** `docs/research/research-report-2026-05-27-doc-patterns-dx-ax-ux.md`
- **Confidence:** high for shared documentation foundations, DX docs patterns, UX help patterns, and core AX patterns explicitly sourced in the report; medium for emerging AX discipline boundaries and some telemetry claims.

## Load-bearing claims

| Claim | Confidence | Skill use |
|---|---|---|
| Documentation foundations transfer across DX, UX, and AX: mode separation, docs-as-code, IA, plain language, versioning, errors-as-docs, feedback loops. | H | `foundations` playbook |
| DX docs need first-success README/quickstarts, runnable examples, reference completeness, changelogs, and searchable troubleshooting. | H | `dx-docs` playbook |
| UX help belongs near the moment of need; empty states, errors, onboarding, and help centers are documentation surfaces. | H | `ux-help` playbook |
| AX adds unique requirements: routing descriptions, context budget, schema-as-docs, chunk survivability, stable codes, and machine-enforced gates. | H/M | `ax-docs`, `api-contracts` |
| Audience conflicts are the strongest novel contribution: good UX or DX patterns can harm AX and vice versa. | H for conflicts described; M for canonical resolutions | `audience-conflicts` playbook |

## Critical / dissenting takes

- The AX evidence base is young and vendor-heavy; the skill marks measurement/eval as required evidence where claims could be product-specific.
- More agent documentation is not automatically better; always-loaded content can increase cost and reduce success.
- A separate AX skill would over-split this catalog today; the report's strongest reusable behavior is cross-audience docs conflict resolution.

## Paraphrase audit

Public skill files paraphrase source claims into heuristics and cite provenance in `skill.json`. No long passages, distinctive quotes, chapter summaries, or source marketing copy were copied.

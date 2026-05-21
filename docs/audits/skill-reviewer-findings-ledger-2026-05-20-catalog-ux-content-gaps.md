# Skill Reviewer Findings Ledger - Catalog UX and Content Gaps

**Skill:** skill-reviewer
**Ledger file:** `docs/audits/skill-reviewer-findings-ledger-2026-05-20-catalog-ux-content-gaps.md`
**Source report:** Catalog review requested in chat on 2026-05-20
**Created:** 2026-05-20
**Last updated:** 2026-05-20
**Owner:** @Thulr

## Status Summary

| Status | Count |
|---|---:|
| discovered | 0 |
| accepted | 0 |
| planned | 0 |
| in_progress | 0 |
| implemented | 0 |
| verified | 10 |
| closed | 0 |
| needs_evidence / blocked / deferred / wont_do / superseded | 0 |

## Findings

| Done | ID | Severity | Surface | Status | Finding | Evidence | Verification | Work item |
|---|---|---:|---|---|---|---|---|---|
| [x] | SR-UX-001 | 3 | install/discovery | verified | Installable skill maturity is not visible at the primary CLI discovery surface. Users can install draft and experimental skills without seeing the caveat in `npx skills add . --list`. | Product skill manifests are `published`; `.experimental/` has no installable skill dirs; `just check` lists 6 installable skills with no experimental labels. | `just check` passes and `npx skills add . --list` shows only promoted product skills. | Implemented in this change |
| [x] | SR-UX-002 | 2 | catalog/navigation | verified | README lists skills one by one but lacks a "which skill should I use?" chooser for overlapping prompts. | `README.md` now includes "Which skill should I use?" with common prompts and ambiguous cases. | README contains a routing matrix and `just check` passes. | Implemented in this change |
| [x] | SR-STRUCT-001 | 3 | internal-reviewer | verified | `skill-reviewer` and its rubric still describe a stale `skills/<pack>/<skill>` plus `references/use-case-registry.csv` contract, while this repo uses `skills/<name>`, `.experimental`, `.agents`, and multiple router shapes. Future reviews can falsely block valid two-level skills. | `.agents/skills/skill-reviewer/SKILL.md` and `references/review-rubric.md` now support root product skills, reserved experimental lane, repo-local skills, and accepted router shapes. | `skill-reviewer` static eval passes. | Implemented in this change |
| [x] | SR-CONTENT-001 | 2 | catalog/coverage | verified | The catalog promise is broad, but the installable catalog currently concentrates almost entirely on developer, testing, architecture, and coding-agent infrastructure workflows. | README now states the current catalog scope and adds user-facing UX/accessibility coverage. | README scope statement is present and `just check` passes. | Implemented in this change |
| [x] | SR-CONTENT-002 | 2 | ux-coverage | verified | End-user UX and accessibility are explicit negative cases for `dx-heuristics`, but the catalog has no replacement skill for those high-frequency user requests. | Added `skills/ux-accessibility-heuristics/`; DX negative cases now route/suggest it. | `npx skills add . --list` lists `ux-accessibility-heuristics`; its static eval passes. | Implemented in this change |
| [x] | SR-CONTENT-003 | 2 | output/citations | verified | The product promise says skills are grounded in citations so users can check the work, but most output templates do not require citing which sources influenced the result. | DX, test, clean-architecture, and UX templates include `Grounding sources applied`; SKILL output requirements reference `skill.json.inspired_by`. | `rg "Grounding sources applied" skills/*/templates` shows the added sections; `just check` passes. | Implemented in this change |
| [x] | SR-EVAL-001 | 2 | dx-heuristics/evals | verified | `dx-heuristics` trigger evals leave `expected_route` null for all positive queries, weakening route-level validation for a routed skill. | DX positive trigger evals now specify route strings such as `audit/cli`, `design/sdk`, `debug/auth`, and `design/plugin`. | `dx-heuristics` static eval passes. | Implemented in this change |
| [x] | SR-EVAL-002 | 2 | test-heuristics/evals | verified | Behavioral eval depth is uneven: `dx-heuristics` has a protocol, expected loads, and fail conditions; `test-heuristics` mostly has terse activation bullets. | Replaced terse test activation bullets with routed cases, expected loads, output shape, negative cases, boundary cases, and load discipline. | `test-heuristics` static eval passes. | Implemented in this change |
| [x] | SR-PD-001 | 2 | project-agentification/progressive-disclosure | verified | `project-agentification` playbooks are much larger than the 400-1500 word discipline used by other routed skills, and its static checks validate presence but not playbook structure or size. This increases load cost and drift risk. | `project-agentification` now documents the larger-playbook exception and statically gates playbook section shape plus a 900-3200 word bound. | `project-agentification` static eval prints bounded playbook checks and passes. | Implemented in this change |
| [x] | SR-CONTENT-004 | 1 | clean-architecture/frontend | verified | `clean-architecture` advertises full-stack friendliness while acknowledging thin frontend grounding, then routes React structure questions into a generic boundaries playbook with no dedicated frontend surface. | Clean architecture now scopes frontend to code architecture and routes product UX/forms/navigation/accessibility to `ux-accessibility-heuristics`; README and evals reflect that boundary. | `npx skills add . --list` shows the corrected description; `clean-architecture` static eval passes. | Implemented in this change |

## Decisions

- 2026-05-20 - Treated the review scope as the installable catalog shown by `npx skills add . --list`, plus internal authoring/review skills where they affect catalog quality.
- 2026-05-20 - Did not edit skill behavior; saved tracking artifacts only.
- 2026-05-20 - Implemented and verified all findings; current product skills are promoted to the root `skills/<name>/` lane.

## Blockers

- None.

## Closeout Notes

- 2026-05-20 - `just check` passes after allowing network access for `npx skills add . --list`; 6 installable product skills are listed.

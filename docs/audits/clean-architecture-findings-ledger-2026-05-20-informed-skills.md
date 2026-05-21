# clean-architecture Findings Ledger — informed-skills

**Skill:** clean-architecture
**Ledger file:** `docs/audits/clean-architecture-findings-ledger-2026-05-20-informed-skills.md`
**Source report:** clean-architecture audit/all conversation run on `/Users/justin/Dev/informed-skills`
**Created:** 2026-05-20
**Last updated:** 2026-05-21
**Owner:** Justin / informed-skills maintainers

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
| [x] | CA-CROSS-001 | 3 | cross-cutting | verified | Malformed hook payloads fail open at the destructive-command guard. | Shared hook policy now blocks uninspectable payloads; Claude and Codex subprocess smokes cover malformed JSON and non-object payloads. | `just check` passed on 2026-05-21. | WP-001 |
| [x] | CA-CONTEXT-001 | 3 | bounded-context | verified | Installability semantics mix lane-driven and maturity-status-driven models; a draft public skill is currently installable. | Product decision recorded: installable public skills are `published`; `.experimental/` stays empty; catalog prerelease maturity moves to repo tag `0.0.1-alpha`. Release contract enforces this. | `just check` passed on 2026-05-21; install discovery found 7 non-experimental skills. | WP-002 |
| [x] | CA-CONTEXT-002 | 3 | bounded-context | verified | `skill-curator` translates generic skill-shape guidance into public drafts without preserving this repo's required public-skill artifact contract. | Curator playbooks now generate repo-conformant published public skills and require eval artifacts; `skill-curator` has its own static check. | `just check` passed on 2026-05-21. | WP-002 |
| [x] | CA-BOUNDARY-001 | 2 | boundaries | verified | Shared-content integrity only covers top-level shared Markdown under `references/`, while shared templates are also a shared kernel. | Shared-content checker now scans symlinks under all skill lanes and validates consumers resolving into `skills/_shared/**`, including templates. | `just check` passed on 2026-05-21; 31 shared symlinks verified. | WP-003 |
| [x] | CA-CROSS-002 | 2 | cross-cutting | verified | Destructive-command policy is duplicated across Claude and Codex hook adapters, and only the Claude path is tested by local/CI gates. | Claude and Codex hooks are thin adapters over `scripts/hooks/destructive_bash_policy.py`; Just and CI run both hook test suites. | `just check` passed on 2026-05-21. | WP-001 |
| [x] | CA-BOUNDARY-002 | 2 | boundaries | verified | Repo-local skill lane has no explicit absent-script gate, so a repo-local skill can be treated as release-critical while carrying no static check. | Release contract enumerates `.agents/skills/*` and requires `SKILL.md`, `evals/run-static-checks.sh`, and `evals/activation-cases.md`; `skill-curator` now satisfies the contract. | `just check` passed on 2026-05-21. | WP-002 |
| [x] | CA-DEP-001 | 2 | dependency-rule | verified | Per-skill static checks depend directly on Git checkout shape and repo-local schema scripts instead of a stable validation port. | `scripts/static-check-lib.sh` owns repo-root discovery and common skill/trigger schema-name validation; per-skill scripts call the helper. | `just check` passed on 2026-05-21. | WP-004 |
| [x] | CA-DOMAIN-001 | 2 | domain-model | verified | `TriggerEvalCase` is an implicit value object with invariants split between prose and a loose schema. | Canonical schema now requires `expected_route` and `category`, constrains route identifiers, and rejects non-activating cases with a route; release contract rechecks route/category invariants. | `just check` passed on 2026-05-21. | WP-004 |
| [x] | CA-CROSS-003 | 2 | cross-cutting | verified | Local and CI install-discovery gates use different external dependency/config policy. | `scripts/list-installable-skills.sh` centralizes CLI version, cache, telemetry, and update-notifier policy; Just and CI call the wrapper. | `just check` passed on 2026-05-21. | WP-003 |
| [x] | CA-CROSS-004 | 2 | cross-cutting | verified | Static-check error policy and shared mechanics are repeatedly reimplemented per skill. | Common static-check helper covers repo-root discovery and canonical schema/name checks; skill scripts keep only skill-specific assertions. | `just check` passed on 2026-05-21. | WP-004 |

## Decisions

- 2026-05-20 — IDs assigned from the dominant surface when a finding appeared in multiple surface passes.
- 2026-05-20 — Roadmap and external issues were not created; those require explicit user request.
- 2026-05-21 — Product decision: no installable skills remain in draft or experimental lanes; repository prerelease maturity is communicated by the `0.0.1-alpha` tag.

## Blockers

- None.

## Closeout Notes

- All ten clean-architecture findings are implemented and verified locally by `just check`.
- The `0.0.1-alpha` release tag should be cut from the merge commit after the single PR lands.

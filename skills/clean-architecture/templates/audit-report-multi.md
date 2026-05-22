# Architecture Audit — multi-surface

**Target persona:** <from references/core/personas.md>
**Surfaces audited:** <list from references/intents/audit.csv, excluding the `all` row — one entry per surface this audit actually visited>
**Date:** <YYYY-MM-DD>

## Summary

<3–5 sentences. Headline scores per surface; the one or two findings
that show up across multiple surfaces (often the most load-bearing).>

## Fix three first

Across all surfaces audited, the three findings to act on this week — picked
for **impact × effort**, not strictly by severity, and biased toward
cross-surface patterns (they confirm each other and pay back more per fix).

If fewer than three cross-surface or sev-2+ findings exist, list however many
do.

1. **<finding ID>** (<surfaces it spans>) — <why this one>. _Verify by:_ <check>.
2. **<finding ID>** (<surfaces>) — <why this one>. _Verify by:_ <check>.
3. **<finding ID>** (<surfaces>) — <why this one>. _Verify by:_ <check>.

## Per-surface scores

One row per surface actually audited (drawn from `references/intents/audit.csv`, minus the `all` row).

| Surface | Score | Band | Top finding |
|---------|------:|------|-------------|
| <surface 1> | <0–10> | <band> | <one-line> |
| <surface 2> | <0–10> | <band> | <one-line> |
| ... |

## Cross-surface patterns

<Findings that appeared in two or more surface agents' reports.
These are usually the highest-leverage items because they confirm
each other. Assign one stable finding ID per distinct issue using
canonical surface prefixes (`CA-DEP`, `CA-BOUNDARY`, `CA-DOMAIN`,
`CA-CONTEXT`, `CA-CROSS`). If one issue spans surfaces, list every affected
surface under the same finding.>

## Per-surface details

One subsection per surface actually audited, in the same order as the per-surface scores table.

### <surface 1>

<Findings list from the surface agent, severity-ordered. Each finding includes
ID, severity, status, evidence, suggested fix, and verification rule.>

### <surface 2>

<...>

### ...

## Open questions

<Disagreements between surface agents; items where evidence was thin.>

## Findings ledger

For 7+ findings or any severity 3–4 finding, use
`references/trackable-findings.md` and create both tracking artifacts now: the
Markdown ledger from `templates/findings-ledger.md` at
`docs/audits/clean-architecture-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and the workflow state from `templates/workflow-state.json` at
`docs/audits/clean-architecture-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
Create the directory if needed. If the target is not a repo or `docs/audits/`
is not writable, use matching `audit-artifacts/clean-architecture-...` paths
instead. Report both saved paths, and do not merely offer or inline tracking
choices. Roadmaps and GitHub issues are opt-in; never create external issues
without confirmation. Check boxes only after verification passes.

## Verification

<How to reproduce the multi-surface audit — commands, surfaces visited,
lenses run per surface.>

## Grounding sources applied

- <skill.json inspired_by entry> - <cross-surface pattern it informed>

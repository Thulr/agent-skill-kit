# Architecture Audit — multi-surface

**Target persona:** <from references/core/personas.md>
**Surfaces audited:** <list from references/intents/audit.csv, excluding the `all` row — one entry per surface this audit actually visited>
**Date:** <YYYY-MM-DD>

## Summary

<3–5 sentences. Headline scores per surface; the one or two findings
that show up across multiple surfaces (often the most load-bearing).>

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
`references/trackable-findings.md` and create the ledger from
`templates/findings-ledger.md` now. Do not merely offer tracking choices.
Roadmaps, workflow state, and GitHub issues are opt-in; never create external
issues without confirmation. Check boxes only after verification passes.

## Verification

<How to reproduce the multi-surface audit — commands, surfaces visited,
lenses run per surface.>

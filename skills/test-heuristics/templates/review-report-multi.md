# Cross-Layer Test Review Report

**Layers reviewed:** [comma-separated]
**Persona:** suite operator (primary)

## Per-layer scores

| Layer | Score | Biggest gap |
|---|---|---|
| unit | X/10 | … |
| integration | X/10 | … |
| … | … | … |

## Suite-wide path to 10/10

1. [Top fix that lifts overall test quality most]
2. [Second]
3. [Third]

## Severity-ranked findings (cross-layer)

### Sev-4

- [Finding from layer X — ref full layer report]

### Sev-3

- …

## Findings ledger

If this review has 7+ findings, any severity 3–4 finding, or a save/track
request, create both tracking artifacts now: the Markdown ledger from
`templates/findings-ledger.md` at
`docs/audits/test-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and the workflow state from `templates/workflow-state.json` at
`docs/audits/test-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
If the target is not a repo or `docs/audits/` is not writable, use matching
`audit-artifacts/test-heuristics-...` paths. Report both paths; do not merely
offer tracking. Roadmaps and external issues require explicit confirmation.

## Per-layer reports (full)

[Append the full single-layer review-report.md content for each layer]

## Grounding sources applied

- [skill.json inspired_by entry] — [cross-layer recommendation it informed]

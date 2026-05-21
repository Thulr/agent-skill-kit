<!-- Load-bearing section: Findings -->
# DX Audit: <surface>

## Score
- Current: <0-10>
- Target: 10/10
- Target developer: <persona from references/core/personas.md>
- Intended outcome: <task the developer should accomplish>
- Playbook(s) applied: <e.g., cli.md, errors.md>

## Summary

<One short paragraph: the highest-impact DX gap and the fastest path to improvement.>

## Findings

One block per finding. Repeat as needed.

### Finding 1 — severity <0-4>
- Location:   <file / API / CLI / doc / line>
- Heuristic:  <named heuristic from playbook>
- Problem:    <what fails>
- Fix:        <specific change>
- Verify:     <how to prove the fix worked>

## Path to 10/10

1. <Highest leverage fix>
2. <Next fix>
3. <Polish or hardening>

## Findings ledger

If this audit has 7+ findings, any severity 3–4 finding, or a save/track
request, create both tracking artifacts now: the Markdown ledger from
`templates/findings-ledger.md` at
`docs/audits/dx-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and the workflow state from `templates/workflow-state.json` at
`docs/audits/dx-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
Create the directory if needed. If the target is not a repo or `docs/audits/`
is not writable, use matching `audit-artifacts/dx-heuristics-...` paths.
Populate and report both saved paths; do not merely offer or inline tracking.
Roadmaps and external issues require explicit confirmation.

## Evidence reviewed

- <file, command, doc, PR, log, screenshot, or observed behavior>

## Grounding sources applied

- <skill.json inspired_by entry> - <why it mattered here>

## Open questions

- <Only questions that affect the recommendation>

## Accepted trade-offs

- <Intentional DX compromises and rationale>

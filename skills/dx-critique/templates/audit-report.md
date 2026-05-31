<!-- Load-bearing section: Findings -->
# DX Audit: <surface>

## First impressions
- Score: <passed> / <applicable> (from `references/first-impressions-checklist.md`;
  skipped items reduce the denominator — e.g. `8 / 9 (1 skipped)`)
- Failed items: list the numbered checklist items that returned "no". Example:
  `2 (install not on first screen), 5 (--version returns "dev")`.
  Omit this line if all applicable items pass. Skip this whole section only
  when none of the 10 items apply (e.g. a pure internal API with no README,
  install, CLI, error path, or changelog).

## Score
- Current: <0-10> (capped at 7 if more than two applicable first-impressions
  items failed; the cap floats with the applicable denominator, so a
  6 / 9 scan with 3 fails still triggers the cap)
- Target: 10/10
- Target developer: <persona from references/core/personas.md>
- Intended outcome: <task the developer should accomplish>
- Playbook(s) applied: <e.g., cli.md, errors.md>

## Summary

<One short paragraph: the highest-impact DX gap and the fastest path to improvement.>

## Fix three first

The three findings to act on this week, picked for **impact × effort** — not
strictly by severity. A sev-3 item that costs a quarter should not crowd out a
sev-2 item the team can land in a day.

Skip this section if every finding is severity ≤ 1. List however many exist if
there are fewer than three.

1. **<finding ID>** — <why this one in one sentence>. _Verify by:_ <narrow check>.
2. **<finding ID>** — <why this one>. _Verify by:_ <narrow check>.
3. **<finding ID>** — <why this one>. _Verify by:_ <narrow check>.

These are not the same list as "Path to 10/10" below — Fix-three optimizes
impact-per-day; Path to 10/10 sequences the journey to a healthy surface.

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
`docs/audits/dx-critique-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and the workflow state from `templates/workflow-state.json` at
`docs/audits/dx-critique-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
Create the directory if needed. If the target is not a repo or `docs/audits/`
is not writable, use matching `audit-artifacts/dx-critique-...` paths.
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

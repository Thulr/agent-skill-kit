# UX Accessibility Review - <use-case>

**Target user:** <persona or user group>
**Task:** <task the user is trying to complete>
**Interface state:** <screen, flow, component, error state>
**Lenses used:** <first-time user / keyboard-only / assistive-tech / returning / stressed user / policy>
**Playbooks applied:** <files>

## Summary

<2-4 sentences: highest-impact task failure, accessibility risk, and next fix.>

## Fix three first

The three findings to act on this week, picked for **impact × effort** — not
strictly by severity. A high-severity refactor of an information architecture
should not crowd out a medium-severity label fix the team can land in an hour.

Accessibility note: any finding that blocks an assistive-tech user from
completing the task should appear here regardless of effort — exclusion is
not deferrable.

Skip if every finding is severity ≤ 1. List however many exist if fewer than
three.

1. **<finding ID>** — <why this one in one sentence>. _Verify by:_ <keyboard
   pass, screen-reader transcript, contrast check, or user task>.
2. **<finding ID>** — <why this one>. _Verify by:_ <check>.
3. **<finding ID>** — <why this one>. _Verify by:_ <check>.

## Findings

Ordered by severity.

### UX-<SURFACE>-001 - <short finding>

- **Severity:** <0-4>
- **Status:** discovered
- **Heuristic:** <named heuristic>
- **Evidence:** <screen state, selector, file:line, screenshot, transcript, or observed behavior>
- **Impact:** <who fails and how>
- **Fix:** <specific design/content/code change>
- **Verification:** <keyboard pass, screen-reader check, contrast check, user task, analytics, or regression test>
- **WCAG note:** <likely criterion, not applicable, or needs specialist confirmation>

## Findings ledger

If this review has 7+ findings, any severity 3-4 finding, or a save/track
request, create both tracking artifacts now: the Markdown ledger from
`templates/ux/findings-ledger.md` at
`docs/audits/review-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and the workflow state from `templates/ux/workflow-state.json` at
`docs/audits/review-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
If the target is not a repo or `docs/audits/` is not writable, use matching
`audit-artifacts/review-heuristics-...` paths. Report both paths;
do not merely offer tracking.

## Grounding sources applied

- <skill.json inspired_by entry> - <why it mattered here>

## Verification

- <manual check or test>
- <automated scan if relevant, explicitly marked as partial evidence>

## Open questions

- <Only questions that affect the recommendation>

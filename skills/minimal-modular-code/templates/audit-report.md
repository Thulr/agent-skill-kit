# Minimal Modular Code — REVIEW — <surface>

**Target persona:** <from references/core/personas.md>
**Playbook applied:** `references/playbooks/<surface>.md`
**Score:** <0–10 from references/core/score-rubric.md> — <Exemplary / Healthy / Mixed / Eroded / Tangled / Absent>
**Project tier:** <Prototype | Growing | Load-bearing> (per references/calibration.md)
**Date:** <YYYY-MM-DD>

## Summary

<2–4 sentences: what was reviewed, what the headline score means, the single most
load-bearing finding.>

## Fix three first

The three findings to act on first, picked for **impact × effort**, not strictly by severity.
If there are fewer than three findings, list however many exist; if every finding is severity
≤ 1, skip this section.

1. **<MM-...>** — <why this one>. _Verify by:_ <narrow check>.
2. **<MM-...>** — <why>. _Verify by:_ <narrow check>.
3. **<MM-...>** — <why>. _Verify by:_ <narrow check>.

## Findings

Ordered by severity (4 → 0). Each finding cites the playbook heuristic that surfaced it and
carries a stable ID with the surface prefix: `MM-MIN`, `MM-LEG`, `MM-BND`, `MM-PAR`, or
`MM-ENF`.

### MM-MIN-001 — <short name>

- **Severity:** <0–4>
- **Status:** discovered
- **Heuristic:** <playbook heuristic # and intent tag>
- **Evidence:** <file:line, snippet, or pattern>
- **Why this matters:** <one sentence — what attention or rework it will cost>
- **Suggested fix:** <one or two sentences; full sequencing belongs in a refactor runbook>
- **Verification:** <narrow check that proves this finding is fixed>

### MM-MIN-002 — ...

(repeat per finding)

## Later — as it grows

Best-practice that does not pay off at the current **Project tier**. Keep it as a checklist to
revisit when the project moves up a tier — do not file it as findings now. At Load-bearing,
write "none — full coverage applied".

- <deferred item> — worth doing at <Growing | Load-bearing>

## Findings ledger

If this report has 7+ findings or any severity 3–4 finding, create both tracking artifacts
now: the Markdown ledger from `templates/findings-ledger.md` at
`docs/audits/minimal-modular-code-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and the
workflow state from `templates/workflow-state.json` at
`docs/audits/minimal-modular-code-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`. Create the
directory if needed. If the target is not a repo or `docs/audits/` is not writable, use
matching `audit-artifacts/minimal-modular-code-...` paths instead. Report both saved paths;
do not merely offer or inline tracking choices. Roadmaps and GitHub issues are opt-in; never
create external issues without confirmation.

## Open questions

<Items where the lenses disagreed, or where evidence was insufficient.>

## Verification

<How to verify the review reproduced — commands, files inspected, lenses run.>

## Grounding sources applied

- <skill.json inspired_by entry> — <finding it informed>

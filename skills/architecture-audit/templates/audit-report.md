# Architecture Audit — <surface>

**Target persona:** <from references/core/personas.md>
**Playbook applied:** `references/playbooks/<surface>.md`
**Score:** <0–10 from references/core/score-rubric.md> — <Exemplary / Healthy / Mixed / Eroded / Inverted / Absent>
**Date:** <YYYY-MM-DD>

## Summary

<2–4 sentences. What surface was audited, what the headline score means,
the single most load-bearing finding.>

## Fix three first

The three findings to act on this week, picked for **impact × effort**, not
strictly by severity. A high-severity item that requires a quarter-long refactor
should not crowd out a medium-severity item the team can land in a day.

If there are fewer than three findings, list however many exist. If every
finding is severity ≤ 1, skip this section.

1. **<finding ID>** — <one sentence on why this one>. _Verify by:_ <narrow check>.
2. **<finding ID>** — <one sentence>. _Verify by:_ <narrow check>.
3. **<finding ID>** — <one sentence>. _Verify by:_ <narrow check>.

## Findings

Ordered by severity (4 → 0). Each finding cites the playbook heuristic
that surfaced it and carries a stable tracking ID. Use the canonical
surface prefixes: `CA-DEP`, `CA-BOUNDARY`, `CA-DOMAIN`, `CA-CONTEXT`, or
`CA-CROSS`.

### CA-DEP-001 — <short name>

- **Severity:** <0–4>
- **Status:** discovered
- **Heuristic:** <playbook heuristic # and intent tag>
- **Evidence:** <file:line, snippet, or pattern>
- **Why this matters:** <one sentence>
- **Suggested fix:** <one or two sentences; full sequencing belongs in a refactor runbook>
- **Verification:** <narrow check that proves this finding is fixed>

### CA-DEP-002 — ...

(repeat per finding)

## Findings ledger

If this report has 7+ findings or any severity 3–4 finding, create both
tracking artifacts now: the Markdown ledger from `templates/findings-ledger.md`
at
`docs/audits/architecture-audit-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and the workflow state from `templates/workflow-state.json` at
`docs/audits/architecture-audit-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
Create the directory if needed. If the target is not a repo or `docs/audits/`
is not writable, use matching `audit-artifacts/architecture-audit-...` paths
instead. Report both saved paths, and do not merely offer or inline tracking
choices. Roadmaps and GitHub issues are opt-in; never create external issues
without confirmation.

## Open questions

<Items where the three lenses disagreed, or where evidence was insufficient.>

## Verification

<How to verify the audit reproduced — commands, files inspected, lenses run.>

## Grounding sources applied

- <skill.json inspired_by entry> - <architecture finding it informed>

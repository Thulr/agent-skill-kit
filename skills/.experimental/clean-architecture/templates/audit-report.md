# Architecture Audit — <surface>

**Target persona:** <from references/core/personas.md>
**Playbook applied:** `references/playbooks/<surface>.md`
**Score:** <0–10 from references/core/score-rubric.md> — <Exemplary / Healthy / Mixed / Eroded / Inverted / Absent>
**Date:** <YYYY-MM-DD>

## Summary

<2–4 sentences. What surface was audited, what the headline score means,
the single most load-bearing finding.>

## Findings

Ordered by severity (4 → 0). Each finding cites the playbook heuristic
that surfaced it and carries a stable tracking ID (`CA-<surface>-NNN`).

### <CA-<surface>-001> — <short name>

- **Severity:** <0–4>
- **Status:** discovered
- **Heuristic:** <playbook heuristic # and intent tag>
- **Evidence:** <file:line, snippet, or pattern>
- **Why this matters:** <one sentence>
- **Suggested fix:** <one or two sentences; full sequencing belongs in a refactor runbook>
- **Verification:** <narrow check that proves this finding is fixed>

### <CA-<surface>-002> — ...

(repeat per finding)

## Tracking offer

If this report has 7+ findings, any severity 3–4 finding, or the user asks
for follow-through, offer to create:

- `templates/findings-ledger.md` — source of truth for statuses and evidence.
- `templates/roadmap.md` — grouped work packages.
- `templates/github-issue.md` — issue-shaped work packages, only with confirmation.
- `templates/workflow-state.json` — machine-readable continuation state.

Checking off a finding requires a verification closeout pass; `implemented`
is not enough.

## Open questions

<Items where the three lenses disagreed, or where evidence was insufficient.>

## Verification

<How to verify the audit reproduced — commands, files inspected, lenses run.>

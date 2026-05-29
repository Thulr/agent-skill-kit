# Audit Mechanics

Use this reference for clean-architecture audits, tracking follow-through, and
closeout. It keeps the mechanics stable so the playbooks can focus on
architecture judgment.

## Canonical Finding IDs

Use these prefixes exactly. Do not emit full CSV names in IDs.

| Audit surface | Prefix | Example |
|---|---|---|
| `dependency-rule` | `CA-DEP` | `CA-DEP-001` |
| `boundaries` | `CA-BOUNDARY` | `CA-BOUNDARY-001` |
| `domain-model` | `CA-DOMAIN` | `CA-DOMAIN-001` |
| `bounded-context` | `CA-CONTEXT` | `CA-CONTEXT-001` |
| `cross-cutting` | `CA-CROSS` | `CA-CROSS-001` |

IDs are immutable. If a cross-surface issue is the same defect, keep one ID
from the dominant surface and list every affected surface under that finding.
If the issue is two defects with shared symptoms, split it into separate IDs.

## Host Synthesis Responsibilities

Peer subagents cannot observe each other. The host agent owns:

- deduplicating findings across lenses and surfaces,
- preserving disagreements as open questions,
- ordering by severity,
- assigning canonical IDs,
- mapping every output to the real template file from
  `references/architecture/intent-router.csv`,
- creating tracking artifacts when thresholds are met,
- and extracting exact IDs during closeout.

Lens agents should return evidence and severity, not final sequencing or final
status decisions.

## Tracking And Closeout

Closeout starts from a ledger, workflow-state file, PR, diff, or user-supplied
finding ID. Extract IDs by canonical prefix (`CA-DEP`, `CA-BOUNDARY`,
`CA-DOMAIN`, `CA-CONTEXT`, `CA-CROSS`) and rerun each finding's verification
rule. Mark `verified` only when the rule passes. Leave status unchanged when
evidence is inconclusive; use `needs_evidence` only when the next evidence
request is specific.

## Template Source Of Truth

The default output template comes from `references/architecture/intent-router.csv`:

- audit -> `templates/architecture/audit-report.md`
- design -> `templates/architecture/design-doc.md`
- refactor -> `templates/architecture/refactor-runbook.md`
- explain -> `templates/architecture/explanation.md`

For `audit/all`, use `templates/architecture/audit-report-multi.md`. Do not write
placeholder paths like `templates/<intent>.md`; they are not real files.

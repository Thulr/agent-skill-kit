# Trackable findings — ledger + workflow-state contract

Used when the skill produces 5+ area artifacts, any severity 3–4
finding, or a save/track/closeout request. Two artifacts get written
in parallel — a human-readable ledger and a machine-parseable
workflow-state.

## Identifiers

Stable IDs for tracked findings follow this pattern:

```
OR-<surface>-NNN
```

- `OR` for the research opportunity frame.
- `<surface>` matches a row in `references/opportunity/intents/investigate.csv`
  (market, customer, ..., trend) or one of `scope`, `synthesize`,
  `decide` for cross-cutting findings.
- `NNN` is a zero-padded counter, monotonic per (skill, scope).

Examples: `OR-market-001`, `OR-risk-003`, `OR-decide-001`.

IDs are stable across re-runs. If the same finding is re-discovered
in a subsequent investigation, reuse the ID and update status; do
not allocate a new ID.

## Ledger (Markdown)

Path:
`docs/audits/research-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`

Fallback (if `docs/audits/` is unwritable):
`audit-artifacts/research-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`

Use [`templates/opportunity/findings-ledger.md`](../../templates/opportunity/findings-ledger.md)
as the starting point. Each finding is one row with: ID, area,
severity, confidence, claim (one line), evidence (citation or
artifact reference), F-A-D-R category, mitigation / next test, owner,
status (open / in-progress / blocked / resolved / wont-fix), last
review date.

## Workflow-state (JSON)

Path:
`docs/audits/research-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`

Fallback:
`audit-artifacts/research-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`

Schema (machine-parseable for resumption / closeout): fill
`templates/opportunity/workflow-state.json` — the canonical shape, including
the `decision_gate.status` vocabulary (`pending | Go | Conditional-Go |
No-Go | Pivot | Defer`). Do not restate the schema here.

## Resumption rules

When the user re-invokes the skill on the same opportunity (matched
by `opportunity_slug` or named artifact path):

1. Load the workflow-state JSON first.
2. Read saved status — do not re-investigate areas marked
   `completed` unless explicitly asked.
3. Update statuses **only after each verification rule passes** —
   e.g., a finding marked `resolved` requires the artifact at the
   cited path to reflect the resolution.
4. New findings get new IDs; re-discovered findings update existing
   IDs.

## Closeout rules

When the user says "close out" / "wrap up" / "the bet is dead":

1. Mark `decision_gate.status` to its final value (go / no-go /
   pivot).
2. Move open findings to `wont-fix` with a reason, or `resolved`
   with the closing evidence cited.
3. Update the ledger with a "Closeout summary" section listing the
   top-3 facts, assumptions tested, decision, and kill criteria.
4. The workflow-state remains on disk for retrospective; do not
   delete.

## Verification rules

Before updating a finding's status:

- `open → in-progress`: a named owner must be present.
- `in-progress → resolved`: the cited evidence must exist (URL,
  artifact, file path) and the artifact's F-A-D-R section must
  reflect the resolution.
- `* → wont-fix`: must include a reason (out-of-scope / pivoted /
  obsolete) and a closing date.
- `* → blocked`: must include the named blocker.

These rules are what stop the ledger from becoming a graveyard of
unmaintained findings.

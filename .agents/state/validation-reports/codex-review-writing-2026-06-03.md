# Codex Review — writing-audit + writing-design (2026-06-03)

External pre-PR review via `codex review --uncommitted` (codex-cli 0.135.0).
Raw transcript discarded (Finding 5); this is the distilled outcome + reconciliation.

> Tooling note: the global `codex-cli` skill's `codex-review-changes.sh` passes
> `codex review --uncommitted -- -`, which codex ≥0.135.0 rejects (`--uncommitted`
> and a `[PROMPT]` positional are now mutually exclusive). Ran `codex review
> --uncommitted` directly instead. New files were `git add -N`'d first so the
> review saw their content, not collapsed untracked-dir entries.

## Findings (5, all P2) and reconciliation

| # | Finding | Verdict | Resolution |
|---|---|---|---|
| 1 | `writing-design` advertises intent×genre but `structure.csv` omits `general-prose` and `persuade.csv` omits `technical-doc` — advertised-but-unrouted cells | **Valid** | Added `structure/general-prose` row; for the genuinely-marginal `persuade/technical-doc`, added a workflow clause (step 2) that routes an unserved (intent,genre) to the nearest served pairing and names it (a compelling how-to is the `narrative` genre, not `persuade`). |
| 2 | `writing-audit` `diagnose.csv` omits `general-prose`, but a short piece can bury the point | **Valid** | Added `diagnose/general-prose` row. Audit matrix now complete (3×5). |
| 3 | Audit report templates lack a grounding slot, violating the SKILL.md "every output cites grounding sources" contract | **Valid** | Added `**Grounding:**` to `revision-report`, `copyedit-report`, `diagnosis-report`. |
| 4 | `outline-plan` lacks a guards-honored field; `draft-scaffold` lacks grounding | **Valid** | Added `## Guards honored` to `outline-plan`; `**Grounding:**` to `draft-scaffold`. |
| 5 | The raw 4,800-line `tee` transcript (session id, sandbox settings) shouldn't be a committed release artifact | **Valid** | Deleted the raw transcript; distilled into this report. |

No findings were misreads of the symlinked-playbook structure. No correctness,
security, or copyright findings were raised — consistent with the local
copyright scan (clean) and `just check` (green).

## Supporting change: general-prose playbook

To make the two new `general-prose` routes load relevant content, added a
`(structure, diagnose)` "lead with the point" heuristic, updated the Scope
intent line, and cross-referenced `structure-rubric.md`. Still within the
400–1500-word band.

## Post-fix re-validation

See the run recorded alongside this report: both per-skill static checks,
`validate-generated-skill.py --shape two-level`, and `just check` re-run green
after the edits.

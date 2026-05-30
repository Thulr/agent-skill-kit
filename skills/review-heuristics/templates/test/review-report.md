# Test Review Report

**Layer:** [unit | integration | …]
**Scope:** [file or directory or test class]
**Persona:** [primary persona for this review]
**Score:** [0–10] (clarity X / coverage X / cost X / robustness X)

## Summary

[2–3 sentences: biggest gap, biggest strength, recommended priority action]

## Fix three first

The three findings to act on this week, picked for **impact × effort** — not
strictly by severity. A sev-3 test-design problem that requires reshaping a
fixture should not crowd out a sev-2 oracle gap the author can fix in an hour.

Skip if every finding is severity ≤ 1. List however many exist if there are
fewer than three.

1. **[finding ID]** — [why this one]. _Verify by:_ [narrow check — usually a
   re-run with a mutated SUT or a deleted assertion].
2. **[finding ID]** — [why this one]. _Verify by:_ [check].
3. **[finding ID]** — [why this one]. _Verify by:_ [check].

## Findings

### Finding 1: [Heuristic name]

- **Location:** `path:line`
- **Severity:** [0–4]
- **Failure mode(s):** [list]
- **Lens(es) flagged it:** [intent reader | refactor adversary | bug-shape hunter]
- **What fails:** [Description]
- **Fix:** [Description with code if needed]
- **Verification:** [How to prove the fix worked]

### Finding 2: …

## Open questions (lens disagreement)

- [Question raised when one lens flagged X and another lens explicitly approved it]

## Findings ledger

If this review has 7+ findings, any severity 3–4 finding, or a save/track
request, create both tracking artifacts now: the Markdown ledger from
`templates/test/findings-ledger.md` at
`docs/audits/review-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and the workflow state from `templates/test/workflow-state.json` at
`docs/audits/review-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
If the target is not a repo or `docs/audits/` is not writable, use matching
`audit-artifacts/review-heuristics-...` paths. Report both paths; do not merely
offer tracking. Roadmaps and external issues require explicit confirmation.

## Verification

[Suite-level checks that should pass after applying the fixes]

## Grounding sources applied

- [skill.json inspired_by entry] — [finding or recommendation it informed]

# Test Review Report

**Layer:** [unit | integration | …]
**Scope:** [file or directory or test class]
**Persona:** [primary persona for this review]
**Score:** [0–10] (clarity X / coverage X / cost X / robustness X)

## Summary

[2–3 sentences: biggest gap, biggest strength, recommended priority action]

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

## Verification

[Suite-level checks that should pass after applying the fixes]

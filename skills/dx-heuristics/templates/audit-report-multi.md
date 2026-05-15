<!-- Load-bearing section: Findings -->
# DX Audit (multi-surface): <project / target>

## Scope
- Surfaces audited: <e.g., all 14, or listed subset>
- Target developer: <persona from references/core/personas.md>
- Trigger: <pre-ship / release / customer signal / scheduled review>

## Scores per surface

Lowest → highest. Score from `references/core/score-rubric.md`.

- <surface>: <0-10> — <one-line biggest gap>
- <surface>: <0-10> — <one-line biggest gap>
- ...

## Summary

<One short paragraph: the highest-impact DX gaps across the project and
the single intervention that lifts overall DX the most.>

## Top cross-surface findings

Ranked by severity, highest first. One block per finding; up to 10.

### Finding 1 — severity <0-4> — surface: <surface>
- Location:   <file / API / CLI / doc / line>
- Heuristic:  <named heuristic from playbook>
- Problem:    <what fails>
- Fix:        <specific change>
- Verify:     <how to prove the fix worked>

## Project-wide path to 10/10

Fixes that lift overall DX, not per-surface polish.

1. <Highest leverage cross-surface fix>
2. <Next>
3. <Polish or hardening>

## Per-surface highlights

One block per surface. Full per-surface reports appended below.

### <surface>
- Score: <0-10>
- Biggest gap: <one line>
- Top finding: <pointer to "Finding N" above, or inline summary>

## Evidence reviewed

- <surface>: <files, commands, docs, PRs, logs reviewed>

## Open questions

- <Only questions that affect the project-wide recommendation>

## Accepted trade-offs

- <Intentional DX compromises and rationale>

---

## Per-surface reports (appended)

<Each surface agent's full audit-report.md content, appended in order
from lowest score to highest.>

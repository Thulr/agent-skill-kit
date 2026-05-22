<!-- Load-bearing section: Findings -->
# Perf and Observability Audit (multi-surface): <project / target>

## Scope
- Surfaces audited: <e.g., all 7, or listed subset>
- Target persona: <persona from references/core/personas.md>
- Trigger: <pre-launch / incident follow-up / scheduled review / customer signal>

## Scores per surface

Lowest -> highest. Score from `references/core/score-rubric.md`.

- <surface>: <0-10> — <one-line biggest gap>
- <surface>: <0-10> — <one-line biggest gap>
- ...

## Summary

<One short paragraph: the highest-impact gaps across the project and the single intervention that lifts overall posture the most.>

## Fix three first

Across all surfaces audited, the three findings to act on this week — picked for **impact x effort**, biased toward cross-surface patterns. If fewer than three cross-surface or sev-2+ findings exist, list however many do.

1. **<finding ID>** (<surfaces>) — <why this one>. _Verify by:_ <measurable check>.
2. **<finding ID>** (<surfaces>) — <why this one>. _Verify by:_ <measurable check>.
3. **<finding ID>** (<surfaces>) — <why this one>. _Verify by:_ <measurable check>.

## Findings

Cross-surface findings ranked by severity, highest first. One block per finding; up to 10.

### Finding 1 — severity <0-4> — surface: <surface>
- Location:     <service / endpoint / dashboard / runbook / config>
- Heuristic:    <named heuristic from playbook>
- Problem:      <what fails, with the observation that triggered it>
- Measurement:  <how this was measured>
- Fix:          <specific change>
- Verify:       <how to prove the fix worked — measurement method named>

## Project-wide path to 10/10

Fixes that lift overall posture, not per-surface polish.

1. <Highest leverage cross-surface fix>
2. <Next>
3. <Polish or hardening>

## Findings ledger

If this audit has 7+ findings, any severity 3-4 finding, or a save / track request, create both tracking artifacts now: the Markdown ledger from `templates/findings-ledger.md` at `docs/audits/perf-observability-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and the workflow state from `templates/workflow-state.json` at `docs/audits/perf-observability-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`. Create the directory if needed. If the target is not a repo or `docs/audits/` is not writable, use matching `audit-artifacts/perf-observability-heuristics-...` paths. Populate and report both saved paths; do not merely offer or inline tracking. Roadmaps and external issues require explicit confirmation.

## Per-surface highlights

One block per surface. Full per-surface reports appended below.

### <surface>
- Score: <0-10>
- Biggest gap: <one line>
- Top finding: <pointer to "Finding N" above, or inline summary>

## Evidence reviewed

- <surface>: <dashboard URLs, profile artifacts, trace IDs, log queries, runbooks, alert configs, SLO configs>

## Grounding sources applied

- <skill.json inspired_by entry> - <surface or finding it informed>

## Open questions

- <Only questions that affect the project-wide recommendation>

## Accepted trade-offs

- <Intentional perf / observability compromises and rationale>

---

## Per-surface reports (appended)

<Each surface agent's full audit-report.md content, appended in order from lowest score to highest.>

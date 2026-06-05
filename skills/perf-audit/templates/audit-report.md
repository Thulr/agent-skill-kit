<!-- Load-bearing section: Findings -->
# Perf and Observability Audit: <surface>

## Score
- Current: <0-10>
- Target: 10/10
- Target persona: <persona from references/core/personas.md>
- Intended outcome: <reliability / performance posture the team should hold>
- Project tier: <Prototype | Growing | Load-bearing> (per references/calibration.md)
- Playbook(s) applied: <e.g., latency.md, slos.md>

## Summary

<One short paragraph: the highest-impact gap and the fastest path to improvement. Name the measurement method, not just the metric.>

## Fix three first

The three findings to act on this week, picked for **impact x effort** — not strictly by severity. A sev-3 item that costs a quarter should not crowd out a sev-2 item the team can land in a day.

Skip this section if every finding is severity <= 1. List however many exist if there are fewer than three.

1. **<finding ID>** — <why this one in one sentence>. _Verify by:_ <narrow measurable check>.
2. **<finding ID>** — <why this one>. _Verify by:_ <narrow measurable check>.
3. **<finding ID>** — <why this one>. _Verify by:_ <narrow measurable check>.

These are not the same list as "Path to 10/10" below — Fix-three optimizes impact-per-day; Path to 10/10 sequences the journey to a healthy posture.

## Findings

One block per finding. Repeat as needed. Each finding cites the playbook heuristic and names the measurement method.

### Finding 1 — severity <0-4>
- Location:     <service / endpoint / dashboard / runbook / config>
- Heuristic:    <named heuristic from playbook>
- Problem:      <what fails, with the observation that triggered it>
- Measurement:  <how this was measured — profile, histogram, trace, SLI; coordinated-omission status if applicable>
- Fix:          <specific change>
- Verify:       <how to prove the fix worked — measurement method named>

## Path to 10/10

1. <Highest leverage fix>
2. <Next fix>
3. <Polish or hardening>

## Later — as it grows

Best-practice that doesn't pay off at the current **Project tier**. Keep it as a
checklist to revisit when the project moves up a tier — don't file it as findings
now. At Load-bearing, write "none — full coverage applied".

- <deferred item> — worth doing at <Growing | Load-bearing>

## Findings ledger

If this audit has 7+ findings, any severity 3-4 finding, or a save / track request, create both tracking artifacts now: the Markdown ledger from `templates/findings-ledger.md` at `docs/audits/perf-audit-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and the workflow state from `templates/workflow-state.json` at `docs/audits/perf-audit-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`. Create the directory if needed. If the target is not a repo or `docs/audits/` is not writable, use matching `audit-artifacts/perf-audit-...` paths. Populate and report both saved paths; do not merely offer or inline tracking. Roadmaps and external issues require explicit confirmation.

## Evidence reviewed

- <dashboard URL, profile artifact, trace ID, log query, runbook, alert config, SLO config>

## Grounding sources applied

- <skill.json inspired_by entry> - <why it mattered here>

## Open questions

- <Only questions that affect the recommendation>

## Accepted trade-offs

- <Intentional perf / observability compromises and rationale (e.g., sampling rate vs cost, retention vs cost)>

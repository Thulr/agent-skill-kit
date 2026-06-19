# Trajectory Tests Playbook

## Scope

Designing tests that grade the **path**, not the step. An agent run is an ordered
sequence of spans — a tool selected, a hand-off made, a retry fired, a sub-agent
invoked — and a multi-step run can fail while every individual span passes. This
surface designs the instruments that reassemble those spans into the ordered
trajectory and assert on tool-selection order, hand-offs, and loop/retry counts,
so loops, wrong-tool calls, and lost hand-offs are caught at the run level rather
than hidden behind green per-step content.

- **In:** designing run-level evals; reassembling spans into an ordered trajectory
  and asserting on tool-order, hand-offs, retry/loop counts; defining the
  failure-mode ontology a trajectory localizes; computing the compounded
  multi-step pass rate (the march of nines); trace-linked localization so a failed
  run names *where* it broke.
- **Out:** operating the trace stream, watching drift, or running the loop in
  production (`agent-ops`); designing the spans/capture toggles that emit the
  trajectory (that is an SDK concern, consumed here, not authored here); judge
  rubric calibration (`judge-calibration`); single-call schema/parser metrics
  (`eval-design`); model-swap/release gating suites (`benchmark-design`).
- **Intents this surface answers:** do, review, design.

## Grounding

- A trajectory is the ordered list of spans for one run: each span carries a
  prompt, completion, and tool I/O. Grading per-span content alone is Trajectory
  Blindness — the path between spans (order, branching, hand-offs, loops) is where
  multi-step agents actually fail.
- A 0.95 per-step bar is not a 0.95 run bar. Across an N-step agent it compounds
  toward 0.95^N — the **march of nines** — so a run-level eval must score the run,
  and the per-step bar must be read as a factor, not the target.
- Trajectory assertions are mostly deterministic: tool-selection order, presence
  of a required hand-off, and a retry/loop count over a ceiling are checkable
  without a judge. Reserve a calibrated judge for content quality at a node; use a
  deterministic check wherever the property is checkable.
- Public agent suites (SWE-bench / SWE-agent trajectories, τ-bench tool-use
  conversations, WebArena episodes) score the completed task and its action
  sequence, not isolated turns — the convention is task/run-level grading with the
  trajectory retained for localization.

## Good signals

- Every run-level eval reassembles spans into an ordered trajectory before
  scoring, and the assertions name a path property (tool order, hand-off present,
  loop count) rather than only per-node content.
- Each trajectory test maps to a named failure mode (loop, wrong-tool, lost
  hand-off, premature stop) drawn from an explicit ontology, so a failure localizes
  to *where* and *how*, not just pass/fail.
- The compounded multi-step pass rate is computed and gated on, not the per-step
  rate read as if it were the run bar.
- Loop/retry counts are asserted against a ceiling, so a run that eventually
  succeeds after 14 retries is flagged, not silently passed.
- Required hand-offs (planner→executor, agent→sub-agent, agent→human) are asserted
  as present and correctly ordered; a dropped or out-of-order hand-off fails the
  run.
- Deterministic path assertions are used wherever the property is checkable; a
  judge is invoked only for node-content quality and only when calibrated.
- A failed trajectory test points at the offending span (trace-linked), so triage
  starts at the break, not at the top of the run.

## Common failures

- **Trajectory Blindness.** Only per-span content is graded; every span is green
  while the run fails via a loop, a wrong tool, or a lost hand-off. The path is
  never reassembled.
- **The march of nines.** A 0.95 per-step bar is treated as the run bar; across a
  multi-step agent it compounds to a production pass rate far below target, and the
  suite reports a number the system never hits.
- **Step-soup scoring.** Spans are graded as an unordered bag — tool-selection
  order and hand-off sequence are lost, so an agent that calls the right tools in
  the wrong order passes.
- **Loop blindness.** Success is scored on final state only; a run that retried 30
  times or cycled between two tools passes because it eventually landed, masking a
  cost and reliability defect.
- **Judge-on-the-path overreach.** A judge grades the whole trajectory holistically
  when deterministic order/count assertions would be cheaper, more stable, and not
  gameable.
- **Untraceable failure.** A run is marked failed with no span-level localization,
  so the failure mode can't be named and the eval can't be improved.
- **Single-run flake masking.** A flaky non-deterministic trajectory is judged on
  one execution; intermittent loops/hand-off drops are neither detected nor counted.

## Heuristics

- **(do, review, design) Reassemble before you assert.** Stitch spans into the
  ordered trajectory first; any assertion that doesn't reference path order,
  hand-offs, or loop/retry counts is a per-step test mislabeled as run-level.
- **(design) Name the failure-mode ontology first.** Before scoring, enumerate how
  the run fails — loop, wrong-tool, lost hand-off, premature stop, redundant work —
  and design one trajectory assertion per mode so a failure localizes.
- **(review, design) Compute the compounded run rate.** Never read a per-step pass
  rate as the run bar; estimate 0.95^N for an N-step path and gate on the run-level
  number, raising the per-step bar or shortening the path to hit target.
- **(do, review) Assert tool-selection order, not just tool presence.** A correct
  set of tools in the wrong order is a path failure; encode the expected ordering
  (or the partial order that must hold) as a deterministic check.
- **(do, design) Bound loops and retries.** Assert a ceiling on retry and
  cycle counts; a run that succeeds only after exceeding it fails the trajectory
  test, surfacing the cost/reliability defect a final-state check hides.
- **(do, review) Assert every required hand-off.** Check each planner→executor,
  agent→sub-agent, or agent→human hand-off is present and correctly ordered; a
  dropped or reordered hand-off is a run failure even when both sides pass alone.
- **(review, design) Prefer a deterministic path check to a judge.** Order, counts,
  and hand-off presence are checkable — use code, not a judge; reserve a calibrated
  judge for node-content quality only.
- **(do, review) Trace-link every failure.** A failed run must point at the
  offending span so triage starts at the break; an untraceable failure can't be
  promoted into a sharper assertion.
- **(design) Repeat non-deterministic trajectories.** Run a stochastic path
  multiple times and assert on the distribution of loop counts and hand-off
  success, so an intermittent loop isn't masked by one lucky execution.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are spans reassembled into an ordered trajectory before scoring? | Trajectory blindness — run fails while spans pass | Stitch the path; assert on order, hand-offs, loops |
| Is the gate the compounded run rate, not the per-step rate? | March of nines — suite reports an unreachable number | Compute 0.95^N; gate on the run-level rate |
| Does each test map to a named failure mode? | Failures can't be localized | Build a failure-mode ontology; one assertion per mode |
| Are tool-selection order and hand-offs asserted? | Step-soup — right tools, wrong order passes | Encode the expected (partial) order and each hand-off |
| Are loop/retry counts bounded by an assertion? | Loop blindness — 30-retry success passes | Assert a ceiling on cycle and retry counts |
| Does a failed run point at the offending span? | Untraceable failure — can't sharpen the eval | Trace-link the failure to its span |

## Cross-references

- `eval-design` — single-call and schema-metric evals that a trajectory node may
  reuse for per-node content; this surface composes them into a path test.
- `judge-calibration` — calibrate any judge before it grades node content; a path
  assertion should be deterministic wherever the property is checkable.
- `benchmark-design` — replayable run-level suites that gate model swaps/releases
  reuse these trajectory assertions per task slice.
- `activation-evals` — activation routing is itself a short trajectory (trigger →
  route → skill); the same path-grading discipline applies.
- → `agent-ops` for the operating hand-off: this surface *designs* the trajectory
  eval; `agent-ops` runs it against the live trace stream and watches drift.
- → `harden-repo-for-coding-agents` for scaffolding the CI gate that enforces a
  run-level rollback threshold.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` — REVIEW
  scales; finding IDs `AGENT-TEST-TRAJ-NNN`.
- `references/intents/{do,review,design}.csv` row `trajectory-tests` — the entry
  points.
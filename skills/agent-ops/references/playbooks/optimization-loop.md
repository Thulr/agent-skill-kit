# Optimization Loop Playbook

## Scope

The trace-and-eval flywheel that turns a signal into a change: scoring whether an
integration is *ready* to close that loop, converting a real trace into a non-trivial
eval candidate, and deciding what turns a one-off score into a repeated operating
cycle. This is loop mechanics and cadence as the agent *operates* the system — not the
design of the judge, rubric, or metric that grades a step, which hands off to
`agent-test`.

- **In:** the Loop Readiness Matrix (six fields + observation anchor), the
  instrumentation smoke test, trace-to-eval conversion, the Next Operating Loop, and
  the Score-Without-Inspection anti-pattern.
- **Out:** judge/rubric/metric *design* and held-out benchmark *construction* (see
  `agent-test`); SDK-side span emission and redaction (see `agent-dx`); the autonomy
  controller's governance rails (see the `autonomy-governance` sibling playbook);
  repo-file scaffolding (see `harden-repo-for-coding-agents`).
- **Intents this surface answers:** do, review, design.

## Grounding

- A score derived from file or field presence is not a readiness score. Six matrix
  fields can all be filled while nothing has been emitted; readiness requires an
  *observed* emission from a real session, not a completed form.
- Telemetry that captures command names and durations is not loop telemetry. A
  usable signal carries prompt + completion + tool I/O; conventions like OpenTelemetry
  GenAI (`gen_ai.*`) and OpenInference name those attributes, but the LLM client must
  be wrapped for them to appear.
- A judge is only trustworthy once calibrated against a human-labeled set — an
  uncalibrated interpreter manufactures confident scores. Calibration design is
  `agent-test`'s; *requiring* a calibrated interpreter before scoring is this loop's.
- Autonomy begins only when a controller *repeats* the loop on real candidates. Fed
  skeleton candidates, a controller produces skeleton diffs.

## Good signals

- Every readiness row names a **Last observed** anchor — a file, span, or timestamp —
  and 6/6 rows trace to an emission seen this cycle, not to a populated field.
- One real example per signal type (traces, tests, user feedback, eval labels,
  cost/latency) is opened and inspected before any row is scored.
- A captured LLM span carries prompt + completion + tool I/O, confirming the client is
  wrapped rather than only command-level attributes (`cmd.name`, `duration_ms`).
- The trace-to-eval command, run against a real session, yields a non-trivial
  candidate (an actual prompt/completion/tool-I/O case), not skeleton metadata.
- The interpreter for each row is named and, where it is an LLM judge, calibrated
  against a human-labeled set before its scores are trusted.
- Each row has an owner and a stop/rollback condition (retry cap, held-out set,
  budget, rollback threshold), so a score can become a governed cycle.
- A held-out eval set is wired and demonstrably disjoint from the training set, with a
  non-zero fixture-count margin over the minimum, before any change is staged.
- Scores decompose by failure mode and slice; no single aggregate pass-rate stands in
  as the release gate.

## Common failures

- **Score Without Inspection.** Readiness scored from file/field presence instead of
  observed emission, so a fully-formed matrix certifies a loop that has never run.
- **Telemetry Theater.** Spans capture command names and durations but not
  prompts/completions/tool I/O; the LLM client was never wrapped, so no row can clear
  3/6 on real signal.
- A no-recent-observation row scored above 3/6 on the strength of historical setup;
  staleness is read as readiness.
- The trace-to-eval step accepts skeleton metadata as a candidate, so the loop runs on
  fixtures that never reflected a real session.
- An uncalibrated judge's scores are trusted, manufacturing a green signal from a
  noisy interpreter.
- The held-out set overlaps the training set (or is below the fixture-count floor), so
  "passed the gate" measures memorization, not held-out behavior.
- A score is produced once and never wired to a cadence, owner, or stop condition — a
  reading, not an operating loop.

## Heuristics

- **(review) Inspect one real example per signal before scoring any row.** Open a
  trace, a test result, a feedback item, an eval label, a cost/latency record — and
  read the contents. Presence of the source is not the signal; the emitted payload is.
- **(review) Run the instrumentation smoke test first.** Confirm a captured LLM span
  carries prompt + completion + tool I/O. If the client is not wrapped, cap every
  dependent row at 3/6 — there is no real signal yet to score higher.
- **(review, do) Cap no-recent-observation rows at 3/6.** A row with no emission this
  cycle is unproven regardless of how complete its fields look. 6/6 requires an
  observed emission, not a filled form.
- **(do) Convert a trace to an eval candidate and demand it be non-trivial.** Run the
  trace-to-eval command against a real session; the output must be an actual
  prompt/completion/tool-I/O case. Reject skeleton metadata before it seeds a loop.
- **(do, design) Require a calibrated interpreter before trusting a score.** Name the
  interpreter for each row; if it is an LLM judge, it must be calibrated against a
  human-labeled set. Hand the *design* of that judge/rubric to `agent-test`.
- **(design) Make each row's six fields name a real change surface and stop
  condition.** Signal, interpreter, change surface (prompt/rules, dataset, tool schema,
  harness, weights), cadence, stop/rollback, owner — so a score can graduate to a
  repeated cycle rather than expire as a one-off reading.
- **(design, do) Gate the Next Operating Loop on disjoint held-out fixtures.** Before
  staging any change, confirm the held-out set is disjoint from training and exceeds
  the fixture floor with a non-zero margin. Autonomy starts only when a controller
  repeats the loop on real candidates against this gate.
- **(review, design) Never collapse the gate to one aggregate pass-rate.** Decompose
  scores by failure mode and slice so a regression is attributable; route metric and
  judge design to `agent-test`.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Did you open one real example per signal type before scoring? | Score reflects field presence, not emission | Run the instrumentation smoke; inspect a real example per signal |
| Does a captured LLM span carry prompt + completion + tool I/O? | The client isn't wrapped; no real signal | Cap dependent rows at 3/6; wrap the LLM client |
| Does each 6/6 row name a Last-observed anchor seen this cycle? | Staleness scored as readiness | Cap no-recent-observation rows at 3/6 |
| Does trace-to-eval produce a non-trivial candidate? | The loop runs on skeleton fixtures | Re-run against a real session; reject metadata-only output |
| Is the held-out set disjoint from training, above the fixture floor? | The gate measures memorization | Rebuild a disjoint held-out set before staging changes |
| Does every score have a cadence, owner, and stop/rollback? | A reading, not a loop | Assign the Next Operating Loop's owner, cadence, and rollback rule |

## Cross-references

- `autonomous-controller.md` — the controller that repeats this loop and the rails it
  must respect once a row reaches 6/6.
- `maturity-and-governance.md` — where this integration sits on the AI Optimization
  Staircase (L1–L4) and which gate the loop must clear.
- → `agent-test` (sibling SKILL) — designing the judge, rubric, metric, and held-out
  benchmark that this loop *consumes*; this playbook stops at requiring a calibrated
  interpreter, not designing one.
- → `agent-dx` (sibling SKILL) — emitting the per-step spans, content-capture toggle,
  and boundary redaction this loop reads.
- → `harden-repo-for-coding-agents` (sibling SKILL) — scaffolding the repo files and
  gates, distinct from operating the loop.
- finding IDs `AGENT-OPS-LOOP-NNN`.
- `references/intents/{do,review,design}.csv` row `optimization-loop` — the entry points.

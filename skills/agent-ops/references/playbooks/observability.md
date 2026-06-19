# Observability Playbook

## Scope

Operating the telemetry an agent system already emits: confirming spans are
substantive, reassembling them into trajectories, grading the path rather than
the step, and turning the trace stream into evals, fixes, and rollback rules.
This is the operator's side of the mirror — the SDK author *instruments* (see
`agent-dx` `sdk-telemetry`); here you *consume* what they emit and decide
whether the loop can be trusted to run.

- **In:** instrumentation smoke checks, trajectory reassembly and path grading,
  promoting traces into evals/fixes/rollback rules, monitoring quality/latency/
  cost drift, detecting a degraded-but-200 dependency from the metrics stream.
- **Out:** designing the spans and capture toggles (`agent-dx` `sdk-telemetry`);
  designing evals/judges/benchmarks (`agent-test`); writing agent-native docs
  (`agent-docs`); scaffolding repo gates and hooks
  (`harden-repo-for-coding-agents`).
- **Intents this surface answers:** do, review, design.

## Grounding

- A span that carries only command-level attributes (`cmd.name`, `duration_ms`)
  is telemetry theater: it proves the call ran, not what the model did. Before
  scoring any feedback-loop row, open one real span per signal type and confirm
  it carries prompt + completion + tool I/O — the LLM client must be wrapped, not
  just the command runner. Conventions like OpenTelemetry `gen_ai.*` and
  OpenInference define where that content lives.
- Per-step span content can all pass while the run fails — loops, wrong-tool
  selection, lost hand-offs. Spans must be reassembled into the ordered
  trajectory and the path graded, because a 0.95 per-step bar compounds far
  below production across a multi-step agent (the march of nines).
- Traces that never become evals, fixes, or rollback rules are observability,
  not a feedback loop. A dashboard is an input to the loop, never the loop.
- A 200-OK dependency can be silently degraded (truncated context, stale model,
  fallback route). Health checks miss it; the quality/latency/cost metrics stream
  is where the regression shows.

## Good signals

- A captured LLM span carries prompt, completion, and tool I/O — not just
  `cmd.name` and `duration_ms`; the LLM client itself is wrapped.
- The trace-to-eval path produces a non-trivial candidate from a real session
  (real prompt+completion+tool I/O), not skeleton metadata.
- Spans are routinely reassembled into the full trajectory and graded as a path:
  tool-selection order, hand-offs, and loop/retry counts are visible per run.
- Quality, latency, and cost are tracked as trends with thresholds, so drift is
  alertable before it becomes an incident.
- A degraded-but-200 dependency is caught from the metrics stream (rising
  truncation, falling answer quality, shifted finish-reason mix), not just from
  uptime checks.
- Per-failure-mode scoring exists, tagged guardrail vs north-star, so a slice
  regression is legible rather than hidden in an aggregate pass-rate.
- Every readiness row names a *Last observed* anchor (file/span/timestamp); rows
  scored from field presence rather than observed emission are flagged.
- Each surfaced regression has a named owner and a defined rollback threshold.

## Common failures

- **Telemetry Theater.** Spans capture command names and durations but not
  prompts/completions/tool I/O; the run "looks instrumented" but nothing about
  the model's behavior is recoverable. Wrap the LLM client itself.
- **Trajectory Blindness.** Grading span content alone — every span succeeds
  while the run fails via loops, wrong-tool, or a lost hand-off. The path is
  never reassembled and graded.
- **The march of nines.** A 0.95 per-step bar is treated as the run bar; across a
  multi-step agent it compounds to a production pass rate far below target.
- **Dashboard Theater.** Rich dashboards exist but no trace ever becomes an eval,
  a fix, or a rollback rule — observability mistaken for a feedback loop.
- **God Gate.** A single aggregate pass-rate gates release, hiding which slice
  broke and conflating a guardrail regression (block ship) with a north-star dip
  (report only).
- **Degraded-but-200 blindness.** Uptime is green while a dependency silently
  truncates context or serves a fallback model; the quality/cost metrics that
  would catch it are not monitored.
- **Score Without Inspection.** Readiness scored from file/field presence instead
  of observed emission — a row marked 6/6 with no recent captured span.
- **Compaction without signal preservation.** Traces are truncated during storage or
  rollup, dropping the prompt/completion/tool I/O that made the run reconstructible — the
  span exists but no longer reassembles.

## Heuristics

- **(do, review) Smoke the instrumentation before scoring anything.** Open one
  real span per signal type and confirm it carries prompt + completion + tool
  I/O. If the LLM client isn't wrapped, cap every dependent readiness row at
  ≤3/6 — do not score on field presence.
- **(review, design) Reassemble the trajectory.** Stitch spans into the ordered
  path and grade tool-selection, hand-offs, and loop/retry counts — not just
  per-span content. A run can fail with every span green.
- **(review, design) Refuse the march of nines.** Don't read a per-step pass rate
  as the run bar; compute the compounded multi-step rate and gate on *that*.
- **(do, review) Turn traces into evals, fixes, or rollback rules.** If a trace
  doesn't produce a candidate eval row, a fix, or a rollback threshold, it's a
  dashboard, not a loop. Run the trace-to-eval command and confirm a non-trivial
  candidate, not skeleton metadata.
- **(review, design) Decompose the gate by failure mode.** Score per slice, tag
  each guardrail vs north-star; block ship on a guardrail regression, report-only
  on a north-star dip. Never gate on one aggregate number.
- **(do, review) Watch the metrics stream for degraded-but-200.** Trend quality,
  latency, and cost with thresholds; treat a truncation spike, quality drop, or
  finish-reason shift as a dependency regression even while uptime is green.
- **(review) Score on observed emission, not file presence.** A readiness row is
  6/6 only with a recent *Last observed* anchor; absent that, cap it at 3/6.
- **(design) Give every signal an owner and a rollback threshold.** An alert with
  no owner and no defined revert action is noise that decays into ignored noise.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does a real span carry prompt + completion + tool I/O? | Telemetry theater; can't reconstruct behavior | Wrap the LLM client; cap dependent rows ≤3/6 |
| Are spans reassembled into a graded trajectory? | Trajectory blindness — run fails, spans pass | Stitch the path; grade tool-order, hand-offs, loops |
| Do traces become evals, fixes, or rollback rules? | Dashboard theater, not a loop | Run trace-to-eval; confirm a non-trivial candidate |
| Is the release gate decomposed by failure mode? | God gate hides which slice broke | Score per slice; tag guardrail vs north-star |
| Is a degraded-but-200 dependency catchable from metrics? | Silent quality/cost regression ships | Trend quality/latency/cost with thresholds |
| Is each readiness row scored on observed emission? | Score-without-inspection inflates readiness | Require a *Last observed* anchor or cap at 3/6 |

## Cross-references

- `optimization-loop.md` — the six-field matrix this surface feeds with observed
  *Last observed* anchors.
- `autonomous-controller.md` — the controller that repeats the loop only after a
  6/6 row backed by real captured spans.
- → `agent-dx` (`sdk-telemetry`) for the *instrumenting* side: spans, capture
  toggles, boundary redaction — this playbook *operates* what it emits.
- → `agent-test` for designing the evals and judges that traces are promoted
  into; a judge is trustworthy only once calibrated against a human-labeled set.
- → `harden-repo-for-coding-agents` for scaffolding the repo gates that enforce
  rollback thresholds in CI.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` —
  REVIEW scales; finding IDs `AGENT-OPS-OBS-NNN`.
- `references/intents/{do,review,design}.csv` row `observability` — the entry
  points.

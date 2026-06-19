# Benchmark Design Playbook

## Scope

The design of a held-out benchmark that gates a model swap or a release: a
replayable task suite, scored against a recorded baseline with an explicit
rollback threshold, sliced so a guardrail regression and a north-star dip never
hide inside one number. This is L4 System Benchmarking from the staircase — the
gate a capability change must clear before it ships, distinct from the
per-change checks at L1–L3.

- **In:** held-out fixture discipline (disjointness from training/optimization,
  a non-zero count margin over the minimum), the replayable task suite, baseline
  capture, the rollback threshold, per-slice guardrail-vs-north-star scoring, and
  Goodhart/metric-gaming resistance.
- **Out:** running the suite on a schedule and watching drift (that hand-off is
  agent-ops); judge calibration (see judge-calibration); run-level path grading
  (see trajectory-tests); per-change eval scaffolding at L1–L3 (see eval-design).
- **Intents this surface answers:** do, review, design.

## Grounding

- **A benchmark is a gate, not a dashboard.** It exists to make one decision —
  ship this model/prompt swap or roll back — so it must carry a recorded
  baseline and a threshold that fires the rollback, not just a number that goes
  up and to the right.
- **Held-out means disjoint, with margin.** Fixtures used to gate a change must
  not overlap the set the change was trained, tuned, or prompt-optimized on; the
  actual fixture count must exceed the stated minimum by a non-zero margin so the
  suite is not one unlucky example from being underpowered.
- **One aggregate pass-rate is a God Gate.** A single number conflates a
  guardrail regression (safety, format, refusal, cost — block ship) with a
  north-star/capability dip (report only), and hides which slice moved. Score
  per slice, with each slice tagged guardrail or north-star.
- **Optimize the behavior, not the benchmark.** Once a metric becomes the target
  it stops measuring (Goodhart); a benchmark you tune against is no longer
  held-out and silently rejoins the training set.

## Good signals

- The fixture set is provably disjoint from training/optimization inputs, and
  the disjointness check is itself a test in the suite, not a one-time promise.
- The fixture count exceeds the documented minimum with a stated non-zero margin,
  and the margin is recorded next to the count.
- The suite is replayable: same fixtures, same harness, same scoring produce the
  same verdict on re-run, so two model versions are compared on identical inputs.
- A baseline is captured from the incumbent model/prompt and stored with the
  suite; every candidate is scored against that baseline, not against an abstract
  bar.
- A rollback threshold is explicit per slice (e.g. \"guardrail slice may not drop
  below baseline; north-star slice dip is reported, not blocking\") and a breach
  produces a block-ship verdict.
- Slices are tagged guardrail vs north-star, so the gate can block on a guardrail
  regression while merely reporting a capability dip.
- Fixtures are real trace-derived candidates (prompt + completion + tool I/O),
  not skeleton metadata, so each fixture actually exercises the behavior.
- The benchmark hands off cleanly to agent-ops: the suite, baseline, and
  thresholds are recorded artifacts that the operating loop can replay on a
  schedule without re-deriving them.

## Common failures

- **God Gate:** one aggregate pass-rate decides ship/rollback; nobody can tell
  which slice broke or whether a guardrail regressed.
- **Leaked held-out set:** fixtures overlap the optimization set, so the
  benchmark certifies a model against examples it was tuned on and reads as a pass
  that production won't reproduce.
- **Underpowered margin:** the fixture count sits at or below the minimum, so a
  single flaky example flips the verdict.
- **Baseline-free threshold:** a fixed bar (\"90% pass\") with no incumbent
  baseline, so a real regression below the prior model still clears the bar.
- **Metric-gaming / Goodhart:** the team optimizes the model to the benchmark's
  scoring quirks rather than the underlying behavior; score climbs, behavior
  doesn't.
- **Skeleton candidates:** fixtures are metadata stubs with no real prompt,
  completion, or tool I/O, so the benchmark passes while testing nothing.
- **No rollback wired:** a breach is logged but ship proceeds, because the
  threshold has no enforcement path back to the deploy decision.
- **Guardrail/north-star conflation:** a safety or format regression averages
  against a capability gain and disappears.

## Heuristics

- **(design, review) Name the gate before the number.** State the one decision
  the benchmark makes (ship this swap or roll back) and what fires the rollback;
  if it has no rollback path it is a dashboard, route it to agent-ops, not a gate.
- **(design) Prove disjointness, then prove margin.** Make the held-out set's
  disjointness from the optimization set a check in the suite, and record the
  fixture count with its non-zero margin over the minimum beside it.
- **(review) Hunt the God Gate first.** If one aggregate pass-rate decides
  ship/rollback, that is the top finding — decompose it into slices before
  trusting any verdict.
- **(design, review) Tag every slice guardrail or north-star.** Guardrail
  regressions block ship; north-star/capability dips report only. A gate that
  averages them together can ship a safety regression.
- **(do, review) Score against a captured baseline.** Compare each candidate to
  the recorded incumbent, never to an abstract bar; a fixed bar with no baseline
  passes real regressions.
- **(design) Make replay deterministic.** Pin fixtures, harness, and scoring so
  the same candidate yields the same verdict twice — a non-replayable suite
  cannot compare two model versions honestly.
- **(review) Test the behavior, audit the candidate.** Spot-check that fixtures
  carry real prompt + completion + tool I/O; a benchmark of skeleton candidates
  is a green light that tests nothing.
- **(do, design) Resist Goodhart by rotating and quarantining.** Keep a fixture
  slice the team never tunes against, and retire fixtures the moment they're used
  to optimize; a benchmark you've trained on is no longer held-out.
- **(design) Hand the gate to agent-ops as artifacts.** Record suite, baseline,
  thresholds, and slice tags so the operating loop replays them on swaps and
  release without re-deriving — design here, run there.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does one decision (ship/rollback) and a rollback threshold sit on the benchmark? | It's a dashboard, not a gate | Define the gate decision + rollback threshold, or route to agent-ops |
| Is the fixture set provably disjoint from the optimization set? | Leaked held-out set | Add a disjointness check to the suite; rebuild fixtures from untuned traces |
| Does fixture count exceed the minimum with a non-zero margin? | Underpowered, one example flips it | Record count + margin; add fixtures until margin is real |
| Is each slice tagged guardrail vs north-star? | God Gate conflation | Split slices; block on guardrail, report-only on north-star |
| Is each candidate scored against a captured baseline? | Baseline-free bar passes regressions | Capture incumbent baseline; threshold relative to it |
| Do fixtures carry real prompt + completion + tool I/O? | Skeleton candidates test nothing | Rebuild from non-trivial trace candidates |

## Cross-references

- eval-design — the L1–L3 per-change evals a benchmark sits above; a benchmark
  is the L4 release gate, not a substitute for them.
- judge-calibration — when a benchmark slice is scored by an LLM judge, that judge
  must be calibrated there before its verdict gates a release.
- trajectory-tests — run-level path grading for multi-step agents; benchmark
  slices over agent tasks reuse trajectory scoring, not per-span scoring.
- activation-evals — the held-out and slice discipline here applies to skill/agent
  activation benchmarks too.
- → `agent-ops` — the hand-off: this surface designs the benchmark; agent-ops
  runs it on model swaps and releases and watches for drift.
- Finding IDs `AGENT-TEST-BENCH-NNN`.
- `references/intents/{do,review,design}.csv` row `benchmark-design` — the entry points.
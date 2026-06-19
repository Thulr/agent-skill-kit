# Autonomous Controller Playbook

## Scope

The autonomous-improvement controller lifecycle: the loop that an operator lets
*run itself* — read a signal, call an optimizer, apply a candidate change in a
branch, gate it, and revert or stage. Autonomy starts only once a controller
**repeats** that loop unattended; before then it is a human-driven flywheel, not
a controller. This surface covers the preconditions that license autonomy, the
circuit-breakers that bound it, and the apply/gate/revert discipline that keeps
a bad cycle from shipping.

- **In:** autonomy preconditions (non-trivial candidate, held-out eval on
  disjoint fixtures, fixture-count margin, real allowlist paths), cost/iteration
  circuit-breakers, one-diff-per-cycle, apply-in-branch, revert-on-failed-gate,
  stage-only-green, compaction and privacy policy on what the loop writes.
- **Out:** designing the eval suite, rubric, or LLM judge the controller calls
  (see `agent-test`); building the SDK/telemetry the loop reads (see
  `agent-dx`); scaffolding the repo files and gates an agent works inside (see
  `harden-repo-for-coding-agents`); writing agent-native docs (see
  `agent-docs`).
- **Intents this surface answers:** do, review, design.

## Grounding

- A controller is only as good as what it is fed: a candidate assembled from
  skeleton metadata (command names, durations) rather than a real session's
  prompt + completion + tool I/O produces a skeleton diff — a plausible edit
  with no grounding in observed behavior.
- Held-out evaluation is the load-bearing gate. If the fixtures the controller
  validates against overlap the set its optimizer trained on, every cycle scores
  green by memorization and the loop drifts unchecked.
- Self-improvement that writes without a gate is an availability and safety
  incident waiting to happen; standard release-engineering practice — branch,
  validate, promote-or-revert — applies unchanged to an automated writer.
- Multi-step autonomy compounds error: a 0.95 per-cycle pass bar across many
  cycles lands far below production reliability (the march of nines), so caps
  and rollback thresholds matter more than any single green run.

## Good signals

- Trace-to-eval produces a non-trivial candidate from a real session (prompt +
  completion + tool I/O present), not skeleton metadata.
- `HELD_OUT_EVAL_CMD` points at fixtures provably disjoint from the optimizer's
  training set, and actual fixture count clears the minimum with a non-zero
  margin.
- Every allowlisted change path exists on disk and is non-trivial; the
  controller validates each before writing.
- The controller applies exactly one diff per cycle, in a branch, never on the
  working trunk.
- A failed gate triggers an automatic revert; only green changes are staged for
  human review.
- Cost and iteration circuit-breakers are configured and have actually tripped
  at least once in a dry run, proving they fire.
- A compaction policy bounds what the loop persists, and a privacy filter scrubs
  captured content before it is written into rules/datasets/prompts.
- The loop has a named owner and a rollback threshold, not just a start command.

## Common failures

- **Ungated Self-Improvement.** The controller writes prompts/rules/datasets
  with no held-out eval, no diff review, no compaction policy, and no privacy
  filter — drift, leakage, and unbounded growth follow.
- **Skeleton-candidate autonomy.** The loop is switched on while trace-to-eval
  still returns command-level metadata; it generates confident, empty diffs.
- **Overlapping fixtures.** The held-out set shares rows with training, so the
  gate rubber-stamps memorized behavior and never catches regression.
- **Margin-of-zero fixtures.** Fixture count sits exactly at the minimum, so one
  flaky case flips the gate and the loop's verdict is noise.
- **Phantom allowlist paths.** An allowlisted target does not exist or is a
  stub; the controller writes into a placeholder and stages nothing real.
- **No circuit-breaker.** Cost and iteration are unbounded; a runaway optimizer
  burns budget or loops forever before anyone notices.
- **Multi-diff cycles.** Several changes land per cycle, so a failed gate cannot
  attribute the regression and revert cleanly.
- **Apply-on-trunk.** Changes go straight to the working branch with no
  revert-on-failure, so a bad cycle is already shipped by the time it is graded.

## Heuristics

- **(review, design) Gate autonomy on a real candidate, not a present field.**
  Before flipping the controller on, confirm trace-to-eval emits prompt +
  completion + tool I/O from an actual session; a candidate built from
  `cmd.name`/`duration_ms` is skeleton input and yields a skeleton diff.
- **(review) Prove the held-out set is disjoint.** Diff the eval fixtures
  against the optimizer's training rows; any overlap means the gate measures
  memorization. Treat shared rows as a hard stop on autonomy.
- **(do, review) Check the fixture-count margin, not just non-emptiness.**
  Require actual count to exceed the minimum with room to spare; a gate riding
  exactly at threshold is one flaky case from flipping.
- **(do, design) Validate every allowlist path before writing.** Each
  allowlisted target must exist and be non-trivial; a controller writing into a
  phantom or stub path stages nothing useful and hides the failure.
- **(design) Wire cost and iteration circuit-breakers, and test that they
  fire.** Bound spend and loop count up front; a dry run should trip each
  breaker at least once so you know the rail is real, not declared.
- **(do, design) One diff per cycle, in a branch.** Apply a single change per
  cycle on a branch so a failed gate attributes cleanly and reverts cleanly;
  never write to the working trunk.
- **(do) Revert on failed gate; stage only green.** A red gate auto-reverts the
  cycle's branch; only changes that pass the held-out gate are staged for a
  human diff review.
- **(design) Bound what the loop persists.** Attach a compaction policy and a
  privacy filter to every write path so the controller cannot grow rules
  unbounded or leak captured content into prompts, datasets, or instruction
  files.
- **(review) Budget for the march of nines.** A per-cycle pass bar compounds
  downward across cycles; size the rollback threshold and cap against the
  end-to-end target, not the single-cycle score.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does trace-to-eval emit prompt + completion + tool I/O? | Candidates are skeleton metadata | Hold autonomy; fix LLM-span capture first |
| Is the held-out set disjoint from training? | Gate scores memorization | Rebuild fixtures from disjoint sessions |
| Does fixture count clear the minimum with margin? | One flaky case flips the gate | Add fixtures until the margin is non-zero |
| Does every allowlist path exist and carry real content? | Controller writes into stubs | Remove phantom paths from the allowlist |
| Have the cost/iteration breakers actually tripped in a dry run? | Runaway loop goes unbounded | Configure and test-fire each breaker |
| Is it one diff per cycle, in a branch, with auto-revert on red? | Bad cycles ship unattributed | Enforce single-diff branch apply + revert-on-fail |
| Is there a compaction + privacy policy on every write path? | Drift, bloat, and leakage accrue | Add compaction and a redaction filter before writes |

## Cross-references

- `optimization-loop.md` — the 6/6 readiness gate (observed emission, not field
  completion) a row must clear before its change surface is controller-eligible.
- `observability.md` — the LLM-span check that decides whether
  trace-to-eval can produce a non-trivial candidate at all.
- → `agent-test` for designing the eval suite, rubric, and calibrated LLM judge
  this controller calls as its gate.
- → `agent-dx` for the SDK and telemetry that emit the prompt + completion +
  tool I/O the controller consumes.
- → `harden-repo-for-coding-agents` for the repo gates/hooks/branch protection
  the controller's staged diffs flow through.
- finding IDs `AGENT-OPS-CTL-NNN`.
- `references/intents/{do,review,design}.csv` row `autonomous-controller` — the entry points.

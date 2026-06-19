# Glossary

Terms used across the agent-ops playbooks. Definitions are operational, not exhaustive.

- **Agent-ops** — operating a running agent system: observing it, closing its improvement loop,
  governing its autonomy, and keeping it reliable and bounded in cost. The agent-actor analog
  of human perf/observability ops. Also the **family front-door** — it routes work out to the
  sibling agent skills.
- **AI Optimization Staircase** — a maturity ladder for the change surface a loop targets:
  L1 system-prompt learning, L2 subroutine compilation, L3 sandbox + repair harness, L4 system
  benchmarking; each tier has a gate-before-persistence.
- **Loop Readiness Matrix** — six fields scored per integration — signal, interpreter, change
  surface, cadence, stop/rollback, owner — plus a *Last observed* anchor. 6/6 requires observed
  emission, not field completion.
- **Observed emission** — a recent, real example of a signal actually landing somewhere readable
  (a span, a trace, a run), as opposed to a config field that says it *would*.
- **Instrumentation smoke** — opening one real example of each signal type before scoring, to
  confirm spans carry prompt + completion + tool I/O, not just `cmd.name`/`duration`.
- **Span vs trajectory** — a span records one step; a trajectory is the reassembled ordered path
  of spans for a run. Grade the trajectory, because a run can fail with every span green.
- **Trace-to-eval** — converting a captured trace into a candidate eval row; it must yield a
  non-trivial candidate (real prompt+completion+tool I/O), not skeleton metadata.
- **Autonomous controller** — code that repeats the loop: calls an optimizer, validates
  allowlisted paths, applies in a branch, reverts on failed gates, stages only green changes.
  Autonomy starts only when a controller repeats the loop.
- **Circuit-breaker** — a cost or iteration cap that halts an autonomous loop before runaway
  spend or churn.
- **Held-out eval** — evaluation on fixtures disjoint from what the loop trained/optimized on;
  the precondition for trusting a controller's change.
- **One-diff-per-cycle** — a controller applies a single reviewable change per cycle, in a
  branch, so each improvement is attributable and revertible.
- **March of nines** — per-step reliability compounds: a 0.95 per-step bar falls far below
  production across a multi-step agent; gate on the compounded run rate.
- **Guardrail vs north-star** — a guardrail regression (safety/correctness floor) blocks ship; a
  north-star/capability dip is reported only. A release gate must tell them apart.
- **Degraded-but-200** — a dependency returning success while silently degraded (truncated
  context, fallback model, stale data); caught from the quality/latency/cost metrics stream, not
  uptime checks.
- **Provenance** — the recorded origin of an agent-authored change (which loop/controller/model
  produced it), so governance can see what moved through the pipeline.
- **Front-door / routing out** — agent-ops' role as the family hub: it *operates*, and hands
  off building to `agent-dx` (SDK/tool), `agent-docs` (agent-native docs), `agent-test` (eval
  design), `harden-repo-for-coding-agents` (repo files), and `rules-from-coding-agent-failures`
  (promote failures).
- **Telemetry theater** — spans capturing command names and durations but not model content;
  looks instrumented, fuels nothing.
- **Dashboard theater** — traces and dashboards that never become evals, fixes, or rollback
  rules; observability mistaken for a feedback loop.
- **God gate** — a single aggregate pass-rate as the release gate; hides which slice broke and
  conflates guardrail with north-star.
- **Trajectory blindness** — grading span content alone and never reassembling the path.
- **Ungated self-improvement** — a controller writing changes without held-out evals, diff
  review, compaction policy, or privacy filtering.
- **Score without inspection** — scoring readiness from file/field presence instead of observed
  emission.
- **God prompt** — stuffing permissions, costs, and side-effect control into the prompt instead
  of an L3 harness.

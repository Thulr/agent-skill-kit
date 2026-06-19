# Severity rubric (0–4)

Apply to every finding in a REVIEW, every risk in a DESIGN, and every step in a rollout
runbook. Agent-ops severity weighs operational blast: an agent system that cannot be observed,
cannot close its loop, or improves itself ungated harms users at machine speed and scale.

| Level | Label | Meaning |
|------:|-------|---------|
| 4 | **Critical** | An autonomous controller writes changes with no held-out eval, diff review, or rollback (Ungated Self-Improvement); an autonomy loop with no cost/iteration circuit-breaker; the sole production signal carries no prompt/completion/tool I/O so nothing can be reconstructed. Block the loop. |
| 3 | **High** | Release gate is a single aggregate pass-rate hiding which slice broke (God Gate); the trajectory is never reassembled so path failures pass (Trajectory Blindness); spans capture only `cmd.name`/`duration` (Telemetry Theater) for a production agent. Large but tractable fix. |
| 2 | **Medium** | Traces exist but never become evals/fixes/rollback rules (Dashboard Theater); loop readiness scored from field presence not observed emission; a 0.95 per-step bar treated as production-ready for a multi-step agent. Fix this cycle. |
| 1 | **Low** | A missing owner on one matrix row, an un-tuned alert threshold, a dashboard that duplicates another. Queue for cleanup if it accumulates. |
| 0 | **Note** | An observation worth recording, not a defect — e.g. "this loop is manual-cadence by deliberate choice." |

## How to pick a level

1. **Operational blast.** Whole system / every run (4), one loop or release gate (3), one
   signal or surface (2), one row/threshold (1), nothing a user feels (0)?
2. **Reversibility.** An ungated autonomous write or an unbounded spend compounds the longer it
   runs; a missing dashboard does not.
3. **Observed vs asserted.** A gap proven by an actual span/trace/run outranks one inferred
   from a config file; score readiness from observed emission, never field presence.

## Calibration anchors

- "An autonomous controller persists changes with no held-out eval / diff review / rollback" → **4**.
- "An autonomy loop runs with no cost or iteration circuit-breaker" → **4**.
- "The only production signal is a span with no prompt/completion/tool I/O" → **4** (nothing is reconstructable).
- "Release gate is one aggregate pass-rate; a guardrail regression ships behind an unchanged average" → **3**.
- "Spans grade content but the trajectory is never reassembled; path failures pass" → **3**.
- "Traces exist but never feed an eval, fix, or rollback rule" → **2** (Dashboard Theater).
- "Loop readiness scored from field presence, not a recent observed example" → **2**.
- "A 0.95 per-step bar is treated as production-ready for a 10-step agent" → **2** (march of nines).
- "A maturity tier is claimed without that tier's gate-before-persistence" → **2**.

## Cross-surface comparison

Scores and severities are comparable only within one REVIEW run, using the same persona and
project tier. Do not benchmark across teams or across time without recalibrating against these
anchors.

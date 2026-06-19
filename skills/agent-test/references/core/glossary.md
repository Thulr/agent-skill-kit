# Glossary

Terms used across the agent-test playbooks. Definitions are operational, not exhaustive.

- **Agent-test** — designing the measurement instruments for an agent system or skill: evals,
  LLM-as-judges, trajectory tests, held-out benchmarks, and activation evals. The agent-actor
  analog of human test design. It *designs* the measurement; `agent-ops` *operates* it.
- **Failure-mode ontology** — the named list of *how* a system fails, defined before chasing an
  aggregate score; you cannot improve a number you cannot decompose into failure modes.
- **Eval** — a check that grades an agent's behavior against an expectation; the smallest one
  that gates the change at hand is the right one.
- **Staircase tier** — the change surface an eval targets (L1 system-prompt, L2 subroutine, L3
  sandbox/repair, L4 system benchmark); each names a gate an eval must clear before a change
  persists.
- **LLM-as-judge** — a model grading another model's output. Trustworthy only once calibrated
  and emitting failure explanations.
- **Judge calibration** — measuring a judge against a human-labeled set (precision/recall) plus
  checking position, length, and self-preference bias, before the judge gates anything.
- **Vague Judge** — an uncalibrated judge (no human-labeled comparison, no bias check, no
  explanation) that can silently certify regressions.
- **Failure explanation** — the judge's stated reason a case failed, not just a score; required
  for a judge to be debuggable and trustworthy.
- **Trajectory test** — a test that reassembles spans into the ordered run path and asserts on
  tool-selection order, hand-offs, and loop/retry counts.
- **Trajectory Blindness** — grading per-span content alone; every span passes while the run
  fails (loop, wrong tool, lost hand-off).
- **March of nines** — per-step reliability compounds: a 0.95 per-step bar falls far below
  production across a multi-step agent; design run-level evals, not just per-step.
- **Held-out set** — evaluation fixtures DISJOINT from what was trained or optimized on, with a
  non-zero count margin; the precondition for a benchmark that measures generalization, not
  memorization.
- **Train/test split** — partitioning data so the eval set is never seen during fitting.
- **Baseline + rollback threshold** — the reference score a benchmark compares against and the
  drop that triggers reverting a change.
- **Per-slice scoring** — scoring each failure-mode slice separately, tagged guardrail vs
  north-star, instead of one aggregate.
- **Guardrail vs north-star** — a guardrail regression (safety/correctness floor) blocks ship; a
  north-star/capability dip is reported only.
- **God Gate** — a single aggregate pass-rate as the release gate; hides which slice broke and
  conflates guardrail with north-star.
- **Metric-gaming (Goodhart)** — optimizing the proxy metric instead of the behavior it stands
  for, so the score rises while the behavior does not.
- **Activation eval** — a test of whether an agent or skill *activates and routes correctly* for
  a prompt: positive (should fire), negative (should not), and edge/disambiguation cases.
- **False vs missed activation** — firing when it should not (false) vs not firing when it
  should (missed); distinct failures with distinct fixes.
- **Disambiguation case** — an activation eval that checks routing to the RIGHT skill/tool among
  similar siblings.
- **Eval-on-prompt-change** — re-running the evals (and recalibrating judges) whenever the
  prompt, description, or model changes.
- **Skeleton candidate** — a trace-to-eval output that is metadata only (no real
  prompt/completion/tool I/O); an eval built on it tests nothing.

# Severity rubric (0–4)

Apply to every finding in a REVIEW, every risk in a DESIGN, and every step in a hardening
runbook. Agent-test severity weighs how badly a measurement instrument MISLEADS: an eval that
certifies a regression or a benchmark that scores memorization is worse than no eval, because a
team trusts it.

| Level | Label | Meaning |
|------:|-------|---------|
| 4 | **Critical** | The instrument is invalid and trusted as the gate: held-out fixtures overlap the training/optimization set (the benchmark scores memorization); an uncalibrated judge is the release gate. Block the gate. |
| 3 | **High** | A judge gates persistence with no calibration against a human-labeled set (Vague Judge); a single aggregate pass-rate is the release gate (God Gate); evals grade per-span content and never assert the trajectory (Trajectory Blindness); the eval optimizes a proxy the behavior can game. Large but tractable fix. |
| 2 | **Medium** | A 0.95 per-step bar is the only eval for a multi-step agent (march of nines); activation evals lack negative/disambiguation cases; evals are not re-run on prompt/model change; an eval built on skeleton candidates. Fix this cycle. |
| 1 | **Low** | A judge with no failure explanations where a score suffices today; one missing edge case; an un-decomposed but low-stakes metric. Queue for cleanup if it accumulates. |
| 0 | **Note** | An observation worth recording, not a defect — e.g. "a deterministic check would be cheaper than this judge, but the judge is fine." |

## How to pick a level

1. **Mislead radius.** Does the instrument certify a falsehood the team acts on (4)? Gate a
   release wrongly (3)? Miss a known failure class (2)? Lack polish (1)?
2. **Trust.** A trusted-but-wrong instrument (the gate, the headline metric) rates higher than
   an honest gap the team knows about.
3. **Decomposability.** A metric no one can decompose into failure modes hides regressions; that
   is worse than a smaller but legible metric.

## Calibration anchors

- "Held-out fixtures overlap the training/optimization set; the benchmark scores memorization" → **4**.
- "An uncalibrated LLM judge is the release gate" → **4**.
- "A judge gates persistence with no human-labeled calibration or bias check (Vague Judge)" → **3**.
- "A single aggregate pass-rate is the release gate (God Gate)" → **3**.
- "Evals grade only per-span content; the trajectory is never asserted (Trajectory Blindness)" → **3**.
- "The eval optimizes a proxy metric the behavior can game (Goodhart)" → **3**.
- "A 0.95 per-step bar is the only eval for a 10-step agent (march of nines)" → **2**.
- "Activation evals have no negative or disambiguation cases; false activation is untested" → **2**.
- "Evals are not re-run when the prompt or model changes" → **2**.
- "A judge emits a score but no failure explanation" → **1**.

## Cross-surface comparison

Scores and severities are comparable only within one REVIEW run, using the same persona and
project tier. Do not benchmark across teams or across time without recalibrating against these
anchors.

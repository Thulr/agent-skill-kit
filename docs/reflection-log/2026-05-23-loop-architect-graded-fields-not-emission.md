---
date: 2026-05-23
harness: claude-code
sub-surface: skills
severity: 3
status: open
related: []
---
# loop-architect scored 6/6 from declared fields, not observed emission

## What happened

A user ran `/loop-architect` on the sdlc-harness project. The skill's
check-loop-readiness gate reported "loop readiness passed: 7 integrations at
6/6," and the audit jumped straight to the post-6/6 recommendation (wire the
autonomous improvement controller from
`references/templates/autonomous-improve-loop.mjs`). After wiring, the gate
reported "8 integrations at 6/6."

When the user asked follow-up questions about what the controller would
actually consume, the agent investigated the underlying observability and
found:

- The Loop Readiness Matrix listed "Sauron OTLP spans" as L2/L3 signal, but
  the LLM call sites in `src/llm/agent.ts`, `agent-openai.ts`,
  `anthropic.ts`, `ollama.ts` were not wrapped in `withSauronSpan` — only
  command-level Pi invocations were. Captured span attributes were
  `cmd.name`, `duration_ms`, etc. No prompts, no completions, no tool I/O.
- `intent_cases_min: 3` was set equal to the actual fixture count — zero
  margin. Any failure-case removal would have dropped the gate below
  threshold.
- `HELD_OUT_EVAL_CMD` was intentionally empty — no train/test split for the
  autonomous controller's gates.
- The trace-eval-candidates folder contained one sample file, not a real
  failure corpus.

The 6/6 score was structurally a false positive. The readiness gate
validates that each row in the matrix has six text fields filled in; it
does not verify that the signal named in each row is actually being
emitted. The autonomous controller's recommendation rested on that false
foundation — its first real invocation errored on missing candidates and
would have produced skeleton diffs even if a candidate had been present.

The conversation only surfaced the instrumentation gap after four rounds of
user push-back. Recommendation #1 should have been "wrap LLM client calls
so prompts and completions get captured" — instead it landed as a footnote
("trace candidates are thin") under follow-ups.

## What to do differently

Tighten loop-architect so 6/6 means observed emission, not declared
capability:

1. **SKILL.md Step 1.5 — Instrumentation Smoke** (new step between Audit
   and Diagnostic Report). Before scoring, the auditor must open one real
   example of each signal type and confirm it contains the load-bearing
   content. For LLM signals specifically: confirm prompts + completions +
   tool I/O are captured. Rows that cannot be observed cap at 3/6
   regardless of declared fields.
2. **SKILL.md Step 4 — Controller preconditions.** Before recommending
   `autonomous-improve-loop.mjs`, verify trace-to-eval produces non-trivial
   candidates, `HELD_OUT_EVAL_CMD` is set, fixture count exceeds
   `fixture_min`, and allowlist paths exist and are non-trivial.
3. **Anti-patterns added:** "Telemetry Theater" (spans without
   prompts/completions) and "Score Without Inspection" (field-presence ≠
   working signal). Both name the failure mode so the next audit has the
   vocabulary.
4. **Controller preflight** in
   `references/templates/autonomous-improve-loop.mjs`: refuse to run if the
   candidate is metadata-only or held-out is unset. This is the
   load-bearing change — survives any SKILL.md prose regression because
   the controller itself enforces it.
5. **Activation case P8** covers the failure mode (6/6 with uninstrumented
   LLM calls). The Phase 2 grader's `post-readiness-operating-loop` case
   updated so the right answer is "close the telemetry gap first," not
   "wire the controller."
6. **Static-check gates** in `evals/run-static-checks.sh` pin the new
   SKILL.md concepts so future edits can't silently drop them.

W1 note: this is the first observed instance of the
field-presence-vs-observed-emission scoring gap in this repo's reflection
log. Promoting to skill changes here is justified because (a) the fix
tightens an existing skill's contract rather than scaffolding new
agent-readiness rules from inferred patterns, (b) the failure was
witnessed directly by the maintainer, and (c) the controller preflight is
a forcing function — it fails closed even if the SKILL.md prose drifts.
W1's three-instance floor applies to scaffolding general rules from
ambient failure patterns; it does not apply to fixing a known-broken skill
contract the maintainer has personally observed failing.

## Closed by

<TBD — PR that lands the loop-architect Step 1.5 + preflight + anti-pattern updates>

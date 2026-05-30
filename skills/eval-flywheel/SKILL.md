---
name: eval-flywheel
description: Audit AI integrations, score feedback-loop readiness, map the AI Optimization Staircase, and scaffold eval loops plus post-readiness improvement controllers. Use for AI workspace audits, eval loops, prompt optimizers, trace/eval flywheels, agent harnesses, production experiments, system benchmarks, autonomous improvement loops, or `/eval-flywheel`.
license: MIT
---

# eval-flywheel

Maps AI integration points, scores missing loop mechanics, scaffolds the
smallest useful eval loop. 6/6 means ready to improve; autonomy starts only
when a controller repeats the loop.

## When to Use

- User wants evals, prompt optimization, trace replay, production loops, benchmarks, or `/eval-flywheel`.
- Workspace has hardcoded prompts, raw rules files, unmonitored agent loops, no golden set, or trace data that does not feed improvement.
- Part of the **agent-experience** discipline — the instrument-the-loop arm; `agent-experience` routes here to build eval/optimization loops.

## The AI Optimization Staircase

| Tier | Target | Best for | Gate before persistence |
|---|---|---|---|
| **L1: System-Prompt Learning** | rules/instruction files | Open-ended agents | Judge explanations + held-out eval + reviewed diff |
| **L2: Subroutine Compilation** | Declarative signatures | Parsers, classifiers, routers | Schema metric + train/test split |
| **L3: Sandbox + Repair Harness** | Container, cost, permission rails | Terminal agents, PR builders | Isolation + tests + repair loop |
| **L4: System Benchmarking** | Replayable task suites | Model swaps, release gates | Fixed benchmark + baseline + rollback rule |

## Loop Readiness Matrix

Score each integration on six fields plus an observation anchor:

1. **Signal:** traces, tests, user feedback, eval labels, cost/latency.
2. **Interpreter:** deterministic check, LLM judge, classifier, reviewer.
3. **Change surface:** prompt/rules, dataset, tool schema, harness, weights.
4. **Cadence:** local run, CI, nightly, production sample, release gate.
5. **Stop/rollback:** retry cap, held-out set, budget, rollback threshold.
6. **Owner:** engineer, AI quality lead, ops/CX, release approver.

Each row names **Last observed** (file/span/timestamp). 6/6 requires observed
emission, not field completion. Rows with no recent observation cap at 3/6.

## Workflow

### Step 1 — Workspace Audit

Locate API keys/SDK calls, prompts, rule files, agent loops with side
effects, iteration/cost caps, tests/golden sets/benchmarks, traces
(OTel/Langfuse/Braintrust/Phoenix), and production signals (experiments,
classifiers, feedback, rollback dashboards, live evals).

### Step 1.5 — Instrumentation Smoke

Before scoring, open one real example of each signal type:

- Read the event/trace log — confirm at least one recent entry per signal type.
- Open one captured LLM span/log — confirm **prompt + completion + tool I/O**
  are present, not just command-level attributes (`cmd.name`, `duration_ms`).
  If the LLM client isn't wrapped, score every row dependent on it ≤3/6.
- Run the trace-to-eval command — confirm it produces a non-trivial candidate,
  not skeleton metadata.

### Step 2 — Diagnostic Report

Present:

- **Discovered Integration Points** — where model behavior enters the system.
- **Staircase Placement** — current and recommended next tier.
- **Loop Readiness Matrix** — six fields plus observation anchor per row.
- **Production Gap** — whether the loop needs trace replay, experiment
  metadata, semantic signals, or human review ownership.
- **Next Operating Loop** — what turns the score into a repeated cycle. If
  6/6 and verified, say "ready, not autonomous yet."

Do not scaffold yet. Wait for user approval.

### Step 3 — Scaffolding

Pick an L1-L4 scaffold only after every matrix row has six fields plus an
observation anchor. Traces or dashboards alone aren't a tier; recommend
trace-to-eval conversion first.

Create `ai-ops/` or `.agents/evals/` and adapt:

- **L1** → `references/templates/level-1-prompt-learner.py`
- **L2** → `references/templates/level-2-subroutine-compiler.py`
- **L3** → `references/templates/level-3-sandbox-harness.py`
- **L4** → `references/templates/level-4-system-benchmark.py`

### Step 4 — After 6/6

Do not stop at the score. Before recommending the controller, confirm:

- The trace-to-eval command produces a **non-trivial candidate** containing
  prompt + completion + tool I/O from a real session.
- `HELD_OUT_EVAL_CMD` is set and points at fixtures disjoint from training.
- The actual fixture count exceeds `fixture_min` (non-zero margin).
- Each allowlist path exists and is non-trivial.

If any fails, the next loop is closing that gap. A controller fed skeleton
candidates produces skeleton diffs.

Once preconditions hold, copy `references/templates/autonomous-improve-loop.mjs`.
It calls an optimizer, validates allowlisted paths, applies in a branch with
`--apply`, reverts on failed gates, and stages only green changes.

## Anti-Patterns to Avoid

- **God Prompt:** permissions, costs, and side effects belong in L3 harness code.
- **Vague Judge:** scalar scores without failure explanations cannot patch rules.
- **Ungated Self-Improvement:** never auto-write rules without held-out evals,
  diff review, compaction policy, and privacy filtering.
- **Dashboard Theater:** traces that do not become evals, fixes, or rollback
  rules are observability, not a feedback loop.
- **Telemetry Theater:** spans that capture command names and durations but
  not prompts, completions, or tool I/O. Wrap the LLM client itself;
  harness-level spans alone cannot fuel trace-to-eval.
- **Score Without Inspection:** scoring readiness from file or field presence
  instead of observed emission. Each row needs a recent example of the signal
  landing somewhere readable, not a declaration that it would.

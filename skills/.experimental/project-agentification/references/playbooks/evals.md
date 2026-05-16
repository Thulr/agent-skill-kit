# evals

## What it is

Evals are the measurement layer that tells you whether agent behavior is correct, consistent, and
safe across prompt changes, model upgrades, tool changes, and policy updates. Three phases of
maturity match the OpenAI progression:

1. **Debug from traces** — inspect individual run trajectories when something fails; identify the
   step where behavior diverged from intent.
2. **Datasets + eval runs** — build a named dataset of input/expected-output pairs and run
   repeatable graded evaluations; comparison across runs becomes valid only when inputs are fixed.
3. **Continuous (not episodic) evaluation** — wire evals into CI so every merge that touches
   AGENTS.md, skills, tools, or hooks triggers a targeted eval run before the change ships.

LangSmith makes the split concrete: **offline evaluation** for benchmarking and regression testing
(fixed datasets, graded runs, trend dashboards) versus **online evaluation** for production
monitoring (sampling live runs, flagging regressions in real traffic, feeding failures back to
datasets).

The PIV (Plan-Implement-Validate) loop treats evals as the Validate phase: the loop captures the
failure, feeds the stack trace back into the executor, and retries autonomously. Adversarial test
sets designed specifically to trigger AI hallucinations are a first-class citizen of that loop.

## Why it matters for agents

- **Prompt compliance is ~70%; evals measure the other 30%.** Evals surface the gap between what
  the agent is told and what it does — the gap that instruction files cannot close. (W3)
- **Policy changes are invisible without evals.** A prompt edit, skill activation condition, or
  tool schema change can silently break passing behaviors; evals are how changes earn their way
  in. (W3 — gate enforcement)
- **Failure costs are asymmetric.** A regression in an offline dataset costs a CI retry; in
  production it costs a rollback, a postmortem, and human trust. (W6)
- **Human overrule moments are the best training signal.** Every "human corrected agent" event is
  a failed eval case that did not yet exist; capturing those moments is the cheapest source of
  high-quality negatives.
- **Evals are expensive; sample smart.** Running the full suite on every commit is unsustainable;
  tier by risk surface and run the adversarial suite only on prompt/tool/policy changes. (W6)

## Heuristics by intent

### assess

- **H1.** Verify that offline eval datasets exist and are sourced from real failures — not
  synthesized examples. Synthesized inputs miss the distribution of real bugs; a dataset built
  from actual "human overruled agent" moments covers the failure modes that actually occur.
  (severity cap: 4; lens: maintainer)
- **H2.** Check whether evals are triggered in CI on every change to AGENTS.md, skills, tools,
  hooks, or prompt files. A team that only runs evals manually runs them infrequently — the first
  unevaluated prompt change is the one that ships a regression. (severity cap: 4; lens: auditor)
- **H3.** Verify an adversarial case set covers all four categories: prompt injection, ambiguous
  tool outputs, long context, and conflicting instructions. Each category targets a distinct
  hallucination trigger; a suite missing any one of them has a blind spot. (severity cap: 4;
  lens: adversarial)
- **H4.** Confirm the eval harness prevents the agent from stalling on human input — an open
  prompt mid-run means the eval never completes, silently masking a regression. (severity cap: 4;
  lens: cold-agent)
- **H5.** Check whether online monitoring is sampling live production runs and routing new
  failures back into the offline dataset. An eval suite that never grows from production signal
  diverges from the real failure distribution over time. (severity cap: 3; lens: auditor)

### harden

- **H1.** Synthesized-only dataset → audit each case for real-failure provenance; add a
  `source: real-failure | synthesized` tag to every case; prioritize harvesting from "human
  overruled" events in traces and approval logs.
- **H2.** Evals not in CI → add a targeted eval job to the agent CI workflow
  (`agent-ci.yml`); trigger on path changes to `AGENTS.md`, `.agents/skills/**`,
  `agent/schemas/**`, `agent/prompts/**`, and hook config; fail the job on regression.
- **H3.** Adversarial suite incomplete → fill all four categories. Prompt injection: embed a
  competing instruction in a file the agent will read. Ambiguous tool output: return a response
  with two valid interpretations. Long context: add filler to push the task near the context
  limit. Conflicting instructions: place contradictory directives in AGENTS.md and a skill file.
- **H4.** Agent stalls on human input during evals → adopt the OpenHands eval harness pattern:
  stub or mock any approval prompt; if the harness cannot proceed without human input, the eval
  marks that run as a failure immediately.
- **H5.** No online monitoring → configure LangSmith (or equivalent) to sample 5–10% of
  production runs; set automated graders on outputs; pipe confirmed failures to the offline
  dataset with a `source: production` tag.

### scaffold

- **Do not autogenerate eval cases from templates or model output.** Synthetic cases regress to
  the model's training distribution and miss the adversarial and edge cases that actually occur
  in production. Every new case must be grounded in a real failure or a named threat. (W1)
- **H1.** (W1 guard) Before adding an eval case, state: the failure mode it covers, the source
  (real failure / named threat / adversarial category), and the grader that will score it. Cases
  without all three are not mergeable.
- **H2.** Start with the smallest viable offline dataset: 5–10 cases from real bugs or "human
  overruled" moments. Add the four adversarial categories. Wire CI. Then expand — small and
  high-signal beats large and low-signal.
- **H3.** Structure eval cases as executable repo-level tasks (SWE-bench pattern), not isolated
  code snippets: include the starting repo state (git ref or fixture), the task description, the
  expected observable outcome, and the grader predicate.
- **H4.** Run untrusted agent-generated code inside Docker during evals (Aider benchmark pattern):
  record repo git hash, model, edit format, and settings in the run manifest; pin the image; never
  execute LLM-written code outside the container.

### diagnose

- **H1.** Eval passes but production regresses → rank: (1) online monitoring not sampling live
  traffic — dataset is stale; (2) grader too lenient — passing cases that should fail; (3) eval
  inputs are synthesized and diverge from production distribution.
- **H2.** Eval suite never catches regressions → rank: (1) not triggered on prompt/tool/policy
  changes in CI — only run manually; (2) adversarial categories missing — suite has no cases
  designed to trigger failure modes; (3) dataset was built entirely from synthesized examples.
- **H3.** Agent stalls mid-eval run → rank: (1) harness not stubbing approval prompts — eval
  blocks waiting for a human; (2) tool output unexpectedly returns an interactive prompt; (3)
  long-context case exceeds model limit and halts rather than failing gracefully.
- **H4.** Eval runs are not reproducible across machines → rank: (1) LLM-generated code run
  outside Docker — environment differs; (2) run manifest missing repo git hash or model version;
  (3) dataset cases reference external state that changes between runs.

## Empirical warnings

- **W3 (dominant)** — Instruction compliance is ~70%; evals measure the delta. Correctness,
  safety, and robustness must be verified by evals, not assumed from instruction files. "The
  agent was told X" is not evidence that X happened.
- **W6 (cost discipline)** — Evals are expensive. Tier by risk surface: smoke evals on routine
  changes; full adversarial suite only on changes to AGENTS.md, skills, tools, hooks, or prompts.
- **W1 (no autogeneration)** — Do not autogenerate eval cases from model output or templates.
  Synthetic cases converge on modal behavior and miss the distribution tail. Eval data must come
  from real failures.

## Canonical examples

- **SWE-bench** — executable repo-level tasks, not isolated code snippets; each task specifies
  a starting repo state, a natural-language task, and a test suite that grades the patch; the
  canonical reference for repo-level eval design that captures real software engineering failures.
- **Aider `--benchmark` flag in Docker** — records repo git hash, model, edit format, and
  settings in the run manifest; executes LLM-written code inside Docker without human review;
  cross-run comparison is valid only because every variable is recorded and the environment is
  pinned.
- **OpenHands eval harness** — prevents the agent from stalling on human input; keeps runs
  consistent by stubbing approval prompts; the reference pattern for harness design that produces
  comparable, non-blocking eval runs.
- **LangSmith offline/online lifecycle** — offline: fixed datasets, graded runs, regression
  dashboards; online: sampling production runs, automated graders on live traffic, failures
  routed back to the offline dataset; named pattern for closing the loop between eval and
  production.

## Sources

- "SWE-agent" — executable repo-level benchmark; trajectory-based grading; the canonical
  reference for task-level eval design over isolated snippet tests.
- "Harness Engineering: Leveraging Codex in an Agent-First World" — eval-on-prompt-change as CI
  requirement; debug-from-traces → datasets → continuous evaluation progression; adversarial
  suite categories (prompt injection, ambiguous tool outputs, long context, conflicting
  instructions).
- "AI Risk Management Framework (and Generative AI Profile)" — pre-deployment testing
  requirements; human-overrule evidence collection; evals as governance evidence for policy
  changes.
- "OWASP LLM and Agent Top 10" — prompt injection and adversarial inputs as primary eval
  threat categories; tool abuse and conflicting instruction scenarios as required test cases.

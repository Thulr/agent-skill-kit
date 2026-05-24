# activation-cases.md — loop-architect

These cases check whether `loop-architect` (1) activates at the right time,
(2) places integration points on the right tier of the optimization
staircase, (3) scores feedback-loop readiness, and (4) scaffolds the right
Level 1 / 2 / 3 / 4 template — without side effects on vague invocation.

## Full test sequence (Phase 1 → 3)

Run from the repository root. Phase 1 is free and fast; Phases 2 and 3 are
opt-in and cost a few cents each in API spend.

```bash
# ── Phase 1 — static / contract gates (free, ~2s) ─────────────────────
just check                                                          # all skills' static checks
bash skills/loop-architect/evals/run-static-checks.sh               # just this skill

# ── Phase 2 — semantic diagnosis grader (free dry-run; ~$0.05 live) ───
python3 skills/loop-architect/evals/phase2-grader.py --dry-run      # preview prompts, no API
python3 skills/loop-architect/evals/phase2-grader.py --live         # grade cases against Claude
python3 skills/loop-architect/evals/phase2-grader.py --live --case agent-needs-sandbox
python3 skills/loop-architect/evals/phase2-grader.py --live --case traces-not-loop
python3 skills/loop-architect/evals/phase2-grader.py --live --case model-swap-benchmark
python3 skills/loop-architect/evals/phase2-grader.py --live --case post-readiness-operating-loop
python3 skills/loop-architect/evals/phase2-grader.py --live --model opus   # ~$0.25, Opus 4.7

# ── Phase 3 — sandbox scaffold + opt-in DSPy run (~$0.20 for execute) ─
bash skills/loop-architect/evals/integration-test.sh setup          # creates test-sandbox/src/classifier.py
#  ↳ HUMAN STEP: in a FRESH Claude Code session, prompt:
#     "Run /loop-architect on test-sandbox/. Scaffold the recommended optimization loop."
#     The agent should produce test-sandbox/ai-ops/dataset.json + compile_classifier.py.
bash skills/loop-architect/evals/integration-test.sh verify         # asserts ai-ops/ shape (free)
bash skills/loop-architect/evals/integration-test.sh execute        # real DSPy compile (~$0.20)
bash skills/loop-architect/evals/integration-test.sh teardown       # rm -rf test-sandbox/ + venv

# Re-running Phase 3 cleanly without paying for a dspy-ai reinstall:
bash skills/loop-architect/evals/integration-test.sh refresh        # teardown sandbox only, keep venv, re-setup
```

**Fresh-session caveat.** Phase 3's "HUMAN STEP" should run in a Claude Code
session that has only `SKILL.md` in context — not this repo's other skills.
Running it inside the host repo grades the *host harness*, not
loop-architect in isolation. The hermetic version of Phase 3 is to
checkout the repo fresh, install the skill, and prompt from there.

**Local credentials.** Both opt-in runners read API keys from `.env` at
the repo root before falling back to the shell environment — see
[Local credentials](#local-credentials) below. First `--live` or `execute`
invocation auto-bootstraps `.venv-loop-architect/` and installs deps.

## Static Verification

What the Phase 1 static check covers: file presence, `skill.json` and
`trigger-evals.json` schema shape, `SKILL.md` frontmatter + word count + no
source-author leak, and that every template under `references/templates/`
and every fixture under `evals/fixtures/` parses with `python3 -m
py_compile`.

## Manual evals (opt-in)

Two additional runners ship with this skill but are **not** invoked by
`just check`. They execute the Phase 2 and Phase 3 verification described
in [`TEST_PLAN.md`](./TEST_PLAN.md).

| Runner | What it does | Cost estimate | When to run |
|--------|--------------|---------------|-------------|
| `evals/phase2-grader.py` | Loads `SKILL.md` as system context, feeds mock workspace fixtures to Claude, has a separate Claude call judge the diagnosis against ground truth. First `--live` invocation auto-bootstraps `.venv-loop-architect/` and installs `anthropic` (shared venv with `integration-test.sh execute`). | ~$0.05 per `--live` run with default sonnet model. ~$0.25 with `--model opus`. | Before any `SKILL.md` edit; after refactoring `references/templates/`. |
| `evals/integration-test.sh` | Sets up `test-sandbox/`, prompts a human to invoke `/loop-architect` on it, verifies the scaffolded `ai-ops/` artifacts, optionally executes the generated DSPy compiler against a real model. | Free for `setup` + `verify` + `teardown`. ~$0.20 per `execute` (real DSPy run against gpt-4o-mini). | Before promoting `skill.json` `status` from `draft` to `published`. |

### Local credentials

Both runners read API keys from a `.env` file at the repo root before
falling back to the shell environment. The file is gitignored; copy
`.env.example` to `.env` and fill in the keys you need:

```bash
cp .env.example .env
# edit .env to add ANTHROPIC_API_KEY (phase2-grader) and/or OPENAI_API_KEY (integration-test execute)
```

Already-set shell environment variables win over `.env`, so a
`OPENAI_API_KEY=... bash ...` one-liner still overrides the file. The
loader is strict — `KEY=VALUE` per line, `#` for comments, optional
quotes; no shell expansion. For richer behavior install `python-dotenv`
and use it directly.

See the [Full test sequence](#full-test-sequence-phase-1--3) at the top of
this file for the canonical invocation order. Behavior on missing keys:

- Missing `ANTHROPIC_API_KEY` → `phase2-grader.py --live` exits 2 cleanly.
- Missing `OPENAI_API_KEY` → `integration-test.sh execute` skips the run.

## Behavioral cases

### Positive

#### P1 — Bare invocation

**Prompt:** `Run /loop-architect on this repo.`

**Expected:**
- Loads `SKILL.md` and begins the Step 1 Audit (workspace scan).
- Reports discovered integration points before scaffolding anything.
- Includes a Loop Readiness Matrix and Production Gap before scaffolding.
- Asks the user to pick a tier (Level 1 / 2 / 3 / 4) before writing any file.

**Fail if:** scaffolds an `ai-ops/` directory without an audit report; jumps to Level 2 by default.

---

#### P2 — Zero-Shot translator

**Prompt:** A file with `prompt = f"Translate this text to Spanish: {text}"` followed by "Can you check how I'm calling OpenAI here and make it better?"

**Expected:**
- Diagnoses the integration as **Level 0 (Zero-Shot)**.
- Recommends extracting into a **Level 2 Cognitive Subroutine** scaffold.
- References `references/templates/level-2-subroutine-compiler.py` as the template.
- Mentions `dspy.Signature` + `dspy.Predict` + one of `MIPROv2`/`BootstrapFewShot`.

**Fail if:** recommends Level 1 prompt-patching for a stateless text-in/text-out task; omits any compilation target.

---

#### P3 — Un-sandboxed agent loop

**Prompt:** A CLI agent that reads files and executes shell via `subprocess` with no isolation, no iteration cap, no cost cap. "How do I stop my agent from failing?"

**Expected:**
- Flags the un-sandboxed `subprocess.run(shell=True)` execution as the primary risk.
- Recommends a **Level 3 Sandbox + Repair Harness** BEFORE any prompt optimization.
- References `references/templates/level-3-sandbox-harness.py`.
- Names the required guardrails: container isolation, iteration cap, cost circuit-breaker, verification step, and failure-to-artifact repair log.

**Fail if:** suggests fixing the prompt first; recommends Level 2 compilation while shell execution remains un-sandboxed.

---

#### P4 — Open-ended developer agent rules

**Prompt:** "Help me set up an eval suite for the coding agent I'm building — I want the agent's rules file to get patched when it fails an eval."

**Expected:**
- Routes to **Level 1 System-Prompt Learning**.
- References `references/templates/level-1-prompt-learner.py`.
- Mentions: golden eval dataset, held-out eval, LLM-as-a-judge with structured critiques (not scalar scores), meta-prompt optimizer that emits Markdown diffs, and reviewed application instead of auto-writing the rules file.

**Fail if:** recommends DSPy compilation for an open-ended developer agent; outputs a single judge score with no explanation.

---

#### P5 — Trace dashboard with no learning loop

**Prompt:** "We have Braintrust traces, LangSmith runs, thumbs-down feedback rows, and sampled production transcripts, but none of it changes prompts, evals, or release gates. Can loop-architect tell us what's missing?"

**Expected:**
- Identifies this as observability without a feedback loop.
- Produces the Loop Readiness Matrix with missing interpreter, change surface, cadence, and rollback fields called out.
- Recommends trace-to-eval conversion before prompt, model, or rules changes.
- Names the Production Gap instead of treating dashboards as the optimization artifact.

**Fail if:** says tracing alone solves self-improvement; scaffolds a prompt optimizer before defining replay/eval selection.

---

#### P6 — Model swap regression gate

**Prompt:** "We're swapping the model behind an AI assistant across the product and need to know whether the new release is safe."

**Expected:**
- Routes to **Level 4 System Benchmarking**.
- References `references/templates/level-4-system-benchmark.py`.
- Requires fixed benchmark tasks, baseline/current comparison, pass-rate/cost/latency thresholds, and a rollback rule.

**Fail if:** recommends ad-hoc prompt tuning or a Level 2 compiler for a product-wide regression problem.

---

#### P7 — 6/6 readiness, no autonomous controller

**Prompt:** "The report says every Loop Readiness Matrix field is 6/6. What am I supposed to do with this? How does it make my system autonomously improve?"

**Expected:**
- First verifies that 6/6 reflects observed signal, not field completion. Checks (or asks about) whether LLM prompts/completions are captured, whether trace-to-eval produces non-trivial candidates, and whether `HELD_OUT_EVAL_CMD` is set.
- If preconditions pass: says 6/6 means ready, not autonomous yet. Produces a Next Operating Loop: failed trace/eval -> one allowlisted diff -> live/held-out evals -> system benchmark -> keep only if gates pass. Offers `references/templates/autonomous-improve-loop.mjs`. States that the controller calls an optimizer model, validates allowlisted paths, applies in a branch, reverts failed patches, and stages only green changes.
- If any precondition fails: names that gap as the next loop instead of the controller.

**Fail if:** treats the score as the final deliverable; recommends the controller without verifying its inputs exist; claims autonomy exists without a controller; recommends unreviewed prompt mutation or a placeholder actuator.

---

#### P8 — 6/6 readiness with uninstrumented LLM calls

**Prompt:** A project has a readiness matrix scoring 6/6, an event log with structured decision/fork events, OTel spans around CLI commands, and a trace-to-eval script — but the LLM client calls themselves are not wrapped in any span (prompts and completions are not captured anywhere). "Loop readiness passed 6/6. What's the next loop?"

**Expected:**
- Detects that prompts/completions aren't captured by inspecting one span or asking.
- Names this as **Telemetry Theater** and downgrades the rows that depend on LLM I/O capture (caps them at 3/6 per Step 1.5).
- Recommends wrapping LLM client calls as the next loop, **not** the autonomous controller.
- States explicitly that the controller can't run usefully on skeleton candidates.

**Fail if:** accepts the 6/6 score at face value; recommends the autonomous controller; treats command-level OTel spans as sufficient trace data for trace-to-eval.

---

### Negative

#### N1 — Refactor a function

**Prompt:** `Refactor this typescript function to use early returns.`

**Expected:** skill declines to activate; this is general code review, not AI workspace optimization.

**Fail if:** loads SKILL.md and produces an audit report for a non-AI function.

---

#### N2 — Marketing copy

**Prompt:** `Design a new homepage hero section for our marketing site.`

**Expected:** skill declines. Audience is not developers and no AI integration is involved.

**Fail if:** scaffolds an `ai-ops/` directory; treats marketing copy as a prompt.

---

#### N3 — End-user UX

**Prompt:** `Our consumer signup form has a 60% drop-off rate. Reduce friction.`

**Expected:** skill declines; routes the user to `ux-accessibility-heuristics` if visible.

**Fail if:** produces a prompt optimization plan for a form-completion task.

---

### Edge

#### E1 — Agent-readiness of a code repo

**Prompt:** "Audit this repo so coding assistants stop tripping on it. AGENTS.md is auto-generated and wrong."

**Expected:** skill defers to `project-agentification` (the agent-readiness skill). loop-architect is for **AI integration points inside the workspace**, not for **the workspace's own ergonomics for coding agents**. If activated by mistake, it should explicitly disambiguate before acting.

**Fail if:** loads its own playbook to audit AGENTS.md / hooks / MCP servers — wrong skill.

---

#### E2 — Docs/DX audit

**Prompt:** `Audit our docs site for developer experience issues.`

**Expected:** skill defers to `dx-heuristics`. Same disambiguation rule as E1.

**Fail if:** runs Step 1 Audit on docs (no AI integration points to find).

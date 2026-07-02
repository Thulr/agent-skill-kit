# Activation cases — agent-test

Natural-language behavioral cases for **designing the measurement an AI agent or skill is judged
by**. Each negative names the sibling skill it disambiguates from. The agent should activate on
realistic measurement-design prompts, ask at most one blocker question, and route to
`<intent>/<surface>`.

## Positive

### P1 — Design the eval suite
**Prompt:** `Design our agent's eval suite — we chase one pass-rate and can't tell what broke.`
**Expected:** activates; intent `design`, surface `eval-design`; starts from a failure-mode
ontology and the staircase tier, not an aggregate.

### P2 — Is the judge trustworthy
**Prompt:** `Is our LLM-as-judge trustworthy, or could it be certifying regressions? Review it.`
**Expected:** activates; intent `review`, surface `judge-calibration`; checks calibration against
a human-labeled set, bias, and explanations (Vague Judge).

### P3 — Grade the whole run
**Prompt:** `Per-step evals are green but the run fails — write tests that grade the trajectory.`
**Expected:** activates; intent `do`, surface `trajectory-tests`; reassembles the path and asserts
on tool order/hand-offs/loops (Trajectory Blindness, march of nines).

### P4 — Held-out benchmark for a model swap
**Prompt:** `Build a held-out benchmark to gate our model swap, with a baseline and rollback.`
**Expected:** activates; intent `design`, surface `benchmark-design`; disjoint fixtures, per-slice
scoring, baseline + rollback.

### P5 — Does the skill activate
**Prompt:** `Test whether our skill activates on the right prompts and stays quiet on the wrong ones.`
**Expected:** activates; intent `do`, surface `activation-evals`; positive/negative/edge and
disambiguation cases, false vs missed activation.

### P6 — Full suite review (fan-out)
**Prompt:** `Audit our agent's whole eval and benchmark suite for trustworthiness and score it.`
**Expected:** activates; intent `review`, surface `all`; fans out one agent per surface with
`AGENT-TEST-*` finding IDs.

## Negative

### N1 — Operating the loop
**Prompt:** `Set up a trace-and-eval optimization loop and watch quality drift in production.`
**Expected:** does not activate; defers to `agent-ops` (operating the loop; agent-test designs the
evals it runs).

### N2 — SDK surface design
**Prompt:** `Design the streaming and tool surface of our Agent SDK.`
**Expected:** does not activate; defers to `agent-dx`.

### N3 — Agent-native docs
**Prompt:** `Audit our llms.txt and AGENTS.md so coding agents can read our docs.`
**Expected:** does not activate; defers to `agent-docs`.

### N4 — Repo CI scaffolding
**Prompt:** `Scaffold our repo's CI gates and hooks so the agent's tests run on every PR.`
**Expected:** does not activate; defers to `harden-repo-for-coding-agents` (wiring the gate, not
designing the measurement).

### N5 — Human test suite
**Prompt:** `Review our human test suite for flaky unit and integration tests.`
**Expected:** does not activate; human-authored test-suite review is out of
this catalog's scope (agent-test measures agent behavior, not code tests).

### N6 — Promote a failure to a rule
**Prompt:** `Promote this recurring agent failure into an AGENTS.md rule.`
**Expected:** does not activate; defers to `rules-from-coding-agent-failures`.

## Edge / boundary

### E1 — Candidate quality before it gates
**Prompt:** `We have a trace-to-eval step — is its candidate good enough to gate a change, or skeleton metadata?`
**Expected:** activates; intent `review`, surface `eval-design`; checks for non-trivial candidates
(real prompt+completion+tool I/O) before the eval is trusted.

### E2 — Judge vs deterministic check
**Prompt:** `Our judge and our schema check disagree on the same output — which should gate, and how do we test that?`
**Expected:** activates; intent `design`, surface `judge-calibration`; prefers the deterministic
check where the property is checkable, scopes the judge to the open-ended residue.

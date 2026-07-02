# Activation cases — agent-ops

Natural-language behavioral cases for **operating a running AI agent system** and for the
**family front-door**. Each negative names the sibling skill it disambiguates from. The agent
should activate on realistic ops prompts, ask at most one blocker question, and route to
`<intent>/<surface>` — or hand off via the front-door when the work is building, not operating.

## Positive

### P1 — Observability that doesn't close the loop
**Prompt:** `Our agent traces look rich but nothing improves — are these usable? Review it.`
**Expected:** activates; intent `review`, surface `observability`; checks spans carry
prompt+completion+tool I/O, trajectory is graded, traces become evals/fixes (not dashboard theater).

### P2 — Stand up the flywheel
**Prompt:** `Set up a trace-and-eval flywheel so production traces turn into evals and fixes.`
**Expected:** activates; intent `do`, surface `optimization-loop`; applies the Loop Readiness
Matrix scored on observed emission.

### P3 — Is autonomy safe to enable
**Prompt:** `We want our agent to auto-apply prompt improvements — is that safe, what gates?`
**Expected:** activates; intent `review`, surface `autonomous-controller`; requires held-out
eval, diff review, circuit-breaker, one-diff-per-cycle, revert-on-failed-gate.

### P4 — Reliability + cost at scale
**Prompt:** `Per-step evals pass but production fails and spend is unbounded — design controls.`
**Expected:** activates; intent `design`, surface `cost-and-reliability`; march-of-nines,
circuit-breakers, a release gate decomposed by failure mode.

### P5 — Maturity placement (front-door)
**Prompt:** `Where are we on the agent maturity ladder and what should we build next?`
**Expected:** activates; intent `design`, surface `maturity-and-governance`; places on the
staircase and routes the next build to the right sibling.

### P6 — Generic "make it production-ready" (front-door)
**Prompt:** `Make our agent system production-ready — not sure where to start.`
**Expected:** activates as the front-door; assesses maturity, then routes onward by what the
prompt actually needs.

## Negative

### N1 — Designing the SDK surface
**Prompt:** `Design the streaming and stop-condition surface of our Agent SDK.`
**Expected:** does not activate; defers to `agent-dx` (building the surface, not operating it).

### N2 — Designing evals/judges
**Prompt:** `Design our LLM-as-judge and held-out benchmark for grading the agent.`
**Expected:** does not activate; defers to `agent-test` (eval design; agent-ops *runs* the loop
but hands judge/benchmark design to agent-test).

### N3 — Agent-native docs
**Prompt:** `Audit our llms.txt and AGENTS.md so coding agents can read our docs.`
**Expected:** does not activate; defers to `agent-docs`.

### N4 — Repo hardening
**Prompt:** `Scaffold our repo's AGENTS.md, hooks, and CI gates so Claude Code stops tripping.`
**Expected:** does not activate; defers to `harden-repo-for-coding-agents`.

### N5 — Human-system perf/observability
**Prompt:** `Audit our production web service for p99 latency and SLO gaps.`
**Expected:** does not activate; human/runtime service observability, not agent-loop ops.

### N6 — Promoting failures to rules
**Prompt:** `Promote this recurring agent failure into an AGENTS.md rule from our log.`
**Expected:** does not activate; defers to `rules-from-coding-agent-failures` (agent-ops routes
out to it once a signal exists).

## Edge / boundary

### E1 — Agent-loop observability vs human-service observability
**Prompt:** `We want to watch agent loop quality drift, not generic service latency.`
**Expected:** activates on the *agent-loop* framing; intent `review`, surface `observability`;
explicitly distinguishes agent-loop observability from the human/runtime service tier.

### E2 — Ready to hand to a controller
**Prompt:** `We have a trace-to-eval step — are we ready to hand it to an autonomous controller?`
**Expected:** activates; intent `review`, surface `optimization-loop`; checks 6/6 on observed
emission and the controller preconditions before recommending autonomy (`autonomous-controller`).

# Maturity and Governance Playbook

## Scope

The front-door surface for agent-ops. It does two jobs: place an integration on the AI Optimization Staircase and recommend the next tier with its gate-before-persistence, and set the governance/provenance posture for agent-authored change. It is also the family router — agent-ops *operates* agent systems but hands *design* work out to siblings. Use it to answer "how mature is this loop, and where do we go next?" and "who owns this change, and what gate must it pass before it ships?"

- **In:** staircase placement (L1–L4) with the gate each tier must clear; next-tier recommendation; provenance/ownership posture for agent-authored diffs; the God Prompt boundary (permissions, costs, side-effects belong in an L3 harness, not the prompt); routing out to the right sibling.
- **Out:** designing the SDK/tool surface (→ `agent-dx`); designing evals, judges, or benchmarks (→ `agent-test`); writing agent-native docs (→ `agent-docs`); scaffolding/hardening repo files (→ `harden-repo-for-coding-agents`); promoting observed failures into rules (→ `rules-from-coding-agent-failures`). Running the loop, scoring readiness, and governing autonomy live in this skill's sibling operator playbooks.
- **Intents this surface answers:** do, review, design.

## Grounding

- The AI Optimization Staircase places an integration on one of four tiers, each with a gate that must clear before a change persists: L1 System-Prompt Learning (rules/instruction files; gate: judge explanations + held-out eval + reviewed diff), L2 Subroutine Compilation (declarative signatures for parsers/classifiers/routers; gate: schema metric + train/test split), L3 Sandbox + Repair Harness (container/cost/permission rails for terminal agents and PR builders; gate: isolation + tests + repair loop), L4 System Benchmarking (replayable task suites for model swaps and release gates; gate: per-slice guardrail-vs-north-star scoring + baseline + rollback).
- Permissions, cost ceilings, and side-effect control are runtime properties of an L3 harness, not text in a prompt. A prompt cannot enforce a budget or contain a side effect; only harness code can.
- Provenance matters because agent-authored changes are a review surface, not free output: an agent-written diff that touches instruction files, hooks, or harness config is reviewed at production-code depth before it persists.
- These are operational conventions for staging and governing agent change, not vendor-specific claims; the staircase, judge calibration, and held-out-eval discipline are the load-bearing pieces.

## Good signals

- Every agent integration has a named tier on the staircase and a one-line reason it sits there, not a vague "we use AI here."
- The next-tier recommendation names the specific gate the integration must clear before it earns the promotion, not just "get better."
- Permissions, cost ceilings, and side-effect control live in harness code (L3), and the system prompt is free of "do not delete," "stay under $X," "you are allowed to" clauses.
- Agent-authored changes carry provenance: which agent/session produced the diff, what signal triggered it, and which human reviewed it before merge.
- Each tier's gate is wired before the tier is claimed: L1 has a held-out eval and reviewed diff, L2 a train/test split, L3 isolation+repair, L4 per-slice scoring with a baseline and a rollback threshold.
- Promotion is evidence-led: a tier moves up only when its current gate is green on observed runs, never on a date or a hunch.
- Routing is explicit — a maturity assessment ends by naming which sibling skill owns the design work this loop now needs.
- A single aggregate pass-rate is never used as the release gate; guardrail regressions and north-star dips are tagged and treated differently.

## Common failures

- **God Prompt.** Permissions, cost limits, and side-effect rules are stuffed into the system prompt instead of enforced by an L3 harness; the prompt grows into a pseudo-policy file that the model can ignore and that nothing enforces.
- **Tier inflation.** An integration is called L4 because it has a dashboard, but there is no replayable suite, baseline, or rollback threshold — so the "benchmark" cannot gate a release.
- **Gate skipped on promotion.** A loop is promoted to the next tier without clearing that tier's gate (e.g. L1 self-improvement with no held-out eval or diff review), so the maturity label overstates what is actually governed.
- **Ungated self-improvement.** Agent-authored changes auto-write to instruction or harness files with no held-out eval, diff review, compaction policy, or privacy filter — provenance and the revert path are both absent.
- **Provenance loss.** Agent-authored diffs land with no record of which session, signal, or reviewer produced them, so a regression cannot be traced back or attributed.
- **God Gate.** A single aggregate pass-rate is the release gate; it hides which slice broke and conflates a guardrail regression (block ship) with a north-star/capability dip (report only).
- **Front-door swallows design work.** agent-ops is asked to redesign an SDK, write docs, or author evals itself instead of routing to the sibling that owns that surface — the operator skill quietly becomes a design skill it was not built for.

## Heuristics

- **(do, review) Place the integration on the staircase first.** Before recommending anything, name its tier (L1–L4) and the single reason it sits there. A loop with no tier has no maturity to govern.
- **(review, design) Recommend the next tier by its gate, not its label.** "Move to L3" is meaningless; "add a sandbox with isolation, tests, and a repair loop before you let it touch the filesystem" is the recommendation. The gate is the deliverable.
- **(design) Push permissions, cost, and side-effects out of the prompt into an L3 harness.** If a control must be enforced rather than requested, it is harness code. Strip God-Prompt clauses and re-home them as rails.
- **(review, design) Require provenance on every agent-authored change.** Record the session, the triggering signal, and the human reviewer on any diff an agent writes to instruction or harness files; an unattributable diff does not persist.
- **(do, review) Gate self-improvement before it writes.** No agent auto-write lands without a held-out eval, a reviewed diff, a compaction policy, and a privacy filter — and a revert path that triggers on a failed gate.
- **(review, design) The L4 release gate must be decomposed, not a single pass-rate.** A tier claiming L4 needs per-slice guardrail-vs-north-star scoring with a baseline and a rollback threshold; the decomposition mechanics live in `cost-and-reliability.md` — confirm the gate is wired and observed-green before you promote, don't re-derive it here.
- **(do) Route design work out, don't absorb it.** When an assessment surfaces SDK, docs, eval, scaffolding, or rule work, hand it to the owning sibling by name rather than doing it inside agent-ops.
- **(review) Promote on green gates, not calendar pressure.** A tier moves up only when its current gate is observed-green; a deadline is not evidence the gate passed.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does every agent integration have a named staircase tier and reason? | Maturity is unassessable | Place each on L1–L4 with a one-line reason |
| Does the next-tier recommendation name the gate to clear? | "Get better" is not actionable | Recommend the specific gate-before-persistence for that tier |
| Are permissions/costs/side-effects in harness code, not the prompt? | God Prompt — nothing enforces them | Re-home the controls as L3 rails; strip the prompt clauses |
| Do agent-authored diffs carry session, signal, and reviewer provenance? | Regressions can't be traced or attributed | Record provenance on every agent-written change |
| Does self-improvement write only after a held-out eval + diff review + revert path? | Ungated self-improvement | Add the gate and rollback before any auto-write |
| Is the release gate decomposed by guardrail-vs-north-star slice? | God Gate hides which slice broke | Tag slices; block on guardrail, report on north-star |
| Does the assessment route design work to the right sibling? | The front-door absorbs work it doesn't own | Hand off to agent-dx / agent-test / agent-docs / harden-repo / rules-from-failures |

## Cross-references

- `optimization-loop.md` — scoring the loop and the instrumentation smoke that must pass before a tier is claimed.
- `autonomous-controller.md` — the autonomous controller that only starts after 6/6 readiness and clears this surface's self-improvement gate.
- `cost-and-reliability.md` — owns release-gate decomposition (per-slice guardrail-vs-north-star, baseline, rollback); the L4 gate this surface checks is scored there.
- → `agent-dx` to design the SDK/tool surface the loop runs on.
- → `agent-test` to design the evals, judges, and benchmarks the L1/L4 gates depend on.
- → `agent-docs` to write the agent-native docs the integration consumes.
- → `harden-repo-for-coding-agents` to scaffold and harden the repo files the harness and rails live in.
- → `rules-from-coding-agent-failures` to promote an observed failure into a durable rule.
- finding IDs `AGENT-OPS-GOV-NNN`.
- `references/intents/{do,review,design}.csv` row `maturity-and-governance` — the entry points.

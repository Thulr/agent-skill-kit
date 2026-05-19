---
date: 2026-05-19
harness: codex
sub-surface: skills
severity: 2
status: resolved
related: []
---
# Clean-architecture audit all implied subagents without host permission

## What happened

The clean-architecture skill treated `audit all` as enough signal to spawn
parallel sub-agents. In Codex, the active platform rule is stricter: sub-agents
may be used only when the user explicitly asks for sub-agents, delegation, or
parallel agent work. When a user selected `all`, Codex responded:

> I can’t use background sub-agents here unless you explicitly ask for delegated agent work

Then it continued sequentially. That preserved safety, but the skill had set
the wrong expectation: `all` meant all audit surfaces, not explicit delegation
consent. The drift lived in
`skills/.experimental/clean-architecture/SKILL.md`,
`references/subagent-dispatch.md`, and the `all` row in
`references/intents/audit.csv`.

## What to do differently

Skill instructions should separate fan-out semantics from delegation consent,
while still trying parallelism whenever it is available. Rows like `all` can
mean "visit every surface," but they should not by themselves imply that the
host is allowed to spawn background agents. When a skill wants sub-agent
parallelism, the runtime should first use any explicit user, project, session,
or host permission that satisfies the active platform policy. If the host
requires fresh explicit permission and none exists, ask one concise opt-in
question before dispatching; absent that opt-in, run the same lenses or
surfaces sequentially. Add activation coverage for the explicit form, e.g.
`clean architecture audit all with parallel sub-agents`, so the intended route
and consent signal are both represented.

## Closed by

Current patch. Updated clean-architecture runtime instructions, dispatch
reference, audit router row, activation cases, trigger evals, and README to
make sub-agent dispatch try-first and consent-aware while keeping `audit all`
as the all-surface route.

# Activation Cases

Positive cases should trigger this skill. Negative cases should NOT trigger it (or should trigger a more specific skill instead).

## Positive — clear triggers

1. "Audit our repo for agent-readiness."
2. "We added Claude Code last month; how do we make this repo work better with it?"
3. "Review our AGENTS.md."
4. "Generate AGENTS.md from the failures we've seen in the last week of agent PRs."
5. "Why does Cursor keep editing the wrong files in our monorepo?"
6. "Add an approval tier for database migrations to our hook config."
7. "Score our repository against the Engineering Agents maturity rubric."
8. "Scaffold a skill for our PR-review workflow."
9. "The agent failed on PR #4321 — root-cause it."
10. "Harden this repo against prompt-injection-via-AGENTS.md."
11. "Set up evals for our agentic workflow."
12. "Should we use MCP or a typed function tool for our internal API?"

## Positive — adjacent triggers (also valid)

- "Make our repo agent-native."
- "Harness engineering for this repo."
- "Run an agent-readiness check."
- "Where are we on Level 1–5?"

## Negative — should NOT trigger

1. "Audit our public API for DX issues." → `dx-heuristics`.
2. "Review the error messages in our CLI." → `dx-heuristics`.
3. "Write a unit test for this function." → general coding.
4. "Bug fix in `src/foo.py`." → general coding.
5. "What's the best way to deploy a Next.js app?" → not in scope.
6. "Run our test suite." → not in scope.

## Edge cases — could be either; ask once

1. "Make our docs better." → could be `dx-heuristics` (developer docs) or `project-agentification` (docs-index sub-surface for agents). Ask: "for human readers or for AI agents?"
2. "Add a hook." → could mean Claude Code hook (this skill, `gates` playbook) or generic Git hook. Ask: "Claude Code PreToolUse/PostToolUse hook, or a Git hook?"
3. "Set up CI for our agent." → overlaps with `gates` playbook + general DevOps. If the question is about agent-specific gates, this skill applies.

## Behavioral assertions

- On a bare invocation (`"use project-agentification"`), the skill must:
  - Load `references/intent-router.csv`.
  - Present the intent menu.
  - NOT inspect the repo, NOT load any playbook, NOT write any file.
- On `scaffold` invocation without project knowledge stated:
  - Ask the user for tech stack, repo layout / scope, build / test / lint
    commands, and top-level invariants.
  - Do not autogenerate from boilerplate (W9).
  - If the user requests reflection-log-driven scaffolding, redirect to
    `evidence-driven-agent-rules` (this skill is project-context-first,
    not evidence-driven).
- On `assess` invocation with a specific sub-surface:
  - Load only that sub-surface's playbook (plus warnings + rubric).
  - Run all four lenses on it.
  - Score that sub-surface only; not the whole repo.
- On any output, every finding has a severity (0–4) and every recommendation has at least one source citation from `skill.json`.

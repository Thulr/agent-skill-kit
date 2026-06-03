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
13. "Audit whether our required GitHub Actions checks are safe to run on self-hosted runners for fork PRs."
14. "Turn these agent-readiness findings into a tracked roadmap."
15. "Verify whether AG-GATES-003 was fixed by this PR."

## Positive — adjacent triggers (also valid)

- "Make our repo agent-native."
- "Harness engineering for this repo."
- "Run an agent-readiness check."
- "Where are we on Level 1–5?"

## Negative — should NOT trigger

1. "Audit our public API for DX issues." → `dx-audit`.
2. "Review the error messages in our CLI." → `dx-audit`.
3. "Write a unit test for this function." → general coding.
4. "Bug fix in `src/foo.py`." → general coding.
5. "What's the best way to deploy a Next.js app?" → not in scope.
6. "Run our test suite." → not in scope.

## Edge cases — could be either; ask once

1. "Make our docs better." → could be `docs-audit` / `docs-design` or `agent-readiness` (docs-index surface for agents). Ask: "for human readers or for AI agents?"
2. "Add a hook." → could mean Claude Code hook (this skill, `gates` playbook) or generic Git hook. Ask: "Claude Code PreToolUse/PostToolUse hook, or a Git hook?"
3. "Set up CI for our agent." → overlaps with general DevOps, but activates when the question is about agent-specific gates, runner trust, or required-check enforcement.

## Behavioral assertions

- On a bare invocation (`"use agent-readiness"`), the skill must:
  - Load `references/intent-router.csv`.
  - Present the intent menu.
  - NOT inspect the repo, NOT load any playbook, NOT write any file.
- On `scaffold` invocation without project knowledge stated:
  - Ask the user for tech stack, repo layout / scope, build / test / lint
    commands, and top-level invariants.
  - Do not autogenerate from boilerplate (W9).
  - If the user requests reflection-log-driven scaffolding, redirect to
    `agent-rules` (this skill is project-context-first,
    not evidence-driven).
- On `assess` invocation with a specific surface:
  - Load only that surface's playbook (plus warnings + rubric).
  - Run all four lenses on it.
  - Score that surface only; not the whole repo.
- On CI/runner-trust prompts:
  - Route to the `ci-runners` control surface.
  - Compare runner labels, workflow events, token/secret exposure, required-check parity, and docs claims against actual enforcement.
- On any output, every finding has a severity (0–4) and every recommendation has at least one source citation from `skill.json`.
- On large `assess` output (7+ findings) or any severity 3–4 finding:
  - Assign stable finding IDs.
  - Save both `agent-readiness-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
    and `agent-readiness-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`
    under `docs/audits/`, or use the matching `audit-artifacts/` fallback.
  - Report both saved paths rather than merely offering tracking.
  - Group findings into issue-sized work before proposing GitHub issues, and
    only create roadmaps or issues after explicit confirmation.
  - Check off a finding only after its verification rule passes; a merged PR
    or closed issue is evidence to inspect, not proof.

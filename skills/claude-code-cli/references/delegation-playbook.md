# Delegation Playbook

Use this playbook for second opinions, plan review, bug analysis, architecture
questions, or prompt preparation.

## Delegation Frame

A good Claude Code prompt includes:

- the precise question to answer
- the repository or file scope
- constraints and non-goals
- what tools Claude may use
- the desired output format
- any known uncertainty or suspected failure mode

Do not ask Claude to "look at everything" when a narrower question would work.

## Prompt Roles

Choose one role:

- **Reviewer**: find defects in an implementation or plan.
- **Skeptic**: attack assumptions and identify overlooked risks.
- **Architect**: evaluate boundaries, dependencies, and future change cost.
- **Debugger**: propose the most likely causes and verification steps.
- **Rubric judge**: score an artifact against explicit criteria.

Use one role per invocation unless the user explicitly wants a broader panel.

## Cross-Project Reflection

Use this frame when another skill, especially `reflect-all-the-things`, asks
Claude Code for evidence about recurring agent mistakes and user workflow
patterns.

Rules:

- Run from a neutral directory such as `$HOME` using
  `scripts/claude-cross-project-reflect.sh`; do not let the current repository
  become the implied project scope.
- Ask for first-person self-assessment, but label it as subjective until
  corroborated by local traces, PR data, or another agent.
- Request patterns across projects: repeated validation misses, instruction
  misses, scope drift, user corrections, review themes, and successful workflows
  worth reusing.
- Ask for source classes or safe path/timestamp references when possible, not
  raw transcripts or secrets.
- Treat "I remember" claims as leads. The calling reflection skill must verify
  high-impact claims before promoting durable rules.

## Prompt Preparation Mode

When the user asks for a prompt only:

1. Build the prompt with clear scope and output rules.
2. Include the exact command to run.
3. Do not invoke Claude Code.
4. Mention any data or secret risks the user should review first.

## Disagreement Handling

When Claude's answer conflicts with the calling agent's analysis:

- quote or summarize the concrete claim
- verify it against files, tests, or docs
- preserve uncertainty instead of forcing consensus
- ask a narrower follow-up only if it will change the next action

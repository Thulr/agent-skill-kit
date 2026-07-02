# Delegation Playbook

Use this playbook for second opinions, plan review, bug analysis, architecture
questions, or prompt preparation with `cursor-agent -p --mode plan`.

## Delegation Frame

A good cursor-agent prompt includes: the precise question, the repository or file
scope, constraints and non-goals, the read-only stance, the desired output
format, and any known uncertainty or suspected failure mode. Don't ask
cursor-agent to "look at everything" when a narrower question would work.

## Prompt Roles

Choose one role per invocation: **Reviewer** (find defects), **Skeptic** (attack
assumptions), **Architect** (evaluate boundaries and change cost), **Debugger**
(most likely causes + verification steps), or **Rubric judge** (score against
explicit criteria).

## Picking a model

Model diversity is the value: run the question past a *different* model than
the agent that produced the work — see the `--model` bullet in `cli-contract.md`.

## Prompt Preparation Mode

When the user asks for a prompt only: build the prompt with clear scope and output
rules, include the exact command to run, do not invoke cursor-agent, and mention
any data/secret risks to review first. `--dry-run` on either script prints the
prompt and command without calling cursor-agent.

## Disagreement Handling

When cursor-agent's answer conflicts with the calling agent's analysis: quote the
concrete claim, verify it against files/tests/docs, preserve uncertainty instead
of forcing consensus, and ask a narrower follow-up only if it will change the next
action.

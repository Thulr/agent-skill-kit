<!-- Reflection-log entry template.

     Drop into target repo at `docs/reflection-log/_template.md`. Contributors
     copy this to `YYYY-MM-DD-<slug>.md` per failure.

     Required fills marked with <placeholder>. Fill every <placeholder>
     before committing — an entry with unfilled placeholders is not
     usable evidence. -->

---
date: YYYY-MM-DD
harness: <claude-code | cursor | codex | copilot | aider | windsurf | other>
sub-surface: <instruction-surface | gates | scaffold | skills | docs-index | specs | governance | sandbox | telemetry | evals | tools | other>
severity: <0-4>
status: open
related: []
---
# <one-line title — what tripped, in imperative-past-tense>

## What happened

<Specific. File paths, commit SHAs, exact commands, exact output. The next
reader should be able to reproduce — or at least picture — the failure
without asking you.>

## What to do differently

<The smallest hook, rule, or gate that closes this gap. Cite W1 from the `rules-from-coding-agent-failures` skill's
`references/empirical-warnings-w1.md`, and W2–W10 from the installed
`harden-repo-for-coding-agents` skill's `references/empirical-warnings.md`,
where applicable. If this points to a skill-level fix (template, playbook
heuristic), name the file + heuristic ID.>

## Closed by

<Filled in when resolved. PR number or commit SHA, plus a one-line summary
of how it was closed (rule, hook, ambiguity removal).>

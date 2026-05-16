<!-- README §Agents pointer block.

     Drop this into the project's existing `README.md` (under a top-level
     `## Agents` or `## Authoring` heading) when AGENTS.md does not yet
     exist. The block makes `docs/agent-failures.md` discoverable in the
     W1-interim where the agent surface has only the reflection log.

     Prescribed by instruction-surface scaffold H5. Required when:
     - The repo has `docs/agent-failures.md` but no `AGENTS.md` (Stage 0).
     - Any harness in the step 4.5 inventory loads README at session start
       (true for Copilot, common for Claude Code and Cursor).

     Once AGENTS.md lands, the §Failure-log workflow there absorbs this
     block; reduce the README block to a single line: "See [AGENTS.md]." -->

## Agents

This repository is set up for AI coding agents (Claude Code, Cursor, Codex,
Copilot, Aider, Windsurf, and other AGENTS.md-compatible harnesses).

When an AI coding agent trips on this repo — wastes tokens, edits the wrong
file, hallucinates a convention, makes an unsafe action — record it in
[`docs/agent-failures.md`](./docs/agent-failures.md). **Three entries
describing the same gap** is the threshold for adding a rule, hook, or
`AGENTS.md` sentence to close it (W1: scaffolding from fewer than three
observed failures produces plausible boilerplate that hurts agent success).

<!-- If the repo already has gates (hooks, CI checks) that an agent should
     be aware of before its first action, list them here. Otherwise delete
     this paragraph. -->

Active gates: <e.g., "`.claude/hooks/block-destructive-bash.py` blocks
force-push to main and `rm -rf` of protected paths; see the file for the
full deny-list.">

<!-- Once `AGENTS.md` lands at the repo root, replace this entire section
     with: -->
<!-- ## Agents
     See [AGENTS.md](./AGENTS.md). -->

<!-- README §Agents pointer block.

     Drop this into the project's existing `README.md` (under a top-level
     `## Agents` or `## Authoring` heading) when AGENTS.md does not yet
     exist. The block tells contributors and AI coding agents how this
     repo is set up and what the active gates are.

     Prescribed by instruction-surface scaffold H5. Required when:
     - The project intends to ship an `AGENTS.md` soon (the README
       block is the bridge for the period before it lands).
     - Any harness in the step 4.5 inventory loads README at session
       start (true for Copilot, common for Claude Code and Cursor).

     Once AGENTS.md lands, the §Agents section here can shrink to a
     single line: "See [AGENTS.md]."

     This block is project-context-first. It does NOT presume the
     project keeps a reflection log; that workflow belongs to the
     `agent-rules` skill and the optional pointer at
     the bottom of this block. -->

## Agents

This repository is set up for AI coding agents (Claude Code, Cursor, Codex,
Copilot, Aider, Windsurf, and other AGENTS.md-compatible harnesses).

<!-- One paragraph: what this project does, who reads this file, what
     agents should know before doing anything. Replace the placeholder. -->

<one-line project description>. <One sentence on what makes this project
agent-relevant: monorepo scope, release cadence, top invariants.>

<!-- If the repo already has gates (hooks, CI checks) that an agent should
     be aware of before its first action, list them here. Otherwise delete
     this paragraph. -->

Active gates: <e.g., "`.claude/hooks/block-destructive-bash.py` blocks
force-push to main and `rm -rf` of protected paths; see the file for the
full deny-list.">

<!-- Optional: if the project also keeps a reflection log per
     `agent-rules`, add this paragraph. Otherwise delete it. -->

<!--
This project also runs an evidence-driven feedback loop: agent failures
that produce useful "what to do differently" notes get recorded under
[`docs/reflection-log/`](./docs/reflection-log/). See
[`docs/reflection-log/README.md`](./docs/reflection-log/README.md) for
the workflow (recording bar is low — one observation is enough;
promotion to a rule waits for ≥3 same-gap entries, per W1).
-->

<!-- Once `AGENTS.md` lands at the repo root, replace this entire section
     with: -->
<!-- ## Agents
     See [AGENTS.md](./AGENTS.md). -->

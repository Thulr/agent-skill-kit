# Agent failure log

Record observed agent failures here. **This is the source-of-truth for any future
hand-curated `AGENTS.md`, `CLAUDE.md`, hook, or new skill** — accrue at least three
entries describing a pattern before scaffolding any of those artifacts (per W1).

> **W1 meta-note.** The `project-agentification` skill normally refuses to scaffold
> files without ≥3 observed failures stated. This file is exempt because it does not
> *contain* agent instructions — it *captures the observations* that future instructions
> will be hand-curated from. The structure (columns, headings) is the only content;
> add real entries before treating any row as evidence.

## How to add an entry

When an agent (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider, etc.) trips
in a way that wasted tokens, edited the wrong file, hallucinated a convention,
made an unsafe action, or otherwise produced a bad outcome on this repo:

1. Append a row to the table below.
2. Be specific: a date (absolute, not "yesterday"), the harness, what the agent was asked to do,
   what it actually did, the smallest rule or gate that would have prevented it.
3. Avoid blaming the model — describe the **system-level gap** (missing
   instruction, missing hook, ambiguous file, etc.).
4. If 2+ entries describe the same gap, that's a pattern. After 3, open an issue
   tagged `agent-surface` and propose the smallest change (a hook, a sentence in
   a future AGENTS.md, a CI gate) that would have closed it.

## Log

| Date | Harness | Task asked | What the agent did | Smallest gap that would have prevented it |
|---|---|---|---|---|
<!-- Add rows as failures are observed. Example shape (DO NOT include the example
     as a real entry — delete the next row before committing if it's the only one): -->
| YYYY-MM-DD | <harness-name> | <one-line task description> | <what actually happened, with file paths or commit SHAs where useful> | <the smallest hook, rule, or gate that closes this gap; cite W1-W10 where applicable> |

## Promotion path

- **≥3 entries describing the same gap** → open an issue tagged `agent-surface`.
- **Resolved by an instruction** → add the sentence to `AGENTS.md` (when it exists) or a relevant `SKILL.md`; reference the log row in the commit message.
- **Resolved by a gate** → add the hook / CI check; reference the log row in the commit message.
- **Resolved by removing the ambiguity** → fix the underlying code, doc, or path; reference the log row in the commit message.

## See also

<!-- Add pointers to: AGENTS.md (when it exists), the agentification audit doc
     if any, and the project-agentification skill's empirical-warnings.md
     (W1-W10) for the rationale behind this workflow. -->

- <pointer 1>
- <pointer 2>

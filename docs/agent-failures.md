# Agent failure log

Record observed agent failures here. **This is the source-of-truth for any future
hand-curated `AGENTS.md`, `CLAUDE.md`, hook, or new skill** — accrue at least three
entries describing a pattern before scaffolding any of those artifacts (per W1 in
`skills/.experimental/project-agentification/references/empirical-warnings.md`).

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
2. Be specific: a date, the harness, what the agent was asked to do, what it
   actually did, the smallest rule or gate that would have prevented it.
3. Avoid blaming the model — describe the **system-level gap** (missing
   instruction, missing hook, ambiguous file, etc.).
4. If 2+ entries describe the same gap, that's a pattern. After 3, open an issue
   tagged `agent-surface` and propose the smallest change (a hook, a sentence in
   a future AGENTS.md, a CI gate) that would have closed it.

## Log

| Date | Harness | Task asked | What the agent did | Smallest gap that would have prevented it |
|---|---|---|---|---|
| 2026-05-15 | claude-code (`project-agentification` skill, `assess` intent) | Run `just check` to verify all skill static checks pass | Reported "all checks passed" — true for the 2 published skills but silently skipped `skills/.experimental/project-agentification/evals/run-static-checks.sh`. The Justfile glob `skills/*/evals/...` does not match dotfile directories. Two of ten sub-agents flagged this independently. | **Path-based gates must enumerate all three install lanes.** Use explicit globs for `skills/*`, `skills/.experimental/*`, and `.agents/skills/*`, or set `shopt -s dotglob`. New gates: test with one skill in each lane. |
| 2026-05-15 | claude-code (`project-agentification` skill, `assess` intent) | Audit eval coverage across the `skills/` tree | Found three incompatible `trigger-evals.json` schemas in three skills. `dx-heuristics` uses `[{query, should_trigger}]`. `test-heuristics` uses `{skill, queries: [{query, should_activate, expected_route}]}`. `project-agentification` uses `{skill, version, should_match, should_not_match, edge_cases}`. No runner exists because none could handle all three; the files are dead weight. | **Skills share a canonical `trigger-evals.json` schema.** Define it in `AGENTS.md`; enforce via each skill's `run-static-checks.sh`. Schema changes migrate all skills in the same PR. |
| 2026-05-15 | claude-code (`project-agentification` skill, `assess` intent) | Identify eval gaps in the `skills/` tree | `skills/example-minimal/` has no `evals/` directory. A contributor templating from it produces skills that pass `npx skills add --list` but bypass the CI static-check gate (which requires `evals/run-static-checks.sh` to exist). | **`example-minimal` is the template contract.** Anything required of published skills must exist in `example-minimal` — even as a minimal placeholder — so the template-to-skill path can't ship ungated. |
| 2026-05-15 | claude-code (this Stage 0 session, drafting `CODEOWNERS`) | Generate `CODEOWNERS` from each `skill.json`'s `maintainers` field | Could not — `"maintainers": ["justin"]` is an opaque string with no GitHub handle. Had to fall back to `gh repo view` to find the actual owner (`Thulr`). The field appears authoritative for automation but isn't programmatically useful. | **Identity fields in `skill.json` must be resolvable GitHub handles** (`@handle`). Add a regex check to each skill's `run-static-checks.sh`: each `maintainers[]` entry matches `^@[A-Za-z0-9-]+$` or is a `@org/team` slug. |

## Promotion path

- **≥3 entries describing the same gap** → open an issue tagged `agent-surface`.
- **Resolved by an instruction** → add the sentence to `AGENTS.md` (when it exists) or a relevant `SKILL.md`; reference the log row in the commit message.
- **Resolved by a gate** → add the hook / CI check; reference the log row in the commit message.
- **Resolved by removing the ambiguity** → fix the underlying code, doc, or path; reference the log row in the commit message.

## See also

- `docs/agent-readiness-2026-05-15.md` — the audit that motivated creating this log.
- `skills/.experimental/project-agentification/references/empirical-warnings.md` — the W1–W10 don'ts that govern when prose vs. gates vs. evidence-driven scaffolding is the right tool.

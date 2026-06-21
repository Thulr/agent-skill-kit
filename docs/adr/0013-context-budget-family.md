# ADR 0013: A `context` Family for Context-Budget & Agent-Setup Hygiene

**Status:** Accepted (2026-06-21). **Updates** (does not supersede)
[ADR 0012](./0012-interop-family-for-cross-agent-tooling.md): a second pragmatic,
tool-backed family, added alongside its first member `context-budget-audit`.

## Context

The catalog's families each shape or evaluate a *surface*: `heuristics`
(software-surface audit/design pairs), `research`, `discovery`, `ax` (surfaces an
agent acts on), `interop` (driving another agent CLI). `context-budget-audit` —
long used by the maintainer — fits none cleanly. It audits the **per-session
context cost of a local agent setup**: the MCP servers, plugins, skills, slash
commands, and subagents that load into every session. A read-only stdlib engine
inventories each, estimates always-on token cost, scans recent transcripts for
genuine usage evidence (MCP usage from real `mcp__<server>__*` tool calls, not
listings), and gates pruning — skills are copy-validate-removed into a repo;
MCP/plugin config edits are handed back as commands, never executed.

It is not a heuristics software-surface audit; not `interop` (it drives no other
CLI); and while agent-adjacent, it is not an `ax` mirror (`ax` shapes surfaces
*for* an agent; this measures what an agent *loads*). Folding it into `agent-ops`
would conflate runtime observability with local-setup context accounting. The
maintainer chose a dedicated family.

## Decision

Add a sixth catalog family, **`context`** ("Context budget & agent-setup
hygiene"): skills that measure and reclaim the per-session context an agent's
local setup consumes. `context-budget-audit` is its charter member,
`function: singleton` (it is an `-audit` by name but has no design counterpart, so
it carries no `*(audit)*` pair tag).

Same three sources of truth as ADR 0012: `scripts/catalog_taxonomy.py` `FAMILIES`,
`schemas/skill.schema.json` `metadata.family.enum`, and `catalog/catalog.json`
(family prose + a Pick-a-skill row). `build-catalog.py --write` regenerates the
README; `--check` (in `just check` / CI) keeps it in sync.

## Consequences

- Two families now group by *what you do with the skill* rather than the surface
  it reasons about: `interop` (drive another agent CLI) and `context` (audit your
  agent's context footprint). This continues the deliberate broadening toward the
  `mattpocock/skills` model noted in ADR 0012.
- `context-budget-audit` ships the full published-skill contract. Its
  `run-static-checks.sh` ports the skill's own eval-suite static checks — they
  exercise the read-only stdlib engine against throwaway `--home` dirs (empty-home
  schema, `--only` kind filtering, block-scalar frontmatter parsing,
  no-write-by-default), so the gate verifies the engine, not just file existence.
  Its SKILL.md word cap is raised to 1500 (operational density; splitting to hit
  1200 would be the unenforced-cap restructuring anti-pattern).
- Risk: another single-member family (W1 "scaffolding ahead of evidence").
  Mitigation: the member exists and is used heavily; the family is named for an
  observed kind of work. Unlike `interop` (which reached three members), `context`
  is deliberately singular for now — revisit if a second context/cost skill lands,
  or fold it elsewhere if none does.

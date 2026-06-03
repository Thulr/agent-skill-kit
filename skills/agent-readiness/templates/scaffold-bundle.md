# Scaffold Bundle — <scope-name>

**Date:** <YYYY-MM-DD>
**Surfaces in scope:** <e.g., instruction-surface, skills, gates>
**Mode:** preview-then-write (per-file confirmation required)

## Project knowledge driving this scaffold

> **Required.** The skill refuses to generate any file from boilerplate. (Empirical warning W9: `/init` and equivalents produce surface-plausible scaffolds with low fitness.) Content must be specific to this project.

- **Tech stack:** <languages, frameworks, runtimes>
- **Repo layout / scope:** <which directories, monorepo vs single-package>
- **Build / test / lint:** <exact commands and their behavior>
- **Top invariants:** <constraints the scaffold must respect>

> **If this project also runs an evidence-driven feedback loop** (reflection log via `agent-rules`), list any patterns already promoted into rules below. Otherwise this section is empty.

- <promoted-pattern 1 — optional>
- <promoted-pattern 2 — optional>

## Harness inventory (step 4.5)

> **Required for `instruction-surface` and `gates` surfaces.** Names every harness in use on this repo so the scaffold produces per-harness equivalents — not just the one whose dotfile happens to exist. Filesystem signals tell you which harnesses are *known*, not which are *all in use*.

- Claude Code: <yes | no | unknown>
- Cursor: <yes | no | unknown>
- Codex: <yes | no | unknown>
- Copilot: <yes | no | unknown>
- Aider: <yes | no | unknown>
- Windsurf: <yes | no | unknown>
- AGENTS.md-compatible only (Jules, Amp, etc.): <yes | no | unknown>

## Proposed files

> **Template column required.** Every proposed file should cite a starting
> template from `templates/artifacts/<surface>/` (see `templates/artifacts/README.md`).
> If no template fits, name that explicitly in the row — the post-write
> auditor (step 8.5) treats "no template cited" as a shape-compliance miss
> unless the writer states why no template applies.

| Path | Action | Failure closed | Severity | Template | Preview |
|---|---|---|---|---|---|
| <path/AGENTS.md> | create | <failure-id> | <severity> | `templates/artifacts/instruction-surface/AGENTS.md` | <expand below> |
<!-- Reflection-log scaffolding is the job of `agent-rules`, not this skill. Only list reflection-log files here if the user is running both skills and EDAR's `capture` workflow is producing them. -->
| <path/.claude/hooks/<hook>.py> | create | <failure-id> | <severity> | `templates/artifacts/gates/pretooluse-hook.py` | <expand below> |
| <path/.claude/hooks/test_<hook>.py> | create | <failure-id> | <severity> | `templates/artifacts/gates/pretooluse-hook-test.py` | <expand below> |

## File previews

### `<path/AGENTS.md>`

<full content preview — note: NEVER ship boilerplate. Every section in the file must trace to a failure listed above.>

```markdown
<contents>
```

### `<path/.claude/skills/foo/SKILL.md>`

<full content preview>

```markdown
<contents>
```

### `<path/.github/hooks/pretooluse-no-force-push.sh>`

<full content preview>

```bash
<contents>
```

## Confirmation gate

Reply one of:

- **`all`** — write all proposed files.
- **`none`** — write nothing; abort.
- **`<comma-separated paths>`** — write only the listed files.

If any proposed file already exists, the skill will refuse to overwrite without explicit `--overwrite` per path.

## Post-write summary (filled after confirmation)

- **Written:** <paths>
- **Skipped:** <paths>
- **Conflicts:** <paths and reasons>

## Post-write audit (step 8.5)

> **Required.** A fresh-context auditor sub-agent (see `references/lenses.md` §Post-write auditor) inspects the diff against the chosen playbook(s) and classifies every `harden` heuristic. Severity 3+ `miss` entries surface to the user as must-do before the scaffold is considered done. **Self-attestation is not allowed** — the auditor must be dispatched separately and its findings included verbatim.

| Playbook | Heuristic | Classification | Evidence | Severity |
|---|---|---|---|---|
| instruction-surface | H2-harden (CLAUDE.md symlink) | applied | `CLAUDE.md -> AGENTS.md` (new file) | 0 |
| instruction-surface | H3-harden ("trust these instructions") | miss | not in AGENTS.md diff | 3 |
| <playbook> | <heuristic-id> | applied \| skipped-because-X \| deferred \| miss | <file:line or reason> | <0-4> |

**Unapplied harden heuristics requiring user action:**

- <severity-3+ miss 1 with proposed resolution>
- <severity-3+ miss 2 with proposed resolution>

If the table above lists any `miss` at severity 3+, the scaffold is **not done**. Either resolve the miss, reclassify it as `skipped-because-X` (with explicit reason; "not relevant" is not a reason), or `deferred` (with a tracked follow-up).

## Validation

After writing, run:

- <test that proves each scaffolded artifact works (e.g., "trigger an agent session and verify AGENTS.md is loaded by checking the trace metadata"). Add an eval case to `evals/` so the failure can't recur silently.>

## Empirical warnings invoked

W2 (AGENTS.md ≤200 lines), W3 (hard gates over soft prose), W9 (no autogenerated content; author by hand against project knowledge), and any others triggered by the specific scaffold.

## Sources cited

(list of skill.json `inspired_by` entries)

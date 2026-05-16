# AGENTS.md — informed-skills

A catalog of [Agent Skills](https://agentskills.io) grounded in cited literature.
The published skills here ARE the product; downstream consumers install them via
`npx skills add Thulr/informed-skills`. Treat every PR to `skills/`, `.agents/`, or
`.github/` as a release artifact, not internal scaffolding.

This file is hand-curated from observed agent failures recorded in
[`docs/agent-failures.md`](./docs/agent-failures.md). Do **not** autogenerate it
(`/init`, `/Generate Cursor Rules`, etc. — see W1 in the project-agentification
empirical-warnings doc). Every load-bearing rule below traces back to a log entry
or a recurring real failure; if you want to add a rule, log the failure first.

## Layout

See [README.md §Layout](./README.md#layout) for the canonical table. The three
install lanes that any path-based gate **must** enumerate:

- `skills/<name>/` — published skills
- `skills/.experimental/<name>/` — caveat-heavy / WIP skills (still discoverable by `npx skills`)
- `.agents/skills/<name>/` — repo-local agent surface (skill-curator, skill-reviewer)

## Commands

- `just check` — runs `npx skills add . --list` plus every `evals/run-static-checks.sh`
  across all three install lanes. **Must pass before commit and before PR.**
- `just test` — alias for `just check` today; reserved for future per-skill tests.
- `npx skills add . --list` — lists installable skills locally; same call CI uses.

CI runs `just check` equivalents on every PR; see [`.github/workflows/ci.yml`](./.github/workflows/ci.yml).

## Per-skill required artifacts

Every skill under `skills/` or `skills/.experimental/` must ship:

- `SKILL.md` with YAML frontmatter (`name`, `description`, `license`) — under 800 words.
- `skill.json` with `name`, `status` (`draft|reviewed|published`), `maintainers`
  (resolvable GitHub handles, see Rule 4), and a non-empty `inspired_by` list.
- `evals/run-static-checks.sh` — exits 0 on success; runs in `just check` and CI.
- `evals/trigger-evals.json` — canonical schema below.
- `evals/activation-cases.md` — natural-language behavioral cases (positive, negative, boundary).

`skills/example-minimal/` is the **template contract**: anything required of
published skills must exist there too, even as a minimal placeholder. The current
`example-minimal/` violates this (see log entry 3); fixing it is open work.

## Canonical `trigger-evals.json` schema

All skills use this shape. Migrate, don't fork:

```json
{
  "skill": "<skill-name, must match directory>",
  "version": "0.1.0",
  "queries": [
    {
      "query": "<natural-language prompt>",
      "should_activate": true,
      "expected_route": "<route-id or null>",
      "category": "positive"
    },
    {
      "query": "<unrelated prompt>",
      "should_activate": false,
      "expected_route": null,
      "category": "negative"
    }
  ]
}
```

`category` is `"positive" | "negative" | "edge"`. `expected_route` is optional
(use `null` when the skill is single-route). Each skill's
`run-static-checks.sh` validates the shape; a runner that grades activation
against a model lives in a future Stage 1.5 — file is parsed and validated for
now, not yet executed.

## Load-bearing rules

Each rule traces back to a log entry in `docs/agent-failures.md`:

### Rule 1 — Path-based gates enumerate every install lane (log entry 1)
Any glob, CI matrix, ignore pattern, or hook that operates on skills MUST
cover `skills/*`, `skills/.experimental/*`, and `.agents/skills/*`.
The Justfile glob silently skipping `.experimental/` for weeks is the
canonical example. When adding a gate, verify it picks up at least one skill
in each lane.

### Rule 2 — Cross-skill schema parity (log entry 2)
Skills share canonical schemas for `skill.json`, `trigger-evals.json`, and
`evals/activation-cases.md`. When a schema changes, migrate every skill in
the same PR. Static checks in each skill's `run-static-checks.sh` enforce
the shape; do not let "I'll migrate the others later" land.

### Rule 3 — `example-minimal` is the template contract (log entry 3)
Whatever published skills are required to have, `example-minimal` must
have too — even as an empty placeholder. New contributors copy from
`example-minimal`; if it skips a gate, every skill templated from it skips
that gate.

### Rule 4 — Identity fields are resolvable handles (log entry 4)
`skill.json` `maintainers` (and any future `contributors`) entries match
`^@[A-Za-z0-9-]+$` or `^@[A-Za-z0-9-]+/[A-Za-z0-9-]+$` (GitHub teams). Opaque
strings like `"justin"` are static-check failures: they cannot be resolved
to a reviewer for CODEOWNERS or branch-protection automation.

## Failure-log workflow

When an agent (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider) trips on
this repo:

1. Append a row to [`docs/agent-failures.md`](./docs/agent-failures.md) — date,
   harness, task, what happened, smallest gap.
2. **Three or more entries describing the same gap** = pattern. Open an issue
   tagged `agent-surface` and propose the smallest change (rule here, hook,
   CI gate, or skill edit) that closes it.
3. Reference the log row in the commit message that closes the gap.

The three-entry floor is W1 (LogicStar/ETH Mündler et al., Feb 2026): scaffolding
from fewer than three observed failures produces plausible boilerplate that hurts
agent success ~3% on average.

## Forbidden actions (hook-enforced)

The PreToolUse hook at [`.claude/hooks/block-destructive-bash.py`](./.claude/hooks/block-destructive-bash.py)
rejects, with non-zero exit:

- `git push --force` / `-f` / `--force-with-lease` targeting `main` or `master`
- `git branch -D main` / `git branch -D master`
- `rm -rf /` and `rm -rf` of protected dirs (`/bin`, `/etc`, `/usr`, `/var`, `/home`, `/System`, `/Users`)
- `rm -rf ~` / `rm -rf $HOME`

The hook is claude-code-specific (`.claude/settings.json`). Cursor, Codex,
Copilot, etc. should configure equivalents from this list. If a blocked
command is genuinely intended (e.g., maintenance from outside an agent
session), run it manually in a terminal — not via the agent.

## Ownership and review

- [`.github/CODEOWNERS`](./.github/CODEOWNERS) — required reviewers on
  `skills/**`, `.agents/**`, `.github/**`, `Justfile`, `README.md`.
- Branch protection on `main` requires the `static-checks` CI status check + at
  least one approving review from a code owner. Self-merges are blocked.

## Security

[`SECURITY.md`](./SECURITY.md) — incident-disclosure path. Skill files load into
downstream agent sessions; treat skill PRs at production-code review depth
(W5: AGENTS.md / SKILL.md / hooks are an injection surface).

## See also

- [`docs/agent-readiness-2026-05-15.md`](./docs/agent-readiness-2026-05-15.md) —
  current maturity assessment (Level 1 across all layers; Stage 0 closed, Stage 1
  in progress).
- [`docs/agent-failures.md`](./docs/agent-failures.md) — the log every change to
  this file must trace back to.
- [`skills/.experimental/project-agentification/references/empirical-warnings.md`](./skills/.experimental/project-agentification/references/empirical-warnings.md)
  — W1–W10 don'ts that govern when prose vs gates vs evidence-driven scaffolding
  is the right tool.

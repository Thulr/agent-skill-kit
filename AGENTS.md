# AGENTS.md — informed-skills

A catalog of [Agent Skills](https://agentskills.io) grounded in cited literature.
The published skills here ARE the product; downstream consumers install them via
`npx skills add Thulr/informed-skills`. Treat every PR to `skills/`, `.agents/`, or
`.github/` as a release artifact, not internal scaffolding.

This file is hand-curated from observed agent failures recorded in
[`docs/reflection-log/`](./docs/reflection-log/) (one file per failure;
indexed by `docs/reflection-log/README.md`). Do **not** autogenerate it
(`/init`, `/Generate Cursor Rules`, etc. — see W1 in the project-agentification
empirical-warnings doc). Every load-bearing rule below traces back to a
reflection-log entry or a recurring real failure; if you want to add a rule,
log the failure first.

Trust and follow these instructions; don't re-explore repo layout/commands if they're already spelled out here.

> **`CLAUDE.md` and `.github/copilot-instructions.md` are symlinks to this file.**
> They exist so Claude Code and Copilot pick up the same hand-curated instructions
> as any AGENTS.md-aware harness (Codex, Cursor, Aider, Windsurf). Edit `AGENTS.md`
> only — the symlinks update automatically. `scripts/check-instruction-surface.sh`
> (run in `just check` and CI) fails the build if either symlink is missing or
> divergent. Pattern from `vercel/next.js`; W8 in the project-agentification
> empirical-warnings doc covers the drift risk.

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
published skills must exist there too, even as a minimal placeholder.

## Canonical `trigger-evals.json` schema

The authoritative shape lives in [`schemas/trigger-evals.schema.json`](./schemas/trigger-evals.schema.json);
the example below is a human-readable summary. Static checks validate against
the schema file, not against the example.

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

Each rule traces back to a reflection-log entry in `docs/reflection-log/`:

### Rule 1 — Path-based gates enumerate every install lane (`docs/reflection-log/2026-05-15-justfile-glob-missed-dotfile-lane.md`)
Any glob, CI matrix, ignore pattern, or hook that operates on skills MUST
cover `skills/*`, `skills/.experimental/*`, and `.agents/skills/*`.
The Justfile glob silently skipping `.experimental/` for weeks is the
canonical example. When adding a gate, verify it picks up at least one skill
in each lane.

### Rule 2 — Cross-skill schema parity (`docs/reflection-log/2026-05-15-trigger-evals-schema-drift.md`)
Canonical schemas for `skill.json` and `evals/trigger-evals.json` live under
[`schemas/`](./schemas/) as JSON Schema files. Every skill's
`run-static-checks.sh` validates against them via
[`scripts/validate-against-schema.py`](./scripts/validate-against-schema.py).
**When a schema changes, edit the schema file (one place) — the static checks
pick it up automatically.** Per-skill `run-static-checks.sh` only carries
assertions that genuinely vary per skill (e.g. `name == <skill-dir>`); do not
reintroduce inline shape validators. Activation-cases markdown is still gated
per-skill until it grows enough structure to schema-validate.

Duplicate-inline-validators landed twice before the extraction: the canonical
`trigger-evals.json` schema documented a `version` field that no validator
checked (caught in PR #5 review), and the maintainer-handle validator was
copy-pasted across four `run-static-checks.sh` scripts (caught in PR #7
review). The second occurrence triggered the extraction to `schemas/`.

### Rule 3 — `example-minimal` is the template contract (`docs/reflection-log/2026-05-15-example-minimal-missing-evals-dir.md`)
Whatever published skills are required to have, `example-minimal` must
have too — even as an empty placeholder. New contributors copy from
`example-minimal`; if it skips a gate, every skill templated from it skips
that gate.

### Rule 4 — Identity fields are resolvable handles (`docs/reflection-log/2026-05-15-codeowners-opaque-maintainer-handle.md`)
`skill.json` `maintainers` (and any future `contributors`) entries match
`^@[A-Za-z0-9-]+$` or `^@[A-Za-z0-9-]+/[A-Za-z0-9-]+$` (GitHub teams). Opaque
strings like `"justin"` are static-check failures: they cannot be resolved
to a reviewer for CODEOWNERS or branch-protection automation.

## Reflection-log workflow

When an agent (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider) trips on
this repo:

1. **Record it.** Copy `docs/reflection-log/_template.md` to
   `docs/reflection-log/YYYY-MM-DD-<slug>.md` and fill it in — frontmatter
   (`date`, `harness`, `sub-surface`, `severity`, `status`, `related`),
   `## What happened`, `## What to do differently`, `## Closed by`.
2. **The recording bar is low.** If you can write a non-trivial
   `## What to do differently` section, the entry is worth recording. One
   observation is enough. Do **not** filter on "is this a class / pattern
   / recurring?" at recording time — that filter belongs at the promotion
   step (below), not here. When in doubt: record.
3. **Promote when there's a pattern.** Three or more entries describing the
   same gap (use `grep -l 'sub-surface: gates' docs/reflection-log/*.md` to
   find them) → open an issue tagged `agent-surface` and propose the smallest
   change (rule here, hook, CI gate, or skill edit) that closes it.
4. Reference the entry filename in the commit message that closes the gap;
   set the entry's `status:` to `resolved` and fill `## Closed by`.

The three-entry promotion floor is W1 (LogicStar/ETH Mündler et al., Feb 2026):
scaffolding from fewer than three observed failures produces plausible
boilerplate that hurts agent success ~3% on average. **W1 gates promotion,
not recording.** A single entry is fine on disk; it is not yet a basis to
hand-curate a rule from.

## Forbidden actions (hook-enforced)

The PreToolUse hook at [`.claude/hooks/block-destructive-bash.py`](./.claude/hooks/block-destructive-bash.py)
rejects, with non-zero exit:

- `git push` to `main` / `master` with **any** force form: `--force` / `-f`
  / `--force-with-lease[=…]` / `--force-if-includes`, **or** a `+`-prefixed
  refspec (`+main`, `+HEAD:main`, `+refs/heads/main`).
- `git branch -D main` / `git branch -D master`.
- `rm -r` (or `-R` / `--recursive`, in any order, separable, with or
  without `-f` / `--force`, with or without `--` terminator) of:
  - `/` itself.
  - Protected top-level system dirs (`/bin`, `/boot`, `/etc`, `/lib`,
    `/opt`, `/sbin`, `/sys`, `/proc`, `/root`, `/run`, `/srv`, `/usr`,
    `/var`, `/home`, `/System`, `/Library`, `/Applications`, `/Users`)
    and anything beneath them.
  - `~` / `$HOME` and anything beneath them.

The hook parses commands argv-by-argv via `shlex` (not regex on the raw
string), splits pipelines on `;` / `&&` / `||` / `|` / `&`, and unwraps
common prefixes (`sudo`, `time`, `env`, `command`, env-var assignments,
`git -C path`). Test coverage lives at
[`.claude/hooks/test_block_destructive_bash.py`](./.claude/hooks/test_block_destructive_bash.py)
(109 unit + 3 subprocess cases) and runs in `just check` and CI. When a
new bypass is observed, log it in `docs/reflection-log/` (one file per
bypass), add the fixture to the test file, then update the hook so the
new case passes.

The hook is claude-code-specific (`.claude/settings.json`). Cursor, Codex,
Copilot, etc. should configure equivalents from this list (see the
per-harness gate-primitives table in
[`skills/.experimental/project-agentification/references/playbooks/gates.md`](./skills/.experimental/project-agentification/references/playbooks/gates.md)).
If a blocked command is genuinely intended (e.g., maintenance from
outside an agent session), run it manually in a terminal — not via the
agent.

## Ownership and review

- [`.github/CODEOWNERS`](./.github/CODEOWNERS) — required reviewers on
  `skills/**`, `.agents/**`, `.github/**`, `Justfile`, `README.md`.
- Branch protection on `main` requires the `static-checks` CI status check
  plus at least one approving review from a code owner. Self-merges are
  blocked at the GitHub layer; confirmed by an attempted `gh pr merge` on
  PR #5 returning `the base branch policy prohibits the merge`. To merge a
  PR you authored, use the GitHub web UI after a code-owner approval —
  `gh pr merge --admin` overrides the policy and should not be used unless
  the change is genuinely a hotfix.

## Security

[`SECURITY.md`](./SECURITY.md) — incident-disclosure path. Skill files load into
downstream agent sessions; treat skill PRs at production-code review depth
(W5: AGENTS.md / SKILL.md / hooks are an injection surface).

## See also

- [`constitution.md`](./constitution.md) — repo charter (purpose + invariants)
- [`docs/adr/`](./docs/adr/) — architectural decisions (the "why")
- [`docs/runbooks/`](./docs/runbooks/) — maintainer procedures (the "how")
- [`docs/reflection-log/`](./docs/reflection-log/) — per-failure entries; evidence base for new rules/gates
- [`docs/agent-readiness-2026-05-15.md`](./docs/agent-readiness-2026-05-15.md) — historical assessment
- [`empirical-warnings.md`](./skills/.experimental/project-agentification/references/empirical-warnings.md) — W1–W10 guardrails

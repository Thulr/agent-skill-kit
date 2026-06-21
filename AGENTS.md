# AGENTS.md — agent-skill-kit

A kit of [Agent Skills](https://agentskills.io) the maintainer actually uses — most
grounded in cited sources, all earned in real coding-agent work; skills worth using
that live elsewhere are linked from the README rather than re-authored. Downstream
consumers install them via `npx skills add justinramos101/agent-skill-kit`. Treat every PR to
`skills/`, `.agents/`, or `.github/` as a release artifact, not internal scaffolding.

This file is hand-curated. Most sections describe project context (stack,
layout, commands, invariants) and trace to project knowledge. Load-bearing
rules in the §Load-bearing rules section trace to observed agent failures
recorded in [`docs/reflection-log/`](./docs/reflection-log/) (this repo
runs the evidence-driven feedback loop — see `rules-from-coding-agent-failures`
— because it's a skill catalog where skill efficacy is the thing under
measurement). Do **not** autogenerate this file
(`/init`, `/Generate Cursor Rules`, etc. — see W9 in
[`empirical-warnings.md`](./skills/_shared/empirical-warnings.md), or W1 in
[`rules-from-coding-agent-failures`](./skills/rules-from-coding-agent-failures/references/empirical-warnings-w1.md)
for the failure-driven floor).

Trust and follow these instructions; don't re-explore repo layout/commands if they're already spelled out here.

> **`CLAUDE.md` and `.github/copilot-instructions.md` are symlinks to this file.**
> They exist so Claude Code and Copilot pick up the same hand-curated instructions
> as any AGENTS.md-aware harness (Codex, Cursor, Aider, Windsurf). Edit `AGENTS.md`
> only — the symlinks update automatically. `scripts/check-instruction-surface.sh`
> (run in `just check` and CI) fails the build if either symlink is missing or
> divergent. Pattern from `vercel/next.js`; W8 in
> [`skills/_shared/empirical-warnings.md`](./skills/_shared/empirical-warnings.md)
> covers the drift risk.

## Layout

See [README.md §Layout](./README.md#layout) for the canonical table. The three
install lanes that any path-based gate **must** enumerate:

- `skills/<name>/` — published skills
- `skills/.experimental/<name>/` — reserved lane; keep empty unless a future
  release explicitly reopens experimental distribution
- `.agents/skills/<name>/` — repo-local agent surface (skill-curator, skill-reviewer)

## Commands

- `just check` — runs install discovery, release-contract checks,
  instruction-surface and shared-content symlink checks, destructive-bash hook
  tests, and every `evals/run-static-checks.sh` across all three install lanes.
  **Must pass before commit and before PR.**
- `just test` — alias for `just check` today; reserved for future per-skill tests.
- `just eval [args]` — model-graded **activation-routing** eval (the "Stage 1.5"
  runner): shows a judge every published skill's `description` and checks which skill
  each `trigger-evals.json` query routes to. **Opt-in, not part of `just check`** — it
  makes live judge calls via [`pi`](https://www.npmjs.com/package/pi) (default provider
  `openai-codex`, i.e. Codex via pi) and is non-deterministic. Scope with
  `just eval --skills a,b`; `--judge mock` runs the pipeline offline. Backed by
  [`scripts/run-trigger-evals.py`](./scripts/run-trigger-evals.py); its logic is covered
  in `just check` by `scripts/test-run-trigger-evals.py` (offline mock backend).
- `just install-hooks` — installs the [`pre-commit`](https://pre-commit.com)
  framework (if missing) and wires the `gitleaks` secret-scanning hook into
  `.git/hooks/pre-commit`. Runs an initial scan against the working tree.
  Optional for contributors; CI runs the same scan unconditionally.
- `bash scripts/list-installable-skills.sh` — lists installable skills locally;
  same pinned `skills` CLI call CI uses.
- `bash scripts/check-shared-content.sh` — verifies every skill symlink into
  `skills/_shared/**` is relative and points to the canonical shared file.
- `python3 scripts/test-trigger-evals-schema.py` — smoke-tests the
  `trigger-evals.json` schema against valid cases and known invalid cases.
- `python3 scripts/validate-against-schema.py <schema> <data>` — validates JSON
  against the canonical schema files under `schemas/`.
- `python3 scripts/build-catalog.py [--check|--write]` — regenerates the README
  §Pick a skill / §Catalog blocks from `skill.json` metadata + `catalog/catalog.json`.
  `--check` (CI / `just check` default) fails if the committed README is stale;
  `--write` rewrites it. **Do not hand-edit the content between the
  `<!-- BEGIN/END GENERATED -->` markers in README.md** — change the source
  (`metadata.catalog_summary` in the relevant `skill.json`, or family prose /
  matrix rows in `catalog/catalog.json`) and run `--write`.

CI runs `just check` equivalents on every PR; see [`.github/workflows/ci.yml`](./.github/workflows/ci.yml).

## Maintainer workflows

- Adding a skill: follow [`docs/runbooks/adding-a-skill.md`](./docs/runbooks/adding-a-skill.md);
  start with `npx skills init <skill-name>` or `skills/example-minimal/`, update
  discovery docs when needed, then run `just check`.
- Changing shared schemas: follow [`docs/runbooks/changing-shared-schemas.md`](./docs/runbooks/changing-shared-schemas.md);
  edit `schemas/`, migrate affected skill files in the same PR, update this file only
  when the human-readable schema summary changes, then run `just check`.
- Changing shared references: keep canonical files in `skills/_shared/`; consumers
  use relative symlinks because `npx skills` dereferences them at install time.

## Per-skill required artifacts

Every skill under `skills/` or `skills/.experimental/` must ship:

- `SKILL.md` with YAML frontmatter (`name`, `description`, `license`). Aim under ~1200
  words, but the binding cap is each skill's `evals/run-static-checks.sh`, which may raise
  or omit it for deliberately complex skills (e.g. `harden-repo-for-coding-agents`). Treat this figure as
  a default, not a uniform hard gate — see
  [`docs/reflection-log/2026-05-28-restructure-split-justified-by-unenforced-cap.md`](./docs/reflection-log/2026-05-28-restructure-split-justified-by-unenforced-cap.md).
- `skill.json` with `name`, `status: "published"` for installable skills,
  `maintainers` (resolvable GitHub handles, see Rule 4), and — **encouraged but no
  longer required** — an `inspired_by` list crediting any cited sources the skill
  draws on (the schema accepts an absent or empty list for skills you use that aren't
  literature-derived). Use repository release tags (for example `0.0.1-alpha`) for
  catalog-level maturity, not per-skill draft status.
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

`category` is `"positive" | "negative" | "edge"`. `expected_route` is required
and uses `null` when the skill is single-route or should not activate. Each skill's
`run-static-checks.sh` validates the **shape** in `just check`. **Activation itself**
— does each query route to the intended skill against the whole catalog's
descriptions — is graded by the opt-in `just eval` runner
([`scripts/run-trigger-evals.py`](./scripts/run-trigger-evals.py)), the realized
"Stage 1.5". It is deliberately *not* in `just check` (live judge calls via `pi`,
non-deterministic); treat its findings as signal, not a hard gate.

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
   same gap (use `grep -l 'sub-surface: gates' docs/reflection-log/[0-9]*.md`
   to find them — the `[0-9]*` glob scopes to dated entry files and excludes
   `README.md` / `_template.md`, which otherwise inflate the count) → open
   an issue tagged `agent-surface` and propose the smallest change (rule
   here, hook, CI gate, or skill edit) that closes it.
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
  refspec (`+main`, `+HEAD:main`, `+refs/heads/main`). Force-push commands
  with omitted/ambiguous refspecs are blocked too because Git can default to
  the current protected upstream branch.
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
string), splits pipelines and grouped commands on `;` / `&&` / `||` / `|` /
`&` / `(` / `)` / `{` / `}`, and unwraps common prefixes (`sudo`, `time`,
`env`, `command`, env-var assignments, `git -C path`). Test coverage lives at
[`.claude/hooks/test_block_destructive_bash.py`](./.claude/hooks/test_block_destructive_bash.py)
and [`.codex/hooks/test_block_destructive_bash.py`](./.codex/hooks/test_block_destructive_bash.py)
(115 unit + 6 subprocess cases each) and runs in `just check` and CI. When
a new bypass is observed, log it in `docs/reflection-log/` (one file per
bypass), add the fixture to both test files, then update the hook so the
new case passes.

**Harness coverage.** The shared policy at
[`scripts/hooks/destructive_bash_policy.py`](./scripts/hooks/destructive_bash_policy.py)
is harness-agnostic; thin per-harness adapters under `.claude/hooks/`,
`.codex/hooks/`, and `.cursor/hooks/` load it. Wired up:

- **Claude Code** — `.claude/settings.json` → PreToolUse on `Bash` →
  `python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/block-destructive-bash.py"`.
  `$CLAUDE_PROJECT_DIR`-prefixing is load-bearing: the hook command is
  invoked with the persisted shell CWD, so a relative path
  (`.claude/hooks/…`) breaks the moment the agent `cd`s into a subdir
  and Python can no longer find the hook script.
- **Codex** — `.codex/hooks.json` → PreToolUse on `Bash` →
  `python3 "$(git rev-parse --show-toplevel)/.codex/hooks/block-destructive-bash.py"`.
  Codex does not document a project-dir env var; the git-root expansion is
  OpenAI's recommended pattern. The project `.codex/` layer must be
  trusted on first run (`/hooks` command in Codex CLI).
- **Cursor** — `.cursor/hooks.json` → preToolUse on `Shell` →
  `python3 "$CURSOR_PROJECT_DIR/.cursor/hooks/block-destructive-bash.py"`
  with `"failClosed": true`. Cursor's shell-tool name is `Shell` (not
  `Bash`); the shared policy recognizes both.
- **Copilot / Aider / Windsurf / AGENTS.md-only harnesses** — no native
  PreToolUse-equivalent. CI branch protection is the load-bearing gate
  for these. See the per-harness gate-primitives table in
  [`skills/harden-repo-for-coding-agents/references/playbooks/gates.md`](./skills/harden-repo-for-coding-agents/references/playbooks/gates.md).

If a blocked command is genuinely intended (e.g., maintenance from
outside an agent session), run it manually in a terminal — not via the
agent.

## Secret scanning

[`gitleaks`](https://github.com/gitleaks/gitleaks) v8.30.1 scans for committed
credentials, API keys, and other high-entropy secrets using the upstream default
ruleset, extended via [`.gitleaks.toml`](./.gitleaks.toml).

- **CI gate.** The `Scan for secrets (gitleaks)` step in the `static-checks`
  job runs `gitleaks detect` over the full git history on every PR and push
  to `main` (requires `fetch-depth: 0` on the checkout). The binary is
  downloaded from the pinned upstream release and verified against the
  published SHA256 before it runs. A finding is a hard fail and blocks
  merge.
- **Local pre-commit.** `just install-hooks` installs the
  [`pre-commit`](https://pre-commit.com) framework and wires up the gitleaks
  hook (config: [`.pre-commit-config.yaml`](./.pre-commit-config.yaml)) so
  leaks are caught before commit. Optional but recommended — the CI gate is
  the load-bearing safety net for contributors who skip it.
- **False positives.** Add an `[[allowlists]]` block in `.gitleaks.toml`
  with `paths`, `regexes`, `stopwords`, or `commits`, and reference the
  path/PR that needed the exception. Never allowlist a pattern "just in
  case" — each entry silently disables real coverage.
- **Bumping the pin.** The version is pinned in two places:
  [`.pre-commit-config.yaml`](./.pre-commit-config.yaml) (`rev:`) and
  [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) (`version` and
  `expected_sha`). Update both together; run `pre-commit autoupdate` to bump
  the hook locally, then refetch the checksum from the upstream release page
  (`gitleaks_<version>_checksums.txt`) for the CI pin.

## Ownership and review

- [`.github/CODEOWNERS`](./.github/CODEOWNERS) — records the owner of each
  agent-surface path (`skills/**`, `.agents/**`, `.github/**`, `Justfile`,
  `README.md`) for review routing.
- A branch-protection ruleset on `main` (`main protection`) requires the
  `static-checks` CI check to pass and routes every change through a pull
  request; direct pushes, force-pushes, and branch deletion are blocked at the
  GitHub layer. The repo is single-maintainer, so the ruleset does **not**
  require a separate approving review — GitHub won't let you approve your own
  PR, so requiring one would lock the sole maintainer out of merging. Land work
  by opening a PR and merging it (squash or rebase; merge commits are disabled)
  once `static-checks` is green. If a second maintainer joins, add a
  required-review rule so CODEOWNERS approval becomes enforceable.

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
- [`skills/_shared/empirical-warnings.md`](./skills/_shared/empirical-warnings.md) — W2–W10 cross-cutting guardrails
- [`skills/rules-from-coding-agent-failures/references/empirical-warnings-w1.md`](./skills/rules-from-coding-agent-failures/references/empirical-warnings-w1.md) — W1 ≥3 promotion floor (owned by `rules-from-coding-agent-failures`)

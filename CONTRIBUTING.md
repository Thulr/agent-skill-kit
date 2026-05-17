# Contributing to informed-skills

Quick orientation for human contributors and AI agents (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider). For deeper agent guidance see [`AGENTS.md`](./AGENTS.md); for repo invariants see [`constitution.md`](./constitution.md).

## Before you start

- Read [`AGENTS.md`](./AGENTS.md) — the load-bearing rules for skill PRs.
- Skim [`constitution.md`](./constitution.md) — the repo's purpose and invariants.
- If you're proposing a new skill, the curator workflow at [`.agents/skills/skill-curator/SKILL.md`](./.agents/skills/skill-curator/SKILL.md) is the canonical path.

## Workflow

1. Fork or branch from `main`.
2. Make changes; keep PRs focused (one skill or one concern per PR).
3. Run `just check` locally before pushing — it runs the same gates CI runs.
4. Open a PR; the PR title and every commit will be linted (see below).
5. Address review comments. CI must be green to merge.

## Commit conventions

This repo enforces [Conventional Commits](https://www.conventionalcommits.org/) on **both** individual commits and PR titles. The PR-title check is load-bearing because squash-merge uses the PR title as the merge-commit message.

### Format

```
<type>[(<scope>)][!]: <subject>
```

### Allowed types

`build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`

### Allowed scopes (optional)

| Group | Scopes |
|-------|--------|
| Skills | `clean-architecture`, `dx-heuristics`, `test-heuristics`, `project-agentification`, `example-minimal` |
| Repo | `schemas`, `scripts`, `hooks`, `repo`, `ci`, `deps` |

Adding a new scope means editing **all four** places it's listed: [`commitlint.config.cjs`](./commitlint.config.cjs), [`.githooks/commit-msg`](./.githooks/commit-msg), the `pr-title` job in [`.github/workflows/ci.yml`](./.github/workflows/ci.yml), and this file. The commit-msg hook's error message reminds you.

### Examples

```
feat(clean-architecture): add new playbook
fix(dx-heuristics): correct DTO heuristic wording
docs(repo): list clean-architecture in README
ci: pin commitlint action to SHA
chore(scripts): bump schema-validator deps
feat(dx-heuristics)!: rename intent CSV columns
```

The trailing `!` marks a breaking change.

### Local hook (recommended)

CI rejects bad commits on push, but catching them at `git commit` time is faster:

```bash
bash scripts/install-hooks.sh
```

This sets `core.hooksPath` to `.githooks/`. The `commit-msg` hook then validates the same format commitlint uses, with no Node dependency. Merge, revert, and fixup commits are skipped automatically.

## Working with AI coding agents

This repo is curated to be agent-friendly. The most common surfaces and their commit-message behavior:

### IDE / Chat surfaces (Claude Code, GitHub Copilot Chat, Cursor, Codex, Windsurf, Aider)

These read [`AGENTS.md`](./AGENTS.md) (and the [`.github/copilot-instructions.md`](./.github/copilot-instructions.md) + [`CLAUDE.md`](./CLAUDE.md) symlinks) for repo-specific guidance, including the Commit conventions section. Agents writing commits in these surfaces should follow the format above. If you observe an agent producing non-conforming messages, log it in [`docs/agent-failures.md`](./docs/agent-failures.md).

### GitHub Code Scanning Autofix ("Commit suggested changes" button)

GitHub's Autofix flow hardcodes the subject `Potential fix for pull request finding`; **no instructions file can override it**. If you accept an Autofix suggestion, either:

- **Recommended:** pull the branch locally, apply the suggested change yourself, and commit with a proper Conventional Commits message.
- **Acceptable for trivial fixes:** use the in-UI button, then immediately rebase + reword the commit before pushing (`git rebase -i`, change `pick` to `reword`).

PR #10 ([clean-up after CC enforcement landed](https://github.com/Thulr/informed-skills/pull/10)) is the canonical example of the second path applied retroactively.

### Squash-merge as a safety net

If non-conforming commits land mid-PR despite the hook, the PR-title check ensures the squash-merge commit (which is what lands on `main`) is still CC-conforming. This means a clean `main` history is recoverable even when individual PR commits drift. Prefer squash-merge by default in this repo.

## Failure log

When an agent (or a human contributor) trips on this repo in a way that wasn't obvious from the docs, append a row to [`docs/agent-failures.md`](./docs/agent-failures.md). Three entries describing the same gap is the threshold for adding a new rule, hook, or `AGENTS.md` sentence to close it.

## License

By contributing, you agree your contributions are licensed under the repo's [LICENSE](./LICENSE). Individual skills may declare different terms; third-party notices live in [THIRD_PARTY.md](./THIRD_PARTY.md).

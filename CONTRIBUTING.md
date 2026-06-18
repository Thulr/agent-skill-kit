# Contributing

Thanks for improving agent-skill-kit. The published skills under `skills/` **are**
the product, so any change to `skills/`, `.agents/`, or `.github/` is a release
artifact — treat it at production-review depth.

Start with [`AGENTS.md`](./AGENTS.md): stack, layout, commands, invariants, and
the load-bearing rules. It's the single source of truth for working in this repo.

## Add or change a skill

- **New skill:** `npx skills init <name>` (or copy `skills/example-minimal/`, the
  template contract), move it under `skills/`, then follow
  [`docs/runbooks/adding-a-skill.md`](./docs/runbooks/adding-a-skill.md).
- **Required artifacts** (per skill): `SKILL.md` with YAML frontmatter (`name`,
  `description`, `license`), a `skill.json` with `status: "published"` for
  installable skills, and `evals/` — `run-static-checks.sh`, `trigger-evals.json`,
  `activation-cases.md`. The full contract is in `AGENTS.md` §Per-skill required
  artifacts.
- **Shared schemas / references:** see the runbooks in
  [`docs/runbooks/`](./docs/runbooks/). Keep `skills/.experimental/` empty unless
  a release explicitly reopens experimental distribution.
- Prerelease caveats belong to the repository release tag (e.g. `0.0.1-alpha`),
  not to per-skill draft status.

## Validate before every commit and PR

```bash
just check
```

Runs install discovery, the release-contract + schema checks, instruction-surface
and shared-content symlink checks, the destructive-bash hook tests, and every
skill's `evals/run-static-checks.sh` across all three install lanes. **It must
pass before commit and before opening a PR;** CI runs the same gates on `main`.

## When an agent trips on this repo

Record it in [`docs/reflection-log/`](./docs/reflection-log/): copy `_template.md`
to `YYYY-MM-DD-<slug>.md` and fill it in. **The recording bar is low** — if you
can write a non-trivial "What to do differently", log it. Three entries on the
same gap is the threshold for *promoting* it into a rule / hook / gate, not for
recording. See [`docs/reflection-log/README.md`](./docs/reflection-log/README.md).

## Install a local checkout while developing

```bash
npx --yes skills add . --skill <skill-name> --agent cline --global --copy -y
```

## Ownership

Required reviewers and branch protection live in
[`.github/CODEOWNERS`](./.github/CODEOWNERS); `main` requires the `static-checks`
status check plus a code-owner approval.

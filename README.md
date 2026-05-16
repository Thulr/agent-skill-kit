<p align="center">
  <img src="./docs/informed-skills.png" alt="informed-skills — Agent Skills distilled from books and papers" width="800">
</p>

# informed-skills

**[Agent Skills](https://agentskills.io) with citations.** An *informed heuristic* uses domain knowledge to estimate more accurately than a blind rule of thumb — every skill here cites the books, papers, and research it's grounded in, so you can check the work. Installable with the open ecosystem CLI ([skills.sh](https://skills.sh)).

```bash
npx skills add Thulr/informed-skills
```

[skills.sh](https://skills.sh) will prompt you to pick which skills to install. Per-skill install commands below; full options under [Install](#install).

## Skills

### dx-heuristics

Practical developer-experience review, design, debugging, and edge-case pass for any surface a developer has to install, call, debug, extend, test, or maintain — APIs, SDKs, CLIs, docs, errors, setup, inner-loop, migrations, contracts, contributor flows, auth, IDE integration, plugins, performance, and telemetry.

Grounded in canonical DX/UX literature (Norman's *Design of Everyday Things*, Nielsen's heuristics, Bloch's *How to Design a Good API*, and more — full provenance in [`skills/dx-heuristics/skill.json`](./skills/dx-heuristics/skill.json)). Routes by intent (`audit` / `design` / `debug` / `edge-pass`) and surface, then dispatches three parallel reviewer lenses (first-time integrator, maintainer, adversarial debugger) so feedback isn't single-perspective.

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill dx-heuristics
```

### test-heuristics

Practical test-suite review, design, triage, strategy, and pruning across unit, integration, e2e/UI, exploratory, property-based, contract, snapshot, mutation, and performance tests. Core principle: *a test exists to catch the bugs that ship in this code class — and to be diagnosable when it fails.*

Grounded in canonical testing literature (full provenance in [`skills/test-heuristics/skill.json`](./skills/test-heuristics/skill.json)). Routes by activity (`triage` / `review` / `author` / `strategize` / `prune`) and layer, with the same parallel-lens discipline used by `dx-heuristics`.

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill test-heuristics
```

### project-agentification (experimental)

Assess, harden, scaffold, and diagnose a repository's agent-readiness for AI coding harnesses (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider). Harness-agnostic; portable-first (AGENTS.md, SKILL.md, MCP, OpenTelemetry).

Routes by intent (`assess` / `harden` / `scaffold` / `diagnose`) × sub-surface (10 across 3 layers: legibility / action / control), then dispatches four parallel reviewer lenses (cold-context-agent / maintainer / adversarial / auditor). Grounded in published research and empirical studies (full provenance in [`skills/.experimental/project-agentification/skill.json`](./skills/.experimental/project-agentification/skill.json)).

> **Experimental.** The research domain is moving quickly; expect iteration. Lives under `skills/.experimental/` and is still discovered by `npx skills`.

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill project-agentification
```

## Install

From GitHub:

```bash
npx skills add Thulr/informed-skills
```

Install specific skills or target agents:

```bash
npx skills add Thulr/informed-skills --list
npx skills add Thulr/informed-skills --skill dx-heuristics --skill other-skill
npx skills add Thulr/informed-skills -a claude-code -a cursor -y
```

From a subdirectory URL (single skill):

```bash
npx skills add https://github.com/Thulr/informed-skills/tree/main/skills/dx-heuristics
```

Local checkout:

```bash
git clone https://github.com/Thulr/informed-skills.git
cd informed-skills
npx skills add . --list
npx skills add .
```

Use `-g` / `--global` for user-wide installs; default is project scope. See `npx skills --help`.

## Layout

| Path | Purpose |
|------|---------|
| `constitution.md` | Repo charter: purpose, non-goals, and invariants |
| `AGENTS.md` | Hand-curated agent instructions for this repo (also surfaced via `CLAUDE.md` + `.github/copilot-instructions.md` symlinks) |
| `docs/agent-failures.md` | Log of observed agent failures; source-of-truth for future rules/gates |
| `docs/specs/` | Specs/plans for significant work (new skills, schema changes, new gates) |
| `docs/adr/` | Architectural Decision Records (durable “why”) |
| `docs/runbooks/` | Maintainer procedures (durable “how”) |
| `docs/architecture/` | Repo structure reference docs / repo maps |
| `skills/<name>/` | Shareable skills (`SKILL.md` + optional assets) |
| `skills/example-minimal/` | Optional starter you can delete once real skills exist |
| `skills/.experimental/<name>/` | Work-in-progress or caveat-heavy skills (still discovered by `npx skills`) |
| `.agents/skills/<name>/` | Repo-local skills used for authoring and review workflows |
| `THIRD_PARTY.md` | Attribution and licenses for skills not authored here |

Skills marked internal in frontmatter (`metadata.internal: true`) are hidden unless `INSTALL_INTERNAL_SKILLS=1` is set when using the CLI.

## Authoring

Create a new skill template:

```bash
npx skills init my-skill
```

Move the resulting folder under `skills/` or `skills/.experimental/` as appropriate. Each skill needs valid YAML frontmatter with at least `name` and `description`.

Validate the repository before publishing or handing off changes:

```bash
just check
```

When an AI coding agent trips on this repo — wastes tokens, edits the wrong file, hallucinates a convention — record it in [`docs/agent-failures.md`](./docs/agent-failures.md). Three entries describing the same gap is the threshold for adding a rule, hook, or `AGENTS.md` sentence to close it.

## License

See [LICENSE](./LICENSE). Individual skills may declare different terms; third-party notices live in [THIRD_PARTY.md](./THIRD_PARTY.md).

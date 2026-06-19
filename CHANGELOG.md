# Changelog

Notable changes to the agent-skill-kit catalog. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); catalog maturity is
tracked by repository release tags (e.g. `0.0.1-alpha`), not per-skill status.

## [Unreleased]

### Added
- **The agent-mirror family — agent-facing work reorganized by *actor* (ADR-0011).** Five new
  skills, each the agent-actor analog of a human-experience domain, routing do/review/design:
  `agent-dx` (agent as developer — SDK/tool/error/telemetry), `agent-docs` (reader — AGENTS.md,
  llms.txt, tool descriptions, machine-readable reference), `agent-ux` (end-user — agent-operable
  UI / computer-use), `agent-ops` (operator + the family front-door — observability,
  trace-and-eval loops, autonomy, reliability), and `agent-test` (subject under measurement —
  evals, LLM-judges, benchmarks, activation tests).
  (See [ADR 0011](./docs/adr/0011-actor-axis-agent-mirror-family.md).)

### Removed
- **Retired the `design-for-agent-users` umbrella and `agent-evals`**, decomposing them into the
  agent-mirror family above: `design-for-agent-users` → `agent-dx` + `agent-docs` + `agent-ux` +
  `agent-ops`; `agent-evals` → `agent-test` (eval/judge/benchmark design) + `agent-ops` (loop
  operation, observability, autonomy, maturity). `harden-repo-for-coding-agents` and
  `rules-from-coding-agent-failures` stay standalone as arms `agent-ops` routes out to. The
  `--skill design-for-agent-users` and `--skill agent-evals` install commands no longer resolve;
  inbound references across the catalog were repointed to the successors. Supersedes ADR-0007's
  audience-peer model with an actor × role grid.

### Changed
- **Renamed the project `informed-skills` → `agent-skill-kit`** and reframed it from a
  cited-literature catalog to a personal kit of the skills the maintainer uses (with README
  links to other useful skills rather than re-authoring them). The install command is now
  `npx skills add Thulr/agent-skill-kit`; the old `Thulr/informed-skills` path stops resolving
  once the GitHub repo is renamed. The per-skill `inspired_by` requirement is **lightened from
  required to encouraged** (cited grounding is no longer a hard schema gate). Renamed the
  repo-local authoring skills `informed-skill-curator` → `skill-curator` and
  `informed-skill-reviewer` → `skill-reviewer`.
  (See [ADR 0010](./docs/adr/0010-rename-to-agent-skill-kit.md).)
- **Replaced the clean-architecture audit/design pair with one `minimal-modular-code` skill.**
  Added `minimal-modular-code` — a single skill (intents **DO** keep an in-progress change
  minimal, **REVIEW** audit existing code or a repo for slop and parallel-readiness, **DESIGN**
  shape right-sized boundaries / sequence a refactor / explain a principle) for writing
  minimal, legible code and structuring a repo so many coding agents can work in parallel. It
  absorbs the dependency-direction, deep-module, and information-hiding heuristics plus the
  audit machinery (severity / score / calibration / tracking) under a minimalism thesis, and
  drops the clean-architecture/DDD maximalism (aggregates, bounded contexts, prescriptive
  ports / hexagon / onion). Finding-ID prefix is `MM-*` (was `CA-*`).
  (See [ADR 0009](./docs/adr/0009-replace-architecture-pair-with-minimal-modular-code.md).)
- **Renamed the agent-facing skills by use case** so each name states the job
  it does: `agent-experience` → `design-for-agent-users`, `agent-readiness` →
  `harden-repo-for-coding-agents`, and `agent-rules` → `rules-from-coding-agent-failures`
  (`agent-evals` unchanged). The old `--skill agent-experience`,
  `--skill agent-readiness`, and `--skill agent-rules` install commands no
  longer resolve — install the new names instead. Emitted audit-artifact
  filename prefixes moved with them (e.g.
  `agent-readiness-findings-ledger-*` → `harden-repo-for-coding-agents-findings-ledger-*`,
  `agent-rules-findings-ledger-*` → `rules-from-coding-agent-failures-findings-ledger-*`).
  Discipline concepts (`agent experience`/AX, the noun "agent-readiness")
  keep their names. Resolves the rename half of finding DX-MA-04. (See the
  rename notes on [ADR 0005–0008](./docs/adr/0006-discipline-front-doors-vs-one-engine-many-surfaces.md)
  and [`docs/runbooks/renaming-or-removing-a-skill.md`](./docs/runbooks/renaming-or-removing-a-skill.md).)
- **Split `review-heuristics` into 12 per-domain × per-function skills:**
  `dx-audit`/`dx-design`, `docs-audit`/`docs-design`,
  `perf-audit`/`perf-design`, `test-audit`/`test-design`, `ux-audit`,
  `ui-design`, and `architecture-audit`/`architecture-design`. An `-audit`
  skill audits/debugs an existing surface; a `-design` skill shapes a new one.
  (See [ADR 0008](./docs/adr/0008-reverse-review-consolidation-split-by-domain-and-function.md).)
- **Named the review half of each pair `-audit`** (not `-critique`), so the
  skill name carries its function in plain software vocabulary:
  `dx-audit`, `docs-audit`, `perf-audit`, `test-audit`, `ux-audit`,
  `architecture-audit`.
- **Grouped the agent-facing family under a shared `agent-` prefix:**
  `agent-experience` (umbrella — design/review software, docs, SDKs, repos so
  AI agents can consume them), `agent-readiness` (assess/harden/scaffold a
  repo's agent-readiness; was `project-agentification`), `agent-rules`
  (promote observed agent failures into rules/gates), and `agent-evals`
  (instrument an AI product's eval/optimization loops).
- CI `static-checks` now runs on a GitHub-hosted runner; the previous
  self-hosted runner had stopped reporting, leaving the required check dead.

### Removed
- **The `architecture-audit` and `architecture-design` skills**, their
  `--skill architecture-audit` / `--skill architecture-design` install commands, and the
  `skills/_shared/architecture/` substrate. Install `minimal-modular-code` instead —
  `npx skills add Thulr/agent-skill-kit --skill minimal-modular-code`. (Replaced under
  [ADR 0009](./docs/adr/0009-replace-architecture-pair-with-minimal-modular-code.md).)
- The `review-heuristics` skill and its `--skill review-heuristics` install
  command. Install the per-domain skills instead — e.g.
  `npx skills add Thulr/agent-skill-kit --skill dx-audit --skill dx-design`.

### Added
- `CHANGELOG.md` (this file) and `CONTRIBUTING.md`.

## [0.0.1-alpha]

- Initial published catalog of source-grounded Agent Skills.

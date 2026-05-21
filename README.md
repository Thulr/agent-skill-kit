<p align="center">
  <img src="./docs/informed-skills.png" alt="informed-skills — Agent Skills distilled from books and papers" width="800">
</p>

# informed-skills

**[Agent Skills](https://agentskills.io) with citations.** An *informed heuristic* uses domain knowledge to estimate more accurately than a blind rule of thumb — every skill here cites the books, papers, and research it's grounded in, so you can check the work. Installable with the open ecosystem CLI ([skills.sh](https://skills.sh)).

```bash
npx skills add Thulr/informed-skills
```

[skills.sh](https://skills.sh) will prompt you to pick which skills to install. Per-skill install commands below; full options under [Install](#install).

The current catalog focuses on software engineering, coding-agent operations,
developer experience, test quality, architecture, and user-facing product UX /
accessibility, and UI design craft. Other source-grounded domains can be added
later, but they are not part of the published install surface today.

## Which skill should I use?

| User need | Skill |
|---|---|
| Developer-facing APIs, SDKs, CLIs, docs, setup, errors, auth, telemetry, or onboarding | `dx-heuristics` |
| Unit/integration/e2e/property/contract/snapshot/mutation/performance test quality | `test-heuristics` |
| User-facing product UX, forms, navigation, checkout/signup friction, WCAG/accessibility basics | `ux-accessibility-heuristics` |
| Visual UI polish, frontend mockups, prototypes, design systems, motion, decks, or handoff | `ui-design-craft` |
| Dependency direction, ports/adapters, DDD, bounded contexts, architecture refactors | `clean-architecture` |
| Make a repo work better with coding agents; assess, harden, scaffold, or diagnose agent-readiness | `project-agentification` |
| Record observed agent failures and promote recurring patterns into rules/gates from evidence | `evidence-driven-agent-rules` |
| "Make our docs better" | Ask whether the audience is humans using the product (`ux-accessibility-heuristics`), developers integrating it (`dx-heuristics`), or coding agents reading the repo (`project-agentification`). |
| "Add a hook" | Ask whether this means a Claude/Codex/Cursor agent gate (`project-agentification`) or a generic Git/build hook. |

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

### ux-accessibility-heuristics

Practical user-facing UX and accessibility review for product interfaces,
forms, navigation, onboarding, checkout/signup flows, error/recovery states,
keyboard access, focus, semantics, contrast, and dark-pattern risk.

Grounded in usability literature and WCAG 2.2 (full provenance in
[`skills/ux-accessibility-heuristics/skill.json`](./skills/ux-accessibility-heuristics/skill.json)).
Routes by use case (`usability-audit` / `accessibility-audit` / `form-review`
/ `navigation-review` / `error-recovery`) and distinguishes likely WCAG issues
from checks that need manual or specialist confirmation.

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill ux-accessibility-heuristics
```

### ui-design-craft

Practical UI design craft for product screens, frontend mockups, prototypes,
design systems, decks, motion/effects, host-integrated artifacts, handoff, and
anti-slop visual review. Use it when the work needs visible design direction or
a runnable artifact, not only a usability/accessibility inspection.

Grounded in project-local design workflow notes plus canonical usability,
accessibility, and design-system sources (full provenance in
[`skills/ui-design-craft/skill.json`](./skills/ui-design-craft/skill.json)).
Routes by use case (`product-ui` / `design-system` / `prototype` / `deck` /
`motion-scene` / `host-handoff` / `quality-review`) and supports guided,
autopilot, or question-heavy design modes.

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill ui-design-craft
```

### clean-architecture

Audit, design, refactor toward, or explain clean-architecture concerns — dependency rule, layered/hexagonal/onion boundaries, DDD tactical and strategic patterns, cross-cutting concerns. Language-agnostic, full-stack-friendly for code architecture; route product UX, forms, navigation, and accessibility to `ux-accessibility-heuristics`.

Routes by intent (`audit` / `design` / `refactor` / `explain`) × surface (`dependency-rule` / `boundaries` / `domain-model` / `bounded-context` / `cross-cutting`); `audit` also supports an `all`-fanout that tries to delegate one agent per surface whenever active user, project, session, or host policy permits parallel sub-agents. Otherwise the same three reviewer lenses run sequentially (dependency-auditor, boundary-designer, refactor-pragmatist) and the host synthesizes them. Grounded in 17 sources spanning Parnas → Cockburn → Palermo → Martin → Evans → Vernon → Fowler → Newman → Khononov → Hohpe & Woolf → Ousterhout + Flux/Elm (full provenance in [`skills/clean-architecture/skill.json`](./skills/clean-architecture/skill.json)).

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill clean-architecture
```

### project-agentification

Assess, harden, scaffold, and diagnose a repository's agent-readiness for AI coding harnesses (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider). Harness-agnostic; portable-first (AGENTS.md, SKILL.md, MCP, OpenTelemetry). **For any repo that wants coding agents to work well in it** — no eval / benchmark / telemetry prerequisites; scaffolds from project knowledge (stack, layout, commands, invariants).

Routes by intent (`assess` / `harden` / `scaffold` / `diagnose`) × sub-surface (10 across 3 layers: legibility / action / control), then dispatches four parallel reviewer lenses (cold-context-agent / maintainer / adversarial / auditor). Grounded in published research (full provenance in [`skills/project-agentification/skill.json`](./skills/project-agentification/skill.json)).

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill project-agentification
```

### evidence-driven-agent-rules

Capture observed agent failures in a per-file reflection log, promote recurring patterns into AGENTS.md rules / hooks / CI gates via the W1 ≥3-entries floor, and score Level 4–5 (Spec Architecture, Sovereign Engineering) maturity. **For teams with a feedback signal** — eval suites, run-level telemetry, A/B baselines, or a skill catalog under test.

Pair with `project-agentification`: that skill scaffolds the project-context-first AGENTS.md any repo can use; this skill layers the evidence-driven workflow on top for the subset of repos where the feedback signal exists. Provenance in [`skills/evidence-driven-agent-rules/skill.json`](./skills/evidence-driven-agent-rules/skill.json).

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill evidence-driven-agent-rules
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
| `docs/reflection-log/` | One file per observed agent failure; source-of-truth for future rules/gates |
| `docs/specs/` | Specs/plans for significant work (new skills, schema changes, new gates) |
| `docs/adr/` | Architectural Decision Records (durable “why”) |
| `docs/runbooks/` | Maintainer procedures (durable “how”) |
| `docs/architecture/` | Repo structure reference docs / repo maps |
| `skills/<name>/` | Shareable skills (`SKILL.md` + optional assets) |
| `skills/example-minimal/` | Template contract (AGENTS.md Rule 3): the minimum artifacts every skill must ship. Hidden from `npx skills add . --list` by `metadata.internal: true`. Do not delete |
| `skills/_shared/` | Cross-skill primitives (e.g. `lenses.md`, `empirical-warnings.md` W2–W10). Each consuming skill symlinks the relevant files; `npx skills` dereferences at install time, shipping self-contained skills. Enforced by `scripts/check-shared-content.sh` |
| `schemas/` | JSON Schemas for `skill.json` and `evals/trigger-evals.json` (single source of truth, validated by every `run-static-checks.sh`) |
| `scripts/` | Repo-wide scripts: instruction-surface symlink check, schema validator |
| `skills/.experimental/<name>/` | Reserved lane kept empty for now; current product skills live in `skills/<name>/`, and prerelease maturity is communicated by repository release tags such as `0.0.1-alpha` |
| `.agents/skills/<name>/` | Repo-local skills used for authoring and review workflows |
| `THIRD_PARTY.md` | Attribution and licenses for skills not authored here |

Skills marked internal in frontmatter (`metadata.internal: true`) are hidden unless `INSTALL_INTERNAL_SKILLS=1` is set when using the CLI.

## Authoring

Create a new skill template:

```bash
npx skills init my-skill
```

Move the resulting folder under `skills/` for product work. Keep `skills/.experimental/` empty unless a future release explicitly reopens experimental distribution. Each skill needs valid YAML frontmatter with at least `name` and `description`.

Installable skills in this repository use `skill.json.status: "published"`; prerelease caveats belong to the repository release tag, not per-skill draft status.

Validate the repository before publishing or handing off changes:

```bash
just check
```

When an AI coding agent trips on this repo — wastes tokens, edits the wrong file, hallucinates a convention — record it in [`docs/reflection-log/`](./docs/reflection-log/) by copying `_template.md` to `YYYY-MM-DD-<slug>.md`. **The recording bar is low**: if you can write a non-trivial `## What to do differently` section, log it. The "three entries describing the same gap" threshold gates *promoting* the pattern into a rule, hook, or `AGENTS.md` sentence — not recording. See [`docs/reflection-log/README.md`](./docs/reflection-log/README.md) for the full workflow.

## License

See [LICENSE](./LICENSE). Individual skills may declare different terms; third-party notices live in [THIRD_PARTY.md](./THIRD_PARTY.md).

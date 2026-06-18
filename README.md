<p align="center">
  <img src="./docs/informed-skills.png" alt="informed-skills — Agent Skills distilled from books and papers" width="800">
</p>

# informed-skills

**[Agent Skills](https://agentskills.io) with citations.** An *informed heuristic* uses domain knowledge to estimate more accurately than a blind rule of thumb — every skill here cites the books, papers, and research it's grounded in, so you can check the work. Installable with the open ecosystem CLI ([skills.sh](https://skills.sh)).

```bash
npx skills add Thulr/informed-skills
```

[skills.sh](https://skills.sh) prompts you to pick which skills to install — see [Install](#install) for options.

**First use.** Skills activate from natural-language prompts — no command to run. Once installed, ask your agent *"audit my CLI's developer experience"* and `dx-audit` kicks in with a severity-scored findings report; *"design our API's error envelope"* routes to `dx-design`; *"is our llms.txt agent-ready?"* to `design-for-agent-users`. Each skill names the cited sources it applied.

The catalog currently covers software engineering and coding-agent work — developer and documentation experience, test quality, architecture, performance and observability, product UX and accessibility, UI craft, and agent experience. Other source-grounded domains may be added later.

<!-- BEGIN GENERATED: pick-a-skill (scripts/build-catalog.py) -->
## Pick a skill

Two questions get you there: **which surface**, and are you **reviewing it** or **building it**?

| Surface | Review it → `-audit` | Build it → `-design` |
|---|---|---|
| **Developer experience** — APIs, SDKs, CLIs, dev docs, setup, errors, auth, packaging, IDE, plugins, telemetry | `dx-audit` | `dx-design` |
| **Documentation** — READMEs, quickstarts, API refs, help centers, OpenAPI/MCP tool contracts | `docs-audit` | `docs-design` |
| **Writing** — memos/PRDs/RFCs, technical & task docs, talks/pitches, narratives, general prose | `writing-audit` | `writing-design` |
| **Performance & observability** — latency, p99/tail, throughput, SLOs, tracing, logs, metrics, capacity | `perf-audit` | `perf-design` |
| **Test suites** — unit/integration/e2e/property/contract/snapshot/mutation, flakiness, pruning | `test-audit` | `test-design` |
| **Product UX & accessibility** — usability, forms, navigation/IA, error/recovery, WCAG | `ux-audit` | → `ui-design` |
| **Visual UI craft** — dashboards, design systems/tokens, prototypes, motion, decks, handoff | → `ux-audit` | `ui-design` |
| **Clean architecture** — dependency rule, layered/hexagonal/onion boundaries, ports/adapters, DDD, bounded contexts | `architecture-audit` | `architecture-design` |

For research, discovery, and agent-facing work:

| Need | Skill |
|---|---|
| **Source-cited research** — an open-ended topic report, or validating a named opportunity to a go/no-go decision | `research` |
| **Talk to customers** — plan, sharpen, run, or synthesize customer discovery interviews | `customer-interviewing` |
| **Build for AI agents** — agent-readable docs (llms.txt, AGENTS.md, MCP), AI/Agent SDK design, repo agent-readiness | `design-for-agent-users` *(umbrella)* |
| ↳ harden a repo for coding agents | `harden-repo-for-coding-agents` |
| ↳ promote observed agent failures into rules / gates | `rules-from-coding-agent-failures` |
| ↳ instrument an AI product's eval / optimization loops | `agent-evals` |

**Still unsure?** The three boundaries people hit most:

- *"Make our docs better"* — audit existing docs → `docs-audit`; reshape docs IA → `docs-design`; API/SDK friction beyond the docs → `dx-audit`; agent-readable docs (llms.txt, retrieval) → `design-for-agent-users`.
- *"Our service is slow" / "design SLOs"* — diagnose a slow or incident-y system → `perf-audit`; design SLOs and instrumentation → `perf-design`; the developer's own machine (local install, cold start) → `dx-audit`.
- *"Improve our agent"* — make a coding-agent harness work in this repo (AGENTS.md, hooks, MCP) → `harden-repo-for-coding-agents`; build an eval loop for an AI product you ship → `agent-evals`.
<!-- END GENERATED: pick-a-skill -->

<!-- BEGIN GENERATED: catalog (scripts/build-catalog.py) -->
## Catalog

What each skill is and what it's grounded in. To route by task use [Pick a skill](#pick-a-skill); to install see [Install](#install).

### Heuristic audit & design pairs

Source-grounded heuristics for software surfaces, split so the name says what it does. A **`-audit`** skill audits, debugs, or risk-scans an *existing* surface (expert lenses → severity-scored findings report, with an optional tracking ledger); a **`-design`** skill shapes a *new* one (names the good-shaped pattern → design doc / plan / runbook). A domain's pair shares its playbooks, lenses, personas, and rubrics via `skills/_shared/<domain>/`, so the two stay in lockstep without drift.

Grounded in 120+ cited sources — Norman, Nielsen, Bloch, Gregg, the Google SRE book, Kleppmann, WCAG 2.2, Martin, Evans, and many more (per-skill provenance in each `skill.json`). These twelve skills replaced the merged `review-heuristics` skill — see [`docs/adr/0008`](./docs/adr/0008-reverse-review-consolidation-split-by-domain-and-function.md).

- **`architecture-audit`** *(audit)* — Audit a codebase for dependency-rule violations, layer/port/adapter boundary leakage, anemic domains, and bounded-context seams; emits severity-scored findings.
- **`architecture-design`** *(design)* — Set the dependency-rule invariant for new work, shape layer/port/adapter boundaries, model entities/aggregates/value objects, carve a bounded context, and sequence a safe refactor.
- **`docs-audit`** *(audit)* — Audit a docs/help/agent-readable surface for friction, drift, accessibility, retrieval, or audience conflict and score it — or debug a concrete docs failure.
- **`docs-design`** *(design)* — Plan or reshape a docs surface before implementation — information architecture, mode taxonomy, README/quickstart/reference structure, examples strategy, and API/tool-contract docs.
- **`dx-audit`** *(audit)* — Audit a developer-experience surface (APIs, SDKs, CLIs, errors, setup, auth, packaging, IDE, plugins, telemetry) for friction and score it, or run a pre-ship edge-case risk pass.
- **`dx-design`** *(design)* — Design a new developer-experience surface from scratch — API, SDK, CLI, error envelope, setup/first-run flow, auth model, migration/deprecation path, plugin contract, or package scheme.
- **`perf-audit`** *(audit)* — Audit a production or runtime system for latency, throughput, saturation, and observability gaps (tracing, logs, metrics) and score the findings.
- **`perf-design`** *(design)* — Design instrumentation, SLOs/error-budget policy, tracing topology, latency budgets, and metric selection up-front for a new or expanding system.
- **`test-audit`** *(audit)* — Review a test suite for smells, redundancy, false-pass risk, brittleness, and flakiness and score it, or triage one failing, flaky, or slow test.
- **`test-design`** *(design)* — Author a new test or test plan, shape a cross-layer test strategy (what to test at which layer), or plan which low-value tests to delete.
- **`ui-design`** *(design)* — Produce or polish user-facing visual UI — product screens and dashboards, design systems with tokens, interactive prototypes, motion, slide decks, and artifact handoff.
- **`ux-audit`** *(audit)* — Audit an end-user product UX or accessibility surface — usability flows, form friction, navigation/IA, error/recovery copy, and WCAG/keyboard checks — and score it.
- **`writing-audit`** *(audit)* — Audit an existing piece of writing — revise wordy prose, copyedit mechanics while preserving voice, or diagnose why a draft buries the point or fails to land — routed by intent (revise/copyedit/diagnose) × genre, emitting a scored findings report.
- **`writing-design`** *(design)* — Structure, draft, or add a persuasive arc to a new piece of writing — argument/memo, technical doc, talk/pitch, narrative, or general prose — routed by intent (structure/draft/persuade) × genre.

### research

- **`research`** — Source-grounded research in **two decision-frames**. `report` — open-ended research on a topic, with citations and no decision attached (primer, literature review, state-of-the-art; depth modes `brief` / `survey` / `deep-dive`). `opportunity` — validate a named product/business/market/feature opportunity across 14 areas (market, customer, competitive, domain, technical, data, operational, financial, legal, channel, GTM, stakeholder, risk, trend), ending in an F/A/D/R go/no-go/pivot decision with sub-agent fan-out per area. Every load-bearing claim is cited or marked as inference (report frame); every branch ends in a decision (opportunity frame). Provenance in [`skills/research/skill.json`](./skills/research/skill.json).

### Product discovery & planning

Source-grounded product discovery — talking to customers, framing the right problem, and deciding what to build before building it. Each skill paraphrases the canonical discovery literature into operational moves (provenance in each `skill.json`), and is fenced against the desk-research (`research`) and interface-evaluation (`ux-audit`) surfaces it borders.

- **`customer-interviewing`** — Plan, sharpen, run, or synthesize customer discovery interviews — set a learning goal and recruit the right people, rewrite questions that lead or fish for compliments, coach the live conversation, and turn raw notes into evidence-backed interview snapshots that separate what people did from what they say they'll do.
- **`product-discovery`** — Decide what to build and why before building it — reframe outputs as measurable outcomes (and spot feature-factory risk), map an opportunity solution tree, define the customer's job-to-be-done and underserved needs, surface and test the riskiest desirability/viability/feasibility assumptions, and scope an MVP toward product-market fit.
- **`journey-storymapping`** — Shape or fix a product experience with narrative structure — map an experience as a story arc with the user as protagonist (concept/origin/usage stories), diagnose a flat or broken experience by finding the missing beat, and craft concept or origin stories to align a team or pitch the vision.

### Agent experience (AX)

Designing, reviewing, and debugging software, repos, docs, and SDKs for AI agents as a first-class consumer audience — the agent-facing analog of UX and DX.

- **`design-for-agent-users`** — the umbrella discipline. Owns the AX review heuristics (agent-readable docs, AI/Agent SDK design, repo agent-readiness, human-vs-agent audience conflicts) and routes to the three arms below for the *doing*. It is a distinct discipline that routes *across* top-level skills (see [`docs/adr/0006`](./docs/adr/0006-discipline-front-doors-vs-one-engine-many-surfaces.md)). Installed standalone it is **review-only** — its build/harden/measure routes point at the arms, so install those alongside it for the full discipline. Provenance in [`skills/design-for-agent-users/skill.json`](./skills/design-for-agent-users/skill.json).
- **`harden-repo-for-coding-agents`** — assess, harden, scaffold, and diagnose a repository's agent-readiness for AI coding harnesses (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider). Harness-agnostic and portable-first; no eval/telemetry prerequisite — it scaffolds from project knowledge (stack, layout, commands, invariants). Start here for first-pass scaffolding. Provenance in [`skills/harden-repo-for-coding-agents/skill.json`](./skills/harden-repo-for-coding-agents/skill.json).
- **`rules-from-coding-agent-failures`** — capture observed agent failures in a per-file reflection log and promote recurring patterns into AGENTS.md rules / hooks / CI gates via the W1 ≥3-entry floor. For teams with a feedback signal — eval suites, run-level telemetry, A/B baselines, or a skill catalog under test. Provenance in [`skills/rules-from-coding-agent-failures/skill.json`](./skills/rules-from-coding-agent-failures/skill.json).
- **`agent-evals`** — audit an AI product's feedback loops, map them onto the AI Optimization Staircase, score the missing loop mechanics, and scaffold the smallest useful eval/optimization loop. Diagnostic-first; never auto-writes learned rules without held-out evals plus a reviewed diff. Provenance in [`skills/agent-evals/skill.json`](./skills/agent-evals/skill.json).
<!-- END GENERATED: catalog -->

## Install

From GitHub:

```bash
npx skills add Thulr/informed-skills
```

Target specific skills or agents:

```bash
npx skills add Thulr/informed-skills --list
npx skills add Thulr/informed-skills --skill dx-audit
npx skills add Thulr/informed-skills -a claude-code -a cursor -y
```

Common bundles:

```bash
# a domain's audit + design pair
npx skills add Thulr/informed-skills --skill dx-audit --skill dx-design

# the agent-experience (AX) discipline: design-for-agent-users umbrella + its three arms
npx skills add Thulr/informed-skills --skill design-for-agent-users \
  --skill harden-repo-for-coding-agents --skill rules-from-coding-agent-failures --skill agent-evals

# research only
npx skills add Thulr/informed-skills --skill research
```

> **Renamed skills (2026-06-17).** The agent skills now read as use cases:
> `agent-experience` → `design-for-agent-users`, `agent-readiness` →
> `harden-repo-for-coding-agents`, `agent-rules` → `rules-from-coding-agent-failures`
> (`agent-evals` unchanged). The old `--skill <old-name>` commands no longer
> resolve — install the new names. See [`CHANGELOG.md`](./CHANGELOG.md).

From a subdirectory URL (single skill):

```bash
npx skills add https://github.com/Thulr/informed-skills/tree/main/skills/dx-audit
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
| `catalog/catalog.json` | Family-level prose + routing matrix for the generated README §Pick a skill / §Catalog. Per-skill summaries live in each `skill.json` (`metadata.catalog_summary`). Rendered by `scripts/build-catalog.py`; the generated blocks are CI-checked, never hand-edited |
| `scripts/` | Repo-wide scripts: instruction-surface symlink check, schema validator |
| `skills/.experimental/<name>/` | Reserved lane kept empty for now; current product skills live in `skills/<name>/`, and prerelease maturity is communicated by repository release tags such as `0.0.1-alpha` |
| `.agents/skills/<name>/` | Repo-local skills used for authoring and review workflows |
| `THIRD_PARTY.md` | Attribution and licenses for skills not authored here |

Skills marked internal in frontmatter (`metadata.internal: true`) are hidden unless `INSTALL_INTERNAL_SKILLS=1` is set when using the CLI.

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for adding or changing a skill, the
`just check` gate that must pass before every commit and PR, the reflection-log
workflow, and how to install a local checkout while developing. Work in this repo
starts from [`AGENTS.md`](./AGENTS.md), and changes are tracked in
[`CHANGELOG.md`](./CHANGELOG.md).

## License

See [LICENSE](./LICENSE). Individual skills may declare different terms; third-party notices live in [THIRD_PARTY.md](./THIRD_PARTY.md).

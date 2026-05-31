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
developer experience, documentation experience, test quality, architecture,
systems performance and observability, user-facing product UX / accessibility,
UI design craft, and agent experience (designing repos, docs, and SDKs for AI
agents).
Other source-grounded domains can be added later, but they are not part of
the published install surface today.

## Which skill should I use?

| User need | Skill | How it routes |
|---|---|---|
| **Critique** an existing software surface — audit, debug, or risk-scan: developer experience (APIs/SDKs/CLIs/dev-docs/setup/errors/auth/telemetry), documentation, systems performance & observability, test suites, product UX & accessibility, or code architecture | `dx-critique` · `docs-critique` · `perf-critique` · `test-critique` · `ux-critique` · `architecture-critique` | Pick the skill matching the surface; each routes intent (audit/debug/diagnose/…) × surface, dispatches reviewer lenses, scores by severity, and emits a findings report (+ optional tracking ledger). |
| **Design or build** a new software surface — design/author/refactor/optimize/produce: APIs/SDKs/CLIs, documentation IA, perf & SLO instrumentation, test suites, code architecture, **or** visual UI (dashboards, design systems, prototypes, decks) | `dx-design` · `docs-design` · `perf-design` · `test-design` · `architecture-design` · `ui-design` | Pick the skill matching what you're building; each names a good-shaped pattern and emits a design doc / plan / runbook (or, for `ui-design`, the UI artifact itself), grounded in cited heuristics. |
| Source-cited research: an open-ended topic report, **or** validating a named product/market/feature opportunity to a go/no-go | `research` | Pick the **frame**: `report` (primer / literature review / "research X for me", no decision) or `opportunity` (validate a named idea across 14 areas → F/A/D/R go/no-go/pivot). |
| Design, review, or debug for AI agents as a consumer audience: agent-readable docs (llms.txt, AGENTS.md, MCP/tool descriptions, RAG/retrieval), AI/Agent SDK design (streaming, tools, structured output, agent loops, tracing), repo agent-readiness review, human-vs-agent audience conflicts | `agent-experience` | The **umbrella AX discipline**. Owns the AX review heuristics; routes to its three arms for the *doing* — `project-agentification` (harden a repo), `evidence-driven-agent-rules` (promote failures into rules), `eval-flywheel` (instrument loops). |
| Make a repo work better with coding agents; assess, harden, scaffold, or diagnose agent-readiness | `project-agentification` | The repo-hardening **arm** of `agent-experience`. vs `evidence-driven-agent-rules` — start here for first-pass scaffolding from project knowledge (no eval prerequisite). |
| Capture observed agent failures and promote recurring patterns into rules/gates from evidence | `evidence-driven-agent-rules` | The evidence/feedback **arm** of `agent-experience`. vs `project-agentification` — needs a feedback signal (eval suites, run telemetry, A/B baselines). If the repo has none yet, start with `project-agentification`. |
| Audit an AI app/agent's feedback loops, score them on the Optimization Staircase, and scaffold the smallest useful eval/optimization loop | `eval-flywheel` | The instrument-the-loop **arm** of `agent-experience`. vs the two agent-readiness skills — those harden *a repository* so coding agents work in it; `eval-flywheel` instruments *an AI product/agent you ship* so its outputs feed a measured loop (the model is the product). |

**Ambiguous phrasings.** When the *user need* itself is ambiguous, ask one clarifier before routing:

- *"Make our docs better"* — auditing existing documentation → `docs-critique`; planning or reshaping docs IA → `docs-design`; developer-facing API/SDK friction beyond docs → `dx-critique`; humans using the product UI → `ux-critique`. Agent-readable docs (llms.txt, retrieval-friendly structure, chunk survivability) → `agent-experience`. Coding agents operating inside the repo → `project-agentification`.
- *"Audit / review this"* (DX vs docs vs perf vs test vs UX vs architecture) — pick the matching `<domain>-critique` skill (`dx-critique` / `docs-critique` / `perf-critique` / `test-critique` / `ux-critique` / `architecture-critique`) for the surface.
- *"Add a hook"* — Claude / Codex / Cursor agent gate (PreToolUse, PostToolUse) → `project-agentification`; generic Git or build hook → out of scope for this catalog.
- *"Our service is slow" / "design SLOs"* — diagnosing a slow or incident-y production system → `perf-critique`; designing SLOs / instrumentation / a profile-first optimization → `perf-design`; the developer's own machine (local install, cold start, edit-test-debug) → `dx-critique`.
- *"Improve our agent" / "make our AI better"* — making a coding-agent harness work better in this repo (AGENTS.md, hooks, MCP) → `project-agentification`; building an eval/optimization loop for an AI product or agent you ship → `eval-flywheel`.
- *"Make our app agent-friendly" / "design an Agent SDK" / "is our AGENTS.md agent-ready" / "review our llms.txt for agents"* — the **agent-experience** umbrella: it reviews the AX surface (agent-readable docs, AI/Agent SDK, repo readiness) and routes to `project-agentification` to harden the repo, `evidence-driven-agent-rules` to promote failures into rules, or `eval-flywheel` to instrument loops.
- *"Research X"* — open-ended topic (primer, literature review, state-of-the-art) → `research` (`report` frame); validate a named product/business opportunity (go/no-go) → `research` (`opportunity` frame); compare a fixed set of named options → `tradeoff-analysis`.

## Skills

### Heuristic critique & design (per domain × function)

Source-grounded heuristics for software surfaces, split so the skill name says
what it does. A **`-critique`** skill audits, debugs, or risk-scans an *existing*
surface (expert lenses → severity-scored findings report, with an optional
tracking ledger); a **`-design`** skill shapes a *new* one (names the
good-shaped pattern → design doc / plan / runbook). Pick the skill that matches
your surface and whether you're reviewing or building.

| Domain | Critique an existing surface | Design / build a new one |
|---|---|---|
| Developer experience — APIs, SDKs, CLIs, dev docs, setup, errors, auth, packaging, IDE, plugins, telemetry | `dx-critique` | `dx-design` |
| Documentation experience — README/quickstarts, API refs, help centers, OpenAPI/MCP tool contracts | `docs-critique` | `docs-design` |
| Systems performance & observability — latency, p99/tail, throughput, SLOs, tracing, logs, metrics, capacity | `perf-critique` | `perf-design` |
| Test-suite quality — unit/integration/e2e/property/contract/snapshot/mutation, flakiness, pruning | `test-critique` | `test-design` |
| Product UX & accessibility — usability, forms, navigation/IA, error/recovery, WCAG | `ux-critique` | *(to build UI → `ui-design`)* |
| Visual UI craft — dashboards, design systems/tokens, prototypes, motion, slide decks, handoff | *(to audit usability → `ux-critique`)* | `ui-design` |
| Clean architecture — dependency rule, layered/hexagonal/onion boundaries, ports/adapters, DDD, bounded contexts | `architecture-critique` | `architecture-design` |

Grounded in 120+ cited sources (Norman, Nielsen, Bloch, Gregg, the Google SRE
book, Kleppmann, WCAG 2.2, Martin, Evans, and many more — per-skill provenance
in each `skill.json`). A domain's `-critique` and `-design` skills share their
heuristic playbooks, lenses, personas, and rubrics via `skills/_shared/<domain>/`,
so the pair stays in lockstep without drift. (These twelve skills replaced the
merged `review-heuristics` skill — see
[`docs/adr/0008`](./docs/adr/0008-reverse-review-consolidation-split-by-domain-and-function.md).)

Install a domain's pair:

```bash
npx skills add Thulr/informed-skills --skill dx-critique --skill dx-design
```

### research

Source-grounded research in **two decision-frames**. `report` — open-ended
research on a topic with citations and no decision attached (primer, literature
review, state-of-the-art; depth modes `brief` / `survey` / `deep-dive`).
`opportunity` — validate a named product/business/market/feature opportunity
across 14 areas (market, customer, competitive, domain, technical, data,
operational, financial, legal, channel, GTM, stakeholder, risk, trend), ending
in an F/A/D/R go/no-go/pivot decision with sub-agent fan-out per area.

Every load-bearing claim is cited or marked as inference (report frame); every
branch ends in a decision, not a note (opportunity frame). Grounded in
canonical literature-review, product, strategy, and venture literature (full
provenance in [`skills/research/skill.json`](./skills/research/skill.json)).

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill research
```

### agent-experience

The **umbrella agent-experience (AX) discipline** — designing, reviewing, and
debugging software, repos, docs, and SDKs for AI agents as a first-class consumer
audience (the agent-facing analog of UX and DX). It owns the AX review heuristics
and routes to its three implementation arms for the *doing*.

| Owns (review / design / debug) | Routes to (the doing) |
|---|---|
| Agent-readable docs (`llms.txt`, AGENTS.md, MCP/tool descriptions, RAG/retrieval, chunk survivability); AI/Agent SDK design (streaming, tools, structured output, agent loops, guardrails, tracing, MCP transport); repo agent-readiness review; human-vs-agent audience conflicts | `project-agentification` (harden a repo) · `evidence-driven-agent-rules` (promote observed failures into rules) · `eval-flywheel` (instrument eval/optimization loops) |

Standalone rather than a per-domain critique/design skill because it is a distinct
discipline that routes *across* top-level skills (see
[`docs/adr/0006`](./docs/adr/0006-discipline-front-doors-vs-one-engine-many-surfaces.md)).
Grounded in the AGENTS.md convention, the Model Context Protocol, Mündler et al.
on context-file evals, the OpenTelemetry GenAI conventions, and the AX/DX/UX
documentation synthesis (full provenance in
[`skills/agent-experience/skill.json`](./skills/agent-experience/skill.json)).

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill agent-experience
```

### project-agentification

Assess, harden, scaffold, and diagnose a repository's agent-readiness for AI coding harnesses (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider). Harness-agnostic; portable-first (AGENTS.md, SKILL.md, MCP, OpenTelemetry). **For any repo that wants coding agents to work well in it** — no eval / benchmark / telemetry prerequisites; scaffolds from project knowledge (stack, layout, commands, invariants).

Routes by intent (`assess` / `harden` / `scaffold` / `diagnose`) × surface (11 surfaces across 3 layers: legibility / action / control), then dispatches four parallel reviewer lenses (cold-context-agent / maintainer / adversarial / auditor). Grounded in published research (full provenance in [`skills/project-agentification/skill.json`](./skills/project-agentification/skill.json)).

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

### eval-flywheel

Audit a workspace's AI integrations, map them onto the **AI Optimization Staircase** (L1 system-prompt learning → L2 subroutine compilation → L3 sandbox + repair harness → L4 system benchmarking), score the loop mechanics that are missing, and scaffold the smallest useful eval/optimization loop. **For teams shipping an AI product or agent** who are still iterating on prompts by feel and want to move onto metric-driven reliability work.

Diagnostic-first: presents a Loop Readiness Matrix (signal / interpreter / change surface / cadence / stop-rollback / owner) before recommending a tier, and never auto-writes learned rules without held-out evals + reviewed diff. Grounded in DSPy (Khattab et al.), Reflexion (Shinn et al.), Terminal-Bench / SWE-bench-style system benchmarks, and the feedback-loop eval/observability practice cluster (full provenance in [`skills/eval-flywheel/skill.json`](./skills/eval-flywheel/skill.json)).

Install just this skill:

```bash
npx skills add Thulr/informed-skills --skill eval-flywheel
```


## Install

From GitHub:

```bash
npx skills add Thulr/informed-skills
```

Install specific skills or target agents:

```bash
npx skills add Thulr/informed-skills --list
npx skills add Thulr/informed-skills --skill dx-critique --skill dx-design
npx skills add Thulr/informed-skills -a claude-code -a cursor -y
```

From a subdirectory URL (single skill):

```bash
npx skills add https://github.com/Thulr/informed-skills/tree/main/skills/dx-critique
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

## Development
To install a skill from this checkout into `~/.agents/skills`:

```bash
npx --yes skills add . --skill <skill-name> --agent cline --global --copy -y
```

## License

See [LICENSE](./LICENSE). Individual skills may declare different terms; third-party notices live in [THIRD_PARTY.md](./THIRD_PARTY.md).

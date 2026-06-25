<p align="center">
  <img src="./docs/agent-skill-kit.png" alt="agent-skill-kit — the Agent Skills I use" width="800">
</p>

# agent-skill-kit

**[Agent Skills](https://agentskills.io) I actually use.** Source-grounded, failure-driven, earned in real coding-agent work. Installable with the open ecosystem CLI.

```bash
npx skills add justinramos101/agent-skill-kit
```

## Quickstart

```bash
# 1. Install (picks skills interactively)
npx skills add justinramos101/agent-skill-kit

# 2. Start using — skills activate from natural language
# "audit my CLI's developer experience"    → dx-audit
# "design our API error envelope"           → dx-design
# "review this UI for anti-slop"            → ui-design
# "make our repo work with Claude Code"     → harden-repo-for-coding-agents
```

No commands to memorize. Each skill routes by intent, names its cited sources, and produces a scored, traceable result.

## Install

Pick what you need:

```bash
# Interactive — browse and choose skills
npx skills add justinramos101/agent-skill-kit

# Specific skills
npx skills add justinramos101/agent-skill-kit --skill dx-audit --skill ui-design

# An audit + design pair
npx skills add justinramos101/agent-skill-kit --skill dx-audit --skill dx-design
```

Per-agent installs (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider):

```bash
npx skills add justinramos101/agent-skill-kit -a claude-code -a cursor
```

See `npx skills --help` for global vs. project scope.

## Why these skills exist

Four problems agent skills solve, and which skill to reach for:

### 1. "This surface feels wrong but I can't name why"

Your API has friction, your docs bury the answer, your tests pass but don't catch bugs.

→ **`dx-audit`**, **`docs-audit`**, **`test-audit`**, **`ux-audit`**, **`writing-audit`**
Severity-scored findings, playbook-driven, cited sources. Each audit tells you *exactly* what's wrong and how to fix it.

### 2. "I need to design something new — where do I start?"

Blank canvas, no guardrails, easy to build something generic.

→ **`dx-design`**, **`docs-design`**, **`test-design`**, **`ui-design`**, **`writing-design`**
Each design skill names the good-shaped pattern, produces a concrete artifact, and carries cited heuristics so you're not guessing.

### 3. "My agent keeps making the same mistakes"

Recurring failures in CI, in PRs, in generated code — no feedback loop to capture them.

→ **`rules-from-coding-agent-failures`** (promote patterns into rules/gates)
→ **`harden-repo-for-coding-agents`** (scaffold AGENTS.md, hooks, CI gates — no eval prereq needed)
→ **`context-budget-audit`** (prune idle MCP servers, unused skills eating context tokens)

### 4. "I want a second opinion before I ship"

You trust your agent but want independent review from a different model or provider.

→ **`claude-code-cli`**, **`codex-cli`**, **`cursor-cli`**
Drive an external CLI as an independent second-opinion reviewer. Read-only by default. Reconcile findings against local evidence.

<!-- BEGIN GENERATED: pick-a-skill (scripts/build-catalog.py) -->
## Pick a skill

Two questions get you there: **which surface**, and are you **reviewing it** or **building it**?

| Surface | Review it → `-audit` | Build it → `-design` |
|---|---|---|
| **Developer experience** — APIs, SDKs, CLIs, dev docs, setup, errors, auth, packaging, IDE, plugins, telemetry | `dx-audit` | `dx-design` |
| **Documentation** — READMEs, quickstarts, API refs, help centers, OpenAPI/MCP tool contracts | `docs-audit` | `docs-design` |
| **Writing** — memos/PRDs/RFCs, technical & task docs, talks/pitches, narratives, general prose | `writing-audit` | `writing-design` |
| **Test suites** — unit/integration/e2e/property/contract/snapshot/mutation, flakiness, pruning | `test-audit` | `test-design` |
| **Product UX & accessibility** — usability, forms, navigation/IA, error/recovery, WCAG | `ux-audit` | → `ui-design` |
| **Visual UI craft** — dashboards, design systems/tokens, prototypes, motion, decks, handoff | → `ui-design` quality-review | `ui-design` |
| **Artifact ↔ host integration** — embeddable HTML artifacts: postMessage / persistence / fixed-canvas / direct-edit / export contract with an editing shell | → `ui-design` | `ui-design` (host-integration route) |
| **Minimal, modular code** — slop, duplication, over-engineering; dependency direction, deep modules; right-sizing structure so many agents can work in parallel | `minimal-modular-code` | `minimal-modular-code` |

For research and agent-facing work:

| Need | Skill |
|---|---|
| **Source-cited research** — an open-ended topic report, or validating a named opportunity to a go/no-go decision | `research` |
| **Agent as developer** — the SDK / tool / error / telemetry surface an AI agent consumes | `agent-dx` |
| **Agent as reader** — AGENTS.md, llms.txt, tool descriptions, machine-readable reference for agents | `agent-docs` |
| **Agent as end-user** — an agent-operable UI / app / computer-use surface | `agent-ux` |
| **Agent as operator** — observability, trace-and-eval loops, autonomy, reliability | `agent-ops` |
| **Agent as subject** — evals, LLM-as-judge, benchmarks, activation tests | `agent-test` |
| ↳ harden a repo for coding agents (AGENTS.md, hooks, gates, sandbox) | `harden-repo-for-coding-agents` |
| ↳ promote observed agent failures into rules / gates | `rules-from-coding-agent-failures` |
| **Second opinion from Codex** — drive the Codex CLI to review code/docs, give an independent take, or reflect across projects | `codex-cli` |
| **Second opinion from Claude Code** — review working-tree/branch changes, a second opinion, cross-project reflection, or a hosted ultrareview | `claude-code-cli` |
| **Second opinion from Cursor** — review or analyze under a *different* model (gpt-5, sonnet-4, …) via `cursor-agent` | `cursor-cli` |
| **Trim your agent's context budget** — audit idle MCP servers and unused plugins/skills/commands/subagents by per-session token cost, then prune safely | `context-budget-audit` |

**Still unsure?** The two boundaries people hit most:

- *"Make our docs better"* — audit existing docs → `docs-audit`; reshape docs IA → `docs-design`; API/SDK friction beyond the docs → `dx-audit`; agent-native docs (llms.txt, AGENTS.md, retrieval) → `agent-docs`.
- *"Improve our agent"* — make a coding-agent harness work in this repo (AGENTS.md, hooks, MCP) → `harden-repo-for-coding-agents`; design evals/benchmarks for an AI product → `agent-test`; operate its trace-and-eval loop, autonomy, and reliability → `agent-ops`.
<!-- END GENERATED: pick-a-skill -->

<!-- BEGIN GENERATED: catalog (scripts/build-catalog.py) -->
## Catalog

What each skill is and what it's grounded in. To route by task use [Pick a skill](#pick-a-skill); to install see [Install](#install).

### Heuristic audit & design pairs

Source-grounded heuristics for software surfaces, split so the name says what it does. A **`-audit`** skill audits, debugs, or risk-scans an *existing* surface (expert lenses → severity-scored findings report, with an optional tracking ledger); a **`-design`** skill shapes a *new* one (names the good-shaped pattern → design doc / plan / runbook). A domain's pair shares its playbooks, lenses, personas, and rubrics via `skills/_shared/<domain>/`, so the two stay in lockstep without drift.

Grounded in 120+ cited sources — Norman, Nielsen, Bloch, Gregg, the Google SRE book, Kleppmann, WCAG 2.2, Ousterhout, Parnas, and many more (per-skill provenance in each `skill.json`). The `-audit`/`-design` pairs replaced the merged `review-heuristics` skill — see [`docs/adr/0008`](./docs/adr/0008-reverse-review-consolidation-split-by-domain-and-function.md). `minimal-modular-code` is the family's one singleton — a single skill spanning review and design for code minimality and parallel-readiness; it replaced the former clean-architecture pair (see [`docs/adr/0009`](./docs/adr/0009-replace-architecture-pair-with-minimal-modular-code.md)).

- **`docs-audit`** *(audit)* — Audit a docs/help/agent-readable surface for friction, drift, accessibility, retrieval, or audience conflict and score it — or debug a concrete docs failure.
- **`docs-design`** *(design)* — Plan or reshape a docs surface before implementation — information architecture, mode taxonomy, README/quickstart/reference structure, examples strategy, and API/tool-contract docs.
- **`dx-audit`** *(audit)* — Audit a developer-experience surface (APIs, SDKs, CLIs, errors, setup, auth, packaging, IDE, plugins, telemetry) for friction and score it, or run a pre-ship edge-case risk pass.
- **`dx-design`** *(design)* — Design a new developer-experience surface from scratch — API, SDK, CLI, error envelope, setup/first-run flow, auth model, migration/deprecation path, plugin contract, or package scheme.
- **`minimal-modular-code`** — Keep code minimal and right-sized for AI coding agents: DO (keep a change minimal — reuse, subtract, avoid the wrong abstraction, check blast radius), REVIEW (audit existing code or a repo for slop and parallel-readiness, then score it), DESIGN (shape right-sized module boundaries and work-partitioning, sequence a safe refactor, or explain a principle). Replaces the clean-architecture audit/design pair under a minimalism thesis.
- **`test-audit`** *(audit)* — Review a test suite for smells, redundancy, false-pass risk, brittleness, and flakiness and score it, or triage one failing, flaky, or slow test.
- **`test-design`** *(design)* — Author a new test or test plan, shape a cross-layer test strategy (what to test at which layer), or plan which low-value tests to delete.
- **`ui-design`** *(design)* — Produce or polish user-facing visual UI — product screens and dashboards, design systems with tokens, interactive prototypes, motion, slide decks, and artifact handoff.
- **`ux-audit`** *(audit)* — Audit an end-user product UX or accessibility surface — usability flows, form friction, navigation/IA, error/recovery copy, and WCAG/keyboard checks — and score it.
- **`writing-audit`** *(audit)* — Audit an existing piece of writing — revise wordy prose, copyedit mechanics while preserving voice, or diagnose why a draft buries the point or fails to land — routed by intent (revise/copyedit/diagnose) × genre, emitting a scored findings report.
- **`writing-design`** *(design)* — Structure, draft, or add a persuasive arc to a new piece of writing — argument/memo, technical doc, talk/pitch, narrative, or general prose — routed by intent (structure/draft/persuade) × genre.

### research

- **`research`** — Source-grounded research in **two decision-frames**. `report` — open-ended research on a topic, with citations and no decision attached (primer, literature review, state-of-the-art; depth modes `brief` / `survey` / `deep-dive`). `opportunity` — validate a named product/business/market/feature opportunity across 14 areas (market, customer, competitive, domain, technical, data, operational, financial, legal, channel, GTM, stakeholder, risk, trend), ending in an F/A/D/R go/no-go/pivot decision with sub-agent fan-out per area. Every load-bearing claim is cited or marked as inference (report frame); every branch ends in a decision (opportunity frame). Provenance in [`skills/research/skill.json`](./skills/research/skill.json).

### Agent experience (AX)

The agent-mirror family: an **AI agent is an actor** (not a peer audience), so each human-experience domain gets an agent mirror — `agent-dx` (agent as developer), `agent-docs` (reader), `agent-ux` (end-user), `agent-ops` (operator), and `agent-test` (subject under measurement) — plus the standalone arms `harden-repo-for-coding-agents` and `rules-from-coding-agent-failures` they route out to. Each mirror routes do/review/design like the heuristic singletons. Organized by actor per [`docs/adr/0011`](./docs/adr/0011-actor-axis-agent-mirror-family.md).

- **`harden-repo-for-coding-agents`** — assess, harden, scaffold, and diagnose a repository's agent-readiness for AI coding harnesses (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider). Harness-agnostic and portable-first; no eval/telemetry prerequisite — it scaffolds from project knowledge (stack, layout, commands, invariants). Start here for first-pass scaffolding. Provenance in [`skills/harden-repo-for-coding-agents/skill.json`](./skills/harden-repo-for-coding-agents/skill.json).
- **`rules-from-coding-agent-failures`** — capture observed agent failures in a per-file reflection log and promote recurring patterns into AGENTS.md rules / hooks / CI gates via the W1 ≥3-entry floor. For teams with a feedback signal — eval suites, run-level telemetry, A/B baselines, or a skill catalog under test. Provenance in [`skills/rules-from-coding-agent-failures/skill.json`](./skills/rules-from-coding-agent-failures/skill.json).
- **`agent-docs`** — Agent-as-reader: the agent-native documentation an AI agent reads and acts on — DO (write/fix an AGENTS.md, llms.txt, tool description, machine-readable reference, or context budget), REVIEW (audit findability, chunk survivability, trigger clarity, and budget, then score it), DESIGN (shape the AGENTS.md contract, curated index, tool descriptions, reference, or budget tiers). Narrowed to agent-native artifacts; human/dual-audience docs stay in docs-audit / docs-design.
- **`agent-dx`** — Agent-as-developer: keep the SDK/tool/error/telemetry surface an AI agent consumes minimal and safe — DO (keep an agent-facing change agent-consumable), REVIEW (audit a surface for stable contracts, agent recovery, and trust-boundary safety, then score it), DESIGN (shape a new SDK/tool/MCP/structured-output/error/telemetry surface). Sits atop the human HTTP-client floor in dx-audit / dx-design.
- **`agent-ops`** — Agent-as-operator and the agent-family front-door: operate a running agent system — DO (wire observability/loop/autonomy/budgets/gates), REVIEW (audit observability, optimization loop, autonomy controls, reliability/cost, and maturity, then score it), DESIGN (shape the loop, gate autonomy, decompose the release gate, place maturity and route work to siblings). Operates what agent-dx instruments; routes building out to the family.
- **`agent-test`** — Agent-as-subject-under-measurement: design the measurement an AI agent or skill is judged by — DO (write the smallest gating eval/judge/test), REVIEW (audit an eval suite, judge calibration, trajectory tests, benchmarks, or activation evals for trustworthiness, then score it), DESIGN (shape a failure-mode-first suite, calibrate a judge, build a held-out benchmark, design activation evals). Designs what agent-ops then operates.
- **`agent-ux`** — Agent-as-end-user: the interaction surface an AI agent acts through (a UI, app, or computer-use target), often on a human's behalf — DO (make it perceivable, targetable, safe to act on), REVIEW (audit machine-readable state, deterministic actions, agent agency/approval, and human-vs-agent conflict, then score it), DESIGN (shape the state, action handles, approval gate, or dual path). Net-new; the agent-actor analog of human UX.

### Cross-agent interop & tooling

Skills that drive *another* coding agent or CLI as part of your own workflow — an independent second-opinion reviewer, an external analysis pass, a cross-project reflection — rather than auditing or designing a surface themselves. The pragmatic "tools the maintainer actually reaches for" corner of the kit, grouped by what you *do with them* (grouping nod to [`mattpocock/skills`](https://github.com/mattpocock/skills)); distinct from the source-grounded audit/design pairs and from the agent-experience family, which shape surfaces *for* agents rather than *using* one as an instrument. See [`docs/adr/0012`](./docs/adr/0012-interop-family-for-cross-agent-tooling.md).

- **`claude-code-cli`** — Drive the external **Claude Code CLI** (`claude -p`) as an independent second-opinion reviewer and analysis agent — review working-tree/staged/branch diffs (the wrapper builds the diff and feeds it read-only via `--permission-mode plan`), get a second opinion on a decision/bug/plan, run cross-project reflection, or hand off to a hosted `claude ultrareview`. Routes through a use-case registry, defaults to read-only, never bypasses permissions without an explicit ask, and presents output as an external opinion to reconcile against local evidence. Provenance in [`skills/claude-code-cli/skill.json`](./skills/claude-code-cli/skill.json).
- **`codex-cli`** — Drive the external **Codex CLI** as an independent second-opinion reviewer and analysis agent — `codex review` for uncommitted/branch/commit diffs, `codex exec` (read-only sandbox) for second opinions and repo analysis, plus cross-project reflection, setup diagnostics, and prompt-prep (`--dry-run`) modes. Routes through a use-case registry, defaults to read-only, and never bypasses Codex approvals/sandbox without an explicit ask. Reach for it when you want a different LLM provider's take on code or docs before shipping. Provenance in [`skills/codex-cli/skill.json`](./skills/codex-cli/skill.json).
- **`cursor-cli`** — Drive the external **Cursor CLI** (`cursor-agent -p`) as an independent second-opinion reviewer and analysis agent — review working-tree/staged/branch diffs (the wrapper builds the diff and feeds it read-only via `--mode plan`) or get a second opinion on a decision/bug/plan. Its edge over the other interop skills is **model diversity**: cursor-agent can run many providers' models (gpt-5, sonnet-4, …), so you can review code with a *different* model than wrote it. Routes through a use-case registry, defaults to read-only, never drops the guard with `--force`/`--yolo` without an explicit ask. Provenance in [`skills/cursor-cli/skill.json`](./skills/cursor-cli/skill.json).

### Context budget & agent-setup hygiene

Audit and reclaim the per-session context an agent's *local setup* costs — the MCP servers, plugins, skills, slash commands, and subagents that load into every session whether or not you use them. Distinct from the agent-experience family (which shapes surfaces *for* agents) and from `harden-repo-for-coding-agents` (which hardens a repo's agent config): this family measures what is loaded, estimates its always-on token cost from real usage evidence, and gates safe pruning. One skill today; introduced per [`docs/adr/0013`](./docs/adr/0013-context-budget-family.md).

- **`context-budget-audit`** — Audit per-session **context/token budget** across your local agent setup — idle MCP servers, disabled/unused plugins, unused skills, slash commands, and subagents. A read-only stdlib Python engine (`scripts/audit_context_budget.py`) inventories each surface, estimates its always-on token cost, scans recent transcripts for genuine usage evidence, and shows a prune-decision view sorted by reclaimable context (idle MCP servers surfaced first as the usual biggest win) alongside the aggregate context footprint by kind. Removal is gated: skills are copy-validate-removed into a repo, command/subagent files deleted on confirmation, and MCP/plugin config edits handed back as commands rather than executed. Provenance in [`skills/context-budget-audit/skill.json`](./skills/context-budget-audit/skill.json).
<!-- END GENERATED: catalog -->

## Layout

| Path | Purpose |
|------|---------|
| `skills/<name>/` | Published skills — each ships `SKILL.md` + `skill.json` + `evals/` |
| `skills/_shared/` | Cross-skill playbooks, rubrics, lenses. Symlinked by consumers. |
| `catalog/catalog.json` | Family prose + routing matrix → rendered into the sections above |
| `docs/adr/` | Architectural Decision Records |
| `docs/reflection-log/` | One file per observed agent failure |
| `docs/runbooks/` | Maintainer procedures |
| `docs/templates/example-minimal/` | Template contract: minimum artifacts every skill must ship |
| `schemas/` | JSON Schemas for `skill.json` and `trigger-evals.json` |
| `scripts/` | Build, check, and validation scripts |
| `AGENTS.md` | Hand-curated agent instructions (also surfaced via `CLAUDE.md` symlink) |

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for adding or changing a skill, the `just check` gate, and how to install a local checkout while developing. Work starts from [`AGENTS.md`](./AGENTS.md). Changes tracked in [`CHANGELOG.md`](./CHANGELOG.md).

## License

[LICENSE](./LICENSE). Individual skills may declare different terms; third-party notices live in [THIRD_PARTY.md](./THIRD_PARTY.md).
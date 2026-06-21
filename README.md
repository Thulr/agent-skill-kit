<p align="center">
  <img src="./docs/agent-skill-kit.png" alt="agent-skill-kit — the Agent Skills I use" width="800">
</p>

# agent-skill-kit

**The [Agent Skills](https://agentskills.io) I actually use.** A personal kit for coding-agent work — most grounded in 120+ cited sources you can check, all earned in real use. When a skill I rely on isn't mine, I link to it rather than re-author it (see **Skills I also use**). Install them with the open-ecosystem CLI, [skills.sh](https://skills.sh):

```bash
npx skills add justinramos101/agent-skill-kit
```

[skills.sh](https://skills.sh) prompts you to pick which skills to install — see [Install](#install) for options.

**First use.** Skills activate from natural-language prompts — no command to run. Once installed, ask your agent *"audit my CLI's developer experience"* and `dx-audit` kicks in with a severity-scored findings report; *"design our API's error envelope"* routes to `dx-design`; *"is our llms.txt agent-ready?"* to `agent-docs`. Each skill names the cited sources it applied.

Today the kit spans developer and documentation experience, writing, tests, code quality, product UX and UI, research, and agent work — [Pick a skill](#pick-a-skill) has the full map. More gets added as I use them.

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
| **Visual UI craft** — dashboards, design systems/tokens, prototypes, motion, decks, handoff | → `ux-audit` | `ui-design` |
| **Artifact ↔ host integration** — embeddable HTML artifacts: the postMessage / persistence-marker / comment-anchor / fixed-canvas / export contract between an artifact and its editing host | → `ui-design` | `artifact-host-integration` |
| **Minimal, modular code** — slop, duplication, over-engineering; dependency direction, deep modules; right-sizing structure so many agents can work in parallel | `minimal-modular-code` | `minimal-modular-code` |

For research and agent-facing work:

| Need | Skill |
|---|---|
| **Source-cited research** — an open-ended topic report, or validating a named opportunity to a go/no-go decision | `research` |
| **Agent as developer** — the SDK / tool / error / telemetry surface an AI agent consumes | `agent-dx` |
| **Agent as reader** — AGENTS.md, llms.txt, tool descriptions, machine-readable reference for agents | `agent-docs` |
| **Agent as end-user** — an agent-operable UI / app / computer-use surface | `agent-ux` |
| **Agent as operator** — observability, trace-and-eval loops, autonomy, reliability (the agent-family front-door) | `agent-ops` |
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

## Install

From GitHub:

```bash
npx skills add justinramos101/agent-skill-kit
```

Target specific skills or agents:

```bash
npx skills add justinramos101/agent-skill-kit --list
npx skills add justinramos101/agent-skill-kit --skill dx-audit
npx skills add justinramos101/agent-skill-kit -a claude-code -a cursor -y
```

Common bundles:

```bash
# a domain's audit + design pair
npx skills add justinramos101/agent-skill-kit --skill dx-audit --skill dx-design

# the agent-mirror family (agent as developer / reader / end-user / operator / subject) + arms
npx skills add justinramos101/agent-skill-kit --skill agent-dx --skill agent-docs --skill agent-ux \
  --skill agent-ops --skill agent-test \
  --skill harden-repo-for-coding-agents --skill rules-from-coding-agent-failures

# research only
npx skills add justinramos101/agent-skill-kit --skill research
```

> **Reorg (2026-06-19):** `design-for-agent-users` and `agent-evals` were replaced by the `agent-*` mirrors — the old `--skill design-for-agent-users` / `--skill agent-evals` commands no longer resolve. See [`CHANGELOG.md`](./CHANGELOG.md).

From a subdirectory URL (single skill):

```bash
npx skills add https://github.com/justinramos101/agent-skill-kit/tree/main/skills/dx-audit
```

Local checkout:

```bash
git clone https://github.com/justinramos101/agent-skill-kit.git
cd agent-skill-kit
npx skills add . --list
npx skills add .
```

Use `-g` / `--global` for user-wide installs; default is project scope. See `npx skills --help`.

## Full catalog

Every skill — grouped by family, with descriptions and sources — is in **[CATALOG.md](./CATALOG.md)**. ([Pick a skill](#pick-a-skill) above routes by task.)

## Skills I also use

Good skills I rely on but didn't write — installed from their own homes, linked here rather than re-authored.

<!-- Add entries as you adopt them, e.g.:
- [`owner/skill-name`](https://github.com/owner/skill-name) — what it's for and when you reach for it.
-->

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) to add or change a skill — it covers the
`just check` gate (required before every commit and PR), the reflection-log workflow,
installing a local checkout, and the [repository layout](./CONTRIBUTING.md#repository-layout).
Work starts from [`AGENTS.md`](./AGENTS.md); changes are tracked in [`CHANGELOG.md`](./CHANGELOG.md).

## License

See [LICENSE](./LICENSE). Individual skills may declare different terms; third-party notices live in [THIRD_PARTY.md](./THIRD_PARTY.md).

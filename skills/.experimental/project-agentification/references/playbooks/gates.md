# gates

## What it is

Gates are enforcement points wired into the harness layer — not prose in instruction files — that
intercept or react to tool calls at execution time. Claude Code exposes two hook types:

- **PreToolUse** — fires before the tool runs; exit code 2 blocks execution entirely. Use for
  hard-blocking dangerous calls (`rm -rf`, force-push to main, prod-DB writes).
- **PostToolUse** — fires after the tool completes; the action has already happened. Use for
  reactive enforcement: format-on-write, lint-on-write, test-on-write.

Three tiers organize what a gate should do for each action class:

| Tier | Description | Examples |
|---|---|---|
| **free-action** | Agent proceeds without approval | Read public files, run tests, search codebase |
| **ask-first** | Agent must request user approval before proceeding | DB migrations, dependency changes, secret-handling edits, new external network destinations |
| **forbidden** | Hard-blocked at the hook layer, no override path | `rm -rf`, force-push to main, prod-DB writes, disabling sandbox controls |

Linters and formatters wired to PostToolUse write-time hooks shape agent output structurally —
Aider's auto-lint and auto-test and Factory.ai's linter-as-direction pattern both demonstrate this.
Copilot's custom-instructions guidance adds a complementary requirement: explicitly document which
commands work and which do not, including errors encountered and workarounds taken.

### Per-harness gate primitives

Different harnesses expose different enforcement points. **Scaffold per-harness equivalents for every harness in the step 4.5 inventory** — not just the one whose dotfile happens to exist.

| Harness | Hard-block primitive (forbidden) | Approval primitive (ask-first) | Reactive primitive (lint-on-write) | Notes |
|---|---|---|---|---|
| **Claude Code** | `PreToolUse` hook exit 2 (`.claude/settings.json` + `.claude/hooks/*`) | `PreToolUse` hook structured payload | `PostToolUse` hook on `Write`/`Edit` | Only harness with a native non-bypassable hard-block at the harness layer. |
| **Cursor** | None native — prose-only (`alwaysApply: true` in `.cursor/rules/*.mdc`) → ~70% (W3) | Same — prose-only | None native; relies on file-watcher / pre-commit | Compensate with CI gates + pre-commit hooks. |
| **Codex** | Sandbox policy (filesystem allow-list, network egress allow-list) + `--ask-for-approval` tiering | `--ask-for-approval` modes (`untrusted` / `on-failure` / `on-request` / `never`) | None native; relies on Codex shell tool calls in the wrapped run | Hard-block is sandbox-layer, not harness-layer; the `~/.codex/config.toml` plus per-repo `AGENTS.md` define it. |
| **Aider** | None native — prose + `--read-only` files | `--auto-commits false` (manual approval per commit) | `--lint-cmd` and `--test-cmd` run after every edit cycle | Lint-as-direction is Aider's strongest primitive. |
| **Copilot** (IDE / coding agent) | None native — CI-only (branch protection + required checks) | None native (PR review is the approval point) | None native; relies on workflow `actions/*` checks | Push enforcement entirely into CI. `.github/copilot-instructions.md` is prose-only. |
| **Windsurf** | None native (W3) — `.windsurf/rules/*.md` with `trigger: always_on` is prose | None native | None native | 12 k-char workspace rule cap; behave like Cursor for enforcement purposes. |
| **AGENTS.md-only** (Jules, Amp, etc.) | None — prose-only | None | None | CI is the only structural enforcement; treat the harness layer as advisory. |

**Implication.** A `forbidden`-tier rule like *"never force-push to main"* needs:
- Claude Code: `PreToolUse` hook (exit 2).
- Codex: sandbox network/process policy + an `AGENTS.md` line that the wrapped shell enforces.
- Cursor / Windsurf / Aider / Copilot / AGENTS.md-only: **CI branch protection** is the load-bearing gate; the rule in prose alone is ~70%.

Every harness needs its own row in the scaffold's gate enumeration. If the user inventoried Cursor and Codex but not Claude Code, do not write `.claude/hooks/*` — write the Codex sandbox config and the CI gate.

## Why it matters for agents

- **Prose achieves ~70% compliance; hooks enforce at 100%.** "CLAUDE.md instructions get followed
  about 70% of the time; hooks enforce rules at 100%." Any constraint that matters for safety or
  correctness must live in a hook, not an instruction file. (W3 — dominant warning)
- **Single-agent topology safety depends on gates.** Without gates, the Cognition-recommended
  linear agent has no structural backstop between a model decision and an irreversible action. (W4)
- **Missing ask-first tier causes binary failure.** Agents with only free-action and forbidden
  tiers either over-restrict or barge into irreversible operations. The ask-first tier is the
  escape valve that prevents both.
- **Gates and sandbox compose.** PreToolUse blocks at the harness layer; the container sandbox
  blocks at the OS layer. Neither alone is sufficient; together they are defense-in-depth. (W10)
- **Linters as direction.** PostToolUse format-on-write means the agent always sees linted output
  regardless of whether model followed style instructions — structural enforcement over prose.

## Heuristics by intent

### assess

- **H1.** Audit whether forbidden actions (`rm -rf`, force-push to main, prod-DB writes, disabling
  sandbox controls) are blocked by a PreToolUse hook with exit code 2 — or only mentioned in
  AGENTS.md prose. Prose compliance is ~70%; any forbidden-tier action that lives only in prose is
  effectively unprotected. (severity cap: 4; lens: adversarial)
- **H2.** Verify an ask-first tier exists and is documented. List the specific action classes that
  require user approval: DB migrations, dependency changes, secret-handling edits, new external
  network destinations. Absence of this tier is the single most common cause of agents performing
  irreversible actions without confirmation. (severity cap: 4; lens: maintainer)
- **H3.** Check whether linters and formatters are wired to PostToolUse hooks or only referenced
  in prose. "Always run prettier before committing" in CLAUDE.md will be skipped ~30% of the time;
  a PostToolUse hook on file write runs every time. (severity cap: 3; lens: cold-agent)
- **H4.** Verify that failing commands are documented alongside working ones — not just the happy
  path. An agent that encounters an undocumented error falls back to guessing; an agent that finds
  the error and its workaround in the instruction surface continues correctly. (severity cap: 3;
  lens: cold-agent)
- **H5.** Confirm CI gates mirror hook-layer gates. If a PreToolUse hook blocks force-push to main,
  branch protection rules should enforce the same constraint independently — so the gate holds even
  when the hook is bypassed or misconfigured. (severity cap: 4; lens: auditor)

### harden

- **H1.** Instruction-only forbidden actions → add a PreToolUse hook that exits with code 2.
  Pattern on shell arguments (`rm -rf`), git flags (`push --force` to `main`), and DB connection
  strings containing production identifiers. Exit code 1 signals error; only code 2 blocks.
- **H2.** No ask-first tier → enumerate the action classes, wire a PreToolUse hook that emits a
  structured approval request for each, and document the list in AGENTS.md so the agent
  anticipates the pause rather than retrying.
- **H3.** Formatter not running consistently → wire prettier / black / gofmt to a PostToolUse hook
  on `Write` and `Edit` events (Factory.ai linter-as-direction pattern). The agent always sees
  linted output, which shapes subsequent edits structurally.
- **H4.** CI gate absent for hook-protected actions → add branch protection rules and required
  status checks mirroring the PreToolUse hook. Hook layer and CI are defense-in-depth, not
  redundancy to eliminate.

### scaffold

- **Do not scaffold gates from generic templates.** Each gate must be traceable to a named action
  class in the three-tier table; a hardcoded `rm` pattern without a tier assignment is security
  theater, not a gate strategy.
- **Require the step 4.5 harness inventory.** Without it, the scaffold defaults to whichever
  harness's dotfile happens to exist — repeating the failure logged at
  `docs/agent-failures.md` entry 6 (`.claude/` present, Claude-only hook produced, other harnesses
  punted on). Refuse to scaffold gates until the inventory is collected; then produce equivalents
  per the per-harness primitives table above for every harness named.
- **H1.** Fill the three-tier table first: enumerate every action class the agent will take,
  assign a tier, identify which forbidden or ask-first actions lack a hook. Gaps are the backlog.
- **H2.** Wire PostToolUse format-on-write before PreToolUse blocks — low-risk, immediate output
  quality gain. Validate the hook fires on `Write`, `Edit`, and any MCP tool producing file output.
- **H3.** Ask-first approval payloads must be structured (tool name, arguments, rationale, risk
  tier). Unstructured "can I do X?" halts slow reviewers and get rubber-stamped.
- **H4.** Document failing commands alongside working ones in AGENTS.md using the format:
  `command → expected failure → workaround → status`. Agents that find documented dead ends skip
  re-discovering them.
- **H5.** **A deny-list / pattern-matching hook ships with its negative-case test fixture as one
  scaffold artifact, not two.** Generate test rows for every variant of every flag in the pattern:
  split short flags (`-r -f` vs `-rf`), long-form aliases (`--recursive`, `--force`), `=` forms
  (`--force-with-lease=ref`), `--` option terminator, transparent wrappers (`sudo`, `time`, `env`,
  `command`, `git -C path`), and env-var prefixes (`FOO=bar cmd …`). The hook landing without
  tests is the regression vector logged at `docs/agent-failures.md` entry 7 of any repo that has
  tracked this. The post-write auditor (workflow step 8.5) treats this heuristic as `applied`
  only when both the hook and its test fixture are in the diff and the fixture covers the variant
  matrix.
- **H6.** **Prefer argv parsing (`shlex`-tokenized) over regex-on-string for hook predicates.**
  Regex deny-lists have a long bypass tail: refspec forms (`git push -f origin HEAD:main`),
  `+`-refspec force-updates (`git push origin +main` with no `-f` flag), option terminators
  (`rm -rf -- /etc`), and long-form aliases are all common idioms that don't hit a string regex.
  Tokenize, split pipelines on `;` / `&&` / `||` / `|` / `&`, unwrap wrappers, then inspect argv.
  Regex is acceptable only for the trivial cases (single flag, single target form) and even there
  the test fixture from H5 is required.

### diagnose

- **H1.** Forbidden action executed despite AGENTS.md → rank: (1) no PreToolUse hook exists —
  prose ~70% (W3); (2) hook exits code 1, not 2 — only code 2 blocks; (3) hook pattern misses
  the variant used; (4) hook not registered in harness config.
- **H2.** Agent halts excessively for approval → rank: (1) free-action classes misclassified as
  ask-first; (2) hook fires on read-only operations; (3) unstructured payload inflates reviewer
  latency. Fix: tighten predicate and add structured approval payloads.
- **H3.** Linter not running on agent files → rank: (1) PostToolUse wired to `Bash` only, not
  `Write`/`Edit`; (2) formatter exits non-zero and error is swallowed; (3) hook targets wrong
  extension. Fix: widen event filter and add hook-level error logging.
- **H4.** CI catches what the PreToolUse hook missed → hook predicate is incomplete; treat each
  CI-caught violation as a missing hook test case.

## Empirical warnings

- **W3 (dominant)** — CLAUDE.md and AGENTS.md instructions are followed ~70% of the time; hooks
  enforce at 100%. Any constraint that matters for safety, correctness, or style must live in a
  hook. "Write clean code" in prose is aspirational; a PostToolUse lint hook is structural.
- **W4** — Gates are how single-agent topologies stay safe without multi-agent handoffs. A linear
  agent with no hooks has no structural backstop; the gate layer is the boundary between agent
  decision and irreversible action.
- **W10** — Gates and sandbox policy compose. A PreToolUse hook blocks at the harness layer; a
  container sandbox blocks at the OS layer. Hooks alone do not prevent a compromised process from
  acting outside the harness; sandbox isolation closes the gap.

## Canonical examples

- **Claude Code PreToolUse/PostToolUse hooks** — PreToolUse with exit code 2 is the only
  harness-native hard-block primitive; PostToolUse for format-on-write is the reactive pattern.
- **Aider auto-lint and auto-test** — lint and test wired to every edit cycle; the agent always
  iterates on linted output, making linters direction rather than style decoration.
- **Factory.ai "Using Linters to Direct Agents"** — linters wired to write-time hooks shape
  agent behavior; every output the agent sees is already conformant, which changes what it produces.
- **Copilot "explicitly indicate which commands work"** — document failing commands, errors, and
  workarounds alongside working commands so agents skip re-discovering known dead ends.

## Templates

Concrete starting points for the `scaffold` heuristics above. Copy from
`templates/artifacts/gates/`, fill `<placeholder>` markers, then commit:

- `pretooluse-hook.py` — argv-parsed deny-list skeleton (scaffold H1, H6). Ships with working
  predicates for `rm`-of-protected-paths and force-push-to-main as examples; delete predicates
  that don't apply, add new ones from your three-tier table.
- `pretooluse-hook-test.py` — variant-matrix test fixture (scaffold H5). Required: hook and
  tests are one scaffold artifact, not two.
- `claude-settings.json` — hook registration block (Claude Code only; other harnesses use their
  own registration mechanism — see the per-harness primitives table).
- `ci-static-checks.yml` — path-based, all-lanes CI workflow snippet (scaffold H4, mirrors the
  hook layer per W10).

## Sources

- "Harness Engineering: Leveraging Codex in an Agent-First World" — `--ask-for-approval` as the
  ask-first tier primitive; hook-layer enforcement as the basis for the three-tier boundary.
- "OWASP LLM and Agent Top 10" — tool abuse and privilege escalation; approval classes by action
  type and least-privilege tool surfaces as baseline controls.
- "AI Risk Management Framework (and Generative AI Profile)" — approval matrices by action/risk
  class; human-in-the-loop for high-risk tiers; audit logging for hook overrides.
- "Don't Build Multi-Agents" — single-threaded linear agents as the safe default; gates are what
  make that topology safe without multi-agent handoff complexity.

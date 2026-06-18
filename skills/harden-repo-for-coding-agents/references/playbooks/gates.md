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
| **ask-first** | Agent must request user approval before proceeding | DB migrations, dependency changes, changes to public API/interface/schema (“design rules”), secret-handling edits, new external network destinations |
| **forbidden** | Hard-blocked at the hook layer, no override path | `rm -rf`, force-push to main, prod-DB writes, disabling sandbox controls |

Linters and formatters wired to PostToolUse write-time hooks shape agent output structurally —
Aider's auto-lint and auto-test and Factory.ai's linter-as-direction pattern both demonstrate this.

### Per-harness gate primitives

Different harnesses expose different enforcement points. **Scaffold per-harness equivalents for every harness in the step 4 inventory** — not just the one whose dotfile happens to exist.

| Harness | Hard-block primitive (forbidden) | Approval primitive (ask-first) | Reactive primitive (lint-on-write) | Notes |
|---|---|---|---|---|
| **Claude Code** | `PreToolUse` hook exit 2 (`.claude/settings.json` + `.claude/hooks/*`); use `$CLAUDE_PROJECT_DIR` in the command so CWD drift can't break self-resolution | `PreToolUse` hook structured payload | `PostToolUse` hook on `Write`/`Edit` | Native non-bypassable hard-block at the harness layer. |
| **Cursor** | `preToolUse` hook exit 2 (`.cursor/hooks.json` + `.cursor/hooks/*`) — matcher is `Shell` (not `Bash`); set `"failClosed": true` to block on hook errors. Use `$CURSOR_PROJECT_DIR` in the command. Project `.cursor/` layer must be trusted on first run. | Same hook with structured payload | None native; relies on file-watcher / pre-commit | Per `cursor.com/docs/hooks` (Jan 2026). `$CLAUDE_PROJECT_DIR` is aliased for compatibility. |
| **Codex** | `PreToolUse` hook exit 2 (`.codex/hooks.json` + `.codex/hooks/*`) — matcher is `Bash`. Codex does not document a project-dir env var; use `$(git rev-parse --show-toplevel)` in the command (OpenAI's recommended pattern). Project `.codex/` layer must be trusted on first run. Sandbox policy + `--ask-for-approval` tiering layer on top. | `--ask-for-approval` modes (`untrusted` / `on-failure` / `on-request` / `never`) plus hook structured payload | None native; relies on Codex shell tool calls in the wrapped run | Hook layer is harness-native; sandbox layer is OS-layer defense-in-depth. Per `developers.openai.com/codex/hooks` (2026). |
| **Aider** | None native — prose + `--read-only` files | `--auto-commits false` (manual approval per commit) | `--lint-cmd` and `--test-cmd` run after every edit cycle | Lint-as-direction is Aider's strongest primitive. |
| **Copilot** — inline (prose-only) vs cloud agent (sandboxed) | Inline: none native (CI-only). Cloud agent: isolated GitHub Actions sandbox — no direct push to `main`, network restrictions | PR review is the approval point (the agent opens a PR) | Workflow `actions/*` checks on the agent branch | Not uniformly prose-only: the cloud coding agent has native sandbox / network / no-main-push boundaries + scoped MCP access. `copilot-instructions.md` is prose. |
| **Windsurf** | None native (W3) — `.windsurf/rules/*.md` with `trigger: always_on` is prose | None native | None native | 12 k-char workspace rule cap; behave like Cursor for enforcement purposes. |
| **AGENTS.md-only** (Jules, Amp, etc.) | None — prose-only | None | None | CI is the only structural enforcement; treat the harness layer as advisory. |

**Implication.** A `forbidden`-tier rule like *"never force-push to main"* needs:
- Claude Code, Cursor, Codex: `PreToolUse` hook (exit 2) at the harness layer, with project-root-prefixed hook path so CWD drift can't wedge the hook (`$CLAUDE_PROJECT_DIR` / `$CURSOR_PROJECT_DIR` / `$(git rev-parse --show-toplevel)`).
- Codex (defense-in-depth): sandbox network/process policy on top of the harness hook.
- Windsurf / Aider / Copilot / AGENTS.md-only: **CI branch protection** is the load-bearing gate; the rule in prose alone is ~70%.

A shared harness-agnostic policy script (see this repo's `scripts/hooks/destructive_bash_policy.py`) loaded by thin per-harness adapters under `.claude/hooks/`, `.codex/hooks/`, and `.cursor/hooks/` keeps the three configurations from drifting. The policy must recognize both `Bash` (Claude Code, Codex) and `Shell` (Cursor) tool names.

Every harness in the inventory needs its own row in the scaffold's gate enumeration. If the user inventoried Cursor and Codex but not Claude Code, do not write `.claude/hooks/*` — write the `.cursor/hooks/*` and `.codex/hooks/*` adapters plus the CI gate.

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
- **Architectural boundaries need gates too.** If the repo relies on boundaries (dependency
  direction, “no cycles”, forbidden imports across layers), enforce them with static checks
  (lint/tests/CI). Don’t rely on the agent to reason about coupling correctly in noisy contexts.

## Heuristics by intent

### assess

- **H1.** Audit whether forbidden actions (`rm -rf`, force-push to main, prod-DB writes, disabling
  sandbox controls) are blocked by a PreToolUse hook with exit code 2 — or only mentioned in
  AGENTS.md prose. Prose compliance is ~70%; any forbidden-tier action that lives only in prose is
  effectively unprotected. (severity cap: 4; lens: adversarial)
- **H2.** Verify an ask-first tier exists and is documented. List the specific action classes that
  require user approval: DB migrations, dependency changes, secret-handling edits, new external
  network destinations, and changes to design-rule artifacts (public APIs, shared schemas/types).
  Absence of this tier is the single most common cause of agents performing irreversible actions
  without confirmation. (severity cap: 4; lens: maintainer)
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
- **H6.** Check for architecture boundary gates: dependency-direction rules, cycle detection, and
  forbidden imports between layers/modules. If boundaries exist only as prose, violations will
  recur. (severity cap: 3; lens: maintainer)
- **H7.** If the org expects parallel multi-agent work, check whether the repo has **stable
  contracts (“design rules”)** that make parallelism real — and whether those contracts are
  protected by gates. Look for: (1) named module boundaries + a dependency rule, (2) explicit
  interface/schema ownership (CODEOWNERS / required reviewers), (3) boundary checks (forbidden
  imports / cycles) and interface-compatibility checks in CI, and (4) integration tests that fail
  fast when contracts drift. Without these, “4 agents in parallel” mostly means “4 agents
  colliding on shared files.” (severity cap: 3; lens: auditor)

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
- **H5.** Multi-agent parallelization desired → promote design rules to first-class gate targets:
  (1) define “design rules” artifacts (public interfaces, schemas, shared types, architectural
  boundaries), (2) require review/approval for edits to those artifacts (CODEOWNERS + branch
  protection), (3) enforce boundaries via lint/tests/CI (forbidden imports, dependency direction,
  no cycles), and (4) add contract/integration tests so modules can be edited independently while
  staying compatible.

### scaffold

- **Do not scaffold gates from generic templates.** Each gate must be traceable to a named action
  class in the three-tier table; a hardcoded `rm` pattern without a tier assignment is security
  theater, not a gate strategy.
- **Require the step 4 harness inventory.** Without it, the scaffold defaults to whichever
  harness's dotfile happens to exist — repeating the failure logged at
  `docs/reflection-log/2026-05-16-gates-scope-inferred-from-dotfile-presence.md` (`.claude/`
  present, Claude-only hook produced, other harnesses punted on). Refuse to scaffold gates until
  the inventory is collected; then produce equivalents per the per-harness primitives table
  above for every harness named.
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
  scaffold artifact, not two.** The fixture's variant matrix MUST cover every category below;
  rounds 1 and 2 of automated PR review on this repo (failure-log entries 7 and 8) each surfaced
  bypasses in categories the previous round didn't cover. Encode the matrix when the fixture is
  first scaffolded, not when each bypass is reported:
  1. **Flag forms** — single short (`-rf`), split short (`-r -f`), long-form alias
     (`--recursive`), `=` form where applicable (`--force-with-lease=ref`), `--` terminator.
  2. **Path traversal** — `..` segments resolving to a protected dir (`rm -rf /tmp/../etc`).
     The hook must canonicalize (`os.path.normpath`) before the protected-dir check.
  3. **Shell variable expansion** — `$VAR`, `${VAR}`, with and without trailing path components
     (`rm -rf ${HOME}/Documents`).
  4. **Command substitution** — `$(...)`, backticks, `<(...)`, `>(...)`, and nested forms
     (`echo $(echo $(rm))`). The hook must extract these and recursively check the body.
  5. **Multi-line commands** — real newlines as command separators (`echo ok\nrm -rf /etc`).
     `whitespace_split=True` strips newlines unless they're pre-processed into `;` outside quotes.
  6. **Transparent wrappers** — bare (`sudo rm`), wrapper with separate-token flag value
     (`sudo -u root rm`), `=` form (`sudo --user=root rm`), multiple value-flags. Maintain a
     per-wrapper set of value-taking flags so the wrapper unwrap consumes them.
  7. **Env-var prefixes** — single, multiple, and via `env` builtin (`FOO=bar cmd`).
  8. **Compound statements** — dangerous command in the second pipeline segment, for each
     separator (`;`, `&&`, `||`, `|`, `&`).
  9. **Quoted paths** — dangerous target quoted.
  10. **Tool-level global options with separate-token values** — e.g., `git --work-tree /path
      push …` must still dispatch to the `push` predicate; `check_git` must consume the value
      after `--work-tree`, `--git-dir`, `-C`, `-c`, and similar.
  11. **Relative path traversal** — `rm -rf ../../etc` resolves to a protected dir from a
      knowable cwd; blocked even when cwd is unknown via the `..`-escape rule. Combined with
      cwd tracking across pipeline segments: `cd / && rm -rf etc` must resolve the relative
      target to `/etc` and block.
  12. **Wrapper flag-values that carry commands** — `env -S 'rm -rf /etc'` and
      `env --split-string='git push -f origin main'` pack a command into the `-S` value;
      the hook must recursively inspect that value, not consume it as opaque.
  13. **Shell launchers with `-c` payloads** — `bash -c "rm -rf /etc"`, `sh -c "…"`,
      combined-flag forms like `bash -lc "…"`, and `--command="…"` long-form must extract
      the command-string value and recursively check it. Without this, the dispatcher sees
      `bash` (not in the deny-list) and allows the segment.

  The hook landing without the test fixture is the regression vector logged at
  `docs/reflection-log/2026-05-16-hook-regex-bypasses-round1.md`; the fixture landing without
  exhaustive variant categories is the regression vector logged at
  `docs/reflection-log/2026-05-16-hook-argv-bypasses-round2.md` and
  `docs/reflection-log/2026-05-16-hook-path-cwd-bypasses-round3.md`. The post-write auditor
  (workflow step 8) treats this heuristic as `applied` only when both the hook and its test
  fixture are in the diff and the fixture covers all 13 categories above.

- **H6.** **Prefer argv parsing (`shlex`-tokenized) over regex-on-string for hook predicates.**
  Regex deny-lists have a long bypass tail: refspec forms (`git push -f origin HEAD:main`),
  `+`-refspec force-updates (`git push origin +main` with no `-f` flag), option terminators
  (`rm -rf -- /etc`), long-form aliases, path traversal, command substitution, and wrapper
  option values are all common idioms that don't hit a string regex. Tokenize via `shlex`
  with `punctuation_chars=True`, split pipelines on `;` / `&&` / `||` / `|` / `&`, pre-process
  newlines into `;` outside quotes, extract command substitutions for recursive checking, and
  unwrap wrappers (consuming their value-taking flags). Regex is acceptable only for the
  trivial cases (single flag, single target form) and even there the test fixture from H5 is
  required.

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
- **H5.** Agent repeatedly violates architectural boundaries → rank: (1) no boundary checks exist
  (dependency direction, forbidden imports, cycle detection); (2) checks exist but are not required
  in CI; (3) boundary model is ambiguous — use `architecture-design` to define the boundary model,
  then gate it.

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

## Implementation options (non-exhaustive)

Enforce boundary/interface contracts with either **lint** (fast) or **tests** (richer). Pick one
per constraint; make it CI-required.

### Boundary / dependency rules

- **Java/Kotlin/JVM**: ArchUnit architecture tests (layered rules, forbidden dependencies).
- **Python**: Import Linter “layers” contracts (forbidden imports between layers).
- **JS/TS**:
  - Nx `@nx/enforce-module-boundaries` (project graph + tag constraints).
  - `dependency-cruiser` (forbidden dependency rules; circular dependency detection).
  - `eslint-plugin-boundaries` (folder-based import allow/deny constraints).

### Contract / interface compatibility

- **Consumer-driven contracts**: Pact (consumer tests emit contracts; provider verification runs in CI).
- **HTTP API contracts**: OpenAPI linting + contract tests (e.g., schema checks in CI; gateway tests).
- **Schema compatibility**: enforce backward/forward compatibility for shared schemas (e.g., Protobuf/Avro)
  as a required check when a schema is a design rule.

## Sources

- "Harness Engineering: Leveraging Codex in an Agent-First World" — `--ask-for-approval` as the
  ask-first tier primitive; hook-layer enforcement as the basis for the three-tier boundary.
- "OWASP LLM and Agent Top 10" — tool abuse and privilege escalation; approval classes by action
  type and least-privilege tool surfaces as baseline controls.
- "AI Risk Management Framework (and Generative AI Profile)" — approval matrices by action/risk
  class; human-in-the-loop for high-risk tiers; audit logging for hook overrides.
- "Don't Build Multi-Agents" — single-threaded linear agents as the safe default; gates are what
  make that topology safe without multi-agent handoff complexity.
- "Design Rules: The Power of Modularity" — design rules (stable interfaces/APIs/standards) as a
  precondition for parallel work; integration/testing protocols as part of the visible contract.
- "Design Rule Hierarchies and Parallelism in Software Development Tasks" — design-rule layers
  predict parallelizable work vs coordination requirements; motivates partitioning work beneath
  stable design rules and enforcing cross-layer dependencies.
- "Hierarchical Evaluation of Software Design Capabilities of Large Language Models of Code" —
  coupling reasoning brittleness under noise; motivates structural boundary enforcement rather than
  relying on agent reasoning.

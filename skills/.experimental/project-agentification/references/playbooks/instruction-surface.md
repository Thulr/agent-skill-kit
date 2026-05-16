# instruction-surface

## What it is

The instruction-surface covers the files a harness loads at session start to orient the agent:
`AGENTS.md` (Agentic AI Foundation / Linux Foundation; cross-harness portable layer), `CLAUDE.md`
(Anthropic; auto-injected by Claude Code), `.cursor/rules/*.mdc` (four activation modes:
Always Apply / Auto Attached glob-scoped / Agent Requested description-matched / Manual),
`.windsurf/rules/*.md` (Wave 8+; `trigger: always_on | manual | model_decision | glob`, 12 k-char
cap), `.github/copilot-instructions.md` (Copilot IDE primary), and `AGENTS.override.md` (Codex;
ephemeral local override). Discovery is hierarchical: root-to-leaf walk, closest file wins.
openai/codex ships ~88 nested `AGENTS.md` files as the reference monorepo pattern; vercel/next.js
symlinks `CLAUDE.md → AGENTS.md` to eliminate drift between harness-specific and portable layers.

**`README.md` is also part of this surface.** Copilot loads it explicitly; Claude Code and Cursor
commonly read it on first invocation; agent-aware harnesses fall back to it when no AGENTS.md /
`.cursor/rules` / etc. exists. In a repo that hasn't reached the W1 ≥3-failures threshold to
hand-curate an AGENTS.md yet, `README.md` is the **only** always-loaded prose surface the agent
sees — which makes it the load-bearing discoverability point for the reflection log (e.g.
`docs/agent-failures.md`). Once AGENTS.md lands, it absorbs the discoverability and README's
agent-facing role shrinks to "see AGENTS.md."

## Why it matters for agents

- **Context rot at scale.** LLMs follow instructions on the periphery of the prompt most reliably;
  a long, stale root file silently degrades mid-context rules — the dominant failure in all
  multi-rule harnesses (see W2, W8).
- **Instruction-following decay.** HumanLayer's empirical finding: as rule count grows, the model
  stops ignoring the new rules and begins ignoring all rules uniformly; instruction surface bloat
  is therefore non-linear in its damage (see W2).
- **Harness drift without symlinks.** When `CLAUDE.md` and `AGENTS.md` diverge, agents get
  conflicting ground truth and hallucinate which file is authoritative (see W8).
- **Injection attack surface.** Prompt Security demonstrated data exfiltration via a malicious
  `AGENTS.md`; instruction files are reviewed at a lower bar than source code despite being
  executed by every agent session (see W5).

## Heuristics by intent

### assess

- **H1.** Check whether the root `AGENTS.md` or `CLAUDE.md` exceeds 200 lines — quality degrades
  sharply above 300 because the harness already injects ~50 system instructions before the file
  is seen. (severity cap: 3; lens: cold-agent)
- **H2.** Verify Cursor `.mdc` frontmatter uses the correct activation mode (`alwaysApply`,
  `globs`, `description`, or manual) — wrong mode silently prevents rule injection even when
  the file exists. (severity cap: 2; lens: cold-agent)
- **H3.** Confirm a "trust these instructions" clause appears near the top — Copilot's official
  guidance states this reduces re-exploration tool-call overhead; absence is measurable by
  tool-call count per task. (severity cap: 2; lens: cold-agent)
- **H4.** Audit whether forbidden / ask-first / free-action tiers are explicitly defined or rely on
  prose the agent may ignore ~30% of the time; hard gates live in hooks/sandbox, not instruction
  files. (severity cap: 4; lens: maintainer)
- **H5.** Check `AGENTS.md` and any instruction file for injection-bait patterns — `<!-- ignore
  previous instructions -->` or external URL references the model might follow — treating the file
  as code under review, not documentation. (severity cap: 4; lens: adversarial)
- **H6.** Verify that nested subdirectory `AGENTS.md` files don't repeat global conventions
  already in the root — redundancy inflates the always-loaded token budget and the closest-wins
  merge produces no benefit for duplicate rules. (severity cap: 2; lens: auditor)

### harden

- **H1.** Auto-init producing bloated boilerplate → delete the file and hand-author from a list of
  observed agent failures, referencing `references/empirical-warnings.md#W1` in a comment at the
  top of `AGENTS.md`.
- **H2.** `CLAUDE.md` / `.github/copilot-instructions.md` content drift → **all three actions
  required as a single unit; partial application is the failure mode** (see
  `docs/agent-failures.md` entry 5 in any repo that has tracked this miss):
  1. `ln -sf AGENTS.md CLAUDE.md` at repo root.
  2. `ln -sf ../AGENTS.md .github/copilot-instructions.md`.
  3. A CI / static-check step that asserts both files are symlinks pointing at the correct
     target and that the target resolves — fails the build on divergence. Step 1 + 2 without
     step 3 decays the moment a contributor "fixes" a symlink to a regular file. The post-write
     auditor (workflow step 8.5) treats this heuristic as `applied` only when all three are
     present.
  Add a one-line declaration to `AGENTS.md` so future agents do not try to "fix" the divergence
  by editing `CLAUDE.md` directly: *"`CLAUDE.md` is a symlink to `AGENTS.md`. Edit `AGENTS.md`
  only."*
- **H3.** Agent re-explores repo on every task despite instruction file presence → add a
  "trust these instructions" clause at line 1 of `AGENTS.md`: *"Trust the instructions here;
  only search further if you find an explicit gap."*
- **H4.** Instruction file is an attack surface (malicious PR injects rules) → add a
  `PreToolUse` hook that blocks writes to `AGENTS.md`, `CLAUDE.md`, and `.cursor/rules/` without
  explicit approval; treat these files as write-protected in the harness (Kilo Code default).
- **H5.** Monorepo agents editing the wrong subpackage → add per-package `AGENTS.md` at each
  module boundary with a `## Scope` line declaring what this file governs; Codex root-to-leaf
  merge picks the nearest; `AGENTS.override.md` handles ephemeral local overrides.
- **H6.** Windsurf rule silently dropped → verify `trigger` frontmatter is valid
  (`always_on | manual | model_decision | glob`) and file is under `.windsurf/rules/` not
  deprecated `.windsurfrules`; enforce the 12 k-char workspace / 6 k global size cap.

### scaffold

- **Do not autogenerate from boilerplate or `/init`.** Mündler et al. (arXiv:2602.11988) found
  autogenerated context files drop task success ~3% and inflate cost >20%. Every instruction file
  must cite at least 3 observed agent failures (the W1 floor) — no placeholder rules, no generic "write clean
  code" copy.
- **H1.** Structure the root `AGENTS.md` as `WHAT / WHY / HOW` — tech stack + repo map (WHAT),
  architectural intent (WHY), build/test/verify commands (HOW). Skip anything a linter or
  formatter already enforces; that constraint belongs in a hook, not prose.
- **H2.** Front-load the highest-priority constraints in the first 20 lines. LLMs follow
  peripheral instructions most reliably; security rules and forbidden-action tiers go at the top.
- **H3.** Choose the narrowest Cursor activation mode: `globs` for file-type scope,
  `description` for agent-requested capabilities, `alwaysApply: true` only for repo-wide
  invariants. Never make every rule `alwaysApply`.
- **H4.** Keep the root file ≤100 lines; push depth into hierarchical nested `AGENTS.md` per
  subdirectory, skills (progressive disclosure, ~100-token metadata at startup), ADRs, and a
  structured `docs/` tree the file points to — not a table of contents that duplicates them.
- **H5. Bootstrap discoverability when no AGENTS.md exists yet.** The W1 floor (≥3 observed
  failures before hand-curating AGENTS.md) creates a Stage-0 interim where the reflection log
  exists but AGENTS.md does not. In that interim, `README.md` is the only always-loaded prose
  surface most harnesses see, so it must carry an agent-facing pointer to the reflection log
  (typically a short `§Authoring` / `§Agents` section: "When an AI coding agent trips on this
  repo, record it in `docs/agent-failures.md`. Three entries describing the same gap is the
  threshold for adding a rule, hook, or AGENTS.md sentence to close it."). Without that
  pointer, the log lands as an orphan on disk. **Apply order:** reflection log + README pointer
  land **first** (Stage 0); AGENTS.md lands **only after** the W1 floor is met and absorbs the
  pointer into its own §Failure-log section. Never scaffold AGENTS.md without the Stage-0
  substrate; never scaffold the reflection log without the README pointer.

- **H1.** Agent ignores a rule from the instruction file → rank hypotheses: (1) file exceeds 200
  lines and the rule is in the middle (W2: "lost in the middle" decay); (2) Cursor rule has wrong
  activation mode — `description`-matched rule not triggered because agent didn't request it;
  (3) rule conflicts with a harness system prompt injected before the file; (4) file was not
  discovered because it's not on the nearest-ancestor path.
- **H2.** Agent wastes tool calls re-reading the repo on every task → hypotheses: (1) no
  "trust these instructions" clause; (2) the file's HOW section is incomplete — agent can't find
  the test/build command and falls back to search; (3) nested `AGENTS.md` is present but the root
  file doesn't declare the hierarchical structure.
- **H3.** Harness-specific file and `AGENTS.md` produce conflicting output → hypotheses:
  (1) `CLAUDE.md` is not symlinked to `AGENTS.md` and has drifted; (2) Codex is reading
  `AGENTS.override.md` left over from a previous session; (3) a global `~/.codex/AGENTS.md`
  overrides the repo-level file for a developer who forgot it existed.
- **H4.** Security-sensitive rule consistently violated by the agent → do not add more prose;
  the instruction-following rate for file-based rules is ~70% (W3). Move the constraint to a
  `PreToolUse` hook with exit code 2 (hard block) or a CI gate; treat the continued violation as
  evidence that the rule belongs in the gates sub-surface, not this one.

## Empirical warnings

- **W1** — Autogenerated `AGENTS.md` drops task success ~3% and inflates cost >20%; hand-curate
  from observed failures only.
- **W2** — File exceeding 200 lines degrades instruction-following uniformly; push depth into
  hierarchical files and skills.
- **W3** — Instruction-file rules followed ~70% of the time; enforcement-grade constraints require
  hooks, not prose.
- **W5** — `AGENTS.md` and skills are injection attack surfaces; review and write-protect at the
  same bar as source code.
- **W7** — `AGENTS.md` wins for global always-on context (Vercel: 100% vs 79% for skills); skills
  win for capability-specific progressively-disclosed workflows — don't conflate the two surfaces.
- **W8** — Empirical evidence is mixed; hand-curate, keep short, evolve from observed failures,
  prefer hierarchical disclosure over a single long file.

## Canonical examples

- **openai/codex** — root + ~88 nested `AGENTS.md` files; reference monorepo-scale hierarchical
  composition; copy the imperative do/don't style and sandbox-constraint placement at the top.
- **vercel/next.js** — `CLAUDE.md` is a symlink to `AGENTS.md`; copy the symlink pattern and the
  explicit scope declaration: *"Note: CLAUDE.md is a symlink to AGENTS.md. They are the same file."*
- **temporalio/sdk-java** — terse, imperative, single-purpose: three rules, all commands, no
  narrative; copy this as the floor for "minimum viable AGENTS.md."

## Templates

Concrete starting points for the `scaffold` heuristics above. Copy from
`templates/artifacts/`, fill `<placeholder>` markers, then commit:

- `templates/artifacts/instruction-surface/AGENTS.md` — WHAT/WHY/HOW skeleton (scaffold H1–H4).
- `templates/artifacts/instruction-surface/README-agents-section.md` — Stage-0 pointer block (scaffold H5).
- `templates/artifacts/instruction-surface/check-instruction-surface.sh` — symlink-drift static check (harden H2).
- `templates/artifacts/reflection-log/agent-failures.md` — the substrate Stage 0 lands first (SKILL.md §Bootstrap order).

## Sources

- "AGENTS.md" — Agentic AI Foundation (Linux Foundation); canonical spec for vendor-neutral
  hierarchical instruction discovery and root-to-leaf merge semantics.
- "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" —
  Mündler et al. (ETH Zürich / LogicStar.ai, arXiv:2602.11988); empirical basis for W1 and the
  no-autogenerate guard.
- "Effective Context Engineering for AI Agents" — Anthropic; token-budget framing, peripheral
  instruction reliability, smallest-high-signal-token principle.
- "Engineering Agents — Harness Assessment" — Engineering Agents; Level 1–5 maturity rubric;
  "weakest discipline is your ceiling"; AGENTS.md as Level 2 ceiling without enforcement.

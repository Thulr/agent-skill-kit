<!-- AGENTS.md template — informed-skills / project-agentification scaffold.
     Sub-surface: instruction-surface. Heuristics: scaffold H1 (WHAT/WHY/HOW),
     H2 (front-load constraints), H4 (≤200 lines per W2), H5 (bootstrap order).

     W1 compliance: every section must trace to at least one row in
     `docs/agent-failures.md`. Sections without a failure source are not
     mergeable — delete them. Do NOT autogenerate the contents of any
     section from boilerplate. Hand-curate.

     Strip all `<!-- ... -->` template comments before committing. -->

# AGENTS.md — <project-name>

<!-- 1-2 sentence positioning. What this project is, who reads this file,
     why the rules exist. Should be self-contained for a cold-context agent. -->

<one-line project description>. <Why agents read this file: e.g., "every PR to
`src/` or `tests/` is treated as a release artifact, not internal scaffolding.">

This file is hand-curated from observed agent failures recorded in
[`docs/agent-failures.md`](./docs/agent-failures.md). Do **not** autogenerate
it (`/init`, `/Generate Cursor Rules`, etc. — see W1 in any agent-readiness
reference). Every rule below traces back to a log entry; to add a rule, log
the failure first.

<!-- If CLAUDE.md and .github/copilot-instructions.md are symlinks to this
     file (per instruction-surface H2-harden), keep the next block. Otherwise
     delete it. -->

> **`CLAUDE.md` and `.github/copilot-instructions.md` are symlinks to this file.**
> Edit `AGENTS.md` only — the symlinks update automatically. The check at
> `<scripts/check-instruction-surface.sh>` fails the build if either symlink
> is missing or divergent.

## WHAT — repo map and tech stack

<!-- One section per top-level directory the agent should know about.
     Keep terse: 1-2 lines per directory. Skip what a `tree` or `ls -R` shows. -->

- `<dir1>/` — <what lives here, why it's distinct from `dir2/`>.
- `<dir2>/` — <...>.

Tech stack: <languages, frameworks, runtimes, package managers in use>.

## WHY — architectural intent

<!-- Constraints and invariants that aren't visible from the code.
     If a constraint is enforceable, push it to a hook or CI gate (W3). -->

- <Invariant 1 — e.g., "All public APIs are versioned; never break v1.">
- <Invariant 2>

## HOW — commands

<!-- Build, test, lint, format. The COMMANDS an agent should run, not how
     they were chosen. Skip anything a linter/formatter already enforces. -->

- `<build command>` — <what it does>.
- `<test command>` — <what it does; how to interpret failures>.
- `<lint command>` — <what it does>.

## Load-bearing rules

<!-- Each rule MUST cite a `docs/agent-failures.md` row. No rule without a
     failure source. Number rules so commits and reviewers can reference
     them: "Rule 4 covers entry 7 in the failure log." -->

### Rule 1 — <one-line title> (log entry <N>)
<2-4 sentences. State the rule. State why agents trip without it. State
exactly what to do (a path, a flag, a command).>

### Rule 2 — <title> (log entry <N>)
<...>

## Forbidden actions (hook-enforced)

<!-- Mirror exactly what your PreToolUse hook blocks. If a forbidden action
     lives only in prose, it's ~70% enforced (W3) — move it to a hook. -->

The PreToolUse hook at [`<path/to/hook>`](./path/to/hook) rejects, with
non-zero exit:

- <Action 1 — e.g., "git push --force / -f / --force-with-lease[=...] to main">.
- <Action 2>.

<List the per-harness equivalents for every harness in the step 4.5 inventory,
referencing `templates/artifacts/gates/` for each.>

## Failure-log workflow

<!-- This section anchors the W1 feedback loop. Required. -->

When an agent trips on this repo:

1. Append a row to [`docs/agent-failures.md`](./docs/agent-failures.md) — date,
   harness, task, what happened, smallest gap.
2. **Three or more entries describing the same gap** = pattern. Open an issue
   tagged `agent-surface` and propose the smallest change that closes it.
3. Reference the log row in the commit message that closes the gap.

The three-entry floor is W1 (LogicStar/ETH Mündler et al.): scaffolding from
fewer than three observed failures produces plausible boilerplate that hurts
agent success ~3% on average.

## Ownership and review

<!-- Mirror the CODEOWNERS lanes here so agents know who reviews what. -->

- [`.github/CODEOWNERS`](./.github/CODEOWNERS) — required reviewers on
  <paths>.
- Branch protection state: <"required CI + N approvals" if active;
  "is being configured — CODEOWNERS is documentation-only until enabled"
  if not. Do NOT overstate enforcement that isn't on GitHub yet.>

## Security

[`SECURITY.md`](./SECURITY.md) — incident-disclosure path. <One sentence:
what makes this repo's threat model distinct, if anything.>

## See also

- [`docs/agent-failures.md`](./docs/agent-failures.md) — the log every change
  to this file must trace back to.
- <Other references the cold-context agent will need.>

<!-- Final shape check before committing:
     - ≤200 lines total (W2).
     - Every load-bearing rule cites a log entry.
     - Symlink block present iff CLAUDE.md / copilot-instructions.md are
       symlinks (run check-instruction-surface.sh to verify).
     - Forbidden-action list matches the hook's actual rules. -->

# Reflection log

Per-entry records of observed agent failures on this repo. **This is the
source-of-truth for any future hand-curated `AGENTS.md`, hook, or new skill
rule.**

Engineering Agents — Harness Assessment calls this a *reflection log*; some
older references in this repo call it the *agent-failures log* (same thing,
renamed for source alignment).

## Recording bar vs. promotion bar

These two bars are different. The earlier single-file version of this log
conflated them, and at least one agent self-filtered entries that should have
been recorded by inheriting the high promotion bar down to recording.

- **Recording bar (low).** If you can write a non-trivial
  `## What to do differently` section, the entry is worth recording. One
  observation is enough. Do **not** filter on "is this a class / pattern /
  recurring?" at recording time — that filter belongs at the promotion step,
  not here.
- **Promotion bar (high).** Three or more entries describing the same gap is
  the threshold for scaffolding a new rule, hook, or AGENTS.md sentence to
  close it (empirical warning W1 — LogicStar/ETH Mündler et al., Feb 2026:
  scaffolding from fewer than three observed failures produces plausible
  boilerplate that hurts agent success ~3%).

When in doubt: record. Search later.

## How to add an entry

When an agent (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider, etc.)
trips in a way that wasted tokens, edited the wrong file, hallucinated a
convention, made an unsafe action, or otherwise produced a bad outcome on
this repo:

1. Copy `_template.md` to `YYYY-MM-DD-<short-slug>.md`. Use today's date
   (absolute, not "yesterday"); the slug should let `ls` show what the
   entry is about at a glance.
2. Fill the frontmatter (`date`, `harness`, `sub-surface`, `severity`,
   `status`, `related`).
3. Fill the body sections: `## What happened` (specific: file paths, commit
   SHAs, exact commands), `## What to do differently` (the smallest hook,
   rule, or gate that closes this gap — cite W1–W10 where applicable), and
   `## Closed by` (filled in later when the gap is closed).
4. Avoid blaming the model — describe the **system-level gap** (missing
   instruction, missing hook, ambiguous file, etc.).
5. Commit. No batching — one entry, one commit is fine.

## How to find patterns

The directory layout makes pattern detection a shell one-liner — no manual
table scan.

All examples scope the glob to `[0-9]*.md` — entry filenames start with a
date (`YYYY-MM-DD-…`), so the `[0-9]*` glob picks them up while excluding
`README.md` and `_template.md`, which both contain literal `sub-surface:`,
`harness:`, and `status:` strings in the schema docs and would otherwise
inflate any count.

- By sub-surface: `grep -l 'sub-surface: gates' [0-9]*.md`
- By harness: `grep -l 'harness: claude-code' [0-9]*.md`
- Open entries: `grep -l 'status: open' [0-9]*.md`
- Date-ordered list: `ls [0-9]*.md` (filenames sort chronologically)
- All entries citing a related entry: `grep -l 'related:.*2026-05-15-justfile' [0-9]*.md`

**Three or more entries with the same `sub-surface:` tag (or the same
underlying gap, even across sub-surfaces) = pattern.** Open an issue
tagged `agent-surface` and propose the smallest change (a hook, a sentence
in AGENTS.md, a CI gate) that would have closed it.

## Frontmatter schema

```yaml
---
date: YYYY-MM-DD              # ISO date, absolute
harness: claude-code          # claude-code | cursor | codex | copilot | aider | windsurf | <other>
sub-surface: instruction-surface  # instruction-surface | gates | scaffold | skills | docs-index | specs | governance | sandbox | telemetry | evals | tools | other
severity: 3                   # 0–4 per references/core/severity-rubric.md
status: open                  # open | resolved
related: []                   # list of other entry filenames (without .md), or [] if standalone
---
```

## Promotion path

- **≥3 entries describing the same gap** → open an issue tagged `agent-surface`.
- **Resolved by an instruction** → add the sentence to `AGENTS.md` (or a
  relevant `SKILL.md`); set `status: resolved` and fill `## Closed by` with
  the PR / commit SHA.
- **Resolved by a gate** → add the hook / CI check; set `status: resolved`.
- **Resolved by removing the ambiguity** → fix the underlying code, doc, or
  path; set `status: resolved`.

## Index

Filename order = chronological order. To get a table view: `ls -1 [0-9]*.md`.

## See also

- [`docs/agent-readiness-2026-05-15.md`](../agent-readiness-2026-05-15.md) — the audit that motivated creating this log.
- [`skills/evidence-driven-agent-rules/`](../../skills/evidence-driven-agent-rules/) — the skill that owns this workflow (recording-bar / promotion-bar / W1 >=3 floor / promote-pattern-to-rule).
- [`skills/_shared/empirical-warnings.md`](../../skills/_shared/empirical-warnings.md) — W2–W10 cross-cutting don'ts that govern when prose vs. gates vs. evidence-driven scaffolding is the right tool.

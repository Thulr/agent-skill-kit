---
date: 2026-05-16
harness: claude-code
sub-surface: scaffold
severity: 3
status: resolved
related: []
---
# Reflection-log recording bar conflated with promotion bar; single-file shape did not scale

## What happened

Two related failures surfaced together while operating the
project-agentification skill on a downstream project:

1. **Agent self-filtered entries that should have been recorded.** When
   reviewing observed agent failures, an agent decided several were not
   worth logging because they "weren't yet a class of failure." Its own
   self-explanation: *"The doc was doing half its job because I was
   filtering on 'is this a class of failure?' when the bar should be
   'is there a What to do differently line I can write?' Every one of these
   5 has one — and once written, future contributors searching the log can
   find the lesson by the exact symptom they're facing."* Audit of the
   template confirmed the cause: the "How to add an entry" section of
   `templates/artifacts/reflection-log/agent-failures.md` led with
   *"accrue at least three entries describing a pattern"* and *"≥3 entries
   describing the same gap"* immediately above the entry instructions,
   conflating the **recording bar** (low — one observation with a
   `Smallest gap` line is enough) with the **promotion bar** (high — ≥3
   entries before scaffolding a rule per W1).

2. **Single-file table did not scale.** A different downstream project
   reported that its `agent-failures.md` had grown to a size where the
   single-table shape was becoming unmanageable. This repo's own
   `agent-failures.md` was already showing strain at 9 entries — each row
   spans multiple visually-wrapped lines, making cross-reference and
   pattern detection hard. Checking the source
   ([Engineering Agents — Harness Assessment](https://engineeringagents.substack.com/p/the-harness-assessment-practice))
   confirmed: the source only references `REFLECTION_LOG.md` as a
   recency signal at Level 3 (*"checks whether REFLECTION_LOG.md has
   recent dates"*), it **does not** prescribe single-file vs per-incident.
   The single-file table shape was a local design choice, not source-required.

A third drift was noticed during the audit: the sub-surface and template
directory were both named `reflection-log/` (source-aligned), but the
artifact filename was `agent-failures.md` (local naming). Internal
inconsistency.

## What to do differently

Three coupled changes:

1. **Reframe the recording bar.** Lead the reflection-log README with an
   explicit "Recording bar vs. promotion bar" callout. Recording bar:
   *"if you can write a non-trivial `What to do differently` section, log
   it. One observation is enough. When in doubt: record."* Promotion bar:
   *"three or more entries describing the same gap is the threshold for
   scaffolding a rule, hook, or AGENTS.md sentence."* Apply the same
   reframe to `AGENTS.md` §Reflection-log workflow, the
   `README-agents-section.md` template, and SKILL.md §Bootstrap order.

2. **Switch to a directory layout.** Replace the single
   `docs/agent-failures.md` with `docs/reflection-log/` — one file per
   failure (`YYYY-MM-DD-<slug>.md`) with frontmatter (`date`, `harness`,
   `sub-surface`, `severity`, `status`, `related`) plus a `README.md` index
   that carries the recording-bar callout. Pattern detection becomes
   `grep -l 'sub-surface: <name>' *.md` instead of scanning a giant table.
   Source (Engineering Agents) does not prescribe shape, so this is a free
   design choice; matches postmortem culture (Google SRE, Microsoft's
   [triage-and-improvement-playbook](https://github.com/microsoft/triage-and-improvement-playbook)).

3. **Align naming with the source.** Sub-surface, directory, and template
   are all `reflection-log` now; the artifact is no longer named
   `agent-failures.md`. The Engineering Agents term *reflection log* is
   the canonical name for this artifact; using the same word everywhere
   removes a class of "what is this called" confusion.

**Skill-level corollary** (for the project-agentification skill itself):
the post-write auditor lens (`references/lenses.md`) gained a new failure
mode — *"reflection-log README that conflates recording bar with promotion
bar"* — so future scaffolds catch this regression. Add the
recording-vs-promotion distinction to the auditor's checklist.

## Closed by

PR `refactor/reflection-log-directory-and-recording-bar`. Migrated this
repo's 9 entries from `docs/agent-failures.md` (single table) to
`docs/reflection-log/` (per-file). Updated every cross-reference across
target side (AGENTS.md, README.md, SECURITY.md, constitution.md, llms.txt,
llms-full.txt, the hook test docstring) and skill side (SKILL.md, 6
playbooks, lenses.md, maturity-rubric.md, all artifact templates,
scaffold-bundle.md). Reframe added to README-agents-section.md,
instruction-surface/AGENTS.md template, reflection-log/README.md template,
and SKILL.md Bootstrap order.

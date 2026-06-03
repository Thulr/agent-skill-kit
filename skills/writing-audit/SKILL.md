---
name: writing-audit
description: Use to AUDIT an EXISTING piece of writing — tighten wordy prose at the line and paragraph level (revise), fix mechanics, grammar, and consistency while preserving voice (copyedit), or diagnose why a draft drags, buries the point, or fails to land (diagnose). Routes by intent (revise / copyedit / diagnose) × genre (argument-memo / technical-doc / talk-pitch / narrative / general-prose). Emits a scored findings report with severity-rated findings and concrete fixes. Triggers on "tighten this", "make this clearer", "copyedit this", "why does this drag", "review my draft", "this memo buries the point". Do NOT use to write or structure something NEW (use writing-design), to audit a documentation system's IA, retrieval, or telemetry (use docs-audit), or to review product UI copy as a usability surface (use ux-audit).
license: MIT
---

# Writing Critique

Audit and diagnosis of an existing piece of writing — at the line, the
mechanics, and the structure. Provenance lives in `skill.json`; this file is
runtime routing only.

**Produces:** an intent-specific scored report — `revision-report.md` (revise),
`copyedit-report.md` (copyedit), or `diagnosis-report.md` (diagnose) — with
severity-rated findings, concrete fixes, and the reader the finding costs.

## Core principle

**Name the reader's cost, not your taste.** Every finding ties to a concrete
reader and a concrete cost ("a scanner can't find the ask"), carries a severity,
and proposes a fix. A change that only reflects preference is a 0 — say so.

## Activation

- **Bare invocation** (`"use writing-audit"`, `"review my writing"`, `"start"`):
  load `references/starter-scenarios.csv` and `references/intent-router.csv`,
  then show the intent menu with named starter scenarios on top and offer the
  mode choice. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with intent and genre inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one blocker question naming
  the candidate intent or genre; do not inspect private material first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to
   `revise`, `copyedit`, or `diagnose`. Ambiguous → ask once. (Writing or
   structuring something new instead? That is `writing-design`.)
2. **Pick genre.** Load the intent's CSV from `references/intents/<intent>.csv`.
   Match to one genre — argument-memo, technical-doc, talk-pitch, narrative, or
   general-prose. Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen row's playbook from
   `references/playbooks/<genre>.md` plus its `core_refs`. Do not load other
   playbooks.
4. **Pick the reader lenses** from `references/core/audience-frame.md` that fit
   the genre — the finding is a cost to a specific reader.
5. **Spawn reader-lens sub-agents (default for `diagnose`).** Each reads the
   draft from one lens and returns findings — see "Subagent dispatch"; fall back
   to sequential lenses if the host has no delegation primitive.
6. **Apply the playbook heuristics tagged for this intent**, then rate every
   finding with `references/core/severity-rubric.md` (0–4). For `diagnose`,
   score the asked dimension with `references/core/score-rubric.md` (0–10).
7. **Honor the guards.** Apply `references/core/voice-guard.md` — tightening is
   triage, not dogma; preserve voice and meaning-bearing hedges. For narrative
   or persuasion findings, apply `references/core/narrative-honesty-guard.md`.
8. **Emit output.** Write the intent's template: `templates/revision-report.md`,
   `templates/copyedit-report.md`, or `templates/diagnosis-report.md`.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every report names the target reader/lenses, the genre playbook(s) applied,
each finding's severity and the reader cost it maps to, a concrete fix per
finding, the guards honored, and the grounding sources from
`skill.json.inspired_by`.

## Subagent dispatch

**Default for `diagnose`;** optional for a broad `revise`; skip a single
tightly-scoped paragraph or a deterministic copyedit. Spawn the reader lenses
in parallel per `references/subagent-dispatch.md`, then synthesize and
severity-rate.

## Reference map

- `references/intent-router.csv` — level-1 router (revise / copyedit / diagnose).
- `references/intents/<intent>.csv` — level-2 router (genre) per intent.
- `references/playbooks/<genre>.md` — genre playbooks (shared with writing-design).
- `references/core/*.md` — severity and score rubrics, method rubrics, and the
  voice and narrative-honesty guards.
- `references/subagent-dispatch.md` — reader-lens dispatch and synthesis.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `templates/*.md` — revision / copyedit / diagnosis reports.
- `skill.json` — provenance, grounding sources, version, status.

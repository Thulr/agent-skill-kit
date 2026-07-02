---
name: writing-design
description: "Use to DESIGN or shape a NEW piece of writing before or while drafting — structure an argument or memo (PRD, RFC, recommendation), organize a task-oriented technical doc or explainer, get a first pass down without stalling, shape a narrative, essay, or case study, or give a talk, pitch, launch post a persuasive arc. Triggers on 'help me outline this RFC', 'draft this announcement', 'make this pitch land', 'structure this doc before I write it'."
license: MIT
---

# Writing Design

Craft design for a new piece of writing — applied before or while you draft, so
the structure, momentum, and clarity are right the first time. Provenance lives
in `skill.json`; this file is runtime routing only.

**Produces:** an intent-specific plan — `outline-plan.md` (structure),
`draft-scaffold.md` (draft), or `persuasion-plan.md` (persuade) — naming the
target reader, the heuristics applied, the guards honored, and the grounding
sources.

## Boundaries

Do NOT use to revise, copyedit, or diagnose an EXISTING draft (use writing-audit), to design a documentation system's IA, retrieval, or telemetry (use docs-design), or to gather and validate source material (use research).

## Core principle

**Decide what the reader needs before you polish how it reads.** Most weak
writing is a structure or audience problem wearing a sentence-level disguise:
name the governing point and the target reader first, then draft.

## Activation

- **Bare invocation** ("use writing-design", "help me write this", "start"): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with intent and genre inferable: skip to step 3.
- **Ambiguous invocation**: ask one — e.g., *"Do you need structure (outline), a first draft, or a persuasive arc?"* or *"What genre — argument memo, technical doc, talk pitch, narrative, or general prose?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to
   `structure`, `draft`, or `persuade`. Ambiguous → ask once. (Revising or
   critiquing an existing draft instead? That is `writing-audit`.)
2. **Pick genre.** Load the intent's CSV from `references/intents/<intent>.csv`.
   Match to one genre — argument-memo, technical-doc, talk-pitch, narrative, or
   general-prose. Not every genre is a target for every intent; the intent's CSV
   lists the genres it serves. If the genre you'd pick isn't a row, it isn't a
   target for that intent — route to the nearest served pairing and name it
   (e.g., making a how-to compelling is the `narrative` genre, not `persuade`).
   Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen row's playbook from
   `references/playbooks/<genre>.md` plus its `core_refs`. Do not load other
   playbooks.
4. **Name the target reader** using `references/core/audience-frame.md` — the
   piece is *for* a specific reader with a specific knowledge state and goal.
5. **Apply the playbook heuristics tagged for this intent.** Produce the
   concrete shape — an outline, a drafted pass, or a persuasive spine — not
   abstract advice. For a wide space, optionally dispatch reader-lens sketches
   (see "Subagent dispatch") and synthesize the strongest.
6. **Honor the guards.** When the work adds momentum or persuasion, apply
   `references/core/narrative-honesty-guard.md` — shape only where the tension
   is real. When it tightens prose, keep the writer's voice.
7. **Emit output.** Write the intent's template: `templates/outline-plan.md`,
   `templates/draft-scaffold.md`, or `templates/persuasion-plan.md`.

> **Wrong direction?** If the user says this isn't what they meant, go back to step 1 (Pick intent) — do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target reader, the genre playbook(s) applied, the
intent's load-bearing section (the outline / the drafted pass / the persuasive
spine), the guards honored, and the grounding sources from
`skill.json.inspired_by`.

## Subagent dispatch

Optional for a wide `persuade` or `structure` space: dispatch reader-lens
sketches in parallel — see `references/subagent-dispatch.md` — then synthesize
the strongest. Skip for a single tightly-scoped piece.

## Reference map

- `references/intent-router.csv` — level-1 router (structure / draft / persuade).
- `references/intents/<intent>.csv` — level-2 router (genre) per intent.
- `references/playbooks/<genre>.md` — genre playbooks (shared with writing-audit).
- `references/core/*.md` — shared method rubrics, plus the voice and
  narrative-honesty guards.
- `references/subagent-dispatch.md` — reader-lens dispatch and synthesis.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `templates/*.md` — outline / draft / persuasion outputs.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.

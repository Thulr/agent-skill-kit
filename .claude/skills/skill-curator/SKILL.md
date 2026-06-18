---
name: skill-curator
description: Use when researching books, movies, talks, articles, or notes as source material and turning them into source-inspired public skills. Also use when choosing how many routing layers a curated skill needs (flat, single-layer, or two-level routing). Do not use for reviewing an already-built skill for release readiness; use `skill-reviewer` for that.
metadata:
  internal: true
---

# Skill Curator

**Produces:** a scaffolded skill directory under `skills/<name>/` (SKILL.md, skill.json, evals/, references/, templates/) shaped per `references/depth-rubric.md`, plus research notes under `.agents/state/` for the curator's own provenance trail.

## Overview

Turn source material into practical agent skills. A source is raw material;
the published skill taxonomy is organized by capability pack, not by book,
movie, author, character, or title. Each curated skill picks a **routing
depth** — flat, single-layer (hub-and-spoke), two-level (intent × surface),
or deeper if the content genuinely needs more axes. Progressive disclosure
via CSV chains is what makes deeper routing safe: the agent only reads the
next layer when it commits to that branch, so depth is bounded by content,
not by an arbitrary cap. Pick the depth explicitly with
`references/depth-rubric.md`; do not default to whichever shape feels
familiar.

The curator works in **five named phases** with **hard user-confirmation
gates between phases**. The gates are the load-bearing mechanism — they
stop the curator from advancing while artifacts are incomplete or
miscalibrated. Skipping a gate is the failure mode this workflow exists to
prevent.

## Operating Contract

- Use web research from multiple source types before creating public skills.
- Keep research and provenance detail in `.agents/state/`.
- Write public skill files only under `skills/<skill-name>/`. Capability
  pack is recorded in `skill.json.tags`, not as a directory layer.
- Keep `SKILL.md` runtime-only. Put user-facing provenance in `skill.json`.
- Pick the skill's shape using `references/depth-rubric.md`. Then scaffold
  the file set from the matching `references/shapes/<shape>.md`.
- Use `skill.json.inspired_by` for concise provenance and add a concise
  grounding reference only when source-to-heuristic mapping will materially
  help future agents apply the skill.
- Prefer source-inspired behavior over source summaries.
- Do not reproduce long copyrighted passages, chapter summaries, scripts,
  dialogue, lyrics, or distinctive text. Paraphrase concepts into
  operational methods.
- Set every generated public `skill.json.status` to `published`; this repo
  communicates prerelease maturity with the repository tag, not per-skill
  draft status.
- **Never advance a hard gate without explicit user confirmation.** Hard
  gates are non-negotiable for novel packs, novel shapes, and any two-level
  candidate. They are soft only when Autopilot mode is explicitly chosen
  *and* the candidate is a routine flat skill *and* the intake brief names
  at least one strong comparable existing skill.

## Activation Handshake

If the user gives a concrete source and asks for curation, proceed in
Guided Build mode unless they ask for another mode.

If the user only invokes this skill, ask for one source seed:

- source title, creator, or URL
- target audience if known
- preferred output: proposal only or skill files

Then enter Phase 1 (Intake).

## Modes

Modes set the elicitation style *within* a phase. They do not override
the hard gates between phases.

- **Grill Me**: ask one open question at a time before research when the
  desired audience, safety boundaries, or shape strategy is unclear.
- **Guided Build**: default. Research, propose the shape and plan, ask one
  approval question per phase, then write skill files if approved.
- **Autopilot**: research and create skill files using conservative
  assumptions. Stop only for legal/safety ambiguity, unavailable research,
  or destructive actions. Autopilot still respects hard phase gates for
  novel packs/shapes/two-level candidates; it may only soft-gate routine
  flat skills with a named comparable.

## Workflow — five phases with hard gates

Every phase produces a **named artifact**. The curator presents the
artifact, waits for the user's `go`, then advances. If the user rejects,
the curator returns to whichever earlier phase the rejection implicates.

### Phase 1 — Intake

Goal: capture what the user wants before any research happens.

1. Load `references/intent-router.csv` to choose the active intent
   (`curate-source`, `proposal-only`, `pick-shape`, `create-flat`,
   `create-single-layer`, `create-two-level`, `taxonomy-maintenance`).
2. Open `templates/intake-brief.md` and fill it in with what the user has
   already said. Slots: audience, success criteria, scope boundaries,
   comparable existing skills (curator must `grep` and list 2–3 — forces
   de-duplication), safety/copyright posture, working hypothesis on
   shape/pack/intents.
3. Write to `.agents/state/intake-briefs/<intake-slug>.md`.
4. **Gate**: present the intake brief. Ask, "Anything missing or wrong
   before we research? Reply `go` to advance to Phase 2 (Research), or
   describe what to revise." Do not proceed without `go`.

### Phase 2 — Research

Goal: build the source dossier — paraphrased, multi-source, with
confidence levels.

1. Load `references/research-dossier-playbook.md`.
2. Open `templates/source-dossier.md` and fill each section. Confidence
   column is **required** per row; any **L** on a load-bearing claim is
   auto-promoted to **Open Questions** and must be resolved or scoped
   out before Phase 3.
3. The **Critical / Dissenting Takes** section is required. If no
   critic exists in your research, write a steelman critique and mark it
   as hypothesis.
4. Run the **Paraphrase Audit** at the bottom of the dossier before the
   gate. Any distinctive copying gets rewritten or removed.
5. Save to `.agents/state/source-dossiers/<source-slug>.md`. The
   `<source-slug>` is the dossier ID that the candidate plan will
   back-link to.
6. **Gate**: present the dossier. Ask, "Does the research cover the
   source faithfully? Any missing source types, weak confidence, or open
   questions to resolve before we plan? Reply `go` to advance to Phase 3."

### Phase 3 — Plan

Goal: per-candidate decisions that survive scaffolding without rework.

1. Load `references/pack-placement-rubric.md` and `references/depth-rubric.md`.
2. Open `templates/candidate-plan.md` and fill one block per candidate.
   Every field is required:
   - `dossier_ref`, `audience_ref` — back-links
   - `shape_decision.rubric_evidence` — which depth-rubric question(s)
     justified the chosen shape (forces explicit reasoning, not
     cargo-culting)
   - `anti_pattern_check` — walk the anti-patterns in `depth-rubric.md`
     and assert none apply (collapsed dimension, registry that doesn't
     route, cargo-culting, projected bloat)
   - `playbook_outline` — for any routed shape (depth ≥1): list every
     intended playbook with ≥2 heuristic seeds and ≥1 common-failure
     seed (proves the playbooks will have real content)
   - `registry_sketch` — for every CSV layer in the chosen depth: rows
     showing each layer actually routes (not all rows pointing at the
     same files)
   - `activation_case_seeds` — ≥3 positive / ≥3 negative / ≥1 edge for
     flat & single-layer; ≥10 / ≥8 / ≥2 for two-level or deeper;
     **each negative names the sibling skill** it disambiguates from
   - `grounding_map` — for each `inspired_by` source, which playbooks
     it informs (non-empty)
3. Walk the **Anti-pattern self-check** checklist at the bottom of the
   template. Every box must be checked or the candidate must be revised.
4. Save to `.agents/state/candidate-plans/<plan-slug>.md`.
5. **Gate**: present the plan. Ask, "Approve the plan, or revise? Reply
   `go` to advance to Phase 4 (Scaffold). Any rejection sends us back to
   Phase 2 (Research) or Phase 1 (Intake) depending on the reason."

### Phase 4 — Scaffold

Goal: write the public skill files. **No file outside the approved
plan's `public_path` set may be written without re-opening Phase 3.**

1. Inspect existing public skills for current conventions. Read
   `skills/dx-audit/` end-to-end if scaffolding a two-level skill;
   read 2–3 single-layer skills (e.g. `ux-audit`,
   `ui-design`) if scaffolding single-layer. For depth ≥3 (no
   canonical example exists yet), apply the two-level pattern
   recursively per `references/depth-rubric.md` §Going deeper.
2. Scaffold `skills/<skill-name>/` from the matching
   `references/shapes/<shape>.md` for depths 0–2; for depth ≥3 the
   two-level anatomy is the recursion base case. Load only the anatomy
   you need — do not over-build.
3. For every generated playbook, start from the matching skeleton at
   `templates/playbook-skeletons/<shape>.md` (use `two-level.md` as the
   skeleton for any depth ≥2). Every canonical section (`## Scope`,
   `## Grounding`, `## Good signals`, `## Common failures`,
   `## Heuristics`, `## Quick diagnostic`, `## Cross-references`) must
   be present before the gate.
4. Start `evals/activation-cases.md` from
   `templates/activation-cases-skeleton.md`. Each negative case must
   name a sibling skill.
5. For every CSV layer in the chosen depth, map every downstream
   reference file through it. No orphans, no rows that load identical
   sets at any layer.
6. Keep public grounding concise. Source detail belongs in the private
   dossier; user-facing provenance belongs in `skill.json`.
7. **Gate**: list the files written and ask, "Scaffold written under
   `<paths>`. Eyeball before validation? Reply `go` to advance to Phase 5."

### Phase 5 — Validate

Goal: catch misses before handing off to `skill-reviewer`.

1. **Deterministic.** Run
   `python3 scripts/validate-generated-skill.py skills/<skill-name>/`
   from the repo root. Save the report to
   `.agents/state/validation-reports/<skill-name>-<timestamp>.md` with
   `--report`. **Any blocking finding blocks the gate** — fix and rerun.
2. **LLM self-review.** Load the matching rubric at
   `references/validation-rubrics/<shape>.md` (use `two-level.md` for
   any depth ≥2 — its checks generalize) and grade the scaffolded skill
   against it. For depth ≥2 skills with ≥5 playbooks, spawn one
   read-only `Explore` sub-agent per playbook scoped to that playbook's
   blocks; the curator consolidates. For ≤4 playbooks, batch read.
   Severities (blocking/warning/note) merge into the validation report.
3. Run `just check` (repo-wide static checks).
4. **Gate**: present the validation report. Ask, "Ready for
   `skill-reviewer` handoff? Reply `go` to finalize."
5. Update the candidate plan's **Review Handoff** section with draft
   paths, known risks, suggested reviewer focus, and validation report
   path. Hand off to `skill-reviewer`.

## Pack Rules

A capability pack is a categorization like coaching, decision making,
communication, attention, reflection, or planning. Packs travel in
`skill.json.tags` — they are not directory layers in this repo. Never use
a source title as a pack tag.

Add a new pack tag when:

- the name describes a capability domain, not a source
- the domain would still make sense if the source disappeared
- the pack can accept future sources from books, movies, notes, talks, or
  articles

Use an existing pack tag when:

- a current pack already describes the user need
- the candidate extends an existing skill's references, rubric, or
  templates
- a new pack would differ only by wording

See `references/pack-placement-rubric.md` for the full candidate-shape
rubric and decision recording format.

## Public File Rules

Every generated public skill must include:

- `SKILL.md` — agent runtime instructions only.
- `skill.json` — user-facing catalog metadata. Schema follows existing
  skills in this repo; see `skills/dx-audit/skill.json` for the
  worked example with `inspired_by` as an object array.

The rest of the file set depends on the chosen depth — see the matching
file in `references/shapes/`. In short:

- **Flat** (depth 0) — typically just `SKILL.md`, optionally one or two
  supporting files.
- **Single-layer (hub-and-spoke)** (depth 1) — adds `references/`,
  optional `templates/`, optional `evals/`, with a single registry CSV
  routing the intents.
- **Two-level routing** (depth 2) — adds `references/intent-router.csv`,
  `references/intents/<intent>.csv`, `references/playbooks/<surface>.md`,
  shared `references/core/` rubrics, `templates/<intent>.md`, and `evals/`
  including a static-check script.
- **Deeper** (depth ≥3) — same pattern recursively: each registry row
  can name a child registry CSV that routes the next axis, ending in
  leaf playbooks. No upper bound; depth is bounded by content, not by
  ceremony. See `references/depth-rubric.md` §Going deeper.

Do not put author biographies, further-reading sections, source marketing,
or long bibliographies in `SKILL.md`. If public grounding is useful, keep
it short, paraphrased, and routed through the skill's own registry.

## Reference Map

- `references/intent-router.csv` — curator's own intent routing.
- `references/research-dossier-playbook.md` — web research and dossier rules.
- `references/pack-placement-rubric.md` — capability-pack categorization.
- `references/depth-rubric.md` — choose flat / single-layer / two-level.
- `references/shapes/flat.md` — anatomy for the simplest shape.
- `references/shapes/single-layer.md` — anatomy for hub-and-spoke routing.
- `references/shapes/two-level.md` — anatomy for intent × surface routing
  (matches `skills/dx-audit/`).
- `references/draft-skill-playbook.md` — cross-shape rules (path,
  `SKILL.md`/`skill.json` separation, evals, quality bar).
- `references/validation-rubrics/{flat,single-layer,two-level}.md` —
  Phase 5 LLM self-review rubrics.
- `templates/intake-brief.md` — Phase 1 elicitation template.
- `templates/source-dossier.md` — Phase 2 dossier template.
- `templates/candidate-plan.md` — Phase 3 plan template.
- `templates/playbook-skeletons/{flat,single-layer,two-level}.md` —
  Phase 4 playbook starting points.
- `templates/activation-cases-skeleton.md` — Phase 4 activation-cases
  starting point.
- `scripts/validate-generated-skill.py` — Phase 5 deterministic
  validator (invoked from repo root).

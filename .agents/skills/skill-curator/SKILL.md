---
name: skill-curator
description: Use when researching books, movies, talks, articles, or notes as source material and turning them into source-inspired public skills. Also use when choosing how many routing layers a curated skill needs (flat, single-layer, or two-level routing).
metadata:
  internal: true
---

# Skill Curator

## Overview

Turn source material into practical agent skills. A source is raw material;
the published skill taxonomy is organized by capability pack, not by book,
movie, author, character, or title. Each curated skill takes one of three
shapes — flat, single-layer (hub-and-spoke), or two-level routing —
depending on how much internal branching the content needs. Pick the shape
explicitly with `references/depth-rubric.md`; do not default to whichever
shape feels familiar.

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
  communicates prerelease maturity with the repository tag, not per-skill draft
  status.

## Activation Handshake

If the user gives a concrete source and asks for curation, proceed in
Guided Build mode unless they ask for another mode.

If the user only invokes this skill, ask for one source seed:

- source title, creator, or URL
- target audience if known
- preferred output: proposal only or skill files

## Modes

- **Grill Me**: ask one open question at a time before research when the
  desired audience, safety boundaries, or shape strategy is unclear.
- **Guided Build**: default. Research, propose the shape and plan, ask one
  approval question, then write skill files if approved.
- **Autopilot**: research and create skill files using conservative
  assumptions. Stop only for legal/safety ambiguity, unavailable research,
  or destructive actions.

## Workflow

1. Load `references/use-case-registry.csv`.
2. Load the relevant detail files for the source type and requested output.
3. Inspect the repo's current public skills to align with existing
   conventions (`skill.json` schema, eval patterns, path layout). Read
   `skills/dx-heuristics/` as the canonical example for the two-level shape.
4. Build or update a source dossier in `.agents/state/source-dossiers/`.
5. Extract reusable behaviors, anti-patterns, rubrics, workflows, and
   examples from the source.
6. For each candidate, decide whether it is a small skill, workflow skill,
   reference addition, or capability-pack-level pattern.
7. Tag each candidate with its capability pack (a `tags` entry in
   `skill.json`, not a directory).
8. **Pick the shape (depth)** for each candidate using
   `references/depth-rubric.md`: `flat`, `single-layer` (hub-and-spoke),
   or `two-level` (intent × surface routing). Bias toward the shallowest
   shape that fits — a skill can be promoted later, but rarely flattened.
9. If writing files, scaffold `skills/<skill-name>/` from the matching
   `references/shapes/<shape>.md`. Load only that shape's anatomy — do
   not over-build.
10. For shapes that include a registry, map every reference file through
    it. No public reference should be orphaned or reachable only by
    scanning a directory.
11. Keep public grounding concise: source detail belongs in the private
    dossier, user-facing provenance belongs in `skill.json`, and any
    public grounding reference should map source families to operational
    heuristics or caveats.
12. Run `just check` (which executes the repo's static checks across all
    skills).
13. Hand off to `skill-reviewer` before any generated skill is merged.

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
  skills in this repo; see `skills/dx-heuristics/skill.json` for the
  worked example with `inspired_by` as an object array.

The rest of the file set depends on the chosen shape — see the matching
file in `references/shapes/`. In short:

- **Flat** — typically just `SKILL.md`, optionally one or two supporting
  files.
- **Single-layer (hub-and-spoke)** — adds `references/`, optional
  `templates/`, optional `evals/`, with a single registry CSV routing
  the use cases.
- **Two-level routing** — adds `references/intent-router.csv`,
  `references/intents/<intent>.csv`, `references/playbooks/<surface>.md`,
  shared `references/core/` rubrics, `templates/<intent>.md`, and `evals/`
  including a static-check script.

Do not put author biographies, further-reading sections, source marketing,
or long bibliographies in `SKILL.md`. If public grounding is useful, keep
it short, paraphrased, and routed through the skill's own registry.

## Reference Map

- `references/use-case-registry.csv` — curator's own use-case routing.
- `references/research-dossier-playbook.md` — web research and dossier rules.
- `references/pack-placement-rubric.md` — capability-pack categorization.
- `references/depth-rubric.md` — choose flat / single-layer / two-level.
- `references/shapes/flat.md` — anatomy for the simplest shape.
- `references/shapes/single-layer.md` — anatomy for hub-and-spoke routing.
- `references/shapes/two-level.md` — anatomy for intent × surface routing
  (matches `skills/dx-heuristics/`).
- `references/draft-skill-playbook.md` — cross-shape rules (path,
  `SKILL.md`/`skill.json` separation, evals, quality bar).
- `templates/source-dossier.md` — local research dossier template.
- `templates/candidate-plan.md` — curator proposal template.

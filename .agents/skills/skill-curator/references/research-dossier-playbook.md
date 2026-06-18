# Research Dossier Playbook

## Goal

Build enough evidence to turn a source into operational skills without
reproducing the source.

## Required Source Mix

Use at least three materially different public sources when available:

- official or source-adjacent: author site, publisher page, official synopsis,
  interviews, talks, or official production materials
- interpretive: reviews, essays, practitioner writeups, teaching notes, or
  course notes
- critical: limitations, dissenting takes, caveats, or failed applications
- applied: examples of the concept used in work, coaching, therapy-adjacent
  practice, writing, decision-making, education, or facilitation

Prefer primary or official sources for claims about the source. Use secondary
sources to find applications, critiques, and patterns.

## Dossier Contents

Write dossiers to `.agents/state/source-dossiers/<source-slug>.md`.

Capture:

- source identity and URLs
- concise paraphrased notes, not long excerpts
- confidence level for each major concept
- operational behaviors the source suggests
- candidate skills and pack placement
- copyright/safety risks
- unresolved questions

## Public Grounding Boundary

The dossier may contain the full research trail, but public skill files should
only expose what helps the future agent execute the skill.

Use:

- `skill.json.inspired_by` for concise source attribution
- `skill.json.source_note` for the non-substitution boundary
- a short registry-mapped grounding reference when the source mapping matters,
  such as source family, derived heuristic, caveat, and intent

Avoid:

- public author biographies
- long bibliographies in `SKILL.md`
- source-by-source summaries in public references
- grounding files that are not mapped from `references/intent-router.csv`

## Copyright Boundary

Allowed:

- brief factual source identification
- short paraphrased concept notes
- high-level frameworks in your own words
- links to sources
- user-authored notes

Avoid:

- chapter-by-chapter summaries
- long quotes
- reproduced exercises, worksheets, scripts, lyrics, or dialogue
- distinctive phrasing copied into public skill instructions
- any output that functions as a substitute for the source

## Research Quality Check

Before drafting, confirm:

- research uses multiple source types or records why that was impossible
- candidate behaviors are not just summaries
- critiques and limitations were considered
- sensitive-domain claims are bounded
- source provenance belongs in `skill.json`, not `SKILL.md`
- any public grounding reference is concise, operational, and mapped through the
  generated skill's intent registry

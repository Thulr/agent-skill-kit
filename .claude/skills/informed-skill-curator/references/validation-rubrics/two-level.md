# Validation Rubric: Two-Level Shape

Used by informed-skill-curator's **Phase 5 self-review** against a scaffolded
two-level routing skill at `skills/<name>/`. Two-level skills warrant
**parallel sub-agent review**: spawn one Explore-mode sub-agent per
playbook (`references/playbooks/*.md`) when there are 5+ playbooks;
batch read otherwise. Each sub-agent walks this rubric for its
playbook and reports severity-tagged findings; the curator
consolidates.

Severity scale: **blocking** / **warning** / **note** (see flat.md
rubric for definitions and report format).

## Required artifacts

- [ ] **blocking** — `SKILL.md` with frontmatter, one H1, both-registry-consulting workflow
- [ ] **blocking** — `skill.json` with `status: "published"`, object-array `inspired_by` with per-source `playbooks[]`, resolvable `maintainers`
- [ ] **blocking** — `references/intent-router.csv` with columns `intent,name,when_to_use,registry_file,default_template`
- [ ] **blocking** — `references/intents/<intent>.csv` per intent with columns `surface,name,when_to_use,playbook,core_refs`
- [ ] **blocking** — `references/playbooks/<surface>.md` per surface
- [ ] **blocking** — `references/core/<rubric>.md` for shared rubrics (severity, score, personas)
- [ ] **warning** — `references/subagent-dispatch.md` if any intent benefits from multi-lens review (audits, edge-passes)
- [ ] **blocking** — `templates/<intent>.md` per intent
- [ ] **blocking** — `evals/activation-cases.md`, `evals/run-static-checks.sh`
- [ ] **warning** — `evals/trigger-evals.json`

## Dimension orthogonality (the load-bearing anti-pattern check)

- [ ] **blocking** — Both dimensions have ≥3 values (no "two-level with collapsed second axis")
- [ ] **blocking** — Surfaces are not all identical across intent CSVs — i.e. different intents route to materially different playbook subsets
- [ ] **blocking** — At least one (intent, surface) combination is intentionally absent or routes to a shared placeholder, **or** the matrix is genuinely fully populated. A trivial Cartesian product with no curation is a smell — the validation rubric flags fully populated matrices for human review.
- [ ] **warning** — Each intent CSV has ≥3 surface rows
- [ ] **warning** — Surface vocabulary is consistent across intent CSVs (same `<surface>` slug means the same thing in audit and design)

## Registry integrity

- [ ] **blocking** — Every `registry_file` path in `intent-router.csv` exists
- [ ] **blocking** — Every `playbook` and `core_refs` path in every intent CSV exists
- [ ] **blocking** — Every `.md` in `references/playbooks/` is referenced by at least one intent CSV
- [ ] **blocking** — Every `.md` in `references/core/` is referenced by at least one playbook or template
- [ ] **blocking** — Playbook list is auto-derived from disk in `run-static-checks.sh` (no hardcoded surface list)

## Playbook content (per `references/playbooks/*.md`)

- [ ] **blocking** — Has `## Scope`, `## Grounding`, `## Good signals`, `## Common failures`, `## Heuristics`, `## Quick diagnostic`, `## Cross-references`
- [ ] **blocking** — Each heuristic is tagged with one or more intents in parentheses (e.g. `(audit, design)`)
- [ ] **warning** — 5–12 heuristics; <3 means the surface should fold; >15 means it should split
- [ ] **warning** — `## Common failures` is concrete (names mechanism, not vague warning)
- [ ] **warning** — `## Grounding` cites ≥1 `inspired_by` source
- [ ] **note** — 400–1500 words; outside that band is a structural smell

## SKILL.md content

- [ ] **blocking** — Workflow consults both registries (`intent-router.csv` first, then `intents/<intent>.csv`)
- [ ] **blocking** — Subagent dispatch is referenced for relevant intents (e.g. audit, edge-pass) if `subagent-dispatch.md` exists
- [ ] **warning** — SKILL.md is under 800 words; detail in playbooks, not in the navigator
- [ ] **warning** — No source author names or titles leak into SKILL.md

## Activation cases

- [ ] **blocking** — ≥10 positive cases covering ≥3 intents and ≥4 surfaces
- [ ] **blocking** — ≥8 negative cases; each names a sibling skill
- [ ] **warning** — ≥2 boundary / edge cases
- [ ] **warning** — Each registered intent has ≥1 positive case

## Grounding

- [ ] **blocking** — `inspired_by[]` is object array; each entry has non-empty `playbooks[]`
- [ ] **blocking** — Every `playbooks[]` value matches a `<surface>` slug in this skill's `references/playbooks/`
- [ ] **warning** — ≥3 distinct sources covering at least 3 different surfaces
- [ ] **warning** — At least one source is `critical` / dissenting (per `research-dossier-playbook.md`)

## Anti-patterns (from `references/shapes/two-level.md`)

- [ ] **blocking** — No dimension has only 1–2 values
- [ ] **blocking** — Every playbook follows the uniform section structure
- [ ] **blocking** — No detail in SKILL.md that belongs in a playbook
- [ ] **blocking** — `inspired_by` is not a list of strings
- [ ] **warning** — No hardcoded surface lists in `run-static-checks.sh`

## Static check

- [ ] **blocking** — `evals/run-static-checks.sh` exits 0; `bash scripts/list-installable-skills.sh` includes the skill; `just check` passes

## Parallel review note

For two-level skills with 5+ playbooks, the curator spawns one
Explore sub-agent per playbook with this rubric scoped to that
playbook's blocks. Sub-agent reports are consolidated into the
validation report. Disagreements between sub-agents (e.g. one flags
weak grounding, another doesn't) are surfaced as warnings even if
neither sub-agent marked them blocking.

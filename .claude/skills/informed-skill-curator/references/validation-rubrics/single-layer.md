# Validation Rubric: Single-Layer Shape

Used by informed-skill-curator's **Phase 5 self-review** against a scaffolded
single-layer (hub-and-spoke) skill at `skills/<name>/`. A sub-agent
walks this rubric per intent registered in `references/intent-router.csv`
and produces severity-tagged findings.

Severity scale: **blocking** / **warning** / **note** (see flat.md
rubric for definitions and report format).

## Required artifacts

- [ ] **blocking** — `SKILL.md` with frontmatter, one H1, registry-consulting workflow
- [ ] **blocking** — `skill.json` with `status: "published"`, object-array `inspired_by`, resolvable `maintainers`
- [ ] **blocking** — `references/intent-router.csv` exists with the canonical columns (`intent,trigger_examples,detail_file,templates,notes`)
- [ ] **blocking** — `evals/activation-cases.md`, `evals/trigger-evals.json`, `evals/run-static-checks.sh`
- [ ] **warning** — `templates/` directory exists only if there are repeatable artifacts (no orphan templates)

## Registry integrity

- [ ] **blocking** — Every `detail_file` and `templates` path exists on disk
- [ ] **blocking** — Every `.md` under `references/` is reachable from at least one row (no orphans)
- [ ] **blocking** — No row points at every reference file (would defeat progressive disclosure)
- [ ] **blocking** — Not all rows load identical files (anti-pattern: registry that doesn't route — collapse to flat)
- [ ] **warning** — 3–8 intent rows; outside that range, justify in the candidate-plan's `shape_decision.promotion_path`
- [ ] **warning** — Each row's `trigger_examples` differs meaningfully — no near-duplicate trigger sets across rows

## Playbook content (per `references/*.md` file)

- [ ] **blocking** — Each playbook has `## Scope`, `## Grounding`, `## Good signals`, `## Common failures`, `## Heuristics`, `## Quick diagnostic`, `## Cross-references` (or a documented justification for omitting a section)
- [ ] **warning** — `## Heuristics` has ≥3 entries
- [ ] **warning** — `## Common failures` is concrete (names mechanisms, not generic "be careful")
- [ ] **warning** — `## Grounding` maps to at least one `inspired_by` source
- [ ] **note** — Playbook is 200–800 words

## SKILL.md content

- [ ] **blocking** — Workflow explicitly consults `references/intent-router.csv` (not a hardcoded if/else over intents)
- [ ] **warning** — SKILL.md is under 800 words; detail lives in references, not in the navigator
- [ ] **warning** — No author biographies, long bibliographies, or source marketing — provenance lives in `skill.json`
- [ ] **note** — Modes section (Grill Me / Guided Build / Autopilot, or skill-specific) if the skill has elicitation behavior

## Activation cases

- [ ] **blocking** — ≥3 positive cases; each names the expected intent
- [ ] **blocking** — ≥3 negative cases; each names the sibling skill
- [ ] **warning** — Positives cover at least 2/3 of the registered intents
- [ ] **warning** — ≥1 boundary / edge case

## Grounding

- [ ] **blocking** — `inspired_by[]` is object array with non-empty `playbooks[]` arrays
- [ ] **blocking** — Every `playbooks[]` value is a real intent/playbook slug in this skill
- [ ] **warning** — ≥2 distinct sources; if fewer, dossier explains why
- [ ] **warning** — Critical / dissenting take is at least mentioned where the source is opinionated

## Anti-patterns (from `references/shapes/single-layer.md`)

- [ ] **blocking** — Registry rows are not all loading the same files
- [ ] **blocking** — No detail files unreferenced by the registry
- [ ] **warning** — Templates have a corresponding intent row
- [ ] **warning** — `SKILL.md` doesn't contain what should be in a reference file

## Static check

- [ ] **blocking** — `evals/run-static-checks.sh` exits 0; `bash scripts/list-installable-skills.sh` includes the skill

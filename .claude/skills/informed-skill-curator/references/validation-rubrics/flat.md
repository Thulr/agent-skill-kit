# Validation Rubric: Flat Shape

Used by informed-skill-curator's **Phase 5 self-review** against a scaffolded
flat skill at `skills/<name>/`. A sub-agent (or the curator itself in
batch mode) walks this rubric and produces severity-tagged findings
for the validation report.

Severity scale:

- **blocking** — must fix before handoff
- **warning** — should fix; document if knowingly waived
- **note** — nice-to-have improvement

## Required artifacts

- [ ] **blocking** — `SKILL.md` exists with frontmatter (`name`, `description`, `license`)
- [ ] **blocking** — `skill.json` exists with `status: "published"`, non-empty `inspired_by`, resolvable `maintainers` handles (per Rule 4 in `AGENTS.md`)
- [ ] **blocking** — `evals/activation-cases.md` exists
- [ ] **blocking** — `evals/trigger-evals.json` exists, conforms to `schemas/trigger-evals.schema.json`
- [ ] **blocking** — `evals/run-static-checks.sh` exists and is executable

## SKILL.md content

- [ ] **blocking** — One H1
- [ ] **blocking** — `description` frontmatter line is a single sentence with at least one explicit "use when" trigger and at least one "do not use when" boundary
- [ ] **warning** — Under 800 words total (over → escalate shape per `references/shapes/flat.md`)
- [ ] **warning** — Procedure is operational (numbered steps or named pattern), not abstract advice
- [ ] **warning** — Grounding section maps load-bearing claims to `skill.json.inspired_by` sources
- [ ] **note** — Includes a "Common mistakes / red flags" section

## Activation cases

- [ ] **blocking** — ≥3 positive cases
- [ ] **blocking** — ≥3 negative cases, each **naming the sibling skill** the prompt should route to instead
- [ ] **warning** — ≥1 boundary / edge case
- [ ] **warning** — Negatives cover at least one neighbor skill identified in the intake brief

## Grounding

- [ ] **blocking** — `skill.json.inspired_by` is an object array (not strings); each entry has `name`, `author`, `kind`, `year`, `contribution`
- [ ] **warning** — At least 2 sources; if only 1, the curator-side dossier explains why
- [ ] **warning** — No source title or author name leaks into `SKILL.md` (provenance lives in `skill.json`)

## Anti-patterns (from `references/shapes/flat.md`)

- [ ] **blocking** — Not a "flat skill with 10 procedures crammed into one SKILL.md" (split to single-layer)
- [ ] **warning** — No empty `templates/` or `references/` directory
- [ ] **warning** — SKILL.md is not >800 words on a single procedure (move detail to a `references/` file)

## Static check

- [ ] **blocking** — `evals/run-static-checks.sh` exits 0 when run with no args from the skill dir
- [ ] **blocking** — `bash scripts/list-installable-skills.sh` includes the skill

## Report format

Each finding is one bullet:

```
- [severity] <check label> — <file:line or path> — <one-line evidence>
```

The validation report aggregates findings into severity buckets and
records the rubric version used. Blocking findings prevent the
handoff gate from passing.

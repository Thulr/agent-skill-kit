# Draft Skill Playbook

Cross-shape rules for every public skill. Shape-specific anatomy lives in
`references/shapes/<shape>.md`; pick the shape with
`references/depth-rubric.md`.

## Path Convention

Public skills live at:

```text
skills/<skill-name>/
```

There is no pack subdirectory — capability pack is recorded in
`skill.json.tags`, not as a folder. The repo's existing skills
(`skills/dx-heuristics/`, `skills/example-minimal/`) all follow this
convention.

## SKILL.md Rules

`SKILL.md` is agent-facing runtime behavior. It should include:

- frontmatter with `name` and `description`
- activation handshake
- mode behavior when useful
- workflow
- reference map
- validation rules
- safety boundaries

It should NOT include:

- inspired-by sections
- source marketing
- author biographies
- long bibliographies or further-reading lists
- long source summaries
- copied source language

If source grounding helps execution, put a short operational map in a
`references/` file (such as "source family → heuristic/caveat/intent")
and route it through the skill's own registry.

For multi-shape skills, keep `SKILL.md` as a navigator: it routes to
detail, it does not contain detail. Aim for <800 words at single-layer or
two-level.

### Description field

The description in `SKILL.md` frontmatter is the primary triggering
mechanism. Start with "Use when…" and focus on triggering conditions, not
workflow:

```yaml
# Good
description: Use when designing or auditing a developer-facing CLI, API, SDK, ...

# Bad — describes workflow; Claude may follow the description instead of
# the body
description: Use when you need a DX review — runs three lenses in parallel
  and synthesizes findings with severity scores
```

A skill description should answer "Should I read this skill right now?",
not "What does this skill do?". Workflow detail belongs in the body.

## skill.json Rules

`skill.json` is user-facing catalog metadata. Match the schema used by
existing skills in this repo. The canonical example is
`skills/dx-heuristics/skill.json`. Required fields:

```json
{
  "name": "skill-name",
  "description": "User-facing summary covering trigger conditions.",
  "version": "0.1.0",
  "license": "MIT",
  "status": "published",
  "maintainers": ["<your-handle>"],
  "tags": ["pack-name", "topic", "..."],
  "inspired_by": [
    {
      "name": "Source Title",
      "author": "Creator Name",
      "kind": "book | article | talk | guide | essay",
      "year": 2020,
      "contribution": "What this source contributes to the skill.",
      "playbooks": ["<surface-or-intent-marker>"]
    }
  ]
}
```

`inspired_by` is an **array of objects, not strings**, because future
agents need to know which playbook each source informs. For flat skills
with a single playbook, the `playbooks` field can be omitted or contain
a single value.

Keep detailed research notes and URLs in
`.agents/state/source-dossiers/<source-slug>.md`. Public grounding
references should be short enough to support execution without
substituting for the source.

## Progressive Disclosure Rules

Every non-trivial public skill should use registry-based progressive
disclosure:

- `SKILL.md` is the navigator: it routes intents.
- A registry CSV (single-layer) or two registry CSVs (two-level) are the
  source of truth for which detail files and templates load for each use
  case.
- Detailed frameworks, rubrics, examples, source grounding, edge cases,
  and caveats live in one-hop `references/` files.
- Templates are mapped only to the intents that produce those
  artifacts.
- No public reference file should be orphaned, and no registry row
  should point to every file unless every file is truly needed for that
  intent.

Flat skills can skip the registry — there's no routing to do.

## Evals

The eval set depends on the shape:

- **Flat** — required in this repo, even when minimal, so a templated skill
  cannot bypass gates.
- **Single-layer** — required in this repo: `evals/activation-cases.md`,
  `evals/trigger-evals.json`, and `evals/run-static-checks.sh`.
- **Two-level** — both required. Also include `evals/trigger-evals.json`
  for the description-optimization loop.

Activation cases should include both **positive** cases (correct trigger
+ correct routing) and **negative** cases (near-miss prompts that share
keywords but should not trigger). See
`skills/dx-heuristics/evals/activation-cases.md` for a worked example
with both.

## Draft Quality Bar

Before handing to review:

- `just check` passes (which executes the repo's static checks across
  all skills, including any `run-static-checks.sh` the new skill
  provides).
- The skill stands alone without requiring the user to know the source.
- Public files paraphrase concepts into behavior — no long quotes, no
  reproduced exercises, no distinctive phrasing copied in.
- Registry rows map all public references and templates needed by each
  intent; no orphan references.
- Source grounding, when present, is concise and operational rather
  than a summary of the source.
- Generated evals test activation (positive and negative) and the main
  workflow.
- `skill.json.status` is `published`; repository-level prerelease tags carry
  maturity caveats.

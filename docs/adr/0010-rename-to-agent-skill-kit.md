# ADR 0010: Rename to `agent-skill-kit`; reframe from cited-literature catalog to a personal skill kit

**Status:** Accepted (2026-06-18). Updates the **Purpose** of [`constitution.md`](../../constitution.md) and relaxes the `inspired_by` requirement documented in `AGENTS.md` §Per-skill required artifacts. Does not disturb the other invariants (release-artifact discipline, `just check` green, reflection-log/W1 for *repo* rules, schema parity, resolvable maintainers).

## Context

`informed-skills` positioned itself as "a catalog of Agent Skills grounded in cited literature; the published skills ARE the product," enforced by a hard `inspired_by` schema gate (every skill required a non-empty, literature-backed provenance list). Two pressures outgrew that framing:

1. **The actual use is a personal kit, not a literature catalog.** The repo is becoming "the Agent Skills the maintainer actually uses." Some are literature-derived; some are simply battle-tested in real work and aren't traceable to cited sources. A hard cited-grounding gate blocks shipping a skill you use but didn't derive from a book or paper.
2. **Re-authoring beats nothing; linking beats re-authoring.** When a useful skill already exists elsewhere, the right move is to *link* to it from the README, not to clone it under a citations requirement.

The "informed" moniker encodes the cited-literature promise as the project's identity. Moving away from that promise means moving away from the name.

## Decision

- **Rename `informed-skills` → `agent-skill-kit`** across the in-repo identity surfaces (README, `AGENTS.md`, `constitution.md`, `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `llms.txt`/`llms-full.txt`, schema `$id`s, config-file headers, the README image). The GitHub repo rename (`gh repo rename`) and the on-disk directory rename are the maintainer's actions; the install command becomes `npx skills add Thulr/agent-skill-kit`.
- **Reframe the Purpose** (constitution) to "the installable Agent Skills the maintainer uses in real coding-agent work" — most grounded in cited sources, but grounding is **encouraged, not required**, and skills worth using that live elsewhere are linked from the README rather than re-authored.
- **Lighten the cited-grounding gate.** `schemas/skill.schema.json` no longer lists `inspired_by` in `required`, and its `minItems` is `0` — an absent or empty `inspired_by` validates. `AGENTS.md` documents it as encouraged.
- **Rename the repo-local authoring skills** `informed-skill-curator` → `skill-curator` and `informed-skill-reviewer` → `skill-reviewer` (drop the "informed" prefix), in both the `.agents/skills/` and `.claude/skills/` mirrors.
- **Add a README "skills I also use" section** for pointers to external skills, rather than cloning them.

## Consequences

- The `--skill` install path changes; `Thulr/informed-skills` stops resolving once the GitHub repo is renamed (the maintainer's action). All in-repo install examples now read `Thulr/agent-skill-kit`.
- `inspired_by` is no longer a hard gate; existing skills keep their provenance, and new "skills I use" may ship without it. Cited grounding remains the norm for literature-derived skills.
- **Historical artifacts keep the old name as record:** `docs/audits/*`, ADR-0001, `docs/agent-readiness-2026-05-15.md`, and the dated reflection-log/research entries retain `informed-skills` rather than rewriting history.
- Governance is lightened at the *identity/grounding* layer only. `just check`, release-artifact discipline, the destructive-bash hook, schema parity, and the reflection-log/W1 promotion floor for *repo* rules all stand.
- Supersedes the "grounded in cited literature" sentence in the constitution Purpose and the "non-empty `inspired_by`" language in `AGENTS.md`.

## History

- **2026-06-18:** Original decision (this ADR). Triggered by the maintainer reframing the repo as a personal, link-friendly kit rather than a citations-gated catalog.

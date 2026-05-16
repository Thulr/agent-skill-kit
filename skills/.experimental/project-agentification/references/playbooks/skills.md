# skills

## What it is

The skills surface covers SKILL.md bundles (Agent Skills, agentskills.io open standard) — the
most portable harness-specific capability unit beyond AGENTS.md. A skill is a directory containing
`SKILL.md` with YAML frontmatter (`name`, `description`, optional `license`, `metadata`) plus
optional `scripts/`, `references/`, and `assets/` subdirectories.

Per-harness paths: `.claude/skills/<name>/SKILL.md` (Claude Code; `.claude/commands/` is legacy,
still works, merged into skills in Claude Code v2.1.101, April 2026); `.agents/skills/<name>/SKILL.md`
(Codex, invoked as `$skill-name` or `/skills`); GitHub Copilot's awesome-copilot ecosystem.
Anthropic published Agent Skills as an open standard at agentskills.io.

Progressive disclosure is the defining feature: only the ~100-token frontmatter loads at session
start; full instructions load on trigger — making skills radically cheaper than always-loaded
AGENTS.md prose for capability-specific workflows.

## Why it matters for agents

- **Token budget.** Skills load only on trigger — ~100-token metadata vs. a full instruction set
  per session; this is the dominant cost advantage over always-loaded AGENTS.md prose. (W6)
- **Capability encapsulation for single-agent topologies.** Skills let a single agent carry many
  capabilities without loading all simultaneously — how single-agent topologies stay focused and
  avoid Cognition's conflicting-implicit-decision failure mode. (W4)
- **Skills ≠ AGENTS.md.** Vercel evals: AGENTS.md 100% vs skills 79% on global repo conventions.
  AGENTS.md wins for always-on context; skills win for on-trigger capability-specific workflows.
  Routing the wrong content to the wrong surface degrades both. (W7)
- **Unit of distribution.** `inngest/inngest-skills` and `apollographql/skills` demonstrate
  publishing skills as standalone repos — cross-repo capability sharing without codebase access.
- **Cross-harness portability.** `.claude/skills/` → `.agents/skills/` requires minimal adaptation;
  agentskills.io is the shared contract — the closest to write-once-run-anywhere in today's ecosystem.

## Heuristics by intent

### assess

- **H1.** Verify SKILL.md frontmatter contains `name` and `description` — absent or vague
  description means the harness cannot match the skill to user intent; the ~100-token trigger
  signal is the only thing the model sees before full-load. (severity cap: 3; lens: cold-agent)
- **H2.** Check whether the skill description uses pushy, trigger-word-rich language — a
  description that names the skill without specifying when to use it will be silently skipped;
  implicit matching requires explicit triggers (see canonical example below). (severity cap: 3;
  lens: cold-agent)
- **H3.** Confirm repeated team workflows (PR description, changelog entry, security review,
  test scaffolding, migration) have corresponding skills rather than living as prose in AGENTS.md
  — prose-in-AGENTS.md is always-loaded token cost; skills are on-trigger. (severity cap: 2;
  lens: auditor)
- **H4.** Audit `.claude/commands/` for legacy slash commands that duplicate capability now
  available as `.claude/skills/` — dual-surface duplication creates drift and inflates the
  always-loaded token budget with redundant definitions. (severity cap: 2; lens: maintainer)
- **H5.** Verify each skill directory has `SKILL.md` at root with optional `scripts/`,
  `references/`, `assets/` — non-standard layouts break harness discovery. (severity cap: 2;
  lens: cold-agent)
- **H6.** Check skill descriptions don't share trigger vocabulary — near-identical triggers
  cause both to load or neither; each skill must own a distinct activation vocabulary.
  (severity cap: 2; lens: maintainer)

### harden

- **H1.** Skill never triggers → rewrite `description` using the pushy-description strategy
  (`anthropics/skills` skill-creator): *"Make sure to use this skill whenever the user mentions
  [trigger A], [trigger B], or wants to [outcome C], even if they don't explicitly ask for
  '[skill name].'"*
- **H2.** Workflow instructions bloating AGENTS.md → extract to `.claude/skills/<name>/SKILL.md`;
  replace with one reference line in AGENTS.md (`PR descriptions → pr-describe skill`); never
  inline skill instructions.
- **H3.** Legacy `.claude/commands/` accumulating drift → migrate to `.claude/skills/<name>/SKILL.md`;
  keep command stubs during transition; delete after one sprint.
- **H4.** `scripts/` or `references/` assets diverge from SKILL.md → add CI lint asserting SKILL.md
  references each asset by name; unreferenced files are dead weight or evidence of a missed update.
- **H5.** Skills needed cross-repo → extract to `<org>/skills` repo (`inngest/inngest-skills`
  pattern); reference from AGENTS.md; document install path in onboarding.

### scaffold

- **Do not autogenerate skills from boilerplate (W1).** Bootstrap from an observed agent failure
  or a repeated manual workflow; a skill with placeholder instructions costs tokens and produces
  no lift.
- **H1.** Write `description` frontmatter before the skill body — it is the trigger signal. End
  with an explicit "use this skill whenever..." clause naming at least three trigger phrases.
- **H2.** Structure SKILL.md as: activation context → step-by-step workflow → output contract →
  failure modes. Reference `scripts/` and `references/` assets by relative path.
- **H3.** Project-scoped: `.claude/skills/<name>/` (Claude Code) or `.agents/skills/<name>/`
  (Codex). Team-scoped: `<org>/skills` repo. Never store skills only in chat history or a wiki.
- **H4.** (W1 guard) Before writing a skill, name the observed failure or manual step it addresses
  in a comment at the top of SKILL.md. "Might be useful" is not a valid trigger.

### diagnose

- **H1.** Skill exists but never loads → rank: (1) `description` uses only the skill name — no
  trigger vocabulary; rewrite with pushy-description (harden H1); (2) wrong harness path —
  verify `.claude/skills/` (Claude Code) or `.agents/skills/` (Codex); (3) harness version
  predates skills — check Claude Code v2.1.101 (April 2026) minimum.
- **H2.** Agent loads the wrong skill → rank: (1) overlapping trigger vocabulary — add explicit
  exclusions to each description; (2) one description is a superset of another — split or merge;
  (3) AGENTS.md prose matches before the skill — remove prose, add a reference line instead.
- **H3.** Skill instructions followed inconsistently → rank: (1) skill body exceeds the harness
  load limit — trim or split; (2) `scripts/` or `references/` files missing or renamed — verify
  asset paths; (3) duplicated in a legacy `.claude/commands/` file loaded first.
- **H4.** Skills coverage thin, agents still working from scratch → audit sessions: find the three
  most common "from scratch" workflows by tool-call count; each is a skill candidate; prioritize
  by frequency × error rate.

## Empirical warnings

- **W1** — Autogenerated skills drop task success ~3%, inflate cost >20%; create only from
  observed agent failures or manual team workflows; no placeholder copy.
- **W4** — Skills are how single-agent topologies stay focused: capability encapsulation avoids
  Cognition's conflicting-implicit-decision failure mode (Principle 2).
- **W6** — On-trigger ~100-token metadata vs. always-loaded prose is the dominant cost difference;
  route capability-specific workflows to skills, global conventions to AGENTS.md.
- **W7** — Not interchangeable: AGENTS.md 100% vs skills 79% on Vercel's Next.js global rules;
  each surface wins only in its intended role.
- **W8** — Evidence is mixed; hand-curate, keep descriptions trigger-rich, evolve from observed
  usage; prefer on-demand → on-trigger → always-loaded escalation.

## Canonical examples

- **anthropics/skills** (skill-creator) — canonical pushy-description example; the skill-creator
  skill's own description encodes the lesson: *"Instead of 'How to build a simple fast dashboard...',
  you might write '...Make sure to use this skill whenever the user mentions dashboards, data
  visualization, internal metrics, or wants to display any kind of company data, even if they don't
  explicitly ask for a "dashboard."'"*
- **inngest/inngest-skills** and **apollographql/skills** — first-party org-level skill libraries
  demonstrating the distribution-as-skills pattern; skills published as standalone repos for
  cross-repo adoption without requiring access to the main application codebase.
- **informed-skills/skills/dx-heuristics/** — local reference for the SKILL.md shape in this
  repo: YAML frontmatter → skill body → `references/`, `evals/`, `templates/` subdirectories;
  `skill.json` for structured metadata alongside SKILL.md.

## Sources

- "Agent Skills (agentskills.io)" — canonical open standard; SKILL.md frontmatter schema
  (`name`, `description`, optional `license`, `metadata`); `scripts/`, `references/`, `assets/`
  layout; progressive disclosure (~100-token metadata at startup, full load on trigger);
  per-harness install paths (`.claude/skills/`, `.agents/skills/`).
- "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" —
  Mündler et al. (arXiv:2602.11988); empirical basis for W1; autogenerated context files drop
  task success ~3% and inflate cost >20%.
- "Effective Context Engineering for AI Agents" — Anthropic; token-budget framing (W6);
  on-trigger vs always-loaded load classification; smallest-high-signal-token principle.
- "Don't Build Multi-Agents" — Cognition (Walden Yan, June 12, 2025); Principle 2 (conflicting
  actions from conflicting implicit decisions); skills as the mechanism for capability encapsulation
  in single-agent topologies (W4).

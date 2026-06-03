# Activation cases — agent-rules

Natural-language scenarios the skill should handle. Cross-references the
`evals/trigger-evals.json` queries with the expected behavior; mostly
relevant when running activation against a model (Stage 1.5 — not yet
wired).

## Positive — should activate

1. **"Set up a reflection log for tracking agent failures in this repo."** → `capture`
   - Scaffolds `docs/reflection-log/README.md` + `_template.md`.
   - Adds README §Agents pointer if missing.
   - Stage-0 README includes the recording-bar / promotion-bar callout.

2. **"We've been recording agent failures and have a few patterns now — promote them into rules."** → `promote`
   - Loads `docs/reflection-log/[0-9]*.md`.
   - Groups by `sub-surface:` frontmatter; finds groups with ≥3 entries.
   - Proposes the smallest closing change for each, preferring hook > CI gate > AGENTS.md rule (W3).
   - Refuses to act on groups < 3 (W1 floor).

3. **"Score our repo against Level 4 / Level 5 of the Engineering Agents maturity rubric."** → `assess-l4l5`
   - Requires user to confirm current Level 1–3 score (from `agent-readiness`).
   - Refuses if Level 1–3 < 3 (fix lower-level gaps first).
   - Otherwise scores Levels 4–5 against `references/core/maturity-rubric.md`.
   - For 7+ gaps, any level-ceiling blocker, or a save/track request, saves
     both `agent-rules-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
     and `agent-rules-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`
     under `docs/audits/`, or the matching `audit-artifacts/` fallback.

4. **"Find any sub-surfaces with 3+ entries and propose a rule that closes the gap."** → `promote`
   - Explicit invocation of the promote workflow; no ambiguity.

5. **"Promote these hook bypass entries into a gate."** → `promote`
   - Loads `references/playbooks/gate-hardening.md`.
   - Requires a variant matrix, regression fixture, and CI binding before
     calling the gate complete.

6. **"Are we at Sovereign Engineering level yet?"** → `assess-l4l5`
   - Maps to Level 5 specifically; same workflow as `assess-l4l5`.
   - Reports both saved tracking paths when artifact thresholds are met; does
     not merely offer to create them.

## Negative — should NOT activate

1. **"Refactor our authentication module."** — unrelated coding task.
2. **"Write a SQL migration to add a users table."** — unrelated coding task.
3. **"Help me debug this failing test in Python."** — unrelated debugging.
4. **"Set up an AGENTS.md for my repo."** — `agent-readiness`'s job, not this skill's.
5. **"Make my repo work well with Claude Code."** — `agent-readiness`'s job; this skill is the evidence-driven layer on top.

## Edge

1. **"Add a new entry to our reflection log."** — borderline `capture`.
   The skill should respond by pointing at the template (`_template.md`)
   and the instructions in `README.md`, not by writing a new entry on
   the user's behalf (the user knows their failure; the skill knows the
   workflow).

2. **"Generate AGENTS.md from our observed failures."** — borderline
   between this skill (uses the reflection log) and `agent-readiness`
   (scaffolds AGENTS.md). The right answer: run
   `agent-readiness` first to scaffold the project-context AGENTS.md,
   then run this skill's `promote` workflow to layer in rules derived
   from the reflection log. State this explicitly rather than picking
   one.

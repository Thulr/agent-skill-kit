# reflection-log

The sole sub-surface this skill owns directly. Covers capturing observed
agent failures, scoping the recording bar low (one observation with a
`What to do differently` line), and gating promotion (turning recurring
patterns into rules / hooks / gates) at the W1 ≥3-entries floor.

## What it is

A per-file log under `docs/reflection-log/` (one
`YYYY-MM-DD-<slug>.md` per failure) that captures observed agent
failures with enough specificity that future contributors can:

- Read entries by date (`ls [0-9]*.md` — filenames sort chronologically).
- Group entries by sub-surface (`grep -l 'sub-surface: gates'
  [0-9]*.md`) to find patterns.
- Trace closed entries to the PR / commit that fixed them.

Single-file table shapes (e.g., the earlier
`docs/agent-failures.md` pattern) do not scale past ~10–20 entries —
rows wrap, pattern detection requires manual scanning, and naming drift
accumulates (the source literature calls this artifact a *reflection
log*, not a "failures table"). Per-file with frontmatter is the
scalable shape.

Engineering Agents — Harness Assessment names this artifact and treats
its recency as a Level 3 maturity signal ("checks whether
`REFLECTION_LOG.md` has recent dates"). The directory shape used here
extends the source's single-file framing while preserving the source's
naming.

## Why it matters for agents

- **Patterns surface, not noise.** Single observations log easily;
  pattern detection runs `grep` against frontmatter tags, not a
  human-scan of a table. The W1 ≥3 floor only fires when there's
  actual evidence of a recurring gap.
- **Audit trail is intrinsic.** Each entry's `## Closed by` field
  records the PR/commit that resolved the gap. Reviewers reconstruct
  "why does this rule exist?" by reading the cited reflection-log
  entry; no separate audit log.
- **W1's promotion floor is enforceable.** Rules / hooks / gates in
  `AGENTS.md` cite their reflection-log entries by filename. A
  reviewer can verify the ≥3 floor was met by reading those entries.
  Without the per-file shape, the citation has nowhere to point.

## Heuristics by intent

### capture

- **H1.** Refuse to scaffold the log directory unless the repo has
  (or will have) a `README.md §Agents` pointer to it. The log lands
  as an orphan otherwise — present on disk, invisible to any agent
  walking in fresh. (Apply order: scaffold log + add pointer, never
  one without the other.)
- **H2.** The Stage-0 README MUST explicitly distinguish the
  recording bar (low — one observation with a `What to do differently`
  line) from the promotion bar (high — ≥3 entries describing the same
  gap). Conflating them causes reviewers to self-filter single
  observations as "not yet a pattern."
- **H3.** Frontmatter is mandatory per entry: `date`, `harness`,
  `sub-surface`, `severity`, `status`, `related`. Without
  frontmatter, `grep` pattern detection produces noise (the schema
  example strings in `README.md` would match).
- **H4.** Glob examples in the README must use `[0-9]*.md`, not
  `*.md` — the latter matches `README.md` and `_template.md` (which
  contain literal frontmatter strings in their schema docs) and
  inflates any count by 1–2, potentially tripping the W1 ≥3 floor
  prematurely.

### promote

- **H1.** Group entries by frontmatter tag: `grep -l 'sub-surface:
  <name>' docs/reflection-log/[0-9]*.md`. A group of ≥3 entries
  describing the same gap is the W1 floor — propose a closing
  change. A group of 2 is "watch"; a group of 1 is "record only."
- **H2.** Propose the smallest change that closes the pattern. In
  order of preference: hook (100% enforcement, W3) > CI gate >
  `AGENTS.md` rule sentence (~70% enforcement, W3 — last resort). A
  prose rule that the agent ignores 30% of the time is not a
  resolution.
- **H3.** The proposed rule / hook MUST cite the reflection-log
  entries that justify it (by filename, in the commit message and
  optionally in the AGENTS.md rule itself). Reviewers verify W1
  compliance by reading those citations.
- **H4.** Set every cited entry's `status:` to `resolved` and fill
  `## Closed by` in the same commit. Open entries that contributed
  to a resolved pattern create false signal for the next `promote`
  pass.
- **H5.** If the recurring gap is *architectural boundary violations*
  (layer-skipping, wrong-direction dependencies, forbidden imports,
  cycles), prefer structural fixes: architecture lints/tests as
  CI-required checks. Use `clean-architecture` to define the boundary
  model; use `project-agentification` gates guidance to enforce it.

### assess-l4l5

- **H1.** Assume Levels 1–3 already scored by
  `project-agentification`. Require user to state the current
  Level 1–3 score before running this; refuse if the score is < 3
  (fixing lower-level gaps is the priority).
- **H2.** For Level 4 (Specification Architecture): verify
  `docs/specs/`, `docs/adr/`, `docs/runbooks/` exist and are
  current (recent dates). Verify safety gates exist on agent
  pipelines (every prompt / tool / policy change triggers targeted
  evals).
- **H3.** For Level 5 (Sovereign Engineering): verify a reusable
  plugin / skill catalog exists; cost tracking per agent session
  is wired in; model-routing policies are documented; CODEOWNERS
  + branch-protection are enforced on agent-surface paths;
  SLSA-style attestations are emitted for release artifacts.

## Empirical warnings

- **W1 (dominant)** — Don't autogenerate AGENTS.md / CLAUDE.md;
  hand-curate from observed failures with the ≥3 floor. See
  `references/empirical-warnings-w1.md`.
- **W3** — Hooks enforce at 100%, prose at 70%. Promoted patterns
  should land as hooks/CI gates where possible, not as AGENTS.md
  prose.
- **W6** — Reflection-log entries are on-demand context (read only
  during `promote`), not always-loaded. They don't inflate the
  always-loaded surface.

## Templates

- `templates/artifacts/reflection-log/README.md` — directory index
  for `docs/reflection-log/` (carries the recording-bar /
  promotion-bar callout).
- `templates/artifacts/reflection-log/_template.md` — per-entry
  template (frontmatter + sections).

## Sources

- "Engineering Agents — Harness Assessment" — Engineering Agents;
  treats the reflection log as a Level 3 maturity signal. This
  playbook extends the source's single-file framing to a per-file
  directory for scalability.
- "Evaluating AGENTS.md" — Mündler et al. (arXiv:2602.11988);
  empirical basis for W1's ≥3-entries promotion floor.
- "AGENTS.md" — Agentic AI Foundation; the instruction-surface
  artifact `promote` writes rules into (scaffolded by
  `project-agentification`, not this skill).

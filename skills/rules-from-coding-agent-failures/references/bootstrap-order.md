# Bootstrap order

The W1 ≥3 floor creates a hard staging dependency for repos using this
workflow. **Scaffold in this order, never out of it:**

1. **Stage 0** — reflection-log directory (`docs/reflection-log/`) with
   `README.md` index + `_template.md` entry template + a `README.md
   §Agents` pointer at the repo root pointing into the log. The
   directory is exempt from the W1 floor because it does not *contain*
   agent instructions; it *captures the observations* future
   instructions will be hand-curated from. **The Stage-0 README MUST
   explicitly distinguish the recording bar (low — one observation with
   a `What to do differently` line is enough) from the promotion bar
   (high — ≥3 entries describing the same gap).** Conflating the two
   causes reviewers and agents to self-filter entries.
2. **Stage 1** — `AGENTS.md` exists. **This skill does not scaffold it
   — use `harden-repo-for-coding-agents` for that.** Once it's there, this
   skill's `promote` workflow can add rules to it that trace to
   reflection-log entries.
3. **Stage 2+** — hooks, gates, evals — each grounded in a promoted
   pattern from the log.

**Refuse to run `promote` without Stage 0 in place** (no log → no
patterns → no evidence-driven rule).

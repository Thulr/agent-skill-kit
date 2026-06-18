# W1 — Don't autogenerate AGENTS.md / CLAUDE.md

Sole-tenant of `rules-from-coding-agent-failures`. W1 belongs here (not in
the shared `_shared/empirical-warnings.md`) because it's the failure-driven
core of this skill and does not apply to `harden-repo-for-coding-agents`'s
project-context-first audience.

ETH Zürich / LogicStar.ai (Gloaguen, Mündler et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*, arXiv:2602.11988, Feb 2026) found that **LLM-generated context files drop task success ~3% on average and inflate cost by over 20%**, while developer-written files improved success by only ~4%. Anthropic's `/init`, Cursor's `/Generate Cursor Rules`, and Codex's auto-init produce plausible but low-value scaffolds. **Hand-curate from observed failures.** The `promote` intent of this skill refuses to write any rule / hook / gate without **at least 3 stated observed-failure entries in `docs/reflection-log/`** that describe the same gap — one failure easily overfits to boilerplate; three forces a pattern.

## Recording bar vs. promotion bar

W1's ≥3 floor gates **promotion**, not **recording**. The recording bar
is low: if a contributor can write a non-trivial `## What to do
differently` section, the entry is worth recording. One observation is
enough. The ≥3 floor only applies when turning a recurring pattern into
a rule / hook / gate.

Conflating the two bars (treating ≥3 as a *recording* threshold) causes
reviewers to self-filter single observations as "not yet a pattern,"
which silently under-records and starves `promote` of evidence. The
reflection-log README in each consuming repo must spell out this
distinction.

## Audience caveat

This warning applies **only when a feedback signal exists** that lets a
team observe agent failures (qualitative — "the agent edited the wrong
file" with eyes — or quantitative — eval-suite regressions, telemetry
deltas). For repos without that signal, the W1 ≥3-floor is unenforceable
in practice (no failures observed → no floor to cross) and the rule is
moot. Those repos should use `harden-repo-for-coding-agents` for project-context-first
AGENTS.md scaffolding, not this skill.

## See also

W2–W10 in `empirical-warnings.md` (symlinked to
`skills/_shared/empirical-warnings.md`).

---
date: 2026-06-03
harness: claude-code
sub-surface: skills
severity: 2
status: open
related: []
---
# Identifier-rename grep skipped symlinked shared content; static checks don't gate doc prose

## What happened

During the test-audit `review`->`audit` intent rename (PR #46, merged as
`b494bd7`), I enumerated every `review` reference with
`grep -rni 'review' skills/test-audit/` and treated the result as the complete
work-list. It was not. `grep -r` does **not** follow symlinked files, and most
of test-audit's reference content is symlinked into `skills/_shared/test/`
(`references/subagent-dispatch.md`, `references/core/{personas,oracles,failure-modes}.md`,
`references/layers/*.md`). So stale `review` identifier references survived the
first pass:

- `skills/_shared/test/subagent-dispatch.md` — the `--surface=all` fan-out still
  pointed at the renamed-away `references/intents/review.csv` and
  `templates/review-report-multi.md`: a documented dispatch path to files that no
  longer exist.
- `skills/_shared/test/core/{personas,oracles,failure-modes}.md` — stale
  `` `review` `` intent refs (per-intent guidance, an oracle "review mode", a tag
  example).

`just check` was green the whole time. `run-static-checks.sh` validates file
existence and CSV/registry structure, but does **not** gate the prose of
reference docs, so stale identifier references inside `.md` reference content are
invisible to it. The misses were caught only by Codex's review on the PR (the
broken dispatch path), then a broader sweep.

## What to do differently

When renaming an identifier (intent ID, template/file name, route) that may
appear in a skill's reference content, sweep the **canonical `_shared/` tree
directly**, not just the skill directory — symlinks hide content from `grep -r`:

- `grep -rn '<old-id>' skills/_shared/ skills/<skill>/` (the `skills/_shared/`
  arm is the load-bearing one), or follow symlinks explicitly with
  `grep -R '<old-id>' skills/<skill>/`.
- Do not treat a green `just check` as proof a rename is complete: the static
  checks gate structure and file existence, not the prose of `.md` reference
  docs. Rename coverage must be verified by content search, not by the gate.

This is **one** observation — below the W1 >=3 promotion floor, so record only;
do not scaffold a gate (e.g. a CI check that greps `skills/_shared/` for retired
identifiers) until two more symlink/rename-coverage misses surface.

## Closed by

Not yet closed. The specific instances were fixed in PR #46 (`b494bd7`); the
systemic gap (rename coverage vs symlinked shared content + un-gated doc prose)
has no rule or gate yet, and is below the W1 >=3 floor for promoting one.

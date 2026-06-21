# activation-cases.md — codex-cli

Natural-language behavioral cases for routing **into** `codex-cli` and, just as
importantly, **away** from it toward neighboring skills. Shape mirrors the
canonical `trigger-evals.json`; this file adds the expected/forbidden behavior
that a schema can't capture. Routes are the `use_case` ids in
[`references/use-case-registry.csv`](../references/use-case-registry.csv).

## Positive

- "Ask Codex to review the changes Cursor just made." → `review-uncommitted`
- "Get a second opinion from Codex on this branch before I open the PR." → `review-branch`
- "Have Codex review commit abc123 for regressions." → `review-commit`
- "Ask Codex what it thinks about this migration plan." → `second-opinion`
- "Ask Codex what recurring mistakes it keeps making across my projects." → `cross-project-reflection`
- "Prepare the Codex prompt to review my changes, but don't run it yet." → `prompt-prep`
- "Codex keeps failing — check my auth and sandbox setup." → `diagnose`

## Negative

These must **not** route to `codex-cli`:

- "Refactor this React component." — ordinary coding work, no external reviewer.
- "Harden this repo's AGENTS.md and add hooks for coding agents." → `harden-repo-for-coding-agents`.
- "Promote this recurring agent failure into an AGENTS.md rule." → `rules-from-coding-agent-failures`.
- "Audit our CLI's developer experience and score it." → `dx-audit` (this kit's own heuristic review, not an external Codex pass).

## Edge

- "Review my changes." — ambiguous: bare review intent with no Codex / second-opinion / different-provider signal. Prefer a local review skill; only route here if the user names Codex or asks for an external/second opinion.
- "Get a second opinion on this architecture decision from a different model." → `second-opinion` even though Codex is not named: "second opinion from a different model" is this skill's territory.

## Bare-activation behavior

Prompt: `/codex-cli`

Expected:

- Presents a concise menu of modes and use cases from the registry, then waits.
- Does **not** run `codex`.
- Asks what scope or task the user wants (one question, not a multi-question form).

## Main scenario — review uncommitted work

Prompt: `Ask Codex to review the changes Cursor just made.`

Expected:

- Selects `review-uncommitted`; runs `scripts/codex-review-changes.sh` from the repo under review.
- Defaults to native `codex review --uncommitted` (no prompt — `codex review` rejects a `[PROMPT]` with every scope flag on 0.141.0, so it uses its built-in review standard; do not pass `-- -`).
- Presents Codex output as external review feedback and verifies obvious file references before relaying them.

Forbidden:

- Passing `--dangerously-bypass-approvals-and-sandbox`.
- Asking Codex to edit files directly.
- Treating Codex output as unquestionable truth.

## Cross-project reflection scenario

Prompt: `Ask Codex what recurring mistakes it remembers making across projects.`

Expected:

- Selects `cross-project-reflection`; uses `scripts/codex-cross-project-reflect.sh`, not a repo-review script.
- Runs with `--cd` set to a neutral/global directory and `--skip-git-repo-check`, so the launching repo is **not** treated as the audit scope.
- Treats Codex's self-assessment as leads needing corroboration, not durable rules.

Forbidden:

- Reviewing only the current repository.
- Passing raw transcripts or secrets without explicit approval.

## Prompt-prep regression

Prompt: `Prepare the Codex prompt but do not run it.`

Expected:

- Uses `--dry-run` / prompt-prep behavior; prints command and prompt material.
- Does not call the live Codex CLI.

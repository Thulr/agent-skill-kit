# activation-cases.md — cursor-cli

Natural-language behavioral cases for routing **into** `cursor-cli` and **away**
toward its interop siblings (`codex-cli`, `claude-code-cli`) and the kit's own
review skills. Routes are the `use_case` ids in
[`references/use-case-registry.csv`](../references/use-case-registry.csv).

## Positive

- "Ask Cursor to review the changes I just made." → `review-working-tree`
- "Get a second opinion from Cursor on this branch before I open the PR." → `review-branch`
- "Have gpt-5 review this design via Cursor." → `second-opinion`
- "Prepare the Cursor prompt to review my staged changes, but don't run it." → `prompt-prep`
- "Cursor agent keeps failing — check my setup and auth." → `diagnose`

## Negative

These must **not** route to `cursor-cli`:

- "Refactor this React component." — ordinary coding work, no external reviewer.
- "Ask **Codex** to review my changes." → `codex-cli` (different external agent).
- "Ask **Claude Code** to review my changes." → `claude-code-cli`.
- "Audit our CLI's developer experience and score it." → `dx-audit` (this kit's own heuristic review).
- "Harden this repo's AGENTS.md and hooks." → `harden-repo-for-coding-agents`.

## Edge

- "Review my changes." — ambiguous: bare review intent with no Cursor / second-opinion / different-model signal. Prefer a local review skill; only route here if the user names Cursor or asks for an external/second opinion.
- "Get a second opinion on this code from gpt-5." → `second-opinion` — "a second opinion from gpt-5/a different model" is cursor-cli's territory (model diversity) even when Cursor is not named, since cursor-agent is the kit's multi-model interop path.

## Bare-activation behavior

Prompt: `/cursor-cli`

Expected:

- Presents a concise menu of modes and use cases from the registry, then waits.
- Does **not** run `cursor-agent`.
- Asks what scope/model the user wants (one question, not a multi-question form).

## Main scenario — review working-tree changes

Prompt: `Ask Cursor to review the changes I just made.`

Expected:

- Selects `review-working-tree`; runs `scripts/cursor-review-changes.sh` from the repo under review.
- Builds the git diff itself and feeds it to `cursor-agent -p --mode plan --output-format text` (read-only — cursor-agent won't edit).
- Presents cursor-agent's output as external review feedback and verifies obvious file references before relaying them.

Forbidden:

- Passing `-f` / `--force` / `--yolo` or `--sandbox disabled`.
- Bare `-p` without `--mode plan`/`ask` (print mode can write and run shell).
- Treating cursor-agent's output as unquestionable truth.

## Different-model second opinion

Prompt: `Have gpt-5 review this migration plan via Cursor.`

Expected:

- Selects `second-opinion`; runs `scripts/cursor-ask.sh --model gpt-5` (read-only `--mode plan`).
- Frames the result as a second opinion from a *different* model than the one that produced the work.

## Diagnose / trust scenario

Prompt: `cursor-agent isn't running headlessly — what's wrong?`

Expected:

- Selects `diagnose`; uses `scripts/cursor-doctor-check.sh`.
- Surfaces likely blockers: not installed/authenticated, **workspace not trusted** for `-p` runs, or model unavailable.

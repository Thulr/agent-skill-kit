# activation-cases.md — claude-code-cli

Natural-language behavioral cases for routing **into** `claude-code-cli` and
**away** toward its interop siblings (`codex-cli`, `cursor-cli`) and the kit's own
review skills. Routes are the `use_case` ids in
[`references/use-case-registry.csv`](../references/use-case-registry.csv).

## Positive

- "Ask Claude Code to review the changes Cursor just made." → `review-working-tree`
- "Get a second opinion from Claude on this branch before I open the PR." → `review-branch`
- "Have Claude Code weigh in on whether this caching design is sound." → `second-opinion`
- "Ask Claude what recurring mistakes it keeps making across my projects." → `cross-project-reflection`
- "Kick off a Claude ultrareview of this branch." → `ultrareview`
- "Prepare the Claude Code prompt to review my staged changes, but don't run it." → `prompt-prep`

## Negative

These must **not** route to `claude-code-cli`:

- "Refactor this React component." — ordinary coding work, no external reviewer.
- "Ask **Codex** to review my changes." → `codex-cli` (different external agent).
- "Ask **Cursor** to review my changes." → `cursor-cli`.
- "Audit our CLI's developer experience and score it." → `dx-audit` (this kit's own heuristic review, not an external Claude pass).
- "Harden this repo's AGENTS.md and hooks." → `harden-repo-for-coding-agents`.

## Edge

- "Review my changes." — ambiguous: bare review intent with no Claude / second-opinion / external-agent signal. Prefer a local review skill; only route here if the user names Claude Code or asks for an external/second opinion.
- "Have another agent review what Cursor wrote and give an independent take." → `review-working-tree` — "another agent reviewing Cursor's work" is this skill's territory when Claude is the implied reviewer.

## Bare-activation behavior

Prompt: `/claude-code-cli`

Expected:

- Presents a concise menu of modes and use cases from the registry, then waits.
- Does **not** run `claude`.
- Asks what scope or task the user wants (one question, not a multi-question form).

## Main scenario — review working-tree changes

Prompt: `Ask Claude Code to review the changes Cursor just made.`

Expected:

- Selects `review-working-tree`; runs `scripts/claude-review-changes.sh` from the repo under review.
- Builds the git diff itself and feeds it to `claude -p --permission-mode plan --output-format text` (read-only — Claude won't edit).
- Presents Claude's output as external review feedback and verifies obvious file references before relaying them.

Forbidden:

- Passing `--dangerously-skip-permissions` or `--permission-mode bypassPermissions`.
- Asking Claude to edit files directly.
- Treating Claude's output as unquestionable truth.

## Cross-project reflection scenario

Prompt: `Ask Claude what recurring mistakes it remembers making across projects.`

Expected:

- Selects `cross-project-reflection`; uses `scripts/claude-cross-project-reflect.sh`, not a repo-review script.
- Runs from a neutral directory (e.g. `$HOME`) so the launching repo is **not** treated as the audit scope.
- Treats Claude's self-assessment as leads needing corroboration, not durable rules.

## Ultrareview scenario

Prompt: `Run a Claude ultrareview on this branch.`

Expected:

- Selects `ultrareview`; explains that `claude ultrareview` is a **hosted, billed, user-initiated** cloud multi-agent review.
- Does not silently auto-run it — surfaces the command and cost/auth implications and lets the user trigger it.

## Prompt-prep regression

Prompt: `Prepare the Claude Code prompt but do not run it.`

Expected:

- Uses `--dry-run` / prompt-prep behavior; prints the prompt material.
- Does not call the live Claude Code CLI.

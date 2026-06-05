# Subagent Dispatch

Use parallel lenses for broad audits, design reviews, and measurement plans. If
subagents are unavailable, run the lenses sequentially and mark that the review
was single-threaded. Each lens is told the project tier
(`references/calibration.md`) and sizes its findings to it — below Load-bearing,
one systemic finding per mechanism, not one per artifact.

## When to dispatch

Dispatch by default when any applies:

- The scope includes more than one surface or audience.
- The user asks for an audit, redesign, or measurement plan rather than a narrow
  copy edit.
- A recommendation could help one audience and harm another.
- The target includes both human docs and agent-readable docs.

Skip dispatch when the task is a small deterministic edit, credentials or
private data would be exposed, or the user asked for a quick narrow answer.

## Lenses

### Developer-docs reviewer

Focus: first success, README/quickstart, examples, API reference, changelog,
search, versioning, and troubleshooting.

Prompt seed: "Review the target documentation as a developer trying to integrate
or maintain this product. Identify first-success blockers, stale/risky examples,
lookup failures, migration gaps, and developer-search vocabulary mismatches."

### End-user help reviewer

Focus: in-product help, empty states, onboarding, microcopy, recovery, help-center
IA, plain language, and accessibility of help content.

Prompt seed: "Review the target documentation as an end user trying to learn or
recover inside the product. Identify hidden help, blame-language errors, missing
next actions, inaccessible help media, and support-deflection gaps."

### Agent-retrieval reviewer

Focus: `llms.txt`, markdown renderings, chunk survivability, stable anchors,
agent context files, schema/tool descriptions, examples, and context budget.

Prompt seed: "Review the target documentation as an agent or RAG retriever. Identify
missing machine-readable entrypoints, bad chunk boundaries, vague trigger text,
unstable links, visual-only instructions, and unsafe action contracts."

### Content-operations reviewer

Focus: docs-as-code, ownership, telemetry, feedback loops, stale-content gates,
release integration, and measurement.

Prompt seed: "Review the target documentation as the owner of the docs program.
Identify missing quality gates, telemetry without action, unclear owners, release
process gaps, and measurement plans that cannot drive backlog work."

## Synthesis rules

1. Deduplicate findings by mechanism, not by page. Below Load-bearing (see
   `references/calibration.md`), also collapse same-mechanism per-artifact
   findings of severity ≤ 3 into one systemic finding at the highest severity it
   subsumes, and route deferred best-practice to "Later — as it grows". Keep
   every severity-4 explicit — never collapsed, never deferred.
2. Preserve audience disagreements instead of flattening them.
3. Assign severity using `references/core/severity-rubric.md`.
4. If one lens proposes a fix that harms another lens, route through
   `references/playbooks/audience-conflicts.md` before final recommendation.
5. The final output names which lenses ran and which were skipped.

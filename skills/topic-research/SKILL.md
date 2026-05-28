---
name: topic-research
description: Use when you need a structured, source-cited research report on a topic — background, current state, key concepts, debates, open questions — without a decision frame attached. Triggers on "research X for me," "tell me about X," "what's the state of X," "give me a primer on X," "literature review on X," "deep dive on X," "summarize what's known about X," "do research on Y." Do not use for validating a named product/business/feature opportunity (use opportunity-research), reviewing existing artifacts like prompts, plans, or specs (use the matching -red-team or -review skill), comparing fixed options (use tradeoff-analysis), or ideating from scratch (use brainstorming).
license: MIT
---

# Topic Research

Source-grounded structured reports on a named topic. Input: a topic.
Output: a report with citations on every load-bearing claim. No
decision required. Provenance lives in `skill.json`; this file is
runtime routing only.

**Produces:** `research-report-<YYYY-MM-DD>-<topic-slug>.md` filled
from [`templates/research-report.md`](./templates/research-report.md).

## Core principle

**Every load-bearing claim is either cited or marked as inference.**
A report that mixes synthesis with assertion without surfacing which
is which is a content brief, not research. The skill exists to keep
that line visible — and to keep the report from collapsing into the
model's prior beliefs.

## Activation

- **Bare invocation** (`"topic research"`, `"research a topic"`,
  `"start"`): ask for the topic in one sentence, then offer the depth
  choice and mode choice. Wait. No file inspection, no network calls,
  no writes.
- **Concrete invocation with topic stated**: skip to step 2.
- **Concrete invocation with ambiguous topic** (`"research AI"`,
  `"research climate"`): ask one blocker question to narrow scope
  before searching. A topic too broad returns noise; the named
  failure mode is producing a 20-page survey of nothing.
- **Object missing** (`"do research"` with no topic): ask for the
  one-sentence topic statement first.

## Workflow

1. **Clarify scope.** Restate the topic as a one-sentence research
   question with explicit inclusions and exclusions. Surface it back
   to the user for sign-off in Guided Draft mode.
2. **Pick depth.** Match the request to one of:
   - `brief` — single-section orientation, ~5 high-quality sources,
     ~1-page output. Use for "primer," "what is X," "introduce me to X."
   - `survey` (default) — multi-section structured report, ~15–20
     sources, full template. Use for "research X for me," "report on X."
   - `deep-dive` — exhaustive review with citation chasing
     (forward and backward from anchor sources), ~30+ sources,
     extended template. Use for "thorough review," "what does the
     literature say," "exhaustive."
3. **Plan the search.** Load
   [`references/search-strategy.md`](./references/search-strategy.md).
   Name the source types to consult (peer-reviewed, industry reports,
   standards bodies, primary sources, expert practitioners), the
   search terms, and explicit exclusions. In Guided Draft mode,
   surface the plan before executing.
4. **Execute the search.** Run web searches per the plan; for
   `deep-dive`, snowball — follow citations forward and backward from
   anchor sources until new sources stop adding new claims. Apply
   [`references/source-triage.md`](./references/source-triage.md):
   prefer primary over secondary, recent over dated unless seminal,
   independent over vendor-aligned, peer-reviewed or institutional
   over editorial.
5. **Synthesize against the template.** Fill
   [`templates/research-report.md`](./templates/research-report.md):
   topic statement, search strategy, background, current state, key
   debates, implications, sources, limitations.
6. **Apply confidence.** Tag every load-bearing claim with H/M/L per
   [`references/confidence-rubric.md`](./references/confidence-rubric.md).
   Cite at the point of claim. Mark synthesis ("inferred from X+Y")
   explicitly — never present synthesis as if it were sourced.
7. **Emit the report.** Write to
   `docs/research/research-report-<YYYY-MM-DD>-<topic-slug>.md`.
   Fall back to
   `research-output/research-report-<YYYY-MM-DD>-<topic-slug>.md`
   if `docs/research/` is unwritable. Report the path.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at
bare invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every report names:
- the one-sentence research question with explicit inclusions and
  exclusions,
- the depth mode applied (`brief` / `survey` / `deep-dive`),
- the search strategy (source types, terms, exclusions),
- confidence (H/M/L) on every load-bearing claim,
- a citation at the point of every load-bearing claim,
- explicit limitations — what was not covered, what is contested,
  what is uncertain,
- the grounding sources from `skill.json.inspired_by` for the
  methodology used.

## Subagent dispatch

Optional. For `deep-dive` topics with several distinct sub-questions,
spawn one sub-agent per sub-question, each producing one section of
the final report against its slice of the search plan. The main
agent integrates sections and applies confidence end-to-end. Skip
sub-agents for `brief` and most `survey` runs — coordination overhead
exceeds parallelism benefit at small scale.

## Reference map

- [`references/search-strategy.md`](./references/search-strategy.md) —
  how to plan the search: source types, terms, exclusions, snowballing.
- [`references/source-triage.md`](./references/source-triage.md) —
  how to filter and rank sources by primacy, recency, independence,
  peer review.
- [`references/confidence-rubric.md`](./references/confidence-rubric.md) —
  H/M/L scale and what each threshold requires.
- [`references/modes.md`](./references/modes.md) — Guided Draft /
  Autopilot / Grill Me contract.
- [`templates/research-report.md`](./templates/research-report.md) — output template.
- `evals/{activation-cases.md,run-static-checks.sh,trigger-evals.json}` — gates.
- `skill.json` — provenance, grounding sources, version, status.

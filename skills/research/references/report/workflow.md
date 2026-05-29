# Report frame — workflow

Open-ended, source-grounded research on a named topic. Input: a topic.
Output: a structured report with a citation on every load-bearing claim.
No decision required.

**Produces:** `research-report-<YYYY-MM-DD>-<topic-slug>.md` filled from
[`../../templates/report/research-report.md`](../../templates/report/research-report.md).

## Core principle

**Every load-bearing claim is either cited or marked as inference.** A report
that mixes synthesis with assertion without surfacing which is which is a
content brief, not research. This frame exists to keep that line visible — and
to keep the report from collapsing into the model's prior beliefs.

## Workflow

1. **Clarify scope.** Restate the topic as a one-sentence research question
   with explicit inclusions and exclusions. Surface it back to the user for
   sign-off in Guided Draft mode.
2. **Pick depth.** Match the request to one of:
   - `brief` — single-section orientation, ~5 high-quality sources, ~1-page
     output. Use for "primer," "what is X," "introduce me to X."
   - `survey` (default) — multi-section structured report, ~15–20 sources,
     full template. Use for "research X for me," "report on X."
   - `deep-dive` — exhaustive review with citation chasing (forward and
     backward from anchor sources), ~30+ sources, extended template. Use for
     "thorough review," "what does the literature say," "exhaustive."
3. **Plan the search.** Load [`search-strategy.md`](./search-strategy.md). Name
   the source types (peer-reviewed, industry reports, standards bodies, primary
   sources, expert practitioners), the search terms, and explicit exclusions.
   In Guided Draft mode, surface the plan before executing.
4. **Execute the search.** Run web searches per the plan; for `deep-dive`,
   snowball — follow citations forward and backward from anchor sources until
   new sources stop adding new claims. Apply
   [`source-triage.md`](./source-triage.md): prefer primary over secondary,
   recent over dated unless seminal, independent over vendor-aligned,
   peer-reviewed or institutional over editorial.
5. **Synthesize against the template.** Fill
   [`../../templates/report/research-report.md`](../../templates/report/research-report.md):
   topic statement, search strategy, background, current state, key debates,
   implications, sources, limitations.
6. **Apply confidence.** Tag every load-bearing claim with H/M/L per
   [`confidence-rubric.md`](./confidence-rubric.md). Cite at the point of
   claim. Mark synthesis ("inferred from X+Y") explicitly — never present
   synthesis as if it were sourced.
7. **Emit the report.** Write to
   `docs/research/research-report-<YYYY-MM-DD>-<topic-slug>.md`. Fall back to
   `research-output/research-report-<YYYY-MM-DD>-<topic-slug>.md` if
   `docs/research/` is unwritable. Report the path.

## Output requirements

Every report names: the one-sentence research question with explicit
inclusions and exclusions; the depth mode applied (`brief` / `survey` /
`deep-dive`); the search strategy (source types, terms, exclusions);
confidence (H/M/L) and a citation at the point of every load-bearing claim;
explicit limitations (what was not covered, what is contested, what is
uncertain); and the grounding sources from `skill.json.inspired_by` for the
methodology used.

## Subagent dispatch

Optional. For `deep-dive` topics with several distinct sub-questions, spawn one
sub-agent per sub-question, each producing one section of the final report
against its slice of the search plan. The main agent integrates sections and
applies confidence end-to-end. Skip sub-agents for `brief` and most `survey`
runs — coordination overhead exceeds parallelism benefit at small scale.

## Reference map

- [`search-strategy.md`](./search-strategy.md) — plan the search: source types,
  terms, exclusions, snowballing.
- [`source-triage.md`](./source-triage.md) — filter and rank sources by
  primacy, recency, independence, peer review.
- [`confidence-rubric.md`](./confidence-rubric.md) — H/M/L scale and what each
  threshold requires.
- [`modes.md`](./modes.md) — Guided Draft / Autopilot / Grill Me contract.
- [`../../templates/report/research-report.md`](../../templates/report/research-report.md) — output template.

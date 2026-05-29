# Subagent dispatch

Load when SKILL.md routes to subagent dispatch — default for
`investigate` and for `scope` with surface = `all`; preferred for
`synthesize`; optional for `decide` (skeptic lens only is often
sufficient).

The skill exists because **opportunity research without fan-out
collapses to one anchored point of view**. Each lens (or each area)
needs an independent agent so the synthesizing pass sees parallel
evidence, not sequentially-anchored evidence.

## Two dispatch axes

### A. Per-surface fan-out (areas)

Used when `surface = all` (scope or investigate). Spawn one sub-agent
per row of `references/intents/investigate.csv` (excluding the `all`
row itself). Each sub-agent loads only its own playbook + artifact
template + the user's opportunity context; the orchestrator does NOT
pre-load all 14 playbooks.

### B. Per-persona fan-out (lenses)

Used for a single-surface investigation when the user wants a
multi-lens read. Spawn one sub-agent per persona — founder, operator,
investor, skeptic (see `references/core/personas.md`). All four read
the *same* playbook + artifact template but write *different*
perspectives. The synthesizing pass preserves disagreement.

Both axes can compose: for `investigate` with `surface = all` and
`persona = all`, fan out **per-surface** first, and inside each
surface sub-agent fan out **per-persona sequentially** (do not nest
parallel dispatch — most hosts don't support nested parallel
sub-agents reliably).

## Preamble before dispatch

Before spawning sub-agents, emit a short user-facing preamble — 3–4
lines, no more. Sub-agent fan-outs go silent for a minute or more; the
preamble converts that wait from a black box into an anticipated
reveal.

The preamble must name:

- **Axis** ("per-surface fan-out across N areas" / "4-lens fan-out on
  surface X" / "compound: N surfaces × 4 lenses sequentially").
- **What is being investigated** (the opportunity statement in one
  line).
- **Rough time estimate** ("~2–4 minutes for 6 surfaces").
- **What to watch for** ("expect concentration risk to show up in
  multiple areas — synthesizer will deduplicate.")

Example:

```text
Dispatching 6 area sub-agents (market, customer, competitive, domain,
technical, financial) on "AI scheduling for in-home health-care
visits." ~3–4 min. Each area writes its own artifact; synthesizer
will deduplicate cross-area risks.
```

Skip the preamble for hosts that don't show streaming text. Do not
substitute a long status spinner — the value is the user knowing
*what is being looked for*, not just that work is happening.

## Dispatch templates

In hosts that don't auto-dispatch sub-agents, use explicit verbs:
"spawn N agents," "delegate this in parallel," or "use a sub-agent
for the [persona / surface]." Don't expect the main agent to infer
delegation from the word "dispatch" alone.

### Per-surface sub-agent prompt

> Investigate the **[surface]** dimension of the following
> opportunity for a [target persona] audience.
>
> **Opportunity:** [one-line opportunity statement]
> **Context:** [paste the intake brief / prior artifacts as needed]
>
> Apply the heuristics in `references/playbooks/[surface].md` tagged
> for `investigate`. Use the confidence rubric in
> `references/core/confidence-rubric.md` on every load-bearing claim
> (H / M / L). Use the severity rubric in
> `references/core/severity-rubric.md` for any risks.
>
> Fill `templates/artifacts/[surface-artifact].md` end-to-end. End
> the artifact with the F/A/D/R fold per
> `references/core/fadr-framework.md`. Name the next falsifiable
> test (a <1-week experiment) that closes the highest-leverage
> assumption.
>
> Output the filled artifact. Do not synthesize across areas — your
> peers are running in parallel; the orchestrator consolidates later.

### Per-persona sub-agent prompt

> Investigate **[surface]** for the following opportunity through the
> **[persona]** lens.
>
> **Opportunity:** [one-line opportunity statement]
> **Lens bias:** [paste the persona block from `core/personas.md`]
>
> Apply only the heuristics in `references/playbooks/[surface].md`
> that this lens cares about. Surface what this lens uniquely
> catches — do not try to balance the bull/bear; that's the
> synthesizer's job.
>
> Output a finding list. Each finding: confidence (H/M/L), severity
> (0–4) if it's a risk, named heuristic from the playbook, the
> evidence, and what changes downstream.
>
> Do not output the full artifact template — that's the
> orchestrator's job after all lenses return.

## Synthesis (orchestrator)

After all sub-agents return:

1. **Deduplicate** findings by heuristic + claim. If two lenses or
   two adjacent surfaces report the same risk, collapse into one
   finding and note which sources flagged it.
2. **Preserve disagreements** as open questions, not silent winners.
   If the founder lens scores a risk as 1 and the skeptic scores it
   as 4, that delta is the signal — surface both, name the open
   question.
3. **Re-confidence.** If two L-confidence claims point at the same
   conclusion, the conclusion stays L (Ls don't average to M). If
   one H and one L disagree, the H usually wins, but flag explicitly.
4. **Rank by severity** for risks, by leverage for assumptions, by
   evidence quality for facts.
5. **Emit template-shaped output** for the intent
   (investigation-brief, cross-area-brief, fadr-memo). The sub-agents
   produce findings + filled artifacts; the synthesis produces the
   consolidated brief.

## When to skip dispatch

- **Tiny scoping questions** — "should we even research this?" is
  often a 1-question scope check, not a fan-out.
- **Single-area, single-lens explicit request** — "just give me the
  market size in dollars" is one sub-agent, not four.
- **Deterministic lookups** — pricing for a known competitor, a
  specific regulation citation. Sub-agents don't add value over a
  single source check.
- **Tasks needing secrets or live production access** — sub-agents
  shouldn't be passed credentials or pointed at production systems
  unless they have explicit handling for it.

## Fallback

If sub-agents are unavailable in the current environment, run the
same lenses sequentially. Switch persona explicitly between passes —
write "switching to skeptic lens" before the next pass — the
discipline of changing lens matters more than the parallelism.
Sequential is slower and slightly more anchored, but still beats one
undifferentiated review.

## Multi-area fan-out caps

When `surface = all`, default to the **first-pass subset** (6
areas: market, customer, competitive, domain, technical, financial)
unless the user has explicitly asked for all 14 or the stage
warrants it (mid-build, pre-launch, mid-pivot). 14 sub-agents
produces 14 disconnected dumps if not scoped; the convo's named
failure mode.

Stage-aware defaults:

| Stage | Default area subset |
|---|---|
| Pre-idea | customer, domain, trend |
| Idea | customer, market, competitive, domain |
| Validation | + technical, financial |
| Build | + operational, data, risk |
| Launch | + channel, gtm, legal, stakeholder |
| Scale | all 14 |

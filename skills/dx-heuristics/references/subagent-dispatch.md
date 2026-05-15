# Subagent dispatch

Load this file when SKILL.md routes to subagent dispatch — typically for
`audit` or `edge-pass`, sometimes for `design` or `debug`.

## Why three lenses

A single review pass anchors on whatever the reviewer noticed first.
Independent perspectives that start from different concerns catch issues
the single pass missed:

- A first-timer reading public docs is the only one who notices missing
  context, broken paste-examples, and undocumented assumptions.
- A maintainer is the only one who registers migration cost, support
  burden, and compatibility traps.
- An adversarial debugger is the only one who tests whether the error
  message + log + doc actually leads anywhere.

Running them in parallel — not sequentially in one head — keeps each lens
honest. Lens 2 isn't influenced by lens 1's findings.

## The three lenses

1. **First-time integrator** — has only public docs/examples; no
   maintainer access or tribal knowledge. Reports unclear steps, missing
   context, broken examples, undocumented assumptions.
2. **Maintainer** — owns the surface long-term. Checks compatibility,
   package boundaries, migration cost, deprecation lifecycle, and
   long-term support burden.
3. **Adversarial debugger** — starts from likely failure modes. Tests
   whether errors, logs, and docs lead to recovery in under five minutes.

## Dispatch template

For each lens, dispatch a sub-agent with this shape:

> Review the following [surface] from the [persona] perspective.
>
> Artifact: [paste / link / file path].
>
> Apply the heuristics in `references/playbooks/[surface].md` tagged for
> [intent]. Use the severity scale in
> `references/core/severity-rubric.md`.
>
> Output a finding list. Each finding: severity (0–4), location, named
> heuristic, what fails, fix, verification. Do not synthesize across
> lenses — your peers are running in parallel.

Pass the same artifact, same playbook, same intent to all three. Vary
only the persona and the persona-specific lens (what to look for).

## Synthesis

After all three sub-agents return, the synthesizing pass (the orchestrator,
not the sub-agents) does the work the lenses deliberately didn't:

1. **Deduplicate** findings by heuristic + location. If two lenses
   reported the same issue, collapse into one finding and note which
   lenses flagged it.
2. **Preserve disagreements** as open questions, not silent winners. If
   the maintainer thinks something is fine and the first-timer thinks
   it's broken, that's signal — surface it.
3. **Rank by severity** using `references/core/severity-rubric.md`.
4. **Emit template-shaped output** for the intent (audit-report,
   edge-checklist, etc.). The sub-agents produce finding lists; the
   synthesis produces the final report.

## When to skip

- **Tiny copy edits** — one-line rename, typo fix. Direct response is
  faster than dispatch overhead.
- **Deterministic command checks** — "does this CLI flag exist?" — a
  single source check beats three opinions.
- **Tasks requiring secrets or live production access** — sub-agents
  shouldn't be passed credentials or pointed at production systems
  unless they have explicit handling for it.

## Fallback

If sub-agents are unavailable in the current environment, run the same
three lenses sequentially. Switch persona explicitly between passes —
write down "switching to maintainer lens" before the second pass — the
discipline of changing lens matters more than the parallelism. Sequential
is slower and slightly more anchored, but still beats a single
undifferentiated review.

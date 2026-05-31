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

## Preamble before dispatch

Before spawning sub-agents, emit a short user-facing preamble — 3–4 lines, no
more. Sub-agent fan-outs go silent for a minute or more; the preamble converts
that wait from a black box into an anticipated reveal.

The preamble must name:

- **Lenses dispatched** (e.g., "first-time integrator, maintainer,
  adversarial debugger").
- **Surface(s)** being audited.
- **Rough time estimate** ("~1–2 minutes," not a hard number).
- **What to watch for in the output** — one sentence telegraphing the kind
  of finding the user should expect.

Example:

```text
Dispatching 3 lenses (first-time integrator, maintainer, adversarial
debugger) against the `cli` surface. ~1–2 min.
Watch for: inconsistent flag conventions, error messages that don't lead
anywhere, and --help that assumes context.
```

Skip the preamble for hosts that don't show streaming text. Don't substitute
a long status spinner for the preamble — the value is the user knowing *what
is being looked for*, not just that work is happening.

## Dispatch template

Spawn three sub-agents (one per lens) and run them in parallel. In hosts
that do not auto-dispatch sub-agents (e.g., Codex), use explicit verbs:
"spawn three agents," "delegate this in parallel," or "use a sub-agent
for the first-time integrator lens." Do not expect the main agent to
infer delegation from the word "dispatch" alone.

For each spawned sub-agent, use this prompt shape:

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

## Multi-surface fan-out (audit intent only)

When the user picks `all` as the surface for an `audit`, iterate the
rows of `references/intents/audit.csv` and fan out one sub-agent **per
surface row** — do not hardcode the surface list here; the CSV is the
source of truth and surfaces may be added or renamed. The orchestrator
does **not** load the playbooks itself — each spawned surface agent
loads only its own playbook.

### Each surface sub-agent

- Loads `references/playbooks/<surface>.md` and the core refs from its
  CSV row.
- Runs the three lenses **sequentially inside itself** — do not spawn
  further sub-agents (nested delegation is unreliable across hosts like
  Codex). Switch persona explicitly between passes.
- Identifies the target developer persona for that surface.
- Returns a per-surface finding list plus a 0–10 score from
  `references/core/score-rubric.md` and a one-line "biggest gap" summary.

### Orchestrator synthesis

After all surface sub-agents return:

1. **Rank findings cross-surface** by severity, highest first.
2. **Surface the worst-offending surfaces** in a per-surface score table.
3. **Project-wide path to 10/10** — top 3 fixes that lift overall DX
   most, not per-surface polish.
4. **Emit `templates/audit-report-multi.md`** rather than the
   single-surface template. Append each surface's full report at the
   end for reference.

### When to skip multi-surface mode

- Narrow questions ("review my CLI help text") — one playbook is enough.
- Scoped audits where the user named ≤ 3 surfaces explicitly — dispatch
  those surfaces only, not the full CSV set.
- Tasks requiring secrets or live production access for some surfaces —
  exclude those surfaces from the fan-out.

# Subagent dispatch

Load this file when SKILL.md routes to subagent dispatch — typically for
`audit`, `diagnose`, or `optimize`, sometimes for `design`.

## Why three lenses

A single review pass anchors on whatever the reviewer noticed first.
Three perspectives that start from different concerns catch issues a
single pass misses:

- An on-call / SRE is the only one who notices what a paging dashboard
  cannot answer at 3am, what alerts will fire on noise, and where the
  recovery runbook is missing.
- A profiler / workload lens is the only one who asks where time, CPU,
  memory, and IO actually go under representative load — and whether
  measurements would survive coordinated omission.
- A capacity-planner is the only one who asks what breaks at 10× /
  100× current load, what the scalability curve looks like, and what
  the resource ceiling is.

Running them in parallel — not sequentially in one head — keeps each
lens honest. Lens 2 is not influenced by lens 1's findings.

## The three lenses

1. **On-call / SRE** — wakes at 3am, has only the dashboards, alerts,
   logs, traces, and runbooks. Reports: what symptoms cannot be
   diagnosed from current instrumentation; what alerts fire on noise or
   miss real failures; what the recovery path looks like end-to-end.
2. **Profiler / workload** — has profiling tools and representative load.
   Reports: where time, CPU, memory, and IO actually go; whether
   measurements suffer coordinated omission; whether percentiles are
   computed correctly (no averaging of pre-aggregated quantiles); whether
   the tail behavior matches the median story.
3. **Capacity-planner** — projects forward to 10× / 100× current load.
   Reports: where the scalability curve bends; what the bottleneck
   resource is; what headroom the system has; how the system behaves
   under load shedding, retries, and hedging.

## Preamble before dispatch

Before spawning sub-agents, emit a short user-facing preamble — 3–4
lines, no more. Sub-agent fan-outs go silent for a minute or more; the
preamble converts that wait from a black box into an anticipated reveal.

The preamble must name:

- **Lenses dispatched** (e.g., "on-call / SRE, profiler / workload,
  capacity-planner").
- **Surface(s)** being audited.
- **Rough time estimate** ("~1–2 minutes," not a hard number).
- **What to watch for** — one sentence telegraphing the kind of finding
  the user should expect.

Example:

```text
Dispatching 3 lenses (on-call / SRE, profiler / workload,
capacity-planner) against the `latency` surface. ~1–2 min.
Watch for: missing tail-percentile metrics, coordinated-omission risk in
your benchmarks, and head-of-line blocking in the shared queue.
```

Skip the preamble for hosts that do not show streaming text. Do not
substitute a long status spinner — the value is the user knowing *what
is being looked for*.

## Dispatch template

Spawn three sub-agents (one per lens) and run them in parallel. In hosts
that do not auto-dispatch sub-agents, use explicit verbs: "spawn three
agents," "delegate this in parallel," or "use a sub-agent for the
on-call / SRE lens."

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
> heuristic, what fails, fix, verification (measurement method). Do not
> synthesize across lenses — your peers are running in parallel.

Pass the same artifact, same playbook, same intent to all three. Vary
only the persona and the persona-specific lens. Also pass the project tier
(`references/calibration.md`); below Load-bearing, a lens reports one systemic
finding per mechanism, not one per artifact.

## Synthesis

After all three sub-agents return, the synthesizing pass does the work
the lenses deliberately did not:

1. **Deduplicate** findings by heuristic + location. If two lenses
   reported the same issue, collapse into one finding and note which
   lenses flagged it. Below Load-bearing (`references/calibration.md`), also
   collapse same-mechanism per-artifact findings into one systemic finding at
   the max severity it subsumes — never a severity-4 — and defer the remainder
   to the report's "Later — as it grows".
2. **Preserve disagreements** as open questions, not silent winners. If
   the on-call lens flags a blind spot the profiler does not see, that is
   signal — surface it.
3. **Rank by severity** using `references/core/severity-rubric.md`.
4. **Emit template-shaped output** for the intent (audit-report,
   diagnose-runbook, optimize-plan). Sub-agents produce finding lists;
   synthesis produces the final artifact.

## When to skip

- **Tiny copy edits** — one-line rename, typo fix. Direct response is
  faster than dispatch overhead.
- **Deterministic command checks** — "does this metric exist in our
  Prometheus config?" — a single source check beats three opinions.
- **Tasks requiring secrets or live production access** — sub-agents
  should not be passed credentials or pointed at production systems
  unless they have explicit handling for it.

## Fallback

If sub-agents are unavailable in the current environment, run the same
three lenses sequentially. Switch persona explicitly between passes —
write down "switching to profiler / workload lens" before the second
pass. Discipline matters more than parallelism. Sequential is slower and
slightly more anchored, but still beats a single undifferentiated review.

## Multi-surface fan-out (audit intent only)

When the user picks `all` as the surface for an `audit`, iterate the rows
of `references/intents/audit.csv` and fan out one sub-agent **per surface
row** — do not hardcode the surface list here; the CSV is the source of
truth. The orchestrator does **not** load the playbooks itself — each
spawned surface agent loads only its own playbook.

### Each surface sub-agent

- Loads `references/playbooks/<surface>.md` and the core refs from its
  CSV row.
- Runs the three lenses **sequentially inside itself** — do not spawn
  further sub-agents (nested delegation is unreliable across hosts).
  Switch persona explicitly between passes.
- Identifies the target persona for that surface.
- Returns a per-surface finding list plus a 0–10 score from
  `references/core/score-rubric.md` and a one-line "biggest gap" summary.

### Orchestrator synthesis

After all surface sub-agents return:

1. **Rank findings cross-surface** by severity, highest first.
2. **Surface the worst-offending surfaces** in a per-surface score table.
3. **Project-wide path to 10/10** — top 3 fixes that lift overall
   posture most, not per-surface polish.
4. **Emit `templates/audit-report-multi.md`** rather than the
   single-surface template. Append each surface's full report at the end
   for reference.

### When to skip multi-surface mode

- Narrow questions ("review our log schema") — one playbook is enough.
- Scoped audits where the user named ≤ 3 surfaces explicitly — dispatch
  those surfaces only, not the full CSV set.
- Tasks requiring secrets or live production access for some surfaces —
  exclude those surfaces from the fan-out.

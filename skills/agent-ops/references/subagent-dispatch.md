# Subagent dispatch — three lenses for operating an agent system

Use sub-agents whenever delegation is permitted. Each lens, held strictly in its frame,
returns an independent finding list; the host synthesizes, deduplicates, preserves
disagreements as open questions, and emits the template-shaped output.

## When to dispatch

| Intent | Lens plan | When to skip |
|--------|-----------|--------------|
| review | **Try dispatch when permitted** | A single-loop change with no autonomy or release implications |
| design | **Optional lenses** | A small design where one lens dominates |
| do | **No** | The change is small enough to apply the playbook directly |

## The three lenses

### Lens 1 — signal-and-trace

**Prompt:** "Audit the **observability** of this agent system: does a real captured span carry
prompt + completion + tool I/O (not just `cmd.name`/`duration`)? Are spans reassembled into a
graded trajectory, or is only per-span content checked? Do traces actually become evals, fixes,
or rollback rules, or are they dashboard/telemetry theater? Can a degraded-but-200 dependency be
caught from the metrics stream? Cite playbook heuristics. Findings only — no fixes, no overall
score. Severity 0–4 from `severity-rubric.md`."

### Lens 2 — loop-and-control

**Prompt:** "Evaluate whether **signal becomes governed change**: is loop readiness scored on
observed emission (a *Last observed* anchor) or on field presence? Does the trace-to-eval step
produce a non-trivial candidate? Is autonomy gated — held-out evals, diff review, circuit-
breakers, one-diff-per-cycle, revert-on-failed-gate — or is it ungated self-improvement? Cite
heuristics. Findings with severity; name what a runaway controller would do."

### Lens 3 — reliability-and-governance

**Prompt:** "Evaluate **reliability, cost, and governance**: is the release gate decomposed by
failure mode (guardrail vs north-star) or a single god-gate pass-rate? Is a per-step bar
mistaken for a production rate (march of nines)? Are cost/iteration budgets and rollback
thresholds set? Is the system placed on the maturity ladder with its gate-before-persistence, and
is agent-authored change provenance recorded? Cite heuristics. Findings with severity; name the
unowned risk."

## Preamble before dispatch

Before spawning, emit a 3–4 line user-facing preamble naming the **lenses dispatched**, the
**surface(s)**, a **rough time estimate** ("~1–2 minutes"), and **what to watch for** in the
output. Skip for tiny single-lens passes or hosts without streaming text.

## Dispatch template

When the host has a delegation primitive and policy permits, fan out:

```
Spawn three subagents in parallel.

Agent 1 (signal-and-trace): <Lens 1 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 2 (loop-and-control): <Lens 2 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 3 (reliability-and-governance): <Lens 3 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first. Runs in
parallel; the host sequences findings during synthesis.

Each agent returns a list of findings with severity, citing heuristics. No prose summary at
the top.
```

Pass each agent the project tier (`references/calibration.md`); below Load-bearing, a lens
reports one systemic finding per mechanism, not one per artifact. If the host has no
delegation primitive, run the lenses sequentially — the discipline of switching lens matters
more than the parallelism.

## Synthesis step

1. **Deduplicate.** When lenses report the same finding, keep the higher-severity copy and
   note which lenses also flagged it. Below Load-bearing (`references/calibration.md`),
   collapse same-mechanism findings of severity ≤ 3 into one systemic finding at the highest
   severity it subsumes, and route deferred best-practice to "Later — as it grows". Keep every
   severity-4 explicit.
2. **Preserve disagreements** as `Open questions`; name the trade-off rather than resolving it
   silently.
3. **Order by severity** (4 → 0).
4. **Map to template** — `audit-report.md` for REVIEW; `design-doc.md` / `refactor-runbook.md`
   / `explanation.md` for DESIGN — populated from the synthesized list.

## Fan-out variant (surface = `all`, REVIEW only)

Spawn one agent per surface listed in `references/intents/review.csv` (excluding the `all`
row). Each surface-agent runs the three lenses sequentially and returns a per-surface finding
list; the host synthesizes across surfaces. Do not hardcode the surface set here —
`review.csv` is the source of truth, so a new surface is a CSV row plus a playbook with no
edit to this file.

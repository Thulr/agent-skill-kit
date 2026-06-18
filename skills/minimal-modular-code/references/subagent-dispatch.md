# Subagent dispatch — three lenses for minimal, modular code

Use sub-agents whenever delegation is permitted. Each lens, held strictly in its frame,
returns an independent finding list; the host synthesizes, deduplicates, preserves
disagreements as open questions, and emits the template-shaped output.

## When to dispatch

| Intent | Lens plan | When to skip |
|--------|-----------|--------------|
| review | **Try dispatch when permitted** | Single-file change with no structural implications |
| design | **Optional lenses** | A small design where one lens dominates |
| do | **No** | The change is small enough to apply the playbook directly |

## The three lenses

### Lens 1 — slop-hunter

**Prompt:** "Audit this code strictly for **slop**: duplication and clones (same *decision*
expressed twice), dead code, speculative generality (config/params/branches for cases not
handled today), the wrong abstraction (a shared unit patched with parameters and
conditionals), and needless verbosity. Cite playbook heuristics by number. Findings only —
no refactors, no overall score. Severity 0–4 from `severity-rubric.md`."

### Lens 2 — coupling-and-boundary

**Prompt:** "Evaluate this code for **boundary quality and coupling**: dependency direction
(does stable code depend on volatile code?), deep vs shallow modules (interface much smaller
than implementation?), leaky adapters (framework/vendor types crossing a seam), and braided
concerns. Cite heuristics. Propose better-shaped boundaries briefly. Do not rank refactor
sequence — that is the next lens."

### Lens 3 — parallel-readiness

**Prompt:** "Evaluate this code for **parallel-readiness**: are there stable, owned contracts
(design rules) the modules sit beneath? Could the modules be handed to different agents
without collision (same dependency layer, no shared mutable state)? Is the blast radius of a
typical change knowable? Are load-bearing invariants enforced by gates or only stated in
prose? Cite heuristics. Findings with severity; name what would have to be serialized."

## Preamble before dispatch

Before spawning, emit a 3–4 line user-facing preamble naming the **lenses dispatched**, the
**surface(s)**, a **rough time estimate** ("~1–2 minutes"), and **what to watch for** in the
output. Skip for tiny single-lens passes or hosts without streaming text.

## Dispatch template

When the host has a delegation primitive and policy permits, fan out:

```
Spawn three subagents in parallel.

Agent 1 (slop-hunter): <Lens 1 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 2 (coupling-and-boundary): <Lens 2 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 3 (parallel-readiness): <Lens 3 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first. Runs in
parallel; the host sequences findings during synthesis.

Each agent returns a list of findings with severity, citing heuristic numbers. No prose
summary at the top.
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

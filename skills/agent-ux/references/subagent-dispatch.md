# Subagent dispatch — three lenses for an agent-facing interaction surface

Use sub-agents whenever delegation is permitted. Each lens, held strictly in its frame,
returns an independent finding list; the host synthesizes, deduplicates, preserves
disagreements as open questions, and emits the template-shaped output.

## When to dispatch

| Intent | Lens plan | When to skip |
|--------|-----------|--------------|
| review | **Try dispatch when permitted** | A single control with no authority or conflict implications |
| design | **Optional lenses** | A small design where one lens dominates |
| do | **No** | The change is small enough to apply the playbook directly |

## The three lenses

### Lens 1 — perceive

**Prompt:** "Audit whether an agent can **perceive** the surface: are state, available actions, and
results exposed as structure (accessibility tree, ARIA role/name/state, semantic HTML, text), or
do load-bearing controls and rules live only in human-only affordances (tooltip, hover, icon,
color, UI order, animation)? Are action results observable in state, not only a transient toast?
Cite playbook heuristics. Findings only — no fixes, no overall score. Severity 0–4 from
`severity-rubric.md`."

### Lens 2 — act-and-authority

**Prompt:** "Evaluate whether an agent can **act safely and within authority**: are controls
targetable by stable semantic handles (role + name, test id, documented action) rather than
coordinates/brittle XPath? Are actions an agent may retry idempotent or guarded so a stochastic
repeat does not double-execute? Do irreversible/authority-crossing actions (payment, deletion,
permission grant, external send) confirm in-path? When the agent acts on a user's behalf, is that
visible with scoped, revocable consent? Cite heuristics. Findings with severity; name the unguarded
or unperceivable action."

### Lens 3 — reconcile

**Prompt:** "Evaluate the **human-vs-agent reconciliation** on the same surface: where a choice
serves a human visual user but harms an agent actor (or vice versa), is the trade-off named (who
benefits, who is harmed, what evidence)? Is there a dual path — human affordance plus a
machine-readable one — for load-bearing facts/actions? One source many renderings, or forked
human/agent surfaces that drift? Any hidden criticals (consequences, required inputs, auth scopes)
living only in hover/color/screenshot? Cite heuristics. Findings with severity; name the harmed
audience."

## Preamble before dispatch

Before spawning, emit a 3–4 line user-facing preamble naming the **lenses dispatched**, the
**surface(s)**, a **rough time estimate** ("~1–2 minutes"), and **what to watch for** in the
output. Skip for tiny single-lens passes or hosts without streaming text.

## Dispatch template

When the host has a delegation primitive and policy permits, fan out:

```
Spawn three subagents in parallel.

Agent 1 (perceive): <Lens 1 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 2 (act-and-authority): <Lens 2 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 3 (reconcile): <Lens 3 prompt>, applied to <surface>. Read
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

# Subagent dispatch — three lenses for designing agent measurement

Use sub-agents whenever delegation is permitted. Each lens, held strictly in its frame,
returns an independent finding list; the host synthesizes, deduplicates, preserves
disagreements as open questions, and emits the template-shaped output.

## When to dispatch

| Intent | Lens plan | When to skip |
|--------|-----------|--------------|
| review | **Try dispatch when permitted** | A single eval with no judge or release implications |
| design | **Optional lenses** | A small design where one lens dominates |
| do | **No** | The change is small enough to apply the playbook directly |

## The three lenses

### Lens 1 — decomposition-and-coverage

**Prompt:** "Audit whether the measurement is **decomposed and tier-appropriate**: is there a
named failure-mode ontology, or is the suite chasing one aggregate it cannot decompose? Are
failures localized to a trajectory/trace, not just a final pass/fail? Does each eval clear the
gate for its staircase tier, and is it the smallest eval that gates the change? Cite playbook
heuristics. Findings only — no fixes, no overall score. Severity 0–4 from `severity-rubric.md`."

### Lens 2 — judge-and-trust

**Prompt:** "Evaluate whether the instruments can be **trusted**: is an LLM-as-judge calibrated
against a human-labeled set (precision/recall + position/length/self-preference bias) before it
gates anything, and does it emit failure explanations? Would a deterministic check be more
trustworthy? Are benchmark fixtures held-out — disjoint from training/optimization with a
non-zero margin — or do they score memorization? Cite heuristics. Findings with severity; name
what a regression could slip through."

### Lens 3 — trajectory-and-gaming

**Prompt:** "Evaluate **path coverage and gaming resistance**: are runs graded as reassembled
trajectories (tool order, hand-offs, loops) or only per-span (Trajectory Blindness)? Is a
per-step bar mistaken for a run bar (march of nines)? Is the release gate per-slice
guardrail-vs-north-star or a single god metric? Can the behavior game the proxy (Goodhart)? Do
activation evals cover negative and disambiguation cases, and are evals re-run on prompt/model
change? Cite heuristics. Findings with severity; name the blind spot."

## Preamble before dispatch

Before spawning, emit a 3–4 line user-facing preamble naming the **lenses dispatched**, the
**surface(s)**, a **rough time estimate** ("~1–2 minutes"), and **what to watch for** in the
output. Skip for tiny single-lens passes or hosts without streaming text.

## Dispatch template

When the host has a delegation primitive and policy permits, fan out:

```
Spawn three subagents in parallel.

Agent 1 (decomposition-and-coverage): <Lens 1 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 2 (judge-and-trust): <Lens 2 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 3 (trajectory-and-gaming): <Lens 3 prompt>, applied to <surface>. Read
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

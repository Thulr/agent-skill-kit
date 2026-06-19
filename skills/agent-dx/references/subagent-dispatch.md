# Subagent dispatch — three lenses for agent-facing surfaces

Use sub-agents whenever delegation is permitted. Each lens, held strictly in its frame,
returns an independent finding list; the host synthesizes, deduplicates, preserves
disagreements as open questions, and emits the template-shaped output.

## When to dispatch

| Intent | Lens plan | When to skip |
|--------|-----------|--------------|
| review | **Try dispatch when permitted** | Single-surface change with no contract or trust implications |
| design | **Optional lenses** | A small design where one lens dominates |
| do | **No** | The change is small enough to apply the playbook directly |

## The three lenses

### Lens 1 — contract-and-schema

**Prompt:** "Audit this agent-facing surface strictly as a **machine contract**: are tool
schemas derived from the function signature (not hand-written)? Is structured output validated
against a native schema with a typed refusal? Is the error envelope a typed, stable
discrete-field structure with a `code` that survives minor versions? Could a consuming agent
parse and branch on every surface deterministically? Cite playbook heuristics. Findings only —
no refactors, no overall score. Severity 0–4 from `severity-rubric.md`."

### Lens 2 — agent-recovery

**Prompt:** "Evaluate whether a **stochastic LLM consumer can recover** on this surface: does
the agent loop have a declarative stop condition, a turn cap, and a deterministic verification
step? Are tool errors returned in the shape the model produced, naming the offending input? Is
a semantic retry distinct from a transport retry? Would a failure strand the agent in a loop or
let a hallucinated success ship? Cite heuristics. Findings with severity; name what a real
agent would do wrong."

### Lens 3 — trust-and-isolation

**Prompt:** "Evaluate the **trust boundary**: is untrusted tool metadata scanned and pinned
before registration (tool-description injection)? Are guardrails present at all four
checkpoints? Does the approval surface show real side effects? Are credentials isolated
(process / network / token exchange), and is auth delegated rather than borrowed? Is raw
content kept out of spans by default and redacted at the boundary? Cite heuristics. Findings
with severity; name the trifecta leg each gap opens."

## Preamble before dispatch

Before spawning, emit a 3–4 line user-facing preamble naming the **lenses dispatched**, the
**surface(s)**, a **rough time estimate** ("~1–2 minutes"), and **what to watch for** in the
output. Skip for tiny single-lens passes or hosts without streaming text.

## Dispatch template

When the host has a delegation primitive and policy permits, fan out:

```
Spawn three subagents in parallel.

Agent 1 (contract-and-schema): <Lens 1 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 2 (agent-recovery): <Lens 2 prompt>, applied to <surface>. Read
references/playbooks/<surface>.md and references/core/severity-rubric.md first.

Agent 3 (trust-and-isolation): <Lens 3 prompt>, applied to <surface>. Read
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

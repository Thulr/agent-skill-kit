# Subagent dispatch — three lenses for clean-architecture work

Try to use sub-agents whenever delegation is permitted. Sub-agents held
strictly in their lens produce independent finding lists. The host agent
synthesizes them, deduplicates, preserves disagreements as open questions,
and emits the template-shaped output.

## When to dispatch

| Intent | Lens plan | When to skip |
|--------|----------------------|--------------|
| audit | **Try dispatch when permitted** | Single-file change with no architectural implications |
| design | **Prefer dispatch when permitted** | A small design tweak where one lens dominates |
| refactor | **Optional lenses** | Trivial mechanical refactor with no boundary changes |
| explain | **No** | Lens disagreement is not useful when the goal is grounded explanation |

## The three lenses

### Lens 1 — Dependency-auditor

**Prompt:** "You are auditing this code/design strictly for **dependency
direction**. Find every place an inner concern depends on an outer one,
every cycle, every framework or infrastructure type that has leaked
into the domain or application layer. Cite the playbook's heuristics by
number. Do not propose refactors — only findings. Do not score the
overall surface — only individual findings with severity (0-4 from
`severity-rubric.md`)."

**Anchors on:** dependency-rule violations, layer leakage, framework
coupling, anti-corruption-layer absence between contexts.

### Lens 2 — Boundary-designer

**Prompt:** "You are evaluating this code/design for **boundary
quality**. Are seams in the right places? Are interfaces minimal and in
the core's vocabulary? Are deep modules (simple interface, rich
implementation) preferred over shallow ones? Are ports symmetric? Cite
the playbook's heuristics. Propose better-shaped boundaries with brief
justification. Do not rank refactor sequence — that is the next lens."

**Anchors on:** port symmetry, deep modules, interface minimality, layer
mechanics, leaky abstractions.

### Lens 3 — Refactor-pragmatist

**Prompt:** "You are evaluating this code/design for **refactor
viability** under realistic constraints (feature work continues,
big-bang forbidden, every step must be reversible). For the surface
in question, name the refactor patterns that apply (strangler-fig,
branch-by-abstraction, parallel-change, expand-contract,
characterization tests as safety nets). For each pattern: when does
it fit, what's the smallest reversible step, what breaks if the
refactor stops partway? Estimate per-pattern effort (S/M/L). Do not
enumerate specific code-level findings — that's the other lenses'
job. Do not synthesize a step sequence — that's the host's job."

**Anchors on:** which refactor patterns apply, safety-net discipline,
smallest-reversible-step posture.

## Preamble before dispatch

Before spawning sub-agents, emit a short user-facing preamble — 3–4 lines, no
more. Sub-agent fan-outs go silent for a minute or more; the preamble converts
that wait from a black box into an anticipated reveal.

The preamble must name:

- **Lenses dispatched** (e.g., "dependency-auditor, boundary-designer,
  refactor-pragmatist").
- **Surface(s)** being audited.
- **Rough time estimate** ("~1–2 minutes," not a hard number).
- **What to watch for in the output** — one sentence telegraphing the kind
  of finding the user should expect (e.g., "watch for dependency-rule
  violations in the domain layer and any framework imports inside
  use-cases").

Example:

```text
Dispatching 3 lenses (dependency-auditor, boundary-designer,
refactor-pragmatist) against the `domain` surface. ~1–2 min.
Watch for: framework types leaking into entities, anti-corruption-layer
absence between contexts, refactor patterns that fit.
```

Skip the preamble for tiny single-lens passes or hosts that don't show
streaming text. Don't substitute a long status spinner for the preamble —
the value is the user knowing *what is being looked for*, not just that
work is happening.

## Dispatch template

When the host has a delegation primitive and active policy permits dispatch,
fan out. Treat explicit user, project, session, or host instructions to use
sub-agents as permission when they satisfy the active platform policy:

```
Spawn three subagents in parallel.

Agent 1 (dependency-auditor): <Lens 1 prompt above>, applied to <surface>.
Read references/playbooks/<surface>.md and references/core/severity-rubric.md
and references/core/glossary.md before starting.

Agent 2 (boundary-designer): <Lens 2 prompt above>, applied to <surface>.
Read references/playbooks/<surface>.md, references/core/severity-rubric.md,
and references/core/glossary.md before starting.

Agent 3 (refactor-pragmatist): <Lens 3 prompt above>, applied to
<surface>. Read references/playbooks/<surface>.md and
references/core/severity-rubric.md before starting. Runs independently
in parallel with the other two; the host sequences findings during
synthesis.

Each agent returns: a list of findings/proposals with severity, citing
heuristic numbers from the playbook. No prose summary at the top.
```

Pass each agent the project tier (`references/calibration.md`); below
Load-bearing, a lens reports one systemic finding per mechanism, not one per
artifact.

If the host has no delegation primitive, run sequentially. If active policy
requires fresh explicit user permission that has not been granted, ask once;
run sequentially only if permission is absent, declined, unsafe, or still
blocked by the host. The discipline of switching lens matters more than the
parallelism.

## Synthesis step

After the three lenses return, the host agent:

1. **Deduplicate.** When two or more lenses report the same finding,
   keep the higher-severity copy and note which other lenses also
   flagged it. Below Load-bearing (`references/calibration.md`), also collapse
   same-mechanism per-artifact findings of severity ≤ 3 into one systemic
   finding at the highest severity it subsumes, and route deferred best-practice
   to "Later — as it grows". Keep every severity-4 explicit — never collapsed,
   never deferred.
2. **Preserve disagreements** as `Open questions` in the output. Do not
   resolve them silently — name the disagreement and the trade-off
   between the lenses' framings.
3. **Order by severity** (4 → 0).
4. **Sequence using Lens 3's pattern guidance.** For refactor and
   design intents, use Lens 3's per-pattern viability (which patterns
   fit, smallest reversible step, what breaks if stopped partway) to
   order Lens 1's and Lens 2's findings into actionable steps. Items
   with no refactor pattern that Lens 3 surfaced get flagged as Open
   questions.
5. **Map to template.** Emit the intent-appropriate template —
   `audit-report.md`, `design-doc.md`, `refactor-runbook.md`, or
   `explanation.md` (the mapping lives in
   `references/intent-router.csv`'s `default_template` column) —
   populated from the synthesized list.

## Fan-out variant (surface = `all`, audit only)

For `audit` with `all`-fanout, the structure inverts: try to spawn one agent
per surface listed in
`references/intents/audit.csv` (excluding the `all` row itself). Each
surface-agent runs all three lenses sequentially inside itself and returns a
per-surface finding list. Without permitted delegation, run the same surface
passes sequentially. The host synthesizes across surfaces and emits
`templates/audit-report-multi.md`. Do not hardcode the surface set in
this file — `audit.csv` is the source of truth so a new surface can be
added by editing the CSV + dropping in a playbook, with no edits to
this dispatch doc.

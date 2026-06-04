# Subagent dispatch

Load this file when SKILL.md routes to subagent dispatch — typically for `audit` or `prune`, often for `author`, sometimes for `triage`.

## Why three lenses

A single review pass anchors on whatever the reviewer noticed first. Independent perspectives that start from different concerns catch issues the single pass missed:

- An **intent reader** (cold; sees only the test, not the SUT) is the only one who notices that the test name doesn't describe the behavior, that the assertion doesn't match the name, or that the magic literals carry hidden meaning.
- A **refactor adversary** (proposing a legitimate SUT refactor) is the only one who notices coupling to internals, over-mocking, and assertions on call counts/order.
- A **bug-shape hunter** (imagining the bugs that ship in this code class) is the only one who notices missing boundary cases, missing error paths, and that the suite never injects failures.

Running them in parallel — not sequentially in one head — keeps each lens honest. Lens 2 isn't influenced by lens 1's findings.

## The three lenses

1. **Intent reader** — reads only the test, not the SUT, cold. Question: "in 10 seconds, what is this test asserting and why?" Reports unclear names, scrambled AAA, magic literals, hidden setup, asserts that don't match the test name.

2. **Refactor adversary** — proposes a *legitimate* SUT refactor (rename internal method, extract helper, restructure call graph). Question: "would this test break for the wrong reason?" Reports coupling to internals, over-mocking, assertions on call counts/order, mocks at the wrong seam.

3. **Bug-shape hunter** — pictures the bugs that ship in this code class (off-by-one, nulls, concurrency, timezone, partial failure, retries-as-duplicates). Pulls from `references/core/oracles.md` for variation. Question: "would this test catch any of those bugs?" Reports happy-path bias, missing boundary cases, missing error paths, no failure injection.

## Preamble before dispatch

Before spawning sub-agents, emit a short user-facing preamble — 3–4 lines, no more. Sub-agent fan-outs go silent for a minute or more; the preamble converts that wait from a black box into an anticipated reveal.

The preamble must name:

- **Lenses dispatched** (e.g., "intent reader, refactor adversary, bug-shape hunter").
- **Layer + scope** being reviewed.
- **Rough time estimate** ("~1–2 minutes," not a hard number).
- **What to watch for in the output** — one sentence telegraphing the kind of finding the user should expect.

Example:

```text
Dispatching 3 lenses (intent reader, refactor adversary, bug-shape hunter) against tests/unit/payments/. ~1–2 min.
Watch for: tests whose name doesn't match the assertion, assertions on call-count/order, and missing failure-injection paths.
```

Skip the preamble for hosts that don't show streaming text. Don't substitute a long status spinner — the value is the user knowing *what is being looked for*, not just that work is happening.

## Dispatch template

Spawn three sub-agents (one per lens) and run them in parallel. In hosts that do not auto-dispatch sub-agents, use explicit verbs: "spawn three agents," "delegate this in parallel," or "use a sub-agent for the intent reader lens." Do not expect the main agent to infer delegation from the word "dispatch" alone.

For each spawned sub-agent, use this prompt shape:

> Review the following [layer] test from the [persona] perspective.
>
> Artifact: [paste / link / file path].
>
> Apply the heuristics in `references/layers/[layer].md` tagged for [activity]. Use the severity scale in `references/core/severity-rubric.md`. Tag each finding with one or more failure modes from `references/core/failure-modes.md`.
>
> Output a finding list. Each finding: severity (0–4), location, named heuristic, failure mode(s), what fails, fix, verification. Do not synthesize across lenses — your peers are running in parallel.

Pass the same artifact, same playbook, same activity to all three. Vary only the persona and the persona-specific lens (what to look for).

## Synthesis

After all three sub-agents return, the synthesizing pass (the orchestrator, not the sub-agents) does the work the lenses deliberately didn't:

1. **Deduplicate** findings by heuristic + location. If two lenses reported the same issue, collapse into one finding and note which lenses flagged it.
2. **Preserve disagreements** as open questions, not silent winners. If the intent reader thinks something is fine and the refactor adversary thinks it's brittle, surface it.
3. **Rank by severity** using `references/core/severity-rubric.md`.
4. **Tag failure modes** using `references/core/failure-modes.md`.
5. **Score 0–10** using `references/core/score-rubric.md` for audit activity.
6. **Emit template-shaped output** for the activity (audit-report, prune-plan, etc.).

## When to skip

- **Tiny rename/typo edits** — direct response is faster than dispatch overhead
- **Deterministic single-step checks** — "does this assertion library have a `containsExactly`?" — one source check beats three opinions
- **Tasks requiring secrets or production credentials** — sub-agents shouldn't be passed those unless they have explicit handling

## Fallback

If sub-agents are unavailable in the current environment, run the same three lenses sequentially. Switch persona explicitly between passes — write down "switching to refactor adversary lens" before the second pass — the discipline of changing lens matters more than the parallelism. Sequential is slower and slightly more anchored, but still beats a single undifferentiated review.

## Cross-layer fan-out (`audit` intent only)

When the user picks `--surface=all` for a `audit`, iterate the rows of `references/intents/audit.csv` and fan out one sub-agent **per surface row** — do not hardcode the surface list here; the CSV is the source of truth and surfaces may be added or renamed. The orchestrator does **not** load the layer playbooks itself — each spawned surface agent loads only its own playbook (`references/layers/<surface>.md`).

### Each layer sub-agent

- Loads `references/layers/<layer>.md` and the core refs from its CSV row
- Runs the three lenses **sequentially inside itself** — do not spawn further sub-agents (nested delegation is unreliable across hosts). Switch persona explicitly between passes.
- Identifies the target persona for that layer
- Returns a per-layer finding list + a 0–10 score from `references/core/score-rubric.md` and a one-line "biggest gap" summary

### Orchestrator synthesis

After all layer sub-agents return:

1. **Rank findings cross-layer** by severity, highest first
2. **Surface the worst-offending layers** in a per-layer score table
3. **Suite-wide path to 10/10** — top 3 fixes that lift overall test quality most, not per-layer polish
4. **Emit `templates/audit-report-multi.md`** rather than the single-layer template; append each layer's full report at the end

### When to skip cross-layer mode

- Narrow questions ("review my unit tests") — one playbook is enough
- Scoped reviews where the user named ≤ 3 layers explicitly — dispatch only those
- Layers requiring secrets or live production access for some — exclude from fan-out

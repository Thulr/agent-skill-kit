# perf-design Eval Cases

Activation + behavioral cases for `perf-design` — designing instrumentation,
SLOs, tracing topology, and latency budgets *before* a problem ships;
profile-first optimization of a known-slow path; and program-level observability
/ reliability strategy (design / optimize / strategize). Auditing or diagnosing
an *existing* system is `perf-audit`; those appear here as **negatives**.
Developer-facing or local build/inner-loop perf is `dx-design`; end-user product
UX is `ux-audit`.

## Static verification

```bash
bash skills/perf-design/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author cleanliness,
the design-doc / optimize-plan / strategy-doc template shapes, CSV registry
integrity, playbook structure/word-count, and that the intent-router carries
exactly design / optimize / strategize.

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic design/optimize/strategize prompts; asks at most
one blocker question when intent or surface is missing; does not inspect
systems/networks or write from a vague invocation; routes `intent-router.csv` →
`intents/<intent>.csv` → one playbook; names a target persona; emits a concrete
good-shaped pattern with a named measurement method and testable acceptance
criteria.

---

## Case 1 — Bare activation menu
**Prompt:** `Use perf-design.`
**Expected:** loads `intent-router.csv`; shows the design / optimize / strategize menu; waits.
**Fail if:** inspects systems, runs commands, or invents a design.

## Case 2 — SLO design
**Prompt:** `Design the SLO program for our new payments service.`
**Expected:** routes (design, slos); loads `playbooks/slos.md`; `design-doc.md` shape — good-shaped pattern (sample SLI/SLO definition + error-budget policy + an alert rule that won't page on noise), heuristics applied, anti-patterns avoided, acceptance criteria.
**Fail if:** uses an audit/severity template for a design task; omits the good-shaped pattern.

## Case 3 — Instrumentation design
**Prompt:** `What metrics and span attributes should we emit for a new service so we can debug it later?`
**Expected:** routes (design, metrics); names the operator persona; produces a concrete RED/USE metric set and span schema + acceptance criteria.

## Case 4 — Profile-first optimization
**Prompt:** `Plan a tail-latency optimization pass for the checkout API.`
**Expected:** routes (optimize, latency); loads `playbooks/latency.md`; `optimize-plan.md` shape — profile *before* sequencing, a before/after measurement gate per step, regression guards.
**Fail if:** proposes changes without a profile; omits the before/after gate.

## Case 5 — Program-level strategy
**Prompt:** `Strategize our observability roadmap across logs, metrics, and traces, anchored on the SLO program.`
**Expected:** routes (strategize, slos); `strategy-doc.md` shape with a baseline, a target end-state, and an adoption sequence — not a single-surface fix.

## Case 6 — Intent/surface ambiguity
**Prompt:** `Help me with our observability.`
**Expected:** recognizes design-family intent but asks for the intent and surface; offers the menu; does not inspect first.

## Case 7 — Load discipline
**Prompt:** `Design our trace sampling topology.` (clear (design, tracing))
**Expected:** loads `intent-router.csv`, `intents/design.csv`, `playbooks/tracing.md`, the row's core_refs. Does NOT load other playbooks.

---

# Negative cases — should not trigger (or should defer)

## N1 — Diagnose a live incident
**Prompt:** `Our p99 doubled overnight — diagnose it.`
**Expected:** recognizes this is **diagnose** of an existing system; defers to `perf-audit`.
**Fail if:** produces a design doc for a live regression.

## N2 — Audit an existing system
**Prompt:** `Audit our observability stack and score the gaps.`
**Expected:** recognizes this is **audit**; defers to `perf-audit`.

## N3 — Review existing SLOs/alerts
**Prompt:** `On-call is paged on noise — review our existing SLIs and thresholds.`
**Expected:** recognizes critique of an existing posture; defers to `perf-audit`.

## N4 — Developer-facing / local build perf
**Prompt:** `Our local build is slow — design a faster inner loop for developers.`
**Expected:** recognizes developer inner-loop perf, not production runtime perf; defers to `dx-design`.

## N5 — Developer-facing config design
**Prompt:** `Design how our CLI reads config — file vs env vs flag precedence.`
**Expected:** recognizes DX surface design; defers to `dx-design`.

## N6 — End-user product UX
**Prompt:** `Design a lower-friction consumer signup flow.`
**Expected:** recognizes end-user audience; defers to `ux-audit`.

## N7 — Internal code refactor
**Prompt:** `Refactor this handler to use early returns.`
**Expected:** recognizes internal refactoring, not perf design; declines.

# dx-design Eval Cases

Activation + behavioral cases for `dx-design` — designing a *new* developer
surface before the code exists. Auditing or debugging an existing surface is
`dx-audit`; those appear here as **negatives**.

## Static verification

```bash
bash skills/dx-design/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author cleanliness,
the design-doc template shape, CSV registry integrity, playbook
structure/word-count, and that the intent-router is design-only.

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic design prompts; asks at most one blocker question
when the surface is missing; does not inspect files/networks or write from a
vague invocation; routes `intent-router.csv` → `intents/design.csv` → one
playbook; names a target developer persona; emits the `design-doc.md` shape with
a concrete good-shaped pattern + acceptance criteria.

---

## Case 1 — Bare activation menu
**Prompt:** `Use dx-design.`
**Expected:** loads `intent-router.csv` + `intents/design.csv`; shows the surface menu; waits.
**Fail if:** inspects files, runs commands, or invents a design.

## Case 2 — API design
**Prompt:** `We're designing a new HTTP API for billing events. What should we get right up front?`
**Expected:** routes (design, api); loads `playbooks/api.md`; `design-doc.md` shape — good-shaped pattern (sample endpoint + error envelope + idempotency key), heuristics applied, anti-patterns avoided, acceptance criteria.
**Fail if:** uses an audit template / severity findings for a design task; omits the good-shaped pattern.

## Case 3 — SDK pre-1.0 shape
**Prompt:** `Lock the public shape of our SDK before 1.0.`
**Expected:** routes (design, sdk); names the integrator persona; produces a concrete interface shape + acceptance criteria; cites stable-contract grounding.

## Case 4 — Plugin contract design
**Prompt:** `Design an extension API for our CLI so third parties can add subcommands.`
**Expected:** routes (design, plugin); loads `playbooks/plugin.md`; good-shaped pattern with named extension points, explicit lifecycle, failure isolation.
**Fail if:** routes to cli only and ignores the plugin playbook.

## Case 5 — Surface ambiguity
**Prompt:** `Help me design our developer experience.`
**Expected:** recognizes design intent but asks for the surface; offers the `intents/design.csv` menu; does not inspect first.

## Case 6 — Load discipline
**Prompt:** `Design our error envelope.` (clear (design, errors))
**Expected:** loads `intent-router.csv`, `intents/design.csv`, `playbooks/errors.md`, the row's core_refs. Does NOT load other playbooks.

---

# Negative cases — should not trigger (or should defer)

## N1 — Audit an existing surface
**Prompt:** `Our CLI --help is dense and confusing — review it and tell me what to tighten.`
**Expected:** recognizes this is **critique** of an existing surface; defers to `dx-audit`.
**Fail if:** produces a design doc for a surface that already ships.

## N2 — Debug a reported issue
**Prompt:** `Users hit "auth failed" after rotating keys — what's wrong?`
**Expected:** defers to `dx-audit` (debug).

## N3 — End-user UI design
**Prompt:** `Design a lower-friction consumer signup flow.`
**Expected:** recognizes end-user audience; defers to `ui-design` / `ux-audit`.

## N4 — AI/Agent SDK design
**Prompt:** `Design the agent loop and tool-call contract for our AI/Agent SDK.`
**Expected:** defers to `agent-dx` (SDK/tool) or `agent-docs` (AGENTS.md); does not route through a DX playbook.

## N5 — Internal refactor
**Prompt:** `Refactor this function to use early returns.`
**Expected:** recognizes internal refactoring, not surface design; declines.

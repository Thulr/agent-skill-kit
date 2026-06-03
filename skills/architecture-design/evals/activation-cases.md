# architecture-design Eval Cases

Activation + behavioral cases for `architecture-design` — designing a target
clean architecture for new work, sequencing a safe refactor toward it, or
explaining a principle (intents: `design`, `refactor`, `explain`). Auditing and
scoring an *existing* codebase for violations is `architecture-audit`; those
appear here as **negatives**.

## Static verification

```bash
bash skills/architecture-design/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author/title
cleanliness, the three template shapes (design-doc / refactor-runbook /
explanation), CSV registry integrity, playbook structure/word-count, and that
the intent-router carries design / refactor / explain (no `audit`).

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic design/refactor/explain prompts; asks at most one
blocker question when the surface is missing; does not inspect files/networks or
write from a vague invocation; routes `intent-router.csv` →
`intents/<intent>.csv` → one playbook; names a target persona; emits the intent's
template shape with a concrete good-shaped pattern (or step sequence / worked
example); surfaces school disagreements rather than flattening them.

---

## Case 1 — Bare activation menu
**Prompt:** `Use architecture-design.`
**Expected:** loads `intent-router.csv` (+ `starter-scenarios.csv`); shows the
intent menu (design / refactor / explain); offers the mode choice; waits.
**Fail if:** inspects files, runs commands, or invents a design.

## Case 2 — Bounded-context design
**Prompt:** `New service, two bounded contexts, unclear seam — where should the boundary go before we write code?`
**Expected:** routes (design, bounded-context); loads `playbooks/bounded-context.md`;
`design-doc.md` shape — concrete seam proposal, heuristics applied, acceptance criteria.
**Fail if:** uses an audit template / severity scoring for code that does not exist yet.

## Case 3 — Boundary design
**Prompt:** `How should I set up layers, ports, and adapters for this new module so the domain doesn't depend on the framework?`
**Expected:** routes (design, boundaries); names the target persona; produces a
concrete layer/port shape + acceptance criteria.

## Case 4 — Refactor sequencing
**Prompt:** `Our handlers call the DB directly. Plan a safe, reversible refactor to ports and adapters.`
**Expected:** routes (refactor, boundaries); loads `playbooks/boundaries.md`;
`refactor-runbook.md` shape — a parallel-change step sequence, each step
reversible, with verification.
**Fail if:** emits a big-bang rewrite plan; omits the per-step verification.

## Case 5 — Concept explanation
**Prompt:** `Explain the difference between an aggregate, an entity, and a value object, and what "anemic" means.`
**Expected:** routes (explain, domain-model); `explanation.md` shape — concept in
one sentence, what it is / is not, a small worked example; grounded in the sources.
**Fail if:** produces a design doc or an audit; gives ungrounded opinion.

## Case 6 — Intent ambiguity
**Prompt:** `Help me with our architecture.`
**Expected:** recognizes design-family work but asks which intent/surface; offers
the menu; does not inspect first.

## Case 7 — Load discipline
**Prompt:** `Design the dependency-direction invariant for this new module.` (clear (design, dependency-rule))
**Expected:** loads `intent-router.csv`, `intents/design.csv`,
`playbooks/dependency-rule.md`, the row's core_refs. Does NOT load other playbooks.

---

# Negative cases — should not trigger (or should defer)

## N1 — Audit an existing codebase
**Prompt:** `Our domain is anemic and our use cases import the JPA impls — audit it and score how bad it is.`
**Expected:** recognizes this is **critique** of existing code; defers to `architecture-audit`.
**Fail if:** produces a design doc instead of a scored findings report.

## N2 — Closeout against saved findings
**Prompt:** `Verify whether CA-DEP-002 is fixed using the saved workflow-state JSON.`
**Expected:** defers to `architecture-audit` (audit closeout).

## N3 — Developer-facing surface design
**Prompt:** `Pin down the public API contracts for our SDK before 1.0.`
**Expected:** recognizes a DX surface, not internal code structure; defers to `dx-design`.

## N4 — End-user UI design
**Prompt:** `Design a lower-friction consumer signup flow.`
**Expected:** recognizes end-user audience; defers to `ui-design` (or `ux-audit`).

## N5 — AI/Agent SDK design
**Prompt:** `Design the agent loop and tool-call contract for our AI/Agent SDK.`
**Expected:** defers to `agent-experience`; does not route through an architecture playbook.

## N6 — Internal function refactor
**Prompt:** `Refactor this function to use early returns.`
**Expected:** recognizes line-level refactoring, not architectural design; declines.

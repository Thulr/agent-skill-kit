# architecture-critique Eval Cases

Activation + behavioral cases for `architecture-critique` — auditing an existing
codebase or module for clean-architecture violations (single intent: `audit`).
Designing, refactoring toward, or explaining a target architecture is
`architecture-design`; those appear here as **negatives**.

## Static verification

```bash
bash skills/architecture-critique/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author/title
cleanliness, CSV registry integrity, playbook structure/word-count, the
tracking gates (CA- IDs, `architecture-critique-` ledger prefix), and that the
intent-router is audit-only (exactly one data row).

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic architecture-audit prompts; asks at most one
blocker question when scope is missing; does not inspect files/networks or write
from a vague invocation; routes `intent-router.csv` → `intents/audit.csv` → one
playbook; names a target persona; scores 0–10; emits the `audit-report.md`
shape; surfaces school disagreements rather than flattening them.

---

## Case 1 — Bare activation menu
**Prompt:** `Use architecture-critique.`
**Expected:** loads `intent-router.csv` (+ `starter-scenarios.csv`); shows the
surface menu (dependency-rule / boundaries / domain-model / bounded-context /
cross-cutting / all); offers the mode choice; waits.
**Fail if:** inspects files, runs commands, or invents an audit.

## Case 2 — Anemic-domain audit
**Prompt:** an entity that is getter/setter-only plus a fat `*Service` class +
"is our domain anemic?"
**Expected:** routes (audit, domain-model); loads `playbooks/domain-model.md` +
core_refs; names the target persona; scores 0–10; findings with severity 0–4,
heuristic cited, evidence, verification; `audit-report.md` shape with `CA-DOMAIN-NNN` IDs.
**Fail if:** loads multiple playbooks; gives generic advice without severity; omits verification.

## Case 3 — Dependency-direction audit
**Prompt:** `Audit dependency direction — use cases import the JPA repo impls and a couple entities have @Entity annotations.`
**Expected:** routes (audit, dependency-rule); recommends a structural
dependency-graph sweep; classifies framework-in-domain as High/Critical;
`CA-DEP-NNN` IDs.
**Fail if:** classifies from names without proposing the structural check.

## Case 4 — Multi-surface audit (fan-out)
**Prompt:** `Do a full architecture review across dependency direction, boundaries, the domain model, and context seams.`
**Expected:** routes (audit, all); dispatches one agent per surface when
permitted; synthesizes into `audit-report-multi.md`; per-surface scores; flags
cross-surface patterns.
**Fail if:** loads every playbook up front in one context; produces no per-surface scores.

## Case 5 — Tracked audit artifacts
**Prompt:** `Audit all our architecture surfaces and save the findings so we can close them out later.`
**Expected:** stable `CA-<surface>-NNN` IDs; creates both
`docs/audits/architecture-critique-findings-ledger-…md` and
`…workflow-state-…json` (or the `audit-artifacts/architecture-critique-…`
fallback); reports both paths.
**Fail if:** only offers to track, or emits the ledger inline without saving.

## Case 6 — Closeout from saved state
**Prompt:** `Verify whether CA-DEP-002 is fixed in this PR using docs/audits/architecture-critique-workflow-state-2026-05-22-billing.json.`
**Expected:** loads `audit-mechanics.md` + `trackable-findings.md` then the saved
state; reruns that finding's verification rule; updates status only if it passes.
**Fail if:** marks it closed because the PR merged; ignores saved state; invents a new ledger.

## Case 7 — Ambiguous private-system request
**Prompt:** `Review our architecture and tell me what to fix.`
**Expected:** asks one blocker question (which surface); does not inspect first.

## Case 8 — Load discipline
**Prompt:** a snippet + "audit the boundaries here."
**Expected:** loads only `intent-router.csv`, `intents/audit.csv`,
`playbooks/boundaries.md`, the row's core_refs. Does NOT load other playbooks.

---

# Negative cases — should not trigger (or should defer)

## N1 — Greenfield design
**Prompt:** `We're starting a new service with two bounded contexts — where should the seam go before we write code?`
**Expected:** recognizes this is **design**, not critique; defers to `architecture-design`.
**Fail if:** runs an audit / produces severity findings for code that does not exist yet.

## N2 — Refactor sequencing
**Prompt:** `Our handlers call the DB directly. Plan a safe refactor to ports and adapters.`
**Expected:** recognizes this is **refactor** (a planned move, not an audit); defers to `architecture-design`.

## N3 — Concept explanation
**Prompt:** `Explain ports-and-adapters and the dependency rule against our code.`
**Expected:** recognizes **explain** intent; defers to `architecture-design`.

## N4 — Developer-facing surface
**Prompt:** `Our CLI --help is dense and confusing — review it and tell me what to tighten.`
**Expected:** recognizes a DX surface, not internal code structure; defers to `dx-critique`.

## N5 — End-user accessibility
**Prompt:** `Audit our checkout page for WCAG 2.2 AA compliance.`
**Expected:** defers to `ux-critique` despite the "audit" keyword.

## N6 — Production performance
**Prompt:** `Our reporting query is slow in production at 2pm. Trace what's causing it.`
**Expected:** recognizes operational/runtime perf, not architecture; defers.

## N7 — Internal function refactor
**Prompt:** `Refactor this function to use early returns instead of nested ifs.`
**Expected:** recognizes line-level refactoring, not architectural critique; declines.

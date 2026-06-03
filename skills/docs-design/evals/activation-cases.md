# docs-design Eval Cases

Activation + behavioral cases for `docs-design` — designing *new* documentation
or defining how to measure it (design / measure) across developer docs, end-user
help, and agent-readable docs. Auditing or debugging *existing* docs is
`docs-audit`; those appear here as **negatives**.

## Static verification

```bash
bash skills/docs-design/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author cleanliness and
word count (<800), the design-doc and measurement-plan template shapes, CSV
registry integrity, playbook structure/word-count, and that the intent-router is
design-and-measure only.

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic design/measure prompts; asks at most one blocker
question when the surface or intent is missing; does not inspect files/networks
or write from a vague invocation; routes `intent-router.csv` →
`intents/<intent>.csv` → one playbook; names the target audience; emits the
`design-doc.md` or `measurement-plan.md` shape.

---

## Case 1 — Bare activation menu
**Prompt:** `Use docs-design.`
**Expected:** loads `intent-router.csv` + starter scenarios; shows the design / measure menu; waits.
**Fail if:** inspects files, runs commands, or invents a design.

## Case 2 — Docs IA design
**Prompt:** `We have no docs yet — design the documentation IA and mode taxonomy for a new product.`
**Expected:** routes (design, foundations); loads `playbooks/foundations.md`; `design-doc.md` shape — source of truth, renderings, IA, audience paths, acceptance criteria.
**Fail if:** uses an audit template / severity findings for a design task; omits the proposed structure.

## Case 3 — API/tool contract docs design
**Prompt:** `What should our MCP tool descriptions and error envelope look like so agents call correctly?`
**Expected:** routes (design, api-contracts); names the agent + developer audiences; proposes a concrete description/error shape + acceptance criteria; cites grounding.
**Fail if:** gives abstract advice with no concrete shape.

## Case 4 — Docs measurement plan
**Prompt:** `Define how we measure docs quality — TTFHW, sample freshness, zero-result search — with thresholds and owners.`
**Expected:** routes (measure, dx-docs or foundations); emits `measurement-plan.md` — metrics table with signal/threshold/owner/action, gates and evals, baseline plan.
**Fail if:** lists dashboards with no threshold, owner, or triggered action.

## Case 5 — Surface ambiguity
**Prompt:** `Help me design our documentation experience.`
**Expected:** recognizes design intent but asks for the surface (or design-vs-measure); offers the CSV menu; does not inspect first.

## Case 6 — Load discipline
**Prompt:** `Design our in-product help and onboarding.` (clear (design, ux-help))
**Expected:** loads `intent-router.csv`, `intents/design.csv`, `playbooks/ux-help.md`, the row's core_refs. Does NOT load other playbooks.

---

# Negative cases — should not trigger (or should defer)

## N1 — Audit existing docs
**Prompt:** `Our quickstart has 9 steps and devs get stuck at auth — audit this README and tell me what's wrong.`
**Expected:** recognizes this is **critique** of existing docs; defers to `docs-audit`.
**Fail if:** produces a design doc for docs that already ship.

## N2 — Debug a docs failure
**Prompt:** `Our refund example throws a 400 because the snippet is stale — why?`
**Expected:** defers to `docs-audit` (debug).

## N3 — End-user UI design
**Prompt:** `Design a lower-friction consumer signup flow.`
**Expected:** recognizes end-user visual UI; defers to `ux-audit` / `ui-design`.

## N4 — Repo agent hardening
**Prompt:** `Make our repo agent-ready — wrong test commands, stale AGENTS.md.`
**Expected:** defers to `agent-experience`; does not route through a docs playbook.

## N5 — Internal refactor
**Prompt:** `Refactor this function to use early returns.`
**Expected:** recognizes internal refactoring, not docs design; declines.

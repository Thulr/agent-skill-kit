# docs-audit Eval Cases

Activation + behavioral cases for `docs-audit` — critiquing *existing*
documentation (audit / debug) across developer docs, end-user help, and
agent-readable docs. Designing or measuring new docs is `docs-design`; cases
that route to design/measure appear here as **negatives**.

## Static verification

```bash
bash skills/docs-audit/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author cleanliness and
word count (<800), CSV registry integrity, playbook structure/word-count, that
the intent-router is critique-only (audit / debug), and that no tracking surface
leaked in (docs does not track findings).

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic docs-audit prompts; asks at most one blocker
question when scope is missing; does not inspect files/networks or write from a
vague invocation; routes `intent-router.csv` → `intents/<intent>.csv` → one
playbook; names the target audience; emits the intent's template shape.

---

## Case 1 — Bare activation menu
**Prompt:** `Use docs-audit.`
**Expected:** loads `intent-router.csv`; shows the audit / debug menu; waits.
**Fail if:** inspects files, runs commands, or invents an audit.

## Case 2 — Concrete dev-docs audit
**Prompt:** a README/quickstart block + "where do new devs get stuck?"
**Expected:** routes (audit, dx-docs); loads `playbooks/dx-docs.md` + core_refs; names target audience; scores 0–10; findings table with severity 0–4, evidence, recommendation, verification; `audit-report.md` shape.
**Fail if:** loads multiple playbooks; rewrites copy without severity; omits verification.

## Case 3 — Stale-example debug
**Prompt:** `Our refund example in the docs throws a 400 — the snippet is from the old API. Why does this keep happening?`
**Expected:** routes (debug, dx-docs); ranks hypotheses by mechanism (staleness vs absence vs ambiguity) before fixes; names a source-of-truth/freshness-gate prevention; `debug-runbook.md` shape.
**Fail if:** jumps to a one-off snippet fix without naming the drift mechanism or a prevention gate.

## Case 4 — Agent tool-call debug
**Prompt:** `Our agent keeps calling the wrong MCP tool — two descriptions are nearly identical. Why?`
**Expected:** routes (debug, api-contracts); loads `playbooks/api-contracts.md`; traces the description ambiguity; recommends targeted (not maximalist) description fixes with a verification.
**Fail if:** suggests adding more prose indiscriminately; omits verification.

## Case 5 — Multi-surface audit with conflict
**Prompt:** `Audit our dev docs, help center, and llms.txt — I think the agent fix is hurting human readers.`
**Expected:** routes (audit, all); dispatches the four lenses; preserves the audience conflict instead of flattening it; routes the conflict through `audience-conflicts.md`; reports which lenses ran.
**Fail if:** collapses the conflict; loads every playbook into one context instead of fanning out.

## Case 6 — Ambiguous private-system request
**Prompt:** `Docs review our onboarding and tell me what to fix.`
**Expected:** asks one blocker question (which intent / which surface); does not inspect first.

## Case 7 — Stable finding IDs
**Prompt:** an audit request on the API reference.
**Expected:** routes (audit, api-contracts); assigns stable IDs like `DOC-api-contracts-NNN`; severity 0–4 per `severity-rubric.md`.
**Fail if:** emits findings without stable IDs or severity.

## Case 8 — Load discipline
**Prompt:** a help-center snippet + "audit this."
**Expected:** loads only `intent-router.csv`, `intents/audit.csv`, `playbooks/ux-help.md`, the row's core_refs. Does NOT load other playbooks.

## Case 9 — Right-size to project scale (calibration)
**Prompt:** `Audit the docs for my ~20-file internal tool — pre-release, just my team uses it.`
**Expected:** infers **Prototype** tier per `references/calibration.md`; narrows to 1–2 surfaces (no `all` fan-out); collapses "every-X" gaps into a few systemic findings; the report names the `Project tier` and splits fixes into "Now" vs "Later — as it grows".
**Fail if:** recommends roughly one doc per code file, runs the full multi-surface fan-out, or files one equal-weight finding per missing artifact.

---

# Negative cases — should not trigger (or should defer)

## N1 — New-docs design
**Prompt:** `Design our docs information architecture from scratch for a new product.`
**Expected:** recognizes this is **design**, not critique; defers to `docs-design`.
**Fail if:** runs an audit / produces severity findings for docs that do not exist yet.

## N2 — Docs measurement
**Prompt:** `What telemetry and CI gates should we set up to measure docs quality?`
**Expected:** recognizes this is **measure**; defers to `docs-design`.

## N3 — End-user product UX
**Prompt:** `Our consumer signup form has a 60% drop-off. Help me reduce friction.`
**Expected:** recognizes end-user product flow (not help content); defers to `ux-audit`.

## N4 — End-user accessibility
**Prompt:** `Audit our checkout page for WCAG 2.2 AA compliance.`
**Expected:** defers to `ux-audit` despite the "audit" keyword.

## N5 — Repo agent hardening
**Prompt:** `Claude Code trips on our repo — wrong test commands, stale AGENTS.md. Make it agent-friendly.`
**Expected:** defers to `agent-experience`; does not route through a docs playbook.

## N6 — Concept explanation
**Prompt:** `Explain how OAuth2 PKCE works for a one-pager.`
**Expected:** recognizes educational content authoring, not docs critique; defers.

## N7 — Internal code refactor
**Prompt:** `Refactor this function to use early returns instead of nested ifs.`
**Expected:** recognizes internal refactoring, not docs critique; declines.

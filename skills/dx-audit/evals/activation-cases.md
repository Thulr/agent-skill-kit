# dx-audit Eval Cases

Activation + behavioral cases for `dx-audit` — critiquing an existing
developer-facing surface (audit / debug / edge-pass). Designing a new surface
is `dx-design`; cases that route to design appear here as **negatives**.

## Static verification

```bash
bash skills/dx-audit/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author cleanliness,
CSV registry integrity, playbook structure/word-count, and intent-router shape
(exactly audit / debug / edge-pass).

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic DX-critique prompts; asks at most one blocker
question when scope is missing; does not inspect files/networks or write from a
vague invocation; routes `intent-router.csv` → `intents/<intent>.csv` → one
playbook; names a target developer persona; emits the intent's template shape.

---

## Case 1 — Bare activation menu
**Prompt:** `Use dx-audit.`
**Expected:** loads `intent-router.csv`; shows the audit / debug / edge-pass menu; waits.
**Fail if:** inspects files, runs commands, or invents an audit.

## Case 2 — Concrete CLI audit
**Prompt:** a CLI `--help` block + "review this CLI help output for DX."
**Expected:** routes (audit, cli); loads `playbooks/cli.md` + core_refs; names target developer; scores 0–10; findings table with severity 0–4, fix, verification; `audit-report.md` shape.
**Fail if:** loads multiple playbooks; rewrites copy without severity; omits verification.

## Case 3 — Tracked audit artifacts
**Prompt:** `Audit all DX surfaces and save the findings so we can close them out later.`
**Expected:** routes (audit, all); stable `DX-<surface>-NNN` IDs; creates both `docs/audits/dx-audit-findings-ledger-…md` and `…workflow-state-…json` (or the `audit-artifacts/dx-audit-…` fallback); reports both paths.
**Fail if:** only offers to track, or emits the ledger inline without saving.

## Case 4 — Closeout from saved state
**Prompt:** `Verify whether DX-CLI-002 is fixed in this PR using docs/audits/dx-audit-workflow-state-2026-05-20-cli.json.`
**Expected:** loads `trackable-findings.md` then the saved state; reruns that finding's verification rule; updates status only if it passes.
**Fail if:** marks it closed because the PR merged; ignores saved state; invents a new ledger.

## Case 5 — Error-message debug
**Prompt:** `Our API returns HTTP 200 with {error:"…"} on bad input. Is that fine?`
**Expected:** routes (debug, errors) or (audit, errors); loads `playbooks/errors.md`; recommends status-code semantics, documented envelope, request id, tests; debug-runbook or audit-report shape.
**Fail if:** says it's acceptable; gives generic advice; omits verification.

## Case 6 — Ambiguous private-system request
**Prompt:** `DX review our onboarding flow and tell me what to fix.`
**Expected:** asks one blocker question (which intent / which surface); does not inspect first.

## Case 7 — Pre-ship edge pass
**Prompt:** `Run a pre-1.0 risk pass on our CLI before we release.`
**Expected:** routes `edge-pass`; selects relevant rows; `edge-checklist.md` shape with severity, blockers, re-run trigger.
**Fail if:** misses categories; omits re-run trigger.

## Case 8 — Load discipline
**Prompt:** a CLI snippet + "audit this."
**Expected:** loads only `intent-router.csv`, `intents/audit.csv`, `playbooks/cli.md`, the row's core_refs. Does NOT load other playbooks.

## Case 9 — Right-size to project scale (calibration)
**Prompt:** `Audit the DX of a single-command CLI I built for my team — not published, no external users.`
**Expected:** infers **Prototype** tier per `references/calibration.md`; narrows to 1–2 surfaces (no `all` fan-out); collapses same-mechanism gaps into a few systemic findings; the report names the `Project tier` and splits fixes into "Now" vs "Later — as it grows".
**Fail if:** runs the full multi-surface fan-out or files one equal-weight finding per missing best-practice.

---

# Negative cases — should not trigger (or should defer)

## N1 — New-surface design
**Prompt:** `We're designing a new HTTP API for billing events from scratch — what should we get right up front?`
**Expected:** recognizes this is **design**, not critique; defers to `dx-design`.
**Fail if:** runs an audit / produces severity findings for a surface that does not exist yet.

## N2 — End-user product UX
**Prompt:** `Our consumer signup form has a 60% drop-off. Help me reduce friction.`
**Expected:** recognizes end-user audience; defers to `ux-audit`.

## N3 — End-user accessibility
**Prompt:** `Audit our checkout page for WCAG 2.2 AA compliance.`
**Expected:** defers to `ux-audit` despite the "audit" keyword.

## N4 — Production performance debugging
**Prompt:** `Our reporting query is slow in production at 2pm. Trace what's causing it.`
**Expected:** recognizes operational/runtime perf, not developer-perceived perf; defers (perf-audit).

## N5 — AI-agent surface
**Prompt:** `Claude Code keeps tripping on our repo — wrong test commands, blocked pushes, bad AGENTS.md. Make it agent-friendly.`
**Expected:** defers to `agent-experience`; does not route through a DX playbook.

## N6 — Concept explanation
**Prompt:** `Explain how OAuth2 PKCE works for a one-pager.`
**Expected:** recognizes educational content; defers.

## N7 — Internal code refactor
**Prompt:** `Refactor this function to use early returns instead of nested ifs.`
**Expected:** recognizes internal refactoring, not surface critique; declines.

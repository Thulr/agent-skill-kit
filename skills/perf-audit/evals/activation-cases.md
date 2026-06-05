# perf-audit Eval Cases

Activation + behavioral cases for `perf-audit` — critiquing the performance
and observability posture of an existing production / runtime system (audit /
diagnose). Designing instrumentation/SLOs or optimizing a known-slow path is
`perf-design`; cases that route there appear here as **negatives**. Developer-
facing or local build/inner-loop perf is `dx-audit`; end-user product UX is
`ux-audit`.

## Static verification

```bash
bash skills/perf-audit/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author cleanliness,
CSV registry integrity, playbook structure/word-count, the tracking-artifact
contract, and intent-router shape (exactly audit / diagnose).

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic perf-audit prompts; asks at most one blocker
question when scope is missing; does not inspect systems/networks or write from a
vague invocation; routes `intent-router.csv` → `intents/<intent>.csv` → one
playbook; names a target persona; names the measurement method (not just the
metric); emits the intent's template shape.

---

## Case 1 — Bare activation menu
**Prompt:** `Use perf-audit.`
**Expected:** loads `intent-router.csv`; shows the audit / diagnose menu with
named starter scenarios; waits.
**Fail if:** inspects systems, runs commands, or invents an audit.

## Case 2 — Concrete latency diagnosis
**Prompt:** `Our checkout API p99 doubled overnight — diagnose it.`
**Expected:** routes (diagnose, latency); loads `playbooks/latency.md` + core_refs; ranks hypotheses *before* naming fixes; names a disconfirming measurement per hypothesis; `diagnose-runbook.md` shape with a root cause and verification.
**Fail if:** jumps to a fix without ranked hypotheses; omits the measurement method; treats the median as the signal.

## Case 3 — Tracked multi-surface audit
**Prompt:** `Audit our whole observability stack and save the findings so we can close them out later.`
**Expected:** routes (audit, all); fans out one agent per surface; stable `PERF-<surface>-NNN` IDs; scores each surface 0–10; creates both `docs/audits/perf-audit-findings-ledger-…md` and `…workflow-state-…json` (or the `audit-artifacts/perf-audit-…` fallback); reports both paths.
**Fail if:** only offers to track, or emits the ledger inline without saving.

## Case 4 — Closeout from saved state
**Prompt:** `Verify whether PERF-latency-002 is fixed in this PR using docs/audits/perf-audit-workflow-state-2026-05-20-checkout.json.`
**Expected:** loads `trackable-findings.md` then the saved state; reruns that finding's verification rule (the measurement returns to baseline); updates status only if it passes.
**Fail if:** marks it closed because the PR merged; ignores saved state; invents a new ledger.

## Case 5 — Coordinated-omission edge
**Prompt:** `Our benchmark says p99 is 12ms but prod feels slower — is our measurement trustworthy?`
**Expected:** routes (diagnose/audit, latency); flags coordinated-omission risk in the load generator; recommends a backpressure-aware generator and lossless quantile recording; measurement-method named.
**Fail if:** accepts the benchmark number at face value.

## Case 6 — Ambiguous private-system request
**Prompt:** `Look at our perf and tell me what to fix.`
**Expected:** asks one blocker question (which intent — audit or diagnose — and which surface); does not inspect first.

## Case 7 — USE-method resource audit
**Prompt:** `Run a USE-method pass on the API tier.`
**Expected:** routes (audit, resources); loads `playbooks/resources.md`; checks utilization / saturation / errors per resource; severity 0–4 findings with measurement and verification; `audit-report.md` shape.
**Fail if:** loads multiple playbooks; gives generic advice without severity.

## Case 8 — Load discipline
**Prompt:** a trace/metric snippet + "audit our tracing."
**Expected:** loads only `intent-router.csv`, `intents/audit.csv`, `playbooks/tracing.md`, the row's core_refs. Does NOT load other playbooks.

## Case 9 — Right-size to project scale (calibration)
**Prompt:** `Perf/observability audit of an internal cron job — single instance, no SLOs yet, just us.`
**Expected:** infers **Prototype** tier per `references/calibration.md`; narrows to 1–2 surfaces (no `all` fan-out); collapses same-mechanism gaps; the report names the `Project tier` and splits fixes into "Now" vs "Later — as it grows".
**Fail if:** audits all seven surfaces and recommends a full SLO/telemetry program for a single-instance internal job.

---

# Negative cases — should not trigger (or should defer)

## N1 — Design instrumentation/SLOs from scratch
**Prompt:** `Design the SLO program for our new payments service from scratch.`
**Expected:** recognizes this is **design**, not critique; defers to `perf-design`.
**Fail if:** runs an audit / produces severity findings for a system that does not exist yet.

## N2 — Optimize a known-slow path
**Prompt:** `Plan a profile-first tail-latency optimization pass for the checkout API.`
**Expected:** recognizes this is **optimize**; defers to `perf-design`.

## N3 — Developer-facing / local build perf
**Prompt:** `pnpm install takes 45s and our jest suite is 8 minutes — what's worth speeding up first?`
**Expected:** recognizes developer inner-loop perf, not production runtime perf; defers to `dx-audit`.

## N4 — Developer-facing CLI ergonomics
**Prompt:** `Our CLI --help is dense and confusing — review it.`
**Expected:** recognizes DX, not production perf; defers to `dx-audit`.

## N5 — End-user product UX
**Prompt:** `Our consumer signup form has a 60% drop-off. Help me reduce friction.`
**Expected:** recognizes end-user audience; defers to `ux-audit`.

## N6 — Concept explanation
**Prompt:** `Explain how trace context propagation works for a one-pager.`
**Expected:** recognizes educational content; defers.

## N7 — Internal code refactor
**Prompt:** `Refactor this handler to use early returns instead of nested ifs.`
**Expected:** recognizes internal refactoring, not posture critique; declines.

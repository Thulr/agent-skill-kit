# Activation cases — review-heuristics

Routes by domain (dx | docs | perf | test | ux | ui-craft | architecture),
then by intent and surface. Cases below are grouped by domain; they were merged
from the seven former heuristics skills when the review family consolidated
(see docs/specs/2026-05-28-catalog-consolidation/). A query that used to be a
negative pointing at a sibling review skill is now a positive intra-skill route.

---

## Domain: dx (formerly dx-heuristics)


These evals check whether `dx-heuristics` activates at the right time and
produces useful DX review behavior without side effects from vague prompts.

## Static Verification

Run from the repository root:

```bash
bash skills/dx-heuristics/evals/run-static-checks.sh
```

The static check verifies file presence, skill.json shape, SKILL.md
cleanliness (no source-author leak), CSV registry integrity, and every
playbook's structure and word count.

## Behavioral Eval Protocol

Run each behavioral case in a fresh agent session with only this skill
available or explicitly loaded. Do not provide extra repository context unless
the case includes it. Record the response and score it against the pass/fail
criteria.

**These are manual review cases by design.** They test conversational
behavior — routing, ambiguity handling, file-load discipline — that has no
single deterministic output, so automated grading would be brittle. The
static check (`evals/run-static-checks.sh`) handles structural and schema
gates in CI; behavioral cases are scored by a human reading the agent's
session log. Trigger-rate accuracy is measured separately by the
description-optimization loop (`evals/trigger-evals.json`).

Passing a case means the agent:

- activates the skill for realistic DX prompts
- asks at most one blocker question when scope is missing
- does not inspect files, call networks, or write files from vague invocation
- routes through `intent-router.csv` → `intents/<intent>.csv` → one playbook
- names a target developer persona
- emits output in the intent's template shape

---

## Case 1: Bare Activation Menu

**Prompt:** `Use dx-heuristics.`

**Expected:**

- Loads `references/intent-router.csv` only.
- Shows the intent menu (audit / design / debug / edge-pass).
- Waits for the user to choose.

**Fail if:** inspects files, runs commands, calls network tools, or invents an audit.

---

## Case 2: Concrete CLI Audit

**Prompt:** A CLI `--help` block followed by "review this CLI help output for DX."

**Expected:**

- Routes to (audit, cli).
- Loads `playbooks/cli.md` plus listed core_refs.
- Names target developer (first-time user or contributor).
- Scores current DX 0–10; target 10.
- Findings table with severity 0–4, fix, verification.
- Output follows `templates/audit-report.md` shape.

**Fail if:** loads multiple playbooks; rewrites copy without severity; omits verification.

---

## Case 2b: Tracked Audit Artifacts

**Prompt:** `Audit all DX surfaces and save the findings so we can close them out later.`

**Expected:**

- Routes to (audit, all).
- Assigns stable `DX-<surface>-NNN` finding IDs.
- Creates both `docs/audits/dx-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and `docs/audits/dx-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`, or the matching `audit-artifacts/dx-heuristics-...` fallback.
- Reports both saved paths.
- Does not create roadmaps, GitHub issues, or modify non-tracking project files without explicit confirmation.

**Fail if:** it only offers to create tracking artifacts or emits the ledger inline without saving.

---

## Case 2c: Closeout From Saved State

**Prompt:** `Verify whether DX-CLI-002 is fixed in this PR using docs/audits/dx-heuristics-workflow-state-2026-05-20-cli.json.`

**Expected:**

- Loads `references/trackable-findings.md`, then the workflow-state JSON and ledger it points at.
- Extracts `DX-CLI-002`, reruns that finding's verification rule, and updates status only if the rule passes.
- Treats the PR as evidence to inspect, not proof; does not close GitHub issues or edit non-tracking files without confirmation.

**Fail if:** it marks the finding closed only because the PR merged, ignores saved workflow state, or invents a new ledger.

---

## Case 3: API Error Message

**Prompt:** `The API returns "bad request" when the payload is wrong. Is that fine?`

**Expected:**

- Routes to (debug, errors) or (audit, errors).
- Loads `playbooks/errors.md`.
- Names target developer (integrator).
- Recommends cause-specific validation, expected shape, remediation, request id, tests.
- Output follows debug-runbook or audit-report template.

**Fail if:** says "bad request" is acceptable; gives generic advice without a concrete error shape; omits verification.

---

## Case 4: Ambiguous Private-System Request

**Prompt:** `DX review our onboarding flow and tell me what to fix.`

**Expected:**

- Asks one blocker question: which intent (audit/design/debug) and/or which surface (setup/docs/cli...).
- Does not inspect private systems, files, or networks before scope is set.

**Fail if:** begins tool use; asks long questionnaire; invents findings.

---

## Case 5: Contributor Workflow Audit

**Prompt:** A short contributor-onboarding step list, "Review for DX."

**Expected:**

- Routes to (audit, contributor).
- Loads `playbooks/contributor.md`.
- Names contributor as target developer.
- Flags missing test command, success criteria, tribal knowledge, PR evidence, fresh-machine path.
- Output follows audit-report template.

**Fail if:** only addresses test command; omits scores; no verification.

---

## Case 6: API Design

**Prompt:** `We're designing a new HTTP API for billing events. What should we get right up front?`

**Expected:**

- Routes to (design, api).
- Loads `playbooks/api.md`.
- Output follows `templates/design-doc.md` shape: good-shaped pattern (sample endpoint + error envelope + idempotency key), heuristics applied, anti-patterns avoided, acceptance criteria.

**Fail if:** uses audit template (severity findings) for a design task; omits the good-shaped pattern.

---

## Case 7: Auth Debug

**Prompt:** `Users keep reporting that auth fails after we rotate their API keys. What's wrong?`

**Expected:**

- Routes to (debug, auth).
- Loads `playbooks/auth.md`.
- Output follows `templates/debug-runbook.md`: hypotheses ranked with evidence, diagnostic steps, fix candidates, prevention.

**Fail if:** jumps to a fix without ranking hypotheses; omits prevention section.

---

## Case 8: Pre-Ship Edge Pass

**Prompt:** `Run a pre-1.0 risk pass on our CLI before we release.`

**Expected:**

- Routes to `edge-pass` and chooses the relevant edge-pass rows from
  `references/intents/edge-pass.csv` (for a CLI release this usually includes
  fresh-machine, env-skew, creds, version-skew, destructive, external-deps, and
  contributor-path).
- Output follows `templates/edge-checklist.md`: risk inventory across all
  selected categories with severity and verification, blockers list, re-run
  trigger.

**Fail if:** misses categories; omits re-run trigger.

---

## Case 9: Intent Ambiguity

**Prompt:** `Look at our SDK.`

**Expected:**

- Asks one question: audit / design / debug? Offers intent menu from intent-router.csv.
- Does not inspect anything yet.

**Fail if:** picks an intent on its own; starts inspection.

---

## Case 10: Surface Ambiguity

**Prompt:** `Audit our developer experience.`

**Expected:**

- Recognizes intent (audit) but asks for surface.
- Offers surface menu from `references/intents/audit.csv`.

**Fail if:** picks a surface on its own; inspects without scope.

---

## Case 11: Load Discipline

**Prompt:** A CLI snippet with "audit this." (clear (audit, cli))

**Expected:**

- Loads `intent-router.csv`, `intents/audit.csv`, `playbooks/cli.md`, and the row's core_refs.
- Does NOT load other playbooks (no api.md, errors.md, etc.).
- May load `templates/audit-report.md` for output shape.

**Verification:** monitor file reads if possible. If not automatable, treat as a manual review case — re-read the agent's session log and confirm only the expected files were read.

**Fail if:** loads unrelated playbooks "for context."

---

## Case 12: IDE Surface (new-coverage smoke test)

**Prompt:** `How can we improve the autocomplete UX for our SDK in VS Code?`

**Expected:**

- Routes to (audit, ide) or (design, ide).
- Loads `playbooks/ide.md`.
- Output cites `ide.md` heuristics (type-info shipped with SDK, hover-doc parity, etc.).

**Fail if:** routes to sdk only and ignores ide playbook.

---

## Case 13: Plugin Surface (new-coverage smoke test)

**Prompt:** `Design an extension API for our CLI so third parties can add subcommands.`

**Expected:**

- Routes to (design, plugin).
- Loads `playbooks/plugin.md`.
- Output follows design-doc template, cites plugin heuristics (named extension points, explicit lifecycle, failure isolation).

**Fail if:** routes to cli only and ignores plugin playbook.

---

## Case 14: README Surface

**Prompt:** `Our README is mostly badges and marketing copy and people ask in support what the install command is. Can you audit it?`

**Expected:**

- Routes to (audit, readme).
- Loads `playbooks/readme.md` and `references/first-impressions-checklist.md`.
- Names the Evaluator persona (not just first-time user).
- Output cites readme.md heuristics (one-line value prop, install on first screen, paste-runnable example, next-step ladder).

**Fail if:** routes to docs.md only; ignores the first-impressions checklist; treats the README as a doc-site page.

---

## Case 15: 30-Second Basics Pass

**Prompt:** `Do a 30-second basics pass on this repo — does it have a working install snippet, a LICENSE, a CHANGELOG, does --help and --version work, etc.`

**Expected:**

- Routes to (edge-pass, first-impressions).
- Loads `references/first-impressions-checklist.md` first.
- Output reports each of the 10 checklist items with yes/no and maps "no" results to findings under the relevant playbook (readme, package, cli, errors, etc.).
- "First impressions: N / 10" appears as a top-line summary.

**Fail if:** scores a per-surface 0–10 without the binary checklist; skips checklist items silently.

---

## Case 16: Package Surface

**Prompt:** `npm install our-sdk pulls in 80MB of transitive deps and our peer deps aren't declared so it silently breaks on React 17. Audit the package surface.`

**Expected:**

- Routes to (audit, package).
- Loads `playbooks/package.md`.
- Output cites package.md heuristics (declared peer deps, install-size budget, types in the box).
- Names Integrator persona.

**Fail if:** routes to setup.md or sdk.md only; ignores semver, peer-deps, and footprint heuristics.

---

## Case 17: Logging Surface

**Prompt:** `Our --verbose flag dumps JSON on top of regular output and we think it's leaking the API key. Take a look at our logging UX.`

**Expected:**

- Routes to (audit, logging) or (debug, logging).
- Loads `playbooks/logging.md`.
- Output cites logging.md heuristics (structured-when-piped vs human-when-TTY, secret redaction at every level, single verbosity dial).
- If debug intent, includes typed hypotheses ranked.

**Fail if:** routes to errors.md only; treats the leak as a one-shot error rather than a logging-path issue.

---

## Cases 18–20: AI-agent readiness, AI/Agent SDK, and stochasticity — moved

The `agent`, `ai-sdk`, and `ai-stochasticity` surfaces moved out of the `dx`
domain into the standalone **`agent-experience`** skill (ADR 0006). Prompts like
"make this repo agent-friendly", "DX checklist for our LLM client SDK", or a
"pre-launch stochasticity edge pass on our AI SDK" now route to
`agent-experience` (routes `repo-readiness` / `ai-sdk`), which hands off to
`project-agentification` for the actual repo hardening. Their behavioral cases
live in `skills/agent-experience/evals/activation-cases.md`.

---

# Negative cases — should not trigger

The skill should *not* activate (or should defer) for prompts that share
keywords with DX work but want a different competence. For each negative
case, "pass" means the skill either recognizes the mismatch and declines to
invoke, or isn't invoked at all. These cases protect against keyword-overlap
false positives.

---

## Case N1: General code style review

**Prompt:** `Review this React component for code style issues — naming, indentation, prop types.` (followed by a JSX snippet)

**Expected:**

- Skill recognizes this is general code review on internal code, not DX review.
- Either declines or asks whether the component is part of a developer-facing surface.

**Fail if:** loads a playbook and produces a DX audit on internal code style.

---

## Case N2: Marketing copy audit

**Prompt:** `Audit the copy on our marketing homepage hero section — we sell developer tools but the page targets economic buyers, not devs.`

**Expected:**

- Skill recognizes the audience isn't developers despite the keyword "audit"
  and the developer-tools product context.
- Declines or asks whether developer audience is involved.

**Fail if:** runs audit intent on marketing copy aimed at non-developers.

---

## Case N3: Concept explanation

**Prompt:** `Explain how OAuth2 PKCE flow works — I'm writing a one-pager for our security team.`

**Expected:**

- Skill recognizes this is educational content, not a DX review.
- Defers; does not load `auth.md` playbook to produce a "review."

**Fail if:** opens auth.md and produces a DX audit of a non-existent flow.

---

## Case N4: End-user product UX

**Prompt:** `Our consumer signup form has a 60% drop-off rate. Help me reduce friction.`

**Expected:**

- Skill recognizes the target audience is end-users, not developers, despite
  the "friction" keyword.
- Declines; routes or suggests `ux-accessibility-heuristics`.

**Fail if:** treats end-users as a developer persona and runs `setup` or `docs` playbook.

---

## Case N5: Internal code refactor

**Prompt:** `Refactor this function to use early returns instead of nested if statements.` (followed by a function body)

**Expected:**

- Skill recognizes this is internal refactoring, not DX surface review.
- Declines.

**Fail if:** invokes the audit intent on internal-only code.

---

## Case N6: Technology comparison

**Prompt:** `Write a decision doc comparing GraphQL vs REST for our backend team.`

**Expected:**

- Skill recognizes this is research / decision support, not surface review.
- Declines.

**Fail if:** opens api.md and produces a comparison report framed as a DX audit.

---

## Case N7: Production performance debugging

**Prompt:** `Our reporting query is slow in production at 2pm. Help me trace what's causing it.`

**Expected:**

- Skill recognizes this is operational debugging of a running system, not
  developer-perceived perf (install, cold start, build, test).
- Either declines or asks whether the goal is developer-facing perf — only
  the latter is in scope.

**Fail if:** opens perf.md and applies DX heuristics to a production query plan.

---

## Case N8: End-user accessibility

**Prompt:** `Audit our checkout page for WCAG 2.1 AA compliance.`

**Expected:**

- Skill recognizes accessibility for end-users isn't a developer surface,
  despite the "audit" keyword.
- Declines; routes or suggests `ux-accessibility-heuristics`.

**Fail if:** routes audit through any DX playbook for an end-user a11y review.

---

## Domain: docs (formerly docs-experience-heuristics)


## Positive

- "Audit our docs site across developers, end users, and coding agents." -> routes to `audit` and `foundations`, may fan out to all playbooks, emits `templates/audit-report.md`.
- "Design a docs IA with tutorials, how-tos, reference, explanation, versioning, accessibility, and feedback loops." -> routes to `design` and `foundations`, loads `references/playbooks/foundations.md`, emits `templates/design-doc.md`.
- "Our README buries install instructions and the quickstart does not reach hello world." -> routes to `audit` and `dx-docs`, loads `references/playbooks/dx-docs.md`, emits `templates/audit-report.md`.
- "Developers copy our example and it fails because imports and environment setup are missing." -> routes to `debug` and `dx-docs`, loads `references/playbooks/dx-docs.md`, emits `templates/debug-runbook.md`.
- "Users read a help article after an error and still open support tickets." -> routes to `debug` and `ux-help`, loads `references/playbooks/ux-help.md`, emits `templates/debug-runbook.md`.
- "Design in-product help for empty states, tooltips, onboarding, and user-facing error recovery." -> routes to `design` and `ux-help`, loads `references/playbooks/ux-help.md`, emits `templates/design-doc.md`.
- The agent-readable-docs (`ax-docs`) surface moved to the standalone `agent-experience` skill (ADR 0006): "Add llms.txt, markdown docs, stable anchors, and RAG-friendly summaries" and "agents under-trigger the right skill and retrieve 'see above' chunks" now route there. The `docs` domain still owns `audience-conflicts` for human-vs-agent tension.
- "Review our OpenAPI schema and MCP tool descriptions for examples, errors, constraints, and retry semantics." -> routes to `audit` and `api-contracts`, loads `references/playbooks/api-contracts.md`, emits `templates/audit-report.md`.
- "Define an eval for tool-call success from schema descriptions and stable error codes." -> routes to `measure` and `api-contracts`, loads `references/playbooks/api-contracts.md`, emits `templates/measurement-plan.md`.
- "Our tooltips are good UX but the instructions disappear for agents and screen readers." -> routes to `debug` and `audience-conflicts`, loads `references/playbooks/audience-conflicts.md`, emits `templates/debug-runbook.md`.
- "Make one source of truth render as human docs, agent markdown, and in-product help without drift." -> routes to `design` and `audience-conflicts`, loads `references/playbooks/audience-conflicts.md`, emits `templates/design-doc.md`.

## Negative

- "Audit the checkout form for keyboard traps, focus order, contrast, and ARIA labels." -> use `ux-accessibility-heuristics` instead, because this is product accessibility rather than documentation/help strategy.
- "Make this dashboard visually polished and build a Tailwind component system." -> use `ui-design-craft` instead, because visual UI creation is not a docs-experience task.
- "Review the SDK API design, naming, auth flow, and developer onboarding; docs are out of scope." -> use `dx-heuristics` instead, because the requested surface is the developer product/API, not documentation.
- "Assess this repository's AGENTS.md, hooks, sandbox, and CI for coding-agent readiness." -> use `project-agentification` instead, because repo agent-readiness and gates are the primary task.
- "Record this agent failure in a reflection log and decide whether it should become a rule." -> use `evidence-driven-agent-rules` instead, because failure-log governance is the task.
- "Investigate why p99 latency increased and whether our tracing coverage is sufficient." -> use `perf-observability-heuristics` instead, because system performance and observability are primary.
- "Review our unit, integration, and e2e tests for brittleness and false-pass risk." -> use `test-heuristics` instead, because the request is test-suite quality.
- "Research the history of documentation frameworks and give me a cited primer." -> use `topic-research` instead, because the output is an open-ended research report, not a docs-experience intervention.

## Boundary / edge

- "Make our docs better." -> activates only if the user confirms a documentation/help/agent-docs surface; otherwise ask whether they mean developer DX (`dx-heuristics`), product UX (`ux-accessibility-heuristics`), repo agent-readiness (`project-agentification`), or cross-audience docs (`docs-experience-heuristics`).
- "Improve our AGENTS.md." -> activates only when the task is about documentation strategy or always-loaded vs load-on-demand docs; otherwise prefer `project-agentification` for repo context files and enforcement.
- "Fix this error message." -> activates if the error is part of docs/help/API contract design; otherwise prefer `dx-heuristics` for developer-facing runtime errors or `ux-accessibility-heuristics` for product form recovery.

---

## Domain: perf (formerly perf-observability-heuristics)


Behavioral cases the skill is expected to handle. Each section is
machine-readable enough for future activation eval runners; today the
file is human-graded.

## Positive — should activate

- "Our p99 latency just doubled and we don't know why. Help me diagnose."
  → `diagnose/latency`. Hypothesis-ranking before naming root causes;
  measurement method must be named in the runbook output.
- "Design the SLO program for our new payments service."
  → `design/slos`. SLI selection, SLO target setting, error-budget
  policy, alerting thresholds.
- "Audit our existing observability stack for gaps before next quarter's
  reliability push." → `audit/all`. Multi-surface fan-out (one sub-agent
  per playbook), per-surface score, project-wide path-to-10.
- "Plan a tail-latency optimization pass for the checkout API."
  → `optimize/latency`. Profile-first; sequenced safe improvements with
  measured before/after gates.
- "Strategize our observability roadmap across logs, metrics, and traces."
  → `strategize/slos` (SLO program is the natural anchor; logs / metrics /
  traces fall out of "what do we need to measure to defend the SLO?").
  Program scope, adoption sequence, instrumentation budget.
- "Review our distributed tracing setup for cardinality and sampling."
  → `audit/tracing`. Three lenses against a single playbook.
- "We're seeing connection-pool exhaustion and slow queries; help us think
  through it." → `diagnose/resources` (resource-saturation framing) with
  cross-link to the DB-tier slice of `latency` and `resources`.
- "Run a USE-method pass on the API tier."
  → `audit/resources`.
- "Add error-budget alerting that doesn't page on noise."
  → `design/slos`.
- "Reduce p99 on the homepage; the median is fine."
  → `optimize/latency`. Tail-tolerant patterns.

## Negative — should NOT activate

- "Pick a good name for this React component." → naming, not perf.
- "Refactor this CRUD endpoint to use the repository pattern." →
  `clean-architecture`, not perf.
- "Review our developer onboarding docs for first-time integrator
  friction." → `dx-heuristics`.
- "Audit this test suite for false-pass risk and flakiness." →
  `test-heuristics`.
- "Design a database schema with proper normalization and foreign keys."
  → future `data-modeling-heuristics`, not perf-observability. (DB
  *performance* is in scope; schema *design* is not.)
- "Critique this user persona for evidence backing." → `persona-critique`.
- "Stress-test this PRD adversarially." → `spec-red-team`.

## Edge — boundary or ambiguous

- "Our CI build farm is saturated and the test stage runtime doubled —
  investigate the pipeline workers." → Activates at `diagnose/latency`.
  Per the README boundary, **CI / build-farm runtime is a production
  system** (owned by an infra / platform team) and stays here; developer
  inner-loop perf on a single workstation (install, cold start, own
  edit-test cycle) routes to `dx-heuristics`. The "investigate the
  pipeline workers" framing is unambiguously the production-system case.
- "First Contentful Paint regressed after the bundler upgrade; investigate
  the browser tier." → `diagnose/latency` (browser-tier slice).
- "We have RED metrics on the gateway but nothing on workers — what to
  add and why?" → `design/metrics`. The "why" framing pulls the
  three-pillars critique from the playbook's grounding.
- "Should we switch from Postgres to a columnar store for analytics?" →
  Not this skill; that's a data-modeling / architecture call. If the
  question reframes as "our OLAP queries are slow, what should we
  measure first?", then `diagnose/latency` (DB-tier slice).
- "How do we keep our observability bill from doubling?" → Could be
  `strategize` (instrumentation budget) or `audit/tracing` (sampling).
  Ask one disambiguation question.
- "Investigate this incident." → Too vague. Ask whether the user wants
  diagnosis (symptom → root cause) or an audit of why detection was slow.

---

## Domain: test (formerly test-heuristics)


These evals check activation, routing, ambiguity handling, load discipline, and
output shape for `test-heuristics`. Static structure is checked by
`evals/run-static-checks.sh`; these behavioral cases are reviewed from session
logs.

## Positive cases

### Case 1: Bare activation menu

**Prompt:** `Use test-heuristics.`

**Expected:** Loads `references/intent-router.csv`, shows the intent menu
(`triage` / `review` / `author` / `strategize` / `prune`), and waits. No file
inspection, commands, network calls, or writes.

### Case 2: Unit review

**Prompt:** `Review my unit tests for false-pass risk.`

**Expected:** Routes to `review/unit`, loads `references/layers/unit.md` plus
the row's core refs, names a target persona, scores 0-10, tags findings with
failure modes, and uses `templates/review-report.md`.

### Case 3: Flaky test triage

**Prompt:** `This e2e test keeps flaking in CI, help me triage it.`

**Expected:** Routes to `triage/e2e-ui`, ranks hypotheses before fixes, names
repro steps, likely failure modes, and prevention. Uses
`templates/triage-runbook.md`.

### Case 4: Test authoring

**Prompt:** `I'm about to write a property-based test for invoice totals; what
shape should it have?`

**Expected:** Routes to `author/property-based`, asks or infers purpose, names
generator/property/shrinking concerns, and uses `templates/author-design.md`.

### Case 5: Cross-layer strategy

**Prompt:** `What should I test at unit vs integration vs e2e for this payment
flow?`

**Expected:** Routes to `strategize/all`, performs a single integrative pass,
loads the cross-layer row's playbooks, and uses `templates/strategy-doc.md`.

### Case 6: Prune review with tracking

**Prompt:** `Review all test layers and save a ledger so we can track closeout.`

**Expected:** Routes to `review/all`, assigns stable `TEST-<layer>-NNN`
finding IDs, saves both
`test-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and
`test-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`, and reports
both paths without creating roadmaps or issues unless explicitly confirmed.

### Case 7: Snapshot review

**Prompt:** `Audit snapshot tests that keep changing after harmless CSS edits.`

**Expected:** Routes to `review/snapshot`, flags brittleness and false-pass
risk, names update discipline, and includes verification.

### Case 8: Contract test review

**Prompt:** `Improve my contract tests so provider changes stop surprising
consumers.`

**Expected:** Routes to `review/contract`, looks for versioned/brokered
contracts, provider verification, consumer relevance, and CI evidence.

### Case 9: Performance test triage

**Prompt:** `Our performance test is noisy and fails on random CI runs.`

**Expected:** Routes to `triage/performance`, ranks environment variance,
measurement setup, thresholds, and workload stability before fixes.

### Case 10: Closeout verification

**Prompt:** `Verify whether TEST-UNIT-004 is fixed using the saved
workflow-state JSON.`

**Expected:** Routes to closeout, reads saved state first, reruns the finding's
verification rule, and updates status only when evidence passes. A merged PR or
closed issue is evidence to inspect, not proof that a finding is closed.

## Negative cases

- `Review my CLI design.` -> `dx-heuristics`, not this skill.
- `Set up jest in my repo.` -> tooling/setup; closer to `dx-heuristics`.
- `Deploy this code to staging.` -> not a test-quality task.
- `Explain how to use pytest fixtures.` -> general programming education unless
  the user asks for test-quality review.
- `Audit our checkout page for WCAG.` -> `ux-accessibility-heuristics`.

## Boundary cases

- `Fix this failing test.` -> ask whether the test is wrong or the system under
  test is wrong. If unsure, default to triage.
- `Improve my tests.` -> ask which layer and improvement target: clarity,
  coverage, cost, or robustness.
- `Review my testing.` -> ask which layer; offer `all`.
- `Write a unit test for this function.` -> plain implementation unless the
  user adds a quality intent such as robust, well-designed, or review.

## Tracking and closeout cases

- A review or prune output with 7+ findings/candidates must save both
  skill-prefixed tracking artifacts, report both paths, and not merely offer
  to create them.
- Tracking artifacts use `docs/audits/` by default and
  `audit-artifacts/test-heuristics-...` when the target is not a writable repo.
- Roadmaps, GitHub issues, and non-tracking project-file edits require explicit
  user confirmation.
- Closeout resumes from the saved workflow-state JSON/ledger; a merged PR or
  closed issue is evidence to inspect, not proof that a finding is closed.

## Load discipline

For a clear `review/unit` prompt, the skill should load
`intent-router.csv`, `intents/review.csv`, `layers/unit.md`, and the
row's core refs only. It may load the review template. It should not load every
layer playbook "for context."

---

## Domain: ux (formerly ux-accessibility-heuristics)


## Positive cases

- "Use ux-accessibility-heuristics." -> bare invocation; show intent menu.
- "Our signup form has 60% drop-off." -> `form-review`; load forms + accessibility playbooks.
- "Audit our checkout page for WCAG 2.2 AA." -> `accessibility-audit`; state that this is not legal certification.
- "Users cannot find billing settings." -> `navigation-review`.
- "This failed payment message only says try again." -> `error-recovery`.

## Negative cases

- "Review my CLI help for DX." -> `dx-heuristics`.
- "Audit our SDK docs for developers." -> `dx-heuristics`.
- "Write unit tests for the signup form." -> general coding or `test-heuristics` if quality-focused.
- "Review AGENTS.md for agent readiness." -> `project-agentification`.

## Behavioral assertions

- Bare invocation loads only `references/intent-router.csv` and waits.
- Concrete invocation loads only the selected row's files.
- Accessibility output distinguishes likely WCAG failures from items needing
  manual or specialist confirmation.
- Findings include severity, impact, fix, verification, and grounding sources.
- For 7+ findings, any severity 3-4 finding, or save/track request, the skill
  saves both tracking artifacts and reports their paths.

---

## Domain: ui-craft (formerly ui-design-craft)


## Positive

- "Use ui-design-craft to make this dashboard look less generic." Activates,
  routes to `product-ui` plus `quality-review`, inspects the existing UI, and
  emits a concrete plan before edits.
- "Prototype this onboarding flow with a few tweakable variants." Activates,
  routes to `prototype`, loads host/tweak guidance, and maps variation axes.
- "Make a presentation deck from these notes." Activates, routes to `deck`,
  chooses a slide system, and asks only if audience or export target is unknown.
- "Author a small design system for this app." Activates, routes to
  `design-system`, and produces token/component/preview requirements.
- "Review this UI for AI slop." Activates, routes to `quality-review`, applies
  visual, task, and handoff lenses.
- "Add subtle animated depth to this hero." Activates, routes to
  `motion-scene`, checks reduced motion and intensity.
- "Package this prototype for handoff." Activates, routes to `host-handoff`,
  checks bundling, direct edit, export, and limitations.

## Negative

- "Run a formal WCAG audit of this checkout." Prefer
  `ux-accessibility-heuristics` unless the prompt also asks for visual redesign.
- "Review this API onboarding guide." Prefer `dx-heuristics`.
- "Refactor the repository architecture." Prefer `clean-architecture` or
  `project-agentification` depending on scope.
- "Write unit tests for this component." Prefer normal coding/test workflow,
  not this skill.

## Edge

- Bare "UI designer" invocation shows modes and intents, then waits.
- If a design system is named but unavailable, ask for it or state the
  from-scratch fallback before inventing visuals.
- If the user asks to copy a third-party product's distinctive UI without
  evidence of ownership, refuse that copy and offer an original adjacent style.
- If host protocol files are not relevant to the target environment, skip them
  and document the portability assumption.

---

## Domain: architecture (formerly clean-architecture)


Plain-English companion to `trigger-evals.json`. Each subsection
explains *why* the listed queries activate or don't, and which surface
the routing picks for edge cases.

## Should activate

These prompts should route into the skill. The category in
`trigger-evals.json` is `positive`.

- **"is my domain code leaking into infrastructure?"** — direct
  invocation of the dependency rule; route to `audit/dependency-rule`.
- **"review this module for clean architecture violations"** — names
  the skill outright; route to `audit/boundaries` by default unless
  the agent can pick a more specific surface from context.
- **"clean architecture audit all with parallel sub-agents"** —
  explicit all-surface audit plus delegation request; route to
  `audit/all` and dispatch when the host permits it.
- **"find anemic domain models in this codebase"** — the anemic-domain
  anti-pattern is the canonical `domain-model` audit signal.
- **"how should I split this monolith into services aligned to bounded
  contexts?"** — strategic split intent; route to
  `design/bounded-context`.
- **"design layer boundaries for this new payments feature"** —
  greenfield design at the boundary surface.
- **"extract a pure use case from this controller without breaking
  callers"** — refactor toward a port; `refactor/boundaries`.
- **"strangler fig refactor to extract the billing bounded context"**
  — refactor pathway named explicitly; `refactor/bounded-context`.
- **"full clean architecture audit produced 8 findings"** —
  threshold-triggered follow-through; route to `audit/tracking` and
  create a findings ledger by default.
- **"audit found a severity 3 boundary leak"** — severity-triggered
  follow-through; route to `audit/tracking` and create a findings ledger.
- **"turn these clean-architecture findings into a tracked roadmap"**
  — explicit roadmap request after audit; load
  `references/trackable-findings.md` and use the ledger as the source
  before creating roadmap artifacts.
- **"verify whether CA-DEP-003 was fixed in this PR"** — closeout pass;
  rerun the narrow verification rule for that finding ID before checking it off.
- **"why did the audit use CA-dependency-rule-001 instead of CA-DEP-001?"**
  — mechanics follow-up; load `references/audit-mechanics.md` and normalize
  future findings to canonical ID prefixes.
- **"what is the difference between an aggregate and an entity?"** —
  explain intent on a `domain-model` distinction.

## Should NOT activate

These prompts share keywords with the skill but address a different
domain. Routing into clean-architecture would waste the user's time.

- **"make my CSS architecture cleaner"** — "architecture" here means
  visual design / file-organization for CSS, not software architecture.
- **"audit my dependency versions for CVEs"** — "dependency" here
  refers to package versions (security), not source-code
  dependency direction.
- **"design a clean UI for this form"** — UX design, not software
  design.
- **"audit checkout accessibility and form usability"** — product UX and
  accessibility, not code architecture; route to
  `ux-accessibility-heuristics`.
- **"refactor this regex to be more readable"** — refactor at a scale
  below the skill's smallest unit.
- **"what is the best React component library?"** — library choice,
  not architecture.
- **"set up CI/CD for my repo"** — infrastructure/tooling, not
  software architecture.
- **"speed up my test suite"** — performance / testing, not
  architecture (route to `test-heuristics` instead).
- **"audit my docker image for vulnerabilities"** — container security,
  not architecture.
- **"close these GitHub issues because the PR merged"** — issue closure
  alone is not clean-architecture verification; requires a referenced
  finding ID or architecture audit evidence.

## Boundary cases

These prompts could plausibly route elsewhere; the routing choice and
rationale is documented here so the description-optimization loop has
a stable target.

- **"explain SOLID principles"** — *activates.* SOLID is the
  class-scale expression of the dependency rule; route to
  `explain/dependency-rule`. Rationale: every SOLID principle except
  SRP (open/closed, Liskov, interface segregation, dependency
  inversion) operationalizes a clean-architecture concern. The
  `dependency-rule.md` playbook treats SOLID explicitly.
- **"how do I structure my React components?"** — *activates.* The
  question is shape-of-code, not styling; route to
  `design/boundaries` because Flux/Elm-style unidirectional flow is
  in the playbook's grounding. Rationale: the playbook's frontend
  representatives (Flux 2014, Elm 2015) explicitly cover this. If
  the prompt instead said "what library should I use" it would NOT
  activate. If it asks whether the form is usable or accessible, route to
  `ux-accessibility-heuristics` instead.
- **"microservices vs monolith for a 5-person startup?"** —
  *activates.* The trade-off is about context boundaries and team
  size, both `bounded-context` concerns; route to
  `design/bounded-context`. Rationale: this is exactly the
  question Newman's *Building Microservices* and Khononov's
  *Learning DDD* address.
- **"should I use Repository pattern with my ORM?"** — *activates.*
  The Repository pattern is in the `cross-cutting` playbook's
  grounding (Fowler, PoEAA 2002) and the design question is about
  the boundary between domain and persistence; route to
  `design/cross-cutting` (could also defensibly go to
  `design/boundaries`; tie-break to cross-cutting because the
  question is about persistence mechanics).

## What this is not

This file is not the activation runtime — it is documentation for
contributors. The runtime activation logic lives in
`SKILL.md` plus the routing CSVs. This file explains *why* the
runtime should behave the way it does and gives the description-
optimization loop a target.

## Delegation boundary

`audit all` alone selects the all-surface fan-out route. Try sub-agent
dispatch whenever user, project, session, or host policy already permits it.
If the host requires fresh explicit opt-in and none exists, ask once before
spawning, then use sequential passes only if consent is absent or dispatch is
blocked.

## Tracking behavior

- Large audit outputs (7+ findings) and any severity 3–4 finding must create a
  Markdown findings ledger plus workflow-state JSON by default, not merely
  offer or inline tracking choices.
- The ledger and workflow-state filenames start with the skill name, for example
  `clean-architecture-findings-ledger-2026-05-19-payments.md`, so ledgers from
  different audit skills are distinguishable.
- Roadmaps and GitHub issues require explicit user request. External issues
  still require confirmation.
- A roadmap or GitHub issue groups related finding IDs into issue-sized work;
  do not produce one issue per finding unless requested.
- A finding is checked off only after the verification rule attached to that
  ID passes. `implemented` and "issue closed" are not final statuses.


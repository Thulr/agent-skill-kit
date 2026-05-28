# DX Heuristics Eval Cases

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

## Case 18: Agent-Readiness Surface

**Prompt:** `Claude Code and Cursor keep tripping on our repo — wrong test commands, blocked git pushes, autogenerated AGENTS.md content that's wrong. How do we make this agent-friendly?`

**Expected:**

- Routes to (audit, agent).
- Loads `playbooks/agent.md`.
- Output cites agent.md heuristics (hand-curated AGENTS.md, harness-mirror parity, documented hooks and gates, evidence-promoted rules).

**Fail if:** routes to contributor.md only; recommends autogenerating AGENTS.md; treats this as a general docs problem.

---

## Case 19: AI/Agent SDK Surface

**Prompt:** `We're building a TS client SDK that wraps an LLM API — streaming completions, tool calls, structured output via Zod, plus an agent loop. Before alpha, what's the DX checklist?`

**Expected:**

- Routes to (audit, ai-sdk) or (design, ai-sdk).
- Loads `playbooks/ai-sdk.md` (not `agent.md`, which is a distinct surface).
- Output cites ai-sdk.md heuristics (streaming at two altitudes, schema-typed structured output with .parse helper, validation-retry distinct from transport retry, tool schema from function signature, declarative stop conditions, hooks at decision points, tracing as default).
- May reference `sdk.md` for inherited HTTP-client patterns (jittered retries, typed exception hierarchy) but does not route there exclusively.

**Fail if:** routes to `agent.md` (the repo-readiness playbook, not the AI/Agent SDK playbook); routes to `sdk.md` only and misses the AI-specific patterns; treats streaming, structured output, and the agent loop as ordinary HTTP-client concerns.

---

## Case 20: AI/Agent Stochasticity Edge Pass

**Prompt:** `Pre-launch edge-case pass on our AI SDK — what stochasticity-related failure modes should we hunt for before alpha?`

**Expected:**

- Routes to (edge-pass, ai-stochasticity).
- Loads `playbooks/ai-sdk.md` and `playbooks/errors.md`.
- Output covers validation-retry semantics, partial-output rendering, agent-loop bounding, provider feature parity, opaque-reasoning round-trip, batch-vs-online divergence.

**Fail if:** treats this as ordinary back-compat or version-skew pass; misses validation-vs-transport retry distinction; misses opaque-reasoning round-trip.

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

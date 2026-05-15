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

- Routes to (edge-pass, cli) — may include multiple edge-pass surfaces.
- Output follows `templates/edge-checklist.md`: risk inventory across all categories with severity and verification, blockers list, re-run trigger.

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

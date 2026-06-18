# ux-audit Eval Cases

Activation + behavioral cases for `ux-audit` — critiquing an existing
end-user product UX or accessibility surface (usability / accessibility / form /
navigation / error-recovery audits). Building or visually polishing UI is
`ui-design`; developer-facing surfaces are `dx-audit`. Cases that route to
those siblings appear here as **negatives**.

## Static verification

```bash
bash skills/ux-audit/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author/title
cleanliness and word count (<800), one-layer intent-router shape (exactly the
five intents, no `intents/` surface layer), router → detail-file/template
registry integrity, playbook structure/word-count, and the tracking gates
(`ux-audit-` ledger/workflow-state prefixes).

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic UX/accessibility-critique prompts; asks at most
one blocker question when the intent or user/task is missing; does not inspect
files/networks or write from a vague invocation; routes `intent-router.csv` →
one playbook + its core refs directly (one layer, no surface CSV); names a
target user and task; and emits the `audit-report.md` shape.

---

## Case 1 — Bare activation menu
**Prompt:** `Use ux-audit.`
**Expected:** loads `intent-router.csv` and `starter-scenarios.csv`; shows the
usability / accessibility / form / navigation / error-recovery menu with named
scenarios on top; offers the mode choice; waits.
**Fail if:** inspects files, runs commands, or invents an audit.

## Case 2 — Concrete form review
**Prompt:** a 12-field signup form + "users drop off here, review the form UX."
**Expected:** routes `form-review`; loads `playbooks/forms.md` (+ accessibility
core refs); names the target user and task; findings table with severity 0–4,
fix, and verification; `audit-report.md` shape.
**Fail if:** loads unrelated playbooks; rewrites copy without severity; omits
verification.

## Case 3 — Accessibility audit with WCAG framing
**Prompt:** `Audit our checkout page for WCAG 2.2 AA — keyboard, focus, contrast, screen reader.`
**Expected:** routes `accessibility-audit`; treats WCAG as a floor; distinguishes
likely failures from items needing manual/assistive-tech confirmation; lists
verification per finding (keyboard pass, screen-reader transcript, contrast
check).
**Fail if:** claims certification; treats an automated scan as sufficient.

## Case 4 — Tracked audit artifacts
**Prompt:** `Audit the signup flow and save the findings so we can close them out later.`
**Expected:** stable `UX-FORM-NNN` / `UX-A11Y-NNN` IDs; creates both
`docs/audits/ux-audit-findings-ledger-…md` and `…workflow-state-…json` (or
the `audit-artifacts/ux-audit-…` fallback); reports both paths.
**Fail if:** only offers to track, or emits the ledger inline without saving.

## Case 5 — Closeout from saved state
**Prompt:** `Verify whether UX-FORM-003 is fixed in this PR using docs/audits/ux-audit-workflow-state-2026-05-22-signup.json.`
**Expected:** loads `trackable-findings.md` then the saved state; reruns that
finding's verification rule; updates status only if it passes.
**Fail if:** marks it closed because the PR merged; ignores saved state; invents
a new ledger.

## Case 6 — Navigation / IA review
**Prompt:** `Users can't find billing settings in our 14-item dashboard nav. Review the IA.`
**Expected:** routes `navigation-review`; loads `playbooks/navigation.md`;
reasons about findability, grouping, and page-level orientation.
**Fail if:** jumps to visual restyling instead of information architecture.

## Case 7 — Ambiguous private-system request
**Prompt:** `Review our onboarding and tell me what to fix.`
**Expected:** asks one blocker question (which intent / which user-task); does
not inspect first.

## Case 8 — Right-size to project scale (calibration)
**Prompt:** `Audit an internal admin form only our ops team uses — it's a throwaway tool for now.`
**Expected:** infers **Prototype** tier per `references/calibration.md`; narrows lenses/scope; collapses same-mechanism findings; the report names the `Project tier` and splits fixes into "Now" vs "Later — as it grows" — but any assistive-tech exclusion stays a Now finding regardless of tier.
**Fail if:** files an exhaustive equal-weight heuristic list, or defers an accessibility blocker to "Later".

---

# Negative cases — should not trigger (or should defer)

## N1 — Building / polishing UI
**Prompt:** `Redesign our dashboard visually — pick a color system, type scale, and build a component library.`
**Expected:** recognizes this is UI building/polish, not a critique; defers to
`ui-design`.
**Fail if:** produces severity findings for visuals it is being asked to author.

## N2 — Interaction prototype
**Prompt:** `Prototype a new onboarding flow in React so I can click through it.`
**Expected:** defers to `ui-design`; does not run an audit.

## N3 — Developer-facing CLI/API critique
**Prompt:** `Our CLI --help is dense; tell me what to tighten.`
**Expected:** recognizes a developer-facing surface; defers to `dx-audit`.

## N4 — Developer-facing API audit
**Prompt:** `Audit our public REST API for friction — error envelope, pagination, idempotency.`
**Expected:** defers to `dx-audit` despite the "audit" keyword.

## N5 — AI-agent surface
**Prompt:** `Claude Code keeps tripping on our repo — bad AGENTS.md, wrong test commands. Make it agent-friendly.`
**Expected:** defers to `design-for-agent-users`; does not route through a UX playbook.

## N6 — Production performance debugging
**Prompt:** `Our reporting query is slow in production at 2pm. Trace what's saturating Postgres.`
**Expected:** recognizes operational/runtime perf, not end-user UX; defers.

## N7 — Concept explanation
**Prompt:** `Explain how WCAG levels A / AA / AAA differ for a one-pager.`
**Expected:** recognizes educational content; defers.

## N8 — Internal code refactor
**Prompt:** `Refactor this React component to extract form state into a hook.`
**Expected:** recognizes internal refactoring, not surface critique; declines.

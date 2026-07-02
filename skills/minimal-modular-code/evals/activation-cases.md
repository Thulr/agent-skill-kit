# Minimal Modular Code — Activation Cases

## Positive

The skill should activate and route correctly.

- "This PR feels over-engineered — trim the slop." -> `review` / `minimalism`, loads `playbooks/minimalism.md`, emits `audit-report.md`.
- "The agent rebuilt a function we already have; audit for duplication and missed reuse." -> `review` / `minimalism`, emits `audit-report.md`.
- "I'm adding a feature — keep the change minimal and reuse what exists." -> `do` / `minimalism`, emits `change-plan.md`.
- "Help me subtract here — what can this change remove instead of add?" -> `do` / `minimalism`, emits `change-plan.md`.
- "Audit our module coupling and boundaries and score them." -> `review` / `boundaries`, emits `audit-report.md`.
- "Is this module deep or shallow? Review the seam." -> `review` / `boundaries`, emits `audit-report.md`.
- "Are these names and this control flow legible, or too clever?" -> `review` / `legibility`, emits `audit-report.md`.
- "Structure this repo so four agents can work in parallel without colliding." -> `design` / `parallel-readiness`, emits `design-doc.md`.
- "Which modules can we hand to parallel agents, and which contracts must we freeze first?" -> `design` / `parallel-readiness`, emits `design-doc.md`.
- "Design the module boundaries for this new service, kept minimal." -> `design` / `boundaries`, emits `design-doc.md`.
- "Sequence a safe, reversible refactor to invert this dependency." -> `design` / `boundaries`, emits `refactor-runbook.md`.
- "Which of our boundary rules are only in prose and should be gates?" -> `review` / `enforcement`, emits `audit-report.md`.
- "Audit the whole repo for slop and parallel-readiness across every surface." -> `review` / `all` (fan-out), emits `audit-report.md`.
- "Explain the wrong abstraction against our code." -> `design` / `minimalism` (explain mode), emits `explanation.md`.
- "Make this helper as short as possible, even if the shorter version is harder to read." -> `do` / `legibility`, rejects code golf; minimal means concise and readable, not terse.
- "Delete the guard clause and its tests so this change stays minimal." -> `do` / `minimalism`, gates deletion on understanding and preserves the safety behavior.
- "Use YAGNI to avoid the interface that keeps our domain code from importing ORM types." -> `design` / `boundaries`, distinguishes speculative ceremony from a present-need boundary investment.
- "Collapse the billing adapter, domain policy, and API handler into one file to reduce line count." -> `design` / `boundaries`, keeps independent concepts modular even if that costs an extra file.
- "Make the smallest safe change to `searchUsers` so empty queries return `[]`; do not refactor." -> `do` / `minimalism`, preserves all non-empty query semantics and rejects opportunistic rewrites.
- "Preserve domain boundaries while adding order-shipped customer notifications; email now, SMS later." -> `design` / `boundaries`, introduces a notifier boundary instead of importing a concrete email client into the service.

## Negative

Near-miss prompts that share keywords but should route elsewhere. Each names the sibling skill.

- "Set up AGENTS.md, hooks, and CI gates so Claude Code works here." -> use `harden-repo-for-coding-agents` — this skill says *what* to enforce and why, not how to wire the gates.
- "Add a pre-commit hook and a sandbox/approval policy for our agent." -> use `harden-repo-for-coding-agents` — enforcement machinery is its surface.
- "Review our public REST API's errors, pagination, and versioning." -> use `dx-audit` — developer-facing API surface, not internal code minimality.
- "Design a new SDK's client surface and retry behavior." -> use `dx-design` — developer-experience product surface.
- "Our signup form confuses users; run a usability audit." -> use `ux-audit` — end-user product UX, not code structure.
- "Build the dashboard UI and a design-token system." -> use `ui-design` — visual UI production.
- "Tighten the wording of this announcement post." -> use `writing-audit` — prose, not code.
- "Reorganize our docs site's information architecture." -> use `docs-audit` — documentation surface, not code.
- "Our test suite is flaky and redundant; review it." -> use `test-audit` — test-suite quality, not source minimality.
- "Profile and optimize this service's p99 latency." -> does not activate — runtime performance, not code structure.
- "Add keyboard shortcuts to the dashboard toolbar." -> use `ui-design` / product code directly — "shortcut" here is an interaction feature, not code minimality.

## Boundary / edge

- "Should I add an abstraction now or duplicate for the second case?" -> activates `do` / `minimalism` (Rule of Three guidance); if the user instead wants the *whole module* restructured, prefer `design` / `boundaries`.
- "This file is 800 lines — should I split it?" -> activates only if the concern is minimality/legibility/deep-modules; if the ask is really "does this violate our layering," route `review` / `boundaries`. A pure "make it read better" line-prose request is `writing-audit`, not this skill.
- "Can we skip error handling and tests because this is internal and the minimal version is smaller?" -> activates `do` / `minimalism`, but the expected behavior is to right-size the safety net, not remove load-bearing checks.
- "Compress this validation flow into a clever one-liner so the code looks minimal." -> activates `do` / `legibility`; expected behavior is to preserve visible control flow and precise names.
- "This small bug fix is an excuse to clean up the whole function, right?" -> activates `do` / `minimalism`; expected behavior is minimal diff discipline unless the cleanup is required for the fix.

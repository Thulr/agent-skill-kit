# Activation cases — agent-docs

Natural-language behavioral cases for the **agent-native documentation an AI agent reads and acts
on**. Each negative names the sibling skill it disambiguates from. The agent should activate on
realistic agent-doc prompts, ask at most one blocker question, and route to `<intent>/<surface>`
— deferring human/dual-audience docs to `docs-audit` / `docs-design`.

## Positive

### P1 — AGENTS.md audit
**Prompt:** `Audit our AGENTS.md — hand-curated? mirrors in sync? rules tied to real failures?`
**Expected:** activates; intent `review`, surface `agents-md`; checks curation, mirror parity,
the ≥3-failure provenance, and the persona/ops boundary.

### P2 — Curate llms.txt
**Prompt:** `Curate an llms.txt so an agent fetches the right pages first instead of crawling.`
**Expected:** activates; intent `do`, surface `llms-txt`; curated index + placement-by-access-pattern.

### P3 — Wrong-tool descriptions
**Prompt:** `Our agent calls the wrong tool — two MCP descriptions are nearly identical. Fix them.`
**Expected:** activates; intent `do`, surface `tool-descriptions`; disambiguates the descriptions
(the readable doc, not the typed schema — that's `agent-dx`).

### P4 — Chunk survivability
**Prompt:** `Will our reference survive retrieval? Agents pull "see above" and can't use it.`
**Expected:** activates; intent `review`, surface `machine-reference`; chunk survivability + stable
anchors.

### P5 — Context budget
**Prompt:** `Our always-loaded context file is huge — what loads up front vs retrieves on demand?`
**Expected:** activates; intent `design`, surface `context-budget`; the three tiers + everything-dump.

### P6 — Full agent-docs review (fan-out)
**Prompt:** `Full agent-docs review across AGENTS.md, llms.txt, tool descriptions, reference, budget — score each.`
**Expected:** activates; intent `review`, surface `all`; fans out with `AGENT-DOC-*` finding IDs.

## Negative

### N1 — Human docs site
**Prompt:** `Audit our human docs site and help center for confusing onboarding and bad search.`
**Expected:** does not activate; defers to `docs-audit` (human / dual-audience docs).

### N2 — Tool schema as code
**Prompt:** `Design the typed tool schema and structured-output validation for our Agent SDK.`
**Expected:** does not activate; defers to `agent-dx` (the schema as code; agent-docs owns the
description's clarity, not the typed contract).

### N3 — Scaffold + enforce repo gates
**Prompt:** `Scaffold our AGENTS.md, hooks, and CI gates and wire do-not-autogenerate enforcement.`
**Expected:** does not activate; defers to `harden-repo-for-coding-agents` (scaffolding and
enforcing; agent-docs designs the AGENTS.md *contract*).

### N4 — Operating the loop
**Prompt:** `Set up a trace-and-eval loop and watch our agent's quality drift in production.`
**Expected:** does not activate; defers to `agent-ops`.

### N5 — Promote a failure to a rule
**Prompt:** `Promote this recurring agent failure into an AGENTS.md rule from our log.`
**Expected:** does not activate; defers to `rules-from-coding-agent-failures` (agent-docs checks
that the rule's provenance link exists; it does not run the promotion loop).

### N6 — Marketing prose
**Prompt:** `Tighten the prose in our marketing landing page.`
**Expected:** does not activate; defers to `writing-audit`.

## Edge / boundary

### E1 — Dual-audience page
**Prompt:** `Our docs serve both humans and an agent — where does the agent-native part live?`
**Expected:** activates on the agent-native slice; intent `review`, surface `machine-reference`;
the dual-audience *page* stays with `docs-audit`/`docs-design`, the agent-native artifacts here.

### E2 — Invariant in prose vs gate
**Prompt:** `Should the agent's invariants live in AGENTS.md prose or a CI gate? Our markdown rule gets ignored.`
**Expected:** activates; intent `review`, surface `agents-md`; flags docs-as-reliability-fix and
routes the gate itself to `harden-repo-for-coding-agents`.

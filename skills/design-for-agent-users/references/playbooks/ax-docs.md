# Agent-Readable Documentation Playbook

## Scope

Covers documentation written for retrieval and action by coding agents, runtime
agents, and RAG systems: curated indexes, markdown renderings, context files,
load-on-demand skills, chunk-survivable pages, stable anchors, glossaries,
examples, and trigger descriptions. Use when an agent must find, choose, or act
on documentation without a human reading the page.

- In: `llms.txt`, full-doc markdown bundles, agent context files, skill
  descriptions, retrieval-friendly structure, stable deep links, glossary
  bridges, examples for agents, and always-loaded vs on-demand decisions.
- Out: repo hook/gate implementation (hand off to `harden-repo-for-coding-agents`) and
  API/tool schema fields (the `docs-audit` / `docs-design` `api-contracts` surface).
- Intents this surface answers: audit, design, debug, measure.

## Grounding

- Research Report — Effective Documentation Patterns and Practices for DX, AX,
  and UX (Informed Skills research synthesis, 2026) — synthesizes unique AX
  documentation requirements and conflicts.
- Agent Skills overview (Anthropic, 2025) — grounds progressive disclosure:
  metadata, instructions, and resources.
- Evaluating repository-level context files for coding agents (Gloaguen and
  coauthors, 2026) — warns that always-loaded context must be minimal and
  measured.
- Cloudflare documentation for AI tooling (Cloudflare, 2026) — grounds markdown
  rendering, token budgeting, and retrieval-friendly authoring.
- OpenAPI Specification 3.1.0 (OpenAPI Initiative, 2021) — reinforces schema and
  description fields as agent-facing docs.
- MCP Tool Descriptions Are Smelly! (Hasan and coauthors, 2026) — evidence for
  targeted tool descriptions and eval-based improvement.

## Good signals

- A curated agent index points to the few pages or bundles agents should fetch
  first.
- Important pages survive chunking: headings carry subjects, no "see above"
  dependency, and summaries define scope.
- Agent-loaded files are short, hand-curated, and evaluated against real tasks.
- Human docs and markdown/agent renderings derive from one source or have drift
  checks.
- Trigger descriptions include what the resource does and when to use it.

## Common failures

- Everything dump — a massive context file is always loaded because more help
  feels safer, increasing cost and distracting the model.
- Trigger invisibility — the right skill/resource exists but its description is
  too vague to activate.
- Chunk amnesia — a retrieved paragraph says "this option" or "see above" with
  no local subject, so the agent cannot use it.
- Human-only affordance — instructions live in tooltips, screenshots, UI order,
  or animation without text/schema equivalents.
- Forked-doc drift — agent docs and human docs are maintained separately with no
  shared source or comparison gate.
- Docs-as-reliability-fix — treating better docs/skills as a path to high-nines
  reliability. Curation raises *average* task success, not worst-case reliability;
  mandatory invariants belong in deterministic gates (hooks/CI), not in markdown
  the model may ignore (hand enforcement to `harden-repo-for-coding-agents`).

## Heuristics

- (audit, design) Retrieval entrypoint — provide a small curated index and, when
  useful, full markdown bundles; name what each link is for rather than dumping
  every URL. Retrieval is an agent-*controlled* tool portfolio, not one index:
  exact search, semantic search, file/shell lookup, and graph traversal each suit
  different query shapes. Low floor / high ceiling — narrow reliable tools for
  common queries, a general tool for surprises; the index is one instrument, and
  which one the agent reaches for is itself an AX lever.
- (audit, design) Load-budget split (three tiers) — always-loaded files hold
  minimal invariant rules; load-on-demand resources hold expansive expertise,
  examples, schemas, and task playbooks; durable **memory** holds what must
  survive across sessions. Context is what the model sees now; memory is what it
  retrieves later — design them as distinct tiers. More always-loaded text can
  *lower* accuracy, not only raise cost, even when it fits the window.
- (audit, debug) Trigger-description test — the description must state purpose,
  use conditions, and near-miss exclusions. If agents under-trigger, tune this
  before adding more body content.
- (audit, design) Chunk-survivability — each section should restate its subject,
  define local terms, avoid anaphora, and start with a high-signal summary.
- (design, debug) Stable-anchor contract — use durable anchors, versioned URLs,
  and canonical links so stored citations and retrieval pointers do not rot. This
  fixes *stored*-citation rot; long agent runs also lose *in-session* context to
  compaction (compaction amnesia), so the facts a later step needs should live in
  high-signal summaries or externalized state, not only mid-window prose.
- (audit, design) Glossary bridge — map user words to product terms and link to
  canonical pages; this helps semantic retrieval cross vocabulary gaps.
- (measure) AX eval loop — compare task success, retrieval hit rate, trigger
  rate, and token cost with and without each agent docs surface; hold inputs and
  evaluators fixed so each delta is attributable to the change. For
  path-correctness (an efficient route, not just the right answer) and
  failure-localization (which surface caused the miss), use trajectory and
  trace-linked evaluations — that depth is owned by `agent-evals`.
- (audit, design) Single-source preference — prefer one source rendered as human
  page, markdown, or bundle; fork only with drift checks and an owner.
- (audit, design) Placement by access pattern — put each fact where its access
  pattern wants it: retrievable docs / `llms.txt` for *reference*, a skill for
  *task guidance*, an MCP tool for a *live action*. Point to the source-of-truth
  doc; don't paste it into an always-loaded file.

## Quick diagnostic

- Does the agent know where to start without crawling the whole site? yes → test
  retrieval quality; no → add curated entrypoint.
- Is the load-bearing instruction present as text or schema? yes → inspect
  clarity; no → move it out of visual-only affordances.
- Are task failures due to no retrieval, wrong retrieval, or wrong action after
  retrieval? classify before editing.
- Does a context file grow because of repeated failures? yes → add an eval and
  consider moving content to load-on-demand resources.

## Cross-references

- `references/playbooks/audience-conflicts.md` (sibling) — resolving human/agent
  doc tension, AX-first.
- `references/core/audience-matrix.md` (sibling) — AX-only requirements and
  transfer rules.
- `docs-audit` / `docs-design` — machine-readable schemas/tool contracts
  (`api-contracts`), IA/versioning/docs-as-code gates (`foundations`), and the
  full four-audience matrix.

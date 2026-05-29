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
- Out: repo hook/gate implementation (use an agentification skill) and API/tool
  schema fields (use `api-contracts.md`).
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

## Heuristics

- (audit, design) Retrieval entrypoint — provide a small curated index and, when
  useful, full markdown bundles; name what each link is for rather than dumping
  every URL.
- (audit, design) Load-budget split — always-loaded files hold minimal invariant
  rules; load-on-demand resources hold expansive expertise, examples, schemas,
  and task playbooks.
- (audit, debug) Trigger-description test — the description must state purpose,
  use conditions, and near-miss exclusions. If agents under-trigger, tune this
  before adding more body content.
- (audit, design) Chunk-survivability — each section should restate its subject,
  define local terms, avoid anaphora, and start with a high-signal summary.
- (design, debug) Stable-anchor contract — use durable anchors, versioned URLs,
  and canonical links so stored citations and retrieval pointers do not rot.
- (audit, design) Glossary bridge — map user words to product terms and link to
  canonical pages; this helps semantic retrieval cross vocabulary gaps.
- (measure) AX eval loop — compare task success, retrieval hit rate, trigger
  rate, and token cost with and without each agent docs surface.
- (audit, design) Single-source preference — prefer one source rendered as human
  page, markdown, or bundle; fork only with drift checks and an owner.

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

- `references/docs/playbooks/api-contracts.md` — machine-readable schemas, tool
  descriptions, errors, and retries.
- `references/docs/playbooks/audience-conflicts.md` — resolving human/agent doc
  tension.
- `references/docs/playbooks/foundations.md` — IA, versioning, and docs-as-code gates.
- `references/docs/core/audience-matrix.md` — AX-only requirements and transfer rules.

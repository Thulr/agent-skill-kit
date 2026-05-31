# Foundations Playbook

## Scope

Covers the shared documentation system beneath developer docs, end-user help,
and agent-readable docs: mode separation, docs-as-code, information
architecture, style, accessibility, versioning, telemetry, and feedback loops.
Use it before specializing into a single audience.

- In: documentation taxonomy, source-of-truth decisions, IA/search, style and
  terminology consistency, public accessibility basics, versioned URLs, doc
  quality gates, and program measurement.
- Out: API/tool schema details (use `api-contracts.md`), product-flow usability
  unrelated to help (use a UX skill), and repo-level agent hardening (use the
  agentification skill).
- Intents this surface answers: audit, design, debug, measure.

## Grounding

- Research Report — Effective Documentation Patterns and Practices for DX, AX,
  and UX (Informed Skills research synthesis, 2026) — provides the cross-audience
  foundation set and conflict map.
- The Documentation System (Procida) — supplies the four-mode taxonomy and the
  anti-mixing rule.
- Docs as Code (Gentle / Write the Docs contributors) — grounds PR review, CI,
  link checks, and docs tests.
- Information Architecture: For the Web and Beyond (Rosenfeld, Morville, and
  Arango, 2015) — grounds organization, labeling, navigation, and search.
- Web Content Accessibility Guidelines 2.2 (World Wide Web Consortium, 2023) —
  sets public help and docs accessibility floors.
- Cloudflare documentation for AI tooling (Cloudflare, 2026) — adds the agent
  rendering and token-budget dimension to shared docs infrastructure.

## Good signals

- Each page has one dominant mode: learning, task completion, lookup, or
  explanation.
- Docs are version controlled, reviewed with code, and blocked by automated
  checks for links, samples, schemas, or accessibility where applicable.
- Navigation, headings, and search labels match the words audiences actually use.
- Public docs expose version, last-updated or applicability, and a feedback path.
- Quality signals produce a backlog item with an owner, not just a dashboard.

## Common failures

- Mode mixing — a getting-started page becomes tutorial, reference, FAQ, and
  concept essay, so no audience gets the page shape it needs.
- Hidden drift — product, API, examples, and docs live in separate review loops;
  nobody notices they disagree until support tickets arrive.
- Search-first neglect — headings are organized by internal component names, so
  user questions and agent retrieval queries miss the right page.
- Accessibility-as-theme — docs pages look polished but have broken heading
  order, low-contrast code blocks, hidden focus, missing captions, or vague link
  text.
- Feedback without closure — helpfulness widgets and analytics exist, but no
  triage rule turns weak signals into fixes.

## Heuristics

- (audit, design) Mode-purity pass — label each major page by its dominant job;
  split or rewrite pages that try to teach, reference, troubleshoot, and explain
  at once.
- (audit, design) Source-of-truth test — identify the canonical artifact for
  every fact class: prose page, schema, code comment, example repo, or product
  copy. If two sources can disagree, add a gate or derive one from the other.
- (audit, measure) Freshness gate — every release path that changes user-visible
  behavior should name the docs surface that must be updated or explicitly mark
  none required.
- (audit, design) Stable-entry architecture — important pages need durable URLs,
  predictable anchors, version disambiguation, and titles written in audience
  vocabulary.
- (audit, design) Accessibility floor — verify semantic headings, keyboard/focus
  behavior, contrast, transcripts/captions, descriptive alt text, and link text
  before optimizing voice or layout.
- (debug) Gap-source trace — when a support ticket, failed quickstart, or bad
  agent action appears, trace whether the failure came from absence, findability,
  ambiguity, staleness, or an audience conflict.
- (measure) Feedback loop contract — define signal, threshold, owner, action,
  and verification for each metric; avoid dashboards that cannot trigger work.

## Quick diagnostic

- Can a newcomer name the page type within ten seconds? yes → continue; no →
  run the mode-purity pass.
- Can a changed API or product string ship without touching docs checks? yes →
  add freshness gates; no → inspect gate quality.
- Do top search queries and page titles use different vocabulary? yes → add
  glossary/search synonyms; no → inspect page content.
- Are feedback signals tied to owners? yes → measure closure time; no → design
  a triage path.

## Cross-references

- `references/playbooks/dx-docs.md` — developer-facing page and example shape.
- `references/playbooks/ux-help.md` — in-product and help-center surfaces.
- the `design-for-agents` skill (ax-docs surface) — retrieval and agent-readable rendering.
- `references/playbooks/audience-conflicts.md` — when shared foundations pull in
  different directions by audience.
- `references/core/audience-matrix.md` — shared audience vocabulary.

# docs-index

## What it is

The docs-index surface covers the machine-readable layer that agents use to locate and navigate
project documentation without exhausting their token budgets: `llms.txt` (LLM-optimized index
placed at the repo root, not a robots.txt variant), `llms-full.txt` (concatenated single-file
ingestion companion), the canonical `docs/` tree (`docs/specs/`, `docs/adr/`, `docs/runbooks/`,
`docs/architecture/`), `ATTRIBUTION.md` (YAML-frontmatter block that agents parse for licensing
and attribution requirements of ingested code), and Aider-style AST repo maps generated via
Tree-sitter → dependency graph → PageRank → binary-search token budget (target 1024–2048 tokens
for a whole-repo map). When available, this surface also includes deterministic repo structure
graphs (build/test graphs and/or repo-level code graphs) exposed as machine-readable artifacts
the agent can treat as ground truth.

Together these surfaces let an agent answer "where is this?" and "what does this repo look like?"
in a single, token-efficient pass rather than an open-ended crawl.

Use `docs-experience-heuristics` instead when the target is a public docs/help
system serving developers, end users, or agents; keep this playbook focused on
repo-local navigation artifacts for coding agents.

## Why it matters for agents

- **llms.txt eliminates hallucinated endpoints.** Agents given a flat index of curated, plain-text
  documentation links produce fewer hallucinated API parameters than agents relying on pre-training
  weights for external library knowledge; `llms-full.txt` goes further by concatenating the critical
  docs into one ingestible file.
- **The `docs/` tree converts tribal knowledge into discoverable artifacts.** ADRs answer "why is
  the code this way?", runbooks give verified operational procedures, and architecture notes give
  structural invariants — the three most common agent hallucination prompts when absent.
- **AGENTS.md as a table of contents, not a duplicate.** Depth lives in `docs/`; AGENTS.md points
  to it. This is the primary mechanism for obeying the ≤200-line limit (W2) without discarding
  content.
- **AST repo maps let agents reason globally within a fixed token budget.** PageRank-weighted
  symbol graphs surface the highest-centrality files without loading every source file; the
  binary-search budget cap (1024–2048 tokens) keeps map cost predictable regardless of repo size.
- **Deterministic structure graphs shift failures away from “repo archaeology”.** When agents
  can rely on a ground-truth build/test/dependency map, they spend less time rediscovering
  structure and more time reasoning about the actual task.

## Heuristics by intent

### assess

- **H1.** Check whether `llms.txt` exists at the repo root with links to plain-text (not HTML)
  endpoints — absent or HTML-heavy entries force bloated page fetches, raising hallucination rate.
  (severity cap: 3; lens: cold-agent)
- **H2.** Verify `llms-full.txt` covers the critical docs subset, not the entire site — a file
  exceeding ~100 KB becomes a token-budget hazard rather than an ingestion aid. (severity cap: 2;
  lens: auditor)
- **H3.** Confirm `docs/` contains at least three of the four canonical subdirectories (`specs/`,
  `adr/`, `runbooks/`, `architecture/`) — absent subdirectories signal content has migrated into
  README or AGENTS.md, violating the table-of-contents discipline. (severity cap: 2; lens: maintainer)
- **H4.** Check that AGENTS.md references `docs/` subdirectories by path with a one-line summary,
  rather than inlining their content — inlining is the primary driver of AGENTS.md length
  violations and causes agents to skip the deeper artifacts. (severity cap: 3; lens: auditor)
- **H5.** Audit `ATTRIBUTION.md` for a YAML frontmatter block with at least `license`,
  `attribution`, and `reciprocity` fields — agents skip compliance checks they cannot parse
  programmatically during autonomous ingestion. (severity cap: 3; lens: adversarial)
- **H6.** Verify source files are capped below 500 lines / 2k LOC — oversized files require
  multi-call reads, breaking the single-pass assumption the repo map relies on, and are the
  leading cause of W6 token overruns during AST map construction. (severity cap: 2; lens: cold-agent)

### harden

- **H1.** Agent hallucinates external library endpoints → add `llms.txt` linking to the library's
  OpenAPI spec or plain-text reference; add `llms-full.txt` for libraries fetched most; reference
  both from AGENTS.md so agents consult them before querying training weights.
- **H2.** AGENTS.md exceeds 200 lines due to inlined documentation → extract each topic into
  `docs/specs/`, `docs/adr/`, `docs/runbooks/`, or `docs/architecture/`; replace inlined text with
  a single path pointer; AGENTS.md becomes a navigational index, not a content host (W2).
- **H3.** Agent invents architectural rationale or copies a deprecated API pattern → add an ADR at
  `docs/adr/NNNN-decision-name.md` for each constraint; annotate the AGENTS.md entry for `docs/adr/`
  with the titles of the three most consequential ADRs so they surface on cold start.
- **H4.** Repo map token cost is uncontrolled, crowding out task context → generate the map with
  Aider's Tree-sitter pipeline or an equivalent AST tool; apply binary-search token capping to
  produce a 1024–2048 token sub-graph; store it as `docs/repo-map.md` and reference it from
  AGENTS.md as the canonical structural snapshot.
- **H5.** Agent ingests third-party code without checking licensing → add `ATTRIBUTION.md` with
  YAML frontmatter; instrument a CI gate that lints the frontmatter schema so agents can parse
  `license`, `attribution`, and `reciprocity` fields programmatically during autonomous ingestion
  tasks.

### scaffold

- **Do not autogenerate `llms.txt`, `llms-full.txt`, or `ATTRIBUTION.md` from boilerplate (W9).**
  LLM-generated context files drop task success ~3% and inflate cost >20% (Mündler et al.,
  arXiv:2602.11988). Every entry in `llms.txt` must link to documentation an agent has already
  needed or that captures a project invariant; every `docs/adr/` entry must capture a real
  decision.
- **H1.** Create `llms.txt` at the repo root: project name, one-line description, then `# Section`
  headings with bulleted links to plain-text or markdown endpoints; add `llms-full.txt` only after
  identifying which docs agents re-fetch most.
- **H2.** Scaffold `docs/` with four subdirectories in one commit: `docs/specs/`, `docs/adr/`,
  `docs/runbooks/`, `docs/architecture/`; add `docs/README.md` mapping each to its Diátaxis mode
  (specs/adr → explanation, runbooks → how-to, architecture → reference).
- **H3.** Scaffold `ATTRIBUTION.md` with YAML frontmatter first: `license`, `spdx`, `attribution`,
  `reciprocity`, `source_url` fields; place it at the repo root alongside `llms.txt` so a single
  directory listing reveals both.
- **H4.** (W6 guard) Before adding any artifact to AGENTS.md, classify by load cost: always-loaded
  (pointer only), on-trigger (skill), or on-demand (`docs/` fetch). Default on-demand; escalate
  only when agents demonstrably miss the file without explicit prompting.

### diagnose

- **H1.** Agent produces wrong API parameters or invents endpoints → rank hypotheses: (1) `llms.txt`
  absent or links to HTML instead of plain-text docs — check root directory; (2) `llms-full.txt`
  too large, causing mid-context "lost in the middle" dropout of the critical API reference section
  (W6); (3) AGENTS.md does not mention `llms.txt`, so agent never discovers it cold-start.
- **H2.** Agent ignores or contradicts existing architectural decisions → rank hypotheses:
  (1) `docs/adr/` exists but AGENTS.md has no pointer — cold-start agent never discovers it;
  (2) ADR file names are cryptic portmanteaus rather than Googleable strings — agent's semantic
  search fails to surface them; (3) ADR was written but code was never updated to match — agent
  treats code as more authoritative than docs.
- **H3.** AGENTS.md length keeps creeping above 200 lines despite pruning → rank hypotheses:
  (1) runbooks and architecture notes are inlined instead of referenced by path — extract to
  `docs/`; (2) `llms-full.txt` equivalent is being embedded inline instead of linked — move to
  external file; (3) per-subsystem conventions are global — push to nested AGENTS.md files at
  module boundaries.
- **H4.** AST repo map is stale or missing high-centrality files → rank hypotheses: (1) map is
  a static checked-in file — add CI to regenerate on each merge; (2) PageRank misses new modules
  — verify Tree-sitter grammar covers new language targets; (3) token budget too low, truncating
  before high-centrality symbols — raise cap to 2048.

## Empirical warnings

- See `../empirical-warnings.md`: W2, W6

## Canonical examples

- **OpenHands/docs** — ships `AGENTS.md`, `.agents/skills`, `llms.txt`, `llms-full.txt`, and
  `docs.json` together; the canonical open-source example of the full docs-index stack
  co-located with agent instructions.
- **Aider repo map** — Tree-sitter → AST → directed dependency graph → PageRank → binary-search
  budget (1024–2048 tokens); reference implementation for token-efficient whole-repo structural
  context; 10x weight boost applied to symbols mentioned in the current prompt.
- **LangChain docs site** — publishes `llms.txt` and `llms-full.txt` as part of the documentation
  build; reference pattern for generated (not hand-maintained) doc indexes on large frameworks.
- **FastMemory taxonomy** — Component / Block / Function / Data / Access / Event clustering; Neo4j
  for real-time partial graph updates; reference for richer ontological clustering beyond PageRank.

## Sources

- "Aider Repo Map (Tree-sitter + PageRank)" — Tree-sitter AST parsing, directed dependency graph,
  PageRank centrality scoring, 10x prompt-mention weight boost, binary-search token-budget cap.
- "Repository Intelligence Graph (RIG)" — deterministic build/test/dependency structure map exposed
  as an LLM-friendly JSON view (ground-truth repo structure rather than rediscovered heuristics).
- "RepoGraph" — repository-level code graph used as navigation/retrieval structure for repo-scale
  tasks.
- "Effective Context Engineering for AI Agents" — smallest-high-signal-token principle; token
  budget as dominant scarcity (W6); always-loaded vs on-trigger vs on-demand load classification.
- "AGENTS.md" — `docs/specs/`, `docs/adr/`, `docs/runbooks/`, `docs/architecture/` as canonical
  subdirectory layout; AGENTS.md as table of contents into `docs/`, not a duplicate of it.
- "Engineering Agents — Harness Assessment" — docs-index as part of the legibility layer; maturity
  requires explicit doc structure, not implicit maintainer convention.

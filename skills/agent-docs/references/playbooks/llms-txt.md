# llms.txt and Agent Index Playbook

## Scope

The curated agent entry-point: the small, hand-named index — `llms.txt`, a
full-markdown bundle, or an equivalent table of contents — that an AI agent
fetches *first* to decide where to look next. It is agent-native because the
page exists for an agent reader, not a human browser: every link is annotated
with what it is *for*, so a context-bound agent can route before it spends
budget. This playbook covers the index itself and the placement decision behind
each entry; it does not cover the documents the index points at.

- **In:** designing/reviewing a curated agent index; naming what each
  link/bundle is for (not a URL dump); placement-by-access-pattern (index for
  reference, skill for task, tool for live action); single-source preference
  with drift checks and an owner; pointing to source-of-truth instead of pasting
  it; treating retrieval as an agent-controlled tool portfolio.
- **Out:** the always-loaded-vs-on-demand tiering of the index's own bytes
  (`context-budget`); the repo-root contract agents read first (`agents-md`);
  the wording of individual tool/skill descriptions (`tool-descriptions`); the
  machine-readable reference targets the index links to, e.g. OpenAPI/JSON
  schemas (`machine-reference`). Human-facing docs/README and dual-audience
  RAG-for-search stay in the human-docs skills.
- **Intents this surface answers:** do, review, design.

## Grounding

- An agent index is a *map*, not the territory: it names a few high-value
  destinations and says what each is for. A public convention here is
  `llms.txt` (a markdown index at the site root) and its `llms-full.txt`
  full-bundle variant; both are linked, annotated tables of contents, not dumps
  of every URL.
- Placement follows access pattern. REFERENCE the agent looks up → a
  retrievable doc or `llms.txt` entry. TASK guidance the agent should follow →
  a skill. A LIVE action against a running system → an MCP/OpenAPI tool. Put the
  pointer where the agent already reaches for that *kind* of thing.
- Point to the source-of-truth; do not paste it into an always-loaded file.
  One source rendered as human page / markdown / bundle beats forked copies.
- Retrieval is an agent-controlled tool portfolio — exact search, semantic
  search, file/shell lookup, graph traversal. The index is one instrument among
  them, useful precisely because it is small and curated; it is not a substitute
  for the agent's own search.

## Good signals

- The index is short and curated: a handful of named entries, each with a
  one-line "this is for X — fetch when Y" annotation, not an exhaustive
  sitemap.
- Each link's purpose is stated in agent-facing language: an agent can decide
  whether to fetch it without opening it first.
- Placement matches access pattern — reference lives in the index/retrievable
  docs, task guidance routes to a skill, live actions route to a tool — rather
  than everything being pasted into one page.
- Entries point to a single source-of-truth (a canonical page/markdown/bundle),
  and any fork carries a named owner plus a drift check.
- Links use stable, versioned, canonical URLs so a stored pointer or citation
  resurfaces the same content later instead of rotting.
- A full-markdown bundle (`llms-full.txt`-style) exists for the cases where one
  fetch beats many, and the index says which case is which.
- The index assumes the agent has other retrieval tools and complements them —
  it narrows the search, it does not pretend to *be* the search.
- An owner and a refresh trigger are named, so the curated set is maintained
  rather than silently going stale.

## Common failures

- **URL Dump.** The index lists every page with no annotation of what each is
  for — the agent must fetch all of them to route, defeating the point of a
  curated entry-point.
- **Paste-Into-Always-Loaded.** The source-of-truth is copied into a page the
  agent always loads, inflating context and creating a fork that drifts from the
  canonical doc.
- **Placement Mismatch.** A live action is documented as static reference, or
  task guidance is buried in a reference list, so the agent reads where it
  should act (or vice versa) and calls the wrong instrument.
- **Silent Fork.** A second rendered copy exists with no owner and no drift
  check; the two diverge and the agent trusts the stale one.
- **Anchor Rot.** Links are unversioned or non-canonical; a stored pointer or
  prior citation 404s or resurfaces changed content on the next run.
- **Index-as-Search.** The curated index is treated as the agent's only
  retrieval path, so anything not pre-listed is invisible — ignoring the
  agent's exact/semantic/file/graph tools.
- **Everything Bundle.** The full-markdown bundle is offered as the *only*
  entry, so every task pays the whole-corpus token cost even for a one-link
  lookup.
- **Orphaned Index.** No owner or refresh trigger; the curated set decays as the
  underlying docs move and nobody re-points the links.

## Heuristics

- **(do, review) Annotate every entry with its purpose.** Each link gets a
  one-line "for X, fetch when Y." If a reader can't route from the annotation
  alone, the entry is a URL dump, not an index.
- **(review, design) Place by access pattern.** Reference → retrievable
  doc/`llms.txt`; task guidance → a skill; live action → an MCP/OpenAPI tool.
  Audit each entry: does it sit where the agent reaches for that kind of work?
- **(do, design) Point, don't paste.** Link the source-of-truth; never inline a
  doc the agent would otherwise fetch on demand. Pasting forks the content and
  spends budget on bytes most tasks won't use.
- **(review, design) Prefer a single source; gate any fork.** One canonical
  render. If a second copy is genuinely needed, require a named owner and an
  automated drift check before it ships.
- **(do, review) Make links stable and versioned.** Use canonical, versioned
  URLs so stored citations and retrieval pointers survive across sessions; flag
  any unversioned or redirect-chained link as anchor-rot risk.
- **(design) Offer a bundle as an option, not the default.** Provide a
  full-markdown bundle for whole-corpus tasks, but keep the small index as the
  primary entry so a one-link lookup doesn't pay corpus-sized token cost.
- **(review) Size the index against the agent's other tools.** Confirm the index
  complements exact/semantic/file/graph retrieval rather than replacing it;
  curate down, don't try to enumerate everything.
- **(do, design) Name an owner and a refresh trigger.** Every index entry has
  someone responsible and a condition that prompts re-pointing, so curation
  doesn't decay into an orphaned, rotting map.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does every entry say what it's for and when to fetch it? | URL dump — agent must fetch all to route | Annotate each link "for X, fetch when Y" |
| Does each entry's placement match its access pattern? | Placement mismatch — agent reads where it should act | Reroute: reference→index, task→skill, live→tool |
| Do entries point to a source-of-truth instead of pasting it? | Paste-into-always-loaded; forked + budget-heavy | Replace inlined text with a canonical link |
| Are forks gated by an owner + drift check? | Silent fork drifts; agent trusts stale copy | Collapse to one source or add owner + drift check |
| Are links canonical and versioned? | Anchor rot breaks stored pointers/citations | Switch to versioned canonical URLs |
| Does the index complement the agent's other retrieval tools? | Index-as-search hides anything unlisted | Curate down; rely on exact/semantic/file/graph too |
| Is there a named owner and refresh trigger? | Orphaned index decays as docs move | Assign an owner and a re-point condition |

## Cross-references

- `agents-md` — the repo-root contract an agent reads first; the agent index is
  the *outward* map (corpus/site entry-point), `agents-md` is the *inward* one
  (this repo's layout, commands, invariants). Link them, don't merge them.
- `tool-descriptions` — when an index entry routes to a tool or skill, the entry
  annotation and the tool's own description must agree on purpose and
  use-conditions; that wording is owned there.
- `machine-reference` — the machine-readable targets (OpenAPI, JSON schema)
  an index links to for REFERENCE; this playbook decides *that* it's linked and
  what for, `machine-reference` shapes the target itself.
- `context-budget` — owns the always-loaded-vs-on-demand tiering of the index's
  own bytes; keep the curated index minimal here, defer the tiering math there.
- → `agent-dx` for the typed tool/SDK *schema* an entry may point at (the index
  owns the link and its purpose, not the schema as code).
- → `docs-design` / `docs-audit` as the human-docs owner: a dual-audience page
  the index links to is shaped there; the agent index only names and routes it.
- `references/intents/{do,review,design}.csv` row `llms-txt` — the entry points;
  finding IDs `AGENT-DOC-LLMS-NNN`.
# Machine-Readable Reference Playbook

## Scope

Machine-Readable Reference covers reference documentation structured so an AI
agent can retrieve a single chunk and use it without reading the surrounding
page. The unit of value is the retrievable chunk — a section that survives being
pulled out of context — plus the durable address that lets a stored citation or
retrieval pointer return to it later. This surface is agent-native: it exists
because agents retrieve and act on fragments, not because a human reads top to
bottom.

- In: chunk survivability (self-contained sections), the stable-anchor contract
  (durable anchors, versioned URLs, canonical links), glossary bridges that map
  user words to product terms for semantic retrieval, markdown rendering, and
  token-budget-aware authoring of reference material.
- Out: the curated retrieval index and load-budget tiering (sibling
  `context-budget`); the repo-root contract file (sibling `agents-md`); the
  site-level discovery file (sibling `llms-txt`); per-tool description copy
  (sibling `tool-descriptions`); the typed SDK/tool schema as code (`agent-dx`);
  generic human reference docs and dual-audience RAG-for-human-search
  (`docs-audit` / `docs-design`, the human-docs owner); eval loops that measure
  retrieval (`agent-test`); repo gates and hooks (`harden-repo-for-coding-agents`).
- Intents this surface answers: do (author a chunk-survivable page), review
  (judge an existing reference page against the chunk and anchor contracts),
  design (set the anchoring and glossary conventions for a doc set).

## Grounding

- Public markdown-rendering conventions (an `.md` twin of each HTML page,
  token-budget-aware) make reference pages retrievable and cheap to load; cite
  the public convention, never a private source.
- Retrieval is an agent-controlled tool portfolio — exact search, semantic
  search, file/shell lookup, graph traversal — so a chunk must be addressable and
  usable by whichever instrument the agent reaches for, not just by full-text read.
- Compaction amnesia (in-session context lost to long-run compaction) is distinct
  from stored-citation rot (a saved URL/anchor that no longer resolves); the
  anchor contract fixes the second, not the first.
- Stable, versioned, canonical addresses are the public-web convention that keeps
  cited fragments resolvable as content moves.

## Good signals

- A retrieved section names its own subject in the heading and opening line, so a
  chunk read alone is still self-explaining.
- Local terms are defined in-section; the reader does not need an earlier
  paragraph to parse this one.
- No anaphora across chunk boundaries — no "this option", "as above", "the
  previous example" pointing outside the retrieved fragment.
- Each section opens with a high-signal summary that states what the chunk
  decides or describes before the detail.
- Deep links use durable, human-meaningful anchors and versioned paths; old
  anchors redirect rather than 404.
- A glossary maps user vocabulary to product terms, so semantic search crosses the
  word gap.
- Pages have a clean markdown rendering sized for an agent's token budget.

## Common failures

- Chunk amnesia — a paragraph says "this flag" or "see above" with no local
  subject, so a retrieved fragment is unusable on its own.
- Heading-as-label — sections titled "Overview" or "Notes" that carry no subject,
  so retrieval and ranking cannot tell what the chunk is about.
- Anchor rot — links use generated hashes or position-based IDs that change on
  every edit, breaking every stored citation downstream.
- Unversioned canonical — one URL silently serves changing content, so a citation
  resolves to text that no longer matches the claim.
- Vocabulary gap — docs use only product terms, so a query in user words never
  retrieves the right chunk and no glossary bridges it.
- HTML-only reference — the page renders for humans but has no markdown twin, so
  agents pay a large token cost or parse it badly.
- Buried lede — the section's decision sits in the last sentence, so a truncated
  or summarized chunk loses the one fact the agent needed.

## Heuristics

- **(do, design) Subject-first sections.** Open each section with a high-signal
  summary line that names its subject and states the decision or fact, so a chunk
  retrieved alone is self-explaining. Heading carries the subject; "Overview" is
  not a subject.
- **(do, review) Kill cross-chunk anaphora.** Replace "this option", "see above",
  "the previous example" with the named referent. A retrieved fragment must not
  depend on text that retrieval left behind.
- **(do, design) Define local terms in place.** Each section defines the terms it
  uses or links to their canonical definition; do not assume the reader saw an
  earlier section.
- **(review, design) Stable-anchor contract.** Use durable, human-meaningful
  anchors and versioned, canonical URLs so stored citations and retrieval
  pointers do not rot. Redirect old anchors; never reuse an anchor for new
  content.
- **(do, design) Glossary bridge.** Map user words to product terms and link to
  the canonical chunk, so semantic retrieval crosses the vocabulary gap between
  how users ask and how the product names things.
- **(do, design) Markdown twin, budget-aware.** Ship a clean markdown rendering of
  each reference page, authored for an agent's token budget — point to the
  source-of-truth chunk rather than re-pasting it, and keep sections short enough
  to retrieve whole.
- **(review) Separate the two amnesias.** When a fact is lost, classify it:
  stored-citation rot (a saved anchor/URL no longer resolves — fix the anchor
  contract) versus in-session compaction amnesia (a long run dropped mid-window
  prose — push the fact into a high-signal summary or externalized state, a
  `context-budget` concern), because the fix differs.
- **(review, design) Chunk-size discipline.** Size sections to the retrieval unit:
  one decision or fact per chunk, front-loaded, so truncation or summarization
  keeps the lede instead of dropping it.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does each section name its own subject in the heading and first line? | Retrieved chunk is unidentifiable out of context | Rewrite headings and opening lines subject-first; emit AGENT-DOC-REF finding. |
| Can a single retrieved section be understood without the section before it? | Chunk amnesia — the agent acts on half a contract | Inline the referent, define local terms, kill cross-chunk anaphora. |
| Do deep links use durable, versioned, canonical anchors? | Anchor rot breaks agent citations and retrieval | Adopt the stable-anchor contract; add redirects for changed anchors. |
| Does a user-word query retrieve the right chunk? | Vocabulary mismatch returns the wrong section | Add a glossary bridge mapping user vocabulary to product terms. |
| Is there a token-budget-aware markdown twin of the reference page? | Agents burn budget parsing HTML boilerplate | Generate the markdown rendering; size sections to the retrieval unit. |
| Is a lost fact citation rot or compaction amnesia? | Classify first: fix the anchor contract, or hand the in-session loss to `context-budget`. |

## Cross-references

- `agents-md` (sibling) — the repo-root contract a chunk's invariants may live in
  when they are project rules, not reference.
- `llms-txt` (sibling) — the site-level discovery file that points at the
  reference pages this surface makes retrievable.
- `tool-descriptions` (sibling) — description copy for a tool; a chunk that
  documents an action hands the description text there.
- `context-budget` (sibling) — the curated index, three-tier load budget, and
  in-session compaction amnesia; this surface owns the chunk and its anchor, not
  the load decision.
- `agent-dx` (sibling SKILL) — owns the typed tool/SDK schema as code; this
  surface owns the clarity of the reference chunk, not the schema fields.
- `docs-audit` / `docs-design` (sibling SKILLS) — own generic human reference docs
  and dual-audience RAG-for-human-search; coordinate when a page serves both
  audiences.
- Finding IDs `AGENT-DOC-REF-NNN`.
- `references/intents/{do,review,design}.csv` row `machine-reference`.
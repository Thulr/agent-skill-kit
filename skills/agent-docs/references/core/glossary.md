# Glossary

Terms used across the agent-docs playbooks. Definitions are operational, not exhaustive.

- **Agent-docs** — documentation that exists because an AI agent reads and acts on it (no human
  reads the page): `AGENTS.md`, `llms.txt`, tool descriptions, machine-readable reference,
  context-budget tiers. The agent-actor analog of human documentation. Generic human docs stay
  in `docs-audit` / `docs-design`.
- **AGENTS.md** — a hand-curated repo-root file agents read first (project, layout, commands,
  invariants, load-bearing rules); a contract with future agents, not a code snapshot.
- **Harness mirror** — a per-harness entry point (`CLAUDE.md`, `.github/copilot-instructions.md`,
  `.cursor/rules`) that symlinks to `AGENTS.md` (one source) or is CI-checked to match it.
- **Evidence-promoted rule** — a load-bearing AGENTS.md rule that traces to ≥3 observed failures
  (a reflection-log floor), not invented from one incident or generic best practice.
- **Persona-vs-operations boundary** — operational/safety rules live in AGENTS.md or the harness,
  NOT a persona/identity file; sub-agents inherit AGENTS.md/SKILL.md but not persona files, so a
  rule in persona prose silently fails to transfer.
- **llms.txt** — a curated agent entry-point index pointing to the few pages/bundles an agent
  should fetch first.
- **Curated index** — a small, named list of agent-facing resources ("what each link is for"),
  not a dump of every URL.
- **Placement-by-access-pattern** — put a fact where its access pattern wants it: retrievable
  docs / `llms.txt` for *reference*, a skill for *task guidance*, an MCP tool for a *live action*.
- **Single-source / drift check** — one source rendered as human page, markdown, or bundle;
  fork only with a drift check and an owner.
- **Load-budget tiers** — always-loaded (minimal invariant rules), load-on-demand (expansive
  expertise/examples/schemas), and durable memory (survives across sessions).
- **Context vs memory** — context is what the model sees now; memory is what it retrieves later;
  design them as distinct tiers.
- **Everything-dump** — a massive always-loaded context file kept because "more help feels
  safer"; it raises cost and can *lower* accuracy.
- **Chunk survivability** — a section that restates its subject, defines local terms, avoids
  anaphora, and opens with a high-signal summary, so a retrieved chunk is usable alone.
- **Chunk amnesia** — a retrieved chunk that says "this option" / "see above" with no local
  subject, so the agent cannot use it.
- **Stable-anchor contract** — durable anchors, versioned URLs, and canonical links so stored
  citations and retrieval pointers do not rot.
- **Glossary bridge** — a mapping from user words to product terms, linked to canonical pages, so
  semantic retrieval crosses vocabulary gaps.
- **Trigger description** — a resource/skill/tool description stating purpose, use conditions, and
  near-miss exclusions; the lever to tune when an agent under- or mis-triggers.
- **Tool-description clarity** — readable, disambiguated tool/MCP descriptions so an agent picks
  the right tool; the *description* (a doc), distinct from the typed schema (owned by `agent-dx`).
- **Progressive disclosure** — metadata always loaded, instructions on trigger, resources on
  demand.
- **Docs-as-reliability-fix (trap)** — treating better docs as a path to worst-case reliability;
  curation raises *average* task success, but mandatory invariants belong in deterministic gates
  (hooks/CI), not markdown the model may ignore.
- **Compaction amnesia** — in-session context loss on long runs (distinct from stored-citation
  rot); facts a later step needs belong in high-signal summaries or externalized state.

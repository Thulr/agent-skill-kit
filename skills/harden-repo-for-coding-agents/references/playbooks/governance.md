# governance

## What it is

Governance is the organisational control layer that makes autonomous agent activity auditable,
attributable, and recoverable at team scale. It operates above the session layer (gates, sandbox)
and below the regulatory layer (NIST AI RMF), covering:

- **Ownership** — explicit named owners for prompts, skills, tools, evals, and policy files,
  enforced via CODEOWNERS; no artifact may be unowned.
- **Approval matrices** — action/risk classification intersecting the gates three-tier table
  (free-action / ask-first / forbidden) with organisational scope: who may approve, at what risk
  class, for which artifact type.
- **Supply-chain provenance** — SLSA L1–L4 build levels and GitHub artifact attestations for
  release artifacts; environment-scoped secrets available only after protection rules pass.
- **Audit and reflection logs** — append-only hook-override record; a separate reflection log
  for "human rejected agent recommendation" events that become eval cases.
- **Incident-disclosure path** — documented in the repo per NIST AI RMF GenAI Profile: detection,
  containment, disclosure, post-incident promotion.
- **Model routing** — Haiku for exploration, Sonnet for daily work, Opus for hard reasoning and
  security review; per-session cost tracked in the audit log.
- **Attention verification** — Green M&M Test: a hidden specific instruction buried in repo
  config, queried before complex sessions as a weak smoke-test for full-context ingestion (a
  reliable negative when it fails; only weak evidence when it passes — not proof).

## Why it matters for agents

- **AGENTS.md is an attack surface — governance enforces review.** Prompt Security demonstrated
  exfiltration via a hostile AGENTS.md. Write-protection and mandatory review are the only
  structural defenses; policy-in-prose is not. (W5)
- **Sub-agent topology requires handoff boundaries.** Governance defines the authority envelope
  (model, tools, approval class) so handoffs do not escalate privilege or drop context. (W4)
- **Provenance closes the audit gap — across three axes.** Run-level telemetry explains *why* an
  agent made a change; SLSA build provenance explains *how* the artifact was constructed; and
  authorship provenance explains *who* wrote which lines — which model/agent/session, recorded
  authored-not-guessed (e.g. line-level attribution in Git notes), so review and governance can trace
  agent-written code as it moves through commit, review, CI, and deploy. Build provenance is not
  authorship provenance; a hardened repo tracks both.
- **Reflection log turns human overrides into learning.** An uncaptured rejection repeats;
  captured, it becomes a new eval case and policy update trigger.
- **Harness accretion is debt.** Gates, hooks, and rules that outlive the model limitation they
  patched silently raise cost and friction. The harness must be *pruned* as models improve, not only
  grown — treat every gate/rule as a hypothesis with an expiry condition. Stale scaffolding is a
  named failure mode, not a maturity credit.
- **Guardrail layering, not output-only checks.** Production guardrails sit at four execution
  points — user input, tool call, tool response, and final output — plus inspection of retrieved
  context, tool/MCP metadata, and agent plans. Checking only the final output (or only the tool
  call) is a named anti-pattern: injection enters through tool responses and retrieved context, not
  just the prompt. (W5)
- **Route by judgment, not just by risk class.** A mature control layer sends *mechanical* failures
  (lint, type, broken tests) straight back to the agent and surfaces *judgment* calls — migrations,
  permission/auth changes, dependency additions, architecture shifts — to humans. Gating everything on
  human review (or nothing) is misrouted friction: reviewers burn on mechanical noise while agents make
  consequential choices unseen.

## Heuristics by intent

### assess

- **H1.** Audit whether every prompt file, skill directory, tool schema, eval dataset, and policy
  file has a named owner in `.github/CODEOWNERS` — unowned agent artifacts are W5-ungated.
  (severity cap: 4; lens: adversarial)
- **H2.** Verify the approval matrix maps action type (code, dependency, secret, schema, network
  destination) × risk class (low / medium / high / critical) to minimum reviewer count and role
  with named approvers, not implied "someone must review." (severity cap: 4; lens: auditor)
- **H3.** Check that SLSA provenance is emitted for release artifacts and that GitHub
  environment-scoped secrets are gated behind protection rules. (severity cap: 4; lens: auditor)
- **H4.** Confirm an append-only audit log captures every hook override (timestamp, actor,
  rationale) and a reflection log records rejection events with enough context to reproduce the
  decision. (severity cap: 4; lens: auditor)
- **H5.** Verify an incident-disclosure path is documented in the repo (not only in external
  policy systems); absence violates the NIST AI RMF GenAI Profile content-provenance and
  incident-disclosure requirements. (severity cap: 4; lens: adversarial)
- **H6.** Run the Green M&M Test before a complex session as a weak smoke-test (one signal, not
  proof): query the agent on the hidden config instruction. A wrong answer is a reliable negative —
  the context surface needs fixing; a correct answer is only weak evidence of full-context ingestion
  (it is a ~70% prompt probe, W3), so pair it with deterministic context checks (token-budget /
  line-count gates, retrieval assertions) rather than gating the session on the probe alone.
  (severity cap: 3; lens: cold-agent)
- **H7.** Audit for harness accretion: list gates, hooks, and AGENTS.md rules with no recent
  trigger/trace evidence. A control that never fires — or that the current model no longer needs —
  is a candidate for removal, not a maturity credit. (severity cap: 2; lens: maintainer)

### harden

- **H1.** Unowned artifacts → add CODEOWNERS for every agent-facing path (`AGENTS.md`,
  `.claude/skills/`, `agent/prompts/`, `agent/evals/`, `docs/policy/`) with two named reviewers;
  enable Kilo Code write-protection so AGENTS.md and skills are read-only without a PR.
- **H2.** Approval matrix missing → define a risk-classification table in
  `docs/policy/approval-matrix.md` keyed by action type × risk class; reference from AGENTS.md
  and the gates three-tier table; require re-approval when any row changes.
- **H3.** SLSA provenance absent → add `actions/attest-build-provenance` to the release workflow;
  scope secrets to named environments with required-reviewer gates; verify with
  `gh attestation verify` before promoting any artifact downstream.
- **H4.** Hook override unlogged → instrument every PreToolUse override as a structured event
  (tool, args, exit code, actor, timestamp, rationale) in an append-only log at `docs/audit/`.
- **H5.** Human rejection events not captured → add `docs/reflection-log/` (directory; one file
  per rejection per the reflection-log surface template) — each entry records session ID,
  agent recommendation, human decision, rationale, and proposed eval case; promote entries to
  `agent/evals/` within one sprint. **Recording bar (one entry) is lower than promotion bar
  (≥3 same-gap entries → scaffold rule)**; the README in the log directory must spell this out
  so reviewers do not self-filter entries.
- **H6.** Stale scaffolding accumulating → for each gate/hook/rule with no recent trace evidence,
  decide promote / keep / **demote**. The native-vs-prompt rule is bidirectional: promote a prose
  boundary to a hook when it starts causing costly failures, *and* demote a low-usage,
  high-maintenance native gate back to a skill/command or prose. Use cheap boundary evals to decide,
  and record each gate's expiry condition.

### scaffold

- **Do not scaffold governance from generic templates.** An empty CODEOWNERS and an unsigned
  attestation workflow are theater. Each artifact must be traceable to a named owner and risk
  class before scaffolding proceeds.
- **H1.** Start with ownership: enumerate all agent-facing files without CODEOWNERS entries;
  add in priority order (prompts, skills, evals, policy); commit before any other artifact.
- **H2.** Wire model routing before new sub-tasks: Haiku for exploration, Sonnet for daily
  implementation, Opus for security review and hard reasoning. Document in
  `docs/policy/model-routing.md`; surface cost-per-session in the audit log.
- **H3.** Embed the Green M&M instruction deep in a config file (`agent/manifest.json` or
  `docs/policy/attention-probe.md`) as a specific, counter-intuitive rule; store the probe
  query separately; run it before each complex session.
- **H4.** Scaffold the incident-disclosure runbook at `docs/runbooks/incident-response.md`:
  detection → containment → disclosure → post-incident (reflection log entry, eval promotion,
  policy update); link from AGENTS.md and the approval matrix.

### diagnose

- **H1.** Ownership gap after incident → rank: (1) CODEOWNERS missing for agent path; (2) entry
  exists but branch protection does not require it; (3) write-protection disabled without a
  logged rationale. Audit the full agent-facing file list before closing the incident.
- **H2.** Agent used Opus where Haiku was appropriate → rank: (1) routing policy undocumented —
  agents default to the most capable model; (2) policy exists but not wired into harness config
  (aspirational prose — W3); (3) cost tracking absent — no feedback signal. Fix: emit
  cost-per-session; wire routing into sub-agent `model:` fields in `.claude/agents/`.
- **H3.** Attestation fails verification → rank: (1) artifact re-packaged after attestation step;
  (2) secret not scoped to the correct environment; (3) verification digest mismatches the
  attestation subject — verify build workflow order and digest computation.
- **H4.** Reflection log empty despite errors → rank: (1) no hook emits a structured reflection
  prompt on rejection; (2) log format is unstructured — agents and reviewers skip it; (3) log
  not linked from AGENTS.md — cold-start agent never discovers it; (4) the log's README conflates
  the recording bar with the promotion bar (≥3 entries language too close to the "how to add an
  entry" instructions), causing reviewers to self-filter single observations as "not yet a
  pattern" instead of recording them.

## Empirical warnings

- **W5 (dominant)** — AGENTS.md and skill files are attack surfaces; a hostile file can instruct
  the agent to disable controls. Write-protection and mandatory CODEOWNERS review are the
  structural defenses — governance is what enforces them.
- **W4** — Sub-agent topologies require explicit handoff boundaries; governance defines the
  authority envelope (model, tool allowlist, approval class) so handoffs do not silently escalate
  privilege or drop shared context.
- **W3** — Approval matrices and routing policies that exist only in prose achieve ~70%
  compliance; wire them into harness config, CI, and hooks.

## Canonical examples

- **SLSA artifact attestations + GitHub environment-scoped secrets** — `actions/attest-build-provenance`
  emits a signed attestation per release; environment protection rules gate secret availability
  behind required reviewers; `gh attestation verify` confirms source and build integrity.
- **Kilo Code write-protection on AGENTS.md and skills** — files are read-only by default,
  requiring a protected-branch PR to modify; canonical reference for W5 enforcement at the
  harness layer rather than in policy prose.
- **The Green M&M Test (Organisational Physics / Engineering Agents)** — a specific
  counter-intuitive instruction buried in repo config; queried before complex sessions as a weak
  smoke-test: a wrong answer reliably flags a broken context surface; a correct answer is only weak
  evidence (a ~70% prompt probe), so pair it with deterministic context checks. Named for Van
  Halen's tour rider clause used to verify contract attention to detail.
- **Anthropic's internal model routing (Haiku / Sonnet / Opus)** — per-session cost surfaced in
  the audit log provides the feedback signal that drives routing discipline over time.

## Templates

Concrete starting points for `scaffold` governance artifacts. Copy from
`templates/artifacts/governance/`, fill `<placeholder>` markers:

- `CODEOWNERS` — required-reviewer lanes with resolvable-handle format (AGENTS.md Rule 4 — no
  opaque strings).
- `SECURITY.md` — incident-disclosure path with honest enforcement-state language (do not
  overstate branch protection that isn't on yet).

## Sources

- "SLSA Framework" — supply-chain provenance L1–L4; `actions/attest-build-provenance`;
  `gh attestation verify`.
- "AI Risk Management Framework (and Generative AI Profile)" — human role clarity; evidence
  for human overrides; content provenance and incident disclosure as GenAI profile requirements.
- "OWASP LLM and Agent Top 10" — AGENTS.md as injection surface (W5); privilege escalation in
  sub-agent topology; supply-chain risk in third-party MCP servers and skill files.
- "Engineering Agents — Harness Assessment" — Level 5 Sovereign Engineering: cost tracking,
  model routing, organisational governance; reflection log (Engineering Agents calls this
  `REFLECTION_LOG.md`; this playbook scaffolds it as `docs/reflection-log/` — a directory of
  per-entry files, scaled past the unbounded-table failure mode of a single file) as Level 3
  signal; Green M&M Test; write-protection on AGENTS.md and skills with mandatory review.

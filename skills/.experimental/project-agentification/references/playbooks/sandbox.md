# sandbox

## What it is

A sandbox is the execution boundary that separates model-generated code and agent shell calls from
the host system, harness credentials, and production networks. Three modes on an escalating-isolation
ladder:

- **Process sandbox** — agent runs as a subprocess; no container boundary. OpenHands labels this
  "unsafe, but fast." No meaningful host isolation; throwaway local experiments only.
- **Docker / container sandbox** — DEFAULT for development and CI. Pinned image; isolated filesystem;
  configurable network egress; reproducible image hash across machines. Aider's benchmark harness
  uses Docker because it executes LLM-written code without human review.
- **Remote sandbox** — hosted execution (E2B, cloud VMs) for high-risk or production-adjacent work.
  Strongest policy control; harness separated from compute so credentials stay out of the environment
  where model-generated code runs. More infrastructure, networking, and latency complexity.

Codex modes map to this ladder: `workspace-write` (write to workspace, network restricted) and
`--ask-for-approval` (destructive/network actions require human confirmation). Claude Code surfaces
permission modes (default, plan, auto) and sandbox env vars (`CODEX_SANDBOX_ENV_VAR`,
`CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR`) that agents must never modify — `openai/codex` AGENTS.md
encodes this as a hard rule.

The sandbox is the second-to-last line of defense (W5 — AGENTS.md is first; hard CI/hook gates are
last). Secrets must be environment-bound, never mounted in the agent's writable workspace (W10 — the
most common silent-failure mode). The sandbox image must be deterministic IaC: same digest every run
so validation is comparable across CI, laptops, and evals.

## Why it matters for agents

- **Credential exposure.** Without container isolation, model-generated code runs with harness
  credentials. OpenAI's position: separate harness from compute. (W10)
- **Reproducibility.** Flaky environments cost agents disproportionately. A pinned image eliminates
  "works on my machine" from the eval loop. (W3)
- **Network egress control.** Default-deny + a per-domain allow-list stops exfiltration and
  supply-chain pulls. A process sandbox has no egress control; a Docker sandbox can. (W10)
- **Injection blast radius.** AGENTS.md is an attack surface (W5); a malicious file can only reach
  what the sandbox allows — container boundaries limit blast radius.
- **Policy enforcement.** Prose in AGENTS.md achieves ~70% compliance (W3); sandbox policy
  achieves 100%. GitHub environment protection gates only fire when the sandbox is the compute target.

## Heuristics by intent

### assess

- **H1.** Identify the current sandbox mode (process / container / remote) and verify it matches
  the risk profile — process sandbox on a developer laptop running production-adjacent tasks is the
  most common mis-match. (severity cap: 5; lens: adversarial)
- **H2.** Verify the Docker image or remote sandbox is pinned to a digest or a deterministic tag,
  not `latest` — unpinned images produce different behavior across CI runs and make eval
  comparisons invalid. (severity cap: 4; lens: auditor)
- **H3.** Check whether secrets are mounted in or exported into the agent's writable workspace —
  W10; inject outside the model's write path. (severity cap: 5; lens: adversarial)
- **H4.** Verify network egress: default-deny outbound with a per-domain allow-list; unrestricted
  egress equals no sandbox for exfiltration. (severity cap: 5; lens: adversarial)
- **H5.** Confirm `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR` and `CODEX_SANDBOX_ENV_VAR` are
  declared read-only invariants in AGENTS.md — absence lets the agent disable its own network
  controls. (severity cap: 4; lens: cold-agent)
- **H6.** Verify sandbox Dockerfile/IaC is version-controlled and reviewed on the same path as
  application code — config outside VCS drifts silently. (severity cap: 3; lens: maintainer)

### harden

- **H1.** Process sandbox in use for non-throwaway work → migrate to Docker: pin the image to a
  content-addressed digest; configure `--network=none` or an allow-list bridge; bind-mount source
  tree read-only; write outputs to a separate ephemeral volume.
- **H2.** Secrets mounted in writable workspace → use GitHub environment protection rules with
  required-reviewer gates; inject via harness env-var pass-through at container start; never bake
  into the image or mount as a file inside the agent's working directory.
- **H3.** Network egress unrestricted → configure default-deny iptables or Docker network policy;
  build a per-domain allow-list (package registries, CI APIs, external services); log blocked
  outbound attempts for audit.
- **H4.** Codex `--ask-for-approval` not set → add `approval_policy: on-failure` (or stricter);
  use `workspace-write` for dev, remote sandbox for production-adjacent runs.
- **H5.** Claude Code permission mode too permissive → use `plan` mode for multi-file mutations;
  add a `PreToolUse` hook (exit-code 2) blocking `rm -rf`, force-push, and prod-DB writes; do not
  rely on AGENTS.md prose for any destructive action.

### scaffold

- **Do not autogenerate Dockerfile or sandbox IaC from templates.** `FROM ubuntu:latest` with no
  egress rules and no secret-scoping plan ships the W10 failure mode directly. Each config must
  address a named threat.
- **H1.** (W1 guard) Before writing sandbox config, name the threat it mitigates (credential
  exfiltration / network exfiltration / environment drift / host isolation) in a top comment.
- **H2.** Scaffold in three ordered layers: (1) image pinning (content-addressed digest);
  (2) filesystem isolation (read-only source mount, ephemeral output volume); (3) network policy
  (default-deny + allow-list). Do not ship layer 3 as a TODO — it is the last structural defense.
- **H3.** Wire secret injection at harness bootstrap via `--env-file` or orchestrator secret
  references; never bake into the image; validate at container start that no secrets appear in
  the agent's working directory.
- **H4.** Add a sandbox smoke-test to CI: verify egress to a non-listed domain is blocked, the
  source tree is read-only, and secrets are not accessible at the workspace path.

### diagnose

- **H1.** Agent exfiltrates credentials or makes unexpected outbound calls → rank: (1) process
  sandbox — no boundary; (2) egress unrestricted — allow-list missing; (3) secrets in writable
  workspace — agent read them before exfiltrating (W10).
- **H2.** Eval results differ across runs or machines → rank: (1) image unpinned — `latest` tag;
  (2) sandbox IaC not version-controlled — config drifted; (3) volume mounts include host-local
  state — side effects persisted.
- **H3.** Agent disables its own sandbox controls → rank: (1) `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR`
  not declared invariant in AGENTS.md; (2) PreToolUse hook absent — no hard gate; (3)
  `--ask-for-approval` not set — model executed network calls without confirmation.
- **H4.** Secrets leak into logs or traces → rank: (1) secret injected as build arg — baked into
  image layer history; (2) env var printed by agent debug output — add `ANTHROPIC_REDACT_SECRETS=1`
  or equivalent; (3) approval log captures the full env — audit trace retention and redaction.

## Empirical warnings

- **W10** — Secrets in the agent's writable workspace can be read, logged, or exfiltrated without
  triggering any guardrail. Always inject environment-side, outside the model's write path.
- **W5** — AGENTS.md and skill files are attack surfaces; a hostile file that passes code review
  can instruct the agent to disable controls. The sandbox is the structural backstop.
- **W3** — Container policy, egress rules, and harness hooks enforce bounds; AGENTS.md prose
  achieves ~70% compliance — never substitute prose for a structural constraint on a high-risk action.

## Canonical examples

- **OpenHands sandbox docs** — canonical "unsafe, but fast" label for process sandboxes; explicit
  Docker recommendation for host isolation; reference framing for the three-mode ladder.
- **E2B (sandboxed execution environments)** — hosted sandbox-as-a-service used in the PIV loop's
  Implement phase; demonstrates remote sandbox for production-adjacent agent work.
- **Codex `--ask-for-approval` + `workspace-write` mode** — `workspace-write` restricts writes to
  workspace with network disabled; `--ask-for-approval` gates destructive/network actions on human
  confirmation; `openai/codex` AGENTS.md bans modification of `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR`.
- **Aider's Docker-by-default benchmark harness** — executes LLM-written code inside Docker without
  human review; pins repo git hash, model, edit format, and settings for reproducible eval runs.

## Sources

- "OWASP LLM and Agent Top 10" — prompt injection, tool abuse, privilege escalation, and data
  exfiltration as the primary threat model; sandbox isolation and network egress as baseline controls.
- "AI Risk Management Framework (and Generative AI Profile)" — deterministic environment
  configuration for eval comparability; harness separation as a risk management posture.
- "Harness Engineering: Leveraging Codex in an Agent-First World" — harness-from-compute separation
  as OpenAI's explicit position; `workspace-write` and `--ask-for-approval` policy modes.
- "Model Context Protocol" — MCP tools as the typed action surface sandbox policy governs;
  harness-level approval for tool invocations; secret scoping at the environment boundary.

# Change Plan — <what agent-facing surface you are changing>

**Target persona:** <from references/core/personas.md> (usually Persona A)
**Surfaces in scope:** <sdk-design | tools-and-mcp | structured-output | errors-and-retry | sdk-telemetry>
**Date:** <YYYY-MM-DD>

A pre-flight plan for keeping an in-progress agent-facing change minimal and correct. Fill it
before writing much code; it is a thinking tool, not a deliverable to track.

## What already exists

<What you searched for and found before writing — the SDK helper, tool, error type, or span
convention you will reuse instead of rebuilding. If you genuinely found nothing reusable, say
so and how you checked. The HTTP-client floor belongs to dx-audit / dx-design; reuse it.>

## The minimal change

- **Reuse:** <existing SDK/tool/schema/convention this change builds on>
- **Add:** <the smallest new agent-facing code the present requirement forces>
- **Remove:** <what this change lets you delete — answer even if "nothing", to force the
  subtractive option to surface>

## Agent-consumability check

- **Contract:** <is the schema derived from code? is output typed? is the error envelope
  stable?>
- **Recovery:** <can a stochastic consumer recover — stop+verify, retry-shaped errors, typed
  refusal?>
- **Trust:** <untrusted tool metadata, credentials, raw content in spans — what leg of the
  trifecta does this change open or close?>

## Seams I am deliberately NOT adding

<The abstractions, extension points, or provider shims you considered and are leaving out
because no present need forces them (YAGNI). Naming them documents the restraint.>

## Blast radius

<Which callers/agents and contracts this change touches. If it touches a public schema or
error `code`, note that it is a coordinate-or-version change, not a free one.>

## Routing

- **Mechanical** (format, types, lint, tests): handled by <gate / will run locally>.
- **Judgment call to flag to a human:** <auth/credential change, new tool source, breaking
  contract change, or "none">.

## Grounding sources applied

- <skill.json inspired_by entry> — <how it shaped this plan>

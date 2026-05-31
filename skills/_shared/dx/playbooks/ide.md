# IDE Playbook

## Scope

IDE and editor integration for SDKs and APIs: autocomplete, hover docs,
jump-to-definition, inline diagnostics, refactoring support, and snippet
packs. The editor is part of the SDK surface — what ships in the package
shapes what users see as they type. Routes to `sdk.md` for the SDK being
surfaced in the editor, and to `docs.md` for hover-doc and reference-doc
parity.

## Grounding

- **Language Server Protocol (LSP) specification** — defines a uniform
  contract between editors and language tooling; speak the protocol and
  every modern editor gets autocomplete, diagnostics, hover, and
  jump-to-definition for free.
- **Andrew Hunt & David Thomas — *The Pragmatic Programmer*** — power
  editing and tool fluency; the editor environment is a first-class
  productivity surface, not an afterthought; knowing your tools deeply
  compounds over time.
- **VS Code Extension API documentation / IntelliJ Platform Plugin SDK** —
  concrete extension patterns for autocomplete providers, hover doc
  handlers, inline diagnostics, and snippet contributions.

## Good signals

- The SDK ships language-native type stubs (`.d.ts`, `.pyi`, etc.) with
  every release so the language server layer picks them up automatically.
- Hover docs match the published reference documentation — no drift between
  what appears on-screen and what appears in the docs site.
- Autocomplete is accurate and deprecated methods are visibly flagged (or
  hidden with an opt-in to show) rather than appearing equal to current API.
- Inline diagnostics fire at edit time for common mistakes — missing
  required fields, wrong types, invalid combinations — not only at
  compile or run time.
- Jump-to-definition resolves to readable source (or routes through source
  maps), not stripped declaration files.
- When cross-file analysis is valuable, the SDK ships or hooks into a
  language server so every editor that understands the protocol benefits.
- Snippet packs reflect the current API and are exercised in CI so they
  cannot silently fall behind.

## Common failures

- The SDK has rich runtime types but no static type stubs; autocomplete
  shows nothing or falls back to `any` / `object`.
- Hover docs are stale or missing entirely; users alt-tab to the docs site
  to find the same information.
- Autocomplete still surfaces deprecated or removed methods with no visual
  distinction from current ones.
- No inline diagnostics for the most common integration mistakes; errors
  only surface when the code runs.
- Jump-to-definition opens generated declaration files with no source map;
  users see stripped output instead of readable implementation.
- Snippet packs exist but were last updated for a prior major version; they
  generate code that no longer compiles.
- The language server integration targets a single editor; users on other
  editors receive none of the IDE benefits.

## Heuristics

- **Type info shipped with SDK** *(design, audit)* — every SDK release
  includes language-native type stubs published inside the package; no
  separate install step required.
- **Hover-doc parity** *(audit, design)* — hover content is generated from
  the same source as the reference documentation; a single authoring pass
  updates both surfaces.
- **Deprecation-aware autocomplete** *(design, audit)* — deprecated entries
  are annotated or hidden; they never appear identical to current API entries
  and never disappear silently.
- **Edit-time diagnostics** *(design, audit)* — common errors (missing
  required field, type mismatch, invalid enum) surface as the developer
  types, not when they run the program.
- **Source-mapped jump-to-def** *(design, audit)* — jumping into the SDK
  lands on commented, readable source code; where the build strips source,
  source maps are included.
- **Editor-agnostic language server** *(design)* — when cross-file analysis
  is needed, implement via the language-server protocol so every conforming
  editor benefits rather than writing per-editor plugins.
- **Tested snippet packs** *(audit, design)* — snippets are compiled and
  exercised in CI against the current API; a failing snippet blocks release.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does the SDK ship type stubs? | Autocomplete empty or `any` | Generate and publish stubs with the package |
| Do hover docs match reference docs? | Drift confuses users | Generate hover content from reference source |
| Are deprecated methods flagged in autocomplete? | Users invoke removed code | Annotate deprecations in type stubs and docs |
| Are edit-time diagnostics present? | Errors surface at runtime only | Add static analysis hooks or language server rules |
| Does jump-to-def land on readable source? | Stripped output, no context | Add source maps or include source in the package |
| Are snippets tested against the current API? | Snippets silently rot | CI-validate snippets on each release |

## Cross-references

- → `sdk.md` for the SDK surface that gets exposed in the editor.
- → `docs.md` for hover-doc and reference-doc parity.

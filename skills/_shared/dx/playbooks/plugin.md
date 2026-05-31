# Plugin Playbook

## Scope

Hook points, plugin APIs, and extension contracts: naming extension points,
defining plugin lifecycle (init, activate, deactivate, dispose), plugin
discovery and registration, failure isolation, and testability seams. Routes to
`api.md` for the underlying host contract, `migration.md` for plugin contract
versioning, and `errors.md` for plugin-failure copy.

## Grounding

- **Daniel Jackson — *The Essence of Software*** — software is composed of
  concepts, each with its own lifecycle and invariants. Extensions have their
  own concept lifecycle and must not violate the host's concept model; a plugin
  that reaches into host internals breaks the concept boundary and makes both
  sides fragile.
- **Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides — *Design
  Patterns*** — composite, observer, and strategy patterns applied to
  extension-point contracts: composite lets the host treat a collection of
  plugins uniformly; observer decouples the host from plugin subscribers;
  strategy allows callers to swap behavior without modifying the host.
- **Microsoft — VS Code Extension API documentation** — concrete patterns for
  extensible host design: declarative contribution points, activation events,
  explicit lifecycle hooks, and manifest-driven discovery. Extensions declare
  what they contribute; the host decides when and whether to activate them.

## Good signals

- Extension points are named and documented; they are deliberate contracts, not
  whatever the host happens to expose internally.
- Plugin lifecycle is explicit: clearly named phases (init, activate,
  deactivate, dispose or equivalents) are defined, and teardown is required,
  not optional.
- Plugin failures are isolated — a crash or thrown exception in one plugin does
  not take down the host or other plugins.
- Plugin discovery is manifest-driven: plugins declare what they contribute in
  package metadata; activation is predictable, not determined by file-system
  scanning with surprising side effects.
- A "hello world" plugin is a single file with no build step; the smallest
  useful plugin has zero ceremony.
- Plugins are testable in isolation: the host context can be stubbed so plugin
  tests run without installing into a live host.
- The plugin contract is versioned; the host can read the declared contract
  version and refuse to load incompatible plugins with a clear message.
- The extension API surface is small and stable; advanced or experimental hooks
  are visibly marked as unstable.

## Common failures

- Extension API = whatever the host exposes; no named contract, no documented
  surface, no boundary between stable and internal.
- A plugin crash takes down the host: no failure boundary, no sandboxing,
  errors propagate unchecked.
- No way to test a plugin without installing it into a running host; tests are
  slow, fragile, and environment-dependent.
- Plugin lifecycle is implicit: no dispose or deactivate phase, teardown is
  never called, and resources (timers, listeners, file handles) are leaked.
- No manifest; plugins are discovered by file scan and activated by side effects,
  with unpredictable ordering and surprising behavior.
- Hello-world plugin needs five files and a build step; friction blocks the
  first attempt entirely.
- Plugin contract is unversioned; the host loads whatever it finds and crashes
  when the contract doesn't match.
- Advanced hooks are not marked as unstable; users depend on them, and the host
  can never change them.

## Heuristics

- **Named extension points** *(design, audit)* — every concept the host allows
  plugins to extend has a documented name and contract; "whatever is accessible"
  is not an extension point.
- **Explicit lifecycle** *(design)* — lifecycle phases are named and documented;
  teardown (deactivate, dispose) is a required phase, not a convention. A plugin
  that cannot be cleanly removed is a liability.
- **Failure isolation** *(design, audit)* — each plugin runs behind a failure
  boundary; an uncaught error or crash is contained, logged, and reported
  without affecting the host or sibling plugins.
- **Manifest-driven discovery** *(design, audit)* — plugins declare their
  contributions in a manifest; the host reads declarations and activates
  explicitly. File-scan activation is a last resort, not a default.
- **Hello-world is one file** *(design, audit)* — the minimal useful plugin is
  a single file with no build step. If the first attempt requires scaffolding,
  the entry cost is too high.
- **Testable in isolation** *(design)* — the host context exposes a stub or
  test double as part of its public API; plugin authors write unit tests without
  a live host.
- **Versioned plugin contract** *(design, audit, debug)* — the host advertises
  a contract version; plugins declare the version they target; mismatches are
  refused with an actionable message, not a cryptic crash.
- **Stable / unstable surface split** *(design)* — stable extension APIs and
  unstable or experimental hooks are clearly distinguished in documentation and
  ideally in naming; users know what they can depend on.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are extension points named and documented? | Plugins depend on internals | Document the contract; name each extension point |
| Is the plugin lifecycle explicit (init / activate / dispose)? | Teardown leaks resources | Name lifecycle phases; require a dispose implementation |
| Are plugin failures isolated from the host? | Host crashes on plugin error | Add a failure boundary around each plugin call |
| Is plugin discovery manifest-driven? | Surprise activation order | Move to declared manifests; remove file-scan activation |
| Is hello-world a single file with no build step? | Friction blocks first try | Simplify the minimal plugin template |
| Is the plugin contract versioned? | Incompatible plugins crash the host | Add contract versioning; refuse and report mismatches |

## Cross-references

- → `api.md` for the underlying host contract and extension surface.
- → `migration.md` for plugin contract versioning and incompatibility handling.
- → `errors.md` for plugin-failure copy and isolation error messages.

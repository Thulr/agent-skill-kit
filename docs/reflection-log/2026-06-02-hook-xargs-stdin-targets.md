---
date: 2026-06-02
harness: other
sub-surface: gates
status: resolved
severity: 3
related: ["2026-06-02-hook-wrapper-bypasses.md", "2026-06-02-hook-watch-command-string.md", "2026-06-02-hook-find-option-bypass.md"]
---
# `<producer> | xargs rm -rf` fed protected delete targets in over a pipe

## What happened

Codex PR review (P1, PR #42): treating `xargs` as a transparent wrapper only
inspects its literal initial args, so the destructive target arriving on stdin
from a *different* pipeline segment was invisible:

```
check_command("echo /etc | xargs rm -rf")               -> None  (ALLOW — rm -rf /etc)
check_command("printf '%s' /etc | xargs -I{} rm -rf {}") -> None  (ALLOW)
```

The hook parses each pipe segment's argv independently, so the `/etc` produced by
`echo` never reaches the `xargs rm` segment's check. This is a real boundary: an
argv-level gate cannot trace arbitrary stdin dataflow.

## What to do differently

Decision (hook owner, PR #42): producer-tracing with **no false positives**
rather than a blanket block. `check_xargs_stdin` runs as a cross-segment pass:
for each `<producer> | xargs <deleter>` where the `|` is a real pipe, it resolves
the upstream segment *only* when it is a literal producer — `echo` / `printf`
args, or a `find <root>` whose root is the destructive surface — and feeds those
paths into the existing `check_rm` / `check_simple_deleter` logic (honoring the
`-I`/`-i` replstr). It never traces across `;` / `&&` (which do not feed stdin),
and never blocks an opaque producer.

**Documented residual gap:** opaque producers — `cat file | xargs rm -rf`,
`$(...) | xargs rm`, any command whose output isn't statically known — are NOT
covered, by design (covering them requires over-blocking common, safe idioms
like `find /safe | xargs rm`). CI branch protection + human review remain the
backstop for those forms. General lesson: when a tool consumes stdin, model the
*producer* side too, but bound the heuristic to producers you can resolve
literally so the gate never fires on a safe command.

## Closed by

This change set: `scripts/hooks/destructive_bash_policy.py`
(`check_xargs_stdin` + `_split_pipeline_with_seps` + `_xargs_deleter_invocation`
+ `_literal_producer_paths` + `_find_roots` extraction; `check_command` wiring)
and the xargs-stdin fixtures in `.claude` / `.codex` / `.cursor`
`test_block_destructive_bash.py`. (Commit SHA on commit.)

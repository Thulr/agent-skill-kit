# First-impressions checklist

A 30-second binary pass an evaluator could run before deciding whether to
adopt a tool. Every item is a yes/no signal observable in under 30 seconds of
looking at the repo, registry page, or first-run output. Apply this as the
opening of any `audit` or `edge-pass` regardless of the deeper surface, so the
basics are not hidden behind a 7/10 score.

## How to use

- Run through the list before scoring; record `yes`, `no`, or `n/a` per item.
- Each "no" maps to a finding tagged with the relevant playbook below; use
  the playbook's severity rubric to set finding severity, with the severity
  floor in the table as a minimum.
- Skip items that genuinely do not apply (e.g. no `--help` for a pure SDK
  with no CLI surface). Mark them `n/a` and document the reason; do not
  silently drop the item.

### Scoring rule

- Let **A** = number of applicable items (10 minus the count of `n/a`).
- Let **P** = number of items that returned "yes".
- Let **F** = number of items that returned "no" (so `A = P + F`).
- **Score is reported as `P / A`**, with `(K skipped)` appended when K > 0.
  Example: `8 / 9 (1 skipped)`. Never normalize to a 0–10 number; keep the
  denominator visible so the reader knows how much of the checklist applied.
- **Score cap**: if `F > 2`, the surface's per-surface score (the 0–10 in
  the audit-report `## Score` section) is capped at 7. The cap floats with
  the applicable denominator: `6 / 9` with 3 fails still triggers it; a
  fully skipped checklist (`A = 0`) cannot trigger the cap at all.
- **All-skipped case**: when `A = 0`, omit the First impressions section
  entirely. This is the only legitimate way to skip the section in single-
  surface audits.

## The 10 items

| # | Check | If "no" → finding under | Severity floor |
| --- | --- | --- | --- |
| 1 | Does `README.md` exist with a one-line value prop in the first paragraph? | `readme.md` | 3 |
| 2 | Is the install command visible without scrolling past the README header? | `readme.md` | 3 |
| 3 | Does the first code example in the README paste-and-run with one substitution? | `readme.md` + `examples.md` | 3 |
| 4 | Does `--help` (CLI) or the SDK's primary import surface produce useful output on first call? | `cli.md` / `sdk.md` | 3 |
| 5 | Does `--version` (CLI) or the package's exported version field return a real version string? | `cli.md` / `package.md` | 2 |
| 6 | Is there a `LICENSE` file at the repo root? | `package.md` | 2 |
| 7 | Is there a `CHANGELOG.md` (or equivalent release notes) at the repo root with an entry for the latest version? | `changelog.md` | 2 |
| 8 | Can a fresh-machine install complete with a single command, ending in a verifiable success signal? | `setup.md` | 4 |
| 9 | Does an error from the first reasonable wrong input name the cause and the fix? | `errors.md` | 3 |
| 10 | Is there a path from the README to deeper docs, examples, and `CONTRIBUTING.md`? | `readme.md` + `docs.md` + `contributor.md` | 2 |

## Reporting

When applied as part of an `audit` or `edge-pass`, surface the result as a
"First impressions" row at the top of the report, before the per-surface
score. Format:

```
First impressions: 7 / 10
  Failed: 2 (install not on first screen), 5 (--version returns "dev"),
          7 (no CHANGELOG.md).
```

This sits alongside, not inside, the per-surface score so the obvious-thing
gaps stay visible even when the deeper surface scores well.

## Why a checklist

Per-surface scoring with rich heuristics tends to focus on the deepest layer
the auditor knows well. A flat 30-second checklist catches the basics that
every developer notices in the first minute — install command, working
example, version disclosure, license, changelog — independent of any one
playbook's depth. The checklist is intentionally short, binary, and
scoped to the most universally applicable signals; longer or fuzzier lists
defeat the purpose.

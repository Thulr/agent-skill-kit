#!/usr/bin/env bash
#
# Validate routing CSVs are well-formed across all three install lanes.
#
# A "routing CSV" is any `*-router.csv` (intent-router, surface-router,
# domain-router, frame-router) or any file under an `intents/` directory.
# These drive the progressive-disclosure router: a ragged row (more or fewer
# fields than the header) silently truncates or misroutes a surface.
#
# Enforced invariants (per routing CSV), ignoring blank lines and leading
# `#` comment lines (used by e.g. test-heuristics' prune.csv to record what a
# route deliberately omits):
#   1. Non-empty, with a header line of >= 2 columns.
#   2. Every data row has exactly as many fields as the header (no ragged
#      rows). Quoted commas are handled via the csv module.
#
# The column vocabulary for each router shape is documented (as convention,
# not a hard gate — the catalog uses two legitimate intent-router shapes) in
# `skills/_shared/routing-contract.md`.
#
# Coverage: enumerates skills/*, skills/.experimental/*, and .agents/skills/*
# (all three install lanes per AGENTS.md Rule 1). Run by `just check` and CI.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

validate_csv() {
  python3 - "$1" <<'PY'
import csv, sys

path = sys.argv[1]
with open(path, newline="") as fh:
    rows = []
    for r in csv.reader(fh):
        if not r or not any(c.strip() for c in r):
            continue                      # blank line
        if r[0].lstrip().startswith("#"):
            continue                      # comment line
        rows.append(r)

if not rows:
    print(f"FAIL: {path}: no header row (only blank/comment lines)")
    sys.exit(1)

header = rows[0]
n = len(header)
if n < 2:
    print(f"FAIL: {path}: header has fewer than 2 columns: {header}")
    sys.exit(1)

for i, r in enumerate(rows[1:], start=2):
    if len(r) != n:
        print(f"FAIL: {path}: data row {i} has {len(r)} fields, header has {n}: {r}")
        sys.exit(1)

sys.exit(0)
PY
}

# Drop git-ignored paths: a contributor's local skill clutter (e.g. a `bmad*`
# pack dropped under `.agents/skills/`, excluded by .gitignore) is not a release
# artifact and must not gate `just check`. Mirrors check-release-contract.py's
# `_git_ignored` filter. CI runs on a clean checkout, so this is a no-op there.
filter_unignored() {
  local all ignored
  all="$(cat)"
  [[ -z "$all" ]] && return 0
  ignored="$(printf '%s\n' "$all" | git check-ignore --stdin 2>/dev/null || true)"
  if [[ -z "$ignored" ]]; then
    printf '%s\n' "$all"
  else
    printf '%s\n' "$all" | grep -vxF -f <(printf '%s\n' "$ignored")
  fi
}

failed=0
checked=0

while IFS= read -r csv; do
  [[ -n "$csv" ]] || continue
  if validate_csv "$csv"; then
    echo "OK:   $csv"
    checked=$((checked + 1))
  else
    failed=1
  fi
done < <(
  {
    find skills -type d -name _shared -prune -o -type f \
      \( -name '*-router.csv' -o -path '*/intents/*.csv' \) -print
    [[ -d .agents/skills ]] && find .agents/skills -type f \
      \( -name '*-router.csv' -o -path '*/intents/*.csv' \) -print
  } | sort -u | filter_unignored
)

if [[ $checked -eq 0 ]]; then
  echo "OK:   no routing CSVs found to check"
fi

if [[ $failed -ne 0 ]]; then
  echo
  echo "Routing-CSV checks FAILED."
  exit 1
fi

echo "All routing-CSV checks passed ($checked CSV(s) verified)."

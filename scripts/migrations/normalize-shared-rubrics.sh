#!/usr/bin/env bash
#
# Normalization (ADR 0008 follow-up): severity-rubric.md and score-rubric.md
# are per-domain SHARED substrate (not critique-local), and trackable-findings.md
# is the catalog-wide shared singleton. Any skill — critique OR design — whose
# intent CSVs reference one symlinks it from the single source; no duplication,
# no drift. Design intents (optimize, refactor, strategize, measure) legitimately
# rate risk by severity, so design skills that reference a rubric ship it too.
#
# Idempotent. Run from repo root.

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; cd "$ROOT"

link_rel() {  # link_rel <target-under-repo> <link-path>
  local target=$1 link=$2 linkdir rel
  linkdir=$(dirname "$link"); mkdir -p "$linkdir"
  rel=$(python3 -c "import os,sys;print(os.path.relpath(sys.argv[1],sys.argv[2]))" "$ROOT/$target" "$linkdir")
  rm -f "$link"; ln -s "$rel" "$link"
}
referenced() {  # referenced <skill> <token> : does any intent CSV name this core_ref?
  grep -rqlF "$2" "skills/$1/references/intents/" 2>/dev/null
}

for D in dx docs perf test architecture; do
  SH="skills/_shared/$D/core"; mkdir -p "$SH"
  CRIT="$D-critique"; DES="$D-design"

  for r in severity-rubric.md score-rubric.md; do
    # establish canonical content in _shared/<D>/core/ (from any current regular copy)
    if [[ ! -f "$SH/$r" ]]; then
      for cand in "skills/$CRIT/references/core/$r" "skills/$DES/references/core/$r"; do
        if [[ -f "$cand" && ! -L "$cand" ]]; then mv "$cand" "$SH/$r"; break; fi
      done
    fi
    [[ -f "$SH/$r" ]] || continue

    # critique: always references severity/score -> symlink
    if referenced "$CRIT" "references/core/$r"; then
      link_rel "skills/_shared/$D/core/$r" "skills/$CRIT/references/core/$r"
    fi
    # design: symlink only if its intent CSVs reference it; else drop any stray copy
    if referenced "$DES" "references/core/$r"; then
      link_rel "skills/_shared/$D/core/$r" "skills/$DES/references/core/$r"
    else
      rm -f "skills/$DES/references/core/$r"
    fi
  done

  # trackable-findings.md (catalog-wide singleton) for design skills that track
  if referenced "$DES" "references/trackable-findings.md"; then
    link_rel "skills/_shared/trackable-findings.md" "skills/$DES/references/trackable-findings.md"
  else
    [[ -e "skills/$DES/references/trackable-findings.md" || -L "skills/$DES/references/trackable-findings.md" ]] \
      && rm -f "skills/$DES/references/trackable-findings.md"
  fi
done

echo "normalized: severity/score rubrics shared per-domain; trackable-findings shared; stray design copies removed"

#!/usr/bin/env bash
#
# One-time migration (ADR 0008 / docs/specs/2026-05-30-domain-function-split/):
# split one mixed domain of review-heuristics into a <domain>-critique and a
# <domain>-design skill, single-sourcing domain-shared substrate in
# skills/_shared/<domain>/.
#
# Mechanical only: creates dirs, copies + path-rewrites shared/local content,
# wires symlinks, splits routing CSVs by intent. SKILL.md, skill.json, and
# evals/ are authored separately per skill.
#
# Shared vs local:
#   SHARED (-> _shared/<domain>/, symlinked into BOTH skills, structure
#   preserved): everything under references/<domain>/ EXCEPT the local set.
#   subagent-dispatch.md is shared but symlinked into the CRITIQUE side only
#   (it is critique-shaped: cites the severity rubric + audit CSVs).
#   LOCAL: intent-router.csv, intents/, starter-scenarios.csv, modes.md
#   (symlink), trackable-findings.md (symlink), core/severity-rubric.md,
#   core/score-rubric.md.
#
# Usage:
#   split-domain.sh DOMAIN CRIT_INTENTS DES_INTENTS CRIT_TEMPLATES DES_TEMPLATES
# comma-separated lists. Re-runnable: removes targets + _shared/<domain> first.

set -euo pipefail

DOMAIN=$1
IFS=',' read -ra CRIT_INTENTS <<< "$2"
IFS=',' read -ra DES_INTENTS  <<< "$3"
IFS=',' read -ra CRIT_TEMPLATES <<< "$4"
IFS=',' read -ra DES_TEMPLATES  <<< "$5"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

SRC="skills/review-heuristics"
SRC_REF="$SRC/references/$DOMAIN"
SRC_TPL="$SRC/templates/$DOMAIN"
SHARED="skills/_shared/$DOMAIN"
CRIT="skills/${DOMAIN}-critique"
DES="skills/${DOMAIN}-design"

rewrite() { sed -i '' -e "s#references/$DOMAIN/#references/#g" -e "s#templates/$DOMAIN/#templates/#g" "$@"; }

link_rel() {  # link_rel <target-under-repo> <link-path>
  local target=$1 link=$2 linkdir rel
  linkdir=$(dirname "$link"); mkdir -p "$linkdir"
  rel=$(python3 -c "import os,sys;print(os.path.relpath(sys.argv[1],sys.argv[2]))" "$ROOT/$target" "$linkdir")
  ln -s "$rel" "$link"
}

echo ">>> $DOMAIN: reset targets"
rm -rf "$SHARED" "$CRIT" "$DES"

# ---- 1. shared substrate -> _shared/<domain>/ (copy tree, prune local set) --
echo ">>> $DOMAIN: _shared/$DOMAIN"
cp -R "$SRC_REF" "$SHARED"
rm -f  "$SHARED/intent-router.csv" "$SHARED/starter-scenarios.csv" \
       "$SHARED/modes.md" "$SHARED/trackable-findings.md" \
       "$SHARED/core/severity-rubric.md" "$SHARED/core/score-rubric.md"
rm -rf "$SHARED/intents"
# drop any stray copied symlinks (modes/trackable were symlinks upstream)
find "$SHARED" -type l -delete
find "$SHARED" -type f \( -name '*.md' -o -name '*.csv' \) -print0 \
  | xargs -0 -r -I{} sed -i '' -e "s#references/$DOMAIN/#references/#g" -e "s#templates/$DOMAIN/#templates/#g" {}

# ---- build one side ---------------------------------------------------------
build_side() {
  local skill=$1 role=$2; shift 2
  local -a intents=("$@")
  mkdir -p "$skill/references/intents" "$skill/templates" "$skill/evals"

  head -1 "$SRC_REF/intent-router.csv" > "$skill/references/intent-router.csv"
  for i in "${intents[@]}"; do grep -E "^$i," "$SRC_REF/intent-router.csv" >> "$skill/references/intent-router.csv" || true; done
  rewrite "$skill/references/intent-router.csv"

  for i in "${intents[@]}"; do
    [[ -f "$SRC_REF/intents/$i.csv" ]] || continue
    cp "$SRC_REF/intents/$i.csv" "$skill/references/intents/$i.csv"; rewrite "$skill/references/intents/$i.csv"
  done

  if [[ -f "$SRC_REF/starter-scenarios.csv" ]]; then
    local pat; pat=$(IFS=','; echo "${intents[*]}")
    python3 - "$SRC_REF/starter-scenarios.csv" "$skill/references/starter-scenarios.csv" "$pat" <<'PY'
import csv, sys
src, dst, pats = sys.argv[1], sys.argv[2], set(sys.argv[3].split(','))
rows = list(csv.reader(open(src, newline='')))
header, data = rows[0], rows[1:]
idx = header.index('intent') if 'intent' in header else 2
keep = [r for r in data if len(r) > idx and r[idx] in pats]
w = csv.writer(open(dst, 'w', newline='')); w.writerow(header); w.writerows(keep)
PY
    rewrite "$skill/references/starter-scenarios.csv"
  fi

  # mirror the shared tree as relative symlinks (preserve subdirs).
  # subagent-dispatch.md -> critique only.
  while IFS= read -r f; do
    local rel=${f#"$SHARED"/}
    [[ "$rel" == "subagent-dispatch.md" && "$role" != "critique" ]] && continue
    link_rel "$f" "$skill/references/$rel"
  done < <(find "$SHARED" -type f)

  link_rel "skills/_shared/modes.md" "$skill/references/modes.md"
}

# ---- 2. critique ------------------------------------------------------------
echo ">>> $DOMAIN: ${DOMAIN}-critique"
build_side "$CRIT" critique "${CRIT_INTENTS[@]}"
for r in severity-rubric.md score-rubric.md; do
  [[ -f "$SRC_REF/core/$r" ]] && { mkdir -p "$CRIT/references/core"; cp "$SRC_REF/core/$r" "$CRIT/references/core/$r"; rewrite "$CRIT/references/core/$r"; }
done
[[ -e "$SRC_REF/trackable-findings.md" ]] && link_rel "skills/_shared/trackable-findings.md" "$CRIT/references/trackable-findings.md"
for t in "${CRIT_TEMPLATES[@]}"; do
  [[ -f "$SRC_TPL/$t" ]] || continue
  cp "$SRC_TPL/$t" "$CRIT/templates/$t"; rewrite "$CRIT/templates/$t"
  sed -i '' -e "s#review-heuristics-#${DOMAIN}-critique-#g" "$CRIT/templates/$t"
done
# shared tracking-artifact singletons (present only for domains that track)
for ta in findings-ledger.md workflow-state.json roadmap.md github-issue.md; do
  [[ -e "$SRC_TPL/$ta" ]] && link_rel "skills/_shared/templates/$ta" "$CRIT/templates/$ta"
done

# ---- 3. design --------------------------------------------------------------
echo ">>> $DOMAIN: ${DOMAIN}-design"
build_side "$DES" design "${DES_INTENTS[@]}"
for t in "${DES_TEMPLATES[@]}"; do
  [[ -f "$SRC_TPL/$t" ]] || continue
  cp "$SRC_TPL/$t" "$DES/templates/$t"; rewrite "$DES/templates/$t"
done

echo ">>> $DOMAIN: done (author SKILL.md / skill.json / evals next)"

#!/usr/bin/env bash
set -euo pipefail

skill_dir="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
activity_router="$skill_dir/references/activity-router.csv"
layer_dir="$skill_dir/references/layers"

failures=0

fail() {
  printf 'FAIL %s\n' "$1" >&2
  failures=$((failures + 1))
}

check_file() {
  [[ -f "$1" ]] || fail "missing file: $1"
}

check_pattern() {
  local label="$1" pattern="$2" path="$3"
  grep -Eq -- "$pattern" "$path" || fail "$label: pattern not found in $path"
}

# ----- File presence -----

check_file "$skill_md"
check_file "$skill_json"
check_file "$activity_router"
for a in triage review author strategize prune; do
  check_file "$skill_dir/references/activities/$a.csv"
done
check_file "$skill_dir/references/core/failure-modes.md"
check_file "$skill_dir/references/core/oracles.md"
check_file "$skill_dir/references/core/severity-rubric.md"
check_file "$skill_dir/references/core/score-rubric.md"
check_file "$skill_dir/references/core/personas.md"
check_file "$skill_dir/references/subagent-dispatch.md"
check_file "$skill_dir/templates/triage-runbook.md"
check_file "$skill_dir/templates/review-report.md"
check_file "$skill_dir/templates/review-report-multi.md"
check_file "$skill_dir/templates/author-design.md"
check_file "$skill_dir/templates/strategy-doc.md"
check_file "$skill_dir/templates/prune-plan.md"

# ----- Discover layer playbooks (source of truth) -----

all_layers=""
if [[ -d "$layer_dir" ]]; then
  for pb in "$layer_dir"/*.md; do
    [[ -f "$pb" ]] || continue
    all_layers+="$(basename "$pb" .md) "
  done
fi

valid_layers=" "
for s in $all_layers; do
  valid_layers+="$s "
done

# Derive activity markers from router
valid_markers=" all "
if [[ -f "$activity_router" ]]; then
  while IFS=, read -r activity _; do
    [[ "$activity" == "activity" ]] && continue
    [[ -z "$activity" ]] && continue
    valid_markers+="${activity}-activity "
  done < "$activity_router"
fi

# ----- skill.json gates -----

if [[ -f "$skill_json" ]]; then
  jq . "$skill_json" > /dev/null 2>&1 || fail "skill.json: invalid JSON"
  name=$(jq -r '.name' "$skill_json")
  [[ "$name" == "test-heuristics" ]] || fail "skill.json: name must be test-heuristics, got $name"
  status=$(jq -r '.status' "$skill_json")
  case "$status" in
    draft|reviewed|published) ;;
    *) fail "skill.json: status must be draft/reviewed/published, got $status" ;;
  esac
  count=$(jq '.inspired_by | length' "$skill_json")
  (( count > 0 )) || fail "skill.json: inspired_by must be non-empty"
  missing=$(jq -r '.inspired_by | map(select(.name == null or .author == null or .kind == null or .contribution == null)) | length' "$skill_json")
  (( missing == 0 )) || fail "skill.json: $missing inspired_by entry/entries missing required fields"
fi

# ----- SKILL.md cleanliness (source-safety) -----

author_stoplist=" Foundation Council Parliament Committee Group Working contributors "

if [[ -f "$skill_md" ]] && [[ -f "$skill_json" ]]; then
  while IFS= read -r author; do
    [[ -n "$author" ]] || continue
    last="${author##* }"
    if [[ "$author_stoplist" == *" $last "* ]] || [[ "$author" == "$last" ]]; then
      if grep -qF -- "$author" "$skill_md"; then
        fail "SKILL.md leaks source author: $author (from inspired_by)"
      fi
    else
      if grep -qw -- "$last" "$skill_md"; then
        fail "SKILL.md leaks source author last name: $last (from inspired_by)"
      fi
    fi
  done < <(jq -r '.inspired_by[].author' "$skill_json")
  while IFS= read -r title; do
    [[ -n "$title" ]] || continue
    if grep -qF -- "$title" "$skill_md"; then
      fail "SKILL.md leaks source title: $title (from inspired_by)"
    fi
  done < <(jq -r '.inspired_by[].name' "$skill_json")
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800 (runtime-only bound)"
fi

# ----- SKILL.md structural gates -----

if [[ -f "$skill_md" ]]; then
  check_pattern 'frontmatter name' '^name:[[:space:]]*test-heuristics$' "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'activity-router routing' 'activity-router\.csv' "$skill_md"
  check_pattern 'bare activation' 'show the activity menu' "$skill_md"
  check_pattern 'subagent dispatch section' '^## Subagent dispatch' "$skill_md"
  check_pattern 'three lenses' 'three lenses' "$skill_md"
fi

# ----- Activity router structure -----

if [[ -f "$activity_router" ]]; then
  rows=$(grep -cE '^(triage|review|author|strategize|prune),' "$activity_router")
  (( rows == 5 )) || fail "activity-router.csv: expected 5 data rows, got $rows"
  for a in triage review author strategize prune; do
    check_pattern "$a activity" "^$a," "$activity_router"
  done
fi

# ----- Layer playbook structure gates -----

if [[ -z "$all_layers" ]]; then
  fail "no layer playbooks found in $layer_dir"
fi

required_failure_modes="false-pass brittleness flakiness gap cost confusion"
seen_modes=" "

for layer in $all_layers; do
  pb="$layer_dir/$layer.md"
  for section in '^## Scope' '^## Grounding' '^## Good signals' \
                 '^## Common failures' '^## Heuristics' \
                 '^## Quick diagnostic' '^## Cross-references'; do
    grep -Eq -- "$section" "$pb" || fail "$layer.md missing section ${section#^## }"
  done
  awk '
    /^## Heuristics/{f=1;next}
    /^## /{f=0}
    f && /\((triage|review|author|strategize|prune)/{found=1}
    END{ if(!found) exit 1 }
  ' "$pb" || fail "$layer.md: # Heuristics has no activity tags like (triage), (review), (author), (strategize), or (prune)"

  grep -qF 'failure-modes.md' "$pb" || fail "$layer.md must reference failure-modes.md"
  for m in $required_failure_modes; do
    if grep -qE "\\($m\\)|\\(.*\\b$m\\b" "$pb"; then
      case "$seen_modes" in
        *" $m "*) ;;
        *) seen_modes+="$m " ;;
      esac
    fi
  done

  wc=$(wc -w < "$pb")
  if (( wc < 400 || wc > 1500 )); then
    fail "$layer.md word count $wc outside 400-1500"
  fi
done

for m in $required_failure_modes; do
  case "$seen_modes" in
    *" $m "*) ;;
    *) fail "no layer playbook tags any heuristic with failure-mode: $m" ;;
  esac
done

# ----- Registry integrity (CSV → file) -----

for activity in triage review author strategize prune; do
  csv="$skill_dir/references/activities/$activity.csv"
  [[ -f "$csv" ]] || { fail "missing activity CSV: $csv"; continue; }
  while IFS='|' read -r pb refs; do
    IFS=';' read -ra parts <<< "$pb"
    for p in "${parts[@]}"; do
      [[ -z "$p" || "$p" == "none" ]] && continue
      full="$skill_dir/$p"
      [[ -f "$full" ]] || fail "$activity.csv references missing layer playbook: $p"
    done
    IFS=';' read -ra rparts <<< "$refs"
    for r in "${rparts[@]}"; do
      [[ -z "$r" ]] && continue
      full="$skill_dir/$r"
      [[ -f "$full" ]] || fail "$activity.csv references missing core_ref: $r"
    done
  done < <(python3 - "$csv" <<'PYEOF'
import csv, sys
with open(sys.argv[1], newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pb = row.get('playbook', '').strip()
        refs = row.get('core_refs', '').strip()
        print(f"{pb}|{refs}")
PYEOF
)
done

# ----- Orphan-playbook check (file → CSV) -----

for layer in $all_layers; do
  pb_path="references/layers/${layer}.md"
  ref_count=0
  for activity in triage review author strategize prune; do
    csv="$skill_dir/references/activities/$activity.csv"
    [[ -f "$csv" ]] || continue
    if grep -qF -- "$pb_path" "$csv"; then
      ref_count=$((ref_count + 1))
    fi
  done
  (( ref_count > 0 )) || fail "layer playbook $layer.md is not referenced by any activity CSV (orphan)"
done

# ----- Activation-cases unambiguous-section gate -----
# Items inside "should NOT activate" sections must not contain "may activate"
# or "could activate" hedges (those belong in the boundary/ambiguous section).
# Symmetric check on positive sections for "may NOT activate".

activation_md="$skill_dir/evals/activation-cases.md"
if [[ -f "$activation_md" ]]; then
  awk '
    BEGIN { section = "" }
    /^## .*NOT activate/ { section = "negative"; next }
    /^## .*should activate/ { section = "positive"; next }
    /^## .*[Bb]oundary/ { section = "boundary"; next }
    /^## / { section = "other"; next }
    section == "negative" && /may activate|could activate|might activate/ {
      printf "FAIL activation-cases.md line %d: \"may/could/might activate\" inside NOT-activate section — move to boundary or rewrite as non-activating\n", NR > "/dev/stderr"
      bad = 1
    }
    section == "positive" && /may not activate|could fail to|might not activate/ {
      printf "FAIL activation-cases.md line %d: \"may not activate\" inside should-activate section — move to boundary or rewrite as activating\n", NR > "/dev/stderr"
      bad = 1
    }
    END { exit bad }
  ' "$activation_md" || failures=$((failures + 1))
fi

# ----- Description-claims-to-registry coverage -----
# If SKILL.md description (frontmatter) names a layer by its basename, the layer
# must be routable from at least one activity CSV. Catches the class of bug
# where the description advertises a layer/surface that has no routable path.

if [[ -f "$skill_md" ]] && [[ -n "$all_layers" ]]; then
  description_line=$(awk '/^description:/{print; exit}' "$skill_md")
  for layer in $all_layers; do
    if printf '%s' "$description_line" | grep -qiwE -- "$layer"; then
      # layer mentioned in description — ensure it's referenced by at least one
      # activity CSV (the orphan check covers presence, but only after the file
      # exists; this gate ensures the description's claim is honored)
      pb_path="references/layers/${layer}.md"
      hit=0
      for activity in triage review author strategize prune; do
        csv="$skill_dir/references/activities/$activity.csv"
        [[ -f "$csv" ]] || continue
        grep -qF -- "$pb_path" "$csv" && { hit=1; break; }
      done
      (( hit == 1 )) || fail "SKILL.md description names layer '$layer' but no activity CSV routes to it"
    fi
  done
fi

# ----- skill.json playbooks-field gate -----

if [[ -f "$skill_json" ]]; then
  while IFS= read -r p; do
    if [[ "$valid_layers" == *" $p "* ]] || [[ "$valid_markers" == *" $p "* ]]; then
      continue
    fi
    fail "skill.json inspired_by.playbooks has unknown value: $p"
  done < <(jq -r '.inspired_by[].playbooks[]' "$skill_json")
fi

# ----- Result -----

if (( failures > 0 )); then
  printf '\ntest-heuristics static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'test-heuristics static eval passed.\n'

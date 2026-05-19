#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir" rev-parse --show-toplevel)"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
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
check_file "$skill_dir/references/trackable-findings.md"
check_file "$skill_dir/templates/triage-runbook.md"
check_file "$skill_dir/templates/review-report.md"
check_file "$skill_dir/templates/review-report-multi.md"
check_file "$skill_dir/templates/author-design.md"
check_file "$skill_dir/templates/strategy-doc.md"
check_file "$skill_dir/templates/prune-plan.md"
check_file "$skill_dir/templates/findings-ledger.md"
check_file "$skill_dir/templates/workflow-state.json"

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
# Shape is enforced by the canonical schema (schemas/skill.schema.json +
# scripts/validate-against-schema.py). Per-skill assertions stay here.

if [[ -f "$skill_json" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/skill.schema.json" "$skill_json" \
    || fail "skill.json: schema validation failed (schemas/skill.schema.json)"
  name=$(jq -r '.name' "$skill_json")
  [[ "$name" == "test-heuristics" ]] || fail "skill.json: name must be test-heuristics, got $name"
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
  check_pattern 'trackable findings reference' 'trackable-findings\.md' "$skill_md"
fi

# ----- Tracking behavior gates -----

check_pattern 'test creates tracking state by default' 'Create tracking state' "$skill_md"
check_pattern 'ledger filename has skill prefix' 'test-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>\.md' "$skill_md"
check_pattern 'workflow-state filename has skill prefix' 'test-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>\.json' "$skill_md"
check_pattern 'tracking fallback path is preserved' 'audit-artifacts/test-heuristics-' "$skill_md"
check_pattern 'roadmaps and issues are opt-in' 'Roadmaps, issues' "$skill_md"
check_pattern 'review report has findings ledger section' '^## Findings ledger' "$skill_dir/templates/review-report.md"
check_pattern 'multi review report has findings ledger section' '^## Findings ledger' "$skill_dir/templates/review-report-multi.md"
check_pattern 'prune plan has findings ledger section' '^## Findings ledger' "$skill_dir/templates/prune-plan.md"
check_pattern 'review report forbids mere offer' 'offer tracking' "$skill_dir/templates/review-report.md"
check_pattern 'review report preserves fallback path' 'audit-artifacts/test-heuristics-' "$skill_dir/templates/review-report.md"
check_pattern 'ledger template has skill field' '^\*\*Skill:\*\*' "$skill_dir/templates/findings-ledger.md"
check_pattern 'ledger template has skill-prefixed markdown path' '<skill-name>-findings-ledger-<YYYY-MM-DD>-<scope-slug>\.md' "$skill_dir/templates/findings-ledger.md"
check_pattern 'workflow-state template has state_file' '"state_file": "docs/audits/<skill-name>-workflow-state-<YYYY-MM-DD>-<scope-slug>\.json"' "$skill_dir/templates/workflow-state.json"
check_pattern 'review CSV loads tracking reference' 'references/trackable-findings\.md' "$skill_dir/references/activities/review.csv"
check_pattern 'prune CSV loads tracking reference' 'references/trackable-findings\.md' "$skill_dir/references/activities/prune.csv"

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
  # Mode detection: only count a mode as "seen" when it appears as a
  # comma-separated token inside an italic-parenthesized tag group
  # (*(mode, ...)*) within the ## Heuristics section. Avoids false matches
  # on prose parens elsewhere in the playbook.
  for m in $required_failure_modes; do
    if awk -v mode="$m" '
      /^## Heuristics/ { f = 1; next }
      /^## / { f = 0 }
      f {
        line = $0
        while (match(line, /\*\([^)]*\)\*/)) {
          group = substr(line, RSTART, RLENGTH)
          inner = substr(group, 3, RLENGTH - 4)
          n = split(inner, parts, /,[ \t]*/)
          for (i = 1; i <= n; i++) {
            gsub(/^[ \t]+|[ \t]+$/, "", parts[i])
            if (parts[i] == mode) { found = 1; exit }
          }
          line = substr(line, RSTART + RLENGTH)
        }
      }
      END { exit (found ? 0 : 1) }
    ' "$pb"; then
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
    lines = [ln for ln in f if not ln.lstrip().startswith('#')]
    reader = csv.DictReader(lines)
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

# ----- Template Layer-enum drift gate -----
# Templates may enumerate layer choices in a `**Layer:** [a | b | c]` line.
# If the enum is exhaustive (no `…`/`...` ellipsis), it must equal the layer
# set in the corresponding activity's CSV. Templates with ellipsis are
# treated as abbreviated and skipped (the writer signals non-exhaustive).
# Activity is resolved via activity-router.csv's default_template column.

if [[ -f "$activity_router" ]]; then
  # Build a template -> activity map from the router.
  while IFS=, read -r activity _name _when _registry tpl; do
    [[ "$activity" == "activity" ]] && continue
    [[ -z "$activity" || -z "$tpl" ]] && continue
    tpl_path="$skill_dir/$tpl"
    [[ -f "$tpl_path" ]] || continue
    enum_line=$(grep -m1 -E '^\*\*Layer:\*\*[[:space:]]*\[' "$tpl_path" || true)
    [[ -z "$enum_line" ]] && continue
    # Skip if the enum is abbreviated (contains ellipsis).
    case "$enum_line" in
      *…*|*"..."*) continue ;;
    esac
    # Extract the bracket content, split on `|`.
    enum=$(printf '%s' "$enum_line" | sed -E 's/.*\[([^]]+)\].*/\1/')
    enum_set=""
    IFS='|' read -ra parts <<< "$enum"
    for p in "${parts[@]}"; do
      v=$(printf '%s' "$p" | tr -d '[:space:]')
      [[ -n "$v" ]] && enum_set+="$v "
    done
    # Layer set from the activity CSV.
    csv="$skill_dir/references/activities/$activity.csv"
    [[ -f "$csv" ]] || continue
    csv_layers=$(awk -F, 'NR>1 && !/^#/ && NF>0 {print $1}' "$csv" | tr '\n' ' ')
    # Compare both directions.
    for v in $enum_set; do
      case " $csv_layers " in
        *" $v "*) ;;
        *) fail "$(basename "$tpl_path") Layer enum lists '$v' but $activity.csv has no row for it (drift; add to CSV or use '…' to mark non-exhaustive)" ;;
      esac
    done
    for v in $csv_layers; do
      [[ "$v" == "all" ]] && continue
      case " $enum_set " in
        *" $v "*) ;;
        *) fail "$(basename "$tpl_path") Layer enum is exhaustive but missing '$v' which appears in $activity.csv (add to enum or use '…' to mark non-exhaustive)" ;;
      esac
    done
  done < "$activity_router"
fi

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

# ----- Description verb-x-layer cross-product coverage -----
# The SKILL.md description names verbs (reviewing / designing / triaging /
# rationalizing) and layers (unit / integration / ... / mutation / performance).
# A reader infers the cross-product: every named verb works for every named
# layer. This gate enforces that: for each (verb-synonym, layer) pair where
# both appear in description, the activity the verb maps to must include the
# layer in its CSV.
#
# Verb-to-activity map below is the single source of truth for this skill's
# vocabulary. Add a synonym here when the description gains a new framing.

verb_activity_map=$(cat <<'EOF'
reviewing review
review review
auditing review
designing author
authoring author
triaging triage
debugging triage
strategizing strategize
strategize strategize
rationalizing strategize
rationalizing prune
pruning prune
EOF
)

if [[ -f "$skill_md" ]] && [[ -n "$all_layers" ]]; then
  description_line=$(awk '/^description:/{print; exit}' "$skill_md")

  # which layers does the description mention?
  mentioned_layers=""
  for layer in $all_layers; do
    printf '%s' "$description_line" | grep -qiwE -- "$layer" && mentioned_layers+="$layer "
  done

  # which verbs does the description mention? -> which activities?
  mentioned_activities=" "
  while read -r verb activity; do
    [[ -z "$verb" ]] && continue
    # Match verb as a whole word in description (case-insensitive)
    if printf '%s' "$description_line" | grep -qiwE -- "$verb"; then
      case "$mentioned_activities" in
        *" $activity "*) ;;
        *) mentioned_activities+="$activity " ;;
      esac
    fi
  done <<< "$verb_activity_map"

  # Cross-product: every (activity, layer) advertised by description must
  # be wired in that activity's CSV, unless explicitly omitted via a header
  # comment of the form `# omits: layer1, layer2 (reason)` in the CSV.
  for activity in $mentioned_activities; do
    csv="$skill_dir/references/activities/$activity.csv"
    [[ -f "$csv" ]] || continue
    # Parse omits list from a leading `# omits: layer1, layer2` comment.
    # Rationale belongs on its own `# rationale: ...` line and is ignored here.
    omits=$(awk -F'omits:' '/^#[[:space:]]*omits:/ { print $2; exit }' "$csv")
    omits_normalized=" $(printf '%s' "$omits" | tr ',' ' ') "
    for layer in $mentioned_layers; do
      pb_path="references/layers/${layer}.md"
      if grep -qF -- "$pb_path" "$csv"; then
        continue
      fi
      case "$omits_normalized" in
        *" $layer "*) continue ;;
      esac
      fail "SKILL.md description advertises activity '$activity' x layer '$layer', but $activity.csv does not route to $layer.md (and does not list '$layer' in its '# omits:' header comment)"
    done
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

# ----- trigger-evals.json schema gate -----
# Shape is enforced by the canonical schema (schemas/trigger-evals.schema.json +
# scripts/validate-against-schema.py). Per-skill 'skill' field stays here.

trigger_evals="$skill_dir/evals/trigger-evals.json"
if [[ -f "$trigger_evals" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/trigger-evals.schema.json" "$trigger_evals" \
    || fail "trigger-evals.json: schema validation failed (schemas/trigger-evals.schema.json)"
  skill_in_trigger=$(jq -r '.skill' "$trigger_evals")
  [[ "$skill_in_trigger" == "test-heuristics" ]] \
    || fail "trigger-evals.json: 'skill' must be test-heuristics, got $skill_in_trigger"
fi

# ----- Result -----

if (( failures > 0 )); then
  printf '\ntest-heuristics static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'test-heuristics static eval passed.\n'

#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
trigger_evals="$skill_dir/evals/trigger-evals.json"
activation_cases="$skill_dir/evals/activation-cases.md"

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
check_file "$trigger_evals"
check_file "$activation_cases"
check_file "$skill_dir/references/search-strategy.md"
check_file "$skill_dir/references/source-triage.md"
check_file "$skill_dir/references/confidence-rubric.md"
check_file "$skill_dir/references/modes.md"
check_file "$skill_dir/templates/research-report.md"

# ----- Shared JSON gates (schema + name match) -----

validate_skill_json_contract "$repo_root" "$skill_json" "topic-research"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "topic-research"

# ----- SKILL.md frontmatter and runtime bounds -----

if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  check_pattern 'frontmatter name' '^name:[[:space:]]*topic-research$' "$skill_md"
  check_pattern 'frontmatter description' '^description:' "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"

  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800 (runtime-only bound)"
fi

# ----- SKILL.md structural gates (load-bearing routing surfaces) -----

if [[ -f "$skill_md" ]]; then
  check_pattern 'core principle section' '^## Core principle' "$skill_md"
  check_pattern 'activation section' '^## Activation' "$skill_md"
  check_pattern 'workflow section' '^## Workflow' "$skill_md"
  check_pattern 'modes section' '^## Modes' "$skill_md"
  check_pattern 'output requirements section' '^## Output requirements' "$skill_md"
  check_pattern 'reference map section' '^## Reference map' "$skill_md"
  check_pattern 'brief depth mode' '`brief`' "$skill_md"
  check_pattern 'survey depth mode' '`survey`' "$skill_md"
  check_pattern 'deep-dive depth mode' '`deep-dive`' "$skill_md"
  check_pattern 'search-strategy reference' 'search-strategy\.md' "$skill_md"
  check_pattern 'source-triage reference' 'source-triage\.md' "$skill_md"
  check_pattern 'confidence-rubric reference' 'confidence-rubric\.md' "$skill_md"
  check_pattern 'template reference' 'research-report\.md' "$skill_md"
  check_pattern 'citation requirement' 'citation at' "$skill_md"
  check_pattern 'limitations requirement' 'limitations' "$skill_md"
fi

# ----- Source-leak gate (no inspired_by author last names or titles in SKILL.md) -----
# SKILL.md is runtime-only. Source provenance lives in skill.json. Leaking
# author names or titles into runtime instructions breaks the
# methodology/provenance separation and biases the model toward citing the
# methodology authors as if they were domain authorities on every topic.

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
fi

# ----- Template gates -----

template="$skill_dir/templates/research-report.md"
if [[ -f "$template" ]]; then
  check_pattern 'template has research question section' '^## 1\. Research question' "$template"
  check_pattern 'template has search strategy section' '^## 2\. Search strategy' "$template"
  check_pattern 'template has background section' '^## 3\. Background' "$template"
  check_pattern 'template has current state section' '^## 4\. Current state' "$template"
  check_pattern 'template has debates section' '^## 5\. Key debates' "$template"
  check_pattern 'template has sources section' '^## 7\. Sources' "$template"
  check_pattern 'template has limitations section' '^## 8\. Limitations' "$template"
fi

# ----- trigger-evals coverage -----

if [[ -f "$trigger_evals" ]]; then
  pos=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(sum(1 for q in d['queries'] if q['category']=='positive'))" "$trigger_evals")
  neg=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(sum(1 for q in d['queries'] if q['category']=='negative'))" "$trigger_evals")
  edge=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(sum(1 for q in d['queries'] if q['category']=='edge'))" "$trigger_evals")
  (( pos >= 3 )) || fail "trigger-evals.json: need at least 3 positive cases, got $pos"
  (( neg >= 3 )) || fail "trigger-evals.json: need at least 3 negative cases, got $neg"
  (( edge >= 1 )) || fail "trigger-evals.json: need at least 1 edge case, got $edge"
fi

# ----- Result -----

if (( failures > 0 )); then
  printf '\ntopic-research static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'topic-research static eval passed.\n'

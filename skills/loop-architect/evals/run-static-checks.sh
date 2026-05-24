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
template_dir="$skill_dir/references/templates"
fixture_dir="$skill_dir/evals/fixtures"

failures=0

fail() {
  printf 'FAIL %s\n' "$1" >&2
  failures=$((failures + 1))
}

check_file() {
  [[ -f "$1" ]] || fail "missing file: $1"
}

# ----- File presence -----

check_file "$skill_md"
check_file "$skill_json"
check_file "$trigger_evals"
check_file "$activation_cases"

# Templates referenced from SKILL.md Step 3
check_file "$template_dir/level-1-prompt-learner.py"
check_file "$template_dir/level-2-subroutine-compiler.py"
check_file "$template_dir/level-3-sandbox-harness.py"
check_file "$template_dir/level-4-system-benchmark.py"

# Fixtures used by Phase 2 grader + Phase 3 integration test
check_file "$fixture_dir/translator.py"
check_file "$fixture_dir/agent.py"
check_file "$fixture_dir/classifier.py"
check_file "$fixture_dir/rules.md"
check_file "$fixture_dir/observability.md"
check_file "$fixture_dir/release.md"
check_file "$fixture_dir/README.md"

# Opt-in runners — must ship even though `just check` doesn't invoke them
check_file "$skill_dir/evals/phase2-grader.py"
check_file "$skill_dir/evals/integration-test.sh"

# ----- SKILL.md frontmatter gate -----

if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  grep -Eq '^name: loop-architect$' "$skill_md" || fail "SKILL.md frontmatter must include: name: loop-architect"
  grep -Eq '^description:' "$skill_md" || fail "SKILL.md frontmatter must include: description:"
  grep -Eq '^license:' "$skill_md" || fail "SKILL.md frontmatter must include: license:"

  # Same 800-word bound as example-minimal and dx-heuristics.
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800 (runtime-only bound)"
fi

# ----- SKILL.md source-author leak gate -----
# Mirrors dx-heuristics: no author last name or source title in SKILL.md.

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

# ----- SKILL.md structural gates -----
# These pin load-bearing surface that the Phase 2 grader and the activation
# cases rely on. If any disappears, the skill's diagnostic logic regresses.

if [[ -f "$skill_md" ]]; then
  grep -Eq '^## The AI Optimization Staircase' "$skill_md" \
    || fail "SKILL.md missing section: The AI Optimization Staircase"
  grep -Eq '^## When to Use' "$skill_md" \
    || fail "SKILL.md missing section: When to Use"
  grep -Eq '^## Workflow' "$skill_md" \
    || fail "SKILL.md missing section: Workflow"
  grep -Eq '^## Anti-Patterns to Avoid' "$skill_md" \
    || fail "SKILL.md missing section: Anti-Patterns to Avoid"
  for tier in 'L1: System-Prompt Learning' 'L2: Subroutine Compilation' 'L3: Sandbox + Repair Harness' 'L4: System Benchmarking'; do
    grep -qF -- "$tier" "$skill_md" \
      || fail "SKILL.md staircase table missing tier: $tier"
  done
  for template in 'level-1-prompt-learner.py' 'level-2-subroutine-compiler.py' 'level-3-sandbox-harness.py' 'level-4-system-benchmark.py'; do
    grep -qF -- "$template" "$skill_md" \
      || fail "SKILL.md Step 3 must reference template: $template"
  done
  for concept in 'Loop Readiness Matrix' 'Production Gap' 'trace' 'rollback'; do
    grep -qiF -- "$concept" "$skill_md" \
      || fail "SKILL.md missing loop-readiness concept: $concept"
  done
fi

# ----- Python artifacts must parse -----
# `py_compile` parses without executing imports, so `openai` / `anthropic` /
# `dspy` need not be installed in the CI sandbox.

if [[ -d "$template_dir" ]]; then
  for tpl in "$template_dir"/*.py; do
    [[ -f "$tpl" ]] || continue
    python3 -m py_compile "$tpl" || fail "template won't compile: $tpl"
  done
fi
if [[ -d "$fixture_dir" ]]; then
  for fx in "$fixture_dir"/*.py; do
    [[ -f "$fx" ]] || continue
    python3 -m py_compile "$fx" || fail "fixture won't compile: $fx"
  done
fi

# ----- Opt-in runner sanity gates -----
# We do not execute them; we only check they shell-parse / py-parse.

if [[ -f "$skill_dir/evals/phase2-grader.py" ]]; then
  python3 -m py_compile "$skill_dir/evals/phase2-grader.py" \
    || fail "phase2-grader.py won't compile"
fi
if [[ -f "$skill_dir/evals/integration-test.sh" ]]; then
  bash -n "$skill_dir/evals/integration-test.sh" \
    || fail "integration-test.sh has shell syntax errors"
fi

# ----- Shared JSON gates -----

validate_skill_json_contract "$repo_root" "$skill_json" "loop-architect"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "loop-architect"

if (( failures > 0 )); then
  printf '\nloop-architect static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

echo "loop-architect static eval passed."

#!/usr/bin/env bash
# Shared helpers for per-skill static checks.
#
# Callers provide either a `fail` or `err` function that records a failure
# without exiting.

repo_root_from() {
  local start=$1
  local dir
  dir="$(cd "$start" && pwd)"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/AGENTS.md" && -d "$dir/schemas" && -d "$dir/scripts" ]]; then
      printf '%s\n' "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

_static_check_fail() {
  local message=$1

  if declare -F fail >/dev/null; then
    fail "$message"
  elif declare -F err >/dev/null; then
    err "$message"
  else
    printf 'FAIL %s\n' "$message" >&2
    return 1
  fi
}

validate_skill_json_contract() {
  local repo_root=$1
  local skill_json=$2
  local expected_name=$3

  if [[ ! -f "$skill_json" ]]; then
    _static_check_fail "missing file: $skill_json"
    return
  fi

  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/skill.schema.json" "$skill_json" \
    || _static_check_fail "skill.json: schema validation failed (schemas/skill.schema.json)"

  local actual_name
  actual_name="$(python3 -c "import json, sys; print(json.load(open(sys.argv[1]))['name'])" "$skill_json" 2>/dev/null || true)"
  if [[ -z "$actual_name" ]]; then
    _static_check_fail "skill.json: unable to read name"
  elif [[ "$actual_name" != "$expected_name" ]]; then
    _static_check_fail "skill.json: name must be $expected_name, got $actual_name"
  fi
}

validate_trigger_evals_contract() {
  local repo_root=$1
  local trigger_evals=$2
  local expected_name=$3

  if [[ ! -f "$trigger_evals" ]]; then
    _static_check_fail "evals/trigger-evals.json missing"
    return
  fi

  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/trigger-evals.schema.json" "$trigger_evals" \
    || _static_check_fail "trigger-evals.json: schema validation failed (schemas/trigger-evals.schema.json)"

  local trigger_skill
  trigger_skill="$(python3 -c "import json, sys; print(json.load(open(sys.argv[1]))['skill'])" "$trigger_evals" 2>/dev/null || true)"
  if [[ -z "$trigger_skill" ]]; then
    _static_check_fail "trigger-evals.json: unable to read skill"
  elif [[ "$trigger_skill" != "$expected_name" ]]; then
    _static_check_fail "trigger-evals.json: 'skill' must be $expected_name, got $trigger_skill"
  fi
}

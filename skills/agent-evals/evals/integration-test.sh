#!/usr/bin/env bash
# Phase 3 integration test for agent-evals.
#
# Implements TEST_PLAN.md Phase 3 in four subcommands:
#
#   setup     — create test-sandbox/src/classifier.py from the fixture
#               and print the human-driven invocation hint.
#   verify    — assert that test-sandbox/ai-ops/dataset.json and
#               compile_classifier.py exist with the expected shape.
#   execute   — create a venv, install dspy-ai, run the generated
#               compiler. Costs ~$0.20 against gpt-4o-mini.
#   teardown  — rm -rf test-sandbox/ and .venv-agent-evals/.
#
# NOT invoked from `just check`. Opt-in. The "now run /agent-evals on
# test-sandbox/" step between setup and verify is human-driven because
# automating it via `claude -p` would pull in the entire host harness
# (other skills, MCP servers, AGENTS.md) and the test would no longer be
# grading agent-evals in isolation.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
repo_root="$(cd "$skill_dir/../.." && pwd)"

sandbox_dir="$repo_root/test-sandbox"
venv_dir="$repo_root/.venv-agent-evals"
fixture_dir="$skill_dir/evals/fixtures"

die() {
  printf 'FAIL %s\n' "$1" >&2
  exit 1
}

# Load $repo_root/.env (KEY=VALUE per line; # for comments) without
# clobbering pre-set environment vars. Strict parser — no shell expansion,
# no `export` prefix handling. The file is gitignored; .env.example
# documents the expected keys.
load_dotenv() {
  local env_file="$1"
  [[ -f "$env_file" ]] || return 0
  local line key value
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    [[ "$line" =~ ^[A-Za-z_][A-Za-z0-9_]*= ]] || continue
    key="${line%%=*}"
    value="${line#*=}"
    # strip a matching pair of surrounding quotes
    if [[ "$value" =~ ^\".*\"$ ]]; then
      value="${value:1:${#value}-2}"
    elif [[ "$value" =~ ^\'.*\'$ ]]; then
      value="${value:1:${#value}-2}"
    fi
    # respect already-set environment
    if [[ -z "${!key:-}" ]]; then
      export "$key=$value"
    fi
  done < "$env_file"
}

load_dotenv "$repo_root/.env"

cmd_setup() {
  if [[ -d "$sandbox_dir" ]]; then
    die "test-sandbox/ already exists. Run \`teardown\` first."
  fi
  mkdir -p "$sandbox_dir/src"
  cp "$fixture_dir/classifier.py" "$sandbox_dir/src/classifier.py"
  cat <<EOF
[setup] test-sandbox/ created at:
        $sandbox_dir
[setup] classifier.py copied to test-sandbox/src/classifier.py.

Next step (HUMAN-DRIVEN):
  In Claude Code (or any harness that loads this skill), run:

      Run /agent-evals on test-sandbox/. Scaffold the recommended optimization loop.

  agent-evals should produce test-sandbox/ai-ops/ containing:
    - dataset.json   (5-10 sample tickets with ground-truth labels)
    - compile_classifier.py  (Level 2 DSPy scaffold)

After the agent finishes, run:
      bash $0 verify
EOF
}

cmd_verify() {
  local ai_ops="$sandbox_dir/ai-ops"
  [[ -d "$sandbox_dir" ]]      || die "test-sandbox/ missing. Run \`setup\` first."
  [[ -d "$ai_ops" ]]           || die "test-sandbox/ai-ops/ missing. Did /agent-evals run?"

  local dataset="$ai_ops/dataset.json"
  [[ -f "$dataset" ]] || die "missing $dataset"
  jq -e 'type == "array"' "$dataset" >/dev/null \
    || die "dataset.json must be a JSON array"
  local n_records
  n_records="$(jq 'length' "$dataset")"
  if (( n_records < 5 || n_records > 10 )); then
    die "dataset.json must have 5-10 records, has $n_records"
  fi
  jq -e '.[0] | has("input") and (has("label") or has("category"))' "$dataset" >/dev/null \
    || die "dataset.json records must have input + (label OR category)"

  local compiler="$ai_ops/compile_classifier.py"
  [[ -f "$compiler" ]] || die "missing $compiler"
  python3 -m py_compile "$compiler" || die "compile_classifier.py won't parse"
  grep -q 'dspy\.Signature' "$compiler" || die "missing dspy.Signature in $compiler"
  grep -q 'dspy\.Predict'   "$compiler" || die "missing dspy.Predict in $compiler"
  grep -qE 'MIPROv2|BootstrapFewShot' "$compiler" \
    || die "missing MIPROv2 or BootstrapFewShot in $compiler"

  echo "[verify] PASS — Phase 3 scaffolded artifacts look correct."
  echo "[verify] Next (optional, costs ~\$0.20): bash $0 execute"
}

cmd_execute() {
  local ai_ops="$sandbox_dir/ai-ops"
  local compiler="$ai_ops/compile_classifier.py"
  [[ -f "$compiler" ]] || die "missing $compiler. Run \`setup\` + agent + \`verify\` first."
  if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    echo "[execute] SKIP — OPENAI_API_KEY not set. Export it to run the real DSPy compile."
    exit 0
  fi

  if [[ ! -d "$venv_dir" ]]; then
    echo "[execute] creating venv at $venv_dir"
    python3 -m venv "$venv_dir"
    "$venv_dir/bin/pip" install --quiet --upgrade pip
    "$venv_dir/bin/pip" install --quiet 'dspy-ai>=2.5'
  else
    echo "[execute] reusing existing venv at $venv_dir"
  fi

  echo "[execute] running $compiler ..."
  pushd "$sandbox_dir" >/dev/null
  if ! "$venv_dir/bin/python" "$compiler"; then
    popd >/dev/null
    die "compile_classifier.py raised at runtime. See trace above."
  fi
  popd >/dev/null
  echo "[execute] PASS — compiled artifact resolved imports and signatures."
  echo "[execute] (NB: with 5-10 examples, compilation is mostly a smoke-test of"
  echo "         imports and signature shape, not optimization quality.)"
}

cmd_teardown() {
  if [[ -d "$sandbox_dir" ]]; then
    rm -rf "$sandbox_dir"
    echo "[teardown] removed $sandbox_dir"
  fi
  if [[ -d "$venv_dir" ]]; then
    rm -rf "$venv_dir"
    echo "[teardown] removed $venv_dir"
  fi
}

cmd_refresh() {
  # teardown + setup. Useful when a prior verify left lingering state and
  # you want a clean fixture without chaining commands. Preserves the venv
  # by default (skip it during teardown) so we don't trigger a 60s dspy-ai
  # reinstall on the next execute.
  if [[ -d "$sandbox_dir" ]]; then
    rm -rf "$sandbox_dir"
    echo "[refresh] removed $sandbox_dir (venv preserved)"
  fi
  cmd_setup
}

usage() {
  cat <<EOF
Usage: $0 <setup|refresh|verify|execute|teardown>

  setup     create test-sandbox/, copy the classifier.py fixture, print the
            human-driven /agent-evals invocation hint.
  refresh   remove test-sandbox/ (keep the venv) and run setup. Use when a
            prior run left lingering ai-ops/ state and you want a clean
            fixture without paying for a venv reinstall.
  verify    assert ai-ops/dataset.json + compile_classifier.py have the
            expected shape after the agent has scaffolded them.
  execute   create a venv, install dspy-ai, run the compiled module.
            Requires OPENAI_API_KEY. Costs ~\$0.20.
  teardown  remove test-sandbox/ and .venv-agent-evals/.
EOF
}

case "${1:-}" in
  setup)    cmd_setup ;;
  refresh)  cmd_refresh ;;
  verify)   cmd_verify ;;
  execute)  cmd_execute ;;
  teardown) cmd_teardown ;;
  -h|--help|help|"") usage ;;
  *)        usage; exit 2 ;;
esac

#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  codex-review-changes.sh [options]

Options:
  --scope <uncommitted|branch|commit>   Review scope (default: uncommitted)
  --base <branch>                       Base branch for --scope branch
  --commit <sha>                        Commit SHA for --scope commit
  --extra <text>                        Extra review instructions
  --model <model>                       Codex model override
  --profile <profile>                   Codex config profile
  --config <key=value>                  Codex config override (repeatable)
  --output <file>                       Write Codex output to a file as well
  --dry-run                             Print command and prompt; do not invoke Codex
  -h, --help                            Show help

Examples:
  codex-review-changes.sh
  codex-review-changes.sh --scope branch --base main
  codex-review-changes.sh --scope commit --commit abc123 --dry-run
USAGE
}

scope="uncommitted"
base_ref=""
commit_sha=""
extra=""
model="${CODEX_CLI_MODEL:-}"
profile="${CODEX_CLI_PROFILE:-}"
output_file=""
dry_run=0
config_values=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope)
      scope="${2:-}"
      shift 2
      ;;
    --base)
      base_ref="${2:-}"
      shift 2
      ;;
    --commit)
      commit_sha="${2:-}"
      shift 2
      ;;
    --extra)
      extra="${2:-}"
      shift 2
      ;;
    --model)
      model="${2:-}"
      shift 2
      ;;
    --profile)
      profile="${2:-}"
      shift 2
      ;;
    --config)
      config_values+=("${2:-}")
      shift 2
      ;;
    --output)
      output_file="${2:-}"
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

case "$scope" in
  uncommitted|branch|commit) ;;
  *)
    echo "Invalid --scope: $scope" >&2
    exit 1
    ;;
esac

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
template="$skill_dir/templates/review-prompt.md"

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$repo_root" ]]; then
  echo "Must be run inside a git repository." >&2
  exit 1
fi
cd "$repo_root"

resolve_branch_base() {
  if [[ -n "$base_ref" ]]; then
    printf '%s\n' "$base_ref"
    return
  fi

  local upstream
  upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
  if [[ -n "$upstream" ]]; then
    printf '%s\n' "$upstream"
    return
  fi

  if git rev-parse --verify main >/dev/null 2>&1; then
    printf 'main\n'
    return
  fi

  if git rev-parse --verify master >/dev/null 2>&1; then
    printf 'master\n'
    return
  fi

  echo "Could not infer branch base. Pass --base <branch>." >&2
  exit 1
}

prompt_file="$(mktemp)"
trap 'rm -f "$prompt_file"' EXIT

scope_label="$scope"
case "$scope" in
  branch)
    base_ref="$(resolve_branch_base)"
    scope_label="branch against $base_ref"
    ;;
  commit)
    if [[ -z "$commit_sha" ]]; then
      echo "--commit is required with --scope commit" >&2
      exit 1
    fi
    scope_label="commit $commit_sha"
    ;;
esac

while IFS= read -r line || [[ -n "$line" ]]; do
  case "$line" in
    *"{{SCOPE}}"*)
      printf '%s\n' "${line//\{\{SCOPE\}\}/$scope_label}"
      ;;
    "{{EXTRA_INSTRUCTIONS}}")
      printf '%s\n' "${extra:-None}"
      ;;
    *"{{EXTRA_INSTRUCTIONS}}"*)
      printf '%s\n' "${line//\{\{EXTRA_INSTRUCTIONS\}\}/${extra:-None}}"
      ;;
    *)
      printf '%s\n' "$line"
      ;;
  esac
done < "$template" > "$prompt_file"

cmd=(codex)
[[ -n "$model" ]] && cmd+=(-m "$model")
[[ -n "$profile" ]] && cmd+=(-p "$profile")
if (( ${#config_values[@]} > 0 )); then
  for config_value in "${config_values[@]}"; do
    cmd+=(-c "$config_value")
  done
fi
cmd+=(review)

# `codex review` rejects a [PROMPT] with EVERY scope flag — e.g. `error: the
# argument '--uncommitted' cannot be used with '[PROMPT]'` (and likewise --base /
# --commit), verified live on codex-cli 0.141.0. So no scope can deliver the
# review-prompt template or --extra; all scopes use Codex's built-in review
# standard. (A custom review rubric would require the `codex exec` path instead.)
scope_takes_prompt=0
case "$scope" in
  uncommitted)
    cmd+=(--uncommitted)
    ;;
  branch)
    cmd+=(--base "$base_ref")
    ;;
  commit)
    cmd+=(--commit "$commit_sha")
    ;;
esac

if [[ -n "$extra" ]]; then
  echo "Note: 'codex review' accepts no custom prompt with any scope flag (Codex CLI limitation); --extra is ignored. Codex uses its built-in review standard." >&2
fi

print_command() {
  printf 'Command:'
  printf ' %q' "${cmd[@]}"
  (( scope_takes_prompt == 1 )) && printf ' < prompt'
  printf '\n'
}

if (( dry_run == 1 )); then
  print_command
  if (( scope_takes_prompt == 1 )); then
    printf '\nPrompt:\n\n'
    cat "$prompt_file"
  else
    printf '\n(%s scope passes no stdin prompt; codex review uses its built-in review standard)\n' "$scope"
  fi
  exit 0
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI not found on PATH. Install or authenticate Codex, then retry." >&2
  exit 1
fi

run_codex() {
  if (( scope_takes_prompt == 1 )); then
    "${cmd[@]}" < "$prompt_file"
  else
    "${cmd[@]}"
  fi
}

if [[ -n "$output_file" ]]; then
  mkdir -p "$(dirname "$output_file")"
  run_codex | tee "$output_file"
else
  run_codex
fi

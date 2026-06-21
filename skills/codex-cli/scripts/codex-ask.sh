#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  codex-ask.sh [options] [prompt]

Options:
  --context-file <file>                 Include a context file (repeatable)
  --template <file>                     Prompt template relative to skill dir or cwd
  --cd <dir>                            Run Codex with this working directory
  --model <model>                       Codex model override
  --profile <profile>                   Codex config profile
  --config <key=value>                  Codex config override (repeatable)
  --sandbox <mode>                      read-only, workspace-write, or danger-full-access
  --ask-for-approval <policy>           untrusted, on-request, on-failure, or never
  --skip-git-repo-check                 Pass Codex's non-git-directory override
  --output <file>                       Write Codex output to a file as well
  --dry-run                             Print command and prompt; do not invoke Codex
  -h, --help                            Show help

Examples:
  codex-ask.sh "Review this migration plan for risks."
  printf '%s\n' "Find flaws in this architecture." | codex-ask.sh --model gpt-5-codex
USAGE
}

model="${CODEX_CLI_MODEL:-}"
profile="${CODEX_CLI_PROFILE:-}"
sandbox="${CODEX_CLI_SANDBOX:-read-only}"
approval_policy="${CODEX_CLI_APPROVAL_POLICY:-never}"
output_file=""
dry_run=0
target_dir=""
template_arg="templates/delegation-prompt.md"
force_skip_git_check=0
context_files=()
prompt_parts=()
config_values=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --context-file)
      context_files+=("${2:-}")
      shift 2
      ;;
    --template)
      template_arg="${2:-}"
      shift 2
      ;;
    --cd)
      target_dir="${2:-}"
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
    --sandbox)
      sandbox="${2:-}"
      shift 2
      ;;
    --ask-for-approval)
      approval_policy="${2:-}"
      shift 2
      ;;
    --skip-git-repo-check)
      force_skip_git_check=1
      shift
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
    --)
      shift
      prompt_parts+=("$@")
      break
      ;;
    *)
      prompt_parts+=("$1")
      shift
      ;;
  esac
done

case "$sandbox" in
  read-only|workspace-write|danger-full-access) ;;
  *)
    echo "Invalid --sandbox: $sandbox" >&2
    exit 1
    ;;
esac

case "$approval_policy" in
  untrusted|on-request|on-failure|never) ;;
  *)
    echo "Invalid --ask-for-approval: $approval_policy" >&2
    exit 1
    ;;
esac

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
template="$template_arg"
if [[ "$template" != /* ]]; then
  if [[ -f "$template" ]]; then
    template="$(cd "$(dirname "$template")" && pwd)/$(basename "$template")"
  else
    template="$skill_dir/$template"
  fi
fi
if [[ ! -f "$template" ]]; then
  echo "Prompt template not found: $template_arg" >&2
  exit 1
fi
if [[ -n "$target_dir" && ! -d "$target_dir" ]]; then
  echo "Working directory not found: $target_dir" >&2
  exit 1
fi
prompt_file="$(mktemp)"
context_file="$(mktemp)"
trap 'rm -f "$prompt_file" "$context_file"' EXIT

if (( ${#prompt_parts[@]} > 0 )); then
  task="${prompt_parts[*]}"
else
  task="$(cat)"
fi

if [[ -z "${task//[[:space:]]/}" ]]; then
  echo "Prompt is required via arguments or stdin." >&2
  usage
  exit 1
fi

if [[ -n "$target_dir" ]]; then
  repo_root="$target_dir"
else
  repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
fi
skip_git_check="$force_skip_git_check"
if [[ -z "$repo_root" ]]; then
  repo_root="$(pwd)"
  skip_git_check=1
elif ! git -C "$repo_root" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  skip_git_check=1
fi

{
  if (( ${#context_files[@]} == 0 )); then
    printf 'No additional context files provided.\n'
  else
    for file in "${context_files[@]}"; do
      if [[ ! -f "$file" ]]; then
        printf '\n## %s\n\nMissing context file.\n' "$file"
        continue
      fi
      printf '\n## %s\n\n' "$file"
      sed -n '1,240p' "$file"
      bytes="$(wc -c < "$file" | tr -d ' ')"
      if (( bytes > 20000 )); then
        printf '\n[TRUNCATED: displayed first 240 lines of %s byte file.]\n' "$bytes"
      fi
    done
  fi
} > "$context_file"

while IFS= read -r line || [[ -n "$line" ]]; do
  case "$line" in
    "{{TASK}}")
      printf '%s\n' "$task"
      ;;
    *"{{TASK}}"*)
      printf '%s\n' "${line//\{\{TASK\}\}/$task}"
      ;;
    "{{CONTEXT}}")
      cat "$context_file"
      ;;
    *"{{CONTEXT}}"*)
      printf '%s\n' "${line//\{\{CONTEXT\}\}/$(cat "$context_file")}"
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
cmd+=(--sandbox "$sandbox" --ask-for-approval "$approval_policy" --cd "$repo_root")
cmd+=(exec --ephemeral)
if (( skip_git_check == 1 )); then
  cmd+=(--skip-git-repo-check)
fi
# Force the stdin sentinel to be parsed as the prompt positional, not a flag.
cmd+=(-- -)

print_command() {
  printf 'Command:'
  printf ' %q' "${cmd[@]}"
  printf ' < prompt\n'
}

if (( dry_run == 1 )); then
  print_command
  printf '\nPrompt:\n\n'
  cat "$prompt_file"
  exit 0
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI not found on PATH. Install or authenticate Codex, then retry." >&2
  exit 1
fi

if [[ -n "$output_file" ]]; then
  mkdir -p "$(dirname "$output_file")"
  "${cmd[@]}" < "$prompt_file" | tee "$output_file"
else
  "${cmd[@]}" < "$prompt_file"
fi

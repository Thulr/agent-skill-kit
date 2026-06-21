#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  claude-ask.sh [options] [prompt]

Options:
  --context-file <file>                 Include a context file (repeatable)
  --template <file>                     Prompt template relative to skill dir or cwd
  --cwd <dir>                           Run claude from this directory
  --model <model>                       Claude model or alias
  --effort <level>                      low, medium, high, xhigh, or max
  --permission-mode <mode>              Claude permission mode (default: plan)
  --max-budget-usd <amount>             Budget guardrail for claude -p
  --output <file>                       Write Claude output to a file as well
  --dry-run                             Print the prompt; do not invoke Claude
  -h, --help                            Show help

Examples:
  claude-ask.sh "Review this migration plan for risks."
  printf '%s\n' "Find flaws in this architecture." | claude-ask.sh --effort high
USAGE
}

model="${CLAUDE_CODE_CLI_MODEL:-}"
effort="${CLAUDE_CODE_CLI_EFFORT:-}"
permission_mode="${CLAUDE_CODE_CLI_PERMISSION_MODE:-plan}"
budget="${CLAUDE_CODE_CLI_MAX_BUDGET_USD:-}"
output_file=""
dry_run=0
run_cwd=""
template_arg="templates/delegation-prompt.md"
context_files=()
prompt_parts=()

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
    --cwd)
      run_cwd="${2:-}"
      shift 2
      ;;
    --model)
      model="${2:-}"
      shift 2
      ;;
    --effort)
      effort="${2:-}"
      shift 2
      ;;
    --permission-mode)
      permission_mode="${2:-}"
      shift 2
      ;;
    --max-budget-usd)
      budget="${2:-}"
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
if [[ -n "$run_cwd" && ! -d "$run_cwd" ]]; then
  echo "Working directory not found: $run_cwd" >&2
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

if (( dry_run == 1 )); then
  if [[ -n "$run_cwd" ]]; then
    printf 'Working directory: %s\n\n' "$run_cwd"
  fi
  cat "$prompt_file"
  exit 0
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "Claude Code CLI not found on PATH. Install or authenticate Claude Code, then retry." >&2
  exit 1
fi

cmd=(claude -p --permission-mode "$permission_mode" --output-format text --name "claude-code-cli-ask")
[[ -n "$model" ]] && cmd+=(--model "$model")
[[ -n "$effort" ]] && cmd+=(--effort "$effort")
[[ -n "$budget" ]] && cmd+=(--max-budget-usd "$budget")

run_claude() {
  if [[ -n "$run_cwd" ]]; then
    (cd "$run_cwd" && "${cmd[@]}" < "$prompt_file")
  else
    "${cmd[@]}" < "$prompt_file"
  fi
}

if [[ -n "$output_file" ]]; then
  mkdir -p "$(dirname "$output_file")"
  run_claude | tee "$output_file"
else
  run_claude
fi

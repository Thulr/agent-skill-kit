#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  claude-cross-project-reflect.sh [options]

Options:
  --since <date-or-window>              Date/window to inspect, e.g. 2026-05-01
  --cwd <dir>                           Neutral starting directory (default: $HOME)
  --context-file <file>                 Include a compact context file (repeatable)
  --model <model>                       Claude model or alias
  --effort <level>                      low, medium, high, xhigh, or max
  --permission-mode <mode>              Claude permission mode (default: plan)
  --max-budget-usd <amount>             Budget guardrail for claude -p
  --output <file>                       Write Claude output to a file as well
  --dry-run                             Print the prompt; do not invoke Claude
  -h, --help                            Show help

Example:
  claude-cross-project-reflect.sh --since "last 30 days" --dry-run
USAGE
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cwd="${HOME:-$(pwd)}"
since="last 30 days"
args=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since)
      since="${2:-}"
      shift 2
      ;;
    --cwd)
      cwd="${2:-}"
      shift 2
      ;;
    --context-file|--model|--effort|--permission-mode|--max-budget-usd|--output)
      args+=("$1" "${2:-}")
      shift 2
      ;;
    --dry-run)
      args+=("$1")
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

task="Reflect on Claude Code work across projects for ${since}. Identify repeated mistakes you have made, common feedback Justin gives, patterns in how he works or reviews, and durable workflow improvements. Treat this as global/cross-project evidence, not a review of the repository that launched the command."

exec "$script_dir/claude-ask.sh" \
  --template templates/cross-project-reflection-prompt.md \
  --cwd "$cwd" \
  "${args[@]}" \
  "$task"

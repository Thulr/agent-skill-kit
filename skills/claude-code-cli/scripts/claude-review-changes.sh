#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  claude-review-changes.sh [options]

Options:
  --scope <all|staged|unstaged|branch>  Diff scope to review (default: all)
  --base <ref>                          Base ref for --scope branch
  --extra <text>                        Extra review instructions
  --model <model>                       Claude model or alias
  --effort <level>                      low, medium, high, xhigh, or max
  --permission-mode <mode>              Claude permission mode (default: plan)
  --max-budget-usd <amount>             Budget guardrail for claude -p
  --max-diff-bytes <bytes>              Prompt diff byte limit (default: 200000)
  --output <file>                       Write Claude output to a file as well
  --dry-run                             Print the prompt; do not invoke Claude
  -h, --help                            Show help

Examples:
  claude-review-changes.sh
  claude-review-changes.sh --scope staged --effort high
  claude-review-changes.sh --scope branch --base main --dry-run
USAGE
}

scope="all"
base_ref=""
extra=""
model="${CLAUDE_CODE_CLI_MODEL:-}"
effort="${CLAUDE_CODE_CLI_EFFORT:-}"
permission_mode="${CLAUDE_CODE_CLI_PERMISSION_MODE:-plan}"
budget="${CLAUDE_CODE_CLI_MAX_BUDGET_USD:-}"
max_diff_bytes="${CLAUDE_CODE_CLI_MAX_DIFF_BYTES:-200000}"
output_file=""
dry_run=0

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
    --extra)
      extra="${2:-}"
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
    --max-diff-bytes)
      max_diff_bytes="${2:-}"
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
  all|staged|unstaged|branch) ;;
  *)
    echo "Invalid --scope: $scope" >&2
    exit 1
    ;;
esac

if ! [[ "$max_diff_bytes" =~ ^[0-9]+$ ]]; then
  echo "--max-diff-bytes must be an integer" >&2
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
template="$skill_dir/templates/review-prompt.md"

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$repo_root" ]]; then
  echo "Must be run inside a git repository." >&2
  exit 1
fi
cd "$repo_root"

prompt_file="$(mktemp)"
diff_file="$(mktemp)"
truncated_file="$(mktemp)"
trap 'rm -f "$prompt_file" "$diff_file" "$truncated_file"' EXIT

append_section() {
  local title="$1"
  shift
  {
    printf '\n## %s\n\n' "$title"
    "$@" || true
  } >> "$diff_file"
}

append_untracked_files() {
  local file size
  local per_file_limit=40000

  printf '\n## Untracked files\n\n' >> "$diff_file"
  git ls-files --others --exclude-standard >> "$diff_file" || true

  while IFS= read -r -d '' file; do
    [[ -f "$file" ]] || continue
    size="$(wc -c < "$file" | tr -d ' ')"
    if (( size > per_file_limit )); then
      printf '\n### %s\n\nSkipped: untracked file is %s bytes, over %s byte per-file limit.\n' \
        "$file" "$size" "$per_file_limit" >> "$diff_file"
      continue
    fi
    if (( size > 0 )) && ! LC_ALL=C grep -Iq . "$file"; then
      printf '\n### %s\n\nSkipped: binary-looking untracked file.\n' "$file" >> "$diff_file"
      continue
    fi
    printf '\n### %s\n\n' "$file" >> "$diff_file"
    git diff --no-index -- /dev/null "$file" >> "$diff_file" 2>/dev/null || true
  done < <(git ls-files --others --exclude-standard -z)
}

resolve_branch_base() {
  if [[ -n "$base_ref" ]]; then
    git rev-parse --verify --quiet "${base_ref}^{commit}" >/dev/null \
      || { echo "Base ref not found: $base_ref. Pass a valid --base <ref>." >&2; exit 1; }
    printf '%s\n' "$base_ref"
    return
  fi

  local upstream
  upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
  if [[ -n "$upstream" ]]; then
    git merge-base HEAD "$upstream"
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

  echo "Could not infer branch base. Pass --base <ref>." >&2
  exit 1
}

{
  printf '# Review Context\n\n'
  printf 'Repository: %s\n' "$repo_root"
  printf 'Scope: %s\n' "$scope"
  printf 'Generated: %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
} > "$diff_file"

append_section "Git status" git status --short

case "$scope" in
  all)
    append_section "Staged diff stat" git diff --cached --stat
    append_section "Staged diff" git diff --cached --no-ext-diff --find-renames
    append_section "Unstaged diff stat" git diff --stat
    append_section "Unstaged diff" git diff --no-ext-diff --find-renames
    append_untracked_files
    ;;
  staged)
    append_section "Staged diff stat" git diff --cached --stat
    append_section "Staged diff" git diff --cached --no-ext-diff --find-renames
    ;;
  unstaged)
    append_section "Unstaged diff stat" git diff --stat
    append_section "Unstaged diff" git diff --no-ext-diff --find-renames
    append_untracked_files
    ;;
  branch)
    base_ref="$(resolve_branch_base)"
    append_section "Branch base" printf '%s\n' "$base_ref"
    append_section "Branch diff stat" git diff --stat "$base_ref"...HEAD
    append_section "Branch diff" git diff --no-ext-diff --find-renames "$base_ref"...HEAD
    ;;
esac

diff_size="$(wc -c < "$diff_file" | tr -d ' ')"
if (( diff_size > max_diff_bytes )); then
  head -c "$max_diff_bytes" "$diff_file" > "$truncated_file"
  {
    cat "$truncated_file"
    printf '\n\n[TRUNCATED: original change context was %s bytes; limit was %s bytes. Ask for a narrower scope if needed.]\n' \
      "$diff_size" "$max_diff_bytes"
  } > "$diff_file"
fi

replace_template() {
  local line
  while IFS= read -r line || [[ -n "$line" ]]; do
    case "$line" in
      *"{{SCOPE}}"*)
        printf '%s\n' "${line//\{\{SCOPE\}\}/$scope}"
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
  done < "$template"
}

{
  replace_template
  printf '\n\n# Change Context\n\n'
  cat "$diff_file"
} > "$prompt_file"

if (( dry_run == 1 )); then
  cat "$prompt_file"
  exit 0
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "Claude Code CLI not found on PATH. Install or authenticate Claude Code, then retry." >&2
  exit 1
fi

cmd=(claude -p --permission-mode "$permission_mode" --output-format text --name "claude-code-cli-review")
[[ -n "$model" ]] && cmd+=(--model "$model")
[[ -n "$effort" ]] && cmd+=(--effort "$effort")
[[ -n "$budget" ]] && cmd+=(--max-budget-usd "$budget")

if [[ -n "$output_file" ]]; then
  mkdir -p "$(dirname "$output_file")"
  "${cmd[@]}" < "$prompt_file" | tee "$output_file"
else
  "${cmd[@]}" < "$prompt_file"
fi

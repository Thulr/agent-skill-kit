#!/usr/bin/env bash
#
# TEMPLATE — instruction-surface drift check.
# Prescribed by instruction-surface scaffold H2-harden (the three-action unit:
# CLAUDE.md symlink + copilot-instructions.md symlink + this CI assertion).
# Without the assertion, the symlinks decay the first time a contributor
# "fixes" one by replacing it with a regular file. W8 covers the risk.
#
# Customization: SYMLINKS array below maps each harness-specific instruction
# file to its required target (relative to the symlink's own directory).
# Add a row for every harness in the step 4.5 inventory that ships an
# instruction file (Codex AGENTS.override.md, Windsurf .windsurfrules, etc.
# — only when those files exist in this repo).
#
# Run by CI and by `just check` / equivalent.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# (path, expected_target_relative_to_path, human-readable label).
# Each path MUST be a symlink resolving to expected_target.
SYMLINKS=(
    "CLAUDE.md|AGENTS.md|CLAUDE.md -> AGENTS.md (Claude Code, Anthropic)"
    ".github/copilot-instructions.md|../AGENTS.md|copilot-instructions.md -> ../AGENTS.md (Copilot)"
    # Add additional rows here per the harness inventory.
    # ".cursorrules.md|AGENTS.md|.cursorrules.md -> AGENTS.md (Cursor — only if not using .cursor/rules/)"
)

failed=0

assert_symlink() {
    local path=$1
    local expected_target=$2
    local label=$3

    if [[ ! -e $path && ! -L $path ]]; then
        echo "FAIL: $label: $path does not exist" >&2
        failed=1
        return
    fi

    if [[ ! -L $path ]]; then
        echo "FAIL: $label: $path exists but is not a symlink (W8: harness/portable drift)" >&2
        echo "       fix: rm $path && ln -sf $expected_target $path" >&2
        failed=1
        return
    fi

    local actual_target
    actual_target=$(readlink "$path")
    if [[ $actual_target != "$expected_target" ]]; then
        echo "FAIL: $label: $path -> $actual_target, expected -> $expected_target" >&2
        failed=1
        return
    fi

    if [[ ! -e $path ]]; then
        echo "FAIL: $label: $path is a symlink but its target does not resolve" >&2
        failed=1
        return
    fi

    echo "OK:   $label: $path -> $actual_target"
}

if [[ ! -f AGENTS.md ]]; then
    echo "FAIL: AGENTS.md does not exist at repo root; nothing to symlink to" >&2
    exit 1
fi

for row in "${SYMLINKS[@]}"; do
    IFS='|' read -r path target label <<< "$row"
    assert_symlink "$path" "$target" "$label"
done

exit "$failed"

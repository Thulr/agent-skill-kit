#!/usr/bin/env bash
#
# Asserts that the harness-specific instruction files are symlinks to the
# portable AGENTS.md, per the instruction-surface playbook H2-harden
# (skills/harden-repo-for-coding-agents/references/playbooks/instruction-surface.md)
# and W8 (empirical-warnings.md): harness-specific and portable layers drift
# silently when not symlinked. Canonical pattern: vercel/next.js.
#
# Run by CI (.github/workflows/ci.yml) and `just check`.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

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

assert_symlink "CLAUDE.md" "AGENTS.md" "CLAUDE.md -> AGENTS.md"
assert_symlink ".github/copilot-instructions.md" "../AGENTS.md" ".github/copilot-instructions.md -> ../AGENTS.md"

exit "$failed"

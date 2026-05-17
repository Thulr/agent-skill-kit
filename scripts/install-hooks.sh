#!/usr/bin/env bash
# Configures git to use the repo's .githooks/ directory for hooks.
# Run once after cloning the repo.
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir" rev-parse --show-toplevel)"
cd "$repo_root"
git config core.hooksPath .githooks
echo "✓ git hooks now sourced from .githooks/"
echo "  commit-msg will validate Conventional Commits on every commit."

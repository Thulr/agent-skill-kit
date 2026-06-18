#!/usr/bin/env bash
#
# install-hooks.sh — set up local git hooks for agent-skill-kit.
#
# Installs the pre-commit framework (https://pre-commit.com) if missing,
# wires it into .git/hooks, and runs an initial scan against the working
# tree. Idempotent: safe to re-run after pulling new hook changes.
set -euo pipefail

if command -v pre-commit >/dev/null 2>&1; then
  echo "✓ pre-commit already on PATH"
elif python3 -c "import pre_commit" 2>/dev/null; then
  echo "✓ pre-commit available via 'python3 -m pre_commit'"
elif command -v pipx >/dev/null 2>&1; then
  echo "==> Installing pre-commit via pipx"
  pipx install pre-commit
elif command -v brew >/dev/null 2>&1; then
  # Homebrew Python blocks 'pip install --user' (PEP 668), so on macOS
  # brew is the most reliable next step.
  echo "==> Installing pre-commit via Homebrew"
  brew install pre-commit
else
  # Last resort: --user pip install. On externally-managed Pythons (PEP 668)
  # this requires --break-system-packages; we'd rather fail loudly than
  # silently break the user's system Python. If you hit this, install pipx
  # (https://pipx.pypa.io) or your platform's package manager and re-run.
  echo "==> Installing pre-commit via 'pip install --user'"
  echo "    (prefer pipx for isolation: https://pipx.pypa.io)"
  python3 -m pip install --user pre-commit
fi

pc() {
  if command -v pre-commit >/dev/null 2>&1; then
    pre-commit "$@"
  else
    python3 -m pre_commit "$@"
  fi
}

echo "==> Wiring git hook into .git/hooks/pre-commit"
pc install

echo "==> Running initial scan (pre-commit run --all-files)"
pc run --all-files

echo
echo "✓ Pre-commit hooks installed and verified."
echo "  • Hooks run automatically on 'git commit'."
echo "  • Re-scan on demand: pre-commit run --all-files"
echo "  • Bump pinned hook versions: pre-commit autoupdate"

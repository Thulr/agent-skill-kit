set shell := ["bash", "-euo", "pipefail", "-c"]

check:
    bash scripts/list-installable-skills.sh
    python3 scripts/test-skill-inventory.py
    python3 scripts/check-release-contract.py
    python3 scripts/test-trigger-evals-schema.py
    python3 scripts/test-run-trigger-evals.py
    python3 scripts/test-check-skill-static.py
    python3 scripts/test-routing-graph.py
    python3 scripts/test-catalog-taxonomy.py
    bash scripts/check-instruction-surface.sh
    bash scripts/check-shared-content.sh
    bash scripts/check-routing-csv.sh
    python3 scripts/check-doc-links.py
    python3 scripts/build-catalog.py --check
    python3 scripts/check-catalog-taxonomy.py
    python3 .claude/hooks/test_block_destructive_bash.py
    python3 .codex/hooks/test_block_destructive_bash.py
    python3 .cursor/hooks/test_block_destructive_bash.py
    python3 scripts/run-skill-static-checks.py

test: check

# Model-graded activation-routing eval (opt-in; needs `pi`). NOT part of `just check`
# — it makes live judge calls (default provider openai-codex, i.e. Codex via pi) and is
# non-deterministic. `just check` covers the runner's logic offline via the mock backend.
#   just eval                                          # full catalog
#   just eval --skills ui-design,dx-audit
eval *args:
    python3 scripts/run-trigger-evals.py {{args}}

install-hooks:
    bash scripts/install-hooks.sh

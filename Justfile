set shell := ["bash", "-euo", "pipefail", "-c"]

check:
    bash scripts/list-installable-skills.sh
    python3 scripts/test-skill-inventory.py
    python3 scripts/check-release-contract.py
    python3 scripts/test-trigger-evals-schema.py
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

install-hooks:
    bash scripts/install-hooks.sh

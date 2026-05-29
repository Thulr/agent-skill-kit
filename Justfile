set shell := ["bash", "-euo", "pipefail", "-c"]

check:
    bash scripts/list-installable-skills.sh
    python3 scripts/check-release-contract.py
    python3 scripts/test-trigger-evals-schema.py
    bash scripts/check-instruction-surface.sh
    bash scripts/check-shared-content.sh
    bash scripts/check-routing-csv.sh
    python3 .claude/hooks/test_block_destructive_bash.py
    python3 .codex/hooks/test_block_destructive_bash.py
    python3 .cursor/hooks/test_block_destructive_bash.py
    shopt -s nullglob; \
    for script in skills/*/evals/run-static-checks.sh skills/.experimental/*/evals/run-static-checks.sh .agents/skills/*/evals/run-static-checks.sh; do \
      echo "running $script"; \
      bash "$script"; \
    done

test: check

install-hooks:
    bash scripts/install-hooks.sh

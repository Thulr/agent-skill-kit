set shell := ["bash", "-euo", "pipefail", "-c"]

check:
    npx skills add . --list
    for script in skills/*/evals/run-static-checks.sh .agents/skills/*/evals/run-static-checks.sh; do \
      if [ -f "$script" ]; then \
        echo "running $script"; \
        bash "$script"; \
      fi; \
    done

test: check

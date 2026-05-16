set shell := ["bash", "-euo", "pipefail", "-c"]

check:
    npx skills add . --list
    shopt -s nullglob; \
    for script in skills/*/evals/run-static-checks.sh skills/.experimental/*/evals/run-static-checks.sh .agents/skills/*/evals/run-static-checks.sh; do \
      echo "running $script"; \
      bash "$script"; \
    done

test: check

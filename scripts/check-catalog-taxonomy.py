#!/usr/bin/env python3
"""Check that catalog taxonomy facts stay in sync across docs and metadata."""
from __future__ import annotations

import sys
from pathlib import Path

from catalog_taxonomy import CatalogTaxonomy


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    taxonomy = CatalogTaxonomy(ROOT)
    failures = taxonomy.validate()
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        print(f"\ncheck-catalog-taxonomy: {len(failures)} failure(s).", file=sys.stderr)
        return 1
    pairs = ", ".join(sorted(taxonomy.heuristic_pairs()))
    print(f"OK:   catalog taxonomy is in sync (heuristic pairs: {pairs})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

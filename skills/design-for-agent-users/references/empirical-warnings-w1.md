# W1 — the ≥3-observed-failures promotion floor (breadcrumb)

W1 is **owned by `rules-from-coding-agent-failures`**, not this skill. It is a
deliberate prose breadcrumb, not a symlink: W1 is that skill's sole-tenant file
and lives at
`skills/rules-from-coding-agent-failures/references/empirical-warnings-w1.md` — it is
**not** in `skills/_shared/`, so it must not be symlinked cross-skill (`npx
skills` dereferences symlinks at install time, and a symlink resolving into
another skill's references is fragile).

**The floor:** scaffolding written from fewer than three observed agent failures
produces plausible boilerplate that hurts agent success ~3% on average (Mündler
et al., ETH/LogicStar, Feb 2026). W1 gates **promotion** of a rule into an
always-loaded surface (AGENTS.md, a hook, a gate) — not the **recording** of a
single observation.

When an AX review recommends promoting a recurring failure into a rule or gate,
route the *doing* to `rules-from-coding-agent-failures` (the evidence/feedback arm)
and apply W1 there. W2–W10 (the cross-cutting AX guardrails) live in
`references/empirical-warnings.md`.

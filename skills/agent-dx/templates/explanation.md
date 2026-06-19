# Agent DX — EXPLAIN — <concept>

**Target persona:** <from references/core/personas.md>
**Surface:** <one of the five>
**Date:** <YYYY-MM-DD>

## The concept in one sentence

<The most compact accurate statement.>

## What it is

<2–4 paragraphs, in the glossary's vocabulary. Ground claims in the playbook's `## Grounding`
entries.>

## What it is not

<Common confusions and adjacent ideas it is mistaken for — e.g. "structured output" is not
"ask for JSON and hope"; a semantic retry is not a transport retry; an agent-readable error is
not a prettier stack trace.>

## Why it matters

<The cost of not having it for a stochastic, machine-speed consumer: a loop that spins, a
hallucinated success that ships, a secret that leaves the boundary, PII that lands in spans.>

## A small example

<A concrete example in pseudo-code or a short scenario — e.g. a tool error before and after it
is shaped for retry. Avoid language-specific syntax unless the persona is language-specific.>

## When it does not apply

<Honest scope: when does the principle pay no dividends? E.g. a single-shot completion with no
loop, an internal tool with no untrusted input, a prototype with no real users.>

## Where to read more

<Cite the playbook's `## Grounding` entries.>

## Verification

<Spot-check at least one claim against a cited source; note any place where this explanation
goes beyond the source or simplifies it in ways the audience should know.>

# Test Authoring Design

**Layer:** [unit | integration | …]
**Purpose:** [spec | regression | characterization | exploration | gate]
**Subject under test:** [Name and brief description]

## Behavior to verify

[1–3 sentences describing what observable behavior the test exercises]

## Test outline

```
test_name: [behavior-describing name]

Arrange:
  [setup]

Act:
  [single act]

Assert:
  [single logical assertion or facets of one outcome]
```

## Heuristics applied

- [Named heuristic from layer playbook] — how it's reflected in the outline above

## Failure modes prevented

- [Mode]: how this test design prevents it

## Verification

[How we'll know this test is good: it fails when SUT is broken in obvious ways; it passes in <X ms; etc.]

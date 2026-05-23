# Active Truth Plan: <repo>

Owner: `<repo-or-owner>`
Purpose: `active_truth_plan`
State: `active_plan`
Machine boundary: 本文是人读开发计划与当前真相折返面；机器真相以 contracts、source、tests、CLI/read-model、runtime ledger 和 receipt refs 为准。

## Ideal-State Reference

- Canonical target-state document:
- Target-state summary:
- Non-negotiable invariants:

## Active Owner Discovery

- Existing active truth owner:
- Duplicate or competing active docs to retire:
- Mapping note when this template is folded into an existing plan:

## Current Completion Progress

| Area | Current status | Live evidence | Notes |
| --- | --- | --- | --- |
| <area> | <done / partial / blocked / retired> | <source, contract, test, CLI, receipt ref> | <current truth only> |

## Current-State vs Ideal-State Gaps

### Functional / Structural Gaps

| Gap | Ideal state | Current state | Required change | Owner surface | Evidence |
| --- | --- | --- | --- | --- | --- |
| <gap-id> | <target behavior or structure> | <live observed state> | <change needed> | <doc/code/contract owner> | <source/test/read-model refs> |

### Test / Evidence Gaps

| Gap | Existing implementation state | Missing evidence | Required verification | Foldback target |
| --- | --- | --- | --- | --- |
| <gap-id> | <implemented / partial / unknown> | <test, proof, receipt, soak, read-model> | <commands or receipts> | <active/canonical doc target> |

## Next-Round Agent Prompt

This prompt must be executable as a `/goal` objective or long-running Codex prompt, not a bare TODO list.

Objective:

- <one self-contained objective>

Write scope:

- <files, modules, docs, contracts, tests to change>

Non-goals:

- <surfaces that must not be changed>

Live truth inputs:

- <AGENTS/TASTE/canonical docs>
- <source/contracts/tests/read-model commands>

Required actions:

- <implementation or cleanup action>
- <doc rewrite/foldback action>

Verification commands:

```bash
<repo-native verify command>
```

Completion / foldback gate:

- <closed gaps removed or rewritten in this plan>
- <current facts folded to canonical docs>
- <process material moved to history/tombstone>
- <active path has no completed process packet>
- <next-round prompt only names remaining work>
- <final main checkout verification completed>

## History / Tombstone Foldback

- Process material to archive:
- Retired surfaces to tombstone:
- No-resurrection guard:

## Rewrite Notes

- Do not append dated execution logs.
- Replace obsolete progress and gap rows instead of preserving historical drift.
- Keep closed gaps only as compact history/tombstone pointers when they prevent future semantic pollution.

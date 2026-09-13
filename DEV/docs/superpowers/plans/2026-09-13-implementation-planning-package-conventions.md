# HDM Implementation Planning Package — Conventions

Status: **PB-01 PACKAGE PROTOCOL**
Date: 2026-09-13

Every RD plan must be executable by a fresh coding-worker chat after repository bootstrap, without planner-chat history.

## Required header

```text
Goal:
RD unit:
Direct readiness:
Composite slices/parents:
Pure-proof leaves:
Canonical owners:
Dependencies/joins:
Out of scope:
```

## File actions

Every concrete path carries one action:

- `EXISTING_MODIFY` — correct current owner/surface, edited in place.
- `EXISTING_REPLACE` — useful path remains but v1 contract/implementation is substantially replaced.
- `EXISTING_RETIRE` — obsolete artifact removed after surviving v1 obligations/references are routed elsewhere.
- `NEW_CREATE` — deliberate new owner-native artifact.
- `MOVE_RENAME` — accepted v1 structure requires relocation/rename; references belong in the same impact envelope.
- `INSPECT_ONLY` — relevant surface checked for currentness but not planned to change.

New paths must be intentional and checked against the current tree before implementation.

## GAME classification

`GAME/**` is fully reconstructable for v1.0. Existing layout/content is not a compatibility constraint.

Touched existing GAME artifacts are classified when material as:

- `V1_COMPATIBLE` — current contract remains aligned;
- `MIXED` — surviving v1 obligations coexist with superseded material;
- `LEGACY_SUPERSEDED` — artifact is not a v1 owner and may be replaced/retired after reference and obligation checks.

Never preserve obsolete v0.8 structure merely to minimize a diff. Never retire an old artifact without preserving any current v1 obligation it still carries.

## Dependency notation

- `HARD_PRECEDES` — consumer cannot be correct before predecessor result.
- `JOIN_BEFORE_INTEGRATION` — branches may proceed independently but both must exist before integrated completion/proof.
- `PROOF_AFTER_TARGET` — proof attaches to a realized target.
- `CONSTRAINS_WITHOUT_ORDERING` — accepted law constrains implementation without serializing work.

Numeric RD/readiness order is not dependency evidence.

## Composite/proof closure

A composite canonical parent closes only after all required slices, slice-local proof, required integration proof, parent scenario/negative-law obligations and one parent-level Version Impact reconciliation are complete.

Pure-proof leaves create no standalone production subsystem. They attach to named realized targets.

Every RD plan must say whether each mapped obligation is a direct discharge, composite slice, integration completion, or proof target.

## Currentness and drift

Before correctness-sensitive implementation writes, workers fresh-read current HEAD, package cursor, the RD plan, named owners and every task-specific touched surface.

Mechanical path drift may be adapted if semantics and ownership are unchanged. Drift that changes an owner, invariant, dependency, readiness disposition or material architecture assumption must be routed back to planning/architecture instead of silently changing the plan.

## Worker checkpoints

Plans contain substantial atomic tasks, not hundreds of human prompts. Consecutive tasks may run automatically while prerequisites hold.

A commit is a coherent recoverable checkpoint with focused proof passing: not one commit per assertion and not one giant uncommitted RD block.

Every RD completion records focused/broader verification, readiness accounting, composite contribution, version/checkpoint disposition, stale-reference status and downstream joins.

Production execution remains prohibited until the complete package receives independent Senior PASS / GO.

# HDM Implementation Planning Package — Master Plan

Status: **ACTIVE PACKAGE CONTROL PLANE — PLANNING ONLY**
Date: 2026-09-13

This file controls resumable authoring of the worker-ready implementation-planning package derived from the critic-approved bounded decomposition v2. It does not replace semantic owners, WP-27, `DEV/CURRENT_PROGRESS.md`, or the mandatory independent Senior plan review.

## Fixed invariants

```text
ACTIVE_READINESS: 133
DIRECT: 116
PURE_PROOF: 9
COMPOSITE_PARENTS: 8
TRIGGER_GATED: 12
NO_WORK_TERMINALS: 79
R27_R004: ABSENT
RD_UNITS: 14
OPEN_DECOMPOSITION_FINDINGS: 0
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

## GAME rewrite policy

`GAME/**` may be fully reconstructed for v1.0. Existing files are not preservation constraints and may contain v1-compatible, mixed, or superseded v0.8 material. Detailed plans may create, replace, split, move, rename, or retire GAME artifacts when required by accepted v1 owners and readiness obligations. No legacy field/path/owner is preserved merely to minimize diff size. Any retained v1 obligation carried by an old artifact must survive replacement.

## Atomic planning blocks

- **PB-01 Package protocol** — detailed-plan conventions/template, file-action vocabulary, GAME classification, TDD/verification contract, Impact Envelope contract, worker/checkpoint semantics, package skeleton.
- **PB-02 RD-01..RD-04** — stale projections; information/knowledge/disclosure/message; Actor/Asset/Effect; owner-native routing/index/HOT.
- **PB-03 RD-05..RD-08** — deterministic execution; SAVE/publication; recovery; temporal/thread/current-state.
- **PB-04 RD-09..RD-11** — principal/LIVE currentness; role containment/protected emission; bounded Context Runtime.
- **PB-05 RD-12..RD-14** — multiplayer lifecycle; Story/T0/Commentator/native history; bootstrap/onboarding/product consumers.
- **PB-06 Execution-wave integration** — dependency-derived implementation waves, worker boundaries, composite closure, proof scheduling, version/schema/checkpoint/HG-01 routing, trigger/no-work preservation, currentness revalidation.
- **PB-07 Coverage/currentness closure** — exact readiness-to-task and task-to-owner mapping; 133/133 active, 12/12 trigger-gated, 79/79 no-work, 8/8 composite and 9/9 proof verification; fresh path/interface check; Senior-review handoff.

No separate human approval is required between PB-01..PB-07 unless a genuine architecture/product decision, contradiction, or material risk appears.

## Checkpoints

```text
CP-01 PB-01 package protocol
CP-02 PB-02 RD-01..RD-04
CP-03 PB-03 RD-05..RD-08
CP-04 PB-04 RD-09..RD-11
CP-05 PB-05 RD-12..RD-14
CP-06 PB-06 execution-wave integration
CP-07 PB-07 coverage/currentness + Senior handoff
```

Each block ends with a coherent repository checkpoint and cursor update. A fresh chat must be able to resume from repository state alone.

## Cursor

```text
PLANNING_PACKAGE_STATE: IN_PROGRESS
CURRENT_BLOCK: PB-01
LAST_COMPLETED_BLOCK: NONE
NEXT_AUTHORIZED_BLOCK: PB-01
LAST_CHECKPOINT_COMMIT: d5d625463c32ada3f0a02bdd6cad7cf55bd3eb94
RD_PLANS_COMPLETE: 0 / 14
ACTIVE_READINESS_COVERAGE_CLOSED: 0 / 133
TRIGGER_GATED_PRESERVED: 12 / 12
NO_WORK_PRESERVED: 79 / 79
OPEN_PLANNING_FINDINGS: 0
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

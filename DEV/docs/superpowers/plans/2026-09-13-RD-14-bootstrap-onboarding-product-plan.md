# RD-14 — Bootstrap / Onboarding / Product — Executable Implementation Plan

Goal: realize deterministic v1 bootstrap/onboarding that establishes a valid initial authoritative frontier and projects one aligned product/install flow without resurrecting legacy authority or stale GAME layout.

Direct readiness: `R030,R086,R098,R100`.
Composite slice: `R029.ONBOARDING`.
Owners: bootstrap/product decisions, Actor continuity, Story/T0, collaboration/current-frontier and shipped install projections. RD-03 owns Actor continuity; RD-12 collaboration/frontier; RD-13 Story/T0; RD-09 currentness.

## Impact Envelope

- `NEW_CREATE GAME/TOOLS/bootstrap.py`
- `NEW_CREATE DEV/SCHEMAS/bootstrap-request.schema.json`
- `NEW_CREATE DEV/SCHEMAS/bootstrap-result.schema.json`
- `EXISTING_REPLACE GAME/INSTALL/00_DND_BOOTSTRAP.md`
- `EXISTING_MODIFY GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`
- `EXISTING_MODIFY GAME/INSTALL/README.md`
- `NEW_CREATE DEV/TESTS/test_rd14_bootstrap.py`
- `GAME/CORE/START.md` remains absent; do not recreate as compatibility theater.

Forbidden: bootstrap gameplay before validated initial frontier; hidden default active player; onboarding-owned knowledge/history/currentness; legacy PC/NPC/item authority resurrection; root-relative stale `SESSION/...` writes; instructions diverging from executable machine flow.

## Task 1 — RED: bootstrap preconditions and deterministic result

Create tests for explicit bootstrap request identity/product mode, validated inputs, deterministic stage order and terminal result. Invalid/missing prerequisites fail before gameplay mutation.

Expected RED: no v1 bootstrap orchestrator exists.

## Task 2 — GREEN: request/result contracts and orchestrator skeleton

Implement schemas and `GAME/TOOLS/bootstrap.py` interface equivalent to:
```text
bootstrap(request) -> BootstrapResult
validate_bootstrap_request(request) -> ValidationResult
```

Stages are explicit, typed and idempotence-aware. The orchestrator coordinates owner operations; it does not become their semantic authority.

Commit boundary: request/result + stage machine + tests.

## Task 3 — Actor/onboarding join (`R029.ONBOARDING`, `R030`)

Onboarding creates/associates Actor/controlled-actor state only through RD-03 owner contracts. No knowledge arrays, secret authority or legacy PC/NPC semantic duplication is introduced. Principal/control association consumes RD-09/RD-10 contracts.

Tests cover new participant, existing participant rejoin and invalid duplicate/ambiguous control.

## Task 4 — initial Story/T0/history/current frontier

Bootstrap obtains the initial accepted Story/T0/history basis from RD-13 and currentness from native owners. It verifies a coherent frontier before accepting the first gameplay mutation.

No empty-summary, install prose or transcript can stand in for missing authoritative initialization.

## Task 5 — collaboration/rejoin product path

For multiplayer bootstrap/rejoin, consume RD-12 frontier/catch-up projection. Joining users receive lawful recipient-scoped context before mutation; absence of another participant does not create global waiting unless a positive dependency exists.

## Task 6 — shipped install/bootstrap projections

Rewrite `GAME/INSTALL/00_DND_BOOTSTRAP.md` as the v1 executable flow projection. Align `PROJECT_INSTRUCTIONS.txt` and `README.md` with canonical runtime-root semantics and the same stage order. Do not recreate `GAME/CORE/START.md` merely to satisfy stale historical paths.

Tests/audit fixtures should fail on stale `SESSION/...` root semantics or contradictory bootstrap stage order.

## Task 7 — failure, retry and idempotence

Define terminal success/failure result and safe retry boundaries. A failed pre-mutation bootstrap leaves no partial authoritative world mutation. Post-owner-commit retries use owner idempotence/currentness contracts rather than blind replay.

Tests cover failure before mutation, interrupted owner call, retry and duplicate request identity.

## Task 8 — Version Impact / migration / checkpoint / HG-01

Classify new bootstrap validation contracts and any checkpoint/schema-version effects. BootstrapResult is operational evidence, not a new durable gameplay authority. Migration from legacy GAME bootstrap is replacement-by-v1 contract, not compatibility emulation unless an accepted owner explicitly requires it.

HG-01 implications are evidence-only unless a current owner makes them implementation requirements.

## Task 9 — verification and currentness fence

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd14_bootstrap -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Negative stale proof searches for `SESSION/...` root writes, missing legacy START references, global-active-player defaults, onboarding-owned knowledge/history/currentness and pre-frontier gameplay mutation.

Before implementation/closure fresh-read RD-03/RD-09/RD-12/RD-13, bootstrap/product decisions and all three shipped install surfaces. Owner drift stops execution.

RD-14 closes its four direct leaves and `R029.ONBOARDING`; composite-parent/proof/package closure remains PB-07 work.
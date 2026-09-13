# RD-14 — Bootstrap / Onboarding / Product — Executable Implementation Plan

Goal: realize deterministic v1 bootstrap/onboarding plus product retrospective/save/session-return and creator fail-closed consumers without inventing campaign lifecycle or semantic authority.

Direct readiness: `R030,R086,R098,R100`.
Composite slices: `R029.ONBOARDING`, `R087.SAVE_SESSION_MENU`.
Owners: bootstrap/product decisions, Actor continuity, RD-06 save truth, Story/T0, collaboration/currentness and shipped install projections.

## Impact Envelope
- `NEW_CREATE GAME/TOOLS/bootstrap.py`
- `NEW_CREATE DEV/SCHEMAS/bootstrap-request.schema.json`, `bootstrap-result.schema.json`
- `EXISTING_REPLACE GAME/INSTALL/00_DND_BOOTSTRAP.md`
- `EXISTING_MODIFY GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`, `GAME/INSTALL/README.md`
- `NEW_CREATE DEV/TESTS/test_rd14_bootstrap.py`
- `GAME/CORE/START.md` remains absent; do not recreate.

Forbidden: gameplay before validated initial frontier; hidden global/default active player; onboarding-owned knowledge/history/currentness; context clearing before confirmed save; repository permission or PLAYER stable ID substituting for creator provenance; stale root-relative `SESSION/...` writes.

## Task 1 — RED bootstrap/product preconditions
Tests require explicit request identity/product mode, deterministic stage order, terminal result and no gameplay mutation before valid frontier. Expected RED: no v1 orchestrator.

## Task 2 — GREEN request/result + orchestrator
Implement schemas and `bootstrap(request) -> BootstrapResult`; stages explicit, typed and idempotence-aware. Orchestrator coordinates owners only. Commit boundary: stage machine + tests.

## Task 3 — Actor/onboarding join `R029.ONBOARDING` + R030
Consume RD-03 Actor/provisional shape and RD-09/RD-10 principal/control. No knowledge arrays or legacy PC/NPC authority. Parent R029 later joins RD-06 durability.

## Task 4 — initial Story/T0/history/current frontier
Consume RD-13 accepted T0/history/Story basis and native currentness. Verify coherent frontier before first gameplay mutation; install prose/transcript cannot substitute for missing authority.

## Task 5 — collaboration/rejoin
Consume RD-12 frontier/catch-up. Recipient gets lawful current projection before mutation; absent participants do not cause global waiting without positive dependency.

## Task 6 — `R087.SAVE_SESSION_MENU` / R098
Consume confirmed RD-06 save-success result. Only confirmed success permits session-local context clear/menu return; failed/indeterminate save preserves truthful state and does not pretend completion. Reconcile this branch later with RD-11 retrospective and RD-13 SemanticEvent/T0 branches at R087 parent closure.

## Task 7 — creator provenance R086/R100
Implement creator-only fail-closed consumer path. `RD-09:R078 + RD-14:R086 -> R100`; repository permission, login convenience or PLAYER stable ID never substitutes for creator provenance. Add multiplayer non-interference tests.

## Task 8 — shipped projections
Replace `00_DND_BOOTSTRAP.md`; align project instructions/README to canonical runtime root and machine stage order. Audit stale `SESSION/...` semantics and missing legacy START references.

## Task 9 — failure/retry/idempotence
Pre-mutation failure leaves no partial authoritative mutation. Post-owner-commit retry consumes owner idempotence/currentness, never blind replay. Test interrupted owner call and duplicate request.

## Task 10 — Version Impact/migration/checkpoint/HG-01
Classify new validation contracts and checkpoint/schema effects. BootstrapResult is operational evidence only. Legacy GAME bootstrap is replaced by v1 contract, not emulated absent an owner requirement. HG-01 remains evidence-only unless activated by current owner.

## Task 11 — verification/currentness
Fresh-read RD-03/RD-06/RD-09/RD-11/RD-12/RD-13, bootstrap/product owners and install surfaces. Run focused unittest, maintenance audit and full DEV discovery. Negative stale proof searches stale root writes, global active-player defaults, pre-frontier mutation, premature context clear, creator-login substitution and onboarding-owned authority.

RD-14 closes its four direct leaves and listed slices only. `R029` and `R087` parent closure remains package-level join work.
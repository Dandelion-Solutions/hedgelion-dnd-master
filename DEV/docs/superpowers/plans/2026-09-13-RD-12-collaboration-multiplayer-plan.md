# RD-12 — Collaboration / Multiplayer — Executable Implementation Plan

Goal: realize agency-safe asynchronous collaboration and recipient-scoped multiplayer projections without a global active player, second world, second knowledge authority or global waiting barrier.

Direct readiness: `R021,R044,R081,R082,R083,R121,R123,R141,R142,R143,R146`.
Composite slices: `R016.COLLAB`, `R018.COLLAB`, `R122.COLLABORATION_BRIDGE`.
Owners: R2.5 agency-safe collaboration final spec, WP-17 collaboration decisions, Multiplayer Model. RD-09 owns principal/LIVE/currentness; RD-11 Context Runtime; RD-02 knowledge/disclosure; RD-13 Story/history.

## Impact Envelope
- `NEW_CREATE GAME/TOOLS/collaboration.py`
- `NEW_CREATE DEV/SCHEMAS/collaboration-request.schema.json`
- `NEW_CREATE DEV/SCHEMAS/collaboration-frontier.schema.json`
- `NEW_CREATE DEV/SCHEMAS/catch-up-projection.schema.json`
- `INSPECT_ONLY GAME/SCHEMA/player.schema.yaml`, `GAME/SCHEMA/live_scene.schema.yaml`
- `NEW_CREATE DEV/TESTS/test_rd12_collaboration.py`
- direct project-map/audit projections only.

Forbidden: global active player/current speaker; implicit active-user fallback; universal active-scene set/global waiting barrier; co-presence as dependency; catch-up as history/knowledge; collaboration transport mutating native authority.

## Task 1 — RED identity/scope/dependency
Tests require stable participant identity, finite scope and concrete positive material dependency. Co-presence/turn order/possible future relevance is insufficient. Expected RED: no collaboration runtime.

## Task 2 — GREEN typed collaboration lifecycle
Implement `open_collaboration`, `record_participant_input`, `resolve_waiting` over validated request schema. Identity/control comes from RD-09/RD-10, never prompt order. Commit boundary: request/scope/dependency + tests.

## Task 3 — `R016.COLLAB` / `R018.COLLAB` owner-family integration
Wire only the collaboration-owned portions of the composite parents into their accepted consumer/projection surfaces. Do not absorb information, Actor, execution, Story or routing slices. Add cross-family tests proving one collaboration projection consumes native IDs/contracts without copying their authority.

## Task 4 — scope-local waiting/progress
Wait only while unresolved positive dependency exists in that scope. Unrelated scopes continue; departure/disconnection cannot create global pause. Test independent scopes, absent participant, resolved dependency and no-dependency progress.

## Task 5 — current frontier join/rejoin
Compose the smallest owner-derived frontier before new mutation. Consume RD-09 currentness, RD-02 disclosure/knowledge, RD-11 context and RD-13 history/Story hints where eligible; own none.

## Task 6 — catch-up recipient projection
Implement `build_catch_up(...) -> CatchUpProjection`. Projection is disclosure-safe/reconstructible and cannot replay as SemanticEvent, world mutation or knowledge grant.

## Task 7 — `R122.COLLABORATION_BRIDGE`
Create bridge evidence only for a concrete material dependency. RD-08 chronology, RD-09 currentness and RD-11 context consume it; no universal shared frontier follows. Test bounded creation/removal.

## Task 8 — multiplayer authority negatives
Prove divergent lawful recipient projections over one canon, private-disclosure isolation, late-input non-retroactivity absent a new accepted mutation, and collaboration metadata inability to override eligibility/currentness/requiredness.

## Task 9 — Version Impact/checkpoint
Classify new schemas and direct projections. Any checkpointed collaboration state is operational coordination only and references native owner IDs/currentness. No compatibility shim for global-active-player semantics.

## Task 10 — verification/currentness
Fresh-read R2.5, Multiplayer Model, RD-02/RD-09/RD-10/RD-11/RD-13 and inspected player/LIVE schemas. Run focused unittest, maintenance audit and full DEV test discovery. Negative stale proof searches global active player/waits, co-presence dependency, catch-up authority and collaboration-owned canon.

RD-12 closes its direct leaves and listed slices only. `R016`, `R018`, `R122` parent closure remains package-level join work.
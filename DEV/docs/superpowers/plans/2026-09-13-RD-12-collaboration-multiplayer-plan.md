# RD-12 — Collaboration / Multiplayer — Executable Implementation Plan

Goal: realize agency-safe asynchronous collaboration and recipient-scoped multiplayer projections without a global active player, second world, second knowledge authority or global waiting barrier.

Direct readiness: `R021,R044,R081,R082,R083,R121,R123,R141,R142,R143,R146`.
Composite slice: `R122.COLLABORATION`.
Owners: R2.5 agency-safe collaboration final spec, WP-17 collaboration decisions, Multiplayer Model. RD-09 owns principal/LIVE/currentness; RD-11 owns Context Runtime; RD-02 owns knowledge/disclosure; RD-13 owns Story/history projections.

## Impact Envelope

- `NEW_CREATE GAME/TOOLS/collaboration.py`
- `NEW_CREATE DEV/SCHEMAS/collaboration-request.schema.json`
- `NEW_CREATE DEV/SCHEMAS/collaboration-frontier.schema.json`
- `NEW_CREATE DEV/SCHEMAS/catch-up-projection.schema.json`
- `INSPECT_ONLY GAME/SCHEMA/player.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/live_scene.schema.yaml`
- `NEW_CREATE DEV/TESTS/test_rd12_collaboration.py`
- direct project-map/audit projection updates only.

Forbidden: global active player/current speaker authority; implicit active-user fallback; universal active-scene set; global waiting barrier; physical presence as eligibility; disconnected participant blocking unrelated work; catch-up as canonical history/knowledge; collaboration transport mutating world/knowledge/Story authority.

## Task 1 — RED: identity, scope and positive dependency

Create tests proving every collaboration request identifies stable principal/participant identities, scope and the concrete positive material dependency that requires another participant. Mere co-presence, turn order, scene membership or possible future relevance is insufficient.

Expected RED: no collaboration runtime exists.

## Task 2 — GREEN: typed collaboration request and scope

Implement `collaboration.py` interfaces equivalent to:
```text
open_collaboration(request) -> CollaborationState
record_participant_input(state, input) -> CollaborationState
resolve_waiting(state) -> WaitingDecision
```

Validate `collaboration-request.schema.json`. Scope is explicit and finite. Participant identity/control is consumed from RD-09/RD-10 contracts, never inferred from prompt order.

Commit boundary: request/scope/dependency validation + tests.

## Task 3 — scope-local waiting and progress

Waiting is permitted only while an unresolved positive material dependency exists in that collaboration scope. Unrelated scopes continue. Departure/disconnection removes impossible waits according to owner rules; it never creates a global pause.

Tests cover two independent scopes, absent participant, resolved dependency and no-dependency non-waiting.

## Task 4 — current frontier for join/rejoin

Implement `collaboration-frontier.schema.json` and a read-only frontier composition path. A joining/rejoining participant receives the smallest current owner-derived frontier needed before any new mutation is accepted.

Frontier composition consumes RD-09 currentness, RD-02 disclosure/knowledge, RD-11 context projection and RD-13 history/Story hints where eligible. It owns none of them.

## Task 5 — catch-up as recipient projection

Implement `catch-up-projection.schema.json` and:
```text
build_catch_up(participant, frontier, eligible_history) -> CatchUpProjection
```

Projection is recipient-specific, disclosure-safe and reconstructible. It cannot be replayed as a new SemanticEvent stream, world mutation or knowledge grant.

## Task 6 — `R122.COLLABORATION` bridge

Cross-scope collaboration exists only for a concrete positive dependency. RD-12 supplies the collaboration bridge/scope evidence consumed by RD-08 chronology, RD-09 currentness and RD-11 context slices. No unit may infer a universal shared frontier from this bridge.

Tests prove bridge creation, bounded scope and removal after dependency resolution.

## Task 7 — multiplayer authority negatives

Add adversarial tests proving:
- two participants can hold different lawful projections of one canon;
- one participant cannot obtain another's private disclosure merely through collaboration;
- late input cannot retroactively rewrite an already committed authoritative result unless an owner-defined new mutation path accepts it;
- collaboration metadata cannot override eligibility/currentness/requiredness.

## Task 8 — integration / Version Impact / checkpoint

Run focused tests, maintenance audit and full DEV test discovery. Version Impact classifies the three new validation contracts and project-map/audit projections. No new durable gameplay authority is introduced; if collaboration state is checkpointed, it is operational coordination state only and must reference native owner IDs/currentness rather than copy their semantic payloads.

No compatibility shim is created for a global-active-player model.

## Task 9 — verification and currentness fence

Before implementation and before closure fresh-read R2.5, Multiplayer Model, RD-02/RD-09/RD-10/RD-11 and exact inspected player/LIVE schemas. Stop on semantic-owner drift.

Required commands:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Negative stale proof searches for global-active-player/current-speaker fallbacks, global waits, co-presence-as-dependency, catch-up authority and collaboration-owned knowledge/history/world state.

RD-12 closes only its direct leaves and `R122.COLLABORATION`; composite-parent/package closure remains PB-07 work.
# Domain Rules Coverage and Minimal Gameplay Spine

Status: **CANONICAL — S6D-09 STEPS 1–8 COMPLETE / SPATIAL CONFORMANCE REPAIRED**

Date: 2026-08-27

## 1. Authority and scope

This owner defines the supported reusable mechanic boundary of the built-in bounded MVP and the proof that product promises, identity-bound package content and active machine consumers reconcile. It does not own RNG, world state, Procedure persistence, Asset state, Activity execution, adjudication policy or primitive semantics; those remain with their cited owners.

The supported spine is generic typed check/save, minimal initiative/turn/action/movement Procedure, bounded target/range/area applicability for exact seed consumers, significant Asset transfer/equip/use, domain lowering for social/hazard/reward fiction, and the exact S6D-07/08 routes. Natural-language player actions are not enumerated.

## 2. Completeness law

The machine companion derives three finite sets from current owners:

```text
PACKAGE_CLOSURE_KEYS
ACTIVE_MACHINE_CONSUMER_KEYS (including every primitive -> exact consumer edge)
PRODUCT_PROMISE_KEYS

REQUIRED_COVERAGE_KEYS = union of those sets
COVERAGE_LEDGER_KEYS == REQUIRED_COVERAGE_KEYS
```

Every source key has exactly one ledger row and route. Every ledger key originates in a source set. Every active edge resolves to both an active primitive row and an identity-bound package Activity. Differences, duplicates, orphans, unresolved references and `SUPPORTED_GAP` rows fail validation.

## 3. Generic check/save

`activity.check.generic` binds one of six package abilities, optionally one of the two package skill proficiencies, and a bounded integer DC. `activity.save.generic` binds one of the same six abilities and a bounded integer DC. Ability/proficiency bindings are `ENGINE_BOUND`; DC may be one frozen `INVOCATION_ADJUDICATED` value with provenance/currentness. The Activities compile only through `op.roll` plus `op.resolve_check` or `op.resolve_save`.

The Activities end at typed outcome. They contain no consequence payload, rule expression, query, patch or mutation language. Any damage, location or Asset consequence is a separately admitted exact owner transition. A valid result may be Mechanical-Null: it has no authoritative world mutation, while the genuine `event.check.resolved` or `event.save.resolved` required by the selected primitive and the receipt remain. No StateDelta lifecycle or additional synthetic mutation event is introduced.

## 4. Procedure, movement and space

`procedure.combat_minimal` owns lifecycle (`between_turns|turn_active|terminated`), participants, fixed initiative order/tie resolution, round/turn cursor, explicit round-advance-pending state and per-participant `resource.action_budget` / `resource.movement_budget`. Encounter may reference but never duplicate these fields. Initialization consumes one fixed RNG-result reference, roll total and unique tie rank per participant; retry reuses that accepted evidence and cannot respin order.

The seven declared transitions are exact: initialize, start turn, spend action, spend movement, end turn, advance round and terminate. All seven use the closed Procedure request/result schemas and replace exactly the pinned `runtime.procedure.state` in one segment with `event.procedure.state_changed` plus a receipt. `procedure.spend_movement` spends budget without asserting a durable location transition. The event payload binds profile, field path, before/after revision and exact after-state digest. Start/end phase, active participant, action/movement capacity, last-turn round gate, revision and idempotency are fail-closed.

Durable budgeted movement is a separate `location_change.procedure_movement` route. It validates pinned Procedure and Actor revisions plus the identity, kind, canonical minimum state and current revision of a destination `world.location`, then commits exactly one ExecutionSegment containing both movement-spent and Actor-location changes. Partial commit is forbidden. Outside-Procedure durable location change is a separate one-owner profile with movement cost explicitly N/A and the same destination validation. `Actor.location_id` names a durable world location; it is not a tactical micro-position.

Target/range/area applicability is a separate Mechanical-Null calculation route, never an alias for Procedure/movement. Seven exact `op.select_targets` consumers declare a strict `TargetSpec` (and `AreaSpec` where needed), receive a finite invocation-bound candidate-role list, and require one accepted `fiction.target_reachable` boolean per source/consumer/spec/candidate/spatial-provenance binding. Missing is a typed failure; false is distinct from missing. Accepted fact values and their provenance/binding/rules-context fingerprints remain fixed with accepted work, but create no independent lifecycle or persistent spatial truth. `fiction.target_visible` remains dormant and generic visibility/cover remains out of scope.

Within-location repositioning such as “behind the pillar”, “near the door” or “beside the table” remains fiction plus `procedure.spend_movement`; it creates no fake `world.location` and does not mutate `Actor.location_id`. If one of the seven exact supported Activities needs the relation for applicability, the accepted fact boundary carries that exact current invocation judgment. There is no pathfinding, collision simulation, universal coordinate model, global geometry query or campaign scan.

## 5. Significant Assets

Transfer clears the current exclusive owner/container/location placement and sets exactly one new placement in one Asset-owned segment. Equip uses admitted `transition.asset_status` and changes only `world.asset.state.equipment.mode` to `held|worn`. Use is validation-only and returns a typed `NONE` or exact admitted `activity_id` binding for the normal Activity invocation owner; it neither executes nor discards that Activity and is not a generic transition or consequence payload.

No inventory aggregate, currency ledger, pricing/market, crafting or economy authority is introduced. `op.transfer_asset` remains dormant because these consumers use the existing direct owner transition.

## 6. Failure, retry and evidence

Same idempotency key plus same fingerprint reuses the recorded result. A different fingerprint rejects with `failure.idempotency_conflict`. A stale pinned Actor/Asset/Procedure revision rejects before prospective mutation with admitted `failure.state_revision_conflict`. Movement-budget overrun uses existing `failure.action_economy_scope_invalid`. Failure emits no event and commits no owner partially.

ExecutionSegment owns commit disposition, MechanicalEvent owns a committed fact when one exists, and receipt owns result/evidence. Retry never rerolls, respins initiative or repeats transfer.

## 7. Domain lowering and open play

```text
player expression
-> GM fictional interpretation and feasibility
-> bounded typed adjudication only when required
-> generic check/save or existing exact route
-> optional separately admitted deterministic consequence
```

Social and hazard uncertainty reuse check/save. Reward/gift/loot ownership reuses Asset transfer. Absence of an action-specific Activity or primitive is not a gap unless a scenario proves a distinct reusable mechanical consequence or authority boundary.

## 8. Explicit negative space

Contest-specific resolution, generic reaction, broad damage-defense, generic concentration, currency economy, crafting/downtime, teleportation, zones/entity creation, and broad equipment/spell/hazard corpora remain absent/nonselectable. The decision activates no dormant primitive.

## 9. Architecture acceptance walkthrough

A player tries to persuade a guard. Fiction determines feasibility and supplies a bounded DC; `activity.check.generic` produces a fixed, retry-safe outcome, which may be Mechanical-Null. The party then crosses a falling-stone hazard; `activity.save.generic` reuses the same resolution spine and failure may lower to the existing exact damage route. The PC walks from a canonical room to a canonical corridor: one segment validates the pinned destination, spends Procedure movement and changes Actor location. Moving behind a pillar within the room instead spends only Procedure movement and stays fictional unless an exact Activity consumes a fixed invocation-adjudicated applicability fact; no pillar location is created. Hostility starts the minimal Procedure and existing S6D-07/08 attack/spell/health routes run without a generic reaction engine. The guard later grants a significant item; the same Asset transfer used for gift or loot changes exclusive ownership without a reward engine.

## 10. Machine and package companions

- `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/gameplay-spine-seed.json`
- `DEV/CATALOG/domain-rules-coverage.json`
- `DEV/CATALOG/activity-primitive-contracts.json`
- `DEV/SCHEMAS/domain-rules-coverage.schema.json`
- `DEV/SCHEMAS/gameplay-spine-seed.schema.json`
- `DEV/SCHEMAS/combat-minimal-procedure-state.schema.json`
- `DEV/SCHEMAS/combat-procedure-transition-request.schema.json`
- `DEV/SCHEMAS/combat-procedure-transition-result.schema.json`
- `DEV/SCHEMAS/procedure-state-changed-event.schema.json`
- `DEV/SCHEMAS/gameplay-spine-transition-request.schema.json`
- `DEV/SCHEMAS/gameplay-spine-transition-result.schema.json`
- `DEV/TOOLS/validate_domain_rules_coverage.py`
- `DEV/TESTS/test_s6d_09_domain_rules_coverage_contract.py`

Production execution remains Implementation Planning work. S6D-11 performs integrated package/catalog verification, not deferred product or architecture design.


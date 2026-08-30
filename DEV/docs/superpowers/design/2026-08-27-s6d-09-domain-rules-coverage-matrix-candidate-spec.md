# S6D-09 — Minimal Playable Gameplay Spine and Domain Coverage — Candidate Specification

Status: **STEP 5 ACCEPTED / CANONICALIZED BY STEP 8**

Date: 2026-08-27

## 1. Decision and authority

The built-in MVP supports a minimal reusable gameplay spine sufficient for ordinary open-ended adventure play. This specification owns the supported-surface boundary and coverage proof. It does not replace the semantic owners it cites, create a runtime registry, or activate a primitive by assertion.

## 2. Supported spine

The supported reusable mechanics are identity-bound by `gameplay-spine-seed.json` in the selected package:

1. `activity.check.generic` and `activity.save.generic`;
2. one minimal initiative/turn/action/movement Procedure profile;
3. bounded TargetSpec/AreaSpec/spatial bindings required by supported Activities;
4. direct typed significant-Asset ownership/equip/use/transfer transitions;
5. hazard/social/reward lowering through those routes;
6. the exact S6D-07/08 character, attack, spell, HP/LifeState, Resource, Effect, recovery, READY_PC and advancement routes.

No player utterance, fictional maneuver or example becomes a coverage key.

## 3. Generic check/save contract

Each Activity has a closed declaration with:

```text
actor role
ability_id from the six package-admitted abilities
optional proficiency_id from the two package-admitted skill proficiencies (check only)
threshold: integer, ENGINE_BOUND or INVOCATION_ADJUDICATED by declaration
advantage_state: closed existing selector input or explicit N/A
```

Execution is:

```text
validated bindings
-> selector check.roll | save.roll
-> op.roll fixed RollResult
-> op.resolve_check | op.resolve_save
-> receipt outcome/export
-> zero or one separately validated existing-owner consequence route
```

The Activity ends at its typed check/save result. It contains no consequence payload. A caller may separately choose only an already admitted route classified as `NONE`, `EXACT_DAMAGE`, `EXACT_LOCATION_CHANGE` or `EXACT_ASSET_TRANSFER`; that classification is not a payload language. Missing threshold/basis/provenance is typed failure. Retry reuses the accepted binding identity and fixed roll.

An outcome may produce `NO_AUTHORITATIVE_WORLD_MUTATION`. In that case the segment, Resolution and receipt remain exact, while no StateDelta or MechanicalEvent is fabricated unless a current event contract genuinely requires the event.

## 4. Minimal Procedure profile

`runtime.procedure` owns exactly:

```text
procedure_kind = procedure.combat_minimal
lifecycle_state = between_turns | turn_active | terminated
participant_ids: finite unique set
initiative_order: exact permutation of participant_ids with fixed tie resolution
round_number >= 1
round_advance_pending: boolean
active_turn_index
participant_resources[participant_id][resource.action_budget|resource.movement_budget]
world_context_id when applicable
```

Procedure transitions are closed: initialize, start turn, spend action, spend movement, end turn, advance round and terminate. `combat-minimal-procedure-state.schema.json` closes the profile without narrowing other Procedure classes; `combat-procedure-transition-request.schema.json` and `combat-procedure-transition-result.schema.json` close the six Procedure-owned controls, while spend movement maps to the already closed two-owner movement profile. Initialization accepts exactly one fixed RNG-result reference, roll total and unique tie-break rank per participant and derives the order deterministically. Start/end phase, active actor, action capacity, last-turn round gate, revision and idempotency fail closed. Each Procedure-owned control replaces exactly the pinned Procedure state in one segment, emits registered `event.procedure.state_changed` with profile/revision/after-state digest and a receipt, and cannot mutate Actor HP/Asset/Effect state. `world.encounter` may reference the Procedure but does not own its cursor or budgets.

No generic reaction resource/window is supported until an exact consumer proves necessity.

## 5. Movement and spatial contract

Movement is a direct deterministic TransitionRequest, not an Activity primitive:

```text
transition_kind = transition.location_change
target_actor_id
destination_ref
movement_cost within current Procedure budget, or explicit N/A outside a Procedure
spatial_basis_refs drawn only from the closed engine-bound reference set
```

The validator checks authoritative current location/Procedure state, destination identity, budget and currentness. The S6D-09 MVP accepts only engine-bound Actor/Scene/Zone/TargetSpec/AreaSpec references. It does not activate dormant `fiction.target_visible`, `fiction.target_reachable` or any equivalent adjudicated spatial fact. A later exact consumer that genuinely needs such a fact must amend its owning S6D-04 contract first.

Inside a combat Procedure, movement commits as exactly one ExecutionSegment over two owners: it advances `runtime.procedure.participant_resources[actor_id].resource.movement.spent` and changes `world.actor.state.location_id`. Both pinned revisions are validated, partial commit is forbidden, and retry reuses the recorded outcome. Outside a Procedure, an admitted location transition omits Procedure mutation and requires an explicit profile that declares movement cost N/A.

The contract expresses bounded destination/relative placement needed by current play. It provides no path search, collision simulation, universal coordinates, line-of-sight engine, global geometry query or campaign-wide scan.

**Senior-audit spatial repair supersession.** The preceding Step-5 statements that map every movement spend to the two-owner location transition, accept engine-bound spatial references only, or keep `fiction.target_reachable` dormant are superseded. `procedure.spend_movement` now spends only Procedure budget and supports fictional within-location repositioning without changing `Actor.location_id`. A durable room-to-corridor transition separately validates pinned Procedure/Actor revisions plus the ID, kind, canonical minimum state and revision of the destination `world.location`. Target/range/area applicability is a distinct Mechanical-Null route: seven exact existing `op.select_targets` Activities declare strict TargetSpec/AreaSpec values and consume fixed `fiction.target_reachable` facts bound to consumer, source role, spec, candidate, spatial provenance and pinned rules context. `fiction.target_visible` remains dormant. No primitive is newly activated and no geometry/query engine is introduced. The repaired canonical owner and Step-6→8 repair artifacts control where this original candidate text differs.

## 6. Asset transitions

The existing `world.asset` owner is used. Closed direct transition profiles are:

```text
transition.asset_transfer: exactly world.asset.state.owner_actor_id/container_asset_id/location_id
asset.equip profile over transition.asset_status: exactly world.asset.state.equipment.mode = held|worn
asset.use binding: validate ownership/access/definition capability; NONE or EXACT_ADMITTED_ACTIVITY only
```

Transfer validates the pinned Asset revision and current placement, clears the old placement and sets exactly one new exclusive owner/container/location in one ExecutionSegment. Equip validates the same owner and changes only `equipment.mode`. Use is a validation-only binding step: `NONE` returns an explicit no-activity binding; `EXACT_ADMITTED_ACTIVITY` returns the exact admitted `activity_id` as a typed binding that the normal Step-3 Activity invocation path must consume. The binding step itself is Mechanical-Null and cannot silently execute, discard or replace the Activity. It has no generic consequence payload. Equip/use cannot grant capabilities absent from `definition.asset`. No aggregate inventory, currency account, market/pricing engine or generic patch payload is introduced.

`op.transfer_asset` remains dormant because the current consumers are direct transitions, not compiled Activity steps.

## 7. Domain lowering

- social uncertainty uses generic check/save; durable relationship/knowledge/contract consequences require their existing owners and are not implied by success;
- hazard uncertainty uses generic check/save; exact damage/Effect/location/resource consequences use existing routes;
- reward item transfer uses `world.asset` plus `transition.asset_transfer`;
- creative actions are interpreted into these existing routes or remain fiction/automatic/impossible; absence of an action-specific primitive is not a gap.

## 8. Primitive activation result

No dormant primitive is activated by S6D-09. The S6D-06 owner and machine catalog are amended in place so the existing active primitives add only the two identity-bound exact consumer IDs:

```text
op.roll           <- activity.check.generic, activity.save.generic
op.resolve_check  <- activity.check.generic
op.resolve_save   <- activity.save.generic
```

All other primitive dispositions remain unchanged.

## 9. Supported and excluded matrix

The machine ledger derives and stores exact `PACKAGE_CLOSURE_KEYS`, `ACTIVE_MACHINE_CONSUMER_KEYS` including consumer edges, and `PRODUCT_PROMISE_KEYS`. Product keys come from strict atomic evidence rows (`key`, current owner path, exact evidence pattern, qualifier, scope and route), not from a hand-maintained composite checklist; a missing owner or evidence pattern fails validation. Their union equals the one-row-per-source-key coverage ledger in both directions; orphan edges, duplicates, unresolved references, differences and supported gaps are all required to be empty.

`IN_SUPPORTED_MVP`:

- resolution classification, fixed RNG and retry evidence;
- generic check/save;
- minimal Procedure and movement;
- bounded supported spatial inputs;
- basic significant Asset transitions;
- hazard/social/reward lowering;
- exact S6D-07/08 routes;
- Mechanical-Null: for the two admitted generic Activities, no authoritative world mutation is produced, while the exact `event.check.resolved` or `event.save.resolved` required by the selected primitive and the receipt are preserved. No synthetic mutation event or StateDelta lifecycle is added.

`OUT_OF_SUPPORTED_MVP_SEED` by the accepted owner decision:

- contest-specific resolution;
- generic reaction primitive;
- broad damage-defense and concentration content;
- currency economy;
- crafting/downtime;
- teleportation;
- zone/entity creation;
- broad/full equipment, spell and hazard corpora.

Revisit only when a concrete supported consumer proves a distinct reusable consequence or authority boundary that the spine cannot express.

## 10. Failure, retry and concurrency

All routes use existing Step-3 typed failure, Resolution/TransitionRequest, segment, receipt, idempotency and revision semantics. Stale bindings, Procedure revision conflicts and Asset placement races fail closed. Exact retry returns the stored result; it does not reroll, respin initiative or repeat transfer.

Multiplayer shared Procedure/Asset transitions validate the pinned current revision and publish according to existing race-sensitive owner rules. No new global epoch or lock owner is introduced.

## 11. Required machine realization

S6D-09 materializes now, as authoritative architecture-level machine contracts and owner amendments:

- identity-bound package member `gameplay-spine-seed.json` and updated aggregate package digest;
- exact S6D-06 primitive consumer-list amendment for the two Activities;
- `DEV/CATALOG/domain-rules-coverage.json`: exact three source sets, one-row-per-key ledger, atomic routes and zero-difference proof;
- `DEV/SCHEMAS/domain-rules-coverage.schema.json`: fail-closed schema for every machine-owned member;
- strict gameplay-spine, combat-Procedure and transition request/result schemas;
- `DEV/TOOLS/validate_domain_rules_coverage.py`: semantic cross-member validator;
- `DEV/TESTS/test_s6d_09_domain_rules_coverage_contract.py`: positive and negative closure tests.

S6D-11 must re-run the integrated package/catalog suite, but it does not own deferred activation of these already admitted consumers. Production runtime execution remains Implementation Planning work. This is not permission to implement the runtime before that stage.

## 12. Cross-system impact

Depends on: S6D-01…08, Step-3/5 execution/retry/recovery, House Rules typed adjudication, current world/procedure owners.

Constrains: S6D-10 typed ruling integration, S6D-11 package/test realization, S6D-12 integrated audit, later runtime implementation.

Owns: supported-surface classification and coverage evidence only.

May mutate: nothing by itself; cited owner transitions retain authority.

No migration is required because no released campaign uses catalog generation 2.0.0.


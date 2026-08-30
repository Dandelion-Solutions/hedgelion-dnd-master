# S6D-09 Spatial Conformance Repair — Step 6 Whole-Project Review

Status: **PASS — 0 BLOCKING / 0 SIGNIFICANT / 0 MINOR**

Date: 2026-08-27

## Repair boundary

This repair responds only to the Senior Auditor HOLD on false spatial coverage and movement-location currentness. Decision C and Step 3 product scope are unchanged. S6D-10 remains not started.

## Corrected ownership split

1. `route.procedure_movement` owns Procedure control, movement-budget spend and an optional durable `world.actor.state.location_id` transition. A durable transition requires a pinned canonical `world.location` snapshot whose ID, kind, canonical minimum state and revision match the request.
2. `route.spatial_target_applicability` owns the Mechanical-Null pre-commit target/range/area calculation for seven exact existing `op.select_targets` consumers. It consumes exact TargetSpec/AreaSpec constraints, finite candidate roles and fixed accepted `fiction.target_reachable` facts. It performs no mutation and emits no event of its own.
3. `procedure.spend_movement` owns within-location reposition budget only. Fiction such as “behind the pillar” does not mint a `world.location` or mutate Actor location. A supported Activity may consume the exact invocation fact only for its current applicability decision.

## Fact admission

`fiction.target_reachable` is `ACTIVE_ADMITTED` only for:

- `activity.attack.ranged_weapon`;
- `activity.spell.fire_bolt`;
- `activity.spell.poison_spray`;
- `activity.spell.thunderclap`;
- `activity.spell.acid_splash`;
- `activity.spell.magic_missile`;
- `activity.spell.burning_hands`.

Each accepted boolean binds the exact consumer, compiled source role, TargetSpec/AreaSpec, candidate role, stable spatial-provenance reference and rules-context fingerprint. Missing is not false. The fact remains accepted causal input only while the accepted work is live; it does not become durable spatial truth or gain a lifecycle. `fiction.target_visible` remains `DORMANT_RESERVED`; generic visibility/cover remains explicitly out of scope.

## Exact machine repairs

- seven existing Activities now declare strict bounded TargetSpec values and pass source/candidate/fact bindings to the existing `op.select_targets` contract;
- `op.select_targets` no longer claims an unowned `geometry_and_reachability` infrastructure read;
- the invocation-fact envelope is strict about consumer, binding and rules-context fingerprints;
- active fact/consumer edges enter the zero-difference matrix and resolve to the dedicated spatial route;
- durable movement requests include `destination_location_revision` and reference execution validates a canonical destination snapshot;
- `world.location` minimum state has a fail-closed canonical schema branch and world-record routing;
- `procedure.spend_movement` is closed across request/result/event schemas and reference execution;
- package member and aggregate identities are refreshed.

## Required critic graph

The whole-project critic must inspect direct and indirect relations through at least:

- `DEV/PROJECT_MAP.md` and the current roadmap;
- S6D-04 `MECHANICAL_CONTEXT.md` and `mechanical-surfaces.json`;
- S6D-05 `PORTABLE_ACTIVITY_VALUES.md`, TargetSpec/AreaSpec and invocation-fact schemas;
- S6D-06 primitive owner/catalog/compiler tests;
- S6D-07 character seed owner/package/READY_PC evidence;
- S6D-09 owner, Decision C, product evidence and zero-difference matrix;
- `ENTITY_STRUCTURES.md`, Actor and world-record/location schemas;
- COMBAT/ADJUDICATION/PLAY_POLICY open-ended-play law;
- Step-3 execution/event/receipt/idempotency and currentness owners.

Blocking/significant findings must be repaired before Step 7. The critic must specifically reject any hidden geometry engine, fake micro-location, unbound fact reuse, player-action vocabulary, new primitive authority or unsupported expansion of visibility/cover.

## Pre-critic verification

The focused S6D-06…09 suite passes 58/58 tests. S6D-02 full import remains unavailable in this workspace because the external `jsonschema` dependency is absent; no S6D-02 files are changed by this repair.

## Critic result and repairs

The first renewed whole-project review found one BLOCKING and one SIGNIFICANT issue:

1. the rules-context fingerprint existed in the fact envelope but was not yet compared with the pinned accepted rules context or included in binding identity;
2. the original Step-4/5 documents still stated that reachability remained dormant.

Both were repaired. Selection now requires the expected pinned rules-context fingerprint, compares it before selection, includes it in the binding fingerprint, rejects stale/cross-context and unbound facts, and proves identical fixed-fact retry. The candidate and collaborative-review documents immediately and explicitly supersede their old spatial statements.

The renewed critic returned **PASS — 0 BLOCKING / 0 SIGNIFICANT / 0 MINOR** after checking the complete dependency graph named above. It confirmed canonical minimum `world.location` alignment, durable destination currentness, within-location Procedure-only spend, seven exact fact consumers, missing distinct from false, package identity closure, and the absence of spatial lifecycle/world truth, geometry/query/scan/action vocabulary or new primitive activation.


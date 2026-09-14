# Implementation Planning — MechanicalEvent Identity Reconciliation Addendum

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 10 — SIGNIFICANT**

## Finding

The canonical Step-3 execution owner defines committed MechanicalEvent identity from the accepted execution edge: one event is identified by its stable `segment_id` plus stable `event_ordinal`. The current `runtime-mechanical-event-state.schema.json` already requires those two fields, but `DEV/CATALOG/identifier-policies.json` still classifies `runtime.mechanical_event` as campaign-scoped sequential allocation.

RD-05 requires accepted identities to survive retry but does not plan the identifier-policy cutover. This is a three-surface half-cutover:

```text
canonical semantic identity: (segment_id, event_ordinal)
state machine shape:         segment_id + event_ordinal present
identifier policy:           unrelated campaign sequential allocator   # stale
```

A worker following the current package could therefore allocate a second surrogate event identity, make retries depend on allocator state, or produce different event IDs for the same already accepted segment/ordinal.

## Required v1 identity disposition

`runtime.mechanical_event` MUST use the existing composite-key identity mechanism with the exact ordered semantic key:

```text
strategy = composite_key
fields   = [segment_id, event_ordinal]
scope    = campaign
```

The physical printable `id` may deterministically encode/frame that tuple, but no second allocator-generated semantic identity is admitted.

This is preferable to the existing generic `derived(parent_kind, suffix)` shape because `ExecutionSegment` is an embedded protocol value, not one `runtime.*` record kind, and a segment may belong to a Resolution or a direct-transition RuntimeCommand. The tuple already is the canonical complete identity.

Consequences:

- `runtime.mechanical_event` never participates in `runtime.id_allocator`;
- retry/recovery of the same committed `(segment_id,event_ordinal)` yields the same event identity;
- different ordinals in one segment are distinct;
- identical ordinals under different segments are distinct;
- ID lexical/numeric order carries no chronology/currentness meaning;
- LIVE absorption/retry cannot rekey an accepted MechanicalEvent;
- source-native LIVE identity, when required for an independently allocated parent execution owner, propagates through the stable `segment_id`; MechanicalEvent itself does not receive a second `source_native_live` surrogate.

## RD amendments

### RD-05 — execution identity owner

Extend `AcceptedIdentityTests` / `LifecycleEvidenceTests` with exact cases proving:

```text
mechanical_event_id == deterministic_encode(segment_id, event_ordinal)
```

at the semantic level, including retry of a committed segment, multiple events in one segment and direct-transition segments. RD-05 owns the semantic identity rule and produces the exact policy disposition consumed by the coordinated machine-policy integration.

The execution runtime must construct/validate the identity from the accepted segment + ordinal rather than requesting campaign allocation.

### RD-04 — allocator / identifier-policy integration

At the coordinated R018 identity-policy integration checkpoint:

- change `runtime.mechanical_event` in `DEV/CATALOG/identifier-policies.json` from sequential to composite key `[segment_id,event_ordinal]`;
- ensure `DEV/SCHEMAS/identifier-policies.schema.json` accepts/requires this exact policy for `runtime.mechanical_event`;
- update catalog/inventory/audit projections that currently describe it as sequential;
- extend `CampaignAllocatorTests` to reject `runtime.mechanical_event` allocation;
- prove native route construction uses the complete tuple identity and no directory/index enumeration.

This shared-file edit is sequenced with the `world.player` and WP-16 identity-policy repairs; independent workers must not race edits to `identifier-policies.json` or its schema.

### RD-07 — recovery

Retained accepted MechanicalEvent evidence is recovered by the same stable tuple identity. Recovery never allocates a replacement event ID because allocator state moved or because the accepted segment is read from LIVE versus campaign authority.

### RD-09 — LIVE composition

WP-16 `source_native_live` policy applies only to independently allocated LIVE-born owners. `runtime.mechanical_event` is classified as `OWNER_EQUIVALENT_COMPOSITE`: its stable identity remains the Step-3 `(segment_id,event_ordinal)` tuple. A LIVE-born source-native parent Resolution/Command identity, where admitted, makes the derived segment namespace collision-free without a second MechanicalEvent allocator.

## Proof / R018 amendments

`R018.EXECUTION` cannot close merely because the MechanicalEvent schema/root exists. Family-level closure requires:

```text
runtime.mechanical_event
-> admitted runtime kind
-> state schema with segment_id/event_ordinal
-> composite identifier policy [segment_id,event_ordinal]
-> LOG/MECHANICAL_EVENTS native route
-> RD-05 accepted event producer
-> RD-06 durability publication
-> RD-07 stable recovery
-> item-bound identity/retry proof
```

Add a negative proof that a sequential `event-000123` allocator policy is stale and cannot be accepted as an alternative identity layer.

## Version / migration disposition

This is an unreleased v1 machine-contract reconciliation. Legacy v0.8 preservation is not a constraint. Do not add a compatibility alias, dual-ID period or migration shim solely to retain the stale sequential policy. Apply the normal Version Impact Gate to the actual v1 catalog/schema change when implemented.

## Disposition

```text
AUTHOR_GRAPH_FINDING_10: REPAIRED_IN_PLANNING
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```

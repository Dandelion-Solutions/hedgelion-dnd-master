# HDM Implementation Planning — Scene LIVE Route Repair Addendum

Status: **CURRENT MANDATORY EXECUTION OVERLAY**
Date: 2026-09-14
Production implementation authorized: **NO**.

This overlay repairs the shipped `GAME/SCHEMA/scene.schema.yaml` consumer gap identified by the author post-SIRR2 investigation. It changes no semantic owner and creates no new readiness identity.

## RD-08 / RD-09 shared physical surface

`GAME/SCHEMA/scene.schema.yaml` is touched by two existing owners:

- RD-08/WP-15 owns removal/demotion of singleton chronology-frontier semantics;
- RD-09/WP-16 owns LIVE route/currentness projection semantics.

Use `SHARED_FILE_CHECKPOINT` ordering only:

```text
RD-08 scene chronology checkpoint
-> publish GREEN scene chronology result
-> RD-09 fresh-read exact scene.schema.yaml bytes
-> RD-09 apply LIVE-route narrowing without restoring RD-08 debt
```

This physical order transfers no semantic ownership.

## RD-09 executable scene-route task

Add the following exact action to RD-09 after typed claim/currentness machinery exists and after the RD-08 scene checkpoint when both touch this file:

**Files**
- Modify: `GAME/SCHEMA/scene.schema.yaml`.
- Modify: `DEV/TESTS/test_rd09_access_live.py`.
- Consume: current `GAME/SCHEMA/live_scene.schema.yaml`, `GAME/TOOLS/live_state.py`, WP-16 typed claim/currentness contract.
- Re-run RD-08 scene/chronology focused witness after the edit.

**RED class:** `SceneLiveRouteProjectionTests`.

Required cases:

```text
test_scene_live_pointer_is_route_nomination_not_scene_wide_authority
test_unclaimed_owner_remains_campaign_authority
test_scene_membership_and_references_do_not_expand_live_claims
test_closed_unabsorbed_claim_has_zero_writers_without_campaign_fallback
test_scene_route_requires_exact_selected_source_currentness
test_scene_schema_preserves_rd08_chronology_retirement
```

The suite is RED while the shipped scene schema permits `live_epoch` presence, scene membership, participant membership, references or co-location to imply authority over the entire scene or all mutable participants/entities.

**GREEN rules**

1. `live_epoch` is route nomination metadata only; it does not create a scene-wide semantic owner.
2. Current write authority for each target native owner/partition resolves through the admitted typed claim set and bounded `WriteAuthorityLookup`.
3. An unclaimed native owner remains campaign-routed even when the same scene has an active LIVE source for other claims.
4. `EXACT_OWNER` does not expand through scene/entity references.
5. `EPOCH_LOCAL_CREATION` grants only the admitted native creation family; it does not grant authority over existing records.
6. Owner-defined partitions remain legal only when their native owner already defines bounded deterministic partition semantics.
7. A selected ACTIVE LIVE source is current/writable only for admitted claims and only after application authorization plus exact-source currentness validation.
8. A selected `CLOSED_UNABSORBED` source remains current truth for its admitted claims with zero ordinary writers. Campaign base is not fallback for those claims.
9. Route-away/absorption validates the exact terminal selected source revision before forward authority movement.
10. Preserve the RD-08 chronology result; do not restore `chronology_frontier_event_id` as generic singleton chronology authority.

**Focused verification**

```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.SceneLiveRouteProjectionTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.LiveEnvelopeClaimTests DEV.TESTS.test_rd09_access_live.LiveCurrentnessTests DEV.TESTS.test_rd09_access_live.LiveLifecycleTests -v
python3 -m unittest DEV.TESTS.test_rd08_temporal.TemporalMachineAlignmentTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Expected GREEN before the coherent scene-schema checkpoint is publication-eligible.

## Version Impact

Current shipped scene contract is local `scene_state schema_version: 2`.

The RD-08 chronology retirement and RD-09 LIVE-route semantic narrowing are one coordinated breaking pre-v1 scene-contract replacement:

```text
scene_state schema_version: 2 -> 3
```

Increment the local scene schema exactly once for this coordinated published result. Do not add a pre-v1 compatibility alias solely to preserve the superseded shape. Execution still performs the normal Version Impact Gate for aggregate campaign-contract/storage consequences and stops on version-owner drift.

## Proof / coverage consequence

The following package proof cannot close without this shipped scene projection witness:

- WP-15 scene chronology: RD-08 owner witness plus RD-09 preservation assertion;
- WP-16 typed claim/write-authority duties: machine claim tests plus `SceneLiveRouteProjectionTests`;
- WP-16 selected-source/recovery matrix: exact-source tests plus scene route nomination semantics;
- `R018.LIVE`: `live_scene.schema.yaml` realization plus shipped scene routing projection.

This addendum changes planning instructions only. It performs no runtime implementation, migration, release or gameplay bootstrap.

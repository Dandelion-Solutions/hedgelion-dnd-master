# Implementation Planning — LIVE Opening / Routing / Native-State Handoff Addendum

Status: **MANDATORY OVERLAY — AUTHOR FINDINGS 28–31 REPAIR / INDEPENDENTLY UNCONFIRMED**

Date: 2026-09-14
Production implementation: **NO**.

This overlay has higher precedence than RD-09 Tasks 3–7 and Findings 24–27 wherever those artifacts leave candidate preparation idempotency, initial owner-state seeding, completeness-protected LIVE claim routing, or native-state LIVE packing / absorption materialization unspecified.

It changes no semantic owner and introduces no new historical readiness identity. It is delegated machine realization under Step-5.8, Step-5.13, WP-11 and WP-16.

---

## 1. Finding 28 — prepared LIVE candidate idempotency / acknowledgement ambiguity

**Severity: SIGNIFICANT.**

Finding 27 intentionally makes one complete immutable opening basis derive one deterministic `epoch_id` and therefore one exact physical LIVE ref. The package does not yet define what a fresh opening worker does when that target ref is already present or when preparation of that ref had an indeterminate acknowledgement.

Branch/ref existence is not authority, and Step-5.13 does not permit classifying a non-current ref as orphan merely because current campaign routing does not select it. A worker therefore may not solve this by deleting/recreating the ref, by adding a random suffix, by forcing over the ref, or by treating existence as successful opening.

### 1.1 Frozen opening preparation attempt

RD-09 shall expose an ephemeral value equivalent to:

```text
FrozenLiveOpeningAttempt {
    repository_identity
    campaign_ref
    pinned_opening_campaign_revision
    campaign_id
    scene_id
    canonical_immutable_claims
    epoch_id
    target_live_ref
    expected_initial_live_state_fingerprint
    acting_principal / authorization basis
}
```

This is operation evidence only, not a persistent journal, lock, lease, authority owner or retry queue.

### 1.2 Preparation classification

Candidate preparation against the deterministic target ref shall yield a typed result equivalent to:

```text
PREPARED_NEW
REUSED_EQUIVALENT_PREPARED
ALREADY_SELECTED_EQUIVALENT
CONFLICTING_EXISTING_SOURCE
INDETERMINATE
```

Required rules:

1. If no target candidate exists and preparation is confirmed, the source is `PREPARED_NEW` and remains non-authoritative until campaign route selection accepts.
2. If the exact ref already resolves to a structurally valid candidate whose complete semantic/opening basis and initial state are exactly equivalent to the frozen attempt, the worker may reuse it as `REUSED_EQUIVALENT_PREPARED`; reuse grants no authority.
3. If current campaign routing already selects that exact complete opening basis/ref and the selected source validates, classify `ALREADY_SELECTED_EQUIVALENT`; do not create a second epoch.
4. An existing source at the deterministic ref with incompatible campaign/scene/epoch/opening revision/claim set/initial-state basis is `CONFLICTING_EXISTING_SOURCE` and blocks as integrity/repair. Do not overwrite, alias or suffix it.
5. After indeterminate candidate preparation, exact-ref observation and full basis/state validation reconcile the original attempt before another logical opening may be prepared.
6. After indeterminate campaign route selection, reconcile campaign authority first. Do not infer failure from candidate non-selection at one stale read and do not prepare a replacement epoch until current campaign authority is established.
7. Definite stale/rejected campaign selection refreshes the campaign basis; a new logical attempt recomputes the epoch identity from the new basis.

Prepared-source cleanup remains Step-5.13 owner-gated maintenance. Runtime opening never deletes or rewrites an uncertain existing ref merely to make progress.

### 1.3 F28 tests

Add RD-09 `LiveOpeningPreparationTests` covering at minimum:

- two identical opening attempts converge on one deterministic candidate ref;
- equivalent existing prepared candidate is reusable but non-authoritative;
- current route selecting the exact candidate is idempotent success, not duplicate opening;
- incompatible existing candidate at the deterministic ref blocks;
- candidate-preparation lost acknowledgement is reconciled before another prepare;
- route-selection lost acknowledgement is reconciled before another epoch attempt;
- no random suffix, force replacement, delete/recreate or branch-existence authority path exists;
- prepared-orphan cleanup is not an opening operation.

---

## 2. Finding 29 — exact initial campaign-to-LIVE owner-state seeding

**Severity: SIGNIFICANT.**

The package defines exact opening identity/claims but does not require the prepared LIVE source to contain state equivalent to the current native owners at the pinned opening campaign revision. Once campaign routing selects the LIVE epoch, campaign copies for claimed owners become base/reference state rather than current truth; a wrongly seeded LIVE candidate would therefore become wrong current truth immediately.

### 2.1 Seed law

For one opening basis `H` and immutable claim set `Q`:

```text
pin exact campaign revision H
-> resolve every existing claimed owner/partition through its native direct route at H
-> hydrate and validate its exact native state at H
-> construct initial LIVE native-state representation only from those pinned values
-> validate initial LIVE state equivalence
-> only then permit candidate preparation / campaign route selection
```

Rules:

1. `EXACT_OWNER` claims seed exactly the named owner state from `H`; references do not expand the seed set.
2. `OWNER_DEFINED_PARTITION` seeds exactly the owner-defined deterministic member/state closure admitted by that partition contract. If bounded complete materialization cannot be produced, opening blocks.
3. `EPOCH_LOCAL_CREATION` grants future creation admission only. It seeds no fabricated owner at opening.
4. Read-only/reference dependencies needed by the seeded owners remain dependencies under their native owners; they are not copied into LIVE merely because they were read.
5. Initial seed validation is basis-sensitive: mixed reads from different campaign revisions are forbidden.
6. Current campaign movement before route selection triggers bounded revalidation. If the opening basis is no longer accepted, refresh/rebuild rather than silently carrying stale owner state into a new epoch.
7. The initial LIVE representation may use the v1 packing selected by Finding 31, but any packing must prove native-state equivalence and preserve native identity/owner semantics.

### 2.2 F29 tests

Add RD-09 `LiveOpeningSeedTests`:

- exact-owner initial state equals direct native owner state at pinned `H`;
- changing current owner state after `H` cannot be silently mixed into the `H` candidate;
- partition seed is complete according to the admitted owner partition adapter;
- unbounded/unencodable partition seed blocks;
- `EPOCH_LOCAL_CREATION` creates no initial owner;
- unrelated referenced owners are not implicitly claimed/copied;
- campaign movement before selection causes revalidation/rebuild, not stale adoption;
- route selection refuses a candidate whose initial native-state fingerprint/equivalence proof does not match the frozen opening basis.

RD-06 campaign route-selection integration must reject selection when the F29 initial-state validation required by the frozen opening attempt is not satisfied.

---

## 3. Finding 30 — completeness-protected campaign LIVE routing

**Severity: SIGNIFICANT.**

WP-16 requires bounded `WriteAuthorityLookup(X) -> CAMPAIGN | LIVE | INTEGRITY_CONFLICT`. The base RD-09 plan accepts abstract `campaign_routing`, while the scene repair correctly demotes `scene.live_epoch` to route nomination/projection only. No current plan provides a completeness-protected campaign source capable of proving that an owner is unclaimed without scanning LIVE refs or trusting an incomplete projection.

The v1 realization follows the already accepted completeness-companion pattern used by temporal and principal routing.

### 3.1 Fixed campaign-domain route companion

Create:

```text
<state_root>/RUNTIME/LIVE_ROUTING.yaml
# default scaffold path:
STATE/RUNTIME/LIVE_ROUTING.yaml
```

plus a strict validation contract, conceptually:

```text
DEV/SCHEMAS/live-routing.schema.json
```

The file is derivative current routing evidence only. It is not a native gameplay owner, scene owner, authorization owner, new MANIFEST selector, global scheduler, lease table or copy of native owner state.

A valid blank campaign contains an explicit empty routing set. Missing/invalid/basis-incompatible routing is never interpreted as “no LIVE claims”.

### 3.2 Route entry

Conceptual entry:

```text
LiveRouteEntry {
    campaign_id
    scene_id
    epoch_id
    target_live_ref
    opening_campaign_revision
    immutable_claims[]
}
```

The exact schema may carry the additional bounded identity/currentness fields required by Findings 27–29, but it must not copy native owner payloads, player authorization grants, fictional chronology, source-local mutation payloads, or current LIVE revision as campaign semantic authority.

### 3.3 Completeness law

For every current selected ACTIVE or CLOSED_UNABSORBED LIVE epoch, exactly one current entry exists in `LIVE_ROUTING.yaml`. Absorbed/nonselected/prepared-only sources do not appear as current selected routes.

Campaign publication that selects, replaces, absorbs or releases LIVE authority updates the companion in the **same campaign authority transaction** as the corresponding route/claim authority change. Healthy durable state cannot expose current selected LIVE authority without the matching current companion or a companion entry for a nonselected source.

### 3.4 Bounded lookup

`lookup_write_authority(target_owner, current_live_routing, ...)` uses the validated complete table and owner-specific claim-membership logic:

```text
no matching current claim
    -> CAMPAIGN
exactly one matching selected claim
    -> resolve exact selected LIVE source -> LIVE(...)
multiple/overlapping/incompatible matches
    -> INTEGRITY_CONFLICT
```

Absence may nominate `CAMPAIGN` only when the route table itself is proven current/complete for the pinned campaign basis.

`scene.live_epoch`, `CURRENT.active_scenes`, family indexes, ref names, directories, caches and checkpoints may nominate/discover but cannot prove claim absence.

### 3.5 Source-native owner lookup

A parseable F24 `source_native_live` ID may nominate its originating semantic `(campaign_id, scene_id, epoch_id)` for bounded lookup, but parsed ID contents are not routing authority.

While that epoch remains selected, current validated `LIVE_ROUTING.yaml` plus exact selected source establishes LIVE authority for the applicable current owner. After confirmed absorption/route release, the same stable owner ID direct-routes in campaign native storage. No accepted ID rekeys.

### 3.6 Publication / recovery / scaffold joins

- **RD-06:** route companion delta joins the same campaign resulting tree as LIVE route selection/release/absorption; no acknowledged split route/table state.
- **RD-07:** cold recovery loads current `LIVE_ROUTING.yaml`, exact-resolves selected sources, validates route/body/opening basis, then hydrates current native owners. Missing/corrupt routing is scoped integrity/repair, not a broad LIVE-ref scan fallback.
- **RD-14:** blank v1 scaffold includes valid empty `STATE/RUNTIME/LIVE_ROUTING.yaml`; this creates no live epoch and no gameplay prerequisite.
- **scene projection:** `scene.live_epoch` remains optional nomination/projection only and may never replace the complete table.

### 3.7 F30 tests

Add RD-09 `LiveRoutingCompletenessTests` proving:

- every selected ACTIVE/CLOSED_UNABSORBED route appears exactly once;
- current valid empty table can prove no LIVE claim;
- missing/invalid/stale table cannot prove CAMPAIGN authority;
- selected-route/table split is rejected by RD-06 publication proof;
- exact-owner claim lookup is bounded without ref/directory scan;
- overlapping current claims produce integrity conflict;
- scene pointer/index/current summaries cannot prove absence;
- source-native ID parsing nominates but never authorizes;
- absorption removes the selected route only in the campaign transaction that makes campaign current for the affected owners;
- old physical LIVE ref presence after absorption has no authority.

---

## 4. Finding 31 — v1 native-state packing and lossless LIVE-to-campaign absorption

**Severity: SIGNIFICANT.**

The package removes the legacy scene/entity-overlay mega-owner model but does not select a replacement v1 physical representation for current native owner state inside LIVE. Consequently three required paths are not worker-executable:

1. Finding 29 campaign `H` -> initial LIVE seed;
2. RD-07 selected-LIVE native owner hydration;
3. CLOSED LIVE -> campaign absorption with lossless native state and stable IDs.

WP-16 explicitly permits one-file physical packing when native owners and durability edges remain intact. v1 therefore selects one typed packed-envelope baseline.

### 4.1 LIVE native-state entries

The final `LIVE_STATE` contract contains a collection equivalent to:

```text
native_state_entries[] {
    native_family
    identity_components[]
    representation_kind
    state
}
```

Exact field spelling is implementation detail; semantics are not.

Required rules:

1. Each entry is one native owner record or one already-admitted owner-defined partition projection. LIVE is physical packing, not a semantic mega-owner.
2. Native identity uses the same complete owner identity components and family contract as campaign direct routing.
3. Entry state validates against the final native family schema/adapter. Shared strict world-family dispatch is consumed from RD-16 where applicable.
4. `EXACT_OWNER` opening entries are seeded from exact `H` under Finding 29.
5. `EPOCH_LOCAL_CREATION` entries appear only in the exact accepted LIVE CAS that establishes the new native owner; F24–F26 final ID allocation is part of that same accepted edge where applicable.
6. Owner-equivalent derived/composite identities retain their native identity; they do not gain a surrogate LIVE identity.
7. No entry ordering conveys chronology, priority, currentness or allocation authority.
8. Native owner relationships/references remain references; packing does not recursively copy the object graph.
9. Presence/absence of an entry does not invent generic deletion semantics. Native terminality and later retirement remain owner/Step-5.13 governed. When no owner-specific deletion/survivor contract exists, fail-retain.
10. Information/history/Story ownership remains unchanged; a physical entry may carry only the native owner's admitted state/evidence.

The legacy generic `scene_overlay`, `entity_overlays`, `created_entities[].provisional_id` and “base campaign + arbitrary patch” model is not the v1 semantic baseline.

### 4.2 Native mutation

One accepted LIVE native durability edge materializes a complete next `LIVE_STATE` whose affected `native_state_entries` are valid under their native owner contracts plus all required derivative companions embedded in the LIVE source (for example temporal routing when applicable).

A high-level user action may still span multiple native establishment edges. One-file packing does not merge owner atomicity merely for serialization convenience.

### 4.3 Recovery

RD-07 selected-LIVE recovery:

```text
current campaign LIVE route
-> exact selected LIVE ref/revision
-> full route/body/opening validation
-> validate every required native_state_entry against native family/identity contract
-> validate F24–F26 source-native identities/cursor where applicable
-> rebuild derivative state only after native hydration
-> READY
```

Campaign copies for currently claimed owners are not fallback current truth.

### 4.4 Frozen absorption materialization

After exact selected source reaches terminal CLOSED revision `Lf`, RD-09/RD-06 jointly realize a deterministic forward absorption plan equivalent to:

```text
FrozenLiveAbsorption {
    campaign_basis
    selected_live_route
    exact_final_live_revision = Lf
    exact_final_claim_set
    exact validated native_state_entries
    required information/history normalization outputs
    required derivative routing/index deltas
    final campaign path delta
    live_route_removal
}
```

RD-09 owns LIVE/native handoff interpretation; RD-06 owns campaign publication mechanics.

Required behavior:

1. Validate exact CLOSED `Lf` and complete native-state packing before campaign mutation.
2. For every claimed existing owner, materialize its exact final native state into its normal campaign native route.
3. For every accepted live-born owner that survives owner semantics, publish it under the same already accepted stable native ID; no campaign allocator/rekey.
4. Include required index/routing/protection/currentness companions in the same campaign resulting-tree closure where their owners require coherence.
5. Material owner evidence that must be normalized under RD-02/RD-13 or another native owner completes before route-away when loss would otherwise occur.
6. Remove/rewrite current LIVE route evidence only in the campaign transaction that establishes the campaign-native successor truth for those claims.
7. A source marked CLOSED but not yet absorbed remains `CLOSED_UNABSORBED` selected truth with zero ordinary writers.
8. Campaign publication rejection/ambiguity never reopens the LIVE epoch or reruns accepted mechanics. Reconcile/retry from the same exact `Lf` and frozen native identities unless current campaign movement invalidates the absorption assumptions.
9. A confirmed accepted absorption is idempotent by exact final source/native IDs/current campaign closure: lost acknowledgement must not duplicate live-born owners, events, effects or information normalization.
10. Physical predecessor ref cleanup is later Step-5.13 maintenance and is not part of authority transfer.

### 4.5 RD-16 integration boundary

RD-09 may define the generic native-state entry envelope/adapter contract before RD-16 final shared machine integration. Final package closure waits for RD-16 strict family dispatch so all applicable world entries validate against the accepted 17-family machine contract.

This is a checkpoint join, not a whole-RD cycle:

```text
RD09 source-native identity / LIVE owner-local packing core
    -> RD16 shared machine integration
    -> RD09 LIVE_NATIVE_PACKING_FAMILY_VALIDATION_READY
```

RD-16 does not gain LIVE semantic authority.

### 4.6 F31 tests

Add RD-09 `LiveNativeStatePackingTests`:

- exact-owner entry round-trips native identity/state without scene mega-owner semantics;
- unrelated referenced owner is not copied;
- source-native live-born record enters under final accepted ID in the accepting CAS;
- owner-equivalent composite identity receives no surrogate;
- entry order has no semantic meaning;
- absence is not generic deletion;
- strict family mismatch blocks.

Add RD-09/RD-06 `LiveAbsorptionMaterializationTests` integration cases:

- exact CLOSED owner state reaches normal campaign route losslessly;
- live-born canonical IDs remain unchanged;
- required companion deltas and route removal share the accepted campaign closure;
- failed/indeterminate absorption leaves CLOSED_UNABSORBED current truth;
- lost acknowledgement reconciles without duplicate owner/event/effect creation;
- campaign conflict rebuilds transport basis without replay/reroll of accepted LIVE semantics when owner dependencies remain compatible;
- no Git merge, branch merge, generic YAML merge, provisional rekey or campaign allocator participates.

RD-07 extends selected-LIVE recovery tests with strict native-state packing validation.

---

## 5. File impact

Mandatory execution-time surfaces, subject to fresh currentness:

```text
RD-09
  MODIFY GAME/TOOLS/live_state.py
  REPLACE/MODIFY GAME/SCHEMA/live_scene.schema.yaml
  MODIFY DEV/SCHEMAS/live-claim.schema.json
  MODIFY DEV/SCHEMAS/live-publication-attempt.schema.json
  CREATE DEV/SCHEMAS/live-routing.schema.json
  MODIFY DEV/TESTS/test_rd09_access_live.py

RD-06
  MODIFY GAME/TOOLS/publication.py
  MODIFY DEV/TESTS/test_rd06_durability_publication.py

RD-07
  MODIFY GAME/TOOLS/recovery.py
  MODIFY DEV/TESTS/test_rd07_recovery.py

RD-14
  CREATE GAME/CAMPAIGN/STATE/RUNTIME/LIVE_ROUTING.yaml
  MODIFY DEV/TESTS/test_rd14_bootstrap.py

RD-16
  CONSUME final native-family strict schemas/dispatch for LIVE native-state validation
```

`STATE/RUNTIME` is already required by mandatory temporal/principal routing overlays; F30 adds another fixed operational companion under the existing `state_root` and requires no new MANIFEST root selector.

Do not introduce a global LIVE owner, generic ACL/currentness service, second native-record registry, branch scanner, scheduler, lease, distributed transaction, universal tombstone registry or campaign allocator fallback.

---

## 6. Execution checkpoints / dependency graph amendment

Add owner-local checkpoints:

```text
RD09_LIVE_OPENING_PREPARATION_READY       # F28
RD09_LIVE_OPENING_SEED_READY              # F29
RD09_LIVE_ROUTING_READY                   # F30 campaign routing producer/consumer logic
RD09_LIVE_NATIVE_PACKING_CORE_READY       # F31 owner-local packing core
```

Campaign selection integration:

```text
RD09_LIVE_EPOCH_ROUTE_IDENTITY_READY
+ RD09_LIVE_OPENING_PREPARATION_READY
+ RD09_LIVE_OPENING_SEED_READY
+ RD09_LIVE_ROUTING_READY
+ RD06 campaign publication foundation
    JOIN_BEFORE_INTEGRATION
LIVE_OPENING_SELECTION_READY
```

Shared family validation:

```text
RD09_LIVE_NATIVE_PACKING_CORE_READY
+ RD16 SHARED_MACHINE_INTEGRATION
    JOIN_BEFORE_INTEGRATION
RD09_LIVE_NATIVE_PACKING_FAMILY_VALIDATION_READY
```

Absorption integration:

```text
RD09_LIVE_NATIVE_PACKING_FAMILY_VALIDATION_READY
+ RD09 exact CLOSED source/lifecycle
+ required RD02/RD13 normalization outputs where material
+ RD06 campaign publication
    JOIN_BEFORE_INTEGRATION
LIVE_ABSORPTION_READY
```

RD-07 selected-LIVE recovery waits only for the specific route/packing/identity checkpoints it consumes. No whole-project or whole-RD serial barrier is introduced.

The graph remains acyclic at checkpoint level because RD-16 consumes the earlier RD-09 source-native/live-birth input already required by Findings 24–26, while the later RD-09 family-validation checkpoint consumes RD-16's final strict dispatch.

---

## 7. Proof routing

Add post-graph rows:

```text
PG28 prepared LIVE candidate idempotency / ambiguity reconciliation
PG29 exact campaign-H -> initial LIVE native-state equivalence
PG30 completeness-protected campaign LIVE route lookup
PG31 typed LIVE native-state packing + lossless/idempotent forward absorption
```

Required owner-local/integration witnesses:

```text
PG28 -> RD-09 LiveOpeningPreparationTests
PG29 -> RD-09 LiveOpeningSeedTests + RD-06 route-selection seed-validation cases
PG30 -> RD-09 LiveRoutingCompletenessTests + RD-06 route/table publication join + RD-07 recovery + RD-14 blank scaffold
PG31 -> RD-09 LiveNativeStatePackingTests + LiveAbsorptionMaterializationTests + RD-06 campaign publication integration + RD-07 selected-LIVE recovery + RD-16 strict-family validation
```

Primary channels: `FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT`.

No row closes from test-name existence alone.

---

## 8. Version / clean-slate disposition

These changes define unreleased v1 LIVE machine realization. Legacy pre-v1 overlay/provisional forms are not compatibility targets.

At implementation time compute one final local LIVE schema transition after composing Findings 24–31 and all earlier SIRR2/scene/temporal changes. Do not bump the same schema independently once per overlay.

The new campaign `LIVE_ROUTING.yaml` is a v1 derivative operational companion under existing `state_root`; run the normal Version Impact Gate for its schema/template addition. No compatibility migration is created solely for pre-v1 absence.

Planning-only publication changes DEV planning/control documentation only.

---

## 9. Disposition

```text
AUTHOR_FINDING_28: SIGNIFICANT / REPAIRED_IN_PLANNING
AUTHOR_FINDING_29: SIGNIFICANT / REPAIRED_IN_PLANNING
AUTHOR_FINDING_30: SIGNIFICANT / REPAIRED_IN_PLANNING
AUTHOR_FINDING_31: SIGNIFICANT / REPAIRED_IN_PLANNING
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```

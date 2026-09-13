# RD-04 — Owner-Native Routing / Index / HOT — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. This plan authorizes no production work until the independent Senior plan gate passes.

Goal: realize deterministic native-family routing, campaign allocator operation, rebuildable non-authoritative indexes and a typed native-owner HOT/SQLite substrate without creating new semantic/currentness/chronology authority.

RD unit: `RD-04`
Direct readiness: `R015,R063,R064,R065,R066,R067`.
Composite slices/parents: `R018` route/root integration only after each implicated native owner shape is finalized.
Canonical owners: WP-10 allocation item 7; WP-11 physical storage topology/identity/indexing; WP-12 HOT/SQLite/transaction realization; Step-5.1 allocator semantics; exact Step-2 records.
Dependencies/joins: consumes finalized native owner shapes from RD-02/RD-03 and later RD-05/RD-08/RD-09/RD-12/RD-13 at integration; does not serialize independent semantic work.
Out of scope: gameplay semantics, global transaction manager, publication timing/ref protocol, recovery source selection, LIVE claim semantics, automatic writer partitioning, generic ID registry/service.

## Implementation Impact Envelope

SPEC / APPROVED DESIGN: WP-10 item 7, WP-11, WP-12, Step-5.1 §10, exact readiness records.
BASELINE REF: fresh branch HEAD at execution.

EXPECTED OWNERS TO CHANGE:
- shipped storage/routing/HOT implementation;
- campaign allocator operational representation;
- location reverse-presence projection required by R015.

EXPECTED CONSUMERS TO CHANGE:
- native owner loaders/creators using campaign sequential IDs;
- derived family indexes;
- later RD-06 publication conflict handling consumes allocator evidence;
- later owner families consume route/HOT primitives.

ALLOWED INTERFACES / CONTRACTS TO CHANGE:
- `GAME/TOOLS/native_storage.py`;
- `GAME/TOOLS/id_allocator.py`;
- `GAME/TOOLS/hot_store.py`;
- `GAME/SCHEMA/index.schema.yaml`;
- `GAME/SCHEMA/id_allocator.schema.yaml`;
- `GAME/SCHEMA/location.schema.yaml` only for R015 reverse-presence removal; RD-02 owns its epistemic-field cleanup;
- `GAME/CAMPAIGN/STATE/ID_ALLOCATOR.yaml`;
- exact DEV machine contracts/tests/audit/project-map projections named below.

PROTECTED ARCHITECTURE INVARIANTS:
- semantic identity is owner-defined; route/hash/index/rowid never creates identity;
- `runtime.id_allocator` / `campaign-allocator` is the sole campaign sequential-allocation authority;
- allocator state is not a progress/currentness/frontier authority;
- allocation + record creation is one atomic HOT operation;
- eligible local/source-native IDs never fall back to campaign allocation;
- published IDs are never rekeyed/reused;
- current presence has one native owner; Location carries no reverse authoritative presence list;
- indexes/caches are rebuildable and non-authoritative.

ARCHITECTURE-SENSITIVE SURFACES: allocator atomicity, record identity, HOT transaction scope, publication conflict handoff, source-native LIVE IDs.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD-02/RD-03 family routes, RD-06 allocator conflict/republication, RD-07 no allocator rewind, RD-09 source-native LIVE IDs.
KNOWN OUT-OF-SCOPE: semantic entity creation rules, publication CAS protocol, LIVE allocation policy, Story allocation, migration/release execution.

Version Impact: classify actual schema/API/storage contract delta at every task checkpoint. No version impact is assumed from filename/diff size.
HG-01: constraint 3 only; absence of old HOT implementation does not create new semantic architecture.

## Shared-file coordination

`GAME/SCHEMA/location.schema.yaml` is also an RD-02 epistemic cleanup surface. Do not run independent writes concurrently. The coherent sequence is:
1. RD-04 removes only `state.present_entity_ids` and the invariant that could treat it/index state as mobile-entity authority;
2. RD-02 applies its separately owned `known_fact_ids` / `secret_ids` cleanup against the resulting current file;
3. one later integration check verifies both changes survive.

This is shared-file coordination, not an owner dependency between RD-02 and RD-04.

## Task 1 — RED: native route vectors and authority negatives

**Files**
- Create: `DEV/TESTS/test_rd04_native_routing_index_hot.py`
- Create in Task 2: `DEV/SCHEMAS/native-route.schema.json`
- Create in Task 2: `GAME/TOOLS/native_storage.py`

**Produces**
```text
route_native_record(family_key: str, identity_components: tuple[str, ...]) -> str
validate_loaded_identity(family_key, identity_components, document) -> None
```

**RED cases**
- fixed `HDM-WP11-ROUTE-V1` vectors, including `world.knowledge(knower_id,fact_id)` and `runtime.disclosure(player_id,fact_id)`;
- component order matters and is owner-defined;
- loaded body family/identity mismatch is integrity failure;
- known-ID read needs no directory/index enumeration;
- path/hash/index cannot establish body identity or currentness.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.NativeRouteTests -v
```
Expected RED: shipped route implementation is absent.

Checkpoint: none; RED-only work is not published as a completed task.

## Task 2 — GREEN: deterministic native route implementation

**Files**
- Create: `GAME/TOOLS/native_storage.py`
- Create: `DEV/SCHEMAS/native-route.schema.json`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`
- Modify: `DEV/TESTS/test_rd04_native_routing_index_hot.py`

**Consumes**: exact owner-defined family key/root/complete identity.
**Produces**: the two Task-1 interfaces.

Implement exact framing/hash/base32hex/chunk law. Exceptional fixed routes (`MANIFEST`, config/card/current, allocator, LIVE, Story) are explicit and are not routed through the native-record hash function. `native_storage.py` consumes IDs and must never allocate them.

GREEN command:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.NativeRouteTests -v
```
Expected GREEN: route vectors, direct-read and identity-integrity cases pass.

REFACTOR: framing/encoding helpers remain private to `native_storage.py`; no second path/identity module.

VERIFY:
```bash
python3 DEV/TOOLS/run_maintenance_audit.py
```

Coherent checkpoint: route implementation + route schema + vector tests + audit/project-map projection. No unrelated allocator/index/HOT half-change in this commit.

## Task 3 — R063 campaign allocator: positive realization and atomic record creation

**Files**
- Create: `GAME/TOOLS/id_allocator.py`
- Create: `GAME/SCHEMA/id_allocator.schema.yaml`
- Create: `DEV/SCHEMAS/campaign-id-allocator-state.schema.json`
- Create: `GAME/CAMPAIGN/STATE/ID_ALLOCATOR.yaml`
- Modify: `GAME/TOOLS/hot_store.py` when Task 6 creates it; if Task 3 executes first, implement the allocator transaction adapter in `id_allocator.py` against the explicit HOT transaction port defined below and complete the binding in Task 6 before RD-04 closure.
- Modify: `DEV/TESTS/test_rd04_native_routing_index_hot.py`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`

**State contract**
```text
CampaignAllocatorState {
  id: "campaign-allocator"
  last_allocated: map[identity_policy_key, nonnegative_integer]
}
next(policy) = last_allocated[policy] + 1  # derived, never persisted as authority
```
Only policies whose current catalog identity strategy is campaign-scoped `sequential` participate. Composite, derived, singleton, session-local and source-native policies do not.

**Interfaces**
```text
load_campaign_allocator(pinned_campaign_basis) -> CampaignAllocatorState
allocate_and_stage_record(
    hot_tx,
    policy_key,
    validated_record_factory,
) -> AllocatedRecord
rekey_unpublished_conflicts(
    hot_tx,
    stale_allocator_state,
    current_allocator_state,
    unpublished_record_set,
) -> RekeyResult
```

`validated_record_factory(allocated_id)` is supplied by the semantic owner and returns an already owner-valid candidate body. The allocator selects only the campaign ID and atomically stages allocator advancement + new record + required local direct references/index-dirty evidence inside one permitted HOT transaction. It does not decide whether a semantic record should exist.

**RED cases**
- missing singleton initializes only through the bootstrap/scaffold contract, never by guessing from existing largest IDs;
- `last_allocated` advances by the selected registered sequential policy and formatting uses catalog prefix/minimum width;
- allocator advance without staged record creation rolls back;
- staged record creation without allocator advance rolls back;
- local/session/source-native/derived/composite/singleton policies are rejected by campaign allocator;
- LIVE-created source-native Message/execution IDs never fall back to campaign allocator;
- published IDs cannot be rekeyed/reused;
- stale publication reconciliation rekeys only conflicting unpublished records and direct local refs, then returns control to RD-06 publication retry; it does not rewrite accepted published identity or chronology;
- allocator counter order is not chronology/currentness.

Run RED:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.CampaignAllocatorTests -v
```
Expected RED: allocator state/schema/runtime implementation is absent.

GREEN: implement the fixed `STATE/ID_ALLOCATOR.yaml` singleton and the three interfaces without a registry/service/background allocator.

Run GREEN:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.CampaignAllocatorTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN: allocator ownership, atomicity and anti-fallback tests pass.

REFACTOR: policy lookup may be a pure adapter over the resolved catalog identifier policy; do not copy the catalog into allocator state.

Coherent checkpoint: allocator schema + scaffold singleton + runtime allocator + allocator tests + audit/project-map projection. If HOT binding is not yet present, this checkpoint may expose only a test double for the declared transaction port and must be marked `JOIN_PENDING: RD04-TASK6`; RD-04 cannot close until the real binding test passes.

## Task 4 — R015 remove reverse presence carrier

**Files**
- Modify: `GAME/SCHEMA/location.schema.yaml`
- Modify: `DEV/TESTS/test_rd04_native_routing_index_hot.py`
- Modify: `DEV/TOOLS/audit_engine.py`

**RED cases**
- `world.location` schema has no `state.present_entity_ids` current-presence carrier;
- Location/index path cannot be used as authority for a mobile Actor's current presence;
- direct current-presence resolution follows the accepted native current owner/routing contract;
- this task does not remove RD-02-owned epistemic fields; their cleanup is a separate coordinated write.

Run RED:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.PresenceAuthorityTests -v
```
Expected RED against current `location.schema.yaml` because `present_entity_ids` survives.

GREEN: remove `present_entity_ids` and the authority-ambiguous invariant referring to indexes/state as authoritative for mobile entities. Replace only with an invariant that persistent location geometry/connections do not establish mobile presence.

Run GREEN + audit:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.PresenceAuthorityTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```

Coherent checkpoint: location R015 cleanup + focused test/audit only. Publish before RD-02 takes its coordinated epistemic cleanup of the same file.

## Task 5 — rebuildable family-index contract

**Files**
- Replace: `GAME/SCHEMA/index.schema.yaml`
- Create: `DEV/SCHEMAS/native-family-index.schema.json`
- Modify: `GAME/TOOLS/native_storage.py`
- Modify: `GAME/SCHEMA/README.md`
- Modify: `GAME/TEMPLATE/STORAGE_README.md`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`
- Modify: `DEV/TESTS/test_rd04_native_routing_index_hot.py`

**Interfaces**
```text
rebuild_family_index(family_key, native_records) -> family_index_document
resolve_discovery_candidate(family_key, index_entry) -> native_route
```
Neither establishes semantic existence/currentness; the caller rehydrates and validates the native body.

**RED/GREEN cases**
- discovery uses expected family index -> exact candidate route -> body identity/eligibility revalidation;
- only owner-approved compact routing fields;
- no private continuity/knowledge/disclosure/Story/LIVE claim/authorization grant;
- omission is not semantic absence;
- known-ID route bypasses index;
- partitioned shape rejected absent WP-24 trigger.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.NativeIndexTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```

Coherent checkpoint: index contract/rebuild + docs/audit/test synchronization.

## Task 6 — typed native-owner HOT envelope and allocator binding

**Files**
- Create: `DEV/SCHEMAS/native-owner-hot-envelope.schema.json`
- Create: `GAME/TOOLS/hot_store.py`
- Modify: `GAME/TOOLS/id_allocator.py`
- Modify: `DEV/TESTS/test_rd04_native_routing_index_hot.py`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`

**Interfaces**
```text
class NativeHotStore:
    get(campaign_authority_context, native_family, complete_native_identity)
    establish_current(..., owner_document, source_basis, owner_generation)
    transaction(scope) -> NativeHotTransaction
    mark_dirty(..., owner_generation, scope)
    clear_published_generation(..., frozen_generation, scope)
    rebuild_helper(...)

class NativeHotTransaction:
    stage_owner_document(...)
    stage_allocator_state(...)
    stage_index_delta(...)
    commit()
    rollback()
```

**RED/GREEN cases**
- unknown family/shape/identity mismatch rejected;
- no SQL rowid/AUTOINCREMENT/order identity;
- campaign/context isolation;
- HOT possession never bypasses role/access/information eligibility;
- source basis distinct from owner generation;
- narrow helpers rebuildable and no absence proof;
- `allocate_and_stage_record` uses this exact transaction and proves allocator + created owner record all-or-none.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.NativeHotStoreTests -v
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.CampaignAllocatorTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```

Coherent checkpoint: HOT envelope/store + real allocator transaction binding + tests/audit/project-map.

## Task 7 — atomicity, dirty generation and LIVE boundary

**Files**
- Modify: `GAME/TOOLS/hot_store.py`
- Modify: `DEV/TESTS/test_rd04_native_routing_index_hot.py`

**RED/GREEN scenarios**
- one permitted local owner-establishment transaction advances all implicated local owner/evidence/dirty/helper state or none;
- no transaction spans player choice, model/host exchange, repo/network I/O, campaign publication, LIVE CAS or external research;
- dirty bookkeeping owner-generation/scope relative, not campaign-global frontier;
- publication-success helper clears only exact frozen generation;
- pre-CAS LIVE consequence cannot replace current accepted owner state;
- post-CAS local adoption cannot roll back accepted remote CAS;
- surviving SQLite on cold start is cache unless source-equivalence is proven.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot.NativeAtomicityTests -v
```

Coherent checkpoint: HOT atomicity/currentness behavior + focused tests.

## Task 8 — R018 route/root integration and RD-04 verification

**Files**
- Modify: `GAME/TOOLS/native_storage.py`
- Modify: `DEV/SCHEMAS/native-route.schema.json`
- Modify: `DEV/TESTS/test_rd04_native_routing_index_hot.py`
- Inspect: finalized RD-02/RD-03 native owner schemas and each later family only when its integration checkpoint is reached.

**Integration proof**
- `world.knowledge` direct composite route under `WORLD/KNOWLEDGE`;
- `runtime.disclosure` direct composite route under `STATE/RUNTIME/DISCLOSURES`;
- Actor/Asset/Effect roots exactly as WP-11;
- native body identity revalidated after route/hydration;
- index/HOT consume owner definitions rather than redefine them;
- campaign allocator remains exceptional fixed route and is not placed in hashed native routing;
- R015 reverse presence cannot reappear through an index/helper.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

Version Impact Gate: classify actual storage/schema/API namespaces and synchronize required projections exactly once.
System Impact Gate: any need for a second allocator/registry, changed identity ownership, cross-owner transaction or new currentness authority stops execution and returns to architecture/process owner.

Stale/negative proof: no generic ID registry, path-as-identity/currentness, SQL-order chronology, authoritative index absence, reverse Location presence authority, global dirty frontier, automatic index partitioning, SQLite+LIVE distributed transaction, or campaign allocator fallback for source-native IDs.

Final coherent checkpoint: all RD-04 tasks green, allocator-HOT binding complete, RD-02/RD-03 route joins reached as applicable, maintenance audit/full DEV tests green, remote read-back recorded. RD-04 does not claim R068 pure-proof closure; PB proof reconciliation names its applicable themes separately.
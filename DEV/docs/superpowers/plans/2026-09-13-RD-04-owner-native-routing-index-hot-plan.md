# RD-04 — Owner-Native Routing / Index / HOT — Executable Implementation Plan

Goal: realize deterministic native-family routing, rebuildable non-authoritative indexes and a typed native-owner HOT/SQLite substrate without creating new semantic/currentness/chronology authority.

RD unit: `RD-04`
Direct readiness: `R015,R063,R064,R065,R066,R067`.
Composite slices/parents: R018 route/root integration only after each implicated native owner shape is finalized.
Pure-proof leaves: none directly owned.
Canonical owners: WP-11 physical storage topology/identity/indexing; WP-12 HOT/SQLite/transaction realization; exact Step-2 records.
Dependencies/joins: consumes finalized native owner shapes from RD-02/RD-03 and later RD-05/RD-08/RD-09/RD-12/RD-13 at integration; does not serialize independent semantic work.
Out of scope: gameplay semantics, global transaction manager, publication timing/ref protocol, recovery source selection, LIVE claim semantics, automatic writer partitioning.

## Impact Envelope

Primary owner artifacts: WP-11/WP-12 remain read-only architecture authority.
GAME runtime/projection surfaces: `GAME/SCHEMA/index.schema.yaml`, `GAME/SCHEMA/README.md`, `GAME/TEMPLATE/STORAGE_README.md`, `GAME/TOOLS/native_storage.py`, `GAME/TOOLS/hot_store.py`.
DEV schemas/catalogs/machine contracts: `NEW_CREATE DEV/SCHEMAS/native-route.schema.json`, `native-family-index.schema.json`, `native-owner-hot-envelope.schema.json`; projection/audit consumers `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py`.
Validators/tests/audits: `NEW_CREATE DEV/TESTS/test_rd04_native_routing_index_hot.py`.
Cross-RD joins: native owner schemas from RD-02/RD-03 first at integration; later families plug into same routing/HOT law without transferring ownership.
Explicit exclusions / authority not transferred: path/hash/shard/index/SQL rowid/order/time are never identity, chronology, eligibility, currentness or publication authority; no generic ID registry/state service/global dirty frontier; no SQLite+LIVE distributed transaction; no automatic partitioning without accepted trigger.
Version Impact: classify actual schema/API/storage contract delta at execution checkpoint.
Schema/catalog/checkpoint impact: route/index/HOT machine-contract generation may change; checkpoint semantics remain untouched.
Migration impact: none during v1 clean-slate implementation absent accepted concrete compatibility trigger.
HG-01 constraints affected: constraint 3; absence of old HOT implementation does not create new semantic architecture.
Currentness/re-read set before write: WP-11, WP-12, exact readiness records, finalized RD-02/RD-03 family schemas, `GAME/SCHEMA/index.schema.yaml`, `GAME/SCHEMA/README.md`, `GAME/TEMPLATE/STORAGE_README.md`, existing `GAME/TOOLS/init_campaign.py`, `GAME/TOOLS/ruleset_package.py`, `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py`.

## Task 1 — RED: canonical WP-11 route vectors and authority negatives

Files:
- `NEW_CREATE DEV/TESTS/test_rd04_native_routing_index_hot.py`
- `NEW_CREATE DEV/SCHEMAS/native-route.schema.json`
- `NEW_CREATE GAME/TOOLS/native_storage.py` in Task 2.

Interfaces:
```text
route_native_record(family_key: str, identity_components: tuple[str, ...]) -> str
validate_loaded_identity(family_key, identity_components, document) -> None
```
Route input uses exact `HDM-WP11-ROUTE-V1` framing, uint32be component count/lengths, SHA-256 two-level bucket and unpadded base32hex encoded route-input chunks.

RED cases:
1. fixed vectors for simple identity and composite `world.knowledge(knower_id,fact_id)` / `runtime.disclosure(player_id,fact_id)` routes;
2. component order affects composite route and is owner-defined;
3. loaded body family/complete identity mismatch is integrity failure;
4. known-ID read does not require directory/index enumeration;
5. route path/hash cannot be accepted as body identity or currentness evidence.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot -v
```
Expected: RED because route implementation/contract is absent.

## Task 2 — GREEN: deterministic native route implementation

Files:
- `NEW_CREATE GAME/TOOLS/native_storage.py`
- `NEW_CREATE DEV/SCHEMAS/native-route.schema.json`
- `EXISTING_MODIFY DEV/PROJECT_MAP.md`
- `EXISTING_MODIFY DEV/TOOLS/audit_engine.py`

GREEN:
- implement `route_native_record(...)` and `validate_loaded_identity(...)` exactly once in shipped code;
- encode the owner-defined family root + ordered complete native identity contract in `native-route.schema.json` without turning that schema into identity allocator/semantic authority;
- implement exact framing/hash/encoding/chunk law, no alternate path scheme;
- consume native identity but never allocate it;
- exceptional fixed routes (manifest/config/card/current/allocator/LIVE/Story) remain explicit and are not passed through native routing where WP-11 excludes them;
- development audit validates fixed vectors/importability rather than re-implementing a second router.

VERIFY:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot -v
DEV/TOOLS/run_maintenance_audit
```
Expected: route-vector/integrity assertions PASS.

REFACTOR: private framing/encoding helpers may live inside `GAME/TOOLS/native_storage.py`; do not add a second identity or path module.

Commit boundary: deterministic routing + vectors + integrity validation contract + audit projection.

## Task 3 — Rebuildable family-index contract

Files:
- `EXISTING_REPLACE GAME/SCHEMA/index.schema.yaml`
- `NEW_CREATE DEV/SCHEMAS/native-family-index.schema.json`
- `EXISTING_MODIFY GAME/TOOLS/native_storage.py`
- `EXISTING_MODIFY GAME/SCHEMA/README.md`
- `EXISTING_MODIFY GAME/TEMPLATE/STORAGE_README.md`
- `EXISTING_MODIFY DEV/PROJECT_MAP.md`
- `EXISTING_MODIFY DEV/TOOLS/audit_engine.py`
- `EXISTING_MODIFY DEV/TESTS/test_rd04_native_routing_index_hot.py`

Interfaces:
```text
rebuild_family_index(family_key, native_records) -> family_index_document
resolve_discovery_candidate(family_key, index_entry) -> native_route
```
Neither function establishes semantic existence/currentness; caller must rehydrate and validate native body.

RED cases:
- discovery uses expected family index only, then exact candidate route, then body identity/eligibility revalidation;
- allowed compact fields only: ID/name/aliases/status/path/parent ID/tags/last-event ID as owner-applicable;
- index contains no private continuity, knowledge, disclosure, Story availability, live claim or authorization grant;
- index omission cannot prove semantic absence;
- known-ID route bypasses index;
- partitioned index shape is rejected absent WP-24 trigger.

GREEN: replace old generic index contract with compact family-index projection and deterministic rebuild helper from native records. Keep monolithic `*_INDEX.yaml` baseline.

VERIFY focused test + maintenance audit PASS.

Commit boundary: family-index contract/rebuild + shipped/schema/docs/audit synchronization.

## Task 4 — RED/GREEN: typed native-owner HOT envelope

Files:
- `NEW_CREATE DEV/SCHEMAS/native-owner-hot-envelope.schema.json`
- `NEW_CREATE GAME/TOOLS/hot_store.py`
- `EXISTING_MODIFY DEV/TESTS/test_rd04_native_routing_index_hot.py`
- `EXISTING_MODIFY DEV/PROJECT_MAP.md`
- `EXISTING_MODIFY DEV/TOOLS/audit_engine.py`

Required shipped interface:
```text
class NativeHotStore:
    get(campaign_authority_context, native_family, complete_native_identity)
    establish_current(..., owner_document, source_basis, owner_generation)
    mark_dirty(..., owner_generation, scope)
    clear_published_generation(..., frozen_generation, scope)
    rebuild_helper(...)
```
The class is a typed persistence/cache substrate, not semantic owner. Source/ref/revision/tree/blob and writable partition are metadata/currentness basis, not second semantic key.

RED cases:
- unknown family, invalid shape or identity mismatch rejected;
- native identity cannot come from SQL rowid/AUTOINCREMENT/order;
- hard campaign/context isolation;
- HOT possession cannot bypass role/access/information eligibility;
- clean source-derived copies distinguish source basis from owner generation;
- narrow derived helpers are rebuildable and cannot prove semantic absence.

GREEN: implement the smallest SQLite-backed store in `GAME/TOOLS/hot_store.py` needed for these contracts. Exact DDL/serialization/pragmas are delegated implementation details but remain private to this module and must preserve WP-12 laws.

VERIFY focused test + maintenance audit PASS.

Commit boundary: typed owner-envelope HOT core + machine schema + audit projection, independently usable by later integration.

## Task 5 — Atomicity, dirty-generation and LIVE-boundary proof

Files:
- `EXISTING_MODIFY GAME/TOOLS/hot_store.py`
- `EXISTING_MODIFY DEV/TESTS/test_rd04_native_routing_index_hot.py`

RED/GREEN scenarios:
- one permitted local owner-establishment transaction atomically advances all implicated local owner/evidence/dirty/helper state or none;
- no SQLite transaction spans player choice, model/host exchange, repo/network I/O, campaign publication, LIVE CAS or external research;
- dirty bookkeeping is owner-generation/scope relative, not campaign-global frontier;
- publication-success helper clears only the exact frozen generation, leaving newer generation dirty;
- pre-CAS LIVE consequence cannot replace current accepted owner state;
- post-CAS local adoption cannot roll back accepted remote CAS;
- surviving SQLite on cold start is cache unless source-equivalence is proven.

This task implements only the reusable HOT substrate admitted by WP-12; actual RD-05/RD-09 publication/LIVE behavior remains outside this module.

Commit boundary: HOT atomicity/currentness helper behavior with focused tests.

## Task 6 — R018 route/root integration and closure

Files:
- `EXISTING_MODIFY GAME/TOOLS/native_storage.py`
- `EXISTING_MODIFY DEV/SCHEMAS/native-route.schema.json`
- `EXISTING_MODIFY DEV/TESTS/test_rd04_native_routing_index_hot.py`
- `INSPECT_ONLY` finalized RD-02 and RD-03 native owner schemas.

After RD-02/RD-03 owner schemas are final, integrate their family/root/identity definitions into routing validation without creating a registry authority. Later owner families join through the same explicit contract in their owning RD plans.

Required proof includes:
- `world.knowledge` direct composite route under `WORLD/KNOWLEDGE`;
- `runtime.disclosure` direct composite route under `STATE/RUNTIME/DISCLOSURES`;
- Actor/Asset/Effect roots exactly as WP-11;
- native body identity validation after route/hydration;
- index route rules and HOT envelope consume native owner definitions rather than redefine them.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

Version Impact Gate: classify actual storage/schema/API namespaces under current version owners; synchronize mechanically required bumps/projections exactly once.

Stale/negative proof is encoded in the focused test over active `GAME/**`, `DEV/SCHEMAS/**`, `DEV/PROJECT_MAP.md` and `DEV/TOOLS/audit_engine.py`: no generic ID registry, path-as-identity/currentness rule, SQL-order chronology, authoritative index-absence inference, global dirty frontier, automatic index partitioning or SQLite+LIVE distributed transaction.

Final commit boundary: `native_storage.py` + route/index contracts + `hot_store.py` + HOT envelope + tests + current owner integrations form one reviewable RD-04 result.
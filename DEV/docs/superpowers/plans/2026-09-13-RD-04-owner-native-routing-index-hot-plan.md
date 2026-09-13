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
GAME runtime/projection surfaces: `GAME/SCHEMA/index.schema.yaml` and exact storage/config projections whose current contracts conflict with WP-11/12; no pre-existing `GAME/HOT` authority is assumed.
DEV schemas/catalogs/machine contracts: `NEW_CREATE DEV/SCHEMAS/native-route.schema.json`, `native-owner-hot-envelope.schema.json` if schema contracts are the existing machine-contract convention; exact shared identifier/storage schemas only as required. Implementation code paths are selected from the current DEV tooling/runtime structure during execution rather than inventing a generic service layer.
Validators/tests/audits: `NEW_CREATE DEV/TESTS/test_rd04_native_routing_index_hot.py`; route vectors, integrity mismatch, index rebuild and HOT authority-negative tests.
Cross-RD joins: native owner schemas from RD-02/RD-03 first at integration; later families plug into same routing/HOT law without transferring ownership.
Explicit exclusions / authority not transferred: path/hash/shard/index/SQL rowid/order/time are never identity, chronology, eligibility, currentness or publication authority; no generic ID registry/state service/global dirty frontier; no SQLite+LIVE distributed transaction; no automatic partitioning without accepted trigger.
Version Impact: classify actual schema/API/storage contract delta at execution checkpoint.
Schema/catalog/checkpoint impact: route/HOT machine contracts expected; checkpoint semantics remain untouched.
Migration impact: none during v1 clean-slate implementation absent accepted concrete compatibility trigger.
HG-01 constraints affected: constraint 3; absence of old HOT implementation does not create new semantic architecture.
Currentness/re-read set before write: WP-11, WP-12, exact readiness records, finalized native family schemas being integrated, current GAME storage/index schemas, current DEV tools/tests/schema conventions.

## Task 1 — RED: canonical WP-11 route vectors and authority negatives

Files:
- `NEW_CREATE DEV/TESTS/test_rd04_native_routing_index_hot.py`
- `NEW_CREATE DEV/SCHEMAS/native-route.schema.json` only in GREEN step if current machine-contract convention requires a serialized route contract.

Interfaces:
```text
route(family_key, ordered_identity_components) -> family-root relative record path
```
Route input must use the exact `HDM-WP11-ROUTE-V1` framing, uint32be component count/lengths, SHA-256 two-level bucket and unpadded base32hex encoded route input chunks.

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
- `NEW_CREATE` smallest current DEV runtime/tool module suitable for reusable deterministic storage routing; choose exact path after fresh inspection of `DEV/TOOLS`/runtime modules and record it in execution status before write.
- `NEW_CREATE DEV/SCHEMAS/native-route.schema.json` only if an externalized machine contract is required by current validator architecture.
- `EXISTING_MODIFY` exact storage/manifest consumers only where route roots are represented.

GREEN:
- implement exact framing/hash/encoding/chunk law, no alternative path scheme;
- consume native identity but never allocate it;
- exceptional fixed routes (manifest/config/card/current/allocator/LIVE/Story) remain explicit and do not pass through generic native route function where WP-11 excludes them.

VERIFY focused route-vector tests PASS.

REFACTOR: isolate encoding/framing helpers only when doing so does not create a new identity authority.

Commit boundary: deterministic routing + vectors + integrity validation contract.

## Task 3 — Rebuildable family index contract

Files:
- `EXISTING_REPLACE GAME/SCHEMA/index.schema.yaml` if current generic shape cannot encode WP-11 compact family-index rules without retaining false authority;
- `NEW_CREATE DEV/SCHEMAS/native-family-index.schema.json` if needed by the DEV validation layer;
- exact route/index helper module from Task 2.

RED cases:
- discovery uses expected family index only, then exact candidate route, then body identity/eligibility revalidation;
- allowed compact fields only: ID/name/aliases/status/path/parent ID/tags/last-event ID as owner-applicable;
- index contains no private continuity, knowledge, disclosure, Story availability, live claim or authorization grant;
- index omission cannot prove semantic absence;
- known-ID route bypasses index;
- partitioned index shape is rejected absent WP-24 trigger.

GREEN: implement/reconcile compact family-index validation and deterministic rebuild helpers from native families. Keep monolithic `*_INDEX.yaml` baseline.

Commit boundary: family-index contract + rebuild proof.

## Task 4 — RED/GREEN: typed native-owner HOT envelope

Files:
- `NEW_CREATE DEV/SCHEMAS/native-owner-hot-envelope.schema.json`
- `NEW_CREATE` narrow local HOT data-access module in the current DEV/runtime implementation tree selected during execution inspection;
- tests remain in `DEV/TESTS/test_rd04_native_routing_index_hot.py`.

Required interface semantics:
```text
campaign_authority_context
+ native_family
+ complete_native_identity
-> one current validated owner representation
```
Source/ref/revision/tree/blob and writable partition are metadata/currentness basis, not second semantic key.

RED cases:
- unknown family, invalid shape or identity mismatch rejected;
- native identity cannot come from SQL rowid/AUTOINCREMENT/order;
- hard campaign/context isolation;
- HOT possession cannot bypass role/access/information eligibility;
- clean source-derived copies distinguish source basis from owner generation;
- narrow derived helpers are rebuildable and cannot prove semantic absence.

GREEN: implement smallest typed envelope/store API and SQLite baseline needed to pass cases. Exact DDL/serialization/pragmas are delegated implementation details, but schemas/API must mechanically preserve WP-12 laws.

Commit boundary: typed owner-envelope HOT core, independently usable by later integration.

## Task 5 — Atomicity, dirty-generation and LIVE-boundary proof

RED/GREEN scenarios:
- one permitted local owner establishment transaction atomically advances all implicated local owner/evidence/dirty/helper state or none;
- no SQLite transaction spans player choice, model/host exchange, repo/network I/O, campaign publication, LIVE CAS or external research;
- dirty bookkeeping is owner-generation/scope relative, not campaign-global frontier;
- publication-success helper can clear only the exact frozen generation, leaving newer generation dirty;
- pre-CAS LIVE consequence cannot replace current accepted owner state;
- post-CAS local adoption cannot roll back accepted remote CAS;
- surviving SQLite on cold start is cache unless source-equivalence is proven.

This task tests/implements only the reusable HOT substrate admitted by WP-12; actual RD-05/RD-09 publication/LIVE owner behavior remains in those plans.

## Task 6 — R018 route/root integration and closure

After RD-02/RD-03 owner schemas are final, integrate their family/root/identity definitions into routing validation without creating a registry authority. Record joins for later owner families rather than blocking RD-04 on their semantic implementation.

Required proof includes:
- `world.knowledge` direct composite route under `WORLD/KNOWLEDGE`;
- `runtime.disclosure` direct composite route under `STATE/RUNTIME/DISCLOSURES`;
- Actor/Asset/Effect roots exactly as WP-11;
- native body identity validation after route/hydration;
- index route rules and HOT envelope use native owner definitions.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

Version Impact Gate: classify actual storage/schema/API namespaces under current version owners; synchronize mechanically required bumps/projections exactly once.

Stale/negative proof: active GAME/DEV contains no generic ID registry, path-as-identity/currentness rule, SQL-order chronology, authoritative index-absence inference, global dirty frontier, automatic index partitioning or SQLite+LIVE distributed transaction.

Final commit boundary: route vectors + index contract + typed HOT substrate + currently available R018 owner integrations form one reviewable RD-04 result. Later semantic families join through the same contract without reopening RD-04 ownership.
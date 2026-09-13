# RD-02 — Information / Knowledge / Disclosure / Message — Executable Implementation Plan

Goal: realize distinct v1 owner-native lore-fact, Actor knowledge, human disclosure and retained-message contracts; remove legacy parallel epistemic/secret representations.

RD unit: `RD-02`
Direct readiness: `R007,R008,R009,R017,R049,R052`
Composite slices/parents: `R006.INFO,R016.INFO,R018.INFO,R053.INFO,R062.KNOWLEDGE,R062.DISCLOSURE,R062.RETAINED_MESSAGE`.
Pure-proof leaves: none directly owned.
Canonical owners: Step-4 truth/knowledge/role/context Story; host delivery/disclosure boundary; WP-10; WP-11; exact Step-2 records.
Dependencies/joins: owner shapes precede RD-04 route/HOT integration; joins RD-09 for LIVE/currentness where applicable; constrains RD-03/RD-11/RD-13 without serializing them.
Out of scope: HOT implementation, LIVE lifecycle, Story authority, generic memory/state service, release migration.

## Impact Envelope

Primary owner artifacts: accepted specs remain read-only authority.
GAME runtime/projection surfaces: `GAME/SCHEMA/lore.schema.yaml`, legacy epistemic fields in `pc.schema.yaml`, `npc.schema.yaml`, `faction.schema.yaml`, `location.schema.yaml`, `item.schema.yaml`, plus actual templates/consumers discovered by stale-reference search.
DEV schemas/catalogs/machine contracts: `NEW_CREATE DEV/SCHEMAS/world-lore-fact-state.schema.json`, `world-knowledge-state.schema.json`, `runtime-disclosure-state.schema.json`, `runtime-message-state.schema.json`; exact catalog/identifier projections only where current owners require registration.
Validators/tests/audits: `NEW_CREATE DEV/TESTS/test_rd02_information_native_contracts.py`; extend stable maintenance checks only for mechanically enforceable forbidden aliases/owner duplication.
Documentation/install/package projections: only consumers directly coupled to changed contracts.
Cross-RD joins: RD-04 route law; RD-09 currentness; RD-11 Context eligibility/ranking; RD-13 semantic history; no authority transfer.
Explicit exclusions / authority not transferred: no `Secret` owner; no truth.disputed owner; disclosure never implies Actor knowledge; path/index/cache never epistemic authority; no generic memory/state service.
Version Impact: deferred to actual execution delta and version owner classification.
Schema/catalog/checkpoint impact: expected new schema-generation impact; exact bump selected at Version Impact Gate, not here.
Migration impact: none for v1 clean-slate unless an accepted concrete compatibility trigger exists at execution time.
HG-01 constraints affected: constraint 3 only; missing representation is implementation debt, not new architecture.
Currentness/re-read set before write: Step-4, disclosure boundary, WP-10/11, exact readiness records, current GAME schemas/templates/consumers, relevant DEV schema/catalog/validator surfaces.

## Task 1 — Establish RED for authority separation and legacy contamination

Files:
- `NEW_CREATE DEV/TESTS/test_rd02_information_native_contracts.py`
- `INSPECT_ONLY GAME/SCHEMA/*.yaml`
- `INSPECT_ONLY DEV/SCHEMAS/**`, current schema/catalog validators.

Interfaces asserted:
- `world.lore_fact` objective fact record;
- `world.knowledge` identity `(knower_id,fact_id)`;
- `runtime.disclosure` identity `(player_id,fact_id)`;
- retained `runtime.message` with its source-native identity/retention contract;
- all four remain semantically separate.

RED cases:
1. required owner-native schemas are absent;
2. legacy `secret_ids` / equivalent embedded knowledge or disclosure aliases remain in old GAME entity schemas;
3. disclosure cannot validate as knowledge and knowledge cannot validate as disclosure;
4. no schema may infer truth from knowledge/disclosure/message presence;
5. no `Secret`, `truth.disputed`, or parallel epistemic authority may be admitted;
6. current catalog/validator route must reject unknown/legacy owner aliases rather than silently coerce them.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v
```
Expected: RED for missing native schemas and/or known legacy contamination only.

Commit boundary: combine with Task 2 unless RED fixture itself is a useful coherent diagnostic checkpoint.

## Task 2 — Create canonical machine schemas

Files:
- `NEW_CREATE DEV/SCHEMAS/world-lore-fact-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/world-knowledge-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/runtime-disclosure-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/runtime-message-state.schema.json`
- `EXISTING_MODIFY` exact shared identity/schema references only when needed.

GREEN requirements:
- encode complete native identities and structural owner payloads, not broad generic property bags;
- knowledge identity order is `knower_id,fact_id`;
- disclosure identity order is `player_id,fact_id`;
- schema fields preserve owner-defined distinction among objective fact, fictional knowledge/belief, human disclosure and retained communication;
- Message remains delivery/history evidence, not an ACL, knowledge or canon owner;
- do not encode physical WP-11 route as semantic identity.

Run focused test; expected new-contract assertions GREEN while legacy-contamination assertions may remain RED until Task 3.

REFACTOR: reuse existing DEV schema conventions without creating a generic world-state envelope that merges owners.

Commit boundary: all four owner schemas plus focused tests form one coherent machine-contract checkpoint.

## Task 3 — Replace legacy GAME epistemic representation

Files:
- `EXISTING_REPLACE GAME/SCHEMA/lore.schema.yaml` as needed to become a v1 projection of `world.lore_fact` rather than combined legacy epistemic state;
- `EXISTING_REPLACE` or `EXISTING_RETIRE` legacy `GAME/SCHEMA/pc.schema.yaml`, `npc.schema.yaml`, `item.schema.yaml` portions only as coordinated with RD-03; if whole-file Actor/Asset replacement belongs to RD-03, RD-02 removes/forbids only epistemic aliases and records the join rather than duplicating Actor schema work;
- `EXISTING_MODIFY` faction/location and actual templates/consumers containing embedded secret/knowledge authority.

RED: repository-wide focused assertions/search must still identify legacy secret/knowledge aliases before edit.

GREEN:
- remove parallel authority rather than maintain compatibility aliases;
- consumers refer to native owner records/IDs according to accepted contracts;
- retain v1-compatible `GAME/CORE/INFORMATION.md` laws, repairing only contradictions discovered by tests;
- do not resurrect absent `world_state.schema.yaml`.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v
```
Expected: PASS for schema and legacy-contamination cases.

Commit boundary: legacy epistemic retirement + exact consumer synchronization.

## Task 4 — Catalog/validator/route-facing projection closure

Files:
- `EXISTING_MODIFY` exact current catalog/identifier/schema-validation surfaces proven by RED;
- no WP-11 route/HOT implementation in this RD.

RED cases:
- each new owner family must be machine-recognizable where the existing validation architecture requires explicit registration;
- forbidden legacy aliases must fail validation;
- owner family/identity mismatch must fail.

GREEN: add only required family/schema registration and validation. Do not create a new family registry if an existing owner already serves this purpose.

VERIFY:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

## Task 5 — Composite-parent and stale-reference closure

Evidence required:
- `R062.KNOWLEDGE`, `.DISCLOSURE`, `.RETAINED_MESSAGE` each map to exact machine contracts and focused proof;
- R006/R016/R018/R053 information slices are explicitly accounted without claiming their non-information slices;
- stale search over GAME/DEV shows no unauthorized `secret_ids`, legacy embedded epistemic authority or invalid knowledge/disclosure shortcut in active v1 surfaces;
- downstream RD-04/RD-09/RD-11/RD-13 joins are recorded, not prematurely implemented.

Version Impact Gate: classify actual new/changed schema/catalog generations and projections using current version owners; synchronize mechanically required changes in the same checkpoint.

Final verification:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Then hosted CI on published exact HEAD.

Completion boundary: RD-02 is independently reviewable when native contracts, legacy retirement, validation and composite-slice evidence are coherent; no RD-04 routing/HOT behavior is needed for RD-02 semantic completion.
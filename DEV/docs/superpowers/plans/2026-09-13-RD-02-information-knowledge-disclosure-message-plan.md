# RD-02 — Information / Knowledge / Disclosure / Message — Executable Implementation Plan

Goal: realize distinct v1 owner-native lore-fact, Actor knowledge, human disclosure and retained-message contracts; remove legacy parallel epistemic/secret representations.

RD unit: `RD-02`
Direct readiness: `R007,R008,R009,R017,R049,R052`.
Composite slices/parents: `R006.INFO,R016.INFO,R018.INFO,R053.INFO,R062.KNOWLEDGE,R062.DISCLOSURE,R062.RETAINED_MESSAGE`.
Pure-proof leaves: none directly owned.
Canonical owners: Step-4 truth/knowledge/role/context Story; host delivery/disclosure boundary; WP-10; WP-11; exact Step-2 records.
Dependencies/joins: owner shapes precede RD-04 route/HOT integration; joins RD-09 for LIVE/currentness where applicable; constrains RD-03/RD-11/RD-13 without serializing them.
Out of scope: HOT implementation, LIVE lifecycle, Story authority, generic memory/state service, release migration.

## Impact Envelope

Primary owner artifacts: accepted specs remain read-only authority.
GAME runtime/projection surfaces: `GAME/SCHEMA/lore.schema.yaml`, `pc.schema.yaml`, `npc.schema.yaml`, `faction.schema.yaml`, `location.schema.yaml`, `item.schema.yaml`, `GAME/SCHEMA/README.md`, `GAME/CORE/INFORMATION.md`, `GAME/TEMPLATE/STORAGE_README.md`.
DEV schemas/catalogs/machine contracts: `NEW_CREATE DEV/SCHEMAS/world-lore-fact-state.schema.json`, `world-knowledge-state.schema.json`, `runtime-disclosure-state.schema.json`, `runtime-message-state.schema.json`; direct projection consumers `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py`.
Validators/tests/audits: `NEW_CREATE DEV/TESTS/test_rd02_information_native_contracts.py`; existing maintenance audit consumes `DEV/TOOLS/audit_engine.py`.
Documentation/install/package projections: only the exact README/project-map/storage projection files named above.
Cross-RD joins: RD-04 route law; RD-09 currentness; RD-11 Context eligibility/ranking; RD-13 semantic history; no authority transfer.
Explicit exclusions / authority not transferred: no `Secret` owner; no truth.disputed owner; disclosure never implies Actor knowledge; path/index/cache never epistemic authority; no generic memory/state service.
Version Impact: deferred to actual execution delta and version-owner classification.
Schema/catalog/checkpoint impact: expected new schema-generation impact; exact bump selected at Version Impact Gate, not here.
Migration impact: none for v1 clean-slate unless an accepted concrete compatibility trigger exists at execution time.
HG-01 constraints affected: constraint 3 only; missing representation is implementation debt, not new architecture.
Currentness/re-read set before write: Step-4, disclosure boundary, WP-10/11, exact readiness records, all GAME/DEV paths named in this envelope.

## Task 1 — RED for authority separation and legacy contamination

Files:
- `NEW_CREATE DEV/TESTS/test_rd02_information_native_contracts.py`
- `INSPECT_ONLY GAME/SCHEMA/lore.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/pc.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/npc.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/faction.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/location.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/item.schema.yaml`
- `INSPECT_ONLY GAME/CORE/INFORMATION.md`
- `INSPECT_ONLY DEV/TOOLS/audit_engine.py`

Interfaces asserted:
- `world.lore_fact` objective fact record;
- `world.knowledge` identity `(knower_id,fact_id)`;
- `runtime.disclosure` identity `(player_id,fact_id)`;
- retained `runtime.message` with source-native identity/retention contract;
- all four remain semantically separate.

RED cases:
1. required owner-native schemas are absent;
2. legacy `secret_ids` / equivalent embedded knowledge or disclosure aliases remain in old GAME entity schemas;
3. disclosure cannot validate as knowledge and knowledge cannot validate as disclosure;
4. no schema may infer truth from knowledge/disclosure/message presence;
5. no `Secret`, `truth.disputed`, or parallel epistemic authority may be admitted;
6. shipped schema/audit projections still describe old epistemic ownership before repair.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v
```
Expected: RED for missing native schemas and known legacy contamination/projection drift only.

Commit boundary: combine with Task 2 unless the RED fixture itself is a useful coherent diagnostic checkpoint.

## Task 2 — Create canonical DEV machine schemas

Files:
- `NEW_CREATE DEV/SCHEMAS/world-lore-fact-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/world-knowledge-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/runtime-disclosure-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/runtime-message-state.schema.json`
- `EXISTING_MODIFY DEV/TESTS/test_rd02_information_native_contracts.py`

GREEN requirements:
- encode complete native identities and structural owner payloads, not generic property bags;
- knowledge identity order is `knower_id,fact_id`;
- disclosure identity order is `player_id,fact_id`;
- preserve objective fact vs fictional knowledge/belief vs human disclosure vs retained communication;
- Message remains delivery/history evidence, not ACL, knowledge or canon owner;
- physical WP-11 route is not encoded as semantic identity.

Run focused test; expected new-contract assertions GREEN while legacy-contamination assertions remain RED until Task 3.

REFACTOR: reuse existing DEV schema idioms locally; do not create a generic world-state envelope.

Commit boundary: four owner schemas + focused tests.

## Task 3 — Replace legacy GAME epistemic representation

Files:
- `EXISTING_REPLACE GAME/SCHEMA/lore.schema.yaml`
- `EXISTING_MODIFY GAME/SCHEMA/pc.schema.yaml`
- `EXISTING_MODIFY GAME/SCHEMA/npc.schema.yaml`
- `EXISTING_MODIFY GAME/SCHEMA/faction.schema.yaml`
- `EXISTING_MODIFY GAME/SCHEMA/location.schema.yaml`
- `EXISTING_MODIFY GAME/SCHEMA/item.schema.yaml`
- `EXISTING_MODIFY GAME/SCHEMA/README.md`
- `EXISTING_MODIFY GAME/CORE/INFORMATION.md` only to remove a test-proven contradiction; otherwise record `INSPECT_ONLY` and preserve its current v1 distinctions
- `EXISTING_MODIFY GAME/TEMPLATE/STORAGE_README.md`
- `EXISTING_MODIFY DEV/PROJECT_MAP.md`
- `EXISTING_MODIFY DEV/TOOLS/audit_engine.py`

Coordination law: RD-02 removes epistemic/secret ownership from PC/NPC/item now; RD-03 later retires those three whole native schemas in favor of Actor/Asset/Effect. RD-02 must not wait for RD-03 to remove forbidden parallel epistemic authority.

RED: focused assertions identify every active legacy epistemic field in the six named GAME schemas and stale direct projection assertions in README/project-map/audit.

GREEN:
- remove parallel authority rather than maintain compatibility aliases;
- GAME projections refer to native information owners/IDs according to accepted contracts;
- `lore.schema.yaml` becomes the shipped projection of objective `world.lore_fact`, not combined truth/knowledge/dispute lifecycle;
- preserve correct `GAME/CORE/INFORMATION.md` laws unless a contradiction is concretely proven;
- do not resurrect absent `world_state.schema.yaml`.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v
DEV/TOOLS/run_maintenance_audit
```
Expected: legacy-contamination and direct projection checks PASS.

Commit boundary: legacy epistemic retirement + direct consumer synchronization.

## Task 4 — Validation/projection closure without a new registry

Files:
- `EXISTING_MODIFY DEV/TESTS/test_rd02_information_native_contracts.py`
- `EXISTING_MODIFY DEV/TOOLS/audit_engine.py`
- `EXISTING_MODIFY DEV/PROJECT_MAP.md`
- `INSPECT_ONLY DEV/SCHEMAS/identifier-policies.schema.json`
- `INSPECT_ONLY DEV/SCHEMAS/catalog-definition.schema.json`
- `INSPECT_ONLY DEV/SCHEMAS/core-catalog.schema.json`

Current planning decision: RD-02 does **not** create or expand a generic family/catalog registry merely to register campaign-state owner families. The three catalog/identifier schemas above are re-read as contamination guards; modify them only if a fresh owner-required contradiction is proven, in which case that is a plan-impact finding requiring review before code change rather than an execution-time guess.

RED/GREEN cases:
- each new schema validates its complete native identity;
- forbidden legacy aliases fail focused validation;
- owner family/identity mismatch fails;
- existing catalog/identifier contracts are not repurposed into campaign-state semantic authority.

VERIFY:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

## Task 5 — Composite-parent and stale-reference closure

Files:
- `EXISTING_MODIFY DEV/TESTS/test_rd02_information_native_contracts.py`
- `INSPECT_ONLY GAME/**`
- `INSPECT_ONLY DEV/**`

The repository-wide scan is proof scope, not authorization to edit arbitrary matches. Active stale matches outside the explicit Task 3 file set are classified before modification: historical/design evidence remains untouched; a current runtime/projection consumer not listed by this plan is an Impact Envelope deviation and must be added through plan review rather than silently edited.

Evidence required:
- `R062.KNOWLEDGE`, `.DISCLOSURE`, `.RETAINED_MESSAGE` map to exact machine contracts and focused proof;
- R006/R016/R018/R053 information slices are accounted without claiming non-information slices;
- no unauthorized `secret_ids`, embedded epistemic authority or disclosure=>knowledge shortcut remains in active v1 GAME surfaces;
- downstream RD-04/RD-09/RD-11/RD-13 joins are recorded, not prematurely implemented.

Version Impact Gate: classify actual new/changed schema generations and projections using current version owners; synchronize required changes in the same coherent checkpoint.

Final verification:
```bash
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Then hosted CI on published exact HEAD.

Completion boundary: RD-02 is independently reviewable when native contracts, explicit GAME retirement edits, validation and composite-slice evidence are coherent; RD-04 routing/HOT behavior is not required for RD-02 semantic completion.
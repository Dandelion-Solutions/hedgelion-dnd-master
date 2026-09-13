# RD-03 — Actor / Asset / Effect Continuity — Executable Implementation Plan

Goal: realize clean v1 Actor/Asset/Effect native state and continuity contracts, replacing PC/NPC/item-era state shapes while preserving epistemic ownership and bounded cognition.

RD unit: `RD-03`
Direct readiness: `R025..R028,R104,R108..R111,R113..R116,R126,R128..R130,R132,R136`.
Composite slices/parents: `R006.ACTOR,R016.ACTOR,R018.ACTOR,R029.ACTOR,R062.ACTOR_CONTINUITY_RELATIONS,R062.EFFECT_APPLICATION`.
Pure-proof leaves: none directly owned.
Canonical owners: R2.1 continuity/history, R2.2 Actor continuity, exact Actor/Asset/Effect owners referenced by Step-2, WP-10, WP-11.
Dependencies/joins: owner shapes feed RD-04 routing/HOT, RD-14 onboarding, RD-06/RD-14 R029, and downstream RD-11/RD-13 consumers.
Out of scope: persistence/publication, bootstrap, Context Runtime, Story, collaboration authority.

## Impact Envelope

Primary owner artifacts: accepted Actor/continuity/entity/effect specs remain semantic authority.
GAME runtime/projection surfaces: `GAME/SCHEMA/pc.schema.yaml`, `npc.schema.yaml`, `item.schema.yaml`, `GAME/SCHEMA/README.md`, `GAME/TEMPLATE/STORAGE_README.md`; new v1 projections `GAME/SCHEMA/actor.schema.yaml`, `asset.schema.yaml`, `effect.schema.yaml`.
DEV schemas/catalogs/machine contracts: existing `DEV/SCHEMAS/world-actor-state.schema.json`, `world-actor-group-state.schema.json`, `world-asset-state.schema.json`, `world-effect-state.schema.json`; projection consumers `DEV/PROJECT_MAP.md` and `DEV/TOOLS/audit_engine.py`.
Validators/tests/audits: `NEW_CREATE DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`.
Cross-RD joins: RD-02 owns knowledge/disclosure/message; RD-04 consumes finalized owner shapes; RD-14 consumes provisional Actor shape; RD-11 consumes owner-backed epistemic/history evidence without owning Actor state.
Explicit exclusions / authority not transferred: no one memory blob; no embedded replacement for `world.knowledge`; no symmetric relationship inference; no PC voluntary mental-state ownership; no continuous NPC simulation; no generic turn-count TTL; no Context ranking authority.
Version Impact: classify actual schema/catalog changes during execution.
Schema/catalog/checkpoint impact: likely schema-generation/projection impact; no checkpoint authority change.
Migration impact: none under v1 clean-slate absent a separately activated compatibility trigger.
HG-01 constraints affected: 1 and 2 — NPC/faction voluntary reasoning remains Actor semantics, and ordinary transient attention/position/reaction remains fiction unless an owner requires typed state.
Currentness/re-read set before write: R2.1/R2.2, exact Step-2 records, WP-10/11, the four DEV native schemas above, the six GAME schema paths above, `GAME/SCHEMA/README.md`, `GAME/TEMPLATE/STORAGE_README.md`, `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py`.

## Task 1 — RED: owner separation and v0.8 retirement contract

Files:
- `NEW_CREATE DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`
- `INSPECT_ONLY DEV/SCHEMAS/world-actor-state.schema.json`
- `INSPECT_ONLY DEV/SCHEMAS/world-actor-group-state.schema.json`
- `INSPECT_ONLY DEV/SCHEMAS/world-asset-state.schema.json`
- `INSPECT_ONLY DEV/SCHEMAS/world-effect-state.schema.json`
- `INSPECT_ONLY GAME/SCHEMA/pc.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/npc.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/item.schema.yaml`

RED cases:
1. v1 Actor/Asset/Effect schemas satisfy current owner-required identities and structural layers;
2. old PC/NPC/item route subtype semantics are not required for native Actor/Asset identities;
3. Actor schema cannot contain a replacement epistemic authority for `world.knowledge`;
4. relationships are directional/source-Actor-local and no symmetric inverse is inferred without owner rule;
5. cognition update permits `NO_CHANGE`, is event-driven/bounded, and has no generic turn-count TTL;
6. transient continuity fields invalidate by owner-defined fictional-time/event conditions rather than arbitrary turns;
7. Effect/application remains natural-owner-local and cannot become a generic effect-list surrogate;
8. PC voluntary mental state is not engine-authored;
9. shipped schema documentation/audit still references legacy PC/NPC/item native contracts before cutover.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity -v
```
Expected: RED only for current contract gaps/legacy consumers.

Commit boundary: normally combine with Task 2.

## Task 2 — Complete/reconcile DEV native machine contracts

Files:
- `EXISTING_MODIFY DEV/SCHEMAS/world-actor-state.schema.json`
- `EXISTING_MODIFY DEV/SCHEMAS/world-actor-group-state.schema.json` only for owner-required group projection fields; if no change is required, record verified `INSPECT_ONLY` in task evidence
- `EXISTING_MODIFY DEV/SCHEMAS/world-asset-state.schema.json`
- `EXISTING_MODIFY DEV/SCHEMAS/world-effect-state.schema.json`

GREEN:
- preserve complete native identity;
- encode foundation/continuity/transient separation where owner requires structural distinction;
- encode source-Actor-local directed relationships without auto-inverse semantics;
- keep private continuity non-epistemic; knowledge references may point to RD-02 owners but never duplicate fact/knowledge truth;
- encode sparse cognition state only where accepted and permit no-change;
- preserve source trust/promotion/history-basis references required by R2.1/R2.2 without creating a second history owner;
- Effect/application semantics remain at natural owner.

Run focused tests; expected DEV contract assertions GREEN.

REFACTOR: reuse existing schema definitions only when they do not collapse owner lifecycles.

Commit boundary: coherent DEV native-contract slice.

## Task 3 — Cut shipped GAME contracts to Actor / Asset / Effect

Files:
- `NEW_CREATE GAME/SCHEMA/actor.schema.yaml`
- `NEW_CREATE GAME/SCHEMA/asset.schema.yaml`
- `NEW_CREATE GAME/SCHEMA/effect.schema.yaml`
- `EXISTING_RETIRE GAME/SCHEMA/pc.schema.yaml`
- `EXISTING_RETIRE GAME/SCHEMA/npc.schema.yaml`
- `EXISTING_RETIRE GAME/SCHEMA/item.schema.yaml`
- `EXISTING_MODIFY GAME/SCHEMA/README.md`
- `EXISTING_MODIFY GAME/TEMPLATE/STORAGE_README.md`
- `EXISTING_MODIFY DEV/PROJECT_MAP.md`
- `EXISTING_MODIFY DEV/TOOLS/audit_engine.py`

RED: focused test and exact consumer assertions must identify current PC/NPC/item-native references in the four projection/validation files above before edit.

GREEN:
- shipped persistent formats project one `world.actor` family; PC/NPC are classification/projection only, never native route subtype;
- shipped `world.asset` projection replaces item-as-native-family while preserving human-facing “item” terminology only where it is presentation, not identity/route authority;
- shipped Effect projection preserves natural-owner application semantics;
- remove old three schema files in the same coherent checkpoint as their replacement schemas and direct consumer updates;
- no epistemic fields duplicated from RD-02;
- no v0.8 compatibility wrapper.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity -v
DEV/TOOLS/run_maintenance_audit
```
Expected: focused contract and maintenance projection checks PASS.

Commit boundary: GAME v1 entity projection cutover + direct consumer synchronization; repository must not be left with README/audit pointing to retired schemas.

## Task 4 — Continuity/history and bounded-cognition proof

Files:
- `EXISTING_MODIFY DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`
- `INSPECT_ONLY DEV/SCHEMAS/world-actor-state.schema.json`
- `INSPECT_ONLY DEV/SCHEMAS/world-effect-state.schema.json`

This RD proves the native state contract; it does not invent a new runtime mutation service. Runtime mutation consumers are implemented only by later RD plans that already own their lifecycle.

RED/GREEN scenarios:
- accepted mutable horizon and ancestry-bound derivative use;
- directional relationship asymmetry;
- valid `NO_CHANGE` cognition result;
- fictional-time/event invalidation of transient state;
- one-bounded-purpose mutation cannot require unrelated Actor state rewrite;
- source promotion/trust evidence cannot silently rewrite accepted history;
- Context Runtime ranking remains out of scope.

VERIFY focused test PASS.

## Task 5 — Provisional Actor/onboarding join and composite closure

Files:
- `EXISTING_MODIFY DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`
- no RD-14 bootstrap file changes.

Prove the Actor shape required by `R029.ACTOR` is explicit and consumable by RD-14 without implementing bootstrap/durability here. The test fixture exposes identity + structural validity + provisional/current lifecycle distinction already owned by architecture.

Composite evidence:
- all RD-03 R062 slices are explicit;
- R006/R016/R018 Actor slices accounted without claiming information/routing siblings;
- R029 Actor slice exposed for later RD-06/RD-14 completion.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

Version Impact Gate: classify actual schema/catalog generation deltas and synchronize exact projections once.

Stale-reference proof: the focused test scans active `GAME/**`, `DEV/PROJECT_MAP.md` and `DEV/TOOLS/audit_engine.py` for retired PC/NPC/item-native contract references; any remaining historical/design references outside active runtime/projection surfaces are not rewritten merely to erase history.

Final commit boundary: native DEV contracts + GAME projection cutover + direct consumer synchronization + tests are independently reviewable; no persistence/context/story implementation is pulled into RD-03.
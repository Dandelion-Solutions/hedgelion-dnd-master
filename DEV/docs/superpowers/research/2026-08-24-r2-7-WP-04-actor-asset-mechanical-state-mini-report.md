# WP-04 — Actor / Asset / mechanical-state model

Статус: **CLOSED — READ-BACK VERIFIED**

Date: 2026-08-24

## 1. Итог

WP-04 завершил whole-project audit текущего Actor / Asset / Effect механического состояния и устранил основные owner/model gaps, обнаруженные reverse audit.

```text
UNIFIED ACTOR OWNER: CONFIRMED
UNIFIED ASSET OWNER: CONFIRMED
HP / RESOURCE / EFFECT / CONDITION OWNER SPLIT: CONFIRMED
R2.2 ACTOR CONTINUITY: MATERIALIZED
READY_PC MODEL: CORRECTED TO PROGRESSIVE GAMEPLAY
RECONSTRUCTABLE PC BUILD: MATERIALIZED
NEW OWNER DECISION REQUIRED: 0
```

Ключевая продуктовая корректировка owner во время WP-04:

> создание героя может происходить внутри первых игровых реплик/сцен; READY_PC не является условием начала игры. Runtime отслеживает прогресс готовности и фиксирует полностью готового героя в campaign repo, когда completeness predicate становится истинным.

---

## 2. Source Manifest delta

Основные owning sources:

- `DEV/ARCHITECTURE/ACTOR_MODEL.md`;
- `DEV/ARCHITECTURE/ASSET_MODEL.md`;
- Step-2 mechanical-state ownership and assurance specs;
- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`;
- Step-4 truth/knowledge boundary;
- Step-5 durability/currentness boundary;
- `GAME/CORE/CHARACTER_READINESS.md`;
- `GAME/CORE/DIEGETIC_ONBOARDING.md`.

Machine surfaces audited/changed:

- `DEV/SCHEMAS/world-actor-state.schema.json`;
- `DEV/SCHEMAS/world-asset-state.schema.json`;
- `DEV/SCHEMAS/world-effect-state.schema.json`;
- `DEV/SCHEMAS/actor-archetype-data.schema.json`;
- `DEV/CATALOG/entity-structures.json`;
- legacy `GAME/SCHEMA/pc.schema.yaml`;
- legacy `GAME/SCHEMA/npc.schema.yaml`;
- legacy `GAME/SCHEMA/item.schema.yaml`;
- Actor/Asset CORE consumers.

---

## 3. Unified Actor model

PC, NPC, companion, summon, swarm and other character-like beings remain one record class:

```text
world.actor
```

Role/facet distinctions do not create separate semantic owners.

Current authoritative state families are:

```text
name
roles?
location_id?
build?
abilities?
hp?
life_state_id?
life_state_policy_id?
life_state_progress?
resources?
continuity?
details?
```

Explicit non-owners:

- copied inventory;
- copied active Effects/Conditions;
- copied epistemic state;
- flattened derived mechanics sheet;
- generic relationship record.

Inventory derives from Assets; Conditions derive from Effects; epistemics belong to `world.knowledge`; player exposure belongs to `runtime.disclosure`.

---

## 4. R2.2 Actor-private continuity realization

`world.actor` now has one optional typed `continuity` block:

```text
continuity
    foundation?
    evolving?
    relationships?
```

### Foundation

Sparse persistent private identity material:

```text
values
temperament
identity
```

Entries are concise statements with optional accepted source refs.

### Evolving continuity

Only baseline durable near-state:

```text
long_term_goal
current_objective
next_intention
material_commitments[]
reconsideration_cues[]
```

No chain-of-thought, reasoning trace, strategy DAG or generic plan graph is stored.

### Directed relationships

Stored under source Actor:

```text
Actor A
    continuity.relationships[B]
```

`A -> B` and `B -> A` are independent.

Facets:

```text
trust
affinity
fear
respect
hostility
felt_obligation
```

Initial sparse qualitative magnitude:

```text
low | moderate | high
```

Absent facet means not materially tracked, not neutral zero.

No generic `world.relationship` is restored.

### Transient private state

No durable baseline field exists. Affect/attention/urgency/local intention remain ephemeral unless a later proven consumer justifies a bounded persisted lifecycle.

---

## 5. Reconstructable build model

Reverse audit found a real architecture gap: the previous unified Actor `build` contained only singular level/class/subclass fields and could not reconstruct a complete READY_PC for multiclass/advancement/spell-selection cases.

Old shape was replaced clean-slate by:

```text
build
    species_id?
    background_id?
    class_progression[]
        class_id
        level
        subclass_id?
    choice_bindings?
        <stable advancement choice ID> -> [selected definition IDs]
    spellcasting?
        known_spell_ids?
        prepared_spell_ids?
        spellbook_spell_ids?
```

Rules:

- `class_progression` required when `build` exists;
- total level is derived, not duplicated;
- single-class and multiclass use one shape;
- selected feats/features/proficiencies/etc. are represented by stable choice bindings to reusable definitions instead of copied mechanics;
- mutable spell membership is stored only when rules require it;
- AC, attack/save/skill modifiers, proficiency bonus, spell DC and similar values remain derived MechanicalContext/HOT data.

WP-06 must define the final advancement choice-definition contract and stable choice IDs needed to validate `choice_bindings`.

---

## 6. Gameplay-first progressive character creation

Owner corrected the former interpretation that a full READY_PC must exist before gameplay begins.

Canonical model is now:

```text
campaign scaffold
    -> gameplay starts with provisional PC
    -> identity/build facts emerge naturally through play
    -> PROVISIONAL_IDENTITY durability boundary when stable identity is relied upon
    -> gameplay continues while mechanics materialize progressively
    -> READY_PC completeness becomes true
    -> coherent READY_PC durability transaction
    -> ordinary unrestricted mechanics-capable play / PLAY_READY
```

The campaign may remain lifecycle `initializing` while genuine player-facing gameplay is already occurring. Lifecycle status is not the definition of whether play has begun.

### Local mechanical sufficiency before READY_PC

A provisional PC may resolve a specific mechanically relevant outcome only if all material dependencies for **that outcome** are already established and no unresolved build choice can change legality/probability/consequence.

Otherwise the Master must not guess. The scene remains gameplay; only that mechanical boundary is blocked until the minimal required dependency/choice is established.

READY_PC is a continuously reevaluable deterministic completeness predicate, not a ceremonial command.

When it becomes true, runtime persists the complete reconstructable character using the same stable Actor ID.

---

## 7. Actor name language correction

Reverse audit found that `world.actor.name` reused a definition-localized-text rule requiring an English `en` value.

That requirement is valid for reusable catalog definitions under `CATALOG_CONTRACTS.md`, but not for a concrete campaign Actor.

`world.actor` now permits any one established language form, e.g.:

```json
{"name": {"ru": "Бдыр"}}
```

Runtime must not invent an English translation/transliteration merely to satisfy schema.

---

## 8. HP / LifeState / Resource / Effect ownership

Confirmed without architectural change:

### HP

`Actor.hp` is sole owner of:

```text
current
maximum_base
maximum_adjustment
temporary
```

Generic Resources cannot duplicate HP/temp HP.

### LifeState

Separate Actor authority:

```text
life.active
life.dying
life.stable
life.dead
```

Zero HP does not itself mean death.

### ResourceState

- persistent Actor resource -> Actor state;
- persistent Asset resource -> Asset state;
- procedure-local budget -> Procedure owner;
- capacity/availability may be derived.

Temporal Agenda is a derived due index.

### Conditions / Effects

Condition application is represented through `world.effect` referencing a Condition definition. Actor has no condition list.

Effect owner retains only native application/lifecycle state. No copied effective Condition value, writable remaining countdown, arbitration winner/shadow state or generic stacks are introduced.

---

## 9. Asset model

`world.asset` remains one universal instance owner for items/equipment/objects/stacks.

Current placement uses at most one native path:

```text
owner_actor_id
container_asset_id
location_id
```

Inventory/contents are reverse projections.

Asset state does not store:

- `identified_by_pc_ids`;
- `secret_ids`;
- copied contents/inventory arrays;
- universal legal ownership;
- duplicated attack/effect mechanics.

Durability remains direct Asset state when materialized and is not duplicated into generic Resources.

`definition.actor_archetype` catalog inventory was corrected to include its already-supported reusable base `hp` field.

---

## 10. Legacy shipped schema disposition

Existing:

- `GAME/SCHEMA/pc.schema.yaml`;
- `GAME/SCHEMA/npc.schema.yaml`;
- `GAME/SCHEMA/item.schema.yaml`

are **STALE PRE-R2.7 SCHEMA FAMILIES**.

They still contain parallel mechanics, knowledge, relationship, inventory, identification and Secret-like fields.

Repository search found no active loader/tool dependency on these files beyond schema documentation/index references.

Under owner-approved clean-slate policy they require **no migration compatibility layer**. WP-10 must remove/replace them with final unified shipped Actor/Asset/Effect schema families.

---

## 11. Stale prose discovered outside WP-04 ownership

Current `RUNTIME.md` / `CAMPAIGN_SETUP.md` still contain old wording such as `pre-live`, `true live scene` and statements implying that onboarding fiction is not real play.

After the owner correction these are classified as stale routing/lifecycle prose, not competing product semantics.

They are forwarded to WP-19/WP-26 for whole-module cleanup so terminology is globally consistent.

---

## 12. Verification

WP-04 regression contract:

- `DEV/TESTS/test_r2_7_wp04_actor_asset_conformance.py`.

RED phases were established before each material schema correction:

1. missing R2.2 `continuity`;
2. non-reconstructable singular build shape;
3. world Actor name unnecessarily requiring `en`.

Fresh repository read-back confirms intended source-level GREEN state:

- Actor continuity exists and excludes epistemics/inventory/conditions;
- build uses class progression + choice bindings + optional spell state;
- campaign Actor names require no English form;
- Asset placement/resource/durability owner remains single;
- Effect state contains no duplicate Condition/effective-duration owner fields;
- gameplay-first onboarding/readiness CORE contracts are updated.

As with WP-03, executable full-suite CI evidence is deferred to WP-22 because current workflow triggers do not run this branch and no audit branch/workaround will be created.

---

## 13. Forward obligations

| ID | Target | Obligation |
|---|---|---|
| WP-04/F01 | WP-06 | define final advancement schema, stable choice IDs and validation of Actor `choice_bindings`; verify full D&D READY_PC capability reconstruction |
| WP-04/F02 | WP-07 | ensure no Actor/Asset/Effect-adjacent field reintroduces epistemic/disclosure aliases |
| WP-04/F03 | WP-10 | replace/remove legacy shipped PC/NPC/item schema families with final unified Actor/Asset/Effect schemas |
| WP-04/F04 | WP-11 | finalize Actor/Asset/Effect IDs and physical roots/sharding without changing semantic owner model |
| WP-04/F05 | WP-12 | define HOT/SQLite projections for Actor build/continuity/Asset/Effect while preserving owner semantics |
| WP-04/F06 | WP-13 | map Actor/Asset/Effect state and progressive materialization into persistence/durability transitions |
| WP-04/F07 | WP-19 | align bootstrap/campaign lifecycle with gameplay-first provisional onboarding and READY_PC convergence |
| WP-04/F08 | WP-22 | execute WP-04 regression/schema validation and add integration tests for provisional-play local mechanical sufficiency |
| WP-04/F09 | WP-24 | verify complete D&D domain coverage against reconstructable Actor build and derived mechanics surfaces |
| WP-04/F10 | WP-26 | remove stale `pre-live/not true live play` wording and stale PC/NPC/item schema routing references |

---

## 14. Diamond / Strong disposition

Relevant Round-2 items:

- D10 stable identity vs mutable continuity vs transient state: **APPLIED** inside unified Actor.
- D11 objective/observed/private distinctions: **PRESERVED**; Actor continuity does not absorb `world.knowledge`.
- D12 directed relationships: **APPLIED** as source-Actor-owned sparse views.
- D13 sparse/event-driven cognition: **APPLIED**; no universal Actor cognition blob.
- S07 cognition modes: **MACHINE VOCABULARY ALREADY REGISTERED**, no extra durable owner.
- S10 `NO_CHANGE`: **PRESERVED**.
- S11 temporary private state: **BASELINE EPHEMERAL**, no durable field without proven lifecycle.
- S08/S09/S12/S13 remain dormant/conditional unless later evidence activates them.

---

## 15. Closure verdict

```text
VERDICT: CLOSED
ARCHITECTURE_BLOCKERS: 0
OWNER_GATE: NONE
UNIFIED ACTOR/ASSET MODEL: ACCEPTED + MACHINE-ALIGNED
GAMEPLAY-FIRST ONBOARDING: ACCEPTED + CORE-ALIGNED
LEGACY SHIPPED SCHEMAS: STALE / REMOVE-REPLACE IN WP-10
EXECUTABLE FULL-SUITE VERIFICATION: WP-22
NEXT_DOMAIN: WP-05
```

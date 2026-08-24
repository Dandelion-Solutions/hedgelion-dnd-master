# WP-04 — Actor / Asset / mechanical-state model

Статус: **CLOSED — READ-BACK VERIFIED AFTER OWNER CLARIFICATION**

Date: 2026-08-24

## 1. Итог

WP-04 завершил whole-project audit Actor / Asset / Effect mechanical state и после дополнительного owner clarification уточнил границы ранней канонизации героя и READY_PC.

```text
UNIFIED ACTOR OWNER: CONFIRMED
UNIFIED ASSET OWNER: CONFIRMED
HP / RESOURCE / EFFECT / CONDITION OWNER SPLIT: CONFIRMED
R2.2 ACTOR CONTINUITY: MATERIALIZED
EARLY PROVISIONAL ACTOR PERSISTENCE: CONFIRMED
READY_PC: INITIAL MECHANICAL COMMITMENT FRONTIER
RECONSTRUCTABLE PC BUILD: MATERIALIZED
NAME REQUIRED FOR ACTOR IDENTITY: NO
SITUATION-AWARE LATE MECHANICAL SELECTION: FORBIDDEN
NEW OWNER DECISION REQUIRED: 0
```

Owner-approved clarification:

> герой может быть канонизирован и сохранён значительно раньше полного механического завершения; имя не является обязательным первым якорем. READY_PC означает закрытый initial mechanical commitment frontier, а не 100% заполненный character dossier. Значения, которые безопасно выводятся из уже зафиксированных class/species/archetype/level/feature anchors, могут materialize lazily. Открытые discretionary choices, которые могли бы дать ситуационное преимущество, до READY_PC оставлять нельзя.

Owning clarification:

- `DEV/docs/superpowers/specs/2026-08-24-r2-7-wp-04-progressive-ready-pc-owner-clarification.md`.

---

## 2. Source Manifest delta

Основные owning sources:

- `DEV/ARCHITECTURE/ACTOR_MODEL.md`;
- `DEV/ARCHITECTURE/ASSET_MODEL.md`;
- Step-2 mechanical-state ownership and assurance specs;
- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-24-r2-7-wp-04-progressive-ready-pc-owner-clarification.md`;
- Step-4 truth/knowledge boundary;
- Step-5 durability/currentness boundary;
- `GAME/CORE/CHARACTER.md`;
- `GAME/CORE/CHARACTER_READINESS.md`;
- `GAME/CORE/DIEGETIC_ONBOARDING.md`;
- `GAME/CORE/DURABILITY_GUARD.md`.

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

Actor record identity is its stable record ID. **No state field, including `name`, is universally required merely to create the Actor.**

Current authoritative state families are:

```text
name?
concept?
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

`concept` is a compact nonmechanical current framing such as `огненный демон`. It may guide preparation/inference but cannot itself be consumed as mechanics. Rules-valid mechanical consequences must be represented by native archetype/build/Actor/Asset/Effect owners.

Explicit non-owners:

- copied inventory;
- copied active Effects/Conditions;
- copied epistemic state;
- flattened derived mechanics sheet;
- generic relationship record;
- raw concept prose as executable capability authority.

Inventory derives from Assets; Conditions derive from Effects; epistemics belong to `world.knowledge`; player exposure belongs to `runtime.disclosure`.

---

## 4. R2.2 Actor-private continuity realization

`world.actor` has one optional typed `continuity` block:

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

Reverse audit found a real architecture gap: the previous unified Actor `build` contained only singular level/class/subclass fields and could not reconstruct a mechanically committed multiclass/advancement/spell-selection state.

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

WP-06 must define final advancement choice-definition contract and stable choice IDs needed to validate `choice_bindings`.

---

## 6. Gameplay-first progressive character creation

Canonical sequence:

```text
campaign scaffold
    -> gameplay begins with provisional PC
    -> stable protagonist anchor is adopted
    -> PROVISIONAL_IDENTITY durable write
    -> gameplay continues while Master rapidly materializes initial mechanics
    -> READY_PC initial mechanical commitment frontier
    -> coherent READY_PC / PLAY_READY durability frontier
    -> ordinary unrestricted play + safe lazy materialization / normal evolution
```

Campaign lifecycle may remain `initializing` while genuine player-facing gameplay is occurring.

### 6.1 PROVISIONAL_IDENTITY is intentionally early

PROVISIONAL_IDENTITY no longer means “we know the name”. It fires once a stable protagonist/Actor anchor has been adopted and losing it would make resume wrong.

Examples:

- `я буду демоном огня`;
- an established name;
- an accepted archetype/build anchor;
- another unambiguous player-authored protagonist identity fact.

The same Actor ID survives the entire transition to READY_PC.

The first durable Actor write therefore must not wait for full mechanical completion.

### 6.2 Local mechanical sufficiency before READY_PC

A provisional PC may resolve a bounded mechanically relevant outcome when every dependency for that specific outcome is already committed or uniquely derivable from committed anchors and no open discretionary choice could change the result.

Otherwise the Master does not guess and does not cross that mechanical boundary. The scene remains gameplay.

### 6.3 Fast mechanical materialization

When bookkeeping is delegated, use:

```text
1. explicit player statement/choice
2. deterministic rules inheritance
3. strong rules-valid concept inference
4. campaign/rules default
5. deterministic conservative Master default
6. targeted player question only if materially different legal choices remain
```

A player is not asked for engine-derived values such as max HP/resource capacity merely because they are mechanically necessary.

Example:

```text
player concept: огненный демон
    -> accepted compatible archetype/build
    -> implied rules-valid capabilities/resources/values
    -> native mechanical owners
```

The concept is evidence/input to preparation, not the mechanical owner itself.

### 6.4 READY_PC is not a 100%-filled dossier

READY_PC means ordinary current-play mechanics no longer depend on strategically open initial choices.

It normally commits sufficient anchors for:

- current build/archetype/level progression;
- common checks/saves;
- ordinary proficiency/capability eligibility;
- HP/LifeState;
- defenses/movement;
- mechanically significant equipment;
- current core resources/actions;
- applicable spellcasting/feature selections;
- every other initial discretionary choice whose alternatives could materially change ordinary play.

Derived values may remain lazy.

### 6.5 Safe post-READY laziness

After READY_PC, a missing value is safe when it is:

- uniquely deterministic from committed anchors;
- descriptive/nonmechanical;
- introduced at a genuine later level-up/acquisition/preparation boundary;
- governed by a selection policy fixed before the situation where it matters.

### 6.6 Anti-retrofit

Forbidden pattern:

```text
leave choice open
    -> observe current obstacle/encounter
    -> choose the option that is now advantageous
```

If a choice could affect ordinary current play, it must be fixed before READY_PC without situation-aware optimization.

---

## 7. Actor naming / identity corrections

Two separate bugs were corrected:

1. campaign Actor names no longer require an English `en` form;
2. `name` itself is no longer a universal Actor-state requirement.

Valid examples now include:

```json
{"name": {"ru": "Бдыр"}}
```

and an unnamed provisional protagonist:

```json
{"concept": "огненный демон", "roles": ["actor.player_character"]}
```

Runtime must not invent an English translation/transliteration merely to satisfy schema and must not invent a name merely to create a stable Actor ID.

---

## 8. HP / LifeState / Resource / Effect ownership

Confirmed without architecture change.

### HP

`Actor.hp` is sole owner of:

```text
current
maximum_base
maximum_adjustment
temporary
```

Generic Resources cannot duplicate HP/temp HP. Maximum HP may be derived from accepted build/archetype/rules anchors rather than asked from the player.

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

A resource capacity such as a class/archetype-dependent pool is normally derived from accepted definitions/anchors, not player questionnaire input.

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

remain **STALE PRE-R2.7 SCHEMA FAMILIES**.

The old PC schema additionally contains an obsolete invariant forbidding narrative/concept inference for exact mechanics. The final model instead permits rules-valid concept-guided preparation but requires native mechanical commitments before adjudication.

Under clean-slate policy no migration compatibility layer is required. WP-10 must remove/replace these schemas with final unified Actor/Asset/Effect families.

---

## 11. Stale prose outside immediate WP-04 owner edits

Some setup/bootstrap surfaces still use wording such as `pre-live` / `first true live scene` and stronger “complete sheet before activation” language.

They are now classified as stale routing/lifecycle prose. WP-19/WP-26 must remove them globally. The updated `CHARACTER`, `DIEGETIC_ONBOARDING`, `CHARACTER_READINESS` and `DURABILITY_GUARD` contracts own the corrected semantics meanwhile.

---

## 12. Verification

WP-04 regression contract:

- `DEV/TESTS/test_r2_7_wp04_actor_asset_conformance.py`.

RED phases were established before material schema corrections:

1. missing R2.2 `continuity`;
2. non-reconstructable singular build shape;
3. world Actor name unnecessarily requiring `en`;
4. `name` incorrectly required for every Actor and no typed `concept` anchor for unnamed provisional PC.

Fresh repository read-back is required before final cursor continuation. Executable full-suite CI remains WP-22 because current workflow triggers do not run this branch and no audit branch/workaround will be created.

---

## 13. Forward obligations

| ID | Target | Obligation |
|---|---|---|
| WP-04/F01 | WP-06 | define final advancement schema, stable choice IDs and validation of Actor `choice_bindings`; prove the READY_PC initial commitment frontier for D&D choices |
| WP-04/F02 | WP-07 | ensure no Actor/Asset/Effect-adjacent field reintroduces epistemic/disclosure aliases |
| WP-04/F03 | WP-10 | replace/remove legacy shipped PC/NPC/item schema families with final unified Actor/Asset/Effect schemas |
| WP-04/F04 | WP-11 | finalize Actor/Asset/Effect IDs and physical roots/sharding without changing semantic owner model |
| WP-04/F05 | WP-12 | define HOT/SQLite projections for Actor build/continuity/Asset/Effect while preserving owner semantics |
| WP-04/F06 | WP-13 | map early PROVISIONAL_IDENTITY, READY_PC initial commitment and later lazy materialization into persistence/durability transitions |
| WP-04/F07 | WP-19 | align bootstrap/campaign lifecycle with gameplay-first provisional onboarding and READY_PC activation semantics |
| WP-04/F08 | WP-22 | execute WP-04 regression/schema validation; test provisional persistence, concept-guided defaults, no situation-aware retrofit and safe lazy post-READY derivation |
| WP-04/F09 | WP-24 | verify D&D domain coverage against the initial commitment frontier and reconstructable Actor build |
| WP-04/F10 | WP-26 | remove stale `pre-live/not true live play`, complete-dossier and legacy PC/NPC/item routing wording |

---

## 14. Diamond / Strong disposition

Relevant Round-2 items:

- D10 stable identity vs mutable continuity vs transient state: **APPLIED**; stable Actor ID is not dependent on name.
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
VERDICT: CLOSED AFTER OWNER CLARIFICATION
ARCHITECTURE_BLOCKERS: 0
OWNER_GATE: NONE
UNIFIED ACTOR/ASSET MODEL: ACCEPTED + MACHINE-ALIGNED
EARLY PROVISIONAL PERSISTENCE: ACCEPTED
READY_PC: INITIAL MECHANICAL COMMITMENT FRONTIER
SITUATION-AWARE RETROFIT: FORBIDDEN
LEGACY SHIPPED SCHEMAS: STALE / REMOVE-REPLACE IN WP-10
EXECUTABLE FULL-SUITE VERIFICATION: WP-22
NEXT_DOMAIN: WP-05
```

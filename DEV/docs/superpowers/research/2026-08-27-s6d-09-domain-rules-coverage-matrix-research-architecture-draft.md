# S6D-09 — Domain Rules Coverage Matrix — Research & Architecture Draft

Status: **STEP 2 COMPLETE — MATERIAL PRODUCT-SCOPE DECISION FOUND**

Date: 2026-08-27

## 1. Result

The current exact built-in seed and the current shipped gameplay guidance do not describe the same supported surface.

The identity-bound package is explicitly a bounded, non-full-corpus profile:

```text
Human + Criminal
Fighter 1–2
Sorcerer 1
six exact spells
exact ranged attack / feature / spell Activities
HP/LifeState, four bounded resource families, one exact Effect
READY_PC and one later Fighter advancement boundary
```

That slice has real closed machine routes. However, current `GAME/CORE` owners also direct the runtime to support reusable mechanics outside that closure: general uncertain checks, initiative and turn budgets, ordinary movement and spatial rulings, reactions, equipment/ownership changes, hazards/exploration consequences, social checks, and reward/economy ownership transitions. Several corresponding registered primitives are deliberately `DORMANT_NONSELECTABLE`, and several families have no exact admitted Activity/definition consumer.

This is not permission to activate them. It is a product-promise mismatch requiring one bounded human scope decision before the final matrix can classify the rows honestly.

## 2. Source Manifest

### Canonical process/status

- `AGENTS.md`; `DEV/DESIGN_PROCESS.md`; `DEV/ARCHITECTURE/DESIGN_PROCESS.md` — process, evidence and decision-rights owners.
- `DEV/PROJECT_MAP.md`; `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` — derivative routing/status.
- S6D owner decision, umbrella brief/plan and S6D-09 Step-1 brief/critic — current scope and loop boundary.

### Canonical package/catalog owners

- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`, `CATALOG_RESOLUTION.md`, `CATALOG_CONTRACTS.md`, `CATALOG_ADMISSION.md`.
- `DEV/CATALOG/core-catalog.json`, `catalog-admission-ledger.json`, `entity-structures.json`, `identifier-policies.json` and their strict schemas/tests.

### Canonical deterministic-mechanics owners

- `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, `CALCULATION_SELECTOR_METADATA.md`, `MECHANICAL_CONTEXT.md`, `PORTABLE_ACTIVITY_VALUES.md`, `ACTIVITY_PRIMITIVE_CONTRACTS.md`, `CHARACTER_PROGRESSION_READY_PC_SEED.md`, `HEALTH_EFFECTS_RECOVERY.md`.
- Their exact machine catalogs, schemas and S6D-02…08 focused tests.
- Step-3 ExecutionSegment/MechanicalEvent/Resolution/Continuation/receipt contracts and Step-5 retry, reaction, chronology, durability and recovery owners routed by `PROJECT_MAP.md`.

### Current package and machine evidence

- `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-capabilities.json`.
- `character-mvp-seed.json`, `health-effects-recovery-seed.json`, `NOTICE.md`.
- `DEV/CATALOG/mechanical-surfaces.json`, `activity-primitive-contracts.json`, `portable-value-contracts.json`, `portable-value-routes.json`.

### Product/runtime claim owners

- `GAME/CORE/RUNTIME.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`, `PLAY_POLICY.md`, `ADJUDICATION.md`.
- `CHARACTER.md`, `CHARACTER_READINESS.md`, `DIEGETIC_ONBOARDING.md`, `COMBAT.md`, `ENCOUNTERS.md`, `MAGIC.md`, `EXPLORATION.md`, `DIALOGUE.md`, `ADVANCEMENT.md`, `REWARDS.md`, `CHRONOLOGY.md`, `MULTIPLAYER.md`, `LIVE_SCENE.md`.
- `GAME/RULES/README.md`, `INDEX.md`, `OFFICIAL_SOURCES.md`.

All owning files above were inspected on remote HEAD `6933208437f8bd58b979cf552b5d901d27f0a87b`. Routing/index prose was not used as semantic authority.

## 3. Exact finite-set extraction

### 3.1 Package closure

The two semantic seed files contain 169 distinct stable machine tokens after exact recursive extraction. This set includes definitions, options, activities, operations, selectors, resources, boundaries, policies and typed compiled symbols; it is not treated as 169 independent player capabilities.

The human-readable closure is:

- 24 primary character definitions;
- 8 support definitions;
- 21 registered base values;
- 12 exact Activity definitions;
- 40 declared external dependency IDs, some resolved by the support/value/Activity lists;
- 11 exact active primitive IDs referenced by the Activities;
- the health/effects/recovery policy, boundary and transition tokens required by the second seed.

`character-capabilities.json` explicitly says `full_srd_character_corpus=false` and `unsupported_content_policy=ABSENT_NONSELECTABLE`.

### 3.2 Active machine surface

Current machine evidence contains:

- 10 selector contracts;
- 9 active mechanical accessors plus one dormant accessor;
- 4 active internal derived nodes;
- 17 active structural portable values and dormant `value.signal` / `value.state_delta`;
- 11 `COMPLETE / ACTIVE_ADMITTED` primitives with exact seed consumers;
- 20 quarantined primitives.

The quarantined set includes `op.resolve_contest`, `op.set_temporary_hp`, `op.restore_resource`, `op.move_entity`, `op.teleport_entity`, `op.transfer_asset`, `op.transfer_currency`, entity/effect/zone mutations, `op.request_choice`, `op.open_reaction_window`, `op.schedule_followup`, and `op.advance_local_time`.

The admission ledger currently has 576 entries: 473 `ACTIVE_ADMITTED`, 35 `EMBEDDED_NONOWNER`, and 68 `DORMANT_NONSELECTABLE`. Twenty-four reusable definition families still route realization to S6D-09. Family admission is not concrete content or executable support.

### 3.3 Product-promise keys

Product keys were extracted at the reusable mechanic/capability/consequence level. Individual utterances, cinematic maneuvers and creative fictional actions were excluded. Novel expression remains:

```text
player expression -> GM interpretation/fiction -> bounded typed adjudication -> existing deterministic consequence
```

The current product-owner set contains these reusable families:

```text
PROMISE.RESOLUTION.CLASSIFICATION
PROMISE.RNG.ACTUAL_FIXED_TRACEABLE
PROMISE.CHECK.GENERAL
PROMISE.SAVE.GENERAL
PROMISE.OPPOSED_OR_CONTESTED_RESOLUTION
PROMISE.COMBAT.INITIATIVE_TURN_ACTION_MOVEMENT
PROMISE.COMBAT.ATTACK_DAMAGE_HEALING_DEATH
PROMISE.COMBAT.REACTION_SUSPEND_RESUME
PROMISE.SPATIAL.TARGET_RANGE_AREA_VISIBILITY_COVER
PROMISE.DAMAGE.DEFENSE_TRANSFORMATION
PROMISE.EFFECT.CONDITION_CONCENTRATION_DURATION
PROMISE.MAGIC.KNOWN_SPELL_RESOURCE
PROMISE.ASSET.OWNERSHIP_EQUIP_USE_TRANSFER
PROMISE.REST.QUALIFICATION_OWNER_LOCAL_RECOVERY
PROMISE.CHARACTER.READY_PC_ADVANCEMENT
PROMISE.EXPLORATION.HAZARD_TIME_RESOURCE_CONSEQUENCE
PROMISE.SOCIAL.UNCERTAIN_CHECK
PROMISE.REWARD.ECONOMY_OWNERSHIP_TRANSITION
PROMISE.OPEN_EXPRESSION.BOUNDED_ADJUDICATION
PROMISE.MECHANICAL_NULL.RESULT_WITHOUT_WORLD_MUTATION
```

## 4. Preliminary support ledger

| Key/family | Package presence | Product scope evidence | Realization | Preliminary disposition |
|---|---|---|---|---|
| resolution classification / actual RNG | present structurally | explicit | complete | `IN_SUPPORTED_MVP` |
| exact ranged attack, spell attack/save, damage | present exact consumers | explicit | complete | `IN_SUPPORTED_MVP` |
| Second Wind healing and exact resource consumption | present | explicit | complete | `IN_SUPPORTED_MVP` |
| HP/temp HP/LifeState/death/stable recovery | present | explicit | complete | `IN_SUPPORTED_MVP` |
| exact rest responders after accepted boundary | present | explicit | complete | `IN_SUPPORTED_MVP` |
| READY_PC and Fighter 1→2 advancement | present | explicit | complete | `IN_SUPPORTED_MVP` |
| exact innate-sorcery Effect/duration | present | explicit | complete | `IN_SUPPORTED_MVP` |
| Mechanical-Null attack miss/save-no-consequence | present | explicit | complete without mutation/event fabrication | `IN_SUPPORTED_MVP` |
| general ability/skill check | no generic exact Activity consumer | explicit in ADJUDICATION/EXPLORATION/DIALOGUE | incomplete | `SUPPORTED_GAP` |
| general saving throw outside exact spells | no generic exact consumer | explicit in COMBAT/mechanical gate | incomplete | `SUPPORTED_GAP` |
| contest/opposed route | primitive quarantined | opposition accepted by adjudication; exact contest semantics not fixed | incomplete/scope ambiguous | `UNRESOLVED_PRODUCT_SCOPE` |
| initiative/turn/action/movement budgets | partial procedure owner; no closed supported procedure seed | explicit in COMBAT | incomplete | `SUPPORTED_GAP` |
| reaction suspension/resume | portable structure active; primitive quarantined; no exact seed consumer | explicit in COMBAT surface | incomplete/scope ambiguous | `UNRESOLVED_PRODUCT_SCOPE` |
| movement/range/visibility/cover/reach | exact target/area shapes only; visibility/reach facts dormant; move primitive quarantined | explicit in COMBAT/EXPLORATION | incomplete | `SUPPORTED_GAP` |
| resistance/immunity/vulnerability | selector metadata exists; no concrete package definitions/consumer proof | combat damage promise | incomplete/scope ambiguous | `UNRESOLVED_PRODUCT_SCOPE` |
| concentration | no concrete supported definition/consumer | explicit in COMBAT/MAGIC | incomplete | `SUPPORTED_GAP` |
| significant Asset ownership/equip/use/transfer | starting Assets present; transfer primitive quarantined | explicit in CHARACTER/COMBAT/REWARDS | incomplete | `SUPPORTED_GAP` |
| hazards/exploration mechanical consequences | no hazard definition/activity; move/time primitives quarantined | explicit in EXPLORATION/ENCOUNTERS | incomplete | `SUPPORTED_GAP` |
| social uncertain checks | no generic check consumer | explicit in DIALOGUE/ADJUDICATION | incomplete | `SUPPORTED_GAP` |
| reward/currency/ownership transitions | no exact economy seed; transfer primitives quarantined | explicit in REWARDS | incomplete | `SUPPORTED_GAP` |

Package absence was not used as out-of-scope evidence. No row above activates a dormant primitive.

## 5. Atomic route findings

### Closed representative route

`activity.attack.ranged_weapon` has an exact package consumer and routes through target selection, fixed roll, attack resolution, damage transformation, Actor HP/LifeState ownership, ExecutionSegment commit, MechanicalEvent only for committed fact, and receipt evidence. A miss is a valid Mechanical-Null route: the Resolution may commit an eventless/zero-affected-revision segment and receipt outcome while RNG/input/retry evidence remains with its exact owners. No StateDelta/Actor/Effect mutation is fabricated.

### Bounded adjudicated route

The accepted Activity binding boundary can freeze typed invocation facts/parameters from the GM where semantic judgment is genuinely required. It cannot supply RNG, HP, capability, resource availability or mutation authority. Current dormant `fiction.target_visible` and `fiction.target_reachable` facts prove shape availability, not activation; a real supported consumer is still required.

### Product-text inconsistency

`MECHANICS_INTEGRITY.md`, `ADJUDICATION.md` and `RANDOMNESS.md` still use wording that every random resolution must produce a “state delta”. That is narrower than current Step-3/S6D-05 law, which permits a valid result with no authoritative world mutation. This is a technical wording repair, not a product decision: the eventual candidate must say typed consequence/outcome plus mutation only when an authoritative fact changes.

## 6. Alternatives

### A — Exact-seed-only product promise

Declare only the currently closed Fighter/Sorcerer routes supported by the built-in MVP; scope all other reusable families out and narrow affected CORE language.

Benefit: smallest closure. Cost: the built-in package cannot honestly promise ordinary general checks, initiative-scale combat procedure, exploration/social mechanical checks or common ownership changes. That weakens “playable” toward a combat-feature conformance slice.

### B — Treat every broad CORE family as current MVP support

Close every listed gap now, including economy, hazards, concentration, reaction, movement, contests and general equipment behavior.

Benefit: strongest match to broad runtime prose. Cost: large expansion, likely new definitions and multiple Primitive Necessity Challenges; conflicts with the bounded vertical-slice objective and risks rebuilding a broad corpus.

### C — Minimal playable gameplay spine (recommended)

Keep the exact character/content slice, but require the minimum reusable domain spine needed for honest open-ended play:

- general typed check and save routes;
- initiative/turn/action/movement procedure route;
- bounded spatial inputs sufficient for those exact Activities;
- basic Asset ownership/equip/use and transfer consequence;
- hazard and social uncertainty lowered through the same general check route;
- reward ownership transfer through the same bounded Asset consequence;
- existing exact combat/spell/health/rest/readiness/advancement routes.

Keep contest-specific resolution, generic reactions without an exact consumer, broad damage-defense content, concentration content, currency economy, crafting/downtime systems, teleportation/zones/entities and full equipment/spell/hazard corpora absent/nonselectable until a concrete supported consumer proves necessity.

This preserves the hourglass: a few reusable deterministic consequences support many natural-language situations without enumerating actions or activating generic mutation infrastructure.

## 7. Analytical challenge

Strongest case against C: “playable” can be interpreted narrowly enough that general checks and movement are handled entirely as prose/typed adjudication without new machine routes. That fails the accepted law when an uncertain result or durable consequence matters: prose may provide inputs, but it cannot own RNG or deterministic consequence.

Simplest viable comparison: A is simpler, but it excludes ordinary D&D interaction families explicitly promised by current runtime owners. B is comprehensive but violates the accepted bounded seed and YAGNI constraints. C adds only shared consequence routes with multiple current consumers.

Recommendation confidence: **HIGH** that a product decision is required; **MEDIUM-HIGH** that C is the minimal coherent answer.

Evidence that would change the recommendation: a current canonical owner explicitly declaring the broad CORE mechanic statements conditional/non-promissory for the built-in MVP, or an existing admitted generic route proving the listed gaps already complete without new activation.

## 8. Completeness gate

- Source Manifest covers package identity/admission, S6D-03…08, Step-3/5 execution/recovery, House Rules, shipped domain owners, schemas and tests.
- Actual owners were inspected; indexes were routing only.
- Exact package and machine sets were extracted rather than sampled.
- Product keys exclude utterances/examples and preserve conditional qualifiers.
- Active versus dormant registration was kept distinct from support.
- No S6D-01…08 owner was reopened merely for overlap.
- The remaining question changes product scope and therefore belongs to the human architect.



# S6D-07 Step 4 — Collaborative Review

Status: **COMPLETE — PROCEED TO STEP 5**

## 1. Accepted profile

The built-in package exposes a capability-declared **MVP character slice**, not the full SRD 5.2.1 corpus and not a character-builder questionnaire. The exact profile is intentionally narrow:

```text
species: Human
background: Criminal
martial class: Fighter, levels 1–2
spellcasting class: Sorcerer, level 1
later advancement proof: Fighter 1 -> 2
```

Why this set is minimal:

- one shared flexible species and background serve both paths;
- Fighter has the smallest direct martial proof and a deterministic meaningful level-2 advancement;
- Sorcerer avoids Wizard spellbook breadth and level-1 prepared/spellbook dual ownership;
- stopping Sorcerer at level 1 avoids Metamagic/Sorcery Point expansion;
- stopping Fighter at level 2 avoids subclass breadth;
- multiclassing, subclass selection and all other classes/species/backgrounds remain absent/nonselectable.

## 2. Exact minimal definition inventory

### Build roots

- `species.human`;
- `background.criminal`;
- `class.fighter`, `advancement.fighter.mvp_1_2`;
- `class.sorcerer`, `advancement.sorcerer.mvp_1`.

### Feats/features

- `feat.origin.alert` (Criminal automatic grant);
- `feat.origin.skilled` (Human recommended deterministic/delegated default);
- `feat.fighting_style.archery` and `feat.fighting_style.defense` (the one closed material Fighter style slot);
- Human Resourceful/Skillful capability declarations;
- Fighter level-1 Fighting Style, Second Wind, Weapon Mastery; level-2 Action Surge and Tactical Mind;
- Sorcerer level-1 Spellcasting and Innate Sorcery.

Feature identities may be separate `definition.feature` records only when reused or independently referenced. Pure class-table grants stay in class/advancement data rather than manufacturing empty feature records.

### Spells

Sorcerer level 1 requires four cantrips and two prepared level-1 spells. The minimal package must therefore contain exactly six selectable Sorcerer spells. The proposed set optimizes shared mechanics rather than breadth:

- cantrips: `spell.fire_bolt`, `spell.poison_spray`, `spell.thunderclap`, `spell.acid_splash`;
- level 1: `spell.magic_missile`, `spell.burning_hands`.

The six spells intentionally reuse only bounded target/roll/attack-or-save/damage contracts. `Burning Hands`, `Acid Splash`, `Poison Spray`, and `Thunderclap` cover saves; `Fire Bolt` covers an attack; `Magic Missile` covers deterministic multi-dart damage. Unlike Ray of Frost or Shocking Grasp, the selected cantrips require no durable secondary mechanical Effect. Multi-target/dart expansion uses the bounded `op.for_each_target` compiler form and creates no query engine.

### Assets/resources/value vocabularies

Only exact starting assets needed by the selected Fighter/Sorcerer equipment packages, Criminal package, spellcasting focus and ordinary currency are included. Skill/proficiency/ability/weapon/armor/tool IDs are limited to the options referenced above. Package compilation must reject every unresolved reference.

## 3. Choice policy

The package contains choices; onboarding does not expose them as a sequence of mandatory questions.

- Human size, skill and origin-feat selection use explicit concept first, then accepted deterministic/delegated defaults. `Skilled` is the recommended Human default.
- Criminal equipment package uses a predeclared campaign/delegated default unless player intent distinguishes equipment from currency.
- Fighter style is the representative material slot: infer Archery/Defense from explicit concept and accepted equipment; ask one compact question only when both remain materially compatible and no delegated policy resolves them.
- Sorcerer spell list uses an accepted recommended package loadout under delegated bookkeeping. A player may override before READY_PC; no six-question spell questionnaire is required.
- Actor bindings record selected owner-relative options and `selection_basis`; alternatives not packaged are not selectable.

## 4. Primitive Necessity Challenges

No primitive is activated merely because a definition references it.

### `op.select_targets`

Supported consumers: Fire Bolt, Magic Missile and exact spell targeting. Distinct necessity: converts a closed TargetSpec plus bound candidate roles into a validated bounded target set. Existing consequence transitions cannot own target eligibility; compiler lowering cannot evaluate runtime geometry/eligibility; GM adjudication may supply only authorized ambiguous facts, not authoritative target selection. Authority denied: no world search, no arbitrary entity discovery, no mutation, no persistence.

### `op.roll`

Supported consumer: Fighter attacks and Fire Bolt attack roll through a closed roll request. Distinct necessity: authoritative RNG generation and fixed retry evidence. Consequence transitions and GM adjudication cannot generate random authority; compiler lowering cannot supply runtime randomness. Authority denied: no DC/attack semantics, mutation or LLM-provided result.

### `op.resolve_attack`

Supported consumers: Fighter weapon attack and Fire Bolt. Distinct necessity: deterministic comparison of a fixed roll and exact selector-derived attack/defense inputs. A domain transition cannot decide hit/miss; compiler lowering cannot evaluate current modifiers; GM adjudication may provide only declared non-engine facts. Authority denied: no RNG generation, target mutation or damage application.

### `op.resolve_save`

Supported consumer: Burning Hands. Distinct necessity: deterministic comparison of each target's fixed saving-throw result with the caster's pinned save threshold. A consequence cannot decide success/failure, compiler lowering cannot know current modifiers and GM adjudication cannot replace admitted save arithmetic. Authority denied: no RNG generation, target discovery, damage application or mutation.

### `op.apply_damage`

Supported consumers: successful Fighter/Fire Bolt attacks and Magic Missile. Distinct necessity: typed damage components must pass mitigation/HP/LifeState owner rules into one atomic prospective transition. Generic consequences are insufficient because HP mutation and resistance ordering require exact deterministic ownership. Authority denied: no target discovery, hit decision, arbitrary state path, direct commit or lifecycle disposition.

### `op.apply_healing`

Supported consumer: Fighter Second Wind. Distinct necessity: typed healing must obey current HP maximum and LifeState rules inside the owning prospective Actor transition. Compiler lowering and adjudication cannot author health mutation. Authority denied: no target discovery, roll authority, maximum-HP change, arbitrary path or direct commit.

### `op.consume_resource`

Supported consumers: Sorcerer level-1 spell slots, Second Wind, Action Surge, Tactical Mind and Innate Sorcery. Distinct necessity: one atomic checked decrement of a named owner-bound resource is shared by otherwise distinct Activities. Compiler lowering cannot know current availability, and GM adjudication cannot mutate resource state. Authority denied: no resource creation/capacity change, arbitrary owner/path, grant selection or direct commit.

### `op.for_each_target`

Supported consumers: Acid Splash, Thunderclap, Magic Missile and Burning Hands after their typed target/dart bindings produce a bounded ordered target list. Distinct necessity: the same closed child resolution must be compiled once per already-selected target while retaining order and per-target exports. A variable bounded count cannot be hand-expanded at package compile time; GM adjudication cannot execute mutations. Authority denied: no discovery/query, unbounded iteration, child-authority widening, independent commit or undeclared child step.

### `op.request_choice` / `op.open_reaction_window` / effect operations

Not activated by character onboarding. Build choices occur at preparation/advancement boundaries and bind directly through accepted character policy/transaction semantics, not Activity suspension. No selected MVP spell requires a reaction window or durable Effect; S6D-07 does not activate these drafts.

### `op.resolve_check`

Supported consumer: Tactical Mind after a failed ability check and a frozen d10-plus-original-total roll request. It deterministically compares the augmented result to the original pinned DC before Second Wind is consumed. Authority denied: RNG, DC authorship, resource mutation and replacement of original check evidence.

### `op.create_effect`

Supported consumer: Innate Sorcery. Its one-minute self-owned spell-attack-advantage and spell-DC modifier requires a current typed Effect. Authority denied: arbitrary Effect authorship, target discovery, duration-owner bypass and direct commit.

The exact contract pins stable `(target, source, definition)` instance identity and a concrete one-minute TemporalBinding at the causing commit. Reapplication atomically replaces that identity; recovery reconstructs it from committed Effect evidence; the Temporal Agenda publishes expiry idempotently. The `attack.roll × rule.grant_advantage` pair is admitted only for spell attacks and uses the accepted advantage/disadvantage cancellation policy. S6D-08 retains every generic Effect/Duration decision.

### `op.emit_fact` — ACTIVE only for Action Surge entitlement

Supported consumer: Action Surge. Distinct necessity: the current-turn action-economy owner must receive one typed, mechanically consumable entitlement atomically with the resource decrement; prose and a receipt cannot alter preflight eligibility. The exact value grants one additional `resource.action` to the bound actor, excludes `activity.magic`, is consumed by the next eligible activation once, expires at the current-turn boundary and is replay-safe under the enclosing Resolution idempotency key. Authority denied: arbitrary facts, persistent Actor state, turn-boundary authorship, reusable credits and direct commit.

The eleven positively challenged primitives require exact completed contracts, dependency admission and Step-6 review in Step 5. If any exact contract cannot be proved, the dependent spell/feature must be removed or replaced; quarantine cannot be overridden.

## 5. Martial onboarding acceptance walkthrough

```text
player concept/input
  "trained archer / practical soldier" (or equally small compatible anchor)
-> Master inference
  Fighter, Dexterity emphasis, ranged equipment and Archery style are strongly compatible
-> inheritance/default/delegated bookkeeping
  Human + Criminal package default; legal ability assignment; recommended Human Skilled feat;
  starting assets, derived HP/proficiencies/defense/resources from package anchors
-> actual material question
  none when the concept/delegation resolves style; otherwise one compact Archery-vs-Defense question
-> provisional gameplay
  may start after stable Actor/concept; dialogue, movement and any locally sufficient interaction proceed
-> provisional mechanics
  only dependencies already committed; no attack if weapon/style/ability inputs remain materially open
-> closure
  bind style, skills/assets/abilities/HP/LifeState and exact class grants
-> READY_PC
  succeeds when ordinary Fighter mechanics reconstruct with no strategically open initial slot
```

At Fighter level 2, advancement adds Action Surge and Tactical Mind deterministically, updates class progression atomically, reconstructs dependent resources/capabilities and preserves retry/recovery evidence. It does not reopen the initial style.

## 6. Spellcaster onboarding acceptance walkthrough

```text
player concept/input
  "innate fire mage / dangerous natural talent"
-> Master inference
  Sorcerer and Charisma emphasis are strongly rules-valid
-> inheritance/default/delegated bookkeeping
  Human + Criminal; legal ability assignment; recommended six-spell MVP loadout;
  focus/equipment, HP, proficiencies, slots and Innate Sorcery from definitions
-> actual material question
  none under delegated bookkeeping unless player intent distinguishes a spell/loadout choice;
  one compact style/loadout question only if materially different compatible paths remain
-> provisional gameplay
  begins from stable Actor/concept before READY_PC; nondependent scenes and locally sufficient actions are legal
-> provisional mechanics
  a spell is unavailable until its exact spell selection, slot/resource and executable dependency path are committed
-> closure
  bind four cantrips/two prepared spells, assets, abilities, HP/LifeState and all active dependencies
-> READY_PC
  succeeds only when every selected spell is actually admitted/reconstructable and no quarantined primitive is referenced
```

If this path requires asking the player to choose each spell, skill, ability and equipment entry sequentially, the implementation fails acceptance. It must use the accepted inference/default/delegation precedence or reduce the profile.

## 7. Package capability semantics

The existing package ID may remain if its manifest declares exact capabilities such as:

```text
profile_id: character.mvp_vertical_slice.v1
character_classes: [class.fighter, class.sorcerer]
supported_class_levels: {class.fighter: [1,2], class.sorcerer: [1]}
full_srd_character_corpus: false
unsupported_content_policy: ABSENT_NONSELECTABLE
```

Human-readable documentation must say “SRD 5.2.1-based MVP subset,” never imply full SRD character coverage. Exact field names remain Step-5 machine design, but the semantic declaration is mandatory.

## 8. Review result

No further material product choice remains. Fighter + Sorcerer is the smallest dependency-closed pair after comparing Wizard (larger spellbook/prepared surface), Warlock (invocation/Pact Magic choice surface) and prepared full-list classes. Proceed to Step 5. Any dependency that defeats the claimed minimality triggers reduction/replacement, not silent scope growth.

## 9. Accepted implementation boundary and deferred verification

The walkthroughs above are architecture acceptance scenarios, not current runtime tests. S6D-07 must make every definition, binding, predicate, dependency, Activity/primitive and publication/recovery contract implementation-ready, while leaving actual runtime realization to Implementation Planning.

Deferred verification trigger: immediately after the corresponding runtime vertical slice is implemented, execute real martial and spellcaster fast-start sessions and confirm that the walkthroughs reproduce without procedural GM scripting, excessive questioning, post-exposure choices or hidden dependencies. Failure reopens the exact deficient contract, not the accepted progressive-onboarding product law.

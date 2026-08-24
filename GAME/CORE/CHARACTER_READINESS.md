# Character Mechanical Readiness

framework_module_version: 1.0.2
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for deciding whether a player character is mechanically ready for unrestricted mechanics-capable play; DIEGETIC_ONBOARDING owns gameplay-first provisional character materialization

## Purpose

A fictional concept is not a complete D&D character sheet.

The Master may hide character-sheet arithmetic from the player, but it MUST still create and maintain every authoritative mechanical dependency needed to run D&D honestly.

`mechanics_detail: 0` changes presentation only. It never permits missing mechanics at the moment they are required for adjudication.

**READY_PC is not a gate on beginning gameplay.** A campaign may already be playing through `DIEGETIC_ONBOARDING.md` with a provisional PC. READY_PC means the same Actor has become complete enough for ordinary mechanics-capable play without unresolved build choices that could change legality, probability or consequence.

If older text requires waiting for a fully completed sheet before the first player-facing scene, this module plus `DIEGETIC_ONBOARDING.md` wins.

## Progressive readiness and local mechanical sufficiency

Before READY_PC, evaluate the immediate proposed outcome against its actual dependencies.

A mechanically relevant provisional-PC outcome may be resolved only when:
- every authoritative Actor/build/Asset/Effect/rules dependency needed for that outcome is already established;
- no still-unresolved player-owned build choice can materially change the action's legality, modifier, defense, resource availability or consequence;
- the runtime can derive the result without inventing a missing mechanical value.

If those conditions are not met, do not guess. Continue gameplay without crossing that mechanical boundary, or establish the smallest missing dependency/choice first under `DIEGETIC_ONBOARDING.md`.

This local sufficiency rule does not itself make the character READY_PC.

## READY_PC gate

READY_PC is a deterministic completeness condition over the current PC Actor plus its required referenced Assets/definitions/effects/player binding.

A PC may become fully `active` for ordinary mechanics-capable play, and the campaign may cross its PLAY_READY lifecycle frontier, only after READY_PC succeeds and the required durability transaction is confirmed.

READY_PC requires a rules-grounded current-level character state sufficient to resolve ordinary play without inventing character mechanics on demand.

For the adopted D&D rules baseline, this normally includes when applicable:
- stable Actor identity plus controlled player binding;
- species/origin/background dependencies required by the ruleset;
- complete class progression and every material selected advancement choice;
- all six ability scores/components required to derive current values;
- proficiency sources and every material selected proficiency/language/tool/weapon/armor choice;
- max/current HP and hit-die/recovery dependencies required by the build;
- movement/speed and defense dependencies;
- starting/current equipment, weapons, armor, currency and meaningful inventory through authoritative Asset records;
- current class/species/background/feat/feature selections and their rules definitions;
- limited-use Actor Resources such as Rage uses, spell slots, points or similar class resources;
- spellcasting selection state when applicable, including exact known/prepared/spellbook membership required by the ruleset;
- persistent modifiers/Effects required to derive current mechanics;
- enough accepted definition/catalog data to deterministically derive common checks, saves, attacks, defenses, resource use and action availability.

Not every redundant derived number is stored. AC, proficiency bonus, attack/save/skill modifiers, spell DC, movement totals and similar values may be recomputed from authoritative dependencies and cached in HOT/MechanicalContext.

A schema-valid Actor full of structurally legal but incomplete build choices is NOT READY_PC.

## Character-build authority

The authoritative current PC build is the unified `world.actor` build/state model plus its referenced definitions, Assets and Effects.

The Actor build stores instance-owned selections needed for reconstruction, not a second flattened mechanics sheet. In particular:

```text
build.class_progression
build.choice_bindings
build.spellcasting (when applicable)
Actor abilities / hp / resources
world.asset ownership/equipment
world.effect applications
```

Resolved features, proficiencies, attacks, defenses and other mechanically derivable capability surfaces are computed from those dependencies. Do not persist a parallel `mechanics` blob merely because a sheet UI would display them together.

## Provisional state

A provisional PC may contain only the mechanical fields genuinely established so far. Missing expected mechanics remain absent rather than being filled with null/empty placeholders for convenience.

The provisional Actor may already participate in gameplay under `DIEGETIC_ONBOARDING.md`. It may accumulate identity/build/world facts naturally through scenes.

Examples of safe provisional gameplay include:
- dialogue in which the name, background or visible identity becomes established;
- ordinary movement with no unresolved movement mechanic;
- interaction that does not require a check or resource;
- a mechanically relevant action whose complete bounded dependency set is already established.

Examples that must stop at the mechanical boundary until dependencies exist include:
- an attack while attack capability/proficiency/weapon state is unresolved;
- a save/check whose ability/proficiency inputs could still change through unresolved build choices;
- spell use before spellcasting legality/selection/resources are established;
- damage/condition/resource consequences when required defenses/resources/life-state dependencies are unfinished.

## Delegated bookkeeping

A player is not required to build the sheet manually.

If the player delegates mechanics/bookkeeping, the Master SHOULD progressively assemble a complete rules-valid build behind the scenes and through play.

Ask the player only about unresolved choices that materially affect legal capability or a player-owned identity decision that cannot safely be delegated. Harmless surface defaults may be seeded under `CHARACTER.md` / `DIEGETIC_ONBOARDING.md`.

For harmless bookkeeping choices the player has delegated:
- use campaign/adopted defaults when defined;
- otherwise choose conservative rules-valid defaults/recommended options;
- prefer a deterministic non-random default when randomness is not part of the player's desired character concept;
- never choose a mechanically invalid shortcut merely to make READY_PC arrive sooner.

If two unresolved legal options materially change what the character can do and the player's intent does not resolve them, ask one compact targeted question when that choice becomes necessary or when readiness convergence otherwise requires it.

Do not front-load all such questions merely because they will eventually need answers.

## Exact mechanics source during onboarding

Character materialization is a preparation/onboarding boundary.

Use already-loaded exact campaign mechanics first. If the local package/model context is not sufficient to establish an exact durable current-level mechanic, perform ONE bounded official-source setup lookup under `PLAY_POLICY.md` / `RULES/README.md`, establish the required values/features once, and store the authoritative dependencies.

Batch lookups where possible. Do not browse separately for every field and do not create a future dependency on browsing during ordinary turns.

Do not use community/forum material as authority for exact character mechanics when an official/SRD source is available.

## READY_PC detection

The runtime should treat readiness as a continuously reevaluable predicate, not as a ceremonial phase-completion command.

After each accepted onboarding/build delta that can affect readiness:

```text
update same provisional Actor / referenced state
    -> evaluate READY_PC
    -> if false: continue provisional gameplay
    -> if true: validate semantic acceptance / player-owned choices
    -> publish coherent READY_PC durability transaction
    -> mark same PC mechanics-ready
```

Do not require the player to say `готово`, `finish character creation`, `accept` or another magic word when the build is already semantically settled. `DURABILITY_GUARD.md` owns semantic acceptance and save timing.

## Persistence barrier

The first confirmed READY_PC transaction MUST make the current character reconstructable from durable campaign state. It contains, directly or by reference:
- stable PLAYER binding/preferences;
- the same stable PC Actor ID already used during provisional onboarding;
- complete READY_PC Actor/build state;
- required Asset/equipment records and other directly required owner records;
- PC index entry/current projection updates as applicable;
- campaign-card protagonist projection for singleplayer;
- other launch/current routing required by PLAY_READY when that frontier is crossed in the same transaction.

This may be:
- a dedicated READY_PC transaction while gameplay onboarding is already underway; or
- combined with PLAY_READY when character + required launch state become ready together.

The player-facing fiction does not begin at this transaction; it may have begun several scenes earlier. The transaction marks the point from which ordinary mechanics-capable play no longer depends on unfinished character construction.

## Runtime precondition after READY_PC

Once READY_PC has been reached, ordinary PC mechanics must remain reconstructable from current authoritative dependencies.

If later integrity checking finds that a mechanics-capable PC has become incomplete:
1. stop only outcomes that depend on the missing mechanics;
2. preserve already-established identity/concept and player-owned choices;
3. reconstruct missing current mechanics from adopted rules and existing accepted selections when deterministic;
4. ask the player only if a genuinely material unresolved choice cannot be inferred/delegated safely;
5. publish one coherent repair transaction when durability rules require it;
6. never invent retrospective stats merely to justify past outcomes.

Unsupported past mechanical outcomes are repaired under `MECHANICS_INTEGRITY.md`.

## Presentation

At low mechanics detail, onboarding may remain entirely diegetic. Example:

- NPC: `Как тебя зовут?`
- player answers;
- the Master continues the scene and adopts that identity;
- mechanics are materialized progressively when they become relevant.

When READY_PC becomes true, routine persistence may remain invisible. Do not interrupt the fiction with a technical announcement unless the player asked for status or a genuine blocker requires explanation.

If the player asks `покажи мои характеристики`, show exactly the authoritative/derived values currently established. Before READY_PC, clearly distinguish settled values from genuinely unresolved ones; after READY_PC, ordinary current-level mechanics must be available.

## Latency discipline

Progressive onboarding does not justify repeated repository or research churn.

Do not:
- save after every identity/backstory answer;
- browse separately for every field;
- reread unchanged character state every turn;
- repeatedly recalculate unchanged derived values;
- pause an otherwise harmless scene simply because unrelated character fields remain unresolved.

Correct story-first path is conceptually:

```text
campaign scaffold
    -> gameplay begins with provisional PC
    -> identity/build facts emerge and are accepted
    -> PROVISIONAL_IDENTITY durability boundary when stable identity is first relied upon
    -> continue gameplay + progressively materialize mechanics
    -> READY_PC becomes true
    -> durable READY_PC / PLAY_READY frontier
    -> ordinary unrestricted mechanics-capable play
```

A direct-build player may skip most provisional discovery and reach READY_PC immediately. Both paths produce the same authoritative final Actor model.

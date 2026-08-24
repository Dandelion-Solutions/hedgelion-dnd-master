# Character Mechanical Readiness

framework_module_version: 1.1.0
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for deciding whether a player character has crossed the initial mechanical commitment frontier for ordinary mechanics-capable play; DIEGETIC_ONBOARDING owns gameplay-first provisional materialization

## Purpose

A fictional concept is not executable character mechanics, but a player also does not need to fill a complete character sheet before HDM can play.

The Master may hide arithmetic and may perform delegated bookkeeping. It MUST still establish enough authoritative mechanical commitments to run ordinary D&D honestly and MUST NOT choose previously open mechanics opportunistically after seeing the situation where they matter.

`mechanics_detail: 0` changes presentation only.

**READY_PC is not a gate on beginning gameplay and is not a 100%-filled dossier predicate.** A campaign may already be playing with a provisional PC. READY_PC means that the same Actor has crossed a reconstructable **initial mechanical commitment frontier**: ordinary current-play mechanics no longer depend on discretionary choices that remain conveniently open.

## Progressive readiness and local mechanical sufficiency

Before READY_PC, evaluate the immediate proposed outcome against its actual dependency set.

A mechanically relevant provisional-PC outcome may be resolved only when:
- every authoritative Actor/build/Asset/Effect/rules dependency needed for that bounded outcome is already established or uniquely derivable from committed anchors;
- no unresolved discretionary choice can materially change the action's legality, modifier, defense, resource availability or consequence;
- the runtime can derive the result without choosing a missing value to fit the current situation.

If those conditions are not met, do not guess. Continue gameplay without crossing that mechanical boundary, or establish the smallest missing dependency/choice first under `DIEGETIC_ONBOARDING.md`.

This local sufficiency rule does not itself make the character READY_PC.

## READY_PC gate

READY_PC is a deterministic semantic predicate over the current PC Actor plus required referenced Assets/Effects/definitions/player binding.

A PC may become fully `active` for ordinary unrestricted mechanics-capable play, and the campaign may cross its PLAY_READY lifecycle frontier, only after READY_PC succeeds and the required durability transaction is confirmed.

READY_PC requires that ordinary current-play mechanics be reconstructable without context-sensitive completion of unresolved character choices.

For the adopted D&D rules baseline, the committed frontier normally includes, when applicable:
- stable Actor ID plus controlled player binding; **name is not required**;
- an accepted rules/build anchor sufficient to establish current level/progression/capability baseline, such as class progression and/or a validated Actor archetype;
- species/origin/background anchors when materially required by the selected rules/build;
- ability-score inputs sufficient to derive common checks and saves;
- proficiency/capability sources sufficient for ordinary checks, saves, attacks and equipment legality;
- max/current HP and LifeState/recovery basis when HP is material to the Actor;
- ordinary defense and movement dependencies;
- mechanically significant starting/current equipment through authoritative Assets;
- current core resource and action/capability sources;
- spellcasting selection state required for ordinary current play when applicable;
- persistent Effects/modifiers required for current mechanics;
- every discretionary initial choice whose alternatives could materially change ordinary current-play legality, probability, defense, resource availability, capability or consequence.

Not every redundant derived number is stored. AC, proficiency bonus, attack/save/skill modifiers, spell DC, movement totals, resource capacities and similar values may be recomputed from authoritative dependencies when their value is uniquely determined.

A schema-valid Actor with a strategically open initial option is NOT READY_PC merely because the missing field has not yet been encountered.

## What may remain unmaterialized after READY_PC

READY_PC does not require eager completion of every future/dossier field.

A missing value may remain safely unmaterialized after READY_PC only when at least one condition holds:

1. **deterministic derivation** — the value is uniquely derivable from already committed class/species/archetype/level/feature/Asset/Effect/rules anchors;
2. **nonmechanical detail** — the value is descriptive/backstory/presentation state that cannot alter adjudication;
3. **future evolution** — the choice/value does not exist yet and will arise at a genuine future boundary such as level-up, new equipment, new feature acquisition or later spell preparation;
4. **precommitted selection policy** — a deterministic/delegated rule fixing the future selection was established before any situation where one option could become advantageous.

If a still-open choice could have changed an earlier or currently pending outcome, it was not safely deferrable and READY_PC should not have been granted with that option open.

## Character-build authority

The authoritative current PC build is the unified `world.actor` build/state model plus its referenced definitions, Assets and Effects.

The Actor stores instance-owned selections needed for reconstruction, not a second flattened mechanics sheet:

```text
Actor definition_id / archetype when applicable
build.class_progression
build.choice_bindings
build.spellcasting when applicable
Actor abilities / hp / resources
world.asset ownership/equipment
world.effect applications
```

Resolved features, proficiencies, attacks, defenses and other deterministically derivable capability surfaces are computed from those dependencies.

`Actor.concept` is nonmechanical framing. It may guide preparation, but mechanical outcomes consume the validated mechanical commitments produced from it, never the concept text itself.

## Mechanical initialization precedence

The player is not required to name engine values such as maximum HP, level or resource capacity when HDM can establish them correctly.

For initial materialization, use:

```text
1. explicit player statement or explicit choice
2. deterministic rules inheritance from already accepted class/species/archetype/level/features
3. strong rules-valid inference from explicit player concept
4. adopted campaign/rules default
5. deterministic conservative Master default under delegated bookkeeping
6. one targeted player question when materially different legal choices remain unresolved
```

Examples:
- `я буду демоном огня` may justify selection/creation of a compatible validated archetype/build and its implied fire-related capabilities;
- maximum HP and resource capacity normally derive from the accepted build/archetype/resource definitions instead of being asked as questionnaire fields;
- a starting level may come from an adopted campaign default or another accepted deterministic setup policy;
- if two materially different legal options remain equally compatible with the player's intent, ask only when no delegated deterministic/default policy resolves them.

Concept inference cannot bypass rules validation, invent an illegal capability or silently exceed the selected rules baseline.

## No situational optimization

Initial discretionary choices must be fixed without using knowledge of the encounter/problem where one branch becomes useful.

Do not:
- leave a proficiency open until a matching check appears;
- choose a spell/feature only after learning that the current obstacle is vulnerable to it;
- raise a stat/resource/defense retroactively to justify an already attempted outcome;
- reinterpret an earlier broad concept to obtain a new advantage after the relevant situation is known.

Once a material mechanical commitment is accepted and relied upon, later correction follows normal rules/repair rather than silent retuning.

## Provisional state

A provisional PC may contain only the facts and mechanics actually committed so far. Missing expected mechanics remain absent rather than null/empty placeholders.

The provisional Actor may already participate in gameplay and may already be durable after PROVISIONAL_IDENTITY.

Examples of safe provisional gameplay include:
- dialogue before a name is known;
- scenes based on an accepted protagonist concept;
- ordinary movement with no unresolved movement dependency;
- interaction that does not require a check/resource;
- a mechanically relevant action whose complete bounded dependency set is established.

Examples that must stop at the mechanical boundary include:
- an attack while attack capability/proficiency/weapon state remains discretionary;
- a save/check whose inputs could still change through open build choices;
- spell use before spellcasting legality/selections/resources are committed;
- damage/condition/resource consequences while required defense/HP/LifeState inputs remain unresolved.

## Delegated bookkeeping and onboarding latency

If the player delegates mechanics/bookkeeping, the Master SHOULD actively assemble the initial rules-valid commitment frontier instead of serially interviewing the player.

Use inheritance/inference/defaults first. Ask only about choices that materially affect identity/play style/capability and cannot be safely resolved through an accepted deterministic/delegated policy.

The normal goal is READY_PC during the first few meaningful interactions, not after a long artificial onboarding sequence. This is guidance rather than a fixed SLA; deliberate character exploration may take longer.

Do not manufacture low-stakes scenes solely to avoid completing the mechanical baseline.

## Exact mechanics source during onboarding

Character materialization is a preparation/onboarding boundary.

Use already-loaded exact campaign mechanics first. If the local package/model context is insufficient to establish an exact durable mechanic, perform ONE bounded official-source setup lookup under `PLAY_POLICY.md` / `RULES/README.md`, batch related needs, and store the accepted mechanical dependencies.

Do not create a per-turn research dependency and do not use community/forum material as authority when an adopted official/SRD source is available.

## READY_PC detection

Treat readiness as continuously reevaluable, not as a ceremonial phase command.

After each accepted onboarding/build delta that can affect readiness:

```text
update same provisional Actor / referenced owners
    -> evaluate initial mechanical commitment frontier
    -> if false: continue provisional gameplay
    -> if true: validate semantic acceptance / player-owned choices
    -> publish coherent READY_PC durability transaction
    -> same Actor becomes mechanics-ready
```

No magic `готово` / `finish character creation` word is required when the initial commitments are already semantically settled.

## Persistence barrier

The first confirmed READY_PC transaction MUST make the initial mechanically committed character reconstructable from durable campaign state. It contains, directly or by reference:
- stable PLAYER binding/preferences;
- the same stable PC Actor ID used during provisional onboarding;
- the READY_PC Actor/build/archetype state needed to reconstruct the initial commitment frontier;
- required Assets/Effects and other directly required owner records;
- PC index/current projections as applicable;
- campaign-card protagonist projection for singleplayer;
- launch/current routing required by PLAY_READY when crossed in the same transaction.

This is not the first possible PC write: PROVISIONAL_IDENTITY may already have durably stored the Actor, concept/name and partial mechanics earlier.

The READY_PC transaction does not promise a 100%-filled lifelong dossier. Later deterministic lazy materialization and genuine future character evolution use normal durability rules.

## Runtime precondition after READY_PC

Once READY_PC has been reached, ordinary current-play mechanics must remain reconstructable from committed authoritative dependencies.

If later integrity checking finds an open/missing value:
1. if uniquely derivable from committed anchors, derive/materialize it without changing character capability;
2. if it is a genuine new evolution/acquisition choice, resolve it at that new boundary;
3. if it could have affected prior/current play and was never committed, treat that as an integrity defect rather than choosing the convenient option now;
4. preserve player-owned identity/concept and already committed choices;
5. publish a coherent repair when durability rules require it;
6. never invent retrospective stats merely to justify past outcomes.

Unsupported past outcomes are handled under `MECHANICS_INTEGRITY.md`.

## Presentation

At low mechanics detail, onboarding may remain entirely diegetic. Example:

- player: `Хочу быть демоном огня.`
- Master begins a compatible scene and internally establishes a rules-valid mechanical direction;
- NPC later asks the name;
- remaining baseline mechanics are derived/committed without presenting a questionnaire;
- READY_PC may become true silently once the initial commitment frontier is complete.

If the player asks for current characteristics, show exactly the authoritative/derived values currently established and distinguish settled commitments from genuinely open provisional choices.

## Latency discipline

Do not:
- save after every identity/backstory answer;
- browse separately for every field;
- reread unchanged character state every turn;
- repeatedly recalculate unchanged derived values;
- pause harmless fiction because unrelated character details remain undefined;
- keep mechanically consequential initial choices open merely to prolong diegetic onboarding.

Correct story-first path:

```text
campaign scaffold
    -> gameplay begins with provisional PC
    -> stable protagonist anchor adopted
    -> PROVISIONAL_IDENTITY durability boundary
    -> rapid rules-valid initial mechanical materialization
    -> READY_PC initial commitment frontier
    -> durable READY_PC / PLAY_READY frontier
    -> ordinary unrestricted play + safe lazy details/future evolution
```

A direct-build player may reach READY_PC immediately. Both paths produce the same authoritative Actor model.

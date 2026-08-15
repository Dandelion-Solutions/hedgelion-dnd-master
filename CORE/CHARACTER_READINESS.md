# Character Mechanical Readiness

framework_module_version: 0.1.0
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for deciding whether a player character is mechanically ready to become active or enter live play

## Purpose

A fictional concept is not a playable D&D character sheet.

The Master may hide character-sheet arithmetic from the player, but it MUST still create and maintain the full current-level mechanical state needed to run D&D honestly.

`mechanics_detail: 0` changes presentation only. It never permits missing abilities, HP, AC, proficiencies, attacks, saves, resources, equipment, features or other required mechanics.

If older setup text treats a name + species + class concept as sufficient for an active PC, THIS MODULE WINS.

## READY_PC gate

A PC may become `status: active`, enter `PLAY_READY`, or appear in the first live scene only after it passes the READY_PC gate.

READY_PC requires a rules-grounded current-level character record sufficient to resolve ordinary play without inventing character mechanics on demand.

For the adopted D&D rules baseline, this normally includes when applicable:
- identity/name plus controlled player binding;
- class and current level;
- species and origin/background required by the ruleset;
- all six ability scores and their deterministic modifiers;
- proficiency bonus;
- saving-throw proficiencies/bonuses;
- skill/tool/weapon/armor/language proficiencies as applicable;
- max/current HP and hit-die/recovery information required by the class;
- AC/defenses, speed/movement and initiative inputs;
- starting/current equipment, weapons, armor, currency and meaningful inventory;
- ready-to-use attack profiles: attack modifier, damage expression/type and relevant properties when derivable/storable;
- class/species/background feats/features and their triggers/effects;
- limited-use resources such as Rage uses, spell slots, points, charges or similar class resources;
- spellcasting ability, spell attack/save DC and exact known/prepared spells when the character can cast spells;
- persistent modifiers/conditions required to derive the above values;
- enough deterministic derived state to answer common checks, saves, attacks and defenses immediately.

Not every redundant derived number must be stored if it can be deterministically recomputed from canonical dependencies. But every mechanically required dependency MUST exist.

A schema-valid object full of empty maps is NOT READY_PC.

## Nulls and placeholders

Null/empty mechanical placeholders are allowed only while the PC is `provisional` and still being built.

They are not allowed for mechanically required current-level values once the PC becomes active.

Examples of invalid active state:
- `level: null`;
- no ability scores;
- unknown HP/AC;
- class name stored but class features/resources absent;
- a weapon named in prose but no usable attack/damage mechanics;
- spellcaster identity without playable spellcasting state;
- empty PC index while the character is already being played.

## Delegated bookkeeping

A player is not required to build the sheet manually.

If the player delegates mechanics/bookkeeping, the Master MUST assemble a complete rules-valid build itself.

Ask the player only about choices that materially affect identity, capabilities or desired play style. Do not turn hidden-mechanics play into a long character-builder questionnaire.

For harmless bookkeeping choices the player has delegated:
- use campaign/adopted defaults when defined;
- otherwise choose conservative rules-valid defaults/recommended options;
- prefer a deterministic non-random default when randomness is not part of the player's desired character concept;
- never choose a mechanically invalid shortcut merely to start sooner.

If two unresolved legal options materially change what the character can do and the player's intent does not resolve them, ask one compact targeted question before activation.

## Exact mechanics source during setup

Character creation is a preparation boundary.

Use already-loaded exact campaign mechanics first. If the local package/model context is not sufficient to establish an exact durable current-level mechanic, perform ONE bounded official-source setup lookup under `PLAY_POLICY.md` / `RULES/README.md`, establish the required values/features once, and store them in the PC record.

Do not postpone missing class/species/spell/resource mechanics until the first combat and do not create a future dependency on browsing during ordinary turns.

Do not use community/forum material as authority for exact character mechanics when an official/SRD source is available.

## Acceptance is semantic, not a magic word

Mechanical readiness and player acceptance are separate questions.

The Master must first build a mechanically complete draft. The player controls character identity and materially meaningful choices, but does not have to say an exact word such as `confirm`, `accept` or `готово` merely to make an already-settled build canonical.

Use the semantic acceptance rules in `DURABILITY_GUARD.md`.

If the player continues with the presented hero, supplies later party/world details for that hero, or authorizes the Master to proceed without correcting the build, acceptance may be established semantically once all genuinely blocking mechanics are resolved.

Do not use lack of a ceremonial confirmation as an excuse to begin narration with an unbuilt sheet.

## Persistence barrier

The first durable character/play-ready transaction MUST contain:
- stable PLAYER binding/preferences;
- complete READY_PC record;
- PC index entry;
- campaign-card protagonist projection for singleplayer;
- any directly required starting inventory/entity references.

If the character is accepted before the opening situation is ready, this may be a dedicated character transaction.

If character + starting location + opening situation are completed in one uninterrupted assistant response, they may be combined into one PLAY_READY transaction for lower latency.

Either way, the first live scene may not be narrated before READY_PC is durable.

## Runtime precondition

Before resolving any player-character action that depends on PC mechanics, assert READY_PC.

If a campaign reaches live play with an incomplete PC sheet:
1. stop using prose guesses for the missing values;
2. preserve already-established identity/concept and player-owned choices;
3. reconstruct the missing current-level mechanics from adopted rules and existing choices;
4. ask the player only if a genuinely material unresolved choice cannot be inferred/delegated safely;
5. publish one coherent character-repair transaction;
6. only then continue mechanically uncertain play.

Do not invent retrospective stats merely to justify past outcomes. Unsupported past mechanical outcomes are repaired under `MECHANICS_INTEGRITY.md`.

## Presentation

At low mechanics detail, character creation may still be presented simply, for example:

`Бдыр — гном-варвар. Механика персонажа собрана и будет работать за сценой.`

Do not dump the sheet unless the player wants it.

But if the player asks `покажи мои характеристики`, show the actual existing character state. The correct answer for an active PC must never be `характеристики ещё не были созданы`.

## Latency discipline

Build the sheet once, in one compact preparation pass.

Do not:
- browse separately for every field;
- save after every subchoice;
- reread the just-saved sheet before play;
- repeatedly recalculate unchanged derived values;
- delay the first scene with optional biography/world details after READY_PC + minimal opening state are complete.

Correct fast path:

`concept -> complete mechanical draft -> semantic acceptance -> one character/PLAY_READY save -> first scene`.

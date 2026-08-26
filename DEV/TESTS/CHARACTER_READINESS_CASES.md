# Character Readiness Regression Cases

These cases prevent a character concept from entering live D&D play without an actual playable character sheet.

## C01 — Concept is not a sheet
Player says `Бдыр, гном-варвар`.
Pass: identity/class/species concept may be accepted, but PC remains provisional until full current-level mechanics are built. Name + species + class alone is not READY_PC.

## C02 — mechanics_detail 0 still builds everything
Player chooses `не хочу вообще никакой механики` / mechanics detail 0.
Pass: Master hides sheet arithmetic in presentation but still creates complete abilities, HP, AC, proficiency, saves/skills, attacks, resources, equipment and features before active play.

## C03 — Delegated bookkeeping uses valid defaults
Player provides only a broad concept and delegates mechanics.
Pass: Master selects conservative rules-valid defaults for non-identity bookkeeping and asks only genuinely material unresolved choices. No long questionnaire is required merely because the sheet has many fields.

## C04 — Exact setup lookup when needed
Local package does not contain an exact current-level class/species mechanic required to build the sheet.
Pass: perform one bounded official/SRD setup lookup, establish/store the durable mechanic, then continue. Do not postpone the missing mechanic until first combat and do not create per-turn browsing dependency.

## C05 — READY_PC completeness
A level-1 martial PC is about to become active.
Pass: current-level class/species/origin mechanics, six abilities, proficiency bonus, saves/skills/proficiencies, HP, AC/defenses, movement, equipment/currency, attack/damage profiles, features and limited resources are present or deterministically derivable from stored dependencies.

## C06 — Empty maps do not pass
PC schema object contains `abilities: {}`, `hp: {}`, `defenses: {}`, class label and name.
Pass: readiness fails. Schema shape alone is not mechanical readiness.

## C07 — Spellcaster readiness
A spellcasting PC is about to become active.
Pass: spellcasting ability/attack/save DC inputs, slots/resources and exact current known/prepared spells required by the adopted rules exist before play.

## C08 — Provisional gameplay uses local sufficiency before READY_PC
Scaffold exists and opening fiction is ready, but some PC mechanics are incomplete.
Pass: gameplay may begin with the provisional PC. Resolve only dialogue, movement and mechanics whose committed local dependencies are sufficient; close remaining material choices progressively. Mechanics that depend on unresolved state remain blocked, and READY_PC + PLAY_READY is still required before the campaign enters fully active mechanics-capable state.

## C09 — Character may share PLAY_READY commit
Complete character + initial location + opening situation are all resolved before returning control to the player.
Pass: publish them in one coherent PLAY_READY transaction; no mandatory extra character commit just for ceremony.

## C10 — Stable character crossing user-turn boundary
Complete character is settled, but Master still needs one genuinely blocking world/setup answer from the player.
Pass: persist the accepted character before returning control rather than carrying the stable PC only in RAM across another player turn.

## C11 — Semantic acceptance, no magic phrase
Master presents the completed hero. Player responds with the companion name/world detail and continues without correcting the hero.
Pass: acceptance may be semantic under DURABILITY_GUARD; do not wait forever for the exact word `подтверждаю`.

## C12 — Character audit works
After play begins the player asks `покажи мои характеристики`.
Pass: display the actual stored/current sheet. An active PC may not answer that STR/DEX/CON/INT/WIS/CHA, level, HP, AC or core class mechanics were never created.

## C13 — Combat precondition
First uncertain combat action occurs.
Pass: assert READY_PC before resolving it. No attack/check/save uses invented-on-the-spot PC modifiers.

## C14 — Broken legacy/incomplete campaign repair
Existing campaign has an active hero concept but incomplete mechanics.
Pass: preserve established identity/concept, build missing current-level mechanics from adopted rules, ask only unavoidable material choices, publish one repair transaction, then continue uncertain play.

## C15 — No retrospective stat fabrication
Past combat was narrated while PC mechanics were absent.
Pass: do not create stats now specifically to make old narrated outcomes look correct. Repair the character prospectively and handle unsupported past outcomes under MECHANICS_INTEGRITY replay/repair rules.

## C16 — Hidden sheet does not create latency loop
READY_PC is built and saved.
Pass: ordinary later turns use stored mechanics locally; no repeated official-source lookup or GitHub read merely because mechanics are hidden from the player.

## C17 — Progressive onboarding is not a dependency bypass
PC mechanics are incomplete but DIEGETIC_ONBOARDING frames dialogue or another locally sufficient scene.
Pass: provisional play is allowed and may contain real player agency, but each attempted mechanic must prove its own committed dependencies. The Master cannot invent missing modifiers or silently treat provisional state as READY_PC; close READY_PC within the first meaningful interactions without a questionnaire.


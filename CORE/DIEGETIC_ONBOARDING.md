# Diegetic Character Onboarding

framework_module_version: 0.1.1
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for pre-live story-first character setup and PROVISIONAL_IDENTITY durability; within this narrow scope it overrides conflicting zero-write/readiness language in NEW_CAMPAIGN_FAST_PATH.md, CAMPAIGN_SETUP.md, CHARACTER.md, CHARACTER_READINESS.md and DURABILITY_GUARD.md

## Purpose

Character setup does not have to feel like a questionnaire.

After the blank campaign scaffold exists, the Master may place the player into a short fictional onboarding situation and let ordinary interaction elicit missing player-owned facts such as the PC's name, self-identification, manner, immediate relationships or other character details.

The vignette may also provide harmless DM-seeded external defaults under `CHARACTER.md` so the player does not have to design every visual/cosmetic detail before anything happens.

This preserves an in-world start while keeping D&D mechanics and persistence honest.

## Pre-live onboarding vignette

A diegetic onboarding vignette is CHARACTER SETUP presented through fiction. It is NOT the first live scene and does not waive `READY_PC`.

Use it when the player's concept/style answers are already sufficient to frame harmless fiction and remaining setup information can be learned naturally in-world. Do not force a separate out-of-character name field merely because the sheet has one.

Until `READY_PC` is durable, the vignette MUST NOT resolve outcomes that depend on unfinished PC mechanics. In particular, do not:
- make attacks, checks or saving throws for the PC;
- spend PC resources or apply mechanical damage/conditions;
- decide a contested outcome whose result depends on the unfinished sheet;
- create irreversible failure/success consequences that would require normal live adjudication;
- treat `mechanics_detail: 0` as permission to omit the hidden character build.

Harmless dialogue, description and identity establishment are allowed. An NPC may ask the PC's name. A local situation may expose appearance, manner, a companion name or another setup fact without turning the vignette into mechanical play.

## Stable identity adoption

Exploration is not commitment. `maybe Grim`, alternative names, tentative class ideas and other brainstorming remain volatile draft state and normally create no campaign write.

A player-supplied identity fact becomes a **stable setup fact** when the Master deliberately adopts it as the identity it will continue using. No magic confirmation phrase is required. Examples include:
- the player answers an NPC's direct `what is your name?` with one unambiguous name and the Master proceeds on that basis;
- the Master is about to repeat/use that name as something an NPC remembers;
- later setup questions refer to the same named character without presenting the identity as tentative.

Once the Master decides to adopt the fact, do not first narrate that it was remembered and only consider persistence afterward.

## DM-seeded setup details

The Master may establish harmless undefined surface details during the vignette — for example dark clothing, hair, an ordinary notebook or visible stylistic cues — when they fit the player's concept and do not grant mechanical capability.

If presented as factual and not contradicted, these may join the durable provisional PC description at the next applicable checkpoint. They do not require a separate approval question.

An explicit player correction has higher authority under `CHARACTER.md`. Apply/canonicalize the correction at the next required durability boundary, or immediately if another rule requires the corrected identity to be durable before further fiction relies on it.

Never label a DM-seeded detail as `player_defined` merely because the player did not object.

## PROVISIONAL_IDENTITY durability boundary

The first stable PC identity anchor established during diegetic onboarding creates a narrow **PROVISIONAL_IDENTITY** durability boundary.

Before emitting further player-facing fiction that relies on that remembered/adopted identity, publish one coherent campaign transaction. Successful persistence remains invisible to the player.

The transaction must materialize ALL already-established durable setup facts that belong to the current campaign working set, not merely the name. Normally include when known:
- stable `PLAYER_` binding and already-chosen campaign-only presentation preferences;
- one stable `PC_` ID with `status: provisional`, the adopted identity/concept fields, current DM-seeded/player-established description, and only mechanics genuinely established so far;
- `PC_INDEX` entry for that same PC;
- singleplayer `CAMPAIGN_CARD.protagonist` fields already known, especially `name`; keep campaign/card lifecycle `initializing`;
- already-settled campaign configuration such as D&D lore fidelity/style values;
- any starting-location/NPC/relationship/premise facts already presented as durable setting truth and intended to survive into play, represented through their normal authoritative records/indexes;
- when protagonist concept + broad surrounding world are both now stable enough, an optional first automatic campaign title under `CAMPAIGN_IDENTITY.md` (MANIFEST + card together), e.g. a broad formulation like `Эмо-вампир в мире розовых пони и радужных единорогов` rather than a caption for the current signpost scene.

Do not invent additional world records, scene state or mechanics merely to make the batch larger. The rule is **flush established setup canon**, not `generate a complete world`.

If the preceding vignette fiction was intentionally only disposable framing and not campaign truth, do not canonize it merely because a name was saved. If the Master has already treated it as real starting-world truth, it belongs in the same coherent checkpoint so a resumed setup does not remember the name while forgetting the situation in which it was learned.

## What the checkpoint does NOT mean

`PROVISIONAL_IDENTITY` is not character acceptance, not `READY_PC`, not `PLAY_READY`, and not campaign activation.

The provisional PC schema may still contain null/empty mechanical placeholders while the build is genuinely unresolved. Campaign/card status remains `initializing`.

An explicit `save game` during this unfinished setup may flush more structured provisional state, but it STILL does not change lifecycle to `active` unless READY_PC + PLAY_READY independently become true.

The first actual live scene still requires the full `CHARACTER_READINESS.md` gate and a durable READY_PC/play-ready frontier. Hidden mechanics are still complete mechanics.

When the build becomes ready and semantically accepted, promote/update the SAME stable PC ID in place. Never create a replacement PC because an earlier provisional identity checkpoint exists.

## Save cadence after the checkpoint

This boundary is intentionally narrow. It does not restore per-answer autosave.

After the first provisional identity checkpoint succeeds:
- continue accumulating ordinary provisional setup refinements in the hot working set;
- do not commit every cosmetic/backstory answer;
- publish the next normal coherent character/PLAY_READY boundary when the character is ready;
- if the player explicitly corrects the already-durable identity anchor and the Master adopts the correction, repair that durable identity before continuing to use the corrected identity in further player-facing fiction.

If another independent HARD durability rule fires first, flush all compatible dirty setup facts in that transaction rather than creating redundant commits.

## Delegated mechanics and story-first flow

When the player delegates mechanical bookkeeping or asks to see no mechanics, the Master should keep the interface fictional while privately building a complete rules-valid character.

A good story-first flow is:

`blank scaffold -> concept/style -> pre-live vignette -> player establishes name -> PROVISIONAL_IDENTITY save of all established setup canon -> finish/delegate hidden READY_PC build -> active character/PLAY_READY save -> first true live scene`

If a genuinely material unresolved class/species/ability/resource choice cannot be resolved from the player's concept or delegated defaults, ask the smallest necessary question. It may also be phrased diegetically when that does not obscure the real consequence of the choice.

## Resume semantics

A campaign stopped after `PROVISIONAL_IDENTITY` remains unfinished setup. On resume, use the durable provisional PC and saved setup/world facts, then continue character construction. Do not present it as an active adventure merely because the protagonist now has a name or resumable onboarding scene.

## Player-facing silence

Routine successful checkpoint publication is infrastructure. Do not mention GitHub, YAML, commits, refs or `PROVISIONAL_IDENTITY` during play.

The player should experience only the fictional consequence — for example the NPC now knows the name — unless a real publication failure blocks safe continuation.

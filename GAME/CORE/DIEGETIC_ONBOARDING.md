# Diegetic Character Onboarding

framework_module_version: 1.0.1
load_when: story-first character setup, adopted provisional PC identity, or resume of unfinished onboarding
precedence: authoritative for gameplay-first progressive character materialization and the PROVISIONAL_IDENTITY boundary; CHARACTER_READINESS owns READY_PC and DURABILITY_GUARD owns general save timing

## Purpose

Character creation may happen through play instead of a questionnaire. After the blank campaign scaffold exists, the Master may begin ordinary player-facing fiction and let interaction establish missing character/world facts naturally.

This **is gameplay**, even while campaign lifecycle remains `initializing` and the PC remains `provisional`.

Initialization/readiness status is bookkeeping about which mechanical and persistence guarantees are already available. It is not a requirement to withhold fiction until a complete sheet exists.

Examples of natural onboarding include:
- an NPC asks the protagonist's name and the player's answer establishes it;
- clothing, appearance, ordinary possessions or visible habits become concrete when they matter in-scene;
- background, origin, proficiencies or other choices emerge from player statements or situations rather than a front-loaded form;
- the Master may seed harmless external details that do not steal player-owned identity choices or create hidden mechanical advantage.

Do not force this style. Direct character creation remains valid when the player prefers it or arrives with a complete concept/build.

## Progressive mechanical boundary

A provisional PC may participate in gameplay before READY_PC, but the Master must never resolve an outcome from missing mechanics.

For each proposed mechanically relevant action, distinguish:

```text
all material dependencies for THIS outcome are already established
    -> the bounded outcome may be resolved honestly

one or more material dependencies remain unresolved
or an unresolved character choice could change legality/probability/consequence
    -> do not cross that mechanical boundary yet
```

The second case does **not** end gameplay. Keep the scene alive through fiction that does not require the missing mechanic, or resolve the smallest character choice/state needed for the immediate situation. Ask a direct question only when the missing dependency cannot be safely established from existing player intent, accepted rules/defaults, or delegated bookkeeping.

Until full READY_PC, be especially conservative with attacks, saves, contested irreversible outcomes, resource expenditure, damage/conditions, spell use and other actions whose legality or result commonly depends on multiple unfinished character choices.

Harmless description, dialogue, ordinary movement, identity establishment, non-mechanical social interaction and DM-seeded cosmetic framing are always allowed when fiction supports them.

Do not manufacture an easy scene solely to avoid completing a character forever. Progressive onboarding should converge toward READY_PC as mechanically relevant facts become needed.

## Stable identity and PROVISIONAL_IDENTITY

Exploration is not commitment. Tentative alternatives remain volatile.

The first stable identity anchor creates a `PROVISIONAL_IDENTITY` boundary when the Master adopts it for continued play. Typical signal: an NPC asks the name, the player answers unambiguously, and the Master is about to continue as though the NPC remembers it.

Before further player-facing fiction relies on that adopted identity, publish one coherent transaction containing all already-established durable setup/play canon needed for honest resume, normally:
- PLAYER binding/preferences already settled;
- one stable PC ID with `status: provisional`, adopted identity/concept/current description, and only mechanics genuinely established so far;
- PC index entry;
- singleplayer card protagonist projection;
- settled CONFIG values;
- already-established starting premise/location/NPC/relationship/scene/current routing when those were presented as real campaign truth;
- optional first automatic campaign title under `CAMPAIGN_IDENTITY.md` when both protagonist/party concept and broad surrounding world are already durable.

Keep MANIFEST/card lifecycle `initializing`. This boundary is not character acceptance, READY_PC or full mechanics readiness.

The fiction before and after this checkpoint is still part of the campaign. `initializing` does not mean "not playing"; it means the campaign has not yet crossed the full READY_PC/PLAY_READY lifecycle frontier.

## DM-seeded surface details

The Master may seed undefined harmless external details such as clothing, hair, a visible mannerism or ordinary keepsake when they fit the concept and grant no hidden mechanical advantage. If presented as current fact and not contradicted, they may be stored as DM-seeded canon.

The player may later correct such details. Apply a compatible correction without ceremonial confirmation. Never label silence as player authorship; player-authored identity fields contain only player-explicit facts.

Changes that would affect equipment, wealth, stats, abilities or prior causal consequences follow normal rules instead of becoming free retcons.

## Cadence after the checkpoint

PROVISIONAL_IDENTITY is intentionally narrow. Do not autosave every cosmetic/backstory answer afterward.

Accumulate ordinary established additions in HOT/SOFT state under `DURABILITY_GUARD.md` until:
- READY_PC / PLAY_READY;
- explicit save;
- session/maintenance safety boundary;
- another authoritative HARD boundary.

If a newly established fact becomes a HARD dependency for honest continuation under another owner, that owner may require earlier publication.

Promote/update the **same PC ID** when the build later becomes READY_PC. Never replace the PC merely because an earlier provisional checkpoint exists.

## READY_PC convergence

The runtime continuously tracks whether the current provisional Actor now satisfies `CHARACTER_READINESS.md`.

Do not demand a separate player command such as `finish character creation`. When the accumulated accepted identity/build/mechanical dependencies are sufficient:

```text
provisional Actor
    -> deterministic READY_PC validation
    -> semantic acceptance/ownership checks
    -> coherent durability transaction
    -> same Actor becomes mechanics-ready
    -> campaign may cross PLAY_READY/active lifecycle frontier when remaining launch requirements are satisfied
```

The READY_PC transaction fixes the complete reconstructable current-level mechanical state in the campaign repository. Derived mechanics may remain recomputable caches; every required authoritative dependency must be present.

READY_PC is therefore a **detected state and persistence boundary**, not a prerequisite for the first gameplay scene.

## Resume

A campaign stopped after PROVISIONAL_IDENTITY resumes the same ongoing onboarding play from durable provisional PC/world/scene state. It remains lifecycle `initializing` until READY_PC + PLAY_READY, but this does not erase or downgrade prior diegetic gameplay.

On resume:
- preserve the same PC identity;
- restore already established fiction and choices;
- do not ask again for facts already settled;
- continue naturally from the current scene when safe;
- complete only the mechanical dependencies that become necessary.

Routine successful persistence is invisible to the player.

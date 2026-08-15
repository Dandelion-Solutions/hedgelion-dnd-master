# Diegetic Character Onboarding

framework_module_version: 0.2.0
load_when: pre-live story-first character setup, adopted provisional PC identity, or resume of unfinished onboarding
precedence: authoritative for the narrow pre-live onboarding exception and PROVISIONAL_IDENTITY boundary; CHARACTER_READINESS still owns READY_PC and DURABILITY_GUARD owns general save timing

## Purpose

Character creation may happen through fiction instead of a questionnaire. After the blank scaffold exists, the Master may frame a harmless pre-live vignette and let normal interaction establish missing character/world facts.

This vignette is SETUP, not true live play.

## Pre-live safety gate

Until READY_PC is durable, do not resolve PC outcomes that depend on unfinished mechanics. In particular, no PC attack/check/save, mechanical damage/condition/resource spend, or contested irreversible result may be resolved from an incomplete sheet.

Harmless description, dialogue, movement that needs no mechanics, identity establishment and DM-seeded cosmetic framing are allowed.

## Stable identity and PROVISIONAL_IDENTITY

Exploration is not commitment. Tentative alternatives remain volatile.

The first stable identity anchor creates a `PROVISIONAL_IDENTITY` boundary when the Master adopts it for continued use. Typical signal: an NPC asks the name, the player answers unambiguously, and the Master is about to continue as though the NPC remembers it.

Before further player-facing fiction relies on that adopted identity, publish one coherent setup transaction containing all already-established durable setup canon needed for honest resume, normally:
- PLAYER binding/preferences already settled;
- one stable PC ID with `status: provisional`, adopted identity/concept/current description, and only mechanics genuinely established so far;
- PC index entry;
- singleplayer card protagonist projection;
- settled CONFIG values;
- already-established starting premise/location/NPC/relationship/scene/current routing when those were presented as real campaign truth;
- optional first automatic campaign title under `CAMPAIGN_IDENTITY.md` when both protagonist/party concept and broad surrounding world are already durable.

Keep MANIFEST/card lifecycle `initializing`. This boundary is not character acceptance, READY_PC, PLAY_READY, or activation.

## DM-seeded surface details

The Master may seed undefined harmless external details such as clothing, hair, a visible mannerism or ordinary keepsake when they fit the concept and grant no hidden mechanical advantage. If presented as current fact and not contradicted, they may be stored as DM-seeded canon.

The player may later correct such details. Apply a compatible correction without ceremonial confirmation. Never label silence as player authorship; `player_defined_traits` contains only player-explicit facts.

Changes that would affect equipment, wealth, stats, abilities or prior causal consequences follow normal rules instead of becoming free retcons.

## Cadence after the checkpoint

PROVISIONAL_IDENTITY is intentionally narrow. Do not autosave every cosmetic/backstory answer afterward. Accumulate normal provisional refinements until character/PLAY_READY, explicit save, session/maintenance safety boundary, or another authoritative HARD rule fires.

Promote/update the SAME PC ID when the build later becomes READY_PC; never replace the PC merely because an earlier provisional checkpoint exists.

## Resume

A campaign stopped after PROVISIONAL_IDENTITY resumes unfinished setup from durable provisional PC/world/scene state. It remains `initializing` until READY_PC + PLAY_READY.

Routine successful persistence is invisible to the player.
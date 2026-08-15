# Explicit Save Contract

framework_module_version: 0.1.0
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for the semantic meaning and completeness of an explicit player save request; PERSISTENCE.md remains authoritative for HOW the resulting batch is published

## Purpose

When the player explicitly says `save`, `сохрани игру`, `save game`, or an unambiguous equivalent, the request means:

**materialize all established cross-session campaign state from the hot working set into the normal authoritative campaign records now.**

It does NOT mean `write some reminder that describes what happened`.

Singleplayer normally uses sparse persistence, but an explicit save overrides buffering for every currently established dirty fact that is meant to survive the chat.

## SAVE_ALL_DIRTY boundary

An explicit save creates a `SAVE_ALL_DIRTY` persistence boundary.

Before publication, classify the hot working set into:
- already-durable unchanged canon;
- dirty existing authoritative records;
- newly established canonical records that do not exist remotely yet;
- genuinely EPHEMERAL material that is not intended to survive the chat;
- unresolved/integrity-defective material that cannot honestly be promoted without repair.

Everything in the middle three durable categories must be materialized through its normal authoritative record/index/state representation before the save may be called successful.

Do not downgrade an established entity, relationship, objective, resource change, location, scene state, character fact or other durable consequence into prose merely because a structured record has not yet been created.

## Materialization checklist

Include only records actually implicated by current canon, but do not omit an implicated domain just to reduce write count.

Typical save materialization may include:
- PLAYER preferences/binding when changed;
- PC record and `PC_INDEX`;
- recurring NPC/companion records and `NPC_INDEX`;
- current/established location record and `LOCATION_INDEX`;
- active quest/contract/objective/thread records and `THREAD_INDEX`;
- item/ownership/currency/resource state in the owning authoritative records;
- active scene state and `SCENE_INDEX` when a resumable scene exists;
- `STATE/CURRENT.yaml` routing for current scene/thread/time/consequences;
- `CAMPAIGN_CARD.yaml` projection when protagonist, focal location, lifecycle/status, engine or relevant access display fields changed;
- compact semantic LOG/event records when needed for causal continuity;
- checkpoint records only when normal checkpoint policy says they add recovery value.

This is a semantic checklist, not an instruction to touch every file on every save.

## Summary-note prohibition

A prose recap, session summary, scratch note or ad-hoc file is NOT authoritative materialization of the state it describes.

Files such as `STATE/SAVE_NOTE.md`, `STATE/NOTES.md`, `*_SAVE.md`, or another invented summary artifact MUST NOT be created as a substitute for PC/NPC/location/thread/scene/current/index/card records.

If a supported session/log summary is useful, it may be written only as a supplementary record inside the SAME coherent save transaction after the authoritative state is represented normally.

If there is dirty durable state and the planned save changes only a summary/note file, the save MUST fail its local completeness check and MUST NOT be presented to the player as successful.

## Missing-record materialization

A fact already established in live play does not remain optional merely because its entity file/index was never created earlier.

At explicit save, missing normal records must be created now from the established hot state.

Examples:
- a played protagonist with no PC file -> materialize the PC and PC index;
- a recurring named companion with no NPC record -> materialize companion/NPC relationship state;
- an accepted job with no thread -> materialize the active thread and current routing;
- a known focal location with a blank campaign card -> materialize authoritative location/current state and refresh the card;
- a live scene represented only in narration -> materialize the minimum resumable scene state.

Do not broaden the world beyond established/currently needed facts merely because save is happening.

## Integrity defects during save

Explicit save is not permission to invent missing mechanics or retroactively validate unsupported narration.

If a dirty record is structurally/integrity-defective:
1. activate the relevant integrity/readiness module;
2. preserve every independently established fact;
3. repair deterministically when existing accepted choices/rules permit it;
4. never fabricate prior dice, mechanics or player choices;
5. if a meaningful player choice is required, persist the maximum honest recovery-safe structured state that schemas/policy permit and mark/retain the unresolved repair state through normal canonical mechanisms;
6. do not claim the campaign is fully play-ready until the defect is resolved.

A save may preserve an honest recovery frontier without pretending an invalid combat result or nonexistent character sheet was valid.

## Save does not imply pause

`save` alone does not change campaign lifecycle or stop play.

Only explicit `pause`, `stop`, `end session`, or equivalent intent should create the corresponding pause/session boundary/status change.

If the player says `save and stop`, both semantics apply in the same coherent transaction when practical.

## One coherent transaction

After materialization is complete, publish the whole `SAVE_ALL_DIRTY` delta as one `CAMPAIGN_TREE_TXN` under `PERSISTENCE.md`.

Do not use one commit for a note, another for the PC, another for CURRENT, etc.

Do not create a checkpoint merely because the player said save. Create one only if session/recovery policy independently justifies it.

## Pre-publication completeness assertions

Before `create_tree`, perform a local zero-I/O completeness check against the hot state and planned resulting records.

At minimum assert as applicable:
- every established active/provisional PC that must survive has a normal PC record and index entry;
- every established recurring actor needed for resume has its normal record/index representation;
- current focal location is represented consistently and campaign-card projection is not knowingly stale;
- current resumable scene/thread routing is represented in `STATE/CURRENT.yaml` and direct records;
- lifecycle/status is not left `initializing` if normal live play has already legitimately begun;
- no dirty durable fact survives only inside a prose summary/note;
- the planned transaction contains every dirty authoritative path required by those facts.

If an assertion fails, repair/materialize before publication rather than committing a knowingly incomplete save.

## Post-publication success semantics

After successful `update_ref(force=false)`:
- all paths included in the transaction become the known durable frontier;
- clear the corresponding dirty working set;
- do not immediately refetch the files just written;
- tell the player the game is saved only if no known cross-session durable fact that the save promised remains solely in volatile chat/prose.

If publication or completeness fails, do not say `saved`. State the blocking problem briefly only when user action or integrity repair is actually required.

## Performance

An explicit save is intentionally a rare boundary and may touch several files, but it is still one Git tree/commit/ref publication.

Do not optimize save latency by replacing structured state with a summary note. The point of sparse singleplayer persistence is that when a save boundary finally occurs, the accumulated batch is complete.
# Campaign Operations

framework_module_version: 0.1.1
load_when: campaign start, session start/end, prep, recap, campaign maintenance

## Campaign-level organization

Keep the campaign operationally legible without turning it into paperwork for the player.

The DM maintains:
- concise premise/tone/config;
- current scene/time and active PCs;
- a small set of active conflicts/threads;
- important NPC/faction changes;
- current unresolved clues/questions;
- relevant next-horizon prep;
- durable resources, ownership and conditions;
- session/checkpoint pointers.

Do not ask the player to manually maintain these records.

## Campaign start

Before first play, establish only the minimum needed:
1. campaign premise and mode;
2. tone/boundaries and house-rule choices;
3. characters and their connection to the premise;
4. starting location and immediate context;
5. first actionable situation;
6. initial active conflicts/factions only if useful now.

Do not require a complete world bible before the first scene.

## Session journal model

A compact session record should be able to answer:
- which session/date/branch is this?;
- what previous events materially affect today?;
- what is the current situation?;
- what prep is likely to matter?;
- what unexpected durable events happened?;
- what remains unresolved at the end?

This corresponds to operational notes, not a transcript.

## Session start

From canonical storage:
- identify HEAD and campaign;
- recap only prior facts needed now;
- restore current scene/resources/participants;
- retrieve active threads and directly relevant entities;
- load RUNTIME + AI_REASONING and only situational modules.

A recap is for orientation. It must not silently add or reinterpret canon.

## Preparation budget

Prioritize likely/high-impact material. A useful hierarchy is:
- `DEFINITE`: almost certain/current material; prepare exact mechanics and consequences;
- `LIKELY`: plausible next scenes/actors; compact preparation;
- `POSSIBLE`: names, motives, locations, clues or rule references only;
- `REMOTE`: leave undefined or indexed until needed.

Preparation detail should track probability and cost of improvisation, not the DM's affection for an idea.

## During play

Take lightweight internal notes only for facts likely to persist. Keep transient tactical detail only while it matters.

Do not commit every exchange. Batch durable changes at natural persistence boundaries. In multiplayer, publish race-sensitive shared changes promptly.

## Session end

Before ending or context transition, if state changed materially:
- persist the batch;
- update CURRENT/active scene state;
- update affected PC/NPC/item/location/faction/thread records;
- append semantic event information at the appropriate granularity;
- compact resolved hot state;
- create/update checkpoint when useful for exact resume;
- keep only next-horizon prep that is still plausible.

Unused provisional scenes do not become canon.

## Campaign conflicts

Maintain a small number of meaningful active conflicts rather than an ever-growing quest list. Conflicts can escalate, resolve, split or become irrelevant through play.

A conflict record should capture actors, goals, current pressure, known stakes and next change if unopposed. It should not prescribe the PCs' response.

## Player investment

Use observed player/character interests to decide what deserves preparation time: people, communities, mysteries, homes, rivals, goals, institutions or themes they repeatedly engage with.

Investment guides attention; it does not retroactively rewrite world truth or guarantee protection/reward.

## Periodic campaign audit

At natural intervals, review only compact active data and ask:
- Are any threads actually resolved but still marked active?
- Did important NPC goals/knowledge change?
- Is hot state duplicating history?
- Are old provisional hooks being mistaken for canon?
- Is lore becoming contradictory?
- Is the campaign accumulating too many simultaneous conflicts?
- Is context retrieval still index-driven and local?

Repair storage organization without altering fictional truth unless evidence requires a canon repair.

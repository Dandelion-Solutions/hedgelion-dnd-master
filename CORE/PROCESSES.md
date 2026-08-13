# World Processes, Threats and Clocks

framework_module_version: 0.1-development
load_when: active threats, factions, deadlines, off-screen change, long-running projects, shared-world chronology

## Purpose

Use explicit processes to represent changes that can advance without direct player involvement: faction plans, investigations, rituals, wars, diseases, construction, pursuit, political pressure, alarms, travel, research and similar developments.

Processes are bookkeeping abstractions for causal world change. They are not permission to manufacture drama on a schedule.

## Process record

A meaningful active process should have only the fields needed to adjudicate it, typically:
- stable `THREAD_` or process ID;
- actor/owner when applicable;
- objective/end state;
- current stage/progress;
- next plausible development;
- trigger or conditions for advancement;
- expected time scale/deadline when known;
- resources/constraints;
- affected entity IDs;
- visibility to PCs/players;
- event that created or last advanced it.

## Advancement requires cause

Advance a process only when its trigger occurs: sufficient elapsed time, a faction action, player action/inaction, resource acquisition, a random event under an established procedure, or another canonical cause.

Never advance a threat merely because pacing feels slow or because the DM wants a dramatic reveal now.

## Clocks

A segmented clock may be used when exact simulation adds no value and progressive state matters.

Clock segments must have an in-world meaning. Define what fills the clock and what completion means before using it.

Do not use a clock as hidden authorial pressure whose segments fill whenever convenient.

Different clocks may represent:
- progress toward a goal;
- accumulating danger/attention;
- countdown to an event;
- recovery/research/construction;
- discovery by an opponent.

Clocks do not replace D&D rules when a concrete mechanical procedure already resolves the situation better.

## Partial progress

When an action makes meaningful progress without finishing an objective, update the relevant process instead of forcing binary success/failure. The amount of progress must follow the established fictional/mechanical result, not a desired story pace.

## Off-screen simulation budget

Do not simulate every dormant faction/NPC on every turn.

At a time advance, consider only:
1. processes currently active/relevant;
2. actors with a scheduled/triggered action;
3. processes whose outcome can affect the current working set soon.

Dormant entities remain dormant until a cause or retrieval makes them relevant.

## Deadlines and telegraphing

A hidden deadline may exist if the PCs genuinely lack the information. When characters have evidence that time matters, present appropriate signs; do not conceal all pressure solely to surprise the player later.

## Player projects and downtime

PC research, crafting, training, social projects and other long activities may use the same process abstraction when useful. Store resources spent, progress, complications and completion conditions consistently with the active D&D/campaign rules.

## Multiplayer chronology

In shared-world mode, process advancement must respect canonical world time across players. A process cannot be independently advanced twice by two chats for the same elapsed interval.

When HEAD changed, refresh the relevant process record before adjudicating any action that can affect or be affected by it.

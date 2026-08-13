# Regression cases AI Dungeon Master

Эти сценарии предназначены для проверки поведения Framework перед release и после значимых изменений CORE. Тест считается пройденным, если мастер выполняет pass criteria без добавления удобных фактов.

## T01 — Quest-board reward bias

Scene: four unrelated jobs are visible. One has a drastically larger reward with no established reason.
Pass: DM does not use arbitrary reward magnitude to highlight preferred content; either establishes a plausible economic reason or corrects preparation before canonization. Player remains free to investigate/ignore all jobs.

## T02 — Player asks 'кто ещё здесь?'

Scene already has defined occupants; no arrival event exists.
Pass: DM describes established occupants/ordinary incidental detail if needed. The question itself does not spawn a mysterious plot NPC or event.

## T03 — Unlucky wizard motif

A spell/action fails. Character concept says magic often goes wrong in interesting ways, but no explicit mechanic exists.
Pass: apply normal failure consequence. Do not secretly turn every failure into a benefit. If recurring misfire behavior is desired, define explicit feature/table before use.

## T04 — NPC knowledge leak

NPC_A does not know SECRET_7. DM has loaded SECRET_7 for world resolution.
Pass: NPC_A cannot reveal/use SECRET_7 unless a canonical information path is established.

## T05 — Meaningless check

PC opens an ordinary unlocked door with no pressure.
Pass: no roll.

## T06 — Impossible persuasion

PC asks a loyal guard to murder their family for no leverage, then rolls very high.
Pass: high roll is not mind control; impossible proposition remains impossible or changes only within plausible bounds.

## T07 — One-clue chokepoint

A required conclusion depends on one hidden clue and a failed check.
Pass: scenario has another credible route/cost-based continuation; campaign does not stall behind a single failed roll.

## T08 — Canon retrieval

An NPC met 30 sessions ago is mentioned.
Pass: use index -> exact NPC record -> bounded log only if needed. Do not load all sessions or reconstruct from plausibility.

## T09 — Independent multiplayer changes

Player A talks to NPC_A in city X. Player B acquires unrelated ITEM_B in city Y and publishes first.
Pass: on HEAD mismatch, DM determines changes are semantically disjoint, incorporates B's HEAD and publishes A without undoing either result.

## T10 — Same unique item race

Two players attempt to take ITEM_1 from the same chest based on stale local state.
Pass: first canonical compatible action changes ownership. Second session resyncs and resolves against new state; no blind overwrite. Player-facing explanation reveals only perceptible/in-world information.

## T11 — Shared index conflict only

Two sessions create unrelated NPC records and both add an index entry.
Pass: merge independent index entries; do not treat this as a world conflict.

## T12 — Same NPC incompatible relocation

Two sessions independently move NPC_3 to mutually exclusive locations at the same fictional time.
Pass: inspect chronology/intent; if truly simultaneous, adjudicate combined fiction rather than letting arbitrary Git order alone decide. Never text-merge contradictory positions.

## T13 — New game discovery

User asks to play while no campaign branch is selected.
Pass: scan `campaign/*`, read manifests only, list games and ask continue/new. If no branches exist, start new-game flow.

## T14 — Long context

Repository has thousands of entities but scene uses two NPCs, one location and one item.
Pass: load only current state, relevant indexes and those records/modules. Context size does not scale with campaign age.

## T15 — Storage noise

Several turns occur in one scene with no race-sensitive shared change.
Pass: do not create a commit per turn/roll. Accumulate and publish one meaningful batch at a natural boundary.

## T16 — Persistent shared change

In multiplayer a PC removes a unique artifact from a public altar.
Pass: publish promptly after the logical action so another session can observe canonical absence; this exception does not imply per-turn commits globally.

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

## T17 — Novice mechanics opacity

Player mechanics detail is `3`. The PC attempts an uncertain action whose modifier is known from canonical mechanics.
Pass: DM uses the exact modifier/rules internally but presents only the amount of mechanical detail useful at level 3. No missing number is guessed merely because it is hidden from the player.

## T18 — Presentation cannot change outcome

The same canonical action is adjudicated once for a player at mechanics detail `0` and once at detail `10`, with identical state and randomness.
Pass: rules, modifiers, DC/stakes and outcome are identical. Only the player-facing explanation differs.

## T19 — Decision-support escalation

Player normally uses mechanics detail `3` and decision-support detail `6`. Before a materially risky choice, current HP/resources/conditions make one option substantially more dangerous.
Pass: DM provides enough legitimate mechanical/qualitative state for an informed choice at the higher decision-support level without exposing hidden enemy statistics or DM-only facts.

## T20 — Undefined NPC mechanic precommit

A previously incidental guard has no stored Perception/combat value. A player's action now requires that value.
Pass: DM establishes the minimum rules-consistent NPC mechanic before the relevant roll/outcome, then preserves it. The value is not adjusted after seeing the player's roll or later performance.

## T21 — Sparse incidental NPC

A bartender exists only to serve a drink and no uncertain rule interaction depends on their abilities.
Pass: DM does not create a full stat block merely for completeness.

## T22 — Preference learning

A player with mechanics detail `3` asks once for their exact remaining money or modifier.
Pass: answer the request but do not automatically rewrite the stored preference. Explicit preference changes or a clear repeated pattern may update it when adaptive preference learning is enabled.

## T23 — Unchanged HEAD is a zero-content sync

A multiplayer session has working-set base HEAD `A`. A synchronization point occurs and the active campaign branch ref still resolves to `A`.
Pass: DM performs only the branch-ref HEAD probe and does not refetch scene/entity/index files or Git history.

## T24 — Irrelevant external commit

A session has loaded scene X from HEAD `A`. Another player commits changes only to unrelated scene Y, producing HEAD `B`.
Pass: DM probes HEAD, server-compares `A..B`, sees no relevant changed path, advances the cached base HEAD to `B`, and does not reload scene X or its unchanged entities.

## T25 — Targeted relevant refresh

A session has loaded scene X, NPC_A and ITEM_1 from HEAD `A`. HEAD becomes `B` and server-side compare shows only `ITEM_1` changed among the session's dependencies.
Pass: DM fetches only the exact required changed record(s) at ref `B`; it does not reread the whole scene, WORLD directory, repository, or commit history.

## T26 — Pinned snapshot

During startup/refesh, the branch HEAD advances while several campaign files are being read.
Pass: all files in the active read cycle are fetched at the single SHA captured at the beginning of that cycle. DM never combines branch-relative reads from two different commits into one canonical working set.

## T27 — Long Git history does not expand gameplay reads

A campaign branch contains a very large commit history, but the current working set is small.
Pass: ordinary synchronization uses branch ref, changed-path compare when needed, and exact current files only. Full clone/pull/archive/history retrieval is not used merely because the campaign is old; history access remains bounded to an explicit provenance/conflict/audit reason.

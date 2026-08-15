# Explicit Save Regression Cases

These cases protect the semantic meaning of `save game` from degrading into summary-note persistence or accidentally changing campaign readiness/lifecycle.

## S01 — Explicit save flushes accumulated singleplayer SOFT state
Hot state contains a played PC, recurring companion, employer NPC, accepted job, payment state, current location and active scene. Much of it has been buffered SOFT.
Player says `сохрани игру`.
Pass: one SAVE_ALL_DIRTY transaction materializes all established cross-session state through the normal PC/NPC/location/thread/scene/CURRENT/index/card/log records implicated by the state.

## S02 — Summary-only save is failure
Dirty structured campaign state exists.
Planned transaction changes only `STATE/SAVE_NOTE.md` (or another prose summary).
Pass: local completeness assertion fails; do not publish/claim successful save as a substitute for structured state.

## S03 — Bdyr incident regression
Established hot state includes Бдыр as protagonist, Кабыздох as recurring companion, the tavern/employer/job/payment facts, current road/ambush situation, while remote PC_INDEX/card/CURRENT are still scaffold-empty.
Player explicitly saves.
Pass: Master may not preserve these facts only in one prose note. It must materialize the normal authoritative records/indexes/card/current state for every independently established fact that can honestly be represented.

## S04 — Missing entity file must be created
A recurring NPC was established during sparse play but has no remote NPC record yet.
Player saves.
Pass: create the NPC record + index entry in the same save transaction; do not merely mention the NPC in LOG/notes.

## S05 — Card is refreshed as part of save
Protagonist/current focal location are known, but CAMPAIGN_CARD still contains stale scaffold values.
Player saves.
Pass: materialize authoritative source state and refresh card in the same transaction. Campaign name on card must exactly match MANIFEST including null.

## S06 — CURRENT must be resumable
There is an active/resumable scene/thread in hot state, while remote STATE/CURRENT has empty arrays.
Player saves.
Pass: update CURRENT plus the direct scene/thread records needed for resume. A prose recap is not a substitute.

## S07 — Save alone does not pause
Player says only `сохрани игру` and intends to continue.
Pass: flush state but do not change campaign lifecycle to paused merely because a save occurred.

## S08 — Save and stop combines boundaries
Player says `сохрани и остановимся`.
Pass: materialize all dirty state and apply the intended pause/session boundary coherently, preferably in one transaction, without inventing READY_PC.

## S09 — No fake mechanics during repair
A legacy/broken campaign has a named/classed PC but no valid character mechanics, and some narrated combat was never mechanically resolved.
Player saves.
Pass: preserve independently established structured facts; do not invent retrospective stats/dice to make the save look complete. Apply CHARACTER_READINESS/MECHANICS_INTEGRITY repair semantics.

## S10 — Supplementary summary allowed but not authoritative
All normal records are correctly included in SAVE_ALL_DIRTY and a supported compact session summary is also useful.
Pass: summary may join the same transaction, but removing it would not remove the authoritative state.

## S11 — No ad-hoc state schema invention
Runtime considers inventing `STATE/NOTES.md`, `STATE/SAVE_NOTE.md`, or another scratch persistence file because creating proper entities seems slower.
Pass: reject that shortcut; use defined campaign records/indexes/state.

## S12 — One save, one campaign transaction
Explicit save affects PC + NPC + thread + scene + CURRENT + card.
Pass: one CAMPAIGN_TREE_TXN/one gameplay commit, not per-file commits.

## S13 — No forced checkpoint
Explicit save occurs during an ordinary safe scene and normal records are enough to resume.
Pass: no checkpoint solely because the word `save` was used.

## S14 — Completeness check is local
Before publication runtime verifies hot established facts against planned resulting records.
Pass: this check does not fetch GitHub; it works from known frontier + hot dirty state + planned tree.

## S15 — Do not say saved on partial failure
Some established durable fact cannot be honestly materialized/published and the unresolved issue remains.
Pass: do not tell the player the game is fully saved. State only the minimal actionable/integrity problem.

## S16 — Successful save clears dirty canonical state
SAVE_ALL_DIRTY publishes successfully.
Pass: all included durable dirty records are cleared in the hot working set and created commit/tree become the known frontier; no confirmation refetch is performed.

## S17 — Explicit save during onboarding stays initializing
Campaign has a provisional PC `Грым`, incomplete abilities/HP/class mechanics, a resumable onboarding road/pony scene and structured current state. Player says `сохрани игру`.
Pass: save all honest structured setup state but keep MANIFEST/CAMPAIGN_CARD `status: initializing`. Do NOT set active merely because a scene/current location exists.

## S18 — Active requires READY_PC + PLAY_READY
Planned explicit-save tree sets status active while PC remains provisional with empty required mechanics.
Pass: pre-publication completeness assertion fails. Rebuild the transaction with initializing setup status (or first genuinely complete READY_PC/PLAY_READY); do not publish contradictory active/provisional state.

## S19 — Save cannot rewrite unrelated template files
Dirty set contains PC/PLAYER/location/NPC/scene/CURRENT/card only. README guide and RULES/HOUSE_RULES have no semantic changes.
Pass: planned tree inherits those blobs byte-for-byte from base tree; they are absent from the dirty path delta.

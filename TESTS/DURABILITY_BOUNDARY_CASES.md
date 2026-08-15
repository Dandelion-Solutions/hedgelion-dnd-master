# Durability Boundary Regression Cases

These cases protect sparse low-latency singleplayer saves without allowing the playable campaign frontier to remain an empty scaffold or contradictory active/provisional state.

## D01 — Scaffold is not play-ready
Initial campaign scaffold commit exists, but PC/PLAYER/current scene are still empty.
Pass: Master may ask setup questions or use a pre-live onboarding vignette, but MUST NOT begin true mechanics-dependent live play while scaffold is the only durable campaign commit.

## D02 — Combined play-ready launch is allowed
READY_PC, initial focal location and opening situation all become settled without returning control to the player.
Pass: one coherent post-scaffold PLAY_READY transaction may contain PC + PLAYER + indexes/card + minimal current scene/state + status active, then true live narration begins. No unnecessary separate commits.

## D03 — Stable character cannot cross another user turn only in RAM
PC identity/mechanics are settled. Master still needs to ask another setup question and return control.
Pass: persist stable character/PLAYER/index/card before returning control, unless the same response will publish full PLAY_READY state.

## D04 — Semantic acceptance without magic phrase
Master presents a viable character. Player answers a later companion/world question without rejecting the character.
Pass: treat character as accepted for durability purposes; do not require an extra `confirm` round trip solely to save it.

## D05 — Genuine unresolved mechanic stays provisional
Character concept exists but a materially different class/ability choice remains unresolved.
Pass: no forced acceptance/activation; ask the smallest required question or continue safe onboarding before true live play.

## D06 — First true live scene requires durable PC
Master is about to resolve normal player action using the chosen hero.
Pass: READY_PC + PLAYER + PC_INDEX + card protagonist and minimum resume state are durable first. `PC_INDEX.entries: []` with true live play is a failure.

## D07 — Solo quest contract stays SOFT
Singleplayer hero accepts a job for 100 gp, receives 50 gp now and will receive 50 gp later. No location/status/session boundary occurs.
Pass: contract/thread/payment/NPC relationship/log become dirty canon in hot working set, but this event alone creates NO GitHub transaction.

## D08 — Solo recurring companion may stay SOFT
During live singleplayer, a named dog becomes an ongoing companion after PLAY_READY.
Pass: companion entity/relationship becomes dirty canon but does not require an immediate standalone commit. It is flushed at the next key boundary.

## D09 — No per-turn autosave
Several meaningful solo actions produce quest, NPC, clue, resource and relationship SOFT changes while focal location remains unchanged.
Pass: keep accumulating one dirty working set; ordinary turns perform zero GitHub calls.

## D10 — Multiple SOFT domains do not force a save by count
Singleplayer dirty set contains recurring actor + active objective + currency/item changes + NPC relationship changes, but no concrete recovery risk and no key boundary.
Pass: continue from hot state without inventing an autosave merely because many domains are dirty.

## D11 — Focal location change flushes accumulated SOFT
Hero leaves the tavern for the market square; `CAMPAIGN_CARD.current_location` must change. Dirty set also contains a contract, 50 gp payment, companion and NPC relationship changes.
Pass: one coherent transaction publishes authoritative location/current state + card update + ALL valid accumulated SOFT changes. Exactly one commit.

## D12 — Tactical movement is not a focal-location boundary
Hero moves from one table to another, upstairs/downstairs within the same tavern, or changes combat position.
Pass: do not update `CAMPAIGN_CARD.current_location` and do not create a save merely for this movement.

## D13 — Lifecycle boundary flush
Singleplayer campaign is explicitly paused/completed or user asks to save/end session.
Pass: publish intended lifecycle/current state + card status and all accumulated SOFT dirty canon in one coherent transaction. Save by itself preserves existing truthful lifecycle.

## D14 — Initializing cannot survive legitimate normal live play
Campaign/card still say initializing, but READY_PC + PLAY_READY exist and Master has already begun normal adventure play.
Pass: classify as durability invariant violation; publish/repair active state before further ordinary play.

## D15 — Active cannot precede READY_PC
Campaign/card say active while protagonist is `status: provisional` and required character mechanics are missing.
Pass: classify as durability invariant violation. Repair back to initializing setup or complete READY_PC/PLAY_READY before further normal play.

## D16 — Durable onboarding scene may remain initializing
A pre-live story-first road/pony vignette has been saved with provisional PC and current scene routing so setup can resume.
Pass: lifecycle remains initializing; the mere existence of current scene/location does not force active.

## D17 — Boundary check is zero-I/O
Before an ordinary response runtime checks whether dirty state crossed a durability boundary.
Pass: classification uses only hot working-set facts and performs no HEAD/fetch call. GitHub transport starts only if answer is yes.

## D18 — Concrete context-loss risk may force exceptional flush
A long solo scene has dirty SOFT state and runtime positively detects impending context compaction/maintenance that will invalidate hot state before a normal location/session boundary.
Pass: one exceptional safety flush is allowed; do not use fixed timers or message counts.

## D19 — Multiplayer is not forced into sparse solo cadence
A shared-world fact becomes material to another active player before a solo-style location boundary.
Pass: follow MULTIPLAYER/LIVE_SCENE/shared durability rules and publish when required for shared canon; do not defer solely because singleplayer profile would.

## D20 — Successful save stays invisible
Any PROVISIONAL_IDENTITY/PLAY_READY/location/lifecycle/safety transaction succeeds.
Pass: continue fiction without commit/HEAD/YAML commentary. Surface persistence only if failure materially blocks or changes play.

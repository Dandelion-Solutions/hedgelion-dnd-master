# Durability Boundary Regression Cases

These cases protect sparse low-latency singleplayer saves while separating pre-live onboarding from READY_PC/PLAY_READY live play and preserving the settled owner-valid durability-risk trajectory.

## D01 — Scaffold is not play-ready
Pass: setup may begin, but true live play cannot begin while scaffold is the only durable campaign commit.

## D02 — Pre-live onboarding may be durable
A provisional PC/name/setup scene exists under DIEGETIC_ONBOARDING. Pass: coherent PROVISIONAL_IDENTITY may be saved while lifecycle remains initializing.

## D03 — Combined PLAY_READY launch is allowed
READY_PC + starting location/situation resolve without another user turn. Pass: one coherent PLAY_READY transaction may activate the campaign and begin true live narration.

## D04 — Stable READY_PC cannot cross another user turn only in RAM
Pass: persist character before returning control unless same response publishes full PLAY_READY.

## D05 — Semantic acceptance has no magic phrase
Pass: continued use of mechanically ready hero may establish acceptance without extra confirm round trip.

## D06 — Genuine unresolved mechanic stays provisional
Pass: ask smallest necessary question; no activation.

## D07 — True live scene requires READY_PC + PLAY_READY
Pass: no mechanically capable live scene with empty/incomplete PC mechanics/index.

## D08 — Solo quest contract stays SOFT
Pass: contract/payment/NPC changes alone create no transaction.

## D09 — Solo recurring companion may stay SOFT
Pass: companion/relationship becomes dirty and waits for next owner-defined boundary or applicable durability-risk preservation opportunity.

## D10 — No per-turn autosave
Pass: multiple ordinary meaningful turns may accumulate dirty state with zero GitHub traffic while exposure remains lawfully deferrable.

## D11 — Dirty-domain count is not a boundary
Pass: quest + item + NPC + relationship dirty together still do not force save by count.

## D12 — Focal location change flushes accumulated SOFT
Pass: live coarse location change publishes location/current/card plus all causally valid dirty SOFT state in one transaction.

## D13 — Tactical movement is not focal-location boundary
Pass: movement within same menu-level location causes no card/save boundary.

## D14 — Generic scene/encounter completion is not a solo boundary
Pass: no commit unless another listed guard (location/lifecycle/save/safety/etc.) also fires.

## D15 — Lifecycle boundary flush
Pass: valid pause/completion/archive/reactivation publishes lifecycle + dirty state coherently.

## D16 — Explicit save is not activation
Provisional onboarding PC is saved. Pass: flush structured truth and remain initializing.

## D17 — Stop unfinished setup is not paused
Pass: remain initializing; paused requires prior PLAY_READY/normal play.

## D18 — Active requires READY_PC + PLAY_READY
Pass: active + provisional/incomplete PC is invariant violation and must be repaired.

## D19 — Boundary/exposure check is zero-I/O
Pass: classification uses already-available owner-valid hot evidence; transport starts only after an actual boundary or bounded preservation opportunity is established.

## D20 — Concrete context-loss risk may force safety flush
Pass: verified compaction/maintenance suspension that would otherwise destroy the hot dirty set may create its existing stronger safety boundary. Fixed message/timer/count autosave remains forbidden.

## D21 — ELEVATED prioritizes preservation without blocking play
SOFT dirty state has increasing owner-valid loss exposure but has not reached DANGER. Pass: at the next suitable safe established-state opportunity preservation outranks optional Story/planning/enrichment; no correctness HARD or automatic gameplay block is created.

## D22 — DANGER gets one bounded preservation attempt before same-scope growth
Owner-valid still-relevant unpublished-state/loss-exposure evidence establishes DANGER and the next operation would materially enlarge that dirty scope. Pass: request one owner-valid bounded preservation/recovery attempt; if it remains unavailable/unsuccessful, guard that state-growing operation in the affected scope. Independent operations outside that scope remain eligible under their owners.

## D23 — DANGER is not HARD, corruption, timer or retry loop
Pass: DANGER alone does not create a named correctness durability edge, rollback, exact wall-clock trigger, background worker/heartbeat/polling or automatic retry.

## D24 — Advisory host pressure alone cannot create gameplay DANGER
Only approximate context/token/message/chat-age/capacity pressure is available; no owner-valid still-relevant unpublished-state/loss-exposure evidence establishes the affected scope. Pass: conservative proactive preservation may be requested, but no gameplay-affecting DANGER guard is established from that advisory signal alone.

## D25 — Clean state never creates heartbeat persistence
No canonical/current dirty state exists. Pass: time/chat/context pressure or exposure reevaluation creates no empty/no-op commit, timestamp mutation or checkpoint.

## D26 — Multiplayer may publish earlier
Pass: shared visibility/access/live synchronization may override sparse solo cadence for that scope.

## D27 — Successful persistence stays invisible
Pass: no commit/HEAD/YAML narration unless user asks or failure/conflict needs action.

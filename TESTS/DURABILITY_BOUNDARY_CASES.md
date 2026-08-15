# Durability Boundary Regression Cases

These cases protect sparse low-latency singleplayer saves while separating pre-live onboarding from READY_PC/PLAY_READY live play.

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
Pass: companion/relationship becomes dirty and waits for next forced boundary.

## D10 — No per-turn autosave
Pass: multiple ordinary meaningful turns may accumulate dirty state with zero GitHub traffic.

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

## D19 — Boundary check is zero-I/O
Pass: classification uses hot state only; transport starts only after yes.

## D20 — Concrete context-loss risk may force safety flush
Pass: verified compaction/maintenance suspension may flush dirty state; fixed message/timer/count autosave is forbidden.

## D21 — Multiplayer may publish earlier
Pass: shared visibility/access/live synchronization may override sparse solo cadence for that scope.

## D22 — Successful persistence stays invisible
Pass: no commit/HEAD/YAML narration unless user asks or failure/conflict needs action.

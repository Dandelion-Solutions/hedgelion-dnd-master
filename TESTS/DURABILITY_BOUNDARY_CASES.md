# Durability Boundary Regression Cases

These cases protect the balance between low-latency play and durable campaign continuity.

## D01 — Scaffold is not play-ready
Initial campaign scaffold commit exists, but PC/PLAYER/current scene are still empty.
Pass: Master may ask setup questions, but MUST NOT begin the first live scene while scaffold is the only durable campaign commit.

## D02 — Combined play-ready launch is allowed
Character, minimal location and opening situation all become settled within one assistant turn.
Pass: one coherent post-scaffold PLAY_READY transaction may contain PC + PLAYER + indexes/card + minimal current scene/state + status active, then narration begins. No unnecessary separate world commit.

## D03 — Stable character cannot cross another user turn only in RAM
PC identity/mechanics are settled. Master still needs to ask one optional/secondary setup question and return control to player.
Pass: persist stable character/PLAYER/index/card before returning control, unless same response will publish the full PLAY_READY transaction.

## D04 — Semantic acceptance without magic phrase
Master presents a viable character. Player answers a later companion/world question without rejecting the character.
Pass: treat character as accepted for durability purposes; do not require an extra `confirm` round trip solely to save it.

## D05 — Genuine unresolved mechanic stays provisional
Character concept exists but a materially different class/ability choice remains unresolved.
Pass: no forced acceptance; ask the smallest required question before making the PC durable as active.

## D06 — First live scene requires durable PC
Master is about to open the first scene using the chosen hero.
Pass: stable PC + PLAYER + PC_INDEX + card protagonist and minimum resume state are durable first. `PC_INDEX.entries: []` with active live play is a failure.

## D07 — Quest contract is HARD
Player agrees to help an NPC for 100 gp, with 50 gp paid now and 50 gp due after completion.
Pass: acceptance + obligation/reward thread + received 50 gp + affected NPC/PC/resource/log state publish as one coherent transaction before the deal is treated as durably completed.

## D08 — Permanent companion is durable
A named dog becomes the hero's ongoing companion rather than incidental scenery.
Pass: companion entity/relationship and directly affected indexes/state become durable at that natural/HARD boundary or in the imminent PLAY_READY launch transaction; do not leave the recurring companion only in chat for a long play sequence.

## D09 — No per-turn autosave regression
Several low-impact actions produce only small SOFT changes and no recovery-sensitive accumulation.
Pass: keep dirty state in memory; zero GitHub calls on ordinary turns.

## D10 — Semantic safety flush
Dirty SOFT state now spans recurring actor + active objective/thread + meaningful ownership/resource change, with another player action about to begin.
Pass: flush one coherent batch at the next quiet beat even if no fixed turn/time threshold was reached.

## D11 — Scene transition flushes meaningful old dirty state
A scene ends while important durable consequences from it are still dirty.
Pass: save them coherently before or at the transition rather than carrying an increasingly large volatile backlog into the next scene.

## D12 — `initializing` cannot survive normal live play
Campaign/card still say `initializing`, but the Master has already begun normal adventure play.
Pass: classify as durability invariant violation; publish/repair the coherent play-ready state silently before further ordinary play.

## D13 — HARD save remains one transaction
A contract creates a thread, changes NPC relationship, gives currency and updates the log/current state.
Pass: one CAMPAIGN_TREE_TXN containing all related records; never one commit per fact/file.

## D14 — Boundary check is zero-I/O
Before an ordinary response the runtime checks whether dirty state has crossed a durability boundary.
Pass: the classification itself uses only hot working-set facts and performs no HEAD/fetch call. GitHub transport starts only if the answer is yes.

## D15 — Successful save stays invisible
A play-ready/HARD/safety-flush transaction succeeds.
Pass: continue narration without commit/HEAD/YAML commentary. Surface persistence only if failure materially blocks or changes play.

# HDM Gameplay Retrospective and Campaign Exit — Product Owner Decision

Status: **OWNER-APPROVED PRODUCT SEMANTICS — CANONICAL INPUT**

Date: 2026-09-05

Purpose:

> Fix two ordinary HDM gameplay/navigation semantics before downstream bootstrap and interaction architecture proceeds: retrospective history interaction for an active player, and an explicit save-and-exit transition back to campaign selection.

This decision adds product/consumer requirements. It does not create a new truth owner, Story authority, persistence authority, lifecycle state, membership state, or hierarchy of gameplay modes.

---

# 1. Product entry model

The baseline user-facing model is:

```text
new chat / campaign-selection state
    -> show campaigns visible to the current principal
    -> explicit campaign choice

selected active campaign
    + gameplay participation allowed
        -> ordinary D&D Master gameplay

selected active campaign
    + visible/readable
    + gameplay participation not allowed
        -> read-only Commentator interaction

selected completed campaign
    + visible/readable
        -> read-only Commentator interaction
```

Commentator is not an additional mode that an authorized active player must enter merely to inspect or discuss campaign history.

Campaign visibility, participation eligibility, PLAYER/PC binding, campaign lifecycle and information eligibility remain owned by their existing HDM authorities.

---

# 2. Retrospective/history capability inside ordinary gameplay

An authenticated/authorized player who is already participating in an active campaign through their normal gameplay context may address the D&D Master in natural language about past campaign history without leaving gameplay.

Examples include requests equivalent to:

- remind me what happened at an earlier point;
- who is this NPC;
- why did that NPC act that way;
- explain an earlier session in more detail;
- recount the history of this place;
- summarize or discuss an earlier event, relationship, clue, decision or consequence.

These are ordinary Master interactions, normally through the existing out-of-character Master channel when the intent is retrospective/meta rather than an in-world utterance.

## 2.1 Information eligibility and no-spoiler law

Retrospective access does not grant omniscience.

The Master may use the campaign's available admitted history/continuity evidence to answer, including eligible Story as orientation/routing evidence under the existing continuity contracts, but the player-facing result MUST respect the current principal/player/PC information boundary.

In particular:

- repository readability or broad DM/runtime access does not widen what may be revealed;
- Story availability does not widen eligibility;
- current `world.knowledge`, `runtime.disclosure`, role-context eligibility and other applicable information owners remain controlling;
- a material current/source-specific claim must use the proper stronger owner/evidence class where existing Context Runtime rules require escalation;
- the Master must not reveal a secret, later fact or other information that the current player/PC is not authorized to receive merely because the complete campaign history contains it.

A retrospective answer is presentation/interaction. It does not itself create a new fictional event, advance world time, alter PC knowledge by fiat, or mutate campaign truth merely because the player asked about history.

## 2.2 No duplicate history subsystem

This requirement creates no new generic memory/history authority and no parallel gameplay-history store.

Existing history/continuity/Story/current-owner architecture remains in force. The requirement is a **new explicit gameplay consumer binding** over those accepted sources and eligibility rules.

---

# 3. Explicit save-and-exit transition

Ordinary HDM gameplay MUST recognize an unambiguous user intent equivalent to:

> `Сохрани игру и выйди из игры.`

The semantic composition is:

```text
explicit save request
    -> satisfy the existing explicit-save / persistence contract
    -> satisfy applicable session/live closure requirements
    -> end the current gameplay context for this chat
    -> clear the selected-campaign gameplay binding/working context
    -> return to the campaign-selection state
    -> show the currently available campaign choices under the normal campaign-menu rules
```

This is an explicit lifecycle/navigation transition of the **current gameplay session/context**, not a new campaign lifecycle enum.

## 3.1 Save correctness precedes successful exit

If the user explicitly requested save-and-exit, HDM MUST NOT claim the transition completed successfully while promised durable state remains only volatile because the save/persistence operation failed or is known incomplete.

Existing save, persistence, durability, concurrency and recovery owners decide the required technical closure. The exit command does not weaken them or create an alternate save path.

If a blocking persistence/integrity problem prevents the requested durable save, surface the necessary blocking problem and preserve the maximum recovery-safe current context instead of falsely reporting both `saved` and `exited`.

## 3.2 Exit is not pause, completion, archive or multiplayer leave

`save and exit` does **not** by itself mean:

- set campaign lifecycle to `paused`;
- set campaign lifecycle to `completed` or `archived`;
- deactivate a multiplayer `PLAYER_` binding;
- voluntarily leave campaign membership;
- relinquish PC control;
- change multiplayer mode or join policy.

Those are distinct semantic transitions and remain governed by their existing owners.

A separate explicit pause/stop/campaign-end/membership-leave intent may compose with exit when the user actually expresses it and the applicable owner permits it.

For multiplayer, one player's session exit must not pause or terminate the campaign for other participants. If an active live/shared-state protocol requires a safe handoff/closure for that departing session, perform only the closure required by the existing live/session/concurrency contracts; do not infer membership removal or global campaign pause.

---

# 4. Ownership and architecture classification

These two requirements are classified as follows.

## 4.1 Retrospective gameplay history

```text
classification:
    NEW EXPLICIT PRODUCT / CONSUMER REQUIREMENT
    NO NEW INFORMATION AUTHORITY
    NO NEW STORY AUTHORITY
    NO NEW MODE

primary accepted semantic inputs:
    Step-4 truth / knowledge / disclosure / role-context architecture
    R2.1 continuity/history architecture
    R2.3 Context Runtime eligibility/retrieval architecture
    accepted Story/continuity architecture including WP-18

runtime consumer surfaces to reconcile:
    GAME/CORE/RUNTIME.md
    applicable information/narration/context-routing instructions
    history/Story retrieval consumers where required
```

Closed Story/continuity/information architecture is not reopened merely because this newly explicit consumer uses it. Reopen only if the current consumer audit demonstrates an actual contradiction or material insufficiency.

## 4.2 Save and exit to campaign selection

```text
classification:
    NEW EXPLICIT PRODUCT / NAVIGATION REQUIREMENT
    COMPOSITION OF EXISTING SAVE + SESSION + CAMPAIGN-SELECTION OWNERS
    NO NEW PERSISTENCE AUTHORITY
    NO NEW CAMPAIGN LIFECYCLE STATE
    NO NEW MEMBERSHIP STATE

primary runtime owners/consumers to reconcile:
    GAME/CORE/SAVE_CONTRACT.md
    GAME/CORE/SESSION.md
    GAME/CORE/MULTIPLAYER.md where applicable
    GAME/CORE/BOOTSTRAP_RUNTIME.md
    GAME/INSTALL/00_DND_BOOTSTRAP.md
    GAME/CORE/RUNTIME.md
```

The campaign-selection state is reusable after an explicit in-chat gameplay exit; starting a brand-new chat remains an alternative path, not the only path back to campaign choice.

---

# 5. WP-19 obligation

R2.7 WP-19 owns the current bootstrap/campaign-selection/lifecycle-navigation audit surface and MUST incorporate this decision before its Step-1 package can again be considered ready for mandatory Senior review.

WP-19 framing must explicitly account for:

1. active+playable selection routing to ordinary gameplay rather than Commentator;
2. active visible/readable but non-playable routing to read-only Commentator;
3. completed visible/readable routing to read-only Commentator;
4. ordinary gameplay retrospective/history interaction with current player/PC eligibility and no-spoiler constraints;
5. explicit save-and-exit composition back to campaign selection;
6. distinction between session/context exit and campaign pause/completion/archive/membership leave;
7. multiplayer non-interference when one participant exits;
8. machine/runtime/instruction/test destinations for those requirements without premature implementation.

Any WP-19 Step-1 critic that predates this owner decision is insufficient for the current mandatory Senior gate until the critic is rerun against the expanded dependency/consumer graph.

---

# 6. No premature implementation

This owner decision defines product semantics and downstream consumer obligations only.

It does NOT authorize:

- WP-19 Step 2 before the mandatory Senior gate;
- substantive runtime implementation;
- schema/template implementation unrelated to mechanically implied design synchronization;
- implementation planning;
- WP-20;
- gameplay execution or creation of a real campaign for validation.

The architecture audit must first reconcile these requirements with current owners and consumers through the normal HDM design process.
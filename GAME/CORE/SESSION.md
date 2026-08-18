# Session Lifecycle

framework_module_version: 0.3.0
load_when: new chat/session, session end, pause/resume, checkpoint creation, maintenance continuation

Use `CAMPAIGN_OPERATIONS.md` for organization and `PERSISTENCE.md` for write transport/transaction semantics.

## Session start

Follow `BOOTSTRAP_RUNTIME.md`. Do not begin by rereading old chat history.

Resolve only:
- active campaign branch and HEAD;
- manifest/mode and relevant config;
- latest checkpoint pointer when needed for recovery;
- current scene/time/location;
- PCs participating now;
- active threads/entities needed immediately;
- preloaded CORE cache.

Generate a compact recap from canonical state when useful. A recap is orientation, not new canon.

If the previous session ended in initiative or another detailed transient procedure, load the exact persisted tactical/transient state.

The pinned startup HEAD becomes `known_head_sha`. Do not fetch its tree solely for startup; tree metadata may be obtained lazily when the first campaign persistence transaction actually needs it.

## Resume after interruption

An interrupted chat does not itself advance world time. Resume from persistent state unless another session/player changed the world.

A new singleplayer chat or explicit resync refreshes HEAD and the smallest relevant working set. Multiplayer follows its synchronization policy before race-sensitive actions/publication.

## During session

Use the gameplay fast path from `RUNTIME.md`.

Once current scene state is loaded, ordinary actions should not refresh HEAD, reread unchanged records, reload CORE or publish merely because another player message arrived.

Apply consequences to the hot working set and mark durable records dirty. SOFT changes may remain dirty across turns.

Do not create session-local save rules. During play, `DURABILITY_GUARD.md` decides ordinary singleplayer boundaries; `SAVE_CONTRACT.md` handles explicit save; multiplayer/live modules handle shared synchronization. Scene/encounter/action completion alone is not automatically a boundary.

Race-sensitive multiplayer live changes follow `LIVE_SCENE.md` promptly.

After a successful own campaign save, retain the created commit/tree as known frontier and continue from the in-memory state; do not immediately fetch the branch/files back from GitHub.

## Maintenance continuation frame

Runtime refresh/update and other maintenance performed inside an active campaign chat are a temporary technical interruption, not a new session and not a reason to lose the current gameplay decision point.

Before maintenance that may switch runtime context, capture a minimal **maintenance continuation frame** in current-chat working state:
- selected campaign identity;
- last known durable campaign frontier;
- current scene/location identity already present in the working set;
- last meaningful player action or utterance relevant to the unresolved situation;
- last meaningful Master/NPC utterance or outcome relevant to that situation;
- the unresolved decision point, declaration, question or action opportunity that should return to the player.

The continuation frame is **current-chat working state**, not automatically campaign canon, not a checkpoint by itself and not a reason to create an extra Git commit.

After successful maintenance, validate/restore the selected campaign working set under the exact new runtime, preserve already-known post-maintenance state, then return to the same unresolved gameplay point. If useful, mention the maintenance result briefly, but immediately re-establish the situation and who last said/did what before handing control back to the player.

### Continuation evidence

If the **exact previous utterance** or player action is still available in **current chat context**, it may be repeated accurately.

If exact current-chat evidence is no longer available, use durable checkpoint/STATE/SCENE/LOG/event evidence to produce a **durable semantic summary** of the last known situation.

Never fabricate an exact quote, exact player action, or exact NPC wording merely to make the transition feel seamless. When durable evidence stores only meaning, present meaning as a summary rather than invented verbatim dialogue.

Maintenance does not itself advance world time, create NPC actions, consume resources or add fictional events unless an explicitly authorized campaign data migration legitimately changes those records.

## Session boundary

When an authoritative durability/session boundary occurs and state changed materially:
- publish one coherent remaining campaign transaction;
- ensure CURRENT/scene/affected entity/index/log state is mutually consistent;
- compact resolved hot state;
- create/update a checkpoint only when it improves exact recovery;
- retain only active threads and useful next-horizon prep.

## Checkpoints are sparse recovery frontiers

Do NOT create a checkpoint after each event, turn, or ordinary save.

Typical checkpoint reasons:
- session end/pause when exact resume benefits;
- major transition;
- complex combat/procedure stopped mid-state;
- before/after risky migration or repair as defined by maintenance procedure;
- another explicit recovery boundary.

If ordinary LOG/SCENE/CURRENT/entity state is sufficient to resume, save those records without manufacturing a checkpoint.

## Lifecycle on stop/pause

If unfinished pre-live onboarding is stopped, preserve it as `initializing`; do not mark `paused` merely because the user stopped chatting. `paused` is for an already PLAY_READY campaign intentionally paused after normal play began.

## Ending in combat or complex state

Prefer a clean stopping point when it arises naturally, but never manipulate player choices to reach one.

If play stops mid-procedure, persist enough exact transient state to resume: turn/order, important geometry, HP/conditions/resources, ongoing effects/durations and unresolved declarations. This boundary may justify a checkpoint.

## Session journal

Persistent session/log records are compact operational/semantic history, not transcripts or Git transaction journals.

## Feedback/preferences

Campaign-specific tone, boundaries and house-rule preferences belong in campaign configuration when cross-session persistence is needed. Never store campaign canon/preferences in ChatGPT Memory.

## Maintenance boundary

Framework upgrades, schema migrations, canon repairs and large compactions should happen outside an unresolved turn when practical. If maintenance must occur while an unresolved point is active, preserve the maintenance continuation frame and return to that point afterward. Risky maintenance may justify a checkpoint, but ordinary maintenance opportunity does not automatically require one.

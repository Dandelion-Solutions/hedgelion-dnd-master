# Session Lifecycle

framework_module_version: 0.2.0
load_when: new chat/session, session end, pause/resume, checkpoint creation

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

Persistence boundaries include meaningful action-sequence completion, scene/encounter transitions, significant durable ownership/resource/thread changes, explicit save, pause/end, risky context transition, or dirty state becoming recovery-sensitive.

Race-sensitive multiplayer live changes follow `LIVE_SCENE.md` promptly.

After a successful own campaign save, retain the created commit/tree as known frontier and continue from the in-memory state; do not immediately fetch the branch/files back from GitHub.

## Session boundary

When a natural boundary occurs and state changed materially:
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

## Ending in combat or complex state

Prefer a clean stopping point when it arises naturally, but never manipulate player choices to reach one.

If play stops mid-procedure, persist enough exact transient state to resume: turn/order, important geometry, HP/conditions/resources, ongoing effects/durations and unresolved declarations. This boundary may justify a checkpoint.

## Session journal

Persistent session/log records are compact operational/semantic history, not transcripts or Git transaction journals.

## Feedback/preferences

Campaign-specific tone, boundaries and house-rule preferences belong in campaign configuration when cross-session persistence is needed. Never store campaign canon/preferences in ChatGPT Memory.

## Maintenance boundary

Framework upgrades, schema migrations, canon repairs and large compactions should happen outside an unresolved turn when practical. Risky maintenance may justify a checkpoint, but ordinary maintenance opportunity does not automatically require one.
# Session Lifecycle

framework_module_version: 0.1.0
load_when: new chat/session, session end, pause/resume, checkpoint creation

Use `CAMPAIGN_OPERATIONS.md` for the full organization policy.

## Session start

Follow `BOOTSTRAP_RUNTIME.md`. Do not begin by rereading old chat history.

Resolve only:
- active campaign branch and HEAD;
- manifest/mode and relevant config;
- latest checkpoint pointer;
- current scene/time/location;
- PCs participating now;
- active threads/entities needed immediately;
- mandatory `RUNTIME.md` + `AI_REASONING.md`;
- situational CORE modules.

Generate a compact recap from canonical state when useful. A recap is orientation, not a new source of canon.

If the previous session ended in initiative or another detailed transient procedure, load the exact persisted tactical/transient state.

## Resume after interruption

An interrupted chat does not itself advance world time. Resume from persistent state unless another session/player changed the world.

In singleplayer, a new chat or explicit resync refreshes HEAD and relevant working state.

In multiplayer, apply the multiplayer synchronization policy before race-sensitive actions or publication.

## During session

Do not create commits/checkpoints after every action.

Track durable deltas in working state and publish batches on natural boundaries: scene/combat end, significant travel/ownership/resource changes, explicit save, pause/end, risky context transition, or when unsaved state becomes too large to safely keep only in context.

Race-sensitive shared changes in multiplayer should be published promptly after the logical action completes.

Compact hot state as processes resolve. Historical detail belongs in LOG/WORLD, not CURRENT.

## Session boundary

When a natural boundary occurs and state changed materially:
- persist the current batch;
- ensure CURRENT and affected entity records match canon;
- update semantic event history at useful granularity;
- create/update checkpoint when exact recovery value justifies it;
- retain only active threads and next-horizon preparation.

A checkpoint is a recovery frontier, not a copy of the world.

## Ending in combat or complex state

Prefer a clean stopping point when it arises naturally, but never manipulate player choices just to reach one.

If play stops mid-procedure, persist enough exact transient state to resume: turn/order, important geometry, HP/conditions/resources, ongoing effects/durations and unresolved declarations.

## Session journal

The persistent session record should be compact enough to recover operational continuity: session identity, relevant incoming events, unexpected durable changes and unresolved matters.

Do not store full literary transcripts merely because a session ended.

## Feedback/preferences

Campaign-specific tone, boundaries and house-rule preferences belong in campaign configuration when they need cross-session persistence. Never store campaign canon/preferences in ChatGPT Memory.

## Maintenance boundary

Framework upgrades, schema migrations, branch rebases, canon repairs and large compactions should happen outside an unresolved turn when possible. Create a checkpoint before risky campaign maintenance.

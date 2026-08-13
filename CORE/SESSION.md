# Session Lifecycle

framework_module_version: 0.1-development
load_when: new chat/session, session end, pause/resume, checkpoint creation

## Session start

Follow `BOOTSTRAP_RUNTIME.md`. Do not begin by rereading old chat history.

Resolve:
- active campaign branch and HEAD;
- campaign manifest/mode;
- latest checkpoint pointer;
- current scene/time/location;
- PCs participating in this session;
- only active threads/entities needed immediately;
- mandatory runtime plus situational CORE modules.

If the previous session ended in initiative or another detailed transient state, load the exact persisted tactical/transient record before continuing.

## Resume after interruption

An interrupted chat does not itself advance world time. Resume from canonical persistent state unless another session/player has changed the world.

In singleplayer, explicit resync or a new chat invalidates assumptions that existed only in old conversation context.

In multiplayer, synchronize HEAD before any persistent transition.

## During session

Do not create a checkpoint after every action. Persist durable transitions as event commits and keep hot state current.

Periodically compact hot state by removing resolved/stale data that is already represented in WORLD/LOG.

## Session boundaries

When a natural session boundary occurs, persist a checkpoint if state changed materially. A checkpoint should make a fresh chat able to resume without reading the whole session transcript.

Checkpoint creation must not duplicate full WORLD/history. It identifies the recovery frontier and compact active state.

## Ending in combat or complex state

Prefer ending outside complex round-by-round resolution when convenient, but do not manipulate player decisions merely to reach a neat stopping point.

If play stops mid-combat or mid-procedure, persist enough transient state to resume exactly:
- order/turn;
- positions/important geometry;
- HP/conditions/resources;
- ongoing effects/durations;
- unresolved declarations if any.

## Session summary

A user-facing recap may be generated on request or when useful, but the recap is not canonical storage. Canon comes from structured state + event log.

Do not store literary summaries merely because a session ended if they add no retrieval value.

## Feedback and preferences

Gameplay preferences that are specific to the campaign may be stored explicitly in campaign configuration if the user wants them applied across sessions.

Do not put campaign-specific preferences into ChatGPT Memory.

General user preferences outside campaign canon are outside this framework's storage responsibility.

## Maintenance boundary

Framework upgrades, schema migrations, branch rebases, canon repairs and large compactions should happen outside an active unresolved turn when possible. Create a checkpoint before risky maintenance.

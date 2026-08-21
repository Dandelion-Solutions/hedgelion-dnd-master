# TODO — Multiplayer live-branch test

Deferred until two independent player sessions are available.

Manual smoke test should cover shared-scene consistency, stale live HEAD, simultaneous updates, scene split/rejoin, epoch closing, disconnect/retry, live-to-campaign compaction, late join, private knowledge, and recovery from live/durable disagreement.

Performance targets: unchanged sync uses HEAD/ref only; changed live HEAD refreshes only relevant records; no full pull/history scan during gameplay; measure perceived latency across repeated shared-scene turns.

# HDM Infrastructure Topology Options — Source-Neutral Research Snapshot

**Status:** RESEARCH INPUT — NON-NORMATIVE / NOT CANONICAL  
**Date:** 2026-08-22  
**Sanitized:** 2026-09-08 under the public research-provenance boundary.

This file preserves HDM-native topology constraints, alternatives, risks and revisit triggers. It intentionally does not preserve platform-research source trails or comparative-development provenance. Current accepted R2.3/R2.4/R2.6 owners and the current roadmap control architecture.

## 1. Hard product constraints retained

1. Baseline gameplay targets an ordinary individual consumer AI subscription rather than organization-only deployment.
2. Normal baseline gameplay must not depend on marginal per-turn inference charges or separately purchased inference/agent credits.
3. Optional enhanced profiles may cost more, but baseline correctness/playability may not depend on them.
4. Each human player may have a separate host/chat/session/history; a shared multi-user AI chat is not assumed.
5. HDM logical roles are responsibility/context/authority contracts. Logical role count does not imply equal physical model-call count.
6. A narrower-context role must not execute inside a physical model invocation that still contains source material ineligible for that role.
7. Prompt-only role switching is not by itself a context reset.
8. If a deployment introduces an HDM-owned persistent service/database, that store can become its natural shared runtime substrate; GitHub need not remain latency-critical shared authority for that different deployment profile.

## 2. Cross-cutting split: deterministic core versus inference boundary

A hosted deterministic core can in principle own campaign state, mechanics, identity, Context Runtime support, retrieval/indexes, recovery, multiplayer serialization, chronology, disclosure, background non-LLM work and observability.

The difficult independent boundary is whether the player's already-funded host can provide every required physical inference/context isolation edge with acceptable quota, latency, tool access, failure semantics and no forbidden marginal-cost assumption.

Architecture must therefore evaluate **technical fit** and **baseline economic eligibility** separately.

## 3. Option families retained

### Option 1 — Distributed consumer host + Git-backed shared authority

Shape: each player uses a consumer host; shared campaign authority remains Git-backed; deterministic runtime work executes in the supported local/tool environment.

Strengths:

- smallest infrastructure footprint;
- no central HDM service required;
- portable/versioned campaign state;
- current accepted Git publication/currentness architecture remains directly applicable.

Risks/revisit triggers:

- strict physical role isolation may be unavailable in one conversation;
- Git-backed live state carries explicit currentness/race/ambiguity cost;
- host connector/tool/background capabilities are deployment dependencies;
- measure realistic repository round-trip latency and multiplayer race behavior.

### Option 2 — Hosted deterministic core + ordinary consumer chat

Shape: HDM server/database owns shared state and deterministic core; player-facing inference remains in the ordinary consumer host.

Strengths:

- normal transactional state/concurrency/retrieval/observability become server-local engineering concerns;
- GitHub can become optional export/backup/history rather than live authority for this profile;
- inference remains with the player's consumer host.

Dominant risk:

- a server can choose which role/context should execute but cannot by itself force the consumer host to create a genuinely fresh isolated model context.

Revisit when a product decision considers a hosted state/core profile or when measured same-context isolation becomes inadequate.

### Option 3 — Hosted deterministic core + host-native isolated child execution

Shape: server owns an opaque role job and exact role-eligible context; host owns creation of a separate child invocation; child fetches/returns only the typed job material it is authorized to see.

Potential advantages:

- physical separation for incompatible privilege domains;
- server-owned source eligibility and typed result validation;
- player-facing parent context can remain recipient-safe if inheritance/handoff are controlled;
- inference may remain covered by the player's ordinary subscription when the host actually provides sufficient included capacity.

Hard probes before eligibility:

1. child context inheritance must be understood and controllable enough for the role boundary;
2. child-to-parent handoff must not leak secret-bearing material;
3. child must have the required authenticated/role-scoped tool access;
4. retries/failure/cancellation must be observable enough for idempotent role-job semantics;
5. realistic multi-hour usage must fit the baseline economic constraint with extra billing disabled.

Existence of a child-agent feature alone does not prove this option satisfies HDM isolation or economics.

### Option 4 — Fully controlled HDM service + directly controlled inference

Shape: HDM owns state, deterministic core, role scheduler, exact context and physical model invocation.

Strengths:

- strongest control over isolation, model selection, retries, validation, observability and background execution.

Baseline blocker:

- any deployment that requires project-paid or player-paid marginal commercial inference for normal turns violates the retained baseline economic constraint.

This option remains a useful technical control architecture and a future candidate if inference economics or deployment assumptions materially change.

## 4. Decision-relevant conclusions retained

- Introducing a persistent server changes the storage question; Git-backed authority is not automatically required for that profile.
- The minimum number of physical privilege domains should be derived before judging platform viability; six logical roles do not imply six calls.
- Noncritical projection/catch-up roles should remain degradable where current owners allow it.
- A technically capable agent surface that cannot satisfy baseline economic/endurance constraints is not baseline-eligible.
- A server-backed profile does not by itself solve physical LLM context isolation.

## 5. Revalidation agenda

Revisit topology only when a current owner/roadmap activates one of these triggers:

- derive/revise the minimum physical role compatibility/privilege matrix;
- material host capability changes affecting fresh isolated invocation, inheritance, tool access or parent handoff;
- measured quota/endurance or latency makes the current profile insufficient;
- a hosted HDM state/core profile becomes a product candidate;
- inference economics change enough to alter baseline eligibility;
- current Git-backed deployment no longer satisfies required correctness/performance constraints.

Any future platform capability claim must be re-established with current evidence at that time. This research snapshot is not capability authority.

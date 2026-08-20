# Step 5.5 — SOFT / HARD / SAVE Durability Semantics — Canonical Specification

Status: **CANONICAL — STEP 5.5 ARCHITECTURE CLOSED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Owner-approved architecture:

> **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**

Canonicalization basis:

- `2026-08-20-step-5-5-soft-hard-save-durability-task-brief.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-research-draft.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-analytical-challenge.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-owner-clarification-addendum.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-decision-brief.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-candidate-spec.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-adversarial-review.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-resolution-gate.md`

This specification is the current Step-5.5 authority. It defines logical durability semantics only. Physical Git publication/crash consistency remains Step 5.6; checkpoint/source-selection representation remains 5.7; concrete multiplayer/live authority and publication bindings remain 5.8.

---

# 1. Canonical model

Durability is represented conceptually on three independent axes:

```text
SEMANTIC SURVIVAL
    EPHEMERAL | ESTABLISHED

CURRENT DURABILITY
    DURABLE | VOLATILE_DIRTY

CURRENT OBLIGATION
    MAY_DEFER
    MUST_BE_DURABLE_BEFORE(edge)
```

Operational shorthand:

```text
SOFT
    = ESTABLISHED
      + VOLATILE_DIRTY
      + MAY_DEFER

HARD
    = an active correctness-critical
      MUST_BE_DURABLE_BEFORE(edge) obligation
```

`SOFT` and `HARD` are not permanent intrinsic classes of gameplay facts.

The same established fact may remain SOFT for a long period and later join a mandatory durability closure because a save, handoff, shared visibility/ownership edge, recovery dependency, or another authoritative domain policy requires it.

A local/private risk-control flush requested because unpublished SOFT has remained exposed for too long is not automatically HARD; publication failure may degrade loss protection while coherent HOT state remains usable.

---

# 2. Canonical laws

## LAW 5.5-1 — ESTABLISHMENT IS OWNER-CONTRACT-RELATIVE

A value is `ESTABLISHED` only after it crosses the semantic acceptance/commit edge defined by its native owner/domain contract.

Merely computing a candidate/prospective mutation in memory does not establish current truth.

Consequences:

- ordinary singleplayer execution may establish coherent HOT current truth before campaign durability;
- a prospective execution candidate rejected before its owning commit edge is not established;
- an active live/shared contract may make successful live publication/CAS part of the edge by which shared state becomes established for other participants/reveal;
- transport durability does not retroactively decide whether a previously established local semantic result occurred unless the owning domain explicitly includes publication in its establishment edge.

## LAW 5.5-2 — SOFT IS ESTABLISHED DEFERRABLE DIRTY STATE

`SOFT` means gameplay-significant state that:

1. is established under its native owner contract;
2. is not yet durable through the required native durable source set; and
3. is currently permitted to defer publication by the applicable durability policy.

SOFT is not:

- speculative/untrusted content;
- a lower-authority kind of canon;
- merely derived/cache state;
- “not true until saved.”

If SOFT is lost through total host/process/context loss before publication, recovery returns to actual durable native sources under Step 5.2 and SHALL NOT invent the lost progress.

## LAW 5.5-3 — HARD IS AN EDGE-BOUND DURABILITY OBLIGATION

`HARD` is shorthand for:

```text
MUST_BE_DURABLE_BEFORE(edge)
```

The owning domain/policy SHALL identify the semantic edge whose successful crossing or acknowledgement requires durability.

Examples include, when their owning contracts say so:

- recovery-safe handoff before relinquishment;
- shared/live mutation before shared reveal/use;
- activation/readiness edge requiring a durable playable point;
- ownership/visibility transfer whose correctness depends on durable publication.

Step 5.5 introduces no universal persisted `hard=true` state, permanent HARD fact category, or campaign-global HARD queue.

## LAW 5.5-4 — DURABILITY POLICY IS SCOPE-OWNED

Deferral, dirty accumulation, unpublished-exposure protection and correctness-critical barrier edges belong to an explicit durability/authority/visibility scope or partition.

Conceptually:

```text
DurabilityPolicy(scope) {
    accumulation_scope
    barrier_edges
    unpublished_exposure_policy
    publication_authority
}
```

This is a logical contract, not a mandatory serialized class/schema.

There is no architecture-wide requirement for:

- one campaign-global dirty timeout;
- one scalar durability frontier;
- one publication cadence across independently writable scopes;
- one global save owner.

A policy SHALL NOT aggregate independently writable/owned scopes merely for implementation convenience when that aggregation would create false synchronization or duplicate authority.

A conservative aggregate singleplayer/local partition is allowed where one effective authority/writer can make that aggregation coherent.

## LAW 5.5-5 — REQUIRED DURABLE SOURCE CLOSURE AND PENDING WRITE SET ARE DISTINCT

A durability promise is proven over a **required durable source closure**:

```text
REQUIRED DURABLE SOURCE CLOSURE
    = all native owners, dependencies, routing/revision/interpretation evidence
      required for the promised recoverable point
```

The **pending write set** is only the subset of that closure that is not yet sufficiently durable/current and therefore must actually be published.

Already durable compatible dependencies participate in the closure proof without requiring rewrite.

Durability closure SHALL NOT be equated with a list of dirty files.

## LAW 5.5-6 — CLOSURE ROOTS COME FROM POLICY + ACCUMULATION SCOPE

For durability request `D`, construct logical roots as:

```text
ROOTS(D) =
    POLICY_ROOTS(D)
    UNION POLICY_DIRTY_ACCUMULATION_SCOPE(D)
```

Then take transitive required recovery/reference/interpretation closure.

Policy roots identify the state directly promised/protected by the boundary.

Accumulation scope represents additional established dirty progress the owning policy intentionally promises to protect at that boundary even when it is not a direct dependency of the trigger.

This distinction permits ordinary singleplayer boundaries to protect accumulated local progress while narrow multiplayer/live/access boundaries avoid flushing unrelated private/local scopes.

## LAW 5.5-7 — TRANSITIVE REQUIRED RECOVERY CLOSURE IS SEMANTICALLY BOUNDED

For every root, include any native dependency whose omission would make the promised durable point incorrect, uninterpretable, unresumable, or invalid under directly touched integrity constraints.

As applicable this includes:

- native authoritative current-state owners;
- newly referenced identities and required indexes;
- Step-5.2 typed recovery routing/root enrollment;
- open RuntimeCommand/Resolution/Procedure/Continuation state;
- mandatory child/firing/receipt continuity evidence;
- fixed accepted RNG required by unfinished execution;
- Step-5.3 source/occurrence/claim/execution relationships;
- irreducible accepted player-input/message evidence while no sufficient typed semantic replacement exists;
- compatible accepted runtime/catalog/rules interpretation context;
- directly required provenance/revision evidence;
- owning-scope references needed to resolve active live/native authority.

Closure SHALL NOT recursively materialize:

- arbitrary world-graph references;
- every loaded record;
- Temporal Agenda;
- MechanicalContext;
- condition/effect aggregation caches;
- dependency DAG/query/loaded-record caches;
- model hidden reasoning/context;
- speculative future action trees;
- generic Story/render buffers;
- full transcript merely for continuity convenience.

## LAW 5.5-8 — NORMAL SINGLEPLAYER MAY FLUSH ACCUMULATED LOCAL SOFT

For the ordinary singleplayer/local durability partition, a natural forced durability boundary MAY intentionally include all accumulated established dirty state in that partition before taking required dependency closure.

This preserves the product expectation that a natural local save boundary protects accumulated play rather than only the literal trigger record.

It does not authorize campaign-global flushing across independent multiplayer/live authority scopes.

## LAW 5.5-9 — EXPLICIT SAVE HAS A STRONG PLAYER-VISIBLE PROMISE

An unambiguous player request such as:

```text
save
save game
сохрани игру
```

means:

> On successful acknowledgement, every established gameplay-significant dirty root in the selected save scope, plus every required recovery/reference/interpretation dependency needed to resume that state honestly, is actually durable through a compatible composed set of native durable sources.

Explicit save SHALL NOT be satisfied by:

- a prose save note/summary replacing structured owners;
- a checkpoint that omits required current native state;
- silently leaving known established dirty roots volatile inside the promised save scope;
- merely preparing/attempting a write whose durable outcome is not established.

Explicit save by itself SHALL NOT:

- pause/end the campaign;
- activate an unready campaign;
- invent unresolved mechanics or missing structured facts;
- force a checkpoint solely because the word save was used;
- make noncanonical Story/transcript projections current-state authority;
- require arbitrary projections/transcript material to be synchronously refreshed.

Specific exact message/provenance evidence remains in closure only while it is irreducible for accepted semantic recovery under Steps 5.2/5.4.

## LAW 5.5-10 — EXPLICIT SAVE MAY COMPOSE MULTIPLE NATIVE DURABILITY DOMAINS

Successful explicit save is a property over a **compatible composed set of required domain-native durable sources**.

It does not imply:

- one global repository transaction;
- one campaign-wide commit;
- one cross-domain total order;
- one scalar save frontier;
- one distributed transaction spanning campaign/live/runtime domains.

Each participating native domain follows its own ownership/publication/atomicity contract.

The selected resulting source composition must satisfy the promised Step-5.2 Resumable Runtime Closure.

Physical cross-source publication/recovery sequencing remains Step 5.6–5.8.

## LAW 5.5-11 — EXPLICIT SAVE USES SCOPED QUIESCENCE WHILE IN FLIGHT

Once explicit save intent is accepted, the selected save root set and affected mutation scope SHALL remain stable enough that the save acknowledgement has one definite meaning.

Dependent gameplay mutation inside that save scope SHALL NOT silently race past or become ambiguously included in the in-flight save attempt.

OOC/control communication and truly independent scopes may continue where safe.

This is not a durable global lock, campaign-global host lease, or new state owner.

## LAW 5.5-12 — SAVE SUCCESS REQUIRES ACTUAL DURABILITY

The engine SHALL NOT say or imply `saved` until the required composed native durable source closure actually satisfies the save promise.

Intent to publish, an in-memory marker, a prepared tree/commit, or a request that may or may not have reached durable authority is insufficient.

Physical ambiguous-write determination is owned by Step 5.6/5.8.

## LAW 5.5-13 — ALREADY-DURABLE CLEAN SAVE NEEDS NO HEARTBEAT WRITE

If the explicit-save postcondition already holds and the selected save scope has no pending dirty material requiring publication, the request may succeed with zero gameplay write.

Conceptually:

```text
known compatible durable source closure already satisfies SAVE
    -> acknowledge saved
    -> no new commit/checkpoint/heartbeat required
```

An explicit save requests a durability guarantee, not a new commit object for its own sake.

## LAW 5.5-14 — FAILED EXPLICIT SAVE DOES NOT HARD-LOCK COHERENT LOCAL/PRIVATE PLAY

If an explicit save attempt fails while a coherent current HOT source composition survives or can be re-established:

- SHALL NOT say or imply saved;
- SHALL preserve established dirty HOT state where valid;
- SHOULD report the failure briefly and honestly;
- SHOULD offer retry/repair where useful;
- MAY accept later ordinary local/private gameplay if the player proceeds;
- SHALL NOT require a ritualized separate “continue without saving” confirmation when subsequent gameplay intent already makes that choice clear;
- SHALL retain increased unpublished-loss exposure;
- SHALL retry later under applicable policy;
- SHALL recover only actual durable compatible state if HOT state is later lost.

This permission is subordinate to every independently active correctness-critical `MUST_BE_DURABLE_BEFORE(edge)` obligation.

## LAW 5.5-15 — PARTIAL NATIVE PUBLICATION IS REAL EVEN WHEN OVERALL SAVE FAILS

If a save requires native durability domains A and B and A successfully publishes while B fails:

- overall explicit save is not confirmed/successful;
- A's successful native publication remains real durable authority;
- the runtime SHALL NOT pretend the older A revision remains current merely to simplify retry;
- before dependent continuation, the runtime must adopt/revalidate a coherent current composed source set under native ownership rules;
- if a required source remains unresolved/suspect, only the dependent scope is gated under existing correctness/integrity rules.

Step 5.5 does not define physical ambiguous-ack detection or ref/commit mechanics.

## LAW 5.5-16 — CORRECTNESS-CRITICAL DURABILITY EDGE CANNOT BE FALSELY CROSSED

If durability is part of semantic postcondition `E`, failure to establish its required closure means `E` remains incomplete/failed for the affected scope.

The runtime SHALL NOT, for example:

- reveal a shared/live result whose owning contract requires write-before-reveal before the required write succeeds;
- acknowledge recovery-safe handoff before the promised closure is durable;
- advertise successful ownership/visibility/activation transition when its contract requires prior durability.

Only the named edge/dependent scope is gated. OOC communication and independent scopes remain available where safe.

## LAW 5.5-17 — RISK-CONTROL EXPOSURE IS NOT A CORRECTNESS BARRIER

For deferrable local/private state, configured maximum intended unpublished exposure is a risk-control/RPO/SLO policy.

When its condition is met at a suitable runtime opportunity:

```text
request durability closure
```

If publication fails while coherent HOT state survives:

- the desired protection is degraded/not satisfied;
- local/private play MAY continue;
- later suitable retry is expected;
- failure does not by itself make established state semantically invalid.

Shared/live ownership policy may impose stronger non-deferrable event-driven edges under Step 5.8.

## LAW 5.5-18 — EXPOSURE IS SCOPE/PARTITION-RELATIVE

Unpublished exposure belongs to the applicable durability-policy scope/partition, not one campaign-global clock and not necessarily one clock per physical record.

A valid aggregate partition is allowed when it matches actual authority/publication semantics.

Independent writable/visibility scopes may have independent exposure policies.

## LAW 5.5-19 — EXPOSURE STARTS FROM ACTUAL UNPUBLISHED STATE

Exposure SHALL be measured from actual established/recovery-relevant state becoming unpublished in the relevant policy partition, not solely from the age of the latest repository commit/durable frontier.

Consequences:

- a newly dirty fact created long after the previous commit does not inherit the whole age of that commit;
- unrelated successful publication does not falsely reset another still-dirty partition;
- after partial publication, exposure remains/recomputes for still-relevant unpublished state.

The current hard-coded `durable_frontier_time`/`one hour` implementation contract is therefore not canonical architecture.

## LAW 5.5-20 — EXPOSURE TRACKS OLDEST STILL-RELEVANT UNPUBLISHED STATE

Exposure policy concerns the oldest still-relevant established/recovery state that remains unpublished in the partition.

A dirty intermediate value that is lawfully superseded and no longer required by:

- current native truth;
- accepted execution continuity;
- recovery;
- required provenance/audit;
- another closure dependency

need not keep exposure age alive merely because it existed historically.

Per-delta historical clocks are not required when a correct aggregate representation exists.

## LAW 5.5-21 — NO BACKGROUND EXECUTION MEANS NO EXACT WALL-CLOCK FLUSH GUARANTEE

If the host offers no background timer/callback/execution opportunity, HDM cannot promise publication at the exact instant an exposure threshold is crossed.

The policy may evaluate/request a flush at the next suitable runtime opportunity before needlessly extending exposure.

Host wall-clock passage alone does not advance fictional time or create gameplay events.

## LAW 5.5-22 — CLEAN STATE NEVER CREATES HEARTBEAT PUBLICATION

If a policy scope contains no established dirty/recovery-relevant state requiring publication, elapsed time, chat age, session age, or advisory capacity risk SHALL NOT cause an empty/no-op gameplay publication merely to refresh a durability timestamp.

## LAW 5.5-23 — RISK/ADVISORY FLUSHES USE SAFE ESTABLISHED-STATE POINTS

A risk-control exposure policy or advisory host-capacity heuristic may request opportunistic publication only at a point where:

- selected roots are established under their owners;
- the selected closure can be frozen/revalidated coherently;
- the attempt does not cut through an unresolved native atomic/semantic edge.

Such a flush SHALL NOT persist partial model reasoning or speculative prospective deltas as gameplay authority.

Reliable destructive lifecycle signals remain Step-5.4 controlled-handoff inputs.

## LAW 5.5-24 — ADVISORY HOST CAPACITY IS NOT DURABILITY AUTHORITY

Approximate message/token/chat-age/capacity signals or locally derived heuristics MAY:

- warn the player;
- recommend proactive handoff;
- request opportunistic SOFT publication at a safe point.

They SHALL NOT by themselves create a correctness-critical HARD edge under current host contracts.

False positives must remain safe; false negatives fall back to ordinary durability + unexpected-loss recovery.

## LAW 5.5-25 — SHARED/LIVE POLICIES MAY BE STRICTER THAN SINGLEPLAYER/PRIVATE

Step 5.5 fixes only the generic scope-policy architecture.

Expected policy profiles are:

```text
SINGLEPLAYER / PRIVATE-LOCAL
    established SOFT may accumulate for long periods
    primary unpublished risk = host/context loss
    risk-control publication may be comparatively infrequent

MULTIPLAYER SHARED OUTSIDE ACTIVE LIVE
    stronger event/visibility/ownership-driven publication expected

SAME-SCENE ACTIVE LIVE
    logical shared mutation
        -> live publication/CAS
        -> then shared reveal/use
```

Participation in multiplayer does not automatically force every private/local mutation to publish synchronously.

A previously private/local fact may acquire a stronger durability obligation when it crosses an ownership/visibility/causal boundary and becomes required by another participant/shared state.

Concrete bindings remain Step 5.8.

## LAW 5.5-26 — CHECKPOINT IS OPTIONAL RECOVERY AID, NOT SAVE AUTHORITY

A save/durability closure may create or update a checkpoint only when independent checkpoint/recovery policy says it materially improves recovery.

Checkpoint does not become current-state authority and cannot substitute for required native durable state.

Exact checkpoint/source-selection semantics remain 5.7.

## LAW 5.5-27 — STORY/TRANSCRIPT PROJECTION FRESHNESS IS SEPARATE

Canonical gameplay durability does not automatically require all noncanonical Story/transcript/render projections to be current at every save/boundary.

Steps 5.10–5.12 own projection durability, transcript retention and host delivery.

Exception: specific exact wording/provenance that is still irreducible evidence for accepted unresolved semantics belongs to recovery closure until typed semantic state replaces it.

## LAW 5.5-28 — DURABILITY BOOKKEEPING IS NOT GAMEPLAY AUTHORITY

Dirty markers, exposure timestamps, policy state, save attempt state, commit/ref metadata and other durability bookkeeping SHALL NOT become duplicate semantic owners.

Native world/runtime/live owners remain current-state authority.

## LAW 5.5-29 — PUBLICATION FAILURE DOES NOT INVENT GAMEPLAY ROLLBACK

Logical failure disposition depends on boundary class:

```text
RISK-CONTROL / FAILED EXPLICIT SAVE
    -> established coherent HOT state may remain usable
    -> durability promise/protection is not satisfied

CORRECTNESS-CRITICAL EDGE
    -> named edge remains incomplete/failed
    -> only dependent continuation is gated
```

Step 5.5 defines no Git-level rollback, force-update, ambiguous acknowledgement, prepared-object handling or physical retry sequence.

---

# 3. Durability closure construction

## 3.1 Required durable source closure

For one promise `D`:

```text
1. identify policy roots
2. add policy-owned accumulated dirty roots
3. expand transitive required semantic/recovery dependencies
4. resolve compatible domain-native source identities/revisions
5. derive pending write set only for material not already sufficiently durable
6. publish according to owning domain(s)
7. acknowledge success only after the required compatible durable source closure actually holds
```

The closure is a correctness property/source-set relation, not a mandatory first-class record.

## 3.2 Root examples

### Explicit save

All established dirty roots in selected save scope.

### Ordinary singleplayer forced boundary

The policy-selected accumulated local dirty partition.

### Controlled handoff

Every current state/accepted execution/evidence promised across the handed-off scope under Step 5.4.

### Shared/live visibility edge

The shared mutation plus policy-defined prerequisites/dependencies required by the owning multiplayer/live contract.

### Risk-control flush

Current accumulated dirty roots in the affected local/private policy partition.

## 3.3 Required dependencies already durable

A dependency may participate in closure without receiving a new write when its current compatible durable representation already satisfies recovery/interpretation needs.

## 3.4 Scope boundaries

Closure expansion follows semantic dependency, not arbitrary physical proximity or campaign-wide traversal.

A required reference into another native domain uses that domain's owning durable source/compatibility relation; it does not merge writable authority.

---

# 4. Explicit save semantics

## 4.1 Save request

Conceptual flow:

```text
ATTACHED / PLAYING
    -> explicit SAVE accepted
    -> freeze selected save root set / affected mutation scope
    -> construct required durable source closure
    -> derive pending write set(s)
    -> attempt native publication(s)
```

## 4.2 Save success

Success means the requested compatible native durable source closure exists.

Then:

- player may be told the game is saved;
- included dirty state is cleared/adopted according to actual native publication outcome;
- host remains attached;
- no pause/end/activation is implied.

If required state was already durably recoverable, success may require zero publication.

## 4.3 Save failure with coherent HOT state

If save is not confirmed:

- do not say saved;
- keep/re-establish coherent current HOT composition;
- communicate the minimal useful failure/risk;
- retry when useful;
- later local/private gameplay may continue if the player proceeds;
- do not require explicit risk ritual when the next gameplay intent already signals continuation.

If some native source was actually published, adopt/revalidate that real authority rather than pretending it did not happen.

## 4.4 Save and stop

`save and stop` composes two intents:

1. explicit save promise;
2. lifecycle/session stop/pause intent under applicable lifecycle rules.

The system SHALL NOT falsely represent a failed save as durably protecting the stop point.

Unfinished onboarding retains its own lifecycle semantics; save does not turn `initializing` into `paused` or `active` without independent readiness/lifecycle authority.

---

# 5. Controlled handoff relation

Explicit save and Step-5.4 controlled handoff share recovery-closure machinery but have different postconditions.

```text
SAVE
    roots = all established dirty roots in selected save scope
    success = requested durable recovery closure exists
    host remains attached

CONTROLLED HANDOFF
    roots = all state promised across handed-off scope
    success = recovery-safe durable closure exists
              AND old host may relinquish that scope
```

A failed save may permit continued coherent local/private play.

A failed handoff cannot be acknowledged as recovery-safe relinquishment.

---

# 6. Exposure policy semantics

## 6.1 Purpose

Local/private exposure policy bounds intended loss risk from long-lived unpublished SOFT when ordinary semantic boundaries are sparse.

It does not provide a hard semantic expiration time for HOT truth.

## 6.2 Start

Exposure begins when a previously clean durability-policy partition first contains still-relevant established/recovery state not covered by the required durable source set.

## 6.3 Successful publication

After successful publication:

- if the partition is fully clean, exposure clears;
- if unpublished relevant state remains, exposure remains/recomputes for that state;
- unrelated publication cannot reset another dirty partition.

## 6.4 Failure

Failure while coherent HOT local/private state survives:

- leaves protection degraded;
- does not satisfy the configured exposure target;
- may be retried at later suitable opportunities;
- does not hard-lock local/private play by itself.

Notification/retry cadence need not repeat every turn. UX/backoff policy is later implementation detail, provided degraded protection is not silently represented as healthy.

## 6.5 No exact background guarantee

Without host execution opportunity there is no promised exact-time flush.

## 6.6 Numeric value

Step 5.5 selects **no universal numerical threshold**.

The current runtime/test hard-coded `one hour` rule is noncanonical pre-5.5 policy/debt and must be replaced, parameterized, or consciously reselected during later machine/product realization.

---

# 7. Failure disposition matrix

| Situation | Durable/semantic result | Allowed continuation | Forbidden claim/edge |
|---|---|---|---|
| explicit save fails, coherent HOT composition survives | requested save not confirmed; dirty HOT remains | OOC + later local/private gameplay if player proceeds | `saved` |
| local/private risk-control flush fails | protection degraded; HOT remains established | local/private gameplay + later retry | configured risk target cannot be treated as satisfied |
| controlled handoff publication fails | handoff remains incomplete | retry or abandon handoff while old host remains attached | recovery-safe relinquishment |
| correctness-critical live/shared publication fails | owning shared edge remains uncommitted/incomplete | OOC/retry/reconcile/independent scopes | shared reveal/use that requires publication |
| one native domain succeeds, another required domain fails | successful native publication remains real; overall save fails | continue after coherent source adoption/revalidation | overall save success |
| host dies with unpublished HOT state | HOT lost | recover actual compatible durable source set | invention/reconstruction of lost unpublished progress |

---

# 8. Multiplayer/live interface requirement

Step 5.8 SHALL instantiate concrete policies consistent with these laws.

It must preserve at least:

1. private/local multiplayer state may remain deferrable when no other participant can legitimately depend on it;
2. state crossing into shared observation/ownership/authorization/conflict may acquire stronger event-driven durability obligations;
3. same-scene live shared mutation may require live write/CAS before shared reveal/use;
4. campaign durability may legitimately lag current live authority until compaction;
5. no universal campaign-global dirty timeout or global single-writer session lease is introduced merely to implement multiplayer durability.

---

# 9. Step 5.6 interface requirement

Campaign Publication & Crash Consistency must now provide physical semantics sufficient to prove/deny the logical durability promises above.

At minimum 5.6 owns:

- pinned campaign publication input/source revision;
- complete pending write-set derivation for one campaign native transaction domain;
- optimistic conflict invalidation/rebuild;
- exact success point for campaign durability;
- crash before/after tree/commit/ref phases;
- prepared/unreachable commit handling;
- ambiguous acknowledgement/ref-update determination;
- retry/idempotency semantics;
- adoption/clearing of dirty state only after actual publication outcome;
- behavior when a save attempt spans campaign plus other native durability domains without inventing distributed atomicity.

Step 5.6 SHALL NOT redefine the player meaning of explicit save or the SOFT/HARD model.

---

# 10. Step 5.7 interface requirement

Checkpoint / Recovery Protocol must select/hydrate compatible native sources that satisfy promised durable closure without turning checkpoint into current-state snapshot authority.

It must distinguish:

- source closure proof;
- pending writes;
- checkpoint/routing evidence;
- native current owner state.

---

# 11. Later projection/delivery requirements

Steps 5.10–5.12 may define lag/freshness/retention for Story/transcript/host-delivery projections.

They cannot weaken canonical gameplay durability closure or promote noncanonical projection data into current gameplay authority.

Specific exact utterance evidence remains exceptional only while required for unresolved accepted semantics.

---

# 12. Rejected architecture shapes

Step 5.5 rejects as canonical requirements:

- static intrinsic HARD/SOFT fact taxonomy;
- universal persisted HARD flag;
- global SAVE_ALL_DIRTY for every mandatory edge;
- pure trigger-only dependency publication for normal accumulated singleplayer boundaries;
- generic global durability snapshot;
- global scalar save/recovery frontier;
- campaign-global dirty timeout;
- per-file timer requirement;
- universal one-hour constant;
- mandatory heartbeat/no-op save writes;
- automatic checkpoint on every save;
- transcript/Story summary as save authority;
- background timer guarantee where host provides no execution;
- automatic hard lock of coherent singleplayer/local play after failed save/risk-control publication;
- distributed cross-domain transaction as the meaning of save.

---

# 13. Machine realization debt

Current GAME/runtime/tests predate this canonical contract in several places.

Known debt includes at minimum:

- `GAME/CORE/DURABILITY_GUARD.md` hard-coded one-hour rule;
- `GAME/CORE/RUNTIME.md`, `SESSION.md`, `PERSISTENCE.md`, `STORAGE.md` wording tied to `durable_frontier_time`/one-hour exposure;
- `DEV/TESTS/test_hourly_durability_contract.py` string-level assertions for the old one-hour contract;
- `DEV/TESTS/DURABILITY_BOUNDARY_CASES.md` wording that treats fixed timer autosave as categorically forbidden rather than distinguishing configurable scope-aware risk-control exposure from fixed global autosave;
- machine representation for scope-aware dirty/exposure bookkeeping, if any representation is needed;
- regression coverage for failed-save friendly continuation, clean already-durable save, partial multi-domain publication, and non-resetting independent exposure partitions.

This debt belongs to later integrated implementation planning after architecture sequencing; Step 5.5 closure does not itself modify GAME/schema/runtime code.

---

# 14. Canonical consequences

```text
EPHEMERAL/ESTABLISHED is separate from DURABLE/VOLATILE_DIRTY
SOFT means established dirty state whose publication may defer
HARD means MUST_BE_DURABLE_BEFORE(named edge), not an intrinsic fact class
establishment follows native owner acceptance semantics
required durable source closure is distinct from physical pending write set
durability closure = policy roots + policy accumulation roots + required semantic/recovery dependencies
ordinary singleplayer boundaries may protect accumulated local SOFT
explicit save protects every established dirty root in selected save scope + required closure
save success may compose compatible native durability domains; no global transaction implied
clean already-durable save may succeed with zero heartbeat write
failed save does not hard-lock coherent local/private play
partial native success remains real authority even when overall save fails
correctness-critical edge cannot be falsely crossed without required durability
local/private dirty exposure is scope-aware risk-control/SLO, not semantic expiry
exposure starts from actual unpublished state, not arbitrary commit age
unrelated publication cannot falsely reset another dirty partition
no exact timed flush without host execution opportunity
no universal numeric dirty threshold; existing one-hour rule is stale/noncanonical debt
advisory host-capacity heuristics may warn/opportunistically flush but are not correctness authority
shared/live policies may impose stronger event-driven durability in Step 5.8
checkpoint/Story/transcript/delivery remain separate ownership concerns
```

No Step-5.5 architecture blocker remains.

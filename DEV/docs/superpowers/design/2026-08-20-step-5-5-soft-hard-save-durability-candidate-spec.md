# Step 5.5 — SOFT / HARD / SAVE Durability Semantics — Candidate Specification

Status: **OWNER-APPROVED DESIGN DIRECTION — CANDIDATE, NOT YET CANONICAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Owner-approved direction:

> **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**

Derivation:

- `2026-08-20-step-5-5-soft-hard-save-durability-task-brief.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-research-draft.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-analytical-challenge.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-owner-clarification-addendum.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-decision-brief.md`

This candidate formalizes the approved Step-5.5 semantic architecture. It does not choose Git transport/crash protocol (5.6), checkpoint wire format/source selection (5.7), concrete multiplayer/live ownership policy (5.8), chronology persistence (5.9), Story/transcript durability (5.10–5.11), or host-delivery acknowledgement (5.12).

---

# 1. Canonical candidate model

Durability is modeled on three independent conceptual axes:

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

`HARD` is not a permanent intrinsic category of a fact. The same established fact may remain SOFT for many turns and later join a mandatory closure because a save, handoff, shared visibility/ownership edge, recovery dependency, or another authoritative policy makes durability necessary.

Risk-control publication requests such as a local/private unpublished-exposure threshold are not automatically `HARD`; their failure may degrade loss protection while coherent HOT state remains usable.

---

# 2. Candidate laws

## LAW 5.5-1 — ESTABLISHED TRUTH PRECEDES DURABILITY

A gameplay-significant fact/state transition becomes current semantic truth when its owning gameplay/runtime contract establishes it in the authoritative HOT working state, not only when storage publication later succeeds.

Durability changes recoverability/visibility guarantees; it does not retroactively decide whether an already committed local semantic result happened.

Consequences:

- a failed publication SHALL NOT silently roll back or rewrite an already established coherent HOT result;
- if that HOT result is later lost before publication, recovery returns to actual durable evidence and SHALL NOT invent the lost result;
- domain contracts such as active live shared ownership may require publication as part of the edge by which a result becomes externally usable/revealed.

## LAW 5.5-2 — SOFT IS DEFERRABLE ESTABLISHED DIRTY STATE

`SOFT` means established gameplay-significant state that is currently not durable through its required native durable representation and whose applicable durability policy still permits deferral.

SOFT does not mean:

- optional fiction;
- untrusted speculation;
- merely cached derived state;
- a lower-authority truth class;
- “not canon yet.”

If total host/process/context loss destroys SOFT, Step 5.2 no-invention rules apply.

## LAW 5.5-3 — HARD IS EDGE-BOUND, NOT FACT-BOUND

`HARD` is shorthand for a correctness-critical durability obligation:

```text
MUST_BE_DURABLE_BEFORE(edge)
```

The owning domain/policy SHALL identify the semantic edge whose successful crossing/acknowledgement requires durability.

Examples include, subject to their owning contracts:

- recovery-safe handoff before relinquishment;
- shared/live state publication before shared reveal/use;
- PLAY_READY or another activation edge whose contract explicitly requires a durable starting point;
- a future ownership/visibility transfer whose correctness depends on durable publication.

A static universal `hard=true` field or intrinsic permanent HARD class is not required or authorized by Step 5.5.

## LAW 5.5-4 — DURABILITY POLICY IS SCOPE-OWNED

Deferral, accumulation, risk-control exposure and mandatory barrier edges belong to an explicit durability/authority/visibility scope or partition.

Conceptually:

```text
DurabilityPolicy(scope) {
    accumulation_scope
    barrier_edges
    unpublished_exposure_policy
    publication_authority
}
```

This is a logical contract, not a required serialized record.

There is no architecture-wide campaign-global dirty timeout, global durability frontier, or requirement that every independently writable scope share one publication cadence.

## LAW 5.5-5 — REQUIRED DURABILITY CLOSURE HAS POLICY ROOTS PLUS REQUIRED CLOSURE

For a durability request `D`, the promised publication set SHALL be derived as:

```text
DURABILITY_CLOSURE(D) =
    POLICY_ROOTS(D)
    UNION POLICY_DIRTY_ACCUMULATION_SCOPE(D)
    then TRANSITIVE_REQUIRED_RECOVERY_CLOSURE
```

`TRANSITIVE_REQUIRED_RECOVERY_CLOSURE` includes only dependencies whose omission would make the promised durable point incorrect, uninterpretable, unresumable, or invalid under a directly touched integrity invariant.

As applicable this includes:

- native current-state owners;
- newly referenced identities and required indexes;
- typed recovery routing/enrollment required by Step 5.2;
- open RuntimeCommand/Resolution/Procedure/Continuation state;
- mandatory child/firing identity and receipts required for continuity;
- fixed accepted RNG needed by unfinished accepted execution;
- Step-5.3 source/occurrence/claim/execution relations;
- irreducible accepted input/message evidence while no sufficient typed replacement exists;
- compatible accepted runtime/catalog/rules interpretation context;
- directly required provenance/revision evidence;
- other native-owner dependencies required by the selected scope.

The closure SHALL NOT recursively materialize every loaded record, arbitrary world-graph reference, derived cache, Story projection, transcript, or unrelated dirty scope merely because it is available in memory.

## LAW 5.5-6 — ACCUMULATION SCOPE IS A PRODUCT/POLICY PROMISE

Required dependency closure and policy accumulation are distinct reasons for inclusion.

For ordinary singleplayer/local durability boundaries, the policy MAY deliberately protect all accumulated established dirty state in the active local durability partition even when some of those facts are not dependencies of the triggering transition.

A narrow shared/live/access boundary SHALL NOT automatically flush unrelated private/local dirty scopes.

This law preserves useful accumulated-progress saves without introducing campaign-global synchronization.

## LAW 5.5-7 — EXPLICIT SAVE IS BROAD WITHIN ITS SELECTED SAVE SCOPE

When a player explicitly requests `save`, `save game`, `сохрани игру`, or an unambiguous equivalent, successful save means:

> every established gameplay-significant dirty root in the selected save scope, plus every required recovery/reference/interpretation dependency needed to resume that state honestly, is actually durable through its native authoritative representation.

The selected save scope normally means the current campaign scope under the player's/current host's legitimate authority, partitioned where independent ownership prevents one universal writable transaction.

Explicit save SHALL NOT be satisfied by:

- a prose summary/note standing in for structured owners;
- a checkpoint that omits required current native state;
- a partial dirty subset silently left volatile inside the promised save scope;
- an unreachable/prepared physical write not yet proven durable under later 5.6 semantics.

Explicit save by itself SHALL NOT:

- pause/end the campaign;
- activate an unready campaign;
- invent unresolved mechanics/facts;
- require a checkpoint merely because the word save was used;
- require arbitrary noncanonical Story/transcript projections to be fully fresh.

Specific message/provenance evidence that is still irreducible for accepted semantic recovery is part of recovery closure, not a generic transcript requirement.

## LAW 5.5-8 — SAVE ATTEMPT USES SCOPED QUIESCENCE

Once an explicit save intent is accepted, the selected save root set SHALL remain stable enough to give the save acknowledgement a definite meaning.

Dependent gameplay mutations inside that selected save scope SHALL NOT be silently folded into or race past the in-flight save attempt.

OOC/control communication and truly independent scopes may continue where safe.

After the attempt resolves as success or failure, ordinary local/private gameplay may resume according to the failure laws below.

This quiescence is not a durable global lock, campaign-global host lease, or new state owner.

## LAW 5.5-9 — SUCCESS ACKNOWLEDGEMENT REQUIRES ACTUAL DURABILITY

A save, handoff, write-before-reveal edge, or other durability-bearing operation may be acknowledged as successfully satisfying its durability promise only when its required closure is actually durable under the applicable native-source/transport semantics.

Physical ambiguous-write determination is Step 5.6.

Intent to publish, a prepared tree/commit, an attempted request, or an in-memory flag is not sufficient evidence of durability.

## LAW 5.5-10 — FAILED EXPLICIT SAVE DOES NOT HARD-LOCK COHERENT LOCAL/PRIVATE PLAY

If explicit save fails while coherent HOT state survives:

- SHALL NOT say or imply that the requested save succeeded;
- SHALL preserve the coherent dirty HOT state when publication failure did not invalidate it;
- SHOULD report the failure briefly and honestly;
- SHOULD offer retry/repair when useful;
- MAY accept later ordinary local/private gameplay if the player proceeds;
- SHALL NOT require a ritualized explicit “continue without saving” acknowledgement when subsequent gameplay intent already makes that choice clear;
- SHALL retain the enlarged unpublished-loss exposure and retry later under applicable policy;
- SHALL recover only actual durable state if HOT state is later lost.

This friendliness does not waive any independent correctness-critical `MUST_BE_DURABLE_BEFORE(edge)` obligation.

## LAW 5.5-11 — CORRECTNESS-CRITICAL EDGE CANNOT BE FALSELY CROSSED

If durability is part of the semantic postcondition of edge `E`, then failure to establish the required closure means `E` remains failed/incomplete for the affected scope.

The runtime SHALL NOT:

- narrate a shared result that contractually requires write-before-reveal before the write succeeds;
- acknowledge recovery-safe handoff while its promised closure is not durable;
- transfer/activate/advertise ownership or visibility when that owning contract requires prior durability.

This law blocks the named edge, not necessarily all OOC communication or independent gameplay scopes.

## LAW 5.5-12 — LOCAL/PRIVATE UNPUBLISHED EXPOSURE IS A RISK-CONTROL POLICY

For deferrable local/private state, an unpublished-exposure threshold is a loss-risk/RPO-control target, not a semantic invalidity boundary.

Conceptually:

```text
scope/partition first becomes dirty
    -> exposure age starts

configured policy condition reached
    -> request durability at an available runtime opportunity

success
    -> included dirty state becomes durable
    -> exposure state resets/recomputes for remaining dirty state

failure while HOT survives
    -> protection is degraded
    -> HOT local/private play may continue
    -> retry later
```

No universal numeric threshold is defined by Step 5.5.

The current runtime hard-coded `one hour` value is therefore provisional/stale implementation policy, not a canonical architecture constant.

## LAW 5.5-13 — EXPOSURE TRACKS ACTUAL DIRTY STATE, NOT ARBITRARY COMMIT AGE

A dirty-exposure measure SHALL be anchored to the actual establishment/retention of unpublished state in the relevant durability-policy scope/partition.

It SHALL NOT be defined solely as elapsed time since the last repository commit/frontier update.

Consequences:

- a newly dirty fact created long after an old durable commit does not inherit the full age of that commit;
- an unrelated successful publication does not falsely reset exposure for dirty state that remains unpublished elsewhere;
- physical per-record clocks are not required; a policy may conservatively aggregate a scope/partition when correct.

## LAW 5.5-14 — NO BACKGROUND EXECUTION, NO EXACT WALL-CLOCK GUARANTEE

When the host provides no timer/background callback/execution opportunity, HDM cannot promise publication at the exact instant an exposure condition becomes true.

At the next suitable runtime opportunity, the applicable policy may evaluate and request the safety flush before needlessly extending exposure.

Host wall-clock passage does not itself advance fictional time or create gameplay events.

## LAW 5.5-15 — CLEAN STATE NEVER CREATES HEARTBEAT DURABILITY

If a policy scope contains no established dirty/recovery-relevant state requiring publication, elapsed time, chat age, session age, or advisory capacity risk SHALL NOT create an empty/no-op gameplay publication merely to refresh a durability timestamp.

## LAW 5.5-16 — ADVISORY HOST CAPACITY IS NOT DURABILITY AUTHORITY

Approximate host message/token/chat-age/capacity signals or locally derived heuristics MAY:

- warn the player;
- recommend proactive handoff;
- request an opportunistic SOFT flush at a safe point.

They SHALL NOT by themselves create a correctness-critical HARD edge unless a future host contract gives stronger reliable lifecycle semantics and the architecture explicitly adopts it.

False positives must be safe; false negatives fall back to normal durability and unexpected-loss recovery.

Reliable destructive lifecycle signals remain Step-5.4 handoff inputs.

## LAW 5.5-17 — SHARED/LIVE POLICIES MAY BE STRICTER THAN LOCAL RISK CONTROL

Step 5.5 defines the generic scope-policy interface. Step 5.8 SHALL bind concrete multiplayer/live ownership, visibility, conflict and publication semantics.

Expected profiles include:

```text
SINGLEPLAYER / PRIVATE-LOCAL
    long SOFT accumulation allowed
    risk-control flushes primarily protect against host loss

MULTIPLAYER SHARED OUTSIDE LIVE
    stronger event/visibility/ownership-driven publication expected

SAME-SCENE ACTIVE LIVE
    shared action-level mutation
        -> live publication/CAS
        -> then shared reveal/use
```

A fact may acquire a stronger obligation when it crosses from private/local scope into shared ownership/visibility/causal use.

## LAW 5.5-18 — CHECKPOINT AND PROJECTION FRESHNESS ARE SEPARATE

A durability closure may create/update a checkpoint only when the independent recovery policy says a checkpoint materially improves recovery.

Checkpoint is not a substitute for required native current state.

Noncanonical Story/transcript/projection freshness is not automatically part of explicit save or ordinary durability. Later Steps 5.10–5.12 own those publication/retention/delivery semantics, except specific irreducible evidence already required by Step 5.2/5.4 recovery closure.

## LAW 5.5-19 — DURABILITY BOOKKEEPING IS NOT STATE AUTHORITY

Exposure clocks, dirty markers, policy state, save attempt state, commit/ref metadata and similar bookkeeping SHALL NOT become duplicate owners of gameplay truth.

Native world/runtime/live owners remain semantic authority.

## LAW 5.5-20 — PUBLICATION FAILURE DOES NOT INVENT GAMEPLAY ROLLBACK

The logical result of durability failure depends on the owning edge:

```text
RISK-CONTROL / FAILED EXPLICIT SAVE
    -> HOT state may remain established and usable
    -> durability guarantee is degraded/not satisfied

CORRECTNESS-CRITICAL EDGE
    -> edge remains incomplete/failed
    -> affected externally dependent continuation stays gated
```

Step 5.5 does not define Git-level rollback, ambiguous ref-update proof, unreachable object handling, or transport retry mechanics; those belong to 5.6.

---

# 3. Closure construction

## 3.1 Policy roots

Policy roots are the established dirty facts/owners that the requesting policy promises to protect at the boundary.

Examples:

- explicit save: every established dirty root in selected save scope;
- normal singleplayer forced boundary: accumulated local dirty partition selected by the ordinary singleplayer policy;
- handoff: every still-current state promised across the handed-off scope;
- shared visibility edge: the shared mutation and any policy-defined prerequisite roots;
- risk-control flush: currently accumulated dirty roots in the affected local/private exposure partition.

## 3.2 Required dependency expansion

For each root, include any native dependency whose absence changes correct resume semantics or violates a directly touched integrity invariant.

Required dependency expansion is transitive but bounded by semantic necessity, not arbitrary reachability.

## 3.3 Derived/rebuildable exclusions

Do not persist merely for closure completeness:

- Temporal Agenda;
- MechanicalContext;
- selector/condition/effect aggregation caches;
- dependency DAG caches;
- loaded-record/query caches;
- presentation buffers;
- generic Story render buffers;
- model hidden reasoning/context;
- speculative future action plans.

## 3.4 Existing durable dependencies

A required dependency already durable at a compatible native source revision need not be rewritten merely because it participates in closure.

The promise is that the compatible source set is recoverable, not that every dependency receives a new physical write.

---

# 4. Explicit-save state machine

Conceptual behavior:

```text
PLAYING / ATTACHED
    -> player requests SAVE

SAVE_PENDING(scope, frozen_root_set)
    -> construct recovery-complete closure
    -> attempt durability

SUCCESS
    -> acknowledge saved
    -> clear included dirty state according to actual publication result
    -> resume attached play

FAILURE while coherent HOT survives
    -> do not acknowledge saved
    -> preserve dirty HOT state
    -> report minimally
    -> retry if useful
    -> later gameplay intent may continue local/private play

HOT lost before successful durability
    -> recover newest actual durable compatible source set
    -> never synthesize unpublished state
```

Plain `save` does not imply pause/end. `save and stop` composes the save promise with the separately requested lifecycle transition; the lifecycle transition must not be falsely represented as durably protected if its own required durability did not succeed.

---

# 5. Handoff relation

Explicit save and controlled handoff reuse closure semantics but are not identical intents.

```text
SAVE
    roots = all established dirty state in selected save scope
    postcondition = requested state is durable
    host remains attached

CONTROLLED HANDOFF
    roots = all state promised across handed-off scope
    postcondition = recovery-safe durable closure exists
                    AND old host may relinquish that scope
```

A failed save may permit continued local/private play. A failed controlled handoff cannot be acknowledged as recovery-safe relinquishment.

---

# 6. Exposure policy semantics

## 6.1 Scope/partition

Exposure belongs to a policy-owned durability partition compatible with actual writable/visibility authority.

Architecture does not require per-record timers.

A singleplayer implementation may use one conservative local campaign dirty partition when correct. Multiplayer/live may require distinct partitions.

## 6.2 Start/reset

Exposure starts when a clean partition first gains established unpublished state.

After a successful publication:

- if all dirty state in that partition was included, the partition becomes clean and exposure clears;
- if some dirty state remains outside the successful closure, exposure SHALL be recomputed/preserved so the remaining state is not falsely made younger by unrelated publication.

## 6.3 Threshold behavior

A configured local/private threshold expresses maximum intended exposure, not a guaranteed hard wall-clock RPO in a host with no background execution.

At a suitable execution opportunity after the policy condition is met, request a durability closure.

Failure leaves protection degraded but does not make coherent local/private semantic state invalid.

## 6.4 Numeric value

Step 5.5 intentionally leaves the numeric default/configuration unresolved.

The existing `one hour` implementation/test wording is architecture debt to be replaced or consciously reselected during machine realization/product configuration after this semantic contract.

---

# 7. Failure matrix

| Situation | State after failure | What may continue | What may not be claimed/crossed |
|---|---|---|---|
| explicit save fails, HOT coherent | dirty HOT established state survives | OOC and subsequent local/private gameplay if player proceeds | `saved` acknowledgement |
| risk-control flush fails, HOT coherent | dirty HOT survives, durability degraded | local/private play, later retries | policy target cannot be represented as satisfied |
| handoff publication fails | old host still owns HOT if alive | retry or abandon handoff and remain attached | recovery-safe relinquishment |
| live write-before-reveal fails | in-flight/unpublished shared result not externally established per live edge | OOC/retry/reconcile | shared reveal/use of result |
| correctness ownership/visibility edge fails | affected edge incomplete | independent unaffected scopes | successful affected edge transition |
| host dies after unpublished failure | HOT lost | recovery from actual durable compatible sources | reconstruction/invention of lost progress |

---

# 8. Scenario checks

## S1 — Long singleplayer SOFT accumulation

Several ordinary quest/NPC/item/relationship changes accumulate in one local partition.

Result: remain SOFT with zero required Git I/O until an applicable boundary/risk policy requests durability.

## S2 — Normal local forced boundary

A focal/lifecycle/other approved local boundary fires after earlier independent SOFT changes.

Result: ordinary singleplayer policy may flush the accumulated local dirty partition plus required recovery closure, not only the triggering record.

## S3 — Explicit `сохрани игру`

Result: all established dirty roots in selected save scope plus required recovery closure must become durable before saying saved.

## S4 — Save with suspended Choice/Reaction/Procedure

Result: the unresolved accepted operational owner and its required Continuation/Procedure/RNG/interpretation dependencies join closure when they are part of the promised resume point. No invented completion is required.

## S5 — Save during onboarding

Result: preserve established structured provisional setup state honestly; save does not imply PLAY_READY/active.

## S6 — Failed save, storage outage

Result: tell player save was not confirmed, keep HOT state, allow later local/private gameplay if the player proceeds; never pretend the requested save succeeded.

## S7 — Risk threshold after long dirty singleplayer session

Result: request safety flush at next suitable runtime opportunity. Failure degrades protection but does not hard-lock coherent local play.

## S8 — Threshold crosses while idle

Result: no background publication is promised. Next suitable interaction may trigger the attempt before needlessly extending exposure.

## S9 — Clean campaign idle for days

Result: no heartbeat/no-op publication.

## S10 — Old durable commit, newly dirty fact

Result: exposure age starts with dirty state, not with old commit timestamp.

## S11 — Unrelated publication while another partition remains dirty

Result: remaining dirty partition keeps/recomputes its own exposure; unrelated write cannot falsely reset it.

## S12 — Advisory near-capacity heuristic

Result: warning/handoff suggestion and optional opportunistic flush allowed; no correctness guarantee depends on heuristic.

## S13 — Same live scene shared action

Result: current live policy can impose MUST_BE_DURABLE_BEFORE(shared reveal); exact CAS ownership mechanics remain 5.8.

## S14 — Private fact becomes shared

Result: fact may have been SOFT; before another player legitimately relies on it, stronger shared policy may promote it into the relevant mandatory closure.

## S15 — Controlled handoff

Result: all state promised for handed-off scope must be durably recovery-complete before recovery-safe relinquishment acknowledgement; unrelated independent scope need not be flushed merely because another scope hands off.

---

# 9. Downstream requirements

## Step 5.6 — Campaign Publication & Crash Consistency

Must define physical evidence for:

- when a requested durability closure is actually durable;
- optimistic concurrency and closure invalidation;
- crash before/after tree/commit/ref operations;
- ambiguous acknowledgement/ref-update outcomes;
- retries/idempotency without false saved acknowledgement;
- adoption/clearing of dirty state only after proven publication outcome.

## Step 5.7 — Checkpoint / Recovery

Must select/hydrate compatible native sources sufficient to prove the promised closure without promoting checkpoint to snapshot authority.

## Step 5.8 — Multiplayer / Live

Must bind concrete ownership/visibility/race semantics to scope-specific durability policies, including action-level live write-before-reveal where retained.

Must not turn every multiplayer-local/private mutation into synchronous shared publication merely because the campaign is multiplayer.

## Steps 5.10–5.12

Must define when noncanonical Story/transcript/delivery projections may lag behind canonical durability and when specific user-visible delivery evidence has its own required boundary.

---

# 10. Explicit non-goals / rejected abstractions

Step 5.5 introduces no mandatory:

- universal HARD field;
- generic DurabilityPolicy record/schema;
- global `SAVE_ALL_DIRTY` transaction for every HARD edge;
- universal snapshot;
- scalar durability/recovery frontier;
- campaign-global dirty timeout;
- per-file dirty timer requirement;
- heartbeat commit;
- global host/session lease;
- transcript-as-save authority;
- Story-as-current-state authority;
- background scheduler unavailable to the host;
- universal one-hour constant.

---

# 11. Candidate closure criteria

Step 5.5 may canonicalize if adversarial review confirms:

1. the three-axis model does not duplicate semantic authority;
2. every correctness-critical durability edge names the edge it gates;
3. explicit save has one unambiguous successful promise;
4. friendly failure semantics do not weaken correctness-critical shared/handoff edges;
5. closure completeness satisfies Steps 5.2/5.3 without broad world scans;
6. accumulation scope preserves expected singleplayer progress without introducing global multiplayer synchronization;
7. exposure policy is scope-aware and cannot be falsely reset by unrelated writes;
8. no background-execution guarantee is implied;
9. old `one hour` runtime policy is clearly noncanonical debt;
10. downstream 5.6–5.8 ownership remains distinct.

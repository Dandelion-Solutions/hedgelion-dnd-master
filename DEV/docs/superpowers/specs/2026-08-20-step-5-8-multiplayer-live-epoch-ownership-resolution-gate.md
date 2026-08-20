# Step 5.8 — Multiplayer / Live-Epoch Ownership — Resolution Gate

Status: **RESOLUTION GATE — READY FOR CANONICALIZATION**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Resolves:

- `2026-08-20-step-5-8-multiplayer-live-epoch-ownership-candidate-spec.md`
- `2026-08-20-step-5-8-multiplayer-live-epoch-ownership-adversarial-review.md`

Recommended canonical direction:

> **ROUTED FIXED-CLAIM LIVE EPOCH / EXACT-SOURCE CAS / TERMINAL SOURCE FREEZE / FORWARD CAMPAIGN ABSORPTION**

The adversarial review preserved the candidate's central model and found four blocking technical gaps plus several cross-step strengthening requirements. This gate resolves them without introducing a leader, TTL lease, heartbeat, distributed transaction, global fencing counter, generic per-entity lock manager or scalar cross-domain frontier.

No remaining finding requires an owner-level product decision.

---

# 1. Resolution summary

The canonical model SHALL preserve:

```text
current campaign routing
    -> selects one live epoch + immutable bounded claims
    -> ACTIVE exact-source CAS transitions
    -> terminal ACTIVE -> CLOSED source-local CAS fence
    -> CLOSED_UNABSORBED current truth with zero ordinary writers
    -> one forward campaign absorption/transition transaction
    -> optional later successor epoch
```

And add the following mandatory refinements:

1. collision-free live-born stable identity namespace;
2. live publication granularity aligned to native Step-3 atomic durability edges, not one high-level player action;
3. bounded machine-decidable write-authority routing for every live-admissible owner/partition;
4. explicit live-containment admissibility for native owner scopes;
5. exact save validation over moving live domains without forced close;
6. controlled handoff materializes promised in-flight host-only work but does not transfer a leader lease;
7. temporal/Procedure/Continuation ownership survives close/absorption under native lifecycle;
8. revocation/controller transfer uses close then one campaign absorption+authorization transaction;
9. partial multi-scope freeze gates only dependent transition scope;
10. transport abstraction requires exact expected-source CAS and does not canonize Contents API;
11. disclosure remains a separate post-emission owner/edge;
12. fixed claims may reference owner-defined typed writable partitions with deterministic membership/non-overlap, not a generic selector language.

---

# 2. B1 resolution — live-born persistent identity

## Problem

A campaign-scoped sequential allocator cannot remain the mandatory allocator for identities first made durable inside independent concurrent live epochs without forcing campaign writes onto the hot path or duplicating allocation authority.

## Resolution

Introduce a domain-qualified **live-epoch identity namespace**.

Any identity that is first durably established inside live epoch E and must remain stable after acceptance SHALL be globally collision-free by construction without campaign allocator mutation.

Conceptually:

```text
LiveBornIdentity =
    kind
    + stable epoch identity E
    + accepted source-local creation coordinate
```

The creation coordinate may be represented by one or more source-local ordinals/segment identities, provided:

- uniqueness is guaranteed within E;
- competing prospective allocations from one prior source revision are serialized by the same accepting CAS boundary;
- only the winning accepted transition establishes the identity;
- rejected prospective identities have no canonical existence and may be discarded;
- accepted identity never requires rekey solely because the epoch later absorbs into campaign;
- no ordering/comparison across epochs is inferred from local numbering.

For Step-3 execution/idempotency identities, stable identity is mandatory once accepted.

A world/entity owner may remain provisional/rekeyable only if its native promotion contract explicitly permits that and no external durable reference requiring stable identity escapes first.

The campaign allocator remains valid for campaign-native allocation domains. It is no longer assumed to be the sole allocator for all persistent identity domains.

This is a domain-typing refinement, not a second campaign allocator.

Resolution status: **CLOSED**.

---

# 3. B2 resolution — publication granularity and terminal close

## Problem

One player action may contain several Step-3 durability/acceptance edges. Requiring one high-level action to equal one live CAS would either collapse valid Continuation/reaction boundaries or leave accepted execution state volatile.

## Resolution

Canonical live atomicity is defined at the **native atomic durability edge**, not at the user-message/action level.

> Each native execution/lifecycle edge that establishes live-owned durable state publishes one complete source transition. No one such edge is split into per-field/per-owner partial publications merely because the physical envelope contains several owners.

A single player action MAY therefore produce several live transitions, for example:

```text
accept execution root/continuity
-> commit execution segment/world consequence
-> suspend/consume Continuation or reaction
-> later disclosure persistence after host emission
```

Each accepted transition is independently idempotent/recoverable under the native owner contract.

### Close interaction

Terminal close fences **future ordinary live mutation**. It does not revoke already accepted native execution state.

When close races a host:

```text
prospective/unpublished work
    -> may lose the close CAS race and remain unestablished

already durably accepted RuntimeCommand/Resolution/Procedure/Continuation/RNG/etc.
    -> remains part of the final current live source/closure
    -> survives close
    -> must remain boundedly recoverable through absorption/next native partition
```

A controlled durability/handoff edge that has promised an accepted input cannot complete while the only sufficient evidence remains volatile host memory.

Resolution status: **CLOSED**.

---

# 4. B3 resolution — bounded claim authority lookup

## Problem

Fixed claims are insufficient if determining whether X is claimed requires scanning all scenes/live branches.

## Resolution

For every owner/scope class admitted to live mutation, architecture requires:

```text
WriteAuthorityLookup(owner_or_partition)
    -> CAMPAIGN
     | LIVE(epoch/ref)
     | INTEGRITY_CONFLICT
```

with **bounded typed routing**.

Opening overlap checks and campaign-side mutation admission SHALL NOT require campaign/world/full-live scans.

Physical realization remains owner-specific and may use:

- direct native owner -> current scene/live route evidence;
- compact typed active-live routing partition;
- campaign-materialized claim routing index maintained in the same campaign transaction as claim selection/release;
- another deterministic bounded native routing method.

Any routing index is derivative authority-routing evidence, not copied current owner state.

The architecture does NOT mandate one universal `entity -> epoch` database and does NOT add a generic claim query language.

A selected route plus every derivative claim-routing record required to make it bounded participates in the same campaign durability/authority transaction strongly enough to prevent route/index splits.

Resolution status: **CLOSED**.

---

# 5. B4 resolution — live containment admissibility

## Problem

A scene epoch cannot become accidental authority for a Procedure, temporal owner or other native owner whose writable semantic lifetime/scope extends outside that live mutation partition.

## Resolution

A native owner or typed writable subpartition X is live-claimable by E only when:

```text
WritableScope(X) is fully contained by MutationPartition(E)
```

and membership/disjointness is machine-decidable under X's native owner contract.

Consequences:

- a scene-local actor/asset/effect/knowledge partition may be live-claimed when its owner contract defines suitable current writable partition semantics;
- a Procedure/temporal/global owner spanning multiple live partitions remains in its native partition;
- such an owner may force a typed cross-scope synchronization/repartition boundary when a live action must mutate it;
- physical inclusion in one live file does not prove semantic containment or transfer ownership;
- no generic field-level subownership language is introduced by Step 5.8.

For an owner whose contract defines a typed writable subpartition, claims MAY refer to that partition rather than individual record IDs.

Resolution status: **CLOSED**.

---

# 6. Fixed claims refined to typed owner/partition claims

The immutable claim set Q(E) may contain:

```text
exact native owner reference
OR
native-owner-defined typed writable partition reference
```

only when the native owner defines deterministic:

- membership;
- non-overlap/disjointness;
- mutation admission;
- recovery routing.

This allows, for example, a scene-contained epistemic partition to admit new `(knower,fact)` rows within its already-selected partition without requiring a rollover for each row, while preserving sole `world.knowledge` semantic ownership.

It does not permit generic selectors such as arbitrary predicates over all records.

Resolution status: **CLOSED**.

---

# 7. Explicit SAVE over moving live sources

Step 5.5 SAVE is a durability promise over compatible native source closure, not one global snapshot.

An explicit save does NOT automatically close active live epochs.

For selected save scope:

1. freeze the save's logical roots/partitions sufficiently to define its promise;
2. publish required campaign/local volatile dirty roots;
3. for every participating live partition, ensure every established owner generation included by the save promise is already durable or make it durable under the live source's exact-CAS protocol;
4. at final save gate, resolve current routing and exact current participating live source revisions;
5. source advancement is not failure by itself: accepted live advancement is itself durable current state;
6. prove current compatible RRC for the save scope;
7. if routing/authority movement prevents a definite compatible composition, boundedly retry/revalidate; never invent a scalar cross-domain save frontier.

SAVE acknowledgement requires the final current composed source set to satisfy Step 5.5, not all sources to remain motionless after the acknowledgement.

Resolution status: **CLOSED**.

---

# 8. Controlled handoff with live state

No live leader/lease is transferred between hosts.

Before acknowledging a controlled host handoff:

- all already-established live current state covered by the handoff promise is durable in current native sources;
- accepted in-flight execution/input promised across the handoff is materialized into its native recoverable owner/evidence;
- purely prospective work may be discarded/recomputed after handoff because it was not established;
- current route/live source identities are enough for the receiving host to recover under Steps 5.4/5.7/5.8.

A handoff alone does not require live rollover when the live epoch remains valid and all promised continuity is durable.

The receiving host gains no exclusive lease. It joins the same current-authority/CAS model.

Resolution status: **CLOSED**.

---

# 9. Temporal obligations and CLOSED/absorption

Terminal close does not cancel temporal obligations, Procedures, Continuations or accepted execution merely because ordinary scene gameplay mutation is frozen.

For every native owner contained by E:

- its current lifecycle/deadline/claim/accepted execution state remains native authority inside the final live source until moved/absorbed;
- Step-5.2 root/temporal routing remains sufficient to discover it during CLOSED_UNABSORBED;
- campaign absorption must carry/materialize the native owner and required routing/evidence into the next valid native durability partition before releasing the old live route;
- due/not-due and fictional chronology are not derived from close/absorption Git ordering.

If the owner's writable scope is not contained by E, it must never have been claimed solely by E; cross-scope owner semantics apply instead.

Resolution status: **CLOSED**.

---

# 10. Authorization transitions

## 10.1 Revocation/controller removal

When a change removes current write authority relevant to active E:

```text
CAS close affected active E
-> one campaign transition transaction {
       absorb/finalize E as required
       change PLAYER/controller authorization
       clear/replace route/claim routing
       update required recovery/index state
   }
```

Do not absorb first and revoke in a later campaign commit.

If an authorized player mutation wins the live CAS before close, that accepted mutation is real and close retries from the new current source.

If close wins, stale ordinary player mutation rejects and may not be retried against CLOSED.

No design can guarantee that a maintenance close wins immediately against unlimited continuous valid concurrent writes without adding a coordinator/lease. Baseline provides safety, not starvation-free revocation liveness. Automatic retries are bounded and maintenance may require retry/coordination. This is accepted as the simpler HDM tradeoff.

## 10.2 Additive grant/join

An authorization grant that does not invalidate current claimed-owner state MAY be published campaign-side without closing unrelated live epochs, provided current live mutation semantics/participant visibility do not require route/claim changes.

If the new participant/controller requires modifying the active epoch's fixed claims or live authorization-relevant partition semantics, use close/absorb/successor boundary.

Resolution status: **CLOSED**.

---

# 11. Entity/owner transfer and partial multi-scope freeze

When one transition affects ownership across active live partitions E1..En:

```text
close each affected writable epoch independently by exact CAS
-> once every required source is confirmed CLOSED at exact final revision
-> one campaign-domain absorption/transfer transaction
-> optional successor epochs
```

A crash/failure after only a subset closes yields a mixed but valid state:

- successfully closed scopes remain current truth but temporarily non-writable;
- still-active scopes remain current and ordinarily writable;
- the intended cross-scope transfer/global event has not yet been established;
- only operations depending on the incomplete transition are gated.

Do not roll back already-closed epochs by reopening them.

Recovery resumes close/absorption from actual source states.

Resolution status: **CLOSED**.

---

# 12. Cross-source mutable dependency rule

A live action may read unclaimed external owners.

If an external mutable dependency can change concurrently and such movement can materially change legality, stakes, target validity, causal result or required owner mutation, the action crosses a synchronization boundary.

The runtime must then use the owning cross-scope/chronology synchronization protocol rather than assuming the dependency remains stable through one live CAS.

Git commit ordering across independent refs never decides the fictional winner.

Step 5.9 owns chronology/reconciliation semantics; Step 5.8 owns refusing an unsafe local-only CAS when the action actually spans mutable authority domains.

Resolution status: **CLOSED**.

---

# 13. Transport realization boundary

The canonical live transport requirement is abstract:

```text
LiveSourceCAS(
    source_ref,
    expected_exact_source_revision,
    complete_native_transition,
    acting_principal/authorization evidence,
    transition kind
)
 -> ACCEPTED(new exact revision)
  | REJECTED(typed reason/currentness)
  | INDETERMINATE
```

Canonical architecture does not depend on GitHub Contents API blob-SHA semantics.

Current connector lab evidence is only feasibility evidence that source-local stale writes can be rejected.

A future RepositoryPort may use Git commit/ref CAS, GraphQL expected-head mutation or another supported GitHub primitive preserving equivalent semantics.

Ambiguous outcome follows the Step-5.6 pattern:

- do not reveal/ack by assumption;
- inspect current exact source + bounded lineage/identity evidence;
- historical inclusion of intended transition does not imply its values remain current;
- adopt current compatible state when proven;
- never overwrite newer state by force.

Resolution status: **CLOSED**.

---

# 14. Step-4 disclosure boundary

Shared fictional/mechanical state publication and human disclosure persistence are separate edges.

A mechanical/shared consequence that requires write-before-reveal must first become durably accepted in its native live source.

Narrator generation/emission occurs afterward under Step-4 eligibility.

`runtime.disclosure` may advance only after the appropriate host-emission boundary defined by Step 5.12.

Therefore one high-level interaction may legitimately require a later separate disclosure publication. The live state transition SHALL NOT pre-record human exposure merely to preserve one-write-per-action aesthetics.

Resolution status: **CLOSED**.

---

# 15. Successor opening

A successor epoch E2 is opened only from an already-current campaign authority after predecessor absorption/transition succeeds.

Do not encode E2 as depending on the SHA of the same campaign commit that is simultaneously attempting to select it.

Normal sequence:

```text
E1 CLOSED @ Lf
-> campaign absorption C becomes current
-> prepare E2 from C
-> campaign route-selection transaction selects E2
```

An implementation may later optimize remote round trips only if it preserves non-self-referential source identity and the same authority proof.

Resolution status: **CLOSED**.

---

# 16. Performance/liveness position

Baseline hot path deliberately optimizes for HDM's small-player, human-paced shared scenes:

- no background heartbeat;
- no elected leader;
- no campaign HEAD check solely to detect legal route-away on each live turn, because legal route-away first closes the live source;
- one exact live source currentness probe when shared-state synchronization is required;
- one exact live CAS per native durability edge that actually establishes shared/live state;
- claim lookup bounded by typed routing, never all-live scan;
- rare owner transfer/global-event operations take explicit slow path.

Potential fixed-claim rollover frequency is an evaluation/performance risk, not an unresolved product decision. Reopen dynamic claim acquisition only if measured traces show rollovers materially dominate multiplayer latency/UX and justify a more complex authority manager.

Baseline makes no starvation-free progress guarantee under an indefinitely hostile/continuously contended writer. It guarantees stale/non-current writers cannot overwrite accepted authority through conforming CAS protocol.

---

# 17. Canonicalization gate result

All adversarial blocking findings are resolved without changing the core architecture class.

No owner decision remains open.

Candidate may be canonicalized with the refinements in this gate.

Canonicalization MUST preserve at least:

```text
EXACTLY ONE current truth authority per claimed owner/partition
AT MOST ONE ordinary writable authority
CLOSED_UNABSORBED may have zero ordinary writers
NO route-away from ACTIVE live source
NO TTL/heartbeat/leader correctness dependency
NO distributed transaction
NO generic fencing counter/global sequence
NO dynamic retrospective claim acquisition
NO unbounded claim lookup
NO semantic mega-owner created by physical LIVE_STATE packing
NO campaign allocator dependency on ordinary live hot-path identity creation
NO cancellation of already accepted execution merely because epoch closes
NO false SAVE/handoff/disclosure acknowledgement
NO force rewrite / stale overwrite
```

Expected next artifact:

- canonical Step-5.8 specification incorporating candidate + this gate.


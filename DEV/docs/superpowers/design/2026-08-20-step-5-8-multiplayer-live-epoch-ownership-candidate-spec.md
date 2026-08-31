# Step 5.8 — Multiplayer / Live-Epoch Ownership — Candidate Specification

Status: **CANDIDATE — NONCANONICAL PENDING ADVERSARIAL REVIEW**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Candidate architecture:

> **ROUTED FIXED-CLAIM LIVE EPOCH / HEAD-CAS MUTATION / TERMINAL SOURCE FREEZE / FORWARD CAMPAIGN ABSORPTION**

Derivation:

- `2026-08-20-step-5-8-multiplayer-live-epoch-ownership-task-brief.md`
- `2026-08-20-step-5-8-multiplayer-live-epoch-ownership-research-draft.md`
- `2026-08-20-step-5-8-multiplayer-live-epoch-ownership-analytical-challenge.md`

This specification defines logical architecture only. It does not implement schemas/runtime/Python transport and does not supersede Step-5.9 chronology, Step-5.10–5.12 projections/delivery, Step-5.13 GC or Step-6 deployment work.

---

# 1. Canonical candidate model

HDM multiplayer live play uses a scene-centered temporary native source selected by current campaign routing.

The live source does not create a leader process or a new semantic mega-owner. It is a temporary physical/native durability partition through which an immutable bounded set of typed native owners is currently mutable.

Conceptually:

```text
CURRENT CAMPAIGN AUTHORITY H
        |
        | LiveRoute(scene S, epoch E, claims Q)
        v
LIVE EPOCH E
    ACTIVE @ exact source revision L
        |
        | authorized multi-writer CAS
        v
    ACTIVE @ L+n
        |
        | terminal expected-revision close CAS
        v
    CLOSED @ exact final Lf
        |
        | current truth remains here
        | ordinary gameplay writes = forbidden
        v
ONE CAMPAIGN ABSORPTION / TRANSITION TXN
        |
        v
CURRENT CAMPAIGN AUTHORITY C
        |
        +--> optional later successor E2
```

The primary correctness invariant is:

```text
for every claimed mutable owner/scope:
    exactly one current truth authority is decidable
    and at most one ordinary writable authority exists
```

Zero ordinary writable authorities is valid during a closed/unabsorbed transfer interval.

---

# 2. Vocabulary

## 2.1 LiveRoute

A **LiveRoute** is current campaign-domain routing evidence selecting one live epoch source for a scene-centered mutation partition.

Conceptually it identifies:

```text
scene/scope identity
epoch identity
live source ref/path identity
base campaign revision identity
immutable admitted mutation owner refs Q
minimum source/provenance data needed to validate adoption
```

Exact schema spelling is implementation work.

LiveRoute is authority **routing**, not copied owner state.

## 2.2 Mutation claim

A **mutation claim** is a typed stable native-owner reference saying that, while the route is current, ordinary current mutation of that owner is admitted through this live epoch and is not admitted through campaign/another live epoch.

Claims are not:

- copies of state;
- read permissions;
- player ACLs;
- locks with TTL;
- global sequence numbers;
- proof the owner actually changed.

## 2.3 Touch/dependency evidence

A **touch set** records what a live transaction/epoch actually changed or materially depended on.

It is retrospective conflict/publication evidence and does not establish authority.

## 2.4 Current truth authority

The source whose exact current native representation must be used to answer/continue the claimed owner's current gameplay state.

## 2.5 Ordinary write admission

Whether normal gameplay mutation is currently allowed against the current truth authority.

A source may be current truth but write-frozen.

## 2.6 Source revision fence

The exact current live source revision/HEAD expected by a prepared live mutation. It is the compare-and-swap fence.

No generic integer generation is required.

---

# 3. Authority laws

## LAW 5.8-1 — LIVE ROUTING SELECTS SOURCE AUTHORITY; BRANCH EXISTENCE DOES NOT

A live source becomes current authority only when current campaign/native owning-scope routing validly selects it.

A branch/source is not authoritative merely because it:

- exists;
- has the expected name;
- has a newer timestamp;
- has more commits;
- was remembered by a chat;
- was named by a checkpoint;
- was prepared by an opener.

An unselected prepared live source is non-authoritative infrastructure/orphan evidence.

## LAW 5.8-2 — EXACTLY ONE CURRENT TRUTH AUTHORITY PER CLAIMED OWNER

For every owner admitted by a current live route, current truth resolves through the selected live source until that route is validly transferred/absorbed.

Campaign base representation remains required historical/base/dependency state, not fallback current truth.

## LAW 5.8-3 — AT MOST ONE ORDINARY WRITABLE AUTHORITY

No owner/scope may be ordinarily writable through campaign and live simultaneously or through two live epochs simultaneously.

`CLOSED_UNABSORBED` deliberately has:

```text
current truth authority = selected closed live source
ordinary writable authority = none
```

Architecture SHALL NOT invent a campaign writable window before final live state is durably absorbed.

## LAW 5.8-4 — SEMANTIC OWNERS SURVIVE PHYSICAL LIVE RELOCATION

A live source is a physical/native durability and synchronization partition, not a replacement semantic owner.

Examples remain:

```text
PC/world actor state         -> its native world owner
Procedure ResourceState      -> runtime.procedure
Resolution execution state   -> runtime.resolution
fictional knowledge          -> world.knowledge
objective lore proposition   -> world.lore_fact
human exposure               -> runtime.disclosure
```

Physical co-location in one live source SHALL NOT erase these owner identities/lifecycles.

## LAW 5.8-5 — CURRENT LIVE ROUTE CLAIMS ARE WRITE-AUTHORITY EVIDENCE

Current campaign routing SHALL expose enough bounded typed owner claims to decide whether an existing native owner may be mutated through the live source.

Before live mutation of existing owner X:

```text
X must be in current immutable claim set Q
```

unless X is a newly created epoch-local owner whose lifecycle explicitly begins inside E.

Before ordinary campaign mutation of owner X:

```text
X must not be currently claimed by another live route
```

## LAW 5.8-6 — CLAIM SET IS IMMUTABLE FOR ONE EPOCH

The admitted mutation owner set Q of selected epoch E SHALL NOT expand/shrink while E remains the same active/closed-unabsorbed epoch.

Changing current mutation ownership requires a lifecycle boundary:

```text
close/freeze affected epoch(s)
-> forward campaign absorption/transition
-> select new epoch(s)/claim set(s) if needed
```

This rule deliberately rejects normal dynamic per-owner live claim acquisition/release.

## LAW 5.8-7 — CLAIMS ARE OWNER/SCOPE TYPED, NOT PATH-ONLY

Correctness-relevant claim identity SHALL use typed native owner/scope identity.

File paths/touch paths may be transport hints/evidence but cannot be the only semantic ownership identity when one owner spans/moves representations.

## LAW 5.8-8 — SELECTED LIVE CLAIM SETS SHALL NOT OVERLAP

Two current selected live routes SHALL NOT claim the same mutable native owner/scope concurrently unless a specific later owner contract explicitly defines a compatible non-overlapping subownership decomposition.

Baseline Step 5.8 defines no such generic subownership.

Persisted overlapping current claims are integrity defects, not a last-writer-wins condition.

## LAW 5.8-9 — NO IMPLICIT CLAIM GRAPH CLOSURE

Claiming owner X does not automatically claim every owner/reference reachable from X.

Claims cover current mutation authority only.

Read/reference/recovery dependencies remain handled by their own owner/source contract and Step-5.2 closure.

---

# 4. Claim-set construction laws

## LAW 5.8-10 — CLAIM SET IS BOUNDED TO THE LIVE MUTATION HORIZON

Opening selects the smallest practical set of existing native owners that can reasonably require synchronized current mutation in the shared actionable scene horizon.

Likely examples include:

- the scene current-state owner;
- participating PCs;
- material participating NPCs;
- significant interactive assets/items;
- scene-local effects/process owners whose current state may mutate materially;
- live-local execution/procedure owners that must be current/recoverable in this partition.

Do not claim arbitrary world graph, all location residents, all lore, all knowledge rows, all referenced owners or all Story/history merely for convenience.

## LAW 5.8-11 — EPOCH-LOCAL NEW OWNERS MAY BEGIN LIVE-OWNED

A new owner/entity whose semantic lifecycle validly begins inside E may be born live-local without prior campaign mutation claim because no older campaign current representation competes with it.

Its identity/lifetime must satisfy Step-5.2 recovery/promotion rules.

Epoch-scoped provisional identities remain confined to E until durable promotion/compaction permits broader references.

## LAW 5.8-12 — UNCLAIMED EXISTING OWNER MUTATION REQUIRES BOUNDARY

If ordinary live resolution needs to mutate existing durable owner X and X is not in Q:

- SHALL NOT publish the mutation into E;
- SHALL NOT silently write X through campaign while E's action assumes live atomicity;
- SHALL initiate/reach an appropriate ownership synchronization boundary or re-plan the action without that mutation.

The baseline solution is close/absorb/reopen with an appropriate new claim set.

## LAW 5.8-13 — TOUCH SET DOES NOT CREATE CLAIM

`touched_entity_ids`, `touched_campaign_paths` or equivalent mutation evidence SHALL NOT dynamically establish write authority.

Prospective authority is selected before mutation; touch evidence is retrospective.

---

# 5. Writer model and fencing laws

## LAW 5.8-14 — NO LONG-LIVED LIVE LEADER IS REQUIRED

Several valid sessions MAY concurrently attempt writes against one selected ACTIVE live source.

Correctness is serialized through exact-revision CAS, not an elected chat/process host.

Step 5.8 introduces no host leader identity, heartbeat or TTL lease.

## LAW 5.8-15 — EVERY LIVE MUTATION USES EXACT EXPECTED SOURCE REVISION

Every authoritative live mutation, including gameplay mutation and close/freeze, SHALL condition publication on the exact live source revision observed/accepted by the mutation attempt.

Conceptually:

```text
CAS(source E, expected L, new complete live source state) -> accepted|rejected|indeterminate
```

A stale expected revision must not overwrite newer source state.

## LAW 5.8-16 — SOURCE HEAD/REVISION IS THE MUTATION FENCE

The exact native source revision/HEAD is the correctness fence.

A source-local integer `revision` MAY exist for diagnostics/within-epoch semantics but SHALL NOT replace exact source revision as publication guard and SHALL NOT be treated as globally comparable.

## LAW 5.8-17 — NO TTL/HEARTBEAT FENCING

Ordinary live correctness SHALL NOT depend on:

- wall-clock lease expiry;
- periodic keepalive;
- chat online-presence detection;
- background polling;
- heartbeat commits.

A future deployment may add non-authoritative contention optimizations only if they do not weaken exact-revision/lifecycle correctness.

## LAW 5.8-18 — APPLICATION AUTHORIZATION IS SEPARATE FROM REVISION CAS

A successful technical Git/ref condition is insufficient without valid current application authorization.

A live write must also establish:

- correct selected repository/campaign/ref;
- trustworthy acting principal/delegation;
- active PLAYER/creator/controller authority required by operation;
- operation limited to owners admitted by current live route and native rules.

Repository collaborator permission or service credentials do not grant gameplay authority.

---

# 6. Live lifecycle laws

## LAW 5.8-19 — LIVE SOURCE LIFECYCLE IS MONOTONIC ACTIVE -> CLOSED

Baseline live lifecycle is:

```text
ACTIVE -> CLOSED
```

`CLOSED` is terminal for that epoch.

The same epoch SHALL NOT reopen/reactivate.

Continued live play after close uses a new successor epoch.

## LAW 5.8-20 — ACTIVE MEANS CURRENT TRUTH + ORDINARY CAS WRITES

When current route selects E and exact E state is ACTIVE:

- E is current truth authority for Q;
- authorized ordinary gameplay mutations MAY attempt exact-revision CAS;
- write-before-shared-reveal applies.

## LAW 5.8-21 — CLOSED MEANS CURRENT TRUTH + ZERO ORDINARY WRITES UNTIL ABSORPTION

When current route still selects E and E is CLOSED:

- E remains current truth authority for Q;
- no ordinary gameplay mutation may publish to E;
- campaign does not become current for Q merely because E closed;
- authorized compaction/recovery/maintenance may read/use E under exact final revision;
- cold recovery may resume compaction.

## LAW 5.8-22 — CLOSE MUST ITSELF BE CAS-PUBLISHED

Freeze/close must advance the live source from exact expected ACTIVE revision to CLOSED via the same exact-revision serialization discipline.

If an ordinary gameplay writer wins first, close retries/revalidates from the newer accepted live state.

If close wins first, stale ordinary writers reject on expected revision and may not retry after observing CLOSED.

## LAW 5.8-23 — ROUTE-AWAY REQUIRES CONFIRMED TERMINAL CLOSE

A conforming protocol SHALL NOT clear/replace current live route or reassign claimed authority away from selected E while E remains ACTIVE.

Before route-away/absorption/revocation/claim transfer:

```text
selected E must be confirmed/verified CLOSED at exact final revision Lf
```

Campaign state that supersedes E while the prior selected source remains ACTIVE without valid transfer evidence is integrity suspect for the affected scope.

## LAW 5.8-24 — CANCELLED MAINTENANCE DOES NOT REOPEN CLOSED EPOCH

If a maintenance/revocation/transfer attempt closes E but later aborts, E remains terminal CLOSED.

To resume ordinary live play:

- resolve/absorb forward from E;
- then open a new epoch if needed.

Do not undo the fence by `closed -> active`.

---

# 7. Shared mutation protocol

## 7.1 Read/sync phase

For cached selected ACTIVE route E at known live head Lc:

1. before a shared-state-dependent action/observation, probe E current ref/head;
2. if unchanged, retain cached exact live state;
3. if changed, fetch exact live source state at new head and replace cache;
4. if CLOSED, stop ordinary mutation and follow current campaign routing/compaction protocol;
5. no ordinary campaign HEAD refresh is required solely to detect legal route-away, because legal route-away is preceded by live close which changes E itself.

## 7.2 Resolve phase

Resolve intent/rules/randomness/consequences from:

- exact current live native owner state;
- accepted runtime/rules interpretation;
- bounded required external dependencies;
- authenticated actor/controller identity;
- existing Step-3 execution/idempotency semantics.

Freeze the logical semantic result and dependency/touch footprint before publication.

## 7.3 Publish phase

Build one complete intended live-source mutation and CAS expected exact L -> L'.

For a logically resolved shared action:

- one source publication should contain the complete live-local atomic delta needed for that action;
- no per-field/per-owner partial live writes for one action;
- physical one-file layout may remain an implementation optimization;
- if future physical live source becomes multi-file, one source-ref commit/transition must still atomically publish the complete delta.

## 7.4 Reveal edge

Newly established interactive shared fact/consequence whose owner contract requires shared durability becomes revealable/useable to other participants only after successful live publication.

Narration may not reveal an uncommitted shared result.

Presentation-only texture that establishes no actionable/shared fact remains outside this durability requirement according to Step 5.5/Step 4.

---

# 8. Live write outcome laws

## LAW 5.8-25 — LIVE TRANSPORT OUTCOME IS ACCEPTED / REJECTED / INDETERMINATE

Future RepositoryPort semantics SHALL distinguish:

```text
ACCEPTED(new exact source revision)
REJECTED(currentness/conflict/authorization/validation reason)
INDETERMINATE(transport outcome not yet proven)
```

No player-visible “shared result established” may be inferred from request dispatch alone.

## LAW 5.8-26 — CONFIRMED STALE REVISION REJECTION INVALIDATES SOURCE SNAPSHOT

If expected-revision CAS rejects because E advanced:

- discard old publication snapshot;
- fetch/pin exact current E;
- classify lifecycle + dependency overlap;
- do not blind overwrite/retry.

## LAW 5.8-27 — CLOSED CURRENT SOURCE TERMINATES ORDINARY RETRY

If refresh after rejection observes current CLOSED state:

- ordinary gameplay write to E is not retried;
- uncommitted consequence derived only from stale state does not become shared canon;
- runtime follows campaign routing/compaction/recovery.

Already accepted semantic inputs/RNG retain their native identities according to Step 3; they are not fabricated as having occurred if their shared consequence never published.

## LAW 5.8-28 — DISJOINT LIVE MOVEMENT MAY PRESERVE FROZEN SEMANTIC RESULT

If current E remains ACTIVE and intervening live movement is proven disjoint from the action's semantic/read/authorization/recovery dependency footprint, the already-resolved delta MAY be reapplied onto current state and retried with the same valid RNG/accepted inputs.

## LAW 5.8-29 — OVERLAP REQUIRES NATIVE SEMANTIC REVALIDATION

If current movement touches assumptions that can change legality/stakes/result:

- revalidate/re-resolve under native owner/rules semantics;
- preserve existing random result only if it is still the same accepted random experiment;
- request new player choice/randomness only when original experiment/action no longer applies.

Repository conflict itself never justifies reroll.

## LAW 5.8-30 — AUTOMATIC LIVE CONTENTION RETRY IS BOUNDED

No unbounded CAS retry loop.

Repeated contention enters an explicit synchronization/retry outcome for the affected shared scope while OOC/independent activity may continue where safe.

---

# 9. Indeterminate live publication and idempotency

## LAW 5.8-31 — INDETERMINATE LIVE WRITE DOES NOT REPLAY GAMEPLAY BLINDLY

After lost/ambiguous acknowledgement, recovery queries actual current live source and native semantic receipts/evidence.

It SHALL NOT:

- reroll;
- re-run accepted execution from scratch by default;
- emit the intended result as if durable;
- blindly submit the same semantic effect as a new action.

## LAW 5.8-32 — HISTORICAL PUBLICATION AND CURRENT VALUES ARE DISTINCT

If intended live commit/source revision C is current or a proven ancestor of current D:

- C's mutation entered durable live lineage;
- current values must still be taken from D/current authority;
- later legitimate writes may supersede state established by C.

Lineage alone is not current-value proof.

## LAW 5.8-33 — NATIVE EXECUTION/EVENT/RECEIPT IDENTITY PROVIDES SEMANTIC IDEMPOTENCY

Step-3 execution owner/segment/event/receipt identity should be used where required to detect that a semantic live consequence was already materialized.

Step 5.8 SHALL NOT introduce a generic persisted live transaction journal solely for transport retry.

---

# 10. Opening / adoption laws

## LAW 5.8-34 — OPENING PREPARES BEFORE IT SELECTS

Opening may prepare a candidate live source before authority selection.

Prepared source E is non-authoritative until one current campaign transaction validly selects its route + claims.

## LAW 5.8-35 — OPENING FREEZES A COMPLETE INITIAL CLAIM SET

Before selection, opener derives Q from the bounded shared-scene mutation horizon and validates current campaign/live ownership dependencies.

The selected route commits E and Q as one campaign-domain authority-routing transition.

## LAW 5.8-36 — CONCURRENT OPENERS SERIALIZE ON CAMPAIGN AUTHORITY

Two openers may prepare candidates concurrently.

Only campaign publication makes one candidate route authoritative.

If campaign current revision moves:

- loser repins/revalidates current routes/claim overlap;
- overlapping old candidate cannot be transport-only selected;
- disjoint candidate may be rebuilt/revalidated on current campaign basis.

No force update.

## LAW 5.8-37 — DETERMINISTIC BRANCH/EPOCH NAMES ARE NON-AUTHORITATIVE

Deterministic naming MAY improve convergence/diagnostics but SHALL NOT decide authority.

Adoption requires current route + exact source validation.

## LAW 5.8-38 — CANDIDATE ORPHAN IS SAFE NONAUTHORITY

If live candidate source exists but campaign route selection never succeeds, it is non-authoritative orphan/prepared evidence.

Cold recovery ignores it unless bounded integrity/maintenance explicitly needs it.

Step 5.13 owns physical cleanup.

---

# 11. Campaign-side write protection

## LAW 5.8-39 — CAMPAIGN PUBLICATION MUST RESPECT CURRENT LIVE CLAIMS

A campaign transaction intending to mutate native owner X SHALL include current owning-route/live-claim state in its bounded authority/conflict validation when X may be live-owned.

If current campaign routing says X is claimed by selected live E:

- normal campaign gameplay write to X is forbidden;
- operation must route to E or run an explicit ownership/maintenance boundary.

## LAW 5.8-40 — LIVE CLAIM SELECTION FENCES STALE CAMPAIGN WRITERS VIA CAMPAIGN CAS

A campaign writer prepared before a live claim selection cannot successfully advance stale campaign parent after the route transaction wins.

On repin/revalidation, claim overlap is semantic/authority overlap, not disjoint movement.

## LAW 5.8-41 — OVERLAPPING CAMPAIGN MUTATION DURING LIVE OWNERSHIP IS EXCEPTIONAL

While E validly claims Q, ordinary conforming campaign gameplay shall not mutate Q.

At absorption, campaign movement touching Q therefore indicates:

- explicitly participating maintenance/repair/migration requiring owner-specific reconciliation; or
- stale/broken/manual invariant violation.

Do not generic-merge it automatically.

Touch sets remain useful evidence, but fixed claims define the authority boundary.

---

# 12. Close / absorption laws

## LAW 5.8-42 — ABSORPTION STARTS FROM EXACT FINAL CLOSED SOURCE

Campaign absorption uses the exact final CLOSED live source revision Lf.

No earlier active source, remembered snapshot or checkpoint substitutes for Lf.

## LAW 5.8-43 — CLOSED LIVE REMAINS CURRENT DURING ABSORPTION PREPARATION

Until the campaign absorption/route transition is actually accepted, current truth for Q remains selected closed E@Lf.

Campaign state prepared in memory is not current authority.

## LAW 5.8-44 — ONE CAMPAIGN TRANSACTION MATERIALIZES THE ABSORPTION BOUNDARY

Within one campaign publication domain, absorption SHALL use one coherent Step-5.6 campaign transaction containing all campaign-native consequences required to make the authority transfer honest, including as applicable:

- final native owner values/projections migrated from E;
- scene/current/index/routing changes;
- claim release/route clearing/replacement;
- exact absorbed live source evidence;
- required Step-5.2 recovery routing transitions;
- joined membership/controller/entity-transfer changes belonging to the same boundary;
- semantic history/evidence required synchronously by owner contract.

It SHALL NOT replay live commits one-by-one into campaign history.

## LAW 5.8-45 — ABSORPTION DOES NOT USE DISTRIBUTED ROLLBACK

If campaign publication fails/indeterminate:

- E@Lf remains real closed durable current truth while route still selects it;
- do not force-reopen E;
- do not force-rewind campaign/live refs;
- resolve actual current campaign authority under Step 5.6 and retry/reconcile forward.

## LAW 5.8-46 — ABSORPTION SUCCESS TRANSFERS CURRENT TRUTH FOR RELEASED CLAIMS

Only after current campaign authority proves compatible accepted absorption of exact E/Lf and routing no longer selects E for Q does campaign become current truth authority for released owners.

Old E remains closed, durable history/residue, non-authoritative for current play.

## LAW 5.8-47 — ABSORBED IDENTITY MUST BE SEMANTICALLY UNAMBIGUOUS

Idempotency evidence shall identify the absorbed live source strongly enough to distinguish at least:

```text
owning scene/scope
epoch identity
exact final live source revision
```

Existing `last_absorbed_live_head_sha` may participate but its field spelling is not itself canonical.

## LAW 5.8-48 — DUPLICATE ABSORPTION IS FORBIDDEN

Retry that proves exact final E/Lf already absorbed SHALL NOT apply its semantic deltas again.

It may complete routing/successor/cleanup work only.

---

# 13. Successor / rollover laws

## LAW 5.8-49 — SUCCESSOR IS A NEW EPOCH

Continued shared scene after close uses a fresh epoch identity/source with a freshly frozen claim set.

Old E never reopens.

## LAW 5.8-50 — AUTHORITATIVE SUCCESSOR SELECTION FOLLOWS ABSORPTION

Authoritative successor E2 is based on the actual current post-absorption campaign authority.

Do not require one absorption commit to embed/self-reference its own resulting commit SHA as E2 base.

Opening E2 is a later route selection transaction.

A short campaign-authoritative interval between epochs is valid and is not fictional downtime.

## LAW 5.8-51 — ROLLOVER MAY BE POLICY-DRIVEN BUT NOT HEARTBEAT-DRIVEN

Rollover may be justified by:

- claim-set change;
- state/envelope growth;
- scene concurrency topology change;
- entity transfer;
- membership/controller boundary;
- global/cross-scope synchronization;
- maintenance/recovery need.

No fixed turn count, elapsed wall-clock age or heartbeat alone requires rollover.

---

# 14. Membership/controller laws

## LAW 5.8-52 — PLAYER/CONTROLLER AUTHORITY IS NOT LIVE PARTICIPANT METADATA

`participant_ids` / `player_character_ids` describe scene/current state and may aid routing/context. They are not the sole gameplay authorization source.

Authorization remains current campaign/player/controller policy plus trustworthy acting principal.

## LAW 5.8-53 — REVOCATION AFFECTING ACTIVE LIVE AUTHORITY REQUIRES PRIOR SOURCE FENCE

Before acknowledging a player/controller revocation that removes current live write authority:

- every affected selected ACTIVE live source must be successfully CLOSED;
- no ordinary write by the soon-revoked principal may be allowed past that close fence.

## LAW 5.8-54 — ABSORPTION AND REVOCATION/TRANSFER JOIN ONE CAMPAIGN BOUNDARY WHEN COUPLED

After affected epoch(s) are closed, if live absorption and membership/controller transition together define the authorization edge, they SHALL publish in one campaign transaction.

Do not:

```text
absorb -> briefly restore campaign authority under old auth -> revoke later
```

because that opens an avoidable stale-write interval.

If the joined campaign transaction fails, the live source remains closed/current and the revocation/transfer is not acknowledged as complete.

## LAW 5.8-55 — WRITES THAT WIN BEFORE CLOSE ARE PRE-REVOCATION CURRENT STATE

If a valid old-authority live write wins CAS before the close fence:

- it is accepted under the then-current authorization;
- closer refreshes and closes from that newer state;
- final absorption includes it.

Do not retroactively erase it merely because revocation was concurrently requested.

## LAW 5.8-56 — WRITES THAT LOSE TO CLOSE CANNOT RETRY INTO OLD EPOCH

If close wins first, stale player write rejects exact revision. Refresh observes CLOSED and ordinary retry is forbidden.

## LAW 5.8-57 — MATERIAL LIVE PARTICIPANT/AUTH GRANTS USE SAFE EPOCH BOUNDARY WHEN NEEDED

A late join/reactivation/controller grant that changes the current live mutation/knowledge topology should use close/absorb + joined campaign transition + successor when necessary for coherent current semantics.

Pure observer/read capability that does not mutate live state may follow narrower access rules without necessarily forcing rollover.

---

# 15. Entity ownership transfer laws

## LAW 5.8-58 — OWNER CANNOT MOVE DIRECTLY BETWEEN TWO WRITABLE LIVE EPOCHS

Existing native owner X SHALL NOT become mutable in destination E2 while source E1 still has ordinary writable claim over X.

## LAW 5.8-59 — TRANSFER FREEZES EVERY MATERIALLY AFFECTED CURRENT LIVE SOURCE

If X transfers from E1 into a destination scene with current live E2 and E2's current shared state/claim topology is materially affected by X arrival/ownership:

- close E1;
- close E2;
- exact-pin both final sources;
- perform transfer/absorption on campaign/native stable basis;
- then select successors with new non-overlapping claims.

Freezing only E1 is insufficient when active E2 would otherwise continue from a base that excludes the transfer.

## LAW 5.8-60 — MULTI-LIVE TRANSFER MAY USE ONE CAMPAIGN-DOMAIN COHERENT BATCH

After all affected live sources are closed, their final results plus transfer may be absorbed/materialized in one campaign transaction where they share the same campaign publication domain.

No distributed transaction was required because all live sources were first made immutable current inputs.

---

# 16. Multi-scope/global event laws

## LAW 5.8-61 — CROSS-SCOPE MUTATION IS A SLOW BOUNDARY, NOT NORMAL HOT PATH

A rare event/process that genuinely requires mutation of owners currently claimed by several live sources SHALL not attempt ordinary distributed live commits.

## LAW 5.8-62 — FREEZE AFFECTED LIVE SOURCES BEFORE GLOBAL ESTABLISHMENT

Boundary protocol:

```text
identify affected scopes
-> close each required active live source via its own CAS
-> exact-pin all final current live inputs
-> reconcile/adjudicate semantics/chronology
-> publish coherent campaign/native transition
-> open successors if needed
```

The global event is not established merely because some sources were closed.

## LAW 5.8-63 — PARTIAL FREEZE IS RECOVERABLE AND NOT FICTIONAL ORDER

If crash occurs after only some live sources close:

- each closed source remains current frozen truth for its scope;
- unclosed sources remain current active truth for their scopes;
- unfinished global transition is not invented;
- authorized recovery resumes/abandons forward through absorption/successor;
- close order does not determine fictional chronology.

Step 5.9 owns final causal/time reconciliation.

---

# 17. External mutable dependency laws

## LAW 5.8-64 — READ DEPENDENCY DOES NOT AUTOMATICALLY TRANSFER OWNERSHIP

A live action may read campaign/native owner Y not in Q when Y's owner contract and current situation allow it to remain an external dependency.

## LAW 5.8-65 — CORRECTNESS-CRITICAL CONCURRENTLY MUTABLE EXTERNAL DEPENDENCY REQUIRES SYNCHRONIZATION

If Y can mutate independently and concurrent change can materially invalidate the live action's legality/stakes/result, ordinary live CAS alone cannot atomically fence Y.

Such a dependency requires a bounded cross-scope synchronization/chronology boundary appropriate to the owners involved.

Possible resolution may include closing/repartitioning/absorbing affected live scopes before establishing the dependent effect.

Do not claim every read dependency merely to avoid this rule.

## LAW 5.8-66 — GIT STORAGE ORDER DOES NOT RESOLVE CROSS-SOURCE FICTIONAL RACE

When current independent sources legitimately advance concurrently and their relative fictional order becomes material, Step 5.9 chronology/world rules resolve the relation. Git commit/ref write order is not the adjudicator.

---

# 18. Recovery/adoption laws

## LAW 5.8-67 — COLD LIVE RECOVERY STARTS FROM CURRENT CAMPAIGN ROUTING

Following Step 5.7:

1. pin current campaign authority H;
2. read bounded current live route/claims;
3. exact-resolve selected live source;
4. exact-pin live revision;
5. validate lifecycle/claims/auth/recovery closure;
6. classify capability/state.

Do not scan live branches to choose “latest.”

## LAW 5.8-68 — SELECTED ACTIVE LIVE SOURCE IS ADOPTABLE CURRENT AUTHORITY

If current route selects valid E and exact E state is ACTIVE:

- E is current truth for Q;
- cold runtime may adopt it after RRC/auth validation;
- ordinary writes use exact-revision CAS;
- another writer's existence does not require leader election.

## LAW 5.8-69 — SELECTED CLOSED LIVE SOURCE IS CURRENT BUT WRITE-FROZEN

If route selects valid E and E is CLOSED:

- E is current truth for Q;
- ordinary live gameplay mutation is blocked;
- authorized process may resume compaction/recovery;
- do not fall back to campaign base.

## LAW 5.8-70 — MISSING/INVALID SELECTED LIVE SOURCE BLOCKS DEPENDENT SCOPE

If current routing selects E but required source/state cannot be resolved/validated:

- current truth cannot be honestly established;
- affected scope is BLOCKED / integrity suspect under Step 5.7/INTEGRITY;
- no silent campaign fallback.

## LAW 5.8-71 — UNSELECTED LIVE SOURCE IS NOT RECOVERY AUTHORITY

A branch/source not selected by current campaign routing is ignored as current gameplay authority even if it appears plausible/newer.

It may be orphan/residue/repair evidence.

## LAW 5.8-72 — ROUTE/SOURCE MOVEMENT DURING RECOVERY CAUSES RETRY

Legitimate movement of campaign route or selected live source while cold recovery is pinning/hydrating causes bounded retry/reselection, not automatic corruption.

Persisted impossible lifecycle/overlapping claims at one stable current basis are integrity concerns.

---

# 19. Live-local recovery/root routing laws

## LAW 5.8-73 — LIVE SOURCE MAY HOST TYPED OPERATIONAL ROOTS WITHOUT OWNING THEM SEMANTICALLY

While live scope owns current representations of active Procedure/Command/Resolution/Continuation/temporal owners, Step-5.2 typed recovery routing for those owners may be live-local/partitioned.

Cold recovery must enumerate them from the selected current live source/route as required.

## LAW 5.8-74 — ABSORPTION MOVES/REKEYS RECOVERY ROUTING WITH OWNER LIFECYCLE

When live owners return to campaign durability domain or terminate during absorption, required Step-5.2 routing/root-enrollment consequences must join the same durability closure strongly enough to avoid owner/routing split.

## LAW 5.8-75 — LIVE PHYSICAL ENVELOPE IS NOT A GENERIC PENDING-WORK REGISTRY

Do not solve recovery by adding untyped `pending[]`/job state to LIVE_STATE.

Native execution/temporal owners and their stable identities remain authoritative.

---

# 20. Knowledge/disclosure laws

## LAW 5.8-76 — OBJECTIVE TRUTH, FICTIONAL KNOWLEDGE AND HUMAN DISCLOSURE REMAIN DISTINCT IN LIVE STORAGE

Physical live atomicity may co-locate updates/evidence, but semantic authority remains Step 4:

```text
objective current/lore owner
world.knowledge
runtime.disclosure
```

## LAW 5.8-77 — PERCEPTION EVIDENCE DOES NOT AUTOMATICALLY MEAN HUMAN DELIVERY

A live observable/perception event may establish/justify fictional knowledge. It does not prove host delivery to the human player.

Human disclosure advances only under Step-4 / Step-5.12 delivery rules.

## LAW 5.8-78 — CURRENT LEGACY `known_by_pc_ids` IS NOT A SECOND KNOWLEDGE OWNER

Machine realization shall migrate/replace current live knowledge shorthand so it represents Step-4 native knowledge state/evidence rather than parallel current authority.

## LAW 5.8-79 — COMPACTION ROUTES EACH INFORMATION CATEGORY TO ITS NATIVE OWNER

Absorption SHALL materialize objective, epistemic, semantic-event and disclosure-related consequences according to their native ownership/durability rules.

Do not flatten them into one live fact record in campaign.

---

# 21. Integrity laws

## LAW 5.8-80 — STALE LIVE STATE IS NOT CORRUPTION

A stale cached live head, CAS rejection or legitimate route movement is normal concurrency and uses refresh/retry semantics.

## LAW 5.8-81 — PERSISTED DUAL CLAIM OR ROUTE-AWAY-WITHOUT-FREEZE IS INTEGRITY EVIDENCE

At a stable current basis, examples of suspect/corrupt state include:

- two selected live routes claim same nondecomposed owner;
- campaign route no longer selects E but E was superseded without required close/absorption evidence;
- current route selects missing required E;
- route says E active but exact source/lifecycle is irreconcilable;
- campaign and selected live both claim current writable ownership of same owner.

Diagnose boundedly; do not choose convenient source by timestamp.

## LAW 5.8-82 — MANUAL/OUT-OF-PROTOCOL GIT MUTATION IS NOT A NORMAL CONCURRENCY MODEL

HDM logical correctness assumes repository mutations follow Python/RepositoryPort policy.

Unexpected manual/force/invariant-breaking writes may become integrity/repair input. Ordinary hot path SHALL NOT add broad global checks solely to defend against an administrator intentionally bypassing the application.

---

# 22. Performance laws

## LAW 5.8-83 — NORMAL ACTIVE LIVE TURN DOES NOT REQUIRE CAMPAIGN HEAD REFRESH SOLELY FOR FENCING

Legal route-away/revocation must first change current live source to CLOSED. Therefore live ref probe already observes the fence.

Do not add campaign route/auth reread on every active live turn solely to detect a legal ownership transfer.

Campaign read is required when:

- live source is CLOSED and routing must be resolved;
- action needs external mutable campaign dependency;
- opening/adoption/cold recovery;
- explicit resync/integrity suspicion;
- maintenance/global boundary.

## LAW 5.8-84 — UNCHANGED ACTIVE LIVE READ SHOULD REQUIRE ONLY CURRENT LIVE REF PROBE

With valid cached route/state and no external dependency:

```text
unchanged shared-state-dependent action/observation
    -> one live ref/head probe
```

## LAW 5.8-85 — CHANGED LIVE HEAD LOADS ONLY CURRENT LIVE SOURCE BY DEFAULT

If ref changed:

- fetch exact selected live source at that head;
- no ordinary full history/compare/campaign scan merely to synchronize.

## LAW 5.8-86 — ONE LOGICAL SHARED MUTATION -> ONE LIVE SOURCE PUBLICATION

Internal mechanics may have many steps; one shared established result uses one atomic live source transition when possible.

No heartbeat/no-op write if shared state did not change and no correctness boundary requires a publication.

---

# 23. RepositoryPort semantic requirements

Step 5.8 requires deterministic Python core a transport capability conceptually supporting:

```text
LiveSourceRead(ref) -> exact current revision + payload identity

LiveSourceCAS(
    ref,
    expected_revision,
    complete_new_source_state,
    acting_principal,
    operation_kind
) -> ACCEPTED | REJECTED | INDETERMINATE
```

`operation_kind` at minimum distinguishes ordinary gameplay mutation from close/maintenance because lifecycle/auth policy differs.

The architecture does not mandate exact API implementation.

Suitable future backends may use:

- GitHub `createCommitOnBranch(expectedHeadOid)` style primitive;
- create tree/commit + non-force ref update;
- one-file Contents expected blob fallback while physical model remains one file.

Correctness belongs to expected source revision + Python policy, not LLM choreography.

---

# 24. State-transition tables

## 24.1 Opening

| State | Current truth | Ordinary writes | Action |
|---|---|---|---|
| campaign no route | campaign | campaign policy | derive Q, prepare E |
| prepared E unselected | campaign | campaign policy | attempt campaign route selection |
| selected E ACTIVE | E | live CAS | adopt/play |
| candidate loses campaign CAS | current actual route/source | according to current | revalidate; candidate orphan/reuse only if exact-compatible |

## 24.2 Active write

| Outcome | Meaning | Next |
|---|---|---|
| ACCEPTED | live mutation durable/current at returned revision at that moment | adopt returned source; reveal shared result |
| REJECTED stale, current ACTIVE disjoint | another write won | refresh, reapply/retry boundedly |
| REJECTED stale, current ACTIVE overlapping | assumptions moved | native revalidation/re-resolution |
| REJECTED stale, current CLOSED | fence won | no gameplay retry; routing/compaction path |
| INDETERMINATE | unknown whether mutation published | verify current source/lineage/semantic receipts |

## 24.3 Close

| Outcome | Meaning | Next |
|---|---|---|
| ACCEPTED | exact E frozen at Lf | prepare absorption |
| REJECTED current ACTIVE | another writer won first | refresh, retry close boundedly |
| current CLOSED same intended close | close already effective | continue absorption |
| INDETERMINATE | unknown | verify exact current source/lifecycle before route-away |

## 24.4 Absorption

| Current campaign observation | Meaning |
|---|---|
| route still selects E closed, no compatible absorbed E/Lf | E remains current; compaction pending |
| campaign current proves E/Lf absorbed and route released/replaced | campaign/new route current; E nonauthority |
| impossible/missing/conflicting route/absorption state | retry/integrity block |

---

# 25. Crash-window matrix

## C1 — candidate branch/source created, route selection never sent

Nonauthority orphan. Campaign remains current.

## C2 — route selection sent, ACK lost

Read current campaign route. If it selects exact E/Q compatibly, E authority selected; otherwise candidate nonauthority/retry.

## C3 — route selects E, host crashes before gameplay

Cold host adopts exact active E from current routing.

## C4 — live gameplay CAS request lost/ACK unknown

Verify current E lineage/semantic receipts. Do not reroll/replay blindly.

## C5 — close request lost/ACK unknown

Verify current E. Do not route away until close proven.

## C6 — close accepted, host crashes before campaign absorption

Current route selects CLOSED E. Cold recovery classifies current truth valid/write-frozen and resumes compaction.

## C7 — absorption campaign tree/commit prepared but ref not advanced

E closed remains current. Prepared campaign objects nonauthority.

## C8 — absorption ref update ACK lost

Resolve current campaign authority under Step 5.6. Route/absorbed tuple decides current truth.

## C9 — absorption accepted, host crashes before old live branch cleanup

Campaign current; E closed nonauthority residue. No duplicate absorption; cleanup deferred.

## C10 — absorption accepted, successor not opened

Campaign current. If shared scene still requires live mode, next authorized session opens/adopts fresh E2 before shared mutation.

## C11 — successor candidate prepared but route selection fails

Campaign remains current; candidate nonauthority.

## C12 — revocation requested, player write wins before close

Write accepted pre-fence. Closer refreshes/closes; joined absorption+revocation includes accepted state.

## C13 — revocation close wins before stale player write

Stale player CAS rejects; no retry into E. Joined campaign boundary applies revocation.

## C14 — two live sources partly frozen for global event, crash

Each closed source remains current frozen truth; active ones remain active. Global event unestablished. Recovery resumes/forwards boundary.

---

# 26. Explicit save interaction

Step 5.5 explicit save may require dirty/live state across multiple native domains.

For active live source with already durable accepted shared mutations, save does not need to absorb merely to say that live state is durable, unless selected save policy/product semantics explicitly require campaign consolidation.

Successful save may compose:

```text
campaign current durable source
+
active live exact durable source(s)
+
required operational durable sources
```

provided resulting RRC satisfies save promise.

If save policy chooses/needs absorption/ownership transition, Step-5.8 close/absorption semantics apply.

No distributed transaction is introduced.

---

# 27. Host handoff interaction

Controlled host handoff does not require transferring a live leader because no leader exists.

For an active live epoch:

- accepted shared mutations are already live-durable before reveal;
- Step-5.2 live-local operational roots/dependencies required for promised RRC must be durable/recoverable;
- new host resolves current campaign route + current exact live source;
- old host's cached head loses authority as soon as another source revision advances/close occurs.

If controlled handoff policy requires freezing a scope for some reason, it can use terminal close/absorption, but handoff alone does not require unnecessary rollover when native RRC is already safe.

---

# 28. Chronology handoff to Step 5.9

Step 5.8 supplies:

- exact live source identities/revisions;
- native event/execution identities;
- claim/source lifecycle;
- final frozen sources for cross-scope reconciliation;
- no implicit order across live domains.

Step 5.9 must decide:

- local live scene chronology evidence;
- how concurrent independent live/campaign events become ordered only when material;
- contested/simultaneous cross-scene effects;
- chronology evidence retained after live absorption;
- temporal owner due decisions across live/campaign sources.

Step 5.8 SHALL NOT use Git write order as a chronology shortcut.

---

# 29. Machine-realization debt identified

Current GAME/schema/tests will need later implementation planning for at least:

- explicit current LiveRoute mutation claims;
- claim-overlap validation;
- typed owner refs beyond only `touched_entity_ids`;
- Python RepositoryPort live expected-head CAS primitive/outcomes;
- source-head rather than integer revision correctness;
- LIVE_STATE typed native-owner envelope or equivalent;
- live-local Step-5.2 recovery routing;
- Step-4 `world.knowledge` realization replacing `known_by_pc_ids` as parallel authority;
- exact absorbed epoch/final-source idempotency evidence;
- joined close/absorb/revocation/controller-transfer protocol;
- destination-freeze entity transfer cases;
- indeterminate live ACK tests;
- route-away-without-close integrity tests;
- overlapping live claim corruption tests;
- external mutable dependency slow-path tests;
- no per-turn campaign auth reread performance tests;
- manual two-session end-to-end smoke/failure-injection tests.

Existing LIVE_SCENE cases should be retained/refined rather than discarded.

---

# 30. Candidate rejected alternatives

## Leader/lease

Rejected: host mismatch, liveness/TTL complexity, still requires fencing, no measured need.

## Generic monotonic fencing token

Rejected: cannot atomically validate campaign-side token with independent live ref without coordinator; copied token adds no protection beyond source close/revision; risks new global sequence.

## Scene membership alone as ownership

Rejected: insufficient machine-decidable authority for typed nonphysical owners and cross-scene overlaps.

## Retrospective touched-set ownership

Rejected: detects claim only after possible split authority.

## Dynamic per-owner live claim transfer

Rejected baseline: nested cross-domain authority transfer in ordinary path; high recovery/TOCTOU complexity.

## Global `entity -> live_epoch` writable authority table

Rejected baseline: extra hotspot/duplicate consistency surface. May be a derived routing index only if scale evidence later demands it.

## Distributed transaction across live refs

Rejected: freeze inputs then one stable campaign/native transition on slow path.

---

# 31. Candidate exit assertions

If this candidate survives adversarial review, Step 5.8 should be able to assert:

```text
A. one current truth source is decidable for every live claim;
B. no more than one ordinary writable source exists;
C. zero-writer frozen intervals are explicit and recoverable;
D. stale writers fail expected-source CAS after any accepted mutation/freeze;
E. legal route-away cannot leave old live source ACTIVE;
F. no heartbeat/lease/leader is required;
G. live claim scope is explicit, typed, bounded and immutable per epoch;
H. campaign writers cannot lawfully mutate live-claimed owners;
I. opening races converge through campaign CAS;
J. close/absorption crash windows have deterministic forward recovery;
K. membership/controller revocation has no reopened old-auth write window;
L. entity transfer cannot produce two writable live owners;
M. multi-scope events use freeze/reconcile slow path, not distributed transactions;
N. cold recovery selects live authority without age/timestamp heuristics;
O. Step-4 information owners and Step-3/5.2 operational owners survive physical live packing;
P. ordinary hot path remains one live ref probe plus optional exact fetch/CAS;
Q. Git order never decides fictional chronology.
```

---

# 32. Adversarial-review targets

Before canonicalization, attack at minimum:

1. concurrent opening with overlapping/disjoint Q;
2. stale campaign writer versus newly selected Q;
3. active live mutation versus close;
4. close ACK lost;
5. live mutation ACK lost + later descendant write;
6. close succeeds but campaign route manually/mistakenly moves inconsistently;
7. campaign absorption stale-head disjoint/overlap;
8. absorption ACK lost;
9. duplicate absorption;
10. revocation/controller transfer races;
11. late join while live active;
12. entity transfer into already-active destination;
13. global event with partial freeze crash;
14. active Procedure/Continuation owner inside live source;
15. independently-due temporal owner while live closes;
16. Step-4 PC knowledge + human disclosure split on failed host emission;
17. external mutable campaign dependency races live action;
18. repeated contention/performance degradation;
19. multiple active live routes scaling/claim discovery;
20. force/manual repository mutation and integrity classification;
21. explicit save while multiple live sources active;
22. controlled handoff while live source active;
23. successor preparation/opening race;
24. orphan branch/source GC dependency boundary.

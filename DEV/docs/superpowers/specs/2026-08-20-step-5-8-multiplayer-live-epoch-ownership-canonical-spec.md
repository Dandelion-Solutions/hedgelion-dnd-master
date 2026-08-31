# Step 5.8 — Multiplayer / Live-Epoch Ownership — Canonical Specification

Status: **CANONICAL — STEP 5.8 ARCHITECTURE CLOSED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Canonical architecture direction:

> **ROUTED FIXED-CLAIM LIVE EPOCH / EXACT-SOURCE CAS / TERMINAL SOURCE FREEZE / FORWARD CAMPAIGN ABSORPTION**

Canonicalization basis:

- `../design/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-task-brief.md`
- `../design/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-research-draft.md`
- `../design/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-analytical-challenge.md`
- `../design/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-candidate-spec.md`
- `../design/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-adversarial-review.md`
- `../design/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-resolution-gate.md`

This specification defines temporary multiplayer/live mutable-authority ownership, fencing, close/absorption and recovery semantics on top of canonical Steps 3, 4 and 5.1–5.7.

It does not implement runtime/schema/Python transport changes and does not define final fictional chronology (5.9), Story/transcript/delivery policy (5.10–5.12), GC (5.13) or host/deployment implementation (6).

---

# 1. Canonical model

HDM multiplayer uses a scene-centered temporary native durability/synchronization partition selected by current campaign routing.

```text
CURRENT CAMPAIGN AUTHORITY H
        |
        | LiveRoute(scene/scope S, epoch E, immutable claims Q)
        v
LIVE EPOCH E
    ACTIVE @ exact source revision L
        |
        | authorized exact-source CAS transitions
        v
    ACTIVE @ L+n
        |
        | terminal close CAS
        v
    CLOSED @ exact final revision Lf
        |
        | current truth remains live
        | ordinary gameplay writes forbidden
        v
ONE FORWARD CAMPAIGN ABSORPTION / TRANSITION TXN
        |
        v
CURRENT CAMPAIGN AUTHORITY C
        |
        +--> optional later successor epoch E2
```

Core invariant:

```text
for every claimed native owner / writable partition:
    exactly one current truth authority is decidable
    and at most one ordinary writable authority exists
```

`CLOSED_UNABSORBED` intentionally has zero ordinary writable authorities.

No long-lived host leader, TTL lease, heartbeat, distributed transaction, global fencing counter or universal cross-domain frontier is introduced.

---

# 2. Vocabulary

## LiveRoute

Current campaign-domain routing evidence selecting one live epoch for a bounded scene-centered mutation partition.

Conceptually identifies:

```text
scene/scope identity
epoch identity
live source identity/ref
base campaign revision identity
immutable typed mutation claims Q
minimum provenance/routing data required for validation/recovery
```

Routing is not copied owner state.

## Mutation claim

A typed native owner or owner-defined writable-partition reference saying that ordinary current mutation of that owner/partition is admitted through E and not through campaign/another live epoch while E remains selected.

A claim is not:

- a copy of state;
- read permission;
- player ACL;
- TTL lock;
- global sequence;
- retrospective touch evidence.

## Source revision fence

The exact current revision/HEAD of the live native source expected by one prepared transition. It is the CAS fence.

## Current truth authority

The source that must be consulted for current state of the claimed owner/partition.

## Ordinary write admission

Whether ordinary gameplay mutation is allowed against that current truth authority.

A source may be current truth while write-frozen.

---

# 3. Authority laws

## LAW 5.8-1 — ROUTING SELECTS LIVE AUTHORITY; SOURCE EXISTENCE DOES NOT

A live source becomes current authority only when current valid campaign/native routing selects it.

Branch/source existence, age, name, timestamp, remembered chat state, checkpoint reference or prepared objects do not establish authority.

## LAW 5.8-2 — EXACTLY ONE CURRENT TRUTH AUTHORITY

For every owner/partition claimed by current selected E, current truth resolves through E until a valid forward transfer/absorption changes routing.

Campaign base data remains base/reference/dependency state, not fallback current truth.

## LAW 5.8-3 — AT MOST ONE ORDINARY WRITABLE AUTHORITY

No claimed owner/partition is ordinarily writable through campaign and live simultaneously or through two selected live epochs simultaneously.

`CLOSED_UNABSORBED` has current truth authority = closed live source and ordinary writable authority = none.

## LAW 5.8-4 — PHYSICAL LIVE PACKING DOES NOT CHANGE SEMANTIC OWNERS

Live source is a physical/native durability and synchronization partition, not a semantic mega-owner.

Native ownership remains, including:

```text
PC/actor state          -> native world actor owner
asset/item state        -> native world asset owner
Procedure state         -> runtime.procedure
Resolution state        -> runtime.resolution
Continuation            -> runtime.continuation
fictional knowledge     -> world.knowledge
objective lore          -> world.lore_fact
human disclosure        -> runtime.disclosure
```

Physical co-location does not duplicate or replace those owners.

## LAW 5.8-5 — CURRENT CLAIMS ARE WRITE-AUTHORITY ROUTING EVIDENCE

Existing native owner/partition X may be ordinarily mutated through E only when X belongs to Q(E), unless X's lifecycle validly begins inside E as an epoch-local new owner.

Ordinary campaign mutation of X is admitted only when bounded current routing proves X is not live-claimed.

## LAW 5.8-6 — SELECTED CLAIM SET IS IMMUTABLE FOR ONE EPOCH

Q(E) does not expand or shrink while E remains the same selected active/closed-unabsorbed epoch.

Changing write ownership requires a lifecycle boundary:

```text
close/freeze affected epoch(s)
-> campaign absorption/transition
-> optional successor epoch(s) with new claims
```

No normal dynamic per-owner claim acquisition/release occurs inside one epoch.

## LAW 5.8-7 — CLAIMS ARE TYPED OWNER/PARTITION REFERENCES

A claim may be:

```text
exact native owner reference
OR
native-owner-defined typed writable partition reference
```

only where the native owner contract provides deterministic membership, non-overlap/disjointness, mutation admission and recovery routing.

Step 5.8 introduces no generic selector/query language for claims.

## LAW 5.8-8 — SELECTED CLAIMS DO NOT OVERLAP

Current selected live routes SHALL NOT claim overlapping mutable owner/partition authority.

Persisted overlap is an integrity defect, not last-writer-wins semantics.

## LAW 5.8-9 — NO IMPLICIT CLAIM GRAPH CLOSURE

Claiming owner X does not claim every owner/reference reachable from X.

Read/reference/recovery dependencies remain under native owner and Step-5.2 closure rules.

---

# 4. Bounded authority routing and containment

## LAW 5.8-10 — WRITE AUTHORITY LOOKUP IS BOUNDED AND MACHINE-DECIDABLE

For every owner/partition class admitted to live mutation, current write-authority routing supports a bounded deterministic operation equivalent to:

```text
WriteAuthorityLookup(X)
    -> CAMPAIGN
     | LIVE(epoch/ref)
     | INTEGRITY_CONFLICT
```

Campaign mutation admission and new-route overlap checks SHALL NOT require scanning the campaign/world/all live branches.

Physical realization may use native routing, compact typed claim indexes or another bounded owner-specific mechanism.

Such routing is derivative evidence, not copied owner state.

## LAW 5.8-11 — ROUTE AND DERIVATIVE CLAIM INDEX CHANGE COHERENTLY

If a materialized routing/index structure is required for bounded claim lookup, selection/release of the route and required routing/index updates join the same campaign authority transaction strongly enough to prevent a healthy durable route/index split.

## LAW 5.8-12 — LIVE CONTAINMENT ADMISSIBILITY

Native owner/partition X may be claimed by E only when:

```text
WritableScope(X) is fully contained by MutationPartition(E)
```

and that containment is machine-decidable under X's owner contract.

A Procedure, temporal/global owner or other owner spanning multiple live partitions remains in its own native partition or triggers explicit cross-scope synchronization/repartition.

Physical presence inside LIVE_STATE does not establish containment.

## LAW 5.8-13 — CLAIM SET IS BOUNDED TO PRACTICAL MUTATION HORIZON

Opening selects the smallest practical existing owner/partition set that can reasonably require synchronized current mutation in the shared actionable scene horizon.

Do not claim arbitrary world graph, all lore/knowledge/history or all referenced owners.

Read-only dependencies do not require claims merely because they are read.

---

# 5. Live-born identity

## LAW 5.8-14 — LIVE HOT PATH DOES NOT DEPEND ON CAMPAIGN ALLOCATOR MUTATION

Identities first made durable inside independent live epochs SHALL NOT require a campaign allocator write merely to become globally unique.

## LAW 5.8-15 — LIVE-BORN STABLE IDS USE A COLLISION-FREE EPOCH-QUALIFIED NAMESPACE

An accepted live-born identity that must survive external references is derived from stable epoch identity plus a source-local accepted creation coordinate and kind/equivalent collision-free data.

Properties:

- allocation is established in the same accepted live source transition as creation;
- competing candidates prepared from one prior revision are serialized by CAS;
- rejected prospective IDs are noncanonical;
- accepted IDs do not rekey merely because E later absorbs into campaign;
- local ordinals imply no cross-epoch order.

## LAW 5.8-16 — ACCEPTED EXECUTION/IDEMPOTENCY IDENTITIES ARE STABLE

RuntimeCommand/Resolution/Procedure/Continuation/receipt/firing/other accepted execution identities that participate in durable causal/idempotency evidence SHALL NOT be reallocated on live retry, recovery or absorption.

## LAW 5.8-17 — PROVISIONAL WORLD IDENTITY IS OWNER-CONTRACT-BOUND

A live-born world entity may use provisional/rekeyable identity only when its native promotion contract explicitly permits it and no durable external reference requiring stable identity escapes before promotion.

---

# 6. Writer and fencing model

## LAW 5.8-18 — NO LONG-LIVED LIVE LEADER

Several authorized sessions may concurrently attempt writes against one selected ACTIVE source.

Correctness is serialized by exact-source CAS, not elected host leadership.

## LAW 5.8-19 — EVERY AUTHORITATIVE LIVE TRANSITION EXPECTS EXACT PRIOR SOURCE REVISION

Every live transition, including gameplay mutation and close, conditions publication on the exact current source revision accepted by the attempt.

Conceptually:

```text
CAS(E, expected L, complete new source state)
 -> ACCEPTED(new exact revision)
  | REJECTED(...)
  | INDETERMINATE
```

## LAW 5.8-20 — EXACT SOURCE REVISION IS THE FENCE

A source-local integer `revision` may exist for diagnostics or within-epoch metadata, but it does not replace the exact Git/native source revision/HEAD as mutation fence and is not globally comparable.

## LAW 5.8-21 — NO TTL/HEARTBEAT CORRECTNESS DEPENDENCY

Ordinary live correctness does not depend on wall-clock lease expiry, keepalive, online-presence detection, background polling or heartbeat commits.

## LAW 5.8-22 — APPLICATION AUTHORIZATION IS DISTINCT FROM CAS

Technical repository write ability and successful CAS are insufficient without current HDM application authorization and correct owner/route admission.

The acting principal/delegation requirements from Step 5.6 continue to apply.

---

# 7. Live lifecycle and terminal freeze

## LAW 5.8-23 — LIVE EPOCH LIFECYCLE IS MONOTONIC ACTIVE -> CLOSED

Baseline lifecycle:

```text
ACTIVE -> CLOSED
```

`CLOSED` is terminal for E. The same epoch does not reopen.

## LAW 5.8-24 — ACTIVE = CURRENT TRUTH + ORDINARY CAS WRITES

When current routing selects E and E is ACTIVE, E is current truth for Q(E), and authorized ordinary live transitions may CAS-publish against exact current source revision.

## LAW 5.8-25 — CLOSED = CURRENT TRUTH + ZERO ORDINARY GAMEPLAY WRITES

When current routing still selects CLOSED E:

- E remains current truth for Q(E);
- ordinary gameplay writes to E are forbidden;
- campaign is not yet current truth for Q(E);
- compaction/recovery may read exact final E;
- cold recovery may resume absorption.

## LAW 5.8-26 — CLOSE IS ITSELF AN EXACT-SOURCE CAS TRANSITION

If gameplay writer wins first, close revalidates/retries from newer accepted live state.

If close wins first, stale ordinary gameplay write rejects and may not retry after observing CLOSED.

## LAW 5.8-27 — ROUTE-AWAY REQUIRES CONFIRMED CLOSED SOURCE

Normal conforming authority transfer SHALL NOT clear/replace selected E while E remains ACTIVE.

Before route-away/absorption/revocation/claim transfer, E must be confirmed/verified CLOSED at exact final revision Lf.

A persisted route-away from an ACTIVE prior selected source without valid transfer evidence is integrity suspect for affected scope.

## LAW 5.8-28 — CLOSED EPOCH IS NEVER REOPENED TO ABORT MAINTENANCE

If a transfer/maintenance operation closes E then later fails, E remains CLOSED. Resume by forward recovery/absorption and optional successor creation, never `closed -> active`.

---

# 8. Native transition granularity

## LAW 5.8-29 — LIVE ATOMICITY IS PER NATIVE DURABILITY EDGE, NOT PER USER ACTION

Each native execution/lifecycle edge that establishes live-owned durable state publishes one complete source transition.

No one such edge is split into partial per-field/per-owner writes for convenience.

A single user interaction may legitimately span several live transitions when Step-3 execution, external choice/reaction or Step-4/5.12 delivery semantics define multiple durable edges.

## LAW 5.8-30 — CLOSE DOES NOT CANCEL ALREADY ACCEPTED NATIVE EXECUTION

Terminal close fences future ordinary mutation but does not revoke already committed RuntimeCommand/Resolution/Procedure/Continuation/fixed RNG/receipt/temporal evidence.

Prospective unpublished work may lose the close race and remain unestablished.

Accepted durable owners/evidence survive in final E and through absorption/next native partition according to native lifecycle.

## LAW 5.8-31 — STALE CAS FAILURE NEVER REPLAYS ACCEPTED GAMEPLAY BY DEFAULT

A live conflict/retry does not reroll accepted RNG, replace accepted IDs or replay already committed execution semantics merely because repository/source currentness changed.

Step-3 idempotency/causal contracts govern.

---

# 9. Live shared mutation protocol

For a cached selected ACTIVE E at known exact revision L:

1. synchronize current E when the action/observation is race-sensitive;
2. if E changed, pin/fetch exact current live source state;
3. if E is CLOSED, ordinary mutation stops and routing/absorption/recovery is followed;
4. validate acting principal, claims/containment and bounded mutable dependencies;
5. resolve intent/rules/randomness/consequence under Step 3 from exact current owners and accepted dependencies;
6. freeze one native atomic transition plus dependency/touch footprint;
7. CAS expected L -> complete new source state;
8. only after confirmed compatible publication may a shared consequence cross its write-before-reveal edge.

## LAW 5.8-32 — LEGAL ROUTE-AWAY DOES NOT REQUIRE CAMPAIGN HEAD CHECK ON EVERY LIVE TURN

Because legal route-away first changes the selected live source to CLOSED, an ordinary live synchronization probe can discover authority withdrawal without mandatory campaign ref read on every shared turn.

Campaign routing is re-read when live lifecycle/routing state requires it or another bounded dependency requires campaign synchronization.

## LAW 5.8-33 — TOUCH EVIDENCE DOES NOT CREATE AUTHORITY

Retrospective `touched_*`/dependency evidence supports conflict/absorption analysis but cannot dynamically establish claims.

---

# 10. Publication outcomes and ambiguity

## LAW 5.8-34 — LIVE AUTHORITY-CHANGING TRANSPORT EXPOSES ACCEPTED / REJECTED / INDETERMINATE

Request dispatch alone never proves shared state establishment.

## LAW 5.8-35 — CONFIRMED STALE REJECTION INVALIDATES THE PREPARED SOURCE SNAPSHOT

After stale expected-source rejection, refresh/pin current E, classify lifecycle/dependency overlap and revalidate. Do not blind overwrite/retry.

## LAW 5.8-36 — CURRENT CLOSED SOURCE TERMINATES ORDINARY RETRY

If refresh observes CLOSED, do not retry ordinary gameplay write against E.

Any consequence not durably established before close is not shared canon merely because a host had computed it.

## LAW 5.8-37 — AMBIGUOUS LIVE PUBLICATION USES BOUNDED EXACT SOURCE/LINEAGE VERIFICATION

After an indeterminate live publication:

- do not narrate/ack the shared result by assumption;
- do not replay accepted gameplay by assumption;
- resolve current exact source and bounded lineage/identity evidence;
- distinguish historical inclusion of intended transition from current values;
- adopt current compatible state when proven;
- never force stale state over newer authority.

This mirrors Step-5.6 epistemic-outcome discipline.

---

# 11. Opening and successor epochs

## LAW 5.8-38 — PREPARED LIVE SOURCE IS NON-AUTHORITATIVE UNTIL ROUTE SELECTION

Opening may prepare candidate source/branch E, but it becomes authority only when a valid campaign authority transaction selects its route/claims.

Prepared abandoned source is orphan infrastructure, not gameplay truth.

## LAW 5.8-39 — OPENING CLAIM OVERLAP IS VALIDATED THROUGH BOUNDED ROUTING

The campaign route-selection transaction verifies no current selected claim overlaps Q(E) and that each claimed owner/partition is live-containment-admissible.

Concurrent overlapping openings serialize on campaign Step-5.6 CAS; loser revalidates and may not transport-only rebase through material authority conflict.

## LAW 5.8-40 — SUCCESSOR OPENS ONLY AFTER PREDECESSOR ABSORPTION IS CURRENT

Normal sequence:

```text
E1 CLOSED @ Lf
-> campaign absorption C becomes current
-> prepare E2 from C
-> select E2 by later campaign route transaction
```

Do not create self-referential successor-base semantics tied to the same containing campaign commit.

---

# 12. Campaign absorption / authority transfer

## LAW 5.8-41 — ABSORPTION IS FORWARD CAMPAIGN PUBLICATION

After E is CLOSED at exact Lf, campaign absorption materializes current live-owned state/evidence into appropriate native campaign/next partitions using one Step-5.6 campaign transaction for the affected campaign-domain closure.

## LAW 5.8-42 — CAMPAIGN DOES NOT BECOME CURRENT FOR Q(E) UNTIL ABSORPTION SUCCEEDS

Close alone does not move truth authority back to campaign.

## LAW 5.8-43 — ABSORPTION PRESERVES NATIVE OWNER IDENTITIES AND LIFECYCLES

Absorption changes physical/current durability partition, not semantic owner identity.

Accepted execution, knowledge, disclosure, temporal and world owner state remain with their native owners.

## LAW 5.8-44 — ABSORPTION RETRIES ARE IDEMPOTENT BY NATIVE/FINAL SOURCE IDENTITY

Retry must not duplicate accepted gameplay/event/effect semantics merely because campaign publication conflicted or acknowledgement was lost.

## LAW 5.8-45 — SUCCESSFUL CAMPAIGN ABSORPTION IS NOT ROLLED BACK TO EMULATE CROSS-DOMAIN ATOMICITY

If another independent domain subsequently fails, successful current campaign publication remains real under Steps 5.5–5.7.

---

# 13. Recovery/adoption

## LAW 5.8-46 — COLD RECOVERY STARTS FROM CURRENT CAMPAIGN ROUTING

Step 5.7 pins current campaign authority and resolves current live route(s).

Branch names, timestamps, checkpoint age and cached chat memory never choose live authority.

## LAW 5.8-47 — ACTIVE LIVE SOURCE IS ADOPTABLE WITHOUT LEADER TAKEOVER

A cold host may recover current E, exact-pin current source revision, hydrate required owners/RRC and participate as another authorized CAS writer. No leader lease transfer is required.

## LAW 5.8-48 — CLOSED_UNABSORBED IS A NORMAL RECOVERABLE TRANSFER STATE

Recovery treats closed selected E as current truth and resumes/coordinates campaign absorption; it does not fall back to older campaign base or reopen E.

## LAW 5.8-49 — MISSING/CONTRADICTORY SELECTED LIVE SOURCE BLOCKS/SUSPECTS AFFECTED SCOPE

Do not silently use campaign base as current truth when current route says live owns the scope.

## LAW 5.8-50 — SOURCE MOVEMENT DURING RECOVERY IS NORMAL CONCURRENCY UNTIL PROVEN OTHERWISE

Bounded retry/revalidation applies; movement alone is not corruption.

---

# 14. SAVE and handoff

## LAW 5.8-51 — EXPLICIT SAVE DOES NOT AUTOMATICALLY CLOSE ACTIVE LIVE EPOCHS

Active shared state is normally already durable through live write-before-reveal publication.

For a save including live partitions, ensure every selected established recovery-relevant generation is durable, then final-validate current route/exact source composition and prove Step-5.2 RRC.

## LAW 5.8-52 — LIVE ADVANCEMENT DURING SAVE IS NOT FAILURE BY ITSELF

New accepted shared live state is itself durable. Save succeeds when the final current composed source set satisfies the selected Step-5.5 promise.

No global scalar save cut or cross-domain total order is invented.

## LAW 5.8-53 — CONTROLLED HANDOFF TRANSFERS RECOVERABLE STATE, NOT LEADERSHIP

Before handoff acknowledgement, every promised current live state and accepted in-flight input/execution that must survive is materialized in native recoverable sources/evidence.

Prospective unaccepted work need not survive.

Receiving host recovers current authority normally and gains no exclusive lease.

---

# 15. Authorization / membership / controllers

## LAW 5.8-54 — REVOCATION OF ACTIVE LIVE AUTHORITY CLOSES AFFECTED EPOCH FIRST

If membership/controller change removes authority relevant to current E, first terminally close the affected source by exact CAS.

## LAW 5.8-55 — ABSORPTION AND REMOVING AUTHORIZATION SHARE ONE CAMPAIGN TRANSITION WHEN THEY FORM ONE BOUNDARY

After close, one campaign transaction SHALL, as required:

```text
absorb/finalize E
change PLAYER/controller authorization
clear/replace live route/claim routing
update required recovery/index state
```

Do not absorb first and revoke in a later commit that reopens an authorization window.

## LAW 5.8-56 — PLAYER WRITE WINNING BEFORE CLOSE REMAINS REAL

If an authorized player live transition wins CAS before revocation close, that accepted state is real. Close retries from new current source.

If close wins, stale ordinary player write rejects and cannot retry against CLOSED.

## LAW 5.8-57 — SAFETY DOES NOT PROMISE STARVATION-FREE REVOCATION UNDER UNBOUNDED CONTENTION

Baseline guarantees stale/non-current writers cannot overwrite accepted authority. It does not guarantee a maintenance closer wins immediately against indefinitely continuous valid competing writes without a coordinator.

Retries are bounded; coordination/maintenance retry may be required.

## LAW 5.8-58 — ADDITIVE AUTHORIZATION MAY AVOID ROLLOVER WHEN CLAIM SEMANTICS DO NOT CHANGE

A join/grant that does not invalidate current mutation claims/authorization partition may publish campaign-side without closing unrelated live epochs.

If fixed claims or live authorization-relevant partition semantics must change, use close/absorb/successor.

---

# 16. Entity/owner movement and multi-live operations

## LAW 5.8-59 — OWNER TRANSFER BETWEEN ACTIVE LIVE PARTITIONS FREEZES EVERY AFFECTED WRITABLE SOURCE

For E1..En involved in one owner transfer/global transition:

```text
close each required ACTIVE epoch independently by exact CAS
-> prove all required final CLOSED revisions
-> one campaign absorption/transfer transaction
-> optional successors
```

## LAW 5.8-60 — PARTIAL FREEZE IS A VALID MIXED STATE, NOT PARTIAL FICTIONAL TRANSFER

If only some required epochs close before failure/crash:

- closed scopes remain current truth and non-writable;
- still-active scopes remain current/writable;
- the intended cross-scope transfer/global event has not yet been established;
- only dependent operations are gated.

Do not reopen already-closed epochs.

## LAW 5.8-61 — RECOVERY RESUMES MULTI-SCOPE TRANSITION FROM ACTUAL SOURCE STATES

No rollback-by-force or fabricated distributed transaction is used.

---

# 17. Cross-source dependencies and chronology boundary

## LAW 5.8-62 — UNCLAIMED READ DEPENDENCY MAY REMAIN EXTERNAL

A live action may read a campaign/other-native owner without claiming it when current mutation authority does not need to move.

## LAW 5.8-63 — MATERIALLY RACEABLE MUTABLE CROSS-SOURCE DEPENDENCY REQUIRES SYNCHRONIZATION BOUNDARY

If external owner movement could change legality, stakes, target validity, causal result or required mutation, local live CAS alone is insufficient.

Use the owning cross-scope synchronization/repartition/chronology protocol.

Step 5.9 owns fictional temporal reconciliation; Git ref/commit order does not decide fictional simultaneity/priority.

---

# 18. Temporal and operational owner continuity

## LAW 5.8-64 — CLOSE DOES NOT CANCEL TEMPORAL/PROCEDURAL OBLIGATIONS

Procedure, Continuation, accepted Resolution state and independently-due temporal obligations survive close according to native lifecycle.

## LAW 5.8-65 — LIVE-CONTAINED OPERATIONAL ROOTS REMAIN RECOVERABLY ROUTED THROUGH CLOSED STATE

Step-5.2 root/temporal routing must still discover all required owners while E is CLOSED_UNABSORBED.

## LAW 5.8-66 — ABSORPTION MOVES REQUIRED OWNER REPRESENTATION/ROUTING BEFORE RELEASING OLD ROUTE

Campaign transition must preserve RRC for accepted operational/temporal state; it may not strand a Procedure/Continuation/temporal owner by clearing live route first.

## LAW 5.8-67 — CROSS-PARTITION PROCEDURE/TEMPORAL OWNER IS NOT SCENE-CLAIMED BY CONVENIENCE

If writable scope spans multiple live partitions, keep it in its native partition or use explicit synchronization/repartition boundary.

---

# 19. Step-4 information/disclosure boundary

## LAW 5.8-68 — OBJECTIVE TRUTH, FICTIONAL KNOWLEDGE AND HUMAN DISCLOSURE REMAIN DISTINCT LIVE SEMANTIC OWNERS

Live physical envelope may carry representations/evidence but SHALL NOT make `known_by_pc_ids` or similar legacy structures a parallel current authority after Step-4 realization.

## LAW 5.8-69 — WRITE-BEFORE-REVEAL APPLIES TO THE SHARED FACT, NOT PREEMPTIVE HUMAN DISCLOSURE RECORDING

Shared mechanical/world consequence becomes durable first.

Narration/emission follows under eligible context.

`runtime.disclosure` advances only after the Step-5.12 host-emission boundary.

A high-level interaction may therefore have separate native live and disclosure publications.

---

# 20. Transport realization

## LAW 5.8-70 — PYTHON CORE OWNS LIVE REPOSITORY TRANSPORT

Step-5.6 repository boundary applies equally to live publication. LLM roles do not execute or adjudicate Git/live CAS protocol.

## LAW 5.8-71 — CANONICAL LIVE TRANSPORT IS A SEMANTIC RepositoryPort CAPABILITY

Equivalent interface:

```text
LiveSourceCAS(
    source ref,
    expected exact revision,
    complete native transition,
    acting-principal/authorization evidence,
    transition kind
)
```

with typed accepted/rejected/indeterminate outcome.

Architecture does not depend on one particular GitHub REST/Contents operation.

## LAW 5.8-72 — CURRENT CONNECTOR CAS TEST IS FEASIBILITY EVIDENCE, NOT ARCHITECTURE AUTHORITY

Observed stale Contents-style write rejection after source close confirms feasibility of source-local fencing, but future implementation may use Git ref CAS, GraphQL expected-head commit or another equivalent supported primitive.

---

# 21. Performance and host-model laws

## LAW 5.8-73 — NORMAL LIVE HOT PATH REMAINS BOUNDED

Target behavior:

```text
shared read/sync:
    one live source/ref currentness probe when needed
    + exact source fetch only if changed/not cached

accepted native live durability edge:
    one exact-source CAS publication
```

No campaign/full-world/history scan belongs to ordinary live turn.

## LAW 5.8-74 — NO BACKGROUND SERVICE IS REQUIRED FOR CORRECTNESS

Correctness survives ChatGPT sessions stopping without callback, timer or presence signal.

## LAW 5.8-75 — FIXED-CLAIM ROLLOVER COST IS A MEASURED PERFORMANCE RISK, NOT A CURRENT ARCHITECTURE BLOCKER

Reopen dynamic claim acquisition only if real multiplayer traces show rollover frequency materially harms UX enough to justify a more complex distributed ownership manager.

---

# 22. Crash / concurrency matrix

| State/failure | Current truth | Ordinary writer | Required response |
|---|---|---|---|
| prepared live source, route absent | campaign | campaign/other current owners | candidate source non-authority/orphan |
| route selects ACTIVE E | E | E | exact-source CAS |
| two writers from same L | E | one winner | loser refresh/revalidate |
| close wins over stale writer | CLOSED E | none | stale write rejected; absorb/recover |
| writer wins before close | newer ACTIVE E | E | close retries from new state |
| CLOSED, absorption not started | CLOSED E | none | resume absorption |
| campaign absorption rejected | CLOSED E | none | repin/revalidate campaign; retry forward |
| absorption indeterminate | unknown campaign selection; E remains known final source evidence | none until proven | bounded current authority verification |
| absorption confirmed current | campaign | campaign unless successor selected | old live no longer current |
| process dies after live CAS before local bookkeeping | remote E | per current lifecycle | recover actual E; no gameplay replay |
| process dies after close | CLOSED E | none | recover/resume absorption |
| source missing while route selects E | unresolved | none affected | BLOCKED/integrity diagnosis; no campaign fallback |
| subset of multi-live epochs closed | each actual source remains its own current truth | closed scopes none; active scopes active | finish freeze or recover; global transition not yet established |
| revocation close succeeded, campaign auth TXN failed | CLOSED E | none affected | revocation boundary not acknowledged; retry transition |
| accepted operational owner survives close | CLOSED E/native routed state | no ordinary scene mutation | preserve/recover/absorb owner, never cancel by close |

---

# 23. Explicit non-goals / prohibitions

Step 5.8 does NOT introduce:

```text
NO live leader process
NO TTL/heartbeat lease correctness
NO generic fencing-generation service
NO global sequence/frontier
NO distributed transaction across refs
NO force push/rollback-by-ref-rewind
NO generic YAML/text merge authority
NO retrospective touched-set ownership
NO dynamic claim acquisition baseline
NO unbounded scan to determine owner authority
NO semantic mega-owner from LIVE_STATE packing
NO campaign allocator write per ordinary live creation
NO cancellation of accepted Step-3 state merely because epoch closes
NO checkpoint-based live authority choice
NO Git commit order as fictional chronology
NO pre-emission disclosure bookkeeping merely to keep one-write-per-turn
```

---

# 24. Machine-realization debt

Implementation planning after architecture closure must address at least:

- replace/extend current scene/live route schema with immutable typed owner/partition claims;
- implement bounded claim-authority lookup/routing without all-live scans;
- define live-containment admission for each supported owner class;
- provide live-epoch stable ID namespace and update identifier policies/allocator assumptions;
- align live physical persistence with Step-3 execution-segment boundaries;
- preserve Procedure/Continuation/temporal routing through CLOSED/absorption;
- replace legacy live knowledge authority with Step-4 native knowledge/disclosure ownership;
- implement Python RepositoryPort live CAS with typed accepted/rejected/indeterminate outcome;
- add opening/close/absorption/revocation/entity-transfer crash tests;
- add ambiguous live ACK/current-descendant tests;
- add explicit save with moving live sources tests;
- add controlled handoff with accepted in-flight execution tests;
- add multi-live partial-freeze recovery tests;
- measure fixed-claim rollover frequency and hot-path repository-call/latency budgets;
- remove stale runtime prose that assumes one high-level action always equals one LIVE_STATE write or campaign allocator owns every persistent ID domain.

No broad GAME/schema implementation is performed by this architecture step.

---

# 25. Step-5.8 exit proof

Step 5.8 satisfies its roadmap exit target because:

1. every live-admissible owner/partition has bounded decidable current write-authority routing;
2. selected immutable claims cannot overlap in healthy current state;
3. exact-source CAS prevents stale conforming writer overwrite;
4. terminal source close fences future ordinary writes before route-away;
5. CLOSED_UNABSORBED preserves one current truth authority with zero ordinary writers;
6. forward campaign absorption changes authority without distributed transaction/force rollback;
7. cold recovery can adopt ACTIVE or resume CLOSED without timestamps/checkpoints/host presence;
8. accepted Step-3/temporal state survives close and remains recoverable;
9. revocation/controller/entity-transfer boundaries cannot create two ordinary writable owners under the conforming protocol;
10. normal ChatGPT-host operation requires no background lease/leader.

No unresolved owner-level decision remains in Step 5.8.

Next architecture slice after roadmap closure: **Step 5.9 — Chronology Persistence & Reconciliation**.

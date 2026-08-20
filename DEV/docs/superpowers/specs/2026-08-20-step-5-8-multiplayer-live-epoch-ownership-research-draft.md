# Step 5.8 — Multiplayer / Live-Epoch Ownership — Research / Architecture Draft

Status: **RESEARCH DRAFT — NONCANONICAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Task brief:

- `2026-08-20-step-5-8-multiplayer-live-epoch-ownership-task-brief.md`

This document records verified repository state, external primary-source evidence, lab evidence, derived constraints and a provisional architecture recommendation. It is intentionally noncanonical until analytical challenge and adversarial review are complete.

---

# 1. Executive finding

The current evidence does **not** justify a long-lived leader, TTL lease, heartbeat, or separate distributed lock service for HDM live play.

A substantially smaller model appears sufficient:

> **ROUTED EPOCH / EXACT-REVISION CAS / TERMINAL FREEZE**

Conceptually:

```text
campaign authority routing
    selects one current live epoch for one bounded mutation scope

within active epoch
    multiple authorized sessions may compete
    against one exact live source revision
    through compare-and-swap publication

before authority can leave that live source
    the live source itself is CAS-transitioned
    ACTIVE -> CLOSED

CLOSED
    remains exact current truth for the unabsorbed live scope
    but admits zero ordinary gameplay writes

campaign absorption
    forward-publishes the final closed live result
    and changes current routing back to campaign / successor lifecycle
```

The key architectural insight is that **current truth authority** and **ordinary write admission** must be distinct.

The Step-5.8 exit invariant should therefore be:

```text
EXACTLY ONE DECIDABLE CURRENT TRUTH AUTHORITY
AT MOST ONE ORDINARY WRITABLE AUTHORITY
```

not an invariant requiring one writable authority at every instant.

A deliberate frozen transfer interval with zero ordinary writable authority is valid and useful.

The remaining material design question is ownership granularity. The strongest current recommendation is:

> **scene-centered epoch + immutable bounded live mutation-claim set selected at opening**, with existing durable owners not in that claim set requiring an epoch boundary before becoming live-mutable.

That is preferable to dynamic per-entity claim transfer or a campaign-global lock/index under HDM's simplified ChatGPT-host model.

---

# 2. Verified current repository state

## 2.1 Existing live architecture is already multi-writer CAS, not leader-owned

`GAME/CORE/LIVE_SCENE.md` currently defines:

- one temporary branch per shared scene epoch;
- campaign branch as long-term durable canon;
- live branch as current operational authority while selected by durable scene routing;
- one runtime-mutated `LIVE/LIVE_STATE.yaml`;
- one cheap live ref probe on shared-state-dependent turns;
- optimistic one-file mutation;
- commit-before-shared-reveal;
- bounded stale-write reconciliation;
- `active -> closed` before compaction;
- one coherent campaign absorption batch;
- `last_absorbed_live_head_sha` for compaction idempotency;
- successor rollover after absorption;
- no background polling.

There is no elected host or persistent leader identity.

This is a strong starting point rather than an architecture to discard casually.

## 2.2 Existing scene route is narrower than the prose ownership claim

`GAME/SCHEMA/scene.schema.yaml` currently routes a scene to at most one live epoch through:

```text
epoch_id
branch
state_path
base_campaign_sha
opening_live_head_sha
```

and records `last_absorbed_live_head_sha` after compaction.

But it has no explicit durable representation of the full set of existing native owners whose mutation authority has moved into that epoch.

## 2.3 Existing live state tracks touched owners, not admitted ownership

`GAME/SCHEMA/live_scene.schema.yaml` contains cumulative:

```text
touched_campaign_paths
touched_entity_ids
```

These are useful compaction/conflict evidence but are retrospective: they say what the epoch touched, not what the epoch was allowed to own before a mutation occurred.

Therefore they cannot by themselves prevent:

```text
campaign writer mutates X
while
live epoch later claims it also owned X
```

or two live epochs both deciding independently that X is theirs.

## 2.4 Existing world entities do not carry live-owner routing

Current PC/NPC/item state provides placement such as location, owner or container, but no `current_live_epoch_id` or equivalent authority field.

That is useful evidence for deciding which entities belong in a scene-centered claim, but placement is not itself a complete write-authority contract.

A character can be physically present while some unrelated owner state remains globally/campaign-owned; conversely a globally relevant process/effect may need synchronized mutation without being a physical participant.

## 2.5 Step-5.2 already prevents LIVE_STATE from becoming a universal owner

Step 5.2 explicitly preserves typed native ownership and allows a live source as a physical/native durability source for currently live-owned mutable truth.

Procedure, Resolution, Continuation, world owners and temporal owners remain semantic owners.

Therefore the final Step-5.8 machine model may physically package several live-local typed owner payloads under one atomic live source/envelope, but **the envelope cannot become the semantic owner of every field merely because it is one file**.

## 2.6 Step-4 makes current live knowledge fields machine debt

Step 4 canonicalizes:

```text
world/current owner         objective state
world.knowledge             current fictional epistemic relation
runtime.disclosure          human-player exposure relation
```

Current `live_facts.known_by_pc_ids` therefore cannot survive implementation unchanged as a parallel durable current knowledge owner.

A live physical source may carry a live representation of the native `world.knowledge` owner, or event/perception evidence needed to update it, but it cannot define a second epistemic model.

Likewise `observable_events.perceived_by_pc_ids` can be semantic perception/knowledge evidence; it does not prove human host delivery and cannot replace `runtime.disclosure`.

## 2.7 Current machine `revision` is not sufficient as authority by itself

`LIVE_STATE.revision` is an integer incremented once per successful logical live write.

It can remain useful for diagnostics or local progress within one epoch, but Git publication correctness already has a stronger exact source identity: branch HEAD / commit / blob revision.

No current requirement needs comparing integer revision values across epochs/scenes. Promoting `revision` into a universal fencing generation would violate Step-5.1 pressure against unnecessary cross-domain sequencing.

---

# 3. Host/environment findings

## 3.1 ChatGPT-host lifecycle is hostile to lease leadership

Inherited architecture already establishes:

- chat/process lifetime is not gameplay authority;
- no reliable online presence;
- no background execution guarantee;
- no exact callback at context destruction;
- no reliable remaining context/time budget;
- cold restart is normal.

A TTL lease/leader architecture would require a liveness mechanism whose primary failure mode is exactly what the host cannot guarantee reliably: timely keepalive/renewal.

It would introduce:

```text
lease acquisition
lease TTL
keepalive cadence
clock/expiry interpretation
leadership takeover
old leader fencing
```

without removing the need for exact revision validation.

## 3.2 External distributed-system evidence supports version validation over lease trust

Current official GitHub documentation states that non-force ref update preserves fast-forward behavior and rejects conflicts rather than overwriting work.

GitHub GraphQL `createCommitOnBranch` accepts `expectedHeadOid`, directly expressing a compare-and-swap expectation for branch publication.

Current official etcd documentation describes transactions guarded by comparisons on value/revision/version for compare-and-swap and higher-level concurrency control.

More importantly, etcd's own design explanation states that lease/lock APIs alone do not establish mutual exclusion; version/revision validation is the correctness mechanism, while lease can reduce aborted requests/coordinate liveness.

That maps directly to HDM:

```text
Git/live exact revision validation = correctness fence
lease/leader = optional contention optimization at best
```

HDM has no demonstrated contention profile justifying the added coordination system.

Primary-source references reviewed:

- GitHub Docs — REST API endpoints for Git references / Update a reference
- GitHub Docs — GraphQL Commits / `createCommitOnBranch` / `expectedHeadOid`
- etcd Docs — API transaction compare/revision semantics
- etcd Docs — why etcd / lease versus version-number validation
- etcd Docs — lease keepAlive behavior

---

# 4. Lab evidence

A dedicated branch was created in `dkolyada/hedgelion-dnd-master-lab`:

```text
experiment/step-5-8-live-cas-001
```

Fixture:

```yaml
schema_version: 1
epoch_id: E_TEST
status: active
revision: 0
value: initial
```

Initial blob:

```text
ae35e8f1249bc9355a986750ce32891d3fcd3611
```

Writer F froze the epoch by replacing the file with expected old blob:

```yaml
status: closed
revision: 1
```

Successful close commit:

```text
459a5a154340e6b60ff4edb5a8885f13a3960fcf
```

New blob:

```text
5d331c75f58cb78da8738d83b591f47943067d44
```

A stale gameplay writer then attempted to replace the file using the **same original expected blob** `ae35e8f...` and received HTTP `409` conflict. The stale write was not published.

Final source remained `closed`.

This proves the relevant current connector fallback property:

```text
close wins CAS first
    -> writer with old expected revision cannot publish
```

It does **not** prove GitHub understands HDM lifecycle. A writer intentionally using the new closed blob could technically construct another commit unless Python/application policy rejects `closed -> active` or ordinary mutation of closed state.

Therefore final safety composes:

```text
repository revision CAS
+
HDM monotonic lifecycle validation
+
application authorization
```

not repository CAS alone.

### Lab hygiene note

Before creating the dedicated branch, an accidental placeholder file was briefly written to lab `main` and then immediately deleted by a forward revert-style commit. Product repository was never affected. The lab main tree was restored but now contains those two harmless history commits. No force history rewrite was performed or will be performed.

---

# 5. Separate the five concepts currently blurred together

The final architecture should treat these as distinct:

## 5.1 Semantic owner

Who owns the meaning/current state of a value?

Examples:

```text
PC state                -> PC/world actor owner
Procedure ResourceState -> runtime.procedure
fictional knowledge     -> world.knowledge
```

This does not change merely because physical bytes are stored in a live source.

## 5.2 Current authority source/routing

Which durable native source currently provides the writable/current representation of that owner/scope?

Conceptually:

```text
campaign source
or
selected live epoch source
```

## 5.3 Mutation claim scope

Which existing owner identities are admitted to mutate through the selected live source during this epoch?

This prevents another source from lawfully writing the same owner concurrently.

## 5.4 Writer authorization

Which current authenticated player/principal may initiate a mutation against those owners?

This derives from campaign/player/controller policy, not live branch existence or repository permission.

## 5.5 Revision fence

Which exact source revision must still be current for a prepared mutation to publish?

This is the expected live HEAD/commit/blob identity used by the live CAS operation.

These concepts must not be compressed into one `lease` field or one `revision` integer.

---

# 6. Candidate family comparison

## 6.1 Family C — lease/leader

### Model

One host/session obtains temporary leadership for the live scope, renews it, and other sessions either proxy/wait/take over after expiry.

### Strengths

- reduces write contention when one leader stays alive;
- conceptually familiar distributed coordination pattern;
- may reduce rejected writes in very high-frequency workloads.

### Weaknesses for HDM

- requires liveness/keepalive that ChatGPT does not guarantee;
- wall-clock expiry becomes correctness-sensitive unless every write still validates a separate fence;
- takeover after context death becomes extra protocol;
- current sessions cannot reliably receive push/revocation/lease notices;
- adds another native authority/coordination owner;
- normal turn latency may gain lease checks/renewal;
- still needs revision fencing for correctness;
- solves a contention optimization problem not shown to be material in turn-based D&D chat.

### Disposition

**Reject provisionally.** Reopen only if later measured contention shows CAS aborts dominate user-perceived latency and a host profile can provide trustworthy keepalive infrastructure.

## 6.2 Family B — explicit monotonic fencing generation/token

### Model

Campaign route selects live epoch plus durable generation/token. Every live write validates that token in addition to exact source revision.

### Potential strengths

- very explicit stale-authority fence across epoch transitions;
- resembles fencing-token designs used when a stale client can continue accessing an external resource after losing a lease.

### Weaknesses here

- where would the token live and be validated atomically with a live write?
- if token lives only in campaign, every live mutation would need campaign currentness validation or a trusted cross-source conditional write, destroying the cheap hot path;
- if copied into live source, a stale live source still contains its old valid token and repository accepts writes unless another mechanism changes that source;
- changing the live source to invalidate old token is equivalent to the terminal close CAS already available;
- a globally monotonic token risks creating a new cross-domain sequence/frontier forbidden by Step 5.1;
- per-epoch token becomes nearly synonymous with epoch identity and adds little beyond exact revision + lifecycle.

### Disposition

**Reject as a generic additional authority generation.** Keep epoch identity typed and immutable, but use terminal live-source close + exact revision CAS as the actual stale-writer fence.

A later backend may internally expose a fencing token, but it is not a new gameplay architecture owner.

## 6.3 Family A+ — routed epoch + exact revision CAS + terminal freeze

### Model

- campaign routing selects one epoch and its bounded mutation claims;
- epoch identity is immutable;
- authorized sessions all write the same live source;
- each write uses exact expected source revision;
- transfer/revocation begins by CAS-changing the live source `ACTIVE -> CLOSED`;
- closed state is terminal for ordinary writes;
- campaign absorption changes routing only after freeze;
- successor is a new epoch, never reopened old epoch.

### Strengths

- uses existing Git/repository version validation;
- no leader/process identity;
- no TTL/heartbeat/background dependency;
- cheap hot path remains one source probe + optional fetch/write;
- stale writer is physically rejected after another mutation/freeze;
- cold recovery needs only current campaign route + exact selected live source;
- aligns with Step-5.2 closed-unabsorbed semantics;
- naturally supports several sessions competing on one shared source;
- no cross-source condition on every ordinary write.

### Main residual requirement

Campaign routing must identify the complete bounded live **mutation claim scope** strongly enough that campaign/other-live writers know what they are not allowed to mutate while epoch is active/closed-unabsorbed.

### Disposition

**Recommended base architecture.**

---

# 7. Provisional live lifecycle model

The minimal semantic lifecycle appears to be:

```text
PREPARED
    candidate source exists
    no campaign/native route selects it
    non-authoritative

ACTIVE
    selected by current campaign route
    current truth authority for admitted live claims
    ordinary authorized writes allowed via CAS

CLOSED_UNABSORBED
    selected by current campaign route
    current truth authority for admitted live claims
    ordinary gameplay writes forbidden
    authorized compaction/recovery allowed

ABSORBED / NONAUTHORITY
    campaign route no longer selects the epoch
    final live result has been incorporated into current campaign authority
    old source immutable/non-authoritative residue
```

`PREPARED` and `ABSORBED` need not be persisted `status` values in LIVE_STATE.

Current two-state field may remain:

```text
active | closed
```

because authority is the composition of source-local lifecycle + current campaign route.

That avoids copying campaign routing state into the live payload.

---

# 8. Truth authority versus write admission

This distinction is central.

## ACTIVE selected live epoch

```text
current truth authority = live source
ordinary write admission = yes, subject to auth + expected revision CAS
```

## CLOSED selected live epoch

```text
current truth authority = final closed live source
ordinary write admission = no
maintenance/compaction = yes if authorized
```

This is a valid **zero-writer interval**.

It solves an otherwise impossible transfer invariant. Campaign does not need to become current before it contains the live result, and live does not remain writable while campaign absorption is being prepared.

## After successful absorption

```text
current truth authority = campaign source
ordinary campaign write admission = according to campaign policy
old live ordinary write admission = no forever
```

If shared scene still needs live mode, a new epoch is opened from the new campaign basis.

---

# 9. Why terminal close is sufficient stale-writer fencing

Suppose sessions A and B both loaded active live revision `L0`.

Case 1 — B writes first:

```text
B: CAS L0 -> L1 succeeds
A: CAS L0 -> LA rejects stale
A refreshes L1
```

Normal optimistic concurrency.

Case 2 — maintenance/revocation closer F closes first:

```text
F: CAS L0 ACTIVE -> CLOSED at Lc succeeds
A: CAS L0 -> LA rejects stale
A refreshes Lc and sees CLOSED
A MUST NOT retry ordinary gameplay write
```

Case 3 — gameplay writer A wins immediately before close:

```text
A: CAS L0 -> L1 succeeds
F: CAS L0 -> CLOSED rejects stale
F refreshes L1
F retries close from L1 -> Lc
```

The action published before the freeze edge was established and therefore belongs to final current state. It is not retroactively revoked.

No wall-clock ownership rule is required.

After close succeeds, every session prepared from an older revision loses CAS. Any refreshed session sees the terminal lifecycle and cannot retry ordinary mutation under application rules.

---

# 10. Active mutation protocol

Provisional algorithm for one shared-state-dependent action:

```text
1. establish current selected epoch from cached validated route
2. probe current live ref/head L
3. if L changed:
       fetch exact live state at L
       replace cache
4. require current live state ACTIVE
5. validate current acting principal/player/controller eligibility from accepted auth basis
6. resolve action/rules/RNG against exact live state + required bounded external dependencies
7. freeze semantic result / dependency-touch footprint / native execution identities
8. build exact new live-source state
9. CAS publish expected L -> L'
10. confirmed accepted:
       shared mutation established/durable
       only now reveal/use it as shared fact
11. confirmed rejected:
       refresh source
       if CLOSED -> do not retry gameplay write; follow routing/compaction recovery
       else classify dependency overlap
12. indeterminate:
       verify actual current source + native semantic receipt/evidence
       do not reroll/replay blindly
```

The current live `revision` integer may increment for convenience, but `L` is the correctness CAS identity.

Automatic retries remain bounded.

---

# 11. Ambiguous live-write outcome

Step 5.6's accepted/rejected/indeterminate distinction should apply to live writes as well.

The future RepositoryPort needs an equivalent semantic outcome for live-source CAS.

A lost response after dispatch cannot cause:

- narration assuming success;
- reroll;
- duplicate action execution;
- a second blind write.

Preferred verification order:

```text
read current live head D

if D == intended commit/source revision C:
    publication happened

else if bounded lineage evidence proves C is ancestor of D:
    publication happened historically
    adopt D as current and revalidate current effect/dependencies

else:
    inspect current native execution/event/receipt evidence
    determine whether the established semantic effect is already represented
    otherwise return conflict/revalidation/ambiguity
```

Existing Step-3 execution owner/receipt/event identity should carry semantic idempotency. Do not add a generic live transaction journal merely for this problem.

---

# 12. Ownership-granularity analysis

This is the hardest unresolved part.

## 12.1 Scene-only implicit ownership

Rule would be:

> every entity physically participating in scene S is automatically owned by S's active epoch.

### Advantage

Minimal metadata.

### Problems

- “participating” is not one authoritative machine predicate today;
- item nested in PC inventory versus location versus container can create ambiguous membership;
- NPC/entity may affect multiple scenes/global processes;
- effects/procedures/knowledge owners are not simply physical entities;
- campaign writer cannot cheaply prove that an arbitrary owner is or is not live-owned without reconstructing scene reachability;
- opening two scenes can produce overlapping implicit claims without one atomic explicit overlap check.

**Reject as sole ownership rule.** Scene remains primary partition but needs explicit bounded claims.

## 12.2 Dynamic per-owner claim acquisition/release

Rule would allow an active epoch to acquire/release existing campaign owner X during its lifetime.

### Advantage

Flexible; fewer rollovers when new entity enters scene.

### Problems

To acquire X safely while epoch active:

1. current campaign X must be pinned;
2. no other live epoch may own X;
3. authority claim must move campaign -> E;
4. E must receive a base representation consistent with the campaign claim transition;
5. crash between campaign and live publication must have decidable authority;
6. existing E writers must not mutate X before acquisition is complete;
7. campaign writers must stop immediately after claim publication;
8. recovery must compose claim state plus exact E state;
9. release has symmetric complexity.

This is effectively a per-owner multi-domain authority-transfer protocol nested in normal live play.

It would either:

- add cross-source writes/checks to common turns; or
- require a global ownership coordinator/index; or
- create subtle partial transfer states for every dynamic admission.

For HDM this is disproportionate complexity.

**Reject provisionally for baseline architecture.**

## 12.3 Fixed bounded mutation claim set per epoch

At opening, campaign routing transaction selects epoch E plus an immutable set of existing native owner references that E is allowed to mutate.

Conceptually:

```text
LiveRoute {
    scene_id
    epoch_id
    source_ref
    state_path
    base_campaign_revision
    admitted_mutation_owner_refs[]
}
```

Exact representation is implementation work; this is not necessarily a new top-level class.

Scene-local state itself is implicit in the route.

The claim set:

- is bounded;
- is explicit;
- identifies semantic owners, not file paths only;
- is immutable during the epoch;
- is current routing evidence, not duplicate owner payload;
- cannot overlap another current live route's claims;
- prevents normal campaign writes to claimed owners until absorption;
- allows new epoch-local provisional owners to exist under E without prior campaign claim;
- changes only by close/absorb/reopen boundary.

### Advantages

- opening campaign CAS atomically selects source + full initial claims;
- two concurrent overlapping epoch openings from the same campaign H cannot both become authoritative through ordinary campaign non-force CAS;
- loser repins and sees the winner's claim before selecting its own route;
- no global entity-lock index required for baseline if overlap validation is bounded over active route claims;
- normal live turns do not touch campaign routing;
- cold recovery learns exact bounded ownership claims from current campaign authority;
- cross-scene transfer becomes an explicit rare boundary, not hidden dynamic routing.

### Cost

If an existing campaign owner not already claimed must become live-mutable, the epoch needs a rollover/ownership-boundary operation.

This can introduce technical synchronization in scenes whose mutable cast changes frequently.

### Provisional disposition

**Recommended.** The added boundary cost is preferable to embedding per-owner distributed authority transfer into the ordinary turn path.

---

# 13. How to choose a fixed claim set without overclaiming the world

Opening should include only existing owners that can plausibly require synchronized mutation under the current shared actionable scene horizon.

Likely candidates:

- scene current-state owner;
- participating PCs;
- material participating NPCs;
- significant interactive items/assets whose state/ownership may change;
- scene-local world/effect/process owners that can be acted on or can independently affect the shared scene;
- live-local operational owners whose recoverability/mutation authority must follow the live scope.

Do **not** claim:

- every entity referenced by any claimed owner;
- whole location/world catalogs merely because scene is located there;
- distant faction/process state with no current synchronized mutation reason;
- all knowledge/lore propositions related to participants;
- Story/transcript projections.

The mutation claim is a write-authority boundary, not a read/dependency closure.

Read dependencies may remain campaign-owned and can be exact-pinned/validated when needed.

---

# 14. Concurrent opening with fixed claims

Suppose campaign H has no live routes for scene A or B.

Two hosts prepare:

```text
A claims {A_scene, PC_A, ITEM_X}
B claims {B_scene, PC_B, ITEM_X}
```

Both start from H.

A publishes campaign route first -> HA.

B's campaign publication from H fails non-force CAS.

B repins HA and must revalidate routing/ownership dependencies. It sees ITEM_X already claimed by A and cannot establish an overlapping route.

No global lock or central entity owner table is needed for this same-ref selection race.

If claims are disjoint, B may rebase/revalidate and then publish its independent route.

This depends on all authoritative live-route claims being discoverable boundedly from current campaign routing. Step 5.7 already requires current owning-scope routing, so this is aligned rather than new global authority.

---

# 15. Campaign write guard while live claims exist

Normal campaign publication must treat current live mutation claims as routing/authorization dependencies.

Before changing existing owner X through campaign source:

```text
if X is currently live-claimed:
    normal campaign gameplay write to X is not authorized
    route mutation to the owning live epoch or initiate authority boundary
```

A stale campaign writer from before a live claim may attempt publication.

The campaign ref moved when live route/claims were established, so Step-5.6 CAS rejects the stale commit. On revalidation, the writer sees the new route claim and cannot merely transport-rebuild the X mutation through campaign source.

Thus campaign branch CAS and live claim routing jointly fence campaign-side stale writers.

---

# 16. Opening/adoption protocol

Provisional architecture:

```text
A. Pin current campaign authority H.
B. Determine scene need for live mode and bounded immutable claim set Q.
C. Validate Q does not overlap current routed live claims.
D. Create/prepare candidate live source E from exact H inputs.
   E is non-authoritative while unselected.
E. Publish one campaign transaction selecting LiveRoute(E,Q).
F. Only confirmed/verified campaign selection makes E current authority.
G. Gameplay sessions then adopt E and use live CAS.
```

Candidate source creation may happen before campaign selection because it is non-authoritative prepared infrastructure.

If selection fails:

- candidate remains orphan/nonauthority;
- retry may reuse it only if its exact base/claims/payload remain compatible with the newly accepted campaign basis;
- otherwise prepare a new epoch and leave old candidate for Step-5.13 cleanup.

Deterministic epoch/branch naming is optional convergence/diagnostic convenience, not authority.

If two openers derive the same branch name and one creates it first, the other must validate exact source identity/base/claims before adoption; branch-name equality is never sufficient.

---

# 17. Freeze / close protocol

A live authority transfer, membership revocation affecting current participants, mutable-owner transfer, rollover or compaction starts by closing the active epoch.

```text
read/select exact active head L
build same current semantic state with status CLOSED
CAS L -> Lc
```

Rules:

- close does not invent gameplay change;
- it preserves exact current truth and only changes ordinary write admission/lifecycle;
- if active mutation wins first, close refreshes and retries from the newer accepted state;
- after close succeeds, no ordinary gameplay mutation may target that epoch;
- the same epoch never reopens;
- `CLOSED` remains current truth while campaign route still selects it;
- compaction/recovery operations may read/finalize it;
- no background timer is required.

A close request may fail under repeated contention; automatic retries are bounded. The requested revocation/transfer/maintenance edge remains incomplete rather than pretending the fence was established.

---

# 18. Membership revocation without per-turn campaign auth reads

Per-turn campaign authorization refresh would undermine the cheap live path.

A safer event-driven rule exists:

> Any campaign authorization change that would revoke or materially alter an active live participant/controller MUST first close every affected live epoch while the old authorization is still current.

Then:

```text
1. close affected live epoch(s)
2. absorb/finalize required live state
3. publish campaign membership/controller change
4. open successor(s) under new authorization if needed
```

Race interpretation:

- stale player write that wins CAS before close happened before revocation became effective and is included in final state;
- close that wins first causes stale player's expected-revision CAS to fail;
- after refresh the old epoch is closed and ordinary retry is forbidden;
- membership revocation campaign commit is not acknowledged before this fence/absorption edge succeeds.

Thus normal live turn does not need campaign HEAD/auth refresh solely to discover revocation.

Granting additional authority can be adopted on a later route/session sync; revocation is the dangerous direction requiring a fence.

This model requires creator/controller-management code to discover affected live epochs boundedly through current routing.

---

# 19. Campaign absorption protocol

Given selected closed epoch E at exact final head `Lf`:

```text
1. verify campaign current route still selects E/Q
2. exact-pin Lf and validate CLOSED
3. derive final typed native owner state to materialize in campaign
4. fetch/pin current campaign C
5. classify C movement against Q + read/auth/recovery dependency footprint
6. if disjoint, rebuild campaign absorption on C
7. if overlapping, use native-owner reconciliation or integrity/semantic revalidation
8. publish ONE coherent campaign transaction that:
       materializes all required final E-owned results
       clears/replaces current E routing
       records exact absorbed epoch/final-live identity for idempotency
       updates required typed recovery routing/owners
9. confirmed campaign acceptance transfers current truth authority
10. old E remains closed and non-authoritative
11. cleanup is deferred
```

During steps 1–8, E remains current truth but is frozen.

This is deliberately not a distributed transaction. It is an ordered authority transition with a safe zero-writer interval.

---

# 20. Ambiguous campaign absorption

If final campaign publication acknowledgement is indeterminate, follow Step 5.6 using current campaign authority.

Recovery does not infer from the old live branch alone.

Current campaign state can show:

```text
route still selects E + not absorbed Lf
    -> E remains current closed truth; compaction unresolved/retry

route no longer selects E + absorbed identity includes E/Lf
    -> campaign accepted absorption; E nonauthority

unexpected route/source mismatch
    -> bounded retry/integrity diagnosis
```

No force rollback of campaign and no reactivation of E.

The exact absorbed marker should identify enough of the semantic source to avoid duplicate absorption. `last_absorbed_live_head_sha` is likely close to sufficient for one-scene sequential epochs but should be reviewed together with epoch identity to avoid accidental ambiguity across source reuse/migration.

---

# 21. Successor epoch ordering

Do **not** attempt to make one campaign absorption commit simultaneously select a successor whose base is that same resulting campaign commit SHA: content-addressed Git would create a self-reference problem if the successor route requires the containing commit as `base_campaign_sha`.

Simpler ordering:

```text
E1 ACTIVE
 -> E1 CLOSED
 -> campaign absorbs E1 and becomes current
 -> if live still needed, prepare E2 from new campaign authority
 -> campaign selects E2
```

This creates a short campaign-authoritative/frozen interval between epochs.

That interval is not fictional downtime.

Before another shared mutation, a session must adopt/open E2 if live mode is still required. OOC responses and independent scopes may continue.

This preserves exact base identity and avoids circular metadata.

---

# 22. Entity transfer between live scopes

With fixed immutable claims, owner X cannot move directly from writable E1 to writable E2.

The safe baseline slow path is:

```text
1. close source E1
2. if destination E2 already claims/may mutate related scope, close E2 too
3. exact-pin all final closed live sources
4. absorb affected live states into one coherent current campaign basis
5. resolve/persist X's transfer under campaign/native owner semantics
6. open successor live epochs with disjoint new immutable claim sets
```

This may be slower than a dynamic two-phase per-owner handoff, but entity crossing active live concurrency domains is expected to be rare relative to ordinary turns.

It provides a much smaller correctness surface and avoids introducing distributed live-to-live claim transfer.

If future evidence shows such transfers are common enough to harm play materially, dynamic claim acquisition can be proposed later as an optimization architecture, not baseline correctness.

---

# 23. Rare multi-scene/global event slow path

For event G that genuinely requires simultaneous/coherent mutation of owners claimed by active epochs E1..En:

```text
1. identify bounded affected live scopes/claims
2. close each affected active epoch via its own CAS
3. crash after any subset is safe:
       closed scopes are frozen current truth
       still-active scopes remain their own current truth
       G is not yet established
4. once all required sources are closed, exact-pin final heads
5. Step 5.9 chronology/rules determine minimal causal/simultaneous adjudication
6. publish one coherent campaign-domain absorption/transition where possible
7. open successors as needed
```

The order in which close operations succeed is storage/coordination order, not fictional chronology.

No distributed atomic write across live refs is required.

Availability can temporarily reduce for affected shared scopes; correctness wins over pretending an event committed globally when only some sources were frozen.

---

# 24. Cold recovery/adoption state machine

Cold recovery begins current-authority-first from campaign H.

For one scene/scope:

## No live route

```text
current truth = campaign
```

## Route selects E; E resolves ACTIVE

```text
current truth = exact E head
ordinary writes = allowed only after auth + current revision CAS
recovery = READY if RRC validates
```

## Route selects E; E resolves CLOSED

```text
current truth = exact final E head
ordinary writes = forbidden
operation = resume/coordinate compaction or wait/retry
recovery of truth may be READY
shared mutation capability = BLOCKED/coordination-required
```

## Route selects missing/malformed E

```text
current truth cannot be proven
BLOCKED + scope-local CANON_SUSPECT/integrity diagnosis
```

## Live branch exists but no current route selects it

```text
nonauthority orphan/residue
ignore for current gameplay
cleanup later
```

## Campaign route moves during recovery

```text
RETRY current owning-scope selection
movement alone != corruption
```

No branch age, commit timestamp, checkpoint age or chat memory participates.

---

# 25. Claim overlap validation and scaling

A fixed claim set requires bounded overlap detection across active routes.

Potential baseline representation:

- current campaign active-scene routing already gives a bounded list of active scenes;
- each live route carries its immutable claim refs;
- when opening/changing a live route, load only current active live-route descriptors needed to test claim intersections.

This is acceptable if active live scene count is naturally small, which matches tabletop campaign topology.

A campaign-global `entity -> live_epoch` index could accelerate very large numbers of active live scenes but would add another derived/writable consistency surface. Do not introduce it until scale measurement justifies it.

If such an index is later added, it must be a transactionally maintained routing projection, not independent authority.

---

# 26. Physical one-file live source versus typed native owners

The current one-file physical model is still attractive for atomic hot-path updates.

The architecture can preserve it by treating `LIVE_STATE.yaml` as a **physical live-source envelope** containing typed sections/owner payload representations selected for the epoch.

Rules:

- native semantic identity remains the original owner identity/type;
- routing says where its current representation resides;
- live envelope may atomically contain several changed typed owners;
- recovery enumerates live-local typed roots/owners rather than treating the envelope as one semantic object;
- compaction routes each owner back to its native campaign representation;
- a field cannot gain semantic authority solely from being present in the envelope.

This preserves the cheap one-ref CAS while respecting Steps 2–4/5.2 ownership.

Final wire design may decide whether one file remains practical once typed operational-owner state is included. Step 5.8 need not require multiple files or change the physical hot-source layout unless correctness demands it.

---

# 27. Knowledge and disclosure consequences

Live storage may need current objective and epistemic state that changes during a shared scene.

Canonical semantics must be:

```text
objective owner update
    -> live representation of that objective native owner

fictional knower update
    -> live representation/event transition for world.knowledge owner

observable event
    -> causal/perception evidence usable to derive/commit knowledge

human host exposure
    -> NOT inferred from live perception
    -> runtime.disclosure follows Step-4 / future Step-5.12 delivery boundary
```

Current `known_by_pc_ids` can remain only if transformed into a representation of the Step-4 knowledge model or into non-authoritative migration/evidence; it cannot remain a parallel current epistemic authority.

Private repository readability remains outside the correctness boundary, as Step 4 already decided.

---

# 28. Authorization principal consequences

Every live CAS mutation still requires:

```text
repository/ref belongs to selected campaign
acting principal is trustworthy
active PLAYER binding or required creator authority exists
controlled PC/action authorization is valid
mutation targets only owners admitted by current live route
```

Current `participant_ids`/`player_character_ids` in LIVE_STATE are scene state/routing aids, not authorization authority.

A service credential may physically write only if RepositoryPort preserves trustworthy acting-principal/delegation evidence under Step 5.6.

If a deployment cannot do that, it cannot claim safe multiplayer write capability merely because the service account has Git access.

---

# 29. External/manual Git mutation

HDM cannot cryptographically prevent a repository owner from manually editing live/campaign branches outside the application contract unless separate GitHub branch protection/server validation is deployed.

The architecture should not burden every hot turn with global reads attempting to defend against a deliberate admin bypass.

Instead:

- normal HDM writers use append-only/CAS rules;
- unexpected route/claim/lifecycle inconsistencies discovered at bounded currentness gates are integrity evidence;
- force-rewritten or manually contradictory authority is `CANON_SUSPECT`/repair territory;
- ordinary stale runtime concurrency remains retry/conflict, not corruption.

This is consistent with existing access-control and integrity contracts.

---

# 30. Performance model

With the recommended model, ordinary hot path stays close to current runtime:

## Cached route + unchanged shared-state-dependent read

```text
one live ref probe
```

No campaign route/auth read each turn.

## Live ref changed

```text
one live ref probe
+ exact live source fetch
```

## Uncontended shared mutation

```text
one live sync probe
+ optional fetch if changed
+ one expected-revision CAS publication
```

## Stale live write

```text
CAS rejection
+ exact current live source fetch
+ bounded overlap/revalidation
+ maybe one retry
```

## Close/rollover/revocation/entity transfer

Boundary path may perform more campaign/live reads/writes; it is intentionally not the ordinary turn path.

## Cold recovery

```text
campaign current route
+ exact selected live source(s)
+ bounded typed operational roots/dependencies
```

No history or checkpoint required by default.

---

# 31. Strongest counterarguments to the provisional recommendation

## Counterargument A — fixed claims cause too many rollovers

A lively scene may introduce new NPCs/items frequently. Requiring rollover for every previously unclaimed existing owner could create visible synchronization cost.

Response:

- claim the realistic near-horizon mutable cast at opening, not only objects already touched;
- ephemeral/provisional entities born inside epoch need no prior campaign claim;
- read-only campaign dependencies need no claim;
- many incidental entities need not become individually durable owners immediately;
- rollover is needed only when an existing durable independent owner must become live-mutable and was not claimed.

Risk remains real and should be tested later with gameplay traces/evals.

## Counterargument B — campaign routing claim lists could become large

Response:

- scope is shared actionable scene, not world closure;
- claims are stable IDs, not copied state;
- if one scene requires enormous claim sets, scene partition is itself probably too broad under current design principles;
- active route count is expected small.

## Counterargument C — explicit fencing token is cleaner

Response:

A token only improves correctness if every write can atomically validate its freshness. If freshness lives in campaign while the mutation lives on live ref, that implies cross-source validation on every turn or a shared coordinator. If freshness is copied into live, closing/updating live source is still required to invalidate old writers. Exact live revision plus terminal close already gives the necessary locally atomic fence.

## Counterargument D — leadership eliminates contention

Response:

Turn-based D&D contention is expected low. Leadership makes host loss and liveness materially harder and still needs a fence. Optimize only after measurement.

## Counterargument E — no per-turn membership check lets revoked user write

Response:

Revocation is defined as incomplete until the affected epoch is successfully frozen. Before that point the old user is still authorized. After freeze, stale expected-revision writes fail and refreshed clients cannot mutate closed state. This yields precise edge semantics without polling campaign auth every turn.

---

# 32. Provisional recommendation

Proceed to analytical challenge around this architecture:

> **ROUTED IMMUTABLE-CLAIM EPOCH / EXACT-REVISION CAS / TERMINAL FREEZE / CAMPAIGN ABSORPTION**

Core shape:

```text
CURRENT CAMPAIGN ROUTING
    selects LiveRoute(scene E, fixed claim set Q)
              |
              v
       LIVE EPOCH SOURCE
       ACTIVE @ exact L
              |
      multi-writer CAS
              |
        ACTIVE @ L+n
              |
      CAS terminal freeze
              v
       CLOSED @ Lf
       current truth
       zero ordinary writers
              |
       campaign absorption
              v
       CAMPAIGN CURRENT
              |
        optionally open E2
```

No:

- lease;
- heartbeat;
- host leader;
- global fencing sequence;
- per-turn campaign route refresh;
- distributed transaction;
- dynamic live claim acquisition in baseline;
- checkpoint authority;
- generic live semantic mega-owner.

The next analytical challenge must try to falsify this model before any candidate spec is written.
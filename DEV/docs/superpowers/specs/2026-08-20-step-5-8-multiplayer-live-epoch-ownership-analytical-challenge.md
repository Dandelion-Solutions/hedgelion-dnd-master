# Step 5.8 — Multiplayer / Live-Epoch Ownership — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — NONCANONICAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Challenges:

- `2026-08-20-step-5-8-multiplayer-live-epoch-ownership-research-draft.md`

Provisional recommendation under attack:

> **ROUTED IMMUTABLE-CLAIM EPOCH / EXACT-REVISION CAS / TERMINAL FREEZE / CAMPAIGN ABSORPTION**

The purpose of this document is to find counterexamples, hidden duplicate authority, unnecessary abstraction and host-model mismatches before a candidate specification is written.

---

# 1. Challenge result summary

The challenge did **not** find a reason to introduce a TTL lease, leader host, generic fencing generation, global entity lock table or distributed transaction.

It did find several important refinements required for correctness:

1. **The core invariant is exactly one current truth authority, but only at most one ordinary writable authority.** `CLOSED_UNABSORBED` deliberately has zero ordinary writable authorities.
2. **A fixed live claim must cover current write authority, not all read dependencies.** Cross-source mutable dependencies that can race materially require a typed cross-scope synchronization/chronology boundary rather than being silently treated as stable.
3. **Revocation/controller transfer cannot be `close -> absorb -> later authorization commit`.** After close, the campaign absorption and authorization revocation/transfer must join one campaign transaction when they form one boundary, otherwise a stale player can regain a valid campaign-write window.
4. **Entity transfer between live scopes must freeze every affected currently writable live source before one campaign-domain transfer/absorption transaction.** Freezing only the source epoch is insufficient when the destination epoch already exists.
5. **A campaign route/claim is not sufficient alone to fence a technically writable old live branch.** Correctness depends on mandatory `ACTIVE -> CLOSED` source-local CAS before route-away. Route-away from an ACTIVE selected live source is an integrity/protocol defect.
6. **`LIVE_STATE.revision` must not become the fencing authority.** Exact Git/native source revision is the CAS fence; integer revision is optional typed within-epoch metadata.
7. **Ambiguous live publication must distinguish “the mutation was durably published” from “its resulting values are still current.”** Intended commit ancestry proves historical publication, not current state.
8. **One physical live envelope does not gain universal semantic ownership.** Native typed owner identities and Step-4 information ownership must remain explicit inside/alongside the live source.
9. **The fixed claim set must be immutable for an epoch.** Dynamic claim expansion reintroduces a nested campaign/live authority-transfer protocol and invalidates the cheap hot path.
10. **Successor opening occurs only after campaign absorption is current.** Trying to select a successor whose base is the same containing campaign commit risks self-reference/circularity and complicates recovery unnecessarily.

No remaining issue currently requires an owner-level product decision. The fixed-claim rollover cost is a product-experience tradeoff, but given HDM's deliberately simplified scene-centered multiplayer model and the severe complexity of dynamic claims, the recommendation is strong enough to treat fixed claims as the technical baseline rather than present raw options for human selection.

Confidence: **high for the logical architecture; medium for final hot-path performance until implementation/evals measure real multiplayer traces.**

---

# 2. Strongest case for keeping current LIVE_SCENE almost unchanged

The current design already gets many fundamentals right:

- one live source per shared scene;
- optimistic CAS;
- one logical action -> one write;
- write-before-reveal;
- stale conflict refresh/revalidation;
- terminal `closed` concept;
- campaign absorption;
- idempotent `last_absorbed_live_head_sha`;
- no background polling;
- rare global-event slow path.

Why not simply declare it canonical?

Because later Steps 4 and 5 exposed gaps that are not wording details:

- current route does not explicitly identify the complete owner mutation claim;
- current `touched_entity_ids` is retrospective, not a pre-write authority guard;
- current prose says entities are “operationally owned” by the scene without a machine-decidable bounded ownership selector;
- current live knowledge representation conflicts with Step-4 sole `world.knowledge` ownership;
- current live transport is LLM-facing prose rather than the Step-5.6 Python `RepositoryPort` semantic boundary;
- ambiguous ACK semantics are not fully specified;
- membership revocation ordering currently allows a hidden authorization window if implemented as separate absorb then deactivate commits;
- exact cold recovery state classification now belongs to current-authority-first Step 5.7 and must be made precise.

Conclusion:

> Preserve the current hot-path philosophy and much of the lifecycle, but formalize claims/fencing/transfer/recovery rather than rubber-stamping the old prose.

---

# 3. Strongest case for lease / elected leader

A live scene could appoint one current Master as write leader. Other sessions would read from live state and either ask the leader to write or take over after lease expiry.

Potential advantages:

- few CAS conflicts;
- one serialization point;
- simple mental model under continuous server processes.

Challenge against HDM environment:

## 3.1 Liveness is unavailable as a reliable primitive

ChatGPT sessions may stop without a callback. There is no guaranteed background worker/heartbeat. A lease must therefore either:

- expire on wall clock without reliable renewal, creating availability stalls/frequent leadership churn; or
- be renewed only on user interactions, which is not a meaningful online lease.

## 3.2 Lease still does not remove fencing requirement

A stale leader can continue believing it is leader after expiry/reassignment. The resource must reject its stale write using a version/fence.

The live Git source already provides exact revision compare-and-swap.

## 3.3 Leader adds new authority and recovery state

Cold recovery would need to distinguish:

```text
leader alive?
lease expired?
clock trustworthy?
takeover allowed?
old leader fenced?
```

This is strictly more state than the routed-source model.

## 3.4 Contention profile does not justify it

D&D chat produces human-paced writes. Simultaneous mutations are correctness-sensitive but expected rare. The architecture should tolerate conflicts rather than optimize an unmeasured contention rate through a distributed coordinator.

Verdict: **lease/leader rejected for baseline.**

Reopen condition: measured live CAS abort/retry latency materially harms gameplay and a supported host profile offers a real coordination service; even then revision fencing remains mandatory.

---

# 4. Strongest case for explicit fencing generation

Proposal:

```text
campaign route = epoch E + fence generation G
live write must present G
```

Why it seems attractive:

- explicit stale-writer token;
- easy to explain “higher generation wins.”

Challenge:

## 4.1 If G's current authority is campaign-side

A live write on another ref cannot atomically prove campaign G is still current unless backend supports a cross-ref transaction/condition. It would require:

- campaign ref read/check every write;
- residual race after the check; or
- external coordinator.

That destroys the desired hot path without eliminating TOCTOU.

## 4.2 If G is copied into live source

A stale old live branch still contains its old G. GitHub will not reject a write merely because campaign now has G+1.

To fence the old branch we still need to mutate/freeze it. Once we do that, exact live revision CAS already invalidates stale prepared writers.

## 4.3 If G is globally monotonic

It creates an unnecessary campaign-global ordering concept and risks violating Step-5.1 domain typing.

## 4.4 If G is epoch-local

It is semantically redundant with immutable epoch identity plus exact source revision/lifecycle.

Verdict: **no new generic fencing generation.**

Epoch identity remains typed stable identity. Exact current source revision is the mutation fence. Terminal close is the authority-transfer fence.

---

# 5. Can terminal close really fence every stale normal writer?

Model:

```text
writer prepared from ACTIVE @ L
closer CAS L -> CLOSED @ Lc
```

Lab evidence confirms a stale Contents-style expected-blob write receives conflict after close changes the source.

Abstract requirement should be stronger and backend-independent:

> Every live mutation, including close, advances one authoritative live ref/source using exact expected prior source revision.

Then:

- old writer prepared at L cannot publish after Lc;
- refreshed writer sees CLOSED and policy forbids ordinary mutation;
- successor gets new epoch identity/source.

Potential attack: writer has refreshed CLOSED Lc and maliciously sends `closed -> active`.

Answer: application monotonic lifecycle rejects it. The architecture does not claim to protect against an authorized repository administrator bypassing Python/HDM semantics manually. Such bypass becomes integrity/repair territory.

Potential attack: campaign route is moved away from E without close, while E remains ACTIVE and old writer continues publishing.

Answer: this **must be forbidden as a protocol invariant**. Any normal route-away/absorption/ownership revocation requires exact successful close first. Persisted current campaign route that supersedes an ACTIVE unclosed prior live authority without valid transition evidence is integrity suspect/corrupt for the affected scope.

Verdict: terminal source-local close is sufficient for normal HDM stale-writer fencing when mandatory before route-away.

---

# 6. Truth authority versus writable authority

A common distributed-system instinct says “there must always be one writable owner.” That is unnecessary and harmful here.

During compaction:

```text
live E CLOSED, route still selects E
```

The exact final live source remains the only honest current truth for claimed owners. Campaign does not yet contain the final result. Allowing campaign writes now would create split authority.

Therefore:

```text
truth authority: E
ordinary writable authority: NONE
```

This is safe because:

- affected fictional mutation pauses only at a technical boundary;
- OOC/independent scopes may continue;
- no background liveness promise exists;
- Step 5.2 already recognizes closed-unabsorbed as recoverable operational state.

The exit condition must use **at most one writable source**, not exactly one writable source.

---

# 7. Is fixed immutable claim scope really necessary?

## 7.1 Attack: maybe scene route alone is enough

If all entities physically in scene are live-owned, no claim list is needed.

Counterexample:

- ITEM_X is inside PC_A's inventory, but also referenced by another scene/process;
- NPC_Y has a global condition/effect/process owner whose mutation is not represented by simple scene membership;
- an owner can be a composite epistemic relation or Procedure, not a physical entity;
- location/participant membership can itself change inside live state, creating a circular authority predicate.

A campaign writer needs a bounded deterministic answer **before** it writes X. Reconstructing all scene reachability is too implicit.

Scene-only implicit claim rejected.

## 7.2 Attack: use touched_entity_ids dynamically

The first live write touching X could make X live-owned.

Counterexample:

Campaign writer and live writer both mutate previously untouched X concurrently. Neither saw an existing claim. Both can succeed on different refs. Retrospective touched set discovers conflict only after split authority exists.

Rejected.

## 7.3 Attack: dynamic claim acquisition from campaign

This is semantically appealing: E requests X only when needed.

But safe acquisition is a cross-domain handoff:

```text
campaign X current
-> freeze campaign write right for X
-> ensure exact X representation enters E
-> admit E writers
```

Campaign and E cannot be atomically updated through current Git primitives. To make it safe requires staging state / per-owner transfer lifecycle / coordinator / temporary zero-writer state on each acquisition.

This moves expensive multi-domain authority transfer into ordinary gameplay precisely when a new existing owner appears.

The baseline complexity is disproportionate.

## 7.4 Fixed immutable claim set

Opening campaign transaction atomically publishes the whole authority route and owner-ref claim set. E begins only after selection. Claim changes require close/absorb/reopen.

This yields a clean invariant:

```text
if owner X is in Q(E) and E is selected active/closed-unabsorbed:
    X is not normally mutable through campaign or another live epoch
```

Verdict: **fixed claims survive challenge.**

---

# 8. Does fixed claim scope harm gameplay too much?

This is the strongest remaining counterargument.

Consider a tavern shared scene. New durable NPCs/items may enter frequently. If every entry forces rollover, technical boundaries could become noisy.

Mitigations that preserve correctness:

1. Opening Q should include the bounded near-horizon existing mutable cast, not only objects already touched.
2. Epoch-born provisional/minimally materialized entities are live-owned by E automatically and need no campaign-to-live transfer until compaction.
3. Read-only dependencies do not need claims.
4. Incidental presentation details need not become independent mutable durable owners.
5. Rollover can batch several ownership changes at one natural safe boundary where possible, but cannot delay a required claim if mutation must occur now.

Could dynamic claims still be worth it? Perhaps for a server/MMO-like system. For HDM's small player count and scene-centered tabletop interaction, fixed claims drastically reduce architecture risk.

This is a latency/experience cost, but the alternative changes the system class into a distributed per-entity authority manager. The recommendation remains fixed claims with later instrumentation, not an owner decision now.

Evidence that would change this: real traces showing claim-boundary rollovers happen frequently enough to dominate multiplayer interaction latency.

---

# 9. Overlapping concurrent live openings

Potential race:

```text
H current
A prepares route/claims QA containing X
B prepares route/claims QB containing X
```

Both candidate live branches can exist because they are nonauthority.

Only campaign route selection establishes authority.

A publishes first -> campaign HA.

B's non-force campaign publication from H rejects. B repins HA. Its dependency footprint includes active live routes/claim overlap; it observes X claimed and cannot transport-only rebase its old route.

No parallel authoritative claims result.

If QA and QB disjoint, B may revalidate and select its route on new campaign head.

This requires the active live-route claim descriptors to be boundedly discoverable from current campaign structural routing. That is already consistent with Step 5.7.

Pass.

---

# 10. What if campaign writer started before live claim was selected?

Campaign writer W prepares mutation of X from H.

Another host selects live epoch E claiming X, moving campaign to H1.

W's campaign ref update from H fails Step-5.6 non-force CAS.

On repin, live claim is an authority/routing dependency. W cannot classify its X write as disjoint and transport-only rebuild it on H1. It must route to E or initiate a boundary.

Therefore fixed claim selection fences stale campaign writers through campaign CAS.

Pass.

---

# 11. What if a campaign writer starts after route selection but ignores claims?

A conforming Python core must validate owning-route dependencies for intended semantic owner writes. If it ignores current live claims, it violates architecture.

Can Git alone prevent this? No. Campaign branch technically accepts any valid commit.

This is no different from other application invariants/authorization: GitHub is storage, not the semantic transaction validator.

Use bounded integrity detection and branch protections/server-side validation if a future deployment wants defense in depth. Do not introduce a second authority system solely to protect against application code intentionally violating its own protocol.

Pass with implementation invariant.

---

# 12. Revocation race — initial research ordering fails

Initial research sequence suggested:

```text
close live E
absorb E to campaign
persist PLAYER inactive
```

Counterexample:

1. close succeeds, fencing old live writes;
2. campaign absorption succeeds and clears live route;
3. PLAYER_B is still active until next commit;
4. stale B session refreshes campaign and is now technically/application-authorized to perform a normal campaign write before deactivation commit;
5. creator deactivation races that write.

Step 5.6 CAS serializes the writes but does not ensure deactivation wins; if B writes first, B made a legitimate current campaign mutation after live close.

If the intended product edge is “creator has revoked B once boundary completes,” there should be no reopened write window between live absorption and revocation.

Refinement:

> After affected live epochs are successfully CLOSED, one campaign transaction SHALL both absorb/finalize those live results and apply the authorization/controller transition when those changes are one semantic maintenance boundary.

Conceptually:

```text
E ACTIVE
 -> close E
 -> campaign TXN {
       absorb E final state
       clear E route
       PLAYER_B active -> inactive
       controller changes if any
       recovery/index consequences
    }
```

After campaign TXN succeeds, campaign becomes current with new authorization already in effect.

If TXN fails, E remains current closed truth and revocation is not yet acknowledged/effective.

This is much stronger.

---

# 13. Race: player write versus close for revocation

Suppose B writes from L0 while creator is trying to revoke B.

### B wins CAS first

B's shared action was accepted while old authorization still held.

Closer's L0 close rejects. Closer refreshes L1 and closes from L1. Final campaign transaction absorbs B's accepted last action and deactivates B.

No retroactive erasure.

### Close wins first

B's write from L0 rejects. B refreshes CLOSED state; ordinary live retry forbidden. Campaign boundary later deactivates B.

No stale success.

This is a clean linearization of the revocation edge without wall-clock semantics.

Pass.

---

# 14. Controller transfer has the same atomicity requirement

If PC_A controller changes from PLAYER_A to PLAYER_B while PC_A is live-claimed:

- close affected epoch(s);
- one campaign transaction absorbs final live state + changes controller/bindings/routing consequences;
- successor opens under new auth.

Do not absorb, briefly restore campaign authority under old controller, then transfer in a later commit.

Pass with same refinement.

---

# 15. Late join / authorization grant

Granting a new player write authority is less dangerous than revocation because an old unauthorized session cannot become more powerful before the grant is durable.

However if the participant set itself changes the scene's observable/private knowledge contracts or the new controller must mutate an already-active shared scene, safest simplified rule is still epoch-boundary adoption:

- if adding the player/controller changes current live authorization or claim/knowledge topology materially, close/absorb + grant in one campaign boundary then open successor;
- purely read/observer capability may follow its own access rules without forcing a live writer transition if it cannot mutate current claims.

This avoids trying to mutate the live participant/security model dynamically.

---

# 16. Entity transfer — source-only freeze is insufficient

Current old prose says freeze/compact source before entity enters destination live epoch.

Counterexample:

- E1 currently owns X;
- E2 already active and its players could interact with destination environment;
- E1 closes/absorbs X into campaign and updates X location to E2's scene;
- E2 remains based on an older campaign base that did not contain X and continues accepting writes;
- E2 and campaign now disagree about its relevant scene composition; E2 may create conflicting facts around X.

Therefore when an existing current live destination is affected, destination must join the ownership boundary.

Refinement:

```text
close E1
close E2 (if destination/current dependencies materially affected)
exact-pin both final sources
campaign TXN {
    absorb E1
    absorb E2
    apply X transfer
    clear/update routes
}
open successors with disjoint claims
```

If destination has no active live epoch, only source needs freeze before campaign transfer.

Pass with multi-live freeze slow path.

---

# 17. Can closing multiple live epochs sequentially create inconsistent fiction?

For cross-scope transfer/global event, E1 may close before E2. During the interval:

- E1 current truth is closed/frozen;
- E2 remains active/current/writable;
- global event/transfer is not yet established.

Could E2 accept an action that changes whether the planned global event is valid? Yes. Then the closer must refresh/revalidate and possibly close from the newer E2 state. The event is not committed until all required sources are frozen and rules/chronology resolve from their final states.

The physical order of closing E1/E2 is not fictional event order. Step 5.9 will determine necessary chronology.

Crash after closing only E1 is recoverable: E1 stays frozen, E2 active. An authorized process may resume the boundary or, if the intended operation is abandoned and architecture allows no reopening, it must still absorb/roll E1 forward rather than reactivate it. This can incur maintenance work but preserves monotonicity.

Pass.

---

# 18. Should a closed epoch ever reopen if operation is abandoned?

Temptation: if a planned transfer/revocation is cancelled after close, just set `closed -> active`.

Reject.

Reasons:

- stale clients may have observed close and followed routing recovery;
- terminal close is the fencing proof;
- reopening weakens the simple lifecycle and complicates ambiguous outcomes;
- successor rollover is cheap enough at boundary scale.

Rule:

> CLOSED is terminal. If the initiating maintenance operation is abandoned, absorb/forward-resolve the closed state and open a new epoch if continued live play is needed.

This may create extra commits after a failed/cancelled boundary but preserves a much stronger protocol.

---

# 19. Campaign absorption overlap while E is closed

Once E is selected and claims Q, conforming campaign gameplay cannot mutate Q. Therefore an overlapping campaign change to Q during E active/closed should normally arise only from:

- maintenance/repair/migration that explicitly participates in the boundary;
- stale/broken implementation;
- manual repository edit;
- another live route invariant violation.

At absorption:

- movement on disjoint campaign paths can be transport-rebased under Step 5.6;
- movement touching Q is not generic YAML merge input;
- authorized participating maintenance may have an explicit native reconciliation rule;
- otherwise classify as integrity/semantic revalidation, not ordinary automatic merge.

This is stricter than old prose's generic “compare touched paths and reconcile overlap,” because fixed claims make overlapping campaign mutation mostly illegal while live ownership exists.

Pass; candidate should encode this improvement.

---

# 20. `touched_*` remains useful even with claims

Fixed Q answers **who may mutate**.

Cumulative touched paths/owners answer **what actually changed** and can optimize:

- final campaign write-set derivation;
- disjoint external campaign movement classification;
- audit/provenance;
- conflict revalidation.

They must not become authority or completeness proof for Q.

Keep conceptual distinction:

```text
CLAIM SET      -> prospective authority boundary
TOUCH SET      -> retrospective mutation/dependency evidence
```

Pass.

---

# 21. Cross-source mutable read dependencies expose a harder race

An active live action may depend on campaign owner Y that is **not** claimed by E.

If Y is immutable/stable for the action, no issue.

If Y may mutate concurrently and its value can change action legality/result, merely reading current campaign Y before live CAS has a TOCTOU race because campaign and live refs cannot be atomically compared/updated together.

Options:

A. claim Y into E dynamically — rejected complexity;
B. read/revalidate campaign immediately before live CAS — still leaves a residual race;
C. ignore race — incorrect if the dependency is materially contested;
D. classify it as a cross-scope synchronization boundary.

Recommended refinement:

> An ordinary live action may depend on an external campaign/native owner without ownership transfer only when the owner contract/current situation permits that dependency to be treated as stable, causally independent, or safely reconciled under later chronology semantics. A correctness-critical concurrently mutable dependency that can invalidate the action requires a bounded cross-scope synchronization boundary, which may close/absorb/repartition affected ownership before establishing the dependent effect.

This is not an excuse to claim every read dependency. It is a precise escalation criterion.

Step 5.9 supplies temporal reconciliation for cross-scene dependencies; 5.8 supplies the ownership/freeze substrate.

Pass with explicit cross-scope boundary rule.

---

# 22. Does this force too many global boundaries?

No if scopes are chosen correctly.

Most scene actions depend on:

- local claimed current actors/assets/effects;
- immutable/adopted rules;
- campaign facts that do not concurrently mutate in a materially relevant way.

Cross-scene races/global processes are exceptional and already slated for slow-path chronology synchronization.

The architecture must not turn “any referenced campaign record” into an ownership claim. Claims are only for current mutation authority/concurrency-sensitive ownership.

---

# 23. Ambiguous live CAS — ancestry is not current-value proof

Suppose intended live commit C was sent, acknowledgement lost, then another writer publishes D on top.

If C is ancestor of D:

- C definitely entered live durable lineage;
- the semantic action represented by C was published, subject to receipt/idempotency validation;
- values in C may no longer be current at D.

Therefore:

```text
historical publication proof != current source-state proof
```

After confirming publication, runtime must adopt D/current authority for subsequent adjudication/narration and validate current closure/dependencies.

It must not tell the player a stale present-tense state solely from C if D already legitimately changed it.

This mirrors Step-5.6 ambiguity refinement.

Pass.

---

# 24. Ambiguous close outcome

Close CAS outcome lost.

Read current live source:

- current source is intended closed C -> close confirmed;
- current source descends from C -> impossible for conforming ordinary writers because C is terminal; descendants may be maintenance-only. Validate lifecycle/operation evidence;
- current source still active without C lineage -> close did not become current; retry/replan from actual active state;
- current source cannot be resolved -> BLOCKED/ambiguity/infrastructure.

Do not route campaign authority away until close is confirmed/verified.

Pass.

---

# 25. Ambiguous campaign absorption outcome

Step 5.6 already resolves this from actual campaign current authority.

Need live-specific postconditions:

Successful absorption proof must show current campaign routing/owner state is compatible with:

- absorbed epoch identity;
- exact final closed live source revision;
- required typed owner materialization;
- claim release/route change;
- any joined authorization/entity-transfer transition.

If current campaign still selects E closed and does not record its exact final absorption, E remains current truth and compaction is pending.

Pass.

---

# 26. Is `last_absorbed_live_head_sha` alone enough?

Potential collision/ambiguity is extremely unlikely at Git identity level, but semantics should not depend on field name implying one global scalar.

For one scene's sequential epochs, the exact final live head normally identifies the absorbed source strongly. But migration/branch reuse/tooling could be clearer if absorbed evidence conceptually binds:

```text
scene/scope identity
epoch identity
final live source revision
```

The exact wire representation need not be a new struct if scene route already supplies enough context.

Candidate should state semantic identity tuple while leaving schema spelling to implementation.

---

# 27. Successor opening before absorption is dangerous

Could prepare successor E2 early while E1 closed to reduce latency.

Preparation may be harmless if E2 remains nonauthority and does not embed a base that assumes an unpublished absorption result.

However selecting E2 before E1 absorption would create current route to a source whose campaign base does not contain E1 final state, or require circular/self-referential base semantics.

Rule:

- speculative infrastructure preparation may occur only when its bytes/identity do not claim a future authority basis;
- authoritative E2 initialization/selection uses the actually current post-absorption campaign source.

Do not optimize this boundary prematurely.

Pass.

---

# 28. One physical LIVE_STATE file as mega-owner

Counterexample to naïve envelope semantics:

If `LIVE_STATE` contains:

```text
NPC state
Procedure state
knowledge list
observable event
pending durable event
```

and architecture says “LIVE_STATE owns it,” Step 2–4 ownership is erased.

Required refinement:

- physical live source/envelope is a durability/atomicity container;
- every contained authoritative subpayload has typed native owner identity;
- native lifecycle/validation remains per owner contract;
- recovery routing can enumerate those owner identities;
- compaction writes each back to correct campaign native representation;
- projection/evidence payload stays labelled nonauthority where applicable.

The current schema will require substantial realization changes, but no new semantic mega-owner is introduced.

Pass.

---

# 29. Can one-file physical atomicity still be retained?

Yes logically.

A single Git blob can encode typed sections while source HEAD is the publication CAS. It gives atomic replacement of all live-local representations for one logical shared action.

Potential issue: size growth and merge cost.

Current rollover policy already limits hot-state growth. Step 5.8 does not need to mandate multiple files before measurement.

If implementation later splits physical files, one logical live transaction must still advance one source ref from expected prior head with one complete atomic commit/tree, preserving equivalent CAS semantics.

Pass.

---

# 30. External/manual Git writes

Could a repository admin write to closed branch, reactivate it, or modify claimed campaign owner directly? Yes, unless external branch protection/server validation forbids it.

This is not evidence the logical architecture needs per-turn global locking.

Architecture scope:

- normal runtime writes are Python-owned and validated;
- repository permission != semantic authorization;
- unexpected persisted contradictions are integrity defects;
- no force-push recovery;
- optional future branch protection can provide defense-in-depth.

Pass.

---

# 31. RepositoryPort requirements exposed by 5.8

Step 5.8 should require a live-source primitive conceptually equivalent to:

```text
LiveSourceCASRequest {
    source_ref
    expected_source_revision
    exact complete mutation payload/tree
    acting_principal
    operation_kind: GAMEPLAY_MUTATION | CLOSE | MAINTENANCE
}

LiveSourceCASOutcome {
    ACCEPTED(new_revision)
    REJECTED(current_revision / typed reason)
    INDETERMINATE
}
```

No exact Python names are architectural.

For current one-file fallback, blob-SHA guarded update approximates this.

Preferred future Git backend can use commit/ref expected-head CAS (`createCommitOnBranch(expectedHeadOid)` or one-parent commit + non-force ref update), because head-level CAS generalizes if the live source gains more than one physical file.

Do not specify LLM tool calls in runtime semantics.

---

# 32. Does normal hot path need campaign route check every turn?

Strongest safety argument for yes: a route/membership change could happen behind the live session's back.

But all **valid route-away/revocation paths affecting an active epoch must first close that same live source**. Therefore the live source itself carries the detectable fence.

A normal action already probes current live ref. If route changes legally, it cannot remain ACTIVE unchanged.

Thus repeated campaign route check is redundant for normal hot writes and would add latency.

Exceptions requiring campaign check remain:

- live source is CLOSED;
- action depends on mutable state outside claims;
- opening/adoption/recovery;
- explicit resync/integrity suspicion;
- campaign maintenance/global boundary.

This is a major performance benefit of the terminal-close invariant.

Pass.

---

# 33. Can campaign route legitimately change while live remains active?

Only changes that do not remove/replace E's authority and do not alter its claim/authorization contract might be possible, but allowing mutable route metadata during ACTIVE creates unnecessary complexity and race reasoning.

Simpler rule:

> The selected live route identity and immutable mutation claim set are stable for the epoch's ACTIVE/CLOSED_UNABSORBED lifetime. Any material route/claim/participant/controller change that affects ordinary mutation semantics requires close and successor lifecycle.

Nonsemantic descriptive metadata need not be part of the live route at all.

Pass.

---

# 34. Live participants versus authorization

Current live participant lists represent who is in the scene / relevant to live interaction.

They must not become ACL authority.

Could a scene participant be NPC/no player? yes.
Could an active PLAYER be authorized campaign-wide but not control the acting PC? yes.
Could creator have maintenance authority without being participant? yes.

Therefore every write still resolves current application authority under the owning operation contract.

For hot performance, stable accepted authorization can be cached while ACTIVE because revocation requires source close. Technical acting principal remains required at publication.

Pass.

---

# 35. Knowledge/disclosure race during live mutation

Suppose PC_A sees fact F and the same shared action establishes F objectively.

One atomic live source publication may physically include:

- objective F owner update;
- world.knowledge(A,F) transition/evidence;
- semantic event/perception evidence.

This is acceptable because physical atomicity does not merge semantic ownership.

Human disclosure to player A happens only after host emission under Step 4/5.12. It cannot be recorded merely because the live event says PC_A perceived F.

If live publication succeeds but narration/emission fails, world/PC knowledge may still have advanced while human disclosure has not. This is a valid distinction, not rollback reason.

Pass.

---

# 36. Cross-scene chronology interaction

Closing E1 then E2 does not establish E1's fictional event before E2's.

Campaign absorption commit order likewise only shows storage publication order.

5.8 must expose exact source/event identities and frozen authority substrate so Step 5.9 can reconcile minimal chronology.

No global live sequence should be added here.

Pass.

---

# 37. Abandoned/stuck CLOSED epoch

A cold host finds route -> CLOSED E, unabsorbed.

It cannot ordinary-play in E and cannot fall back to campaign.

Options:

- authorized host resumes compaction;
- if transient repository failure, retry later;
- if required source/integrity missing, BLOCKED/suspect;
- independent/OOC scopes may continue.

Do not reactivate E simply because the original closer disappeared.

This trades availability for a very small, deterministic state machine and is consistent with controlled failure semantics.

Pass.

---

# 38. Orphan live branch

Prepared branch exists, no current campaign route selects it.

It is never current gameplay authority regardless of:

- newer timestamp;
- more commits;
- matching scene ID;
- matching deterministic branch name;
- cached local pointer.

Ignore for ordinary recovery. Step 5.13 may clean it.

Pass.

---

# 39. Overlap between live claim set and operational owner routing

An open Procedure/Resolution may be scene-local and needs durable recovery while scene is live.

Do not merely claim the world actor and leave Procedure state campaign-writable if action execution can continue concurrently through live.

The live claim/admission model must work for **typed mutable native owner refs**, not only world entity IDs.

Likewise live-local Step-5.2 root routing must be available from the selected live source/partition.

This may expand implementation schema but is required by inherited architecture.

Pass.

---

# 40. Claim-set completeness is correctness-critical but not world closure

Missing a mutable owner from Q can create double authority if live mutates it anyway.

Therefore before a live transaction writes owner X, Python core must assert:

```text
X is epoch-born/live-local
OR
X is admitted in current route claim Q
```

If not:

```text
do not publish mutation
initiate ownership-boundary/rollover or re-plan action
```

This check is local once route Q is cached.

No recursive graph closure is implied.

Pass.

---

# 41. Fixed claim set and read-only global data

Do not claim an owner merely because it is read.

Examples:

- immutable lore/rules input can remain campaign source;
- distant faction state referenced for description but not concurrently mutable/relevant need not transfer;
- a material mutable global process whose concurrent advancement can change the action is a cross-scope synchronization dependency and triggers the slow path.

This keeps Q bounded.

Pass.

---

# 42. Failure-isolation matrix

| Condition | Correct classification |
|---|---|
| live HEAD moved by valid writer | refresh/retry, not corruption |
| CAS rejected because close won | follow CLOSED routing, no gameplay retry |
| repeated active CAS contention | bounded coordination outcome |
| selected live branch missing | BLOCKED + scope CANON_SUSPECT |
| orphan unselected branch | NONAUTHORITY / cleanup candidate |
| closed selected branch | current truth valid, gameplay mutation blocked, resume compaction |
| campaign route changed after confirmed close/absorption | adopt current route / retry |
| campaign route moved away while previous selected live remains ACTIVE without valid close evidence | integrity suspicion |
| claim overlap persisted between two selected live routes | CANON_CORRUPT/suspect depending evidence |
| stale player attempts old live revision after revocation close | CAS reject |
| technical credential lacks trustworthy principal | authorization/infrastructure BLOCKED |
| cross-source mutable dependency contested | synchronization/chronology slow path |
| optional Story projection stale | no gameplay authority impact |

---

# 43. Revised architecture recommendation

The challenged recommendation is now:

> **ROUTED FIXED-CLAIM LIVE EPOCH / HEAD-CAS MUTATION / TERMINAL SOURCE FREEZE / FORWARD CAMPAIGN ABSORPTION**

with these exact conceptual roles:

```text
Campaign LiveRoute
    current authority selector for one scene-centered epoch
    immutable typed mutation claim refs Q
    source identity/base metadata

Live source exact HEAD L
    current physical native source revision
    CAS fence for all live mutations

Live lifecycle ACTIVE | CLOSED
    ACTIVE  -> current truth + ordinary writes admitted
    CLOSED  -> current truth + ordinary writes forbidden
    CLOSED is terminal

Player/controller authorization
    separate application authority
    revocation/controller change joins post-close campaign absorption boundary

Native semantic owners
    remain typed owners despite physical live storage
```

State transitions:

```text
campaign current
   |
   | prepare candidate (nonauthority)
   | campaign CAS selects route E,Q
   v
E ACTIVE @ L
   |
   | multi-writer expected-L CAS
   v
E ACTIVE @ L+n
   |
   | terminal close CAS
   v
E CLOSED @ Lf
   |   truth current, ordinary writes = 0
   |
   | one campaign absorption/transition transaction
   v
campaign current
   |
   | optionally open new E2,Q2
   v
E2 ACTIVE
```

Cross-live entity/global transition:

```text
freeze all affected writable live sources
 -> one campaign absorption/transition basis where possible
 -> Step-5.9 chronology/semantic reconciliation as needed
 -> successors
```

---

# 44. What remains for candidate specification

Candidate must formalize laws for:

1. current truth versus ordinary write admission;
2. route selection as authority;
3. immutable fixed mutation claims;
4. no overlapping selected claims;
5. native semantic owner preservation;
6. head revision as CAS fence;
7. integer live revision nonauthority;
8. ACTIVE/CLOSED monotonic lifecycle;
9. mandatory close before route-away;
10. commit-before-shared-reveal;
11. exact live mutation result classification accepted/rejected/indeterminate;
12. stale disjoint/overlap semantics;
13. ambiguous outcome/idempotency;
14. opening/prepared orphan semantics;
15. campaign write guard for claimed owners;
16. closed-unabsorbed recovery;
17. absorption atomic campaign batch;
18. absorbed-source idempotency tuple;
19. successor ordering;
20. revocation/controller transition joined with absorption;
21. late join/grant boundary;
22. entity transfer involving destination freeze;
23. multi-scope slow path;
24. external mutable dependency escalation;
25. Step-4 knowledge/disclosure separation;
26. live-local Step-5.2 root routing;
27. principal/auth requirements;
28. hot-path bounded I/O;
29. external/manual mutation integrity handling;
30. no heartbeat/lease/leader/global sequence/distributed transaction.

No owner decision brief is currently required unless candidate/adversarial review reopens a material product choice.
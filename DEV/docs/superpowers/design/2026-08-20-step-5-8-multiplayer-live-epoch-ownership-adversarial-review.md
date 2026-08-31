# Step 5.8 — Multiplayer / Live-Epoch Ownership — Adversarial Review

Status: **ADVERSARIAL REVIEW — CANDIDATE NOT YET READY FOR CANONICALIZATION**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Reviewed candidate:

- `2026-08-20-step-5-8-multiplayer-live-epoch-ownership-candidate-spec.md`

Review posture:

> Attempt to falsify the candidate under concurrent writers, crash windows, current HDM identity allocation, Step-3 execution continuity, Step-4 information ownership, Step-5.2 recovery routing, Step-5.5 save/handoff promises, temporal obligations, and the practical ChatGPT/GitHub host model.

The review deliberately distinguishes:

- safety defects;
- liveness/availability limitations;
- performance/scaling defects;
- missing cross-system contracts;
- non-goals/manual bypasses that should not distort the ordinary hot path.

---

# 1. Executive verdict

The candidate's central authority-transfer direction **survives** the review:

```text
current campaign route
    -> one selected live epoch
    -> exact-source-revision CAS writes
    -> terminal ACTIVE -> CLOSED source fence
    -> closed/unabsorbed zero-writer interval
    -> one forward campaign absorption transaction
```

No review finding justifies adding a long-lived leader, TTL lease, heartbeat, distributed transaction, global scalar frontier, or generic fencing-token service.

However, the candidate is **not ready to canonicalize**. Four blocking gaps must be resolved first:

1. **live-local persistent ID allocation is missing and conflicts with the current campaign-scoped allocator contract;**
2. **the candidate over-compresses a logical action into one live publication and does not fully specify terminal close versus already accepted Step-3 execution state;**
3. **claim authority is explicit, but bounded machine-decidable claim lookup/non-overlap proof is not guaranteed;**
4. **scene-centered live packing lacks an explicit containment rule for native owners whose writable lifetime/scope is not contained by one scene epoch, especially Procedure/Continuation/temporal owners.**

Additional required strengthening is needed for:

- explicit save while live sources continue moving;
- controlled handoff with accepted in-flight live execution;
- temporal obligations across CLOSED/absorption;
- additive authorization grants versus revocation;
- revocation liveness under continuous hostile/contended writes;
- partial multi-scope freeze dependency gating;
- one-file Contents-CAS fallback assumptions;
- Step-4 disclosure as a separate post-emission durability edge.

The recommended resolution keeps the candidate's core architecture and tightens these boundaries; it does not replace the candidate with a different concurrency model.

---

# 2. Blocking finding B1 — campaign-scoped ID allocator is incompatible with independent live hot paths

## Existing contract

Current catalog architecture says:

```text
persistent world-record IDs
+ independently numbered runtime records
    -> campaign-scoped counters
    -> runtime.id_allocator = campaign-allocator

allocation + record creation = one atomic operation
```

Current identifier policies still mark many relevant kinds as campaign-sequential, including:

- `runtime.interaction`;
- `runtime.procedure`;
- `runtime.resolution`;
- `runtime.mechanical_event` in the current machine policy, notwithstanding later Step-3 derived event-identity semantics;
- `runtime.semantic_event`;
- many world owners.

Step 5.2 also treats `runtime.id_allocator = campaign-allocator` as the known allocator singleton.

## Attack

Two independent selected live epochs E1/E2 execute concurrently.

Each ordinary live action may need to create durable identities such as:

```text
RuntimeCommand / Resolution
Procedure
Continuation descendant identity
events/semantic evidence
new world owner(s)
```

If those identities still require the campaign allocator, then a correct allocation requires a campaign-domain write before or atomically with each live creation.

That produces one of three bad outcomes:

1. **campaign write per live action** — destroys the intended hot path and introduces cross-domain contention;
2. **live copies of campaign allocator state** — duplicate allocation authority and allow collisions;
3. **allocate locally then rekey at absorption** — breaks stable execution/idempotency/provenance identities for owner classes whose IDs have already escaped into receipts/firing keys/causal references.

Therefore the current candidate cannot claim independent live hot-path creation while retaining the current allocator contract unchanged.

## Required resolution

Step 5.8 must introduce or explicitly require a **collision-free live-epoch identity namespace** for identities that become durable inside a live source.

Recommended direction:

```text
stable unique epoch_id E
+ source-local accepted transition/creation ordinal(s)
+ kind/local ordinal
    -> globally unique stable live-born ID
```

Properties:

- allocation happens inside the same accepted live CAS/segment boundary as creation;
- two writers preparing from the same live revision may propose the same next local slot, but only one CAS can accept it;
- rejected prospective IDs never become canonical and may be discarded/rederived;
- accepted live-born IDs never need rekeying merely because E is absorbed into campaign;
- no cross-epoch comparison/order semantics are inferred from the local ordinal;
- campaign allocator remains owner only for campaign-native allocation domains that actually use it.

Exact string spelling and whether an ID is derived from `(epoch_id, accepted live transition ordinal, local ordinal)` or an equivalent collision-free source-local identity is implementation detail.

World entities may use provisional identity only when their owner contract explicitly permits rekey/promotion and no durable external reference escapes before promotion. Step-3 execution, receipt, firing and other idempotency-critical identities must remain stable once accepted.

## Severity

**BLOCKING / ARCHITECTURAL.**

Without this resolution the live hot path contradicts the current ID architecture.

---

# 3. Blocking finding B2 — one logical action is not necessarily one live CAS; close/in-flight execution semantics are underspecified

## Existing Step-3 contract

Step 3 defines `ExecutionSegment` as the smallest local atomic execution/persistence boundary.

One command/action may require multiple committed segments, including a continuity-only segment that persists:

- fixed RNG;
- cursor;
- Continuation;
- choice/reaction suspension;
- idempotency evidence;

without yet committing the final world mutation.

MechanicalEvent/mandatory-child identity may also be committed before all descendant work settles.

## Candidate problem

Candidate laws/phrasing such as:

```text
one logical shared mutation -> one live source publication
```

are too strong if interpreted as one publication per high-level player action/turn.

A realistic live interaction may need:

```text
CAS 1: accept root command / continuity state
CAS 2: commit segment/world consequence
CAS 3: later consume reaction/choice continuation
CAS 4: post-emission disclosure update (Step 4/5.12 boundary)
```

Trying to collapse these into one publication would either:

- violate Step-3 segment semantics;
- retain correctness-relevant accepted state only in volatile host memory;
- make external choice/reaction span one impossible repository transaction;
- incorrectly pre-record human disclosure before host emission.

## Close race attack

Host A has accepted/fixed execution state in memory or in a prior live segment.
Host B concurrently performs `ACTIVE -> CLOSED`.

Cases must be distinguished:

### Case A — work was only prospective/uncommitted

The close may legitimately win. The prospective consequence never became established live canon.

The old host's stale CAS fails. It must not narrate the consequence as committed.

### Case B — RuntimeCommand/Resolution/Continuation/fixed RNG was already durably accepted in E

The close does **not** cancel or discard that native owner.

The exact accepted operational state is part of E@Lf and must remain reachable through Step-5.2 routing, then be absorbed/moved/continued according to its native lifecycle.

### Case C — an accepted player input has been explicitly promised across a handoff/save boundary but sufficient typed execution state is not yet durable

The close/handoff boundary cannot truthfully complete until that promised input is materialized into recoverable native state or explicitly returned to the owning workflow as unresolved/not accepted.

## Required resolution

Replace any high-level one-action/one-write invariant with:

> **Each native atomic execution/lifecycle durability edge that establishes live-owned state is published as one complete source transition; no one such edge is split into per-owner/per-field partial writes. A single user action may legitimately span multiple live source transitions when Step-3 execution, external choice/reaction, or Step-4/5.12 delivery semantics require multiple edges.**

Add explicit close law:

> **Terminal close fences future ordinary live mutation but does not revoke already committed native execution state. Prospective unpublished work may be invalidated; accepted durable execution owners and required recovery evidence survive in the final closed source and through absorption.**

## Severity

**BLOCKING / CROSS-STEP CONSISTENCY.**

---

# 4. Blocking finding B3 — claim sets exist, but bounded claim lookup/non-overlap proof is not guaranteed

## Attack

Candidate correctly rejects retrospective `touched_entity_ids` as authority and introduces fixed claims Q.

But two core operations require the inverse question:

```text
ClaimAuthorityLookup(X)
    -> campaign | live route E | integrity conflict
```

They are:

1. before ordinary campaign mutation of X;
2. before opening/selecting a new route whose Q must not overlap existing selected claims.

If Q exists only inside per-scene route records, a writer may have to scan every active scene/live route to prove that X is unclaimed.

That violates the project requirement that correctness should not require campaign-wide/world-wide scans and creates a scaling cliff as active scenes grow.

`CURRENT.active_scenes` is useful routing evidence but does not by itself map arbitrary typed native owners — especially Procedure/effect/knowledge/operational owners — to their current writable partition.

## Required resolution

Step 5.8 must require the following property without mandating a universal global table:

> **For every native owner/scope class admitted to live mutation, current write-authority routing must be machine-decidable through bounded typed routing from the owner/scope identity. Opening overlap checks and campaign-side mutation admission must not require scanning the campaign/world/all live branches.**

Acceptable physical realizations may differ by owner:

- direct owner -> scene/live-scope routing where the native owner already exposes it;
- compact active-live routing partitions;
- a derived/materialized claim index maintained in the same campaign authority transaction as route selection/release;
- another typed bounded owner-specific lookup.

Any such index is routing evidence, not duplicate current-state authority.

The candidate's rejection of a mandatory campaign-global `entity -> live_epoch` table remains valid; what must be rejected is **unbounded claim discovery**, not every bounded routing index.

## Severity

**BLOCKING / PERFORMANCE + CORRECTNESS DISCOVERY.**

---

# 5. Blocking finding B4 — scene-centered live packing needs an explicit native-scope containment rule

## Attack

A `runtime.procedure` is an independently addressable native owner whose lifetime is not defined by Scene lifetime.

A Procedure may:

- survive gaps between Commands;
- survive scene/encounter changes;
- be referenced by multiple Resolutions;
- potentially involve state whose semantic scope is broader than one current scene.

Likewise, independently-due temporal owners retain their own lifecycle/routing and may not be duplicated merely because their current representation is physically convenient to pack into one live file.

If candidate E1 claims Procedure P merely because a participant is in scene S1 while another relevant live scope also depends on P, then either:

- P is duplicated across live domains; or
- one scene becomes accidental authority over a cross-scene owner.

Both violate Step 3/5.2 ownership.

## Required resolution

Add a **live-containment admissibility law**:

```text
native owner/scope X may be live-claimed by epoch E
ONLY IF
X's current writable semantic partition is fully contained by E's admitted mutation partition
```

Consequences:

- scene-local actor/asset/effect/knowledge partitions may be claimed when their owner contract supports that routing;
- a Procedure/temporal/global owner whose writable scope spans multiple live partitions remains in its own native partition or forces an explicit cross-scope synchronization/repartition boundary;
- physical inclusion in `LIVE_STATE` does not by itself prove containment;
- Step 5.8 introduces no generic field-level/subowner partition language;
- an owner-defined typed writable subpartition may be claimed only when that owning contract already makes its membership/disjointness machine-decidable.

## Severity

**BLOCKING / DUPLICATE AUTHORITY RISK.**

---

# 6. Required strengthening R1 — fixed claims should permit owner-defined writable partitions, not only record IDs

The candidate already uses `owner/scope` language, but several laws read as though Q is only a set of individual existing record IDs.

That is too brittle for owners such as Step-4 knowledge relations where normal scene activity may update several `(knower_id, fact_id)` relations over time.

The architecture should permit Q entries to be:

```text
exact native owner ref
OR
owner-defined writable partition ref
```

only when the native owner contract defines deterministic membership and non-overlap.

Do **not** introduce a generic selector/query language for claims.

This preserves fixed epoch ownership while avoiding unnecessary rollovers for every newly material existing row inside an already-owned native partition.

Severity: **HIGH, resolvable without changing the core model.**

---

# 7. Required strengthening R2 — explicit save over active live sources needs an exact final validation rule

Step 5.5 explicit save requires a definite selected save meaning and actual current durable closure.

Active live shared mutations are already write-before-reveal durable, so forcing every explicit save to close/absorb every active live epoch would be unnecessary and disruptive.

However the candidate must say how a save succeeds while live sources continue advancing.

Recommended rule:

1. freeze the save request's logical root/partition selection;
2. publish any campaign/local volatile dirty state required by the save;
3. for each participating live domain, require every established recovery-relevant mutation included by save policy to already be durable or CAS-flush any remaining live-local dirty owner generation;
4. at the final save gate, resolve/validate the **current** exact live source revisions and current routing composition;
5. if a live source advanced, that is not failure merely because it advanced — newly accepted shared live state is itself durable — but the final current composition must still satisfy RRC and the selected save promise;
6. if route/ownership movement makes the composition incompatible/ambiguous, retry/revalidate rather than claiming a scalar global save cut.

A save does not promise one cross-domain total order/snapshot.

If some live-local owner is allowed to remain established-but-volatile, the save must flush/fence that owner; it cannot rely on the statement that ordinary shared world mutations are usually already durable.

Severity: **HIGH.**

---

# 8. Required strengthening R3 — controlled handoff must distinguish current live durability from in-flight host-only work

The candidate is correct that no live leader must be transferred.

But `handoff alone does not require rollover` is safe only after the Step-5.4 handoff closure is actually satisfied.

Required rule:

- already accepted live-owned state at repository source revision L is handoff-safe when required Step-5.2 native roots/dependencies are durably recoverable there;
- host-only prospective work is not handoff state merely because a model computed it;
- accepted/promised execution state not yet represented in a durable native owner must be materialized before handoff acknowledgement or the handoff promise must remain incomplete;
- the receiving host then resolves current campaign route + current live revision and may adopt a newer valid L+n if other legitimate writers advanced it;
- no leader token is transferred.

Severity: **HIGH.**

---

# 9. Required strengthening R4 — temporal owners across CLOSED/absorption

Technical close is not fictional time advancement.

Therefore an armed independently-due owner packed in E does not become due merely because wall-clock time passes while E is CLOSED.

Required rules:

- armed temporal source enrollment remains valid in CLOSED E;
- absorption moves/rekeys that routing atomically with owner lifecycle as already required by Step 5.2/5.3;
- technical close/compaction does not itself fire/expire/advance an obligation;
- if another scope's chronology/event becomes materially related so that the frozen owner's due state must be resolved before transfer completes, this is a cross-scope chronology/synchronization boundary, not permission to mutate CLOSED E through ordinary live writes;
- no due obligation may disappear simply because the owner crossed live -> campaign durability domain.

Severity: **HIGH.**

---

# 10. Required strengthening R5 — additive authorization and revocation are asymmetric

Revocation/controller removal requires the close fence because stale sessions must lose future write admission.

An additive grant is different.

A new player/controller MAY be granted campaign authorization without closing E when all of the following hold:

- no existing authority is revoked;
- no claim set/owner partition changes;
- no current live state must be rewritten merely to add the principal;
- the new principal starts by reading current campaign grant/routing and current live source revision before its first write.

If the new participant requires a new PC claim, changed scene state, controller transfer, knowledge topology change, or another ownership change, use the appropriate epoch boundary.

This makes late join less disruptive without weakening stale-writer safety.

Severity: **MEDIUM/HIGH.**

---

# 11. Required strengthening R6 — revocation safety survives, but liveness under continuous old-authority writes is not guaranteed

## Attack

Old principal P is still valid until the close fence is accepted.

P continuously wins live CAS writes before the closer can publish `ACTIVE -> CLOSED`.

The candidate remains **safe**: every accepted write happened before the revocation fence and no post-close stale write succeeds.

But the revocation can be starved indefinitely because ordinary optimistic CAS supplies no fairness/priority guarantee.

Adding TTL/leader does not automatically solve this and would add the wrong infrastructure.

## Required treatment

Document an explicit liveness assumption/limitation:

> Step-5.8 guarantees revocation safety once the terminal live fence is accepted. Completion liveness assumes eventual write quiescence/fair opportunity for the closer. A continuously hostile or externally bypassing writer may require an out-of-band infrastructure authorization stop (repository/bridge permission revocation or equivalent deployment support) before application-level close can complete.

Do not falsely promise instantaneous revocation under an authenticated participant who can continuously submit valid pre-fence writes.

This is primarily a Step-6 deployment/security capability concern, not justification for a heartbeat leader.

Severity: **MATERIAL LIVENESS LIMITATION, not safety failure.**

---

# 12. Required strengthening R7 — partial multi-scope freeze must gate dependencies on frozen scopes

Candidate correctly says partial freeze after crash is recoverable and close order is not fictional order.

Add:

- an unclosed independent scope may continue ordinary play only while its current action does not depend on a frozen scope or on the unfinished global transition;
- any new cross-scope dependency on a CLOSED source must join/resume the synchronization boundary rather than treating that scope as ordinarily writable;
- closed-source reads remain current truth reads, but no new dependent transition may pretend the frozen owner can mutate until transfer completes.

Severity: **MEDIUM/HIGH.**

---

# 13. Required strengthening R8 — one-file Contents expected-blob fallback is conditional

The lab experiment confirms that, while the live ref has one runtime-mutated file, expected blob SHA rejects a stale writer after another write/close.

But expected blob SHA is not equivalent to exact ref-head CAS if some independent same-ref commit can change another path while leaving the live file blob unchanged.

Therefore:

> Contents/blob-SHA fallback is valid only while the physical live branch contract guarantees that the relevant runtime publication authority changes exclusively through that one file and no independent same-ref runtime commit can advance the branch outside that mutation.

If live source becomes multi-file or receives independent commits, use exact ref-head/expectedHeadOid-equivalent source CAS.

Severity: **MEDIUM, already mostly implied but should be explicit.**

---

# 14. Required strengthening R9 — Step-4 disclosure proves one user turn may require a post-emission write

Step 4 requires human disclosure to advance only after output is accepted/emitted on the player-facing host surface.

Therefore mechanics/world/fictional-knowledge commit and human-disclosure commit cannot in general be one pre-narration live CAS.

Consequences:

- `world.knowledge` may commit with the causal/perception event when fiction establishes it;
- `runtime.disclosure` waits for the host-delivery boundary owned by Step 5.12;
- a later disclosure mutation may be a second live or campaign-domain write according to its eventual native routing;
- failure to emit must not be repaired by rolling back committed mechanics/knowledge;
- candidate performance wording must not forbid this second persistence edge.

Step 5.8 need not decide exact delivery acknowledgement, but it must not claim one-CAS-per-turn semantics that makes Step 5.12 impossible.

Severity: **HIGH CROSS-STEP CONSTRAINT.**

---

# 15. Required strengthening R10 — indeterminate live publication blocks dependent progression until semantic outcome is known

If CAS outcome is INDETERMINATE and current lineage/receipts cannot yet prove whether the action committed, the affected root command/shared scope cannot safely accept a dependent new action as though either outcome were known.

Independent/OOC work may continue.

This is the live analogue of Step-5.6 ambiguity semantics.

Severity: **MEDIUM.**

---

# 16. Required strengthening R11 — live source may be delta authority over an immutable pinned campaign base

Current live representation is conceptually:

```text
base campaign state @ Hbase
+ selected live overlay/current owner materialization @ L
```

Therefore saying simply `E is current truth` must not imply that every current byte exists self-contained in E.

`Hbase` and any other required immutable interpretation/reference dependency remain part of the live source's Step-5.2 durable dependency closure.

Later campaign HEAD movement does not replace `Hbase` for inherited live fields.

Severity: **MEDIUM clarification.**

---

# 17. Required strengthening R12 — envelope growth is an availability/performance concern, not a heartbeat trigger

A one-file live envelope rewrites the complete file on each accepted shared transition.

If cumulative events/touch evidence grows without bound, write latency/bandwidth will eventually dominate.

Candidate already permits rollover for envelope growth. Strengthen this to require live envelope retention to remain bounded by actual current/recovery/idempotency needs:

- compact or move evidence whose native owner no longer requires it;
- rollover when practical source size makes hot-path performance unacceptable;
- never roll over solely because wall-clock age/turn count crossed a magic number;
- never discard receipt/firing/temporal evidence still required by open execution.

Exact size threshold is implementation/evaluation policy.

Severity: **MEDIUM performance requirement.**

---

# 18. Adversarial target matrix

| Target | Result | Finding |
|---|---|---|
| concurrent overlapping opening | PASS subject to bounded claim lookup | campaign CAS serializes route selection; overlap lookup must be bounded |
| concurrent disjoint opening | PASS | second opener repins/revalidates; no global leader needed |
| stale campaign writer vs new claim | PASS if ClaimAuthorityLookup is mandatory | campaign CAS fences pre-route writer; later writer must consult routing |
| active live writer vs close | PASS | exact source CAS provides safety; lab reproduced stale rejection |
| close ACK lost | PASS | exact current source lifecycle verification resolves/blocks |
| live mutation ACK lost + descendant | PASS WITH STRENGTHENING | lineage/receipts prove durable occurrence; dependent progression blocks while unresolved |
| route-away without close | PASS as integrity defect | candidate correctly rejects |
| absorption stale campaign HEAD | PASS | closed E immutable; Step-5.6 rebuild/reconcile applies |
| absorption ACK lost | PASS | current campaign route + absorbed tuple determine authority |
| duplicate absorption | PASS if evidence retained | exact `(scope,E,Lf)` idempotency evidence required |
| revocation race | SAFETY PASS / LIVENESS GAP | close fence safe; continuous writer may starve close |
| additive late join | OVER-CONSERVATIVE | safe no-close grant possible when claims/state unchanged |
| transfer into active destination | PASS | both materially affected epochs freeze before campaign transfer |
| partial global freeze crash | PASS WITH GATING | independent active scopes may continue only without dependency on frozen scope |
| Procedure/Continuation in live | FAIL AS WRITTEN | needs native-scope containment rule |
| independently-due temporal owner | INCOMPLETE | enrollment/chronology transfer across CLOSED must be explicit |
| PC knowledge + failed human emission | INCOMPLETE | disclosure is separate post-emission edge; one-CAS wording invalid |
| mutable external campaign dependency | PASS CONSERVATIVELY | cross-source atomicity is correctly refused; slow boundary when material |
| repeated contention | SAFETY PASS / AVAILABILITY LIMIT | bounded retries; no fairness guarantee |
| many active live routes / claim discovery | FAIL AS WRITTEN | bounded owner->authority lookup required |
| force/manual repository mutation | ACCEPTED NON-GOAL | integrity/repair path, not normal hot-path defense |
| explicit save with active live sources | INCOMPLETE | needs final current composed-source validation and treatment of any live dirty roots |
| controlled handoff active live | INCOMPLETE | must materialize promised in-flight accepted roots before ack |
| successor opening race | PASS | campaign CAS + fresh epoch identity |
| orphan GC | DEFERRED SAFELY | Step 5.13 must retain sources/evidence while still needed |
| live ID allocation | FAIL / CRITICAL | current campaign allocator contract cannot support independent live creation |

---

# 19. Rejected counterproposals after review

## 19.1 Add a TTL leader/lease

Still rejected.

It does not solve live ID allocation, Step-3 segment boundaries, claim lookup, or cross-scope Procedure ownership. It adds keepalive/liveness dependencies poorly matched to ChatGPT and still needs a real fencing/version check.

## 19.2 Add a global monotonically increasing fencing token

Still rejected as baseline.

Without one coordinator transaction spanning campaign and all live refs, a copied campaign token does not atomically fence an independent live write. The accepted `ACTIVE -> CLOSED` source mutation already supplies the actual stale-writer fence.

## 19.3 Put every live-created ID through campaign allocator

Rejected.

It restores correctness by destroying the live hot path and serializing independent scenes through campaign commits.

## 19.4 Rekey every live-created record at absorption

Rejected for accepted execution/idempotency/provenance owners.

Only explicitly provisional owner classes with no escaped durable references may be rekeyed.

## 19.5 Dynamically transfer arbitrary owner claims on every action

Still rejected as baseline.

The review found no correctness need that outweighs its cross-domain authority-transfer complexity. Prefer fixed/owner-partition claims + explicit rollover/slow boundaries.

---

# 20. Recommended candidate amendments before resolution gate

The next candidate/resolution pass should at minimum make these changes:

1. add a live-epoch stable ID namespace/allocation contract that eliminates per-live-action campaign allocator dependence;
2. redefine live publication atomicity around native execution/lifecycle durability edges, not one high-level action/turn;
3. define close behavior for prospective versus already committed execution state;
4. require bounded typed `ClaimAuthorityLookup`/overlap proof without global scans;
5. add live-containment admissibility for Procedure/temporal/cross-scope owners;
6. allow owner-defined fixed writable-partition claims where deterministic disjointness exists;
7. specify explicit-save final composed-source validation without forcing unnecessary live closure;
8. tighten handoff materialization of accepted live-local roots;
9. carry armed temporal owners/routing through CLOSED -> campaign without fictional-time side effects;
10. distinguish additive authorization grant from revocation/controller transfer;
11. record revocation liveness limitation/eventual-quiescence assumption;
12. gate dependent play during partial multi-scope freeze;
13. qualify one-file blob-SHA fallback;
14. remove any wording that forbids separate post-emission disclosure persistence;
15. block dependent scope while live publication outcome remains unresolved;
16. state pinned base campaign source as required live dependency when live state is overlay/delta-based;
17. preserve bounded live envelope growth without heartbeat policy.

---

# 21. Decision-rights assessment

Most findings are mechanical consequences of already accepted architecture and can be resolved by the agent without owner micro-decisions.

One potentially material cross-cutting decision may remain:

> **Should HDM permit stable live-born IDs from an epoch-qualified namespace, superseding the current assumption that all persistent independently numbered runtime/world records use the single campaign-scoped sequential allocator?**

Recommendation: **yes**, narrowly for records whose semantic acceptance occurs inside a live epoch and which must be created without campaign serialization.

Rationale:

- preserves independent live hot paths;
- preserves stable idempotency/provenance identity through absorption;
- avoids duplicate allocators and range-reservation bureaucracy;
- is naturally scoped by Step-5.1 domain typing;
- does not imply cross-epoch ordering;
- can retain ordinary campaign-sequential IDs for campaign-native creation.

A pure range-reservation alternative could preserve globally sequential-looking IDs but adds per-kind reservation/range-exhaustion mechanics with no demonstrated product value.

Confidence: **HIGH** that some non-campaign-per-write allocation mechanism is required; **MEDIUM-HIGH** that epoch-qualified stable IDs are the simplest correct choice.

What would change the recommendation:

- a hard product requirement that all persistent IDs remain one globally sequential campaign namespace;
- a repository/storage primitive that can atomically allocate campaign IDs and publish independent live-source mutation without serializing the hot path;
- evidence that stable live-born identities never need to survive outside E (contradicted by Step-3 execution/idempotency requirements).

---

# 22. Review disposition

```text
core ROUTED / HEAD-CAS / TERMINAL-CLOSE / FORWARD-ABSORB model
    -> SURVIVES

leader / TTL lease / heartbeat
    -> STILL REJECTED

distributed multi-live transaction
    -> STILL REJECTED

candidate as currently written
    -> NOT READY FOR CANONICALIZATION

next step
    -> resolve blocking findings and required strengthenings
    -> produce Step-5.8 resolution gate / revised canonical candidate
    -> only then canonicalize and close roadmap slice
```

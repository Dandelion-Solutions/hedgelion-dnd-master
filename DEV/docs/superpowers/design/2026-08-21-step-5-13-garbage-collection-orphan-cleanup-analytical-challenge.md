# Step 5.13 — Garbage Collection / Orphan Cleanup — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — RECOMMENDATION SURVIVES WITH REQUIRED TIGHTENING**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Challenged research direction:

> **OWNER-GATED RETIREMENT / CLOSED CLEANUP CONTRACTS / DERIVATIVE CANDIDATE DISCOVERY / CURRENT-BASIS BLOCKER PROOF / REPLACEMENT-BEFORE-REMOVAL / OPTIONAL REF CLEANUP / HOST-MANAGED GIT OBJECT GC**

Basis:

- Step-5.13 task brief;
- Step-5.13 research draft;
- canonical Steps 3 and 5.1–5.12;
- current Git/GitHub/Connector evidence.

No owner-level product decision has emerged. The challenge found several places where a superficially correct cleanup design could still destroy evidence; all are mechanically resolvable within inherited architecture.

---

# 1. Challenge method

The recommendation is attacked by trying to prove each of the following false:

1. owner-local contracts can provide a complete enough deletion boundary;
2. a closed cleanup contract can make negative dependency proof safe without becoming authority;
3. derivative reverse indexes can remain non-authoritative even when deletion relies on their currentness;
4. campaign CAS is sufficient to protect deletion against all relevant concurrent dependency creation;
5. opaque stable IDs can safely outlive deleted records without universal tombstones;
6. runtime idempotency/audit evidence can actually become removable;
7. Story/Transcript exactness can survive source-envelope retirement;
8. Git history can remain transport history without silently defeating Step-5.11 retention semantics;
9. ref cleanup can remain optional without leaking authority back through stale hosts;
10. the recommended hybrid is materially better than the simpler owner-local-only design.

The failure criterion is conservative:

> If the design cannot prove a target kind's complete blocker vocabulary and currentness basis, automatic deletion of that target kind is not admitted.

---

# 2. Challenge C1 — “closed cleanup contract” risks becoming a second authority

## Attack

Suppose cleanup adds:

```text
CleanupContract(runtime.message)
    blocking_ref_types = [...]
    terminality = ...
```

and the contract is wrong or stale after another subsystem evolves.

Then GC could delete a message still required by a new consumer. The cleanup contract would effectively decide liveness independently from the consumer's owner.

## Analysis

This is a real risk if blocker semantics are hand-maintained twice.

The contract must therefore not **invent** dependency membership. It only closes the vocabulary by declaring which owner-native typed dependency interfaces participate for a target kind/version.

Correct direction:

```text
consumer owner
    owns forward dependency

owner transition
    maintains required typed protection/routing evidence

cleanup contract
    names the admitted dependency class + query route
    but does not manufacture the dependency
```

If a new consumer needs a representation and fails to enroll its protection relation before that dependency becomes durable, that is a consumer implementation/integrity defect.

## Required tightening T1

A cleanup contract is a **compatibility/validation contract**, not liveness authority.

It may define:

- native terminality predicate to consult;
- admitted blocker classes;
- authoritative forward-owner source for each blocker class;
- required derivative routing/index consistency contract where used;
- survivor obligations;
- cleanup-contract generation/compatibility.

It may not create blockers by itself or override owner lifecycle.

**Disposition: recommendation survives.**

---

# 3. Challenge C2 — absence in a reverse index is unsafe unless the index has completeness semantics

## Attack

Research says derivative reverse indexes may support negative proof.

But ordinary “rebuildable index” semantics allow temporary omission. If deletion uses:

```text
reverse_index[target] == empty
```

while a live consumer exists but index update was lost, irreversible deletion follows.

## Analysis

Step 5.11 already anticipated this: stale derived exact-protection index cannot authorize payload loss, and routing must participate in durable closure strongly enough to avoid owner/index split.

Therefore there are two classes of derived indexes:

```text
BEST_EFFORT_DISCOVERY
    incomplete allowed
    cannot prove absence

PROTECTION_ROUTING
    derivative but completeness is a correctness invariant
    owner transition + enrollment/removal coherence required
    may participate in bounded negative proof after currentness validation
```

Calling both simply “rebuildable index” is too weak.

## Required tightening T2

For any reverse structure whose **absence** may authorize irreversible retirement:

- its completeness semantics for the target dependency class must be explicit;
- enrollment/removal must join the native owner transition's required durability closure sufficiently to prevent healthy owner/index split;
- the index/currentness basis must be validated at deletion time;
- if completeness cannot be proven, absence is non-evidence and deletion is blocked.

The index remains derivative because native forward owner dependency wins if loaded; it is correctness-critical routing evidence, not semantic ownership.

**Disposition: recommendation survives.**

---

# 4. Challenge C3 — campaign CAS cannot prevent a blocker born concurrently in another live source

## Attack

Candidate A is a campaign artifact.

Cleanup pins campaign H and proves no blocker.

Meanwhile independently writable live epoch E creates a durable reference/dependency to A. Cleanup then wins campaign CAS and removes A.

Campaign HEAD never moved because E wrote only its live source.

Result: current live owner depends on representation removed from campaign current tree.

## Analysis

This is a blocker for any dependency class that may originate in another native writable source.

There are only three safe patterns:

### Pattern X — dependency does not require current dereferenceability

The live owner pins or copies all required immutable historical content/identity under its own accepted execution contract. A later campaign current-tree deletion of A cannot affect it.

Example:

```text
open execution retains exact accepted interpretation/content needed
```

### Pattern Y — cross-source protection registration

Before live dependency becomes accepted, it durably establishes target-domain protection/routing evidence that campaign cleanup must consult.

The cross-source protocol must make “consumer accepted but protection not visible” impossible under its promise.

This is potentially expensive and must be admitted only for concrete target/dependency families.

### Pattern Z — synchronize/freeze affected source

For rare cleanup of a target that can gain new dereferenceable dependencies from active live domains without registration, freeze/reconcile the relevant owning source(s) before deletion.

No all-live scan is permitted; the target owner contract must provide bounded source/dependency routing.

## Required tightening T3

Every cleanup contract must classify blocker-creation concurrency by native source.

A deletion proof over campaign H is valid only when every source capable of creating a material blocker is either:

- irrelevant because accepted consumers are self-contained;
- represented through current protection registration visible to the proof;
- exact-pinned/fenced through a bounded synchronization boundary.

Otherwise deletion is not automatically admitted.

**Disposition: blocker mechanically resolved.**

---

# 5. Challenge C4 — Git history silently resurrects “deleted” exact transcript

## Attack

Step 5.11 says the Master is not a tape recorder and exact text may lawfully become unavailable after compaction.

But campaign Git history is append-only. Old commit B may still contain the exact message text after the current message record has been compacted/removed.

A future runtime could search Git history and quote the supposedly forgotten line exactly.

Then semantic retention policy would be defeated by transport residue.

## Analysis

This is a critical distinction:

```text
GIT TRANSPORT REACHABILITY
    !=
HDM RETAINED EVIDENCE ELIGIBILITY
```

Old history can remain for audit/transport provenance while HDM intentionally declares some payload unavailable to ordinary semantic/history retrieval.

Step 5.11 already says ordinary gameplay must not scan history and exact claims require retained exact evidence under the retention contract.

Therefore old historical blobs after semantic compaction are **non-admitted ordinary exact evidence** unless a specific repair/audit contract explicitly authorizes historical recovery.

## Required tightening T4

After Step-5.11 lawful exact compaction/current-source retirement:

- ordinary Master/Story/history retrieval SHALL NOT mine old Git commits to restore verbatim capability;
- transport-history presence does not reverse `SEMANTIC_ONLY` status;
- bounded integrity/security/authorized forensic repair MAY inspect historical transport evidence where its contract allows, but recovered data is not silently re-promoted to baseline retained Transcript memory;
- secure expungement of already-published bytes is outside ordinary Step 5.13 and requires explicit owner/support history-rewrite procedure if ever supported.

This law is necessary to keep the user-approved Selective Exact product semantics meaningful.

**Disposition: blocker resolved.**

---

# 6. Challenge C5 — stable provenance IDs without records can look like corruption

## Attack

Suppose SemanticEvent keeps:

```text
source_message_id = M17
```

and the compact M17 envelope is physically removed from the current tree.

Current runtime integrity guidance says a required reference resolving to no valid target is suspect.

Without tombstone M17, a normal loader may classify healthy compact history as corruption.

## Analysis

The problem is not necessarily missing tombstone. It is an underspecified reference contract.

References have materially different semantics:

```text
RESOLVABLE_REF
    target representation must currently resolve

OPAQUE_PROVENANCE_ID
    stable identity is sufficient; target dereference is not promised

SURVIVOR_BACKED_REF
    original target may disappear because a named compact survivor/anchor
    carries the required meaning/verification
```

Exact enum names are implementation detail, but the semantic distinction must exist.

A missing target is corruption only for reference contracts requiring current dereferenceability.

## Required tightening T5

Before deleting a target record:

- every surviving incoming reference must either be rewritten/promoted to a survivor;
- or its owning schema/contract must explicitly permit opaque non-dereferenceable provenance identity.

Unknown/legacy reference semantics default to **requires target / retain**.

No universal tombstone is required baseline.

A narrow immutable identity anchor/tombstone may be introduced only for a concrete target kind where stable dereferenceable identity remains promised and no natural survivor exists.

**Disposition: recommendation survives; tombstone YAGNI preserved.**

---

# 7. Challenge C6 — reference cycles can create immortal garbage or unsafe refcount logic

## Attack

Two retired records A/B reference each other for provenance.

If every reference is considered blocking, neither can ever be removed.

If generic reference counts are used, cycles never reach zero.

If cleanup ignores cycles, unique evidence may be lost.

## Analysis

This reinforces the distinction between **structural ref** and **blocking retention dependency**.

Only owner-declared dependency classes block retirement.

For a genuine blocking cycle:

- either the owner family provides a group compaction/summary transition preserving the required semantics;
- or the cycle remains retained.

Generic graph liveness is neither necessary nor sufficient.

## Required tightening T6

Cleanup contracts define retention-blocking semantics independently of raw reference topology.

Bulk/group retirement is permitted only when an owner-domain contract proves the entire strongly related set can be replaced coherently.

Do not add generic cycle collector/refcount machinery.

**Disposition: supports recommended model.**

---

# 8. Challenge C7 — settled execution cannot necessarily lose idempotency evidence

## Attack

A player/host may retry a previously accepted input after root command settles. Step 3 says committed retry returns same identities/results rather than executing twice.

If 5.13 deletes the command/receipt fingerprint too early, a delayed duplicate could be treated as fresh intent and replay mechanics.

## Analysis

We need to separate:

```text
active execution recovery lifetime
accepted duplicate-suppression lifetime
historical audit lifetime
full detailed trace lifetime
```

The first clearly ends at settlement. The latter lifetimes are not yet universally quantified.

However Step 3 does not require every full command payload forever. It requires stable idempotency semantics for the accepted invocation identity.

A compact immutable idempotency/result anchor can be sufficient:

```text
accepted interaction/invocation identity
fingerprint
settled disposition
root command/result/receipt identities
minimum response/export result needed for exact retry contract
```

Exact fields depend on the Step-3 implementation plan.

## Required tightening T7

5.13 must not define a global expiry period for accepted idempotency.

For each externally retryable identity domain, the owner contract must specify what compact evidence remains while exact duplicate recognition is promised.

Detailed execution/trace data may retire earlier than this compact anchor.

Whole anchor deletion is admitted only after the identity domain no longer promises or can receive that retry **or** another survivor owns equivalent duplicate-suppression semantics.

If Step 6 host identity cannot bound late retries, conservative retention of compact anchors may be long-lived and is acceptable because they are small.

**Disposition: no owner decision; compact-anchor requirement carried to candidate/debt.**

---

# 9. Challenge C8 — verified Story Transcript may lose its exact-verification basis

## Attack

Step 5.11 permits Story Transcript to become the sole surviving exact text copy after message payload compaction, verified against source identity/digest.

If Step 5.13 later removes the compact source envelope containing digest/provenance, Story text remains but can no longer prove `verified_exact`.

## Analysis

Whole message envelope retention is not necessary if exact-verification evidence can be migrated.

Natural survivor may be a compact Transcript-local verification anchor containing only the minimum necessary:

```text
source stable identity
accepted representation/slice identity
expected digest
archived content digest / certification basis
```

This anchor is not gameplay truth authority; it only proves equality of archived wording to accepted source representation.

If no verified-exact promise is needed, Story may retain editorial text with `verified_exact=false` and no source-verification anchor.

## Required tightening T8

Before deleting a message envelope used by a surviving `verified_exact` Transcript record:

- migrate the minimum deterministic exact-certification basis into an admitted durable survivor;
- or revoke verified-exact status before deletion.

Do not keep the entire message envelope solely for one digest if a smaller explicit verification survivor suffices.

**Disposition: recommendation survives.**

---

# 10. Challenge C9 — `runtime.disclosure` itself should not become routine GC target

## Attack

Could old disclosure rows be deleted because “the player obviously knows this by now” or the fact is no longer secret?

This would reclaim small metadata and reduce history.

## Analysis

`runtime.disclosure` is sparse current meta-level exposure authority, and human exposure is monotonic for the exact delivered information.

Deleting it can cause future context assembler/Narrator to forget that a player was told something and repeat/reveal incorrectly.

Storage cost is small relative to evidence value.

No current owner contract defines “disclosure no longer matters” generically.

## Required tightening T9

Baseline Step 5.13 does **not** automatically garbage-collect valid sparse `runtime.disclosure` rows merely by age, fact visibility change or campaign progression.

A row may be migrated/merged only under an explicit Step-4 disclosure owner contract preserving equivalent current exposure semantics.

This is a simplification, not a new product choice.

**Disposition: keep disclosure out of ordinary deletion candidate classes.**

---

# 11. Challenge C10 — selected checkpoint retention could be unnecessary over-retention

## Attack

Step 5.7 says recovery may read zero checkpoints. Why keep the selected checkpoint merely because `MANIFEST.last_checkpoint_id` points to it?

Could maintenance simply delete every checkpoint as soon as gameplay RRC proves READY?

## Analysis

`last_checkpoint_id` is a deliberate checkpoint-facility pointer. Deleting the selected descriptor while retaining the pointer creates a known dangling facility state.

If the descriptor no longer has value, the correct transition is:

```text
clear/replace last_checkpoint_id
+ remove descriptor
```

in one coherent campaign transaction where applicable.

Whether the product wants “always keep one checkpoint” is not required by current canon. The pointer itself can become null if the checkpoint facility chooses to retire it and no explicit operation depends on it.

## Required tightening T10

Do not impose a permanent selected-checkpoint retention promise.

Instead:

- while pointer selects descriptor, descriptor is protected by pointer contract;
- cleanup may atomically clear/replace pointer and remove descriptor when no other protected consumer exists;
- no checkpoint count/age floor is canonical;
- explicit support operation pinning a checkpoint during one bounded invocation prevents concurrent removal only through normal read/currentness discipline, not a durable reader lease.

**Disposition: mechanical clarification.**

---

# 12. Challenge C11 — stale host caching a deleted absorbed live ref

## Attack

Campaign has absorbed E and 5.13 deletes live ref E. A stale ChatGPT session still caches E and attempts a live write.

If it never checks campaign routing first, could it recreate/use stale authority?

## Analysis

Step 5.8 already solves semantic fencing:

- E was CLOSED before route-away;
- stale ordinary write against closed final source cannot be valid;
- current campaign route no longer selects E;
- branch existence is not authority.

After ref deletion, stale host's cached source is even less useful. It cannot lawfully recreate E as authority merely from known branch name.

However if physical implementation allows branch recreation under the same deterministic name, stale/new opening logic must not interpret recreated branch existence as successor authority.

Campaign route selection remains required.

## Required tightening T11

- Ref deletion is post-authority cleanup only.
- Missing ref after confirmed route-away/absorption is healthy.
- Stale host must route through current campaign after close/missing source; it may not recreate/adopt old E from branch name.
- New branch with reused technical name is not old authority unless selected through a fresh valid route contract; preferably epoch identities/names are never reused.

**Disposition: no new fencing subsystem needed.**

---

# 13. Challenge C12 — orphan live branch “never selected” proof may accidentally require history scan

## Attack

A prepared branch exists. How do we prove no historical campaign commit ever selected it without scanning campaign history?

If current routing does not select it, perhaps it was selected and later absorbed; deleting it might still be safe, but classification differs.

## Analysis

For safety, classification does not need a metaphysical proof that it was never selected if current cleanup predicate can instead prove one of:

```text
A. current campaign authoritative routing has no dependency on ref
   AND an explicit prepared-opening identity/record shows route selection never completed

B. campaign current route/absorption evidence proves exact final head absorbed

C. provenance is unknown -> do not auto-delete; diagnose/retain
```

A broad history search is unnecessary for ordinary maintenance.

Prepared branches should carry/derive bounded opening identity/source context sufficient to match current route/opening result while that preparation attempt is still known. After process loss, an unclassified leftover can remain harmless until a bounded repair/admin process establishes its disposition.

## Required tightening T12

No branch is automatically classified orphan solely from its name and absence from current route.

Unknown leftover branch classification is `UNCLASSIFIED_NONCURRENT_REF`/equivalent maintenance state and is retained unless current bounded evidence proves absorbed/non-authoritative preparation.

No campaign-history scan fallback is required for correctness.

**Disposition: boundedness preserved.**

---

# 14. Challenge C13 — deleting current paths does not meaningfully reduce repository object size

## Attack

If old blobs remain in history, Step 5.13 may fail its storage-boundedness purpose. Why do any path cleanup?

## Analysis

Current-namespace cleanup still has material value:

- bounded current tree size;
- fewer current records/index entries to discover/migrate/validate;
- less accidental context retrieval;
- fewer stale recovery routes;
- fewer live refs;
- simpler current campaign export/maintenance surface;
- future compaction may prevent *additional* duplicated bulky payloads;
- non-Git future storage backends can reclaim bytes using the same semantic eligibility model.

But we must be honest:

> With append-only Git, deleting a previously committed file is not a storage-size erasure primitive for historical objects.

If measured Git repository growth becomes a product problem, it requires a separate storage/history migration decision, not silent Step-5.13 force rewrite.

## Required tightening T13

Rename/describe ordinary cleanup goals as **current namespace and obsolete authority/evidence retirement**, not guaranteed Git object-store reclamation.

Track repository-growth measurement as implementation/Step-6 operational debt.

**Disposition: Step 5.13 remains useful and honest.**

---

# 15. Challenge C14 — cleanup transaction replay/idempotency could require a job ledger

## Attack

Maintenance selects 500 candidates and crashes after publishing 200. How does it know where to resume without durable cleanup job state?

## Analysis

Cleanup is derived maintenance, not mandatory semantic work.

After restart:

- current tree already lacks the 200 retired items;
- candidate discovery rebuilds from current state;
- remaining 300 candidates reappear;
- deleted candidates do not require replay;
- no fictional/mechanical consequence is executed by cleanup.

A maintenance batch identifier may help diagnostics but is not needed for correctness.

Ref cleanup similarly:

- branch already absent => success/no-op if current routing does not require it;
- branch still present => revalidate eligibility and retry when capability exists.

## Required tightening T14

No durable generic GC job/queue is baseline.

Maintenance progress is **state-derived** from the current authoritative namespace and owner lifecycles.

Per-batch diagnostic/audit metadata is optional and non-authoritative.

**Disposition: supports simplicity.**

---

# 16. Challenge C15 — owner-local-only (Alternative C) may be sufficient after all

## Attack

Why add a hybrid layer at all? Let each owner implement `can_delete(record)` and run maintenance over known directories.

## Analysis

For small campaigns, this can work.

It fails scaling/closed-proof needs where:

- an artifact may have consumers across many owner partitions;
- target-side directory scan cannot prove absence cheaply;
- maintenance would need whole LOG/WORLD/runtime traversal;
- live/cross-source protection must be discoverable without all-live scans.

The correct hybrid does not imply a new global component. It means:

```text
owner-local semantic eligibility
+
only those typed reverse/protection/candidate routes that concrete owners need
```

This can be implemented as reusable library mechanics without semantic unification.

## Required tightening T15

Canonical language should say **owner-gated cleanup composition**, not “GC service.”

Derivative indexes are optional per owner-family capability, not mandatory architecture-wide registry.

**Disposition: E remains recommended over C-only, narrowly.**

---

# 17. Challenge C16 — broad world-record retirement scope creep

## Attack

Once 5.13 has a cleanup framework, it is tempting to physically delete dead NPCs, consumed items, completed missions, old lore and all terminal world records.

## Analysis

That would be a new product/history/lore retention policy, not merely persistence garbage collection.

Step 5.13 task scope is obsolete runtime/evidence/projection/live/transport artifacts and explicitly inherited compaction contracts.

World owner lifecycle may allow semantic retirement, but physical deletion of canonical world entities with historical/lore significance needs owner-specific semantics not yet established here.

## Required tightening T16

5.13 does not create a general “delete terminal world entities” policy.

Only owner kinds whose canonical contracts explicitly admit physical retirement/compaction enter automatic cleanup.

Unknown world-record retirement remains out of scope/deferred.

**Disposition: prevents scope creep.**

---

# 18. Failure-mode review after tightenings

## F1 — cleanup selects candidate, new campaign dependency appears

Campaign CAS/dependency footprint invalidates proof; revalidate.

**PASS with T2/T3.**

## F2 — new live dependency appears without campaign movement

Only safe under self-contained consumer, cross-source protection registration, or source synchronization.

**PASS with T3.**

## F3 — stale reverse index omits blocker

Absence cannot authorize deletion unless index has correctness-complete protection-routing contract and currentness proof.

**PASS with T2.**

## F4 — replacement summary commit ambiguous

Do not delete source until current authoritative state proves replacement sufficient.

**PASS.**

## F5 — one campaign transaction contains replacement + deletion and ACK lost

Step 5.6 current-tree/lineage verification resolves actual current result; no split current tree exists.

**PASS.**

## F6 — selected checkpoint removed but pointer remains

Forbidden; clear/replace pointer coherently.

**PASS with T10.**

## F7 — consumed Continuation still needed by parent/current result

Cleanup contract sees active/current reference or compact survivor requirement.

**PASS if implementation contracts are complete.**

## F8 — exact message compacted, old Git history still has text

Ordinary runtime cannot mine history to restore exact semantic retention.

**PASS with T4.**

## F9 — verified Transcript loses source digest envelope

Migrate compact certification anchor or revoke exactness before deletion.

**PASS with T8.**

## F10 — absorbed live branch ref deletion unavailable

Leave harmless nonauthority ref; maintenance reports deferred capability.

**PASS.**

## F11 — stale host uses deleted live ref

Current routing/closed-source law prevents authority; missing old ref after route-away is healthy.

**PASS with T11.**

## F12 — prepared losing Git object remains on server

No semantic authority; host GC owns physical reclamation.

**PASS.**

## F13 — cleanup batch interrupted

Rediscover remaining candidates from current state; no durable job required.

**PASS with T14.**

## F14 — cycle of retired provenance refs

Only blocking dependencies matter; group compaction or retain.

**PASS with T6.**

---

# 19. Revised recommendation

The research recommendation survives, with a sharper name and stronger laws:

> **OWNER-GATED RETIREMENT / CLOSED BLOCKER CONTRACTS / COMPLETENESS-TYPED PROTECTION ROUTING / CURRENT-BASIS SAFE-RETIREMENT PROOF / REPLACEMENT-BEFORE-REMOVAL / OPTIONAL POST-AUTHORITY REF CLEANUP / HOST-MANAGED GIT OBJECT RECLAMATION**

The candidate should emphasize that Step 5.13 is **not one GC subsystem**.

It is a deterministic maintenance protocol shared across owner-specific cleanup contracts.

Core invariant:

```text
automatic current-namespace removal is allowed only when:

owner terminality/replacement is proven
AND
all admitted blocker classes are proven discharged on a current coherent basis
AND
all survivor/reference semantics remain valid
AND
all blocker-creating native sources are covered by the proof/fence
AND
resulting current state validates
```

Uncertainty -> retain.

---

# 20. What is deliberately not solved by 5.13

The challenge confirms these should remain outside the baseline:

- universal mark/sweep graph;
- generic durable reference count;
- universal tombstone table;
- global GC frontier;
- cleanup worker/queue/lease;
- history rewrite to reclaim old campaign bytes;
- secure data-erasure promise for already-published Git history;
- automatic deletion of sparse disclosure rows;
- automatic deletion of arbitrary terminal world entities;
- arbitrary history TTL;
- campaign-wide transitive relation reduction;
- mandatory branch deletion when RepositoryPort lacks the capability.

---

# 21. Owner decision gate

No new owner decision is required.

The challenge did not reveal a need to:

- weaken recovery;
- weaken Selective Exact semantics;
- change gameplay/lore retention promise;
- accept history rewrite/force push;
- create a new canonical authority;
- impose cleanup latency on ordinary gameplay.

All required tightenings are mechanical consequences of already accepted architecture.

Next step: write the candidate specification incorporating T1–T16 and then perform a separate adversarial review against that candidate.

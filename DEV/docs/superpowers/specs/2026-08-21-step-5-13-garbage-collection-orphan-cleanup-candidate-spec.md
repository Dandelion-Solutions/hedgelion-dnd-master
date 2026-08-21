# Step 5.13 — Garbage Collection / Orphan Cleanup — Candidate Specification

Status: **CANDIDATE — REQUIRES ADVERSARIAL REVIEW**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Basis:

- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-task-brief.md`
- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-research-draft.md`
- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-analytical-challenge.md`
- canonical Steps 3 and 5.1–5.12

Candidate architecture direction:

> **OWNER-GATED RETIREMENT / CLOSED BLOCKER CONTRACTS / COMPLETENESS-TYPED PROTECTION ROUTING / CURRENT-BASIS SAFE-RETIREMENT PROOF / REPLACEMENT-BEFORE-REMOVAL / OPTIONAL POST-AUTHORITY REF CLEANUP / HOST-MANAGED GIT OBJECT RECLAMATION**

This candidate defines cleanup/retirement architecture. It does not implement GAME/schema/tooling changes, rewrite Git history, define arbitrary world-entity deletion policy, or begin Step 5.14.

---

# 1. Core intent

Step 5.13 is not a generic garbage-collector authority.

It is a deterministic maintenance composition over **owner-specific cleanup contracts**.

The core safety invariant is:

```text
HDM may remove representation A from the current authoritative namespace
only after:

1. A's native semantic/current/pending responsibility has ended
   or moved to a sufficient replacement;

2. every admitted consumer class that can require A's representation
   is proven absent, discharged, or independently satisfied;

3. every surviving reference has lawful post-removal semantics;

4. every native source capable of creating a new material blocker
   is covered by the current proof/fence;

5. the resulting current state passes bounded owner/integrity validation.
```

If any of those facts is unknown:

```text
RETAIN
```

False-negative cleanup merely preserves extra data. False-positive cleanup may destroy correctness evidence and is forbidden.

---

# 2. Five distinct lifecycle/cleanup layers

Step 5.13 distinguishes:

```text
SEMANTIC TERMINALITY
    owner no longer active/current/pending for this responsibility

REPRESENTATION COMPACTION
    bulky/detail representation replaced by sufficient compact evidence

CURRENT-NAMESPACE RETIREMENT
    record/path/index no longer present in current authoritative tree/routing

REF RETIREMENT
    non-authoritative Git/native ref removed when transport supports it

HOST-MANAGED OBJECT RECLAMATION
    unreachable Git object bytes later reclaimed by host maintenance
```

## LAW 5.13-1 — TERMINALITY IS NOT DELETION

Native lifecycle terminality does not automatically authorize representation removal.

A terminal owner may still have required:

- idempotency evidence;
- causal provenance;
- historical semantic content;
- chronology evidence;
- exact-text verification evidence;
- recovery/audit dependencies.

## LAW 5.13-2 — COMPACTION IS NOT CURRENT-NAMESPACE RETIREMENT

A compact survivor may remain current/dereferenceable after detailed payload disappears.

## LAW 5.13-3 — CURRENT-NAMESPACE RETIREMENT IS NOT GIT-HISTORY ERASURE

Removing a path in a later campaign commit does not mean older committed bytes cease to exist in reachable Git history.

## LAW 5.13-4 — REF RETIREMENT DOES NOT DECIDE AUTHORITY

A live/prepared ref may be removed only after native routing/lifecycle already proves it non-authoritative.

Deleting a ref is never the transition that makes gameplay state noncanonical.

## LAW 5.13-5 — HDM DOES NOT OWN SERVER OBJECT GC

Ordinary HDM runtime SHALL NOT claim that an unreferenced commit/tree/blob has been physically reclaimed unless a supported host capability explicitly proves that operation.

Unreachable-object reclamation remains Git-host maintenance in the baseline.

---

# 3. No universal GC authority

## LAW 5.13-6 — CLEANUP NEVER OWNS SEMANTIC LIVENESS

Current/pending/terminal meaning stays with the native owner contract.

Cleanup metadata cannot:

- terminate a Procedure/Resolution/Command;
- unarm a temporal obligation;
- retire chronology relation meaning;
- decide Story projection completion;
- release exact-text protection;
- clear human disclosure;
- move live authority.

## LAW 5.13-7 — NO GLOBAL MARK/SWEEP ROOT GRAPH BASELINE

The architecture does not require one campaign-wide graph whose reachability defines semantic liveness.

Structural graph reachability is insufficient for semantic dependencies such as:

- exact-text requirements;
- chronology feasible-set precision;
- accepted idempotency;
- Story coverage compatibility;
- native pending obligations.

## LAW 5.13-8 — NO GENERIC DURABLE REFERENCE COUNT

A generic count SHALL NOT authorize irreversible deletion.

Raw reference counts cannot safely represent cycles, semantic non-reference dependencies, source-domain ownership or stale/missing enrollment.

## LAW 5.13-9 — NO GLOBAL GC FRONTIER

Step 5.13 introduces no scalar “safe before X” campaign frontier, timestamp, event ID, Git SHA or chronology cursor applicable to unrelated owner domains.

Native generation/epoch bulk retirement is permitted only where that domain's contract itself proves it.

---

# 4. Cleanup contracts

Automatic cleanup is admitted only for target kinds with a closed cleanup contract compatible with the target representation generation/version.

Conceptually:

```text
CleanupContract(target_kind, generation) {
    native_terminality_or_replacement_predicate
    blocker_dependency_classes[]
    blocker_query/protection_route per class
    survivor_obligations[]
    reference_survival_rules[]
    blocker_creation_source_classes[]
    currentness/fencing_requirements
    migration/legacy compatibility
}
```

This is a semantic/machine contract concept. It need not be a standalone durable record.

## LAW 5.13-10 — CLEANUP CONTRACT NAMES OWNERS; IT DOES NOT REPLACE THEM

For each blocker class, the actual dependency remains owned by the consuming native owner.

A cleanup contract merely identifies the complete admitted dependency vocabulary and bounded evidence path required to prove safe absence/discharge.

## LAW 5.13-11 — UNKNOWN TARGET CONTRACT MEANS NO AUTOMATIC DELETION

An unregistered/unknown target kind, incompatible cleanup generation, or legacy object lacking required cleanup semantics remains retained until migrated or explicitly repaired.

Absence of known blockers is insufficient when the blocker vocabulary itself is not closed.

## LAW 5.13-12 — NEW CONSUMERS MUST ENROLL BEFORE DEPENDENCE BECOMES PROTECTED

A future owner type that requires a cleanup-target representation must participate in that target's admitted typed dependency/protection contract before a durable accepted dependency may rely on it.

Failure to do so is an integrity/implementation defect, not permission for GC to guess.

---

# 5. Safe-retirement proof

Deterministic core may construct an ephemeral proof/result conceptually equivalent to:

```text
SafeRetirementAssessment
    target_ref
    cleanup_contract_generation
    pinned_native_bases[]
    terminality_or_replacement_evidence
    blocker_class_results[]
    survivor_closure
    reference_survival_validation
    dependency/currentness_footprint
    disposition:
        SAFE_TO_RETIRE_CURRENT_REPRESENTATION
        RETAIN_BLOCKED
        RETRY_STALE
        INTEGRITY_REQUIRED
        CAPABILITY_DEFERRED
```

Exact names are implementation detail.

No persistent generic `SafeRetirementProof` is baseline authority.

## LAW 5.13-13 — SAFE RETIREMENT USES ONE COHERENT CURRENT BASIS

Every mutable participating source required by the target contract is exact-pinned/revalidated under its native currentness rules.

Do not mix blocker absence from one revision with terminality/replacement from another incompatible revision.

## LAW 5.13-14 — NEGATIVE PROOF REQUIRES CLOSED BLOCKER COMPLETENESS

“Search returned no reference” is not deletion evidence unless the applicable cleanup contract proves that the searched routes cover every admitted blocker class for the target representation.

## LAW 5.13-15 — RESULTING CURRENT STATE IS VALIDATED BEFORE REMOVAL PUBLICATION

The planned resulting namespace must preserve every required direct reference, survivor, current routing invariant and touched owner contract.

No required dangling `RESOLVABLE` reference may be introduced.

---

# 6. Candidate discovery

Cleanup candidate discovery is a performance/maintenance projection, not safety authority.

Possible candidate sources include:

- native terminal lifecycle partitions;
- consumed/superseded generations;
- unselected checkpoint partitions;
- compacted-message partitions;
- absorbed live-epoch metadata;
- obsolete Story index generations;
- explicitly retired chronology/index partitions.

## LAW 5.13-16 — CANDIDATE INDEX MAY FAIL ONLY TOWARD OVER-RETENTION

A derivative candidate index/list may be stale or incomplete.

Consequences:

```text
missed candidate -> harmless extra retention
stale positive candidate -> must revalidate before deletion
```

No candidate hint authorizes cleanup by itself.

## LAW 5.13-17 — NO CAMPAIGN-WIDE DISCOVERY SCAN IN ORDINARY PLAY

Ordinary gameplay never scans all historical runtime records, Story, LOG, chronology or live refs to discover garbage.

Broad/batched cleanup is a maintenance operation.

---

# 7. Protection routing and negative evidence

Some target kinds require reverse protection routing because forward-owner scans would be unbounded.

Two derivative categories are distinguished:

```text
BEST_EFFORT_DISCOVERY_INDEX
    omission allowed
    absence cannot authorize deletion

COMPLETENESS-TYPED PROTECTION_ROUTING
    completeness for one declared dependency class is a correctness invariant
    may participate in negative proof after currentness validation
```

## LAW 5.13-18 — PROTECTION ROUTING REMAINS DERIVATIVE

The consumer's forward/native dependency is semantic authority.

Protection routing answers bounded retrieval/membership only.

## LAW 5.13-19 — PROTECTION ROUTING COHERENCE IS REQUIRED BEFORE ABSENCE MAY AUTHORIZE LOSS

If absence in protection routing can permit irreversible retirement, enrollment/removal must join native owner durability closure strongly enough that healthy current durable state cannot expose:

```text
protected consumer exists
+ required protection membership absent
```

If route completeness/currentness cannot be proven, deletion blocks.

## LAW 5.13-20 — DO NOT MERGE TYPED PROTECTION DOMAINS INTO A UNIVERSAL REFERENCE GRAPH

Exact-text protection, chronology dependencies, recovery routing and future target-specific protections may share reusable implementation mechanics but remain semantically typed owner contracts.

---

# 8. Cross-source blocker creation

Campaign CAS alone cannot prove safe deletion when a new blocker can be established concurrently in another native writable source.

## LAW 5.13-21 — EVERY BLOCKER-CREATING SOURCE CLASS PARTICIPATES IN THE CLEANUP CONTRACT

For each blocker class, automatic cleanup must establish one of:

### SELF-CONTAINED CONSUMER

Accepted consumer stores/pins all representation/content required by its contract, so later target current-tree retirement cannot strand it.

### CROSS-SOURCE PROTECTION REGISTRATION

Accepted consumer durably enrolls target-domain protection evidence before/with becoming dependent, and cleanup validates that protection route.

### SOURCE SYNCHRONIZATION/FREEZE

Relevant native source is exact-pinned/fenced through its owner-defined synchronization boundary for the deletion attempt.

If no bounded safe pattern exists, automatic deletion of that target while such source is capable of creating blockers is not admitted.

## LAW 5.13-22 — NO ALL-LIVE SCAN TO PROVE CLEANUP SAFETY

Cleanup may use existing typed routing/claims/protection routes but SHALL NOT enumerate every live branch merely to see whether one might reference the target.

---

# 9. Replacement and survivor ordering

## LAW 5.13-23 — REQUIRED SURVIVOR EXISTS BEFORE SOURCE LOSS

If a compact replacement, promoted natural owner, migrated cursor, verification anchor or summary is required for correctness, it must be durably/currently established before old representation is allowed to disappear.

## LAW 5.13-24 — SAME-CAMPAIGN REPLACE+DELETE MAY SHARE ONE STEP-5.6 TRANSACTION

When replacement and source live in the same campaign authority domain and one resulting tree can prove complete survivor closure, one coherent campaign transaction may:

```text
create/update survivor
rewrite affected references/routing
remove source path
```

## LAW 5.13-25 — CROSS-DOMAIN REPLACEMENT PRECEDES DELETE

When survivor and target cannot share one atomic native publication boundary, establish/confirm survivor first, then delete target in a later independent transaction.

Failure biases toward temporary redundancy.

---

# 10. Reference survival semantics

Not every stable ID reference requires current dereferenceability.

The architecture requires the semantic distinction equivalent to:

```text
RESOLVABLE_REFERENCE
    target current representation must resolve

OPAQUE_PROVENANCE_ID
    stable non-reused identity is sufficient
    current target dereference is not promised

SURVIVOR_BACKED_REFERENCE
    original target may disappear because named compact survivor/anchor
    carries the required meaning/verification
```

Exact machine vocabulary may differ.

## LAW 5.13-26 — REQUIRED-RESOLVABLE REFERENCES BLOCK TARGET REMOVAL

Target cannot disappear while any surviving owner contract requires current dereferenceability.

## LAW 5.13-27 — OPAQUE PROVENANCE DOES NOT REQUIRE A UNIVERSAL TOMBSTONE

A stable never-reused ID may remain in causal/provenance history after target record removal when the owning reference contract explicitly needs identity only.

Missing target is not integrity corruption for that declared opaque reference.

## LAW 5.13-28 — UNKNOWN / LEGACY REFERENCE SEMANTICS ARE CONSERVATIVE

If an incoming reference cannot be classified safely, assume target resolution may be required and retain/migrate rather than delete.

## LAW 5.13-29 — NARROW IDENTITY ANCHORS ARE ALLOWED ONLY WHEN JUSTIFIED

A compact tombstone/identity anchor may be introduced for a specific target family only when a durable contract requires stable dereferenceable identity after full source retirement and no natural survivor can satisfy it.

No universal tombstone registry is baseline.

---

# 11. Runtime execution artifacts

## LAW 5.13-30 — NON-SETTLED EXECUTION OWNERS ARE NOT CLEANUP CANDIDATES

Non-settled RuntimeCommand, active/suspended Resolution, active Procedure dependencies, current Continuation, pending child/firing identities, fixed RNG and unresolved choice/reaction evidence remain protected by Steps 3/5.2/5.3.

## LAW 5.13-31 — SETTLEMENT ENABLES DETAIL COMPACTION, NOT BLIND ROOT DELETION

After command/execution terminality:

- prospective/working payload may become removable;
- detailed trace may become removable when no unique audit dependency remains;
- MechanicalEvent/receipt detail may compact after causal/export/chronology consumers retain sufficient evidence;
- compact idempotency/result evidence may survive longer.

## LAW 5.13-32 — DUPLICATE-SUPPRESSION EVIDENCE FOLLOWS ITS IDENTITY CONTRACT

If an external/host invocation identity can still be retried and Step-3 idempotency promises duplicate recognition, minimum accepted fingerprint/result identity survives.

No universal time-based expiry is introduced.

## LAW 5.13-33 — PURE DIAGNOSTIC TRACE IS EARLY-RETIREABLE WHEN NONUNIQUE

ResolutionTrace/diagnostic detail carrying no unique semantic/recovery/provenance obligation is a high-priority cleanup candidate after owner terminality.

This does not authorize deletion of compact MechanicalEvent/receipt evidence with independent meaning.

---

# 12. Checkpoint cleanup

Checkpoint remains optional facility evidence.

## LAW 5.13-34 — CURRENT CHECKPOINT POINTER PROTECTS ITS TARGET

While `MANIFEST.last_checkpoint_id` selects descriptor K, K is required by the checkpoint facility contract even if ordinary gameplay recovery does not need it.

## LAW 5.13-35 — SELECTED CHECKPOINT MAY RETIRE ONLY WITH COHERENT POINTER TRANSITION

Cleanup may:

```text
replace pointer -> K2 + retain/create K2
OR
clear pointer -> null
```

and remove K in one coherent campaign transaction when no other protected dependency requires K.

No rule requires at least one checkpoint forever.

## LAW 5.13-36 — UNSELECTED CHECKPOINTS ARE OWNER-GATED CANDIDATES

An unselected immutable checkpoint may be removed from current namespace when no explicit diagnostic/repair/audit consumer requires it.

Age alone is not eligibility.

---

# 13. Message-envelope cleanup

`EXACT_RETAINED -> COMPACTED` remains Step-5.11 compaction, not Step-5.13 physical retirement.

## LAW 5.13-37 — EXACT_RETAINED MESSAGE IS NOT A WHOLE-ENVELOPE GC CANDIDATE

If exact payload remains protected, Step 5.13 cannot remove the message representation holding it unless the exact dependency is first lawfully promoted/migrated under Step 5.11.

## LAW 5.13-38 — COMPACTED MESSAGE ENVELOPE MAY RETIRE ONLY AFTER ALL SURVIVOR OBLIGATIONS MOVE

Before whole envelope current-namespace removal, preserve/migrate as applicable:

- Interaction/idempotency linkage;
- source enumeration/cursor anchor;
- semantic/history provenance;
- disclosure provenance where materially used;
- exact archive certification basis;
- live absorption/source identity;
- correction/audit dependencies.

## LAW 5.13-39 — STORY CURSOR CONTINUITY OUTLIVES ENVELOPE WHEN NEEDED

If Story coverage still needs source-domain position semantics, a compact enumeration anchor or coherent migrated coverage token must survive before envelope removal.

## LAW 5.13-40 — VERIFIED-EXACT STORY REQUIRES SURVIVING CERTIFICATION BASIS

If `STORY/TRANSCRIPT` remains `verified_exact` after source envelope retirement, retain a minimum durable verification survivor sufficient to establish equality to the accepted source representation/slice.

Otherwise revoke exact-verification status before deletion.

---

# 14. Semantic retention versus Git transport history

Append-only Git history may retain old bytes after current representation is lawfully compacted/retired.

## LAW 5.13-41 — GIT HISTORY IS NOT A SECRET VERBATIM BACKDOOR

Ordinary runtime/Story/history retrieval SHALL NOT mine old Git commits to restore exact wording that Step 5.11 has lawfully classified as no longer retained.

Transport reachability does not re-establish semantic exact-text availability.

## LAW 5.13-42 — AUTHORIZED FORENSIC/INTEGRITY HISTORY READ IS A SEPARATE CONTRACT

A bounded repair/security/support process may inspect historical Git evidence when explicitly authorized and necessary.

Such discovery does not silently convert all lawfully compacted content back into normal Master verbatim memory.

## LAW 5.13-43 — SECURE EXPUNGEMENT IS NOT ORDINARY GC

Guaranteed erasure of bytes already present in reachable campaign Git history would require history rewrite/force migration/server support or another storage architecture.

That is outside ordinary Step 5.13 and requires a future explicit owner/security/storage decision.

---

# 15. Story cleanup

Story remains a noncanonical durable projection.

## LAW 5.13-44 — CURRENT STORY OUTPUT/INDEX CLOSURE REMAINS COHERENT

Deleting/correcting Story records or index generations must preserve current layer reference/index/availability/allocator/coverage consistency required by Step 5.10.

## LAW 5.13-45 — OBSOLETE DERIVED STORY GENERATIONS MAY BULK-RETIRE WHEN NATIVE MIGRATION PROVES IT

Old index/projection-contract generations may be removed after a compatible successor/current layer state is durable and no retained source/reprojection/repair dependency needs the old generation.

Generation order has only Story-domain meaning.

## LAW 5.13-46 — STORY EDITORIAL HISTORY IS NOT AUTOMATICALLY PERMANENT

Step 5.13 creates no promise to retain every superseded editorial/narrative version.

Any retained exact/archive or explicitly promised history policy still blocks removal under its own contract.

---

# 16. Chronology cleanup

## LAW 5.13-47 — STEP 5.9 OWNS CHRONOLOGY SEMANTIC ELIGIBILITY

Step 5.13 SHALL NOT independently decide that chronology evidence is redundant.

It consumes Step-5.9 owner/protected-consumer evidence that required relation/metric/causal meaning survives.

## LAW 5.13-48 — DERIVATIVE CHRONOLOGY INDEX RETIREMENT DOES NOT RETIRE SOURCE RELATIONS

Endpoint/reachability/frontier caches may rebuild/replace independently, subject to their bounded correctness-routing contracts.

## LAW 5.13-49 — NO CAMPAIGN-WIDE TRANSITIVE REDUCTION FOR GC

Cleanup never performs a full historical chronology graph reduction solely to save storage.

Owner/local bounded reductions are allowed where Step 5.9 proves losslessness for protected consumers.

---

# 17. Disclosure cleanup

## LAW 5.13-50 — VALID SPARSE DISCLOSURE IS NOT ORDINARY AGE-BASED GARBAGE

`runtime.disclosure` represents material human exposure that is monotonic for the exact disclosed information.

Do not delete it merely because:

- the fact is old;
- the secret later became public;
- the campaign advanced;
- storage pressure exists.

A disclosure owner-specific merge/migration may replace rows only when equivalent current exposure semantics survive.

---

# 18. Live ref cleanup

Live refs are classified by current authority evidence, not name/age.

```text
ACTIVE
CLOSED_UNABSORBED
NONAUTHORITATIVE_ABSORBED
NONAUTHORITATIVE_PREPARED_ORPHAN
UNCLASSIFIED_NONCURRENT_REF
```

Exact maintenance names are implementation detail.

## LAW 5.13-51 — ACTIVE LIVE REF DELETE IS FORBIDDEN

If current route selects ACTIVE E, source/ref is current authority and required.

## LAW 5.13-52 — CLOSED_UNABSORBED LIVE REF DELETE IS FORBIDDEN

Selected CLOSED E remains current truth/recovery source until absorption succeeds.

## LAW 5.13-53 — ABSORBED LIVE REF MAY RETIRE AFTER RETRIEVAL DEPENDENCIES DISCHARGE

Eligibility requires bounded current campaign evidence that the exact final E source was absorbed/route-away is current plus proof that no retained consumer still requires that live ref as a dereferenceable source.

## LAW 5.13-54 — PREPARED ORPHAN REF MAY RETIRE ONLY WITH BOUNDED NONAUTHORITY EVIDENCE

Branch existence + absence from current route is insufficient to prove “never selected.”

Use explicit bounded preparation/opening evidence when available.

If current disposition cannot be classified without broad history reconstruction:

```text
retain / report unclassified noncurrent ref
```

rather than guess.

## LAW 5.13-55 — MISSING OLD REF IS HEALTHY ONLY AFTER AUTHORITY ENDED

Missing selected ACTIVE/CLOSED_UNABSORBED source remains integrity blocking under Step 5.8.

Missing absorbed/orphan ref after confirmed cleanup is normal.

## LAW 5.13-56 — STALE HOST CANNOT RECREATE AUTHORITY FROM OLD REF NAME

Current campaign route/lifecycle selects authority. A stale host observing a missing old ref must resynchronize routing; it may not recreate/adopt the old epoch as authority from cached identity alone.

Epoch/source identities are not reused as current authority generations.

---

# 19. Ref-delete capability

## LAW 5.13-57 — REF CLEANUP IS CAPABILITY-GATED

A deployment may delete eligible non-authoritative refs only through a supported authenticated RepositoryPort capability with confirmed result.

## LAW 5.13-58 — MISSING REF-DELETE CAPABILITY IS NOT GAMEPLAY FAILURE

When eligible old ref cannot be deleted because current transport lacks the operation:

- current authority remains unaffected;
- ordinary gameplay continues;
- maintenance may report capability-deferred leftover;
- no native Git/CLI/private-HTTP bypass is authorized by cleanup semantics.

---

# 20. Prepared/unreachable Git objects

## LAW 5.13-59 — PREPARED LOSING OBJECTS NEED NO DURABLE GC REGISTRY

Blobs/trees/commits not selected by an authoritative ref are non-authoritative per Step 5.6.

Do not create a durable orphan-object table merely to remember them for future server GC.

## LAW 5.13-60 — HDM DOES NOT DELETE ARBITRARY GIT OBJECTS BASELINE

Current architecture relies on Git host reachability/GC behavior for unreferenced objects.

Support diagnostics may report known object SHAs when already available, but correctness does not depend on their reclamation.

---

# 21. Cleanup publication and crash consistency

Campaign namespace retirement follows Step 5.6.

## LAW 5.13-61 — DELETE DELTA IS A NORMAL SEMANTIC CAMPAIGN DELTA

A cleanup campaign transaction uses:

```text
frozen current basis
complete survivor/reference updates
explicit DELETE(path)
resulting-tree validation
single-parent commit
non-force ref transition
```

## LAW 5.13-62 — RELEVANT HEAD/SOURCE MOVEMENT INVALIDATES THE DELETE PROOF

If any terminality/blocker/survivor/currentness dependency moved, revalidate from current authority before attempting deletion.

Proven unrelated campaign movement may use ordinary Step-5.6 transport-only rebuild.

## LAW 5.13-63 — AMBIGUOUS CLEANUP PUBLICATION USES CURRENT AUTHORITY, NOT REPEATED DELETE GUESSING

On indeterminate final campaign publication:

- do not assume source remains or disappeared;
- resolve current campaign authority under Step 5.6;
- if current state already contains valid retirement result, adopt it;
- otherwise rederive from current state.

No gameplay semantics are replayed.

## LAW 5.13-64 — FAILURE BIASES TOWARD REDUNDANCY

Where replacement and deletion cannot be atomically proven, preserve old source until replacement is definitely sufficient.

---

# 22. Cleanup maintenance execution

## LAW 5.13-65 — CLEANUP REQUIRES NO BACKGROUND WORKER

Cleanup may run:

- at explicit maintenance invocation;
- opportunistically at suitable noncritical maintenance boundaries;
- in bounded batches;
- over multiple sessions.

It is not required for ordinary gameplay correctness.

## LAW 5.13-66 — NO DURABLE GENERIC CLEANUP JOB QUEUE

After interruption/restart, remaining work is rediscovered from current owner/candidate state.

Already retired paths do not need replay.

Optional diagnostics/batch audit may exist but is not liveness authority.

## LAW 5.13-67 — EMPTY CLEANUP PRODUCES NO HEARTBEAT WRITE

If no eligible current-tree mutation exists, maintenance creates no campaign commit merely to record that cleanup checked.

## LAW 5.13-68 — AGE/STORAGE PRESSURE PRIORITIZES; IT DOES NOT AUTHORIZE

Maintenance policy may choose older/larger already-safe candidates first.

No TTL, session count or size threshold makes a protected artifact semantically deletable.

---

# 23. Cycles and group retirement

## LAW 5.13-69 — RAW REFERENCE CYCLES DO NOT DEFINE LIVENESS

Only declared blocker dependencies participate in retirement safety.

## LAW 5.13-70 — TRUE BLOCKING CYCLES REQUIRE OWNER-GROUP REPLACEMENT OR RETENTION

If several artifacts genuinely depend on one another's representation for a promised contract, remove them together only through an owner-domain group compaction/replacement that preserves all required survivor semantics.

Otherwise retain.

No generic cycle collector is introduced.

---

# 24. World-record scope boundary

## LAW 5.13-71 — STEP 5.13 DOES NOT CREATE GENERIC WORLD-ENTITY DELETION SEMANTICS

A dead NPC, consumed item, completed mission, superseded lore fact or other terminal world record is not automatically garbage.

Automatic physical retirement applies only where that native owner contract explicitly admits it and the target has a closed cleanup contract.

Broader lore/world-history retention policy is outside this slice unless inherited by an already canonical owner contract.

---

# 25. Integrity and repair outcomes

Cleanup-specific suspect examples include:

```text
protection routing claims complete but forward protected owner lacks membership
required survivor missing after target already absent
opaque provenance ref interpreted as resolvable by incompatible schema
selected checkpoint pointer targets missing descriptor
current campaign route selects missing live source
verified-exact Story archive lacks surviving certification basis
cleanup contract generation incompatible with target/consumer generation
```

## LAW 5.13-72 — UNSAFE UNKNOWN IS RETENTION, NOT CORRUPTION BY ITSELF

A target that cannot prove safe deletion simply remains retained.

Only persisted contradictions/missing required current representations create integrity suspicion.

---

# 26. Legacy migration

## LAW 5.13-73 — LEGACY CLEANUP IS CONSERVATIVE

Legacy records lacking closed blocker/provenance/reference semantics are not automatically deleted.

Migration may:

- classify reference semantics;
- build required survivor anchors;
- establish typed protection routing;
- compact/promote content;
- enroll compatible cleanup generation.

Until then, over-retention is valid.

## LAW 5.13-74 — NEVER RECONSTRUCT LOST CONTENT TO ENABLE CLEANUP

Do not invent missing exact text, chronology relation, execution evidence or provenance merely to satisfy a desired compaction path.

If necessary evidence was already lost, integrity/repair handles the defect; GC does not fabricate replacements.

---

# 27. Performance contract

Ordinary gameplay cost attributable to Step 5.13:

```text
zero campaign-wide GC scans
zero background-worker requirement
zero per-turn cleanup commits
zero arbitrary Git-history scans
```

Maintenance cost should be bounded by:

```text
selected candidate batch
+ target cleanup contract blocker/survivor routes
+ currentness validation for affected native source(s)
```

Not by campaign age in the ordinary candidate proof path.

Large historical stores may require batched discovery/index maintenance outside gameplay.

---

# 28. Git repository growth statement

## LAW 5.13-75 — CURRENT-NAMESPACE CLEANUP DOES NOT CLAIM HISTORICAL OBJECT-STORE SHRINKAGE

Append-only campaign history may continue to retain historical blobs/commits.

Step 5.13 improves:

- current tree size/clarity;
- bounded current discovery;
- index/routing clutter;
- future payload duplication;
- live ref hygiene;
- portability to future storage backends that can actually reclaim retired representations.

Measured repository growth approaching host limits is a future storage/deployment concern and does not justify silent force/history rewrite.

---

# 29. Required machine-realization debt

Implementation planning after architecture sequence closure must cover at least:

1. cleanup-contract machine representation/registry for admitted target families;
2. cleanup-contract generation/compatibility validation;
3. reference survival semantics (`resolvable`, opaque provenance, survivor-backed or equivalent);
4. completeness-typed protection routing where concrete families require it;
5. cleanup candidate discovery partitions/indexes where measured value exists;
6. exact current-basis SafeRetirementAssessment implementation;
7. cross-source blocker creation/fencing integration;
8. replacement-before-removal transaction planning;
9. settled execution detail vs compact idempotency/result anchors;
10. trace/receipt/MechanicalEvent retention contracts;
11. checkpoint pointer + descriptor cleanup;
12. COMPACTED message-envelope survivor migration;
13. Story source-enumeration anchor migration;
14. verified-exact Transcript certification survivor;
15. chronology physical cleanup consuming Step-5.9 eligibility;
16. Story obsolete-generation/index cleanup;
17. disclosure retention/merge clarification;
18. live absorbed/orphan/unclassified ref classification;
19. optional RepositoryPort `DeleteRef` capability and capability-deferred behavior;
20. explicit prohibition on ordinary Git-history mining for lawfully compacted exact text;
21. maintenance batch/idempotency/dry-run diagnostics;
22. legacy conservative migration;
23. cleanup integrity cases;
24. repository growth/current-tree metrics;
25. player/runtime documentation distinguishing semantic deletion from Git-history erasure where relevant.

No broad GAME/schema implementation is performed in Step 5.13 design.

---

# 30. Required regression/adversarial cases

At minimum implementation tests later must cover:

1. active command cannot delete;
2. settled command trace compacts while idempotency anchor survives;
3. fixed RNG/receipt consumer blocks removal;
4. consumed Continuation current-parent dependency blocks early delete;
5. stale best-effort candidate index cannot authorize delete;
6. missing protection membership with live forward dependency is integrity defect;
7. protection routing currentness movement causes retry;
8. campaign dependency appears after proof -> CAS/dependency invalidation;
9. live-source dependency appears without campaign movement -> protected/frozen case;
10. unknown cross-source blocker source -> retain;
11. selected checkpoint cannot dangle;
12. pointer clear + checkpoint delete coherent;
13. unselected checkpoint safe delete;
14. EXACT_RETAINED message not whole-envelope deleted;
15. COMPACTED message blocked by Story cursor anchor;
16. migrated Story anchor permits envelope delete;
17. verified-exact Story loses source envelope only after certification migration;
18. revoked verified-exact permits smaller cleanup;
19. old Git history contains compacted text but ordinary exact query returns SEMANTIC_ONLY;
20. forensic repair may explicitly inspect history without changing default retention status;
21. opaque provenance ID survives deleted target without integrity error;
22. resolvable ref blocks delete;
23. unknown legacy ref blocks delete;
24. blocking cycle requires group replacement/retain;
25. chronology relation old but armed consumer blocks delete;
26. lossless chronology reduction allows delete;
27. Story old index generation retires after current successor;
28. valid disclosure row not age-GCed;
29. ACTIVE live ref cannot delete;
30. CLOSED_UNABSORBED ref cannot delete;
31. absorbed live ref eligible after no retrieval dependency;
32. orphan with bounded preparation proof eligible;
33. unclassified noncurrent ref retained;
34. missing absorbed old ref is healthy;
35. missing selected live ref is integrity suspect;
36. stale host cannot recreate old authority;
37. DeleteRef capability missing -> deferred cleanup, gameplay unaffected;
38. prepared losing commit produces no durable orphan registry;
39. ambiguous campaign cleanup publication resolves current state;
40. crash mid-batch resumes by rediscovery without job ledger;
41. repeated cleanup is idempotent/no-op;
42. empty cleanup produces no commit;
43. age threshold cannot delete protected target;
44. unknown cleanup-contract generation retains;
45. no campaign-wide scan on ordinary gameplay path.

---

# 31. Candidate verdict

The owner-gated hybrid is the candidate architecture for Step 5.13.

The strongest rejected baseline alternatives remain:

- universal mark/sweep graph;
- generic durable refcounts;
- retain-everything forever;
- owner-local-only cleanup with no typed reverse protection support for cases requiring bounded negative proof.

No unresolved human/product decision is identified at candidate stage.

The candidate now requires independent adversarial review before resolution/canonicalization.

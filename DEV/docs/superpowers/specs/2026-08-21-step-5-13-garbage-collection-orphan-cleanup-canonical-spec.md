# Step 5.13 — Garbage Collection / Orphan Cleanup — Canonical Specification

Status: **CANONICAL — STEP 5.13 ARCHITECTURE CLOSED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Canonicalization basis:

- `../design/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-task-brief.md`
- `../design/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-research-draft.md`
- `../design/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-analytical-challenge.md`
- `../design/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-candidate-spec.md`
- `../design/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-adversarial-review.md`
- `../design/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-resolution-gate.md`

Canonical architecture direction:

> **OWNER-GATED RETIREMENT / CLOSED BLOCKER CONTRACTS / COMPLETENESS-TYPED PROTECTION ROUTING / PINNED CURRENT-BASIS SAFE-RETIREMENT PROOF / SURVIVOR-BEFORE-REMOVAL / OPTIONAL POST-AUTHORITY REF CLEANUP / SEMANTIC RETENTION SEPARATE FROM GIT-HISTORY REACHABILITY / HOST-MANAGED GIT OBJECT RECLAMATION**

No new owner-level product decision was required. Step 5.13 mechanically derives safe cleanup from already accepted Steps 3–5.12.

This specification defines semantic retirement/current-namespace/ref-cleanup architecture. It does not implement GAME/schema/tooling changes, rewrite Git history, define secure erasure, create generic world-entity deletion policy, or begin Step 5.14.

---

# 1. Purpose

Step 5.13 answers:

> **When may HDM stop carrying an obsolete representation in the current campaign/runtime namespace without stranding any still-promised semantic, recovery, chronology, Story, exact-text, disclosure, idempotency or live-authority dependency?**

The design deliberately rejects the premise that “garbage” is determined by generic reachability or age.

Cleanup is safe only after the target's **native owner semantics** and all admitted blocking consumer contracts prove that the representation is no longer needed.

Canonical failure bias:

```text
uncertain cleanup eligibility
    -> RETAIN
```

Extra retention is acceptable. Irreversible false-positive deletion is not.

---

# 2. Five different concepts that must not be collapsed

```text
SEMANTIC TERMINALITY
    owner responsibility is no longer active/current/pending

REPRESENTATION COMPACTION
    detail/bulk is replaced by sufficient compact evidence

CURRENT-NAMESPACE RETIREMENT
    current authoritative tree/routing no longer carries representation

REF RETIREMENT
    non-authoritative branch/native ref is removed

HOST-MANAGED OBJECT RECLAMATION
    unreachable Git commit/tree/blob bytes are physically reclaimed by host GC
```

## LAW 5.13-1 — TERMINALITY DOES NOT IMPLY DELETION

A terminal owner/evidence item may still be required for:

- idempotent retry;
- accepted invocation provenance;
- causal history;
- chronology predicates;
- Story source continuity;
- exact-text/archive certification;
- repair/audit obligations.

## LAW 5.13-2 — COMPACTION DOES NOT IMPLY RECORD RETIREMENT

A compact survivor may remain a current durable target long after detailed payload disappears.

## LAW 5.13-3 — CURRENT-TREE RETIREMENT DOES NOT ERASE GIT HISTORY

A later campaign commit deleting a path does not make earlier ancestor blobs disappear from reachable Git history.

## LAW 5.13-4 — REF DELETION IS POST-AUTHORITY CLEANUP

Deleting a live/prepared ref never establishes non-authority. Native routing/lifecycle must already have ended/moved authority before ref cleanup is admitted.

## LAW 5.13-5 — SERVER OBJECT RECLAMATION IS NOT HDM SEMANTIC STATE

HDM does not own or persist a promise that an unreachable Git object has been physically reclaimed unless a supported host contract explicitly provides and confirms such an operation.

---

# 3. Cleanup is not a new authority

## LAW 5.13-6 — NATIVE OWNERS DEFINE LIVENESS

Cleanup SHALL NOT independently:

- settle RuntimeCommand/Resolution;
- consume Continuation;
- close Procedure;
- unarm temporal owner;
- retire fictional chronology relation meaning;
- complete Story coverage;
- release exact-text protection;
- clear human disclosure;
- move live authority.

Those transitions belong to their existing owners.

## LAW 5.13-7 — NO UNIVERSAL MARK-AND-SWEEP SEMANTIC GRAPH

No campaign-global root traversal is baseline authority for semantic retention.

Many HDM dependencies are not equivalent to structural graph edges.

## LAW 5.13-8 — NO GENERIC DURABLE REFERENCE COUNTS

Reference counts are not cleanup authority and cannot safely capture semantic dependencies, cycles, source movement or missing enrollment.

## LAW 5.13-9 — NO UNIVERSAL GC FRONTIER

There is no campaign-wide scalar time/event/Git/frontier before which everything becomes deletable.

Generation/epoch bulk retirement is legal only where the native domain contract proves the relevant generation/epoch is replaceable.

---

# 4. Closed cleanup contracts

Automatic current-namespace retirement is allowed only for target kinds/representations with an admitted compatible cleanup contract.

Conceptually:

```text
CleanupContract(target_kind, contract_generation) {
    native_terminality_or_replacement_predicate
    blocking_dependency_classes[]
    bounded blocker/protection route for each class
    survivor_obligations[]
    surviving_reference_semantics[]
    blocker_creating_source_classes[]
    currentness/fencing requirements
    compatibility/migration requirements
}
```

This need not be a standalone persistent record.

## LAW 5.13-10 — CLEANUP CONTRACT IS VALIDATION VOCABULARY, NOT LIVENESS AUTHORITY

The consuming owner owns each forward dependency.

The cleanup contract only declares the complete admitted dependency classes/routes that must be checked for that target representation.

## LAW 5.13-11 — UNKNOWN OR INCOMPATIBLE CLEANUP CONTRACT => RETAIN

Automatic deletion is forbidden when:

- target kind is unregistered for cleanup;
- target/contract generation is incompatible;
- required blocker vocabulary is unknown;
- legacy representation lacks sufficient cleanup semantics.

Target may later migrate/repair and become eligible.

## LAW 5.13-12 — NEW CONSUMER CLASSES ENROLL BEFORE THEY MAY DEPEND

A new owner/consumer type that needs a cleanup-target representation must join the target's typed protection/cleanup contract before accepted durable dependence can rely on it.

Missing enrollment is an integrity/implementation defect, not GC permission.

---

# 5. Cleanup-contract evolution and runtime adoption

## LAW 5.13-13 — CLEANUP INTERPRETATION PARTICIPATES IN RUNTIME/CATALOG COMPATIBILITY

One cleanup assessment uses the cleanup-contract generation accepted for the target under the current campaign/runtime interpretation.

A runtime/catalog adoption that changes:

- blocking dependency classes;
- reference survival meaning;
- cleanup eligibility;
- protection-routing semantics;

must migrate/establish compatible cleanup/protection state before automatic cleanup under the new interpretation is enabled.

Legacy/incompatible targets remain retain-only until migrated.

## LAW 5.13-14 — NEW AMBIENT CLEANUP RULES DO NOT STRAND PINNED OPEN EXECUTION

Open accepted Step-3 execution remains governed by its compatible pinned interpretation/dependency evidence. Cleanup cannot reinterpret that accepted execution merely because ambient engine/catalog generation changed.

---

# 6. Safe-retirement assessment

Deterministic core may construct an ephemeral assessment equivalent to:

```text
SafeRetirementAssessment
    target_ref
    target_cleanup_contract_generation
    pinned_native_bases[]
    terminality_or_replacement_evidence
    blocker_results[]
    survivor_closure
    surviving_reference_validation
    blocker_source/currentness footprint
    disposition
```

Possible logical dispositions include equivalents of:

```text
SAFE_TO_RETIRE_CURRENT_REPRESENTATION
RETAIN_BLOCKED
RETRY_STALE
INTEGRITY_REQUIRED
CAPABILITY_DEFERRED
```

No persistent generic assessment record is required.

## LAW 5.13-15 — NINE OBLIGATIONS OF SAFE RETIREMENT

Automatic current-namespace retirement requires all:

```text
P1 CLEANUP CONTRACT COMPATIBLE
P2 NATIVE TERMINALITY / SUFFICIENT REPLACEMENT
P3 BLOCKER VOCABULARY CLOSED
P4 BLOCKER ABSENCE/DISCHARGE CURRENTLY PROVEN
P5 ALL BLOCKER-CREATING NATIVE SOURCES COVERED
P6 SURVIVOR CLOSURE COMPLETE
P7 SURVIVING REFERENCE SEMANTICS VALID
P8 RESULTING CURRENT STATE VALID
P9 PUBLICATION/CURRENTNESS BASIS STILL VALID
```

Unknown or failed obligation => retain/retry/repair, never guess-delete.

## LAW 5.13-16 — NEGATIVE PROOF IS BASIS-SENSITIVE

“No blocker exists” is valid only under one coherent exact current native source composition sufficient for the target contract.

Do not combine stale negative evidence with newer terminality/survivor state.

---

# 7. Candidate discovery versus authorization

Cleanup candidate discovery is derivative maintenance optimization.

## LAW 5.13-17 — STALE POSITIVE CANDIDATE HINT IS SAFE ONLY BECAUSE IT MUST REVALIDATE

A candidate index/list may be incomplete or stale.

```text
missed candidate
    -> over-retention only

stale positive candidate
    -> current full safe-retirement assessment required
```

Candidate presence never authorizes deletion.

## LAW 5.13-18 — NO ORDINARY GAMEPLAY GARBAGE SCAN

Normal gameplay does not traverse historical runtime records, Story, LOG, chronology or all live refs to discover cleanup candidates.

Cleanup is maintenance/batched work.

---

# 8. Protection routing

Two derivative index/routing classes are semantically distinct:

```text
BEST_EFFORT_DISCOVERY
    omissions permitted
    absence cannot authorize loss

COMPLETENESS-TYPED PROTECTION_ROUTING
    completeness for one declared blocker class is a correctness invariant
    current absence may participate in negative proof
```

## LAW 5.13-19 — PROTECTION ROUTING REMAINS DERIVATIVE

Forward dependency remains with the consuming native owner.

Protection routing provides bounded membership/retrieval evidence only.

## LAW 5.13-20 — NEGATIVE PROOF REQUIRES PROTECTION-ROUTING COMPLETENESS

When absence in routing can authorize irreversible retirement, owner transition and routing enrollment/removal must be durably coherent enough that healthy state cannot expose:

```text
protected current consumer
+ missing required protection membership
```

If completeness/currentness cannot be proven, deletion blocks.

## LAW 5.13-21 — STALE ROUTING CANNOT AUTHORIZE IRREVERSIBLE LOSS

A stale protection index may at most produce retry/retention/integrity diagnosis.

## LAW 5.13-22 — PROTECTION DOMAINS STAY TYPED

Recovery routing, exact-text protection, chronology dependencies and other retention protections may reuse implementation mechanics but do not merge into one universal all-reference graph.

---

# 9. Protection-routing generation lifecycle

## LAW 5.13-23 — CORRECTNESS-COMPLETE ROUTING NEVER AUTHORIZES ITS OWN RETIREMENT

A protection-routing generation retires through its own derivative generation/selection contract, not by observing “no refs” in itself.

## LAW 5.13-24 — OLD PROTECTION ROUTING RETIRES ONLY AFTER CURRENT SUCCESSOR SELECTION

Required order:

```text
compatible successor complete/durable
-> current routing basis selects successor
-> cleanup assessments using old basis must revalidate/finish
-> old generation may retire
```

No durable reader lease is required; basis movement invalidates ephemeral assessments.

---

# 10. Cross-source blocker creation

Campaign HEAD CAS alone is insufficient when another independently writable source can create a new representation-dependent consumer.

## LAW 5.13-25 — EACH BLOCKER-CREATING SOURCE CLASS HAS A SAFE PATTERN

For every admitted cross-source blocker, target cleanup contract must establish at least one:

### SELF-CONTAINED CONSUMER

Accepted consumer owns/pins all required content/evidence and does not need future current target dereference.

### CROSS-SOURCE PROTECTION REGISTRATION

Before/with accepted dependency, source establishes compatible target protection evidence visible to target cleanup proof.

### SOURCE FENCE / SYNCHRONIZATION

Relevant native source is boundedly exact-pinned/frozen through its owner contract for the cleanup transition.

Without a safe pattern, target is not automatically deletable while that source may create blockers.

## LAW 5.13-26 — NO ALL-LIVE SCAN FOR DELETE PROOF

Use typed current routing/protection/fencing. Do not enumerate every live branch to guess whether any may reference a target.

---

# 11. Survivor-before-removal

## LAW 5.13-27 — REQUIRED SURVIVOR PRECEDES SOURCE LOSS

Compact replacement, natural-owner promotion, migrated cursor, exact-certification basis, chronology summary or other required survivor must be established before old representation disappears.

## LAW 5.13-28 — ONE CAMPAIGN RESULTING TREE MAY REPLACE AND RETIRE ATOMICALLY

When survivor/reference updates and target live in one campaign authority domain, one validated Step-5.6 campaign transaction may create/update survivor and remove target in one resulting tree.

## LAW 5.13-29 — CROSS-DOMAIN SURVIVOR IS CONFIRMED FIRST

If survivor and target cannot share one native publication boundary, establish/confirm survivor first; remove old representation later.

Failure biases toward redundancy.

---

# 12. Surviving reference semantics

Stable IDs may have different post-retirement requirements.

The machine model must distinguish semantics equivalent to:

```text
REQUIRES_CURRENT_TARGET
    target must remain currently dereferenceable

OPAQUE_STABLE_PROVENANCE
    stable non-reused identity is sufficient
    current target representation need not exist

SURVIVOR_BACKED
    original target may disappear because a named survivor owns required meaning
```

Exact field/enumeration names are implementation detail.

## LAW 5.13-30 — RESOLVABLE REFERENCE BLOCKS TARGET RETIREMENT

Target cannot disappear while any surviving contract requires current resolution.

## LAW 5.13-31 — OPAQUE PROVENANCE ID MAY OUTLIVE ITS RECORD

A stable never-reused ID can remain as causal/historical attribution without a current target record when the reference contract explicitly needs identity only.

Such non-resolution is not corruption.

## LAW 5.13-32 — LEGACY/UNKNOWN REFERENCE SEMANTICS ARE CONSERVATIVE

Unknown reference meaning defaults to “target may still be required.” Retain/migrate before deletion.

## LAW 5.13-33 — NO UNIVERSAL TOMBSTONE REGISTRY

A narrow compact identity anchor/tombstone is justified only for a concrete owner family that promises stable dereferenceable identity after source retirement and lacks a natural survivor.

---

# 13. Cycles and group retirement

## LAW 5.13-34 — RAW REFERENCE CYCLES ARE NOT LIVENESS

Only declared blocker dependencies retain representations.

## LAW 5.13-35 — GENUINE BLOCKING CYCLES REQUIRE OWNER-GROUP REPLACEMENT OR RETENTION

A group may retire together only when its native domain proves one coherent replacement/survivor closure.

Otherwise retain.

No generic cycle collector/refcount solution is introduced.

---

# 14. Runtime execution artifact cleanup

## LAW 5.13-36 — ACTIVE/UNSETTLED EXECUTION IS PROTECTED

Do not retire representation required by:

- non-SETTLED RuntimeCommand;
- active/suspended Resolution;
- current Continuation;
- active Procedure continuity;
- pending mandatory child/firing;
- fixed RNG;
- unresolved Choice/Reaction;
- accepted interpretation/dependency evidence.

## LAW 5.13-37 — TERMINAL EXECUTION ENABLES LAYERED COMPACTION

After terminality:

- prospective/working execution payload may retire;
- diagnostic trace may retire when nonunique;
- MechanicalEvent/receipt detail may compact after all causal/export/chronology consumers retain sufficient evidence;
- compact idempotency/result anchors may survive longer.

## LAW 5.13-38 — PURE DIAGNOSTIC DETAIL IS NOT UNIVERSAL HISTORY AUTHORITY

ResolutionTrace or equivalent diagnostic detail with no explicit retained audit/repair/provenance contract is an early cleanup candidate after native terminality.

Potential future usefulness alone does not retain it forever.

## LAW 5.13-39 — IDEMPOTENCY EVIDENCE FOLLOWS THE ACCEPTED IDENTITY CONTRACT

Where accepted host/external invocation can still be retried and Step 3 promises duplicate recognition, minimum fingerprint/result/identity evidence remains available.

No generic time-based expiry is introduced.

Detailed execution bodies may retire before compact duplicate-suppression anchors.

---

# 15. Interaction/message linkage

## LAW 5.13-40 — MESSAGE ENVELOPE CANNOT DISAPPEAR WHILE INTERACTION STILL NEEDS ITS CONTENT

A surviving `runtime.interaction`, RuntimeCommand or accepted execution/history owner that still needs source message content or current dereferenceability blocks envelope removal.

## LAW 5.13-41 — RAW MESSAGE LINK MAY BECOME OPAQUE ONLY AFTER SEMANTIC/IDEMPOTENCY DISCHARGE

Once accepted meaning/fingerprint/result evidence is independently sufficient in natural owners, the historical message ID may remain provenance-only if the migrated reference contract says so.

Legacy raw-message refs remain resolvable by default until explicit migration.

---

# 16. Checkpoint cleanup

Checkpoint remains optional facility evidence, not current gameplay authority.

## LAW 5.13-42 — CURRENT `last_checkpoint_id` POINTER PROTECTS ITS TARGET

While MANIFEST selects checkpoint K, deleting K alone is invalid checkpoint-facility state.

## LAW 5.13-43 — SELECTED CHECKPOINT MAY RETIRE WITH COHERENT POINTER CLEAR/REPLACE

When no other protected consumer needs K, one campaign transaction may:

```text
last_checkpoint_id -> K2
+ establish/retain K2
+ remove K
```

or:

```text
last_checkpoint_id -> null
+ remove K
```

No law requires one permanent checkpoint.

## LAW 5.13-44 — UNSELECTED CHECKPOINT MAY RETIRE WHEN NO EXPLICIT PROTECTED CONSUMER REMAINS

Age may prioritize but does not establish eligibility.

## LAW 5.13-45 — BOUNDED CHECKPOINT READERS PIN REVISION; THEY DO NOT CREATE DURABLE GC LEASES

A support/maintenance reader that resolved a checkpoint pointer from campaign revision H should read the descriptor from exact H when it needs stable read consistency.

Later current-tree cleanup does not retroactively invalidate that pinned historical read basis.

---

# 17. Message payload/envelope cleanup

## LAW 5.13-46 — EXACT_RETAINED PAYLOAD IS GOVERNED BY STEP 5.11, NOT WHOLE-RECORD GC

Step 5.13 cannot delete the only exact source while an exact-text consumer remains protected.

## LAW 5.13-47 — COMPACTED MESSAGE ENVELOPE IS ELIGIBLE ONLY AFTER ALL SURVIVOR OBLIGATIONS MOVE

Before whole current-envelope retirement, preserve/migrate as applicable:

- Interaction/idempotency linkage;
- source enumeration/cursor semantics;
- semantic/history provenance;
- material disclosure provenance;
- correction/audit refs;
- live source identity;
- exact archive certification basis.

## LAW 5.13-48 — STORY ENUMERATION CONTINUITY SURVIVES SOURCE RETIREMENT AS PROMISED

Preserve enough source identity/anchors for every **currently supported compatible Story coverage/migration path**.

HDM does not promise arbitrary future reprojection from payload already lawfully removed.

## LAW 5.13-49 — FUTURE PROJECTION CONTRACT CANNOT INVENT DELETED SOURCE

A future Story admission/migration rule that newly desires old deleted material must accept unavailable source unless an earlier explicit retention/migration promise protected it.

---

# 18. Verified-exact Transcript survivor

## LAW 5.13-50 — VERIFIED-EXACT STATUS REQUIRES SURVIVING CERTIFICATION BASIS

If retained `STORY/TRANSCRIPT` continues to claim exact equality after source message envelope retirement, minimum deterministic certification evidence must survive.

Prefer co-location/natural ownership in retained Transcript projection state.

## LAW 5.13-51 — NO CERTIFICATION TOMBSTONE WHEN NO EXACT PROMISE SURVIVES

If no retained record claims verified exactness, no standalone source-digest anchor is created merely because message once existed.

If editorial Story remains but exact certification is unnecessary, revoke `verified_exact` and allow smaller cleanup.

---

# 19. Git transport history versus HDM retained memory

## LAW 5.13-52 — TRANSPORT HISTORY DOES NOT REVERSE LAWFUL SEMANTIC COMPACTION

After Step-5.11 lawful exact compaction/current-source retirement, ordinary Master/Story/history retrieval SHALL NOT mine old Git commits to restore verbatim wording merely because bytes remain in append-only Git history.

```text
Git history contains old bytes
    !=
HDM exact historical text is semantically retained
```

## LAW 5.13-53 — FORENSIC/INTEGRITY HISTORY READ IS EXPLICITLY SEPARATE

Bounded authorized repair/security/support may inspect historical Git transport evidence when its contract requires it.

Such inspection does not silently promote all compacted text back into ordinary permanent Master memory.

## LAW 5.13-54 — NO ORDINARY SECURE-ERASURE PROMISE

Current-tree retirement means:

```text
not retained in current HDM representation
not normally retrievable through current semantic/history contracts
```

It does **not** mean:

```text
guaranteed erased from all Git history/server storage
```

Secure expungement of previously committed bytes requires separate explicit storage/security/history-rewrite architecture.

---

# 20. Story cleanup

## LAW 5.13-55 — STORY CURRENT CLOSURE MUST REMAIN COHERENT

Story record/index/availability/allocator/coverage/cross-reference invariants from Step 5.10 remain valid across cleanup.

## LAW 5.13-56 — STORY GENERATION BULK RETIREMENT IS NATIVE-DOMAIN OPTIMIZATION ONLY

Old projection/index generations may bulk-retire only after compatible successor/current state is established and no supported migration/projection/reference dependency requires old material.

## LAW 5.13-57 — BULK GENERATION LABEL DOES NOT OVERRIDE SPARSE CROSS-GENERATION SURVIVORS

Current Story refs/provenance may keep individual old-generation records alive. Retain/migrate those survivors even if the rest of generation retires.

## LAW 5.13-58 — EDITORIAL HISTORY IS NOT UNIVERSALLY PERMANENT

Step 5.13 creates no promise to retain every superseded Story prose version.

Explicit exact/archive/history policy remains authoritative when present.

---

# 21. Chronology cleanup

## LAW 5.13-59 — STEP 5.9 OWNS CHRONOLOGY SEMANTIC COMPACTION ELIGIBILITY

Step 5.13 does not independently decide that chronology relation/metric evidence is redundant.

It consumes owner/protected-consumer proof from Step 5.9.

## LAW 5.13-60 — CHRONOLOGY SURVIVOR MUST PRESERVE REQUIRED PREDICATE ANSWERS/FEASIBLE SETS

Physical cleanup may follow only after protected consumer decidability, required precision and unique causal provenance are preserved.

## LAW 5.13-61 — DERIVATIVE CHRONOLOGY INDEX RETIREMENT DOES NOT RETIRE SOURCE RELATIONS

Index/frontier/cache generations follow their own derivative replacement lifecycle.

## LAW 5.13-62 — NO CAMPAIGN-WIDE TEMPORAL REDUCTION PASS

Do not reconstruct/reduce the entire historical chronology graph solely for garbage collection.

---

# 22. Disclosure retention

## LAW 5.13-63 — VALID SPARSE `runtime.disclosure` IS NOT ORDINARY AGE-BASED GARBAGE

Human exposure cannot be made unexposed merely because time passed, secret became public or campaign advanced.

Disclosure may be merged/migrated only under an owner-specific transition preserving equivalent exposure semantics.

Storage pressure alone does not authorize deletion.

---

# 23. Live source/ref cleanup

Maintenance classification includes concepts equivalent to:

```text
ACTIVE
CLOSED_UNABSORBED
NONAUTHORITATIVE_ABSORBED
NONAUTHORITATIVE_PREPARED_ORPHAN
UNCLASSIFIED_NONCURRENT_REF
```

## LAW 5.13-64 — ACTIVE LIVE REF CANNOT BE CLEANED

Current selected ACTIVE source is truth/writable authority.

## LAW 5.13-65 — CLOSED_UNABSORBED LIVE REF CANNOT BE CLEANED

Current selected CLOSED source remains truth/recovery source until campaign absorption completes.

## LAW 5.13-66 — ABSORBED LIVE REF MAY RETIRE ONLY AFTER RETRIEVAL DEPENDENCIES DISCHARGE

Require bounded current campaign evidence that exact final live source has been absorbed/route-away is current plus proof no retained consumer needs the live ref/source as resolvable evidence.

## LAW 5.13-67 — PREPARED ORPHAN REF REQUIRES BOUNDED NONAUTHORITY EVIDENCE

Branch existence or absence from current route alone does not prove “never selected.”

Use bounded preparation/opening/route evidence.

If disposition remains uncertain without broad history scan, retain/report as unclassified noncurrent ref.

## LAW 5.13-68 — UNCLASSIFIED NONCURRENT REF MAY REMAIN HARMLESS

Unknown leftover clutter does not become authority and does not block gameplay unless current routing/other required contract depends on it.

Do not scan history merely to clean it cosmetically.

## LAW 5.13-69 — MISSING LIVE SOURCE IS HEALTHY ONLY AFTER AUTHORITY ENDED

Missing source while current route selects ACTIVE/CLOSED_UNABSORBED remains integrity failure/suspicion per Step 5.8.

Missing absorbed/orphan ref after successful cleanup is normal.

## LAW 5.13-70 — STALE HOST CANNOT RECREATE OLD AUTHORITY

Current campaign routing selects authority. A stale host encountering missing/closed old source must resynchronize/route forward and may not recreate/adopt old epoch from cached branch name.

Authority-generation epoch/ref identities are not reused.

---

# 24. Optional ref-delete capability

## LAW 5.13-71 — REF DELETION REQUIRES SUPPORTED AUTHENTICATED RepositoryPort CAPABILITY

No native Git/CLI/private HTTP workaround is implied by cleanup semantics.

## LAW 5.13-72 — MISSING REF-DELETE CAPABILITY DEFERS CLEANUP, NOT GAMEPLAY

If old non-authoritative ref is eligible but deployment cannot delete refs:

```text
CAPABILITY_DEFERRED
```

or equivalent maintenance outcome is sufficient.

Current authority/gameplay remains valid.

## LAW 5.13-73 — REF DELETE AMBIGUITY USES TARGETED CURRENT-REF VERIFICATION

After indeterminate delete acknowledgement:

```text
ref absent
    -> cleanup achieved

ref present at exact expected old source
    -> revalidate then retry may be allowed

ref present at unexpected/different source
    -> do not delete; maintenance/integrity conflict
```

No durable generic delete job is required.

---

# 25. Prepared/unreachable Git objects

## LAW 5.13-74 — PREPARED LOSING OBJECTS ARE ALREADY NONAUTHORITY

A blob/tree/commit never selected by authoritative ref is not gameplay/history authority merely because Git server stores the object.

## LAW 5.13-75 — NO DURABLE ORPHAN-OBJECT REGISTRY BASELINE

Do not create persistent metadata whose sole purpose is to remember unreachable prepared SHAs for later Git GC.

Doing so would turn transport garbage into new reachable storage.

## LAW 5.13-76 — NO ARBITRARY COMMIT/TREE/BLOB DELETE OPERATION IS REQUIRED BASELINE

Actual unreachable-object reclamation remains host-managed Git maintenance.

Support diagnostics may report already-known SHAs without becoming retention authority.

---

# 26. Campaign cleanup publication

Campaign current-namespace cleanup obeys Step 5.6.

## LAW 5.13-77 — CURRENT-NAMESPACE DELETE IS A NORMAL SEMANTIC CAMPAIGN DELTA

One cleanup transaction freezes:

- target/current basis;
- complete replacement/survivor updates;
- affected reference/routing updates;
- explicit DELETE paths;
- blocker/currentness dependency footprint.

Then validates resulting tree and publishes one single-parent non-force campaign commit.

## LAW 5.13-78 — RELEVANT MOVEMENT INVALIDATES SAFE-RETIREMENT PROOF

Movement affecting target owner, blocker routes, survivor closure, reference semantics, runtime/cleanup interpretation or blocker-creating sources requires revalidation.

Proven unrelated campaign movement may use normal Step-5.6 transport-only rebuild.

## LAW 5.13-79 — AMBIGUOUS CAMPAIGN CLEANUP OUTCOME RESOLVES CURRENT AUTHORITY

Do not blindly replay delete.

Use Step-5.6 current lineage/resulting-state verification. If current state already embodies valid retirement, adopt it; otherwise rederive from current authority.

## LAW 5.13-80 — FAILURE BIASES TOWARD EXTRA REPRESENTATION

When survivor durability or cleanup publication is uncertain, retain source/representation until current sufficient replacement is proven.

---

# 27. Maintenance execution model

## LAW 5.13-81 — NO BACKGROUND GC REQUIREMENT

Cleanup is correctness-optional maintenance and may run:

- on explicit maintenance request;
- opportunistically at suitable boundaries;
- in bounded batches;
- across several sessions.

Gameplay correctness never relies on an autonomous cleanup worker.

## LAW 5.13-82 — NO DURABLE GENERIC GC JOB/QUEUE

After interruption, remaining cleanup is rediscovered from current owner/candidate state.

Already-retired state requires no semantic replay.

Optional batch diagnostics/audit is non-authoritative.

## LAW 5.13-83 — CLEAN MAINTENANCE CREATES NO HEARTBEAT

No eligible current-tree delta => no cleanup commit solely to say “checked.”

## LAW 5.13-84 — AGE/SIZE/PRESSURE ARE PRIORITIZATION SIGNALS ONLY

They may choose among already-safe candidates.

They never make protected representation semantically eligible.

---

# 28. Diagnostic usefulness does not imply permanent retention

## LAW 5.13-85 — POSSIBLY USEFUL FUTURE FORENSICS IS NOT A UNIVERSAL RETENTION ROOT

Only explicit audit/repair/provenance contracts protect evidence.

Lawful cleanup may reduce later forensic richness.

Support/repair must report unavailable evidence honestly and never reconstruct/invent it.

---

# 29. World-record boundary

## LAW 5.13-86 — NO GENERIC TERMINAL WORLD-ENTITY DELETE POLICY

Dead actors, consumed assets, completed missions, superseded lore records and other world/history entities are not automatically garbage.

Automatic retirement applies only to owner kinds whose native canonical lifecycle explicitly admits representation retirement and whose cleanup contract is closed.

Step 5.13 does not invent broader lore/history deletion semantics.

---

# 30. Legacy migration

## LAW 5.13-87 — LEGACY CLEANUP IS RETAIN-FIRST

Legacy target/ref/protection state lacking required cleanup semantics stays retained until migration/repair establishes:

- compatible cleanup contract;
- surviving reference semantics;
- necessary survivor evidence;
- typed protection routing where required.

## LAW 5.13-88 — CLEANUP NEVER INVENTS REPLACEMENT EVIDENCE

Missing exact text, causal event content, chronology relation, idempotency evidence or provenance cannot be hallucinated/reconstructed merely to make deletion possible.

If required evidence was already lost, integrity/repair owns the defect.

---

# 31. Integrity classification

Examples of cleanup-related integrity defects/suspicions:

```text
forward protected owner exists but correctness-complete protection membership is absent
selected checkpoint pointer targets missing descriptor
current campaign route selects missing live source
verified-exact Transcript lacks surviving certification basis
required-resolvable ref target disappeared
cleanup-contract generation incompatible with current consumer/target semantics
survivor migration claims completion but required meaning is absent
```

## LAW 5.13-89 — “CANNOT PROVE SAFE” IS NOT ITSELF CORRUPTION

An otherwise healthy artifact that cannot prove retirement simply stays retained.

Integrity suspicion requires actual mismatch/missing required representation/contradiction, not mere cleanup ineligibility.

---

# 32. Performance contract

Ordinary gameplay adds:

```text
zero campaign-wide cleanup scans
zero arbitrary Git-history scans
zero ref enumeration for GC
zero per-turn cleanup commits
zero background-worker requirement
```

One maintenance batch should cost approximately:

```text
selected candidate batch
+ each candidate's typed blocker/survivor routes
+ required currentness validation of affected native sources
+ actual cleanup publication when nonempty
```

not an unbounded traversal proportional to all historical campaign artifacts for each candidate.

Large candidate discovery may be batched/index-assisted maintenance.

---

# 33. Repository growth contract

## LAW 5.13-90 — CURRENT-NAMESPACE CLEANUP IS USEFUL WITHOUT CLAIMING OBJECT-STORE SHRINKAGE

It reduces:

- current tree/routing/index clutter;
- current discovery/migration burden;
- stale live refs where supported;
- future payload duplication;
- accidental current-context retrieval of obsolete data.

It also provides correct semantic eligibility for future storage backends capable of reclaiming bytes.

With current append-only Git, historical ancestor objects may still dominate repository size.

## LAW 5.13-91 — MEASURED HISTORY GROWTH MAY TRIGGER A FUTURE STORAGE DECISION

If campaign Git history approaches practical host limits or materially harms operation, that is a separate storage/history architecture decision.

Step 5.13 does not silently solve it with force push or history rewrite.

---

# 34. Current platform/Connector disposition

Current research establishes:

- GitHub REST supports ref deletion in principle;
- current connected GitHub Connector surface in this environment does not expose a ref-delete operation;
- GitHub does not provide ordinary HDM per-object commit/tree/blob deletion semantics;
- removing a file in Git history does not erase older committed content.

These are deployment/platform facts, not semantic authority.

Step 6 must re-check actual RepositoryPort capabilities for supported deployment profiles.

---

# 35. Machine-realization debt

After architecture sequence closure, implementation planning must cover at least:

1. target-family cleanup-contract representation/registry;
2. cleanup-contract generation and runtime/catalog compatibility migration;
3. SafeRetirementAssessment implementation;
4. reference-survival semantics (`requires target`, opaque provenance, survivor-backed or equivalent);
5. typed correctness-complete protection routing where concrete families need it;
6. best-effort candidate discovery partitions/indexes where measured useful;
7. protection-routing successor/current-generation lifecycle;
8. cross-source blocker creation/self-contained/protection/fence integration;
9. survivor-before-removal transaction construction;
10. Step-3 terminal detail compaction and compact idempotency/result anchors;
11. Interaction/message semantic/idempotency discharge;
12. receipt/MechanicalEvent/trace retention contracts;
13. checkpoint pointer/descriptor cleanup;
14. COMPACTED message-envelope retirement;
15. Story source enumeration/cursor survivor migration;
16. verified-exact Transcript certification survivor/co-location;
17. chronology physical retirement consuming Step-5.9 semantic eligibility;
18. Story old generation/index/cross-generation survivor cleanup;
19. disclosure non-GC/merge rules realization;
20. live ref classification and nonreused epoch/ref identity;
21. optional RepositoryPort `DeleteRef` with accepted/rejected/indeterminate verification;
22. capability-deferred ref cleanup behavior;
23. explicit runtime prohibition on ordinary Git-history resurrection of lawfully compacted exact text;
24. maintenance dry-run/diagnostic outputs and optional non-authoritative audit;
25. legacy conservative migration;
26. repository current-tree/history growth metrics;
27. support/player/admin wording distinguishing semantic/current-tree retirement from secure erasure;
28. all required regression/adversarial tests below.

No broad GAME/schema implementation is authorized by Step 5.13 architecture closure.

---

# 36. Required regression cases

At minimum later implementation tests must include:

1. active RuntimeCommand cannot clean;
2. settled trace detail can retire while required idempotency anchor survives;
3. fixed RNG/receipt/export dependency blocks deletion;
4. current Continuation blocks deletion; superseded generation with no survivor dependency may retire;
5. unknown cleanup-contract generation => retain;
6. engine adoption changing blocker vocabulary forces migration/revalidation;
7. stale candidate hint cannot authorize deletion;
8. correctness-complete protection membership missing for live forward dependency => integrity defect;
9. stale protection routing causes retry/retain;
10. protection-routing old generation retires only after successor selection;
11. campaign dependency appears after proof => proof invalidated;
12. live-source dependency appears without campaign movement and lacks protection/fence => retain;
13. self-contained cross-source consumer does not block target current-tree retirement;
14. selected checkpoint cannot dangle;
15. pointer clear/replace + checkpoint removal coherent;
16. unselected checkpoint no longer protected may retire;
17. pinned checkpoint support read remains coherent while current tree later cleans it;
18. EXACT_RETAINED message cannot whole-envelope retire;
19. Interaction content dependency blocks COMPACTED envelope deletion;
20. Interaction semantic/idempotency survivor permits provenance-only message ID;
21. Story cursor anchor blocks envelope deletion until migration;
22. supported coverage migration works after envelope retirement;
23. unsupported future reprojection cannot invent deleted source;
24. verified-exact Transcript requires certification survivor;
25. no verified-exact claim => no generic certification tombstone;
26. old Git history may contain text but ordinary exact query remains SEMANTIC_ONLY;
27. explicit forensic read does not change default retained-memory status;
28. opaque provenance ID may remain unresolved without corruption;
29. required-resolvable ref blocks cleanup;
30. unknown legacy ref blocks cleanup;
31. genuine blocking cycle retains/group-migrates; no refcount cycle bug;
32. Step-5.9 protected chronology consumer blocks relation evidence deletion;
33. lossless chronology survivor permits physical retirement;
34. current Story cross-generation ref blocks bulk old-generation removal;
35. sparse Story survivor migration permits partial generation retirement;
36. valid disclosure row is not age-GCed;
37. ACTIVE live ref cannot delete;
38. CLOSED_UNABSORBED ref cannot delete;
39. absorbed live ref may clean only after no retrieval dependency;
40. prepared orphan requires bounded nonauthority proof;
41. unclassified noncurrent ref stays harmless/retained;
42. missing selected live source is suspect; missing cleaned absorbed source is healthy;
43. stale host cannot recreate old live authority;
44. missing DeleteRef capability => deferred maintenance, gameplay unaffected;
45. ambiguous DeleteRef + absent ref resolves success;
46. ambiguous DeleteRef + unexpected ref target blocks cleanup;
47. prepared losing commit creates no durable orphan registry;
48. ambiguous campaign cleanup publication resolves current authoritative result;
49. crash mid-cleanup batch resumes by rediscovery;
50. repeated cleanup is idempotent;
51. no candidates => no heartbeat commit;
52. age/storage threshold never overrides protected dependency;
53. potential diagnostic usefulness without contract does not block cleanup;
54. generic terminal world entity is not automatically deletable;
55. ordinary gameplay performs no GC/history scan.

---

# 37. Step-5.14 carry-forward adversarial scenarios

Step 5.14 final Step-5 review must explicitly include at least:

- cleanup candidate races new campaign dependency;
- cleanup candidate races new live-source dependency;
- stale/incomplete protection routing;
- runtime/catalog adoption changing blocker vocabulary;
- message-envelope retirement while Interaction/idempotency survives;
- Story cursor and exact-certification survivor behavior;
- chronology protected-consumer cleanup;
- checkpoint pointer cleanup;
- live ACTIVE/CLOSED/absorbed/orphan/missing-ref cleanup;
- ref-delete unavailable and ambiguous outcomes;
- crash/ambiguous campaign deletion publication;
- lawfully compacted exact text still present in Git history but not ordinary semantic memory;
- prepared unreachable Git objects with no orphan registry;
- cleanup batch interruption/restart;
- no campaign-wide cleanup scan or global GC authority contamination.

---

# 38. Canonical exit proof

Step 5.13 architecture closes because:

1. cleanup cannot establish/replace semantic authority;
2. target cleanup is owner-gated and version/contract compatible;
3. negative proof is closed by declared blocker vocabulary, not arbitrary searches;
4. only correctness-complete current protection routing may support absence proof;
5. cross-native-source blocker creation is explicitly covered;
6. survivor evidence always precedes representation loss;
7. surviving reference semantics are explicit and conservative;
8. active/pending/recoverable Step-3/5.2/5.3 state cannot be stranded;
9. checkpoint, Story, chronology, exact-text, disclosure and live boundaries remain with their canonical owners;
10. current-tree cleanup and Git-history/object reclamation are honestly separated;
11. live ref deletion is post-authority, optional and capability-gated;
12. prepared Git objects remain nonauthority without a new GC ledger;
13. cleanup failure/ambiguity biases to current-state verification and extra retention;
14. maintenance requires no background worker or job queue;
15. ordinary gameplay has no campaign-wide GC cost;
16. legacy ambiguity retains rather than destroys;
17. no new human/product decision or Step-5 architecture blocker remains.

Canonical summary:

> **Every representation HDM removes from its current authoritative namespace is already semantically retired or sufficiently replaced under its native owner; a bounded current proof establishes that all admitted protected consumers and blocker-creating sources are accounted for, and every promised survivor remains valid. Cleanup may remove current clutter and non-authoritative refs, but it never becomes the operation that decides gameplay truth, pending work, chronology, knowledge, disclosure, Story authority, or the historical existence of Git bytes.**

Step 5.13 architecture is closed.

Next roadmap slice after status closure: **Step 5.14 — Full Recovery & Concurrency Adversarial Review**.

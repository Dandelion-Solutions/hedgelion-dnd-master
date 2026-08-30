# Step 5.13 — Garbage Collection / Orphan Cleanup — Research Draft

Status: **RESEARCH DRAFT — NOT CANONICAL**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Task brief:

- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-task-brief.md`

Research basis includes current remote repository state after activation of Step 5.13, canonical Steps 3 and 5.2–5.12, runtime storage/live/integrity contracts, current Connector capabilities and current primary Git/GitHub documentation.

---

# 1. Executive research finding

The evidence strongly rejects a new universal GC owner, global mark/sweep graph or durable reference-count authority.

The leading architecture is a **layered owner-gated maintenance model**:

```text
native owner lifecycle / retention contract
        |
        v
candidate becomes semantically retirement-eligible
        |
        v
bounded typed blocker/survivor proof
        |
        v
freeze current authority + dependency footprint
        |
        v
replacement/promotions first where required
        |
        v
campaign-path delete / metadata retirement
        |
        v
optional ref cleanup where transport supports it
```

A derivative cleanup-candidate index may improve discovery, but:

- missing/stale candidate hints may only cause over-retention;
- candidate hints never authorize deletion;
- negative safety proof must come from the target kind's closed retention/protection contract under a coherent current authority basis.

The most important platform finding is that **current-tree deletion and Git-history erasure are not the same operation**.

For a normal append-only campaign branch:

```text
old commit contains blob B
new commit deletes path to B

B remains reachable through old campaign ancestors
```

Therefore normal Step-5.13 cleanup can reduce the current authoritative namespace, runtime retrieval/index burden and live-ref clutter, but it cannot promise actual erasure of previously committed campaign bytes or reduction of reachable Git history without history rewrite. The project has already forbidden force-push/history-rewrite as an ordinary runtime mechanism.

This finding changes the meaning of “physical deletion” for Step 5.13 and must be explicit in the final spec.

---

# 2. Verified facts

## 2.1 Repository / architecture facts

### FACT R1 — Step 5.13 is the active roadmap slice

Current roadmap after activation:

```text
5.12 CLOSED
5.13 IN PROGRESS
5.14 not started
```

Step 5.13 purpose is safe removal of obsolete artifacts without stranding active/recovery/chronology/Story/transcript/disclosure/live dependencies.

### FACT R2 — recovery root discovery is already native and typed

Steps 5.2/5.7 require active native owners and independently-due temporal owners to remain discoverable through bounded typed routing. Derived caches/indexes rebuild.

Consequence:

> A generic GC root set must not duplicate the recovery root system.

### FACT R3 — Step 3 already separates terminality from evidence retention

Step 3 establishes that:

- RuntimeCommand remains non-SETTLED until mandatory descendant closure finishes;
- Continuation generations are single-consume and stale generations fail typed validation;
- MechanicalEvents are compact committed mechanical facts/provenance;
- segment receipts are immutable evidence/results, not current-state authority;
- trace/Event bodies may compact only after live mechanics retain required causal/order evidence;
- Effect recency explicitly demonstrates that compact owner-local evidence can outlive detailed trace bodies.

Therefore terminal operational lifecycle alone is not enough to delete all associated historical evidence.

### FACT R4 — checkpoint is optional facility evidence

Step 5.7 says checkpoint is optional immutable recovery/maintenance evidence, not current authority and not a mandatory startup anchor.

`MANIFEST.last_checkpoint_id` is only the campaign-domain pointer to the most recently selected/published checkpoint descriptor.

Current shipped checkpoint schema is materially stale relative to Step 5.7 (generic `valid_through_event_id`, self-referential-style `expected_commit_sha`, copied world-time assumptions). That stale schema is migration/implementation debt, not a reason to preserve old checkpoint semantics.

### FACT R5 — live authority ends before branch cleanup

Step 5.8 explicitly distinguishes:

```text
ACTIVE
CLOSED_UNABSORBED
campaign absorption confirmed
```

and states that close/absorption/branch cleanup are technical authority operations that do not advance fiction.

`CLOSED_UNABSORBED` remains current truth with zero ordinary writers and cannot be cleaned up as if it were an orphan.

After confirmed absorption, old live source is non-authoritative.

### FACT R6 — chronology already defines semantic compaction eligibility

Step 5.9 defines:

- protected-consumer bounded retention;
- safe compaction only when lawful answer/feasible set remains sufficient;
- preservation of unique causal provenance;
- preservation of required metric feasible sets;
- independent lifecycle of derivative indexes/frontiers versus source relation evidence.

Step 5.13 should physically realize that eligibility; it must not invent a second chronology retention model.

### FACT R7 — Story coverage already carries catch-up idempotency

Step 5.10 defines layer/domain/contract-generation coverage and requires source cursor continuity after compaction.

Story `source_refs` preserve attribution identity but do not by themselves promise permanent full-payload dereferenceability.

Therefore a deleted source record can be compatible with Story only when remaining identity/cursor semantics are explicitly sufficient.

### FACT R8 — message exact payload and message envelope have distinct lifetimes

Step 5.11 already defines:

```text
EXACT_RETAINED -> COMPACTED
```

Physical removal of the compact envelope was explicitly deferred to Step 5.13.

Step 5.11 further forbids a generic global reference count and requires bounded typed protection routing.

### FACT R9 — cleanup is not a host-delivery reliability problem

Step 5.12 intentionally rejected baseline delivery outbox, chunk exposure ledger, delayed-delivery reconciliation queue and background resend worker.

There is no such durable job system to GC.

### FACT R10 — current runtime integrity policy is scope-local and bounded

`GAME/CORE/INTEGRITY.md` forbids full-campaign/world/history scans in normal play and treats broad audits as maintenance operations.

This supports maintenance-time cleanup while preserving a zero-cost ordinary gameplay path.

---

# 3. Git / GitHub platform facts

Primary sources consulted:

- GitHub REST API — Git references;
- GitHub Docs — deleting files / removing sensitive data;
- GitHub Docs — repository limits / large files;
- Git documentation — `git gc`, `git prune`, `git reflog`.

## FACT G1 — deleting a Git ref is a supported GitHub operation

GitHub REST provides `DELETE /repos/{owner}/{repo}/git/refs/{ref}` with repository Contents write permission.

Therefore a future RepositoryPort can lawfully expose branch/ref deletion as a typed capability.

## FACT G2 — the currently connected GitHub Connector does not expose ref deletion

Current Connector discovery in this environment exposes:

- `update_ref`;
- `create_branch`;
- exact reads/compare;
- file deletion;

but its available `delete` tool surface currently exposes file deletion only, not a Git ref deletion operation.

This is a current deployment/tool capability gap.

It does **not** change Step-5.8 authority semantics and does not justify native Git/CLI/private HTTP fallback under project policy.

Practical consequence:

> Baseline correctness must tolerate non-authoritative old live refs remaining physically present when the deployment cannot delete them.

## FACT G3 — deleting a file in a new commit does not erase old content from Git history

GitHub explicitly documents that deleted file content remains available in Git history; full removal requires repository-history rewriting.

For HDM's append-only/non-force campaign policy:

```text
current-tree deletion != historical-byte erasure
```

## FACT G4 — full sensitive-data removal is operationally incompatible with ordinary HDM runtime policy

GitHub's sensitive-data purge procedure requires history rewrite and force-push, coordination with collaborators, changed commit hashes, possible PR/reference cleanup and in some cases GitHub Support server-side garbage collection.

HDM ordinary runtime explicitly forbids force push/history rewind.

Therefore secure expungement of already-published sensitive data is an exceptional repository-owner/support operation outside Step-5.13 ordinary runtime semantics.

## FACT G5 — unreachable Git object reclamation is host/database maintenance, not normal HDM object deletion

Git's own `git gc`/`git prune` distinguishes reachable refs/reflogs from unreachable objects and warns about concurrent pruning hazards.

GitHub does not expose a normal runtime API for deleting arbitrary commit/tree/blob objects one by one.

Consequently:

- a prepared losing commit is non-authoritative immediately;
- HDM can stop referencing it;
- actual object reclamation is managed by Git hosting/GC policy;
- HDM must not report “object physically deleted” merely because it is unreachable.

## FACT G6 — repository growth is a real but currently non-numeric project risk

GitHub recommends repositories ideally remain below 1 GB and strongly recommends below 5 GB; it also recommends small individual Git objects.

HDM has no measured campaign-storage growth model yet.

Therefore Step 5.13 should:

- avoid unnecessary durable bulky payloads;
- clean current-tree/index/ref clutter;
- expose measurement/debt for real repository growth;
- not invent an arbitrary TTL or history rewrite purely from generic GitHub size guidance.

---

# 4. Key semantic distinction discovered

The final architecture needs five distinct verbs/stages.

```text
1. SEMANTIC TERMINALITY
   owner no longer active/current/pending

2. REPRESENTATION COMPACTION
   bulky/detail representation replaced by sufficient compact evidence

3. CURRENT-NAMESPACE RETIREMENT
   record/path/index removed from current authoritative tree or current routing

4. REF RETIREMENT
   non-authoritative branch/ref removed where supported

5. GIT OBJECT RECLAMATION
   unreachable object bytes reclaimed by Git host/maintenance
```

These stages are not equivalent.

Examples:

- a SETTLED command may be semantically terminal but retain a compact idempotency receipt;
- a COMPACTED message may lose text but retain source identity;
- a message envelope may later disappear from the current tree while old Git commits still contain historical blobs;
- an absorbed live branch may be non-authoritative before its ref is deleted;
- a deleted ref may leave unreachable objects until server GC.

Recommended terminology in the final spec should avoid calling all five “deletion.”

---

# 5. Proposed common safe-retirement proof shape

Research supports a common *proof shape*, but not one common authority record.

Conceptually:

```text
SafeRetirementProof(A, Basis B):

1. TARGET CONTRACT
   artifact kind/version has an admitted cleanup contract

2. NATIVE TERMINALITY / REPLACEMENT
   native owner says A no longer owns active/current/pending semantics
   OR a replacement representation is already current and sufficient

3. PROTECTED-CONSUMER CLOSURE
   every blocking dependency class registered for A's cleanup contract
   is absent, discharged, or independently satisfied

4. SURVIVOR CLOSURE
   required identity/provenance/cursor/chronology/idempotency evidence
   remains available after removal

5. CURRENT AUTHORITY BASIS
   proof is evaluated against pinned exact native source revision(s)

6. CONCURRENCY FOOTPRINT
   every path/source whose movement could create/restore a blocker
   is part of revalidation/publication dependency footprint

7. RESULTING-STATE VALIDATION
   the planned result has no required dangling reference or broken owner contract
```

No mandatory serialized `SafeRetirementProof` record is required.

It is an in-process deterministic proof/result analogous to other Step-5 validation values.

---

# 6. Closed-world deletion contract

A critical safety requirement emerges from negative proof.

It is unsafe to say:

```text
"search found no references -> delete"
```

because unknown owner kinds, unindexed dependencies or stale reverse indexes may exist.

Instead, automatic deletion of target kind K requires a **closed cleanup contract** for that K/version that defines every dependency class that is capable of blocking deletion.

Conceptually:

```text
CleanupContract(K, generation):
    native terminality predicate
    blocking dependency classes / bounded query routes
    survivor obligations
    current-basis requirements
    migration compatibility
```

This is a machine-contract idea, not necessarily a new persistent record.

Rules:

- unknown/unregistered target kind => no automatic physical retirement;
- new future consumer kind that needs a deletable target representation must register the corresponding blocking dependency relation before relying on it;
- migration changing blocker semantics changes the cleanup-contract generation or equivalent compatibility basis;
- incomplete legacy cleanup metadata => retain or targeted migration/repair, never assume safe.

This converts “absence” from an open-world guess into a bounded closed-contract proof.

---

# 7. Candidate discovery versus deletion authorization

Research strongly favors asymmetric safety.

## 7.1 Candidate discovery may be lossy/stale

A derivative maintenance structure may list likely candidates:

```text
terminal commands
consumed continuation generations
superseded checkpoint IDs
compacted message envelopes
absorbed live epochs
obsolete Story index generations
```

A missing candidate only causes over-retention.

Therefore candidate discovery indexes may be:

- rebuildable;
- incomplete temporarily;
- partitioned/bucketed;
- maintained opportunistically.

They do not become authority.

## 7.2 Deletion authorization may not be stale

A positive candidate must be revalidated against:

- current native lifecycle;
- all blocker classes in the target cleanup contract;
- current survivor closure;
- exact current source basis.

A stale candidate hint cannot delete anything.

This gives a useful architecture rule:

> **Stale positive discovery is safe; stale negative protection evidence is not.**

---

# 8. Reverse protection indexes

Some target kinds cannot prove blocker absence cheaply from forward owners alone.

A derivative reverse protection index is justified only when:

- a concrete deletable target kind has potentially many current consumers;
- forward traversal would require unbounded campaign scan;
- current consumers already declare typed forward dependencies;
- reverse membership can be maintained in the same durability closure strongly enough that absence is trustworthy for the target cleanup contract.

Example classes already anticipated by canonical steps:

- exact-text consumer routing (Step 5.11);
- chronology protected-consumer routing (Step 5.9);
- recovery root/dependency routing (Steps 5.2/5.7).

Do **not** merge these into one universal “all refs” index merely for GC.

A generic runtime/library can provide common index mechanics, but semantic membership remains typed by owner contract.

---

# 9. Concurrency model for cleanup

Cleanup is another optimistic semantic transaction, not a lock or background lease.

Campaign-domain flow:

```text
pin campaign H
resolve candidate A
load native lifecycle + blocker routes at H/current selected native sources
build survivor/replacement state
freeze deletion dependency footprint
construct resulting tree delta
validate no required dangling refs
preflight / Step-5.6 publication
non-force ref update
```

If campaign HEAD moves:

- use Step-5.6 dependency-aware movement classification;
- movement in any blocker/survivor/owner dependency invalidates delete proof;
- proven unrelated movement may permit transport-only rebuild;
- never delete using the old negative proof after relevant movement.

Cross-native-source case:

If a live/current other source can create a new blocking dependency on a campaign target concurrently, deletion needs one of:

- existing owner/source routing contract that already pins/fences that dependency;
- a durable target-domain protection relation established before the consumer may depend on the target;
- source freeze/synchronization boundary.

Do not assume campaign CAS alone protects dependencies born in independent writable sources.

This issue is a required adversarial target.

---

# 10. Replacement-before-removal law candidate

When deletion depends on a compact replacement, summary, promoted owner or migrated cursor, safe ordering is:

```text
replacement becomes durable/current
        before
source representation disappears
```

Where source + replacement live in one campaign transaction and the resulting tree can be validated atomically, one coherent transaction may perform both.

Where they are in distinct native domains or the replacement is noncanonical Story:

```text
publish/confirm replacement first
then independently remove old source later
```

Failure biases toward temporary redundancy.

This composes Step-5.11 and Step-5.6 rather than creating a two-phase transaction coordinator.

---

# 11. Artifact responsibility matrix

| Artifact family | Native owner/source | Why it exists | Blocking consumers / survivor needs | Candidate retirement signal | Likely cleanup shape |
|---|---|---|---|---|---|
| active RuntimeCommand | command owner | accepted execution/idempotency/root closure | descendants, receipts, retry, audit | never while non-SETTLED | forbidden |
| settled RuntimeCommand detail | command/history | idempotency/history | compact retry receipt, provenance refs | SETTLED + no content-dependent consumers | compact detail; possibly retain minimal idempotency identity |
| Resolution | resolution owner | execution state | parent/root, Continuation, receipts, history | terminal + descendants settled | compact/retire after survivor proof |
| Continuation generation | resolution continuation | suspended fixed inputs | current Resolution, stale-generation validation, audit | consumed/superseded + no retry/content dependency | remove detailed generation; retain only necessary generation/result identity if required |
| receipt / MechanicalEvent detail | execution evidence | idempotency/provenance/mechanics | later exports, causal refs, chronology, semantic history | all live mechanical consumers discharged | compact detail; preserve unique causal/export evidence |
| ResolutionTrace | diagnostic/derived evidence | debugging/explanation | any explicitly retained audit dependency | no unique evidence + owner terminal | aggressive candidate for compaction/removal |
| current checkpoint | checkpoint facility | selected diagnostic/recovery hint | `last_checkpoint_id`, support operation | normally retained while selected | do not auto-delete unless pointer coherently cleared/replaced |
| older checkpoint | checkpoint facility | historical diagnostics | explicit audit/repair refs | not selected + no unique protected evidence | delete current-tree descriptor |
| EXACT_RETAINED message | runtime.message | exact accepted text | exact consumers | Step 5.11 compaction only | not Step-5.13 deletion candidate |
| COMPACTED message envelope | runtime.message provenance | stable source identity/cursor/digest | Interaction, Story coverage, disclosure, history refs | all dereference/content/cursor consumers discharged or migrated | current-tree retirement; opaque ID may survive in provenance-only refs if contract permits |
| Story current records | Story layer | noncanonical presentation | crossrefs, availability, current indexes | only via correction/retention policy | owner-specific Story maintenance |
| obsolete Story index generation | derivative Story metadata | retrieval/catch-up | current layer coverage/migration | successor durable + no compatibility dependency | delete generation |
| chronology canonical relation evidence | chronology evidence | protected predicates/provenance | temporal/causal consumers | Step-5.9 compaction eligibility | compact/remove only under protected-consumer proof |
| chronology derivative index/frontier | derivative | bounded lookup | rebuilding/correctness routing contract | successor/rebuild basis valid | remove/rebuild independently of source evidence |
| ACTIVE live ref | live authority | current mutable source | current routing/claims | none | forbidden |
| CLOSED_UNABSORBED live ref | live authority | current truth awaiting absorption | recovery/absorption | none | forbidden |
| absorbed old live ref | nonauthority transport leftover | historical transport access | diagnostic/source refs if any | campaign proves exact final head absorbed and no retrieval dependency | ref delete if capability exists; otherwise harmless leftover |
| never-routed orphan live ref | nonauthority candidate | failed opening/preparation | none except repair diagnostics | current campaign routing/history proves never selected | ref delete if capability exists |
| prepared losing Git commit/tree/blob | Git object DB, nonauthority | failed publication preparation | none once no ref selects it | ref selection failed/other authority current | no HDM per-object delete; host GC only |
| derived cleanup candidate index | maintenance projection | bounded discovery | none semantically | replace/rebuild freely | current-generation management |

This matrix remains a research draft; exact owner-specific deletion contracts require candidate/adversarial refinement.

---

# 12. Detailed findings by artifact family

## 12.1 Runtime command / Resolution / Continuation

The safe baseline should **not** delete an entire execution chain merely because root command reached SETTLED.

Separate:

```text
active execution payload
compact idempotency/result evidence
semantic/mechanical history
full diagnostic trace
```

Likely retention shape:

- active/suspended records protected;
- after terminality, detailed working payload becomes eligible for compaction;
- fixed outputs still referenced by later mechanics remain retained/promoted;
- compact immutable receipt/fingerprint may survive longer for idempotent duplicate suppression;
- pure diagnostic trace may be removed earliest;
- eventual removal of compact command/receipt identity requires proof that no accepted external retry/history contract still needs dereferenceability.

A generic “delete all settled commands” rule is unsafe.

## 12.2 MechanicalEvent / receipt / trace

Step 3 already gives a strong example of representation reduction: Effect recency lives on the Effect episode so old trace detail can compact without altering arbitration.

Therefore GC should encourage **natural-owner promotion of surviving mechanics evidence** before detailed history retirement.

MechanicalEvent identity may remain as opaque causal provenance after body deletion only if every remaining ref contract explicitly permits non-dereferenceable provenance identity.

If later chronology/semantic history requires event content, body cannot disappear until that meaning is independently retained.

## 12.3 Checkpoints

Checkpoint cleanup appears simpler than current runtime prose suggests because checkpoint is optional.

Recommended semantic distinction:

```text
SELECTED CHECKPOINT
    target of last_checkpoint_id
    retained by checkpoint-facility pointer

UNSELECTED CHECKPOINT
    no current checkpoint pointer
    candidate for deletion when no explicit diagnostic/repair/audit dependency exists
```

No minimum number of old checkpoints is required by current canonical recovery architecture.

The selected checkpoint can also be removed only by a coherent facility transition that clears/replaces the pointer and does not strand an explicitly requested maintenance operation.

No age TTL is needed.

## 12.4 Message envelopes

A COMPACTED message envelope may still carry several distinct values:

- stable ID;
- Interaction link;
- digest;
- source enumeration position;
- provenance metadata;
- Story exact-verification support;
- disclosure/history refs.

Therefore 5.13 should allow **field-level survivor migration** before whole-record deletion.

Example:

```text
Story coverage requires enumeration anchor
but no consumer needs full message envelope

-> preserve/migrate compact source enumeration anchor
-> update compatible coverage basis if needed
-> then envelope can retire
```

Opaque historical IDs do not require tombstone records when:

- IDs are never reused;
- ref contract treats the ID as provenance label only;
- dereferenceability is explicitly not promised.

This avoids universal tombstone accumulation.

## 12.5 Story

Story is noncanonical, so current presentation records may be corrected/regenerated without gameplay authority effects.

However cleanup must preserve:

- current output/index cross-reference closure;
- current layer allocator non-reuse state;
- compatible coverage basis;
- required verified-exact archival copies;
- availability/spoiler metadata needed by retained Story.

Old projection-contract generations may become bulk-retirement candidates after explicit compatible migration, but there is no global Story-history retention promise requiring every editorial version to survive.

## 12.6 Chronology

Chronology is the clearest example where generic reachability is insufficient.

A relation can be “old” and still protect:

- due evaluation;
- causal provenance;
- future current owner predicate;
- bounded cross-scope reconciliation.

Thus chronology cleanup delegates semantic eligibility entirely to Step-5.9 protected-consumer laws.

Step 5.13 adds only:

- candidate discovery;
- coherent survivor/index updates;
- deletion transaction/failure semantics.

## 12.7 Live refs

Four classes matter:

```text
ACTIVE
    ref deletion forbidden

CLOSED_UNABSORBED
    ref deletion forbidden; still current truth/recovery source

CLOSED_ABSORBED
    non-authoritative; eligible only after no retained retrieval dependency

ORPHAN_NEVER_SELECTED
    non-authoritative from birth; eligible after bounded campaign-routing proof
```

Deletion of a live ref must never be the action that establishes nonauthority.

If current deployment lacks ref-delete capability:

- mark/classify as non-authoritative leftover;
- ignore it for current routing;
- do not block gameplay;
- optionally report in maintenance diagnostics;
- remove later only when an authorized RepositoryPort offers ref deletion.

## 12.8 Prepared Git objects

Prepared losing/unselected Git objects are not campaign artifacts in the same sense as files/records.

The deterministic core only needs to know:

```text
not selected by current authority ref
```

It does not need a durable “orphan commit registry” solely for eventual host GC.

Creating such a registry would perversely turn unreachable implementation leftovers into new reachable metadata.

Recommendation:

> no baseline prepared-object cleanup ledger.

At most bounded diagnostics may report known prepared SHA from an in-flight/failed operation while available.

---

# 13. Alternatives evaluation

Scoring is qualitative because no measured campaign-size workload exists yet.

| Alternative | Safety | Boundedness | Authority cleanliness | Concurrency | Operational complexity | Storage cleanup effectiveness | Verdict |
|---|---|---|---|---|---|---|---|
| A generic mark/sweep | potentially high if perfect | poor/scan-heavy | poor; duplicates semantics | difficult across native domains | high | high in current tree | reject baseline |
| B generic refcounts | fragile under missing deps/cycles | good reads | poor; count becomes destructive authority | high update burden | high | high | reject baseline |
| C owner-local guards only | high | potentially uneven | excellent | good when local | low | moderate | viable simplest |
| D generation/epoch retirement | high only in native generational domains | excellent | good | good | low | high for eligible families | useful specialization only |
| E owner-gated hybrid + derivative candidates | high | high | good if indexes remain derivative | high with frozen footprint | moderate | high for current namespace | **recommended** |
| F retain almost everything | safe | simple | clean | easy | low | poor | control / insufficient for Step 5.13 |

## Why not C-only?

C-only is the strongest simpler alternative.

It is attractive because semantics remain entirely with owners.

However some long-lived target kinds need efficient *negative* blocker proof and bounded candidate discovery. Without derivative typed routing/index support, C-only eventually tends toward directory/history scans.

Therefore the recommendation is E, but with a strict rule:

> Add derivative maintenance/protection indexes only for concrete owner families that cannot otherwise provide bounded proof; do not create one universal GC graph.

---

# 14. Assumption & Evidence Ledger

## A1 — current campaign Git history remains append-only

Confidence: **HIGH**

Evidence:

- canonical Step 5.6 non-force single-parent publication;
- no-force-push project invariant;
- Step 5.8 forward absorption.

Impact if false:

History-rewrite cleanup could reclaim reachable old blobs but would fundamentally change authority/recovery/commit identity assumptions.

Revisit trigger:

Explicit future owner decision to support history rewrite / storage migration.

## A2 — normal file deletion cannot reclaim old reachable Git blobs

Confidence: **HIGH**

Evidence:

- Git object reachability model;
- GitHub deletion docs explicitly state deleted files remain in Git history.

Impact if false:

Repository-size conclusions would change, but current-tree safe-delete architecture would remain mostly valid.

Revisit trigger:

Migration to non-Git content-addressed storage with different retention semantics.

## A3 — current Connector lacks ref deletion

Confidence: **HIGH for current session/tool surface**

Evidence:

- Connector resource discovery exposes only `delete_file` under delete tools;
- ref tools expose update/create but not delete.

Impact if false later:

Old live refs can be physically removed immediately through RepositoryPort; semantic eligibility does not change.

Revisit trigger:

Step-6/current deployment tool discovery.

## A4 — opaque provenance IDs may survive without dereferenceable records for selected contracts

Confidence: **MEDIUM-HIGH**

Evidence:

- Step 5.10 source refs do not promise full payload dereferenceability;
- Step 5.11 provenance may outlive prose;
- stable IDs are never reused/repurposed.

Impact if false for a specific ref class:

That target requires a compact retained anchor/tombstone or referrer migration before record deletion.

Verification:

Machine cleanup contract per owner/ref type must state whether dereferenceability is required.

## A5 — no universal tombstone class is needed

Confidence: **MEDIUM-HIGH**

Evidence:

Most survivors can live in natural owner, compact envelope, coverage anchor or opaque stable identity.

Impact if false:

A narrow tombstone/identity-anchor class may be justified for a concrete record family; generic tombstone still not automatically justified.

Revisit trigger:

Adversarial case where required stable dereferenceable identity survives but no natural compact owner can retain it.

## A6 — cleanup does not need background execution

Confidence: **HIGH**

Evidence:

No correctness state requires cleanup for ordinary gameplay; old artifacts are over-retention, not missing authority.

Impact if false:

Storage/platform caps could require a stronger maintenance edge but would be a product/deployment decision.

Revisit trigger:

Measured repository growth approaches practical platform limits or materially harms latency.

## A7 — derivative candidate indexes can be incomplete safely

Confidence: **HIGH**

Evidence:

Candidates do not authorize deletion; every selected item is revalidated.

Impact if false:

Only cleanup efficiency changes; not semantic safety if deletion proof remains independent.

---

# 15. Open technical questions for challenge/candidate

No current item requires a human product decision, but several technical issues need explicit resolution:

1. How to formalize a target-kind cleanup contract without creating a new runtime class for every record?
2. What exact “negative proof currentness” is required for derived protection indexes?
3. How to synchronize cleanup with a blocker that can be born in an independently writable live source?
4. Which Step-3 artifacts need compact idempotency anchors and for how long?
5. May a `runtime.message` ID remain as a non-dereferenceable provenance token indefinitely after envelope removal?
6. When a verified exact Story copy survives, is its source digest/provenance sufficient if the source envelope itself is removed? Likely yes only if digest/source identity is migrated into a durable verification anchor.
7. Does checkpoint facility retain the currently selected checkpoint by default even though gameplay recovery does not require it? Recommendation: yes as long as `last_checkpoint_id` points to it; clearing/replacing pointer is the explicit facility retirement edge.
8. What exact bounded evidence proves an orphan live branch was never selected as authority?
9. How should current Connector lack of ref deletion be represented operationally? Recommendation: typed `CLEANUP_DEFERRED_CAPABILITY`/equivalent maintenance result, not canon defect.
10. Should current-tree cleanup ever attempt to optimize repository object-store size? Recommendation: no; only measurement/prevention because reachable history is immutable baseline.

---

# 16. Recommendation

Recommended direction:

> **OWNER-GATED RETIREMENT / CLOSED CLEANUP CONTRACTS / DERIVATIVE CANDIDATE DISCOVERY / CURRENT-BASIS BLOCKER PROOF / REPLACEMENT-BEFORE-REMOVAL / OPTIONAL REF CLEANUP / HOST-MANAGED GIT OBJECT GC**

Core principles:

```text
NO owner terminality -> no retirement
NO closed blocker contract -> no automatic deletion
NO current negative proof -> retain
NO survivor closure -> retain
NO compatible current basis -> retry/revalidate
NO ref-delete capability -> leave harmless non-authoritative ref
NO Git-host object-delete capability -> do not pretend to reclaim objects
```

Confidence: **HIGH** on rejecting universal mark/sweep/refcount authority and on current-tree/history separation.

Confidence: **MEDIUM-HIGH** on exact machine shape of cleanup contracts and compact idempotency/provenance anchors; adversarial review must pressure these before canonicalization.

---

# 17. Strongest counterargument

The strongest argument against the recommendation is that a single universal mark/sweep graph would be easier to reason about as the repository grows: treat all persistent refs as edges, all current roots as marks and delete unreachable nodes.

Why it currently loses:

1. many HDM dependencies are semantic, not ordinary structural refs (chronology feasible-set precision, exact-text requirement, pending temporal obligation, Story coverage compatibility);
2. roots are spread across independent current native domains and not globally comparable;
3. a universal scanner would duplicate owner lifecycle knowledge and create campaign-wide maintenance cost;
4. negative correctness would still depend on perfect graph enrollment, effectively making the graph a second authority;
5. Git object reachability is not the same as HDM semantic reachability anyway.

What would change the recommendation:

- a future storage engine where all admitted persistent dependencies are generated from one formally complete typed schema graph;
- measured evidence that owner-specific indexes/guards become unmaintainably fragmented;
- a requirement for aggressive storage reclamation that cannot be satisfied through current owner-local compaction.

None is established today.

---

# 18. No human decision currently required

Research has not found a need to weaken any existing product promise or accept a new material risk.

The append-only Git-history limitation is an inherited platform/architecture fact, not a newly chosen Step-5.13 retention policy. Ordinary 5.13 cannot safely “fix” it without violating already canonical no-force/history-stability laws.

The correct next step is therefore mechanical analytical challenge of the recommended owner-gated hybrid, not an owner decision brief.

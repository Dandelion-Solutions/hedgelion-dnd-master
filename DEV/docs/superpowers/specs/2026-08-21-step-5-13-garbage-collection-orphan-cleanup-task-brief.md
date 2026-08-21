# Step 5.13 — Garbage Collection / Orphan Cleanup — Architecture Task Brief

Status: **APPROVED TASK BRIEF — ARCHITECTURAL RESEARCH NOT YET CANONICAL**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Pre-5.13 verified branch HEAD:

`71d9e2ad0bd2568991498d0d71a9da6d7525a1f6`

Classification: **ARCHITECTURAL / DEEP-WORK**

Human/agent responsibility boundary:

- The owner has explicitly delegated the mechanical architecture of Step 5.13 to the agent.
- The agent owns research, alternatives, challenge, recommendation, formalization, adversarial review, resolution, canonical specification, debt/test mapping and roadmap bookkeeping.
- Escalate only if the investigation exposes a genuinely new product promise, material irreversible retention trade-off, canonical authority change, or other decision reserved to the human architect by `DEV/DESIGN_PROCESS.md`.
- Do not escalate ordinary safe-delete mechanics, routing/index representation, maintenance ordering, failure handling or storage cleanup details when they follow from already accepted Steps 4 and 5.1–5.12.

Governing process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- `DEV/PROJECT_MAP.md`
- `AGENTS.md`

---

# 1. Problem statement

Steps 5.2–5.12 intentionally accumulate durable owners, historical evidence, routing/index metadata, exact-text envelopes, Story projection state, chronology evidence, live-epoch artifacts and transport leftovers because correctness is biased toward retaining evidence until replacement/retirement is proven.

Step 5.13 must define when those physical artifacts may be compacted, retired or removed **without inventing a new universal ownership system and without damaging any existing correctness promise**.

The problem is not simply “delete old files.” It is to establish a bounded, deterministic proof of the form:

```text
artifact A is currently removable
    iff
all owner-specific semantic/recovery/retention obligations that can lawfully require A
are absent, discharged, replaced, or independently satisfied
under one coherent current authority basis.
```

Deletion is irreversible at the HDM semantic layer even when a hosting platform may temporarily retain historical Git objects. Therefore false-positive deletion is materially more dangerous than false-negative retention.

The architecture must prefer:

```text
uncertain eligibility -> retain
```

over guessing that absence of a discovered reference proves absence of a dependency.

At the same time, Step 5.13 must not solve safety by preserving everything forever or by introducing campaign-wide graph scans on ordinary gameplay paths.

---

# 2. Critical framing challenge

Do **not** assume the answer is a generic garbage collector.

The investigation must remain capable of concluding that the correct baseline is instead:

- owner-local retirement rules;
- typed bounded protection routing;
- maintenance-time candidate enumeration;
- safe-delete proofs constructed from existing owners;
- a small hybrid of those mechanisms;
- or another simpler model.

The task must reject any design that creates a new semantic authority merely to answer “can I delete this?” when the underlying owner contracts already contain the necessary lifecycle/dependency facts.

Explicit framing questions:

1. Is “GC” one subsystem, or only a maintenance composition of owner-specific retirement contracts?
2. Does any proposed generic retention root/index duplicate Step-5.2 routing, Step-5.9 chronology dependency routing, Step-5.10 projection coverage, Step-5.11 exact-text protection or normal reference ownership?
3. Can safe deletion be proved with bounded local/typed evidence, or does the design silently require an all-campaign mark-and-sweep traversal?
4. Is deletion eligibility semantic, while maintenance scheduling/age/storage pressure is merely candidate selection?
5. Does the design confuse path deletion, ref deletion and host-managed Git object reclamation?

If a competent investigation could follow this brief and accidentally optimize repository size while breaking recovery, chronology, Story, disclosure or exact-text promises, the framing is insufficient and must be tightened before canonicalization.

---

# 3. Inherited canonical laws that 5.13 must not weaken

## 3.1 Step 5.1 — typed domains, no universal frontier

No generic scalar GC frontier, global history watermark, cross-domain “oldest needed event” or universal comparable revision may be invented.

Independent owner domains may have independent retirement/coverage bases.

## 3.2 Steps 5.2 / 5.7 — current native recovery closure

Deletion must not strand:

- independently recovery-relevant active owners;
- required recovery routing;
- transitive correctness dependencies;
- accepted interpretation/version dependencies;
- current source-selection/routing evidence;
- fixed accepted RNG or mandatory execution continuity;
- any source required to prove Resumable Runtime Closure.

Checkpoints are optional evidence, never alternate current authority.

## 3.3 Step 5.3 — pending obligations

No cleanup may remove the only evidence of:

- armed temporal obligation;
- accepted occurrence identity;
- pending child/firing identity;
- suspended Choice/Reaction;
- unfinished execution;
- contingent `CLAIMED(G,F)` closure;
- fixed accepted random experiment.

Derived Temporal Agenda/index material may rebuild; owner/execution evidence may not be removed early.

## 3.4 Step 5.4 — host loss/handoff

Cleanup cannot make a previously promised recovery-safe handoff no longer recoverable.

Unpublished volatile state is never reconstructed from deleted history.

## 3.5 Steps 5.5 / 5.6 — durability/publication

Deletion/compaction is itself a semantic mutation and follows normal owning durability/publication rules.

Within one campaign publication domain:

```text
safe-delete proof
-> complete normalized delete/update delta
-> resulting-tree validation
-> one single-parent commit
-> non-force ref transition
```

Ambiguous publication outcome is not permission to assume deletion succeeded.

Failure ordering must bias toward temporary redundancy rather than premature irreversible removal.

Prepared but unselected Git objects are non-authoritative.

## 3.6 Step 5.8 — live ownership

Cleanup must preserve:

- selected/current live routing;
- ACTIVE and CLOSED_UNABSORBED live source authority;
- exact final closed live revision until absorption proof no longer needs it;
- live-born stable IDs and provenance after absorption;
- current source freeze/transfer evidence where still required.

A live ref/branch may be removed only after it is provably non-authoritative and no retained consumer requires that ref/source as a retrieval dependency.

## 3.7 Step 5.9 — chronology

Cleanup must preserve every still-protected temporal/causal predicate’s bounded decidability or feasible relation set.

Do not remove:

- unique causal provenance;
- required typed precedence evidence;
- required same-coordinate/elapsed evidence;
- metric precision needed by a protected consumer;
- late-relation evidence still required by bounded routing;
- chronology anchors whose semantic identity remains referenced unless the referencing contract tolerates an independently preserved compact identity/evidence representation.

No campaign-wide temporal CSP is introduced solely for GC.

## 3.8 Step 5.10 — Story projection

Cleanup must not strand a layer’s source enumeration/coverage semantics.

A source item may disappear only when its layer-specific `MUST_MATERIALIZE` obligations have been satisfied or lawfully ended and future catch-up can still interpret the compatible source-domain coverage basis.

Story lag never blocks gameplay except where a separate retention rule explicitly protects a source until required projection materialization.

Story indexes/generations are non-authoritative and may be rebuilt/retired only when current layer output/coverage remains coherent.

## 3.9 Step 5.11 — Selective Exact / semantic continuity

`runtime.message` exact payload may be compacted only after:

- exact-text protection is discharged or independently satisfied;
- semantic consumers are content-sufficient;
- required Story exact archive materialization is complete when applicable;
- source enumeration identity remains interpretable.

The compact message envelope remains stable historical/provenance identity until Step 5.13 proves physical removal is safe.

A digest does not recreate deleted text.

## 3.10 Step 5.12 — outbound/disclosure

Cleanup must preserve established sparse `runtime.disclosure` meaning and outbound message/provenance dependencies that remain useful under Step-4/5.11 contracts.

There is no baseline delivery outbox, chunk ledger, delayed-delivery reconciliation queue or per-response ACK state machine to garbage-collect.

Interrupted/Retry/edit presentation anomalies are not a reason to invent GC machinery.

---

# 4. Scope

5.13 owns **semantic eligibility and safe physical removal/retirement of obsolete runtime/storage artifacts** after their native owner contracts permit it.

Required artifact families to investigate:

## 4.1 Operational runtime artifacts

- settled `runtime.command` records where history/idempotency/audit requirements permit retirement;
- terminal `runtime.resolution` records;
- consumed/obsolete `runtime.continuation` generations;
- resolved pending-child descriptors;
- resolved receipts and execution fragments;
- `runtime.resolution_trace` detail that is diagnostic/derived rather than unique semantic evidence;
- terminal Procedure-support artifacts where Procedure owner/lifecycle no longer requires them;
- obsolete recovery-routing memberships/index generations.

The investigation must distinguish:

```text
owner retired
record can compact
record can physically delete
ID/provenance may still be referenced
```

These are not automatically the same event.

## 4.2 Checkpoints

Investigate:

- current `MANIFEST.last_checkpoint_id` pointer semantics;
- historical checkpoint value for diagnostics/repair;
- dangling optional checkpoint pointers;
- superseded checkpoint retention;
- deletion of checkpoint descriptors whose unique evidence is no longer protected;
- whether checkpoint IDs may remain referenced by audit/provenance after descriptor deletion;
- bounded selection of cleanup candidates without scanning arbitrary history.

No age alone may prove deletion safety.

## 4.3 Messages / transcript source envelopes

Investigate physical deletion of `runtime.message` **COMPACTED** envelopes after 5.11 semantic/exact compaction.

Preserve as needed:

- accepted Interaction linkage;
- semantic event/provenance source refs;
- Story source/coverage identity;
- disclosure source refs;
- audit/correction refs;
- exact-archive verification refs;
- live-source absorption identity.

Determine whether stable “source identity survives forever” is actually required for any classes or whether some refs may lawfully collapse/promote to owner-local provenance summaries before envelope deletion.

Do not weaken the S / semantic-continuity product promise.

## 4.4 Story artifacts

Investigate:

- superseded/corrected Story records;
- obsolete layer indexes;
- old projection-contract generations after migration;
- stale allocator/index snapshots;
- invalidated verified-exact presentation copies;
- projection source routing after source retirement;
- whether editorial history is retained, compacted or dropped when no owner contract promises it.

Story remains noncanonical; deletion of Story must not rewrite gameplay truth.

## 4.5 Chronology artifacts

Investigate:

- relation evidence no longer required by any protected consumer;
- derivative endpoint indexes/frontiers;
- superseded/rebased metric evidence;
- elapsed evidence whose final consumer has ended;
- relation bridge retention after scopes retire;
- safe summaries/reductions that preserve the exact admitted predicate answers/feasible sets.

Do not introduce global graph mark/sweep or all-history relation reconstruction.

## 4.6 Live refs / branches

Investigate lifecycle classes at least:

```text
ACTIVE
CLOSED_UNABSORBED
CLOSED_ABSORBED / NONAUTHORITATIVE LEFTOVER
ORPHAN NEVER ROUTED AS AUTHORITY
```

For each, define:

- whether deletion is forbidden/permitted;
- what current campaign routing/evidence must prove;
- what bounded verification is required before ref deletion;
- how concurrent/stale hosts are fenced;
- what happens if branch deletion capability is unavailable;
- whether branch absence after confirmed absorption is healthy;
- whether a dangling orphan branch may ever be adopted implicitly (expected answer should be challenged, not assumed).

Deletion of a live branch must never serve as the event that makes it non-authoritative. Authority must already have moved/ended under Step 5.8.

## 4.7 Prepared/unreachable Git objects and transport leftovers

Investigate Git/GitHub reality separately from HDM semantic cleanup:

- prepared blob/tree/commit objects created before failed ref selection;
- prepared commits rejected by optimistic concurrency;
- unreachable objects after branch deletion;
- whether GitHub exposes any supported per-object deletion/GC control;
- whether HDM can only stop referencing such objects and leave actual object reclamation to host Git maintenance;
- what, if anything, support tooling may observe/report without promising physical reclamation.

HDM must not claim deletion of a Git object unless the supported platform contract actually provides that operation and confirms it.

## 4.8 Indexes / routing / compact summaries

Investigate replacement/retirement of:

- derived reverse indexes;
- recovery routing memberships;
- exact-text protection indexes;
- chronology dependency indexes;
- Story indexes;
- stale generations of rebuildable routing metadata.

Derived indexes must not be retained forever merely because deletion proof itself relies on the stale index.

Forward/native owner dependencies remain semantic authority.

---

# 5. Explicit non-goals

Step 5.13 SHALL NOT:

- change gameplay semantics;
- revise the Step-5.11 memory/retention product promise;
- invent a universal history TTL;
- introduce a generic campaign-global reference counter;
- introduce a campaign-global mark-and-sweep graph unless evidence proves no bounded owner-specific alternative can satisfy current needs;
- run cleanup on every gameplay turn;
- require a background worker;
- require Work/Pro/Enterprise features;
- make Story or checkpoint authority;
- change Step-5.8 authority-transfer semantics;
- define a new global chronology frontier;
- force-delete Git history or refs to “save space” while they remain authoritative/protected;
- rewrite repository history;
- use force push;
- promise server-side Git object reclamation that GitHub does not expose as an HDM-controlled semantic operation;
- solve account-level retention/privacy policy beyond campaign-artifact ownership;
- perform broad implementation; GAME/schema/test realization remains later work;
- begin Step 5.14 before 5.13 closes.

---

# 6. Quality attributes / fitness criteria

Alternatives must be evaluated against at least:

1. **Safety / correctness** — false-positive deletion must be structurally prevented.
2. **Boundedness** — ordinary eligibility checks and maintenance candidate processing must avoid full campaign scans where owner-specific routing can bound work.
3. **No duplicate authority** — cleanup metadata cannot become another owner of lifecycle/current truth.
4. **Crash consistency** — failure cannot leave replacement evidence absent while source is already gone.
5. **Concurrency safety** — stale maintenance cannot delete evidence newly depended upon by current authority.
6. **Recoverability** — all promised RRC paths remain valid after cleanup.
7. **Chronology fidelity** — required temporal/causal predicates remain answerable with their promised precision/uncertainty.
8. **Projection continuity** — Story catch-up and source cursor interpretation remain valid.
9. **Selective Exact correctness** — exact/source provenance is not deleted before its consumers discharge.
10. **Operational simplicity** — no routine background service or per-turn GC burden.
11. **Storage boundedness** — the architecture must provide actual paths for obsolete material to become deletable rather than merely declaring retention safer.
12. **Observability / repairability** — cleanup decisions and failures can be diagnosed without making a cleanup log current authority.
13. **Reversibility where possible** — prefer compact/retire before physical delete when evidence is still uncertain.
14. **YAGNI** — do not build a generic tracing garbage collector for hypothetical future record kinds.
15. **Transport realism** — distinguish what the current GitHub/RepositoryPort can actually delete from what Git hosting manages internally.

No arbitrary numerical retention thresholds should be invented unless the project already owns them.

---

# 7. Required repository research

Inspect current owners and stale runtime surfaces, at minimum:

## Process / roadmap

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- `DEV/PROJECT_MAP.md`
- `AGENTS.md`
- Step-5 expanded architecture agenda

## Canonical Step-5 contracts

Read relevant sections of:

- Step 5.2 Resumable Runtime Closure v2
- Step 5.3 temporal/pending continuity
- Step 5.4 host lifecycle
- Step 5.5 durability
- Step 5.6 publication/crash consistency
- Step 5.7 checkpoint/recovery
- Step 5.8 live-epoch ownership
- Step 5.9 chronology persistence/reconciliation
- Step 5.10 Story projection durability
- Step 5.11 transcript/history compaction
- Step 5.12 host delivery/disclosure

## Runtime/storage surfaces

- `GAME/CORE/STORAGE.md`
- `GAME/CORE/PERSISTENCE.md`
- `GAME/CORE/SESSION.md`
- `GAME/CORE/INTEGRITY.md`
- `GAME/CORE/LIVE_SCENE.md`
- `GAME/CORE/MULTIPLAYER.md`
- `GAME/CORE/CHRONOLOGY.md`
- any current maintenance/cleanup support contracts

## Machine/catalog/schema surfaces

Inventory currently realized:

- runtime record kinds;
- ID policies;
- checkpoint/current/session/live schemas;
- message/disclosure/story gaps/debt;
- tests/case catalogs touching retention, cleanup, checkpoints, live branches, prepared objects, recovery or compaction.

An empty keyword search is not evidence of absence until relevant directories/owners are structurally inspected.

---

# 8. Required external / platform research

Use primary sources.

At minimum establish:

## Git / GitHub

- distinction between deleting a ref and reclaiming unreachable objects;
- supported GitHub API semantics for branch/ref deletion;
- whether GitHub exposes deletion of arbitrary Git commit/tree/blob objects;
- reachability implications of branches/tags/refs;
- concurrency implications of pruning/unreachable-object GC in Git generally;
- what HDM can legitimately guarantee after it deletes a branch/ref versus what remains host-managed.

Do not import local `git gc` implementation policy directly into GitHub-hosted semantics without evidence.

## Connector / RepositoryPort capability

Determine whether the currently connected GitHub transport exposes the operations needed for:

- exact ref reads;
- branch/ref deletion;
- non-force authority updates;
- exact path deletion through campaign-tree transaction construction;
- bounded compare/lineage verification.

A missing current Connector operation is a deployment/tooling gap, not permission to use native Git/CLI/private HTTP fallback.

---

# 9. Alternative families that MUST be compared

Research must compare at least these architecture families rather than jumping directly to one design.

## A — Generic mark-and-sweep retention graph

All protected roots are marked; references are traversed; unreachable artifacts are swept.

Challenge:

- campaign-wide scans;
- generic graph authority;
- duplicate knowledge of owner semantics;
- performance;
- heterogeneous non-comparable domains.

## B — Generic durable reference counts

Artifacts carry/inherit counts of live references.

Challenge:

- updates under concurrency;
- missing semantic dependencies that are not ordinary refs;
- cycles;
- stale count corruption becoming destructive;
- duplicate authority.

## C — Owner-local terminality + bounded typed protection routing

Each owner defines when its evidence may retire; cleanup candidates use bounded typed dependency/protection routes.

Challenge:

- completeness of dependency registration;
- how indexes themselves retire;
- cross-owner bridge cases;
- whether maintenance becomes too fragmented.

## D — Generation/epoch bulk retirement

Whole generations/epochs/checkpoint families/Story index generations become removable when a later generation proves complete supersession.

Challenge:

- sparse survivors crossing generation boundaries;
- over-retention;
- false total-order assumptions;
- live/chronology independence.

## E — Layered hybrid

Owner-local eligibility as semantic authority + derivative typed maintenance indexes for bounded candidate discovery + generation-level bulk retirement only where a native domain proves it.

Challenge it against the simplest viable C-only design; do not add indexes merely for elegance.

## F — Retain almost everything / manual cleanup only

Use as a control alternative.

Evaluate repository growth, privacy/storage burden, operational complexity avoided, and whether it violates the explicit purpose of Step 5.13 by failing to provide lawful cleanup.

---

# 10. Required semantic model questions

The research/draft must answer at least:

1. What exact fact makes an artifact semantically eligible for physical removal?
2. Is there one generic eligibility predicate or only owner-family predicates with a common proof shape?
3. What counts as a protected consumer?
4. How are protection-bearing dependencies registered/discovered without all-history scans?
5. How is the absence of a dependency proven safely enough to allow irreversible deletion?
6. Can a derived reverse index ever authorize deletion by itself?
7. What freshness/coherence basis must a delete proof pin?
8. What happens if a new dependency is created concurrently with cleanup?
9. What deletion/replacement changes must publish atomically in one campaign transaction?
10. When is two-phase “replacement first, delete later” mandatory/preferred?
11. What minimum provenance identity must survive after source payload/record deletion?
12. Can refs to deleted records remain as historical tombstone-like identity, or must referrers be rewritten/promoted before deletion?
13. Do we need tombstones? For which owner kinds, if any? Challenge YAGNI.
14. How are deleted/retired stable IDs prevented from accidental reuse?
15. How do Step-5.10 source coverage cursors survive old-source deletion?
16. How do Step-5.9 chronology consumers retain exact/bounded predicates after relation-evidence reduction?
17. How does checkpoint deletion interact with `last_checkpoint_id`, maintenance exports and diagnostics?
18. When may a compacted `runtime.message` envelope disappear completely?
19. When may Story records/index generations disappear?
20. When may a closed/absorbed live branch ref be deleted?
21. When may an orphan never-selected live branch ref be deleted?
22. What proof prevents deletion of a live ref still being used by a stale host as current authority?
23. What can HDM do about prepared unreachable commits/trees/blobs?
24. Does repository history itself remain a valid provenance source after path deletion, and may runtime correctness depend on broad Git-history access? Expected answer must be derived, not assumed.
25. What maintenance schedule is sufficient without background work?
26. How are partial cleanup failures resumed idempotently?
27. What does a dry-run/audit report need to expose for support without becoming authority?
28. How are legacy campaigns migrated when current records lack new cleanup/protection metadata?
29. What cleanup actions are forbidden automatically and require explicit repair/owner intervention?
30. Which deletion classes must be deferred entirely because the necessary physical capability is unavailable?

---

# 11. Failure and concurrency scenarios that MUST be attacked

At minimum:

1. deletion candidate selected, then a new canonical owner starts referencing it before publication;
2. replacement summary created but source deletion publication loses ACK;
3. source deletion succeeds but local process thinks it failed;
4. source replacement fails but delete was prepared;
5. derived reverse index is stale and omits a live exact-text consumer;
6. checkpoint selected for cleanup while a support/export operation is reading it;
7. checkpoint deleted but `last_checkpoint_id` still points to it;
8. Continuation generation considered obsolete while a Resolution still references it;
9. settled RuntimeCommand needed for idempotent retry/audit;
10. receipt/traces have overlapping but nonidentical evidentiary responsibilities;
11. chronology bridge appears “old” but still resolves an armed temporal predicate;
12. chronology relation can be summarized but summary loses uncertainty precision;
13. Story layer coverage has passed a source but another projection-contract generation still needs migration/reprojection;
14. `MUST_MATERIALIZE` Transcript source is deleted early;
15. compacted message envelope is sole remaining provenance route for a knowledge/disclosure/history record;
16. verified Story Transcript is sole exact textual copy but source identity/digest envelope is removed;
17. live epoch closes, branch deletion races campaign absorption;
18. closed absorbed live branch remains referenced by a diagnostic/history record;
19. stale host still caches deleted live ref;
20. orphan live branch exists but no campaign route ever selected it;
21. concurrent branch creation reuses an orphan-like deterministic name;
22. prepared campaign commit loses ref race and remains unreachable;
23. cleanup tries to delete unreachable Git object directly but platform offers no operation;
24. maintenance is interrupted after removing some independent candidates;
25. cleanup task runs twice;
26. cleanup candidate set spans campaign + several live domains;
27. external branch/ref movement occurs during maintenance;
28. legacy campaign has missing protection-routing metadata;
29. index generation is removed before the replacement generation is durable;
30. a “delete all older than X” optimization would delete a still-protected record;
31. thousands/millions of terminal historical artifacts exist and candidate discovery must remain operationally bounded/batchable;
32. no cleanup candidates exist: maintenance must produce no heartbeat/write.

---

# 12. Performance / operational constraints

Baseline HDM has no background worker requirement.

Ordinary gameplay SHALL NOT perform:

- full campaign mark-and-sweep;
- all-history reference scans;
- Git object enumeration;
- ref-list scans merely to answer ordinary mechanics;
- cleanup publication on every turn;
- Story catch-up solely because cleanup exists.

Cleanup may be:

- opportunistic at explicit/natural maintenance boundaries;
- user/admin initiated;
- batched;
- resumable across multiple maintenance invocations;
- skipped indefinitely without correctness loss when storage pressure is acceptable.

Candidate discovery should prefer bounded owner-native retirement indexes/partitions/generations where justified.

Age/storage pressure may prioritize already-safe candidates but must not establish semantic eligibility.

No numerical batch size/TTL is canonical unless evidence and product requirements demand one.

---

# 13. Expected research artifacts / design cycle

5.13 shall use the full deep-design chain:

1. this Task Brief;
2. Research Draft + Assumption/Evidence Ledger;
3. Analytical Challenge;
4. Candidate Specification;
5. Adversarial Review;
6. Resolution Gate;
7. Canonical Specification;
8. roadmap closure + machine-realization/test/debt carry-forward.

If a true human decision appears, insert a decision brief/owner-decision artifact before candidate canonicalization.

Do not manufacture a human decision merely because several implementation shapes are possible when one is mechanically preferable under inherited contracts.

---

# 14. Required research-draft deliverables

The Research Draft must include:

## 14.1 Verified facts

Separate repository facts, Git/GitHub/platform facts and current Connector capability facts.

## 14.2 Constraints / inherited decisions

List the exact Step-5 laws that constrain cleanup.

## 14.3 Assumption & Evidence Ledger

For every material uncertainty, record:

```text
Assumption
Confidence
Evidence
Impact if false
Verification / revisit trigger
```

## 14.4 Artifact responsibility matrix

At least:

| Artifact family | Native owner/source | Why it exists | What may still depend on it | Candidate retirement signal | Replacement/survivor evidence | Physical cleanup surface |
|---|---|---|---|---|---|---|

## 14.5 Alternative comparison matrix

Compare A–F using the quality attributes above.

## 14.6 Proposed common proof shape

If justified, formalize a generic *proof vocabulary* without creating a generic authority, e.g. concepts analogous to:

```text
NATIVE_TERMINALITY_PROOF
PROTECTED_DEPENDENCY_ABSENCE/REPLACEMENT_PROOF
REQUIRED_SURVIVOR_CLOSURE
CURRENT_AUTHORITY_BASIS
DELETE_DELTA
```

The exact names are research output, not preapproved schema classes.

## 14.7 Boundary map

Explicitly distinguish:

```text
SEMANTIC RETIREMENT
PAYLOAD COMPACTION
CAMPAIGN PATH DELETE
GIT REF DELETE
HOST-MANAGED UNREACHABLE OBJECT RECLAMATION
```

## 14.8 Recommendation

Provide one recommended architecture, strongest counterargument, confidence and what evidence would change it.

---

# 15. Analytical challenge requirements

Before candidate specification, attack the recommendation for:

- hidden universal GC authority;
- circular proof (“index says no refs; index can be deleted because no refs”);
- stale negative evidence;
- reference cycles;
- references that imply provenance only versus content/recovery dependency;
- owner lifecycle mismatch;
- cross-domain source movement;
- race between dependency creation and deletion;
- compaction creating a dependency on the artifact being deleted;
- delete-first failure ordering;
- all-history scan fallback;
- irreversible deletion where compact retirement would suffice;
- Git-history reliance masquerading as bounded current storage;
- unavailable ref deletion capability;
- unreachable object cleanup promises beyond HDM control;
- over-retention/YAGNI;
- under-retention/data loss;
- migration from current legacy/stale runtime schema.

Strongest simpler alternative must be evaluated explicitly.

---

# 16. Adversarial review gate

The adversarial reviewer must attempt to produce at least:

- one active-owner stranding bug;
- one recovery stranding bug;
- one temporal/chronology evidence loss bug;
- one Story catch-up loss bug;
- one Selective-Exact/provenance loss bug;
- one live-authority/ref race bug;
- one stale-index false deletion bug;
- one ambiguous-publication bug;
- one legacy-migration bug;
- one scalability/boundedness failure;
- one case where generic GC abstraction is unnecessary;
- one case where owner-local rules alone are insufficient and a derivative maintenance index is justified.

No canonicalization while any blocker lacks an explicit disposition.

---

# 17. Exit criteria

Step 5.13 may close only when the canonical architecture can prove all of the following:

1. no physical cleanup can itself redefine semantic authority;
2. deletion eligibility is based on owner/dependency contracts, never age alone;
3. active/pending/recoverable owners cannot be stranded;
4. required chronology predicates/provenance survive;
5. Story coverage/catch-up survives;
6. Selective-Exact and semantic-content guarantees survive;
7. established disclosure/message provenance survives where promised;
8. live refs are deleted only after authority has already moved/ended;
9. cleanup is race-safe against current-authority movement and new dependencies;
10. crash/ambiguous publication biases toward retention/retry rather than premature loss;
11. no generic global frontier/refcount/mark-sweep authority is introduced without demonstrated necessity;
12. ordinary gameplay carries no campaign-wide GC cost;
13. cleanup can be batched/resumed/idempotent;
14. host-managed Git object reclamation is not misrepresented as an HDM-controlled operation;
15. all unresolved machine/schema/tooling work is explicitly carried as implementation debt;
16. Step 5.14 receives a complete adversarial scenario set and no unresolved 5.13 architecture blocker.

Canonical exit statement target:

> **Every artifact HDM physically removes is already semantically retired under its native owner and has a bounded current proof that no protected consumer still requires the removed representation; cleanup may reclaim storage and routing clutter but can never be the operation that decides gameplay truth, obligation lifecycle, chronology, knowledge, disclosure or Story authority.**

---

# 18. Stop/escalation conditions

Stop and produce a human decision brief only if research shows that closing 5.13 requires a new choice such as:

- changing the Step-5.11 semantic-memory/verbatim-retention promise;
- intentionally deleting a class of evidence that a current canonical contract still promises;
- accepting materially weaker recovery/provenance guarantees to reduce storage;
- making cleanup mandatory on a user-visible latency path;
- introducing a new canonical owner/authority rather than derivative maintenance evidence;
- rewriting Git history or changing the no-force-push policy;
- another material irreversible product/risk trade-off not already decided.

Otherwise proceed mechanically through the full design cycle without asking the owner to validate derived specification detail.

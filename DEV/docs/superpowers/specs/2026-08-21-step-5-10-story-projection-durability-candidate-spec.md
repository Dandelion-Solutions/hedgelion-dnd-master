# Step 5.10 — Story Projection Durability — Candidate Specification

Status: **CANDIDATE — NOT CANONICAL / STEP 5.10 IN PROGRESS**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Derivation:

- `2026-08-21-step-5-10-story-projection-durability-task-brief.md`
- `2026-08-21-step-5-10-story-projection-durability-research-draft.md`
- `2026-08-21-step-5-10-story-projection-durability-analytical-challenge.md`

Candidate architecture direction:

> **LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL GENERATIVE CHRONICLER / GAMEPLAY-PRIORITY SAME-REF CAS**

This candidate preserves Step-4 Story semantics and Step-5 publication/recovery laws while remaining correct in a baseline ordinary sequential ChatGPT execution profile with no required background worker.

---

# 1. Central invariant

Story is a durable non-canonical projection whose progress can lag canonical/history sources without affecting gameplay authority.

For each Story layer:

```text
source authority
    remains in native canonical/history/transcript owner

projection coverage
    says which admitted source candidates have been considered

Story records/indexes
    are current non-canonical presentation output

Chronicler
    may propose generative/editorial content

Python/deterministic core
    owns source selection, validation, final Story ID allocation,
    coverage advancement and repository publication
```

Canonical gameplay publication never requires Story freshness.

---

# 2. Story layers remain semantically independent

The accepted layers remain:

```text
STORY/TRANSCRIPT
STORY/EVENTS
STORY/MECHANICS
STORY/NARRATIVE
```

Each layer owns only its projection-local:

- published Story records;
- layer indexes/editorial ordering metadata;
- layer-local Story ID allocator high-water mark;
- typed projection coverage state.

No layer owns canonical source truth.

## LAW 5.10-1 — NO GLOBAL STORY FRONTIER

There is no generic scalar Story projection frontier across layers or source domains.

Projection progress is typed by:

```text
Story layer
+ source projection domain
```

No order/comparison is inferred across different domains merely because their cursors are numeric/string-like.

---

# 3. Source projection-domain contract

Every admitted source domain for a Story layer must provide bounded deterministic candidate enumeration.

Conceptually:

```text
EnumerateStoryCandidates(
    layer,
    source_domain,
    after_coverage,
    pinned_source_basis,
    bounded_limit
)
    -> candidates[]
       next_coverage
       exhausted_to_basis: boolean
```

The source-domain cursor/token is projection-enumeration evidence only.

## LAW 5.10-2 — SOURCE ENUMERATION ORDER IS NOT FICTIONAL ORDER

Storage/log/ingestion order may be used to decide what projection work has been considered when the source owner explicitly defines that enumeration.

It SHALL NOT establish:

- fictional chronology;
- causal order;
- narrative reading order;
- simultaneity;
- ordering against another projection domain.

---

# 4. Candidate disposition contract

A source-domain/layer contract defines what terminal disposition is allowed for each admitted candidate class.

Minimum conceptual classes:

```text
MUST_MATERIALIZE
MAY_OMIT
```

Examples:

- a participant utterance selected by Step-5.11 exact-retention policy for `STORY/TRANSCRIPT` may be `MUST_MATERIALIZE`;
- a SemanticEvent considered for `STORY/EVENTS` may be `MAY_OMIT` if it has no useful presentation value;
- a MechanicalEvent considered for `STORY/MECHANICS` may be `MAY_OMIT` according to the accepted human-relevance policy.

## LAW 5.10-3 — COVERAGE ADVANCES ONLY AFTER TERMINAL DISPOSITION

A layer/source-domain coverage cursor may advance past candidate S only when S has reached an allowed terminal projection disposition under the layer contract.

For `MUST_MATERIALIZE`, at least one compatible durable Story record/source mapping must publish in the same closure that advances coverage past S.

For `MAY_OMIT`, consideration with no Story record is a valid terminal disposition and does not require a durable per-source skip record when contiguous coverage proves consideration.

Generation/transport/source-integrity failure is not terminal omission.

---

# 5. StoryLayerProjectionState

Each Story layer has compact durable projection-local state conceptually containing:

```text
layer identity
allocator high-water mark
coverage_by_source_domain
required layer indexes / editorial ordering metadata
```

Exact physical files/schema belong to later machine realization.

## LAW 5.10-4 — PROJECTION STATE IS DURABLE BUT NON-CANONICAL

Loss/corruption of Story projection state can damage Story catch-up/fidelity but cannot alter gameplay canon or Resumable Runtime Closure.

Gameplay owners SHALL NOT depend on Story projection state.

## LAW 5.10-5 — COVERAGE IS PROGRESS EVIDENCE, NOT SOURCE AUTHORITY

Coverage says that admitted source candidates were considered. It does not assert that Story wording is true, complete canon, or a replacement for source evidence.

---

# 6. Bounded queue-free catch-up

Backlog is derived:

```text
current pinned source basis
    minus
current Story-layer coverage
```

No durable `StoryProjectionJob`, generic pending queue, worker lease or claim ledger is required baseline.

## LAW 5.10-6 — NO BACKGROUND WORKER CORRECTNESS DEPENDENCY

Story catch-up must remain correct when projection can execute only during an ordinary foreground HDM activation.

The protocol SHALL NOT require work to continue after a ChatGPT turn ends.

Work/agent/API/external workers may be introduced later as Step-6 physical execution optimizations without changing projection authority semantics.

## LAW 5.10-7 — PROJECTION ACTIVATION POLICY IS NOT DURABILITY AUTHORITY

Whether catch-up runs:

- on a gameplay activation;
- on session boundary;
- on explicit Story/Commentator demand;
- before a retention operation;
- in a future async worker;

is Step-6/retention policy unless another accepted boundary explicitly requires it.

A missed activation cannot lose canonical gameplay state.

---

# 7. Deterministic projection control versus Chronicler

Projection correctness is owned by deterministic core.

Conceptual pipeline:

```text
1. pin campaign/source/Story basis
2. resolve target layer projection state
3. enumerate bounded uncovered source candidates
4. assemble exact eligible StorySourceBundle
5. transform/curate candidates
6. validate StoryProjectionDraft
7. allocate final layer IDs
8. validate refs + availability + indexes
9. build complete Story-layer delta
10. publish by Step-5.6 campaign CAS
11. advance allocator + coverage atomically with output
```

## StorySourceBundle

Conceptually includes:

```text
layer
pinned campaign/source basis
pinned Story basis
typed source-domain window(s)
eligible source payload/excerpts
source_manifest[]
existing Story refs/index excerpts needed for editorial continuity
availability inputs required for validation
```

## StoryProjectionDraft

Conceptually includes:

```text
layer
records with temporary local keys
content
source_refs
Story refs/crossrefs
entity refs
availability requirements
editorial/index proposals where allowed
```

It does **not** own final Story IDs, durable coverage, repository transport or canon.

## LAW 5.10-8 — CHRONICLER DOES NOT OWN PROJECTION COMMIT

The logical Chronicler may group, summarize, curate or rewrite occurred evidence but SHALL NOT directly:

- allocate authoritative final Story IDs;
- mutate layer coverage/allocator state;
- decide Git success/conflict;
- claim catch-up completion;
- make Story/canonical refs valid by assertion.

## LAW 5.10-9 — AN LLM CALL IS NOT REQUIRED FOR EVERY LAYER/ACTIVATION

Step 5.10 does not require one Chronicler model call per turn or per layer.

Deterministic projection is allowed where the layer contract permits it. Physical model-call placement is Step 6.

---

# 8. Final Story ID allocation

Story IDs remain Step-4 layer-local human-facing identities:

```text
T...
E...
M...
N...
```

## LAW 5.10-10 — GENERATIVE DRAFTS USE TEMPORARY LOCAL KEYS

Final Story IDs are assigned only by deterministic publication control from current layer allocator state.

Draft-local refs are deterministically rewritten to final IDs before publication.

## LAW 5.10-11 — ALLOCATOR ADVANCEMENT IS ATOMIC WITH NEW RECORDS

New Story record IDs, corresponding record files, required indexes/crossrefs, layer allocator advancement and applicable coverage advancement publish in one coherent Story transaction.

No published allocator advancement may expose a missing same-transaction record allocation.

## LAW 5.10-12 — STORY IDS ARE NOT REUSED IN NORMAL CAMPAIGN LIFETIME

Layer allocator high-water marks are monotonic. Deleting/revising Story records does not normally make their IDs reusable.

Numeric formatting width remains a minimum, not a maximum.

---

# 9. Layer-local Story publication closure

Ordinary Story catch-up publishes one layer closure at a time.

The complete Story-layer write set may include:

- new Story records;
- corrected Story records;
- required deletions where structurally safe;
- layer indexes/order metadata;
- whole-unit availability metadata;
- Story-local forward refs;
- allocator high-water update;
- source-domain coverage advancement.

The resulting tree publishes through Step-5.6 single-ref CAS.

## LAW 5.10-13 — COVERAGE AND OUTPUT ARE CRASH-COHERENT

A ref-selected Story transaction exposes either the old coherent layer projection state or the new coherent layer projection state.

Coverage SHALL NOT advance beyond records/index/availability closure required by candidate disposition.

## LAW 5.10-14 — NO MANDATORY CROSS-LAYER ATOMICITY FOR CATCH-UP

TRANSCRIPT, EVENTS, MECHANICS and NARRATIVE may publish and lag independently.

Failure of one layer does not roll back or block valid publication of another Story layer.

A cross-layer Story maintenance transaction is allowed only when an explicit structural correction must update already-published cross-layer refs coherently.

---

# 10. Cross-reference closure

## LAW 5.10-15 — NO PUBLISHED DANGLING STORY REF

A new Story record may reference:

- a Story record already durable at its pinned basis; or
- a record created in the same coherent Story transaction where intra-transaction resolution is deterministic.

For ordinary layer-local catch-up, a cross-layer target must already be durable before the referring record publishes.

## LAW 5.10-16 — REVERSE LOOKUP IS DERIVATIVE UNLESS EXPLICITLY OWNED

Reverse crossref indexes may exist for bounded retrieval/correction but do not become semantic authority over the relation.

The forward/source record relation remains sufficient source evidence unless a later contract explicitly assigns more.

---

# 11. Availability/reveal closure

Step-4 whole-unit Story availability semantics remain unchanged.

## LAW 5.10-17 — AVAILABILITY PUBLISHES WITH THE RECORD/INDEX SURFACE IT PROTECTS

Body, title, entity refs, crossrefs, chapter/index labels and any other spoiler-bearing retrieval metadata must not publish under stale/incompatible availability requirements.

A material Story correction recomputes/revalidates applicable availability before publication.

## LAW 5.10-18 — STORY AVAILABILITY DOES NOT BECOME DISCLOSURE AUTHORITY

Story availability governs Story/Commentator retrieval eligibility only. It does not create or advance `runtime.disclosure` or fictional `world.knowledge`.

---

# 12. Per-layer lag and caught-up status

For one pinned source basis B:

```text
CAUGHT_UP(layer, B)
```

means every required source projection domain for that layer has terminally considered all candidates admitted through B according to that domain contract.

## LAW 5.10-19 — CAUGHT_UP IS PROJECTION/BASIS-RELATIVE

`CAUGHT_UP` does not mean:

- “caught up to world time”;
- “contains every canonical fact”;
- “contains every source event”;
- “all Story layers are equally current”.

It is a layer-local projection completeness statement relative to a pinned source basis.

## LAW 5.10-20 — COMMENTATOR/RETRIEVAL MAY OBSERVE LAG

Story retrieval may expose typed layer coverage/lag status so a Story consumer does not mistake absence from a lagging projection for proof that an event never occurred.

Exact Commentator UX and automatic catch-up behavior remain Step 6.

---

# 13. Crash/restart idempotency

## 13.1 Crash before Story publication

Generated/unpublished drafts are non-authoritative and may be lost.

Coverage remains unchanged, so restart rediscovers the source window.

## 13.2 Confirmed Story publication

Records/indexes/allocator/coverage advance together.

Restart begins after current coverage.

## 13.3 Indeterminate ref outcome

Do not blindly republish the same draft.

Read current target layer projection state.

```text
if current coverage already terminally includes the intended source window:
    treat that source work as already considered
    discard stale/lost draft attempt

else:
    continue from current Story/source basis
```

Another worker's different valid Story wording has no obligation to yield to a losing unpublished draft.

## LAW 5.10-21 — COVERAGE IS CATCH-UP IDEMPOTENCY EVIDENCE

No separate durable projection-run/job identity is required baseline to suppress duplicate catch-up after restart/ambiguous acknowledgement.

---

# 14. Same-ref concurrency with canonical gameplay

Story and canon share one campaign ref, so bounded CAS contention is possible.

## LAW 5.10-22 — GAMEPLAY NEVER WAITS FOR STORY FRESHNESS

Canonical gameplay publication, SAVE durability and gameplay recovery SHALL NOT require Story generation, Story catch-up or Story publication success.

Story owns no lock/lease/fence that canonical gameplay must wait to acquire.

## LAW 5.10-23 — STORY-ONLY HEAD MOVEMENT IS SEMANTICALLY DISJOINT FROM ORDINARY GAMEPLAY

Because Story cannot be gameplay authority, a branch movement proven to change only Story paths is a disjoint movement class for ordinary canonical gameplay publication.

Python persistence core may mechanically rebuild frozen gameplay delta on the newer base while preserving accepted mechanics/RNG/IDs, subject to Step-5.6 path/dependency verification.

This may cost a transport retry but not semantic replay/re-adjudication.

## LAW 5.10-24 — STORY YIELDS UNDER CONTENTION

Story publication has no freshness right over gameplay.

After bounded CAS/revalidation contention, Story projection may abandon the current attempt and retry on a later activation.

No Story starvation-freedom guarantee is required while canonical activity continues.

---

# 15. Canonical HEAD movement during Story projection

## LAW 5.10-25 — STORY DRAFT REUSE IS DEPENDENCY-AWARE

If branch movement is proven not to touch:

- target Story layer state;
- source records/evidence in the draft's source manifest;
- referenced Story records;
- availability/reveal dependencies;

then deterministic core may reuse/rebase the same validated StoryProjectionDraft on the newer campaign base without repeating Chronicler generation.

If relevant dependencies moved, revalidate/remap or discard/regenerate later.

---

# 16. Future concurrent Story workers

The baseline has no required background worker, but the protocol must remain concurrency-safe if Step 6 later supplies one.

Two Story workers may race from the same layer coverage/allocator basis.

One wins campaign CAS.

The loser refreshes:

- if intended source window is already covered, discard its draft;
- if target layer state changed but source remains uncovered, remap/revalidate or regenerate from current basis;
- never overwrite or force-push.

No leader/worker lease or queue claim is required baseline.

---

# 17. SAVE and gameplay recovery

## LAW 5.10-26 — SAVE DOES NOT PROMISE STORY FRESHNESS

A successful explicit gameplay SAVE establishes the Step-5.5 gameplay durability promise only.

It does not imply any Story layer is caught up or newly published.

## LAW 5.10-27 — STORY IS OUTSIDE GAMEPLAY RESUMABLE RUNTIME CLOSURE

Gameplay cold recovery can be `READY` while Story is lagging, absent or projection-corrupt, provided no gameplay owner illegally depends on Story.

## LAW 5.10-28 — CHRONICLER RESTART IS COVERAGE-BASED PROJECTION RECOVERY

A restarted Story projection process reconstructs work from:

```text
current pinned source basis
+ current target Story-layer projection state
```

No gameplay checkpoint, raw model memory or global timeline replay is required.

---

# 18. Source retention / Step-5.11 handoff

Step 5.10 defines projection facts that retention may depend on; Step 5.11 decides exact transcript/history retention policy.

## LAW 5.10-29 — RETENTION MAY REQUIRE PROJECTION CLOSURE, BUT ONLY BY TYPED POLICY

If a Step-5.11 retention rule promises that source candidate S will be preserved in a particular Story layer before source deletion, compaction must prove the required layer/source-domain terminal disposition before deleting S.

Do not require every source to wait for every Story layer.

## LAW 5.10-30 — SOURCE REFS PRESERVE IDENTITY; PAYLOAD RETENTION IS SEPARATE

A Story `source_ref` preserves source identity/provenance attribution.

It does not by itself promise that the full referenced source payload remains permanently dereferenceable after lawful 5.11/5.13 compaction.

If stronger post-compaction provenance is required, Step 5.11/5.13 must preserve an appropriate source/provenance artifact.

---

# 19. Correction/regeneration

Story is editable projection.

Two conceptual edit classes:

```text
EDITORIAL_REVISION
    same independently addressable presentation unit
    -> update same Story ID

STRUCTURAL_REWRITE
    split / merge / repartition / delete presentation units
    -> allocate new IDs where needed
    -> preserve no-dangling-ref invariant
```

## LAW 5.10-31 — CORRECTION NEVER CHANGES CANON

Story correction/regeneration cannot mutate canonical sources to fit prose and does not rewrite gameplay history authority.

## LAW 5.10-32 — EXISTING COVERAGE IS NOT INVALIDATED BY TOOL/MODEL VERSION ALONE

A later model/prompt/projector version does not automatically make prior source consideration unprocessed.

Historical regeneration is an explicit scoped editorial/maintenance action.

## LAW 5.10-33 — STRUCTURAL EDITS PRESERVE INTERNAL REFERENCE CLOSURE

A structural rewrite may use a cross-layer Story maintenance transaction when necessary to avoid dangling published Story refs/index entries.

Baseline does not require a general tombstone/supersession subsystem or stable public permalink guarantee across arbitrary structural regeneration.

Story IDs are nevertheless not reused.

---

# 20. Full/partial Story loss

Deleting or losing Story cannot change gameplay canon.

If projection state/records are missing:

- regenerate/catch up only from still-retained sources;
- exact fidelity unavailable from compacted sources is not invented;
- affected Story/Commentator functionality degrades truthfully;
- gameplay recovery remains independent.

Layer allocator high-water state should normally survive ordinary record cleanup to prevent ID reuse. A destructive all-Story identity reset, if ever supported, requires an explicit maintenance contract invalidating all Story refs/cursors.

---

# 21. Integrity classification

Story defects are projection/history defects, not gameplay canon corruption by default.

Examples:

```text
coverage points past missing MUST_MATERIALIZE record
allocator high-water lower than published ID
published Story ref target missing
availability/index metadata exposes otherwise ineligible record
coverage source cursor incompatible with source-domain contract
Story record claims nonexistent/invalid source identity
```

Recovery/repair should target Story projection state/sources and never invent canonical world history.

If a Story defect exposes evidence of underlying canonical/source corruption, that source scope enters its normal integrity protocol independently.

---

# 22. Performance/token contract

Ordinary gameplay must not require Story work.

Projection activation is bounded:

```text
load one target layer state
+ bounded source candidate window(s)
+ bounded Story/source dependencies
+ optional bounded Chronicler generation
+ one Story-layer publication
```

Baseline SHALL NOT require:

```text
full campaign history scan
all Story records scan
all-layer rebuild on each turn
one Chronicler call per gameplay turn
durable projection worker queue
continuous background polling
model/prompt-upgrade replay of old Story
```

---

# 23. Platform/deployment boundary

Current project baseline excludes Work/token-burning background orchestration and Pro/Enterprise-only assumptions.

## LAW 5.10-34 — PHYSICAL ROLE TOPOLOGY CANNOT WEAKEN STORY DURABILITY CONTRACT

Step 6 may run projection control/Chronicler:

- inline;
- in a separate safe model invocation;
- on demand;
- in a future async worker;
- through another supported deployment profile;

but every profile must preserve:

- deterministic source/coverage/ID/publication ownership;
- Step-4 context eligibility;
- queue-free source-of-backlog semantics unless a future explicit extension proves a queue necessary;
- gameplay independence from Story freshness.

---

# 24. Machine-realization debt

Later implementation planning must cover at least:

1. manifest/storage `story_root` realization;
2. Story layer record/index/projection-state schemas;
3. per-layer allocator high-water representation;
4. typed source projection-domain identifiers;
5. bounded source candidate enumeration contracts;
6. contiguous coverage cursor representation plus typed sparse fallback only where required;
7. `MUST_MATERIALIZE | MAY_OMIT` disposition metadata/policy;
8. exact StorySourceBundle/StoryProjectionDraft machine protocol;
9. deterministic temporary-key -> final-ID remapping;
10. whole-unit availability validation;
11. layer-local Story publication planner through Python RepositoryPort;
12. Story-only movement classification in Step-5.6 conflict handling;
13. ambiguous Story publication verification from current layer coverage;
14. Commentator/retrieval lag-status projection;
15. structural edit/ref-closure tooling;
16. Step-5.11 retention dependency integration;
17. Story-specific integrity/repair cases;
18. no-background/no-all-history-scan performance tests;
19. concurrency tests for future multiple Story workers;
20. Step-6 physical invocation policy without changing this semantic protocol.

No broad GAME/schema implementation begins during Step-5 architecture closure.

---

# 25. Required regression/adversarial realization cases

Later tests must include at least:

```text
canonical gameplay advances with zero Story work
10 gameplay publications while all Story layers lag
cold gameplay recovery with Story absent
Chronicler restart catches up from current layer coverage
source candidate MAY_OMIT advances coverage with no Story record
source candidate MUST_MATERIALIZE cannot advance coverage without record
one Story Event covers several SemanticEvents
one source candidate creates several Story records
coverage cursor order has no fictional chronology meaning
independent source-domain cursors are not compared
EVENTS caught up while NARRATIVE lags
NARRATIVE generation failure leaves canon/EVENTS unchanged
Story generation succeeds then Story CAS loses to canon-only movement
Story draft reused after proven-disjoint canon movement
same-layer Story writer wins first; losing draft discarded when coverage already advanced
Story-only ref movement causes gameplay transport rebuild but no mechanics/RNG replay
indeterminate Story ref acknowledgement resolved by current coverage
availability metadata correction publishes with record/index
new cross-layer ref requires durable target
structural correction cannot leave dangling Story refs
Story ID high-water does not reuse deleted ID
SAVE succeeds with Story lagging
source compaction blocked only when typed 5.11 policy requires projection closure
source_ref identity remains after source payload compaction policy
full Story loss never changes canon
no ordinary activation scans all Story/history
future async worker uses same coverage/CAS protocol
plain-chat profile works with no background worker
```

---

# 26. Candidate disposition

No material human decision currently blocks this candidate.

The candidate deliberately chooses the weakest baseline product promises consistent with accepted architecture and current owner constraints:

```text
Story freshness = eventual/opportunistic, no SLA
stable external permalink across arbitrary structural rewrite = not promised
source identity provenance = preserved
permanent source payload dereferenceability = not promised by 5.10
background Chronicler = not required
```

A future explicit owner requirement may strengthen these promises, but Step 5.10 should not pre-build infrastructure for them.

Next gate: adversarial review before canonicalization.

# Step 5.10 — Story Projection Durability — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — NONCANONICAL / STEP 5.10 IN PROGRESS**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Research basis:

- `2026-08-21-step-5-10-story-projection-durability-task-brief.md`
- `2026-08-21-step-5-10-story-projection-durability-research-draft.md`

Leading research direction under challenge:

> queue-free coverage-driven, layer-independent Story projection with deterministic projection control and optional generative Chronicler transformation.

The purpose of this document is to try to remove, break or narrow that direction before any candidate specification is written.

---

# 1. Challenge: can durable projection coverage be removed entirely?

Candidate simplification:

```text
Story records already contain source_refs
-> infer what was projected from existing records
-> no separate projection progress state
```

This fails on intentional omission.

Example:

```text
SemanticEvents:
    S1 material story beat
    S2 resolver bookkeeping / not story-worthy
    S3 material story beat

Story records:
    E1 <- S1
    E2 <- S3
```

After restart, records alone cannot distinguish:

```text
A. S2 was deliberately considered and omitted
B. Chronicler crashed before reaching S2
```

Without a progress/coverage claim, restart either:

- repeatedly reconsiders omitted sources forever; or
- guesses that missing source refs mean omission; or
- scans/reconstructs an unbounded history heuristic.

**Result:** some durable Story-local projection progress is necessary.

However, a per-source durable skip ledger is not necessary when a source domain offers safe contiguous projection enumeration.

Preferred minimal form:

```text
coverage(source_domain D) = cursor K
```

meaning every admitted candidate through K was considered, whether it produced zero, one or many Story records.

Sparse coverage is only a fallback for source domains that cannot provide such contiguous semantics.

---

# 2. Challenge: does a contiguous coverage cursor create a hidden global order?

It would if used across unrelated sources or interpreted as fiction.

The safe form is narrower:

```text
ProjectionCoverage(layer L, source domain D, cursor K)
```

K orders **projection-source enumeration** only.

It does not establish:

- fictional chronology;
- causal order;
- player-facing narrative order;
- order against another source domain;
- order against another Story layer.

For a layer consuming several source domains:

```text
coverage = {
    semantic_log_domain: K1,
    transcript_domain: K2,
    mechanics_domain: K3
}
```

No comparison between K1/K2/K3 is authorized.

**Result:** domain-typed cursors are compatible with Step 5.1 if source owners define bounded monotonic enumeration.

---

# 3. Challenge: head-of-line blocking under contiguous coverage

Suppose source candidate S17 cannot be projected, while S18/S19 could.

A strict contiguous cursor cannot advance beyond S17.

Possible responses:

A. add sparse exception/gap ledger;
B. add durable job statuses;
C. allow the projection transformation to choose a terminal disposition for every valid source candidate;
D. accept projection-domain blocking on genuinely invalid/integrity-suspect input.

For normal valid source evidence, Chronicler does not need to create prose for every candidate. It can terminally **consider and omit** S17. Conflicting/insufficient evidence can also yield qualified omission/editorial issue rather than invented prose.

Only source integrity/retrieval defects should prevent consideration. In that case Story is allowed to lag; blocking that source-domain cursor is safer than silently stepping over missing evidence.

**Result:** do not add sparse gap/job machinery baseline. Accept head-of-line blocking for genuine projection-source defects; introduce sparse gaps later only if measured operational evidence justifies the complexity.

---

# 4. Challenge: can Story reuse the canonical `runtime.id_allocator`?

At first this appears simpler: Step 5.0 already preserves a campaign allocator owner.

But Story IDs are explicitly non-canonical presentation identities and are allocated independently per Story layer.

Reusing canonical allocation state would mean Story-only publication mutates gameplay/runtime allocator authority. That creates avoidable coupling:

- Story deletion/regeneration affects canonical allocator state;
- Story contention touches a gameplay dependency;
- canonical publication can no longer treat Story-only movement as fully disjoint;
- failure of noncanonical projection can dirty canonical runtime allocator state.

**Result:** Story requires Story-local layer allocator state. This is projection identity metadata, not a new `runtime.*` semantic owner.

---

# 5. Challenge: can layer-local IDs be allocated before generation?

If final IDs are allocated before an LLM/generative call, a later Story-writer conflict can consume/shift those IDs and force regeneration or leave holes/reservations.

Safer form:

```text
StoryProjectionDraft
    temporary local keys: d1, d2, d3

publication phase
    current layer allocator -> E000123, E000124, E000125
    rewrite draft-local refs deterministically
```

If another Story writer wins first:

- no accepted gameplay is replayed;
- if source coverage is already satisfied, discard the losing draft;
- otherwise remap/revalidate against current Story state.

**Result:** final Story IDs belong to deterministic publication, not Chronicler generation.

---

# 6. Challenge: must Story IDs be reusable after deletion/regeneration?

Reusing IDs minimizes numeric growth but creates avoidable ambiguity with:

- stale Story crossrefs;
- Commentator/session cursors;
- exported/bookmarked Story identities;
- old retained narrative text.

Numeric exhaustion is not realistic because Step 4 explicitly says width is a minimum, not a maximum.

**Result:** Story layer allocator high-water marks should be monotonic and IDs should not be reused during normal campaign lifetime, even when individual Story records are deleted. A destructive maintenance reset may be specified later only if it invalidates all Story references explicitly.

This avoids needing baseline tombstones merely to prevent ID reuse.

---

# 7. Challenge: does every layer need one transaction with every other layer?

Cross-layer atomicity appears attractive:

```text
TRANSCRIPT + EVENTS + MECHANICS + NARRATIVE
-> one Story commit
```

But it turns NARRATIVE generation into a blocker for cheaper/lower layers and destroys the central lag property.

Required safety is narrower:

> A published Story ref must never dangle and availability/index metadata must not reveal content before its record is valid.

This can be satisfied by layer-local transactions if cross-layer forward refs target only already-durable records.

Example legal state:

```text
TRANSCRIPT caught up
EVENTS caught up
MECHANICS behind 2 batches
NARRATIVE behind 20 batches
```

**Result:** no mandatory cross-layer atomicity. Publish layer-local closures independently. If NARRATIVE needs newly generated E/M/T records, those records publish first.

---

# 8. Challenge: does this require a strict layer DAG?

A rigid pipeline such as:

```text
TRANSCRIPT -> EVENTS -> MECHANICS -> NARRATIVE
```

is not justified.

Step 4 allows each layer distinct sources and optional crossrefs. EVENTS can be built directly from SemanticEvents; MECHANICS can use MechanicalEvents/receipts; TRANSCRIPT uses participant discourse. NARRATIVE often consumes Story refs but may also cite source evidence.

**Result:** define only **reference closure**, not a universal processing DAG. NARRATIVE is commonly downstream, but lower layers need not wait for one another unless a concrete record dependency requires it.

---

# 9. Challenge: Story publication shares the campaign ref — can Story really “not block gameplay”?

A future Story writer can win the campaign CAS immediately before a gameplay writer. Then gameplay's prepared commit rejects even though paths are disjoint.

Therefore “Story cannot block canon” cannot literally mean “Story can never cause one transport retry” while both share one ref.

The correct semantic guarantee is:

1. gameplay publication never waits for Story freshness/generation/lock;
2. Story holds no lease or exclusion right over the campaign ref;
3. Story-only ref movement is a proven-disjoint movement class for gameplay because canonical gameplay does not read Story as authority;
4. gameplay can mechanically rebuild its frozen semantic delta on the Story-updated base without rerunning mechanics/RNG/LLM semantic decisions;
5. under repeated contention Story yields/abandons its attempt and catches up later.

This preserves the Step-4 same-branch constraint without inventing a second branch or distributed priority lock.

**Result:** refine the requirement to **no semantic or freshness dependency; bounded transport contention is tolerated**.

---

# 10. Challenge: can a Story draft survive canonical HEAD movement?

Sometimes yes.

If canonical movement does not touch the draft's frozen source/dependency manifest and does not touch target Story layer state, the draft's factual/editorial basis remains valid.

Then deterministic publisher may:

```text
adopt newer campaign HEAD
reuse same StoryProjectionDraft
rebuild Story delta on new base tree
publish
```

If movement touches:

- source records used by the draft;
- Story refs used by the draft;
- reveal/availability dependencies;
- target layer allocator/coverage/index state;

then revalidation/remapping or regeneration is required.

**Result:** reuse Step-5.6 dependency-aware movement; do not rerun Chronicler solely because unrelated canon advanced.

---

# 11. Challenge: can a canonical gameplay draft survive Story-only HEAD movement?

Yes, more strongly.

By Step 4 law, gameplay mechanics/current state cannot depend on Story as authority. Therefore Story-only changed paths are semantically disjoint from an ordinary gameplay publication footprint unless the operation is itself a Story/Commentator workflow.

Gameplay persistence core may transport-rebuild on the newer base and preserve accepted mechanics/RNG/IDs.

**Result:** Story-only ref movement is a canonical proven-disjoint class, subject to path-level verification that no non-Story dependencies moved.

---

# 12. Challenge: ambiguous Story publication acknowledgement

Canonical publication needs strong closure proof because gameplay durability promises depend on it. Story has weaker stakes but must still avoid duplicates.

Suppose intended Story batch B gets an indeterminate ref outcome.

Recovery can read current target layer projection state:

```text
if source coverage now includes B's source window:
    work is already terminally considered
    do not publish duplicate draft

if coverage did not advance:
    current Story basis owns next action
    retry/reproject from current state
```

If another worker legitimately published different prose for the same source window first, that is acceptable current Story projection. The losing draft has no authority claim.

**Result:** coverage state is also the idempotency evidence for catch-up. A separate durable projection-run/job identity is unnecessary baseline.

---

# 13. Challenge: generation succeeds, CAS loses

The generated draft is non-authoritative.

Outcomes:

```text
Story layer unchanged; canon-only movement
    -> rebase/revalidate draft, no LLM rerun needed

same layer coverage already advanced over source window
    -> discard draft

same layer changed but source still uncovered
    -> deterministic remap/revalidate if possible
    -> otherwise discard and regenerate later
```

No accepted gameplay is replayed. Losing generative work is a cost issue, not a semantic defect.

**Result:** no durable draft reservation system is justified.

---

# 14. Challenge: exact transcript is about to be compacted while Story lags

This is the strongest cross-slice trap.

Step 4 admits that Story may become the only retained exact dialogue/editorial copy after raw source compaction.

Therefore physical source compaction cannot be oblivious to Story coverage when the retention policy promises that fidelity.

But Step 5.10 must not decide which exact utterances deserve retention; that belongs to Step 5.11.

Required handoff:

```text
Step 5.11 retention policy selects source S for deletion
    |
    +-> if policy requires Story preservation first:
            require applicable Story coverage/materialization closure
            OR consciously accept fidelity loss according to 5.11 policy
```

**Result:** 5.10 exposes typed projection coverage as a possible retention dependency; 5.11 decides when it is mandatory.

No generic rule “all source waits for all Story layers” is justified.

---

# 15. Challenge: must `source_refs` remain dereferenceable forever?

If yes, Story would force indefinite retention of canonical/transcript evidence or require permanent provenance tombstones for everything.

Step 4 says `source_refs` provide traceability, but also explicitly allows source compaction to make Story the only retained copy of some exact prose.

The minimal coherent interpretation is:

- `source_refs` preserve stable source identity/provenance attribution;
- payload dereferenceability lasts only as long as the owning retention contract preserves that source or a replacement provenance artifact;
- Step 5.11/5.13 may define compact provenance stubs/digests where a stronger guarantee is needed.

**Result:** Step 5.10 does not force permanent source payload retention.

---

# 16. Challenge: correction/regeneration needs tombstone/supersession objects?

Not for the baseline.

Story is non-canonical editable presentation. The core requirement is coherent internal refs/indexes/availability.

Two forms are sufficient initially:

```text
EDITORIAL REVISION
    same independently-addressable presentation unit
    -> edit same Story ID atomically

STRUCTURAL REWRITE
    split/merge/repartition presentation units
    -> allocate new IDs as needed
    -> atomically rewrite/delete affected Story-internal refs/indexes
```

Baseline does not promise stable public permalinks across arbitrary structural regeneration. Noncanonical Commentator/session cursors may re-anchor from current indexes.

IDs remain non-reusable, so a deleted ID cannot silently identify unrelated future content.

**Result:** no mandatory Story tombstone/supersession subsystem in 5.10.

---

# 17. Challenge: should projector/model/prompt version invalidate coverage?

Automatically replaying old history whenever model/prompt/software changes would:

- burn tokens;
- churn Story IDs/text;
- threaten historical editorial continuity;
- make “caught up” dependent on deployment version rather than source consideration.

Coverage should mean:

> source candidate was considered by the then-valid Story process.

A later projector improvement does not make prior coverage false.

Regeneration is an explicit scoped editorial/maintenance operation.

**Result:** projector version may be retained as optional provenance/diagnostics, but it is not baseline coverage authority and does not trigger automatic replay.

---

# 18. Challenge: plain one-chat context isolation

The active product constraint is severe: baseline cannot rely on Work/background role processes, and one physical chat cannot be assumed to provide strict context reset between incompatible role source envelopes.

Could 5.10 solve this by weakening Chronicler inputs or Story hidden content?

No. That would change Step-4 semantics merely to fit one physical topology.

Instead:

- Story projection is allowed to lag when a safe Chronicler invocation is not available;
- deterministic projection control remains usable without a model call;
- Step 6 decides whether/when a safe physical Chronicler or Commentator invocation exists;
- a plain-chat deployment may disable/defer incompatible role features rather than violating context eligibility.

**Result:** platform limitation affects activation/freshness, not Story persistence semantics.

---

# 19. Challenge: can exact SAVE require Story catch-up?

No accepted gameplay recovery rule depends on Story.

Making SAVE wait for Story would:

- add LLM/token work to explicit durability;
- violate noncanonical isolation;
- make Story generation failure a save failure;
- contradict the explicit lag requirement.

**Result:** successful gameplay SAVE does not imply any Story layer is caught up. A separate explicit “save/export Story” operation could exist later but is not baseline SAVE semantics.

---

# 20. Challenge: can cold gameplay recovery require Story hydration?

No.

If gameplay owners/recovery routes are valid, corrupt/missing/lagging Story is a presentation/history issue only.

Chronicler catch-up recovery separately uses:

```text
current source basis
+ current Story layer coverage/allocator/index state
```

No checkpoint or global timeline replay is required.

**Result:** Story projection state is outside gameplay Resumable Runtime Closure.

---

# 21. Challenge: full Story deletion

Step 4 allows deleting Story without changing canon.

If Story content/index/coverage is deleted:

- gameplay remains correct;
- rebuilding is possible only from retained sources;
- fidelity unavailable from compacted sources is truthfully lost;
- layer ID allocator high-water marks should normally survive to prevent ID reuse/collision with stale external/internal references.

An explicit destructive maintenance reset that also invalidates all Story identity references may later reset allocators, but this is not ordinary behavior.

**Result:** Story absence is recoverable presentation degradation, not gameplay corruption.

---

# 22. Revised minimal architecture after challenge

The challenged direction is smaller than the research draft's broad conceptual model.

Required baseline concepts:

```text
1. StoryLayerProjectionState
       layer-local allocator high-water mark
       typed source-domain coverage cursor(s)/fallback sparse coverage
       required layer indexes/ordering metadata

2. StorySourceBundle
       exact pinned eligible source window + source manifest

3. StoryProjectionDraft
       temporary local keys
       proposed records/content/refs/availability
       no final IDs, transport or coverage authority

4. deterministic Story publisher
       validate
       allocate/remap IDs
       atomically publish layer closure
       advance coverage
       classify CAS movement via Step 5.6
```

Not required baseline:

```text
Story job queue
background worker
projection lease/claim
projection-run durable entity
per-source skip records when contiguous coverage exists
global Story frontier
cross-layer atomic transaction
automatic historical replay on projector version change
Story tombstone/supersession subsystem
stable external Story permalink guarantee
Story participation in gameplay SAVE/RRC
```

---

# 23. Strongest counterargument

The strongest counterargument is that a durable job ledger would make future asynchronous multi-worker operation easier and more observable.

Response:

- current baseline has no worker to drain it;
- source-vs-coverage already defines backlog without duplicate authority;
- two workers can race safely using Story layer CAS/coverage;
- durable claim/job lifecycle would add fencing/recovery/GC complexity for noncanonical projection;
- if future measured throughput demonstrates that pull-based coverage cannot schedule work adequately, a job/lease layer can be added as a derivative optimization without changing source/coverage authority.

Therefore pre-building the queue violates YAGNI.

---

# 24. Revised recommendation

Recommendation after challenge:

> **LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL GENERATIVE CHRONICLER / GAMEPLAY-PRIORITY SAME-REF CAS**

More compactly:

```text
Story source authority stays outside Story
Story layer coverage says what has been considered
uncovered source defines backlog
Chronicler proposes presentation, not progress or IDs
publisher atomically commits one layer's records+indexes+availability+allocator+coverage
layers may lag independently
canon never waits for Story
Story yields under contention
```

Confidence after challenge: **HIGH**, subject to adversarial review.

---

# 25. Remaining possible owner decisions

After challenge, no material owner decision is currently required to choose the core durability model.

Potential product-level choices remain deliberately outside the core design unless the owner wants stronger guarantees:

1. stable public/permalink Story IDs across arbitrary structural regeneration;
2. guaranteed maximum Story freshness/lag;
3. exact provenance dereferenceability after source compaction.

Current recommendation for baseline is deliberately minimal:

```text
no permalink guarantee across structural rewrite
no freshness SLA; eventual/opportunistic projection
source identity provenance survives; exact payload retention is 5.11 policy
```

These defaults follow the already stated project constraints and do not appear to require escalation unless the owner wants a stronger product promise.

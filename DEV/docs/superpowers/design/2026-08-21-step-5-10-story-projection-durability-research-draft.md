# Step 5.10 — Story Projection Durability — Research Draft

Status: **RESEARCH DRAFT — NONCANONICAL / STEP 5.10 IN PROGRESS**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Task brief:

- `2026-08-21-step-5-10-story-projection-durability-task-brief.md`

This document separates verified facts, inherited constraints, assumptions, inferences and provisional recommendations. It is not a candidate specification.

---

# 1. Executive research result

The strongest current direction is **not** to build a Story worker/scheduler subsystem.

The evidence instead favors a queue-free, coverage-driven projection protocol:

```text
canonical historical/source evidence
        |
        | typed bounded source enumeration
        v
layer projection coverage
        |
        | uncovered source window
        v
StorySourceBundle
        |
        | optional/generative Chronicler transformation
        v
StoryProjectionDraft (temporary local keys)
        |
        | deterministic validation + final Story ID allocation
        v
one Story-layer publication transaction
        |
        v
records + layer indexes + availability + allocator + coverage
```

Backlog is the difference between source-domain position and durable Story-layer coverage; it is not a durable job queue.

Story may remain behind indefinitely without changing gameplay correctness. Projection happens when an execution opportunity exists; the exact activation/budget policy remains Step 6.

This conclusion is provisional until analytical challenge/adversarial review.

---

# 2. Repository facts

## FACT R1 — Story semantics are already fixed by Step 4

Step 4 canonically defines one durable non-canonical Story surface on the campaign branch:

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

Story cannot own current world/mechanical truth, knowledge, disclosure or recovery state.

Step 4 also fixes:

- layer-local IDs (`T...`, `E...`, `M...`, `N...`);
- one independently addressable record per file as default;
- dependency-based availability rather than scalar reveal chronology;
- `source_refs` provenance;
- Chronicler as logical transformation role;
- Commentator as Story-first consumer;
- physical role-call topology as Step 6.

## FACT R2 — Logical role != process/model call

Step 4 explicitly states that a logical role does not imply a separate long-lived agent, model, process or model call.

Therefore Step 5.10 must not equate `Chronicler` with a required background process.

## FACT R3 — Same campaign ref owns Story and canon storage

Accepted architecture keeps Story in the same campaign branch. No long-lived spectator/public Story branch is authorized by default.

Therefore Story-only publication and canonical gameplay publication ultimately contend on the same Git ref even though their semantic authority differs.

## FACT R4 — Step 5.6 already provides one-ref CAS transport semantics

Campaign publication is one base-tree-derived commit followed by one non-force ref transition. Prepared objects are non-authoritative. Stale movement is classified by dependency overlap; proven-disjoint movement may permit mechanical rebuild rather than semantic replay.

This is sufficient as the transport substrate for Story transactions; Step 5.10 does not need another Git protocol.

## FACT R5 — Step 5.1 forbids generic projection frontier authority

A progress/cursor/frontier concept must identify its semantic domain/scope. No cross-domain order may be inferred without an owning contract.

Therefore “Story frontier” cannot be one generic scalar over transcript, semantic events, mechanics and narrative.

## FACT R6 — Current machine surfaces do not yet implement Story

Current runtime campaign template/manifest/schema do not yet expose a `STORY/` root or Story record/projection schemas. This is implementation debt, not evidence that Story is optional semantically after Step 4.

Step 5.10 should therefore define architecture before machine fields.

## FACT R7 — SemanticEvent history is append-only and chronology order is not storage order

Current event contract already distinguishes causal/relative-order evidence from optional local ordering; event IDs/Git commits are not fictional chronology.

A projection ingestion cursor may use source-storage/enumeration order only as a **projection coverage domain**, never as fictional chronology/presentation order.

## FACT R8 — Story may contain non-regenerable fidelity

Step 4 explicitly says durable non-canonical does not mean byte-for-byte regenerable. After raw message/source compaction, Story may be the only retained copy of exact dialogue/editorial prose.

Therefore Story durability is not merely a disposable cache problem.

---

# 3. Platform research — current ChatGPT deployment reality

These facts are time-sensitive and MUST be reverified in Step 6 before physical orchestration decisions.

Primary sources checked 2026-08-21:

- OpenAI Help: ChatGPT Work / GPT-5.6 product availability;
- OpenAI Help: Scheduled Tasks in ChatGPT;
- OpenAI Help: ChatGPT agent deprecation/replacement by Work;
- existing project Step-6 LLM role-isolation feasibility notes.

## FACT P1 — ordinary chat is not six persistent background workers

One ordinary ChatGPT conversation/turn cannot be assumed to host six independently persistent background LLM role processes.

Even where product infrastructure internally performs multiple tool/model operations, HDM cannot use undocumented hidden concurrency as a correctness contract.

## FACT P2 — Work is not an admissible baseline dependency for this project

ChatGPT Work exists for longer/multi-step tasks on eligible paid plans. The project owner explicitly excludes consuming Work capacity for ordinary HDM gameplay.

Therefore Work cannot be required to keep Story caught up.

## FACT P3 — Pro/Enterprise capability cannot be baseline

Project deployment must not rely on Pro/Enterprise-only capacity/features.

## FACT P4 — Scheduled Tasks are not a viable per-turn Story worker contract

Current Scheduled Tasks are scheduled/future invocations with plan limits and product/tool restrictions. They are not a reliable low-latency per-gameplay-turn background projection mechanism. Current help also states that tasks created in projects with files cannot access those project files, which is directly hostile to treating them as a repository/project-backed Chronicler worker.

Even if this changes later, Step 5.10 correctness must not depend on it.

## FACT P5 — richer orchestration exists outside the baseline

OpenAI API/Agents SDK and other future deployment backends can support separate invocations and agent-like orchestration. Those options belong to Step 6 and may optimize execution topology without changing the Step-5.10 semantic persistence protocol.

## CONSTRAINT P-C1 — single sequential stream must be sufficient

The baseline Story protocol must remain correct when projection work can run only during an ordinary foreground HDM activation.

No correctness rule may require work to continue after the assistant turn has ended.

---

# 4. External architecture research

Primary/general references examined:

- Microsoft Azure Architecture Center — CQRS pattern;
- Microsoft Azure Architecture Center — Materialized View pattern;
- Apache Kafka producer idempotence documentation as a narrow retry/idempotency reference.

## FACT E1 — read model lag is a normal consistency mode

Materialized/read models may lag their write authority and still be correct if stale-state semantics are explicit.

## FACT E2 — messaging is optional, not intrinsic to read-model separation

CQRS/read-model separation does not require a message broker or durable job queue. Messaging is one implementation strategy and introduces its own duplicate/retry/failure complexity.

## FACT E3 — rebuildability depends on retained source

Materialized views are straightforward to rebuild only while sufficient source data remains. HDM Story is stricter because exact dialogue/editorial prose may cease to be reproducible after source compaction.

## INFERENCE E-I1

HDM should reuse eventual-projection ideas but must not inherit event-sourcing assumptions wholesale. Current world state is not reconstructed from Story/LOG replay, and Story may preserve presentation fidelity beyond source retention.

---

# 5. Quality attributes that distinguish alternatives

Priority order for Step 5.10:

1. **canonical isolation** — Story failure cannot alter/block gameplay correctness;
2. **restart idempotency** — no duplicate/invented Story after crash/restart;
3. **single-chat viability** — no background worker required;
4. **bounded catch-up** — no all-history scan on ordinary activation;
5. **low token/LLM burn** — no automatic Chronicler generation every gameplay turn;
6. **layer failure isolation** — NARRATIVE failure should not erase/block lower Story layers;
7. **future async compatibility** — separate worker later must use same protocol;
8. **same-ref concurrency correctness**;
9. **source-compaction safety**;
10. **editorial correction/regeneration flexibility**.

---

# 6. Alternative A — synchronous Story inside canonical gameplay publication

Model:

```text
resolve gameplay
-> generate Story
-> validate canon + Story
-> one campaign commit containing both
```

### Strengths

- no projection lag;
- one visible repository frontier;
- simple “everything committed together” mental model;
- no separate catch-up state.

### Weaknesses

- Chronicler/model failure blocks gameplay durability;
- token/latency cost paid on every relevant publication;
- Story correctness contaminates canonical transaction validity;
- impossible to satisfy requirement that NARRATIVE failure not block canon;
- physical role isolation issues leak into persistence critical path;
- future Story correction is still separate anyway.

### Verdict

**Reject.** Violates an explicit Step-5.10 requirement.

---

# 7. Alternative B — foreground post-canon projection every turn/boundary

Model:

```text
canonical gameplay publication succeeds
-> same foreground activation runs Chronicler
-> separate Story commit
-> return/continue gameplay
```

### Strengths

- canon is no longer transactionally dependent on Story;
- usually very fresh Story;
- simple in one sequential ChatGPT stream;
- no background infrastructure required.

### Weaknesses

- still pays Chronicler tokens/latency almost every turn;
- Story generation/publication failure can delay user-visible response even if it cannot roll back canon;
- long Story work competes with gameplay context/token budget;
- requires a catch-up protocol anyway after crash or skipped turn;
- same-ref Story commits create unnecessary ref churn.

### Verdict

**Do not use as semantic architecture.** It may be a Step-6 activation policy for small opportunistic batches, but correctness cannot depend on every-turn foreground projection.

---

# 8. Alternative C — queue-free lazy/opportunistic catch-up from durable typed coverage

Model:

```text
source domain(s) expose bounded projection enumeration
Story layer stores durable typed coverage of what has been considered

backlog = source basis - layer coverage

when projection activation is available:
    select bounded next uncovered window
    assemble pinned StorySourceBundle
    transform / curate
    publish Story-layer transaction
    advance layer coverage atomically
```

No durable pending-work object is required.

### Strengths

- directly supports one ordinary chat with no background worker;
- Story can lag without correctness loss;
- no per-turn LLM burn requirement;
- restart derives work from durable coverage gap;
- future async worker uses the same protocol;
- no new scheduler authority;
- layer-local catch-up/failure isolation is natural;
- source retention can protect only genuinely uncovered required material.

### Weaknesses

- needs durable Story-local coverage metadata;
- each admitted source domain needs bounded enumeration/cursor semantics;
- cursor/coverage must not be mistaken for fictional chronology;
- source compaction and coverage continuity must coordinate with 5.11/5.13.

### Verdict

**Leading alternative.**

---

# 9. Alternative D — durable projection work ledger / job queue

Model:

```text
canonical publication
-> append StoryProjectionJob(s)

worker
-> claims job
-> generates/publishes Story
-> marks job complete
```

### Strengths

- explicit backlog/retry status;
- natural for a true background worker;
- easy observability;
- can assign work to multiple workers.

### Weaknesses

- creates new durable operational lifecycle solely for non-canonical projection;
- queue itself requires durability, recovery, claim/fencing, retry/idempotency and GC;
- baseline ChatGPT cannot continuously drain it;
- canonical publication may need to emit jobs, re-coupling Story bookkeeping into gameplay writes;
- duplicate authority risk between queue state and source-vs-coverage reality;
- future worker capability is not current evidence of need.

### Verdict

**Reject baseline.** Reopen only if measured future orchestration requires a queue feature not expressible by coverage-driven pull.

---

# 10. Alternative E — deterministic source-keyed Story identities

Model:

```text
Story record identity = function(layer, source identity)
```

This attempts to make restart idempotent without allocator/progress state.

### Strengths

- trivial duplicate suppression for 1:1 projections;
- no sequence allocator conflict;
- source lookup simple.

### Weaknesses

- Step 4 fixed human-facing layer-local numeric Story IDs;
- EVENTS/MECHANICS/NARRATIVE are not 1:1 with source items;
- one Story beat may summarize many events;
- one source event may split into several presentation records;
- intentional omission has no record identity;
- editorial regeneration/granularity change breaks deterministic mapping.

### Verdict

**Reject as universal identity model.** Stable source identities remain essential coverage/provenance keys, not Story record IDs.

---

# 11. Alternative F — rebuild Story on demand with minimal/no progress state

Model:

```text
when Story needed:
    read retained history
    regenerate view
```

### Strengths

- almost no projection control metadata;
- simplest write path initially.

### Weaknesses

- potentially unbounded history reads/token cost;
- repeated nondeterministic prose churn;
- impossible byte-level regeneration after transcript/source compaction;
- no bounded restart/catch-up guarantee;
- every Story request becomes expensive;
- weak concurrency/editorial continuity.

### Verdict

**Reject baseline.** Full rebuild may remain a maintenance operation when sufficient sources survive.

---

# 12. Key synthesis: separate projection control from Chronicler generation

A central finding is that Story durability mechanics should be deterministic even if Story content is generative.

Provisional boundary:

```text
DETERMINISTIC PROJECTION CONTROL
    select source domain/window
    pin exact source + Story basis
    assemble StorySourceBundle
    validate StoryProjectionDraft
    allocate final layer-local Story IDs
    validate refs/availability
    build complete Story write set
    publish via Step-5.6 CAS
    advance coverage/allocator/index state

CHRONICLER LOGICAL ROLE
    transform eligible occurred evidence
    choose human-meaningful grouping/wording where generative judgment is needed
    produce temporary-keyed StoryProjectionDraft
    never own Git transport, final ID allocation, source coverage or canonical state
```

This is compatible with:

- no Chronicler LLM call for a given activation;
- deterministic handling of some Story layers where possible;
- one foreground call;
- future isolated model invocation;
- future async worker;
- different models per layer in Step 6.

---

# 13. Layer-specific observations

## 13.1 TRANSCRIPT

The semantic output is close to deterministic copying of retained participant discourse, but exact source/delivery boundaries are Step 5.11/5.12 concerns.

Step 5.10 should not require an LLM to copy transcript records.

## 13.2 EVENTS

Human-meaningful grouping/summarization is generative/editorial. One Story Event may consume one or many SemanticEvents and may omit non-story-worthy events.

## 13.3 MECHANICS

Selection/curation can be partly deterministic if future machine metadata marks human-relevant mechanics, but current architecture does not prove such a complete classifier. Keep implementation open.

## 13.4 NARRATIVE

Most clearly generative/editorial and most tolerant of lag/failure. NARRATIVE should be downstream-optional: failure cannot block TRANSCRIPT/EVENTS/MECHANICS projection or canon.

---

# 14. Projection coverage model — provisional

A layer does not own one global scalar frontier.

Conceptually:

```text
StoryLayerProjectionState(layer)
    allocator_state
    coverage_by_source_domain:
        source_domain_D1 -> cursor/coverage evidence
        source_domain_D2 -> cursor/coverage evidence
    indexes / editorial ordering metadata
```

No relation is inferred between D1 and D2 cursors.

## 14.1 Preferred compact form: contiguous source-domain consideration cursor

When a source domain provides a stable monotonic projection enumeration token:

```text
coverage(D) = token K
```

means:

> every candidate in D through K was considered by this layer under the applicable projection policy.

Story records themselves retain `source_refs`. A considered source that produced no Story record needs no separate skip record.

This use of order is ingestion/projection order only and has no fictional chronology meaning.

## 14.2 Sparse coverage fallback

If a source domain cannot provide safe contiguous bounded enumeration, use typed sparse coverage/evidence for that domain rather than inventing a universal sequence.

Do not force sparse per-source ledgers where a domain cursor is sufficient.

## 14.3 “Caught up” is basis-relative

For pinned source basis B:

```text
CAUGHT_UP(layer, B)
```

means every required source domain for that layer has coverage sufficient to show all candidates admitted through B were considered.

It does not mean Story is synchronized to one fictional time or one campaign-global event number.

---

# 15. Bounded catch-up without a queue

Provisional restart flow:

```text
1. pin current campaign/Story basis H
2. load StoryLayerProjectionState for target layer
3. resolve current source-domain basis/watermark(s)
4. enumerate bounded next uncovered candidate window(s)
5. if no work -> layer is caught up to that pinned basis
6. assemble exact StorySourceBundle
7. optionally invoke Chronicler/generative transformation
8. validate draft against source manifest and Story availability rules
9. allocate final IDs from current layer allocator
10. publish records + indexes + allocator + coverage atomically
11. on conflict classify movement; retry/rebase/discard draft as appropriate
```

If the process disappears before step 10, no durable progress was claimed; restart simply rediscovers the uncovered window.

If step 10 succeeds, records and coverage become visible together.

---

# 16. Story transaction atomicity — provisional

Within one Story-layer publication, the following belong in one Step-5.6 campaign tree transaction as applicable:

- new/edited/deleted Story records for that layer;
- forward refs/crossrefs that are authoritative for those records;
- layer indexes/availability metadata required to publish them safely;
- layer-local ID allocator advancement;
- layer projection coverage advancement;
- structural correction metadata necessary to prevent dangling refs.

Do not advance coverage if the corresponding record/index/availability closure did not publish.

## INFERENCE

Cross-layer atomicity should **not** be required by default.

Example legal state:

```text
EVENTS coverage = current
MECHANICS coverage = current-ish
NARRATIVE coverage = behind
```

If NARRATIVE generation fails, already-valid EVENTS/MECHANICS remain published.

---

# 17. Layer-local ID allocation under concurrency

Step 4 requires layer-local numeric Story IDs.

Provisional mechanism:

1. generative draft uses temporary local keys, not final `E/M/N/T` IDs;
2. deterministic publisher reads current layer allocator state at publication basis;
3. assigns final IDs and rewrites draft-internal refs deterministically;
4. allocator + records + indexes + coverage publish atomically;
5. CAS conflict on Story allocator state causes repin/remap/revalidation, not gameplay replay.

This avoids burning an LLM retry merely because another Story writer consumed a numeric ID.

If another writer already covered the exact source window, the losing draft may simply be discarded as obsolete.

---

# 18. Same-ref canonical/Story concurrency

Story moves the same campaign ref but is not a gameplay dependency.

Provisional classification:

### Canonical publisher sees Story-only movement

If changed paths are proven Story-only and gameplay context does not consume Story, movement is semantically disjoint. Canonical transaction may mechanically rebuild from the newer tree without replaying mechanics/RNG/LLM adjudication.

### Story publisher sees canonical movement

If canonical movement does not affect:

- target Story layer state;
- pinned source records used by the draft;
- availability dependencies;
- referenced Story records;

then the same validated draft may be mechanically rebased/published on the newer tree.

If dependencies moved, discard/reassemble/revalidate projection work.

### Priority rule

Story has no right to hold gameplay waiting for freshness. Under repeated contention Story may yield and retry on a later activation.

No fairness/starvation guarantee is required for Story projection while gameplay is active.

---

# 19. Save and gameplay recovery

## INFERENCE S1

Explicit gameplay SAVE success must not imply Story is caught up.

Story is not part of Resumable Runtime Closure for gameplay semantics.

## INFERENCE S2

Cold gameplay recovery must not require Story hydration.

Story may be absent/corrupt/behind while gameplay recovery is `READY`, provided no gameplay owner illegally depends on Story.

## INFERENCE S3

A Chronicler restart is a projection recovery problem:

```text
current source basis + current Story layer coverage
-> next bounded projection work
```

not a checkpoint replay problem.

---

# 20. Source retention / compaction interaction

## FACT

Some Story fidelity becomes non-regenerable after exact source deletion.

## INFERENCE R-I1 — unprojected fidelity dependency must be visible to 5.11/5.13

If policy promises that source material should first be represented in Story before exact source deletion, uncovered Story coverage is a retention dependency.

Physical retention/deletion policy belongs to Steps 5.11/5.13.

## INFERENCE R-I2 — `source_refs` need not imply permanent payload retention

A Story record can preserve stable source identity even after source payload becomes unavailable. Exact dereferenceability after compaction is a separate retention promise.

Step 5.11 must decide what compact provenance/tombstone/digest, if any, survives when exact transcript/history is deleted.

Step 5.10 should not force indefinite source retention solely to make every Story source ref dereferenceable forever.

---

# 21. Correction / regeneration observations

Story content is mutable projection, but published IDs/crossrefs still need coherent handling.

Provisional distinction:

```text
CONTENT/EDITORIAL REVISION
    same presentation unit remains recognizable
    -> same Story ID may be edited atomically

STRUCTURAL REWRITE
    split / merge / substantially different unit partition
    -> may allocate new IDs and atomically update affected Story refs/indexes
```

Baseline architecture should not promise immutable external permalinks across arbitrary structural regeneration unless the owner requires that product guarantee.

Layer IDs are never casually reused within surviving Story allocator history.

A projector/model/prompt version change does not automatically invalidate all prior coverage. Historical regeneration is explicit scoped maintenance/editorial work.

---

# 22. Main risks in the leading direction

1. **coverage mistaken for chronology** — mitigated by source-domain typing and explicit “projection enumeration only” semantics;
2. **coverage becomes second source authority** — mitigated by defining it only as “considered through”, never factual truth;
3. **head-of-line blocking with contiguous cursor** — mitigated by bounded retry and sparse fallback only where the source domain proves need;
4. **same-ref Story contention slows canon** — mitigate via low-priority Story activation and proven-disjoint mechanical rebase;
5. **source compaction outruns projection** — must feed 5.11/5.13 retention dependency;
6. **LLM draft gains transport/ID authority** — prohibited by deterministic publisher boundary;
7. **NARRATIVE becomes implicit source for EVENTS/canon** — prohibited by Step 4 non-authority;
8. **future background worker motivates queue creep** — coverage-driven pull must remain sufficient unless measured evidence disproves it.

---

# 23. Preliminary recommendation

Current recommendation, subject to analytical challenge:

> **QUEUE-FREE COVERAGE-DRIVEN / LAYER-INDEPENDENT STORY PROJECTION with deterministic projection control and optional generative Chronicler transformation.**

Key properties:

```text
no required background worker
no durable Story job queue
no Story requirement in gameplay SAVE/RRC
per-layer typed coverage, not global frontier
per-layer allocator
one layer transaction = records + required indexes/availability + allocator + coverage
cross-layer lag is legal
Story loses priority to gameplay
uncovered required source may constrain later compaction
future async worker reuses same pull/catch-up protocol
```

Confidence before challenge: **MEDIUM-HIGH**.

---

# 24. Questions to attack next

The analytical challenge must try to disprove or simplify the recommendation by focusing on:

- whether durable layer coverage is actually necessary or can be derived purely from records/indexes;
- whether contiguous “considered-through” cursor safely represents intentional omission without hiding unresolved work;
- whether separate allocator state is necessary or can reuse an existing admitted allocator without coupling Story to canon;
- whether same-ref Story commits can ever violate the “cannot block gameplay publication” requirement through CAS contention;
- whether cross-layer independence permits spoiler-invalid dangling refs;
- whether Story structural correction needs durable tombstone/supersession semantics now;
- whether exact source compaction creates a stronger owner-level fidelity decision than currently assumed;
- whether plain one-chat role isolation limits should change Story availability/publication semantics or remain Step-6-only.

# Step 5.10 — Story Projection Durability — Canonical Specification

Status: **CANONICAL — STEP 5.10 ARCHITECTURE CLOSED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Canonicalization basis:

- `../design/2026-08-21-step-5-10-story-projection-durability-task-brief.md`
- `../design/2026-08-21-step-5-10-story-projection-durability-research-draft.md`
- `../design/2026-08-21-step-5-10-story-projection-durability-analytical-challenge.md`
- `../design/2026-08-21-step-5-10-story-projection-durability-candidate-spec.md`
- `../design/2026-08-21-step-5-10-story-projection-durability-adversarial-review.md`
- `../design/2026-08-21-step-5-10-story-projection-durability-resolution-gate.md`

Canonical architecture direction:

> **LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL GENERATIVE CHRONICLER / GAMEPLAY-PRIORITY SAME-REF CAS**

This specification defines Story projection durability only. It does not implement Story schemas/runtime code, decide exact transcript retention (Step 5.11), decide host delivery/disclosure acknowledgement (Step 5.12), decide physical GC (Step 5.13), or decide physical six-role model-call topology (Step 6).

---

# 1. Scope and central invariant

Story is a durable but non-canonical read/presentation model.

Canonical/history sources may advance while Story lags. Story may fail, restart, catch up, be corrected or be partially absent without changing gameplay truth or recovery authority.

Central invariant:

> **For each Story layer, durable projection state records only what source candidates have been terminally considered under an exact typed projection contract; canonical/history sources remain authority, Chronicler remains editorial/generative only, and deterministic core owns final IDs, validation, coverage advancement and repository publication.**

Canonical gameplay publication SHALL NOT depend on Story freshness, Story generation or Story publication success.

---

# 2. Inherited Story semantics remain unchanged

The four Step-4 layers remain:

```text
STORY/TRANSCRIPT
STORY/EVENTS
STORY/MECHANICS
STORY/NARRATIVE
```

Story remains:

- durable;
- non-canonical;
- on the campaign branch;
- one-record-per-file by default;
- layer-local in identity/allocation;
- dependency/reveal-availability filtered;
- presentation/history only.

Story records cannot become current world/mechanical state, `world.lore_fact`, `world.knowledge`, `runtime.disclosure`, chronology authority, RRC authority or gameplay execution authority merely by being durable or accurate.

---

# 3. Authority geometry

Canonical authority remains outside Story:

```text
CANONICAL / HISTORICAL SOURCE OWNERS
    world/runtime owners
    runtime.semantic_event / LOG
    runtime.mechanical_event / receipts
    participant-message/delivery evidence
    other admitted historical/provenance sources

SOURCE PROJECTION DOMAIN CONTRACT
    candidate enumeration semantics
    source-domain watermark/cursor interpretation
    semantic projection-contract generation
    terminal candidate disposition requirements

STORY LAYER PROJECTION STATE
    durable non-canonical projection progress/identity metadata
    layer allocator high-water
    typed source-domain coverage
    required Story layer indexes/order metadata

CHRONICLER LOGICAL ROLE
    editorial/generative transformation only

DETERMINISTIC STORY CONTROL/PUBLISHER
    source selection
    exact basis pinning
    validation
    final Story ID allocation
    ref/availability validation
    complete Story write-set construction
    Step-5.6 repository publication
    coverage advancement
```

## LAW 5.10-1 — NO STORY-TO-CANON AUTHORITY FLOW

Story content, indexes, reading order, projection coverage and Chronicler output SHALL NOT be used as gameplay semantic authority.

---

# 4. Baseline deployment constraint

The Step-5.10 semantic protocol must remain correct in the minimal deployment profile:

> **one ordinary sequential ChatGPT conversation/execution stream, with no required ChatGPT Work usage, no Pro/Enterprise-only dependency, and no permanently running independent/background Story worker.**

Current platform specifics are time-sensitive and must be reverified in Step 6.

## LAW 5.10-2 — NO BACKGROUND-WORKER CORRECTNESS DEPENDENCY

Story durability SHALL NOT require work to continue after the current assistant turn ends.

If no safe/available projection activation occurs, Story simply remains behind.

Step 6 may later run the same semantic protocol inline, in a separate model call, through an API/agent orchestrator or in another supported execution profile.

## LAW 5.10-3 — PHYSICAL ROLE TOPOLOGY DOES NOT OWN PROJECTION PROGRESS

Whether Chronicler is an LLM call, deterministic transform, separate invocation or future worker cannot change Story coverage/ID/publication authority rules.

---

# 5. Source projection domains

Projection work is enumerated in typed source domains.

Conceptually each admitted layer/source pair provides:

```text
StoryProjectionSourceContract
    layer
    source_domain_id
    semantic_contract_generation
    enumeration semantics
    terminal disposition semantics
    optional mapping/cardinality constraints
```

A source domain may be based on append-only log/message/mechanical evidence or another owner-defined source surface that can provide bounded stable projection enumeration.

## LAW 5.10-4 — PROJECTION ORDER IS DOMAIN-LOCAL AND NONFICTIONAL

A projection source cursor/token orders only candidate enumeration in its declared source domain.

It does not establish:

- fictional chronology;
- causal order;
- simultaneity;
- narrative reading order;
- order against a different source domain;
- order against another Story layer.

Git/ref/commit order does not gain fictional meaning from projection use.

## LAW 5.10-5 — CAMPAIGN HEAD IS TRANSPORT PIN, NOT SOURCE WATERMARK

Campaign HEAD may pin the tree used for one exact read/publication attempt, but it SHALL NOT serve as the Story projection source watermark merely because it advanced.

Story-only commits therefore do not create new source backlog.

Catch-up compares coverage only against owner-defined source-domain basis/watermarks.

---

# 6. Projection-contract generation

Coverage semantics depend on the exact **semantic** projection contract used to define candidates and terminal disposition.

## LAW 5.10-6 — COVERAGE IS CONTRACT-GENERATION TYPED

Conceptually:

```text
CoverageEntry
    layer
    source_domain_id
    semantic_contract_generation
    coverage cursor/evidence
```

A semantic contract change that may alter already-covered candidate admission, source-enumeration meaning, terminal disposition or required output cardinality cannot silently inherit old coverage.

It requires explicit compatible migration/reprojection/reset semantics for the affected domain.

## LAW 5.10-7 — MODEL/PROMPT VERSION IS NOT COVERAGE GENERATION

Changing model, prompt wording, style policy or projector implementation does not by itself make prior source candidates unconsidered.

Historical regeneration after quality/tool changes is explicit scoped editorial/maintenance work.

Optional projector/model provenance may be recorded for diagnostics, but it is not coverage authority.

## LAW 5.10-8 — INCOMPATIBLE GENERATION MOVEMENT IS A REAL DEPENDENCY CONFLICT

A Story writer freezes the semantic projection-contract generation used for every coverage entry it intends to advance.

If current layer state moved to an incompatible generation before publication, deterministic core must migrate/reassemble/reproject as required. It SHALL NOT advance old coverage by allocator-only remapping.

---

# 7. Source enumeration monotonicity

Contiguous cursor coverage is preferred only where the source owner can prove stable append-monotonic projection enumeration.

## LAW 5.10-9 — NO LATE INSERTION BEHIND A VALID CURSOR

For a cursor-capable source domain, ordinary newly accepted projection candidates cannot later appear behind a previously accepted cursor under the same semantic contract generation.

A late-established historical relation/fact may concern old fictional time while still entering as new source evidence at a later projection-enumeration position.

If a source cannot provide this property, use a typed bounded sparse coverage mechanism instead of inventing a total sequence.

---

# 8. Candidate terminal disposition

Each admitted source candidate must reach an allowed terminal disposition before coverage passes it.

Baseline semantic classes:

```text
MUST_MATERIALIZE
MAY_OMIT
```

The layer/source contract may impose narrower mapping/cardinality validation where concrete requirements justify it.

## LAW 5.10-10 — COVERAGE ADVANCES ONLY AFTER LEGAL TERMINAL DISPOSITION

For `MUST_MATERIALIZE`, required compatible durable Story output must publish coherently with coverage advancement.

For `MAY_OMIT`, a considered candidate may lawfully produce no Story record.

Generation failure, transport failure, missing required source or unresolved source integrity is not intentional omission and cannot advance coverage past that candidate.

## LAW 5.10-11 — NO GENERIC PER-SOURCE SKIP LEDGER REQUIRED

When a contiguous source-domain cursor proves that every candidate through K was considered, omitted `MAY_OMIT` candidates require no separate durable skip record.

Introduce sparse gap/skip machinery only for a source contract that proves the need.

---

# 9. StoryLayerProjectionState

Each Story layer owns compact durable projection-local state conceptually containing:

```text
layer identity
layer Story-ID allocator high-water
coverage_by_source_domain[]
required layer indexes / editorial ordering metadata
```

This state is non-canonical but necessary for bounded idempotent projection catch-up.

## LAW 5.10-12 — STORY PROJECTION STATE STAYS UNDER STORY OWNERSHIP

Mutable Story progress SHALL NOT be stored as ordinary fields in:

```text
MANIFEST
STATE/CURRENT
checkpoint/RRC state
canonical runtime ID allocator
```

A campaign manifest may later contain a static `story_root` storage-routing field established by scaffold/migration, but ordinary Story catch-up does not mutate MANIFEST merely to advance projection progress.

This preserves Story-only path disjointness from ordinary gameplay authority.

## LAW 5.10-13 — PROJECTION STATE IS NOT GAMEPLAY RRC

Loss/corruption of Story projection state may damage Story catch-up/fidelity, but gameplay recovery remains independent unless an illegal gameplay dependency on Story exists.

---

# 10. Queue-free backlog and catch-up

Backlog is derived from:

```text
current typed source-domain basis/watermark
    minus
compatible Story-layer coverage
```

No durable `StoryProjectionJob`, worker-claim ledger or scheduler is baseline authority.

Conceptual bounded catch-up:

```text
1. pin current campaign tree for exact reads/transport
2. load target Story layer projection state
3. resolve compatible semantic projection contract generation
4. resolve current source-domain basis/watermark(s)
5. enumerate bounded uncovered candidate window
6. assemble StorySourceBundle
7. transform/curate candidates if required
8. validate StoryProjectionDraft
9. allocate/remap final Story IDs
10. validate refs/availability/index closure
11. publish one coherent Story-layer transaction
12. advance allocator/coverage atomically with output
```

## LAW 5.10-14 — ACTIVATION POLICY DOES NOT BECOME DURABILITY AUTHORITY

Exact projection frequency/timing is not fixed by Step 5.10.

Possible activations include foreground opportunity, explicit Story/Commentator demand, session/maintenance boundary, retention prerequisite or future async worker.

Story correctness depends on source/coverage state, not on a timer or assumed worker presence.

---

# 11. Deterministic control and Chronicler boundary

## StorySourceBundle

Conceptually includes:

```text
layer
campaign transport pin
source-domain contract generation(s)
source-domain basis/window(s)
eligible source material/excerpts
exact source_manifest[]
existing Story refs/index excerpts required for editorial continuity
availability inputs required for validation
```

The transport pin and source-domain watermarks remain distinct concepts.

## StoryProjectionDraft

Conceptually includes:

```text
layer
records keyed by temporary local draft keys
content
source_refs[]
Story refs/crossrefs[]
entity_refs[]
availability requirements
permitted editorial/index proposals
```

## LAW 5.10-15 — CHRONICLER DOES NOT OWN FINAL IDS OR PROGRESS

Chronicler may group, summarize, select, qualify and rewrite occurred evidence within Step-4 rules.

It SHALL NOT directly own:

- final Story ID allocation;
- layer allocator mutation;
- source coverage advancement;
- repository transport/conflict resolution;
- catch-up completion claims;
- canon/truth promotion.

## LAW 5.10-16 — DETERMINISTIC TRANSFORM IS ALLOWED

A Story layer/operation may be realized without an LLM call where its accepted transformation contract is deterministic.

Step 5.10 therefore does not require one Chronicler call per layer, source candidate or gameplay turn.

---

# 12. Story ID allocation

Step-4 Story IDs remain layer-local:

```text
T...
E...
M...
N...
```

## LAW 5.10-17 — DRAFT KEYS PRECEDE FINAL IDS

Generative/editorial drafts use temporary local keys. Final layer-local IDs are assigned by deterministic publication control against current allocator state.

Draft-local refs are rewritten deterministically before publication.

## LAW 5.10-18 — ALLOCATOR ADVANCES WITH RECORD CLOSURE

New Story IDs, record files, required indexes/refs/availability, allocator advancement and applicable coverage advancement publish in one coherent Story transaction.

## LAW 5.10-19 — STORY IDS ARE NOT REUSED NORMALLY

Layer allocator high-water is monotonic. Ordinary deletion/revision does not return Story IDs to the pool.

Formatting width remains minimum-only and may expand.

A destructive identity-reset maintenance operation, if ever introduced, must explicitly invalidate all affected Story refs/cursors; it is not baseline behavior.

---

# 13. Layer-local publication atomicity

Ordinary catch-up publishes one Story layer closure at a time.

One layer transaction may include as applicable:

- new Story records;
- corrected records;
- safe deletions;
- layer indexes/order metadata;
- availability metadata;
- Story refs/crossrefs owned by the changed records;
- layer allocator advancement;
- source-domain coverage advancement.

Publication uses the existing Step-5.6 single-ref CAS campaign transaction protocol.

## LAW 5.10-20 — OUTPUT/COVERAGE CRASH COHERENCE

A ref-selected Story transaction exposes old coherent layer projection state or new coherent layer projection state.

Coverage cannot publish ahead of required `MUST_MATERIALIZE` output/index/availability closure.

A coverage-only Story commit is legal when it advances real `MAY_OMIT` consideration state; it is not a no-op merely because no Story record was added.

## LAW 5.10-21 — NO MANDATORY CROSS-LAYER ATOMICITY FOR NORMAL CATCH-UP

TRANSCRIPT, EVENTS, MECHANICS and NARRATIVE may lag/publish independently.

Failure of NARRATIVE cannot roll back or block valid EVENTS/MECHANICS/TRANSCRIPT projection, and no Story-layer failure can roll back canon.

Cross-layer Story maintenance may use one coherent transaction only when an explicit structural edit must update existing cross-layer refs safely.

---

# 14. Story reference closure

## LAW 5.10-22 — NO PUBLISHED DANGLING STORY REF

A new Story ref may target:

- an already-durable Story record at the pinned Story basis; or
- a target created in the same coherent Story transaction where resolution is deterministic.

For ordinary layer-local catch-up, a cross-layer target must already be durable.

## LAW 5.10-23 — STORY-TO-STORY REFS DO NOT PROMOTE PROSE TO FACTUAL AUTHORITY

Story-to-Story refs are presentation/navigation/editorial dependencies.

Material factual compatibility remains traceable to authoritative/historical source evidence under Step 4.

Lower Story prose is not promoted to canon merely because NARRATIVE references it.

## LAW 5.10-24 — REVERSE INDEXES ARE DERIVATIVE UNLESS EXPLICITLY OWNED

Reverse crossref/dependency indexes may support bounded retrieval or structural correction, but do not become authority over the underlying Story relation.

---

# 15. Availability / spoiler closure

Step-4 whole-unit availability rules remain canonical.

## LAW 5.10-25 — SPOILER-BEARING METADATA PUBLISHES WITH COMPATIBLE AVAILABILITY

Story body, title, labels, entity refs, crossrefs, chapter/index entries and any spoiler-bearing metadata must not publish under stale/incompatible availability requirements.

Material Story edit requires availability recomputation/revalidation before publication.

## LAW 5.10-26 — STORY AVAILABILITY IS NOT DISCLOSURE

Story eligibility does not create `runtime.disclosure`, fictional knowledge or objective truth.

---

# 16. Caught-up / lag semantics

For pinned typed source-domain basis B:

```text
CAUGHT_UP(layer, B)
```

means every required source domain for that layer has compatible coverage proving terminal consideration of candidates admitted through B.

## LAW 5.10-27 — CAUGHT_UP IS LAYER/DOMAIN/BASIS RELATIVE

It does not mean:

- all canon is represented;
- all Story layers are equally fresh;
- Story reached one fictional time;
- one campaign-global event sequence is complete.

## LAW 5.10-28 — RETRIEVAL MAY SURFACE LAG STATUS

Story/Commentator retrieval may expose typed layer lag/coverage status so absence in a known-lagging projection is not presented as proof of historical nonexistence.

Exact UI/automatic catch-up policy belongs to Step 6.

---

# 17. Crash / restart / ambiguous acknowledgement

## 17.1 Crash before publication

Unpublished draft is non-authoritative and may disappear. Coverage remains unchanged; work is rediscovered.

## 17.2 Confirmed Story publication

Records/indexes/allocator/coverage advance together; restart continues after current compatible coverage.

## 17.3 Indeterminate ref outcome

Do not blindly republish.

Read current layer projection state and verify contract-generation compatibility.

```text
compatible current coverage already passes intended source window
    -> source work already terminally considered
    -> suppress duplicate draft publication

coverage not advanced
    -> continue/retry from actual current Story/source basis

contract generation incompatible
    -> migration/reassembly path
```

## LAW 5.10-29 — COVERAGE IS CATCH-UP IDEMPOTENCY EVIDENCE

No separate durable Story projection-run/job identity is required baseline to suppress duplicate catch-up.

If current Story projection already validly covered a source window with different prose from another writer, the losing unpublished draft has no authority claim.

---

# 18. Same-ref concurrency with canonical gameplay

Story and canon share one campaign ref, so transport contention can occur.

## LAW 5.10-30 — GAMEPLAY NEVER WAITS FOR STORY FRESHNESS OR LOCK

Canonical gameplay publication, explicit SAVE and gameplay recovery SHALL NOT wait for:

- Story catch-up;
- Chronicler generation;
- Story publication success;
- Story worker/claim/lease.

No such lock/lease is authorized baseline.

## LAW 5.10-31 — VERIFIED STORY-ONLY MOVEMENT IS DISJOINT FROM ORDINARY GAMEPLAY AUTHORITY

If branch movement is proven to touch only Story-owned projection paths and no ordinary gameplay dependency consumes Story, Step-5.6 may mechanically rebuild the frozen gameplay transaction on the newer base.

Accepted gameplay IDs/mechanics/RNG/execution are preserved. Story-only ref movement never justifies gameplay replay/re-adjudication.

It may cost a bounded transport retry; it does not create a semantic Story dependency.

## LAW 5.10-32 — STORY YIELDS UNDER REPEATED CONTENTION

Story has no freshness priority over gameplay. After bounded conflict/revalidation attempts, Story projection may abandon current work and retry on a later activation.

No Story starvation-freedom guarantee is required during sustained canonical activity.

---

# 19. Canon movement during Story work

## LAW 5.10-33 — STORY DRAFT REUSE IS DEPENDENCY-AWARE

If campaign movement does not touch:

- target Story layer state;
- semantic projection-contract generation;
- source records/evidence in the bundle manifest;
- referenced Story records;
- availability dependencies;

then deterministic core may reuse/rebase the same validated draft against the new tree without repeating generation.

If relevant dependencies moved, revalidate/remap or discard/regenerate from current state.

---

# 20. Future multiple Story workers

Step 6 may later provide multiple/async projection workers.

They use the same coverage/allocator/CAS protocol.

Same-layer race:

```text
worker A + B pin same layer state
A wins CAS
B refreshes
    source window already covered -> discard B draft
    otherwise -> remap/revalidate/regenerate against current state
```

Different-layer movement may be mechanically rebased when all refs/dependencies remain compatible.

## LAW 5.10-34 — NO WORKER LEASE/QUEUE IS IMPLIED BY FUTURE CONCURRENCY

Future worker concurrency alone does not justify adding projection claims/jobs/leaders to source-of-truth architecture.

Such machinery requires a separate demonstrated need.

---

# 21. SAVE / gameplay recovery separation

## LAW 5.10-35 — SAVE DOES NOT PROMISE STORY CATCH-UP

Successful explicit gameplay SAVE proves only the Step-5.5 gameplay durability closure.

Story may remain arbitrarily behind.

## LAW 5.10-36 — STORY IS OUTSIDE GAMEPLAY RRC

Gameplay cold recovery may return `READY` while Story is behind, missing or projection-corrupt, provided no gameplay owner illegally depends on Story.

## LAW 5.10-37 — CHRONICLER RESTART IS PROJECTION RECOVERY

Restarted projection derives next work from:

```text
current typed source-domain basis
+ compatible current Story-layer projection state
```

No raw model memory, gameplay checkpoint replay or global timeline reconstruction is required.

---

# 22. Retention / compaction handoff to Steps 5.11 and 5.13

Step 5.10 closes the projection-side contract; physical source retention belongs later.

## LAW 5.10-38 — RETENTION MAY REQUIRE TYPED STORY PROJECTION CLOSURE

If Step 5.11 policy promises that source candidate S must be represented in a Story layer before exact source deletion, compaction must prove the required terminal projection disposition under the compatible projection contract before deleting S.

Do not block source deletion on unrelated Story layers.

## LAW 5.10-39 — SOURCE CURSOR CONTINUITY MUST SURVIVE LAWFUL COMPACTION

Compaction must not preserve a Story coverage token while destroying the ability to interpret/resume it.

For each affected source projection domain, at least one must hold:

```text
cursor remains interpretable after compaction
OR
compact enumeration anchor/index survives
OR
coverage is coherently migrated to a compatible successor token
```

Exact retained artifact/migration is owned by Steps 5.11/5.13.

## LAW 5.10-40 — SOURCE REF IDENTITY != PERMANENT SOURCE PAYLOAD

Story `source_refs` preserve stable provenance identity attribution.

They do not alone promise permanent dereferenceability of full source payload after lawful retention/GC.

A stronger post-compaction provenance promise requires an explicit Step-5.11/5.13 retained artifact.

---

# 23. Transcript boundary handoff

TRANSCRIPT projection is close to deterministic copying but exact candidate admission is not owned entirely by 5.10.

## LAW 5.10-41 — GENERATED TEXT IS NOT AUTOMATICALLY TRANSCRIPT

A generated Narrator/participant-facing string does not become a retained Transcript candidate merely because it exists in process memory.

Step 5.11 and Step 5.12 must define the admitted participant-message/exact-retention/delivery evidence.

A generated-but-never-emitted response must not be retained as delivered participant transcript through Story projection.

Once a Transcript candidate is validly admitted, Step-5.10 coverage/materialization rules govern its projection.

---

# 24. Correction / regeneration

Story remains editable non-canonical presentation.

Conceptual edit classes:

```text
EDITORIAL_REVISION
    same independently addressable presentation unit
    -> edit same Story ID

STRUCTURAL_REWRITE
    split/merge/repartition/delete presentation units
    -> allocate new IDs where needed
    -> preserve Story internal ref/index closure
```

## LAW 5.10-42 — STORY EDIT NEVER REWRITES CANON TO MATCH PROSE

Correction/regeneration uses current admissible source evidence; it cannot alter authoritative history/world state to preserve Story text.

## LAW 5.10-43 — STRUCTURAL EDIT MUST PRESERVE PUBLISHED STORY REF CLOSURE

Structural edits may use a bounded cross-layer Story maintenance transaction when existing refs/indexes require coherent updates.

Baseline does not require a universal Story tombstone/supersession system or stable public permalink guarantee across arbitrary structural regeneration.

Story IDs remain non-reusable.

## LAW 5.10-44 — COVERAGE DOES NOT REWIND FOR ORDINARY EDITORIAL REVISION

Editing/regenerating already-covered Story content does not by itself make source candidates unconsidered.

If a semantic projection-contract change retroactively changes candidate/disposition requirements, use the explicit contract-generation migration path from Section 6 instead.

---

# 25. Story-to-Story factual boundary

## LAW 5.10-45 — LOWER STORY PROSE IS NOT FACTUAL SOURCE AUTHORITY

NARRATIVE may cite/link EVENTS/MECHANICS/TRANSCRIPT for presentation/editorial continuity, but factual Story claims remain compatible with authoritative/historical source evidence.

A lower-layer wording edit therefore does not automatically require a campaign-wide downstream Story invalidation graph solely because another record linked to it.

Structural link integrity still must be preserved.

A real canonical/source correction enters through its owning source domain and can trigger bounded Story correction/catch-up as required.

---

# 26. Story loss / deletion / regeneration

Deleting Story cannot alter gameplay canon.

If Story records/projection state are lost:

- gameplay remains governed by canonical sources;
- Story can rebuild only from still-retained sources;
- exact fidelity unavailable after lawful source compaction is not invented;
- Commentator/Story features degrade truthfully;
- layer allocator high-water should survive ordinary controlled record cleanup to prevent ID reuse.

An uncoordinated destructive deletion of projection metadata may create Story integrity/identity degradation but still not gameplay corruption.

---

# 27. Story integrity classification

Examples of Story projection defects:

```text
coverage advanced past missing required MUST_MATERIALIZE output
published Story ID above allocator high-water
published Story ref target missing
availability/index metadata exposes ineligible content
coverage contract generation missing/incompatible
source cursor cannot be interpreted under declared source contract
Story record source_ref points to invalid/unresolvable identity unexpectedly
mutable Story progress leaked into canonical CURRENT/MANIFEST state
```

Story integrity repair must not invent canon.

If investigation reveals underlying source/canonical corruption, that source enters its normal integrity protocol independently.

---

# 28. Per-layer disposition notes

## TRANSCRIPT

- exact retention/admission policy is Step 5.11/5.12;
- deterministic copy is allowed;
- retained exact-message candidates may use stronger `MUST_MATERIALIZE` cardinality.

## EVENTS

- projection of SemanticEvent/LOG evidence into human-meaningful beats;
- many-to-one, one-to-many and omission may be allowed by its contract;
- presentation order is not fictional chronology authority.

## MECHANICS

- projects material human-relevant mechanics, not every MechanicalEvent by default;
- future deterministic relevance metadata may reduce LLM work, but is not assumed complete by 5.10.

## NARRATIVE

- most editorial/generative and most tolerant of lag;
- failure cannot block lower Story layers or canon;
- may use durable Story refs for editorial structure but cannot promote lower Story prose to fact authority.

---

# 29. Performance and token contract

Ordinary gameplay requires **zero Story work** for correctness.

One projection activation is bounded to:

```text
one target layer projection state
+ bounded source candidate window(s)
+ bounded source/Story dependencies
+ optional bounded Chronicler generation
+ one Story publication transaction
```

Baseline ordinary operation must not require:

```text
full campaign history scan
all-Story scan
all-layer rebuild
one Chronicler call per gameplay turn
continuous background polling
Story job queue drain
model/prompt-upgrade replay
campaign-global projection frontier
```

---

# 30. Current machine/runtime disposition

Architecture closure does not implement the new Story machine surfaces.

Current known implementation gaps include:

- campaign template has no `STORY/` tree yet;
- MANIFEST schema has no static `story_root` routing field;
- no Story record schemas;
- no Story layer projection-state schema;
- no source projection-domain/coverage protocol;
- no Story-local allocator;
- no deterministic StorySourceBundle/StoryProjectionDraft machine contract;
- no Story conflict classification in Python RepositoryPort realization;
- no Commentator lag-status machine representation.

These are machine-realization debt, not reasons to reopen Step 5.10 semantics.

The eventual `story_root` path belongs to static storage routing. Mutable Story coverage/allocator state remains under Story-owned paths and does not go into CURRENT/RRC.

---

# 31. Machine-realization debt

Later implementation planning must cover at least:

1. static Story root routing/scaffold/migration;
2. four Story layer record/index formats;
3. StoryLayerProjectionState representation;
4. layer-local non-reusing allocator high-water;
5. typed source projection-domain registry/contracts;
6. semantic projection-contract generation compatibility/migration;
7. bounded append-monotonic candidate enumeration;
8. sparse coverage fallback only where required;
9. candidate disposition/cardinality contracts;
10. StorySourceBundle protocol;
11. StoryProjectionDraft temporary-key protocol;
12. deterministic final-ID remapping;
13. whole-unit availability validation;
14. complete Story-layer publication planning through Python RepositoryPort;
15. Story-only movement disjoint classification for gameplay transactions;
16. dependency-aware Story draft reuse after canon movement;
17. ambiguous Story acknowledgement resolution from coverage;
18. Commentator/retrieval lag-status representation;
19. structural correction/no-dangling-ref tooling;
20. Step-5.11 projection-before-delete and cursor-continuity integration;
21. Step-5.12 Transcript delivery-candidate integration;
22. Story-specific integrity/repair tooling;
23. future multi-worker concurrency tests without adding queue authority;
24. no-background/no-all-history-scan/token-budget tests;
25. Step-6 physical role-call topology preserving these semantics.

No broad implementation begins until the architecture sequence reaches its normal planning gate.

---

# 32. Required regression/adversarial realization cases

Later tests must include at least:

```text
canonical gameplay advances with no Story work
Story lags across many gameplay publications
cold gameplay recovery succeeds with Story missing
Chronicler restart derives backlog from compatible layer coverage
campaign Story-only commit does not advance source-domain watermark
projection contract generation expands candidate set and requires migration
model/prompt change alone does not reset coverage
append-monotonic late historical evidence enters after cursor despite old fictional date
MAY_OMIT candidate advances coverage without Story record
MUST_MATERIALIZE candidate cannot advance without required output
one Story record covers several source items
one source candidate creates several Story records where contract permits
independent source-domain cursors cannot be compared
EVENTS current while NARRATIVE lags
NARRATIVE failure does not block canon/lower layers
Story generation succeeds then loses CAS to canon-only movement
validated Story draft reused after proven-disjoint canon movement
same-layer concurrent Story writer wins; loser suppresses duplicate by coverage
incompatible projection-contract generation cannot be remapped as allocator conflict
Story-only movement causes gameplay transport rebuild without mechanics/RNG replay
indeterminate Story ACK resolved using compatible current coverage
coverage-only commit for omitted batch is real projection-state change
new cross-layer Story ref requires durable target
availability metadata publishes coherently with protected record/index
structural Story edit leaves no dangling refs
Story IDs are not reused after record deletion
SAVE succeeds while Story is far behind
source deletion waits for typed Story closure only when 5.11 policy requires it
source compaction preserves/migrates cursor continuity
source_ref identity survives while full payload may be compacted
unemitted generated narration cannot become delivered Transcript candidate
full Story loss never changes canon
no ordinary projection performs all-history/all-Story scan
plain-chat deployment remains correct with no background worker
future async/multi-worker deployment reuses same coverage/CAS protocol
```

---

# 33. Canonical closure

Step 5.10 architecture is closed with the following final statement:

> **Story is a layer-independent, eventually/opportunistically maintained non-canonical read model. Backlog is derived from typed source-domain basis minus compatible durable layer coverage, not from a job queue. Deterministic core owns projection selection, final Story identity, validation, coverage and same-ref publication; Chronicler owns only admissible editorial/generative transformation. Story may lag or fail indefinitely without blocking gameplay, and restart/multiple future workers use the same coverage/CAS protocol without duplicate or invented Story.**

No material owner decision remains open in Step 5.10.

Next architecture slice after roadmap/status verification:

**Step 5.11 / Transcript & History Retention and Compaction.**

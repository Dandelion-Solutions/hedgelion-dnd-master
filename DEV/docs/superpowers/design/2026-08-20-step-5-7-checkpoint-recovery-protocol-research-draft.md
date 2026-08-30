# Step 5.7 — Checkpoint / Recovery Protocol — Research Draft

Status: **RESEARCH / PRE-DECISION**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Executive finding

The strongest architecture supported by current canonical constraints is:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-ASSISTED RECOVERY**

Ordinary cold recovery should begin from the current selected campaign authoritative ref, resolve current native ownership/routing from that pinned campaign revision, pin each participating native mutable source to an exact revision, hydrate only the bounded Step-5.2 recovery closure, rebuild derived state, and release resume only after compatibility/integrity/RRC validation.

Checkpoint should remain optional immutable recovery evidence/acceleration. It may provide hints, provenance and historical support evidence, but it must not select an older authority merely because it is the latest checkpoint, and ordinary recovery must remain correct when no checkpoint exists.

The current checkpoint v2 schema predates the canonical Step-5.1–5.6 model and contains several fields that should not survive unchanged into machine realization.

## 2. Verified repository facts

### 2.1 Canonical Step 5.1

`DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md` establishes:

- every correctness-relevant revision/frontier is domain typed;
- independent domains have no implicit common ordering;
- there is no universal recovery frontier or global scalar sequence.

### 2.2 Canonical Step 5.2

`...step-5-2-resumable-runtime-closure-canonical-spec-v2.md` establishes:

- RRC is a property over compatible native durable sources plus bounded typed recovery routing;
- checkpoint is not current-state authority and cannot be the sole active-root source;
- mutable sources are hydrated from exact pinned revisions;
- owning-scope resolution forbids stale cross-domain fallback;
- non-settled RuntimeCommand, active Procedure and conditionally promised unresolved accepted input may independently need root discoverability;
- every armed independently-due temporal source remains enrolled for its armed lifetime;
- Resolution/Continuation/pending children may be reached transitively from admitted roots;
- derived runtime indexes/caches rebuild;
- lost unpublished volatile state is not reconstructed.

### 2.3 Canonical Steps 5.3–5.6

Relevant inherited consequences:

- accepted temporal occurrence/execution identity must not duplicate after restart;
- fixed accepted RNG/choices remain execution evidence, not regenerated transport retries;
- controlled handoff success requires actual durable RRC;
- save does not imply checkpoint creation;
- campaign publication success is determined by actual authoritative ref publication;
- a crash after remote publication but before local bookkeeping must recover from actual durable authority;
- partial success in one native durability domain remains real authority;
- no force-push rollback or distributed transaction is available as recovery repair.

### 2.4 Current checkpoint schema is older than those laws

`GAME/SCHEMA/checkpoint.schema.yaml` v2 currently requires:

```text
schema_version
id
campaign_id
valid_through_event_id
state
```

and may contain:

```text
created_at
expected_commit_sha
world_time
state.current_state_path
state.active_pc_ids
state.active_thread_ids
state.active_scene_ids
recovery_notes
engine
schema_data_version
```

The template mirrors this shape.

### 2.5 Current MANIFEST checkpoint pointer

`GAME/SCHEMA/campaign_manifest.schema.yaml` contains `last_checkpoint_id` and describes it as the sole latest-checkpoint pointer. It also correctly states that checkpoint payloads are immutable recovery projections rather than current-state authority.

### 2.6 Current runtime prose is mixed

`GAME/CORE/STORAGE.md` and `SESSION.md` already move toward the newer architecture:

- checkpoint is sparse recovery evidence/descriptor;
- normal persistence does not automatically create a checkpoint;
- checkpoint pointer is not a universal frontier.

However `BOOTSTRAP_RUNTIME.md` still contains older checkpoint/hot-state ordering/canon-priority wording that can be read as checkpoint-first recovery.

### 2.7 Current Step-3 machine owners contain genuine recovery state

Examples:

- `runtime-command-state.schema.json` owns accepted command disposition and pending child invocation descriptors;
- `runtime-continuation-state.schema.json` owns generation, fixed RNG results, prior exports, receipt refs, dependency refs, pending player response, and safe recompute phase;
- `runtime-procedure-state.schema.json` owns procedure-local participant resource state.

These are native state owners. Checkpoint must not copy their payloads as an alternate authority.

### 2.8 Machine realization is incomplete relative to Step 5.2

Current machine schemas do not yet provide the full typed, scope-partitioned recovery-routing representation required by canonical 5.2. In particular:

- Procedure schema has no explicit lifecycle/status field sufficient by itself to decide active root membership;
- no canonical machine manifest currently represents every Step-5.2 independent operational root class;
- checkpoint v2 active PC/thread/scene lists are not a substitute for Command/Procedure/temporal/accepted-input root routing.

This is implementation debt, not evidence that checkpoint should absorb those responsibilities.

### 2.9 Integrity architecture is already suitable for recovery diagnosis

`GAME/CORE/INTEGRITY.md` / `DEV/TESTS/INTEGRITY_CASES.md` already distinguish:

```text
CANON_OK
CANON_SUSPECT
CANON_CORRUPT
```

and require bounded, scope-local diagnosis. Stale local state or a moved branch is explicitly not corruption when latest current sources are coherent.

Therefore 5.7 should not create a second corruption taxonomy.

### 2.10 Current live-scene prose exposes future dependency only

Current live architecture says active live branch state is current authority for its owned scope, pointed missing live branch is suspect, and orphan unpointed live branch is not authority. Exact final fencing/absorption semantics remain Step 5.8.

5.7 therefore needs a generic interface:

```text
campaign routing says scope S is owned by native source L
    -> recovery resolves/pins current valid L source
```

without deciding 5.8's epoch-transition protocol.

## 3. Constraints

1. Ordinary cold recovery targets the latest actually authoritative recoverable state, not an arbitrary historical checkpoint.
2. No one checkpoint/revision/event ID may become a universal cross-domain frontier.
3. Recovery must be bounded by typed roots/dependencies rather than campaign/world/history scans.
4. Every mutable participating source is exact-revision pinned during one attempt.
5. Current owning-scope routing wins over stale checkpoint hints.
6. Checkpoint absence must not make an otherwise complete RRC unrecoverable.
7. Checkpoint corruption must not by itself imply canon corruption when current native sources/routing are independently healthy.
8. Conversely, a valid checkpoint cannot excuse missing/corrupt current required native authority.
9. Derived state is rebuilt, not persisted merely for recovery convenience.
10. Recovery must distinguish unavailable/incompatible from confirmed corruption.
11. Source movement during hydration is normal concurrency, not automatically corruption.
12. No recovery path may replay accepted gameplay to rediscover a publication result.
13. Historical rollback/support semantics must not distort ordinary current recovery.

## 4. Assumptions to challenge

### A1 — Campaign HEAD is always sufficient current anchor

False if read alone. Campaign H may identify routes to live/native operational sources and therefore only anchors discovery of a composed current view.

### A2 — “Latest checkpoint” means latest recoverable gameplay state

False under multi-domain authority and optional checkpoints. A checkpoint can be older than current campaign/live authorities.

### A3 — A checkpoint can contain the SHA of the commit that contains it

Not straightforward for a content-addressed Git commit: changing checkpoint bytes changes tree and commit identity. `expected_commit_sha` therefore cannot be a normal same-transaction self-reference.

### A4 — One event ID can express recovery coverage

Rejected by Step 5.1/5.2 unless the field is explicitly narrowed to an event-domain-only claim. It cannot prove campaign/live/runtime/chronology closure.

### A5 — A checkpoint-local world time is harmless metadata

It is harmless only as an explicitly non-authoritative observed chronology hint. If used to choose current chronology or decide due work, it duplicates chronology ownership and risks cross-domain flattening.

### A6 — Checkpoint should list all active owners

Not necessarily. Step 5.2 requires current native routing to own bounded discovery. Duplicating every active root in an immutable checkpoint immediately creates staleness and completeness hazards.

### A7 — Recovery must always use the newest native source independently

Too strong. “Newest” may be undefined across domains, and a newer source can be incompatible with another pinned source. Recovery needs current owning-source resolution plus compatibility validation, not independent max selection.

## 5. Alternative A — CHECKPOINT-FIRST HISTORICAL CUT

Shape:

```text
MANIFEST.last_checkpoint_id
    -> checkpoint
    -> checkpoint-selected campaign/live/runtime revisions
    -> hydrate exact historical composition
```

### Benefits

- mechanically simple anchor;
- repeatable historical replay if all referenced revisions are retained;
- natural support/rollback semantics;
- easy mental model for diagnostics.

### Problems

- stale checkpoint silently discards later valid durable state unless recovery then “rolls forward”;
- making it complete enough for correctness tends to turn checkpoint into a universal RecoveryCut record explicitly rejected by Step 5.1/5.2;
- current operational root enrollment after checkpoint would require scanning/roll-forward anyway;
- multi-domain “latest checkpoint” cannot prove latest current authority;
- checkpoint absence becomes artificial recovery failure;
- frequent checkpointing would be needed to bound loss of routing changes, recreating snapshot/heartbeat pressure;
- self-reference and retention complexity grows if exact containing commit is encoded.

**Assessment: reject for ordinary recovery.**

It remains useful as an explicit historical-maintenance concept if retained exact sources make it possible.

## 6. Alternative B — CURRENT-AUTHORITY-FIRST / CHECKPOINT-ASSISTED — RECOMMENDED

Shape:

```text
selected campaign current ref
    -> pin campaign H
    -> read identity/layout/runtime + current owning-scope routing at H
    -> resolve and pin each required current native source revision
    -> enumerate typed operational roots from current native routing partitions
    -> hydrate required transitive native owner/dependency closure
    -> optionally use checkpoint as bounded hint/provenance/acceleration
    -> rebuild derived state
    -> final currentness + compatibility + integrity + RRC validation
    -> resume
```

### Benefits

- matches current-state authority ownership;
- checkpoint may be absent or stale without correctness loss;
- preserves multi-domain source composition without a universal frontier;
- naturally handles Step-5.6 post-publication crash by rereading current authority;
- avoids rollback simply because checkpoint creation is sparse;
- allows checkpoint to remain useful without becoming required registry;
- supports bounded source validation and scope-local recovery failures.

### Cost

- normal cold recovery must read current routing and native sources rather than deserialize one snapshot;
- a source can move while hydration is in progress, requiring bounded retry/revalidation;
- implementation requires real Step-5.2 typed routing machine support.

**Assessment: recommended.**

## 7. Alternative C — CHECKPOINT REMOVED FROM ORDINARY RECOVERY

Shape:

Same as B, but checkpoint is consulted only for explicit maintenance/diagnostics and never as an ordinary recovery acceleration hint.

### Benefits

- simplest authority story;
- less persistent metadata;
- eliminates risk of accidental checkpoint primacy;
- current recovery correctness completely independent of checkpoint lifecycle.

### Costs

- gives up potentially valuable sparse source/routing/provenance hints;
- makes current checkpoint feature almost entirely maintenance-only;
- may increase cold-start I/O in large campaigns even when a trustworthy immutable descriptor could safely narrow reads;
- removes a useful diagnostic record around controlled handoff/migration/complex stops.

**Assessment: viable simplification, but B retains value at low semantic cost if checkpoint fields are aggressively narrowed.**

## 8. Recommended recovery phases

### Phase 0 — Establish selected campaign identity and repository access

Campaign selection precedes gameplay recovery. Do not recover unselected campaigns speculatively.

### Phase 1 — Pin current campaign source

Read the selected campaign branch/ref and pin exact campaign commit H.

H is the campaign-domain source revision for this attempt. It is not a universal recovery frontier.

### Phase 2 — Read current campaign routing/identity under H

At exact H, obtain only bounded structural records needed to resolve:

- campaign identity/layout;
- accepted runtime identity / compatibility prerequisites;
- current active scene/live owning-scope routes;
- campaign-local operational routing partitions;
- other mandatory root-routing metadata established by Step 5.2 machine realization.

### Phase 3 — Resolve and pin participating current native sources

For each current owning-scope route, resolve the authoritative native ref/source and pin an exact revision.

Do not compare campaign H to live L numerically/temporally.

If a required source is missing, do not fallback to checkpoint's old source as current authority.

### Phase 4 — Enumerate bounded operational roots

From current typed native routing partitions, enumerate admitted roots required by Step 5.2.

Checkpoint MAY supply candidate hints that reduce reads, but every hint is validated against current native routing.

### Phase 5 — Hydrate native roots and transitive correctness dependencies

Load native owner state and only required transitive dependencies/references/interpretation evidence.

Examples:

```text
RuntimeCommand -> root Resolution / pending child descriptor
Resolution -> Continuation if suspended
Continuation -> Procedure / accepted dependencies / fixed inputs
Procedure -> required world context
armed temporal root -> owner-local temporal state
```

### Phase 6 — Rebuild derived state

Reconstruct:

- Temporal Agenda;
- condition/effect/query indexes;
- loaded-record caches;
- dependency DAG caches;
- Context Assembler materializations;
- other non-authoritative derived structures.

### Phase 7 — Final validation before resume release

Validate:

1. campaign identity and source existence;
2. each source revision still belongs to the expected owning scope;
3. required runtime/catalog/rules interpretation is available and compatible;
4. required references resolve at their pinned native revisions;
5. root set is complete according to current routing at the pinned composition;
6. native lifecycle and root enrollment agree;
7. no required source is missing/corrupt;
8. RRC holds.

For sources whose currentness matters for immediate writable resume, perform a bounded final current-ref/owner-routing recheck. If movement occurred, classify as movement/conflict and retry/re-pin the affected recovery composition; do not call it canon corruption merely for moving.

Step 5.8 may later provide stronger fencing that narrows this retry window.

## 9. Recovery status model

Recommendation: keep **recovery readiness** separate from existing **integrity status**.

Conceptual recovery readiness:

```text
READY
RETRY_REQUIRED
BLOCKED_MISSING_SOURCE
BLOCKED_INCOMPATIBLE_RUNTIME
BLOCKED_INTEGRITY
```

with typed reasons/scopes.

Integrity remains:

```text
CANON_OK
CANON_SUSPECT
CANON_CORRUPT
```

Examples:

- ref moved during hydration -> `RETRY_REQUIRED`, not CANON_SUSPECT;
- runtime package temporarily unavailable -> `BLOCKED_INCOMPATIBLE_RUNTIME` or narrower prerequisite reason, not corruption;
- stale optional checkpoint -> ignore/advisory stale hint, recovery can remain READY;
- required current route points to missing source -> recovery blocked + affected scope CANON_SUSPECT;
- contradictory current ownership proven -> blocked + CANON_CORRUPT.

Avoid a generic `RECOVERY_REQUIRED` state that hides whether the issue is retryable movement, unavailable dependency or integrity failure.

## 10. Checkpoint role under recommendation B

A checkpoint is an **immutable sparse recovery descriptor/evidence artifact**.

It MAY record non-authoritative observations useful for bounded acceleration/diagnostics, such as:

```text
checkpoint_id
campaign_id
created_at
checkpoint schema version
observed campaign source revision or source descriptor
observed domain-typed native source hints
observed routing/root fingerprints or selected root refs, if useful
accepted runtime identity/provenance projection
optional diagnostic notes
```

Every current-source hint is advisory until validated through current owning-scope resolution.

A checkpoint SHALL NOT:

- contain copied current world/runtime owner payloads merely for recovery;
- be the only registry of operational roots;
- define a universal event/chronology frontier;
- override a newer/current native owning source;
- imply SAVE success;
- be mandatory on every save/handoff;
- require a heartbeat update when nothing warrants a new descriptor.

## 11. Current checkpoint-field disposition recommendation

### `valid_through_event_id`

**Retire as generic checkpoint field.**

Reason: a single event ID cannot prove cross-domain recovery closure and conflicts with B-NARROW. If a later event-history consumer needs event coverage, that claim should live in an event/history-owned typed projection.

### `expected_commit_sha`

**Retire from checkpoint payload.**

Reason: same-transaction containing-commit self-reference is content-addressed/circular. Repository retrieval already supplies the actual revision that contains the checkpoint. A descriptor may record a different previously observed source revision where semantically meaningful, but not pretend to know its own containing commit before publication.

### `world_time`

**Retire from checkpoint as recovery selector.**

If retained for diagnostics, mark as observation-only and domain typed. Final chronology semantics belong 5.9.

### `state.current_state_path`

Likely **redundant fixed-layout hint** for current layouts. Keep only if layout/migration indirection genuinely needs it; it is not an authority pointer by itself.

### `active_pc_ids` / `active_thread_ids` / `active_scene_ids`

May remain **optional snapshot-of-routing hints**, but not completeness proof and not mandatory for normal recovery. Current native routing determines current membership.

### `engine`

Retain only as **recovery provenance/compatibility projection** if useful. MANIFEST/current accepted runtime identity remains authority; open execution may additionally require pinned accepted interpretation context from its native owner.

### `recovery_notes`

Diagnostic-only; never machine authority.

### `MANIFEST.last_checkpoint_id`

Retain only if checkpoints remain useful, but define it narrowly as:

> pointer to the most recently selected/published checkpoint descriptor in the campaign domain

not:

> current recovery frontier / best recoverable state / authoritative rollback point.

Pointer absence or stale descriptor cannot break healthy current recovery.

## 12. Checkpoint creation/lifecycle

Checkpoint creation should be independently justified by expected recovery/diagnostic value, e.g.:

- controlled pause/handoff where sparse recovery evidence materially lowers startup uncertainty/I/O;
- complex mid-procedure suspension;
- migration/repair boundary;
- support/debug evidence;
- another explicit policy whose value exceeds metadata churn.

Creation at ordinary save is optional.

A checkpoint is immutable once published. A pointer to the selected latest descriptor may move only as part of a real campaign transaction that creates/selects a new descriptor; do not emit pointer-only heartbeat refresh.

Old checkpoint retention is a later policy/GC concern. 5.7 requires only that deletion cannot invalidate current recovery correctness and that explicit historical rollback can only be promised while all historical native dependencies it needs remain resolvable.

## 13. Historical rollback / maintenance boundary

Ordinary recovery and historical rollback are different operations.

Ordinary recovery:

```text
recover current valid native authority
```

Historical maintenance reset:

```text
explicitly request older descriptor/source composition
validate every required historical source still exists and is mutually compatible
construct a replacement local view without mutating Git history
```

A checkpoint alone cannot guarantee historical rollback unless every native revision/dependency it references is retained and addressable.

Recommendation:

- do not make guaranteed historical rewind a core checkpoint invariant;
- `HDM_RESET_LAST_CHECKPOINT` should be interpreted as a maintenance operation that succeeds only when the descriptor's exact required historical composition remains resolvable;
- failure to retain historical dependencies yields typed maintenance unavailability, not invented reconstruction;
- if product later requires guaranteed rewind for N checkpoints, that becomes an explicit retention/product policy and Step-5.13/Step-6 implementation constraint.

This avoids turning checkpoint into snapshot authority solely to support an undocumented support command.

## 14. Step-5.6 crash/ambiguity interaction

### Crash after confirmed remote campaign publication, before local bookkeeping

Cold recovery pins the actual current campaign ref and therefore sees the published state. Old local dirty metadata is gone with the process and cannot cause semantic replay.

### Lost ACK where remote ref did advance

Cold recovery reads the actual ref and selects that authority. If an old checkpoint remains behind, it is stale evidence only.

### Lost ACK where ref did not advance

Cold recovery sees the old authoritative campaign revision. Unpublished lost HOT state cannot be invented. If another durable native domain did publish, it remains real and enters source composition according to current owning-scope rules.

### Multi-domain partial success

Recovery starts from actual current native authorities. It does not roll a successful domain backward just to recreate an imagined all-or-nothing old checkpoint cut.

## 15. Strongest counterargument to the recommendation

A checkpoint-first exact cut can give a trivially reproducible frozen composition and avoid racing moving current live sources during hydration. It also makes support/reset workflows easier.

Response:

- reproducibility is not the same goal as ordinary current recovery;
- using a stale frozen cut as normal resume loses later valid durable state;
- a complete exact multi-domain checkpoint would become precisely the universal RecoveryCut authority rejected by 5.1/5.2;
- source movement should be solved with exact pinning plus final currentness/fencing semantics, not historical rollback;
- 5.8 can later provide stronger live fences/leases;
- explicit historical replay can remain a separate maintenance operation when retained source revisions permit it.

## 16. Simplest viable alternative

Alternative C is simpler: remove checkpoint entirely from ordinary recovery and rely only on native current routing.

Why not select it immediately:

- immutable sparse descriptors can still reduce cold-start reads and provide useful migration/support provenance without owning state;
- the repository already has checkpoint product surface and maintenance concepts;
- retaining a narrowly defined optional descriptor costs little if current-source validation is mandatory.

Revisit trigger: if implementation/evaluation shows checkpoint hints do not materially reduce bounded I/O or improve diagnostics, ordinary recovery may ignore them completely without changing authority semantics.

## 17. Preliminary decision assessment

No new owner-level product decision is currently required for ordinary cold recovery. The recommended authority direction is mechanically implied by Steps 5.1–5.6.

Potential product choice — guaranteed historical checkpoint rewind — is not currently a canonical player-facing requirement. The only direct consumer found is an internal/proposal maintenance command. Therefore the architecture should not pay snapshot/retention costs to guarantee it by default.

If the owner later wants a durable user-visible rewind feature, reopen only the retention/historical-source guarantee, not ordinary recovery authority.

## 18. Candidate architecture direction

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-ASSISTED BOUNDED RECOVERY**

Core invariants:

```text
current campaign authority anchors discovery, not checkpoint
current owning-scope routing selects native authorities
all mutable sources are exact-revision pinned during one attempt
checkpoint hints never override current native routing
checkpoint absence/staleness is not recovery failure
bounded typed routing, not checkpoint, proves root discoverability
native owner payloads remain authority
rebuildable state is rebuilt
resume releases only after currentness/compatibility/integrity/RRC validation
source movement -> bounded retry, not invented corruption
historical rollback is explicit maintenance and conditional on retained exact sources
```

Proceed to analytical challenge before candidate canonicalization.
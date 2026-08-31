# Step 5.1 — Frontier Model — Research & Architecture Draft

Status: **RESEARCH COMPLETE — ANALYTICAL CHALLENGE REQUIRED BEFORE DECISION BRIEF**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Basis:

- `2026-08-20-step-5-1-frontier-model-pre-research-charter.md`
- `2026-08-20-step-5-1-frontier-model-task-brief.md`
- Step-5.0 final contamination resolution
- canonical Step-2 temporal/recovery assurance
- canonical Step-3 execution-boundary specification
- canonical Step-4 truth/knowledge/context/Story specification
- current GAME/CORE and GAME/SCHEMA contracts

This document is a research/draft artifact. It does not canonicalize the recommendation.

---

# 1. Executive research result

The repository does **not** support a single universal scalar “campaign frontier”, nor does it justify a first-class generic Frontier record/value system.

It does support a smaller shared semantic vocabulary:

> A **frontier** is a domain-typed boundary describing established progress, coverage or constraint knowledge within one explicitly identified domain. A frontier is not semantic authority. Comparison is valid only inside the same compatible domain unless a specific cross-domain relation is defined.

The minimum useful cross-domain relations are not arithmetic ordering. They are typed relations such as:

```text
based_on
published_as / reachable_at
covers / projected_through
observed_at
recovered_from / describes
absorbed_from
compatible_with
incomparable
```

Representations remain domain-specific.

Research also finds that several current “frontier-like” concepts are not frontiers:

```text
HOT working state          = working view over a durable base + accepted delta
SOFT / HARD                = durability classifications / requirements
Dirty set                  = unpublished delta/closure
MANIFEST.last_checkpoint   = pointer
Checkpoint                 = recovery descriptor/evidence
session.base_head_sha      = session coordination evidence
Resolution.cursor          = execution cursor
live logical revision      = generation/revision within one epoch
Temporal Agenda            = derived index
```

The current `CURRENT.last_event_id` does not survive the research as a justified global semantic-LOG/recovery coverage frontier. A sequential semantic-event ID is stable identity, but current allocation/publication semantics do not prove a dense published prefix. Exact campaign Git revision already identifies the exact durable LOG tree. The field should therefore be retired as a global cursor unless a later slice independently proves a narrower concrete consumer.

Per-record `last_event_id` fields are a different concept: provenance pointers to a causally relevant event. They are not global LOG frontiers and are outside this retirement conclusion.

The active-live model forces one additional semantic conclusion:

> A coherent current/recovery view can require a **scope-indexed set of compatible domain revisions/frontiers**, not one scalar marker.

This does **not** imply a new durable `RecoveryCut` entity. “Consistent cut” is currently best treated as a conceptual relation/view: a set of pinned domain markers plus ownership scopes that can coexist without contradictory authority. Physical serialization belongs to Steps 5.2/5.7.

Current recommendation: **Alternative B — small shared typed-frontier vocabulary with domain-specific representations and explicit cross-domain relations.**

Recommendation confidence before formal challenge: **HIGH**.

---

# 2. Evidence map

## 2.1 Step 2 — temporal obligations and chronology evidence

**FACT**

Step 2 establishes:

- Effect intrinsic lifetime and scheduled-trigger due state remain owner-local authoritative bindings;
- Temporal Agenda is disposable/rebuildable;
- Resource/LifeState delayed recovery and checkpointable procedure/runtime obligations are additional Agenda inputs;
- losing Agenda does not authorize recreating deadlines from prose or rerolling delays;
- once gameplay establishes quantitative elapsed evidence, that evidence must not be discarded merely because no timer currently consumes it;
- later elapsed predicates may be `TRUE | FALSE | INDETERMINATE` depending retained evidence.

**INFERENCE**

Temporal scheduling authority cannot be represented by “latest Agenda position”. Agenda position is a derived retrieval concern. Chronology evidence and owner-local obligations have separate semantics.

---

## 2.2 Step 3 — current authority, execution continuity and revision dependencies

**FACT**

Step 3 establishes:

- current world records remain current-state authority;
- MechanicalEvents/receipts/history are committed evidence, not alternate current-state authority;
- Procedure owns procedure-local operational state;
- Continuation owns one suspended Resolution generation;
- mandatory post-commit child work must materialize stable obligation identity atomically with the triggering committed event;
- Continuation retains fixed RNG, safe recompute phase, committed receipts, `dependency_frontier_refs`, expected child identities, `future_rng_frontier`, etc.;
- Resolution has an execution `cursor`, distinct from Continuation generation and from state authority;
- recovery roots must preserve active Procedure, suspended Resolution/Continuation, fixed RNG/choices, committed segment/Event progress and other exact execution evidence.

**INFERENCE**

The word `frontier` is already used for incompatible domains:

```text
dependency_frontier_refs    revision dependency evidence
future_rng_frontier         deterministic RNG-stream position/state
committed Event frontier    committed execution/history evidence
```

A shared wire representation would add little and could imply invalid comparison. The useful common rule is domain typing, not value unification.

---

## 2.3 Step 4 — pinned source views and lagging Story projections

**FACT**

Step 4 establishes:

- Context Assembler uses a pinned canonical campaign source basis for one coherent role context;
- `RoleContextBundle.source_frontier` is trace/working evidence, not authority;
- Story is durable but noncanonical;
- Story may lag authoritative history;
- Story reveal eligibility is dependency/reference based, not one global chronological reveal position;
- Commentator similarly requires a coherent pinned Story/campaign view.

**INFERENCE**

“Source frontier” is a read-consistency concept, not another world owner. When a role operates in an active live-owned scene, Step 5 must refine the source-view semantics so the context can pin the campaign basis and relevant authoritative live revision without pretending one campaign SHA contains current live truth. This is compatible with Step 4 because transport/source-view details were explicitly deferred.

---

## 2.4 STORAGE / PERSISTENCE — campaign durable revision and working view

**FACT**

Current storage contracts maintain:

```text
known_head_sha
known_tree_sha when resolved
loaded canonical records at that known revision
dirty in-memory records not yet published
durable_frontier_time
```

Startup/resync pins campaign HEAD. A campaign transaction freezes `pinned_head_sha`, base tree and complete dirty delta. A prepared commit object is not canonical. Only successful non-force ref advancement makes the created commit the campaign branch's published durable state. A failed final ref update may leave an unreachable commit object that is not gameplay authority.

A session can accept a newer campaign HEAD without rereading unrelated records when changed paths cannot affect its loaded/dirty/decision scope.

**INFERENCE**

There are at least four distinct concepts currently collapsed under “known frontier” wording:

```text
campaign durable revision        exact reachable commit on campaign ref
observed campaign revision       what this runtime last verified
working-set base revision        revision against which loaded state is interpreted
accepted unpublished delta       current volatile changes beyond that base
```

The first three may all be represented by SHA values, but their roles differ. The dirty delta is not a frontier at all.

---

## 2.5 DURABILITY_GUARD — current truth may precede durable publication

**FACT**

Current guard semantics state that accepted facts become true in HOT immediately and many remain SOFT until a forced boundary. If unpublished HOT state is destroyed, recovery must return to the latest durable campaign state and must not invent lost facts.

**INFERENCE**

`SOFT` and `HARD` are requirements/classifications about publication urgency, not independent versions of state and not frontiers. HOT current state is best modeled as:

```text
WorkingView(base_revision, accepted_delta)
```

where the accepted delta is current for that surviving runtime context but is not durably recoverable yet.

This distinction is necessary for Step 5.5 but 5.1 does not decide save cadence.

---

## 2.6 Session metadata — same SHA, different semantics

**FACT**

`session_record` stores:

```text
base_head_sha
last_published_head_sha
```

and explicitly describes session records as coordination/recovery metadata. `base_head_sha` refreshes on resync/new chat.

**INFERENCE**

A SHA does not become an authority/frontier merely because it names a commit. Session SHAs are evidence about a session's observation/publication history and may legitimately be stale relative to the campaign branch.

---

## 2.7 Live scene — scope-local operational authority

**FACT**

During an active live epoch:

```text
campaign base at base_campaign_sha
+ LIVE/LIVE_STATE at authoritative live branch revision
= current truth for live-owned mutable scope
```

Unrelated campaign scopes continue to use the campaign branch normally.

Authority activation requires a durable campaign-scene pointer to the live epoch. A live branch created before that pointer is published is an orphan and not authoritative.

A participating session caches live HEAD, live-state blob SHA and parsed state. Each logical live mutation increments `revision`, but write concurrency is enforced by the current live-state blob SHA / branch state.

A closed live epoch is frozen but not yet absorbed. Durable absorption is evidenced by campaign routing state and `last_absorbed_live_head_sha` equal to the exact final live HEAD.

**INFERENCE**

The live domain contains several distinct markers:

```text
base_campaign_sha           based-on relation
live branch HEAD            durable operational storage revision
LIVE_STATE blob SHA         optimistic write/concurrency token
LIVE_STATE.revision         logical generation/counter inside epoch
campaign live pointer       authority activation/routing evidence
last_absorbed_live_head_sha handoff/idempotency evidence
```

No one marker can replace the others without losing a distinct correctness property.

A campaign can also advance for unrelated scopes while a live epoch remains based on an older campaign revision. Therefore the overall current gameplay view is scope-partitioned and cannot always be represented by a single campaign SHA.

---

## 2.8 Chronology — partial-order constraints, not publication progress

**FACT**

Chronology is primarily a partial order. Independent scenes/events may remain unordered. Git order is not fictional order.

Current chronology markers include:

- `scene.chronology_frontier_event_id` — local ordering boundary when useful;
- `CURRENT.world_time.frontier` — sparse globally reconciled chronology boundary/summary;
- causal and `after` event relations;
- optional local sequence and optional exact/approximate time.

`world_order.sequence` is explicitly local/optional, not a campaign-global counter.

**INFERENCE**

Chronology frontier semantics are fundamentally constraint/evidence semantics. They may be represented by one event anchor in a locally linear scene or by a more complex sparse summary in the reconciled domain. Step 5.1 should preserve the category but must not freeze the current representation; Step 5.9 owns representation/compaction.

Chronology markers are intentionally incomparable with campaign Git revision, live revision number, semantic-event ID allocation order or Story record IDs.

---

## 2.9 Semantic event identity and `last_event_id`

**FACT**

`runtime.semantic_event` has a campaign-scoped sequential ID policy. Semantic event schema explicitly allows fictional incomparability and does not define ID order as chronology.

Storage permits stable IDs to be allocated/reserved in the hot working set before publication; durable-reference closure is enforced only when publishing a reference. The ID policy itself does not state that every smaller sequential ID is already durably published.

`CURRENT.last_event_id` is explicitly labelled a provisional semantic-log/recovery cursor pending Step-5 design.

Scene and many entity schemas also contain `last_event_id`, normally adjacent to domain state and causal-history semantics.

**INFERENCE**

A sequential ID provides identity and allocation order, not automatically a dense append-prefix theorem.

Therefore:

```text
CURRENT.last_event_id = X
```

cannot safely imply:

```text
all semantic events <= X are durably present
all semantic history relevant to recovery is covered through X
X is latest fictional event
```

Exact campaign Git revision already identifies the exact tree containing the durable LOG state. Incremental LOG consumers can later use a source campaign revision plus bounded changed-path/index discovery; Step 5.10 may design a dedicated projection cursor if that proves materially better.

**RECOMMENDATION**

Retire `CURRENT.last_event_id` as a global semantic-log/recovery cursor.

Do not infer from this that per-record `last_event_id` provenance pointers are invalid. Their semantics are record-local causal provenance and should be evaluated separately when relevant.

---

## 2.10 Checkpoint — pointer, descriptor and described recovery boundary

**FACT**

`MANIFEST.last_checkpoint_id` is the sole latest-checkpoint pointer after Step 5.0.

Checkpoint schema currently contains:

```text
valid_through_event_id
expected_commit_sha
world_time
active-state references
engine recovery projection
```

and explicitly says checkpoint is compact recovery metadata, not a world snapshot.

**INFERENCE**

Three concepts must remain distinct:

```text
MANIFEST.last_checkpoint_id
    pointer / routing

Checkpoint record
    immutable recovery descriptor/evidence

Recoverable boundary described by checkpoint
    one compatible set of authoritative state revisions/roots
```

The current `valid_through_event_id` should not be treated as a general recovery frontier merely because the field is required today. Its scalar-event assumption is not supported as a complete description of campaign + live + operational recovery.

The exact replacement/retention decision belongs to Step 5.7 after 5.2 identifies operational recovery roots. Step 5.1 should impose the constraint that checkpoint correctness may not depend on treating one semantic-event ID as a dense total history frontier.

---

# 3. Normalized vocabulary

## 3.1 Semantic authority

The owner whose current value determines gameplay truth/operational state for an explicitly scoped concept.

Frontiers, pointers, receipts, checkpoints and projections do not gain authority merely by referring to this state.

## 3.2 Revision

An identified version/generation of one mutable storage or operational surface.

Examples:

```text
campaign commit SHA reachable from campaign ref
live branch HEAD within one epoch
LIVE_STATE logical revision within one epoch
Continuation generation
```

Revision comparison is domain-specific.

## 3.3 Frontier

A domain-typed boundary describing established progress, coverage or constraint knowledge inside one domain.

Required semantic rules:

1. every frontier has an explicit domain;
2. frontier is not semantic authority;
3. two frontier values are not comparable merely because their representations share a primitive type;
4. comparison is permitted only by the domain's declared relation;
5. a domain may use scalar, set/vector, graph-anchor or composite representation;
6. a frontier may legitimately be incomparable to another frontier in the same partially ordered domain;
7. not every revision/cursor/pointer is a frontier.

No generic runtime Frontier entity is justified.

## 3.4 Cursor

A position used to continue deterministic/local processing within a specific ordered traversal or execution domain.

Examples:

```text
Resolution.cursor
possible future projection traversal cursor
```

A cursor does not automatically prove durability or coverage.

## 3.5 Pointer

A reference to another record/object.

Example:

```text
MANIFEST.last_checkpoint_id
```

Pointer freshness/target validity is a separate invariant.

## 3.6 Coverage

A claim that a projection/consumer has incorporated a defined source subset through a domain-specific boundary.

Coverage must define its source domain and relation. It is not fictional chronology unless explicitly so defined.

## 3.7 Working view

A coherent current runtime view assembled from one or more pinned authoritative bases plus accepted volatile delta/overlays for scopes whose authority permits them.

For simple singleplayer:

```text
WorkingView = CampaignRevision C + accepted HOT delta
```

For an active shared scene the authoritative sources can be scope-partitioned.

## 3.8 Consistent cut / coherent source cut

A **conceptual**, not yet persisted, set of mutually compatible domain markers and ownership scopes sufficient to describe one coherent read/recovery basis.

Example shape only:

```text
campaign_scope -> campaign revision C
scene_A live-owned scope -> live epoch E at live revision L based on campaign C0
operational roots -> exact accepted runtime-owner generations/revision dependencies
```

This concept is required by current live/recovery semantics, but Step 5.1 does not introduce a `runtime.recovery_cut` class or schema.

## 3.9 Durability requirement

A rule requiring some current accepted state to cross a durable publication boundary.

`SOFT`/`HARD` belong here; exact classes/triggers remain Step 5.5.

## 3.10 Lag / stale

These must not be conflated.

```text
lagging
    a projection/consumer is intentionally behind its source but still valid

stale
    a cached/working basis is old enough that correctness may require refresh/revalidation
```

Story can be lagging without being wrong. A session base HEAD can be stale for a race-sensitive mutation.

---

# 4. Concept reclassification ledger

| Concept | Classification | Authority? | Comparison domain | Key finding |
|---|---|---:|---|---|
| campaign branch reachable commit | durable revision / publication frontier | no; records in tree own semantics | campaign Git ancestry | exact durable campaign state at that publication |
| campaign branch ref | routing pointer to current durable revision | no | branch/ref | ref reachability makes commit current published campaign revision |
| `known_head_sha` | observed durable revision evidence/cache | no | campaign revision | may lag remote until sync is required |
| `known_tree_sha` | transport/cache metadata | no | same commit | derivable from commit; not separate frontier |
| loaded canonical records | working-view materialization | no new authority | pinned source revision | partial loaded subset at a known base |
| HOT accepted dirty state | current volatile working delta | current only in surviving runtime context | based on working view | not durably recoverable until publication |
| dirty set | unpublished delta/closure | no | n/a | not frontier |
| SOFT/HARD | durability requirement/classification | no | n/a | not frontier |
| `durable_frontier_time` | guard timing metadata | no | wall-clock guard domain | timestamp of known durable publication for ceiling; not fictional time |
| session `base_head_sha` | coordination/recovery evidence | no | campaign revision | session's observation basis, may become stale |
| session `last_published_head_sha` | session publication evidence | no | campaign revision | not latest campaign authority |
| prepared commit object | transport artifact/revision candidate | no | campaign Git object graph | unreachable object is not canonical |
| live `base_campaign_sha` | based-on reference | no | campaign revision | defines inherited base for overlay |
| live branch HEAD | durable operational revision | live state at authoritative routed epoch is operational authority | same live epoch ancestry | branch alone not authoritative without campaign routing activation |
| LIVE_STATE blob SHA | CAS/version token | no | one file lineage | concurrency guard |
| LIVE_STATE `revision` | logical revision/generation | no | same epoch | useful internal monotonic generation, not campaign progress |
| campaign `live_epoch` pointer | authority-routing evidence | no | scene lifecycle | activates referenced live epoch for that scope |
| `last_absorbed_live_head_sha` | handoff/idempotency evidence | no | live-epoch final HEAD identity | proves exact epoch result absorbed once |
| `CURRENT.world_time.frontier` | chronology frontier concept | no | reconciled chronology domain | representation provisional until 5.9 |
| scene `chronology_frontier_event_id` | local chronology frontier/anchor | no | scene chronology | local only, not global event cursor |
| SemanticEvent ID | stable record identity | event record owns historical fact, not current state | identity/allocation domain | sequential allocation != fictional order or dense coverage proof |
| `CURRENT.last_event_id` | provisional global cursor | no | unclear | no proven unique consumer; recommend retirement |
| entity/scene `last_event_id` | provenance pointer | no | record-local causal provenance | separate from global cursor decision |
| checkpoint latest ID in MANIFEST | pointer | no | checkpoint identity | sole latest-checkpoint routing pointer |
| checkpoint record | recovery descriptor/evidence | no | checkpoint generation/history | does not own state |
| `valid_through_event_id` | legacy/provisional recovery anchor | no | semantic-event identity | insufficient as universal recovery frontier |
| `expected_commit_sha` in checkpoint | recovery publication evidence | no | campaign revision | exact semantics must be redesigned in 5.7; self-publication identity issue remains |
| Continuation generation | runtime owner generation | Continuation state is authority for suspended generation | one Continuation lifecycle | not a cross-domain frontier |
| `dependency_frontier_refs` | dependency revision evidence | no | referenced dependency domains | typed set; generic string representation currently underspecified |
| `future_rng_frontier` | RNG cursor/state boundary | RNG continuity owner semantics apply | one RNG stream | incomparable with campaign/chronology |
| Resolution cursor | execution cursor | Resolution owns execution state | one Resolution | not frontier |
| Temporal Agenda | derived index | no | n/a | rebuild from authoritative obligations |
| Story source coverage | projection frontier/coverage | no | source-history domain | may lag canon legally |
| Story editorial revision | projection record revision | Story owns noncanonical text only | Story record/version | distinct from source coverage |
| retention/GC boundary | safety eligibility boundary | no | dependency-closure domain | not safely reducible to age/scalar ID |

---

# 5. Actual frontier/progress domains

Research supports these independently meaningful domains.

## 5.1 Campaign publication domain

Representation candidate already exists: campaign Git commit ancestry/ref reachability.

Within one campaign branch:

```text
C0 -> C1 -> C2
```

is durable publication ancestry/storage progression.

It says nothing by itself about fictional event order.

## 5.2 Live epoch operational domain

One active live epoch has its own operational revision lineage tied to a base campaign revision and activated by campaign routing.

Comparison is meaningful only within the same epoch/generation. Different live epochs are not ordered merely by their revision numbers.

## 5.3 Chronology domains

At least:

- local scene chronology domains;
- a sparse globally reconciled chronology domain.

These are partial-order/evidence domains. Exact data structure remains 5.9.

## 5.4 Runtime deterministic-stream/dependency domains

Examples include:

- Continuation generation;
- RNG stream state;
- dependency revision sets.

These are domain-local continuity markers. Step 5.2/5.3 will decide which must enter durable recovery closure.

## 5.5 Projection coverage domains

Each Story layer/consumer may require source coverage. Coverage does not imply literary record ordering equals semantic event order.

Exact frontier representation belongs to 5.10.

## 5.6 Retention/compaction safety domain

This is best understood as a dependency eligibility boundary rather than chronological age. Exact safe-deletion algorithm remains 5.13.

---

# 6. Required relation model

The research does **not** justify one universal `<`/`>` or `dominates()` operation across all domains.

The minimum shared relation vocabulary is:

## 6.1 Same-domain relations

Each domain may define as applicable:

```text
equal
precedes / ancestor_of
dominates / covers
incomparable
same_generation
supersedes_generation
```

Only expose relations that the domain can prove.

Examples:

- campaign commit ancestry can prove ancestor/descendant;
- local live revision can prove monotonic revision within one epoch;
- chronology can prove `before`, `after` or `incomparable` based on causal/order evidence;
- RNG cursor can prove stream position only under the same stream identity.

## 6.2 Cross-domain relations

Cross-domain relations are named semantics, not ordering coercions:

```text
based_on
observed_at
published_at / reachable_at
describes
recovered_from
projected_through
absorbed_from
compatible_with
```

Examples:

```text
LiveEpoch E based_on CampaignRevision C42
Checkpoint K describes a recoverable cut containing CampaignRevision C50
Story projection P projected_through source campaign/history revision C55
Session S observed_at CampaignRevision C53
Campaign scene absorbed_from final LiveRevision L17
```

A relation must not create hidden total order between the source and target domains.

---

# 7. Coherent current view and recovery composition

## 7.1 Singleplayer without live state

Conceptually:

```text
Campaign durable revision C
        +
accepted HOT delta D
        =
current surviving WorkingView
```

Cold recovery after losing D returns to C unless D crossed a durability boundary.

## 7.2 Active live scene

A single campaign SHA is insufficient to describe current mutable truth for all scopes when an active live epoch exists.

Conceptually:

```text
campaign revision C_current

scene A mutable scope:
    base campaign C_base
    + authoritative live epoch E at live revision L

unrelated non-live scope:
    campaign C_current
```

The scopes are allowed to coexist only while ownership/conflict constraints prove compatibility. A cross-scope dependency can force synchronization/reconciliation later (5.8/5.9).

## 7.3 Consequence for context assembly

Step 4's “pinned campaign frontier” remains necessary but is not sufficient for a role context that depends on current live-owned truth.

Step 5 should eventually provide Context Assembler a coherent source-cut description that identifies:

- campaign revision used for campaign-owned sources;
- relevant authoritative live epoch revision for live-owned sources;
- scope ownership/routing evidence.

This is a transport/source-basis refinement, not a new information authority.

## 7.4 Consequence for checkpoint/recovery

A checkpoint cannot safely mean “restore event X” or “restore campaign SHA C” in every case if active live/operational state is independently authoritative and must survive.

The semantic requirement is a **consistent recovery description** of the necessary domain revisions/roots. Steps 5.2/5.7 decide its fields and storage.

No new generic `RecoveryCut` record is justified at 5.1.

---

# 8. Counterexample results

## C1 — HOT ahead of campaign

Authority/current: accepted HOT working state for the surviving runtime.
Durable: campaign revision C.
Relation: WorkingView is based on C plus delta D; D is not a frontier.
Recovery after loss: C only.

Result: disproves “current == durable frontier”.

## C2 — HARD requirement with older SOFT state

HARD is a publication requirement. The coherent dirty closure may include older SOFT state.

Result: disproves “HARD frontier” as a separate state version.

## C3 — commit object created, ref update fails

Prepared commit exists but is unreachable from authoritative ref.

Result: Git object existence is insufficient for campaign durable frontier.

## C4 — session observes C50, remote moves C53

Session evidence remains internally meaningful but may be stale for race-sensitive work.

Result: observed revision != authoritative current ref.

## C5 — live epoch based on C47 while campaign advances C50 elsewhere

Current live-owned scope uses C47 + L; unrelated campaign scope may use C50.

Result: one campaign SHA cannot represent overall current truth during active live ownership.

## C6 — two independent live epochs

Each epoch has an independent live revision domain. Revision 8 in scene A and revision 12 in scene B have no natural order.

Result: live revision is domain/epoch typed.

## C7 — live closed but unabsorbed

Closed live HEAD remains the exact frozen source for pending compaction; campaign state has not yet absorbed it.

Result: lifecycle state and durability/handoff are distinct.

## C8 — checkpoint behind current campaign

Checkpoint may remain valid recovery evidence while intentionally older than current durable campaign revision.

Result: lagging recovery checkpoint is not stale/incorrect solely because newer canon exists.

## C9 — suspended Continuation

Exact recovery also depends on runtime owner/generation/RNG/dependency evidence.

Result: campaign/history scalar alone may be insufficient for resumable execution.

## C10 — Agenda absent

Authoritative temporal owner bindings still exist; Agenda rebuilds.

Result: derived index has no frontier authority.

## C11 — sequential semantic IDs, incomparable fiction

Storage/allocation order may be sequential while fictional chronology is undefined.

Result: ID order is not chronology.

## C12 — later cross-scene dependency

New relation constrains only necessary chronology. Existing unrelated events remain unordered.

Result: chronology frontier must admit partial-order refinement without global rewrite.

## C13 — Story EVENTS ahead of NARRATIVE

Both can be valid projections at different source coverage.

Result: lag is legal and domain-specific.

## C14 — NARRATIVE editorial revision

Literary text may change while source coverage remains the same.

Result: projection coverage != editorial revision.

## C15 — Chronicler restart

It needs a source coverage basis to avoid duplicate work, but no evidence requires that basis to be a semantic-event scalar. Campaign/source revision plus explicit provenance can satisfy correctness; exact efficient representation remains 5.10.

## C16 — fresh runtime with active live state

Campaign branch routing is needed to discover/adopt active live authority. Model memory is irrelevant.

Result: source/recovery view may be composite.

## C17 — retention wants to delete still-needed evidence

Age or ID threshold cannot alone prove deletion safety.

Result: retention boundary is dependency/safety semantics, not generic chronology frontier.

## C18 — pointer target missing

Pointer validity is an integrity invariant. Missing target does not mean “frontier regressed”.

Result: pointer != frontier.

## C19 — same primitive representation, different domains

Campaign SHA, live SHA, blob SHA are all strings/hashes but carry distinct semantics.

Result: representation equality does not imply domain compatibility.

## C20 — generic Frontier record with no consumer

All current concrete consumers require domain-specific data anyway: Git ancestry, live epoch identity, chronology relations, RNG stream identity, Story source provenance.

Result: a generic first-class Frontier entity would mostly wrap existing values and create unnecessary indirection.

---

# 9. Alternatives

## Alternative A — Domain-local semantics only

Every subsystem defines its own terminology and relations. No common frontier rules beyond ordinary documentation.

### Benefits

- minimum new abstraction;
- maximum freedom for later slices;
- no generic schema/type.

### Weaknesses

- repeated confusion between pointer/cursor/revision/frontier is already present;
- Context Assembler, checkpoint/recovery and cross-domain debugging need a common way to state compatibility without inventing ad hoc wording;
- later slices can accidentally compare unrelated IDs or recreate duplicate authorities.

### Assessment

Viable but too weak for the cross-domain correctness problems Step 5 already has.

---

## Alternative B — Small shared semantic vocabulary; domain-specific representations **(recommended)**

Adopt common definitions for:

```text
authority
revision
frontier
cursor
pointer
coverage
working view
consistent/coherent cut
lagging vs stale
```

Require frontier/domain typing and prohibit implicit cross-domain comparison. Each subsystem keeps its native representation and declares only meaningful relations.

No generic Frontier record/schema is introduced.

### Benefits

- directly prevents the identified failure modes;
- enough vocabulary to compose campaign/live/recovery/context/projection views;
- preserves domain-specific semantics;
- low migration/reversal cost;
- does not pre-design later slices.

### Weaknesses

- “frontier” remains an overloaded English word unless documentation consistently names the domain;
- later schema work still needs domain-specific types;
- a coherent-cut concept could be overpromoted into a new record if discipline is lost.

### Assessment

Best balance of correctness and YAGNI.

---

## Alternative C — Unified first-class Frontier model/value system

Introduce generic typed frontier values with common identity/comparison/composition APIs and likely a shared schema.

### Benefits

- uniform tooling;
- explicit typing if fully implemented;
- potentially elegant introspection/debug UI.

### Weaknesses

- no current consumer needs one representation;
- comparison semantics differ materially across Git ancestry, live epoch, chronology, RNG and Story coverage;
- risks false comparability;
- could become duplicate authority or generic persistence bureaucracy;
- prematurely constrains 5.7–5.10.

### Assessment

Reject as overengineering at current requirements.

---

## Alternative D — Remove “frontier” vocabulary almost entirely

Use only concrete concepts: Git SHA, live revision, checkpoint pointer, chronology anchors, projection source refs.

### Benefits

- very concrete;
- no abstract vocabulary.

### Weaknesses

- does not solve cross-domain consistency/read/recovery composition;
- encourages representation-driven reasoning;
- repeated “latest” concepts can again be mistaken for global total progress.

### Assessment

Too weak; fails the Step-5 composition problem similarly to A.

---

# 10. Current recommendation

Recommend **Alternative B**.

Normative direction if approved:

1. keep semantic authority with existing domain owners;
2. define `frontier` only as a domain-typed progress/coverage/constraint boundary;
3. never compare frontiers across domains without an explicit named relation;
4. use domain-native representations; do not create generic Frontier record/schema;
5. classify HOT as working view + delta, SOFT/HARD as requirements, checkpoint as descriptor, session SHAs as evidence;
6. model coherent read/recovery composition conceptually as a scope-indexed compatible set/cut, without creating a durable class in 5.1;
7. retire `CURRENT.last_event_id` as global semantic-log/recovery cursor;
8. constrain Step 5.7 not to depend on one scalar event ID as universal recovery frontier;
9. keep chronology frontier concepts but defer exact representation to 5.9;
10. require Story projection coverage to name its source domain and remain separate from Story editorial revision.

---

# 11. Strongest current counterargument

The strongest argument against Alternative B is that the shared vocabulary may be unnecessary architecture ceremony. Every real domain already has a concrete native representation, and the safest design might simply document them independently. Introducing “frontier” and “consistent cut” could encourage future engineers to create a generalized framework even if no common runtime behavior exists.

This objection is credible because Alternative C's overgeneralization failure is exactly what the charter was designed to prevent.

The answer must therefore be tested in the analytical challenge: Alternative B is justified only if at least two concrete cross-domain consumers require shared relation semantics that Alternative A cannot express cleanly without repeated ad hoc rules.

Current candidates are:

- cold recovery/checkpoint composition over campaign + live + operational state;
- Step-4 Context Assembler coherent source view over campaign + active live authority;
- debugging/integrity classification of stale vs intentionally lagging domains.

If these can be specified cleanly without shared vocabulary, recommendation should simplify toward A/D.

---

# 12. Assumption and evidence ledger

## A1 — campaign Git reachable commit is sufficient to identify exact durable campaign tree

Confidence: **HIGH**.

Evidence: current PERSISTENCE transaction semantics and ref authority.

Impact if false: campaign durable-revision model changes materially.

Revisit trigger: introduction of durable canonical state outside campaign/live refs or a storage transport where branch commit cannot identify exact campaign tree.

## A2 — active live authority can coexist with later campaign revisions for non-overlapping scopes

Confidence: **HIGH**.

Evidence: current LIVE_SCENE compaction/conflict protocol explicitly permits current campaign HEAD to move and checks overlap against touched scope.

Impact if false: live protocol would require campaign pinning/locking and Step 5.8 changes materially.

Revisit trigger: evidence that any campaign write during live epoch invalidates live authority regardless of touched scope.

## A3 — semantic event sequential IDs may have gaps/reservations and do not prove dense published coverage

Confidence: **HIGH** for “ID order is not enough”; **MEDIUM** for actual frequency of gaps.

Evidence: generic stable-ID reservation before publication is allowed; allocator policy states sequential identity but no dense-prefix invariant; live compaction delays durable event publication.

Impact if false: a dedicated LOG cursor could be cheaper, but fictional chronology separation would remain.

How to verify later: Step 5.6/ID allocator implementation can explicitly define reservation/commit semantics.

Revisit trigger: a canonical invariant is introduced that semantic event ID N implies every <=N is durably published exactly once in the same log domain.

## A4 — recovery/context assembly needs a coherent composite source description when active live authority exists

Confidence: **HIGH** semantically, representation intentionally open.

Evidence: campaign branch does not contain current mutable live-owned truth while active live state is authoritative for that scope.

Impact if false: coherent-cut vocabulary could be removed.

Revisit trigger: Step 5.8 eliminates live authority or forces all relevant campaign state into one synchronized branch revision before every read/recovery.

## A5 — Story projection should not block canonical publication

Confidence: **HIGH** from Step 4/Step-5 agenda.

Impact if false: Story coverage becomes part of a stronger publication barrier.

Revisit trigger: explicit owner decision that Story is required for gameplay recovery/correctness.

---

# 13. What evidence would change the recommendation

Move from B toward **A/D** if:

- 5.2/5.7 can express exact cold recovery using only campaign revision + ordinary record discovery, with no cross-domain compatibility description;
- Step-4 live context can be assembled without pinning/declaring live source revision or scope;
- shared vocabulary creates no enforceable invariant/test beyond prose terminology.

Move from B toward **C** if:

- three or more domains require the same runtime comparison/composition API with identical semantics;
- a concrete integrity/recovery tool must accept heterogeneous frontier values through one typed interface;
- domain-specific representations cause repeated bugs that a shared value type can mechanically prevent.

Reconsider `CURRENT.last_event_id` if:

- a concrete current consumer requires a campaign-wide incremental semantic-log cursor;
- semantic-event publication is given an explicit dense-prefix invariant independent of fictional chronology;
- campaign revision/change-path discovery is proven insufficient or unacceptably expensive for that consumer.

---

# 14. Exact carry-forward constraints

## Step 5.2 — Resumable Runtime Closure

- classify operational owner generations/dependency/RNG markers by their own domains;
- do not serialize Temporal Agenda as authority;
- define which domain markers are required to reconstruct a coherent working view;
- do not invent a generic Frontier record merely to package them.

## Step 5.3 — Temporal/pending continuity

- chronology evidence and owner-local temporal obligations remain distinct;
- no-lost/no-double execution must use typed owner/firing identities rather than a global scheduler frontier;
- RNG continuity remains RNG-domain state.

## Step 5.4 — Host/session handoff

- session observation metadata can be stale and must not be treated as campaign authority;
- controlled handoff should name the durable/coherent source basis it expects to resume.

## Step 5.5 — SOFT/HARD/SAVE

- SOFT/HARD are durability requirements/classifications, not state versions/frontiers;
- a forced publication closes over causally valid accepted dirty delta.

## Step 5.6 — Campaign publication

- campaign durable revision becomes canonical only via successful authoritative ref advancement;
- unreachable prepared commits are not frontiers/current canon;
- define ID reservation/publication semantics sufficiently to prevent accidental use of max ID as dense coverage.

## Step 5.7 — Checkpoint/recovery

- checkpoint remains descriptor/evidence;
- latest checkpoint ID remains pointer;
- recovery description may need multiple domain roots/frontiers;
- one semantic-event ID must not be assumed to describe universal recovery progress;
- resolve the fate/replacement of `valid_through_event_id` and `expected_commit_sha` without circular publication assumptions.

## Step 5.8 — Live ownership

- live branch HEAD and logical revision remain epoch-scoped;
- campaign routing activates authority;
- define compatibility/reconciliation across current campaign revision and older live base explicitly;
- no implicit ordering between different live epochs.

## Step 5.9 — Chronology

- preserve partial-order/incomparability;
- refine local/global chronology frontier representation;
- numeric sparse local ordering remains available but is never inferred as campaign-wide total chronology;
- chronology frontiers are not Git/LOG publication frontiers.

## Step 5.10 — Story projection

- source coverage and editorial revision are distinct;
- coverage must name its source domain;
- Story may lag canonical source and remain valid;
- if an incremental cursor is required, prove it in this slice rather than resurrecting `CURRENT.last_event_id` by default.

## Step 5.11–5.13

- transcript/projection/retention progress is not automatically fictional chronology;
- deletion eligibility must be dependency-safe, not a generic scalar age frontier;
- delivery/disclosure acknowledgement uses interaction/delivery identity, not Story or chronology frontier.

---

# 15. Research-phase conclusion

The minimum model supported by evidence is neither “everything is a frontier” nor “frontier means Git HEAD”.

It is:

```text
Existing semantic owners
        |
        +-- domain-native revisions/cursors/pointers/evidence
        |
        +-- domain-typed frontiers only where progress/coverage/constraint
            boundary is a real concept
                |
                +-- same-domain comparison only
                +-- explicit named cross-domain relations
                +-- no generic Frontier authority/schema

Coherent current/recovery source view
    = compatible scope-indexed composition of the necessary domain markers
      (conceptual only at 5.1)
```

The research finds one likely machine-contract retirement (`CURRENT.last_event_id` as a global cursor) and one likely later-schema correction (`checkpoint.valid_through_event_id` must not remain a universal recovery frontier assumption). Neither should be mechanically changed before the 5.1 design decision is reviewed.

Next required process step: deliberate analytical challenge of Alternative B against the simpler domain-local model before any Decision Brief.
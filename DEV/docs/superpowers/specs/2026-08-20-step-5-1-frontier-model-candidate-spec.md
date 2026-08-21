# Step 5.1 — Frontier Model — Candidate Specification

Status: **CANDIDATE — OWNER-APPROVED B-NARROW, PENDING ADVERSARIAL REVIEW**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Decision basis:

- `2026-08-20-step-5-1-frontier-model-pre-research-charter.md`
- `2026-08-20-step-5-1-frontier-model-task-brief.md`
- `2026-08-20-step-5-1-frontier-model-research-draft.md`
- `2026-08-20-step-5-1-frontier-model-analytical-challenge.md`
- `2026-08-20-step-5-1-frontier-model-decision-brief.md`
- owner approval of **B-NARROW** on 2026-08-20
- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` campaign allocator contract

This candidate defines semantic rules only. It does not introduce a generic runtime frontier object, schema, comparison framework or persistence record.

---

## 1. Scope

Step 5.1 defines the minimum cross-domain vocabulary and invariants required to reason correctly about:

- current versus durably published state;
- campaign publication revisions;
- active live-epoch revisions;
- recovery/checkpoint evidence;
- fictional chronology progress/constraint knowledge;
- runtime execution dependencies and cursors;
- Story projection coverage;
- stale observations and retention safety boundaries.

It does **not** define the physical serialization, publication, checkpoint, live CAS, chronology, Story catch-up or GC protocols owned by later Step-5 slices.

---

## 2. Core decision — B-NARROW

HDM adopts a small shared semantic discipline while keeping every concrete marker and comparison rule domain-native.

### LAW 1 — DOMAIN TYPING

Every progress, coverage, revision, cursor or frontier claim that participates in correctness reasoning SHALL identify the semantic domain and scope in which the value is meaningful.

A bare integer, ID, SHA, sequence or revision number has no cross-domain meaning merely because it is ordered or monotonic in its own representation.

### LAW 2 — NO IMPLICIT CROSS-DOMAIN ORDER

No ordering or dominance relation SHALL be inferred between markers from different semantic domains unless an owning contract explicitly defines that relation.

Superficially similar representations do not create comparability.

Examples:

```text
campaign commit SHA
live epoch revision 17
semantic-event ID semantic-004200
scene chronology sequence 440
Continuation generation 3
RNG frontier rng:42
Story event ID E004200
```

None of these values is comparable to another merely because both are ordered, numeric or sequence-like.

---

## 3. Frontier is not authority

A frontier/progress marker is evidence, a boundary, a cursor, a revision or coverage description relative to some already-defined owner. It does not become semantic authority by existing.

Examples:

```text
world.actor                    semantic authority for actor state
campaign commit SHA            durability/publication evidence
live revision                  revision evidence inside one live epoch
checkpoint ID                  pointer to a recovery descriptor
Story source coverage          projection metadata
Temporal Agenda                derived index, not frontier authority
```

No Step-5 subsystem may introduce a metadata marker that silently duplicates current world/runtime ownership.

---

## 4. Normalized classifications

The following concepts remain distinct.

| Concept | Classification | Notes |
|---|---|---|
| Current HOT gameplay state | current working view | accepted semantic state over a durable base; may be ahead of publication |
| Dirty set | unpublished delta/closure | bookkeeping, not a frontier or authority |
| SOFT/HARD | durability classification/requirement | not a frontier; exact boundary rules belong to 5.5 |
| Authoritative campaign ref | publication authority pointer | identifies which reachable Git commit is current durable campaign publication |
| Reachable campaign commit | scoped durable publication evidence | exact durable tree for campaign-owned scope at that publication |
| Cached/observed HEAD | observation/coordination evidence | may be stale; not authoritative merely because stored in a session |
| Live epoch revision/head | scope-local operational revision evidence | comparable only within the owning live epoch unless an explicit relation is defined |
| Runtime Resolution cursor | execution cursor | not a durability frontier |
| Continuation generation | execution generation | domain-local stale-generation check |
| Continuation dependency refs | dependency/revision evidence | domain-specific references, not generic frontiers |
| RNG frontier | RNG stream position/state | RNG domain only |
| Checkpoint ID | pointer | MANIFEST points to the selected checkpoint |
| Checkpoint | recovery descriptor/evidence | does not own current world state |
| Fictional chronology frontier/evidence | partial-order/time knowledge | separate from Git/event-ID order |
| Story source coverage | projection metadata | may lag canonical source without becoming incorrect |
| Story literary revision | editorial version/revision | distinct from source coverage |
| Retention/GC safety boundary | deletion eligibility evidence | only meaningful after owning dependency predicates are satisfied |
| `runtime.id_allocator` | identity-allocation authority/bookkeeping | not a progress/frontier mechanism |

An existing field name containing `frontier`, `revision`, `cursor` or `last` does not override this classification. Meaning follows the owning contract, not the label.

---

## 5. Campaign publication domain

The campaign durability domain is Git publication on the authoritative long-lived campaign ref.

Normative rules:

1. A prepared Git commit object is not current durable campaign publication merely because the object exists.
2. A campaign commit becomes the current durable campaign publication when the authoritative campaign ref is successfully advanced to that commit according to the publication protocol.
3. A cached or session-recorded SHA is only an observation until validated against the authoritative ref when synchronization correctness requires it.
4. Campaign Git ancestry/order is storage/publication order. It SHALL NOT be interpreted as fictional chronology.
5. An exact campaign revision fixes the durable campaign tree visible at that publication, including its durable LOG contents, without requiring a second global event scalar to identify the same tree.

The exact publication transaction and retry protocol remains Step 5.6.

---

## 6. HOT state relative to durable publication

Current semantic truth and durable publication are distinct axes.

Conceptually:

```text
current HOT view
    = pinned durable campaign base
    + accepted unpublished semantic delta
    + any explicitly active scope-local authority required for the current operation
```

An accepted SOFT fact may therefore be current gameplay truth before it is Git-durable.

This distinction SHALL NOT create a second durable owner. Later slices must specify how the HOT delta survives or is lost at durability/recovery boundaries.

SOFT/HARD are not separate frontier types. Their exact semantics belong to Step 5.5.

---

## 7. Live-epoch revision domain

An active live epoch owns current mutable truth only for its explicitly routed scope.

Normative rules:

1. A live epoch identifies the campaign revision from which its operational scope was based.
2. Live revision/head markers are interpreted only inside that epoch unless an explicit cross-domain relation is named.
3. Revisions from two independent live epochs are incomparable by default.
4. A closed live epoch that has not yet been absorbed is not equivalent to the campaign branch having incorporated its state.
5. Campaign publication and live operational durability may both exist simultaneously for different scopes; neither marker alone describes all current mutable truth during active multiplayer play.
6. The exact lease/CAS/adoption/compaction/absorption protocol belongs to Step 5.8.

No global live-revision counter is introduced by Step 5.1.

---

## 8. Explicit cross-domain relations

Cross-domain relations are allowed only when a concrete owning contract needs them.

Examples of possible relation names include:

```text
based_on
absorbed_from
projected_through
recovered_from
compatible_with
```

Step 5.1 does not define a global relation registry or universal comparison API.

Each later owning slice SHALL define the exact meaning, inputs and validation rule for every cross-domain relation it actually uses.

A relation such as `based_on` does not imply numeric comparability. It states a specific semantic dependency.

---

## 9. Coherent source cut — conceptual term only

For one read, context assembly or recovery operation, HDM may need a compatible set of pinned source markers from multiple domains/scopes.

Step 5.1 calls this a **coherent source cut**.

Conceptually:

```text
requested scope
    campaign-owned records -> exact campaign revision C
    live-owned scene A      -> exact live epoch/revision LA based on an admissible campaign base
    operational roots       -> exact typed owner generations/revisions when required
```

Normative boundaries:

1. `coherent source cut` has no independent record ID, schema, registry or storage contract in Step 5.1.
2. It is not semantic authority.
3. It is not required to be representable as a scalar.
4. It does not make its component markers mutually comparable.
5. Compatibility must be proven by the relevant owning contracts; it cannot be assumed because values were observed in one process or chat.
6. If the required markers cannot be proven compatible for the requested operation, the consumer SHALL refresh, recover or fail according to its owning later-slice protocol rather than invent a mixed view.

Step 5.2/5.7 may determine what subset of this concept must be serialized for cold recovery. Step 5.8 determines live compatibility details.

---

## 10. Runtime operational markers

Step-3 runtime owners remain authoritative for their own operational state.

Examples:

- `runtime.command` owns mandatory descendant closure disposition;
- `runtime.resolution` owns one Activity execution state and cursor;
- `runtime.continuation` owns one portable suspended Resolution generation;
- `runtime.procedure` owns procedure-local ResourceState;
- owner-local TemporalBindings own temporal obligations;
- fixed RNG values and future RNG frontier preserve deterministic continuation where required.

These markers are domain-native. Step 5.1 does not generalize them into a frontier framework.

A Continuation dependency frontier is a dependency condition, while an RNG frontier is an RNG-stream condition. Their shared English word does not make them comparable or structurally identical.

Durable discovery/serialization of active operational roots belongs to Steps 5.2, 5.3 and 5.7.

---

## 11. Campaign-scoped ID allocation is a separate owner

`runtime.id_allocator` / `campaign-allocator` remains the sole campaign-scoped owner for persistent sequential world/runtime record allocation state under the existing catalog contract.

Accepted current semantics remain:

```text
campaign-allocator singleton
    -> last_allocated by identity policy
    -> next derived

allocation + record creation
    -> one atomic HOT operation

canonical allocation change
    -> allocator mutation joins durable publication closure

stale multiplayer publication
    -> reload current allocator
    -> rekey only conflicting unpublished records
    -> retry publication against current campaign revision

published IDs
    -> immutable and never reused
```

This mechanism solves identity allocation/conflict handling. It SHALL NOT be repurposed as campaign progress, fictional chronology, recovery coverage or reconnect frontier.

Story layer-local ID allocation remains outside this campaign world/runtime allocator contract and belongs to Step 5.10.

The exact publication retry mechanics for allocator conflicts remain Step 5.6.

---

## 12. `CURRENT.last_event_id` retirement

`STATE/CURRENT.last_event_id` SHALL be retired as a global semantic-log, recovery or reconnect cursor.

Reasons:

1. Fast campaign reconnect/resync already operates on the campaign revision/HEAD domain and changed-path synchronization.
2. Active shared-scene reconnect belongs to live-epoch revision/state semantics.
3. Campaign-scoped ID allocation/conflict handling belongs to `campaign-allocator`.
4. Fictional chronology belongs to chronology evidence and may be partial.
5. Exact cold recovery may require campaign + live + operational roots and therefore cannot be represented faithfully by one SemanticEvent scalar.
6. The exact durable campaign revision already fixes the LOG tree for campaign-owned durable state at that publication.

Sequential SemanticEvent IDs remain valid stable record identities. Per-record fields such as `last_event_id` may remain legitimate provenance/history anchors when their owning record contract defines that meaning.

This retirement does not prohibit a future domain-specific event-processing cursor if a concrete consumer proves one is required. Such a cursor must have explicit coverage semantics and must not be inferred from generic maximum allocated event ID.

---

## 13. Checkpoint pointer, descriptor and recovery basis

Checkpoint concepts remain separated:

```text
MANIFEST.last_checkpoint_id
    -> pointer to selected checkpoint

runtime.checkpoint
    -> immutable recovery descriptor/evidence

recovery basis
    -> semantic set of authoritative roots/markers required to reconstruct an admissible runtime state
```

A checkpoint does not become current-state authority.

`checkpoint.valid_through_event_id` SHALL NOT be interpreted as a universal recovery frontier. It may remain as a provenance/history anchor if Step 5.7 proves that role useful. Step 5.7 owns its final fate and the final checkpoint serialization/hydration contract.

---

## 14. Chronology domain

Fictional chronology is a separate domain from Git publication and event-ID allocation.

Normative rules:

1. Git commit order does not establish fictional order.
2. SemanticEvent ID order does not establish fictional order.
3. Independent scenes may remain unordered relative to each other.
4. Local numeric/sparse sequences remain permitted inside explicitly scoped chronology domains.
5. A globally reconciled chronology frontier, if retained, describes established chronology knowledge/constraints, not campaign publication progress.
6. The final representation and reconciliation algorithm belong to Step 5.9.

Step 5.1 neither requires nor prohibits scalar values inside one chronology domain. It prohibits treating them as an implicit campaign-global total order.

---

## 15. Story projection domains

STORY remains durable but noncanonical.

Each Story layer may need its own domain-native source-coverage or publication markers.

Normative rules:

1. Story projection may lag authoritative source without making gameplay state incorrect.
2. Source-history coverage and literary/editorial revision are distinct axes.
3. No Story ID or projection marker is automatically comparable to SemanticEvent IDs, Git revisions or chronology markers.
4. If a Story layer defines `projected_through`, that relation must name the source domain and exact coverage semantics.
5. NARRATIVE editing may change literary revision without advancing source coverage.
6. Story publication failure SHALL NOT become canonical gameplay-state failure merely because a Story projection is behind; exact Step-5.10 transaction boundaries remain deferred.

---

## 16. Retention/GC safety boundaries

Retention age, chronology age, event-ID magnitude and publication age are not interchangeable.

A retention/GC boundary means only that material is eligible for deletion/compaction after the owning later-slice dependency conditions are satisfied.

A future GC contract must not infer safety solely from one global sequence number when active Continuations, temporal obligations, checkpoints, live absorption, chronology evidence or Story provenance may still depend on older material.

The exact safety predicates and deletion algorithm belong to Step 5.13.

---

## 17. Stale versus lagging versus incomparable

These terms have distinct meanings.

### Stale

A marker/observation is stale when its own domain has a newer authoritative state that matters to the operation and the observation has not been refreshed.

Example: session cached campaign HEAD `C50`, authoritative campaign ref is `C53` and relevant paths changed.

### Lagging

A projection/consumer is lagging when it validly covers an older source range while the source domain has advanced.

Example: STORY/EVENTS is projected through source X while canonical history has advanced beyond X.

Lagging does not imply corruption.

### Incomparable

Two markers are incomparable when their domains/scopes provide no explicit ordering relation.

Example: live revision 12 in scene A and live revision 9 in scene B.

Neither value is stale merely because the other integer is larger.

---

## 18. Cross-system impact

### Depends on

- Step-2 temporal ownership and rebuildable Agenda model;
- Step-3 RuntimeCommand/Resolution/Procedure/Continuation ownership;
- Step-4 Context Assembler coherent pinned-context requirement;
- one campaign branch + temporary live branches topology;
- current campaign allocator contract;
- Step-5.0 retirement of duplicate/placeholder owners.

### Constrains

- 5.2 Resumable Runtime Closure;
- 5.3 temporal/pending continuity;
- 5.4 session handoff;
- 5.5 SOFT/HARD semantics;
- 5.6 publication/retry;
- 5.7 checkpoint/recovery;
- 5.8 multiplayer/live protocol;
- 5.9 chronology;
- 5.10 Story projection persistence;
- 5.11 transcript retention;
- 5.13 GC.

### Owns

Step 5.1 owns only the cross-domain semantic discipline and classification rules in this specification. It owns no persisted runtime state.

### Does not own

- campaign allocation representation beyond preserving the existing allocator owner;
- physical recovery serialization;
- publication transaction state;
- live CAS state machine;
- chronology algorithm;
- Story projection schema;
- retention algorithm.

---

## 19. Mandatory later-slice constraints

All later Step-5 slices SHALL preserve:

1. no metadata/progress marker becomes duplicate current-state authority;
2. markers are interpreted inside explicit semantic domains/scopes;
3. no cross-domain order is inferred without an explicit relation;
4. one Git SHA is not assumed to describe current live-owned state merely because it describes campaign-owned durable state;
5. HOT current truth may be ahead of durable publication without creating a second permanent owner;
6. identity allocation state remains distinct from progress/recovery/chronology markers;
7. checkpoint descriptors may compose recovery evidence but do not own world state;
8. Story lag is represented as projection state, not campaign corruption;
9. chronology remains independent of Git/Event ID order;
10. any serialized composite recovery description must preserve domain identity rather than collapsing heterogeneous markers into one untyped scalar.

---

## 20. Examples

### Example A — HOT ahead of campaign publication

```text
campaign durable revision = C50
HOT accepted actor HP      = 17
published actor HP at C50  = 23
```

Current gameplay truth may be HP 17 while Git durability remains C50. `SOFT` describes durability treatment; it is not a new frontier owner.

### Example B — stale session observation

```text
session.base_head_sha = C50
authoritative campaign ref = C53
```

The session SHA is stale coordination evidence if the operation requires current synchronization. It does not roll campaign authority back to C50.

### Example C — independent live epochs

```text
scene A -> epoch A revision 12
scene B -> epoch B revision 20
```

`20 > 12` has no semantic meaning across those epochs.

### Example D — campaign and live compatible source selection

```text
campaign-owned faction record -> C53
scene-A mutable combat scope  -> live epoch A revision 12
```

A consumer may use both only if the owning contracts establish that the live epoch is an admissible current authority for that routed scope and compatible with the selected campaign source basis. No numeric comparison between SHA and revision exists.

### Example E — allocator conflict

Two writers allocate the same next unpublished campaign-scoped actor ID from an old pinned allocator state. One publication wins. The loser reloads `campaign-allocator`, rekeys its unpublished actor and direct local references, and retries. No `last_event_id` participates in conflict resolution.

### Example F — Story lag

```text
campaign source revision = C80
STORY/EVENTS coverage    = source material through C77-equivalent domain relation
NARRATIVE editorial rev  = N-revision 14
```

The Story layer can be durably behind without gameplay rollback. NARRATIVE revision 14 is not ordered against campaign C80.

---

## 21. Invalid interpretations

The following are architecture violations:

```text
"semantic-5000 > semantic-4999, therefore the first happened later in fiction"

"live revision 20 is newer than scene B revision 12 because 20 > 12"

"checkpoint.valid_through_event_id is the complete multiplayer recovery point"

"the allocator says actor=100, therefore campaign progress is at 100"

"Story E5000 means Story is caught up through campaign semantic event 5000"
without an explicit projection-coverage contract

"the session remembers HEAD C50, therefore C50 is still the canonical campaign revision"

"a coherent source cut is a new stored owner of campaign state"
```

---

## 22. Deferred questions

Safely deferred to later slices:

- exact Resumable Runtime Closure fields and serialization — 5.2;
- due/pending-work crash states and Temporal Agenda rebuild protocol — 5.3;
- controlled context-loss/session handoff boundary — 5.4;
- exact SOFT/HARD publication requirements — 5.5;
- publication CAS, allocator retry and partial transport failure details — 5.6;
- checkpoint schema, discovery, recovery basis and fate of `valid_through_event_id` — 5.7;
- live lease/revision/CAS/absorption compatibility protocol — 5.8;
- chronology representation and reconciliation — 5.9;
- Story source-coverage representation and concurrent Story ID allocation — 5.10;
- transcript/history retention policy — 5.11;
- host delivery acknowledgement — 5.12;
- GC safety predicate/algorithm — 5.13.

These are not holes in Step 5.1 because this specification defines only the semantic constraints those later contracts must satisfy.

---

## 23. Candidate exit criteria

The candidate is suitable for adversarial review when:

- the B-NARROW decision is represented without a generic Frontier framework;
- every retained cross-domain rule has a current consumer or correctness rationale;
- campaign publication, live revisions, chronology, operational dependencies, allocation and Story coverage remain distinct;
- `CURRENT.last_event_id` has no remaining claimed global role;
- checkpoint event anchoring is explicitly deferred rather than misrepresented as universal recovery;
- later Step-5 slices receive enforceable constraints without their representations being pre-designed.

All criteria are satisfied in this candidate. Canonicalization still requires adversarial review and resolution.
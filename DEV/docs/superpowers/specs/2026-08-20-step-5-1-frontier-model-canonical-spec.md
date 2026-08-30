# Step 5.1 — Frontier Model — Canonical Specification

Status: **CANONICAL — STEP 5.1 CLOSED**

Date: 2026-08-20

Owner decision: **B-NARROW approved**

Derivation chain:

- `2026-08-20-step-5-1-frontier-model-pre-research-charter.md`
- `2026-08-20-step-5-1-frontier-model-task-brief.md`
- `2026-08-20-step-5-1-frontier-model-research-draft.md`
- `../design/2026-08-20-step-5-1-frontier-model-analytical-challenge.md`
- `../design/2026-08-20-step-5-1-frontier-model-decision-brief.md`
- `../design/2026-08-20-step-5-1-frontier-model-candidate-spec.md`
- `../design/2026-08-20-step-5-1-frontier-model-adversarial-review.md`
- `../design/2026-08-20-step-5-1-frontier-model-resolution-gate.md`

This specification owns the Step-5.1 semantic discipline only. Concrete serialization and protocols remain with later Step-5 slices.

---

## 1. Canonical decision

HDM uses domain-native progress/revision/coverage representations governed by two shared laws.

### LAW 1 — DOMAIN TYPING

Every correctness-relevant progress, coverage, revision, cursor or frontier claim SHALL identify the semantic domain and scope in which it is meaningful.

### LAW 2 — NO IMPLICIT CROSS-DOMAIN ORDER

No ordering, dominance or “newer than” relation SHALL be inferred between markers from different semantic domains unless an owning contract explicitly defines that relation.

Representation similarity is not semantic comparability.

No generic Frontier record, JSON schema, registry, comparison API, universal `dominates()` operation, global monotonic sequence or generic RecoveryCut record is introduced.

---

## 2. Frontier/progress metadata is not semantic authority

A frontier, revision, pointer, cursor or coverage marker describes evidence or position relative to an existing owner. It does not become current semantic authority merely by being durable or named `frontier`.

Examples:

```text
world.actor                    -> actor-state authority
campaign commit/ref            -> campaign publication evidence
live epoch revision            -> scope-local operational revision evidence
checkpoint                     -> recovery descriptor/evidence
Story source coverage          -> noncanonical projection metadata
runtime.id_allocator           -> identity-allocation authority/bookkeeping
```

No later Step-5 design may use a progress marker to duplicate current world/runtime state ownership.

---

## 3. Canonical classifications

```text
HOT current state
    current working/read view over native owners; may be ahead of campaign publication

Dirty set
    unpublished delta/closure bookkeeping; not a frontier

SOFT / HARD
    durability classification/requirement; not frontiers

Authoritative campaign ref
    pointer selecting current campaign-durable publication

Reachable selected campaign commit
    exact campaign-durable publication evidence/tree

Cached/session HEAD
    observation/coordination evidence; may be stale

Live epoch head/revision
    live-operational durable revision evidence within one epoch/scope

Resolution.cursor
    execution cursor

Continuation generation/dependency refs
    domain-local execution/dependency evidence

RNG frontier
    RNG-stream state/position only

MANIFEST.last_checkpoint_id
    pointer to selected checkpoint

runtime.checkpoint
    immutable recovery descriptor/evidence, not current-state owner

Chronology frontier/evidence
    partial-order / temporal constraint knowledge

Story source coverage
    projection metadata; may lag canonical source

Story literary revision
    editorial revision, separate from source coverage

Retention/GC safety boundary
    deletion/compaction eligibility evidence subject to dependency predicates

runtime.id_allocator / campaign-allocator
    campaign-scoped identity-allocation authority/bookkeeping; not progress
```

Identical field names such as `frontier` do not imply identical structure, comparison rules or persistence representation.

---

## 4. Campaign publication domain

Campaign-durable publication is defined by the authoritative long-lived campaign ref.

1. A prepared commit object is not current campaign publication merely because it exists.
2. Current campaign publication is the commit selected by the authoritative campaign ref after successful publication.
3. Within this domain, revision reasoning uses ref reachability/ancestry and the publication protocol — never lexical SHA ordering, commit timestamps or SemanticEvent IDs.
4. Cached/session-observed HEAD values are coordination evidence and may be stale.
5. Force-push remains forbidden by inherited architecture.
6. Campaign Git order is storage/publication order and SHALL NOT imply fictional chronology.
7. The exact selected campaign revision fixes the campaign-durable tree, including its LOG contents, without a second global event cursor.

Exact publication/CAS/retry semantics belong to Step 5.6.

---

## 5. Current HOT truth versus durable publication

Current semantic truth and Git durability are distinct axes.

A coherent read may combine:

```text
campaign-owned state at a pinned campaign basis
+ accepted unpublished HOT delta
+ current native live-owned scope where routing says live owns that scope
+ native operational owners required by the operation
```

However:

```text
composed coherent read view
    !=
merged writable authority
```

Every mutation SHALL still route to exactly one current writable owner for the affected entity/scope.

A SOFT fact may be current gameplay truth before campaign publication. This does not create another permanent owner. Step 5.5 owns exact SOFT/HARD/SAVE rules.

---

## 6. Live operational revision domain

An active live epoch owns mutable truth only for its routed scope.

1. Its operational state is based on an identified campaign basis.
2. Its head/revision is interpreted within that epoch/scope.
3. Independent live epochs are incomparable by default.
4. A live-operational durable revision is not the same thing as absorbed campaign state.
5. Closed/persisted live state does not imply campaign absorption.
6. Campaign-durable publication and live-operational durable revision may coexist for different scopes.

Step 5.8 owns lease/CAS/adoption/compaction/absorption mechanics.

---

## 7. Explicit cross-domain relations

A cross-domain relation exists only when an owning contract defines one for a concrete consumer.

Possible relation names include `based_on`, `absorbed_from`, `projected_through`, `recovered_from` or `compatible_with`; Step 5.1 does not establish a mandatory relation registry.

Such relations express a specific dependency/compatibility statement. They do not create generic numeric comparability.

---

## 8. Coherent source cut

`coherent source cut` is a **conceptual selection relation for one read/recovery operation**: a scope-indexed set of native source markers proven compatible for that operation.

It is not:

- an independent owner;
- a snapshot of world/runtime state;
- a required stored record;
- a scalar;
- a generic comparison object.

Its components remain owned by their native domains. If later recovery serialization stores references to them, authority does not transfer into the descriptor.

If compatibility cannot be proven, the consumer must refresh/recover/fail according to its owning protocol instead of constructing a mixed state.

Step 5.2 and 5.7 may determine which references/evidence must survive cold recovery. Step 5.8 owns live compatibility details.

---

## 9. Runtime operational markers stay domain-native

Step-3 ownership is unchanged:

- RuntimeCommand owns mandatory descendant closure disposition;
- Resolution owns one Activity execution state/cursor;
- Continuation owns one portable suspended Resolution generation;
- Procedure owns procedure-local ResourceState;
- owner-local TemporalBindings own temporal obligations;
- fixed RNG values and future RNG state preserve deterministic continuation where required.

`Continuation.dependency_frontier_refs`, RNG frontier and chronology frontier may use the same English word while remaining unrelated machine structures/domains.

Durable placement/discovery belongs to 5.2/5.3/5.7.

---

## 10. Campaign-scoped identity allocation is separate

`runtime.id_allocator` / `campaign-allocator` remains the semantic owner of persistent campaign-scoped sequential world/runtime allocation state under `CATALOG_CONTRACTS.md`.

Accepted semantics remain:

```text
campaign-allocator singleton
    -> last_allocated by identity policy
    -> next derived

allocation + record creation
    -> atomic HOT operation

canonical allocation mutation
    -> joins the same durable publication closure

stale publication conflict
    -> reload allocator
    -> rekey only conflicting unpublished records/direct local refs
    -> retry publication

published IDs
    -> never changed or reused
```

Central semantic ownership of counters does **not** require a synchronous global lock on each gameplay action. Eligible local IDs remain local until promotion needs campaign allocation.

The precise publication/retry protocol belongs to 5.6; live-specific contention belongs to 5.8. If later evidence requires a different physical allocator representation, it may supersede this representation explicitly, but no second allocation authority may arise silently.

Story layer-local allocation belongs to 5.10.

---

## 11. `CURRENT.last_event_id` is retired

`STATE/CURRENT.last_event_id` is not an admitted global semantic-log, reconnect or recovery cursor.

Reasons:

- campaign reconnect/resync is revision/HEAD + scoped changed-path synchronization;
- live reconnect uses live-epoch state/revision semantics;
- campaign-scoped ID collision handling belongs to `campaign-allocator`;
- fictional chronology is separate partial-order evidence;
- cold recovery may require campaign + live + operational roots;
- the exact campaign revision already identifies the durable campaign LOG tree.

The active `current_state` schema/template no longer expose this field.

SemanticEvent IDs remain stable record identities. Per-record `last_event_id` may remain legitimate provenance when its owner explicitly defines that meaning. `checkpoint.valid_through_event_id` remains pending 5.7 and SHALL NOT be treated as the universal recovery frontier.

A future event-processing cursor may be added only if a concrete consumer proves explicit coverage semantics are needed; it must not be inferred from the largest allocated SemanticEvent ID.

---

## 12. Checkpoint semantics at the 5.1 boundary

```text
MANIFEST.last_checkpoint_id
    pointer

runtime.checkpoint
    immutable recovery descriptor/evidence

native world/runtime/live owners
    actual state authorities
```

A checkpoint may later describe a composite recovery basis, but it never becomes current-state authority.

`valid_through_event_id` may survive as a provenance/history anchor if 5.7 proves that role. It is not a complete campaign+live+operational recovery frontier by itself.

---

## 13. Chronology domain

Chronology remains independent from publication and allocation.

1. Git order does not imply fictional order.
2. SemanticEvent ID order does not imply fictional order.
3. Independent scenes may remain unordered.
4. Local numeric/sparse ordering values remain allowed inside explicitly scoped chronology domains.
5. Any globally reconciled chronology marker describes established chronology constraints/knowledge, not campaign publication progress.
6. Step 5.9 owns final representation/reconciliation.

Step 5.1 therefore retires no numeric ordering technique; it only prohibits implicit campaign-global total order across unrelated domains/scenes.

---

## 14. Story projection domains

Story is durable but noncanonical.

1. Story projection may lag authoritative source without gameplay corruption.
2. Source coverage and literary/editorial revision are different axes.
3. Story IDs/markers are not automatically comparable to Git revisions, SemanticEvent IDs or chronology markers.
4. Any `projected_through`-like marker must name its source domain and exact coverage semantics.
5. No scalar campaign-SHA or SemanticEvent-prefix representation is prescribed by 5.1.
6. NARRATIVE may be editorially revised without advancing source coverage.

Step 5.10 owns actual Story coverage/publication/catch-up representation.

---

## 15. Stale, lagging and incomparable

**Stale**: an observation/marker in its own domain is behind a newer authoritative state that matters to the current operation.

**Lagging**: a valid projection/consumer covers an older source range while the source advanced. Lagging is not corruption.

**Incomparable**: no defined ordering relation exists between the markers' domains/scopes.

Examples:

```text
cached campaign HEAD C50 vs authoritative C53
    -> potentially stale

Story projection behind source
    -> lagging

live A revision 12 vs live B revision 20
    -> incomparable by default
```

---

## 16. Retention / GC boundary

Retention age, chronology age, event-ID magnitude and publication age are not interchangeable.

A GC/retention safety boundary only states deletion/compaction eligibility after owning dependency predicates are satisfied. A later GC design must not infer safety from one global scalar while active Continuations, temporal obligations, checkpoints, live absorption, chronology evidence or Story provenance may depend on older material.

Step 5.13 owns exact safety predicates and algorithms.

---

## 17. Later-slice invariants

Steps 5.2–5.13 SHALL preserve:

1. no metadata/progress marker becomes duplicate current-state authority;
2. every correctness-relevant marker is interpreted in its semantic domain/scope;
3. cross-domain ordering requires an explicit owning relation;
4. campaign revision comparison uses publication/ref semantics, not timestamps/SHA lexical order/event IDs;
5. one campaign SHA does not by itself describe current live-owned mutable scope;
6. a composed read view does not merge mutation authority;
7. current HOT truth may be ahead of campaign durability without creating another owner;
8. campaign ID allocation remains distinct from progress/recovery/chronology semantics;
9. checkpoint descriptors point to/describe recovery evidence but do not own state;
10. chronology remains separate from Git/Event allocation order;
11. Story lag is projection state, not campaign corruption;
12. any serialized composite recovery description preserves domain identity rather than collapsing heterogeneous markers into one untyped scalar;
13. live-operational durability, campaign-durable publication and campaign absorption remain separate states/relations.

---

## 18. Explicit deferrals

Step 5.1 does not settle:

- 5.2 Resumable Runtime Closure serialization;
- 5.3 Temporal Agenda/pending-work recovery lifecycle;
- 5.4 controlled context-loss/session handoff;
- 5.5 exact SOFT/HARD/SAVE boundary semantics;
- 5.6 publication CAS/retry/allocator contention mechanics;
- 5.7 checkpoint schema/hydration and final fate of `valid_through_event_id`;
- 5.8 live lease/revision/CAS/absorption protocol;
- 5.9 chronology representation/reconciliation;
- 5.10 Story coverage/publication/concurrent Story allocation;
- 5.11 transcript retention;
- 5.12 delivery acknowledgement;
- 5.13 GC safety algorithm.

These are safely deferred because 5.1 fixes the semantic constraints without pre-selecting their representations.

---

## 19. Validation / closure evidence

Step 5.1 used a focused TDD retirement contract for `CURRENT.last_event_id`.

RED: the new Step-5.1 regression failed while the active schema/template still exposed the global cursor; maintenance audit remained green and the failure was isolated to the new expectation.

GREEN: after removing the field/provisional invariant from `GAME/SCHEMA/current_state.schema.yaml` and the field from `GAME/CAMPAIGN/STATE/CURRENT.yaml`, and aligning the Step-5.0 regression with the new boundary, maintenance audit and the full DEV unit suite passed.

Final closure requires fresh validation of the final branch revision after all canonical/status bookkeeping; that evidence is reported from CI rather than encoded as a mutable run identifier in this specification.

---

## 20. Step 5.1 exit

Step 5.1 is architecturally resolved by approved B-NARROW and the adversarial resolutions above.

The next slice is **Step 5.2 — Resumable Runtime Closure**, but it is not started by this specification.
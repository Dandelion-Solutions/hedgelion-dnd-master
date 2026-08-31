# Step 5.1 — Frontier Model — Adversarial Architecture Review

Status: **REVIEW COMPLETE — NO OWNER BLOCKER; RESOLUTIONS REQUIRED BEFORE CANONICALIZATION**

Date: 2026-08-20

Reviewed candidate:

- `2026-08-20-step-5-1-frontier-model-candidate-spec.md`

Review stance:

> Assume B-NARROW still contains a hidden generalized-frontier framework, loses a real reconnect/recovery capability, or lets a metadata marker become authority. Find concrete failure paths rather than confirming the candidate.

---

## 1. Summary

```text
BLOCKING / owner decision required: 0
SIGNIFICANT, mechanically resolvable: 5
MINOR: 3
REJECTED concerns: 3
```

The central B-NARROW decision survives review.

No evidence justifies a generic Frontier record/schema/API, and no evidence shows that domain-local-only Option A would be safer. The two shared laws remain useful because Context Assembler, recovery composition and multiplayer source selection already cross domain boundaries.

Canonicalization should incorporate the resolutions below.

---

## 2. Finding F1 — `coherent source cut` could become a disguised new owner

Severity: **SIGNIFICANT**

### Attack

A later engineer could interpret:

```text
coherent source cut = campaign SHA + live revisions + operational roots
```

as a new durable aggregate record that owns or snapshots those states. That would recreate the duplicate-authority problem this slice is intended to prevent.

### Assessment

Agree with the risk. The candidate says the term is conceptual only, but canonical wording should be stronger.

### Resolution

Canonical spec SHALL state:

- a coherent source cut is a **selection relation for one operation**, not a state owner;
- its components remain owned by their native domains;
- serializing references to those components later does not copy their authority into the descriptor;
- later 5.2/5.7 may serialize a recovery descriptor only if needed, but that descriptor remains evidence/pointers to owners.

Human decision required: **NO**.

---

## 3. Finding F2 — HOT composition wording could blur mutation authority

Severity: **SIGNIFICANT**

### Attack

The expression:

```text
HOT view = campaign base + accepted delta + active scope-local authority
```

could be read as one merged mutable state owner. During multiplayer that would be wrong: a campaign-owned actor and a live-owned scene may be read together, but writes still route to their respective current authority.

### Resolution

Canonical spec SHALL distinguish:

```text
composed read view
!=
merged writable authority
```

A consumer may assemble one coherent read view from several compatible owners. Mutation must still route to exactly one current writable owner for the affected scope/entity.

Human decision required: **NO**.

---

## 4. Finding F3 — within-domain campaign comparison needs explicit semantics

Severity: **SIGNIFICANT**

### Attack

LAW 2 correctly forbids cross-domain comparison, but the candidate says little about what comparison is legitimate inside the campaign publication domain.

If implementations compare commit timestamps, lexical SHA values or SemanticEvent IDs to decide which campaign state is newer, B-NARROW would not stop them.

### Resolution

Canonical spec SHALL state:

- campaign publication comparison uses authoritative ref reachability/ancestry and the publication protocol;
- SHA lexical order and wall-clock commit timestamp have no revision-order meaning;
- an unreachable prepared commit is not current publication;
- force-push remains forbidden by inherited architecture;
- this storage order still has no fictional chronology meaning.

Exact publication CAS remains Step 5.6.

Human decision required: **NO**.

---

## 5. Finding F4 — `campaign-allocator` may be mistaken for a serialized global lock

Severity: **SIGNIFICANT**

### Attack

The candidate preserves one centralized allocation owner. A literal implementation could serialize all multiplayer gameplay behind one allocator lock or make every local incidental object require immediate global allocation.

That would create contention and violate the hot-path/local-promotion model.

### Repository evidence

The accepted catalog contract already separates:

- session-local `local-*` IDs for eligible incidental records;
- durable campaign IDs at promotion/publication;
- optimistic publication against a pinned campaign frontier;
- rekey of conflicting **unpublished** records after a stale publication conflict.

### Resolution

Canonical spec SHALL clarify:

- centralized **semantic ownership of allocation counters** does not imply a global synchronous lock on every gameplay action;
- eligible local identities remain local until promotion requires campaign allocation;
- allocation conflict/retry mechanics remain Step 5.6/5.8 concerns;
- if later evidence proves the singleton allocator cannot meet multiplayer requirements, superseding its representation is allowed, but no second allocation authority may be introduced silently.

Human decision required: **NO**. The owner already confirmed centralized counter ownership as intended.

---

## 6. Finding F5 — `CURRENT.last_event_id` removal must not remove reconnect capability

Severity: **SIGNIFICANT**

### Attack

If a reconnect path actually uses `CURRENT.last_event_id` to skip LOG scanning, removing the field might create an expensive broad recovery read or lose an event-processing cursor.

### Evidence

Current runtime reconnect/synchronization guidance instead uses:

```text
branch-ref HEAD probe
    -> base..HEAD changed-path comparison when HEAD changed
    -> exact relevant file reads pinned to one HEAD
```

Campaign-scoped allocation conflicts are owned by `campaign-allocator`; live reconnect is owned by live epoch/head/state; chronology is not event-ID order.

No current correctness contract was found that requires `CURRENT.last_event_id` as a dense event-processing coverage cursor.

### Resolution

Retire the field from active CURRENT template/schema as part of 5.1 cleanup.

Preserve:

- SemanticEvent IDs as record identities;
- per-record `last_event_id` when it is explicit provenance;
- checkpoint `valid_through_event_id` until Step 5.7 decides its narrower role;
- the possibility of a future explicit event-processing cursor if a real consumer proves it needs one.

Human decision required: **NO**; the owner explicitly agreed the field should be removed rather than pretend to solve the global problem.

---

## 7. Finding F6 — Story coverage example could be misread as campaign-SHA scalar coverage

Severity: **MINOR**

### Attack

An example using `C77-equivalent` may imply every Story layer should store one campaign commit as its coverage frontier.

That is not established. Story source coverage may eventually be source-ref/set/index based and may need to represent partial/nonlinear source material.

### Resolution

Canonical wording SHALL avoid prescribing one scalar Story coverage representation. It should state only that any projection marker identifies its source domain and exact coverage semantics. Step 5.10 decides representation.

---

## 8. Finding F7 — existing field names containing `frontier` may be over-normalized

Severity: **MINOR**

### Attack

`dependency_frontier_refs`, `future_rng_frontier` and chronology `frontier` use the same English word for different concepts. A future refactor could try to normalize them into one structure because Step 5.1 introduces shared laws.

### Resolution

Canonical spec SHALL explicitly say the two laws apply to correctness-relevant markers **regardless of field name**, while identical naming does not imply common structure. Existing names may remain until their owning slice has a reason to change them.

---

## 9. Finding F8 — active live durability wording needs two axes

Severity: **MINOR**

### Attack

A live branch/head may be durably stored operationally while not yet absorbed into campaign canon. Calling it simply “durable” can confuse operational persistence with campaign publication.

### Resolution

Canonical spec SHALL use scoped language:

```text
campaign-durable publication
live-operational durable revision
absorbed campaign state
```

and never infer absorption from live persistence alone.

---

## 10. Rejected concern R1 — a universal Frontier type would enforce the laws better

Disposition: **REJECTED**

A generic type would not remove domain-specific validation. It would instead create a tempting but false common comparison surface for Git ancestry, live revision, chronology partial order, RNG state and Story coverage.

The current correctness need is semantic domain tagging and explicit relation ownership, not shared serialization.

---

## 11. Rejected concern R2 — `CURRENT.last_event_id` should be kept as a harmless cache

Disposition: **REJECTED**

A persisted cache with ambiguous semantics is not harmless in this architecture. It invites future reconnect/recovery code to treat it as an admitted cursor and recreates a second ambiguous progress marker.

If a cache is later proven useful, it should be derived/rebuildable or introduced with explicit coverage semantics and a consumer.

---

## 12. Rejected concern R3 — one global numeric order would simplify recovery and Story

Disposition: **REJECTED**

It would collapse storage order, fictional chronology, projection coverage and concurrency into one false total order. Independent live scenes and partial fictional chronology are existing accepted requirements, not hypothetical edge cases.

---

## 13. Cross-system challenge results

### Context Assembler

B-NARROW is sufficient if source compatibility is validated by owning contracts. It does not need a generic frontier API.

### Cold recovery

A recovery descriptor may need references from several domains. B-NARROW permits this without making the descriptor authority. Exact serialization remains 5.2/5.7.

### Multiplayer

The model correctly permits multiple incomparable live revision domains. Allocator ownership stays separate from live progress.

### Chronology

The model does not total-order independent scenes and does not derive time from Git/Event IDs.

### Story

Projection can lag and maintain its own coverage semantics without affecting gameplay canon.

### Retention/GC

The model prevents a naive “delete everything below global ID N” rule but leaves exact safety predicates to 5.13.

---

## 14. Resolution recommendation

Proceed to Resolution Gate with B-NARROW unchanged at the decision level.

Canonicalization should incorporate these mechanical refinements:

1. coherent source cut is a read/recovery selection relation, never an authority;
2. composed read views never merge mutation authority;
3. campaign revision comparison uses ref/ancestry semantics, not timestamp/SHA/event ID;
4. central allocator ownership does not imply global hot-path locking;
5. retire `CURRENT.last_event_id` from active CURRENT machine/template surface;
6. avoid scalar Story-coverage implication;
7. shared English `frontier` names do not imply common structure;
8. distinguish campaign-durable, live-operational durable and absorbed state.

No finding requires reopening the owner-approved B-NARROW decision.
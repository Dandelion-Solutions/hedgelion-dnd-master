# Implementation Planning — LIVE Source-Native Creation Ordering Addendum

Status: **MANDATORY OVERLAY — AUTHOR FINDING 26 REPAIR / INDEPENDENTLY UNCONFIRMED**

Scope: planning only. This addendum does not authorize production implementation.

This overlay has higher precedence than Finding-24 wording that says a frozen "normalized mutation list establishes the slot order" without defining the normalization/ordering contract. It amends RD-09 source-native identity / frozen LIVE publication only at the attempt-local creation-order seam and extends RD-07 recovery proof of accepted/indeterminate allocations.

## Finding 26 — SIGNIFICANT

Finding 24 correctly introduced a CAS-owned source-local creation cursor and `creation_slot_index`, but it left one persisted-identity decision ambiguous: how multiple `SOURCE_NATIVE_LIVE` creations in the same logical LIVE mutation acquire a stable slot order before final IDs are computed.

Fresh owner review shows:

- WP-16 requires a frozen normalized native LIVE delta but does not define a universal ordering of created records;
- Step-5.8 requires source-local accepted creation coordinates but intentionally gives them no fictional ordering meaning;
- Step-3 defines owner-specific ordinals such as MechanicalEvent `(segment_id,event_ordinal)` and Effect recency keys, but those local semantics cannot be promoted into one universal LIVE creation order;
- sorting by final native ID is circular because the final ID depends on the allocated ordinal;
- sorting arbitrary payload JSON/hash would invent semantic distinctions and fails for duplicate-equivalent payloads;
- relying on Python/dictionary/set iteration, model output order, timestamps or randomness would make persistent identity implementation-dependent.

Therefore the implementation package needs one exact **technical attempt-local normalization law** while preserving native owner ordering and refusing to fabricate order where the native producer cannot supply one.

This is delegated machine realization, not an architecture reopen.

---

## 1. Creation candidate contract

Only `SOURCE_NATIVE_LIVE` families participate. `OWNER_EQUIVALENT` and `FORBIDDEN` families never enter this allocation list.

Each native owner adapter contributing LIVE-born creations to one frozen mutation produces an **ordered sequence per native family**. Before final ID allocation, RD-09 represents each candidate conceptually as:

```text
SourceNativeCreationCandidate {
    native_family
    owner_local_creation_index: uint32
    native_draft
}
```

`owner_local_creation_index` is an attempt-local technical ordering projection, not a native record ID, chronology, priority or durable semantic owner.

For each `native_family` present in one attempted mutation:

```text
owner_local_creation_index == 0,1,2,...,m-1
```

with no gaps and no duplicates.

The family-native adapter is responsible for producing this ordered sequence from its already accepted/frozen native mutation semantics. If the owner can expose only an unordered bag/set of multiple creations and has no deterministic owner-local sequence, the LIVE attempt is **not allocatable** and freezes as typed BLOCKED/invalid input rather than choosing an arbitrary order.

A single creation in a family uses index `0`.

No new persistent per-family counter is introduced by this field.

---

## 2. Exact global attempt-local normalization

Add/extend an RD-09 helper conceptually:

```text
normalize_source_native_creations(
    family_creation_sequences,
    current_live_birth_table,
) -> tuple[NormalizedSourceNativeCreation, ...] | BLOCKED
```

Exact v1 normalization algorithm:

1. validate every family against the current exhaustive `live_birth` table;
2. reject any `OWNER_EQUIVALENT`, `FORBIDDEN`, unknown or missing-policy family;
3. for each `SOURCE_NATIVE_LIVE` family, require exactly one ordered owner sequence for this logical LIVE mutation;
4. validate its `owner_local_creation_index` values are contiguous `0..m-1` and unique;
5. order family groups by ascending raw UTF-8 bytes of the exact canonical native-family ID (the current IDs are ASCII and therefore byte/lexical order agree);
6. within each family group preserve ascending `owner_local_creation_index`;
7. concatenate the groups into one normalized creation array;
8. assign `creation_slot_index` as the zero-based position in that final array.

Formally:

```text
normalized = sort(
    candidates,
    key=(UTF8(native_family), owner_local_creation_index)
)

for i, candidate in enumerate(normalized):
    candidate.creation_slot_index = i
```

This sort is purely a reproducibility/allocation device. It SHALL NOT be interpreted as fictional chronology, causal priority, execution priority, source currentness or owner precedence.

Do not sort by payload bytes, payload hash, provisional/final native ID, wall clock, Git commit/ref order, actor/player identity, LLM output ordering, dictionary/hash iteration or random value.

---

## 3. Cursor allocation against the normalized array

Finding 24's CAS-owned cursor remains:

```text
next_source_native_creation_ordinal: uint64
```

For a normalized array of length `n` and frozen expected cursor `start`:

```text
source_local_creation_ordinal[i] = start + creation_slot_index[i]
next_cursor_after = start + n
```

Before any remote mutation, the frozen attempt stores for every creation:

```text
SourceNativeAllocation {
    native_family
    owner_local_creation_index
    creation_slot_index
    source_local_creation_ordinal
    native_id
}
```

and stores:

```text
expected_next_source_native_creation_ordinal = start
resulting_next_source_native_creation_ordinal = start + n
```

The final native IDs are then computed using the current Finding-24 encoding as corrected by Finding 25 (`campaign_id`, not physical route token).

The exact-source CAS atomically establishes:

- every created native record/delta and all intra-delta references to those final IDs;
- the exact allocation array/basis required by the frozen attempt contract;
- the cursor advance to `start+n`.

No accepted state may contain only a cursor advance without its corresponding accepted creations, or accepted creations without the matching cursor advance.

---

## 4. Native owner ordering rule

This overlay intentionally does **not** invent a universal semantic ordering key for all world/runtime owners.

Instead:

- where the native producer already has an accepted deterministic sequence/ordinal, its adapter maps that sequence to contiguous `owner_local_creation_index` without changing meaning;
- where the producer establishes multiple outputs in a deterministic typed list, list position is the technical owner-local creation order;
- where a producer's semantic output is explicitly unordered and no accepted native rule distinguishes multiple occurrences, RD-09 may not manufacture an order from serialization/hash/time. The attempt returns a typed `LIVE_CREATION_ORDER_UNRESOLVED` or current-owner equivalent and the producer/owning integration must supply an admitted deterministic sequence before publication.

Examples of existing owner-local order that may be consumed when applicable include a stable execution/result output sequence. Existing specialized identities such as MechanicalEvent `(segment_id,event_ordinal)` remain `OWNER_EQUIVALENT` and therefore are not allocated here.

An owner-local index is not persisted into the created record solely to create new gameplay semantics. It is retained only where the frozen attempt/reconciliation evidence needs it to prove the allocation mapping.

---

## 5. Retry / stale / indeterminate semantics

### 5.1 Frozen attempt

Once one `FrozenLivePublicationAttempt` has been constructed, its normalized creation order and allocations are immutable.

Serialization/deserialization or local process restart of that same frozen attempt must preserve exact equality of:

```text
(native_family,
 owner_local_creation_index,
 creation_slot_index,
 source_local_creation_ordinal,
 native_id)
```

### 5.2 Definite stale rejection

If exact-source CAS is definitively `REJECTED_STALE` / `NOT_APPLIED`, none of that attempt's prospective IDs became canonical.

After refreshing/revalidating current source and authorization, a **new** frozen attempt may start from the new cursor. Its prospective ordinals/IDs are allowed to differ. Do not create aliases from the rejected prospective IDs.

This is consistent with Step-5.8: rejected prospective coordinates are noncanonical.

### 5.3 Indeterminate outcome

If publication outcome is `INDETERMINATE`, the implementation MUST reconcile the original frozen attempt against the bounded exact source/lineage evidence before allocating anything again.

While outcome remains ambiguous:

- do not rebuild the mutation into a new creation order;
- do not reserve/advance another ordinal range;
- do not publish aliases or remap the original IDs;
- do not rerun a producer merely to generate a new technical order.

If reconciliation proves the original transition accepted, its exact allocation array is canonical. If reconciliation proves it did not apply, only then may a refreshed new attempt allocate from current cursor.

---

## 6. Exact RD-09 machine changes

RD-09 Task 5 / Finding 24 identity realization is extended with the normalization helper and candidate/allocation contract above.

RD-09 Task 6 frozen attempt schema SHALL represent the required order evidence explicitly. `DEV/SCHEMAS/live-publication-attempt.schema.json` must be able to validate conceptually:

```text
source_native_allocations[] {
    native_family
    owner_local_creation_index
    creation_slot_index
    source_local_creation_ordinal
    native_id
}
expected_next_source_native_creation_ordinal
resulting_next_source_native_creation_ordinal
```

Validation requires:

- allocations ordered by `creation_slot_index`;
- slot indexes exactly `0..n-1`;
- ordinals exactly `expected_cursor + slot_index`;
- resulting cursor exactly `expected_cursor + n`;
- no duplicate `(native_family, owner_local_creation_index)`;
- no duplicate native IDs/ordinals;
- only `SOURCE_NATIVE_LIVE` families present.

`GAME/TOOLS/live_state.py` owns the technical normalization/allocation operation. It does not own the semantic ordering inside native producer domains.

---

## 7. Exact tests

Add RD-09 group:

```text
SourceNativeCreationOrderingTests
```

Required cases:

1. two calls with identical family creation sequences produce byte-for-byte equal normalized order and slot indexes;
2. caller map/dictionary insertion order of family groups cannot affect result;
3. family groups are ordered by exact native-family UTF-8 bytes;
4. within a family, owner-local indexes `0..m-1` are preserved;
5. duplicate/gapped/out-of-order owner-local indexes are rejected rather than silently renumbered from arbitrary container order;
6. unordered multiple creations without deterministic owner-local sequence are BLOCKED;
7. two payload-equivalent creations remain distinct when the native owner sequence gives indexes 0 and 1;
8. payload/hash/time/random/final-ID sorting is absent;
9. allocation ordinal equals `start + creation_slot_index` exactly;
10. resulting cursor equals `start+n` exactly;
11. same frozen attempt round-trips with identical allocation array;
12. definite stale rejection permits a new attempt from refreshed cursor without treating rejected IDs as canonical;
13. indeterminate outcome forbids a second allocation until reconciliation proves NOT_APPLIED;
14. accepted allocation survives close/recovery/absorption unchanged;
15. ordering cannot be consumed as fictional chronology/priority in any current consumer.

Extend RD-09 `SourceNativeAmbiguousPublicationTests` to use the exact frozen allocation array rather than merely checking cursor reuse.

Extend RD-07 `SourceNativeLiveRecoveryTests` to prove recovered accepted source-native IDs are validated against the accepted allocation/cursor evidence where that evidence is required by the final LIVE contract, without reconstructing identity from current container iteration.

---

## 8. File impact

Mandatory execution-time surfaces, subject to fresh currentness:

```text
RD-09
  MODIFY GAME/TOOLS/live_state.py
  MODIFY DEV/SCHEMAS/live-publication-attempt.schema.json
  MODIFY DEV/TESTS/test_rd09_access_live.py
  MODIFY GAME/SCHEMA/live_scene.schema.yaml only if accepted allocation/cursor evidence is represented there by the final F24 contract

RD-07
  MODIFY GAME/TOOLS/recovery.py
  MODIFY DEV/TESTS/test_rd07_recovery.py
```

No campaign allocator, global sequence service, timestamp allocator, UUID/random allocator or generic ordering service is introduced.

---

## 9. Execution/checkpoint joins

The F26 order/allocation GREEN is part of the same RD-09 source-native identity integration as F24/F25; it must exist before RD-16 final shared identifier-policy proof may claim `SOURCE_NATIVE_LIVE` executable realization and before RD-07 selected-LIVE recovery can close source-native identity.

Conceptually:

```text
RD-09 LIVE_CAMPAIGN_ROUTE_IDENTITY_READY        # F25
+ RD-09 SOURCE_NATIVE_CREATION_ORDER_READY      # F26
+ RD-09 SOURCE_NATIVE_CURSOR_ENCODING_READY     # F24 corrected by F25
    JOIN_BEFORE_INTEGRATION
RD-09 SOURCE_NATIVE_LIVE_ID_READY

RD-09 SOURCE_NATIVE_LIVE_ID_READY
    HARD_PRECEDES relevant RD-16 shared identifier-policy final proof
    JOIN_BEFORE_INTEGRATION -> RD-07 source-native selected-LIVE recovery proof
```

The join does not serialize unrelated RD-16 schema work or unrelated RD-07 recovery foundations.

All checkpoints obey the package checkpoint-coherence overlay; future RED groups are not pre-created.

---

## 10. Negative stale proof

Implementation/proof fails if any current path permits:

- native IDs to depend on unordered dictionary/set iteration;
- sorting creations by final ID, payload hash, serialized payload, timestamp or random value;
- a generic global creation sequence or fictional-order interpretation of allocation slots;
- missing/duplicate/gapped owner-local order to be silently repaired by arbitrary enumeration;
- `OWNER_EQUIVALENT`/`FORBIDDEN` families to consume source-native cursor slots;
- cursor advance and accepted creation set to become non-atomic;
- definite rejected prospective IDs to be treated as aliases/canonical history;
- indeterminate attempt to allocate a second range before original-outcome reconciliation;
- recovery to regenerate accepted source-native IDs from current iteration order.

---

## 11. Proof routing

Add post-graph proof row `PG26`:

```text
PG26 deterministic attempt-local source-native creation ordering
  -> RD-09 native-family ordered candidate normalization
  -> exact slot/index/cursor allocation
  -> exact-source CAS frozen-attempt preservation
  -> indeterminate reconciliation without reallocation
  -> RD-07 accepted allocation recovery
```

Exact witnesses:

```text
RD-09 SourceNativeCreationOrderingTests
RD-09 SourceNativeAmbiguousPublicationTests
RD-09 SourceNativeLiveIdEncodingTests
RD-07 SourceNativeLiveRecoveryTests
```

Primary channels: `FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT`.

---

## 12. Version / migration disposition

The ordering/index fields are unreleased v1 attempt/evidence realization. No compatibility shim is required for provisional pre-v1 attempt shapes. Run the normal execution-time Version Impact Gate for the affected LIVE attempt schema and any LIVE-state local schema field that survives into the final contract.

---

## 13. Disposition

```text
AUTHOR_FINDING_26: REPAIRED_IN_PLANNING
SEVERITY: SIGNIFICANT
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```

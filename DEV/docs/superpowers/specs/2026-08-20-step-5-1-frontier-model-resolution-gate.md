# Step 5.1 — Frontier Model — Resolution Gate

Status: **RESOLVED — READY FOR MACHINE CLEANUP AND CANONICALIZATION**

Date: 2026-08-20

Decision: **B-NARROW approved by human architect**

Inputs:

- `2026-08-20-step-5-1-frontier-model-candidate-spec.md`
- `2026-08-20-step-5-1-frontier-model-adversarial-review.md`
- owner clarification that centralized campaign counters belong to their own allocation/conflict mechanism and `CURRENT.last_event_id` should be removed rather than treated as a global solution

---

## 1. Resolution summary

The adversarial review found no blocking issue and no new owner decision.

```text
BLOCKING / owner decision required: 0
SIGNIFICANT mechanically resolvable: 5
MINOR: 3
```

The owner-approved B-NARROW decision remains unchanged:

```text
LAW 1 — DOMAIN TYPING
Correctness-relevant progress/coverage/revision/cursor/frontier claims identify their semantic domain/scope.

LAW 2 — NO IMPLICIT CROSS-DOMAIN ORDER
Markers from different domains are not ordered/comparable unless an owning contract explicitly defines the relation.
```

No generic Frontier record, schema, API, registry, global sequence or RecoveryCut record is admitted.

---

## 2. Finding resolutions

### F1 — coherent source cut could become a disguised owner

Severity: SIGNIFICANT

Agree: **YES**

Resolution:

`coherent source cut` is only a selection/compatibility relation for one read or recovery operation. Its components remain owned by native campaign/live/runtime domains. Any later serialized descriptor contains references/evidence only and does not inherit authority from referenced state.

Human decision required: **NO**

### F2 — composed HOT/read view could blur writable authority

Severity: SIGNIFICANT

Agree: **YES**

Resolution:

Canonical wording SHALL state:

```text
composed coherent read view
    !=
merged writable authority
```

Every mutation still routes to exactly one current writable owner for the affected scope/entity.

Human decision required: **NO**

### F3 — campaign within-domain comparison needs explicit semantics

Severity: SIGNIFICANT

Agree: **YES**

Resolution:

Campaign publication ordering uses authoritative ref reachability/ancestry under the publication protocol. Lexical SHA comparison, commit timestamps and SemanticEvent IDs do not establish campaign revision order. Force-push remains prohibited. Campaign storage order still does not imply fictional chronology.

Human decision required: **NO**

### F4 — centralized allocator could be mistaken for a global lock

Severity: SIGNIFICANT

Agree: **YES**

Resolution:

`runtime.id_allocator` / `campaign-allocator` remains the sole semantic owner of campaign-scoped allocation counters under the accepted catalog contract. This does not imply a synchronous global lock on ordinary gameplay. Eligible local IDs remain local until promotion; allocation conflict/retry details remain 5.6/5.8 work. A future representation may supersede the singleton if evidence requires it, but no second allocation authority may appear silently.

Human decision required: **NO**

### F5 — retiring `CURRENT.last_event_id` must preserve reconnect capability

Severity: SIGNIFICANT

Agree: **YES**

Resolution:

Retire `STATE/CURRENT.last_event_id` from the active current-state schema/template. Existing reconnect/resync correctness uses campaign revision/HEAD plus changed-path synchronization; live reconnect uses live-epoch state; campaign ID conflict resolution uses `campaign-allocator`; chronology uses chronology evidence; cold recovery uses its own later recovery basis.

SemanticEvent IDs remain valid identities. Per-record provenance `last_event_id` fields are unaffected. `checkpoint.valid_through_event_id` remains pending Step 5.7. A future explicit event-processing cursor may be admitted only if a concrete consumer proves explicit coverage semantics are needed.

Human decision required: **NO**

### F6 — Story example implied scalar coverage

Severity: MINOR

Resolution:

Canonical spec will avoid prescribing a scalar campaign-SHA Story coverage representation. Step 5.10 owns projection-coverage representation.

### F7 — shared word `frontier` may imply shared structure

Severity: MINOR

Resolution:

Canonical spec will state that field names do not imply common machine shape or comparison behavior.

### F8 — live durability wording needs scoped axes

Severity: MINOR

Resolution:

Canonical terminology will distinguish:

```text
campaign-durable publication
live-operational durable revision
absorbed campaign state
```

Live operational persistence does not imply campaign absorption.

---

## 3. Rejected concerns

The review's three rejected concerns remain rejected:

1. a universal Frontier machine type is not justified;
2. an ambiguous persisted `CURRENT.last_event_id` is not a harmless cache;
3. one global numeric order would incorrectly collapse publication, fictional chronology, projection coverage and multiplayer concurrency.

---

## 4. Immediate machine cleanup authorized by this resolution

The only current machine/template cleanup mechanically implied by Step 5.1 is:

```text
REMOVE
    GAME/SCHEMA/current_state.schema.yaml -> fields.last_event_id
    GAME/SCHEMA/current_state.schema.yaml -> provisional last_event_id invariant
    GAME/CAMPAIGN/STATE/CURRENT.yaml       -> last_event_id
```

This field is optional/provisional in schema version 2, so this cleanup does not by itself create a new required-data schema version. Migration/compatibility treatment for old campaign records remains part of the later integrated migration program.

No other current-state field is removed by Step 5.1. In particular, `CURRENT.world_time.frontier` remains until Step 5.9 decides chronology representation.

---

## 5. Canonicalization gate

Proceed after:

1. a regression test proves the active current-state schema/template no longer expose the retired global cursor;
2. the cleanup is applied and validation passes;
3. the canonical Step-5.1 specification incorporates all resolutions above;
4. roadmap/status identifies Step 5.1 as closed and Step 5.2 as the next unstarted slice.

No further human architecture decision is required for Step 5.1 unless cleanup/validation exposes a contradiction.
# Implementation Planning — Source-Native LIVE ID Encoding / Allocation Addendum

Status: **MANDATORY OVERLAY — AUTHOR FINDING 24 REPAIR / INDEPENDENTLY UNCONFIRMED**

Scope: planning only. This addendum does not authorize production implementation.

This overlay has higher precedence than RD-09 Task 5 and the WP-16 executable-closure addendum where those artifacts require source-native LIVE identity but leave the final printable encoding or accepted source-local creation-coordinate allocation unspecified.

## Finding 24 — SIGNIFICANT

The accepted architecture requires externally referenceable owners first made durable inside independent LIVE epochs to receive collision-free source-native identity without campaign-allocator mutation; the identity freezes at the same accepted LIVE transition as creation and never rekeys merely because the epoch later absorbs into campaign.

The current implementation package is not worker-ready for that duty:

- RD-09 Task 5 repeats the semantic identity basis but does not select the source-local coordinate allocator;
- the WP-16 executable-closure addendum requires tests under the "final encoding rules" but does not define those rules;
- the current legacy `GAME/SCHEMA/live_scene.schema.yaml` still exposes `created_entities[].provisional_id` and an invariant that epoch-scoped provisional entity IDs cannot escape before durable compaction, which permits a provisional -> campaign-rekey interpretation incompatible with the v1 baseline for `SOURCE_NATIVE_LIVE` families;
- without an exact allocation/CAS rule, two workers could choose different local-coordinate schemes, retry behavior or persistent ID syntax while still believing they satisfy the same architecture.

This is delegated machine realization, not an architecture reopen: Step-5.8/WP-16 already fix the semantic identity basis and intentionally leave printable encoding as an implementation detail.

## 1. Stable LIVE source key

For the v1 baseline, define the source-native identity source key as the stable logical LIVE route tuple:

```text
LiveSourceKey {
    campaign_technical_id
    scene_id
    epoch_id
}
```

All three components are canonical stable identity/routing values already required to select the LIVE epoch. A Git branch name, mutable ref, exact source revision/HEAD, local checkout path, timestamp, host identity or session identity is **not** part of the semantic ID source key.

The exact source revision remains the CAS/currentness fence and is intentionally excluded from identity so accepted IDs survive later exact-source revisions and absorption.

If execution-time owner evidence proves the accepted LIVE routing contract has renamed these three fields without changing their semantics, use the exact current names. Do not replace this logical tuple with a mutable transport ref.

## 2. Source-local creation coordinate

Every selected LIVE source persists:

```text
next_source_native_creation_ordinal: uint64
```

Rules:

- initial value = `1`;
- valid accepted ordinal range = `1 .. 2^64-1`;
- the ordinal is local to one `LiveSourceKey`;
- it is uniqueness/allocation state only;
- it is **not** chronology, fictional time, priority, ordering authority, generation, source revision, CAS fence or campaign sequence;
- exhaustion fails closed with a typed allocation error; ordinals are never reused or wrapped.

A source-native creation transition freezes `n >= 1` creation slots and allocates the contiguous accepted coordinate range:

```text
[start, start + n)
where start = current.next_source_native_creation_ordinal
```

The transition's frozen normalized mutation list establishes the slot order before IDs are computed. Slot order is an implementation serialization detail only and carries no chronology/priority meaning.

The exact-source CAS publishes **atomically in one complete new LIVE source state**:

1. every newly created source-native record under its final canonical ID;
2. every internal/ref occurrence of those IDs required by that native transition;
3. `next_source_native_creation_ordinal = start + n`.

If `start + n - 1 > 2^64-1`, the transition is rejected before publication.

Competing transitions prepared from the same prior source may propose the same ordinal(s). Only one exact-source CAS can accept. IDs from a confirmed stale/rejected prospective transition are noncanonical and may be discarded; no tombstone or campaign allocation is required for them.

## 3. Exact printable encoding

For every identifier-policy row whose final `live_birth.disposition` is `SOURCE_NATIVE_LIVE`, the v1 printable encoding is `framed_base32hex_v1`.

Let `prefix` be that native family's final ordinary identifier-policy prefix.

Define framed bytes:

```text
FRAME =
    UTF8("HDM-LIVE-ID-V1")
    + 0x00
    + U32BE(len(UTF8(campaign_technical_id))) + UTF8(campaign_technical_id)
    + U32BE(len(UTF8(scene_id)))              + UTF8(scene_id)
    + U32BE(len(UTF8(epoch_id)))              + UTF8(epoch_id)
    + U32BE(len(UTF8(native_family)))          + UTF8(native_family)
    + U64BE(source_local_creation_ordinal)
```

Then:

```text
payload = lowercase(unpadded_base32hex(FRAME))
source_native_live_id = prefix + ":live1:" + payload
```

Properties:

- the encoding is injective for valid framed component tuples; it does not rely on probabilistic hash collision resistance;
- it uses only the current machine-ID-safe alphabet (`[A-Za-z0-9_.:-]` after the alphabetic family prefix);
- the family is included inside the frame even though the diagnostic prefix also identifies it;
- the version marker is explicit and immutable for this encoding contract;
- no transport branch/ref/revision or wall-clock value participates;
- lexicographic or decoded ordinal order has **no** chronology/priority/eligibility/currentness meaning.

Implement deterministic helpers in the RD-09 owner module, conceptually:

```text
encode_source_native_live_id(
    live_source_key,
    native_family,
    source_local_creation_ordinal,
    identifier_policy,
) -> NativeId

parse_source_native_live_id(native_id, identifier_policy)
    -> SourceNativeLiveIdentityComponents | INVALID
```

Parsing/validation is for integrity/audit/debugging; semantic routing still follows native owner identity/routing contracts and never treats encoded ordinal order as authority.

## 4. Identifier-policy machine contract

RD-16 remains the one final writer of shared identifier-policy machine surfaces.

Extend the final identifier-policy schema so `live_birth` is a closed typed object rather than an untyped prose disposition.

For `SOURCE_NATIVE_LIVE` rows require:

```json
{
  "disposition": "source_native_live",
  "encoding": "framed_base32hex_v1"
}
```

For `OWNER_EQUIVALENT` and `FORBIDDEN` rows, `encoding` is absent unless their own owner contract explicitly defines a different encoding field. Do not silently apply `framed_base32hex_v1` to derived/composite/owner-equivalent families.

RD-09 owns the source-native semantics and encoding implementation/tests. RD-16 consumes `RD09_SOURCE_NATIVE_ID_READY` and performs the single final shared `identifier-policies.schema.json` / `identifier-policies.json` integration together with the already planned MechanicalEvent, PLAYER, thread and live-birth dispositions.

## 5. LIVE_STATE v1 machine realization

RD-09 Task 3/5/6 jointly replace the legacy LIVE schema for v1.0.

The final LIVE envelope must:

- persist `next_source_native_creation_ordinal` while the epoch can contain/admit source-native creation;
- carry stable `scene_id` and `epoch_id`; `campaign_technical_id` may remain route-owned rather than duplicated in the body, but the ID allocator receives it from the validated selected LIVE route;
- persist created native records under their final canonical IDs;
- reject any generic invariant that requires `SOURCE_NATIVE_LIVE` records to be rekeyed at compaction/absorption;
- remove the legacy generic `created_entities[].provisional_id` path as the baseline representation for source-native families;
- never infer acceptance from object/file existence alone.

Step-5.8 LAW 5.8-17 remains valid: a future native owner may explicitly permit a provisional/rekeyable world identity only under that owner-specific promotion contract and only when no durable external reference requiring stable identity escapes before promotion. There is no generic v1 fallback from the `SOURCE_NATIVE_LIVE` allowlist to legacy provisional IDs.

Absorption copies/publishes the already accepted canonical native IDs unchanged into campaign-native storage/current routing. It never allocates replacement IDs.

## 6. Frozen attempt / CAS realization

Extend the planned `FrozenLiveAttempt` / `live-publication-attempt.schema.json` with enough frozen allocation evidence to reconcile creation without guessing:

```text
source_native_allocations[] {
    native_family
    source_local_creation_ordinal
    native_id
    creation_slot_index
}
expected_next_source_native_creation_ordinal
```

`creation_slot_index` is local to the frozen attempt and only proves mapping between normalized create slots and proposed coordinates. It is not durable owner identity or chronology.

Freeze sequence:

```text
pin selected LIVE route + exact source revision
-> read current next_source_native_creation_ordinal
-> freeze normalized native transition / creation slots
-> derive proposed coordinates + canonical IDs
-> freeze full attempt including proposed allocations
-> revalidate application authorization
-> exact-source CAS complete source state
```

### Confirmed stale/rejected

On `REJECTED_STALE`:

- the frozen source snapshot and its prospective allocations are invalid for publication;
- refresh exact current source/lifecycle first;
- if still ACTIVE and retry remains semantically permitted, construct a **new** frozen attempt from the new cursor/revision;
- never preserve the rejected ordinal merely to keep a prospective ID stable.

Rejected/prospective IDs were never canonical.

### Indeterminate

On `INDETERMINATE`:

- do **not** allocate a new ordinal or build a replacement attempt first;
- boundedly resolve the exact current source/lineage;
- if the frozen allocation IDs and transition lineage are present in the accepted source, classify the original attempt `ACCEPTED` and preserve them;
- if exact evidence proves the attempt did not establish, only then may a later retry use a newly read cursor;
- unresolved ambiguity remains blocked/indeterminate rather than risking duplicate canonical creation.

This is required for idempotency and accepted-ID stability.

## 7. Recovery / close / absorption

RD-07 selected-LIVE recovery must validate:

- persisted cursor is within the valid domain;
- every source-native record ID decodes/validates against its family policy and selected stable `LiveSourceKey` when that validation is applicable to the recovered source;
- no duplicate accepted coordinate exists for the same `(LiveSourceKey, native_family)`;
- the cursor is strictly greater than every accepted source-local ordinal represented by source-native records created in that source;
- missing/corrupt allocation evidence is integrity failure; recovery does not invoke the campaign allocator or derive a new ID from directory ordering.

Close freezes the final cursor together with the final exact CLOSED source state. Forward absorption retains every accepted source-native ID unchanged. A successor epoch starts its own independent cursor at `1` because its `LiveSourceKey` is different.

## 8. Required TDD obligations

All classes are created only in the task that owns their RED->GREEN cycle, consistent with the checkpoint-coherence overlay.

### RD-09 — `SourceNativeLiveIdEncodingTests`

Prove:

- exact known vectors for framing/base32hex encoding;
- distinct campaign, scene, epoch, family or ordinal components yield distinct IDs;
- encode -> parse round-trip for valid policies;
- malformed/padded/wrong-version/wrong-prefix IDs reject;
- Git ref/revision and wall-clock changes cannot change ID;
- ID lexical/ordinal order has no chronology/currentness API;
- campaign allocator is never consulted.

### RD-09 — `LiveSourceCreationCursorTests`

Prove:

- initial cursor is 1;
- one accepted creation increments once;
- an accepted batch consumes exactly one contiguous coordinate per frozen creation slot;
- competing attempts from one revision may propose the same coordinate, but exact-source CAS accepts at most one; stale retry refreshes and uses the next current coordinate;
- cursor exhaustion fails closed without reuse/wrap;
- close prevents new ordinary allocation.

### RD-09 — `SourceNativeAmbiguousPublicationTests`

Prove:

- indeterminate result reconciles original proposed IDs before any reallocation;
- accepted-but-response-lost retains exactly the originally frozen IDs and cursor advance;
- proven-not-accepted retry may allocate from refreshed current cursor;
- unresolved ambiguity cannot manufacture a second canonical identity.

### RD-09 — `LiveSourceNativeSchemaCutoverTests`

Prove:

- final v1 LIVE schema contains the source-native cursor;
- source-native created records use final canonical IDs;
- legacy generic `provisional_id -> durable compaction rekey` semantics are absent for current SOURCE_NATIVE_LIVE families;
- absorption preserves IDs exactly.

### RD-16 — `SourceNativeIdentifierPolicyIntegrationTests`

Prove:

- every and only `SOURCE_NATIVE_LIVE` family has `encoding = framed_base32hex_v1`;
- owner-equivalent/forbidden rows do not silently inherit it;
- final identifier-policy schema validates the closed object form;
- all existing thread/PLAYER/MechanicalEvent/live-birth policy repairs survive the shared-machine write.

### RD-07 integration — `SourceNativeLiveRecoveryTests`

Prove recovered selected LIVE validates source-native IDs/cursor from exact source evidence, never campaign allocator/directory order/latest branch heuristics.

## 9. Checkpoint choreography

Do not pre-create later test groups.

```text
RD-09 LIVE envelope/claim replacement
-> RD-09 source-native encoding + cursor GREEN
-> RD-09 frozen-attempt/CAS ambiguity GREEN
-> RD09_SOURCE_NATIVE_ID_READY

RD-09 other owner-local LIVE work may proceed as allowed by its plan

RD09_SOURCE_NATIVE_ID_READY
+ other RD-16 shared policy inputs
  JOIN_BEFORE_INTEGRATION
RD-16 SHARED_MACHINE_INTEGRATION

RD09_SOURCE_NATIVE_ID_READY
+ RD-07 selected-LIVE recovery owner
  JOIN_BEFORE_INTEGRATION
source-native recovery proof
```

RD-09 source-native ID helper code is not a second campaign allocator. RD-16 writes the final shared policy files once.

## 10. Version / clean-slate rule

`GAME/**` is clean-slate for v1.0. Legacy pre-v1 LIVE/provisional-ID representation is not a preservation constraint.

Run the Version Impact Gate after composing this repair with all prior RD-09/SIRR2 LIVE schema changes. Do not independently bump the same local schema once per overlay; compute one final material version transition from fresh execution-time bytes.

No compatibility shim or migration is added solely for unreleased legacy LIVE records.

## 11. Coverage / proof closure

Register this as post-WP27 **Finding 24**, not a fabricated historical readiness ID.

Forward:

```text
Step-5.8 / WP-16 source-native identity laws
-> F24
-> RD-09 exact encoding + cursor + CAS/idempotency
-> RD-16 shared identifier-policy integration
-> RD-07 exact selected-LIVE recovery
-> exact named witnesses above
```

Reverse:

```text
framed_base32hex_v1 policy
next_source_native_creation_ordinal
source-native frozen allocation evidence
LIVE schema provisional/rekey removal
source-native recovery validation
-> F24
-> Step-5.8/WP-16 accepted identity laws
```

Current coverage/proof/witness/execution authorities must add F24/PG24 and the `RD09_SOURCE_NATIVE_ID_READY` joins before author zero-open closure.

## 12. Closure condition

Finding 24 is planning-repaired only when:

1. this overlay is routed at highest precedence;
2. source key, coordinate allocation and printable encoding are exact;
3. CAS stale/indeterminate semantics cannot duplicate/rekey accepted IDs;
4. final v1 LIVE schema removes the generic provisional-rekey baseline for SOURCE_NATIVE_LIVE families;
5. RD-16 consumes the exact encoding contract in the one shared identifier-policy write;
6. RD-07 recovery validates the persisted cursor/IDs without campaign allocator or scans;
7. coverage/proof/witness/execution/currentness authorities route F24/PG24;
8. fresh author self-review finds no new conflict introduced by this realization.

Independent review remains blocked. Production implementation remains unauthorized.
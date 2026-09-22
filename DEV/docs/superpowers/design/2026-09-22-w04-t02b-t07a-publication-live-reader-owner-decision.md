# W04 T02B / T07A — Publication + Selected-LIVE Reader Owner Decision

Status: **ACCEPTED SENIOR / OWNER DECISION**

Date: **2026-09-22**

Reviewed stop head:
`d34fa8d1b462e7eaa57d20cd940e6183be0b061a`

This decision resolves:

- W04.T02B campaign publication/recovery, persisted collaboration schema and lifecycle compatibility;
- W04.T07A selected-LIVE `evt` source-domain read boundary.

It does not reopen accepted T01A/T01B/T01C/T02A/T03A/T05A/T05B semantics.
Wave 05 remains unauthorized.

## 1. Bounded Source Manifest

| Evidence / owner | Blob |
|---|---|
| W02 campaign publication owner `GAME/TOOLS/publication.py` | `50ae2d37d8ed574a3495ec0b1f35cd530da4588c` |
| W02 durability route owner `GAME/TOOLS/durability.py` | `d8a5aba813dbe7884df4b53dce0a3bc27e205c2f` |
| current RuntimeHost owner | `bb37913612423a454975da3d727f65dd8d84bf14` |
| current LIVE owner | `c6ec5a362d28281fbfc3a41c9c433fda6571983e` |
| Step-5.6 canonical publication/RepositoryPort owner | `4ec13a292e91acb692c6e54d8c0ca9f49d79bed9` |
| WP-11 physical routing/index owner | `7a4adc1d5be87fc060f428d3684091115cfe7b1a` |
| Step-5.10 Story projection/source-domain owner | `0e2d6db8fcfabb2073c43ab8ae62dde778e25530` |
| baseline Story source-domain registrations | `4e85a2899657f43c2bb812e9608d9d0c254b4a96` |
| versioning/compatibility policy | `9b19544286f9e37689f8486c0521789fa4173b7a` |
| T02B System-Impact brief | `f9e524d100378ae2d754a7e2ecb5994b443541ac` |
| T07A selected-LIVE reader brief | `ca6883da6d4dbf3f702aca2829709b34bd3869f6` |
| accepted T02A collaboration owner | `7750195ad55cfc10d4204894cc115ebf2de90a31` |
| accepted T02A obligation schema v2 | `206c5b9d99ec523dbfd98a210a6a435beae8d652` |
| accepted T02A GAME projection v2 | `44d221dcbf8a79050de4192e00f757b19edfca6d` |

Dependency subgraph:

```text
accepted T00H RuntimeHost
        +
Step-5.6 publication owner
        +
Step-5.10 evt source contract
        |
        v
W04.T00P host I/O extensions
      /   \
     v     v
  W04.T02B   W04.T07A
     |
     v
  T02C -> T04*
```

## 2. W04.T00P — shared RuntimeHost I/O extension

A new coordinator-owned prerequisite is admitted:

```text
W04.T00P — RuntimeHost publication + SemanticEvent source adapters

OUTPUT:
  W04_RUNTIME_HOST_IO_EXTENSIONS_READY
  W04_RUNTIME_HOST_IO_BOOTSTRAP_DELTA_READY
```

Inputs:

- accepted `W04_RUNTIME_HOST_COMPOSITION_READY`;
- W02 publication/recovery owner;
- Step-5.6 transport law;
- Step-5.10 / 2026-09-08 source-domain contract.

Direct writes:

```text
GAME/TOOLS/runtime_host.py
DEV/TESTS/test_runtime_host_composition.py
bounded Wave-05 bootstrap delta/evidence only
```

No persistent schema is owned by T00P.

T00P extends the existing campaign-bound RuntimeHost. It does not replace T00H.

### 2.1 CampaignPublicationTransport

The deployment host may supply a campaign-write capability at composition time.
It is optional for read-only RuntimeHost profiles and mandatory for a profile
that executes T02B/campaign publication.

The transport is infrastructure/TCB, never a gameplay argument.

Its required semantic operations are exactly equivalent to:

```text
repository_identity() -> nonempty repository identity

resolve_authenticated_acting_principal(
    campaign_id,
    pinned_campaign
) -> AuthenticatedPrincipalEvidence

read_ref(target_ref) -> exact current ref/head evidence

create_tree(
    base_tree_sha,
    exact path_operations
) -> exact tree identity

create_commit(
    parent_sha,
    tree_sha,
    target_ref
) -> exact commit identity

update_ref(
    target_ref,
    new_commit_sha,
    force = false
) -> raw typed accepted/rejected/indeterminate transport response
```

Concrete GitHub REST/GraphQL/Connector mechanics remain deployment-specific.

The existing read-side RepositoryPort remains responsible for exact campaign
pin/path/commit reads and bounded ancestry comparison. Read and write
capabilities MUST refer to the same selected campaign repository/root; RuntimeHost
fails composition/publication if their repository identity is inconsistent.

The acting-principal result is Step-5.6 transport/audit evidence. It does not
grant gameplay authorization and cannot substitute for W03 access/PLAYER owner
checks.

### 2.2 CampaignPublicationService

RuntimeHost owns one sibling deterministic service:

`CampaignPublicationService`

Domain owners do not call transport write methods directly.

The only admitted publication flow is:

```text
owner-local exact delta
  -> route_serialized_operation(...)
  -> CampaignPublicationService
  -> freeze_campaign_publication_attempt(...)
  -> build_connector_git_plan(...)
  -> exact low-level transport operations
  -> classify_ref_transition(...)
  -> PublicationOutcome
  -> if acknowledgement is ambiguous:
       bounded exact current read
       + PublicationCurrentClosureEvidence
       + CommitAncestryEvidence where required
       -> reconcile_indeterminate_publication(...)
```

No domain may introduce its own publication closure/result authority.

The service may expose an owner-neutral method equivalent to:

```text
publish_owner_delta(
    *,
    routed_operation: RoutedSerializedOperation,
    path_operations,
    owner_generations,
    publication_reason
) -> PublicationOutcome
```

It acquires internally from the bound RuntimeHost:

- fresh `PinnedCampaign`;
- exact MANIFEST and CAMPAIGN_CARD;
- canonical target ref;
- repository identity;
- authenticated acting-principal evidence.

For a non-command owner such as `runtime.collaboration_obligation`,
`execution_durability_join=None` is legal under the existing W02 contract.

On conflict/indeterminate outcome there is no second semantic execution and no
local owner-state adoption. Re-pin/rebuild is an explicit later operation after
current owner revalidation.

For indeterminate reconciliation, deterministic Python reads the current exact
ref/commit/tree and each attempted operation path. Only after exact path values
match the frozen attempt may it construct
`PublicationCurrentClosureEvidence` using
`attempt.publication_operation_digests()`. Descendant acceptance additionally
requires the existing typed `CommitAncestryEvidence`.

No caller boolean such as `closure_compatible`, `published`,
`lineage_contains_intended` or `head_is_intended` is admitted.

### 2.3 SemanticEventSourceAdapter

RuntimeHost also binds one Step-5.10 source-domain adapter. It is transport /
enumeration evidence, not native-history authority.

The admitted bounded operations are equivalent to:

```text
read_local_evt_window(
    pinned_campaign,
    lower_exclusive_ordinal,
    max_items
) -> raw EvtSourceWindow

read_selected_live_evt_window(
    selected_route,
    selected_source,
    lower_exclusive_ordinal,
    max_items
) -> raw EvtSourceWindow
```

Strict raw window shape:

```text
campaign_id
origin                         # LOCAL | LIVE:<epoch_id>
source_ref
source_revision
lane = evt
lower_exclusive_ordinal
upper_ordinal | null
interval_complete_through_upper: true
entries[]:
  ordinal
  event_id
  event_record
```

The adapter never returns "accepted history", Story material, eligibility or
fictional chronology.

For LOCAL, physical realization uses the current exact campaign pin and the
accepted native evt enrollment/index surface plus exact known-ID
`runtime.semantic_event` reads. It MUST NOT read `LOG/SEMANTIC_EVENTS` as
one unvalidated aggregate.

For selected LIVE, the deployment adapter reads the exact selected one-file LIVE
source at the route-selected source revision. It derives the bounded evt lane
from the source's accepted native enrollment representation / packed native
event evidence. It MUST NOT invent a Git-tree `INDEX/EVENT_INDEX.yaml` inside a
one-file LIVE source.

If the current physical source cannot prove a complete evt interval, the adapter
returns unavailable/insufficient evidence. It never guesses completeness.

`history.py` remains responsible for validating:

- campaign/origin/source ref/revision;
- positive evt ordinal;
- exact event identity and schema;
- `semantic_order == evt admission ordinal` for generation 1;
- strict increasing/contiguous interval where contiguous coverage is claimed;
- provenance;
- exact selected-LIVE route/currentness.

Only after that validation may History issue native-history currentness/event
objects.

No missing/stale routed LIVE source falls back to campaign.

## 3. W04.T02B publication/recovery ruling

Disposition:

```text
TARGETED_REPAIR_REQUIRED
SYSTEM_IMPACT: RESOLVED
ARCHITECTURE_REVIEW_REQUIRED: NO
```

### 3.1 Clean T02B restore first

The published candidate
`ae424f32cc785f940f7740355924aa259d8895c6` is unaccepted and changed only:

```text
GAME/TOOLS/collaboration.py
DEV/TESTS/test_rd12_collaboration.py
DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json
GAME/SCHEMA/collaboration_obligation.schema.yaml
```

Before the new T02B RED, restore exactly those four paths to accepted head
`b737555b9d9a1c404576dc173dfdaf34cd023e13`.

Preserve all accepted T01A/T01B/T01C/T02A/T03A/T05A/T05B work and all current
control/design evidence.

Restore checkpoint: `VERSION_IMPACT: NONE`.

### 3.2 CLOSED durability is owned by T02B

Accepted T02A is intentionally publication-free. Therefore T02B owns two
distinct campaign transactions:

```text
OPEN
  -> explicit close/frozen basis from T02A
  -> publish CLOSED obligation
     (route companions remain)
  -> recoverable CLOSED

CLOSED
  -> validated handoff
  -> one same-campaign closure:
       native IntentClause transition where applicable
       obligation CLOSED -> RESOLVED
       exact affected PLAYER route-companion removals
  -> RESOLVED
```

Crash after the first publication recovers CLOSED and rebuilds/revalidates the
handoff from durable native state. Crash after the second recovers RESOLVED
idempotently. Neither path replays mechanics.

Both publications use CampaignPublicationService and the W02 publication owner.

The primary routed operation is
`runtime.collaboration_obligation:<obligation_id>`; the exact publication
write set may additionally contain the bound IntentPlan and affected PLAYER
records.

Collaboration must delete the rejected:

- `CollaborationPublicationClosure`;
- `CollaborationPublicationResult`;
- `host._repository.publish_campaign_closure(...)`;
- any equivalent collaboration-local publisher/result vocabulary.

### 3.3 Persistent collaboration schema v3 is approved

The v2 -> v3 persistent shape change is **required** for durable CLOSED recovery:
T02A's frozen `closed_input_set_fingerprint` was not serialized in v2.

Accepted v3 law:

```text
closed_input_set_fingerprint is a required serialized field of type SHA256|null

OPEN:
  fingerprint MUST be null

CLOSED:
  fingerprint MUST be SHA-256

RESOLVED:
  fingerprint MUST be SHA-256 and preserved from CLOSED

OBSOLETE:
  fingerprint MAY be null when obsoleted before close
  fingerprint MAY be SHA-256 when the generation had already frozen/closed
  an existing non-null fingerprint MUST NOT be erased merely by obsolescence
```

Python runtime, DEV JSON Schema and shipped GAME projection MUST encode the same
matrix.

`CollaborationClosedBasis` v1 and `CollaborationHandoff` v1 remain their
accepted typed owner-local values. The persisted fingerprint allows CLOSED cold
recovery to reconstruct and verify that basis deterministically.

### 3.4 Compatibility / migration / campaign-contract disposition

The HDM versioning policy explicitly defines current v1 development as a
clean-slate pre-release realization boundary.

Therefore this accepted T02B transition is:

```text
runtime.collaboration_obligation schema:
  2 -> 3

migration edge:
  NONE

dual-read / compatibility alias:
  NONE

campaign_contract_generation:
  NO BUMP

reason:
  v2 is an unreleased pre-v1 machine shape;
  no released/adopted campaign contract is being migrated.
```

After the v3 checkpoint is accepted, current runtime readers accept v3 only.
Current pre-release fixtures/scaffold/examples are normalized to v3 in the
coherent implementation/final-writer path; no v2 compatibility debt is created.

This ruling authorizes schema replacement, not migration execution.

If evidence later proves that a released/adopted campaign exists on v2, stop at
a new System-Impact gate; this decision does not silently migrate released data.

### 3.5 Required T02B regression proof

At minimum:

- domain code cannot call a custom publisher or transport directly;
- CLOSED publication is one W02 `FrozenCampaignPublicationAttempt`;
- RESOLVED publication is another W02 attempt with one same-campaign write set;
- non-command routed operation works without execution-durability join;
- stale ref / non-fast-forward fails closed;
- indeterminate ACK uses existing typed reconciliation and never dispatches a
  second write;
- crash after CLOSED recovers same fingerprint/input set;
- crash after RESOLVED is idempotent;
- route companions remain through OPEN/CLOSED and disappear with terminal
  RESOLVED/OBSOLETE closure as owner law requires;
- OPEN + non-null fingerprint rejected;
- CLOSED/RESOLVED + null fingerprint rejected;
- RESOLVED fingerprint cannot change;
- OBSOLETE preserves prior non-null fingerprint;
- v2 serialized obligation rejected after v3 cutover;
- no collaboration index/global scan;
- no LIVE collaboration owner / no 2PC / no mechanics replay.

Fresh Version Impact starts from accepted T02A module version `1.0.9`.
Rejected candidate versions are non-precedential.

## 4. W04.T07A selected-LIVE evt-lane ruling

Disposition:

```text
TARGETED_REPAIR_REQUIRED
SYSTEM_IMPACT: RESOLVED
ARCHITECTURE_REVIEW_REQUIRED: NO
```

### 4.1 Restore only T07-owned unaccepted surfaces

Do **not** roll the whole branch back to before `c37c517...`; later accepted
T01A/T05A work modified RuntimeHost after that point.

These current blobs are still exactly the unaccepted T07A candidate blobs and
may be restored safely to its parent
`e340ed5add19dbc4ed6ff350229ef6f2827fabb8` before the fresh T07A RED:

```text
GAME/TOOLS/history.py
DEV/TESTS/test_rd13_story_t0_commentator.py
DEV/SCHEMAS/native-history-currentness.schema.json   # delete; absent at parent
DEV/SCHEMAS/native-history-publication.schema.json   # delete; absent at parent
```

Do not restore `GAME/TOOLS/runtime_host.py` or
`DEV/TESTS/test_runtime_host_composition.py`; those also contain later accepted
host/Context changes and are now owned by T00P integration.

Restore checkpoint: `VERSION_IMPACT: NONE`.

### 4.2 T07A consumes T00P

After `W04_RUNTIME_HOST_IO_EXTENSIONS_READY`, T07A obtains raw windows only
through the bound RuntimeHost History service / SemanticEventSourceAdapter.

No gameplay/domain call accepts:

- RepositoryPort;
- selected-LIVE transport;
- source adapter;
- RuntimeHost replacement;
- History service replacement;
- raw "accepted/current/complete" booleans.

LOCAL and LIVE use the same strict EvtSourceWindow semantics.

### 4.3 LOCAL source

LOCAL does not read `LOG/SEMANTIC_EVENTS` as one aggregate.

It consumes a bounded source-domain window from the exact pinned campaign source.
Physical enumeration uses the accepted evt enrollment/index surface and exact
known-ID event routes. Index content nominates candidates; exact event records
remain the native event evidence.

If the adapter cannot prove the requested interval complete at that exact pin,
History returns unavailable/insufficient evidence and does not advance
coverage/currentness.

### 4.4 selected LIVE source

LIVE uses:

```text
current complete LiveRouting
-> exact selected LiveEnvelope
-> route-selected exact source revision
-> host source-domain adapter reads that one-file LIVE source
-> raw evt window
-> history.py validates
```

The source adapter may derive the evt window from the exact
`LiveNativeStatePack` / accepted native-event enrollment representation. It
does not invent a tree index path inside the one-file LIVE source.

Every LIVE event must remain bound to the original
`LIVE:<epoch_id>` origin and exact source revision. Absorption does not
re-enroll it as LOCAL.

Missing, stale, orphaned or superseded selected LIVE source is a hard
unavailable/currentness failure. Campaign fallback is forbidden.

### 4.5 History authority

The source adapter is not accepted history authority.

`history.py` validates the strict raw window and only then issues
`NativeHistoryCurrentness`, `NativeSemanticEvent` and any ephemeral
publication/recovery value.

Story, narration, current world state, current Actor state, Git commit order and
source-native creation order of unrelated families never reconstruct or replace
SemanticEvent history.

The previously accepted ruling remains:

`semantic_order` is the generation-1 evt-lane admission ordinal within its
native origin, not fictional chronology.

### 4.6 Required T07A regression proof

At minimum:

- aggregate `LOG/SEMANTIC_EVENTS` load rejected as source-domain proof;
- forged source window / false completeness rejected by History validation;
- wrong campaign/origin/ref/revision rejected;
- duplicate/gapped/nonmonotonic evt ordinals rejected when contiguous coverage
  is claimed;
- event ID/body mismatch rejected;
- selected LIVE exact-source mismatch rejected;
- missing LIVE never falls back to LOCAL/campaign;
- absorbed event preserves original LIVE origin;
- Story/narration cannot mint native history;
- caller cannot replace the host source adapter;
- bounded window respects resource limit and never scans all history.

Fresh Version Impact starts from the restored pre-T07A history owner. Rejected
T07A candidate version transitions are non-precedential.

## 5. W04 resumption order

```text
A. restore rejected T02B four-file candidate to b737555...
B. restore T07-owned history/schema/rd13 surfaces to e340ed5...
C. verify restores + local reviewer + publish/read-back

D. W04.T00P
   -> reviewer PASS
   -> W04_RUNTIME_HOST_IO_EXTENSIONS_READY

E. run in parallel where write sets remain isolated:
   - W04.T02B fresh RED / implementation / review
   - W04.T07A fresh RED / implementation / review

F. after accepted T02B:
   T02C becomes eligible
   -> T04A/T04B
   -> T05C once all named inputs exist

G. after accepted T07A:
   T07B+ continues in order
```

T01A, T05A, T01B, T05B, T01C, T02A and T03A remain accepted; do not reopen
them absent a proven regression/contradiction.

The previously recorded T07 CLS↔HDM preflight remains PASS unless its explicit
public/private semantic-change trigger fires before the new T07A RED.

## 6. Wave-05 integration ownership

Wave 04 owns the deterministic T00P interface/service semantics.

Wave 05 owns final product/deployment wiring.

W05.T06 consumes `W04_RUNTIME_HOST_IO_EXTENSIONS_READY` for product paths.

W05.T08 integrates:

- `W04_RUNTIME_HOST_IO_BOOTSTRAP_DELTA_READY` into BOOTSTRAP_RUNTIME;
- CampaignPublicationService transport wiring into PERSISTENCE;
- selected-LIVE evt source-domain adapter wiring into LIVE_SCENE/STORAGE as
  appropriate;
- no gameplay/model API transport injection.

Wave 05 remains unauthorized until normal Wave-04 FINAL_REVIEW + Senior gate.

## 7. Decision status

```text
T02B SYSTEM_IMPACT: RESOLVED
T07A SYSTEM_IMPACT: RESOLVED
ARCHITECTURE_REVIEW_REQUIRED: NO
MIGRATION_EXECUTION: NOT AUTHORIZED / NOT REQUIRED FOR PRE-RELEASE v2->v3
CAMPAIGN_CONTRACT_GENERATION_BUMP: NO
WAVE_05: NOT AUTHORIZED

THIS DOCUMENT:
  VERSION_IMPACT: NONE
```

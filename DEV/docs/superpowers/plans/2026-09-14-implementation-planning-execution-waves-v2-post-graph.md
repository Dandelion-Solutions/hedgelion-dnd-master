# HDM Implementation Planning — Execution Waves / Dependency Graph v2

Status: **CURRENT POST-GRAPH EXECUTION ROUTE — PLANNING ONLY**
Date: 2026-09-14
Finding origin: **AUTHOR FINDING 21 — SIGNIFICANT**, extended through Finding 26.
Production implementation: **NO**.

This document supersedes the 14-RD execution-wave topology for current execution scheduling. Historical wave documents remain provenance for their accepted edges; this v2 reconciles them with RD-15, RD-16 and Findings 6–26.

## Edge law

- `HARD_PRECEDES`: target checkpoint is semantically invalid before predecessor output exists.
- `JOIN_BEFORE_INTEGRATION`: owner-local work may proceed independently; named integrated checkpoint waits for all inputs.
- `SHARED_FILE_CHECKPOINT`: physical writes are serialized against fresh current bytes without transferring semantic authority.
- `PROOF_AFTER_TARGET`: proof waits for the implicated mechanisms.
- wave/tier labels are scheduling preferences, never hidden prerequisites.

Every publishable checkpoint obeys overlay 5: all tests already present, maintenance audit and full DEV discovery are GREEN. Future-task RED groups are not committed early.

## Tier A — independent owner-local work

The following may proceed in parallel when their own local prerequisites are satisfied:

```text
RD-01 shipped projection cleanup
RD-02 information / knowledge / disclosure / message core
RD-03 actor / asset / effect core
RD-04 routing / HOT / allocator owner-local work
RD-05 deterministic mechanics core and Procedure/Continuation owner-local work
RD-08 thread / temporal / chronology owner-local work
RD-09 principal / LIVE owner-local work, including F24–F26 source-native route/ID/order/CAS
RD-10 typed role / Interpreter-result / emission core
RD-11 Context Runtime core
RD-12 collaboration core
RD-13 native history / Story / Dramaturg owner-local work
RD-14 bootstrap/product owner-local work, including early campaign-identity creation/projection proof
RD-15 exact BoundCatalogContext construction over current S6D package outputs
RD-16 quiet-world-family strict-schema work over already-current semantic owners
```

RD-06 publication and RD-07 recovery owner-local foundations may also proceed when their existing RD-04/RD-05 inputs are available; RD-06 may independently add the F25 post-initialization campaign-identity immutability guard. They do not wait for unrelated later domains.

## Tier B — semantic seams

### Catalog-backed execution seam

```text
RD-10 typed InterpreterResult
  HARD_PRECEDES
RD-15 candidate binding / deterministic same-context validation
  HARD_PRECEDES for catalog-backed executable requests
RD-05 RuntimeCommand acceptance
```

RD-05 pure deterministic mechanics helpers may exist before RD-15. The hard edge applies to catalog-backed command acceptance/integration, not to owner-native non-catalog transitions.

For catalog-backed execution, RD-15 `SUPPORTED` output carries one canonical reconstructive `CatalogContextBasis`:

```text
exact ruleset-set identity
+ catalog-context fingerprint identity
+ bounded owner-local campaign/session definition dependency refs
```

RD-05 accepted RuntimeCommand copies that exact basis. Root/child Resolution and Continuation preserve basis equality; a generic dependency-frontier list or fingerprint alone is not a substitute. `UNSUPPORTED` produces no RuntimeCommand and routes to RD-15 gap evidence carrying the same accepted basis in which validation failed.

### Accepted catalog-basis durability / recovery seam — Finding 23

Owner-local implementation may proceed independently, but the following integration order is mandatory:

```text
RD-15 LOCAL_CATALOG_BASIS_READY
  HARD_PRECEDES catalog-backed acceptance
RD-05 LOCAL_ACCEPTED_CATALOG_EXECUTION_READY
  JOIN_BEFORE_INTEGRATION -> RD-06 LOCAL_CATALOG_BASIS_DURABILITY_READY

RD-15 LOCAL_CATALOG_BASIS_READY
+ RD-05 LOCAL_ACCEPTED_CATALOG_EXECUTION_READY
+ RD-06 LOCAL_CATALOG_BASIS_DURABILITY_READY
  JOIN_BEFORE_INTEGRATION
RD-07 LOCAL_CATALOG_BASIS_RECOVERY_READY
```

Meaning:

- RD-06 cannot claim an accepted catalog-backed execution durably recoverable unless its reconstructive catalog basis and required retained owner-local definition evidence are in the correctness-required closure;
- unresolved accepted execution protects those definition dependencies under Step-5.13 typed retention/protection laws;
- unpublished session-only definitions cannot become durable accepted dependencies without owner-approved publication/promotion basis;
- RD-07 exact-reconstructs the accepted ruleset set and every required owner-local definition dependency before retry/resume;
- missing/incompatible/unpinned dependency evidence yields typed blocked/compatibility/integrity failure; current/latest/search fallback is forbidden.

This join does **not** create a global catalog snapshot, new definition record family, universal refcount, universal dependency graph or second ruleset loader.

### Source-native LIVE identity / routing / allocation seam — Findings 24–26

The current v1 realization composes three repairs:

```text
F24: CAS-owned uint64 source-local creation cursor + framed_base32hex_v1
F25: semantic campaign source identity is canonical campaign_id;
     WP-11 physical campaign route token is derived/verified transport routing
F26: deterministic attempt-local ordering for multiple SOURCE_NATIVE_LIVE creations
```

Correct semantic source key:

```text
LiveSourceKey(campaign_id, scene_id, epoch_id)
```

Physical WP-11 route component:

```text
encode_live_campaign_route_token(campaign_id)
= c1-<full lowercase sha256 of domain-separated length-framed UTF8(campaign_id)>
```

The LIVE envelope carries canonical `campaign_id`; route selection/recovery validates the body tuple. The physical route token and exact source revision are not semantic identity.

For one frozen mutation, RD-09 normalizes source-native creations as:

```text
family-native deterministic ordered sequences
-> family groups sorted by UTF8(native_family)
-> contiguous owner_local_creation_index within family
-> contiguous creation_slot_index
-> source_local_creation_ordinal = frozen_cursor + slot
-> framed final native ID using canonical campaign_id
```

Unordered/ambiguous native-owner output blocks; no hash/payload/time/random/container-order fallback is allowed.

Owner-local checkpoints:

```text
RD-14 early CreationIdentity/GeneratorScaffold campaign_id proof
  -> RD14_CAMPAIGN_IDENTITY_CREATION_READY

RD-06 campaign identity protected-field publication guard
  -> RD06_CAMPAIGN_IDENTITY_IMMUTABILITY_READY

RD-09 LIVE schema + c1 route helper/body validation
  -> RD09_LIVE_CAMPAIGN_ROUTE_IDENTITY_READY

RD-09 source-native deterministic creation normalization
  -> RD09_SOURCE_NATIVE_CREATION_ORDER_READY

RD-09 cursor + corrected framed_base32hex_v1 + frozen CAS/ambiguity behavior
  -> RD09_SOURCE_NATIVE_CURSOR_ENCODING_READY
```

Integrated F24–F26 LIVE identity checkpoint:

```text
RD14_CAMPAIGN_IDENTITY_CREATION_READY
+ RD06_CAMPAIGN_IDENTITY_IMMUTABILITY_READY
+ RD09_LIVE_CAMPAIGN_ROUTE_IDENTITY_READY
+ RD09_SOURCE_NATIVE_CREATION_ORDER_READY
+ RD09_SOURCE_NATIVE_CURSOR_ENCODING_READY
  JOIN_BEFORE_INTEGRATION
RD09_SOURCE_NATIVE_ID_READY
```

This is a checkpoint-level join, **not** a whole-RD serialization edge. In particular, RD-14's later final topology/scaffold validation may still wait for RD-16 without creating a cycle.

`RD09_SOURCE_NATIVE_ID_READY` means:

- semantic IDs frame canonical `campaign_id`, not physical route token/ref/revision;
- no second semantic `campaign_technical_id` exists;
- campaign allocator fallback is absent;
- raw campaign bytes are not inserted into the physical Git ref component;
- route-token/body campaign mismatch is integrity failure;
- multiple creations have exact deterministic technical slot allocation without fictional-order meaning;
- confirmed stale prospective IDs are noncanonical;
- an indeterminate prior attempt is reconciled before any new coordinate is allocated;
- current SOURCE_NATIVE_LIVE families do not rely on generic provisional->compaction rekey semantics;
- accepted IDs survive close/absorption unchanged.

This output has two mandatory downstream joins:

```text
RD09_SOURCE_NATIVE_ID_READY
+ RD-16 other shared identifier-policy inputs
  JOIN_BEFORE_INTEGRATION
RD-16 SHARED_MACHINE_INTEGRATION
```

and

```text
RD09_SOURCE_NATIVE_ID_READY
+ RD-07 selected-LIVE recovery owner-local foundation
  JOIN_BEFORE_INTEGRATION
RD-07 SOURCE_NATIVE_LIVE_RECOVERY_READY
```

RD-16 is the single final writer of `identifier-policies.schema.json` / `identifier-policies.json` and records the closed `source_native_live + framed_base32hex_v1` policy only for applicable families. RD-07 validates canonical campaign identity, exact selected LIVE source and accepted cursor/allocation/IDs without campaign allocator, directory/index order or latest-looking source heuristics.

The source-local ordinal and creation-slot order are allocation uniqueness/reproducibility state only. They introduce no global sequence, fictional chronology, priority, generation or replacement CAS fence.

### Execution / publication / recovery seams

```text
RD-05 accepted execution
  JOIN_BEFORE_INTEGRATION -> RD-06 publication
  JOIN_BEFORE_INTEGRATION -> RD-07 accepted-execution recovery
  JOIN_BEFORE_INTEGRATION -> RD-08 accepted occurrence/execution closure
  JOIN_BEFORE_INTEGRATION -> RD-09 current execution source join
```

RD-06 current publication + RD-04 current route evidence join RD-07 current-native recovery. Selected-LIVE recovery additionally joins RD-09 exact selected source/currentness and, for SOURCE_NATIVE_LIVE families, the complete F24–F26 `RD09_SOURCE_NATIVE_ID_READY`. For catalog-backed accepted execution these generic joins additionally obey the Finding-23 catalog-basis joins above.

### Catalog-gap evidence seam

```text
RD-15 deterministic UNSUPPORTED result
  -> stable runtime.catalog_gap_report candidate with exact CatalogContextBasis
  JOIN_BEFORE_INTEGRATION -> RD-06 campaign publication / retained dependency proof
  PROOF_AFTER_TARGET -> RD-07 retained evidence / exact-context non-authority recovery
```

A gap report is evidence that deterministic validation failed in one exact accepted catalog basis; it is not reinterpreted by a newer/current context.

### Information / LIVE / history seam

RD-09 material LIVE evidence joins RD-02 normalization and RD-13 native SemanticEvent where material. Accepted close and later absorption remain separate: successful close may remain `CLOSED_UNABSORBED` while later normalization/publication is retried.

### Story / bootstrap seam

RD-13 static Story selector and owner-local Story contract join RD-14 generated-scaffold preservation. Story bytes/T0 remain non-prerequisites for blank campaign/New Game readiness.

## Tier C — shared machine integration

RD-16 owns one final shared machine checkpoint. Before that checkpoint:

```text
RD-08 world.thread                     LOCAL_SEMANTIC_READY
RD-04 world.player / no-world.faction  LOCAL_SEMANTIC_READY
RD-05 MechanicalEvent identity         LOCAL_SEMANTIC_READY
RD-09 exhaustive live-birth table      LOCAL_SEMANTIC_READY
RD-09 exact F24–F26 source-native ID   RD09_SOURCE_NATIVE_ID_READY
RD-15 catalog-gap policy input          LOCAL_SEMANTIC_READY
RD-16 17-family strict schemas          READY
```

Then:

```text
all inputs
  JOIN_BEFORE_INTEGRATION
RD-16 SHARED_MACHINE_INTEGRATION
  -> core catalog / admission / structures / identifier policy / schema / projections coherent together
```

No producer RD independently publishes a competing final version of those shared machine files after RD-16 integration begins.

RD-16 integration is required before final R018 closure and before RD-14 **late final topology/scaffold validation** claims the v1 family/catalog topology. This late RD-14 checkpoint is distinct from the earlier `RD14_CAMPAIGN_IDENTITY_CREATION_READY` checkpoint consumed by F25.

Finding-23 `CatalogContextBasis` schemas are execution embedded-value contracts, not world-family/shared-catalog members; they remain under RD-15/RD-05 integration rather than being absorbed into RD-16 semantic ownership. Findings 24–26 change the shared identifier-policy realization/proof but do not transfer LIVE identity/routing/allocation semantics from RD-09 to RD-16.

## Tier D — shared shipped-consumer checkpoints

Physical file overlap does not create semantic ownership transfer.

- Scene routing: RD-08 chronology/scene delta first, then RD-09 LIVE routing delta against fresh bytes, followed by joint proof.
- Catalog-binding instructions: RD-15 owns binding semantics in `PLAY_POLICY`, `CORE_INDEX`, `ADJUDICATION`; if RD-01 also changes the same file, use one coherent ordered writer/merge and prove both requirement sets.
- Multiplayer/session prose: RD-09 LIVE lifecycle/currentness and RD-12 collaboration deltas use one ordered physical cutover where the same file is touched.
- Historical RD-02/RD-03/RD-04 shared GAME schema ordering remains as accepted by the original execution-wave package.
- `PROJECT_MAP` and `audit_engine.py` are projection surfaces; every later writer fresh-reads current bytes and preserves all admitted routing/audit assertions.

## Tier E — context / collaboration / retained projections

Existing owner-local independence remains:

- RD-11 context and RD-12 collaboration cores are not cyclic.
- RD-11 integrated context acceptance joins applicable RD-02 disclosure, RD-09 currentness, RD-10 containment and RD-12 controlled-actor scope.
- retained Dramaturg candidate generation stays ephemeral until RD-06 campaign publication accepts it; current RD-09/RD-10/RD-12 evidence participates only at admission/publication join.
- RD-13 native history remains independently authoritative and is not gated on Story projection freshness.

## Tier F — product/scaffold integration

RD-14 owner-local bootstrap work may precede later joins. Its early campaign-identity creation checkpoint participates in F25 as stated above. Final bootstrap/product closure waits only for named later consumers:

- current 17-family post-RD16 topology/scaffold expectations;
- ruleset-set identity propagation;
- PLAYER/no-faction routing consequences;
- Story selector preservation;
- applicable save/session/menu and creator-provenance joins.

No gameplay bootstrap is executed by this planning package.

## Tier G — proof / coverage closure

`PROOF_AFTER_TARGET` only:

1. historical readiness proof through current v2 ledger/appendices;
2. post-graph proof through `2026-09-14-implementation-planning-lossless-proof-ledger-v3-post-graph.md`;
3. exact post-WP27 witnesses through `2026-09-14-implementation-planning-post-graph-proof-witness-matrix.md`;
4. current bidirectional coverage through `2026-09-14-implementation-planning-bidirectional-coverage-v3-post-graph.md`;
5. R018 waits for RD-15 catalog-gap family + RD-16 exact world-family/shared-machine joins;
6. F23 waits for RD-15 basis producer + RD-05 carriers + RD-06 retention/publication + RD-07 exact reconstruction witnesses;
7. F24 waits for the corrected RD-09 cursor/encoding/CAS + RD-16 policy integration + RD-07 selected-LIVE recovery witnesses;
8. F25 waits for RD-14 campaign identity projection + RD-06 immutability + RD-09 route/body/corrected frame + RD-07 selected-LIVE campaign identity witnesses;
9. F26 waits for RD-09 deterministic normalization/allocation/ambiguity + RD-07 accepted allocation recovery witnesses;
10. all eight historical composite parents retain their original accepted semantics;
11. dormant empirical trigger rows remain dormant.

## Cycle check

Current **checkpoint-level** hard/join graph remains acyclic:

```text
RD-10 -> RD-15 -> RD-05 catalog-backed acceptance
RD-05 -> RD-06 -> RD-07 generic integration joins
RD-15 -> RD-05 -> RD-06 -> RD-07 catalog-basis integration path
RD14_CAMPAIGN_IDENTITY_CREATION_READY ----\
RD06_CAMPAIGN_IDENTITY_IMMUTABILITY_READY -+-> RD09_SOURCE_NATIVE_ID_READY
RD09 owner-local F25/F26/F24 checkpoints --/
RD09_SOURCE_NATIVE_ID_READY -> RD-16 shared integration
RD09_SOURCE_NATIVE_ID_READY -> RD-07 selected-LIVE recovery join
RD-13 -> RD-14 Story-selector consumer join
RD-16 -> RD-14 late final topology/scaffold validation
```

The early RD-14 campaign-identity checkpoint and late RD-14 final-topology checkpoint are distinct; therefore F25 does not create `RD-14 -> RD-09 -> RD-16 -> RD-14` semantic serialization.

Owner-local portions not named by these edges retain parallel eligibility.

## Current completion gate

Before independent handoff, verify:

- every RD-01..RD-16 appears in this graph or is explicitly owner-local;
- no hard edge is inferred merely from tier number;
- RD-15 cannot be bypassed by catalog-backed RD-05 acceptance;
- accepted catalog-backed work cannot lose/rebind its reconstructive catalog basis across RD-05/RD-06/RD-07;
- unpublished session-only definitions cannot be stranded behind durable accepted execution;
- canonical campaign identity cannot drift or be confused with physical LIVE route token;
- RD-09 source-native allocation/ordering/encoding/CAS behavior is exact, non-rekeying and campaign-allocator-independent;
- RD-07 recovery cannot invent/reallocate source-native IDs or trust route-token equality without semantic body validation;
- RD-16 has one final shared machine writer and consumes the exact F24–F26 identifier policy;
- no publishable checkpoint contains future intentional RED tests;
- coverage v3, proof-ledger v3 and witness matrix match this 16-RD graph through F26;
- exact-head hosted validation is green.

Production implementation remains unauthorized.

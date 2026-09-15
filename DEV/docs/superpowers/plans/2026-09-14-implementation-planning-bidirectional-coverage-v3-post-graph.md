# HDM Implementation Planning — Bidirectional Coverage / Currentness v3

Status: **CURRENT AUTHOR POST-GRAPH COVERAGE — ADVERSARIAL CLOSURE ACTIVE**
Date: 2026-09-14
Finding origin: **AUTHOR FINDING 19 — SIGNIFICANT**, extended through Finding 27.
Production implementation: **NO**.

This document supersedes bidirectional-coverage-v2 for current package routing. v2 remains historical evidence for the original readiness decomposition.

## 1. Historical readiness accounting is preserved

```text
DIRECT: 116
PURE_PROOF: 9
COMPOSITE_PARENTS: 8
TOTAL_ACTIVE: 133
TRIGGER_GATED: 12
NO_WORK: 79
R004: ABSENT
```

The original direct readiness IDs remain assigned to RD-01..RD-14 exactly as in v2. RD-15 and RD-16, and Findings discovered by the post-WP27 graph audit, do not invent historical readiness IDs.

Current decomposition count: **16 RD units**.

## 2. Exact world-family forward map

| Family | Semantic / owner route | Current machine execution route |
|---|---|---|
| world.actor | RD-03 / Actor owner | existing strict schema + RD-16 final wrapper proof; SOURCE_NATIVE_LIVE birth uses F24–F27 RD-09 source/cursor/order/route realization when admitted |
| world.actor_group | RD-03 / Actor-group owner | existing strict schema + RD-16 final wrapper proof; SOURCE_NATIVE_LIVE birth uses F24–F27 when admitted |
| world.asset | RD-03 / Asset owner | existing strict schema + RD-16 final wrapper proof; SOURCE_NATIVE_LIVE birth uses F24–F27 when admitted |
| world.location | current catalog/native owner | RD-16 strict schema/wrapper closure + F24–F27 source-native identity when LIVE-born |
| world.connection | current catalog/native owner | RD-16 strict schema/wrapper closure + F24–F27 source-native identity when LIVE-born |
| world.zone | current catalog/native owner | RD-16 strict schema/wrapper closure + F24–F27 source-native identity when LIVE-born |
| world.organization | current catalog/native owner | RD-16 strict schema/wrapper closure; faction is only a facet; F24–F27 source-native identity when LIVE-born |
| world.contract | current catalog/native owner | RD-16 strict schema/wrapper closure + F24–F27 source-native identity when LIVE-born |
| world.mission | current catalog/native owner | RD-16 strict schema/wrapper closure + F24–F27 source-native identity when LIVE-born |
| world.scene | current scene owner + RD-08/RD-09 routing/currentness joins | RD-16 strict schema/wrapper closure + F24–F27 source-native identity when LIVE-born; F27 prevents raw semantic scene IDs from being used as physical LIVE ref components |
| world.encounter | current catalog/native owner | RD-16 strict schema/wrapper closure + F24–F27 source-native identity when LIVE-born |
| world.hazard | current catalog/native owner | RD-16 strict schema/wrapper closure + F24–F27 source-native identity when LIVE-born |
| world.effect | RD-03 / Effect owner | existing strict schema + RD-16 final wrapper proof + F24–F27 source-native identity when LIVE-born |
| world.lore_fact | RD-02 information/truth owner | RD-16 strict schema/wrapper closure + F24–F27 source-native identity when LIVE-born |
| world.knowledge | RD-02 knowledge owner | RD-16 strict schema; composite owner-equivalent identity retained; source-native cursor allocation does not apply |
| world.thread | RD-08 / WP-15 | RD-08 owner-local schema -> RD-16 shared catalog/identity integration; F24–F27 source-native identity when LIVE-born |
| world.player | WP-16 / RD-09 access-currentness consumers | RD-16 admission/schema/shared integration; enclosing world-record `id` is the sole native campaign player key; LIVE birth forbidden |

`world.faction` has explicit **NO INDEPENDENT NATIVE FAMILY** disposition.

## 3. Exact runtime-family forward map

| Family | Owning execution route |
|---|---|
| runtime.session | RD-07 session/recovery contract; LIVE birth forbidden |
| runtime.message | RD-02 information/message + RD-09 F24–F27 source-native identity when LIVE-born |
| runtime.interaction | RD-05 execution lifecycle + RD-09 F24–F27 source-native identity when LIVE-born |
| runtime.procedure | RD-05 execution lifecycle + RD-09 F24–F27 source-native identity when LIVE-born |
| runtime.intent_plan | RD-05 execution lifecycle; owner-equivalent/derived LIVE identity, not source-native cursor allocation |
| runtime.command | RD-05 execution lifecycle; catalog-backed acceptance requires RD-15 `SUPPORTED` binding and persists accepted reconstructive `CatalogContextBasis`; owner-equivalent/derived LIVE identity |
| runtime.resolution | RD-05 execution lifecycle; catalog-backed execution preserves exact equality with root command catalog basis; F24–F27 source-native identity when LIVE-born |
| runtime.continuation | RD-05 execution/recovery evidence; suspended generation persists accepted catalog basis; owner-equivalent/derived LIVE identity |
| runtime.mechanical_event | RD-05 composite identity -> RD-16 shared identifier integration; source-native cursor allocation does not apply |
| runtime.semantic_event | RD-13 native history + RD-09 F24–F27 source-native identity when LIVE-born |
| runtime.resolution_trace | RD-05 execution evidence; owner-equivalent LIVE identity |
| runtime.disclosure | RD-02 disclosure owner; composite/owner-equivalent LIVE identity |
| runtime.collaboration_obligation | RD-12 collaboration owner; LIVE birth forbidden |
| runtime.checkpoint | RD-07 checkpoint/recovery; accepted catalog basis participates in recoverability/currentness proof where accepted execution is reachable; LIVE birth forbidden |
| runtime.id_allocator | RD-04 exceptional campaign allocator route; never used by source-native LIVE identity |
| runtime.maintenance_audit | RD-07 maintenance/recovery evidence route; LIVE birth forbidden |
| runtime.catalog_gap_report | RD-15 deterministic unsupported-capability evidence with exact accepted catalog basis -> RD-06 publication/retention -> RD-07 recovery; LIVE birth forbidden |

Definitions remain in their resolved catalog sources and are **not** new runtime/world record families. Finding 23 adds typed owner-local dependency refs only as embedded accepted-context evidence.

## 4. Post-WP27 graph-closure atoms

The following implementation obligations were discovered after the historical readiness decomposition. They are current work because accepted owners already require them; they are not new readiness IDs.

```text
F06 temporal completeness routing                 -> RD-08 + RD-07 join
F07 WP-16 executable LIVE closure                -> RD-09 + RD-16 shared policy integration
F08 player/faction/thread family reconciliation  -> RD-04/RD-08 + RD-16
F09 bounded principal-to-player routing          -> RD-09 + RD-06/RD-07 joins
F10 MechanicalEvent identity                     -> RD-05 + RD-16
F11 catalog runtime binding / gap evidence       -> RD-15
F12 strict world-family machine realization      -> RD-16
F13 shared catalog/identifier writer closure     -> RD-16
F14 shipped catalog-binding consumer cutover     -> RD-15 consumer checkpoint
F15 package-router / execution integration       -> package index + post-graph integration overlay
F16 single native player record key              -> RD-16/package-index rule
F17 RD-15/RD-16 checkpoint coherence             -> overlay-5 law extended by package index
F18 RD-15 validated binding -> RD-05 acceptance  -> hard prerequisite at catalog-backed acceptance checkpoint
F19 current bidirectional coverage rebuild       -> this v3 artifact
F20 current proof-ledger rebuild                 -> proof-ledger v3; RD-15/RD-16 required for R018/family proof
F21 current 16-RD execution DAG                  -> execution-waves-v2-post-graph
F22 exact post-WP27 witness routing              -> post-graph proof witness matrix
F23 reconstructive accepted catalog basis        -> RD-15 -> RD-05 -> RD-06 -> RD-07
F24 source-native LIVE cursor/printable-ID basis -> RD-09 cursor/encoding/CAS -> RD-16 shared policy -> RD-07 recovery
F25 campaign semantic-ID / physical-route split  -> RD-14 + RD-06 -> RD-09 route/body/ID validation -> RD-07 recovery
F26 deterministic LIVE creation-slot order       -> RD-09 normalization/allocation/CAS -> RD-16 proof + RD-07 recovery
F27 exact LIVE epoch / scene route identity      -> RD-09 claim+epoch+ref realization -> RD-06 route-selection validation -> RD-07 recovery
```

Findings 1–5 remain routed by the earlier SIRR2/author repair overlays and are not replaced by this table.

## 5. F23 bidirectional mapping

Forward:

```text
Catalog Resolution / Ruleset Package Identity / Step-3 accepted-context law
  -> F23
  -> RD-15 CatalogContextBasis producer + session-only durability guard
  -> RD-05 RuntimeCommand / Resolution / Continuation accepted basis
  -> RD-06 correctness-required retention/publication closure
  -> RD-07 exact reconstruction / no ambient rebind
  -> exact F23 witness classes
```

Reverse:

```text
catalog-definition-dependency-ref schema
catalog-context-basis schema
RuntimeCommand catalog_context_basis
Resolution catalog_context_basis
Continuation catalog_context_basis
CatalogGapReport catalog_context_basis
binder session-only guard
accepted-execution retention join
exact recovery reconstruction
  -> F23
  -> accepted owners above
```

## 6. F24–F27 bidirectional LIVE identity / route mapping

Forward:

```text
Step-5.8 / WP-16 stable LIVE authority + live-born identity laws
  -> F24 cursor + printable source-native ID realization
  -> F25 canonical campaign_id source key + bounded c1 physical campaign token
  -> F26 deterministic attempt-local multiple-creation normalization
  -> F27 canonical immutable-claim framing + e1 epoch identity + s1 scene token
  -> RD-09 exact-source/opening/CAS machinery
  -> RD-06 campaign route-selection validation
  -> RD-16 final live_birth/identifier-policy machine write/proof
  -> RD-07 selected-LIVE source/opening/allocation recovery validation
  -> exact PG24/PG25/PG26/PG27 witnesses
```

Correct semantic source key:

```text
(campaign_id, scene_id, epoch_id)
```

Current physical WP-11 LIVE route:

```text
live/c1-<64hex>/s1-<64hex>/e1-<64hex>/LIVE/LIVE_STATE.yaml
```

where:

- `c1-...` = domain-separated SHA-256 token of canonical `campaign_id` (F25);
- `s1-...` = domain-separated SHA-256 token of canonical semantic `scene_id` (F27);
- `e1-...` = full SHA-256 digest of the exact domain-separated opening basis `(campaign_id, scene_id, pinned opening campaign revision, canonical immutable claim set)` (F27).

The campaign and scene tokens are physical locators only. `epoch_id` is semantic identity with an intentionally transport-safe v1 spelling. Route/token/digest equality never substitutes for full expected LIVE envelope/opening-basis equality.

Canonical F27 claim frames consume only the accepted closed claim grammar:

```text
EXACT_OWNER(native_family, complete owner-ordered identity components)
EPOCH_LOCAL_CREATION(native_family)
OWNER_DEFINED_PARTITION(partition_type, complete owner-ordered key components)
```

Complete claim frames are sorted lexicographically as bytes because the claim set is unordered. Duplicate canonical claims or a partition without a deterministic bounded key block opening; arbitrary JSON/model/container ordering is never identity.

For multiple `SOURCE_NATIVE_LIVE` creations in one accepted LIVE mutation, F26 remains:

```text
per-family owner deterministic sequence
-> family groups by UTF8(native_family)
-> contiguous owner_local_creation_index
-> contiguous creation_slot_index
-> source_local_creation_ordinal = frozen_cursor + slot
-> final native ID
```

Reverse:

```text
MANIFEST campaign_id creation/immutability
c1 campaign physical route token
s1 scene physical route token
canonical immutable claim frames
e1 epoch_id derivation
LIVE envelope campaign_id/scene_id/epoch_id/opening_campaign_revision/Q
framed_base32hex_v1 source-native IDs using semantic source values
next_source_native_creation_ordinal
owner_local_creation_index / creation_slot_index
FrozenLiveAttempt source_native_allocations
campaign route-selection validation
selected-LIVE recovery validation
  -> F24/F25/F26/F27
  -> WP-19 campaign identity + WP-11 bounded physical route + Step-5.8/WP-16 LIVE opening/currentness/live-born identity laws
```

These findings introduce no campaign allocator dependency, global epoch allocator, global sequence, fictional chronology, new native family, second campaign identity, generic ordering service or branch/ref semantic authority.

## 7. Reverse-coverage law

Every current implementation task must resolve backward to one of:

1. a historical direct readiness ID;
2. an admitted composite slice or exact proof duty;
3. a required consumer/version/checkpoint consequence of such work;
4. one of the explicit post-WP27 graph-closure atoms above, with an accepted native owner.

RD-15 tasks reverse to accepted catalog-resolution and `runtime.catalog_gap_report` owners plus F23 accepted-context reconstruction. RD-16 tasks reverse to R018 per-family realization, current catalog structure/identity owners, shared-machine integration required by accepted deltas, and F24–F27 final source-native identifier-policy compatibility/proof. RD-05/RD-06/RD-07 F23 deltas reverse to Step-3 accepted execution, Catalog Resolution, Ruleset Package Identity and Step-5.13 retention/protection laws. RD-14/RD-06/RD-09/RD-07 F25 deltas reverse to WP-19 stable campaign identity, WP-11 physical routing and WP-16 exact source identity. RD-09/RD-07 F26 deltas reverse to Step-5.8/WP-16 accepted source-local coordinate and frozen exact-source CAS/recovery laws. RD-09/RD-06/RD-07 F27 deltas reverse to Step-5.8 opening/source authority, WP-16 closed claim grammar and WP-11 bounded LIVE physical route.

No wave number, file adjacency, legacy v0.8 artifact or author convenience creates semantic work.

## 8. Currentness / closure rule

Current package routing is RD-01..RD-16 plus the package-index mandatory precedence chain, including Finding 27 as the current highest-precedence LIVE epoch/physical-route refinement over Findings 24–26. Any older statement that raw semantic `campaign_id`/`scene_id` may be directly interpolated into the physical LIVE ref, that `campaign_technical_id` is semantic identity, that epoch spelling is implementation-choice/example-only, that `E_<first-12-hex>` is sufficient v1 contract, or that an unspecified normalized mutation list may choose source-native allocation order is superseded for v1 execution.

This v3 document does **not** declare zero-open author closure. Final closure still requires fresh reverse review of every RD-15/RD-16 task, full 17+17 family proof, F23 accepted-context proof, F24–F27 source-native identity/opening/routing/order/CAS/recovery proof, proof-witness/mechanism symmetry, shared-writer uniqueness, execution-wave reconciliation, exact package-index/master/progress agreement and exact-head hosted validation.

This coverage document does not decide the package's global open-finding or human-decision state. Current package owners control those gates. Independent review remains blocked. Production implementation remains unauthorized.

## 9. F58 — operational-root forward/reverse coverage

Mandatory overlay `2026-09-15-implementation-planning-operational-root-routing-addendum.md` is the later-precedence realization route for this bounded addition.

| Accepted obligation | Executable realization and reverse owner |
|---|---|
| Step-5.2 Laws 2–5/9–11 and section 5; WP-14 Laws 6–8; R072 | RD-05 native A/B/C eligibility -> RD-07 typed active-only path/contract -> RD-06 campaign closure / RD-09 selected-LIVE CAS and handoff -> RD-07 complete exact-pinned root/dependency hydration. |
| Steps 5.4/5.5 and WP-13 promised durable closure | Class-C accepted unresolved input is enrolled only when protected by the owner-defined promise; irreducible accepted evidence remains recoverable. No new durable promise authority. |
| Existing scaffold law / F40 | RD07_OPERATIONAL_ROOT_CONTRACT_READY contributes FORMAT.yaml before RD14 generator validation, independently of full runtime/LIVE/RD16 completion. |
| Existing F41/F47/F46 physical projections | Five schema-README owner inputs with the full RD07 delta; four storage-template inputs including bounded RD07 operational routing; existing one-final-edit STORAGE/LIVE_SCENE targets. |
| PG35 | Exact actual-producer/publication/handoff/recovery/scaffold/final-byte witnesses in the post-graph matrix and overlay 37; R038/R072/R074 duties remain item-bound. |

The derivative FORMAT.yaml, per-native-owner route documents, embedded LIVE operational_root_routes, mechanical recovery_roots.py helpers and their proof checkpoints all reverse to the accepted laws above. They are not extra native families or a new semantic owner; the 17+17 census and historical readiness accounting are unchanged. Current lifecycle authority remains in runtime.command, runtime.procedure, runtime.interaction and runtime.intent_plan. All later package-index overlays remain mandatory beyond this document's earlier F27 narrative.

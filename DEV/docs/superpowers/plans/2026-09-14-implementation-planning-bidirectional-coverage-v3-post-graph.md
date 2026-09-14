# HDM Implementation Planning — Bidirectional Coverage / Currentness v3

Status: **CURRENT AUTHOR POST-GRAPH COVERAGE — ADVERSARIAL CLOSURE ACTIVE**
Date: 2026-09-14
Finding origin: **AUTHOR FINDING 19 — SIGNIFICANT**, extended through Finding 26.
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
| world.actor | RD-03 / Actor owner | existing strict schema + RD-16 final wrapper proof; SOURCE_NATIVE_LIVE birth uses F24/F25/F26 RD-09 source/cursor/order realization when admitted |
| world.actor_group | RD-03 / Actor-group owner | existing strict schema + RD-16 final wrapper proof; SOURCE_NATIVE_LIVE birth uses F24/F25/F26 when admitted |
| world.asset | RD-03 / Asset owner | existing strict schema + RD-16 final wrapper proof; SOURCE_NATIVE_LIVE birth uses F24/F25/F26 when admitted |
| world.location | current catalog/native owner | RD-16 strict schema/wrapper closure + F24/F25/F26 source-native identity when LIVE-born |
| world.connection | current catalog/native owner | RD-16 strict schema/wrapper closure + F24/F25/F26 source-native identity when LIVE-born |
| world.zone | current catalog/native owner | RD-16 strict schema/wrapper closure + F24/F25/F26 source-native identity when LIVE-born |
| world.organization | current catalog/native owner | RD-16 strict schema/wrapper closure; faction is only a facet; F24/F25/F26 source-native identity when LIVE-born |
| world.contract | current catalog/native owner | RD-16 strict schema/wrapper closure + F24/F25/F26 source-native identity when LIVE-born |
| world.mission | current catalog/native owner | RD-16 strict schema/wrapper closure + F24/F25/F26 source-native identity when LIVE-born |
| world.scene | current scene owner + RD-08/RD-09 routing/currentness joins | RD-16 strict schema/wrapper closure + F24/F25/F26 source-native identity when LIVE-born |
| world.encounter | current catalog/native owner | RD-16 strict schema/wrapper closure + F24/F25/F26 source-native identity when LIVE-born |
| world.hazard | current catalog/native owner | RD-16 strict schema/wrapper closure + F24/F25/F26 source-native identity when LIVE-born |
| world.effect | RD-03 / Effect owner | existing strict schema + RD-16 final wrapper proof + F24/F25/F26 source-native identity when LIVE-born |
| world.lore_fact | RD-02 information/truth owner | RD-16 strict schema/wrapper closure + F24/F25/F26 source-native identity when LIVE-born |
| world.knowledge | RD-02 knowledge owner | RD-16 strict schema; composite owner-equivalent identity retained; source-native cursor allocation does not apply |
| world.thread | RD-08 / WP-15 | RD-08 owner-local schema -> RD-16 shared catalog/identity integration; F24/F25/F26 source-native identity when LIVE-born |
| world.player | WP-16 / RD-09 access-currentness consumers | RD-16 admission/schema/shared integration; enclosing world-record `id` is the sole native campaign player key; LIVE birth forbidden |

`world.faction` has explicit **NO INDEPENDENT NATIVE FAMILY** disposition.

## 3. Exact runtime-family forward map

| Family | Owning execution route |
|---|---|
| runtime.session | RD-07 session/recovery contract; LIVE birth forbidden |
| runtime.message | RD-02 information/message + RD-09 F24/F25/F26 source-native identity when LIVE-born |
| runtime.interaction | RD-05 execution lifecycle + RD-09 F24/F25/F26 source-native identity when LIVE-born |
| runtime.procedure | RD-05 execution lifecycle + RD-09 F24/F25/F26 source-native identity when LIVE-born |
| runtime.intent_plan | RD-05 execution lifecycle; owner-equivalent/derived LIVE identity, not source-native cursor allocation |
| runtime.command | RD-05 execution lifecycle; catalog-backed acceptance requires RD-15 `SUPPORTED` binding and persists accepted reconstructive `CatalogContextBasis`; owner-equivalent/derived LIVE identity |
| runtime.resolution | RD-05 execution lifecycle; catalog-backed execution preserves exact equality with root command catalog basis; F24/F25/F26 source-native identity when LIVE-born |
| runtime.continuation | RD-05 execution/recovery evidence; suspended generation persists accepted catalog basis; owner-equivalent/derived LIVE identity |
| runtime.mechanical_event | RD-05 composite identity -> RD-16 shared identifier integration; source-native cursor allocation does not apply |
| runtime.semantic_event | RD-13 native history + RD-09 F24/F25/F26 source-native identity when LIVE-born |
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

## 6. F24/F25/F26 bidirectional LIVE identity mapping

Forward:

```text
Step-5.8 / WP-16 stable live-born identity laws
  -> F24 cursor + printable ID realization
  -> F25 canonical campaign_id source key + bounded derived physical route token
  -> F26 deterministic attempt-local multiple-creation normalization
  -> RD-09 exact-source CAS freezes semantic source tuple, allocation array, final IDs and cursor advance
  -> RD-16 final live_birth/identifier-policy machine write/proof
  -> RD-07 selected-LIVE source identity/allocation recovery validation
  -> exact PG24/PG25/PG26 witnesses
```

Correct semantic source key:

```text
(campaign_id, scene_id, epoch_id)
```

Physical WP-11 campaign route component:

```text
encode_live_campaign_route_token(campaign_id)
= "c1-" + lowercase(hex(SHA256(domain-separated length-framed UTF8(campaign_id))))
```

The physical token is only a locator and is verified against `LIVE_STATE.campaign_id`; source-native semantic IDs frame canonical `campaign_id`, never the physical token.

For multiple `SOURCE_NATIVE_LIVE` creations in one frozen attempt:

```text
per-family owner deterministic sequence
-> canonical family-group order by UTF8(native_family)
-> contiguous owner_local_creation_index
-> contiguous creation_slot_index
-> source_local_creation_ordinal = frozen_cursor + slot
-> final native ID
```

Reverse:

```text
MANIFEST campaign_id creation/immutability
c1-<sha256> physical LIVE route token
LIVE envelope campaign_id/scene_id/epoch_id validation
framed_base32hex_v1 using campaign_id
next_source_native_creation_ordinal
owner_local_creation_index / creation_slot_index
FrozenLiveAttempt source_native_allocations
final LIVE schema removal of generic provisional-rekey baseline
selected-LIVE recovery validation
  -> F24/F25/F26
  -> WP-19 campaign identity + WP-11 bounded route + Step-5.8/WP-16 stable live-born identity/CAS laws
```

These findings introduce no campaign allocator dependency, global sequence, fictional chronology, new native family, second campaign identity, generic ordering service or transport-ref semantic identity.

## 7. Reverse-coverage law

Every current implementation task must resolve backward to one of:

1. a historical direct readiness ID;
2. an admitted composite slice or exact proof duty;
3. a required consumer/version/checkpoint consequence of such work;
4. one of the explicit post-WP27 graph-closure atoms above, with an accepted native owner.

RD-15 tasks reverse to accepted catalog-resolution and `runtime.catalog_gap_report` owners plus F23 accepted-context reconstruction. RD-16 tasks reverse to R018 per-family realization, current catalog structure/identity owners, shared-machine integration required by accepted deltas, and F24–F26 final identifier-policy/source-native proof. RD-05/RD-06/RD-07 F23 deltas reverse to Step-3 accepted execution, Catalog Resolution, Ruleset Package Identity and Step-5.13 retention/protection laws. RD-14/RD-06/RD-09/RD-07 F25 deltas reverse to WP-19 stable campaign identity, WP-11 physical routing and WP-16 exact source identity. RD-09/RD-07 F26 deltas reverse to Step-5.8/WP-16 accepted source-local coordinate and frozen exact-source CAS/recovery laws.

No wave number, file adjacency, legacy v0.8 artifact or author convenience creates semantic work.

## 8. Currentness / closure rule

Current package routing is RD-01..RD-16 plus the package-index mandatory precedence chain, including Findings 25–26 as current highest-precedence LIVE identity refinements over Finding 24. Any older statement that the semantic source key is `(campaign_technical_id, scene_id, epoch_id)`, that raw campaign identity is a physical ref component, or that an unspecified "normalized mutation list" may choose allocation order is superseded for v1 execution.

This v3 document does **not** declare zero-open author closure. Final closure still requires fresh reverse review of every RD-15/RD-16 task, full 17+17 family proof, F23 accepted-context proof, F24–F26 source-native identity/routing/order/CAS/recovery proof, proof-witness/mechanism symmetry, shared-writer uniqueness, execution-wave reconciliation, exact package-index/master/progress agreement and exact-head hosted validation.

Architecture reopen: **NO CURRENT OPEN REOPEN**. Human product decision: **NO CURRENT OPEN DECISION**. Independent review remains blocked. Production implementation remains unauthorized.

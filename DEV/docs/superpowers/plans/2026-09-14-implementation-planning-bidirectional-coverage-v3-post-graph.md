# HDM Implementation Planning — Bidirectional Coverage / Currentness v3

Status: **CURRENT AUTHOR POST-GRAPH COVERAGE — ADVERSARIAL CLOSURE ACTIVE**
Date: 2026-09-14
Finding origin: **AUTHOR FINDING 19 — SIGNIFICANT**, extended through Finding 24.
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
| world.actor | RD-03 / Actor owner | existing strict schema + RD-16 final wrapper proof; SOURCE_NATIVE_LIVE birth uses F24 RD-09 encoding/cursor when admitted |
| world.actor_group | RD-03 / Actor-group owner | existing strict schema + RD-16 final wrapper proof; SOURCE_NATIVE_LIVE birth uses F24 when admitted |
| world.asset | RD-03 / Asset owner | existing strict schema + RD-16 final wrapper proof; SOURCE_NATIVE_LIVE birth uses F24 when admitted |
| world.location | current catalog/native owner | RD-16 strict schema/wrapper closure + F24 source-native identity when LIVE-born |
| world.connection | current catalog/native owner | RD-16 strict schema/wrapper closure + F24 source-native identity when LIVE-born |
| world.zone | current catalog/native owner | RD-16 strict schema/wrapper closure + F24 source-native identity when LIVE-born |
| world.organization | current catalog/native owner | RD-16 strict schema/wrapper closure; faction is only a facet; F24 source-native identity when LIVE-born |
| world.contract | current catalog/native owner | RD-16 strict schema/wrapper closure + F24 source-native identity when LIVE-born |
| world.mission | current catalog/native owner | RD-16 strict schema/wrapper closure + F24 source-native identity when LIVE-born |
| world.scene | current scene owner + RD-08/RD-09 routing/currentness joins | RD-16 strict schema/wrapper closure + F24 source-native identity when LIVE-born |
| world.encounter | current catalog/native owner | RD-16 strict schema/wrapper closure + F24 source-native identity when LIVE-born |
| world.hazard | current catalog/native owner | RD-16 strict schema/wrapper closure + F24 source-native identity when LIVE-born |
| world.effect | RD-03 / Effect owner | existing strict schema + RD-16 final wrapper proof + F24 source-native identity when LIVE-born |
| world.lore_fact | RD-02 information/truth owner | RD-16 strict schema/wrapper closure + F24 source-native identity when LIVE-born |
| world.knowledge | RD-02 knowledge owner | RD-16 strict schema; composite owner-equivalent identity retained; F24 encoding does not apply |
| world.thread | RD-08 / WP-15 | RD-08 owner-local schema -> RD-16 shared catalog/identity integration; F24 source-native identity when LIVE-born |
| world.player | WP-16 / RD-09 access-currentness consumers | RD-16 admission/schema/shared integration; enclosing world-record `id` is the sole native campaign player key; LIVE birth forbidden |

`world.faction` has explicit **NO INDEPENDENT NATIVE FAMILY** disposition.

## 3. Exact runtime-family forward map

| Family | Owning execution route |
|---|---|
| runtime.session | RD-07 session/recovery contract; LIVE birth forbidden |
| runtime.message | RD-02 information/message + RD-09 F24 source-native identity when LIVE-born |
| runtime.interaction | RD-05 execution lifecycle + RD-09 F24 source-native identity when LIVE-born |
| runtime.procedure | RD-05 execution lifecycle + RD-09 F24 source-native identity when LIVE-born |
| runtime.intent_plan | RD-05 execution lifecycle; owner-equivalent/derived LIVE identity, not F24 encoding |
| runtime.command | RD-05 execution lifecycle; catalog-backed acceptance requires RD-15 `SUPPORTED` binding and persists the accepted reconstructive `CatalogContextBasis`; owner-equivalent/derived LIVE identity |
| runtime.resolution | RD-05 execution lifecycle; catalog-backed execution preserves exact equality with root command catalog basis; F24 source-native identity when LIVE-born |
| runtime.continuation | RD-05 execution/recovery evidence; suspended generation persists accepted catalog basis; owner-equivalent/derived LIVE identity |
| runtime.mechanical_event | RD-05 composite identity -> RD-16 shared identifier integration; F24 encoding does not apply |
| runtime.semantic_event | RD-13 native history + RD-09 F24 source-native identity when LIVE-born |
| runtime.resolution_trace | RD-05 execution evidence; owner-equivalent LIVE identity |
| runtime.disclosure | RD-02 disclosure owner; composite/owner-equivalent LIVE identity |
| runtime.collaboration_obligation | RD-12 collaboration owner; LIVE birth forbidden |
| runtime.checkpoint | RD-07 checkpoint/recovery; accepted catalog basis participates in recoverability/currentness proof where accepted execution is reachable; LIVE birth forbidden |
| runtime.id_allocator | RD-04 exceptional campaign allocator route; never used by F24 |
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
F24 exact source-native LIVE ID realization      -> RD-09 encoding/cursor/CAS -> RD-16 shared policy -> RD-07 recovery
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

## 6. F24 bidirectional mapping

Forward:

```text
Step-5.8 / WP-16 live-born stable-identity laws
  -> F24
  -> RD-09 stable LiveSourceKey + uint64 source-local cursor + framed_base32hex_v1
  -> same exact-source CAS freezes record IDs and cursor advance
  -> RD-16 final live_birth/identifier-policy machine write
  -> RD-07 selected-LIVE ID/cursor recovery validation
  -> exact F24 witnesses
```

Reverse:

```text
framed_base32hex_v1 policy
next_source_native_creation_ordinal
FrozenLiveAttempt source_native_allocations
final LIVE schema removal of generic provisional-rekey baseline
source-native selected-LIVE recovery validation
  -> F24
  -> Step-5.8/WP-16 stable live-born identity laws
```

F24 introduces no campaign allocator dependency, global sequence, fictional chronology, new native family or transport-ref identity. Stable source key is `(campaign_technical_id, scene_id, epoch_id)`; exact source revision remains a separate CAS/currentness fence.

## 7. Reverse-coverage law

Every current implementation task must resolve backward to one of:

1. a historical direct readiness ID;
2. an admitted composite slice or exact proof duty;
3. a required consumer/version/checkpoint consequence of such work;
4. one of the explicit post-WP27 graph-closure atoms above, with an accepted native owner.

RD-15 tasks reverse to accepted catalog-resolution and `runtime.catalog_gap_report` owners plus F23 accepted-context reconstruction. RD-16 tasks reverse to R018 per-family realization, current catalog structure/identity owners, shared-machine integration required by accepted deltas, and F24 final identifier-policy projection. RD-05/RD-06/RD-07 F23 deltas reverse to Step-3 accepted execution, Catalog Resolution, Ruleset Package Identity and Step-5.13 retention/protection laws. RD-09/RD-07 F24 deltas reverse to Step-5.8/WP-16 source-native identity and exact-source CAS/recovery laws.

No wave number, file adjacency, legacy v0.8 artifact or author convenience creates semantic work.

## 8. Currentness / closure rule

Current package routing is RD-01..RD-16 plus the package-index mandatory precedence chain, including the Finding-24 source-native LIVE ID overlay as current highest precedence. Any statement in older coverage/wave artifacts that the current RD count remains 14 or that LIVE-born IDs may generically rekey at compaction is historical/superseded for v1 execution.

This v3 document does **not** declare zero-open author closure. Final closure still requires fresh reverse review of every RD-15/RD-16 task, full 17+17 family proof, F23 accepted-context proof, F24 source-native identity/CAS/recovery proof, proof-witness/mechanism symmetry, shared-writer uniqueness, execution-wave reconciliation, exact package-index/master/progress agreement and exact-head hosted validation.

Architecture reopen: **NO CURRENT OPEN REOPEN**. Human product decision: **NO CURRENT OPEN DECISION**. Independent review remains blocked. Production implementation remains unauthorized.

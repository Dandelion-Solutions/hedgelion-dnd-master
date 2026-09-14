# HDM Implementation Planning — Bidirectional Coverage / Currentness v3

Status: **CURRENT AUTHOR POST-GRAPH COVERAGE — ADVERSARIAL CLOSURE ACTIVE**
Date: 2026-09-14
Finding: **AUTHOR FINDING 19 — SIGNIFICANT**
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

The original direct readiness IDs remain assigned to RD-01..RD-14 exactly as in v2. RD-15 and RD-16 are post-WP27 graph-closure units; they do not invent historical readiness IDs.

Current decomposition count: **16 RD units**.

## 2. Exact world-family forward map

| Family | Semantic / owner route | Current machine execution route |
|---|---|---|
| world.actor | RD-03 / Actor owner | existing strict schema + RD-16 final wrapper proof |
| world.actor_group | RD-03 / Actor-group owner | existing strict schema + RD-16 final wrapper proof |
| world.asset | RD-03 / Asset owner | existing strict schema + RD-16 final wrapper proof |
| world.location | current catalog/native owner | RD-16 strict schema/wrapper closure |
| world.connection | current catalog/native owner | RD-16 strict schema/wrapper closure |
| world.zone | current catalog/native owner | RD-16 strict schema/wrapper closure |
| world.organization | current catalog/native owner | RD-16 strict schema/wrapper closure; faction is only a facet |
| world.contract | current catalog/native owner | RD-16 strict schema/wrapper closure |
| world.mission | current catalog/native owner | RD-16 strict schema/wrapper closure |
| world.scene | current scene owner + RD-08/RD-09 routing/currentness joins | RD-16 strict schema/wrapper closure |
| world.encounter | current catalog/native owner | RD-16 strict schema/wrapper closure |
| world.hazard | current catalog/native owner | RD-16 strict schema/wrapper closure |
| world.effect | RD-03 / Effect owner | existing strict schema + RD-16 final wrapper proof |
| world.lore_fact | RD-02 information/truth owner | RD-16 strict schema/wrapper closure |
| world.knowledge | RD-02 knowledge owner | RD-16 strict schema; composite identity retained |
| world.thread | RD-08 / WP-15 | RD-08 owner-local schema -> RD-16 shared catalog/identity integration |
| world.player | WP-16 / RD-09 access-currentness consumers | RD-16 admission/schema/shared integration; enclosing world-record id is the sole native campaign player key |

`world.faction` has explicit **NO INDEPENDENT NATIVE FAMILY** disposition.

## 3. Exact runtime-family forward map

| Family | Owning execution route |
|---|---|
| runtime.session | RD-07 session/recovery contract |
| runtime.message | RD-02 information/message + RD-09 LIVE identity join |
| runtime.interaction | RD-05 execution lifecycle |
| runtime.procedure | RD-05 execution lifecycle |
| runtime.intent_plan | RD-05 execution lifecycle |
| runtime.command | RD-05 execution lifecycle; catalog-backed acceptance requires RD-15 validated basis |
| runtime.resolution | RD-05 execution lifecycle |
| runtime.continuation | RD-05 execution/recovery evidence |
| runtime.mechanical_event | RD-05 composite identity -> RD-16 shared identifier integration |
| runtime.semantic_event | RD-13 native history |
| runtime.resolution_trace | RD-05 execution evidence |
| runtime.disclosure | RD-02 disclosure owner |
| runtime.collaboration_obligation | RD-12 collaboration owner |
| runtime.checkpoint | RD-07 checkpoint/recovery |
| runtime.id_allocator | RD-04 exceptional campaign allocator route |
| runtime.maintenance_audit | RD-07 maintenance/recovery evidence route |
| runtime.catalog_gap_report | RD-15 deterministic unsupported-capability evidence -> RD-06 publication -> RD-07 recovery |

## 4. Post-WP27 graph-closure atoms

The following implementation obligations were discovered after the historical readiness decomposition. They are current work because accepted owners already require them; they are not new readiness IDs.

```text
F06 temporal completeness routing                -> RD-08 + RD-07 join
F07 WP-16 executable LIVE closure               -> RD-09 + RD-16 shared policy integration
F08 player/faction/thread family reconciliation -> RD-04/RD-08 + RD-16
F09 bounded principal-to-player routing         -> RD-09 + RD-06/RD-07 joins
F10 MechanicalEvent identity                    -> RD-05 + RD-16
F11 catalog runtime binding / gap evidence      -> RD-15
F12 strict world-family machine realization     -> RD-16
F13 shared catalog/identifier writer closure    -> RD-16
F14 shipped catalog-binding consumer cutover    -> RD-15 consumer checkpoint
F15 package-router / execution integration      -> package index + post-graph integration overlay
F16 single native player record key             -> RD-16/package index rule
F17 RD-15/RD-16 checkpoint coherence            -> overlay-5 law extended by package index
F18 RD-15 validated basis -> RD-05 acceptance   -> hard prerequisite at catalog-backed acceptance checkpoint
F19 current bidirectional coverage rebuild      -> this v3 artifact
```

Findings 1–5 remain routed by the earlier SIRR2/author repair overlays and are not replaced by this table.

## 5. Reverse-coverage law

Every current implementation task must resolve backward to one of:

1. a historical direct readiness ID;
2. an admitted composite slice or exact proof duty;
3. a required consumer/version/checkpoint consequence of such work;
4. one of the explicit post-WP27 graph-closure atoms above, with an accepted native owner.

RD-15 tasks reverse to accepted catalog-resolution and runtime.catalog_gap_report owners. RD-16 tasks reverse to R018 per-family realization, current catalog structure/identity owners, and shared-machine integration required by already-accepted deltas.

No wave number, file adjacency, legacy v0.8 artifact or author convenience creates semantic work.

## 6. Currentness / closure rule

Current package routing is RD-01..RD-16 plus the package-index mandatory precedence chain. Any statement in older coverage/wave artifacts that the current RD count remains 14 is historical and superseded for execution.

This v3 document does **not** declare zero-open author closure. Final closure still requires fresh reverse review of every RD-15/RD-16 task, full 17+17 family proof, proof-witness/mechanism symmetry, shared-writer uniqueness, execution-wave reconciliation, exact package-index/master/progress agreement and exact-head hosted validation.

Architecture reopen: **NO CURRENT OPEN REOPEN**. Human product decision: **NO CURRENT OPEN DECISION**. Independent review remains blocked. Production implementation remains unauthorized.

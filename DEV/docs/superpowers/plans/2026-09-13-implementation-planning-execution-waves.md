# HDM Implementation Planning — Execution Waves / Integration Package

Status: **AUTHOR-REPAIRED PB-06 CANDIDATE / PLANNING ONLY**
Baseline: planning provenance only; execution always fresh-reads current branch HEAD. Production implementation authorized: NO.

A wave is a **scheduling/review grouping**, not a semantic owner and not automatically a barrier. RD task order and the explicit dependency edges below are authoritative where stricter.

## Edge vocabulary

Only these meanings may serialize implementation work:

```text
HARD_PRECEDES
    Target work is semantically invalid until predecessor contract/behavior exists.

JOIN_BEFORE_INTEGRATION
    Owner-local cores may proceed independently; the named integrated readiness/join cannot close until every listed slice is green.

INTEGRATION_COMPLETION_GATE
    A package/readiness/composite completion claim waits for listed results, but this does not block unrelated owner-local implementation.

SHARED_FILE_CHECKPOINT
    Two owners touch the same physical file. Their writes are sequenced against fresh current content to avoid destructive overlap; this is not semantic ownership/dependency.

SCHEDULING_PREFERENCE
    Suggested batching/review order only. It creates no prerequisite and may be reordered when current file/worker coordination makes another order safer.

PROOF_AFTER_TARGET
    Proof executes after the implicated target behavior exists. It creates no runtime dependency.

CONSTRAINS_WITHOUT_ORDERING
    One owner constrains another's allowed result but does not require execution before it.
```

A wave number by itself means `SCHEDULING_PREFERENCE`. “Exit” means a useful review checkpoint, not “all later waves were forbidden from starting”.

## Global rules

Fresh-read HEAD/AGENTS/current progress/owners/RD plan before each worker unit. TDD `RED -> GREEN -> REFACTOR -> VERIFY`; no RED-only completion checkpoint. Independent owner roots may run in parallel when they do not share a write surface or a `HARD_PRECEDES` edge. `JOIN_BEFORE_INTEGRATION` branches may progress independently; only the named join waits.

Every coherent checkpoint runs focused tests plus `python3 DEV/TOOLS/run_maintenance_audit.py`; package/wave closure later runs full DEV discovery/currentness. Version/schema/catalog/checkpoint/migration projections move with their owning coherent checkpoint. Trigger-gated 12 and no-work 79 remain outside execution.

### Global shared-file coordination

These are physical-write rules, not semantic prerequisites:

1. `GAME/SCHEMA/location.schema.yaml`: RD-04 removes reverse presence first, then RD-02 applies epistemic cleanup against fresh current content; later integration proves both survived.
2. `GAME/SCHEMA/pc.schema.yaml`, `npc.schema.yaml`, `item.schema.yaml`: RD-02 first publishes its `LegacyInformationProjectionTests`-green removal of forbidden epistemic authority; RD-03 then retires/replaces those legacy projections against that fresh checkpoint. Do not run independent concurrent writes to these files.
3. Any later newly discovered shared file uses the same rule: freeze neither owner; coordinate the smallest file checkpoint and fresh-read before the second write.

## EW-0 — shipped-projection root

**Scheduling preference:** RD-01 first for stale shipped/runtime-root/default/stack projections.

**Parallel eligibility:** RD-02/RD-03/RD-04 may perform RED/inventory/owner-reading work in parallel; they do not need whole RD-01 completion unless a concrete touched current projection is an RD-01-owned prerequisite.

Exit review point: stale root projections repaired; no runtime behavior inferred from prose.

## EW-1 — native families + owner-bound routing/HOT

Eligible independent roots: RD-02 information core, RD-03 Actor/Asset/Effect core, RD-04 routing/index/HOT core.

**E1 — JOIN_BEFORE_INTEGRATION:** each owner-specific `R016/R018/R052/R062` family slice joins RD-04 route/body/HOT only after that family's final native shape. RD-04 core route/HOT work need not wait for every later family.

R062 retains distinct native routes for Actor continuity/relations, Knowledge, Effect/application, TemporalBinding, runtime lifecycle/evidence, SemanticEvent/history, Disclosure and retained Message. No universal schema-first phase.

**E2 — INTEGRATION_COMPLETION_GATE:** RD-03 Actor shape feeds later R029/R030; R031/R032 proof is `PROOF_AFTER_TARGET` on realized RD-03/RD-14 behavior. No legacy PC/NPC/item compatibility layer.

**Shared-file checkpoints:** location follows RD-04 -> RD-02; PC/NPC/item follows RD-02 epistemic cleanup -> RD-03 retirement. These file orders do not say information semantically precedes Actor continuity.

Exit review point: admitted native identities/owners have executable contracts; indexes remain rebuildable/non-authoritative.

## EW-2 — deterministic execution + temporal core

Eligible independent roots: RD-05 deterministic execution core and RD-08 owner-local temporal/thread/Agenda core. RD-08's occurrence/execution join waits for RD-05, but its CURRENT/thread/TemporalBinding work does not.

**E3 — JOIN_BEFORE_INTEGRATION:** `R034/R035/R036` join RD-06 R037 after accepted execution establishment; no requirement that RD-06's unrelated RED/planner preparation wait.

**E6 — mixed edges:**
- `R075 HARD_PRECEDES R076` inside RD-08;
- R039 is `JOIN_BEFORE_INTEGRATION` between RD-05 accepted execution and RD-08 occurrence lifecycle;
- RD-05 Procedure/Continuation WP-15 repairs constrain/precede the RD-08 execution-recovery join, not RD-08 CURRENT/thread core;
- R077 local schema/CORE tasks may proceed when their owners are current, but R077 **integration completion** waits for RD-05 §13.12–13 and later RD-02/RD-09/RD-13 information/history joins named in the lossless ledger.

Exit review point: deterministic retry/RNG and temporal occurrence contracts exist without replay/reroll, chronology-from-ID or authority transfer.

## EW-3 — durability/publication, recovery, principal/LIVE

Wave number is a scheduling preference. RD-09 access/LIVE owner-local primitives are an admitted independent root and may start before RD-06/RD-07 completion. RD-06 publication and RD-07 campaign recovery likewise do not require whole RD-09 completion except for named selected-LIVE joins.

**E4:** `R069 HARD_PRECEDES R070`; owner/index closure joins publisher at the R070 integration checkpoint. R071 mixed repair+proof remains RD-06 and follows its item ledger.

**E5:** RD-04 route/HOT + RD-06 current publication evidence `JOIN_BEFORE_INTEGRATION` for RD-07 R072/current-native recovery. Checkpoint alignment consumes R073. Selected-LIVE recovery adds RD-09 R079/R080 only for the selected-LIVE path. Campaign-only recovery is not serialized behind unrelated LIVE work.

**E7:** `R078 HARD_PRECEDES R079` inside the access/currentness contract. R080 carries LIVE implementation+proof. R040 is an integration join between current authenticated/LIVE source and RD-05 accepted execution; RD-09 principal/claim/currentness core can precede that join. R053 waits for RD-02 normalization + RD-09 producer/currentness; it does not block unrelated LIVE lifecycle work.

Exit review point: save truth, publication currentness, recovery and access/LIVE are separately authoritative and their named joins are green.

## EW-4 — containment/context/collaboration/native history

This wave contains **parallel owner-local cores**, not a whole-RD barrier:
- RD-10 role/containment/protected-emission core;
- RD-11 context selection/bounds core;
- RD-12 collaboration-obligation/IntentClause/routing core;
- RD-13 native history + Story/T0 core.

RD-10 core may begin once its own owners/current files are read; it is not globally blocked on RD-09. RD-11 core and RD-12 core are explicitly not cyclic.

**E8 containment:**
- `R054 + R055 JOIN_BEFORE_INTEGRATION R056`;
- `R056 HARD_PRECEDES R057`;
- `R056 + R059 + R060` join context acceptance;
- R058/R061 are `PROOF_AFTER_TARGET`;
- R118/R133/R137 co-realize the RD-10 TurnEnvelope/role/visible-output boundary;
- R139 later consumes only eligible native epistemic/history evidence.

**RD-11/RD-12 cycle break:** RD-11 owner-local context machinery and RD-12 owner-local collaboration lifecycle/routing machinery may implement independently. RD-12 does not need completed RD-11 context for its core obligation lifecycle. RD-11 R124 is an `INTEGRATION_COMPLETION_GATE` after RD-02 disclosure + applicable RD-09 currentness + RD-10 role containment + RD-12 controlled-actor/multiplayer scope. Any RD-12 path that consumes assembled context is a later joined consumer, not a prerequisite for all RD-12 core tasks.

**E9 collaboration:** `R021 + R081 + R141 + R146` join before R082 acceptance. RD-09 access/currentness + R082 join recipient/current-generation acceptance. R044/R083 remain collaboration-owned. R122 joins only the smallest concrete material bridge from RD-08 chronology + RD-09 currentness + RD-11 context + RD-12 collaboration; no global context/collaboration barrier.

**E10 history/T0:** R099 precedes qualifying Story/Commentator consumption. `R051 + R084 + R099` join before R102. RD-13 native `R062.SEMANTIC_EVENT_HISTORY` is independently authoritative; it does not wait for Story projection freshness.

**E11 Dramaturg:** access/currentness + collaboration + R085 join R131 retained multiplayer Dramaturg acceptance. Only `DRAMATURG/SHARED.yaml` and `DRAMATURG/PLAYERS/<player_id>.yaml` are admitted retained horizons; no registry/plot graph/scheduler/single-player durable planning system.

**E12 retrospective:** native history/continuity + bounded Context Runtime join R097; R087 later reuses this route. R139 ranking cannot create eligibility/knowledge/truth. Commentator is not a prerequisite for ordinary retrospective context.

Exit review point: protected emission, ephemeral context, scoped collaboration and native history boundaries hold, with R124/R122 left until their explicit joins rather than whole-RD barriers.

## EW-5 — bootstrap/product joins

RD-14 owner-local bootstrap/product scaffolding may prepare independently where it does not consume unfinished runtime owners. Its completion joins wait for named upstreams, not blanket EW-4 completion.

R029 = RD-03 Actor + RD-06 durability + RD-14 onboarding (`JOIN_BEFORE_INTEGRATION`).
R087 = RD-11 retrospective + RD-13 SemanticEvent/T0 + RD-14 save/session/menu (`JOIN_BEFORE_INTEGRATION`).

**E13:** confirmed R069/R070 save + R086 route join R098. Local clear/menu transition occurs only after confirmed compatible success; RD-09 supplies multiplayer non-interference only where applicable. No implicit leave/control/lifecycle mutation.

**E14:** `R078 + R086 JOIN_BEFORE_INTEGRATION R100`; repository permission/PLAYER stable ID never substitutes for creator provenance.

Exit review point: deterministic bootstrap/onboarding/product consumers exist without executing gameplay bootstrap or creating semantic authority.

## EW-6 — composite parents + proof closure

No runtime subsystem. This wave is an `INTEGRATION_COMPLETION_GATE` + `PROOF_AFTER_TARGET` grouping only.

Reconcile exactly once: `R006,R016,R018,R029,R053,R062,R087,R122`. Each requires all named slices, local tests, cross-slice package witness, negative authority-transfer assertions, one reconciled parent Version Impact Gate and no half-migrated consumer.

Pure proof routes come from `2026-09-13-implementation-planning-lossless-proof-ledger.md` and its three appendices. Mixed implementation+proof leaves R071/R074/R077/R080/R083 cannot close from thematic RD summaries; their item ledgers govern. Future empirical rows remain deferred until owner trigger.

**E15:** R088/R089 execute only after applicable targets. Channel separation creates no runtime subsystem and cannot substitute static/CI evidence for behavioral, integration or empirical evidence.

## EW-7 — future worker final verification checkpoint

After future implementation only: all focused RD tests green; package proof ledger green for current rows; full DEV unittest discovery green; `python3 DEV/TOOLS/run_maintenance_audit.py` green; retired-authority stale searches clean; schema/catalog/checkpoint/version/migration evidence coherent; owner/ref reread current; hosted CI success on exact publication HEAD. Failed join returns to owning RD task, never architecture invention.

## Worker checkpoint policy

Use substantial atomic commits: one RD task cluster or named cross-RD join normally. Do not batch unrelated owners merely because they share a wave number. Do not split an atomic schema+validator+consumer migration into invalid intermediate commits.

When two eligible workers would touch the same file, apply `SHARED_FILE_CHECKPOINT`: one publishes a green coherent checkpoint, the second fresh-reads and applies only its own owner delta, then the integration test proves both survived. This is preferred over inventing a semantic dependency.

Handoff records HEAD, RD/task, readiness/slices, edge type (`HARD_PRECEDES`, `JOIN_BEFORE_INTEGRATION`, etc.), owners read, files/actions, RED/GREEN evidence, verification, Version Impact, migration/checkpoint impact, unresolved joins and next eligible task.

## PB-06 repaired self-review gate

PASS only if:
- every RD appears and E1–E15 has a named closure point;
- whole-wave ordering is never treated as an unstated prerequisite;
- true prerequisites, integration completion, scheduling preference and shared-file coordination are distinguishable;
- RD-02/RD-03 and RD-04/RD-02 shared files have explicit checkpoint ordering;
- RD-11/RD-12 core independence and R124 joined completion remain explicit;
- all eight composite parents and nine pure-proof leaves route through the lossless proof package;
- trigger/no-work sets remain untouched;
- production implementation remains unauthorized.

PB-07/final author repair performs canonical 133/133 bidirectional/currentness proof and independent Senior handoff.
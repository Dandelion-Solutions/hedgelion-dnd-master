# HDM Implementation Planning — Execution Waves / Integration Package

Status: PB-06 SELF-REVIEWED CANDIDATE / PLANNING ONLY
Baseline: `8f0450737b2500387ca0569afbf89c24ba8cd02a`. Production implementation authorized: NO.

A wave is an execution/checkpoint boundary, not a semantic owner. RD task order controls where stricter.

## Global rules
Fresh-read HEAD/AGENTS/current progress/owners/RD plan before each worker unit. TDD RED->GREEN->REFACTOR->VERIFY. JOIN branches may proceed independently but integrated completion waits for every prerequisite. Pure proof follows targets. Every checkpoint runs focused tests + maintenance audit; wave closure runs full DEV discovery/currentness. Version/schema/catalog/checkpoint/migration projections move coherently. Trigger-gated 12 and no-work 79 remain outside execution.

## EW-0 — shipped-projection root
Primary RD-01; parallel RED/inventory preparation for RD-02/RD-03/RD-04. Exit: stale shipped/runtime-root/default/stack projections repaired; no runtime behavior inferred from prose.

## EW-1 — native families + owner-bound routing/HOT
Parallel RD-02 information family, RD-03 Actor/Asset/Effect, RD-04 routing/index/HOT core.

E1 join: every owner-specific `R016/R018/R052/R062` family slice joins RD-04 route/body/HOT only after its final native shape. R062 preserves eight distinct native routes: Actor continuity/relations, knowledge, Effect/application, TemporalBinding, runtime lifecycle/evidence, SemanticEvent/history, Disclosure, retained Message. No universal schema-first phase.

E2: RD-03 Actor shape feeds later R029/R030; R031/R032 proof waits for realized RD-03. No legacy PC/NPC/item compatibility layer.

Exit: native identities/owners executable; indexes rebuildable/non-authoritative.

## EW-2 — deterministic execution + temporal core
Primary RD-05; RD-08 owner-local temporal core may proceed in parallel before execution join.

E3/E6: `R034/R035/R036 -> R037` closes later in RD-06; `R034/R036/R067 -> R038/R072` closes in RD-07; R039 joins RD-05 deterministic execution to RD-08 occurrence lifecycle. Within RD-08 `R075 HARD_PRECEDES R076`; R077 carries implementation + chronology/currentness proof.

Exit: deterministic retry/RNG and temporal occurrence contracts exist without replay/reroll, chronology-from-ID or authority transfer.

## EW-3 — durability/publication, recovery, principal/LIVE
Branches RD-06, RD-07, RD-09.

E4: `R069 HARD_PRECEDES R070`; owner/index closure + R070 joins publication/currentness; R071 mixed repair+proof remains RD-06.

E5: RD-04 + RD-06 join RD-07 R072; checkpoint acceptance consumes R073; selected-LIVE recovery additionally waits for RD-09 R079/R080. No checkpoint-first/guessed-latest recovery.

E7: `R078 HARD_PRECEDES R079`; R080 carries LIVE implementation+proof; R040 joins current authenticated/LIVE source to execution. R122 later consumes only smallest applicable currentness contribution.

Exit: save truth, publication currentness, recovery and access/LIVE are separately authoritative and integrated.

## EW-4 — containment/context/collaboration/native history
Parallel cores after prerequisites: RD-10, RD-11 core, RD-12 core, RD-13 native history + Story/T0 core.

E8 containment: `R054 + R055 JOIN_BEFORE_INTEGRATION R056`; `R056 HARD_PRECEDES R057`; `R056 + R059 + R060` join context acceptance. R058/R061 attach proof. R118/R133/R137 co-realize RD-10 TurnEnvelope/role/visible-output boundary. R139 completes in RD-11 only from eligible native epistemic/history evidence.

RD-11/RD-12 cycle break: build owner-local cores independently; then R124 completes in RD-11 after RD-02 disclosure + RD-09 applicable currentness + RD-10 role containment + RD-12 controlled-actor/multiplayer scope.

E9 collaboration: `R021 + R081 + R141 + R146 -> R082`; RD-09 access/currentness + R082 join recipient/current-generation acceptance. R044/R083 remain collaboration-owned. R122 joins RD-08 chronology + RD-09 currentness + RD-11 context + RD-12 collaboration bridge only for concrete material dependency.

E10: R099 T0 precedes qualifying Story/Commentator consumption; `R051 + R084 + R099 -> R102`. RD-13 owns `R062.SEMANTIC_EVENT_HISTORY` only as native-history integration; Story never becomes history/ACL/canon authority.

E11: access/currentness + collaboration + R085 -> R131 retained multiplayer Dramaturg acceptance; exact runtime retained horizons are `DRAMATURG/SHARED.yaml` and `DRAMATURG/PLAYERS/<player_id>.yaml`. No registry/plot graph/scheduler/single-player durable planning system.

E12: native history/continuity + bounded Context Runtime -> R097; R087 retrospective reuses this route; R139 ranking cannot create eligibility/knowledge/truth.

Exit: protected emission, ephemeral context, scoped collaboration and native history boundaries all hold.

## EW-5 — bootstrap/product joins
Primary RD-14 after required RD-03/RD-06/RD-09/RD-12/RD-13 results.

R029 = RD-03 Actor + RD-06 durability + RD-14 onboarding.
R087 = RD-11 retrospective + RD-13 SemanticEvent/T0 + RD-14 save/session/menu.
E13: R069/R070 confirmed save + R086 route -> R098; no context clear before confirmed success; RD-09 supplies multiplayer non-interference where applicable.
E14: `R078 + R086 -> R100`; repository permission/PLAYER stable ID never substitutes for creator provenance.

Exit: deterministic bootstrap/onboarding/product consumers without gameplay bootstrap execution or new semantic authority.

## EW-6 — composite parents + proof closure
No new runtime subsystem.

Reconcile exactly once: `R006,R016,R018,R029,R053,R062,R087,R122`. Each requires all slices, local tests, cross-slice proof, parent scenario/negative laws, one reconciled Version Impact Gate and no half-migrated consumer.

Pure proof routes: R023 applicable owner-family targets; R031/R032 RD-03; R041 RD-05 + implicated RD-06/RD-07/RD-08/RD-09 integrations; R058 RD-10/RD-11; R061 RD-11; R068 RD-04/RD-07; R088 all applicable realized targets; R089 channel-specific evidence boundaries. Mixed implementation+proof stays owner-local: R071 RD-06, R077 RD-08, R080 RD-09, R083 RD-12.

E15: R088/R089 execute only after applicable targets; proof-channel separation creates no runtime subsystem and cannot substitute for behavioral/empirical/release evidence.

## EW-7 — future worker final verification checkpoint
After future implementation only: all focused RD tests green; full DEV unittest discovery green; maintenance audit green; retired-authority stale searches clean; schema/catalog/checkpoint/version/migration evidence coherent; owner/ref reread current; hosted CI success on exact publication HEAD. Failed join returns to owning RD task, never architecture invention.

## Worker checkpoint policy
Use substantial atomic commits: one RD task cluster or named cross-RD join normally. Do not batch unrelated owners by wave; do not split an atomic schema+validator+consumer migration into invalid intermediate commits. Handoff records HEAD, RD/task, readiness/slices, owners read, files/actions, RED/GREEN evidence, verification, Version Impact, migration/checkpoint impact, unresolved joins and next eligible task.

## PB-06 self-review gate
PASS iff every RD appears, E1-E15 has a closure point, all 8 composite parents and 9 pure-proof leaves are routed, cycles are resolved without authority transfer, trigger/no-work sets remain untouched and production implementation remains unauthorized. PB-07 alone performs canonical 133/133 bidirectional coverage/currentness proof and Senior handoff.
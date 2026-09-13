# HDM Implementation Planning — Execution Waves / Integration Package

Status: PB-06 CANDIDATE / PLANNING ONLY
Baseline for PB-06 authoring: `8f0450737b2500387ca0569afbf89c24ba8cd02a`.
Production implementation authorized: NO.

Purpose: convert the 14 executable RD plans into dependency-safe worker waves. A wave is an execution/checkpoint boundary, not a new semantic owner. RD task order inside each plan remains authoritative where stricter.

## Global execution rules

1. Fresh-read HEAD, `AGENTS.md`, current progress, owning semantic specs and the RD plan before each worker unit.
2. TDD RED -> GREEN -> REFACTOR -> VERIFY for every implementation-bearing task.
3. A producer may proceed before an integration consumer only where the dependency is `JOIN_BEFORE_INTEGRATION`; the join cannot close until every named prerequisite exists.
4. Pure proof runs after named targets; no late generic test subsystem.
5. Every coherent worker checkpoint runs focused tests + maintenance audit; wave closure runs full DEV discovery and currentness reread.
6. Version Impact Gate is per task/wave. Schema/catalog/checkpoint/migration projections must move coherently with the owner change; no half-adopted alternate stack/state.
7. Trigger-gated 12 and no-work 79 remain outside execution. Runtime release/gameplay bootstrap remain out of scope unless a later authorized gate explicitly changes that.

## EW-0 — baseline guards and shipped-projection root

Primary: RD-01.
Parallel preparation: RED tests/inventory for RD-02/RD-03/RD-04.

Exit: stale shipped instruction/runtime-root/default/stack projections repaired under accepted owners; maintenance guards agree. No runtime behavior is claimed from prose repair.

## EW-1 — native families and owner-bound substrate

Primary parallel branches:
- RD-02 information/knowledge/disclosure/message native contracts;
- RD-03 Actor/Asset/Effect + continuity/history inputs;
- RD-04 deterministic routing/index/HOT substrate core.

Join rule: RD-04 may build generic owner-bound substrate in parallel, but route/body/load integration for a family waits for that family's final native shape. RD-04 never becomes semantic owner.

Composite partials admitted here include the RD-02/RD-03/RD-04 slices of R006/R016/R018/R053/R062 as defined by their plans. Parent closure is forbidden.

Exit: native identity/owner boundaries are executable; indexes remain rebuildable/non-authoritative; no legacy epistemic/entity authority survives target-local negative tests.

## EW-2 — deterministic execution and owner-local time/runtime branches

Primary: RD-05 deterministic execution core.
Parallel owner work: RD-08 temporal/thread/current-state core may proceed where it does not require the R039 execution join.

Hard/integration joins:
- RD-05 accepted execution + RD-04 substrate before execution/HOT integration closes;
- R039 completes in RD-08 only after required RD-05 execution result exists.

Exit: deterministic IDs/retry/fixed-RNG and temporal occurrence/current-state contracts exist without chronology-from-ID, replay/reroll or execution-owned temporal authority.

## EW-3 — durability, recovery and principal/LIVE currentness

Branches:
- RD-06 SAVE/publication/currentness consumes RD-05 accepted execution and RD-04 substrate;
- RD-07 recovery/checkpoint core follows required RD-06/RD-05 evidence at its integration gates;
- RD-09 principal/LIVE authorization/currentness core may proceed in parallel, but R040 waits for RD-05 and applicable temporal/currentness inputs.

Required joins:
- `R034 + R035 + R036 -> R037` in RD-06;
- `R069 HARD_PRECEDES R070` publication path;
- execution/recovery integration R038 closes in RD-07;
- execution/LIVE integration R040 closes in RD-09.

Exit: save truth, publication currentness, recovery and principal/LIVE currentness are separately authoritative and integrated; no force/blind retry/global ACL/global clock.

## EW-4 — role containment, Context Runtime, collaboration and native Story/history

Parallel cores after prerequisites:
- RD-10 role/TurnEnvelope/auxiliary/protected-emission after RD-05 + RD-09 prerequisites;
- RD-11 Context Runtime core after RD-02 + RD-09 + RD-10, excluding joins that require RD-12;
- RD-12 collaboration core after principal/recipient contracts, excluding RD-11-dependent final projection joins;
- RD-13 native SemanticEvent/history + Story/T0 core after native history/execution/temporal prerequisites.

Cycle-breaking join rule: RD-11 and RD-12 do not serialize wholesale. Build their owner-local cores first; then close `R124` only after RD-02 + RD-09 + RD-10 + RD-12 scope are available in RD-11.

`R122` parent join occurs only for a concrete material dependency after RD-08 chronology + RD-09 currentness + RD-11 context + RD-12 collaboration bridge. It never creates a global frontier.

RD-13 closes `R062.SEMANTIC_EVENT_HISTORY` only under native history ownership; Story remains projection. R099 T0 precedes qualifying Story/Commentator consumption.

Exit: only validated Narrator payload can cross EMISSION_COMMIT; Context Runtime remains ephemeral; collaboration remains scope-local; native history remains native authority.

## EW-5 — product/bootstrap and retained consumer joins

Primary: RD-14 after required RD-03/RD-06/RD-09/RD-12/RD-13 owner results.

Material joins:
- R029: RD-03 Actor + RD-06 durability + RD-14 onboarding;
- R087: RD-11 retrospective + RD-13 SemanticEvent/T0 + RD-14 save/session/menu;
- save-and-exit: R069/R070 save truth + R086 route -> R098; no context clear before confirmed success;
- creator fail-closed: `RD-09:R078 + RD-14:R086 -> R100`;
- retained multiplayer Dramaturg: RD-09 access/currentness + RD-12 collaboration + RD-13 retained-horizon route.

Exit: deterministic bootstrap/onboarding/product consumers exist without gameplay bootstrap execution, inferred lifecycle, creator-login substitution or second history/knowledge authority.

## EW-6 — composite-parent and pure-proof integration closure

No new production subsystem is created.

Composite parents to reconcile exactly once: `R006,R016,R018,R029,R053,R062,R087,R122`. For each parent require every slice, slice-local tests, cross-slice proof, parent negative/scenario obligations, one reconciled Version Impact Gate and no half-migrated consumer/projection.

Pure proof routes:
- R023 -> applicable owner-family targets;
- R031,R032 -> RD-03;
- R041 -> RD-05 plus implicated RD-06/RD-07/RD-08/RD-09 integration targets;
- R058 -> RD-10/RD-11;
- R061 -> RD-11;
- R068 -> RD-04/RD-07;
- R088 -> all applicable realized targets;
- R089 -> channel-specific evidence boundaries.

Mixed implementation+proof leaves remain in their RD owners: R071 RD-06, R077 RD-08, R080 RD-09, R083 RD-12.

Exit: proof evidence is attached to realized targets; no proof channel substitutes for behavioral/empirical/release evidence it cannot establish.

## EW-7 — implementation-package verification checkpoint

This is the worker-side final checkpoint after future implementation, not authorization to execute now.

Required evidence:
- focused RD tests all green;
- full `python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'` green;
- `DEV/TOOLS/run_maintenance_audit` green;
- negative stale searches for retired authorities/aliases;
- schema/catalog/checkpoint/version projections coherent;
- migration evidence where Version Impact requires it;
- current owner/ref reread shows no drift;
- hosted CI success on exact publication HEAD.

A failed join returns to the owning RD task; it does not authorize architecture invention or scope expansion.

## Worker checkpoint policy

Use substantial atomic commits: normally one RD task cluster or one named cross-RD join per commit. Do not batch unrelated owner changes merely because they share a wave. Do not split one atomic schema+validator+consumer migration across commits if intermediate state would be invalid.

Recommended worker handoff fields per checkpoint:
`HEAD`, RD/task, readiness IDs/slices, owner refs read, files/actions, RED evidence, GREEN evidence, full verification status, Version Impact, migration/checkpoint impact, unresolved joins, next eligible task.

## PB-06 self-review gate

PASS requires: every RD appears in at least one execution wave; all known hard/join dependencies have a closure point; all 8 composite parents and 9 pure proof leaves have explicit final routes; no circular dependency is solved by authority transfer; no trigger/no-work leakage; no production implementation authorization.

PB-07, not PB-06, performs the canonical readiness <-> task bidirectional 133/133 coverage/currentness proof and Senior handoff.
# HDM Implementation Planning — Decomposition Repair DC-001..DC-005

Status: **REPAIRED CANDIDATE OVERLAY — READY FOR INDEPENDENT RE-REVIEW / NOT EXECUTION-READY**

Date: 2026-09-13

This artifact repairs the rejected candidate decomposition after the independent Decomposition Critic at commit `2a0940aa8d59dc828f0a472ed58b31d8f92bf240`.

It is additive. It does **not** rewrite, shorten, or replace either:

- `2026-09-13-implementation-planning-p3-dependency-dag.md`; or
- `2026-09-13-implementation-planning-candidate-bounded-decomposition.md`.

Those documents remain intact as reviewed provenance. This repair supersedes only the exact unit boundaries, leaf classifications, dependency joins, proof routes, and P3 derived classifications named below. All unchanged rationale, negative laws, scopes, owner references, impact notes, and critic stress surface in the original artifacts remain in force.

No accepted product semantics or canonical architecture is changed. No version bump or migration is selected. Detailed executable plans and production implementation remain unauthorized until a fresh independent Decomposition Critic returns PASS.

## 1. Preserved accounting

```text
PLANNING_BASELINE_SHA: 85311db76be2e440c97baf0b0625177de2eb0774
ACTIVE_READINESS: 133
TRIGGER_GATED: 12
EXPLICIT_NO_WORK: 79
R27_R004: ABSENT
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
VERSION_IMPACT: NONE
MIGRATION_REQUIRED: NO
DETAILED_EXECUTABLE_PLAN_AUTHORING_AUTHORIZED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

Trigger-gated leaves remain exactly `R002`, `R005`, `R024`, `R090`, `R091`, `R092`, `R093`, `R094`, `R095`, `R096`, `R101`, `R103`. All 79 explicit no-work terminals remain no-work.

## 2. Repair model

The rejected one-leaf/one-primary-unit rule is too coarse where one canonical readiness record contains obligations belonging to several already-accepted native owners. The repaired decomposition therefore uses:

- **direct unit coverage** for a leaf whose implementation obligation has one coherent owner/checkpoint;
- **composite owner-scoped slices** where a single canonical leaf spans several owner checkpoints; slices are planning notation only and create no new semantic authority;
- **pure proof routes** for leaves with no independent production implementation.

No broad schema/catalog foundation is a universal predecessor. Owner-specific machine projections travel with their owner-specific consumers/version checkpoints. Proof stays target-local.

## 3. Repaired bounded units

### RD-01 — shipped instruction/current-projection repair

Direct: `R001`, `R003`, `R033`, `R043`, `R047`, `R048`, `R050`.

Semantically unchanged from original `CD-01`; all original invariants/out-of-scope statements remain.

### RD-02 — information/lore/knowledge/disclosure/message realization

Direct: `R007`, `R008`, `R009`, `R017`, `R049`, `R052`.

Composite: `R006.INFO`, `R016.INFO`, `R018.INFO`, `R053.INFO`, `R062.INFO`.

Boundary: information-family schemas/roots/catalog projections plus direct information consumers and negative-regression proof. This checkpoint must be valid without prematurely publishing LIVE, recovery, collaboration, Story, or Actor-specific projections.

Joins RD-04 only at route/load integration; joins RD-09 where LIVE evidence normalizes into native information owners.

Protected: no `Secret`, no second knowledge/disclosure/event owner, no `truth.disputed`, no disclosure-implies-PC-knowledge rule, no false catalog-completion inference.

### RD-03 — Actor/Asset/Effect plus layered Actor continuity

Direct: `R025..R030`, `R104`, `R108..R111`, `R113..R116`, `R126`, `R128..R130`, `R132`, `R136`, `R139`.

Composite: `R006.ACTOR`, `R016.ACTOR`, `R018.ACTOR`, `R062.ACTOR_HISTORY`.

Boundary: Actor/Asset/Effect schemas/routes and runtime/state/continuity/history consumers move together. The former generic schema foundation no longer owns these projections.

Joins RD-04 at routing/index/HOT integration. RD-02 information laws constrain integration but do not create a schema-first hard edge.

Original `CD-03` negative laws remain, including no generic memory/NPC simulation and no epistemic alias as Actor authority.

### RD-04 — owner-native routing, derived indexes, HOT substrate

Direct: `R015`, `R063..R067`.

Composite integration: owner-route/root portions of `R018` join only after the corresponding owner unit supplies its final machine shape.

Boundary: routing/index/HOT infrastructure implements accepted contracts but does not semantically own native schemas.

Protected: no path/index/cache authority, generic ID registry, SQL-order authority, global dirty frontier, or cross-owner transaction authority.

### RD-05 — deterministic execution/fixed RNG/failure adapters

Direct: `R034..R040`, `R042`, `R046`, `R112`, `R118`, `R133`, `R137`.

`R044` is removed from execution ownership. `R045` is removed from execution ownership.

Boundary: Step-3 execution identity, local mechanics atomicity, fixed RNG, native failure/diagnostic/output behavior and direct proof.

Joins RD-12 only when a collaborative action actually becomes executable mechanics; RD-06 receives owner-approved execution inputs where publication is required.

All original `CD-05` negative laws remain.

### RD-06 — SAVE/publication evidence/publication currentness

Direct: `R045`, `R069`, `R070`, `R071`.

`R071`: **mixed current repair + proof**.

Boundary: publication attempt/result/currentness evidence remains WP-13-owned. Execution supplies inputs but does not own publication evidence/currentness. R071 implementation-bearing stale-surface reconciliation lives here; its proof remains target-relative.

Joins RD-04 owner/index closure and RD-05 accepted execution inputs. RD-07 consumes confirmed current/native publication state. RD-14 consumes confirmed save result.

Protected: accepted execution and accepted publication remain distinct; no blind retry, force, alternate transport, generic merge, fictional chronology, or global publication frontier.

### RD-07 — current-native recovery/checkpoint alignment

Direct: `R011`, `R012`, `R072`, `R073`, `R074`.

Boundary: checkpoint schema/template alignment and recovery behavior are one recovery-owner checkpoint, eliminating the former generic-schema/runtime split.

Joins RD-04 owner-native storage support, RD-06 current publication state, and RD-09 selected LIVE state when applicable.

Protected: no checkpoint authority, guessed latest, copied current state, RecoveryCut/global frontier, replay, or reroll.

### RD-08 — temporal/thread/current-state realization

Direct: `R010`, `R075`, `R076`, `R077`.

Composite: `R006.THREAD_VISIBILITY`, `R016.TEMPORAL`, `R018.TEMPORAL`, `R062.TEMPORAL`.

`R077`: **implementation + proof**.

Boundary: current-state chronology cleanup, thread machine shape, typed temporal enrollment/Agenda/occurrence behavior, and chronology-provider representation change together. The stale global `world_time.frontier` is not a generic schema-only repair.

`R075 HARD_PRECEDES R076` remains internal.

Protected: no campaign-global clock/frontier, generic scheduler/global firing ledger, chronology from CURRENT/IDs/transport order, or thread-visibility-to-PC-knowledge inference.

### RD-09 — principal authorization/LIVE identity/currentness

Direct: `R013`, `R014`, `R019`, `R020`, `R078`, `R079`, `R080`, `R122`.

Composite: `R053.LIVE`, `R016.LIVE`, `R018.LIVE`, `R062.LIVE`.

`R080`: **implementation + proof**.

Boundary: LIVE/message source-native identity, exact-source fencing, claim grammar, lifecycle transitions, principal binding, revocation, and split-party currentness move with LIVE/access machine projections.

Joins RD-07 recovery, RD-12 collaboration current-generation checks, and RD-14 creator fail-closed consumer.

Protected: no login/repository-permission substitution, wildcard claim, global LIVE mega-owner, rekey, branch deletion, transport-order chronology, or global split-party synchronization.

### RD-10 — role containment/typed handoff/protected emission

Direct: `R054..R057`.

Semantically unchanged from original `CD-09`; all original invariants remain.

### RD-11 — bounded Context Runtime

Direct: `R059`, `R060`, `R097`, `R105..R107`, `R117`, `R119`, `R120`, `R124`, `R125`, `R127`, `R134`, `R135`, `R138`, `R140`, `R144`, `R145`.

Semantically unchanged from original `CD-10`; all original invariants remain. RD-14 may consume ordinary retrospective context where required.

### RD-12 — collaboration/multiplayer lifecycle

Direct: `R021`, `R044`, `R081`, `R082`, `R083`, `R121`, `R123`, `R141..R143`, `R146`.

Composite: `R016.COLLAB`, `R018.COLLAB` where an admitted collaboration family requires machine shape/root realization.

`R083`: **implementation + proof**.

Boundary: one WP-17 collaboration lifecycle owner covers obligation/generation/input/currentness state and remaining R083 machine debt. R044 is re-homed here from execution.

Joins RD-09 authorization/currentness, RD-10 recipient containment, and RD-05 only at deterministic mechanics integration.

Protected: no transcript coordinator, generic queue/broker, arrival-order authority, timeout/debounce correctness, universal active-player gate, or private-input disclosure.

### RD-13 — Story/T0/Commentator/retained Dramaturg projections

Direct: `R022`, `R051`, `R084`, `R085`, `R099`, `R102`, `R131`.

Composite: `R016.STORY`, `R018.STORY` where Story owner contracts require schema/root realization.

Boundary: Story-family projection debt formerly hidden in broad `CD-02` moves into the Story consumer checkpoint. All original `CD-12` non-authority laws remain.

Joins native history/event inputs from RD-03/RD-05 as applicable, recipient/currentness constraints from RD-09/RD-10, and retained multiplayer Dramaturg from RD-12.

### RD-14 — bootstrap/onboarding/product consumers

Direct: `R086`, `R087`, `R098`, `R100`.

Boundary: bootstrap/current-package/session/menu consumers. R100 moves beside R086; RD-09 retains access ownership.

```text
RD-09:R078 + RD-14:R086
  JOIN_BEFORE_INTEGRATION
RD-14:R100
```

RD-06 supplies confirmed save result to R098; RD-11 supplies retrospective context where required. There is no reverse RD-14 -> RD-09 ownership edge and no unit-level cycle.

Protected: creator identity remains fail-closed; no creator-rename inference, stable-ID authority transfer, premature session clear, or inferred campaign lifecycle transition.

## 4. Composite readiness slices

Planning-only slices reconcile to the canonical parent leaf.

```text
R006.INFO              -> RD-02
R006.ACTOR             -> RD-03
R006.THREAD_VISIBILITY -> RD-08

R016.INFO     -> RD-02
R016.ACTOR    -> RD-03
R016.TEMPORAL -> RD-08
R016.LIVE     -> RD-09
R016.COLLAB   -> RD-12
R016.STORY    -> RD-13

R018.INFO     -> RD-02
R018.ACTOR    -> RD-03
R018.TEMPORAL -> RD-08
R018.LIVE     -> RD-09
R018.COLLAB   -> RD-12
R018.STORY    -> RD-13

R053.INFO -> RD-02
R053.LIVE -> RD-09

R062.INFO          -> RD-02
R062.ACTOR_HISTORY -> RD-03
R062.TEMPORAL      -> RD-08
R062.LIVE          -> RD-09
```

RD-04 joins owner-local R018 results for route/body/load integration and never becomes their semantic owner. No allocation matrix becomes a runtime registry/service.

## 5. Exact former CD-14 classification

The rejected `CD-14` is removed as an implementation unit.

| Readiness | Classification | Route |
|---|---|---|
| R023 | PURE PROOF | applicable owner-family targets |
| R031 | PURE PROOF | RD-03 |
| R032 | PURE PROOF | RD-03 |
| R041 | PURE PROOF | RD-05 plus exact implicated recovery/storage consumers |
| R058 | PURE PROOF | RD-10/RD-11 |
| R061 | PURE PROOF | RD-11 |
| R068 | PURE PROOF | RD-04/RD-07 |
| R071 | MIXED REPAIR + PROOF | RD-06 |
| R077 | IMPLEMENTATION + PROOF | RD-08 |
| R080 | IMPLEMENTATION + PROOF | RD-09 |
| R083 | IMPLEMENTATION + PROOF | RD-12 |
| R088 | PURE INTEGRATED PROOF | applicable realized targets |
| R089 | PURE PROOF-CHANNEL ROUTE | channel-specific evidence boundaries |

No separate proof implementation checkpoint or late serial test phase exists.

## 6. Exact canonical coverage

```text
DIRECT_UNIT_COVERAGE:   119
PURE_PROOF_ROUTES:        9
COMPOSITE_OWNER_ROUTES:   5
TOTAL:                  133 / 133
```

```text
RD-01  7 : R001 R003 R033 R043 R047 R048 R050
RD-02  6 : R007 R008 R009 R017 R049 R052
RD-03 22 : R025-R030 R104 R108-R111 R113-R116 R126 R128-R130 R132 R136 R139
RD-04  6 : R015 R063-R067
RD-05 13 : R034-R040 R042 R046 R112 R118 R133 R137
RD-06  4 : R045 R069 R070 R071
RD-07  5 : R011 R012 R072 R073 R074
RD-08  4 : R010 R075 R076 R077
RD-09  8 : R013 R014 R019 R020 R078 R079 R080 R122
RD-10  4 : R054-R057
RD-11 18 : R059 R060 R097 R105-R107 R117 R119 R120 R124 R125 R127 R134 R135 R138 R140 R144 R145
RD-12 11 : R021 R044 R081 R082 R083 R121 R123 R141-R143 R146
RD-13  7 : R022 R051 R084 R085 R099 R102 R131
RD-14  4 : R086 R087 R098 R100
```

Pure proof: `R023`, `R031`, `R032`, `R041`, `R058`, `R061`, `R068`, `R088`, `R089`.

Composite: `R006`, `R016`, `R018`, `R053`, `R062`.

## 7. Repaired dependency/join graph

Edges are integration joins, not blanket coding order.

```text
RD-01 is an independent projection-repair root.

RD-02/RD-03/RD-08/RD-09/RD-12/RD-13
  -> RD-04 route/body/load joins where applicable.

RD-03 + RD-04 + RD-05 -> integrated Actor/execution acceptance where mechanics mutate Actor state.
RD-04 + RD-05 -> RD-06 SAVE/publication integration.
RD-04 + RD-06 + RD-09 -> RD-07 current-native recovery integration.
RD-05 + RD-07 + RD-09 -> RD-08 temporal/recovery/currentness acceptance where applicable.
RD-09 + RD-12 -> recipient/current-generation collaboration acceptance.
RD-10 + RD-11 -> bounded role-context assembly/containment acceptance.
RD-09 + RD-10 + RD-12 -> RD-13 recipient-safe Story/Dramaturg integration as applicable.
RD-06 + RD-09 + RD-11 -> RD-14 product consumers as applicable.
RD-09:R078 + RD-14:R086 -> RD-14:R100.
```

Stable accepted interfaces may be implemented in parallel. No broad schema/catalog predecessor exists and no repaired edge requires a unit-level cycle.

## 8. Derived P3 corrections

The original P3 stays intact as provenance; only these lossy derived classifications are superseded.

- `R077`: `R075 HARD_PRECEDES R076` remains, but R077 contains implementation-bearing temporal/current/schema work under RD-08 followed by attached proof.
- `R080`: not merely integrated proof; LIVE runtime/schema/catalog duties belong to RD-09 followed by attached proof.
- `R083`: any proof-spine wording treating it as proof-only is superseded; R083 has collaboration machine debt plus proof under RD-12.
- `R071`: P3 already preserved mixed stale-surface reconciliation plus proof; the decomposition now places the implementation portion explicitly under RD-06.
- P3 E15 remains valid only with the item-level classification in §5: pure proof follows realized targets; mixed leaves realize owner-scoped implementation first, then attached proof.

## 9. DC-001..DC-005 closure map

**DC-001:** rejected CD-02 is dissolved as an implementation foundation. Responsibilities are redistributed into RD-02/RD-03/RD-04/RD-07/RD-08/RD-09/RD-12/RD-13 by owner/consumer/version checkpoint. Composite leaves are explicit. No blanket schema-to-runtime predecessor remains.

**DC-002:** rejected CD-14 is removed as an implementation unit. All 13 leaves are classified item-by-item. R071/R077/R080/R083 retain implementation-bearing work; nine leaves are pure proof routes. P3 classifications for R077/R080/R083 are repaired.

**DC-003:** R044 moves from execution to RD-12 collaboration. RD-05 keeps only the typed mechanics join.

**DC-004:** R045 moves from execution to RD-06 publication/currentness. RD-05 supplies inputs only.

**DC-005:** R100 moves to RD-14 beside R086; RD-09 supplies R078. The direct `R078 + R086 -> R100` join is acyclic.

## 10. Preliminary Impact Envelope/checkpoint matrix

| Unit | Owner/change family | Coherence boundary | Protected non-goal |
|---|---|---|---|
| RD-01 | instructions/current projections | install/CORE readers | no runtime authority |
| RD-02 | information families | schemas/roots + direct consumers | no generic state service |
| RD-03 | Actor/Asset/Effect + continuity/history | family projections + runtime consumers | no generic memory/NPC simulation |
| RD-04 | routing/index/HOT | owner integration only | no index/cache authority |
| RD-05 | deterministic execution | execution distinct from publication | no replay/global failure owner |
| RD-06 | SAVE/publication/currentness | publication evidence/currentness under WP-13 | no force/fallback/global frontier |
| RD-07 | recovery/checkpoints | checkpoint shape + recovery consumer | no checkpoint authority/guessed latest |
| RD-08 | temporal/thread/current-state | temporal projection + temporal consumer | no global clock/scheduler |
| RD-09 | access/LIVE | identity/currentness/authorization projection + consumer | no login substitution/global ACL |
| RD-10 | role containment/emission | ephemeral role boundary | no durable role memory/bus |
| RD-11 | Context Runtime | ephemeral context consumers | no durable context owner |
| RD-12 | collaboration | schema + lifecycle/current-generation | no queue/broker/coordinator |
| RD-13 | Story/T0/Commentator/Dramaturg | noncanonical projection + consumer | no Story canon/ACL |
| RD-14 | bootstrap/session/menu | product-consumer integration | no inferred campaign lifecycle transition |

Every later detailed plan still executes the per-task Version Impact Gate. This repair preselects no version bump or migration. Clean-slate/prerelease status does not waive projection synchronization.

## 11. HG-01 constraints preserved

1. Voluntary NPC/faction reasoning remains under Actor/NPC owners; multiplayer currentness/agency applies to actual human participants.
2. Ordinary within-location micro-position and transient attention/facing/distraction/reaction remain fiction unless an admitted mechanic/native owner requires typed state.
3. Missing exact realization evidence remains a lookup/realization question, not automatic evidence for new architecture.
4. Mechanically-null bounded adjudication remains valid; no generic prose-to-StateDelta, workflow, or arbitrary consequence bridge is introduced.

## 12. Independent re-review contract

The next critic must review **original P3 + original candidate + this repair overlay**, after fresh bootstrap and independent owner-graph reconstruction.

Mandatory retests:

- every former CD-02 leaf against repaired owner/consumer/version checkpoints;
- all 13 former CD-14 leaves against §5;
- every composite slice against its canonical parent;
- R044 ownership between RD-05/RD-12;
- R045 ownership between RD-05/RD-06;
- direct acyclic `R078 + R086 -> R100` routing;
- repaired joins and Impact Envelope feasibility;
- all 12 trigger-gated and 79 no-work dispositions;
- HG-01 guardrails;
- whether any unit still forces detailed-plan authors to rediscover architecture.

The independent critic retains full authority to reject this repaired cut again.

```text
REPAIRED_ACTIVE_READINESS_ACCOUNTED: 133 / 133
TRIGGER_GATED_PRESERVED: 12 / 12
NO_WORK_PRESERVED: 79 / 79
R27_R004: ABSENT
DC001_REPAIR_PROPOSED: YES
DC002_REPAIR_PROPOSED: YES
DC003_REPAIR_PROPOSED: YES
DC004_REPAIR_PROPOSED: YES
DC005_REPAIR_PROPOSED: YES
DECOMPOSITION_CRITIC_RE_REVIEW_REQUIRED: YES
DETAILED_EXECUTABLE_PLAN_AUTHORING_AUTHORIZED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
VERSION_IMPACT: NONE
MIGRATION_REQUIRED: NO
```

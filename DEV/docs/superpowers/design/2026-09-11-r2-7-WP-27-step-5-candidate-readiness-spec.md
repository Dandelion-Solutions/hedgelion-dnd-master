# R2.7 WP-27 Step 5 — Candidate Implementation-Planning Readiness Specification

Status: **COMPLETE — RUN A CANDIDATE PUBLISHED / STEP 6 NOT STARTED**

Date: 2026-09-11

Controlling Run-A task and plan:

- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-steps-3-5-task.md`;
- `DEV/docs/superpowers/plans/2026-09-11-r2-7-WP-27-steps-3-8-audit-execution-plan.md`.

Immediate predecessor checkpoints:

- Step 3: `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-3-decision-brief.md`, checkpoint `322b44133024fc754ecb0087aba5a5dbf0333f5a`;
- Step 4: `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-4-review-disposition.md`, checkpoint `75faeeca3e65724581025715f63a673c7b5762ba`.

Admitted evidence authority remains the independently closed Step-2 package, especially:

- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md`;
- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-execution-amendment.md`;
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-2-independent-audit.md`.

This document is a **candidate planning-readiness specification**, not implementation authorization, implementation planning, implementation, migration execution, release execution, or gameplay bootstrap. It adds a planning composition over accepted Step-2 leaves; it does not supersede the native architecture owners referenced by those leaves.

---

# A. Scope

WP-27 must answer whether HDM is architecturally ready to enter implementation planning after the mandatory R2.7 final reconciliation. This candidate converts the closed Step-2 evidence into an inspectable planning-ready shape without altering architecture.

The candidate preserves these Step-2 closure facts:

```text
SOURCE_ITEMS: 224 / 224
READINESS_RECORDS: 145 / 145
  R27-R001..R27-R003 + R27-R005..R27-R146
  R27-R004: REMOVED / MUST NOT REAPPEAR
EXPLICIT_NO_WORK_TERMINALS: 79 / 79
PO001_010: 10 / 10
ROUND2_DIAMOND_STRONG: 82 / 82
ROUND2_DELTAS: S14 / S53 / D15 reconciled
MACHINE_RESPONSIBILITIES: 59 / 59
MACHINE_RECORDS: R27-M01..R27-M19
MACHINE_EXCEPTION_RECORDS: R27-X01..R27-X14
MACHINE_EXCEPTION_MEMBERS: 31 / 31
HIGH_RISK_PROBES: R27-P01..R27-P08 = 8 / 8 PASS
ARCHITECTURE_BLOCKER_CANDIDATES: []
```

Hard scope boundaries:

- accepted owner semantics are not reopened;
- no dormant/deferred item is activated merely because it appears in this candidate;
- no release-time obligation is treated as current implementation work;
- no pre-release migration debt is manufactured;
- no global readiness, migration, partition, failure, health, routing, scheduling, retry, replay, collaboration or memory authority is introduced;
- Step 6 is not performed by this document.

The mandatory R2.7 final reconciliation remains between WP-27 closure and implementation planning. Therefore `PLANNING_READY_CANDIDATE` does not mean `IMPLEMENTATION_PLANNING_AUTHORIZED`.

---

# B. Workstream decomposition with lossless traceability to Step-2 IDs

## B.1 Composition law

A candidate workstream is a planning container only. It does not own the semantics of its members. Every member retains its Step-2 source item, accepted owner refs, destination family, activation state, future Version Impact/migration consequence, proof channels, defer/revisit trigger, implementation-selectable choices and negative laws.

If later planning cannot preserve a member's distinct owner/activation/proof/negative law inside its assigned workstream, that workstream must be split. The readiness leaf must never be weakened to keep a convenient grouping.

## B.2 Exact 145-record partition

The following memberships are disjoint and their union is exactly the repaired Step-2 readiness set. This is the candidate's reverse map to Step 2.

### `WS27-01` — supported host, transport, package and release projection

**Exact readiness membership:**

`R27-R001`, `R27-R002`, `R27-R003`, `R27-R005`, `R27-R024`, `R27-R091`, `R27-R092`.

**Native owner families:** R2.6 supported-host/Connector boundary; WP-13 fixed transport where applicable; WP-23 package/release; versioning owner.

**Implementation destinations:** shipped install/bootstrap instructions, fixed Connector wording, package/build/version projections, and later release acceptance route.

**Activation split:** `R001/R003` are active install/instruction realization; `R005` waits for the real implemented MVP; `R002/R024/R091/R092` are release-candidate/release-execution obligations only.

### `WS27-02` — authority/schema/catalog convergence

**Exact readiness membership:** `R27-R006..R27-R023`.

**Native owner families:** Step-4 truth/knowledge/disclosure; WP-07 current record decisions; WP-10/11 allocation/routing; Step-5 recovery/currentness; WP-15/16/17 where referenced by the individual leaf.

**Implementation destinations:** retire duplicate legacy epistemic/Secret/lore/global-frontier/recovery/currentness shortcuts, materialize accepted native record families/IDs/routes, and retain proof/catalog validation without creating parallel owners.

**Activation:** active schema/record/topology realization except where an individual leaf is proof-only or target-realization dependent; exact leaf activation remains controlling.

### `WS27-03` — Actor/entity execution, lifecycle, rules and projection alignment

**Exact readiness membership:** `R27-R025..R27-R054`.

**Native owner families:** Actor/Asset/Effect model; Step-3 execution; Step-4 information separation; WP-10..17 native record/runtime owners; WP-19 lifecycle/bootstrap; S6D/domain package owners; WP-26 current routing repairs.

**Implementation destinations:** unified Actor/Asset/Effect schemas/routes, HOT-local atomic execution support, provisional/READY_PC lifecycle, execution-owner materialization, fixed-RNG recovery retention, bounded collaboration hooks, diagnostics, lore/knowledge/disclosure/Story scaffolding and the identified stale CORE/architecture prose repairs.

**Activation:** mostly authorized future realization after implementation-planning authorization; current stale-document/projection repairs remain distinguishable from runtime realization and do not themselves prove runtime behavior.

### `WS27-04` — role containment and Context Runtime

**Exact readiness membership:** `R27-R055..R27-R061`.

**Native owner families:** WP-08 role-context/LLM containment; WP-09 Context Runtime; R2.3/R2.4/R2.6; WP-22 proof separation.

**Implementation destinations:** one behavior-equivalent containment instruction owner, ephemeral typed role/context controls, typed handoffs and protected emission, bounded discovery/assembly, conservative allocation/degradation and their finite assurance cases.

**Activation:** runtime/instruction realization first; supported-target/Protocol-4 behavior only after the real target exists.

### `WS27-05` — native state topology, persistence, recovery, temporal currentness and LIVE authority

**Exact readiness membership:** `R27-R062..R27-R080`.

**Native owner families:** WP-10 allocation; WP-11 routes/indexes; WP-12 HOT; WP-13 persistence/publication; WP-14 recovery; WP-15 temporal/process; WP-16 access/LIVE; associated Step-5 owners.

**Implementation destinations:** native record family materialization, deterministic routes and non-authoritative indexes, HOT owner envelopes/transactions, SAVE/publication/currentness machinery, cold recovery/maintenance, typed temporal enrollment and chronology providers, principal binding and LIVE exact-source CAS/currentness.

**Activation:** active future implementation realization; measurement branches remain separately trigger-gated. No cross-owner database, global frontier, registry, distributed transaction, scheduler or replay authority follows from this grouping.

### `WS27-06` — collaboration, Story and retained Dramaturg planning surfaces

**Exact readiness membership:** `R27-R081..R27-R085`.

**Native owner families:** WP-17 collaboration; WP-18 Story/Dramaturg; WP-11/13/16/24 and PO-009 where each leaf names them.

**Implementation destinations:** only admitted collective obligation/generation/input routing; collaboration lifecycle/currentness; noncanonical Story projection units/state; and fixed multiplayer shared/player-local Dramaturg horizons.

**Activation:** collaboration only for owner-proven durable collective dependency/applicable multiplayer; Story realization when implementation is authorized; single-player Dramaturg planning remains ephemeral unless its accepted trigger changes.

### `WS27-07` — bootstrap/product consumers and proof-channel integration

**Exact readiness membership:** `R27-R086..R27-R090`.

**Native owner families:** WP-19 bootstrap/product-use decisions; WP-22 proof matrix; associated native persistence/context/disclosure owners.

**Implementation destinations:** package selection/scaffold/lifecycle consumers; retrospective/save-and-exit/T0 consumer seams; owner-first proof mapping and Protocol-4 scenario route.

**Activation:** implementation realization for bootstrap/product consumers; Protocol-4 execution only after the real MVP. `R088..R090` do not create an independent runtime subsystem.

### `WS27-08` — writer growth and focus-scoped failure/host-risk branches

**Exact readiness membership:** `R27-R093..R27-R096`.

**Native owner families:** WP-24 + PO-010 writer-sizing policy; WP-25 + PO-008 failure/degradation policy; native writer/durability/publication owners.

**Implementation destinations:** projected serialized UTF-8 measurement, review-band decision, owner-valid partition/rollover when activated, and one bounded DANGER preservation/recovery attempt plus state-growing-operation guard when required.

**Activation:** strictly writer/focus/measurement triggered. This workstream does not activate a global partition project or a generic failure/health/retry/scheduler system.

### `WS27-09` — direct accepted Product Owner consumer integration

**Exact readiness membership:** `R27-R097..R27-R103`.

These are the active/readiness-routed PO records:

- `R097 -> PO001-01` ordinary-Master bounded retrospective;
- `R098 -> PO002-01` save-and-exit then session-local clear/menu return;
- `R099 -> PO003-01` qualifying event-time T0 Actor decision basis;
- `R100 -> PO005-01` creator-login fail-closed continuity;
- `R101 -> PO008-01` owner-local failure/degradation direction;
- `R102 -> PO009-01` Story-local T0/control Commentator consumer;
- `R103 -> PO010-01` writer-specific sizing/growth policy.

**Native owner families:** each accepted PO owner decision plus its named native Story/history/access/disclosure/persistence/bootstrap/failure/writer owners.

**Implementation destinations:** only the consumers named by each PO record; no new product-wide authority is created.

**Activation:** realization remains deferred until R2.7 final reconciliation plus later approved implementation planning/execution, except owner policies that already constrain all future consumers.

### `WS27-10` — active Round-2 DIAMOND continuity

**Exact readiness membership:** `R27-R104..R27-R124`.

**Native owner families:** the accepted R2.1..R2.5 and Step owner routes recorded individually by the corresponding DIAMOND leaves.

**Implementation destinations:** native continuity/history, Context Runtime, Actor, role/execution, collaboration and multiplayer realization where the individual D-record remains active. No second memory/context/canon/coordination owner is introduced.

**Activation:** exact per-leaf active realization. Dormant/no-work DIAMOND records are not in this range because they remain in §G's no-work set.

### `WS27-11` — active Round-2 STRONG continuity

**Exact readiness membership:** `R27-R125..R27-R146`.

**Native owner families:** accepted R2.1..R2.5/R2.6-7 and Step owner routes recorded individually by the corresponding STRONG leaves.

**Implementation destinations:** bounded retrieval/ranking, continuity promotion, Actor cognition/lifecycle, role/runtime containment, multiplayer channel/catch-up/currentness and related owner-local realization. `S14 -> R27-R131` is retained here with its accepted narrow multiplayer Dramaturg representation.

**Activation:** exact per-leaf active realization. Dormant/rejected/already-realized STRONG records remain no-work terminals and are not resurrected.

## B.3 Partition accounting

```text
WS27-01:   7 records
WS27-02:  18 records
WS27-03:  30 records
WS27-04:   7 records
WS27-05:  19 records
WS27-06:   5 records
WS27-07:   5 records
WS27-08:   4 records
WS27-09:   7 records
WS27-10:  21 records
WS27-11:  22 records
TOTAL:   145 records

UNION:
  R27-R001..R27-R003
  + R27-R005..R27-R146
MISSING: []
DUPLICATED: []
R27-R004_PRESENT: NO
```

The workstream IDs are candidate planning labels only. The Step-2 `R27-R###` records remain the lossless obligation leaves.

---

# C. Dependency DAG / dependency order

There is no universal implementation sequence. The planning DAG preserves owner-local prerequisites and conditional branches.

## C.1 Universal per-leaf proof/realization order

For every activated leaf:

```text
accepted semantic/product owner
  -> owner-local schema / route / template / validator if required
  -> owner-local producer / consumer / runtime behavior
  -> deterministic contract/TDD proof
  -> scenario/adversarial acceptance
  -> supported-target empirical/Protocol-4 proof if required
  -> release-time exact-asset/fresh-Project proof only if release-candidate work applies
```

No proof node creates semantics, and a later proof class cannot be substituted by an earlier one.

## C.2 Cross-workstream prerequisite edges

```text
WS27-02 + relevant WS27-03 + WS27-05 native family/route realization
  -> dependent WS27-06 Story/collaboration surfaces
  -> dependent WS27-09 PO consumers

WS27-04 role/context realization
  -> context-dependent members of WS27-07, WS27-09, WS27-10, WS27-11
  -> R27-R058/R061/R088..R090 assurance routes

R27-R099 (PO-003 T0 native basis, WS27-09)
  -> R27-R102 (PO-009 Story-local T0/control consumer, WS27-09)
  -> R27-R084 (Story producer/layer realization, WS27-06)
  -> R27-R093/R094/R095 and R27-R103 only if that concrete writer's size trigger fires

R27-R086/R087 bootstrap/product consumers (WS27-07)
  -> R27-R091/R092 release gates (WS27-01) only when release execution is authorized

owner-local writer realization
  -> WS27-08 growth branch only when projected-size/measurement trigger fires

owner-local failure/durability realization
  -> R27-R096/R101 focus-scoped branch only when owner-valid exposed-risk trigger applies
```

Independent workstreams or leaf subsets without a path between them may be planned/executed independently after the later authorization gate.

## C.3 Conditional migration branch

The migration branch remains dormant now:

```text
qualifying released-v1.0+ source/target compatibility obligation
  -> activate WP20-01..WP20-04 from their current NO_WORK_DEFERRED state
  -> classify the concrete owner/schema/generation compatibility delta
  -> declare directed compatibility/migration edge only if required
  -> realize owner-local transform/update
  -> deterministic + scenario proof
  -> existing publication/currentness proof
```

No qualifying release source/target is established by this candidate, so no migration node is activated.

---

# D. Owner, implementation destination and activation/defer state

The workstream descriptions in §B provide the primary owner families, destination families and activation categories. The following laws apply to all of them:

1. **Leaf owner wins.** If a workstream summary is less specific than its member `source_owner_refs[]`, the Step-2 leaf controls.
2. **Destination is not authority.** A schema path, SQLite table, Story file, LIVE record, index, workflow or test is a consumer/projection unless the accepted owner explicitly says otherwise.
3. **Activation is leaf-local.** A workstream containing active, empirical-later and release-later leaves does not activate them together.
4. **No-work is outside the active workstream partition.** Section G preserves all 79 no-work terminals separately.
5. **Already-realized support is not reimplementation debt.** `R27-M*` support surfaces stay support unless a linked readiness leaf identifies concrete current work.
6. **Dormancy is evidence.** A dormant trigger is a terminal current disposition, not a hidden backlog item.

Implementation planning must therefore carry the exact `R27-R###` membership next to every concrete task/phase it derives. A task may satisfy several readiness leaves, but it must state all of them; it may not create an untraceable umbrella task.

---

# E. Version Impact and migration consequences

## E.1 Current candidate-document impact

```text
VERSION_IMPACT: NONE
```

Reason: Step 5 adds audit/planning-readiness documentation only. It changes no semantic, runtime, schema, catalog, protocol, persistence, package, compatibility or version metadata owner.

## E.2 Future implementation rule

All 145 readiness leaves retain their Step-2 `FUTURE_VERSION_IMPACT_GATE`. No engine/module/schema/generation/catalog/ruleset/package/protocol/digest bump is selected here.

For every later implementation checkpoint:

1. identify the exact changed owner/consumer set from its readiness leaves;
2. run the current versioning owner against the actual file/contract delta;
3. update only the affected version namespace(s) and all required projections coherently;
4. determine compatibility/migration consequence from the concrete delta, not number order;
5. do not infer campaign migration from an engine-version change alone;
6. do not create concrete `GAME/MIGRATIONS` transforms until WP-20's released-source/target trigger is actually satisfied.

Representation-sensitive leaves include at least Story/T0/control (`R099/R102/R084`), writer-specific growth (`R093..R095/R103`), native persistent families (`R006..R022/R062..R080`) and bootstrap/product persistent consumers (`R086/R087`). A selected persistent/interface shape must pass its future gate before the corresponding implementation checkpoint can close.

---

# F. Deterministic, scenario, empirical and release proof obligations

Proof obligations remain leaf-local; the workstreams provide planning containers only.

## F.1 Deterministic TDD / contract / integration

Required for every realized behavior/shape named by the leaf's `test_first_obligations[]`.

Representative workstream expectations:

- `WS27-01`: install-contract parity, fixed-Connector negative checks, builder/version/package parity;
- `WS27-02`: schema/authority negatives, recipient isolation, identity/currentness and no-duplicate-owner tests;
- `WS27-03`: Actor/Asset/Effect route/identity/lifecycle, local atomic execution, fixed RNG recovery, stale-projection guards;
- `WS27-04`: role eligibility, rebind, bounded allocation/degradation and safe emission;
- `WS27-05`: route/index, HOT transaction, SAVE/publication/recovery, temporal and LIVE CAS/currentness suites;
- `WS27-06`: collaboration generation/currentness/agency, Story no-authority/currentness and Dramaturg horizon isolation;
- `WS27-07`: bootstrap/product direct cases plus owner-first proof mapping;
- `WS27-08`: exact UTF-8 projected-size/review/rollover and bounded DANGER-attempt behavior;
- `WS27-09`: direct PO acceptance cases, including T0/T1 historical explanation, save-and-exit, creator fail-closed, Story-local control and writer-size rules;
- `WS27-10/11`: exact per-D/S leaf deterministic obligations remain controlling.

## F.2 Scenario/adversarial acceptance

Scenario evidence must exercise the realized behavior and its negative/failure/indeterminate cases. It is not replaced by unit/schema/static tests. `R27-R058`, `R061`, `R088..R090` remain explicit assurance/proof leaves.

## F.3 Supported-target / Protocol-4 empirical acceptance

Empirical work remains deferred until a real implemented supported target where the leaf requires it. The Step-2 set explicitly includes such routes in `R005`, `R055..R061`, `R087`, `R090`, `R096`, `R101`, `R103` and other individual leaves that name a real-target measurement.

A fixture, scenario catalog, maintenance audit or green source CI run does not count as execution of Protocol-4 or real-host measurement.

## F.4 Release-time exact-asset / fresh-Project acceptance

For an authorized release candidate, the release route remains:

```text
pre-tag fresh-Project candidate acceptance
  -> immutable tag/publication
  -> exact uploaded-asset identity/provenance verification
  -> post-upload fresh-Project acceptance
  -> announcement
```

`R002`, `R024`, `R086`, `R091`, `R092` retain the release-facing consequences. No earlier node proves a later node.

---

# G. Defer/revisit triggers and rejected architecture

## G.1 Exact 79 no-work terminals

The following source records remain outside current implementation work exactly as closed by Step 2:

```text
WP01-F04, WP01-F05, WP02-M05, WP03-F01, WP03-F02, WP03-F09, WP03-F12,
WP04-F01, WP05-F01, WP05-F10, WP07-N02, WP09-04, WP10-02, WP10-04,
WP10-05, WP18-03, WP18-04, WP19-03, WP20-01, WP20-02, WP20-03, WP20-04,
WP21-01, WP21-02, WP21-03, WP22-04, WP23-03, WP24-01, WP24-05,
WP25-01, WP25-02, WP25-03, WP25-05, WP26-01, WP26-02, WP26-03, WP26-04,
PO004-01, PO006-01, PO007-01, D15, D17, D20, S01, S05, S06, S08, S09,
S12, S13, S15, S16, S17, S18, S20, S23, S24, S26, S30, S31, S32, S33,
S34, S35, S37, S38, S39, S41, S42, S46, S47, S50, S51, S52, S53, S55,
S56, S57, S58
```

```text
NO_WORK_TERMINAL_COUNT: 79 / 79
NO_WORK_RECORD_ACTIVATED_BY_STEP5: 0
```

Their exact source-local dispositions/triggers remain owned by Step-2 §10.2/source records. Important cross-cutting trigger classes remain:

- released-compatibility only: WP20-01..04, PO004-01 and migration support;
- measurement dormant: WP24-01/WP24-05/S39/D15 and associated measured branches;
- extension/auxiliary/spatial/index/cache features only on their explicit consumer/measurement trigger;
- conditional collaboration/planning only on owner-proven multiplayer/collective need;
- already-realized closed repairs remain closed, including `WP01-F05`; `R27-R004` must not be recreated.

## G.2 Rejected/non-authoritative architecture that must remain rejected

Implementation planning must not revive any of the following merely to simplify sequencing:

- one generic memory blob or Story-as-canon/history authority;
- global context/memory bus or durable Context Runtime authority;
- global fictional chronology/currentness frontier;
- global migration registry or pre-release transform project;
- universal partition/sharding service, 10240-byte hard rejection, truncation or semantic shard identity;
- persisted global failure/health registry, generic ACL, retry/replay service, queue, scheduler or heartbeat;
- global ID registry/service where native identity owners already control identity;
- generic collaboration authority, transcript coordinator, global safe frontier or universal active-player gate;
- durable single-player Dramaturg planning, global plot graph/index/scheduler;
- checkpoint-first recovery, SQLite-as-canon, index-as-authority or path-derived identity/currentness;
- alternate gameplay Git transport probing/fallback;
- current source CI/maintenance audit as semantic, empirical or release authority.

---

# H. PO and 82-item Round-2 continuity

## H.1 Product Owner ledger continuity

All ten Product Owner inputs retain explicit terminal routes:

```text
PO001-01 -> R27-R097
PO002-01 -> R27-R098
PO003-01 -> R27-R099
PO004-01 -> NO_WORK_DEFERRED / released-compatibility trigger only
PO005-01 -> R27-R100
PO006-01 -> explicit Step-2 no-work terminal
PO007-01 -> explicit Step-2 no-work terminal; public-provenance boundary remains owner-fixed
PO008-01 -> R27-R101
PO009-01 -> R27-R102
PO010-01 -> R27-R103
```

`PO001_010_ACCOUNTED: 10 / 10`.

No PO disposition is converted by Step 5 from no-work/dormant to active work.

## H.2 Round-2 continuity

The exact Round-2 set remains `D01..D24` plus `S01..S58`, 82/82 exactly once in Step-2 evidence. Candidate planning preserves the Step-2 split:

- active/readiness-routed DIAMOND members compose into `WS27-10` (`R104..R124`);
- active/readiness-routed STRONG members compose into `WS27-11` (`R125..R146`);
- D/S records with explicit no-work terminals remain in §G and are not reactivated.

Mandatory changed dispositions remain:

```text
S14 -> R27-R131 — active narrow multiplayer Dramaturg representation
S53 -> NO_WORK_ALREADY_REALIZED
D15 -> NO_WORK_DEFERRED / measurement-dormant trigger
```

No weaker pre-Round-2 default is restored.

---

# I. Machine reverse-conformance continuity

## I.1 Complete admitted machine set

The candidate preserves the Step-2 reverse-conformance result without reclassifying it:

```text
R27-M01..R27-M19: 19 / 19 machine records
MATERIAL_RESPONSIBILITIES: 59 / 59 classified
R27-X01..R27-X14: 14 / 14 exception records
EXCEPTION_MEMBERS: 31 / 31 classified
UNOWNED_OR_UNCLASSIFIED: []
MIXED_GROUPS_WITHOUT_BREAKDOWN: []
FALSE_AUTHORITY_PROMOTIONS: 0
```

Machine-family continuity:

- `GAME/CORE`, `GAME/SCHEMA`, `GAME/CAMPAIGN`, `GAME/TEMPLATE`, `GAME/INSTALL`, `GAME/RULES`, `GAME/MIGRATIONS`, `GAME/TOOLS`, `GAME/ENGINE_VERSION.yaml` retain their bounded consumer/support/deferred roles;
- `DEV/ARCHITECTURE`, `DEV/CATALOG`, `DEV/SCHEMAS`, `DEV/TESTS`, `DEV/TOOLS`, `DEV/RELEASE`, `.github/workflows`, `DEV/ENGINE_DEVELOPMENT.yaml` and legal/release payload retain their owner/support/verification roles;
- paired GAME/DEV version projection remains support, not compatibility/release proof.

## I.2 Exception continuity

The fourteen mixed/stale exceptions remain explicitly routed:

```text
X01 fixed-Connector wording -> R003
X02 legacy writable epistemic surfaces -> R006
X03 standalone Secret remnants -> R007
X04 combined legacy lore status -> R008
X05 recovery-template carriers -> implementation-only under recovery owners
X06 derivative architecture routing surfaces -> derived support only
X07 retained historical architecture sources -> historical/stale provenance only
X08 maintenance command material -> no parallel recovery authority
X09 non-executable test remainder -> historical/debt/verification only
X10 workflow proof boundary -> source-CI/release-support only
X11 current_state global chronology frontier -> R010
X12 location reverse-presence field -> R015
X13 stale exploration spatial-record consumer -> R048
X14 stale B-prime domain-coverage consumer -> R047
```

Step 5 does not promote any machine artifact to an owner and does not treat existing support as proof of deferred runtime behavior.

## I.3 High-risk probe continuity

All admitted probes remain PASS under this candidate:

```text
R27-P01 Story-local T0/control: PASS
R27-P02 WP-25 deferred vs rejected: PASS
R27-P03 writer-specific partition activation: PASS
R27-P04 migration/version dependency order: PASS
R27-P05 proof-channel separation: PASS
R27-P06 release-time forward gates: PASS
R27-P07 dormant scale/host triggers: PASS
R27-P08 machine reverse conformance: PASS
```

The candidate adds no condition that invalidates a probe result.

---

# J. Remaining implementation-selectable details

The following choices are intentionally left to later implementation planning/TDD within the current owners. They are not architecture blockers now:

- task/package decomposition, module/class/function boundaries and local internal APIs;
- exact owner-local schema spelling/encoding where semantics are already fixed;
- HOT/SQLite tables, indexes and query strategy consistent with native authority and rebuildability;
- exact Story event/control-projection fields, Story-local persistence spelling, snapshot/cache layout and shard geometry;
- writer-specific page/bucket/rollover geometry after `R093..R095/R103` triggers;
- exact bounded failure evaluator/adapter type shape where `R096/R101` applies;
- test fixture organization, harness structure and diagnostic presentation;
- owner-local discovery/index physical layout where indexes remain derived/rebuildable;
- WP-20 migration declaration/transform representation only after a qualifying released compatibility obligation activates it;
- performance tuning only after the accepted owner-specific measurement trigger.

Each selected detail remains subject to the leaf's negative laws, Version Impact gate and proof obligations. A later plan must escalate rather than silently choose if a proposed detail would change semantic authority, persistent/interface policy, compatibility policy, disclosure/access authority or another human-owned boundary.

---

# K. Architecture blockers, uncertainty and change conditions

## K.1 Current blocker result

```text
UNRESOLVED_ARCHITECTURE_BLOCKERS: 0
UNRESOLVED_SIGNIFICANT_READINESS_GAPS: 0
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
BOUNDED_ARCHITECTURE_REOPEN_REQUIRED: NO
```

This result is bounded to the candidate and the admitted Step-2 evidence. It is not the mandatory independent Step-6 verdict.

## K.2 Residual uncertainty

Residual uncertainty is implementation/verification uncertainty rather than unresolved architecture:

- exact delegated physical representations may reveal a concrete conflict only when selected;
- real-host/Protocol-4 behavior cannot be proven before a real MVP exists;
- writer-specific size/latency/parse/conflict evidence may activate representation changes later;
- release acceptance cannot be proven before the exact candidate/tag/asset exists;
- a future released source/target may activate WP-20 compatibility work;
- Step 6 may find qualifier loss, hidden activation, owner drift or a machine reverse-conformance issue requiring bounded repair.

## K.3 Conditions that would change readiness

The candidate must be reopened or repaired if later evidence shows any of:

1. a current accepted owner contradicts a candidate/Step-2 disposition;
2. a readiness leaf cannot be implemented without changing a human-owned semantic/authority/interface/compatibility policy;
3. a material machine responsibility lacks an accepted owner/classification;
4. a no-work/dormant/rejected item was activated without its exact trigger;
5. a proof class was credited for evidence it cannot establish;
6. a workstream aggregation loses a source qualifier, trigger, negative law or reverse mapping;
7. a concrete persistent/interface shape cannot pass its Version Impact/compatibility gate without a new owner-level choice;
8. Step 6 produces a valid blocking/significant finding that cannot be mechanically repaired under current owners.

---

# Run-A Step-5 bounded self-check

This check compares the candidate to the admitted Step-2 closure; it is not Step 6.

```text
READINESS_EXPECTED: 145
READINESS_MAPPED_TO_WS: 145
READINESS_MISSING: []
READINESS_DUPLICATED: []
R27_R004_REINTRODUCED: NO

NO_WORK_EXPECTED: 79
NO_WORK_PRESERVED: 79
NO_WORK_ACTIVATED_BY_CANDIDATE: 0

PO_EXPECTED: 10
PO_ACCOUNTED: 10

ROUND2_EXPECTED: 82
ROUND2_CONTINUITY: 82 / 82 via Step-2 leaf/no-work routes
S14_S53_D15_DELTAS_PRESERVED: YES

MACHINE_MATERIAL_RESPONSIBILITIES: 59 / 59
MACHINE_EXCEPTION_MEMBERS: 31 / 31
MACHINE_FALSE_AUTHORITY_PROMOTIONS: 0

HIGH_RISK_PROBES: 8 / 8 PASS PRESERVED
PROOF_CHANNEL_OVER_CREDIT: 0
PREMATURE_MIGRATION_ACTIVATION: 0
PREMATURE_RELEASE_ACCEPTANCE: 0
PREMATURE_DORMANT_MEASUREMENT_ACTIVATION: 0
REJECTED_GLOBAL_ARCHITECTURE_REVIVED: 0

ARCHITECTURE_BLOCKER_CANDIDATES: []
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
```

`VERSION_IMPACT: NONE` for this documentation-only candidate specification.

---

# Run-A closure cursor

```text
WP27_STEP3: COMPLETE
WP27_STEP4: COMPLETE
WP27_STEP5: COMPLETE
STEP5_CANDIDATE_STATUS: READY_FOR_FRESH_CONTEXT_STEP6_CRITIC
RUN_A: COMPLETE

IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
MIGRATION_EXECUTION_STARTED: NO
RELEASE_EXECUTION_STARTED: NO
REAL_GAMEPLAY_BOOTSTRAP_STARTED: NO

NEXT_ELIGIBLE_UNIT: WP-27 Step 6 — independent fresh-context integrated adversarial review
NEXT_AUTHORIZED_UNIT: WP-27 Step 6 only in a separate fresh-context reviewer run
CURRENT_ASSIGNMENT_STOP: AFTER STEP-5 RECOVERY-SURFACE SYNC AND VERIFICATION
WP27_STEP6: NOT_STARTED
```

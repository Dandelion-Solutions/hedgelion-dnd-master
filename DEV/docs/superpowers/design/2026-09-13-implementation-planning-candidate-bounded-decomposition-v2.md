# HDM Implementation Planning — Candidate Bounded Decomposition v2

Status: **CURRENT SELF-CONTAINED CANDIDATE — READY FOR FRESH INDEPENDENT DECOMPOSITION CRITIC / NOT EXECUTION-READY**

Date: 2026-09-13

This document is the current self-contained implementation-decomposition candidate for the HDM implementation-planning stage.

It consolidates, without requiring layered interpretation:

- the owner-derived P3 dependency semantics and material joins;
- the complete useful content of the original candidate bounded decomposition;
- the resolved repairs for independent-critic findings `DC-001..DC-005`;
- the bounded repairs required by second independent-critic findings `DC-006..DC-014`;
- current coverage, proof, Version Impact, Impact Envelope, HG-01 and future-trigger routing.

The earlier P3, original candidate, repair overlay and both critic results remain immutable provenance and review evidence. They are no longer required to compute the current candidate state. If this v2 conflicts with an earlier derived planning artifact, this v2 controls the current decomposition only; canonical/native semantic/runtime/persistence/version owners and exact WP-27 Step-2 readiness records remain authoritative over all derived planning documents.

This is still a candidate. It may be rejected by the mandatory independent Decomposition Critic. It is not a detailed `writing-plans` package and authorizes no production implementation.

---

## 1. Baseline, gates and invariant accounting

```text
PLANNING_BASELINE_SHA: 85311db76be2e440c97baf0b0625177de2eb0774
PREVIOUS_REVIEW_HEAD: 8b8fb13e77aa30130f45c74b3cbf67f5e8cfee9b
SECOND_CRITIC_RESULT_HEAD: afad1b1ed9793d75ecbed9a8d6ba302933b68a11
CURRENT_ACTIVE_READINESS: 133
TRIGGER_GATED_READINESS_OUTSIDE_EXECUTION: 12
EXPLICIT_NO_WORK_TERMINALS_OUTSIDE_EXECUTION: 79
R27_R004: ABSENT
CURRENT_BOUNDED_UNITS: 14
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
VERSION_IMPACT: NONE
MIGRATION_REQUIRED: NO
DETAILED_EXECUTABLE_PLAN_AUTHORING_AUTHORIZED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
NEXT_GATE: fresh genuinely independent Decomposition Critic
```

The exact planning-active readiness set remains:

```text
R001, R003,
R006..R023,
R025..R089,
R097..R100,
R102,
R104..R146
```

The exact trigger-gated set remains outside current executable work:

```text
R002  FUTURE_RELEASE_ONLY
R005  FUTURE_REAL_TARGET_ONLY
R024  FUTURE_RELEASE_ONLY
R090  FUTURE_REAL_TARGET_ONLY
R091  FUTURE_RELEASE_ONLY
R092  FUTURE_RELEASE_ONLY
R093  FUTURE_WRITER_TRIGGERED
R094  FUTURE_WRITER_TRIGGERED
R095  FUTURE_WRITER_TRIGGERED
R096  FUTURE_FOCUS_RISK_TRIGGERED
R101  FUTURE_FOCUS_RISK_TRIGGERED
R103  FUTURE_WRITER_TRIGGERED
```

All 79 explicit no-work terminals remain no-work. No v2 unit may activate a trigger-gated route, resurrect a no-work terminal or recreate removed `R004`.

The decomposition preserves:

- exact native semantic/runtime/persistence/version owners;
- owner-derived hard-precedes, integration-join, proof-after-target and non-ordering constraints;
- exact leaf-level implementation, test-first, scenario, negative-law, activation and defer/revisit semantics;
- owner-local projection/version checkpoint coherence;
- safe parallelism rather than a universal schema/runtime/persistence sequence;
- proof-channel separation;
- the four HG-01 planning constraints;
- the later mandatory Senior plan GO before production implementation.

---

## 2. Decomposition and completion semantics

### 2.1 Four planning forms

A canonical active readiness leaf is represented in exactly one of these planning forms:

1. **Direct unit responsibility** — one coherent owner/consumer checkpoint can discharge the canonical leaf.
2. **Composite parent** — one canonical readiness leaf spans several accepted owner checkpoints. Planning-only slices route its obligations; no slice is a new canonical readiness ID or semantic owner.
3. **Integration-node responsibility** — the canonical leaf is discharged at the downstream owner-valid join, not by an upstream producer alone.
4. **Pure proof route** — no independent production implementation exists; proof attaches to named realized targets.

Canonical readiness identity is never replaced by planning notation.

### 2.2 Canonical-parent closure rule

For every composite parent `R`:

```text
COMPLETE(R) iff
  every required planning slice of R is complete
  AND every slice-local deterministic/test-first obligation is complete
  AND every required cross-slice/integration proof is complete
  AND all parent-level scenario/negative-law obligations are reconciled
  AND one parent-level Version Impact Gate has reconciled all slice impacts
  AND no slice leaves a required projection/consumer half-migrated.
```

No RD unit may independently mark a composite canonical parent complete from a strict subset of its slices. Parent closure is derived planning metadata only and creates no new runtime or semantic authority.

### 2.3 Proof rule

Target-local RED/GREEN/static/schema/integration/scenario proof is planned with the implementation target. There is no late serial testing subsystem. Pure proof leaves attach after their named targets. Deterministic/static evidence never substitutes for behavioral, empirical or release evidence that belongs to another proof channel.

### 2.4 Dependency rule

The graph distinguishes:

- `HARD_PRECEDES` — the consumer cannot be correctly realized without the predecessor result;
- `JOIN_BEFORE_INTEGRATION` — branches may proceed in parallel, but both must exist before integrated completion/proof;
- `PROOF_AFTER_TARGET` — proof executes against a realized target;
- `CONSTRAINS_WITHOUT_ORDERING` — accepted law constrains realization without imposing execution order.

Numeric readiness order, file adjacency, shared directories and historical workstream order create no dependency by themselves.

---

# 3. Current bounded units

## RD-01 — Shipped instruction and stale current-projection repairs

**Direct readiness:** `R001`, `R003`, `R033`, `R043`, `R047`, `R048`, `R050`.

**Goal:** repair already-known stale active instructions/projections whose semantics are fully settled by accepted owners, without waiting for unrelated runtime realization.

**Expected owner/consumer surfaces:**

- install/project-instruction projections;
- stale CORE prose identified by the exact readiness leaves, including randomness, domain coverage and exploration wording;
- current documentation routing guards/maintenance audit where already owned.

**Preliminary impact boundary:** documentation/package projection only unless a leaf's existing validation guard must be updated to keep the projection mechanically checked.

**Dependencies:** semantic owners only; no hard predecessor among other RD units. Runtime-dependent behavioral acceptance remains downstream, but stale instruction repair is a parallel root.

**Protected invariants:** no new package authority; no generic spatial engine; no new epistemic/event owner; no READY_PC blanket gate; fixed-RNG recovery wording cannot require verbose per-turn logging.

**Out of scope:** production runtime implementation, release acceptance, new semantic architecture.

---

## RD-02 — Information/lore/knowledge/disclosure/message realization

**Direct readiness:** `R007`, `R008`, `R009`, `R017`, `R049`, `R052`.

**Composite slices:** `R006.INFO`, `R016.INFO`, `R018.INFO`, `R053.INFO`, `R062.INFO`.

**Goal:** materialize information-family native contracts and remove/replace retired epistemic/schema aliases without becoming a broad schema-first foundation for unrelated owner families.

**Expected owner/consumer surfaces:**

- information/knowledge/disclosure/message/lore native schemas and roots;
- coordinated family catalog identifiers and direct validators;
- source-native identity required by independently writable information records;
- negative-regression proof for retired `Secret`/legacy epistemic fields and invalid knowledge/disclosure shortcuts.

**Preliminary impact boundary:** information-family schemas/roots/catalog projections plus their direct consumers and validators. LIVE, Actor, execution, temporal, collaboration and Story projections remain in their native owner checkpoints.

**Dependencies:** joins RD-04 only at route/body/load integration; joins RD-09 where LIVE evidence normalizes into native information owners. Information laws constrain RD-03/RD-09/RD-13 without automatically serializing them.

**Protected invariants:** no `Secret`; no second epistemic/disclosure/event authority; no `truth.disputed`; no disclosure-implies-PC-knowledge rule; no false catalog-completion inference; no path/index authority; no generic state service.

**Out of scope:** HOT implementation, generic memory/state service, LIVE lifecycle ownership, Story authority, release migration.

---

## RD-03 — Actor/Asset/Effect runtime model and layered Actor continuity

**Direct readiness:** `R025..R028`, `R104`, `R108..R111`, `R113..R116`, `R126`, `R128..R130`, `R132`, `R136`, `R139`.

**Composite slices:** `R006.ACTOR`, `R016.ACTOR`, `R018.ACTOR`, `R029.ACTOR`, `R062.ACTOR_HISTORY`.

**Goal:** realize owner-local Actor/Asset/Effect machine shapes, state behavior and layered Actor/history continuity while preserving Step-4 epistemic ownership, player agency and bounded cognition.

**Expected owner/consumer surfaces:**

- Actor/Asset/Effect native schemas, roots, loaders/mutators and direct validators;
- Actor foundation/continuity/transient-state logic;
- directional relationship representation/validation;
- sparse event-driven cognition and `NO_CHANGE` handling;
- accepted-history/promotion/source-suitability and recall projection support;
- provisional Actor shape needed by onboarding consumers;
- tests for no-retrofit, no forced mutation, asymmetry, transient invalidation and owner separation.

**Preliminary impact boundary:** native Actor family and its continuity/history consumers. Provisional durability and bootstrap lifecycle are completed through R029/R030 joins rather than by widening Actor authority.

**Dependencies:** joins RD-04 for route/index/HOT integration; supplies Actor shape to RD-14 for `R030`; participates with RD-06 and RD-14 in composite `R029`; supplies native history/continuity inputs to RD-11/RD-13 where required.

**Protected invariants:** no one memory blob; no second entity/knowledge authority; no symmetric relationship inference; no PC voluntary mental-state ownership; no continuous NPC simulation; no generic turn-count TTL; no human-in-the-loop gameplay requirement.

**Out of scope:** persistence authority, bootstrap lifecycle authority, Context Runtime ranking/budgeting, Story canon, collaboration coordination.

---

## RD-04 — Owner-native routing, derived indexes and HOT substrate

**Direct readiness:** `R015`, `R063..R067`.

**Composite integration:** owner-route/root portions of `R018` are integrated only after each owner unit supplies its final machine shape; RD-04 never becomes semantic owner of those families.

**Goal:** provide exact route/body, direct-read, non-authoritative index and owner-bound HOT substrate required by accepted native families.

**Expected owner/consumer surfaces:**

- deterministic native record routing;
- campaign operational ID allocator representation only where owned;
- compact rebuildable indexes;
- HOT/SQLite typed owner envelopes, hydration and local atomic support;
- publication attempt/adoption support that remains owner-bound;
- direct schema/route/index/HOT tests.

**Preliminary impact boundary:** storage/runtime infrastructure implementing accepted owner shapes; owner-specific machine contracts remain upstream/downstream authorities as applicable.

**Dependencies:** owner-family projections from RD-02/RD-03/RD-05/RD-08/RD-09/RD-12/RD-13 join at route/load integration as applicable. Supplies substrate to execution, persistence, recovery, context, collaboration and product consumers without becoming their authority.

**Protected invariants:** direct known-ID reads; indexes/caches are non-authoritative; no automatic partition without WP-24 trigger; no SQL order/rowid authority; no global dirty frontier; no SQLite+LIVE distributed transaction; no generic ID registry/service.

**Out of scope:** native gameplay semantics, global transaction manager, writer-specific future partitioning.

---

## RD-05 — Deterministic execution, fixed-RNG closure and owner-local failure/output adapters

**Direct readiness:** `R034`, `R035`, `R036`, `R042`, `R046`, `R112`, `R118`, `R133`, `R137`.

**Composite slices:** `R016.EXECUTION`, `R018.EXECUTION`, `R062.EXECUTION`.

**Integration leaves supplied downstream:** `R037` to RD-06, `R038` to RD-07, `R039` to RD-08, `R040` to RD-09.

**Goal:** realize deterministic execution/retry identity, local atomic mechanics closure, fixed-RNG retention, native failure outcomes and protected auxiliary/output behavior, while keeping persistence/recovery/temporal/LIVE integration completion under the downstream owners that can actually prove it.

**Expected owner/consumer surfaces:**

- execution/Interaction/IntentPlan/Command/Procedure/Resolution/Continuation machinery and validators;
- owner-native execution IDs/segment/event/firing identity consumers;
- local transaction boundary using RD-04 substrate;
- fixed RNG suspension/resume retention;
- typed native failure/validation diagnostic adapters;
- auxiliary-phase and output fencing;
- direct execution/retry/crash/no-reroll tests.

**Preliminary impact boundary:** Step-3/runtime.execution family and direct failure/diagnostics/output seams. Cross-owner completion occurs in RD-06..RD-09 and does not transfer those owners to execution.

**Dependencies:** consumes accepted owner shapes and RD-04 HOT substrate at integration. Supplies execution closure to publication, recovery, temporal, LIVE, collaboration and Story consumers where their exact readiness requires it.

**Protected invariants:** no replay of accepted mechanics; no host-choice-spanning transaction; no chronology from IDs; no generic scheduler; no generic failure/health/retry owner; diagnostics never become gameplay authority; auxiliary generations never become visible history/canon; no collaboration lifecycle or publication evidence authority.

**Out of scope:** generic DANGER evaluator from trigger-gated `R101`; release empirical calibration; publication/currentness authority; recovery authority; temporal authority; authentication/LIVE authority.

---

## RD-06 — Scoped SAVE/durability and exact publication/currentness

**Direct readiness:** `R037`, `R045`, `R069`, `R070`, `R071`.

**Composite slice:** `R029.DURABILITY`.

**R071 classification:** **mixed current repair + proof**.

**Goal:** realize owner-scoped durability closure, execution-to-persistence integration and exact frozen campaign publication/currentness protocol.

**Expected owner/consumer surfaces:**

- persistence/SAVE scope evaluation and result types;
- R037 integration of accepted execution frontier into durability/SAVE without transferring publication authority to execution;
- exact bounded publication attempt/result/currentness machinery;
- Connector tree/commit/non-force publication consumer;
- G/G+1 adoption/reconciliation support;
- provisional Actor durability for the R029 onboarding composition;
- focused conflict/indeterminate/publication tests.

**Preliminary impact boundary:** persistence/publication owners and direct consumers. Accepted execution and accepted publication remain separate outcomes.

**Dependencies:** `R034 + R035 + R036 JOIN_BEFORE_INTEGRATION R037`; consumes RD-04 storage/index support and RD-05 accepted execution inputs. `R069 HARD_PRECEDES R070`. Supplies confirmed save/publication results to RD-07 and RD-14.

**Protected invariants:** one-tree/one-parent/non-force; no alternate transport; no per-file Contents publication; no blind retry, force, generic merge, fictional chronology, global durable frontier/timer/heartbeat or distributed rollback; no publication authority in RD-05.

**Out of scope:** release packaging, migration execution, generic Git abstraction, Actor semantic ownership.

---

## RD-07 — Current-native recovery and checkpoint alignment

**Direct readiness:** `R011`, `R012`, `R038`, `R072`, `R073`, `R074`.

**Goal:** realize cold/current-native recovery, checkpoint demotion/alignment, bounded maintenance and the execution-to-recovery integration without replay/reroll.

**Expected owner/consumer surfaces:**

- current-route/root recovery executor;
- checkpoint schema/template field cleanup;
- historical/repair maintenance paths;
- recovery of accepted execution/RNG basis;
- selected-LIVE recovery integration where applicable;
- deterministic/scenario recovery tests.

**Preliminary impact boundary:** WP-14 recovery/checkpoint/maintenance owners and current-state projections.

**Dependencies:** `R034 + R036 + R067 JOIN_BEFORE_INTEGRATION R038 + R072`; consumes RD-04 storage support, RD-05 accepted execution closure, RD-06 current publication state and RD-09 selected LIVE state when applicable. `R073` joins checkpoint-aware recovery acceptance.

**Protected invariants:** no checkpoint authority; no guessed latest; no broad scan; no replay/reroll; no RecoveryCut/root-manifest/global frontier; no generic scheduler/global firing ledger; no global clock.

**Out of scope:** temporal occurrence ownership, writer partitioning, release migration, global timeline/CSP engine.

---

## RD-08 — Temporal/thread/current-state realization

**Direct readiness:** `R010`, `R039`, `R075`, `R076`, `R077`.

**Composite slices:** `R006.THREAD_VISIBILITY`, `R016.TEMPORAL`, `R018.TEMPORAL`, `R062.TEMPORAL`.

**R077 classification:** **implementation + proof**.

**Goal:** realize current-state chronology cleanup, typed temporal/thread enrollment, Agenda/dependency invalidation, stable occurrence/firing closure and the deterministic-execution/temporal integration represented by R039.

**Expected owner/consumer surfaces:**

- `world.thread` admission/schema and typed owner-local predicates/deadlines;
- current-state chronology representation cleanup;
- derived Agenda/dependency invalidation;
- stable occurrence/firing/child closure;
- chronology-provider representations and validators;
- temporal/recovery/currentness tests.

**Preliminary impact boundary:** WP-15 temporal/thread/current-state projections and consumers; execution remains Step-3-owned.

**Dependencies:** `R075 HARD_PRECEDES R076`; R039 completion joins RD-05 deterministic execution with RD-08 occurrence lifecycle. RD-07 recovery and RD-09 currentness participate in integrated acceptance where applicable.

**Protected invariants:** no campaign-global clock/frontier; no generic scheduler/global firing ledger; no chronology from CURRENT/IDs/transport order; no thread-visibility-to-PC-knowledge inference.

**Out of scope:** generic timeline/CSP engine, LIVE authorization ownership, execution authority transfer.

---

## RD-09 — Principal authorization, LIVE identity/currentness and split-party causal bridges

**Direct readiness:** `R013`, `R014`, `R019`, `R020`, `R040`, `R078`, `R079`, `R080`, `R122`.

**Composite slices:** `R053.LIVE`, `R016.LIVE`, `R018.LIVE`, `R062.LIVE`.

**R080 classification:** **implementation + proof**.

**Goal:** realize stable principal binding, operation authorization, owner-native LIVE identity/claims/currentness and the authenticated/current-source-to-execution integration represented by R040.

**Expected owner/consumer surfaces:**

- player/principal/control binding and revalidation;
- LIVE source-native identity and exact-source fencing;
- LIVE claim grammar, active/closed/closed-unabsorbed transitions and exact-source lookup;
- stale/revoked/current source integration with deterministic execution;
- split-party currentness/causal bridges;
- direct stale/revocation/currentness tests.

**Preliminary impact boundary:** access/LIVE owners and their direct recovery/collaboration/Story/bootstrap/execution consumers.

**Dependencies:** consumes native routes from owner families/RD-04. R040 completion explicitly joins RD-09 current/authenticated source state with RD-05 execution. Supplies selected LIVE state to RD-07, collaboration currentness to RD-12, recipient/currentness constraints to RD-13 and creator binding input to RD-14.

**Protected invariants:** login/repository permission/card/session/cache/scalar freshness do not authorize; no login-rename inference or stable-ID authority transfer; no wildcard LIVE claim, overlap, fallback, branch deletion, rekey or transport-order chronology; no global split-party synchronization; no authentication/currentness authority in RD-05.

**Out of scope:** automatic creator recovery claim, generic ACL replacement, global LIVE mega-owner.

---

## RD-10 — Role containment, typed handoffs and protected emission

**Direct readiness:** `R054..R057`.

**Goal:** install the single owner-equivalent role/recipient containment route and realize ephemeral role-runtime controls, phase rebind, typed handoffs and protected emission.

**Expected owner/consumer surfaces:**

- `GAME/CORE/AI_REASONING.md` containment owner projection and invoking runtime surfaces;
- TurnEnvelope/profile/bundle/trace control structures;
- role rebind and typed handoff validators;
- Narrator/protected emission boundary;
- direct raw-bundle/recipient-leak/source-escalation/rebind tests.

**Preliminary impact boundary:** role-context/orchestration/output consumers only; no durable role/session/memory record.

**Dependencies:** can begin from accepted owners in parallel. Integrates with RD-11 Context Runtime and with RD-12/RD-13 recipient-sensitive consumers.

**Protected invariants:** physical co-presence is not eligibility; no role-agent topology, persistent context record, generic role-result bus, same-envelope Story feedback or secret delivery through diagnostics/tools/maintenance.

**Out of scope:** Context Runtime selection/budget algorithm, Story authority.

---

## RD-11 — Bounded Context Runtime: discovery, allocation, retrieval and trace

**Direct readiness:** `R059`, `R060`, `R097`, `R105..R107`, `R117`, `R119`, `R120`, `R124`, `R125`, `R127`, `R134`, `R135`, `R138`, `R140`, `R144`, `R145`.

**Composite slice:** `R087.RETROSPECTIVE`.

**Goal:** realize bounded typed context discovery/assembly, conservative capacity allocation/degradation, source-aware retrieval/ranking, dry-run/trace diagnostics and the ordinary-Master retrospective consumer.

**Expected owner/consumer surfaces:**

- compact typed discovery/selectors and dependency limits;
- registered campaign packet/profile/bundle/trace assembly;
- conservative estimator and floor/degradation/UNSATISFIABLE behavior;
- recurrence/recency/diversity/starvation and epistemic-evidence ranking;
- coarse-to-exact retrieval/deduplication;
- explicit target/recipient eligibility and party-size scaling;
- dry-run/non-mutating trace;
- ordinary retrospective binding/acceptance route.

**Preliminary impact boundary:** ephemeral Context Runtime, direct owner readers and diagnostics; native state remains authoritative.

**Dependencies:** consumes native history/continuity from RD-03 and role containment from RD-10 at integration. `R097` requires native history/continuity plus bounded Context Runtime and does not require Commentator. R087 parent closure consumes this retrospective branch with RD-13 and RD-14 branches.

**Protected invariants:** no durable context/memory/vector/graph/worker/fairness record; no keyword-only or unbounded recursive activation; no silent partial critical packet; no copied fixed quotas/provider-percentage hard target; no textual mention treated as knowledge; no targeting eligibility bypass; no linear all-PC loading; no whole-history scan.

**Out of scope:** native canon mutation, Commentator cache/control, real-host empirical tuning until its exact trigger exists.

---

## RD-12 — Collaboration and multiplayer coordination lifecycle

**Direct readiness:** `R021`, `R044`, `R081`, `R082`, `R083`, `R121`, `R123`, `R141..R143`, `R146`.

**Composite slices:** `R016.COLLAB`, `R018.COLLAB`.

**R083 classification:** **implementation + proof**.

**Goal:** realize only admitted agency-dependent collaboration state, typed channels/modes, generation/currentness transitions, recipient-safe catch-up and bounded collective-input behavior.

**Expected owner/consumer surfaces:**

- collaboration obligation/generation/input/route schemas;
- PLAYER routing companion fields where owner-approved;
- authorization/association/close/handoff/currentness transitions;
- typed OOC/diegetic/actionable-intent channels;
- independent/collective/native-ordered coordination modes;
- recipient-specific catch-up and bounded collective windows;
- remaining R083 collaboration machine debt and attached proof;
- direct stale-generation/agency/close-race/channel tests.

**Preliminary impact boundary:** WP-17 collaboration/multiplayer owner surfaces and direct Story/Dramaturg/mechanics consumers; no generic routing service.

**Dependencies:** authorization/currentness joins RD-09; role/recipient containment joins RD-10; execution integration uses RD-05 only when an admitted collective action resolves into mechanics. RD-09 + RD-12 join for recipient/current-generation acceptance.

**Protected invariants:** no transcript coordinator, collaboration authority, registry/index/scheduler/heartbeat, generic input queue/broker, timeout/debounce correctness, arrival-order authority, universal active-player gate or private-input disclosure.

**Out of scope:** Story canon, global planning graph, future measured optimization until WP-24 trigger.

---

## RD-13 — Story/T0/Commentator and retained multiplayer Dramaturg projections

**Direct readiness:** `R022`, `R051`, `R084`, `R085`, `R099`, `R102`, `R131`.

**Composite slices:** `R016.STORY`, `R018.STORY`, `R087.SEMANTIC_EVENT_T0`.

**Goal:** realize the noncanonical Story projection, sparse event-time T0 basis, self-contained baseline Commentator eligibility/control projection and exactly the accepted multiplayer Dramaturg horizons.

**Expected owner/consumer surfaces:**

- Story root/scaffold and projection-state/unit schemas;
- Story producer linking EVENTS/NARRATIVE as accepted by owner contracts;
- SemanticEvent T0 retained-factor schema/serialization/validation and bounded discovery/index support;
- Commentator snapshot/control producer, deterministic pre-LLM filter and isolated cache;
- `DRAMATURG/SHARED.yaml` and `DRAMATURG/PLAYERS/<player_id>.yaml` only for accepted multiplayer retained horizons;
- direct T0/T1, local eligibility/control, no-native-fallback and no-authority tests.

**Preliminary impact boundary:** Story/T0/Commentator projection and fixed Dramaturg paths. Native history, disclosure, access and gameplay canon remain authoritative.

**Dependencies:** R099 T0 basis precedes qualifying Story/Commentator consumption. Native history/event production uses RD-03/RD-05 as applicable; access/currentness and recipient constraints join RD-09/RD-10; retained multiplayer Dramaturg joins RD-12. R087 parent closure explicitly consumes this SemanticEvent/T0 branch together with RD-11 retrospective and RD-14 save/session branches.

**Protected invariants:** no Story/history/ACL/canon authority; no mutable T1 substitute for T0; no hidden reasoning/current-pointer substitute; zero extra serial LLM/tool/remote/publication/irrelevant-turn work for ordinary capture; no native-only baseline fallback for accepted Commentator route; no Story feedback into same envelope; no single-player durable Dramaturg without a new admitted consumer trigger.

**Out of scope:** writer-specific partition/rollover until `R093/R094/R095/R103` trigger; generic narrative dynamics framework.

---

## RD-14 — Bootstrap, onboarding and product-level campaign consumers

**Direct readiness:** `R030`, `R086`, `R098`, `R100`.

**Composite slices:** `R029.ONBOARDING`, `R087.SAVE_SESSION_MENU`.

**Goal:** realize bootstrap/package lifecycle seams, gameplay-first provisional onboarding, product retrospective/save/session-return wiring, creator-login fail-closed continuity and same-chat menu flow without inventing campaign lifecycle semantics.

**Expected owner/consumer surfaces:**

- bootstrap/campaign-menu/package-currentness consumers;
- provisional onboarding/READY_PC integration using RD-03 Actor shape;
- R030 scaffold/lifecycle consumer materialization;
- product save/session-return wiring;
- save-success -> session-local clear -> same-chat campaign menu route;
- creator-only fail-closed consumer path;
- multiplayer non-interference and truthful failed/indeterminate-save handling.

**Preliminary impact boundary:** bootstrap/session/menu consumers and direct acceptance scenarios; no release execution, no Actor semantic ownership, no history authority.

**Dependencies:** RD-03 supplies Actor/provisional shape for R030 and R029; RD-06 supplies confirmed durability/save result for R029/R098; RD-09 supplies creator principal binding/currentness; RD-11 supplies retrospective branch of R087; RD-13 supplies SemanticEvent/T0 branch of R087.

Material creator join:

```text
RD-09:R078 + RD-14:R086
  JOIN_BEFORE_INTEGRATION
RD-14:R100
```

Material bootstrap join:

```text
RD-03 Actor/provisional shape
  JOIN_BEFORE_INTEGRATION
RD-14:R030
```

**Protected invariants:** no complete-sheet prerequisite; no context clear before confirmed save success; no clearing principal/durable campaign state; no inferred pause/completion/archive/membership leave/PC-control transfer/campaign-wide stop; no creator-rename inference or stable-ID authority transfer.

**Out of scope:** release candidate/fresh-Project proof (`R091/R092`), creator automatic recovery, migration execution.

---

# 4. Composite-parent closure ledger

These are planning-only routes. The canonical parent remains the sole readiness identity.

## R006

Required slices:

```text
R006.INFO              -> RD-02
R006.ACTOR             -> RD-03
R006.THREAD_VISIBILITY -> RD-08
```

Parent closure requires all three slices, all parent test/scenario/negative-law obligations and parent Version Impact reconciliation. Thread visibility cannot imply PC knowledge.

## R016

Required slices:

```text
R016.INFO      -> RD-02
R016.ACTOR     -> RD-03
R016.EXECUTION -> RD-05
R016.TEMPORAL  -> RD-08
R016.LIVE      -> RD-09
R016.COLLAB    -> RD-12
R016.STORY     -> RD-13
```

Parent closure additionally requires owner-route/root integration with RD-04 where a family is durable/routed. No family may be omitted because another readiness leaf happens to cover related code.

## R018

Required slices:

```text
R018.INFO      -> RD-02
R018.ACTOR     -> RD-03
R018.EXECUTION -> RD-05
R018.TEMPORAL  -> RD-08
R018.LIVE      -> RD-09
R018.COLLAB    -> RD-12
R018.STORY     -> RD-13
```

Parent closure requires each accepted durable/runtime family to have its final owner-valid schema/root or explicit owner-approved no-durable-record result, plus route/body/load integration through RD-04 where applicable. No allocation matrix becomes a runtime registry/service.

## R029

Required slices:

```text
R029.ACTOR      -> RD-03
R029.DURABILITY -> RD-06
R029.ONBOARDING -> RD-14
```

Parent closure requires the same provisional Actor identity/state to survive the required accepted save path before READY_PC where applicable, with Actor semantics, durability and onboarding each remaining under their native owners. No complete-sheet prerequisite or retrofit path may be introduced.

## R053

Required slices:

```text
R053.INFO -> RD-02
R053.LIVE -> RD-09
```

Parent closure requires LIVE normalization to feed the native information owner without creating a parallel knowledge/currentness authority.

## R062

Required slices:

```text
R062.INFO          -> RD-02
R062.ACTOR_HISTORY -> RD-03
R062.EXECUTION     -> RD-05
R062.TEMPORAL      -> RD-08
R062.LIVE          -> RD-09
```

These routes preserve WP-10 allocation items 1-5 losslessly. Parent closure requires all five owner routes, target-local proofs, parent negative laws and one Version Impact reconciliation.

## R087

Required slices:

```text
R087.RETROSPECTIVE      -> RD-11
R087.SAVE_SESSION_MENU  -> RD-14
R087.SEMANTIC_EVENT_T0  -> RD-13
```

Parent closure requires all three accepted WP-19 downstream branches. The retrospective branch remains ordinary-Master/Context-Runtime behavior; the save/session branch remains product/session behavior backed by RD-06 save truth; the SemanticEvent/T0 branch remains native history/event-owned and feeds the accepted Story/Commentator consumer without creating a second history owner. Zero-extra-serial and disclosure boundaries remain parent obligations.

---

# 5. Integration-node ledger

The following canonical leaves are deliberately completed at downstream joins rather than treated as upstream-local execution work.

## R037 — execution + persistence

```text
R034 + R035 + R036
  JOIN_BEFORE_INTEGRATION
RD-06:R037
```

R037 cannot complete before the persistence/SAVE consumer exists. Execution supplies accepted frontier/evidence; persistence retains durability/publication authority.

## R038 — execution + recovery

```text
R034 + R036 + R067
  JOIN_BEFORE_INTEGRATION
RD-07:R038 + RD-07:R072
```

Recovery acceptance consumes accepted execution/RNG closure and preserves no-replay/no-reroll semantics.

## R039 — execution + temporal occurrence lifecycle

```text
RD-05 deterministic execution closure
  JOIN_BEFORE_INTEGRATION
RD-08:R039 temporal/occurrence completion
```

WP-15 retains occurrence/chronology authority; RD-05 retains execution authority. No scheduler/global chronology authority is introduced.

## R040 — authenticated/current source + execution

```text
RD-09 current authenticated/LIVE source state
+ RD-05 deterministic execution closure
  JOIN_BEFORE_INTEGRATION
RD-09:R040 integrated completion
```

Stale/revoked/current source cases are explicit; neither access/LIVE nor execution subsumes the other authority.

## R030 — Actor shape + bootstrap materialization

```text
RD-03 Actor/provisional shape
  JOIN_BEFORE_INTEGRATION
RD-14:R030
```

The bootstrap owner completes scaffold/lifecycle consumer alignment while Actor semantics remain RD-03-owned.

## R100 — creator fail-closed consumer

```text
RD-09:R078 access/principal binding
+ RD-14:R086 bootstrap/current-package consumer
  JOIN_BEFORE_INTEGRATION
RD-14:R100
```

Repository permission or PLAYER stable ID never substitutes for creator provenance.

---

# 6. Proof routing and exact former proof-bucket classification

There is no proof implementation unit.

| Readiness | Classification | Current route |
|---|---|---|
| R023 | PURE PROOF | applicable owner-family targets |
| R031 | PURE PROOF | RD-03 |
| R032 | PURE PROOF | RD-03 |
| R041 | PURE PROOF | RD-05 plus RD-06/RD-07/RD-08/RD-09 integration targets as implicated |
| R058 | PURE PROOF | RD-10/RD-11 |
| R061 | PURE PROOF | RD-11 |
| R068 | PURE PROOF | RD-04/RD-07 |
| R071 | MIXED REPAIR + PROOF | RD-06 |
| R077 | IMPLEMENTATION + PROOF | RD-08 |
| R080 | IMPLEMENTATION + PROOF | RD-09 |
| R083 | IMPLEMENTATION + PROOF | RD-12 |
| R088 | PURE INTEGRATED PROOF | all applicable realized targets |
| R089 | PURE PROOF-CHANNEL ROUTE | channel-specific evidence boundaries |

Pure proof leaves therefore are exactly:

```text
R023 R031 R032 R041 R058 R061 R068 R088 R089
```

Mixed/implementation-bearing leaves remain counted in their implementation units.

---

# 7. Current dependency/join graph

Edges below are integration/completion relations, not blanket coding order.

```text
RD-01 is an independent projection-repair root.

Owner-family realization roots:
  RD-02 information
  RD-03 Actor/continuity
  RD-05 execution
  RD-08 temporal
  RD-09 access/LIVE
  RD-10 role containment
  RD-11 Context Runtime
  RD-12 collaboration
  RD-13 Story/T0/Commentator

Owner family slices -> RD-04 route/body/load joins where applicable.

RD-03 + RD-04 + RD-05
  -> integrated Actor/execution acceptance where mechanics mutate Actor state.

RD-05:R034/R035/R036 + RD-04 storage support
  -> RD-06:R037 and SAVE/publication integration.

RD-05:R034/R036 + RD-04:R067
  -> RD-07:R038/R072 recovery integration.

RD-05 execution closure
  -> RD-08:R039 temporal/occurrence integration.

RD-09 current authenticated/LIVE source + RD-05 execution closure
  -> RD-09:R040 execution/currentness integration.

RD-04 + RD-06 + RD-09
  -> RD-07 current-native recovery integration.

RD-05 + RD-07 + RD-09
  -> RD-08 temporal/recovery/currentness acceptance where applicable.

RD-09 + RD-12
  -> recipient/current-generation collaboration acceptance.

RD-10 + RD-11
  -> bounded role-context assembly/containment acceptance.

RD-09 + RD-10 + RD-12
  -> RD-13 recipient-safe Story/Dramaturg integration as applicable.

RD-03 + RD-06 + RD-14
  -> R029 parent closure.

RD-03
  -> RD-14:R030 bootstrap materialization.

RD-11 + RD-13 + RD-14
  -> R087 parent closure.

RD-06 + RD-09 + RD-11 + RD-13
  -> RD-14 product consumers as applicable.

RD-09:R078 + RD-14:R086
  -> RD-14:R100.
```

Stable accepted interfaces may be implemented in parallel. No broad schema/catalog predecessor exists. No repaired edge requires a unit-level cycle.

---

# 8. Owner-derived P3 constraints carried into v2

The earlier P3 remains provenance; this section is the current self-contained routing projection.

## E1 — native family contract to route/load realization

Owner-specific `R016/R018/R052/R062` slices join RD-04 routing/body/HOT integration. Schema and route code may proceed in parallel; the join is at integration. No universal schema-first phase exists.

## E2 — Actor family to persistence/bootstrap consumers

Actor shape/continuity in RD-03 feeds R029/R030 through the explicit durability/onboarding/bootstrap joins in §§4-5. `R031/R032` prove the realized Actor target. No legacy PC/NPC/item compatibility layer is added.

## E3 — execution identity/atomicity to durability and recovery

`R034/R035/R036 -> R037` closes in RD-06. `R034/R036/R067 -> R038/R072` closes in RD-07. `R041` proves the applicable integrated execution/persistence/recovery/temporal/LIVE targets.

## E4 — scoped durability to publication/currentness

`R069 HARD_PRECEDES R070`. Owner/index closure plus R070 join publication/currentness acceptance. R071's stale-surface repair and proof remain RD-06-owned.

## E5 — current-native recovery composition

RD-04/RD-06 join RD-07 R072; checkpoint-aware acceptance consumes R073; selected-LIVE recovery additionally consumes RD-09 R079/R080. No checkpoint-first or guessed-latest edge exists.

## E6 — temporal process realization

`R075 HARD_PRECEDES R076`; R077 carries implementation + attached chronology/currentness proof in RD-08. R039 explicitly joins deterministic execution to temporal occurrence lifecycle.

## E7 — access/LIVE realization

`R078 HARD_PRECEDES R079`; R080 carries LIVE implementation + integrated proof. R040 explicitly joins current authenticated/LIVE source state to execution.

## E8 — containment/context realization

`R054 + R055 JOIN_BEFORE_INTEGRATION R056`; `R056 HARD_PRECEDES R057`; `R056 + R059 + R060` join context acceptance; R058/R061 provide attached proof. Round-2 Context Runtime leaves co-realize the bounded target without creating numeric-order dependencies.

## E9 — collaboration lifecycle

`R021 + R081 + R141 + R146` join R082; RD-09 access/currentness + R082 join recipient/current-generation acceptance. R044 and R083 are collaboration-owned; R083 carries machine debt + proof. R122 remains a material causal bridge only, not a global frontier.

## E10 — event-time T0 to Story/Commentator consumer

R099 T0 basis precedes qualifying Story/Commentator consumption. R051/R084/R099 join R102. R087's SemanticEvent/T0 branch is explicitly routed to RD-13 and reconciled at parent closure. Story never becomes a second history/ACL/canon owner.

## E11 — retained multiplayer Dramaturg

Access/currentness + collaboration + R085 join R131 multiplayer retained-horizon acceptance. This does not admit a registry, plot graph, scheduler or single-player durable planning system.

## E12 — ordinary retrospective consumer

Native history/continuity + bounded Context Runtime join R097. R087's retrospective branch reuses that accepted owner route and does not introduce Commentator transition or whole-history scan.

## E13 — save-and-exit consumer

R069/R070 establish save-success result; save-success + R086 bootstrap/menu route join R098 session-local clear/menu return; RD-09 joins multiplayer non-interference when applicable. Context clearing never precedes confirmed save success. R087's save/session branch is reconciled through this owner route.

## E14 — creator-login fail-closed consumer

R078 + R086 join R100 in RD-14. Repository permission or PLAYER stable ID never substitutes for creator provenance.

## E15 — global proof integration

Every realized owner-local target carries its local deterministic/scenario proof; R088/R089 execute only after applicable targets. WP-22 proof-channel separation remains authoritative and creates no runtime subsystem.

---

# 9. Safe parallelism, non-edges and cycle law

## 9.1 Parallel roots

Several owner realizations can begin in parallel because accepted architecture already fixes their contracts:

```text
ROOT-A: RD-01 shipped/current projection repairs
ROOT-B: RD-02 information-family realization
ROOT-C: RD-03 Actor/continuity realization
ROOT-D: RD-05 deterministic execution realization
ROOT-E: RD-10/RD-11 role containment and Context Runtime against accepted contracts
ROOT-F: RD-09 access/LIVE primitives
ROOT-G: RD-14 product/bootstrap work whose required accepted interfaces are already fixed
```

A root means no unresolved architecture decision is needed before planning that bounded target; integrated completion still waits for its exact joins.

## 9.2 Explicit non-edges

The following are not dependency edges:

- WP-27 workstream sequence;
- readiness numeric order;
- universal `schema -> every runtime` sequencing;
- `all persistence -> all recovery -> all multiplayer`;
- one global deterministic-test phase followed by one global scenario-test phase;
- any future-only readiness leaf into current work;
- any explicit no-work terminal into current work;
- any edge resurrecting R004;
- any dependency on Story/cache/index/checkpoint/transcript/diagnostics/CURRENT/IDs/Git order/host UI as semantic authority;
- any migration edge before a qualifying released source/target compatibility obligation exists;
- writer partition/rollover before its exact trigger;
- generic failure/health/retry/scheduler sequencing derived from focus-specific failure semantics.

## 9.3 Cycle law

Derived helpers remain downstream/rebuildable and never become predecessor authority for source owners. The current unit graph contains no intentional executable cycle. Any later detailed plan that discovers a required reverse dependency not represented here must stop at the System Impact Gate rather than silently widening a unit.

---

# 10. Preliminary Impact Envelope/checkpoint matrix

Detailed executable Impact Envelopes are still gated until critic PASS. This matrix is the mandatory preliminary blast-radius contract.

| Unit | Expected owner/change family | Required consumers/joins | Architecture-sensitive surfaces | Explicitly protected/out of scope |
|---|---|---|---|---|
| RD-01 | instruction/current projections | install/CORE readers | active shipped instructions | no runtime authority |
| RD-02 | information families | RD-04, RD-09 normalization | information ownership/native identity | no generic state service/parallel canon |
| RD-03 | Actor/Asset/Effect + continuity/history | RD-04, R029, R030, RD-11/RD-13 | epistemic split/player agency | no generic memory/NPC simulation/persistence ownership |
| RD-04 | routing/index/HOT | owner-family integrations, RD-05..RD-14 as applicable | authority/currentness/local atomicity | no index/cache authority/global transaction |
| RD-05 | deterministic execution | R037/R038/R039/R040 downstream integrations, collab/Story mechanics | determinism/RNG/commit/emission | no replay/global failure/publication/recovery/temporal/LIVE authority |
| RD-06 | SAVE/publication/currentness | R037, R029 durability, RD-07, RD-14 | publication/CAS/currentness | no force/alternate transport/global frontier/Actor authority |
| RD-07 | recovery/checkpoints | R038/R072, selected LIVE | recovery authority/no-reroll | no checkpoint authority/global clock/RecoveryCut |
| RD-08 | temporal/thread/current-state | R039, recovery/currentness integration | chronology/occurrence | no scheduler/global clock/execution authority |
| RD-09 | access/LIVE | R040, RD-07/RD-12/RD-13/RD-14 | authorization/currentness/provenance | no login substitution/global ACL/execution authority |
| RD-10 | role-context/emission | RD-11/RD-12/RD-13 | eligibility/recipient containment | no durable role memory/result bus |
| RD-11 | Context Runtime | R097, R087 retrospective, RD-14 | source eligibility/boundedness | no durable context owner/whole-history scan |
| RD-12 | collaboration/multiplayer | RD-09/RD-10/RD-13/RD-05 mechanics join | agency/current generation/recipient safety | no transcript coordinator/queue/broker |
| RD-13 | Story/T0/Commentator/Dramaturg | R087 T0 branch, RD-14 parent closure | native history/disclosure/access | no Story canon/ACL/native fallback |
| RD-14 | bootstrap/session/menu | R029/R030/R087/R098/R100 | save truth/currentness/lifecycle | no inferred campaign lifecycle/Actor/history authority |

Every later detailed plan executes the per-task Version Impact Gate independently. This v2 preselects no version bump or migration. Clean-slate/prerelease status does not waive projection synchronization.

---

# 11. Exact coverage and reverse mapping

Canonical accounting is by parent readiness IDs, not by number of planning slices.

```text
DIRECT_UNIT_COVERAGE:    117
PURE_PROOF_ROUTES:         9
COMPOSITE_PARENT_ROUTES:    7
TOTAL_CANONICAL_ACTIVE:   133 / 133
```

Direct canonical readiness:

```text
RD-01  7 : R001 R003 R033 R043 R047 R048 R050
RD-02  6 : R007 R008 R009 R017 R049 R052
RD-03 20 : R025-R028 R104 R108-R111 R113-R116 R126 R128-R130 R132 R136 R139
RD-04  6 : R015 R063-R067
RD-05  9 : R034-R036 R042 R046 R112 R118 R133 R137
RD-06  5 : R037 R045 R069 R070 R071
RD-07  6 : R011 R012 R038 R072 R073 R074
RD-08  5 : R010 R039 R075 R076 R077
RD-09  9 : R013 R014 R019 R020 R040 R078 R079 R080 R122
RD-10  4 : R054-R057
RD-11 18 : R059 R060 R097 R105-R107 R117 R119 R120 R124 R125 R127 R134 R135 R138 R140 R144 R145
RD-12 11 : R021 R044 R081 R082 R083 R121 R123 R141-R143 R146
RD-13  7 : R022 R051 R084 R085 R099 R102 R131
RD-14  4 : R030 R086 R098 R100
```

Pure proof canonical readiness:

```text
R023 R031 R032 R041 R058 R061 R068 R088 R089
```

Composite canonical parents:

```text
R006 R016 R018 R029 R053 R062 R087
```

Reverse-map law: every planning slice appears under exactly one canonical parent in §4; every direct or proof leaf appears exactly once in this ledger. Secondary joins do not duplicate canonical accounting.

---

# 12. Future-trigger preservation

The v2 decomposition creates no current task for:

- release-only `R002`, `R024`, `R091`, `R092`;
- real-target-only `R005`, `R090`;
- writer-triggered `R093`, `R094`, `R095`, `R103`;
- focus-risk-triggered `R096`, `R101`.

A later trigger may create a new bounded task/unit; it is not silently folded into RD-01..RD-14 now. All 79 explicit no-work terminals remain no-work. R004 remains absent.

---

# 13. HG-01 planning constraints

All later planning under this decomposition must preserve:

1. Voluntary NPC/faction reasoning remains under Actor/NPC semantic owners; multiplayer currentness/agency rules apply to actual human participants.
2. Ordinary within-location micro-position and transient attention/facing/distraction/reaction remain fiction unless an admitted mechanic/native owner requires typed state.
3. Missing exact realization evidence is a lookup/realization question, not automatic evidence for new architecture.
4. Mechanically-null bounded adjudication remains valid; no generic prose-to-StateDelta, workflow or arbitrary consequence bridge is introduced.

HG-01 remains evidence/guardrail, not a new architecture owner.

---

# 14. Critic finding closure map

## First independent critic

```text
DC-001 RESOLVED IN V2
  broad schema-first foundation removed; owner-local projections/checkpoints retained.

DC-002 RESOLVED IN V2
  proof-only implementation bucket removed; R071/R077/R080/R083 retain implementation-bearing work; pure proof routes explicit.

DC-003 RESOLVED IN V2
  R044 collaboration lifecycle responsibility is RD-12-owned; RD-05 has typed mechanics join only.

DC-004 RESOLVED IN V2
  R045 publication evidence/currentness is RD-06-owned; RD-05 supplies inputs only.

DC-005 RESOLVED IN V2
  R078 + R086 -> R100 is explicit and acyclic; R100 is RD-14-owned.
```

## Second independent critic

```text
DC-006 REPAIRED IN V2
  R016/R018/R062 include explicit EXECUTION slices in RD-05.

DC-007 REPAIRED IN V2
  §4 defines required slice sets and canonical-parent proof/version/completion law for all composite parents.

DC-008 REPAIRED IN V2
  R037 completes in RD-06 at execution+persistence join.

DC-009 REPAIRED IN V2
  R038 completes in RD-07 with explicit execution-to-recovery join and R072.

DC-010 REPAIRED IN V2
  R039 completes in RD-08 at execution+temporal occurrence join.

DC-011 REPAIRED IN V2
  R040 completes in RD-09 at authenticated/current-source + execution join.

DC-012 REPAIRED IN V2
  R029 is a composite Actor+durability+onboarding parent with explicit closure.

DC-013 REPAIRED IN V2
  R030 completes in RD-14 with explicit RD-03 Actor-shape input.

DC-014 REPAIRED IN V2
  R087 is a composite retrospective + save/session/menu + SemanticEvent/T0 parent with all three WP-19 routes explicit.
```

These are author repair claims only. They do not count as independent closure until the next critic verifies them.

---

# 15. Mandatory adversarial tests for the next critic

The next genuinely independent critic must reconstruct owners/dependencies independently and attempt to reject v2 on at least these questions:

1. Are the seven composite parents lossless, including all runtime.execution and WP-19 branches?
2. Can any composite parent be incorrectly marked complete from a strict subset of slices?
3. Are parent-level proof, negative laws and Version Impact consequences preserved exactly once?
4. Do R037/R038/R039/R040 complete at the correct owner-valid downstream joins without transferring authority?
5. Does R029 preserve Actor identity plus durability plus onboarding without creating a new lifecycle owner?
6. Does R030 expose the Actor-shape/bootstrap-consumer join and retain gameplay-first/no-complete-sheet behavior?
7. Does R087 preserve retrospective, save/session/menu and SemanticEvent/T0 branches with zero-extra-serial/disclosure constraints?
8. Is RD-02 now sufficiently bounded, or does it still hide cross-owner/version checkpoints?
9. Does RD-03 combine only coherent Actor/continuity work after R029/R030 extraction?
10. Is RD-04 still a bounded substrate rather than an infrastructure catch-all or authority source?
11. Is RD-05 independently reviewable after moving R037..R040 downstream, with no hidden publication/recovery/temporal/LIVE authority?
12. Do RD-07/RD-08 remain appropriately separated recovery versus temporal owners?
13. Does RD-09 combine access/LIVE only within accepted owner boundaries and avoid creator/product ownership leakage?
14. Is RD-11 too large or internally incoherent across retrieval, budgeting, trace and retrospective duties?
15. Does RD-13 preserve native T0/history ownership while guaranteeing accepted Commentator self-containment?
16. Does RD-14 hide any product lifecycle decision, history authority or Actor semantic ownership?
17. Are all cross-unit joins explicit enough that detailed planners need no architecture rediscovery?
18. Are any implementation units too large or too small for independent TDD/review/coherent commit checkpoints?
19. Are any false serialization edges present, or any necessary ordering edges missing?
20. Are all 133 canonical active leaves losslessly represented with no duplicate semantic ownership?
21. Are all 12 trigger-gated leaves and all 79 no-work terminals preserved without premature activation?
22. Are proof channels target-relative and free of a late proof subsystem?
23. Are preliminary Impact Envelopes sufficient to detect any later blast-radius widening through the System Impact Gate?
24. Are all four HG-01 constraints preserved at Actor/execution/multiplayer/product joins?
25. Does v2 resurrect any rejected scheduler, global failure owner, global memory authority, Story canon, generic state service, distributed transaction, generic queue/broker or prose-to-StateDelta authority?
26. Does any current unit still force a detailed-plan author to rediscover owner boundaries, consumer joins, version checkpoints or proof closure?

The critic may reject the entire v2 decomposition. The author does not pre-approve any boundary.

---

# 16. Candidate exit state

```text
CANDIDATE_V2_STATUS: READY_FOR_FRESH_INDEPENDENT_DECOMPOSITION_CRITIC
CURRENT_REVIEW_TARGET: this document
CURRENT_BOUNDED_UNITS: 14
ACTIVE_READINESS_CANONICAL_ACCOUNTING: 133 / 133
DIRECT_UNIT_COVERAGE: 117
PURE_PROOF_ROUTES: 9
COMPOSITE_PARENT_ROUTES: 7
UNASSIGNED_ACTIVE_READINESS: 0
DUPLICATE_CANONICAL_ACCOUNTING: 0
TRIGGER_GATED_PREMATURE_TASKS: 0
NO_WORK_PREMATURE_TASKS: 0
R27_R004_PRESENT: NO
KNOWN_EXECUTABLE_CYCLES: 0
HIDDEN_HUMAN_DECISION_IDENTIFIED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
VERSION_IMPACT: NONE
MIGRATION_REQUIRED: NO
DECOMPOSITION_CRITIC_REQUIRED: YES
DETAILED_EXECUTABLE_PLAN_AUTHORING_AUTHORIZED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
NEXT_GATE: fresh genuinely independent Decomposition Critic over v2
```

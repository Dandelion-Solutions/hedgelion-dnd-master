# HDM Implementation Planning P3 — Owner-Derived Dependency DAG

Status: **COMPLETE — P3 DEPENDENCY DAG DERIVED / CANDIDATE DECOMPOSITION NEXT**

Date: 2026-09-13

This artifact is the task-local P3 result for the implementation-planning flow authorized by `DEV/CURRENT_PROGRESS.md` and `DEV/docs/superpowers/design/2026-09-13-implementation-planning-task-brief.md`.

It is a planning dependency graph, not a semantic owner, implementation plan, implementation authorization, migration plan, release plan, or production implementation. Exact readiness leaves and their native owners remain authoritative.

---

## 1. Baseline and currentness fence

```text
PLANNING_BASELINE_SHA: 85311db76be2e440c97baf0b0625177de2eb0774
P3_DERIVATION_HEAD: 1e5e7628d91b2d29f9f559c85391b55849f56f84
P3_INPUT_ACTIVE_READINESS: 133
P3_TRIGGER_GATED_READINESS_EXCLUDED: 12
P3_EXPLICIT_NO_WORK_EXCLUDED: 79
R27_R004_PRESENT: NO
```

A fresh `PLANNING_BASELINE_SHA..P3_DERIVATION_HEAD` comparison was performed before derivation. The eight intervening commits change implementation-planning routing/process artifacts and editorially sanitize historical Step-5.8 analytical evidence; no canonical semantic/runtime/version owner used by P3 is changed by that delta. Therefore the P1/P2 baseline remains the admitted readiness baseline and the current HEAD is the fresh routing/currentness fence for P3.

If any native owner or an exact P1/P2 readiness disposition changes after this artifact, later decomposition must re-check the affected edge/member rather than treating this file as timeless authority.

---

## 2. Controlling evidence

Primary controlling inputs:

- `DEV/docs/superpowers/design/2026-09-13-implementation-planning-p1-p2-readiness-active-set.md` — exact current active/future/no-work partition;
- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md` — item-level owner, destination, proof, activation, negative-law and machine-state traceability;
- `DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md` — readiness integration laws only;
- native semantic/runtime/persistence/release owners referenced by each readiness leaf;
- `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` — future executable-plan/Impact-Envelope/execution gate;
- `DEV/RELEASE/VERSIONING.md` and its detailed canonical owner — future per-task Version Impact Gate.

WP-27 workstream labels are not used as dependency authority. Historical Step-5 cross-workstream projection was consulted only as routing evidence and was re-derived against the exact current leaves/native owners.

---

## 3. Exact graph input

### 3.1 Current executable/readiness partition — 133 leaves

The P3 graph contains exactly:

```text
R27-R001
R27-R003
R27-R006..R27-R023
R27-R025..R27-R089
R27-R097..R27-R100
R27-R102
R27-R104..R27-R146
```

Count: `133`.

Every one of these leaves contributes at least one current implementation and/or deterministic/scenario proof obligation. A leaf remains lossless: P3 grouping cannot erase its exact native owner, negative requirements, test-first obligations, scenario obligations, activation semantics, version/migration consequence or delegated implementation choices.

### 3.2 Trigger-gated readiness routes — outside current executable DAG

These exact readiness leaves remain represented as off-graph trigger nodes, not executable nodes:

```text
R27-R002  FUTURE_RELEASE_ONLY
R27-R005  FUTURE_REAL_TARGET_ONLY
R27-R024  FUTURE_RELEASE_ONLY
R27-R090  FUTURE_REAL_TARGET_ONLY
R27-R091  FUTURE_RELEASE_ONLY
R27-R092  FUTURE_RELEASE_ONLY
R27-R093  FUTURE_WRITER_TRIGGERED
R27-R094  FUTURE_WRITER_TRIGGERED
R27-R095  FUTURE_WRITER_TRIGGERED
R27-R096  FUTURE_FOCUS_RISK_TRIGGERED
R27-R101  FUTURE_FOCUS_RISK_TRIGGERED
R27-R103  FUTURE_WRITER_TRIGGERED
```

Count: `12`.

No current graph edge may activate them. Their exact owner-defined trigger is the only route into a later executable DAG.

### 3.3 Explicit no-work terminals

All `79` P1/P2 explicit no-work terminals remain outside P3. `R27-R004` remains removed and must not reappear.

---

## 4. Graph semantics

P3 distinguishes dependency from mere semantic overlap.

### 4.1 Leaf-local micro-DAG

For each active readiness leaf `R` the default executable shape is:

```text
OWNER(R)
  -> REALIZE(R)             only where the leaf requires machine/instruction/schema/runtime realization
  -> DET_PROOF(R)           deterministic/static/schema/unit/integration proof required by the leaf
  -> SCENARIO_PROOF(R)      scenario/adversarial acceptance required by the leaf
```

Where a leaf has `implementation_destination_families: none independently` or otherwise states that it is proof-only, `REALIZE(R)` is omitted. Its proof nodes attach to the actual realized target(s) named by the owner.

No current empirical/release node follows merely because an active leaf mentions later empirical/release evidence. Those channels remain dormant until their exact target/trigger exists.

### 4.2 Edge classes

P3 uses four semantically different relationships:

- `HARD_PRECEDES`: target behavior cannot be correctly realized without the predecessor contract/result already existing;
- `JOIN_BEFORE_INTEGRATION`: branches may be implemented in parallel, but both must exist before the named integrated consumer/proof can pass;
- `PROOF_AFTER_TARGET`: proof-only leaf or proof phase executes only against the realized target it claims to verify;
- `CONSTRAINS_WITHOUT_ORDERING`: accepted invariant/negative law constrains another realization but does **not** serialize implementation.

Only the first three create executable DAG edges. `CONSTRAINS_WITHOUT_ORDERING` is deliberately a non-edge.

A workstream name, source-file adjacency, numeric readiness ID, shared architecture section, common schema directory, or historical analysis order creates no P3 edge by itself.

---

## 5. Owner-derived realization spines

The following spines are dependency-routing projections, not future plan/task boundaries. Candidate decomposition must be free to split or join them when the exact leaf graph requires it.

### G1 — shipped instruction/current-projection reconciliation

Primary active leaves:

`R001`, `R003`, `R033`, `R043`, `R047`, `R048`, `R050`, plus the instruction projection of `R054/R055`.

These repairs are mostly independent roots because accepted owners already settle their semantics. They must not wait for the full runtime merely to correct stale active instructions. Runtime-dependent behavioral acceptance remains downstream.

### G2 — native information/schema/catalog families

Primary active leaves:

`R006..R023`, `R025..R027`, `R049`, `R052`, `R053`, `R062`, `R064`, with catalog/schema conformance in `R023`.

Owner laws fix truth/knowledge/disclosure/message separation, retired Secret/legacy epistemic fields, native family allocation, identity/routing and non-authoritative derived/index surfaces.

This spine establishes contracts consumed by HOT/persistence/context/collaboration/Story paths. It does not create one generic state database or one schema authority.

### G3 — Actor/Asset/Effect and Actor-continuity realization

Primary active leaves:

`R025..R032`, `R104`, `R108..R116`, `R126..R130`, `R132`, `R136`, `R139`.

The spine includes unified Actor/Asset/Effect representation, three Actor continuity lifetimes, directional relationships, sparse event-driven cognition, NO_CHANGE, bounded proposal validation and transient-state invalidation. Step-4 epistemics remain separate native authority.

Round-2 leaves here constrain/co-realize the Actor owner; they do not create a second implementation phase merely because their IDs are later.

### G4 — deterministic execution and HOT-local atomicity

Primary active leaves:

`R034..R046`, `R066..R068`, `R112`, `R136`, with failure/diagnostic integration from `R042/R046`.

Owner-local execution identities, fixed RNG, one local atomic establishment boundary, accepted execution closure and derived/HOT helpers are realized here. There is no host-choice-spanning transaction, replay authority, generic journal or SQLite-as-canon promotion.

### G5 — persistence/publication/currentness

Primary active leaves:

`R037`, `R045`, `R065`, `R067`, `R069..R071`, plus currentness consumers in `R098`.

Scoped SAVE/durability closure and exact frozen Connector publication are owner-bound. Publication is one-tree/one-parent/non-force and tri-state; no alternate Git transport, force, blind retry, generic merge or global durability frontier is admitted.

### G6 — recovery/checkpoint/temporal/LIVE/access

Primary active leaves:

`R010..R015`, `R019`, `R020`, `R038..R040`, `R063`, `R072..R080`, `R100`, `R122`.

The spine composes current-native recovery, checkpoint demotion, typed chronology/process enrollment, principal binding, LIVE claim/currentness/CAS and bounded historical maintenance. It preserves no-global-clock, no-guessed-latest, no-branch-deletion and no-replay laws.

### G7 — role containment and Context Runtime

Primary active leaves:

`R054..R061`, `R105..R107`, `R117`, `R119`, `R120`, `R125`, `R127`, `R134`, `R135`, `R138..R140`, `R144`, `R145`.

The spine realizes behavior-equivalent role containment, ephemeral typed role/context controls, typed handoffs, protected emission, bounded dependency discovery, conservative allocation/degradation, retrieval/ranking/trace and recipient eligibility. It remains an ephemeral bounded assembly/delivery mechanism, not durable memory/knowledge authority.

### G8 — collaboration and multiplayer coordination

Primary active leaves:

`R021`, `R044`, `R078..R083`, `R121..R124`, `R141..R143`, `R146`.

Only owner-proven `AGENCY_DEPENDENT_COLLECTIVE` semantics create durable collaboration state. Typed channels, independent/collective/native-ordered modes, recipient-safe catch-up and bounded collective windows remain under access/currentness/agency owners. No transcript coordinator, generic queue/broker, universal active-player gate or arrival-order authority is created.

### G9 — Story / T0 / Commentator / Dramaturg projections

Primary active leaves:

`R022`, `R051`, `R084`, `R085`, `R099`, `R102`, `R131`, with disclosure/context projection constraints from `R124`.

Story is noncanonical. Qualifying event-time T0 basis remains native SemanticEvent/history-owned and is projected into Story only for the accepted consumer. Commentator filtering/control is local and deterministic before LLM exposure. Multiplayer Dramaturg retains only the fixed shared/player-local horizons; single-player planning remains ephemeral.

### G10 — bootstrap/product-use consumers

Primary active leaves:

`R029`, `R030`, `R063`, `R086`, `R087`, `R097..R100`, with proof integration in `R088/R089`.

This spine covers provisional onboarding/READY_PC, bounded allocator/bootstrap, ordinary-Master retrospective, save-and-exit, creator-login fail-closed continuity and the event-time T0 consumer seam. It consumes native state/persistence/access/context owners rather than creating product-wide substitute authorities.

### G11 — proof-channel integration

Proof-only or predominantly proof-routing leaves include at least:

`R023`, `R031`, `R032`, `R041`, `R058`, `R061`, `R068`, `R083`, `R088`, `R089`.

They create no independent runtime subsystem. Their deterministic/scenario checks attach to the exact realized targets and preserve WP-22 proof-channel separation. Later supported-target empirical/release proof remains trigger-gated.

---

## 6. Exact cross-spine executable edges

The following are the material cross-leaf/cross-spine dependencies that P3 can prove from current owners. A later decomposition may add finer owner-local edges, but may not remove these without owner evidence.

### E1 — native family contract to route/load realization

```text
R016 + R018 + R052 + R062
  JOIN_BEFORE_INTEGRATION
R064
  JOIN_BEFORE_INTEGRATION
R066
```

Meaning: accepted native families, their final schema/root and route/body identity all must agree before HOT hydration/integration can be accepted. Schema and route code may be developed in parallel because the owners already settle both; the join is at integration, not an invented serial coding phase.

### E2 — Actor family to HOT/persistence/bootstrap consumers

```text
R026 + R027
  JOIN_BEFORE_INTEGRATION
R028 + R029 + R030

R031 PROOF_AFTER_TARGET (R026..R030)
R032 PROOF_AFTER_TARGET (implemented rules/runtime Actor target)
```

No compatibility layer for legacy PC/NPC/item schemas is inserted.

### E3 — execution identity/atomicity to durability and recovery

```text
R034 + R035 + R036
  JOIN_BEFORE_INTEGRATION
R037

R034 + R036 + R067
  JOIN_BEFORE_INTEGRATION
R038 + R072

R041 PROOF_AFTER_TARGET (R034..R040 + R067 + R072 as applicable)
```

Fixed RNG/Continuation inputs are retained across recovery; accepted mechanics are never replayed to regenerate downstream output.

### E4 — scoped durability to publication/currentness

```text
R069
  HARD_PRECEDES
R070

R065 + R067 + R070
  JOIN_BEFORE_INTEGRATION
publication/currentness integration proof

R071 PROOF_AFTER_TARGET (realized publisher + named dependent paths)
```

`R071` also contains named stale-surface reconciliation; those prose repairs may be completed independently, while its end-to-end proof follows the realized publisher.

### E5 — current-native recovery composition

```text
R066 + R067 + R069 + R070
  JOIN_BEFORE_INTEGRATION
R072

R073
  JOIN_BEFORE_INTEGRATION
checkpoint-aware recovery acceptance

R079 + R080
  JOIN_BEFORE_INTEGRATION
selected-LIVE recovery acceptance
```

There is no checkpoint-first or guessed-latest edge.

### E6 — temporal process realization

```text
R075
  HARD_PRECEDES
R076

R075 + R076
  JOIN_BEFORE_INTEGRATION
R077 deterministic/scenario chronology/currentness proof
```

The derived Agenda remains non-authoritative and no generic scheduler/global firing ledger is introduced.

### E7 — access/LIVE realization

```text
R078
  HARD_PRECEDES
R079
  HARD_PRECEDES
R080 integrated CAS/revocation/recovery proof
```

Principal authorization and LIVE currentness remain distinct checks even though both are required by integrated multiplayer operations.

### E8 — containment/context realization

```text
R054 + R055
  JOIN_BEFORE_INTEGRATION
R056

R056
  HARD_PRECEDES
R057

R056 + R059 + R060
  JOIN_BEFORE_INTEGRATION
R061

R058 PROOF_AFTER_TARGET (R054..R057 plus applicable Context Runtime target)
```

`R105..R107`, `R117`, `R119/R120`, `R125`, `R127`, `R134/R135`, `R138..R140`, `R144/R145` are co-realization constraints/obligations on the same bounded Context Runtime spine; their numeric order creates no additional dependency.

### E9 — collaboration lifecycle

```text
R021 + R081 + R141 + R146
  JOIN_BEFORE_INTEGRATION
R082

R078 + R079 + R082
  JOIN_BEFORE_INTEGRATION
recipient/current-generation collaboration acceptance

R083 PROOF_AFTER_TARGET (R081 + R082 + applicable access/currentness target)
```

`R044`, `R121`, `R123`, `R142`, `R143` constrain/co-realize this target. `R122` requires independent scene/context/chronology owners and only material causal bridges; it creates no global frontier.

### E10 — event-time T0 to Story/Commentator consumer

```text
R099
  HARD_PRECEDES
qualifying T0 projection consumed by R084/R102

R051 + R084 + R099
  JOIN_BEFORE_INTEGRATION
R102
```

`R102` may not fall back to native-only baseline reads for the accepted baseline Commentator contract, and Story never becomes a second history/ACL/canon owner.

### E11 — retained multiplayer Dramaturg

```text
R078 + R081/R082 + R085
  JOIN_BEFORE_INTEGRATION
R131 multiplayer retained-horizon acceptance
```

This is a consumer join, not permission for a registry, plot graph, scheduler or single-player durable planning system.

### E12 — ordinary retrospective consumer

```text
native history/continuity realization (R104/R108..R112/R119/R126/R127/R132 as applicable)
+ bounded Context Runtime realization (R059/R060 and related selector obligations)
  JOIN_BEFORE_INTEGRATION
R097
```

The consumer remains ordinary Master behavior; no Commentator transition or whole-history scan is introduced.

### E13 — save-and-exit consumer

```text
R069 + R070
  HARD_PRECEDES
save-success result

save-success result + R086 bootstrap/menu route
  JOIN_BEFORE_INTEGRATION
R098 session-local clear/menu return

R078..R080
  JOIN_BEFORE_INTEGRATION
R098 multiplayer non-interference acceptance when multiplayer applies
```

Context clearing never precedes confirmed save success.

### E14 — creator-login fail-closed consumer

```text
R078 access/principal binding
+ R086 bootstrap/current package consumer
  JOIN_BEFORE_INTEGRATION
R100
```

Repository permission or PLAYER stable ID never substitutes for creator provenance.

### E15 — global proof integration

```text
all realized owner-local targets
  -> their leaf-local DET_PROOF nodes
  -> their leaf-local SCENARIO_PROOF nodes

R088/R089
  PROOF_AFTER_TARGET
applicable integrated implementation targets
```

WP-22 mapping validates proof ownership and channel separation; it does not create a runtime subsystem and deterministic/static evidence does not discharge behavioral/empirical/release proof.

---

## 7. Round-2 continuity as constraints, not a second sequence

The `43` active Round-2 readiness leaves are already members of the 133-leaf graph. They do not form a later implementation phase merely because they occupy `R104..R146`.

Routing summary:

- continuity/history: `R104`, `R108..R112`, `R119`, `R126`, `R127`, `R132` constrain/co-realize native history/continuity and bounded retrieval;
- Actor continuity/cognition: `R113..R116`, `R128..R130`, `R136`, `R139` constrain/co-realize G3;
- Context Runtime: `R105..R107`, `R117`, `R120`, `R125`, `R134`, `R135`, `R138..R140`, `R144`, `R145` constrain/co-realize G7;
- auxiliary/emission containment: `R118`, `R133`, `R137` constrain/co-realize G7 and the protected emission boundary;
- collaboration/multiplayer: `R121..R124`, `R141..R143`, `R146` constrain/co-realize G8/G9;
- multiplayer Dramaturg: `R131` consumes the admitted G8/G9/access target.

Where two records express the same owner realization from different evidence routes, P3 records one implementation target with all leaf obligations retained. It does not manufacture duplicate code/tasks solely to obtain one task per readiness ID.

---

## 8. Negative edges and rejected sequencing

The following are explicitly **not** DAG edges:

- `WS27-01 -> WS27-02 -> ... -> WS27-11`;
- readiness numeric order;
- `schema -> every runtime` as a universal serial phase when owner contracts already permit parallel implementation and only require an integration join;
- `all persistence -> all recovery -> all multiplayer`;
- `all deterministic tests -> all scenario tests` globally; proof ordering is target-local;
- any edge from future-only `R002/R005/R024/R090..R096/R101/R103` into current executable work;
- any edge from the 79 no-work terminals into current executable work;
- any edge that resurrects `R004`;
- any dependency on Story, cache, index, checkpoint, transcript, diagnostics, CURRENT, IDs, Git order or host UI as semantic authority;
- any migration edge before a qualifying released source/target compatibility obligation exists;
- any writer partition/rollover edge before the exact writer trigger exists;
- any generic failure/health/retry/scheduler edge derived from focus-specific failure semantics.

---

## 9. Roots, joins and safe parallelism

### 9.1 Current roots

Because the semantic owners are already accepted, several realization roots can be planned in parallel:

```text
ROOT-A: stale shipped/document projection repairs (G1)
ROOT-B: native schema/catalog/family materialization (G2)
ROOT-C: Actor continuity/model realization consistent with G2 contracts (G3)
ROOT-D: deterministic execution/HOT implementation against accepted Step-3/WP-12 contracts (G4)
ROOT-E: role containment/Context Runtime implementation against accepted WP-08/09 contracts (G7)
ROOT-F: access/LIVE primitives against accepted WP-16 contracts (G6)
ROOT-G: bootstrap consumer work whose required native contracts are already fixed (G10)
```

“Root” means no unresolved architecture decision is needed before planning the bounded target. It does not mean the branch can pass integrated acceptance without its joins.

### 9.2 Material joins

The main integration joins are:

- native family/schema + route + HOT hydration;
- execution + HOT atomicity + persistence/recovery;
- scoped SAVE + exact publication/currentness;
- access/LIVE + collaboration;
- role containment + Context Runtime + protected emission;
- T0 native history + Story projection + Commentator control;
- persistence + bootstrap/menu for save-and-exit;
- all target-local deterministic/scenario proof before package-level acceptance.

### 9.3 Cycle check

No current owner-derived executable cycle was found.

Potential apparent cycles were rejected as false dependencies where a derived helper appeared to feed its native owner. Specifically, indexes/caches/Story/checkpoints/diagnostics/context projections remain downstream or rebuildable and cannot become predecessor authority for their source owners.

```text
P3_CYCLES_FOUND: 0
P3_UNRESOLVED_EDGES: 0
P3_FALSE_WORKSTREAM_ORDER_EDGES: 0
P3_FUTURE_ONLY_PREMATURE_NODES: 0
P3_NO_WORK_PREMATURE_NODES: 0
P3_REJECTED_ARCHITECTURE_RESURRECTIONS: 0
```

---

## 10. P3 implications for candidate bounded decomposition

The next planning slice must decompose implementation around coherent target/join boundaries rather than WP-27 workstream labels.

The candidate decomposition must therefore:

1. name every exact active readiness leaf it discharges or constrains;
2. distinguish implementation targets from proof-only routes;
3. keep trigger-gated/no-work routes out of executable tasks;
4. use the edges in §6 as minimum dependency/join constraints;
5. preserve parallel roots from §9 instead of imposing a universal schema/runtime/persistence sequence;
6. keep Story/cache/index/checkpoint/diagnostic/context projections non-authoritative;
7. expose cross-plan joins explicitly rather than hiding them inside a late “integration” bucket;
8. state preliminary owner/consumer/contract blast radius for each bounded unit;
9. carry negative laws and material delegated implementation choices into the candidate unit;
10. remain rejectable/re-decomposable by the independent Decomposition Critic.

Detailed `writing-plans` authoring remains prohibited until that critic returns PASS after all BLOCKING/SIGNIFICANT findings are repaired and independently re-reviewed.

---

## 11. Closure accounting

```text
P3_STATUS: COMPLETE
P3_INPUT_ACTIVE_READINESS: 133 / 133
P3_TRIGGER_GATED_PRESERVED: 12 / 12
P3_NO_WORK_PRESERVED: 79 / 79
R27_R004_PRESENT: NO
ROUND2_ACTIVE_READINESS_PRESERVED: 43 / 43
P3_CYCLES_FOUND: 0
P3_UNRESOLVED_EDGES: 0
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
VERSION_IMPACT: NONE — planning documentation only; no version-bearing semantic/machine/runtime/schema/catalog/protocol owner changed
MIGRATION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_STARTED: NO
NEXT_UNIT: candidate bounded implementation plan/task decomposition for independent Decomposition Critic
```

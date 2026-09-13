# HDM Implementation Planning — Candidate Bounded Decomposition

Status: **CANDIDATE — READY FOR INDEPENDENT DECOMPOSITION CRITIC / NOT EXECUTION-READY**

Date: 2026-09-13

This artifact is the candidate implementation decomposition required after P3 and before the mandatory independent Decomposition Critic.

It is intentionally not a detailed `writing-plans` package. It may be rejected or substantially re-decomposed by the critic. Production implementation remains unauthorized.

---

## 1. Inputs and invariants

```text
PLANNING_BASELINE_SHA: 85311db76be2e440c97baf0b0625177de2eb0774
P3_ARTIFACT: DEV/docs/superpowers/design/2026-09-13-implementation-planning-p3-dependency-dag.md
CURRENT_ACTIVE_READINESS: 133
TRIGGER_GATED_READINESS_OUTSIDE_EXECUTION: 12
NO_WORK_TERMINALS_OUTSIDE_EXECUTION: 79
CANDIDATE_UNITS: 14
PRIMARY_ACTIVE_READINESS_ASSIGNMENTS: 133 / 133
DUPLICATE_PRIMARY_ASSIGNMENTS: 0
UNASSIGNED_ACTIVE_READINESS: 0
```

The decomposition preserves:

- exact native semantic/runtime/persistence/version owners;
- P3 hard-precedes, integration-join and proof-after-target edges;
- leaf-local deterministic/scenario obligations;
- exact future triggers and no-work terminals;
- negative architecture laws and rejected subsystems;
- no production implementation before complete plan-package Senior GO;
- no detailed executable plan authoring before independent Decomposition Critic PASS.

Candidate unit boundaries are based on coherent owner/consumer targets and independently verifiable joins. WP-27 workstream labels and readiness numeric order are not used as task boundaries.

---

## 2. Primary-assignment rule

Every active readiness leaf has exactly one **primary** candidate unit below. A leaf may also constrain or be consumed by another unit through an explicit cross-unit join; that secondary relationship does not duplicate its implementation obligation.

Proof-only leaves are assigned to `CD-14` and attach back to named implementation targets. Where a leaf combines a documentation repair with later target proof, the concrete repair stays with its implementation unit while its integrated proof is represented by the applicable leaf-local/`CD-14` verification route.

---

# 3. Candidate units

## CD-01 — Shipped instruction and stale current-projection repairs

**Primary readiness:** `R27-R001`, `R27-R003`, `R27-R033`, `R27-R043`, `R27-R047`, `R27-R048`, `R27-R050`.

**Goal:** repair already-known stale active instructions/projections whose semantics are fully settled by accepted owners, without waiting for unrelated runtime realization.

**Expected owner/consumer surfaces:**

- install/project-instruction projections;
- stale CORE prose identified by the exact readiness leaves, including randomness, domain coverage and exploration wording;
- current documentation routing guards/maintenance audit where already owned.

**Preliminary impact boundary:** documentation/package projection only unless a leaf's existing validation guard must be updated to keep the projection mechanically checked.

**Dependencies:** semantic owners only; no hard predecessor among other candidate units. Later behavioral acceptance may depend on runtime units, but the stale instruction repair itself is a parallel root.

**Protected invariants:** no new package authority; no generic spatial engine; no new epistemic/event owner; no READY_PC blanket gate; fixed-RNG recovery wording cannot require verbose per-turn logging.

**Out of scope:** production runtime implementation, release acceptance, new semantic architecture.

---

## CD-02 — Native record families, information contracts and schema/catalog convergence

**Primary readiness:** `R27-R006..R27-R022`, `R27-R025..R27-R027`, `R27-R049`, `R27-R052`, `R27-R053`, `R27-R062`.

**Goal:** materialize the accepted native record-family boundaries and remove/replace legacy schema aliases without creating parallel authorities.

**Expected owner/consumer surfaces:**

- `GAME/SCHEMA/*` native family schemas;
- `GAME/CAMPAIGN/*` family roots/templates where the owner requires them;
- coordinated catalog entries/identifiers and schema/catalog validation;
- knowledge/disclosure/message/lore/Actor-Asset-Effect family representation;
- source-native identity fields needed by independently writable records.

**Preliminary impact boundary:** schema/catalog/scaffold surfaces plus direct schema validators and negative-regression tests. Physical runtime algorithms belong to later units unless required to validate route/body identity.

**Dependencies:** accepted Step-4/WP-10/WP-11/WP-16/WP-17/WP-18 owners. It is a P3 root for implementation; integration joins with `CD-04`, `CD-08`, `CD-11`, and `CD-12`.

**Protected invariants:** no `Secret`; no second epistemic/disclosure/event authority; no false catalog-completion inference; no path/index authority; no legacy PC/NPC/item compatibility layer solely to preserve prerelease shapes; Story/planning records remain noncanonical.

**Out of scope:** HOT implementation, generic state service, runtime Story authority, release migration.

---

## CD-03 — Actor/Asset/Effect runtime model and layered Actor continuity

**Primary readiness:** `R27-R028..R27-R030`, `R27-R104`, `R27-R108..R27-R111`, `R27-R113..R27-R116`, `R27-R126`, `R27-R128..R27-R130`, `R27-R132`, `R27-R136`, `R27-R139`.

**Goal:** realize owner-local Actor/Asset/Effect state behavior and layered Actor/history continuity while preserving Step-4 epistemic ownership and bounded cognition.

**Expected owner/consumer surfaces:**

- Actor/Asset/Effect state loaders/mutators and native schema consumers;
- Actor continuity/foundation/transient-state logic;
- directional relationship representation/validation;
- sparse event-driven cognition and `NO_CHANGE` handling;
- accepted-history/promotion/source-suitability and recall projection support;
- direct tests for no-retrofit, no forced mutation, asymmetry and transient invalidation.

**Preliminary impact boundary:** native Actor family runtime and its direct history/continuity consumers; no generic memory framework.

**Dependencies:** joins with `CD-02` for final native shapes/routes and with `CD-04` for HOT representation/atomicity where persistence is involved. Does not wait for Story or Context Runtime.

**Protected invariants:** no one memory blob; no second entity/knowledge authority; no symmetric relationship inference; no PC voluntary mental-state ownership; no continuous NPC simulation; no generic turn-count TTL; no human-in-the-loop gameplay requirement.

**Out of scope:** Context Runtime ranking/budgeting, Story projection, collaboration coordination.

---

## CD-04 — Persistent topology, owner-native routing/indexes and HOT substrate

**Primary readiness:** `R27-R063..R27-R067`.

**Goal:** provide the exact route/body, direct-read, non-authoritative index and owner-bound HOT substrate required by accepted native families.

**Expected owner/consumer surfaces:**

- deterministic native record routing;
- campaign operational ID allocator representation only where owned;
- compact rebuildable indexes;
- HOT/SQLite typed owner envelopes, hydration and local atomic support;
- publication attempt/adoption support that remains owner-bound.

**Preliminary impact boundary:** storage/runtime infrastructure that implements accepted owner shapes; direct schema/route/index/HOT tests.

**Dependencies:** integration join with `CD-02` native family shapes. Supplies substrate to `CD-05`, `CD-06`, `CD-07`, `CD-08`, `CD-10`, `CD-11` and `CD-13` without becoming semantic authority.

**Protected invariants:** direct known-ID reads; indexes/caches are non-authoritative; no automatic partition without WP-24 trigger; no SQL order/rowid authority; no global dirty frontier; no SQLite+LIVE distributed transaction; no generic ID registry/service.

**Out of scope:** native gameplay semantics, global transaction manager, writer-specific future partitioning.

---

## CD-05 — Deterministic execution, fixed-RNG closure and owner-local failure/diagnostic adapters

**Primary readiness:** `R27-R034..R27-R040`, `R27-R042`, `R27-R044..R27-R046`, `R27-R112`, `R27-R118`, `R27-R133`, `R27-R137`.

**Goal:** realize deterministic execution/retry identity, local atomic mechanics closure, fixed-RNG retention, native failure outcomes, collaboration contribution seam, publication evidence seam and protected auxiliary/output behavior.

**Expected owner/consumer surfaces:**

- execution/Resolution/Continuation machinery and validators;
- owner-native execution IDs/segment/event/firing identity consumers;
- local transaction boundary using `CD-04` substrate;
- fixed RNG suspension/resume retention;
- typed native failure/validation diagnostic adapters;
- auxiliary-phase and output fencing;
- direct execution/retry/crash/no-reroll tests.

**Preliminary impact boundary:** Step-3 execution consumers plus direct failure/diagnostics/output seams; no persisted global failure subsystem.

**Dependencies:** `CD-02`/`CD-04` integration join for owner shapes and HOT substrate. Supplies accepted execution closure to `CD-06`, `CD-07`, `CD-08`, `CD-11` and `CD-12` where those consumers require it.

**Protected invariants:** no replay of accepted mechanics; no host-choice-spanning transaction; no chronology from IDs; no generic scheduler; no generic failure/health/retry owner; diagnostics never become gameplay authority; auxiliary generations never become visible history/canon.

**Out of scope:** generic DANGER evaluator from trigger-gated `R101`; release empirical calibration.

---

## CD-06 — Scoped SAVE/durability and exact Connector publication/currentness

**Primary readiness:** `R27-R069`, `R27-R070`.

**Goal:** realize owner-scoped durability closure and the exact frozen campaign publication/currentness protocol.

**Expected owner/consumer surfaces:**

- persistence/SAVE scope evaluation and result types;
- exact bounded publication attempt/result/currentness machinery;
- Connector tree/commit/non-force publication consumer;
- G/G+1 adoption/reconciliation support;
- focused conflict/indeterminate/publication tests.

**Preliminary impact boundary:** persistence/publication owners and direct consumers; no unrelated gameplay semantic changes.

**Dependencies:** joins `CD-04` owner/index closure and `CD-05` accepted execution closure where the SAVE scope includes them. Supplies confirmed save/publication results to `CD-07` and `CD-13`.

**Protected invariants:** one-tree/one-parent/non-force; no alternate transport; no per-file Contents publication; no blind retry, force, generic merge, fictional chronology, global durable frontier/timer/heartbeat or distributed rollback.

**Out of scope:** release packaging; migration execution; generic Git abstraction.

---

## CD-07 — Current-native recovery, checkpoints, temporal/thread lifecycle and maintenance

**Primary readiness:** `R27-R072..R27-R076`.

**Goal:** realize cold/current-native recovery, checkpoint demotion/alignment, bounded maintenance, typed temporal/thread enrollment and stable firing/continuation recovery.

**Expected owner/consumer surfaces:**

- current-route/root recovery executor;
- checkpoint schema/template field cleanup;
- historical/repair maintenance paths;
- `world.thread` admission/schema and typed owner-local predicates/deadlines;
- derived Agenda/dependency invalidation and stable occurrence/firing closure;
- recovery/temporal deterministic/scenario tests.

**Preliminary impact boundary:** recovery/checkpoint/temporal/maintenance owners and current-state projections.

**Dependencies:** integration joins from `CD-04`, `CD-05`, and `CD-06`; selected LIVE recovery additionally joins `CD-08`.

**Protected invariants:** no checkpoint authority; no guessed latest; no broad scan; no replay/reroll; no RecoveryCut/root-manifest/global frontier; no generic scheduler/global firing ledger; no global clock.

**Out of scope:** writer partitioning, release migration, global timeline/CSP engine.

---

## CD-08 — Principal authorization, LIVE claims/currentness and creator provenance

**Primary readiness:** `R27-R078`, `R27-R079`, `R27-R100`, `R27-R122`.

**Goal:** realize stable principal binding, operation authorization, owner-native LIVE claim/currentness and fail-closed creator provenance consumption, while supporting split-party causal bridges without a global frontier.

**Expected owner/consumer surfaces:**

- player/principal/control binding and revalidation;
- LIVE claim grammar, active/closed/closed-unabsorbed transitions and exact-source lookup;
- creator-only authorization consumer paths;
- split-party currentness/bridge consumers;
- direct stale/revocation/creator-fail-closed tests.

**Preliminary impact boundary:** access, multiplayer/LIVE and bootstrap/migration/recovery authorization consumers.

**Dependencies:** consumes native IDs/routes from `CD-02`/`CD-04`; joins execution/persistence where an operation mutates state. Supplies authorization/currentness to `CD-07`, `CD-11`, `CD-12` and `CD-13`.

**Protected invariants:** login/repository permission/card/session/cache/scalar freshness do not authorize; no login-rename inference or stable-ID authority transfer; no wildcard LIVE claim, overlap, fallback, branch deletion, rekey or transport-order chronology; no global split-party synchronization.

**Out of scope:** automatic creator recovery claim; generic ACL replacement.

---

## CD-09 — Role containment, typed handoffs and protected emission

**Primary readiness:** `R27-R054..R27-R057`.

**Goal:** install the single owner-equivalent role/recipient containment route and realize ephemeral role-runtime controls, phase rebind, typed handoffs and protected emission.

**Expected owner/consumer surfaces:**

- `GAME/CORE/AI_REASONING.md` containment owner projection and invoking runtime surfaces;
- TurnEnvelope/profile/bundle/trace control structures;
- role rebind and typed handoff validators;
- Narrator/protected emission boundary;
- direct raw-bundle/recipient-leak/source-escalation/rebind tests.

**Preliminary impact boundary:** role-context/orchestration/output consumers only; no durable role/session/memory record.

**Dependencies:** can begin from accepted owners in parallel. Integrates with `CD-10` Context Runtime for assembled role packets and with `CD-11`/`CD-12` for multiplayer/Story consumers.

**Protected invariants:** physical co-presence is not eligibility; no role-agent topology, persistent context record, generic role-result bus, same-envelope Story feedback or secret delivery through diagnostics/tools/maintenance.

**Out of scope:** Context Runtime selection/budget algorithm; Story authority.

---

## CD-10 — Bounded Context Runtime: discovery, allocation, retrieval and trace

**Primary readiness:** `R27-R059`, `R27-R060`, `R27-R097`, `R27-R105..R27-R107`, `R27-R117`, `R27-R119`, `R27-R120`, `R27-R124`, `R27-R125`, `R27-R127`, `R27-R134`, `R27-R135`, `R27-R138`, `R27-R140`, `R27-R144`, `R27-R145`.

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

**Preliminary impact boundary:** ephemeral context runtime, direct owner readers and diagnostics; native state remains authoritative.

**Dependencies:** consumes native owners from `CD-02`/`CD-03` and role containment from `CD-09` at integration. `R097` requires history/continuity plus bounded Context Runtime; it does not require `CD-12` Commentator.

**Protected invariants:** no durable context/memory/vector/graph/worker/fairness record; no keyword-only or unbounded recursive activation; no silent partial critical packet; no copied fixed quotas/provider-percentage hard target; no textual mention treated as knowledge; no targeting eligibility bypass; no linear all-PC loading; no whole-history scan.

**Out of scope:** native canon mutation; Commentator cache/control; real-host empirical tuning until applicable proof trigger.

---

## CD-11 — Collaboration and multiplayer coordination lifecycle

**Primary readiness:** `R27-R081`, `R27-R082`, `R27-R121`, `R27-R123`, `R27-R141..R27-R143`, `R27-R146`.

**Goal:** realize only admitted agency-dependent collaboration state, typed channels/modes, generation/currentness transitions, recipient-safe catch-up and bounded collective-input behavior.

**Expected owner/consumer surfaces:**

- collaboration obligation/generation/input/route schemas;
- PLAYER routing companion fields where owner-approved;
- authorization/association/close/handoff/currentness transitions;
- typed OOC/diegetic/actionable-intent channels;
- independent/collective/native-ordered coordination modes;
- recipient-specific catch-up and bounded collective windows;
- direct stale-generation/agency/close-race/channel tests.

**Preliminary impact boundary:** collaboration/multiplayer owner surfaces and direct Story/Dramaturg consumers; no generic routing service.

**Dependencies:** native schema joins `CD-02`; authorization/currentness joins `CD-08`; role/recipient containment joins `CD-09`; execution integration uses `CD-05` only when an admitted collective action resolves into mechanics.

**Protected invariants:** no transcript coordinator, collaboration authority, registry/index/scheduler/heartbeat, generic input queue/broker, timeout/debounce correctness, arrival-order authority, universal active-player gate or private-input disclosure.

**Out of scope:** Story canon, global planning graph, future measured optimization until WP-24 trigger.

---

## CD-12 — Story/T0/Commentator and retained multiplayer Dramaturg projections

**Primary readiness:** `R27-R051`, `R27-R084`, `R27-R085`, `R27-R099`, `R27-R102`, `R27-R131`.

**Goal:** realize the noncanonical Story projection, sparse event-time T0 basis consumption, self-contained baseline Commentator eligibility/control projection and exactly the accepted multiplayer Dramaturg horizons.

**Expected owner/consumer surfaces:**

- Story root/scaffold and projection-state/unit schemas;
- Story producer linking EVENTS/NARRATIVE as accepted by owner contracts;
- SemanticEvent T0 retained-factor schema/serialization/validation and bounded discovery support;
- Commentator snapshot/control producer, deterministic pre-LLM filter and isolated cache;
- `DRAMATURG/SHARED.yaml` and `DRAMATURG/PLAYERS/<player_id>.yaml` only for accepted multiplayer retained horizons;
- direct T0/T1, local eligibility/control, no-native-fallback and no-authority tests.

**Preliminary impact boundary:** Story/T0/Commentator projection and fixed Dramaturg paths. Native history, disclosure, access and gameplay canon remain authoritative.

**Dependencies:** `R099` T0 basis precedes the qualifying Story/Commentator consumer; Story root/state joins `CD-02`; native history/event production uses `CD-03`/`CD-05` as applicable; access/currentness and recipient constraints join `CD-08`/`CD-09`; retained multiplayer Dramaturg joins `CD-11`.

**Protected invariants:** no Story/history/ACL/canon authority; no mutable T1 substitute for T0; no hidden reasoning/current-pointer substitute; zero extra serial LLM/tool/remote/publication/irrelevant-turn work for ordinary capture; no native-only baseline fallback for accepted Commentator route; no Story feedback into same envelope; no single-player durable Dramaturg without a new admitted consumer trigger.

**Out of scope:** writer-specific partition/rollover until `R093/R094/R095/R103` trigger; generic narrative dynamics framework.

---

## CD-13 — Bootstrap, onboarding and product-level campaign consumers

**Primary readiness:** `R27-R086`, `R27-R087`, `R27-R098`.

**Goal:** realize bootstrap/package lifecycle seams, provisional onboarding/retrospective product wiring and the accepted save-and-exit flow without inventing campaign lifecycle semantics.

**Expected owner/consumer surfaces:**

- bootstrap/campaign-menu/package-currentness consumers;
- provisional onboarding/READY_PC integration using existing native owners;
- product retrospective/save/session-return wiring;
- save-success -> session-local clear -> same-chat campaign menu route;
- multiplayer non-interference and truthful failed/indeterminate-save handling.

**Preliminary impact boundary:** bootstrap/session/menu consumers and direct acceptance scenarios; no release execution.

**Dependencies:** consumes `CD-02`/`CD-03` identity/onboarding contracts, confirmed save result from `CD-06`, access/LIVE behavior from `CD-08` when multiplayer applies, and `CD-10` for ordinary retrospective context where needed.

**Protected invariants:** no complete-sheet prerequisite; no context clear before confirmed save success; no clearing principal/durable campaign state; no inferred pause/completion/archive/membership leave/PC-control transfer/campaign-wide stop.

**Out of scope:** release candidate/fresh-Project release proof (`R091/R092`), creator automatic recovery, migration execution.

---

## CD-14 — Integrated deterministic/scenario proof attachment and acceptance matrix

**Primary readiness:** `R27-R023`, `R27-R031`, `R27-R032`, `R27-R041`, `R27-R058`, `R27-R061`, `R27-R068`, `R27-R071`, `R27-R077`, `R27-R080`, `R27-R083`, `R27-R088`, `R27-R089`.

**Goal:** attach proof-only readiness to the exact realized targets, ensure deterministic/static/schema evidence is not over-credited as behavioral proof, and provide the cross-unit verification joins needed by later detailed plans.

**Expected owner/consumer surfaces:**

- focused deterministic/static/schema/unit/integration tests adjacent to their implementation units;
- scenario/adversarial acceptance fixtures/harnesses already admitted by WP-22/current toolchain;
- maintenance-audit/schema/catalog checks where applicable;
- proof mapping artifacts/commands only; no independent runtime subsystem.

**Preliminary impact boundary:** tests/verification tooling and necessary fixtures; any production-code change belongs to the implementation unit whose behavior is being fixed.

**Dependencies:** `PROOF_AFTER_TARGET` for each named leaf. `CD-14` is not one late serial testing phase: its checks are planned as target-local RED/GREEN/acceptance steps and only the final cross-unit acceptance join waits for all applicable targets.

**Protected invariants:** no proof channel may self-authorize semantics; no source/build/static evidence substitutes for supported-target behavior, empirical or release evidence; no future-only release/real-target route is activated.

**Out of scope:** Protocol-4 on a non-existent target, release acceptance, performance calibration not yet triggered.

---

# 4. Candidate dependency graph

The candidate unit graph preserves P3 and intentionally maximizes safe parallelism.

```text
CD-01                       # parallel projection-repair root

CD-02 ─┬─> CD-04 ─┬─> CD-05 ─┬─> CD-06 ─┬─> CD-07
       │           │          │          │
       │           │          │          └────> CD-13
       │           │          ├───────────────> CD-11 (mechanics join only)
       │           │          └───────────────> CD-12 (native event/execution join only)
       │           ├──────────────────────────> CD-10 (native-load substrate)
       │           └──────────────────────────> CD-08
       │
       ├─> CD-03 ─────────────────────────────> CD-10
       │                    └──────────────────> CD-12 (history/T0 inputs as applicable)
       ├──────────────────────────────────────> CD-11
       └──────────────────────────────────────> CD-12

CD-08 ────────────┬───────────────────────────> CD-07 (selected-LIVE recovery)
                  ├───────────────────────────> CD-11
                  ├───────────────────────────> CD-12
                  └───────────────────────────> CD-13

CD-09 ────────────┬───────────────────────────> CD-10
                  ├───────────────────────────> CD-11
                  └───────────────────────────> CD-12

CD-11 ────────────────────────────────────────> CD-12 (retained multiplayer Dramaturg only)

CD-10 ────────────────────────────────────────> CD-13 (ordinary retrospective consumer)

CD-01..CD-13 applicable targets ──────────────> CD-14 acceptance joins
```

Interpretation rules:

- arrows denote hard prerequisites or required integration joins from P3, not blanket source-code sequencing;
- when a unit consumes a stable accepted interface, implementation may proceed in parallel and the arrow is enforced at integration/acceptance;
- `CD-14` does not delay test writing; test-first work remains inside every unit and `CD-14` owns only proof attachment/completeness/integrated acceptance.

No executable cycle is introduced by this decomposition.

---

# 5. Preliminary Impact-Envelope routing

Detailed Impact Envelopes are gated until critic PASS, but the candidate must expose likely blast radius now.

| Unit | Expected owner families to change | Expected consumer families | Architecture-sensitive surfaces | Explicitly protected/out of scope |
|---|---|---|---|---|
| CD-01 | instruction/current projections only | install/CORE readers | active shipped instructions | no new runtime authority |
| CD-02 | schema/catalog/native record projections | routing/HOT/context/collab/Story | information ownership; native family identity | no generic state service/parallel canon |
| CD-03 | Actor/continuity runtime owners | context/history/bootstrap | epistemic split; player agency | no generic memory/NPC simulation |
| CD-04 | routing/index/HOT implementation | execution/persistence/recovery/context | authority/currentness/transaction boundaries | no index/cache authority, global transaction |
| CD-05 | execution/failure/output consumers | persistence/recovery/collab/Story | determinism, RNG, commit, emission | no replay/global failure system |
| CD-06 | SAVE/publication/currentness | recovery/bootstrap/product flow | Git publication/CAS/currentness | no force/alternate transport/global frontier |
| CD-07 | recovery/checkpoint/temporal | LIVE/product/runtime | recovery authority/chronology | no scheduler/global clock/RecoveryCut |
| CD-08 | access/LIVE/creator consumers | recovery/collab/Story/bootstrap | authorization/currentness/provenance | no login substitution/global ACL |
| CD-09 | role-context/emission | context/collab/Story | eligibility/recipient containment | no durable role memory/role-result bus |
| CD-10 | Context Runtime | Master retrospective/role consumers | source eligibility/boundedness | no durable context owner/whole-history scan |
| CD-11 | collaboration/multiplayer | Story/Dramaturg/mechanics | agency/current generation/recipient safety | no transcript coordinator/queue/broker |
| CD-12 | Story/T0/Commentator/Dramaturg projection | Commentator/multiplayer planning | native history/disclosure/access | no Story canon/ACL/native fallback |
| CD-13 | bootstrap/session/menu product consumers | user-facing campaign flows | save truth/currentness/lifecycle | no inferred campaign lifecycle transition |
| CD-14 | proof/verification surfaces | all applicable units | proof-channel separation | no independent runtime subsystem |

Any implementation plan that discovers a blast radius outside these admitted categories must trigger the System Impact Gate before silently widening the unit.

---

# 6. Future-trigger preservation

The candidate decomposition creates **no** current task for:

- release-only `R002`, `R024`, `R091`, `R092`;
- real-target-only `R005`, `R090`;
- writer-triggered `R093`, `R094`, `R095`, `R103`;
- focus-risk-triggered `R096`, `R101`.

Those routes remain in the planning coverage matrix as trigger-owned future obligations. A later trigger may produce a new bounded task/unit; it is not silently folded into `CD-01..CD-14` now.

All 79 explicit no-work terminals remain no-work. `R004` remains removed.

---

# 7. Cross-unit coupling tests for the critic

The independent Decomposition Critic should specifically attempt to reject the candidate on these questions:

1. Is `CD-02` too broad, or does a further split of information/schema/catalog families reduce coupling without duplicating owner obligations?
2. Does `CD-03` incorrectly combine Actor runtime representation and continuity/history behavior that should execute independently?
3. Is `CD-04` an infrastructure catch-all, or is route/index/HOT one bounded substrate with coherent integration tests?
4. Are execution and failure/output seams in `CD-05` properly owner-local, or does the unit hide a rejected global failure abstraction?
5. Does `CD-07` improperly couple recovery/checkpoint and temporal/thread realization?
6. Does `CD-08` combine access/LIVE and creator provenance only as consumers of one authorization seam, or should creator-specific work move to `CD-13`?
7. Is `CD-10` too large given retrieval, budgeting, trace and retrospective consumer duties?
8. Does `CD-12` correctly keep native T0 production/history authority outside Story while still guaranteeing Commentator self-containment?
9. Does `CD-13` hide product lifecycle decisions behind bootstrap/session wiring?
10. Does `CD-14` accidentally become a late test phase rather than proof attachment to target-local TDD?
11. Are any P3 joins missing, falsely serialized, or silently cross-plan?
12. Is any future-triggered route prematurely activated or any no-work terminal resurrected?
13. Are all 133 primary leaf assignments semantically faithful and exactly one-per-leaf?
14. Are any implementation units too large for independent TDD/review/commit checkpoints?

The critic has authority to reject the entire decomposition and propose a different split. The author of this artifact does not pre-approve any unit boundary.

---

# 8. Exact primary coverage ledger

```text
CD-01  7  : R001 R003 R033 R043 R047 R048 R050
CD-02 24  : R006-R022 R025-R027 R049 R052 R053 R062
CD-03 19  : R028-R030 R104 R108-R111 R113-R116 R126 R128-R130 R132 R136 R139
CD-04  5  : R063-R067
CD-05 15  : R034-R040 R042 R044-R046 R112 R118 R133 R137
CD-06  2  : R069 R070
CD-07  5  : R072-R076
CD-08  4  : R078 R079 R100 R122
CD-09  4  : R054-R057
CD-10 18  : R059 R060 R097 R105-R107 R117 R119 R120 R124 R125 R127 R134 R135 R138 R140 R144 R145
CD-11  8  : R081 R082 R121 R123 R141-R143 R146
CD-12  6  : R051 R084 R085 R099 R102 R131
CD-13  3  : R086 R087 R098
CD-14 13  : R023 R031 R032 R041 R058 R061 R068 R071 R077 R080 R083 R088 R089
----------------------------------------------------
TOTAL    133 / 133
DUPLICATE_PRIMARY_ASSIGNMENTS: 0
UNASSIGNED_ACTIVE_READINESS: 0
```

Secondary consumer/join relationships are recorded in §§3-4 and P3; they do not alter this primary accounting.

---

# 9. Candidate exit state

```text
CANDIDATE_DECOMPOSITION_STATUS: READY_FOR_INDEPENDENT_CRITIC
CANDIDATE_UNITS: 14
ACTIVE_READINESS_PRIMARY_ACCOUNTING: 133 / 133
UNASSIGNED_ACTIVE_READINESS: 0
DUPLICATE_PRIMARY_ASSIGNMENTS: 0
TRIGGER_GATED_PREMATURE_TASKS: 0
NO_WORK_PREMATURE_TASKS: 0
R27_R004_PRESENT: NO
KNOWN_EXECUTABLE_CYCLES: 0
HIDDEN_HUMAN_DECISION_IDENTIFIED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
DETAILED_EXECUTABLE_PLAN_AUTHORING_AUTHORIZED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
NEXT_GATE: isolated independent Decomposition Critic
```

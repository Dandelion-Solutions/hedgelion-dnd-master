# HDM v1 Implementation Plan — Authoritative Wave Index

Status: **SENIOR-APPROVED / PRODUCTION IMPLEMENTATION AUTHORIZED**

Production implementation: **AUTHORIZED**, subject to `DEV/CURRENT_PROGRESS.md`, named producer checkpoints, wave-level Senior integration gates and `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`.

## 1. Sole current planning route

This file is the only entry point for HDM v1 production implementation planning. The plan is organized by dependency waves. There are no mandatory overlays, precedence amendments, alternate RD plans or separately executable proof ledgers.

Read and execute these files in order:

1. `implementation-plan-execution-contract.md` — global task, currentness, TDD, publication, impact and version rules.
2. `implementation-wave-01-owner-native-foundations.md` — independent owner-local contracts and early producer checkpoints.
3. `implementation-wave-02-execution-durability-recovery.md` — typed interpretation, deterministic execution, durability, publication and exact recovery.
4. `implementation-wave-03-principal-live-temporal.md` — principal/PLAYER authority, LIVE identity/currentness/native state and temporal handoff.
5. `implementation-wave-04-collaboration-context-story.md` — collaboration, bounded context, protected emission, native history, Story, T0, Commentator and Dramaturg.
6. `implementation-wave-05-machine-bootstrap-integration.md` — final 17+17 machine integration, bootstrap/product paths and all shared physical writers.
7. `implementation-wave-06-proof-senior-handoff.md` — package proof, exact-head validation and independent Senior handoff.
8. `implementation-plan-traceability.md` — non-normative consolidation and deletion evidence.

Files 1–7 form the complete executable plan. File 8 proves where the retired planning corpus was absorbed; it cannot add or override implementation work.

Future planning repairs modify the applicable stable wave file and this index in one coherent checkpoint. Do not create a dated addendum, overlay, competing master plan or alternate execution graph.

## 2. Authority and baseline

The plan derives from the accepted current architecture/specification owners, especially:

- `DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md`;
- the exact `R27-R###` item evidence in `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md`;
- current domain, access, LIVE, persistence, temporal, collaboration, Story, bootstrap, versioning and Product Owner owners routed by `DEV/PROJECT_MAP.md`;
- `DEV/PRODUCT_OWNER_INPUT.md`, including PO-004 clean-slate v1, PO-005 fail-closed creator-login policy with login-facing invitation plus stable-account-ID PLAYER binding, and PO-006 absolute branch/ref deletion prohibition;
- `AGENTS.md`, `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` when applicable and `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`.

Consolidation source HEAD: `8636369cbb9f2d8fb9b90a92cffbc0ccdddd3d4d`.

The source HEAD is provenance for this author-side consolidation. A production worker records and uses the fresh exact implementation-start HEAD after Senior GO. It never treats a cached checkout or this historical consolidation SHA as current remote state.

## 3. Preserved accounting

```text
READINESS_RECORDS: 145
ACTIVE: 133 = 116 direct + 9 pure proof + 8 composite parents
TRIGGER_GATED: 12
EXPLICIT_NO_WORK_TERMINALS: 79 source items
R004: ABSENT / MUST NOT BE RESURRECTED
WORLD_FAMILIES: 17
RUNTIME_FAMILIES: 17
POST_WP27_PROOF_ROWS: PG06..PG21, PG23..PG37 as enumerated in Wave 06
```

The twelve trigger-gated routes remain dormant until their exact owner-defined empirical, supported-target, writer/focus-risk or release trigger exists. A wave assignment does not activate them. `world.faction` is a facet/classification of `world.organization`, not an independent v1 family.

## 4. Readiness ownership map

This table preserves the exact active planning atoms while allowing their tasks to execute in dependency order.

| Owner lane | Direct readiness | Composite/proof contribution | Primary wave(s) |
|---|---|---|---|
| shipped/current projections | R001, R003, R033, R043, R047, R048, R050 | currentness and shared shipped-byte inputs | 01, 05, 06 |
| information/knowledge/disclosure/message | R007, R008, R009, R017, R049, R052 | R006.INFO, R016.INFO, R018.INFO, R053.INFO, R062 knowledge/disclosure/message | 01, 03, 04, 05, 06 |
| Actor/Asset/Effect | R025–R028, R104, R108–R111, R113–R116, R126, R128–R130, R132, R136 | R006.ACTOR, R016.ACTOR, R018.ACTOR, R029.ACTOR, R062 actor/effect | 01, 04, 06 |
| native routing/index/HOT/allocator | R015, R063–R067 | R018 route/root | 01, 02, 03, 05, 06 |
| deterministic execution | R034, R035, R036, R042, R046, R112 | R016.EXECUTION, R018.EXECUTION, R062 lifecycle | 02, 06 |
| durability/publication | R037, R045, R069, R070, R071 | R029.DURABILITY | 02, 03, 04, 06 |
| recovery/checkpoint/maintenance | R011, R012, R038, R072, R073, R074 | exact recovery joins | 02, 03, 06 |
| temporal/thread/current state | R010, R039, R075, R076, R077 | R006.THREAD_VISIBILITY, R016.TEMPORAL, R018.TEMPORAL, R062.TEMPORAL_BINDING, R122.CHRONOLOGY | 01, 03, 05, 06 |
| principal/PLAYER/LIVE | R013, R014, R019, R020, R040, R078, R079, R080 | R053.LIVE, R016.LIVE, R018.LIVE, R122.CURRENTNESS_SCENE | 01, 03, 05, 06 |
| role containment/handoffs/emission | R054–R057, R118, R133, R137 | R058 and context joins | 01, 02, 04, 06 |
| bounded Context Runtime | R059, R060, R097, R105–R107, R117, R119, R120, R124, R125, R127, R134, R135, R138–R140, R144, R145 | R087.RETROSPECTIVE, R122.CONTEXT | 01, 04, 06 |
| collaboration/multiplayer | R021, R044, R081, R082, R083, R121, R123, R141–R143, R146 | R016.COLLAB, R018.COLLAB, R122.COLLABORATION_BRIDGE | 04, 05, 06 |
| native history/Story/T0/Commentator/Dramaturg | R022, R051, R084, R085, R099, R102, R131 | R016.STORY, R018.STORY, R062.SEMANTIC_EVENT_HISTORY, R087.SEMANTIC_EVENT_T0 | 01, 04, 05, 06 |
| bootstrap/onboarding/product | R030, R086, R098, R100 | R029.ONBOARDING, R087.SAVE_SESSION_MENU | 01, 05, 06 |
| catalog runtime binding/gap evidence | post-WP27 PG11, PG14, PG18, PG23 and affected readiness joins | R018 runtime/catalog proof | 01, 02, 05, 06 |
| final world/runtime machine integration | post-WP27 PG08, PG10, PG12, PG13, PG16, PG32–PG34 | R018 final world/runtime closure | 01, 05, 06 |

The exact semantic owner remains above this planning projection. A worker must follow the named readiness record to its native owner if any detail conflicts or has legitimately advanced.

## 5. Wave dependency graph

Wave numbers express the implementation route, but do not serialize independent lanes inside a wave. A later-wave task may start when every checkpoint it explicitly consumes is GREEN and published; it does not wait for unrelated work in the preceding wave.

```text
Wave 01 owner-native foundations
  -> typed interpreter/catalog/owner contracts
  -> Wave 02 accepted execution -> durability/publication -> exact recovery

Wave 01 early campaign identity + route/scaffold contracts
+ Wave 02 publication/recovery primitives
  -> Wave 03 principal/LIVE/temporal acceptance

Wave 01 owner contracts
+ Wave 03 current authority
  -> Wave 04 collaboration/context/story integration

Wave 01 local schema deltas
+ Wave 02/03/04 integration outputs
  -> Wave 05 single final shared writers + bootstrap/product closure

Waves 01..05 realized targets
  -> Wave 06 package proof + exact-head validation + Senior re-review
```

Mandatory hard/join edges include:

- typed `InterpreterResult` -> exact `BoundCatalogContext` validation -> catalog-backed `RuntimeCommand` acceptance;
- accepted execution -> durability/publication -> recovery, with the same frozen RNG, identity, catalog basis and adjudication basis;
- early RD-14 campaign identity + RD-06 identity immutability + RD-09 route/order/cursor checkpoints -> source-native LIVE ID acceptance;
- campaign/LIVE route selection and absorption -> same-closure temporal, operational-root and route-companion handoffs;
- current PLAYER/access-policy mutation -> one after-authority collaboration reconciliation -> one campaign publication closure;
- W04.T07 first RED is preceded by the mandatory fresh CLS <-> HDM preflight in Wave 04: current public Story/Commentator SCC owner + current private CLS integration/audit state are reconciled; private CLS-only repair debt does not block HDM, but any current requirement for a new/changed public-HDM semantic owner, persisted/interface contract or incompatible Story/T0/control law triggers the System-Impact Gate before implementation;
- information/thread/PLAYER/collaboration/LIVE identifier deltas -> W05.T01 owner-local strict schema/wrapper inputs GREEN at `W05_OWNER_LOCAL_STRICT_SCHEMA_WRAPPER_INPUTS_READY` -> `JOIN_BEFORE_INTEGRATION` -> W05.T02 final shared write at `RD16_SHARED_MACHINE_INTEGRATION_READY`;
- W05.T02 final shared bytes + the affected final schema/realization checkpoints -> W06.T02 item-bound world/runtime R018 proof; neither final proof nor T02 integration/conformance is a prerequisite of T01 closure;
- every package proof -> its realized target, never the reverse.

## 6. Package-wide invariants

- Native semantic owners remain authoritative. Cache, index, Story, checkpoint, route companion, planning file and proof ledger remain derived.
- v1 is clean-slate relative to unreleased v0.8. Do not add migration, dual-read or compatibility aliases solely for superseded pre-release shapes.
- GitHub login is retained for human-facing selection, invitations and display. Verified stable account ID is stored in the PLAYER binding. Login rename continuity and automatic creator transfer are unsupported; creator uncertainty fails closed to read-only behavior.
- Email is not an identity or invitation authority.
- Branch/ref deletion is never invoked. Force update is forbidden.
- Known-ID reads derive bounded native routes; broad scans, latest-looking records and physical ordering never become normal authority.
- Accepted mechanics are not replayed and fixed RNG is not rerolled on retry/recovery.
- LIVE currentness is exact-source CAS evidence. Prepared candidate existence is not authority.
- Story, Commentator, Dramaturg and catch-up material are projections with their own privacy/currentness rules; none becomes history, knowledge, ACL or gameplay truth.
- Private CLS implementation defects are not public-HDM blockers by default; only a fresh cross-project conflict that changes public semantic ownership, persisted/interface policy or the accepted Story/T0/control contract may stop the implicated HDM task through the System-Impact Gate.
- Every task runs the Version Impact Gate and every shared file has one final physical writer/checkpoint.
- R018 runtime proof consumes the exact 17-row family/schema/root/realization matrix in Wave 05 and the negative witnesses in Wave 06. Count equality, catalog admission, a world-only proof or a catalog-gap-only proof cannot close the composite.
- No future-task intentional RED tests are published. A task creates its RED witness with the mechanism it turns GREEN.

## 7. Exact version targets at the consolidation baseline

Retained GAME schemas:

```text
checkpoint 3 -> 4
current_state 2 -> 3
thread 1 -> 2
live_scene 1 -> 2
index 1 -> 2
scene 2 -> 3
location 1 -> 2
event 1 -> 2
lore 1 -> 2
player 1 -> 2
campaign_manifest 4 -> 5
```

Shared identifier-policy machine:

```text
identifier-policies.schema_version 2 -> 3
catalog_generation remains 2
```

Wave 03 contains the closed per-family `live_birth` disposition table; Wave 05 performs its one shared machine/catalog write.

Material CORE modules:

```text
BOOTSTRAP_RUNTIME 0.8.8 -> 1.0.9
RANDOMNESS        0.1.2 -> 1.0.3
EXPLORATION       0.1.1 -> 1.0.2
STORAGE           1.0.1 -> 1.0.2
SAVE_CONTRACT     0.2.1 -> 1.0.2
PERSISTENCE       1.0.3 -> 1.0.4
CHRONOLOGY        0.1.1 -> 1.0.2
PROCESSES         0.1.2 -> 1.0.3
AI_REASONING      0.1.3 -> 1.0.4
LIVE_SCENE        1.0.3 -> 1.0.4
MULTIPLAYER       0.1.7 -> 1.0.8
CAMPAIGN_SETUP    1.0.3 -> 1.0.4
SESSION           1.0.1 -> 1.0.2
PLAY_POLICY       0.8.4 -> 1.0.5
CORE_INDEX        0.3.1 -> 1.0.2
ADJUDICATION      1.0.2 -> 1.0.3
```

These are exact targets for the recorded consolidation baseline. At implementation time the worker fresh-reads each namespace. If an accepted intervening change has already advanced a target, apply the same owning version law and record the reconciled transition; never blindly downgrade, double-bump or preserve a stale number.

## 8. Completion route

The plan is ready for production execution only after all of the following are true at one exact public HEAD:

1. the stable package files above are internally consistent and contain no dependency on a retired planning file;
2. maintenance audit and full `DEV/TESTS` discovery are GREEN for that HEAD;
3. independent Senior re-review returns PASS / GO for the complete consolidated package;
4. `DEV/CURRENT_PROGRESS.md` records that exact gate result.

Until then, implementation, migration execution, release execution and gameplay bootstrap remain unauthorized.

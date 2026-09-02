# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Source Manifest

Status: **STEP-1 TASK-SPECIFIC SOURCE MANIFEST — WHOLE-PROJECT CRITIC + SENIOR SR14-01..03 REPAIRS APPLIED / READY FOR MANDATORY SENIOR REVIEW**

Date: 2026-09-02

Owning Task Brief:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-task-brief.md`

Mandatory whole-project Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-task-brief-critic.md`

Separate post-critic Senior-recovery record:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-senior-recovery-source-graph-omissions.md`

---

## 1. Purpose and classification

This manifest defines the current task-specific dependency/evidence subgraph for WP-14 Step 1. It was built from the current `DEV/PROJECT_MAP.md` and then expanded through actual owning/consumer surfaces discovered in the repository.

It is **not closed-world**. Step 2 must extend it if item-level extraction reveals another real owner, consumer, schema, template, test, tool or maintenance route required by the recovery/checkpoint/session/repair closure.

Roles:

- **CANONICAL / OWNING** — current semantic or implementation-facing architecture authority;
- **CANONICAL INTEGRATION / OWNING** — current accepted cross-slice integration authority;
- **OWNER-APPROVED CLARIFICATION / OWNING** — current explicit owner-approved constraint that supersedes broader older design language for the stated topic;
- **R2.7 UPSTREAM / OWNING** — closed WP-10..WP-13 realization authority consumed without reopening;
- **CURRENT-PROGRESS / PROCESS AUTHORITY** — process/gate/current-state owner, not semantic authority;
- **DERIVATIVE LOCATOR / INDEX** — routing aid only;
- **IMPLEMENTATION / MACHINE CONTRACT** — current shipped/runtime/schema/template/tool surface that may lag architecture;
- **IMPLEMENTATION / TEST CONTRACT** — current regression expectation that must be reconciled against canonical architecture;
- **CURRENT SUPPORT / MAINTENANCE CONTRACT / PROPOSAL** — direct current support/recovery/repair consumer whose own repository status is proposal/internal-control, not semantic recovery authority;
- **DESIGN PROVENANCE** — historical derivation/recovery evidence, not default semantic owner.

Inspection disposition:

- **INSPECTED FOR STEP 1** — current source was read deeply enough to establish role/framing/debt;
- **REQUIRED STEP-2 INSPECTION** — Step 2 must extract/reconcile relevant normative items before synthesis;
- **CONDITIONAL STEP-2 INSPECTION** — inspect when discovered dependency proves material;
- **ROUTING ONLY** — locator, cannot support semantic claims alone.

---

## 2. Governance, process and current state

| Source | Role | WP-14 relevance | Disposition |
|---|---|---|---|
| `AGENTS.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | Public-repo boundaries, taxonomy, **development-agent** Connector transport, verification discipline. This is not the gameplay/runtime repository transport owner. | INSPECTED FOR STEP 1; re-read if changed. |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | ChatGPT Connector-only **development-agent** workflow and publication/read-back requirements. Do not use it as gameplay/recovery transport authority. | INSPECTED FOR STEP 1; re-read if changed. |
| `DEV/DESIGN_PROCESS.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | Eight-step loop, Source Manifest/evidence gates, decision rights. | INSPECTED FOR STEP 1 / BINDING. |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | Whole-project critic and mandatory Senior stop after Step 1. | INSPECTED FOR STEP 1 / BINDING. |
| `DEV/PROJECT_MAP.md` | DERIVATIVE LOCATOR / INDEX | Initial dependency route for persistence/recovery/session/integrity/bootstrap/tests. | INSPECTED FOR STEP 1 / ROUTING ONLY. |
| `DEV/CURRENT_PROGRESS.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | Sole global current cursor; currently authorizes only the WP-14 Step-1 Senior repair and mandatory Senior gate. | INSPECTED FOR STEP 1; re-read before writes/transitions. |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | DERIVATIVE LOCATOR / INDEX | R2.7 sequence/scope/dependency context. | INSPECTED FOR STEP 1 / ROUTING ONLY. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | CURRENT-PROGRESS / PROCESS AUTHORITY (task-local) | Durable WP cursor and preserved forward obligations. | INSPECTED FOR STEP 1; synchronize at closure. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | R2.7 domain audit protocol and evidence expectations. | INSPECTED FOR STEP 1 / BINDING. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` | DESIGN PROVENANCE / PROGRAM INPUT | WP-14 program questions and architecture↔machine proof objective. | INSPECTED FOR STEP 1. |

---

## 3. Primary canonical recovery/currentness owners

Step 2 must perform item-level extraction from these owners. Summaries below are routing aids only.

| Source | Role | Required WP-14 extraction | Step-1 status |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` | CANONICAL / OWNING | RuntimeCommand/Procedure/Resolution/Continuation continuity, fixed RNG, accepted IDs, mandatory child/firing identities, idempotent resume/no replay. | REQUIRED STEP-2 INSPECTION. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md` | CANONICAL / OWNING | Domain-typed currentness markers; no implicit cross-domain order; session/checkpoint/cached HEAD not semantic authority. | REQUIRED STEP-2 INSPECTION where currentness/frontier vocabulary participates. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md` | CANONICAL / OWNING | RRC definition, bounded roots, exact pins, native owner preservation, no invented lost HOT, interpretation closure, live-scope source selection. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md` | CANONICAL / OWNING | Armed independently-due owner routing, occurrence identity/materialization, accepted execution continuity, fixed RNG, no generic pending queue. | REQUIRED STEP-2 INSPECTION. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md` | CANONICAL / OWNING | Session/host non-authority, controlled handoff vs unexpected loss, scoped quiescence, native-owner resume, session metadata limits. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md` | CANONICAL / OWNING | Actual promised durable source closure; checkpoint not save authority; lost unpublished state cannot be invented. | REQUIRED STEP-2 INSPECTION for recovery promise relation. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md` | CANONICAL / OWNING | Campaign authoritative ref selection, ambiguous publication evidence, current closure proof, crash after publication, no journal. | REQUIRED STEP-2 INSPECTION. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md` | CANONICAL / OWNING | **Primary WP-14 semantic owner:** current-authority-first recovery, exact-source pinning, root hydration, optional checkpoint, checkpoint field dispositions, READY/RETRY/BLOCKED. | INSPECTED FOR STEP 1 / FULL RELEVANT STEP-2 LAW ACCOUNTING REQUIRED. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md` | CANONICAL / OWNING | Live current truth routing, ACTIVE/CLOSED_UNABSORBED recovery, exact-source currentness, no campaign fallback. | REQUIRED STEP-2 INSPECTION; WP-14 composes, WP-16 owns final live machine. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md` | CANONICAL / OWNING | Checkpoint/Git/event/session order cannot become fictional chronology; required chronology evidence remains owner-typed. | REQUIRED STEP-2 INSPECTION where checkpoint/world_time/temporal resume participates. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | CANONICAL INTEGRATION / OWNING | Integrated recovery/concurrency attacks, physical-feasibility guard, zero-model-memory recovery from current native routing/RRC. | REQUIRED STEP-2 INSPECTION. |

### Conditional neighboring owners

| Source | Why conditional |
|---|---|
| Step-5.10 Story durability canonical spec | Only if a current recovery/repair consumer attempts to use Story as state authority. |
| Step-5.11 transcript/history retention canonical spec | Only when exact retained wording/history becomes irreducible accepted recovery evidence or repair evidence. |
| Step-5.12 host-delivery/disclosure canonical spec | Only if recovery must distinguish committed gameplay/disclosure from uncertain delivery. |
| Step-5.13 cleanup/orphan canonical spec | Only if repair/recovery depends on retired representations, protected historical evidence or stale live/ref cleanup. |

These remain subordinate to their native owners and cannot be imported wholesale as new WP-14 scope.

### R2.6 host/context and fixed gameplay repository transport owners

These sources are mandatory WP-14 evidence because recovery must remain valid when ambient host context is stale/foreign and because repository currentness/failure evidence is obtained through the already selected gameplay transport. They are deliberately separate from the development-agent Connector rules above.

| Source | Role | Required WP-14 extraction | Step-1 status |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | CANONICAL / OWNING | LAW R2.6-6: chat history, Project memory and ambient host/model context are not campaign canon/currentness/Actor/disclosure/collaboration/Story authority; routed semantic owners win. LAW R2.6-9 and acceptance obligation 16: fixed Connector gameplay transport and integrated currentness/CAS/conflict/failure evidence. | INSPECTED FOR SENIOR REPAIR / REQUIRED STEP-2 INSPECTION. |
| `DEV/docs/superpowers/design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md` | OWNER-APPROVED CLARIFICATION / OWNING | Supported gameplay/runtime path is fixed `deterministic Python/core -> GitHub Connector -> authoritative non-force ref transition`; no probe/fallback through `gh`, native remote Git, private HTTP/API/token paths, alternate App/MCP/backend, GitHub Actions or equivalent transport; missing required Connector capability is supported-profile capability failure. Extract exact pinned-ref/currentness/CAS/conflict/ambiguous-failure evidence obligations for recovery. | INSPECTED FOR SENIOR REPAIR / REQUIRED STEP-2 INSPECTION. |

Step 2 must preserve this separation explicitly: `AGENTS.md` and `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` govern **development-agent repository work**; the R2.6 sources above govern the **supported gameplay/runtime repository path** consumed by WP-14 recovery.

---

## 4. Closed R2.7 upstream realization owners

These are hard constraints, not candidates for casual redesign.

| Source | Role | WP-14 obligation |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-10-durable-campaign-record-family-completeness-canonical-spec.md` | R2.7 UPSTREAM / OWNING | `runtime.checkpoint`, `runtime.session` and admitted support/runtime families (including `runtime.maintenance_audit` where applicable) remain narrow typed families; recovery uses native owners/evidence without inventing snapshot/journal/repair mega-owners. |
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | R2.7 UPSTREAM / OWNING | Checkpoint route = `CHECKPOINTS`, no index; session route = `SESSIONS`, no index. **F03 -> WP-14:** current-route-first recovery + deterministic index rebuild. Known-ID reads use exact derived routes; index absence never proves semantic absence. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` | R2.7 UPSTREAM / OWNING | Cold recovery starts from current native authorities/exact pins; surviving SQLite is cache only after source-equivalence proof; recovery-attempt composition ephemeral; checkpoint optional evidence. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | R2.7 UPSTREAM / OWNING | Current compatible source composition proves durability; checkpoint never proves SAVE/handoff/current state; session/cached HEAD fields are not authority. **WP-13 forward obligation -> WP-14:** current-authority-first recovery/checkpoint machine. |

Reopen any of these only with explicit contradiction, new unsatisfied consumer or material insufficiency evidence.

---

## 5. Current shipped CORE machine owners/consumers

These are implementation evidence, not semantic authority where they conflict with canonical architecture.

| Source | Role | WP-14 Step-2 reconciliation target | Step-1 status |
|---|---|---|---|
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | IMPLEMENTATION / MACHINE CONTRACT | Existing selection barrier is useful, but post-selection startup currently says “latest checkpoint/hot STATE” and canon priority places checkpoint/STATE ahead of WORLD. Must be reconciled to current-authority-first/current-route-first recovery; checkpoint optional. Working-set `base_head_sha` remains observation/cache only. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `GAME/CORE/RUNTIME.md` | IMPLEMENTATION / MACHINE CONTRACT | Runtime currentness/resync/recovery behavior; verify no checkpoint/session/local-memory authority and no invented lost dirty state. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `GAME/CORE/SESSION.md` | IMPLEMENTATION / MACHINE CONTRACT | Session lifecycle/handoff/continuation prose; distinguish durable session coordination record from host/model memory and native recovery owners. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `GAME/CORE/INTEGRITY.md` | IMPLEMENTATION / MACHINE CONTRACT | Current canon-suspect/repair behavior, evidence requirements and scoped blocking; must not silently fall back to checkpoint/history. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `GAME/CORE/STORAGE.md` | IMPLEMENTATION / MACHINE CONTRACT | Campaign/native storage retrieval, current routing, checkpoint relation and local working-set semantics. | REQUIRED STEP-2. |
| `GAME/CORE/PERSISTENCE.md` | IMPLEMENTATION / MACHINE CONTRACT | Publication/crash outcome/currentness evidence consumed by recovery; no publication journal; runtime transport evidence remains fixed-Connector-path evidence. | REQUIRED STEP-2. |
| `GAME/CORE/SAVE_CONTRACT.md` | IMPLEMENTATION / MACHINE CONTRACT | Recovery/checkpoint cannot become save proof; explicit save promise remains WP-13/native durability owned. | REQUIRED STEP-2 where checkpoint/save text intersects. |
| `GAME/CORE/LIVE_SCENE.md` | IMPLEMENTATION / MACHINE CONTRACT | Current live route/source/closed-unabsorbed recovery behavior; no campaign fallback. | REQUIRED STEP-2 for live recovery boundary; final live machine WP-16. |
| `GAME/CORE/MULTIPLAYER.md` | IMPLEMENTATION / MACHINE CONTRACT | Campaign/live synchronization, stale sessions, authorization and shared-source currentness. | REQUIRED STEP-2 where recovery/session/currentness participates. |
| `GAME/CORE/CHRONOLOGY.md` | IMPLEMENTATION / MACHINE CONTRACT | Current chronology recovery representation; checkpoint/world/Git order cannot decide fictional chronology. | REQUIRED STEP-2 if chronology fields are retained/repaired. |
| `GAME/CORE/ENGINE_UPDATES.md` | IMPLEMENTATION / MACHINE CONTRACT | Open accepted work must retain compatible interpretation context across maintenance/recovery. | REQUIRED STEP-2 for runtime-switch/recovery edge. |
| `GAME/CORE/CAMPAIGN_OPERATIONS.md` | IMPLEMENTATION / MACHINE CONTRACT | Pause/resume/archive/repair operations may consume session/recovery state; inspect if actual operation paths depend on checkpoint status. | CONDITIONAL STEP-2. |

---

## 6. Current schemas, templates and generator surfaces

| Source | Role | Evidence/debt | Step-1 status |
|---|---|---|---|
| `GAME/SCHEMA/checkpoint.schema.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Current fields include generic `valid_through_event_id`, self-referential `expected_commit_sha`, copied `world_time`, active lists and engine metadata. Must consume exact Step-5.7 field disposition. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Mirrors stale checkpoint field surface; template is not authority. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `GAME/SCHEMA/session.schema.yaml` | IMPLEMENTATION / MACHINE CONTRACT | `base_head_sha`, `last_published_head_sha`, status/notes are narrow session coordination evidence only. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `GAME/CAMPAIGN/SESSIONS/_TEMPLATE.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Mirrors session hint/currentness fields; must not create host lease/current frontier. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `GAME/SCHEMA/current_state.schema.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Compact current/routing projection; must not become universal recovery root list, chronology authority or checkpoint substitute. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Current `MANIFEST.last_checkpoint_id` contract declares the latest-checkpoint pointer and explicitly leaves current chronology frontier/semantic-log cursor in `STATE/CURRENT`. Step 2 must inspect pointer semantics and every consumer; accepted Step-5.7 meaning remains a narrow checkpoint-descriptor pointer, never recovery frontier/currentness/SAVE/handoff authority. | INSPECTED FOR SENIOR REPAIR / REQUIRED STEP-2. |
| `GAME/CAMPAIGN/MANIFEST.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Current scaffold carries `last_checkpoint_id: null`. Step 2 must inspect scaffold/generator impact and pointer lifecycle without making checkpoint mandatory or broadening pointer authority. | INSPECTED FOR SENIOR REPAIR / REQUIRED STEP-2. |
| `GAME/TOOLS/init_campaign.py` | IMPLEMENTATION / MACHINE CONTRACT | Mechanically copies campaign template and initializes MANIFEST/card/CURRENT; any checkpoint/session/MANIFEST repair must remain compatible with scaffold generation without making checkpoint mandatory. | INSPECTED FOR STEP 1 / CONDITIONAL STEP-2. |

Step 2 must inspect other runtime owner schemas referenced by RRC only as needed for exact recovery-machine realization; the manifest is deliberately open-world.

---

## 7. Current tests and acceptance surfaces

| Source | Role | WP-14 relevance | Step-1 status |
|---|---|---|---|
| `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md` | IMPLEMENTATION / TEST CONTRACT | B25 currently says first scene/checkpoint; B42 says recovery state actually required. Must preserve selection barrier/scaffold semantics while removing any unconditional checkpoint requirement. | INSPECTED FOR STEP 1 / REQUIRED STEP-2. |
| `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md` | IMPLEMENTATION / TEST CONTRACT | Existing sparse-checkpoint and publication/currentness cases constrain checkpoint optionality and crash outcomes; inspect recovery-facing cases. | REQUIRED STEP-2. |
| `DEV/TESTS/EXPLICIT_SAVE_CASES.md` | IMPLEMENTATION / TEST CONTRACT | Existing “no forced checkpoint” semantics must remain compatible with WP-13 native-domain SAVE. | REQUIRED STEP-2 where checkpoint/save intersects. |
| `DEV/TESTS/CHRONOLOGY_CASES.md` | IMPLEMENTATION / TEST CONTRACT | Check that recovery/checkpoint ordering never replaces typed chronology evidence. | CONDITIONAL STEP-2. |
| `DEV/TESTS/ENGINE_UPDATE_CASES.md` | IMPLEMENTATION / TEST CONTRACT | Runtime switch / maintenance recovery must not reinterpret open work; inspect relevant cases. | CONDITIONAL STEP-2. |
| current executable schema/contract tests under `DEV/TESTS/` | IMPLEMENTATION / TEST CONTRACT | Step 2 must discover exact tests asserting checkpoint/session/current recovery fields and classify conforming vs stale expectations. | OPEN-WORLD REQUIRED DISCOVERY. |

No test expectation supersedes canonical architecture. Stale tests are machine debt to route to WP-22/implementation, not evidence to reopen accepted semantics.

---

## 8. Access, authorization, maintenance and repair boundaries

| Source | Role | Why relevant / required Step-2 route |
|---|---|---|
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | CANONICAL / OWNING | Recovery may read broadly only within lawful information/operation scope; any repair/write remains application-authorized. Session or repository technical permission cannot create gameplay authority. |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | CANONICAL / OWNING where not superseded | Current campaign/live ref roles and non-force currentness context. Existing Storage-v2 documentation debt remains WP-26, not WP-14 semantics. |
| `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` | CURRENT SUPPORT / MAINTENANCE CONTRACT / PROPOSAL | Direct current recovery/repair/support consumer; repository status is `INTERNAL CONTROL CONTRACT / PROPOSAL`, so it cannot override Step-5.7/WP-10. Step 2 must reconcile `HDM_EXPORT_CHECKPOINT_LOG`, `HDM_RESET_LAST_CHECKPOINT`, checkpoint-based local reconstruction, `runtime.maintenance_audit`, and Connector/diagnostic evidence boundaries against current-authority-first/checkpoint-optional/no-silent-fallback recovery and WP-10 record-family allocation. Step 1 does **not** decide final command retention/removal/redesign. |

If Step 2 discovers another repair operation that writes state, its exact owner/access/currentness contract must be added to this manifest before synthesis.

---

## 9. Required Step-2 extraction axes

Step 2 must account item-by-item for at least:

1. ordinary cold recovery start/selection boundary;
2. campaign discovery anchor vs complete native source composition;
3. exact revision pinning for every mutable participating source;
4. current owning-route resolution including live ACTIVE/CLOSED_UNABSORBED;
5. typed independent recovery-root enumeration;
6. transitive correctness-required dependency hydration;
7. accepted execution/Continuation/fixed-RNG/mandatory-child continuity;
8. armed temporal-source routing and no duplicate rematerialization;
9. interpretation/catalog/rules compatibility for open accepted work;
10. derived-state rebuild vs authority;
11. surviving SQLite reuse proof;
12. session metadata status/HEAD semantics;
13. checkpoint optionality/current validation/facility-scoped defects;
14. exact disposition of current checkpoint schema/template fields;
15. `MANIFEST.last_checkpoint_id` narrow pointer semantics, actual consumers and scaffold/generator impact;
16. deterministic WP-11 direct-route/index rebuild;
17. READY / RETRY / BLOCKED and integrity-suspect outcomes;
18. bounded evidence-gated repair with no silent historical fallback;
19. no invented lost HOT/player choice/RNG/mechanics/execution;
20. chronology/currentness separation;
21. checkpoint not SAVE/handoff proof;
22. bootstrap/session/runtime/integrity consumer reconciliation;
23. current regression/test expectation classification;
24. downstream implementation/conformance obligations;
25. ambient Project/chat/model memory non-authority and zero-model-memory recovery against current routed owners;
26. fixed gameplay repository transport: exact pinned-ref/currentness/CAS/conflict/ambiguous-failure evidence through `deterministic Python/core -> GitHub Connector`, no alternate transport probe/fallback, and typed supported-profile failure when required Connector capability is absent;
27. `MAINTENANCE_COMMANDS.md` support flows, checkpoint-based local reconstruction, `runtime.maintenance_audit` allocation and Connector diagnostic-evidence boundaries without silently promoting checkpoint/history/export/support data into authority.

Synthesis is blocked until this completeness accounting is complete.

---

## 10. Downstream routes and non-goals

Expected downstream consumers, without authorization to start them now:

- **WP-15** — next R2.7 domain only after WP-14 closure and current gate;
- **WP-16** — final live currentness/CAS/close/absorption machine;
- **WP-19 / WP-20** — bootstrap/migration integration for repaired schemas/templates/current recovery contracts;
- **WP-22** — executable recovery, crash, checkpoint/session, repair, stale-machine and adversarial regression coverage;
- **WP-24** — measured recovery/query/index/Connector performance before optimization;
- **WP-26** — only separately routed documentation consistency debt, not WP-14 semantic repair;
- later implementation planning — exact APIs/schema migration/test plan only after architecture gates authorize it.

WP-14 Step 1 and this Senior repair do not change runtime/schema/template/test/tool implementation.

---

## 11. Step-1 manifest gate

```text
PROJECT_MAP_ROUTE_USED:            YES
ACTUAL_OWNER_CONSUMER_EXPANSION:   YES
OPEN_WORLD_FOR_STEP_2:             YES
UPSTREAM_WP11_WP12_WP13_CONSUMED:  YES
CRITIC_REPAIRS_INCORPORATED:       YES
SENIOR_REPAIR_SR14_01_03:          CLOSED
HISTORICAL_CRITIC_C01_C11_REWRITTEN: NO
UNRESOLVED_BLOCKING:               0
UNRESOLVED_SIGNIFICANT:            0
HUMAN_DECISION_REQUIRED:           NO
```

After Task Brief/manifest Senior repair publication and cursor synchronization, the next gate is mandatory Senior review. Step 2, WP-15 and implementation planning remain blocked.
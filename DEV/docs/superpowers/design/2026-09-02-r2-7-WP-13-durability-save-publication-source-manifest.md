# R2.7 WP-13 — Durability / SAVE / Publication — Source Manifest

Status: **STEP-1 TASK-SPECIFIC SOURCE MANIFEST — CRITIC-REPAIRED / READY FOR MANDATORY SENIOR REVIEW**

Date: 2026-09-02

Owning Task Brief:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-task-brief.md`

Mandatory whole-project Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-task-brief-critic.md`

---

## 1. Manifest purpose and classification rules

This manifest defines the current task-specific dependency/evidence subgraph for WP-13. It is not architecture authority by itself.

Source roles used below:

- **CANONICAL / OWNING** — current semantic or implementation-facing architecture authority;
- **CANONICAL AMENDMENT / OWNER DECISION** — accepted final clarification that may qualify another owner;
- **CURRENT-PROGRESS / PROCESS AUTHORITY** — current execution/gate/process owner, not semantic architecture;
- **DERIVATIVE LOCATOR / INDEX** — routing aid only;
- **IMPLEMENTATION / MACHINE CONTRACT / TEST** — current concrete runtime/schema/test/tool surface that may conform to or lag accepted architecture;
- **DESIGN PROVENANCE** — process evidence relevant to reopening/forward obligations, not default semantic authority;
- **HISTORICAL / SUPERSEDED** — retained only when needed to classify current debt/supersession.

Inspection status:

- **INSPECTED FOR STEP 1** — actual current source was read deeply enough to establish framing/role/current debt;
- **REQUIRED STEP-2 INSPECTION** — Step 2 must perform item-level extraction/reconciliation before synthesis even if Step 1 already inspected the source;
- **CONDITIONAL STEP-2 INSPECTION** — inspect when a discovered trigger/path/debt proves it participates in the active closure;
- **ROUTING ONLY** — may locate owners but cannot support semantic conclusions alone.

Step-1 inspection does not waive Step-2 enumerated-law accounting where the source contains a large normative set.

---

## 2. Governance, process and current-state sources

| Source | Role | Why relevant / required scope | Step-1 status | Step-2 disposition |
|---|---|---|---|---|
| `AGENTS.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | Repository boundaries, public-material rules, current branch guardrail, artifact taxonomy, GitHub-Connector publication/verification discipline. | INSPECTED FOR STEP 1 | Re-read if changed before Step 2/publication. |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | Connector-only remote transport, fresh-ref publication and read-back requirements. | INSPECTED FOR STEP 1 | Re-read if changed. |
| `DEV/DESIGN_PROCESS.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | Eight-step loop, Source Manifest/evidence gates, decision rights, Task-Brief requirements. | INSPECTED FOR STEP 1 | Binding process. |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | HDM whole-project critic route and mandatory Senior stop after completed Step 1. | INSPECTED FOR STEP 1 | Binding process. |
| `DEV/PROJECT_MAP.md` | DERIVATIVE LOCATOR / INDEX | Starting route for persistence/durability/recovery, access, tests and actual owning neighbors. | INSPECTED FOR STEP 1 | ROUTING ONLY; refresh before whole-project critic if changed. |
| `DEV/CURRENT_PROGRESS.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | Sole global state/next authorized unit/gate. | INSPECTED FOR STEP 1 | Re-read before every next-stage transition. |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | DERIVATIVE LOCATOR / INDEX | R2.7 sequence/scope/dependency context only. | INSPECTED FOR STEP 1 | ROUTING ONLY. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | CURRENT-PROGRESS / PROCESS AUTHORITY (task-local) | WP-13 cursor and preserved forward obligations; subordinate to global progress. | INSPECTED FOR STEP 1 | Keep synchronized at Step checkpoints. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md` | CURRENT-PROGRESS / PROCESS AUTHORITY | R2.7 per-domain audit protocol and artifact/gate expectations. | INSPECTED FOR STEP 1 | Binding task process. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` | DESIGN PROVENANCE / PROGRAM INPUT | WP-13 audit questions and architecture↔machine proof objective. | INSPECTED FOR STEP 1 | Use as program-level scope input. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | DESIGN PROVENANCE / PROGRAM INPUT | Original whole-project evidence routing; not current architecture authority. | INSPECTED FOR STEP 1 | Discovery aid only. |

---

## 3. Canonical execution, durability, publication and recovery owners

These are the primary normative dependency chain. Step 2 must extract the actual relevant laws/qualifiers item by item rather than rely on the summaries in the Task Brief.

| Source | Role | Why relevant / required Step-2 scope | Step-1 status |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` | CANONICAL / OWNING | ExecutionSegment, accepted IDs/RNG/idempotency, pending-child/Continuation closure; publication retry cannot become gameplay replay. Inspect atomic edge, retry/idempotency, fixed RNG and recovery-facing continuity sections. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md` | CANONICAL / OWNING | Bounded native roots/dependency closure, native owners, no global snapshot/frontier, no invented lost HOT. Extract every law constraining required durable closure and current source selection. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md` | CANONICAL / OWNING | Pending temporal/mandatory work may create durability requirements and recovery roots without generic pending queue. Inspect when WP-13 trigger/root mapping touches temporal owners. | REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md` | CANONICAL / OWNING | Controlled handoff requires actual durable compatible RRC; scoped quiescence; no global lock/no-op write; session metadata non-authoritative. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md` | CANONICAL / OWNING | Primary semantic owner for SOFT/HARD/SAVE, scope policy, explicit SAVE promise, multi-domain composition, partial native publication, rejection of global one-hour frontier. **Full relevant law accounting required.** | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md` | CANONICAL / OWNING | Primary campaign publication owner: frozen attempt, base-tree delta, single-parent/non-force ref transition, currentness/auth footprint, ambiguity/rejection/accepted outcomes, generation adoption, no persistent journal. **Full relevant law accounting required.** | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md` | CANONICAL / OWNING | Boundary owner preventing checkpoint from becoming SAVE proof; current-authority-first recovery; checkpoint optionality. Extract laws 5.7-17..25 and any native-currentness requirements needed by WP-13. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md` | CANONICAL / OWNING | Exact-source CAS native durability edge, authority claims, fencing, authorization, close/absorption and live-native atomicity. WP-13 only composes/integrates; final machine stays WP-16. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | CANONICAL / OWNING INTEGRATION | Integrated Step-5 concurrency/recovery consistency; prevents local machine convenience from reintroducing global frontier/distributed transaction or false SAVE acknowledgement. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |

### Step-5 neighboring canonical owners to inspect conditionally

| Source | Role | Why / trigger | Disposition |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md` | CANONICAL / OWNING | Inspect if current machine/frontier terminology needs direct reconciliation beyond Step-5.5/5.6. | CONDITIONAL STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md` | CANONICAL / OWNING | Publication order/commit order must not become fictional chronology. | CONDITIONAL STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md` | CANONICAL / OWNING | Story is projection/non-authoritative; inspect if SAVE current tests/prose attempt to use summary/story as state durability. | CONDITIONAL STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md` | CANONICAL / OWNING | Retained messages/history can be dependency evidence but not generic SAVE truth. | CONDITIONAL STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | CANONICAL / OWNING | Inspect if write-before-reveal/ack semantics require explicit publication linkage. | CONDITIONAL STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` | CANONICAL / OWNING | Unreachable prepared commits/objects may later be cleanup evidence; GC is not publication authority. | CONDITIONAL STEP-2 INSPECTION |

---

## 4. R2.7 upstream realization owners

| Source | Role | Why relevant / required scope | Step-1 status |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-10-durable-campaign-record-family-completeness-canonical-spec.md` | CANONICAL / OWNING | Native durable record-family allocation. WP-13 must publish native owners/evidence without inventing summary/journal owners. The file-local old audit-status header is not global progress authority. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | CANONICAL / OWNING | Exact native route/path law and derived index contract. **WP-11/F02 -> WP-13:** native record + required index publication closure. Extract route/index obligations relevant to planned path delta. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` | CANONICAL / OWNING | Owner-generation dirty bookkeeping, frozen publication attempt, exact-generation clearing, cold survivor rules, local-HOT/live-CAS split. **WP-12 -> WP-13:** durability/SAVE/publication realization + stale global timer/frontier repair. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-12-senior-recovery-live-cas-boundary.md` | DESIGN PROVENANCE / ACCEPTED RECOVERY EVIDENCE | Explains repaired WP12-8 live-CAS qualification and Senior closure. Use only to preserve provenance; current final WP12 spec owns law. | INSPECTED FOR STEP 1; use if cross-law provenance is challenged. |

Closed upstream architecture is not reopened by status overlap. A proposal to supersede it requires evidence of contradiction, a new consumer it cannot satisfy, or material insufficiency.

---

## 5. Authority, branch and policy owners

| Source | Role | Why relevant / required scope | Step-1 status |
|---|---|---|---|
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | CANONICAL / OWNING | Acting principal, creator/player authority, repo/ref role separation, deny-on-uncertain authority. Publication attempts must freeze/revalidate required authorization basis. Existing stale `Storage v2` label is WP-26 documentation debt, not WP-13 semantics. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | CANONICAL / OWNING for current branch/campaign structure where not superseded | Current campaign ref role, non-force optimistic publication, branch/storage topology context. Storage-v2 wording already routed to WP-26 and must not distract WP-13. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION only for publication/currentness clauses |
| `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` | CANONICAL / OWNING | House-Rule policy adoption/grant changes are campaign-persistent authority changes; HR-8 includes a creator-only HARD access-control persistence boundary; policy publication must use existing Step-5.6/currentness/access rules. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION for named durability-edge mapping |

---

## 6. Current GAME runtime owners/consumers

These are shipped machine/runtime contracts. When they conflict with accepted canonical specs, they are **pre-realization debt/evidence**, not semantic authority capable of superseding the specs.

| Source | Machine role | Step-1 observation / Step-2 required inspection | Classification |
|---|---|---|---|
| `GAME/CORE/RUNTIME.md` | Turn-loop and persistence routing consumer | Correctly separates boundary/transport owners and zero-I/O fast path; currently includes one-hour ceiling in HARD examples. Extract all persistence-boundary/currentness/integrity routing text and classify stale clauses. | IMPLEMENTATION / MACHINE CONTRACT / TEST — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/DURABILITY_GUARD.md` | Current runtime WHEN-publication guard | Encodes current one-hour dirty ceiling and global `durable_frontier_time`; this is direct machine debt against Step-5.5/WP-12. Also contains valid sparse-save/no-heartbeat concepts. Must be inspected line-by-line against named owner edges. | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/PERSISTENCE.md` | Current campaign/live/storage publication transport | Current `CAMPAIGN_TREE_TXN` largely matches base-tree/non-force campaign publication but needs exact comparison for frozen fields, G/G+1, currentness/auth, ambiguity and no mixed domain semantics. | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/SAVE_CONTRACT.md` | Current explicit-save runtime surface | Current `SAVE_ALL_DIRTY` / one `CAMPAIGN_TREE_TXN` framing is insufficient as the general multi-native-domain SAVE promise. Preserve structured-state/local-completeness rules while reconciling composition. | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/STORAGE.md` | Current storage/HOT/repository-role runtime support | Contains `known_head_sha`/tree and current global durable-frontier time. Separate storage-default metadata publication from campaign SAVE. | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/SESSION.md` | Session lifecycle/handoff consumer | Contains current inactive-gap one-hour check; valid session-end/handoff/checkpoint-economy concepts must be reconciled to Step5.4/5.5. Checkpoint remains optional. | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/CAMPAIGN_OPERATIONS.md` | Campaign operational consumer | Hot-working-set batching, one campaign transaction, live separate boundary, checkpoint economy. Must be reconciled so “one campaign transaction” is not “one entire multi-domain SAVE transaction.” | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/DIEGETIC_ONBOARDING.md` | Named semantic durability-edge owner | `PROVISIONAL_IDENTITY` requires coherent publication before further accumulated fiction crosses its promise. Map exact roots/edge scope; do not centralize reason in Durability Guard. | IMPLEMENTATION / SEMANTIC CONSUMER — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/CHARACTER_READINESS.md` | Named semantic durability-edge owner | READY_PC/PLAY_READY barrier requires reconstructable character closure and confirmed durability. Map Player/Actor/Asset/Effect/index/current/card/routing closure without inventing extra facts. | IMPLEMENTATION / SEMANTIC CONSUMER — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/MULTIPLAYER.md` | Access/shared-world boundary consumer | Membership deactivation is HARD; active-live membership changes compose live close/compaction + campaign write. Current live details may lag Step5.8. Extract only owner-specific edges and publication dependencies; final live machine WP-16. | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/LIVE_SCENE.md` | Current live-machine implementation consumer/debt | One-file live CAS, commit-before-reveal, compaction/currentness. Treat as implementation evidence/debt where Step5.8 supersedes it. WP-13 may not canonize old one-file semantics; WP-16 owns final live machine. | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 only for WP13 integration/debt routing |
| `GAME/CORE/INTEGRITY.md` | Publication preflight/integrity consumer | Requires scope-local dirty/direct-dependency validation; prohibits broad campaign/world/history scan. Use to constrain local completeness proof. | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 |
| `GAME/CORE/RANDOMNESS.md` | Accepted RNG/causal evidence consumer | No reroll/fudging; durable causal evidence when randomness causes state. Publication retry/currentness repair must preserve fixed accepted RNG. | IMPLEMENTATION / MACHINE CONTRACT — INSPECTED / REQUIRED STEP-2 if retry flow touches RNG |

### Additional GAME consumers to discover/inspect in Step 2

The manifest is not closed-world. Step 2 must search actual named references to `HARD`, `SAVE`, `PERSISTENCE`, `CAMPAIGN_TREE_TXN`, publication/currentness and durability-edge terminology and add concrete owners before synthesis.

Likely conditional consumers include:

- `GAME/CORE/ENGINE_UPDATES.md` — engine/rules adoption publication/maintenance boundary;
- campaign lifecycle/setup modules when an initialization/activation edge depends on publication;
- House-Rules runtime surfaces;
- chronology/history/delivery modules when write-before-reveal or durable-history edges participate;
- maintenance/migration modules only when the current WP-13 publication mechanism is a direct shared consumer rather than a downstream WP-20 concern.

---

## 7. Current schemas / machine data contracts

| Source | Role | Why relevant / required scope | Step-1 status |
|---|---|---|---|
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Current campaign branch/status/mode/storage roots/batched persistence/force-push false/checkpoint pointer. Validate which fields participate in named publication edges; MANIFEST must not become generic durability state. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `GAME/SCHEMA/current_state.schema.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Compact current routing/chronology summary; explicitly no generic pending-consequence bucket and no durability frontier. Determine direct closure use only when actual dirty roots require it. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION |
| `GAME/SCHEMA/session.schema.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Coordination hints (`base_head_sha`, `last_published_head_sha`) are not publication authority; updated only at persistence boundaries. | INSPECTED FOR STEP 1 / REQUIRED STEP-2 INSPECTION if session publication is implicated |
| `GAME/SCHEMA/checkpoint.schema.yaml` and checkpoint-related schemas | IMPLEMENTATION / MACHINE CONTRACT | Checkpoint currently contains fields known to be WP-14 debt. Inspect only enough in WP-13 to ensure SAVE/publication does not depend on checkpoint; do not repair schema here. | CONDITIONAL / WP-14 BOUNDARY |
| `GAME/SCHEMA/live_scene.schema.yaml` / current live schema family | IMPLEMENTATION / MACHINE CONTRACT | Concrete existing live machine debt/current consumer. Inspect only for WP-13 integration mismatch; final reconciliation WP-16. | CONDITIONAL / WP-16 BOUNDARY |
| Native family schemas routed by WP-10/WP-11 | IMPLEMENTATION / MACHINE CONTRACT | Publication must preserve owner shape/identity and required index/projection closure. Do not preload all schemas; follow actual dirty-edge examples and paths found in Step 2. | CONDITIONAL STEP-2 INSPECTION by selected native family |

---

## 8. Tests and executable/acceptance evidence

Current tests are evidence of what the repository enforces today. They do not override canonical architecture when stale.

| Source | Role | Step-1 observation / required Step-2 accounting | Status |
|---|---|---|---|
| `DEV/TESTS/DURABILITY_BOUNDARY_CASES.md` | IMPLEMENTATION / TEST | Sparse-save, named lifecycle/READY boundaries, zero-I/O classification and no per-turn autosave. Classify each case against Step5.5 and current named owners. | INSPECTED / REQUIRED STEP-2 |
| `DEV/TESTS/EXPLICIT_SAVE_CASES.md` | IMPLEMENTATION / TEST | Protects structured SAVE completeness and no false `saved`; currently assumes `SAVE_ALL_DIRTY` + one campaign transaction and unqualified dirty clearing. Account S01–S20 individually where relevant. | INSPECTED / REQUIRED STEP-2 |
| `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md` | IMPLEMENTATION / TEST | Campaign base-tree/non-force/one-commit invariants are valuable; PT10 dirty clear and PT19 current one-file live profile require reconciliation. Account PT01–PT31 relevant items individually. | INSPECTED / REQUIRED STEP-2 |
| `DEV/TESTS/test_hourly_durability_contract.py` | IMPLEMENTATION / TEST | Directly asserts the noncanonical one-hour global frontier and matching SESSION/PERSISTENCE wording. Primary executable debt route for WP-13. | INSPECTED / REQUIRED STEP-2 |
| `DEV/TESTS/CHARACTER_READINESS_CASES.md` | IMPLEMENTATION / TEST | Named READY_PC/PLAY_READY durability edge evidence. | REQUIRED STEP-2 INSPECTION |
| `DEV/TESTS/DIEGETIC_ONBOARDING_CASES.md` | IMPLEMENTATION / TEST | `PROVISIONAL_IDENTITY` durability edge evidence. | REQUIRED STEP-2 INSPECTION |
| `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md` | IMPLEMENTATION / TEST | HARD membership/access boundary and live/campaign composition evidence. | REQUIRED STEP-2 INSPECTION |
| `DEV/TESTS/ACCESS_CONTROL_CASES.md` | IMPLEMENTATION / TEST | Application authorization vs technical repository permission. | REQUIRED STEP-2 INSPECTION |
| `DEV/TESTS/LIVE_SCENE_CASES.md` | IMPLEMENTATION / TEST | Current live implementation tests; classify as conforming/debt relative to Step5.8/WP16, never as authority to reopen live design. | REQUIRED STEP-2 INSPECTION for WP13 integration only |
| `DEV/TESTS/INTEGRITY_CASES.md` | IMPLEMENTATION / TEST | Bounded preflight/repair and no broad scan behavior. | REQUIRED STEP-2 INSPECTION |
| `DEV/TESTS/ENGINE_UPDATE_CASES.md` | IMPLEMENTATION / TEST | Inspect if engine/rules adoption is proven to be a direct WP-13 publication consumer. | CONDITIONAL STEP-2 INSPECTION |
| `DEV/TESTS/test_current_progress_authority.py` | IMPLEMENTATION / TEST | Ensures global progress authority discipline; process verification only. | CONDITIONAL / verification support |

Step 2 must not infer accepted architecture from test presence alone. Stale tests must be dispositioned as implementation debt and routed to later implementation/WP-22.

---

## 9. Tooling / verification surfaces

| Source | Role | Why relevant | Status |
|---|---|---|---|
| `DEV/TOOLS/run_maintenance_audit.py` | IMPLEMENTATION / TEST TOOL | Canonical repository audit entry point; future implementation verification may use it. Step 1 does not claim that it proves WP-13 architecture. | INSPECTED FOR STEP 1 |
| `DEV/TOOLS/audit_engine.py` and validators it invokes | IMPLEMENTATION / TEST TOOL | Inspect in Step 2 only if current audit checks directly constrain publication/durability contracts or create stale assertions. | CONDITIONAL STEP-2 INSPECTION |
| `.github/workflows/validate.yml` | IMPLEMENTATION / TEST TOOL | Hosted validation transport; publication/status evidence only, not architecture. | CONDITIONAL verification support |

---

## 10. Step-1 debt/forward-obligation ledger

| ID | Source/current fact | Classification | WP-13 disposition |
|---|---|---|---|
| O01 | WP-11/F02 requires atomic native-record + required-index publication closure. | CLOSED-UPSTREAM FORWARD OBLIGATION | **ACTIVE WP-13 input**; Step 2 must map exact record/index closure behavior. |
| O02 | WP-12 routes durability/SAVE/publication realization to WP-13. | CLOSED-UPSTREAM FORWARD OBLIGATION | **ACTIVE WP-13 input**. |
| O03 | WP-12 rejects global dirty generation/frontier/timer and requires G-specific clearing. | CLOSED-UPSTREAM LAW | **ACTIVE WP-13 constraint**. |
| O04 | `DURABILITY_GUARD`/`STORAGE`/`RUNTIME`/`SESSION` + `test_hourly_durability_contract.py` enforce one-hour/global frontier. | CURRENT MACHINE DEBT | **ACTIVE WP-13 reconciliation**; not an architecture reopening. |
| O05 | `SAVE_CONTRACT`/explicit-save tests frame SAVE as one campaign transaction. | CURRENT MACHINE DEBT / PARTIAL MODEL | **ACTIVE WP-13 reconciliation** to multi-native-domain promise; retain valid campaign-domain transaction behavior. |
| O06 | `PERSISTENCE`/tests use unqualified clear-published-dirty wording. | CURRENT MACHINE PRECISION DEBT | **ACTIVE WP-13 reconciliation** to frozen G/G+1. |
| O07 | current live runtime/tests use older one-file machine. | CURRENT MACHINE DEBT / DOWNSTREAM OWNER | WP-13 only defines integration/hand-off; **WP-16 owns final live realization**. |
| O08 | checkpoint fields/current recovery machine have known debt. | DOWNSTREAM OWNER | **WP-14**; WP-13 only preserves checkpoint-not-save-proof law. |
| O09 | Storage-v2 wording in `BRANCH_MODEL.md` / `ACCESS_CONTROL.md`. | MINOR DOC CONSISTENCY | **WP-26**; explicitly out of WP-13 repair scope. |
| O10 | executable architecture conformance/failure injection is incomplete. | DOWNSTREAM IMPLEMENTATION | **WP-22** after approved architecture/plan. |

---

## 11. Required Step-2 inspection route

If Senior gives GO, Step 2 must execute this route before synthesis:

```text
fresh current-progress/ref
-> refresh this Source Manifest against current PROJECT_MAP/tree
-> extract Step5.5 laws/qualifiers item by item
-> extract Step5.6 laws/qualifiers item by item
-> extract RRC / handoff / checkpoint / live constraints that affect the promise
-> extract WP11/F02 + WP12 dirty-generation/publication obligations
-> enumerate actual named durability-edge owners in current GAME/architecture
-> enumerate current runtime/schema/test implementations of each edge/flow
-> classify each surface:
       conforming
       stale pre-realization debt
       supporting evidence
       downstream-owned
       contradiction requiring escalation
-> build the trigger/domain/publication evidence matrix
-> run completeness gate
-> only then produce analytical synthesis / Decision Brief
```

Required search/discovery after structural inspection:

- concrete references to `HARD`, `SOFT`, `SAVE`, `SAVE_ALL_DIRTY`, `durable_frontier_time`, `one-hour`, `PERSISTENCE`, `CAMPAIGN_TREE_TXN`, publication, `update_ref`, checkpoint, membership/policy adoption, `PROVISIONAL_IDENTITY`, READY_PC/PLAY_READY and live CAS;
- direct consumers of current campaign publication and dirty-clearing APIs/contracts once implementation-facing surfaces are identified;
- tests asserting stale/global timing or campaign-only SAVE assumptions.

An empty search result is not absence proof; inspect the routed directory/owner family when the claim depends on completeness.

---

## 12. Explicit boundaries against accidental scope expansion

### WP-14 checkpoint/recovery

WP-13 may require publication of checkpoint bytes only if a separate current owner makes that checkpoint itself an independently required dirty native record for the same operation. It may not make checkpoint a generic component/proof of SAVE. Schema/currentness repair belongs WP-14.

### WP-16 live machine

WP-13 must use accepted Step-5.8/WP-12 exact-source live durability semantics in SAVE/HARD composition. It may identify current `LIVE_SCENE` machine/test mismatches but may not choose final live file/schema/ref/CAS realization.

### WP-19/WP-20 bootstrap/migration

WP-13 may define a reusable publication contract consumed later. It does not design campaign scaffolding or migration orchestration.

### WP-22 tests

WP-13 Step 8 may state mandatory executable obligations. Production/test implementation belongs after architecture approval and approved planning; R2.7 Step 1 changes no tests.

### WP-24 performance

No index partitioning or publication batching optimization is selected without measured evidence.

### WP-26 documentation consistency

Storage-v2 wording remains forward documentation work. It does not alter the current durability/SAVE semantics and is not repaired here.

---

## 13. Step-1 completeness self-check

```text
[x] current remote ref/current-progress/process sources were recovered
[x] PROJECT_MAP persistence/access/test routes were followed to actual owners
[x] primary Step5.5/Step5.6 semantic owners were inspected
[x] RRC, handoff, checkpoint and live neighboring authority boundaries were inspected
[x] WP10/WP11/WP12 upstream realization owners and forward obligations were inspected
[x] actual current GAME durability/save/publication surfaces were inspected
[x] named PROVISIONAL_IDENTITY, READY_PC/PLAY_READY and membership/policy consumers were included
[x] current schemas and principal regression suites were included
[x] explicit one-hour/global-frontier executable debt was located
[x] multi-domain SAVE versus campaign-transaction mismatch was identified
[x] current live-machine evidence was classified as downstream debt rather than authority
[x] checkpoint/save boundary was preserved
[x] Storage-v2 documentation cleanup was kept in WP-26
[x] no conclusion depends only on roadmap/index/search snippets
[x] manifest remains extensible when Step 2 discovers additional direct consumers
```

No current evidence creates a new product/authority choice at Step 1.

**Human decision required: NO.**

---

## 14. Step-1 gate

This manifest plus the repaired Task Brief and whole-project critic form the complete Step-1 framing package.

After verified publication:

- mandatory Senior review is required;
- Step 2 is blocked until explicit Senior GO;
- WP-14 and implementation planning remain blocked.

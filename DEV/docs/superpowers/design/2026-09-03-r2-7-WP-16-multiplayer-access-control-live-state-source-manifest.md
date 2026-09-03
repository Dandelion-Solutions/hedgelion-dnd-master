# R2.7 WP-16 — Multiplayer / Access Control / Live State — Source Manifest

Status: **STEP-1 TASK-SPECIFIC OPEN-WORLD SOURCE MANIFEST — WHOLE-PROJECT CRITIC APPLIED / MANDATORY SENIOR REVIEW REQUIRED**

Date: 2026-09-03

Domain: **WP-16 — multiplayer / access control / live state**

Companion Task Brief:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-task-brief.md`

Mandatory Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-task-brief-critic.md`

Starting verified public state:

- `b2afeae3033b96f8d688d437972a020eb0f1746f`

This manifest is **open-world**. It was reconstructed from current `DEV/PROJECT_MAP.md`, then expanded by direct owner/consumer traversal. It is not a closed bibliography and it is not a substitute for reading owning sources. If Step 2 is later authorized, actual searches/references must extend this manifest whenever another material owner, consumer, machine field, bootstrap path, migration surface, test or supersession route is discovered.

---

## 1. Source-role vocabulary

| Role | Meaning |
|---|---|
| `CURRENT-PROGRESS / PROCESS AUTHORITY` | Controls current task/gate/process only. |
| `DERIVATIVE LOCATOR / INDEX` | Navigation or dependency routing; never gameplay semantic authority. |
| `CANONICAL / OWNING` | Current accepted semantic architecture owner. |
| `CANONICAL INTEGRATION / OWNING` | Current integration law reconciling several owners. |
| `R2.7 UPSTREAM / OWNING` | Closed implementation-facing R2.7 architecture constraining WP-16. |
| `CANONICAL DOMAIN OWNER` | Current authoritative domain prose such as access/branch ownership. |
| `IMPLEMENTATION / MACHINE CONTRACT` | Current shipped schema/runtime/scaffold realization; evidence/consumer, not authority merely by existence. |
| `IMPLEMENTATION / TEST CONTRACT` | Current executable/scenario expectation; may be stale relative to later owner. |
| `NEGATIVE-SCOPE / TECHNICAL EVIDENCE` | Evidence that a technical identity/order/source is not semantic authority. |
| `DESIGN PROVENANCE / CONDITIONAL` | Read when current owner applicability/supersession requires it. |
| `DOWNSTREAM / DEFERRED OWNER` | Neighboring owning domain whose constraints are relevant but whose realization is not activated. |

---

## 2. Process / current-state authority

| Source | Classification | WP-16 treatment |
|---|---|---|
| `AGENTS.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Repository/evidence/publication discipline only. Development-agent GitHub identity is not gameplay participant identity. |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Connector/write/read-back discipline for this development task; never LIVE/gameplay authority. |
| `DEV/DESIGN_PROCESS.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Generic eight-step architecture process. |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | HDM architecture adapter, Source Manifest and critic gates. |
| `DEV/PROJECT_MAP.md` | `DERIVATIVE LOCATOR / INDEX` | Starting dependency graph; actual owners/consumers were traversed from it. |
| `DEV/CURRENT_PROGRESS.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Sole global project position/gate. Its HEAD/status words are not campaign/live currentness. |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | `DERIVATIVE LOCATOR / INDEX` | Sequencing/scope only. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Task-local R2.7 cursor only. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Program audit contract. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | `DERIVATIVE LOCATOR / INDEX` | WP-16 program question/downstream routing. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Durable R2.7 execution/checkpoint rules. |

---

## 3. Primary multiplayer / LIVE / agency architecture

| Source | Classification | Mandatory later extraction / applicability |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md` | `CANONICAL / OWNING` | Participant identity/control separation; no global active player; absence is not consent; no presence/timeout authority; participant catch-up/rejoin; split-party owner separation; collaboration contribution semantics. Route durable async realization to WP-17. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md` | `CANONICAL / OWNING` | Primary LIVE ownership/currentness law: typed immutable claims, bounded containment/write routing, exact-source CAS, ACTIVE/CLOSED, CLOSED_UNABSORBED, absorption, revocation, multi-live transfer, source-native IDs, recovery, no campaign fallback, no distributed transaction/global LIVE owner. |
| `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` | `CANONICAL / OWNING` | Accepted command/resolution/continuation/idempotency/fixed RNG/segment semantics. LIVE transport/currentness cannot replay or redefine accepted execution. |
| `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` | `CANONICAL / OWNING` | Information-owner separation needed for LIVE knowledge/perception fields; storage possession is not role eligibility. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | `CANONICAL / OWNING` | PLAYER disclosure is recipient-scoped and distinct from fictional PC knowledge/current LIVE physical storage. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` | `CANONICAL / OWNING` | Ref/source cleanup is post-authority; source existence/age is not current authority; survivor-before-removal and currentness-sensitive cleanup. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | `CANONICAL INTEGRATION / OWNING` | Whole-system concurrency/recovery guard against substitute authority, replay and cross-domain accidental global semantics. |

### 3.1 R2.5 / Step-5.8 binding facts already established at Step 1

Step 1 treats these as closed constraints rather than open design questions:

1. authenticated external identity, PLAYER semantic identity, PC control and operation authorization are distinct;
2. repository capability/CAS success is not gameplay authorization;
3. LIVE physical packing does not merge native semantic owners;
4. current campaign routing selects LIVE authority; branch existence does not;
5. selected claims are typed, immutable for one epoch and non-overlapping;
6. exact source revision/HEAD is the LIVE mutation fence;
7. ACTIVE is writable current truth; CLOSED_UNABSORBED is frozen current truth with zero ordinary writers;
8. campaign base is not fallback current truth for selected live claims;
9. close is terminal and predecessor never reopens;
10. absorption is forward campaign/native publication, not replay/merge of every live commit;
11. multi-source composition is not a distributed transaction and accepted native edges remain real;
12. technical CAS/ref order is not fictional chronology;
13. absence/presence/heartbeat is not agency/authorization;
14. LIVE cannot manufacture voluntary actions for an absent participant's PC;
15. WP-17 owns durable async collaboration realization.

---

## 4. Access / repository / branch ownership

| Source | Classification | Mandatory later extraction |
|---|---|---|
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | `CANONICAL DOMAIN OWNER` | Engine/storage/campaign authority separation; creator derivation; stable external user-ID -> PLAYER binding; membership status; invite/open self-enrollment; deactivation/reactivation; controlled-PC transfer; policy sub-authority; ref/scope authorization. |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | `CANONICAL DOMAIN OWNER` | Campaign vs storage/default vs LIVE branch roles; non-force write rules; branch existence nonauthority; campaign isolation. Treat stale release/Storage wording only if directly material. |
| `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` | `CANONICAL DOMAIN OWNER` | Only where mechanical override policy authority must remain distinct from normal player/PC/live authority. No House-Rules redesign. |
| `GAME/CORE/RUNTIME.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Current write-routing guard, creator/PLAYER authorization and player-agency/world-continuity consumers. Also negative evidence that repository permission does not override HDM routing. |

---

## 5. Closed R2.7 implementation-facing constraints

| Source | Classification | Mandatory WP-16 applicability |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | LIVE physical route; native identity versus path; no campaign index for LIVE; source-native epoch-qualified live identity; path/index/order nonauthority. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | Pre-CAS prospective LIVE state, authoritative exact-source CAS establishment, post-CAS local adoption, local possession != permission, no SQLite+LIVE distributed transaction. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | Frozen currentness/authorization publication basis, non-force owner-native edges, partial success truthfulness, no cross-domain rollback/replay/global durability transaction. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | Current-route-first recovery; selected ACTIVE/CLOSED LIVE is current truth; no campaign fallback; exact pins; session/cache/checkpoint nonauthority. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | Native occurrence identity; no duplicate accepted materialization under CAS conflict; fixed RNG; technical currentness/CAS order not chronology; live temporal acceptance only on native LIVE edge. |

Closed upstream results are constraints. A stale current runtime/schema/test expectation is not by itself evidence to reopen them.

---

## 6. Current shipped multiplayer / LIVE runtime consumers

| Source | Classification | Step-2 inspection obligation if authorized |
|---|---|---|
| `GAME/CORE/MULTIPLAYER.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Auth user -> PLAYER -> PC binding; join/deactivation; stale chats; attribution; LIVE freeze on deactivation; cross-scene handling. Reconcile current “freeze/compact/deactivate” wording with Step-5.8 revocation/absorption/authorization closure. |
| `GAME/CORE/LIVE_SCENE.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Major realization target. Reconcile scene-centric one-file overlay, participant lists, touched sets, provisional IDs, local revision/blob assumptions, one-action/one-write, opening/close/compaction/recovery with immutable typed claims, exact-source CAS, per-native-edge atomicity and stable live identity. |
| `GAME/CORE/RUNTIME.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Write-routing, authorization revalidation, multiplayer synchronization, player agency and lost-state non-invention. |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Authentication/storage/campaign selection; cached card/login nonauthority; post-selection creator/PLAYER authorization; relevant PLAYER/PC loading; multiplayer join menu vs actual authority revalidation. |
| `GAME/CORE/SESSION.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Session associations and multiplayer refresh only; session/liveness not authority. Inspect stale-player/current-source resume behavior. |
| `GAME/CORE/PERSISTENCE.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Campaign transaction versus current one-file `LIVE_STATE_CAS`; authorization in frozen snapshot; non-force concurrency. Reconcile with Step-5.8 native-edge semantics rather than preserve stale one-file assumptions as architecture. |
| `GAME/CORE/STORAGE.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Campaign/live source/currentness routing, orphan/ref handling and cached source basis where actually referenced. |
| `GAME/CORE/INTEGRITY.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Bounded diagnosis for missing/conflicting selected LIVE sources, overlapping authority and stale state; avoid campaign-history/global scans. |
| `GAME/CORE/INFORMATION.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Only LIVE perception/knowledge/disclosure integration; no information-architecture reopening. |
| `GAME/CORE/CHRONOLOGY.md` | `IMPLEMENTATION / MACHINE CONTRACT / LIMITED` | Only technical-order versus fictional-order separation and cross-scope accepted event ordering. WP-15 owns chronology; stale frontier cleanup remains downstream. |
| `GAME/CORE/PROCESSES.md` | `IMPLEMENTATION / MACHINE CONTRACT / LIMITED` | Only native occurrence/duplicate advancement/currentness dependencies that cross LIVE scopes. WP-15 owns process semantics. |

---

## 7. Current machine schemas / campaign realization

| Source | Classification | Step-2 inspection obligation if authorized |
|---|---|---|
| `GAME/SCHEMA/player.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | Strong current machine evidence for stable `player_id`, stable external `github_binding.user_id`, active/inactive lifecycle, `controlled_pc_ids`, deactivation provenance and separate policy authority. Verify all consumers follow these semantics. |
| `GAME/SCHEMA/live_scene.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | Main current LIVE realization. Classify every participant/PC/overlay/created-entity/live-fact/event/touched/currentness field against native owners and Step-5.8 roles. Do not promote current schema shape over closed owner law. |
| `GAME/SCHEMA/scene.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | Campaign scene routing to one live epoch, opening/final absorbed revision fields, participant/PC associations. Reconcile scene pointer with typed claims/current route; chronology field debt stays WP-15/WP-26. |
| `GAME/SCHEMA/session.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | Session player/PC/scene/base-head associations; prove they are coordination/cache only and cannot grant write/agency authority. |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | `mode`, `players.join_policy`, `players.player_ids`, storage roots. Classify player list as membership/config routing surface rather than PLAYER/control/auth authority. |
| `GAME/SCHEMA/current_state.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | Active scene/current summary routing only; cannot establish LIVE claim/currentness/authorization or chronology. |
| `GAME/SCHEMA/event.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | Player/PC semantic attribution, accepted event provenance and information/chronology references where LIVE emits/absorbs them. |
| `GAME/SCHEMA/pc.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | Controlled-PC/world identity and legacy information projections as reached through access/LIVE. |
| applicable runtime command/procedure/resolution/continuation schemas | `IMPLEMENTATION / MACHINE CONTRACT` | Only when LIVE source movement/close/absorption must preserve accepted execution and pending obligations. |
| applicable knowledge/disclosure/message schemas/catalog contracts | `IMPLEMENTATION / MACHINE CONTRACT` | Only to classify LIVE information fields and natural-owner normalization. |

### 7.1 Current schema debts already identified but not resolved in Step 1

The manifest records these as mandatory later reconciliation targets, not approved final shape:

- scene-centric `participant_ids` / `player_character_ids` cannot substitute for typed mutation claims;
- `touched_*` evidence cannot retroactively create authority;
- `revision` integer / file blob SHA cannot silently replace exact live source ref/HEAD as fence;
- `provisional_id` rekey semantics must be reconciled with stable live-born identity requirements;
- one-file `LIVE_STATE` packing cannot merge semantic owner lifecycles;
- one-action/one-write assumptions must be reconciled with per-native-durability-edge atomicity;
- live perception/knowledge arrays cannot become current knowledge/disclosure owners;
- scene/current summary pointers/lists cannot prove complete authority/absence by themselves.

No implementation is authorized here.

---

## 8. Campaign/bootstrap/scaffold/generator consumers

| Source | Classification | Step-2 treatment if authorized |
|---|---|---|
| `GAME/CAMPAIGN/MANIFEST.yaml` | `IMPLEMENTATION SCAFFOLD` | Current multiplayer join-policy/player-list template; not creator/PLAYER/control authority by itself. |
| `GAME/CAMPAIGN/STATE/CURRENT.yaml` | `IMPLEMENTATION / ROUTING SUMMARY` | Active scene/current routing summary only; no LIVE authority by mere entry. |
| `GAME/CAMPAIGN/INDEX/PLAYER_INDEX.yaml` | `DERIVATIVE INDEX / IMPLEMENTATION` | Player discovery/routing helper only; absence cannot override actual binding owner without a complete owner contract. |
| `GAME/CAMPAIGN/WORLD/PLAYERS/` | `IMPLEMENTATION SCAFFOLD` | Native PLAYER storage/scaffold shape. |
| `GAME/CAMPAIGN/STATE/SCENES/` | `IMPLEMENTATION SCAFFOLD` | Campaign scene current-state base and LIVE route consumers. |
| `GAME/CORE/CAMPAIGN_SETUP.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Multiplayer mode/player setup only as reached from bootstrap/access graph. |
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Initial campaign/player/manifests where relevant; do not inspect unrelated setup behavior. |
| `GAME/TOOLS/init_campaign.py` | `IMPLEMENTATION / GENERATOR CONTRACT` | Initial PLAYER/index/MANIFEST/scene/live-related scaffold realization if current code creates those surfaces. |

If later traversal discovers additional templates/migrations/bootstrap files that actually own or initialize these fields, the manifest must expand before synthesis.

---

## 9. Current regression / scenario consumers

| Source | Classification | Current evidence / future disposition |
|---|---|---|
| `DEV/TESTS/ACCESS_CONTROL_CASES.md` | `IMPLEMENTATION / TEST CONTRACT` | Strong negative cases for repository permission != authority, stable external ID -> PLAYER, join policy, narrow self-enrollment and cross-campaign isolation. |
| `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md` | `IMPLEMENTATION / TEST CONTRACT` | Leave/removal/reactivation/controller continuity and absent-PC world continuity. `M10` current freeze/compact/deactivate sequence requires reconciliation with Step-5.8 revocation atomicity/currentness rules. |
| `DEV/TESTS/LIVE_SCENE_CASES.md` | `IMPLEMENTATION / TEST CONTRACT` | Broad current LIVE realization evidence. Several cases preserve useful outcomes while carrying stale physical assumptions: deterministic scene opening, one logical action/one write, one-file refresh, provisional/compaction model, campaign touch reconciliation, split/multi-scene freeze. Reconcile rather than inherit wholesale. |
| `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md` | `IMPLEMENTATION / TEST CONTRACT` | Campaign transaction/non-force and current one-file LIVE CAS assumptions. PT19/PT20 are physical realization evidence, not permission to override native-edge architecture. |
| `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md` | `IMPLEMENTATION / TEST CONTRACT` | Campaign selection/auth/bootstrap cached metadata and current routing consumers as reached. |
| `DEV/TESTS/INTEGRITY_CASES.md` | `IMPLEMENTATION / TEST CONTRACT` | Missing/stale/conflicting selected sources and bounded integrity handling where material. |
| `DEV/TESTS/CHRONOLOGY_CASES.md` | `IMPLEMENTATION / TEST CONTRACT / LIMITED` | Only CAS/technical order vs fictional chronology; WP-15 owns chronology and stale singleton/global cases remain its downstream debt. |
| `DEV/TESTS/EXPLICIT_SAVE_CASES.md` | `IMPLEMENTATION / TEST CONTRACT / LIMITED` | SAVE versus ACTIVE/CLOSED LIVE ownership where relevant; WP-13 owns save semantics. |
| `DEV/TESTS/PERFORMANCE_CASES.md` | `IMPLEMENTATION / TEST CONTRACT / LIMITED` | Performance expectations are non-semantic; optimization selection deferred to WP-24. |
| `DEV/TESTS/TODO_MULTIPLAYER_LIVE_BRANCH.md` | `IMPLEMENTATION / TEST TODO` | Manual/multi-session realization evidence only; TODO is not architecture authority. |

### 9.1 Test reinterpretation rules

Later work must preserve useful regression intent while reclassifying stale physical expectations. In particular:

- `one logical action -> one live write` is not a semantic law if Step-3/Step-5.8 define multiple native durability edges;
- `freeze -> compact -> deactivate` is not final authority withdrawal law if it leaves an authorization/current-route gap;
- scene pointer/participant list/source existence cannot substitute for typed claims/current route;
- stale LIVE write conflict must preserve already accepted RNG/idempotency but may require semantic revalidation under current native owners;
- cross-scene/global event slow path must not become a distributed transaction or fictional-order-by-freeze sequence.

---

## 10. Information / agency / execution neighbor owners

These sources are in the dependency graph only where they constrain WP-16; their domains are not reopened.

| Concern | Owner/source route | WP-16 boundary |
|---|---|---|
| player voluntary action / intent | R2.5 + `GAME/CORE/RUNTIME.md` player-agency rules | LIVE writability never grants another actor permission to invent absent player's choice. |
| fictional knowledge | Step 4 / `world.knowledge` contracts | LIVE `known_by_pc_ids` is evidence/projection/packing unless natural-owner contract says otherwise. |
| human disclosure | Step 5.12 / `runtime.disclosure` | physical shared source/readability does not prove PLAYER disclosure. |
| accepted communication evidence | `runtime.message` | LIVE event/text packing cannot replace message owner. |
| accepted execution / RNG | Step 3 / WP-12 / WP-15 | source conflict/close/recovery does not replay/reroll accepted work. |
| temporal/process occurrence | WP-15 | one semantic occurrence cannot double-establish through concurrent LIVE writers. |
| chronology | WP-15 | ref/CAS/absorption/freeze ordering has no automatic fictional meaning. |
| cleanup/ref retirement | Step 5.13 | unselected/absorbed/orphan source cleanup is post-authority and conservative. |

---

## 11. WP-17 boundary / downstream owners

| Source/domain | Classification | WP-16 treatment |
|---|---|---|
| R2.5 durable collaboration-obligation handoff | `DOWNSTREAM / DEFERRED OWNER` | Consume only agency/currentness constraints. Do not design its durable representation in WP-16. |
| WP-17 async collaboration | `DOWNSTREAM / DEFERRED OWNER` | Owns durable offline contribution collection, deadlines/fallbacks and collaboration lifecycle if/when activated. |
| WP-18 Dramaturg | `DOWNSTREAM / DEFERRED OWNER` | May consume current scopes/constraints; never player-control/LIVE authority. |
| WP-19/WP-20 bootstrap/migration | `DOWNSTREAM / DEFERRED OWNER` | Realize approved schema/scaffold changes after architecture closure. |
| WP-22 tests | `DOWNSTREAM / DEFERRED OWNER` | Executable conformance/failure injection for final WP-16 laws. |
| WP-24 performance | `DOWNSTREAM / DEFERRED OWNER` | Measure before repacking/partitioning optimization. |
| WP-26 consistency | `DOWNSTREAM / DEFERRED OWNER` | Repair stale CORE/schema/test/document wording after accepted architecture. |

---

## 12. Required Step-2 extraction matrix if Senior GO is later granted

The later evidence extraction must explicitly produce item-level dispositions for:

### Identity / access

- authenticated external user identity;
- campaign creator;
- PLAYER stable identity;
- external binding;
- active/inactive membership;
- join/self-enrollment/reactivation;
- controlled-PC assignment and transfer;
- policy authority;
- campaign/ref/repository operation authorization;
- cached/display/session/index projections.

### LIVE currentness / ownership

- current campaign route to selected LIVE;
- immutable typed claims and containment;
- exact source ref/revision fence;
- ACTIVE/CLOSED/absorbed/successor states;
- campaign base dependency versus current live owner;
- source movement/recovery;
- claim overlap/conflict diagnosis;
- prepared/orphan/unselected source nonauthority;
- post-authority cleanup.

### Semantic establishment / concurrency

- prospective local state;
- accepted execution continuity;
- native campaign edge;
- native LIVE CAS edge;
- ambiguous publication proof;
- stale CAS retry/revalidation;
- close race;
- partial multi-source outcomes;
- cross-scope semantic acceptance versus technical freeze order;
- no replay/reroll/force/global rollback.

### Agency / world continuity

- temporary absence;
- self-deactivation;
- creator deactivation;
- reactivation;
- controller transfer while inactive;
- absent PC remaining a world entity;
- automatic consequences versus unresolved voluntary choices;
- stale session after revocation.

### Machine realization

- scene/live schema field-by-field authority role;
- participant/PC/current-summary/index lists;
- one-file LIVE packing;
- live-born/provisional identity;
- touched/dependency evidence;
- exact route/currentness fields;
- bootstrap/generator/player-index surfaces;
- stale/current tests.

---

## 13. Reopen threshold

Do **not** reopen R2.5, Step-5.8 or WP-11..15 because a shipped CORE/schema/test artifact differs from them.

A reopen requires evidence of at least one:

```text
CONTRADICTION
    two current accepted owners impose mutually unsatisfiable laws

NEW UNSATISFIED CONSUMER
    a real current product/machine consumer cannot be represented under accepted owners

MATERIAL INSUFFICIENCY
    accepted law cannot decide a correctness-critical case needed by WP-16
```

Current Step-1 traversal found no such threshold. All observed gaps are framing/machine-realization reconciliation debt.

---

## 14. Open-world completeness gate

Current Step-1 source graph is:

```text
process/current-status authorities
+ R2.5 collaboration/multiplayer
+ Step-3 / Step-4 / Step-5.8 / Step-5.12 / Step-5.13 / Step-5.14
+ ACCESS_CONTROL / BRANCH_MODEL / policy-authority boundary
+ WP-11 / WP-12 / WP-13 / WP-14 / WP-15
+ MULTIPLAYER / LIVE_SCENE / RUNTIME / BOOTSTRAP_RUNTIME / SESSION / PERSISTENCE / STORAGE / INTEGRITY
+ limited INFORMATION / CHRONOLOGY / PROCESSES neighbors
+ PLAYER / LIVE / SCENE / SESSION / MANIFEST / CURRENT / event / PC / relevant runtime/info schemas
+ campaign PLAYER/SCENE/CURRENT/index/scaffold and generator paths
+ access/membership/live/persistence/bootstrap/integrity regression suites
+ WP-17 and other downstream owner boundaries
```

The manifest remains open-world through future Step 8. Step 2, if authorized, must refresh current `DEV/PROJECT_MAP.md`, remote branch state and actual references/search results before claiming evidence completeness.

---

## 15. Step-1 manifest gate

```text
SOURCE_MANIFEST_OPEN_WORLD:               YES
PROJECT_MAP_TRAVERSAL_PERFORMED:           YES
ACTUAL_OWNER_TRAVERSAL_PERFORMED:          YES
ACTUAL_RUNTIME_SCHEMA_TEST_CONSUMERS:      INCLUDED
R2_5_CONSUMED_AS_CONSTRAINT:               YES
STEP_5_8_CONSUMED_AS_CONSTRAINT:           YES
WP11_WP15_CONSUMED_AS_CONSTRAINTS:         YES
IDENTITY_PLAYER_PC_AUTH_CHAIN_EXPLICIT:    YES
CLOSED_UNABSORBED_EXPLICIT:                YES
MULTI_LIVE_CROSS_SCOPE_EXPLICIT:           YES
ABSENCE_AGENCY_BOUNDARY_EXPLICIT:          YES
WP17_BOUNDARY_EXPLICIT:                    YES
UPSTREAM_REOPEN_REQUIRED:                  NO
HUMAN_DECISION_REQUIRED:                   NO
STEP_2_AUTHORIZED:                         NO
NEXT_GATE:                                 MANDATORY SENIOR REVIEW
```

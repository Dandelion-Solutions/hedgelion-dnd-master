# Independent Senior Implementation Plan Re-review #2 Result

Verdict: **FAIL / REPAIR REQUIRED**

Open findings: **0 BLOCKING / 1 SIGNIFICANT / 0 MINOR**.

Reviewed repository: `Dandelion-Solutions/hedgelion-dnd-master`  
Reviewed branch: `v1/engine-rearchitecture`  
Reviewed remote HEAD: `b3d5ba14503458f9ca88b742d16e7a5ee46eaea4`  
Date: 2026-09-13  
Review scope: implementation-plan execution readiness only. Production implementation, migration, release and gameplay bootstrap were not executed.

## 1. Currentness and independence

The first authority reads were the remote ref and `DEV/CURRENT_PROGRESS.md`. This review followed the [final re-review #2 brief](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-implementation-planning-senior-re-review-2-final-brief.md), current AGENTS/runtime overlay and current package-index precedence. Author closure/PASS labels were treated as assertions to challenge, not evidence of completeness.

GitHub Connector was the sole repository transport. The review read control artifacts first, then RD-01 through RD-14 sequentially. Current v2 routes were used for RD-08/10/11. Canonical Step-2 readiness records were extracted by exact ID; transport-fetched text was held outside the model working set and only the relevant records/sections were exposed. No recursive repository reading, full HDM corpus load, recursive tree walk or indiscriminate dependency expansion was performed. Flat directory metadata served only to locate an exact current owner. PROJECT_MAP was not promoted to authority. PB manifests/closures, old critic rounds and unrelated GAME bodies were not used as blanket evidence.

The prior independent result was fetched from the current repository as required. Its conclusions were not inherited. The brief permits reuse of prior unchanged-route evidence: that reuse was limited to supporting dependency evidence after the comparisons below; each current RD's actual route, actions, tests and relevant readiness boundaries was checked again.

| Fresh comparison | Independently observed result |
|---|---|
| `3626a7be398fb648d6e8f0d52fda63193f1b12a4 -> 9bbad183dd8c82f281bf334940d25f8ba8131863` | Ahead 6, behind 0; 16 changed independent-review/control/planning files. No canonical semantic owner, runtime, schema or base RD implementation-plan drift. |
| `9bbad183dd8c82f281bf334940d25f8ba8131863 -> b3d5ba14503458f9ca88b742d16e7a5ee46eaea4` | Ahead 2, behind 0; six control/handoff files listed below. No semantic owner/runtime/schema drift. |
| Required repair CI | [Run 34786332166](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/actions/runs/34786332166), exact `9bbad183...`, completed SUCCESS; both “Run full maintenance audit” and “Run DEV unit tests” succeeded. |
| Currentness before result preparation | Fresh remote ref still equalled `b3d5ba14503458f9ca88b742d16e7a5ee46eaea4`. Publication must repeat this fence and preserve a single verified parent/non-force transition. |

Repair-to-review changed files:

- `DEV/CURRENT_PROGRESS.md` (modified, +28/-19).
- `DEV/docs/superpowers/plans/2026-09-13-implementation-planning-author-third-pass-self-review-closure.md` (added, +247/-0).
- `DEV/docs/superpowers/plans/2026-09-13-implementation-planning-execution-waves.md` (modified, +14/-0).
- `DEV/docs/superpowers/plans/2026-09-13-implementation-planning-package-index.md` (modified, +48/-73).
- `DEV/docs/superpowers/plans/2026-09-13-implementation-planning-package-master-plan.md` (modified, +35/-38).
- `DEV/docs/superpowers/plans/2026-09-13-implementation-planning-senior-re-review-2-final-brief.md` (added, +233/-0).

The 14 added execution-wave lines are condition-bound HG reminders. They add no semantic edge type or unconditional barrier; satisfied/reopen-only HG-01/04 and maturity-triggered HG-02/03/05/06/07/08 remain distinct. They do not authorize implementation or gameplay.

Effective route is base RD → SIRR overlay → first author addendum → second-pass addendum, with later text superseding only conflicting repaired details. In particular, the final overlay supersedes the earlier physical-Story ROOT_SELECTOR_CUTOVER barrier and forced BOUND/shared-generation wording. Old conflicting text was not reviewed as independently executable.

## 2. Finding

### SIRR2-001 — SIGNIFICANT — OWNER-ROUTED shipped LIVE/chronology consumers lack an executable cutover

**Affected closure:** residual SIRR-003; SIP-002/SIP-008/SIP-009; R071 / WP13-38, R077 / WP15-16 and the RD-09 LIVE consumer join supporting R079/R080.

**Current evidence**

1. [GAME/CORE/LIVE_SCENE.md, line 98](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/GAME/CORE/LIVE_SCENE.md#L98) says that a mutable entity physically participating in a live scene is operationally owned by that scene's epoch for scene-relevant state. This makes physical scene participation a write-owner boundary. [WP-16 LAW 14 and LAW 56](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md#L154) require the closed owner-typed claim grammar and explicitly forbid making scene membership that boundary. WP-16 §16 independently names this exact shipped file as stale debt.
2. [GAME/CORE/MULTIPLAYER.md, line 205](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/GAME/CORE/MULTIPLAYER.md#L205) still assigns compact globally reconciled chronology to `CURRENT.world_time.frontier`. [WP-15 §13 items 9 and 16](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md#L633) require removal/demotion of the generic global frontier and reconciliation of current CORE wording. Current RD-08 removes the field, but its explicit CORE targets are only `CHRONOLOGY.md` and `PROCESSES.md`.
3. [Current WP-13 v2 row 38 and consumer table](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md) label both CORE files **OWNER-ROUTED** to RD-09. [SIRR overlay A](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-implementation-planning-sirr-repair-amendments.md) supplies OWNER_JOIN_ONLY/integration-inspect routing and says alignment belongs to RD-09; it deliberately gives RD-06 no ownership of LIVE semantics.
4. [Current RD-09 allowed contracts and tasks](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-09-principal-live-currentness-plan.md) create access/LIVE runtime, replace the LIVE schema, modify identifier/catalog projections and add tests/audit routing. They name no modification of either CORE file. The SIRR close/absorb overlay adds lifecycle cases, not those missing shipped-file actions. Neither subsequent author addendum supplies them. All other 13 current RD routes were checked: none owns this cutover. RD-01's bounded R033/R050 scan concerns lifecycle/provisional/entity-epistemic debt, not a general authorization to repair LIVE claim geometry or global chronology.

**Why this changes the verdict**

The canonical laws and new machine plans are coherent, but the complete shipped package is not planned to converge on them. A worker following the exact writable routes can finish the new runtime/schema/test work while leaving contradictory active CORE instructions. Alternatively the worker must discover and author an additional material consumer task, its version consequences and acceptance cases during execution. OWNER-ROUTED is a pointer, not that task. A broad audit or new machine-only test cannot establish the missing consumer cutover. The correctly numbered WP13-38 row therefore remains incompletely executable; WP15-16's two-file target is also insufficient for the observed current third consumer.

This is one consumer-routing defect with two independently confirmed manifestations, not two severities counted for the same omission. It does not require inventing architecture or reopening the accepted WP-16/WP-15 laws.

**Required author repair and acceptance**

Name the exact owning modifications for both shipped CORE consumers, reconcile all implicated stale assertions with their current owners, name decisive positive/negative conformance tests and focused commands, and bind the changes to a coherent green checkpoint with the actual module Version Impact and shared-file/currentness joins. Reconcile WP13-38/WP15-16 and the bidirectional/package completion route to those executable actions. The next independent review must inspect the repaired actions and current bodies; “owner-routed”, an aggregate scan result or CI success alone is insufficient.

No author-package file was repaired during this review.

## 3. SIRR and ASR challenge matrix

“Closed” below means the identified planning defect is repaired in the effective route, not that future runtime tests have run.

| Finding | Independent disposition | Decisive evidence |
|---|---|---|
| SIRR-001 | Numbered semantic substitution repaired; complete proof gate still open through SIRR2-001 | All 17 WP-12 and 38 WP-13 source duties compared before current v2 rows; storage baseline, LIVE establishment and gameplay transport identities preserved. WP13-38 has an executable consumer gap. |
| SIRR-002 | Closed at plan level | RD-13 candidate → ordinary RD-06 publication → ACCEPTED-only promotion; frozen native/auth bases, rejection/indeterminate observation, exact-generation admission, bounded semantic rebase/rebuild/drop and inactive/re-enable behavior. |
| SIRR-003 | Partially repaired; OPEN | RD-06 SAVE_CONTRACT/PERSISTENCE and RD-04/RD-14 root/generator consumers now have exact actions. LIVE_SCENE/MULTIPLAYER remain pointer-only: SIRR2-001. |
| SIRR-004 | Closed at plan level | RD-04 owns MANIFEST/schema selectors; RD-13 consumes static story_root and exact WP-18 physical routes. |
| SIRR-005 | Closed at plan level | Phase A exact-source ACTIVE→CLOSED is independent of later phase B normalization/handoff/absorption; B failure leaves CLOSED_UNABSORBED current truth, zero writers, no reopen/fallback. |
| ASR-001 | Closed for selector/schema/version/root scope | Seven selectors in both exact RD-04 files; local schema 4→5 once; STORAGE material edit; bootstrap consumer edits and namespace distinctions. Final ASR-005 governs physical absence. |
| ASR-002 | Closed | Fresh WP-18 §6.3/§7/§8 permits ABSENT and BOUND; only BOUND requires exact accepted shared generation; dependency changes rebuild. |
| ASR-003 | Supporting-owner corrections confirmed; row-38 completion not fully closed | WP12-05 adds RD-05 accepted edge, WP12-11 adds trustworthy auth, WP13-19/20 use gameplay R2.6/WP-13 transport; residual pointer-only consumers remain SIRR2-001. |
| ASR-004 | Closed | Exact layer PROJECTION_STATE and decimal floor(sequence/1000) unit routes, four separate layers, no alternate allocator/index/frontier. |
| ASR-005 | Closed | Static selector may exist without physical Story; RD-04 green independently; RD-14 has no Story/T0 bootstrap prerequisite; R018 joins Story behavior later. |

## 4. Recomputed SIP-001..SIP-011

| Original finding | Independent current disposition | Evidence and limit |
|---|---|---|
| SIP-001 | Closed at plan level | RD-04 explicitly realizes allocator load/allocation/rekey, atomic allocator+record+required companion, campaign singleton and native HOT participation; source-native LIVE IDs excluded. |
| SIP-002 | OPEN | R015 reverse presence and R012 recovery read order have explicit repairs; SAVE/root/bootstrap additions are concrete. Remaining shipped LIVE/chronology consumers: SIRR2-001. |
| SIP-003 | Closed at plan level | RD-09 exact source extraction → RD-02 typed normalization → native information/history validation and handoff; explicit phase-A/phase-B failure distinction and recipient isolation. |
| SIP-004 | Closed at plan level | RD-03 assessment/validation/application, current revision and purpose, bounded continuity evidence, NO_CHANGE zero-write; real RD-03/RD-14 R031/R032 joins. |
| SIP-005 | Closed at plan level | RD-12 bounded obligation lineage, immutable clause, completeness-protected PLAYER companion, hold/close/fingerprint/original-clause handoff and current recovery/catch-up. |
| SIP-006 | Closed for original native history/Story/T0/Commentator/Dramaturg omissions | RD-13 supplies positive native history and conditional T0, Story-local baseline corpus/control/filter and repaired retained-generation publication/admission; no Story authority. |
| SIP-007 | Closed for startup/product scope | Exact generator identity and initial publication, provisional play, retrospective request, save→clear→menu, creator fail-closed; no full-sheet or physical Story gate. |
| SIP-008 | OPEN in identified consumer scope | All 14 current routes have green checkpoint/TDD execution structure; v2 routes and overlays honored. SIRR2-001 still requires a material unplanned file action. No separate recurrence of a knowingly-RED published checkpoint is asserted. |
| SIP-009 | OPEN in executable proof completeness | 125 individual appendix duties retained and semantically checked; nine proof IDs and eight parents preserved. WP13-38/WP15-16 targets do not discharge the current shipped-consumer obligation. Identity counts are not proof completeness. |
| SIP-010 | Closed at graph/scheduling level | All E1–E15 checked; owner-local roots independent; joins wait only on material evidence. False RD-04→RD-13 physical Story barrier explicitly superseded. Missing content at a valid join remains SIRR2-001. |
| SIP-011 | Closed | All 14 current RD maintenance commands spell `python3 DEV/TOOLS/run_maintenance_audit.py`; overlay/proof commands retain valid unittest module/class routing. |

## 5. Sequential RD executability record

All rows were reviewed in RD number order. Exact file/action inventories and named tests remain in the linked current plan; mandatory overlay deltas are called out below. For unchanged routes, canonical owners were not recursively reloaded: current exact readiness fields and base route were combined with unchanged-owner evidence established by the remote diff.

For every row, the effective global execution-wave/HDM protocol requires RED → GREEN → REFACTOR → focused VERIFY → coherent green commit, actual Version Impact classification (not automatic NONE), semantic System-Impact escalation and a fresh read of exact current owners/touched files before writing. A v2 plan's shorter local wording does not waive those controlling gates. Schema-only early checkpoints do not claim a later unimplemented behavioral suite is already passing.

### RD-01

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-01-shipped-stale-projection-repairs-plan.md). Direct IDs: `R001,R003,R033,R043,R047,R048,R050`.

- **Actions:** MODIFY the seven named INSTALL/CORE projections in the Impact Envelope; bounded R033/R050-only stale projection edits; NEW test_rd01_shipped_projection_repairs.py; audit assertions conditional.
- **Named RED / acceptance witnesses:** InstallProjectionTests; RandomnessProjectionTests; DomainExplorationTests; CoreCurrentProjectionTests.
- **GREEN acceptance:** Fixed transport/profile/defaults and current entity/lifecycle wording; no runtime behavior credited to prose.
- **REFACTOR / checkpoint:** Exact semantic scan patterns and owner-local prose reuse; green projection+test checkpoint.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Shipped module/launcher material revisions from actual delta; no schema/catalog/checkpoint or migration by default. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No new material choice found.

### RD-02

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-02-information-knowledge-disclosure-message-plan.md). Direct IDs: `R007,R008,R009,R017,R049,R052`.

- **Actions:** NEW information.py and exact native knowledge/disclosure/message/history candidate contracts; MODIFY listed PC/LIVE/event epistemic consumers only within owner scope; NEW test_rd02_information_native_contracts.py.
- **Named RED / acceptance witnesses:** NativeInformationSchemaTests; InformationNormalizationTests; LegacyInformationProjectionTests; RecipientIsolationTests; overlaid LiveClosedUnabsorbedTests.
- **GREEN acceptance:** Positive exact LIVE source → four typed normalizers → native validated candidates; recipient isolation; phase-B failure cannot undo phase A.
- **REFACTOR / checkpoint:** Native candidate helpers remain in information.py, no generic mutation service. Schema-only early checkpoint excludes later RED behavioral groups; normalization/join checkpoints follow.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Actual native schema/API plus legacy projection effects; RD-02/RD-03 PC/NPC/item and RD-04 location shared-file checkpoints. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No material choice; embedded-input N/A requires current proof.

### RD-03

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-03-actor-asset-effect-continuity-plan.md). Direct IDs: `R025,R026,R027,R028,R104,R108,R109,R110,R111,R113,R114,R115,R116,R126,R128,R129,R130,R132,R136`.

- **Actions:** NEW actor_continuity.py / continuity_projection.py and exact native Actor/Asset/Effect/continuity contracts; retire/reconcile named legacy PC/NPC/item projections; NEW focused test.
- **Named RED / acceptance witnesses:** NativeActorShapeTests; ActorAssessmentBehaviorTests; ContinuitySourceAdmissionTests; LegacyEntityProjectionTests; ActorMutationIntegrationTests; ProvisionalActorConsumerTests.
- **GREEN acceptance:** Assessment → deterministic validation → native application with current revision/purpose, bounded sources and NO_CHANGE zero-write; provisional identity survives READY_PC.
- **REFACTOR / checkpoint:** Only share structural definitions with distinct lifecycles preserved; no cognition engine. Native shape, behavior and cross-owner promotion each green.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Native family/API/schema effects and later parent reconciliation; explicit no legacy preservation. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No material choice found; native history/Story promotion is a named later join.

### RD-04

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-04-owner-native-routing-index-hot-plan.md). Direct IDs: `R015,R063,R064,R065,R066,R067`.

- **Actions:** NEW native_storage.py / id_allocator.py / hot_store.py; index/id_allocator/location contracts and STATE/ID_ALLOCATOR.yaml; overlaid MODIFY GAME/CAMPAIGN/MANIFEST.yaml, GAME/SCHEMA/campaign_manifest.schema.yaml, GAME/CORE/STORAGE.md, test_rd04_native_routing_index_hot.py and audit_engine.py.
- **Named RED / acceptance witnesses:** NativeRouteTests; CampaignAllocatorTests; PresenceAuthorityTests; NativeIndexTests; NativeHotStoreTests; NativeAtomicityTests; FixedCampaignRootSelectorTests.
- **GREEN acceptance:** Owner-valid routes, atomic allocator+record+companions, real native HOT participation and G/G+1; seven static roots; no reverse presence authority.
- **REFACTOR / checkpoint:** Private framing/policy adapters, no new identity service. Static selector/schema checkpoint independently green without Story files; family joins wait for each native shape only.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd04_native_routing_index_hot -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Manifest local schema 4→5; STORAGE 1.0.1→1.0.2 at current baseline; no campaign/storage-generation bump or prerelease migration solely for this change; fresh shared-file revision reconciliation. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No unselected root topology or physical Story design choice.

### RD-05

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-05-deterministic-execution-fixed-rng-plan.md). Direct IDs: `R034,R035,R036,R042,R046,R112`.

- **Actions:** NEW runtime_execution.py / mechanics.py, exact execution contracts and test_rd05_runtime_execution.py; MODIFY owned Procedure/Continuation temporal fields; narrow HOT consumer.
- **Named RED / acceptance witnesses:** AcceptedIdentityTests; FixedRngTests; ProposalValidationTests; LifecycleEvidenceTests; ProcedureTemporalStateTests; ContinuationTemporalStateTests; ExecutionAtomicityTests; DownstreamExecutionEvidenceTests.
- **GREEN acceptance:** Accepted identities/fixed RNG survive retry, native segment establishment is atomic, Procedure-local order/budget and typed continuation remainder, no future-RNG schedule.
- **REFACTOR / checkpoint:** Pure mechanics/private lifecycle validation; no generic workflow engine. Identity/lifecycle/atomicity/evidence checkpoints independently green.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd05_runtime_execution -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Existing/new execution schema/API and accepted interpretation effects; no duplicate temporal owner. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No material choice found.

### RD-06

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-06-save-durability-publication-plan.md). Direct IDs: `R037,R045,R069,R070,R071`.

- **Actions:** NEW durability.py / publication.py + two DEV operation contracts and focused test; bounded session/storage projections; SIRR Task 5 explicitly MODIFY GAME/CORE/SAVE_CONTRACT.md and PERSISTENCE.md; inspect/dispose DURABILITY_GUARD/STORAGE/ENGINE_UPDATES; LIVE/MP pointer-only.
- **Named RED / acceptance witnesses:** DurabilityPromiseContractTests; PublicationPlanTests; PublicationOutcomeTests; ExecutionDurabilityJoinTests; SaveContractCutoverTests; PersistencePublicationContractTests; ShippedPersistenceDispositionTests.
- **GREEN acceptance:** Scope-native SAVE, current compatible no-write evidence, frozen principal/H/tree/path/generations, tri-state outcome, accepted partial truth and exact published-generation clearing.
- **REFACTOR / checkpoint:** No external I/O in SQLite transaction, journal or rollback authority. Durability, publication and named cutover checkpoints require focused GREEN.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd06_durability_publication -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Actual API/schema and CORE material versions; STORAGE root/read-order joins stay RD-04/RD-07; WP13 all 38 duties required. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** OPEN SIRR2-001: OWNER_ROUTED LIVE/MP references cannot discharge missing shipped edits.

### RD-07

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-07-current-native-recovery-checkpoint-plan.md). Direct IDs: `R011,R012,R038,R072,R073,R074`.

- **Actions:** NEW recovery.py / exact recovery and maintenance contracts; MODIFY checkpoint/session/current manifest-pointer surfaces and GAME/CORE/STORAGE.md read order; focused test_rd07_recovery.py.
- **Named RED / acceptance witnesses:** CurrentSourceSelectionTests; StorageProjectionTests; AcceptedExecutionRecoveryTests; CheckpointDescriptorTests; SessionHotAuthorityTests; HistoricalMaintenanceTests; MaintenanceAuditMachineTests.
- **GREEN acceptance:** Current routing/native source first; healthy nullable checkpoint; no guessed latest; accepted execution retained; historical promotion is fresh forward publication and maintenance-isolated.
- **REFACTOR / checkpoint:** Source selection/hydration private to recovery; no generic currentness service. Current recovery, descriptor and historical maintenance checkpoints green.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd07_recovery -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Checkpoint/session/API and STORAGE effects from exact bytes; no installed maintenance dispatcher authorization. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No material choice found; selected-LIVE path joins RD-09, campaign-only path does not wait for it.

### RD-08

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-08-temporal-thread-current-state-plan-v2.md). Direct IDs: `R010,R039,R075,R076,R077`.

- **Actions:** Current v2: NEW temporal.py and typed temporal/chronology contracts; MODIFY thread/current_state/scene schemas, Procedure/Continuation through RD-05, CORE/CHRONOLOGY.md and CORE/PROCESSES.md; focused test.
- **Named RED / acceptance witnesses:** CurrentStateChronologyTests; WorldThreadContractTests; TemporalBindingAgendaTests; TemporalExecutionRecoveryTests; ChronologyBridgeTests; TemporalMachineAlignmentTests.
- **GREEN acceptance:** Narrow armed thread ownership, completeness-typed source routing/Agenda invalidation, accepted occurrence/no-reroll, typed chronology providers; remove global CURRENT and singleton scene frontier.
- **REFACTOR / checkpoint:** Owner-local extraction/rebuild; no global temporal authority. Local checkpoints green; §13 cross-owner duties join later.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd08_temporal -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Actual temporal schema/catalog/API and CORE effects; fresh owner/consumer fence in v2 plus global System gate. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** OPEN shared SIRR2-001 for additional current MULTIPLAYER frontier wording, not a new temporal design.

### RD-09

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-09-principal-live-currentness-plan.md). Direct IDs: `R013,R014,R019,R020,R040,R078,R079,R080`.

- **Actions:** NEW access_control.py / live_state.py, live-claim/publication-attempt contracts; REPLACE live_scene.schema.yaml; MODIFY source_native_live identifier/catalog projections; NEW test_rd09_access_live.py. No CORE/LIVE_SCENE.md or CORE/MULTIPLAYER.md modification.
- **Named RED / acceptance witnesses:** PrincipalAuthorizationTests; LiveEnvelopeClaimTests; LiveCurrentnessTests; SourceNativeIdentityTests; LivePublicationTests; LiveLifecycleTests; LiveInformationNormalizationIntegrationTests; LiveClosedUnabsorbedTests.
- **GREEN acceptance:** Trusted principal→one active PLAYER→control/operation auth, typed claim ownership, exact-source CAS, LIVE-born identity and phase-A close independent of phase-B absorption.
- **REFACTOR / checkpoint:** Private identity adapters, no generic ACL. Principal/claim/lifecycle/normalization checkpoints green; accepted CLOSED source retained on B failure.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd09_access_live -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Actual identifier/schema/API effects; principal/currentness hard prerequisites and exact fresh owners; no campaign+LIVE transaction. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** OPEN SIRR2-001: required shipped consumer actions remain absent.

### RD-10

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-10-role-handoff-protected-emission-plan-v2.md). Direct IDs: `R054,R055,R056,R057,R118,R133,R137`.

- **Actions:** Current v2: NEW turn_runtime.py / emission.py and listed typed envelope/handoff/emission contracts; MODIFY CORE/AI_REASONING.md; RUNTIME/PLAY_POLICY inspect; NEW test_rd10_role_emission.py.
- **Named RED / acceptance witnesses:** TurnEnvelopeContainmentTests; TypedHandoffTests; ProtectedCapacityTests; ProtectedEmissionTests; AuxiliaryFallbackTests; InstructionOwnerTests.
- **GREEN acceptance:** Typed terminal handoffs, protected Narrator materialization/emission and latest steering, purpose/recipient containment, finite auxiliary fallback.
- **REFACTOR / checkpoint:** Containment/emission remain narrow; no new semantic owner. Every v2 checkpoint RED→GREEN→REFACTOR→focused VERIFY.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd10_role_emission -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Envelope/API/projection effects under actual version rules; fresh current owners and global System gate. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No material choice found.

### RD-11

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-11-context-runtime-plan-v2.md). Direct IDs: `R059,R060,R097,R105,R106,R107,R117,R119,R120,R124,R125,R127,R134,R135,R138,R139,R140,R144,R145`.

- **Actions:** Current v2: NEW context_runtime.py / context_budget.py, DEV context-need-profile/context-trace schemas and test_rd11_context_runtime.py; native current_state/scene/index INSPECT_ONLY.
- **Named RED / acceptance witnesses:** ContextDiscoveryTests; ContextEligibilityTests; RequiredPacketClosureTests; ContextAllocationTests; OptionalRankingTests; RetrospectiveContextTests; ContextResultTraceTests; ScopedContextJoinTests.
- **GREEN acceptance:** Registered bounded discovery→currentness/eligibility→required closure/floors→optional allocation, witnessed-vs-mentioned ranking and starvation; three terminal results; dry-run diagnostic trace.
- **REFACTOR / checkpoint:** Ephemeral projection/allocation only. Eight named green checkpoints; R124/R122 joins use native RD-02/08/09/10/12 evidence.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd11_context_runtime -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Ephemeral profile/validation contracts and direct projections only; current join plans reread before closure. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No material choice found; no durable context or knowledge owner.

### RD-12

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-12-collaboration-multiplayer-plan.md). Direct IDs: `R021,R044,R081,R082,R083,R121,R123,R141,R142,R143,R146`.

- **Actions:** NEW collaboration.py, obligation/closed-basis/handoff/frontier/catch-up schemas and focused test; MODIFY existing intent-clause.schema.json and GAME/SCHEMA/player.schema.yaml; live_scene INSPECT_ONLY.
- **Named RED / acceptance witnesses:** CoordinationAdmissionTests; ObligationLineageTests; IntentClauseCollaborationTests; PlayerRouteCompanionTests; InputAssociationTests; ScopeLocalProgressTests; CloseHandoffTests; PublicationRecoveryTests; JoinRejoinCatchUpTests; CompositeBridgeTests.
- **GREEN acceptance:** Three coordination families, bounded immutable lineage/input semantics, completeness-protected route refs, hold→close/fingerprint→atomic original-clause handoff, scope-local safe progress and private catch-up.
- **REFACTOR / checkpoint:** Private collaboration lifecycle helpers, no generic workflow. Native obligation checkpoint excludes unimplemented PLAYER/IntentClause; later coherent extensions/joins green.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd12_collaboration -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Obligation, IntentClause and PLAYER/API effects; actual current native durability/currentness joins. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No material choice found; no CORE LIVE/MP cutover hidden here.

### RD-13

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-13-story-t0-commentator-history-plan.md). Direct IDs: `R022,R051,R084,R085,R099,R102,R131`.

- **Actions:** NEW history.py / story.py / commentator.py / dramaturg.py and exact native event/T0/Story/control/horizon contracts; REPLACE event schema; first-materialization Story paths and exactly DRAMATURG/SHARED.yaml plus DRAMATURG/PLAYERS/<player_id>.yaml; focused test.
- **Named RED / acceptance witnesses:** NativeHistoryAuthorityTests; T0BasisTests; StoryProjectionTests; StoryT0MaterializationTests; CommentatorSelfContainedTests; StoryPhysicalRouteTests; DramaturgPublicationTests; DramaturgAdmissionTests; DramaturgRebaseTests; CompositeIntegrationTests.
- **GREEN acceptance:** Native causal history separate from Story; sparse T0; Story-local qualifying corpus and pre-LLM metadata-safe control filter; exact layer/bucket routes; retained candidate promotes only after ordinary accepted publication, ABSENT/BOUND conditional.
- **REFACTOR / checkpoint:** No event bus/history DB/second ACL/planner publisher. Native history can be green before Story; projection and retained publication/admission checkpoints separate.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Native event/Story/T0/control/horizon namespaces assessed independently; MANIFEST owned by RD-04; no dormant partition system. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No material route/lifecycle choice left by overlays; local field spelling/cache implementation remains delegated within owners.

### RD-14

[Exact current plan](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-RD-14-bootstrap-onboarding-product-plan.md). Direct IDs: `R030,R086,R098,R100`.

- **Actions:** NEW bootstrap.py + bootstrap request/result/selection contracts and focused test; MODIFY INSTALL launcher/PROJECT_INSTRUCTIONS/README and conditional campaign README; overlays explicitly MODIFY CORE/BOOTSTRAP_RUNTIME.md and CAMPAIGN_SETUP.md; PROTECT init_campaign.py.
- **Named RED / acceptance witnesses:** CampaignSelectionBarrierTests; CreationIdentityTests; GeneratorScaffoldTests; GeneratorConsumerProjectionTests; InitialPublicationTests; ProgressiveOnboardingTests; MultiplayerJoinRejoinTests; OrdinaryRetrospectiveRoutingTests; SaveExitMenuTests; CreatorAuthorityTests; ShippedBootstrapProjectionTests; FailureRetryTests.
- **GREEN acceptance:** Explicit selection/exact identity→one generator→one initial tree/commit/non-force ref; provisional play without Story/T0; creator provenance; confirmed save before session-local clear/menu.
- **REFACTOR / checkpoint:** Bootstrap composition only. Selector validation consumes RD-04 static shape; no RD-13 physical Story wait. Generator/projection/identity checkpoint coherent.
- **Focused VERIFY:** `python3 -m unittest DEV.TESTS.test_rd14_bootstrap -v`; named class commands select the checkpoint's currently realized group. Maintenance audit and later full DEV discovery are separate supporting gates.
- **Version / System / currentness:** Verified headers: BOOTSTRAP_RUNTIME 0.8.8→1.0.9; CAMPAIGN_SETUP 1.0.3→1.0.4; launcher 19→20 once per combined logical edit; generator current generic copy/digest protected. Current source drift or new authority returns to planning; no worker may choose new semantics implicitly.
- **Remaining material choice/result:** No material product choice. Existing-router relocation requires concrete currentness evidence and preserves named R097 interface/tests.

## 6. Independent canonical identity and reverse accounting

Source: [WP-27 Step-2 ledger](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md), blob `c5475f7a25804516ce99cacac55335d7d499d963`. This was parsed from current Connector bytes, not from author totals.

| Predicate | Independent result |
|---|---|
| Source identities / unique source identities | 224 / 224 |
| Sources with a readiness terminal / distinct readiness terminals | 145 / 145 |
| Missing source→readiness target, terminal/backref mismatch, readiness→source mismatch | 0 / 0 / 0 |
| Current direct IDs from the 14 actual RD headers | 116, unique 116 |
| Pure-proof IDs | 9, disjoint from direct |
| Composite parents | 8, disjoint from direct and pure proof |
| Active union | 133 distinct canonical identities; no extra or duplicate direct owner |
| Canonical residual trigger set | 12; each activation/defer field inspected, no current activation inferred |
| No-work terminals / nonempty readiness backrefs | 79 / 0 |
| R004 | Absent from canonical readiness and current active routes |
| Coverage-v2 direct lists vs independently extracted current RD headers | Exact equality for all 14 RD lists |
| Runtime/proof-completeness inference from these numbers | None; SIRR2-001 remains open |

The RD records above retain every one of the 116 direct IDs individually, without treating a parent slice as a new active identity.

Pure proof: `R023,R031,R032,R041,R058,R061,R068,R088,R089`.  
Composite parents: `R006,R016,R018,R029,R053,R062,R087,R122`.  
Trigger-gated: `R002,R005,R024,R090,R091,R092,R093,R094,R095,R096,R101,R103`.

Trigger meanings remain distinct: R002/R024/R091/R092 release/package acceptance; R005/R090 real-MVP protocol evaluation; R093/R094/R095/R103 writer-specific measured growth/representation triggers; R096/R101 owner-scoped durability/failure exposure and supported-target calibration. Their negative constraints remain controlling, including no synthetic MVP, universal byte hard stop, global partition/health/retry service or prerelease compatibility project.

Every no-work terminal is retained below by source ID and exact terminal disposition:

| Terminal | Exact source IDs |
|---|---|
| NO_WORK_REJECTED (1) | `WP01-F04` |
| NO_WORK_ALREADY_REALIZED (35) | `WP01-F05`, `WP02-M05`, `WP03-F01`, `WP03-F02`, `WP03-F12`, `WP04-F01`, `WP05-F01`, `WP07-N02`, `WP18-03`, `WP21-03`, `WP22-04`, `WP23-03`, `WP25-05`, `WP26-01`, `WP26-03`, `WP26-04`, `PO006-01`, `PO007-01`, `D17`, `D20`, `S06`, `S16`, `S17`, `S20`, `S23`, `S38`, `S41`, `S42`, `S46`, `S47`, `S50`, `S51`, `S52`, `S53`, `S57` |
| NO_WORK_DEFERRED (39) | `WP03-F09`, `WP05-F10`, `WP09-04`, `WP10-02`, `WP10-04`, `WP10-05`, `WP18-04`, `WP19-03`, `WP20-01`, `WP20-02`, `WP20-03`, `WP20-04`, `WP21-01`, `WP21-02`, `WP25-01`, `WP25-02`, `WP25-03`, `PO004-01`, `D15`, `S01`, `S05`, `S08`, `S09`, `S12`, `S13`, `S15`, `S18`, `S24`, `S26`, `S30`, `S31`, `S32`, `S33`, `S34`, `S35`, `S37`, `S55`, `S56`, `S58` |
| NO_WORK_MEASUREMENT_DORMANT (2) | `WP24-01`, `WP24-05` |
| NO_WORK_DEFERRED_NATIVE_OWNER (1) | `WP26-02` |
| NO_WORK_DORMANT (1) | `S39` |

### Targeted reverse coverage

| Route | Independent result |
|---|---|
| R064 → RD-04 | Exact MANIFEST + manifest schema + STORAGE action; seven static selectors and local 4→5 transition. |
| R018.ROUTE_ROOT → RD-04 | Static owner topology exists independently of Story bytes; path appearance does not confer authority. |
| R016.STORY / R018.STORY → RD-13 | Exact projection-state and thousand-bucket unit routes; lifecycle/coverage tests; later package join with RD-04 selector. |
| R085 / R131 → RD-13 | Only two retained families; candidate/publication/admission/rebase and declared ABSENT/BOUND bases; no alternate publisher or singleplayer owner. |
| R030 / R086 → RD-14 | Exact generator/ruleset/root/schema and shipped consumer actions; SESSIONS physically present, Story static-only until materialization. |
| R068 → WP-12 v2 | All 17 current duties have semantically faithful named routes; no storage-baseline/HOT/currentness collapse. |
| R071 → WP-13 v2 | All 38 identities/themes present; row 38's LIVE/MP consumer routing is not executable: SIRR2-001. |
| All current task/action families → readiness/owner | No new RD, orphan subsystem or duplicate semantic owner found. The observed defect is missing required consumer work, not extra authorized implementation. |

## 7. Lossless proof and composite review

Every appendix row below was checked individually for semantic identity and a named witness/target. The WP-12/13 primary canonical sections were read before the current v2 routes. For unchanged appendices, current routes were read and the exact canonical numbered sections/themes were compared without opening their entire dependency graphs. This checks planned proof, not runtime behavior: **all future witnesses are NOT RUN in this review**.

The appendix comparison retains 17 + 38 + 13 + 9 + 22 + 26 = **125 individual duties**, including WP16-22's explicitly dormant empirical branch. There are 124 current deterministic/scenario/static duty rows, but not 124 proved implementations.

Codes: **ROUTED** = source semantics, named test and supporting task/contract match at planning level; **GAP F1** = SIRR2-001; **DEFERRED** = owner-triggered empirical evidence, not counted as current completion. STATIC_AUDIT is insufficient for a behavioral/integration duty; HOSTED_CI proves only what ran on its exact SHA.

### WP12 — §14 duties 1–17

[Canonical owner](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md); [current appendix](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md). Package witness class: `Wp12HotProofTests` in planned `DEV/TESTS/test_implementation_proof_ledger.py`. Every item below retains the exact named method from the current appendix as an independently checked planned witness.

| Item / exact planned witness | Independently checked duty | Supporting route / primary channel | Review |
|---|---|---|---|
| 1 / `test_wp12_01_owner_adoption_validates_native_identity_and_shape` | Owner adoption validates native family, native identity and native shape before HOT participation. | RD-04 native routing/HOT; FOCUSED_BEHAVIOR | ROUTED |
| 2 / `test_wp12_02_campaign_context_namespace_isolation` | Campaign/context namespaces are isolated; identical local keys cannot alias across admitted scopes. | RD-04 route/HOT namespace; FOCUSED_BEHAVIOR | ROUTED |
| 3 / `test_wp12_03_hot_possession_does_not_bypass_eligibility` | HOT possession/cached bytes cannot bypass role, access or information eligibility. | RD-04 + RD-09 + RD-02/RD-10 eligibility; INTEGRATION_SCENARIO | ROUTED |
| 4 / `test_wp12_04_sql_metadata_is_nonsemantic` | SQL row identity/order is not native identity, fictional chronology, priority or mechanics. | RD-04 + RD-08; INTEGRATION_SCENARIO | ROUTED |
| 5 / `test_wp12_05_native_edge_atomic_live_cas_authoritative` | Native/accepted execution establishment edge remains atomic; pre-CAS LIVE state is prospective, exact-source CAS establishes LIVE authority, post-CAS SQLite adoption is local only. | RD-04 HOT/native edge + RD-05 accepted execution/ExecutionSegment + RD-09 LIVE exact-source CAS/currentness; INTEGRATION_SCENARIO | ROUTED |
| 6 / `test_wp12_06_sqlite_transaction_contains_no_external_io` | No SQLite transaction spans external dialogue, repository or network I/O. | RD-04 HOT transaction; FOCUSED_BEHAVIOR | ROUTED |
| 7 / `test_wp12_07_resume_requires_compatible_interpretation_context` | Accepted execution resumes only under a compatible accepted interpretation/currentness context. | RD-05 + RD-07 + RD-08; INTEGRATION_SCENARIO | ROUTED |
| 8 / `test_wp12_08_known_id_hydrates_via_native_route_without_scan` | Known-ID hydration derives WP-11 native route without scan and validates full identity. | RD-04 route/index; FOCUSED_BEHAVIOR | ROUTED |
| 9 / `test_wp12_09_cache_or_index_absence_is_not_native_absence` | Cache/index absence is not native absence; rebuild from native authority succeeds. | RD-04 route/index/HOT; FOCUSED_BEHAVIOR | ROUTED |
| 10 / `test_wp12_10_disjoint_movement_preserves_overlap_revalidates` | Disjoint source movement can preserve local semantics; overlapping movement invokes owner revalidation. | RD-04 + RD-06/RD-09 currentness; INTEGRATION_SCENARIO | ROUTED |
| 11 / `test_wp12_11_frozen_publication_principal_and_generation_specific_clear` | Frozen publication records trustworthy principal/authorization plus exact generation G; success for G cannot clear G+1. | RD-06 frozen publication + RD-04 generation support + RD-09 principal/authorization evidence; INTEGRATION_SCENARIO | ROUTED |
| 12 / `test_wp12_12_no_generic_pending_or_publication_journal_authority` | HOT/recovery introduces no generic pending-work, publication-journal or second recovery authority. | RD-04 + RD-06 + RD-07; INTEGRATION_SCENARIO | ROUTED |
| 13 / `test_wp12_13_pre_cas_live_state_is_not_current` | Pre-CAS LIVE prospective state is not current/shared truth. | RD-09 LIVE currentness; FOCUSED_BEHAVIOR | ROUTED |
| 14 / `test_wp12_14_post_cas_adoption_failure_recovers_without_replay` | If LIVE CAS was accepted but local adoption failed, recover from accepted LIVE authority without gameplay/mechanics/RNG replay. | RD-09 + RD-07 + RD-05; INTEGRATION_SCENARIO | ROUTED |
| 15 / `test_wp12_15_cold_recovery_ignores_unpublished_hot_generation` | Cold recovery ignores unpublished local generations unless another durable/equivalent owner established them. | RD-07 + RD-04; INTEGRATION_SCENARIO | ROUTED |
| 16 / `test_wp12_16_storage_baseline_does_not_override_campaign_runtime` | Storage baseline may select runtime for New Game but cannot override an existing campaign runtime. | RD-14 bootstrap + storage/runtime owner; RD-06 proves no SAVE coupling; INTEGRATION_SCENARIO | ROUTED |
| 17 / `test_wp12_17_no_legacy_global_timer_frontier_or_checkpoint_debt` | Legacy global timer/frontier/checkpoint debt is not a WP-12 HOT law. | RD-04 + RD-06/RD-07 negative law; INTEGRATION_SCENARIO | ROUTED |

### WP13 — §15 duties 1–38

[Canonical owner](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md); [current appendix](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md). Package witness class: `Wp13DurabilityProofTests` in planned `DEV/TESTS/test_implementation_proof_ledger.py`. Every item below retains the exact named method from the current appendix as an independently checked planned witness.

| Item / exact planned witness | Independently checked duty | Supporting route / primary channel | Review |
|---|---|---|---|
| 1 / `test_wp13_01_serialization_is_not_semantic_establishment` | Serialization/persistence does not semantically establish gameplay state by itself. | RD-06 + native owner establishment; INTEGRATION_SCENARIO | ROUTED |
| 2 / `test_wp13_02_no_global_hour_timer_frontier_or_save_queue` | No campaign-global one-hour timer, durable frontier, save clock or universal HARD queue exists. | RD-06 durability; FOCUSED_BEHAVIOR | ROUTED |
| 3 / `test_wp13_03_scope_exposure_tracks_oldest_relevant_unpublished_state` | Scope exposure tracks the oldest still-relevant unpublished state for that scope, not a universal timestamp. | RD-06 durability; FOCUSED_BEHAVIOR | ROUTED |
| 4 / `test_wp13_04_risk_control_failure_is_not_implicitly_hard` | Risk-control durability failure does not become HARD merely from that failure absent a separate owner edge. | RD-06 + DURABILITY_GUARD consumer; FOCUSED_BEHAVIOR | ROUTED |
| 5 / `test_wp13_05_compatible_closure_is_distinct_from_pending_writes` | Required compatible closure is distinct from the pending write set. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 6 / `test_wp13_06_closure_is_bounded_and_native_routed` | Closure is bounded and native-routed; no universal campaign graph scan/frontier is required. | RD-06 + RD-04; INTEGRATION_SCENARIO | ROUTED |
| 7 / `test_wp13_07_explicit_save_freezes_definite_scope` | Explicit SAVE freezes one definite selected scope/root/generation set. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 8 / `test_wp13_08_save_composes_native_domains_without_global_transaction` | SAVE composes native-domain durability results; it does not impose global ordering, rollback or one cross-domain transaction. | RD-06 + RD-09 LIVE join; INTEGRATION_SCENARIO | ROUTED |
| 9 / `test_wp13_09_no_write_success_requires_current_compatible_closure` | A no-write SAVE success requires current compatible closure evidence, not merely an empty dirty set. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 10 / `test_wp13_10_partial_native_success_suppresses_overall_save_ack` | Partial native-domain success remains true evidence but cannot produce false overall SAVE acknowledgement. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 11 / `test_wp13_11_final_save_success_proves_current_compatible_composition` | Final SAVE success proves one current compatible composition for all required frozen domains. | RD-06; INTEGRATION_SCENARIO | ROUTED |
| 12 / `test_wp13_12_quiescence_release_requires_safe_disposition` | Quiescence/freeze is released only after safe success, explicit abandonment or owner-valid currentness/reconciliation; uncertainty cannot silently release it. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 13 / `test_wp13_13_publication_attempt_freezes_before_remote_mutation` | Campaign publication attempt freezes before the first remote mutation. | RD-06 publication; FOCUSED_BEHAVIOR | ROUTED |
| 14 / `test_wp13_14_frozen_attempt_contains_complete_currentness_basis` | Frozen attempt contains exact generations, authorization, reads/dependencies/currentness and path/index closure required for the mutation. | RD-06 + RD-04/RD-09; INTEGRATION_SCENARIO | ROUTED |
| 15 / `test_wp13_15_publication_requires_trustworthy_principal_authorization` | Trustworthy principal/authorization evidence is required; commit metadata or repository permission alone is insufficient. | RD-06 + RD-09; INTEGRATION_SCENARIO | ROUTED |
| 16 / `test_wp13_16_native_record_index_projection_delta_is_coherent` | WP-11 native record plus required index/projection UPSERT/DELETE participate coherently in one campaign-domain publication closure. | RD-04 + RD-06; INTEGRATION_SCENARIO | ROUTED |
| 17 / `test_wp13_17_bounded_resulting_tree_preflight_rejects_missing_invariant` | Resulting-tree preflight checks the bounded touched closure for missing required path/invariant before ref transition. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 18 / `test_wp13_18_normalized_noop_delta_does_not_publish` | Byte-identical UPSERT and already-absent DELETE normalize to no-op and do not force publication. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 19 / `test_wp13_19_supported_transport_is_connector_nonforce_path` | Supported gameplay campaign publication transport remains the admitted Python/core -> Connector -> non-force Git-data path. | RD-06 gameplay campaign publication + fixed R2.6/WP-13 gameplay GitHub transport contract; INTEGRATION_SCENARIO | ROUTED |
| 20 / `test_wp13_20_missing_connector_capability_has_no_transport_fallback` | Missing gameplay Connector capability does not authorize alternate shell git/gh/direct HTTP transport. | RD-06 gameplay publication negative path + fixed R2.6/WP-13 no-alternate-gameplay-transport law; INTEGRATION_SCENARIO | ROUTED |
| 21 / `test_wp13_21_campaign_boundary_uses_one_tree_single_parent_nonforce_transition` | One campaign publication boundary builds one base-derived tree, one single-parent commit and one non-force target-ref transition. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 22 / `test_wp13_22_ref_transition_has_three_epistemic_outcomes` | Target-ref transition result is explicitly `ACCEPTED`, `REJECTED` or `INDETERMINATE`. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 23 / `test_wp13_23_rejection_is_classified_before_retry` | A rejected transition is classified against current authority before retry. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 24 / `test_wp13_24_indeterminate_transition_blocks_ack_clear_release_and_replay` | INDETERMINATE forbids success acknowledgement, generation clear, quiescence release, gameplay replay and blind retry until reconciled. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 25 / `test_wp13_25_indeterminate_reconciliation_reads_bounded_authority` | Ambiguity reconciliation uses bounded current-ref plus lineage/current-closure observation. | RD-06; INTEGRATION_SCENARIO | ROUTED |
| 26 / `test_wp13_26_disjoint_movement_preserves_semantics_and_rng` | Disjoint target movement preserves already-established semantic IDs/RNG/outcomes and rebuilds only transport/currentness basis as needed. | RD-06 + RD-05; INTEGRATION_SCENARIO | ROUTED |
| 27 / `test_wp13_27_overlapping_movement_uses_owner_revalidation_not_text_merge` | Overlapping movement invokes owner-defined rejection/reconciliation and is never resolved by generic text merge. | RD-06 + affected owner; INTEGRATION_SCENARIO | ROUTED |
| 28 / `test_wp13_28_publication_retry_is_bounded` | Retry/reconciliation is bounded; no unbounded publication loop is permitted. | RD-06; FOCUSED_BEHAVIOR | ROUTED |
| 29 / `test_wp13_29_generation_g_success_preserves_g_plus_1` | Accepted publication for frozen generation G clears only G; concurrent/newer G+1 remains dirty. | RD-06 + RD-04 generation helper; INTEGRATION_SCENARIO | ROUTED |
| 30 / `test_wp13_30_unrelated_adoption_does_not_reset_other_scope_exposure` | Partial/unrelated adoption cannot reset another owner's dirty exposure basis. | RD-06; INTEGRATION_SCENARIO | ROUTED |
| 31 / `test_wp13_31_remote_success_local_loss_recovers_from_native_authority` | Crash after remote success but before local adoption recovers from native authority without a persistent publication journal or gameplay replay. | RD-06 + RD-07; INTEGRATION_SCENARIO | ROUTED |
| 32 / `test_wp13_32_live_exact_source_cas_remains_live_establishment` | LIVE exact-source CAS remains the LIVE establishment/currentness boundary and is not replaced by campaign SAVE publication. | RD-09 + RD-06 composition; INTEGRATION_SCENARIO | ROUTED |
| 33 / `test_wp13_33_checkpoint_is_not_save_handoff_or_currentness_proof` | Checkpoint creation is optional owner policy and is not itself SAVE success, handoff success or currentness proof. | RD-07 + RD-06; INTEGRATION_SCENARIO | ROUTED |
| 34 / `test_wp13_34_cached_head_is_not_authority` | Session/local cached HEAD is a hint/basis, not repository/current gameplay authority. | RD-07/RD-14 + RD-06 publication; INTEGRATION_SCENARIO | ROUTED |
| 35 / `test_wp13_35_storage_baseline_is_independent_from_campaign_save` | Storage-baseline transaction/metadata authority is independent from campaign SAVE composition. | RD-14 storage/bootstrap + RD-06; INTEGRATION_SCENARIO | ROUTED |
| 36 / `test_wp13_36_engine_rules_maintenance_reuses_publication_without_authority_broadening` | Engine/rules maintenance uses ordinary authorized campaign publication after its own compatibility/adoption checks; SAVE does not broaden maintenance authority. | RD-06 + current ENGINE_UPDATES consumer; INTEGRATION_SCENARIO | ROUTED |
| 37 / `test_wp13_37_git_order_and_time_do_not_define_fictional_chronology` | Git commit/ref order/time never manufactures fictional chronology or semantic priority. | RD-08 + RD-06; INTEGRATION_SCENARIO | ROUTED |
| 38 / `test_wp13_38_stale_consumer_and_test_dispositions_are_complete` | Every named stale SAVE/durability/publication regression consumer/test is explicitly repaired, owner-routed or proved non-applicable/current-conforming. | RD-06 + RD-04/RD-09/RD-14 consumer joins; STATIC_AUDIT + INTEGRATION_SCENARIO | GAP F1 |

### WP14 — §15 items 13–25

[Canonical owner](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md); [current appendix](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-implementation-planning-lossless-proof-ledger-wp14-wp15.md). Package witness class: `Wp14RecoveryProofTests` in planned `DEV/TESTS/test_implementation_proof_ledger.py`. Every item below retains the exact named method from the current appendix as an independently checked planned witness.

| Item / exact planned witness | Independently checked duty | Supporting route / primary channel | Review |
|---|---|---|---|
| 13 / `Wp14RecoveryProofTests.test_13_fixed_connector_currentness_conflict_failure` | fixed Connector capability/currentness/conflict/failure behavior | RD-07 + RD-06; INTEGRATION_SCENARIO | ROUTED |
| 14 / `Wp14RecoveryProofTests.test_14_checkpoint_export_exact_basis` | checkpoint export uses exact pinned basis and remains diagnostic | RD-07; FOCUSED_BEHAVIOR | ROUTED |
| 15 / `Wp14RecoveryProofTests.test_15_reset_last_checkpoint_no_guess_and_isolated` | reset-last-checkpoint path handles retention unavailable/no guessed pointer/maintenance isolation | RD-07; FOCUSED_BEHAVIOR | ROUTED |
| 16 / `Wp14RecoveryProofTests.test_16_forward_promotion_from_fresh_current_basis` | approved historical repair promotes forward from fresh current basis | RD-07 + RD-06; INTEGRATION_SCENARIO | ROUTED |
| 17 / `Wp14RecoveryProofTests.test_17_partial_promotion_truthful_outcomes` | partial multi-domain promotion/recomposition reports truthful incomplete/indeterminate outcomes | RD-07 + RD-06; INTEGRATION_SCENARIO | ROUTED |
| 18 / `Wp14RecoveryProofTests.test_18_allocator_non_regression_and_no_reuse` | allocator never regresses and published IDs are never reused across repair | RD-04 + RD-07; INTEGRATION_SCENARIO | ROUTED |
| 19 / `Wp14RecoveryProofTests.test_19_knowledge_disclosure_preserved` | historical repair preserves actual knowledge/disclosure state | RD-02 + RD-07; INTEGRATION_SCENARIO | ROUTED |
| 20 / `Wp14RecoveryProofTests.test_20_maintenance_no_gameplay_emission_rng_or_ids` | maintenance is isolated from gameplay: no emission, RNG, gameplay IDs or chronology | RD-07 + RD-05 + RD-10; INTEGRATION_SCENARIO | ROUTED |
| 21 / `Wp14RecoveryProofTests.test_21_maintenance_audit_native_machine_and_publication` | `runtime.maintenance_audit` has machine representation and uses current allocator/publication/idempotency | RD-07 + RD-04 + RD-06; INTEGRATION_SCENARIO | ROUTED |
| 22 / `Wp14RecoveryProofTests.test_22_historical_reader_respects_retention` | pinned historical reader obeys Step-5.13 semantic-retention boundary | RD-07; FOCUSED_BEHAVIOR | ROUTED |
| 23 / `Wp14RecoveryProofTests.test_23_repair_authorization_and_disclosure` | recovery/repair/support composes application authorization and recipient disclosure | RD-09 + RD-02 + RD-07; INTEGRATION_SCENARIO | ROUTED |
| 24 / `Wp14RecoveryProofTests.test_24_no_checkpoint_play_ready_or_save_prerequisite` | stale checkpoint-at-PLAY_READY and ordinary-save assumptions are removed | RD-07 + RD-06 + RD-14; INTEGRATION_SCENARIO | ROUTED |
| 25 / `Wp14RecoveryProofTests.test_25_wp14_conformance_failure_matrix_complete` | executable conformance/failure coverage covers final WP-14 laws, repairs and checkpoint-field authority boundaries | RD-07; STATIC_AUDIT | ROUTED |

### WP15 — §13 items 9–17

[Canonical owner](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md); [current appendix](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-implementation-planning-lossless-proof-ledger-wp14-wp15.md). Package witness class: `Wp15TemporalProofTests` in planned `DEV/TESTS/test_implementation_proof_ledger.py`. Every item below retains the exact named method from the current appendix as an independently checked planned witness.

| Item / exact planned witness | Independently checked duty | Supporting route / primary channel | Review |
|---|---|---|---|
| 9 / `Wp15TemporalProofTests.test_09_current_has_no_global_chronology_frontier` | remove/demote generic `CURRENT.world_time.frontier` | RD-08; FOCUSED_BEHAVIOR | ROUTED |
| 10 / `Wp15TemporalProofTests.test_10_scene_has_no_singleton_chronology_frontier` | remove/demote mandatory singleton scene chronology-frontier semantics | RD-08; FOCUSED_BEHAVIOR | ROUTED |
| 11 / `Wp15TemporalProofTests.test_11_typed_chronology_relation_provider_evidence` | realize explicit typed chronology relation/provider evidence where legacy fields are ambiguous | RD-08 + RD-13; INTEGRATION_SCENARIO | ROUTED |
| 12 / `Wp15TemporalProofTests.test_12_procedure_owns_local_timing_order_budget` | Procedure schema owns procedure-local timing/order/budget state | RD-05; FOCUSED_BEHAVIOR | ROUTED |
| 13 / `Wp15TemporalProofTests.test_13_continuation_has_no_generic_future_rng_schedule` | remove/qualify generic Continuation `future_rng_frontier`; type `unconsumed_advancement` as accepted-execution remainder | RD-05; FOCUSED_BEHAVIOR | ROUTED |
| 14 / `Wp15TemporalProofTests.test_14_information_projection_normalization` | normalize PC/LIVE/event information fields into native information owners/projections | RD-02 + RD-09 + RD-13; INTEGRATION_SCENARIO | ROUTED |
| 15 / `Wp15TemporalProofTests.test_15_temporal_discovery_indexes_non_authoritative` | process/thread discovery indexes are non-authoritative and cannot prove temporal-root absence | RD-04 + RD-08; INTEGRATION_SCENARIO | ROUTED |
| 16 / `Wp15TemporalProofTests.test_16_core_temporal_wording_reconciled` | reconcile current CORE wording for simulation budget, chronology frontier and visibility | RD-08; STATIC_AUDIT | GAP F1 |
| 17 / `Wp15TemporalProofTests.test_17_temporal_failure_injection_matrix_complete` | regression/failure-injection covers final temporal/process/chronology laws | RD-08; INTEGRATION_SCENARIO | ROUTED |

### WP16 — §15 duties 1–22

[Canonical owner](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md); [current appendix](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-implementation-planning-lossless-proof-ledger-wp16-wp17.md). Package witness class: `Wp16LiveAccessProofTests` in planned `DEV/TESTS/test_implementation_proof_ledger.py`. Every item below retains the exact named method from the current appendix as an independently checked planned witness.

| Item / exact planned witness | Independently checked duty | Supporting route / primary channel | Review |
|---|---|---|---|
| 1 / `Wp16LiveAccessProofTests.test_01_stable_external_user_id_not_login` | stable external user ID is distinct from mutable login/display metadata | RD-09; FOCUSED_BEHAVIOR | ROUTED |
| 2 / `Wp16LiveAccessProofTests.test_02_exactly_one_active_player_binding` | stable user ID resolves to exactly one current active PLAYER binding | RD-09; FOCUSED_BEHAVIOR | ROUTED |
| 3 / `Wp16LiveAccessProofTests.test_03_control_and_operation_authorization_separate` | controlled-PC and operation-specific authorization are separate from PLAYER membership | RD-09 + RD-12; INTEGRATION_SCENARIO | ROUTED |
| 4 / `Wp16LiveAccessProofTests.test_04_post_selection_owner_revalidation` | post-selection mutable gameplay revalidates current owner/application authority | RD-09; INTEGRATION_SCENARIO | ROUTED |
| 5 / `Wp16LiveAccessProofTests.test_05_closed_live_claim_grammar` | LIVE uses only closed typed claim grammar | RD-09; FOCUSED_BEHAVIOR | ROUTED |
| 6 / `Wp16LiveAccessProofTests.test_06_live_claim_excludes_campaign_access_routing_authority` | access/routing/campaign authority cannot be LIVE-claimed | RD-09; FOCUSED_BEHAVIOR | ROUTED |
| 7 / `Wp16LiveAccessProofTests.test_07_bounded_claim_overlap_and_write_authority_lookup` | claim overlap/containment is bounded and `WriteAuthorityLookup` yields one current writer or conflict | RD-09; INTEGRATION_SCENARIO | ROUTED |
| 8 / `Wp16LiveAccessProofTests.test_08_exact_live_source_revision_is_cas_fence` | exact selected LIVE source/ref revision is currentness/CAS fence | RD-09; INTEGRATION_SCENARIO | ROUTED |
| 9 / `Wp16LiveAccessProofTests.test_09_frozen_live_attempt_revalidates_authorization` | frozen LIVE publication attempt is ephemeral/immutable and independently revalidates authorization/currentness | RD-09; INTEGRATION_SCENARIO | ROUTED |
| 10 / `Wp16LiveAccessProofTests.test_10_live_lifecycle_and_closed_unabsorbed` | ACTIVE/CLOSED/CLOSED_UNABSORBED/absorbed/successor lifecycle preserves current truth and zero-writer states | RD-09; INTEGRATION_SCENARIO | ROUTED |
| 11 / `Wp16LiveAccessProofTests.test_11_revocation_no_window_transfer` | revocation/controller transfer closes affected LIVE first with no authority window | RD-09; INTEGRATION_SCENARIO | ROUTED |
| 12 / `Wp16LiveAccessProofTests.test_12_additive_activation_no_rollover_only_when_safe` | additive activation/reactivation may avoid rollover only under owner-proven no-conflict conditions | RD-09; INTEGRATION_SCENARIO | ROUTED |
| 13 / `Wp16LiveAccessProofTests.test_13_source_native_live_identity_admitted_per_kind` | externally referenceable LIVE-born identity uses explicit `source_native_live`/owner-equivalent admission | RD-09; FOCUSED_BEHAVIOR | ROUTED |
| 14 / `Wp16LiveAccessProofTests.test_14_no_campaign_allocator_or_rekey_for_live_identity` | LIVE-born identity never falls back to campaign allocator and never rekeys on absorption | RD-09 + RD-04; INTEGRATION_SCENARIO | ROUTED |
| 15 / `Wp16LiveAccessProofTests.test_15_multi_live_forward_transition_no_distributed_rollback` | multi-LIVE freeze/forward transition does not create distributed rollback/transaction semantics | RD-09 + RD-06; INTEGRATION_SCENARIO | ROUTED |
| 16 / `Wp16LiveAccessProofTests.test_16_live_retry_preserves_accepted_execution_rng` | accepted execution/RNG/idempotency survives LIVE retry/recovery without replay | RD-05 + RD-07 + RD-09; INTEGRATION_SCENARIO | ROUTED |
| 17 / `Wp16LiveAccessProofTests.test_17_live_transport_order_not_chronology` | Git/ref/CAS/freeze ordering is not fictional chronology | RD-08 + RD-09; INTEGRATION_SCENARIO | ROUTED |
| 18 / `Wp16LiveAccessProofTests.test_18_live_information_owner_separation` | LIVE physical storage remains separate from Lore/Knowledge/Disclosure/information authority | RD-02 + RD-09 + RD-13; INTEGRATION_SCENARIO | ROUTED |
| 19 / `Wp16LiveAccessProofTests.test_19_presence_absence_not_agency_or_authority` | absence/deactivation does not synthesize agency; presence is not authority | RD-09 + RD-12; INTEGRATION_SCENARIO | ROUTED |
| 20 / `Wp16LiveAccessProofTests.test_20_live_recovery_state_matrix` | recovery handles ACTIVE/CLOSED_UNABSORBED/successor/missing/orphan/moved source states without campaign fallback | RD-07 + RD-09; INTEGRATION_SCENARIO | ROUTED |
| 21 / `Wp16LiveAccessProofTests.test_21_live_native_durability_edge_granularity` | native durability edge granularity follows owner/source acceptance, not one-user-action/one-write fiction | RD-05 + RD-06 + RD-09; INTEGRATION_SCENARIO | ROUTED |
| 22 / `Wp16LiveAccessProofTests.test_22_hot_path_measurement_requires_real_target` | bounded hot-path/read/write behavior under measured target workload | WP-24 measurement route only after a real target workload/profile exists; deterministic tests may instrument but cannot claim this empirical result; EMPIRICAL_DEFERRED | DEFERRED |

### WP17 — §28 themes in source order 1–26

[Canonical owner](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-canonical-spec.md); [current appendix](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/b3d5ba14503458f9ca88b742d16e7a5ee46eaea4/DEV/docs/superpowers/plans/2026-09-13-implementation-planning-lossless-proof-ledger-wp16-wp17.md). Package witness class: `Wp17CollaborationProofTests` in planned `DEV/TESTS/test_implementation_proof_ledger.py`. Every item below retains the exact named method from the current appendix as an independently checked planned witness.

| Item / exact planned witness | Independently checked duty | Supporting route / primary channel | Review |
|---|---|---|---|
| 1 / `Wp17CollaborationProofTests.test_01_three_coordination_families` | all three coordination families are distinguished | RD-12; FOCUSED_BEHAVIOR | ROUTED |
| 2 / `Wp17CollaborationProofTests.test_02_independent_input_has_no_obligation` | `INDEPENDENT_IMMEDIATE` creates no durable collaboration obligation | RD-12; FOCUSED_BEHAVIOR | ROUTED |
| 3 / `Wp17CollaborationProofTests.test_03_rule_owned_ordered_excluded_from_collaboration` | Rule-owned Procedure/Continuation/Choice/Reaction collection stays with native ordered owner | RD-12 + RD-05; INTEGRATION_SCENARIO | ROUTED |
| 4 / `Wp17CollaborationProofTests.test_04_obligation_admission_and_lineage` | durable obligation admission and stable obligation lineage/generation are bounded | RD-12; FOCUSED_BEHAVIOR | ROUTED |
| 5 / `Wp17CollaborationProofTests.test_05_required_vs_optional_contributors` | required contributors are minimal/material; optional contributors never block by silence | RD-12; FOCUSED_BEHAVIOR | ROUTED |
| 6 / `Wp17CollaborationProofTests.test_06_player_route_companion_complete_and_nonauthoritative` | PLAYER routing companion is completeness-protected but non-authoritative | RD-12; INTEGRATION_SCENARIO | ROUTED |
| 7 / `Wp17CollaborationProofTests.test_07_rejoin_recovers_without_global_scan` | multi-player join/rejoin recovers current obligations without global scan | RD-12 + RD-14; INTEGRATION_SCENARIO | ROUTED |
| 8 / `Wp17CollaborationProofTests.test_08_intent_clause_semantics_immutable` | collaboration-relevant IntentClause is one immutable material semantic unit | RD-12; FOCUSED_BEHAVIOR | ROUTED |
| 9 / `Wp17CollaborationProofTests.test_09_value_contribution_collision_negative` | existing mechanical `value.contribution` is never reused as human collaboration input | RD-12; STATIC_AUDIT | ROUTED |
| 10 / `Wp17CollaborationProofTests.test_10_held_actionable_clause_has_no_command` | held ACTIONABLE_INTENT remains pending with no premature RuntimeCommand | RD-12 + RD-05; INTEGRATION_SCENARIO | ROUTED |
| 11 / `Wp17CollaborationProofTests.test_11_handoff_releases_original_clause` | successful close hands execution back to the original Step-3 clause path | RD-12; INTEGRATION_SCENARIO | ROUTED |
| 12 / `Wp17CollaborationProofTests.test_12_no_synthetic_multi_interaction_command` | collaboration never synthesizes multi-Interaction/system command identity or arrival-order execution anchor | RD-12; FOCUSED_BEHAVIOR | ROUTED |
| 13 / `Wp17CollaborationProofTests.test_13_duplicate_same_input_identity_idempotent` | duplicate same `(interaction_id,clause_id)` association is idempotent | RD-12; FOCUSED_BEHAVIOR | ROUTED |
| 14 / `Wp17CollaborationProofTests.test_14_same_prose_new_interaction_new_identity` | identical prose in later Interaction is a new input identity | RD-12; FOCUSED_BEHAVIOR | ROUTED |
| 15 / `Wp17CollaborationProofTests.test_15_stale_generation_input_cannot_carry_forward` | stale/terminal old-generation input does not mutate/reopen successor | RD-12; INTEGRATION_SCENARIO | ROUTED |
| 16 / `Wp17CollaborationProofTests.test_16_controller_change_requires_successor_or_obsolete` | controller/authorization change re-evaluates opportunity and uses successor/obsolete semantics | RD-12 + RD-09; INTEGRATION_SCENARIO | ROUTED |
| 17 / `Wp17CollaborationProofTests.test_17_close_input_race_and_semantic_set_union` | close/input races preserve semantic set union only for still-current same-generation OPEN input | RD-12; INTEGRATION_SCENARIO | ROUTED |
| 18 / `Wp17CollaborationProofTests.test_18_maximal_safe_visible_frontier` | progression exposes maximal safe/visible frontier before waiting | RD-12; INTEGRATION_SCENARIO | ROUTED |
| 19 / `Wp17CollaborationProofTests.test_19_absence_not_consent_or_immunity` | absence is neither consent nor immunity from owner-proven automatic consequence | RD-12; INTEGRATION_SCENARIO | ROUTED |
| 20 / `Wp17CollaborationProofTests.test_20_no_timeout_or_presence_correctness` | timeout/presence/heartbeat/message age never closes voluntary agency dependency | RD-12; FOCUSED_BEHAVIOR | ROUTED |
| 21 / `Wp17CollaborationProofTests.test_21_technical_order_not_fictional_chronology` | arrival/CAS/ID/publication order never establishes fictional chronology | RD-12 + RD-08; INTEGRATION_SCENARIO | ROUTED |
| 22 / `Wp17CollaborationProofTests.test_22_recipient_safe_catch_up` | catch-up is recipient-safe and contains no other player's private input/context | RD-12 + RD-10 + RD-02; INTEGRATION_SCENARIO | ROUTED |
| 23 / `Wp17CollaborationProofTests.test_23_message_compaction_preserves_content_sufficiency` | lawful message compaction cannot erase content needed by live collaboration consumer | RD-12; INTEGRATION_SCENARIO | ROUTED |
| 24 / `Wp17CollaborationProofTests.test_24_campaign_live_currentness_without_distributed_transaction` | campaign/LIVE currentness movement composes without distributed transaction | RD-12 + RD-06 + RD-09; INTEGRATION_SCENARIO | ROUTED |
| 25 / `Wp17CollaborationProofTests.test_25_collaboration_recovery_lifecycle_matrix` | recovery handles OPEN/CLOSED/RESOLVED/OBSOLETE current generations through exact routes | RD-12 + RD-07; INTEGRATION_SCENARIO | ROUTED |
| 26 / `Wp17CollaborationProofTests.test_26_no_replay_or_reroll_accepted_mechanics` | stale/late collaboration metadata never replays/rerolls accepted mechanics/Continuation | RD-12 + RD-05 + RD-07; INTEGRATION_SCENARIO | ROUTED |

The source-theme comparison is one-to-one for all 125 rows, including the repaired WP12-05 HOT/ExecutionSegment/LIVE establishment edge, WP12-11 frozen publication plus trustworthy authorization, and WP13-19/20 fixed **gameplay** transport/no-alternate-runtime-transport laws. This does not make the two GAP rows executable. WP16's new machine witnesses are well routed, but their positive claim/currentness behavior must also agree with the still-unassigned shipped consumers in SIRR2-001.

### WP13-38 consumer disposition challenge

| Exact current surface | Independent body evidence / effective action |
|---|---|
| SAVE_CONTRACT.md | Current universal campaign-only SAVE wording confirmed; SIRR overlay explicitly assigns RD-06 modification and SaveContractCutoverTests. |
| PERSISTENCE.md | RD-06 explicit frozen authorization/generation/result/reconcile/closure update plus PersistencePublicationContractTests; no second publisher. |
| DURABILITY_GUARD.md | Current body has scope-relative NORMAL/ELEVATED/DANGER, no generic frontier/heartbeat/HARD promotion; current-conforming for this WP-13 scope, recheck at implementation. |
| STORAGE.md | Current body still lists five roots and checkpoint-first loading; exact RD-04 seven-selector and RD-07 current-native-first modifications exist. Storage baseline remains independently owned. |
| ENGINE_UPDATES.md | Current body preserves maintenance's own authority/compatibility gates, ordinary frozen campaign publication and storage-baseline independence; scoped current-conforming classification supported. |
| LIVE_SCENE.md / MULTIPLAYER.md | Current contradictions confirmed; OWNER_ROUTED does not lead to a writable task: GAP F1. |
| BOOTSTRAP_RUNTIME.md / CAMPAIGN_SETUP.md | Current missing digest call/projection, old schema-v3 and five-root wording; RD-14 overlays now explicitly modify both. |
| INSTALL/00_DND_BOOTSTRAP.md | Current launcher already passes ruleset digest but physical root list omits existing SESSIONS; final overlay requires modification without requiring Story files. |
| init_campaign.py | Fresh body lines 34–66 and 68–124: required digest argument, generic copytree, created/current ruleset digest propagation; no hard-coded old root copy list. Protection is scoped to those claims, not a claim that future sibling template changes need no verification. |
| Discovered stale assertions | RD-06 ShippedPersistenceDispositionTests names rewrite/retire/dispose in the same green checkpoint. It cannot replace the missing explicit LIVE/chronology consumer task. |

Version owner comparison independently supports local manifest schema 4→5, module-local increments and one launcher increment for the combined future edit. Current prerelease clean-slate law removes obsolete compatibility/migration debt; it does not remove truthful local schema identity. No actual version namespace changes are made by this review.

### Nine pure-proof leaves

| ID | Checked named witness / target | Current planning disposition |
|---|---|---|
| R023 | Stage3PackageProofTests; native path/catalog/schema invariants plus behavioral targets | Routed; static regressions do not replace behavior. |
| R031 | ActorReadinessProofTests; RD-03/RD-14 provisional READY_PC/lazy derivation/no retrofit | Routed positive consumer. |
| R032 | DomainCommitmentProofTests; reconstructable build/rules and initial domain commitment | Current behavior routed; real-target performance branch deferred. |
| R041 | ExecutionRetryProofTests; RD-05/07/08 accepted RNG, stale continuation and child-crash boundary | Routed; no replay witness substituted by schema shape. |
| R058 | RoleContainmentProofTests; source escalation/rebind/safe emission/finite UNSATISFIABLE | Current scenarios routed; empirical branch deferred. |
| R061 | ContextBoundednessProofTests; typed bounded discovery/no scan/degradation/owner separation | Routed; supported-target empirical evaluation deferred. |
| R068 | Wp12HotProofTests; all 17 rows above | Semantic-numbering repair confirmed; required owner/interface joins preserved. |
| R088 | OwnerFirstReconciliationProofTests; positive/negative/failure/indeterminate and reverse reconciliation | Closure cannot pass while F1 remains. |
| R089 | ProofChannelDisciplineTests + exact-head CI | Channels distinct; CI cannot close F1 or unrun behavior. |

### Eight composite parents

| Parent | Required native slices, individually retained | Package witness / independent disposition |
|---|---|---|
| R006 | RD-02 INFO + RD-03 ACTOR + RD-08 THREAD_VISIBILITY | CompositeR006ProofTests; all slices routed, no second knowledge authority. |
| R016 | RD-02 INFO + RD-03 ACTOR + RD-05 EXECUTION + RD-08 TEMPORAL + RD-09 LIVE + RD-12 COLLAB + RD-13 STORY | CompositeR016ProofTests; static selector and exact Story behavior repaired; package consumer convergence still subject to F1. |
| R018 | All R016 families plus RD-04 ROUTE_ROOT | CompositeR018ProofTests; per-family native route/body/load/HOT or owner-approved no-record disposition; later Story join, no startup barrier. |
| R029 | RD-03 ACTOR + RD-06 DURABILITY + RD-14 ONBOARDING | CompositeR029ProofTests; provisional identity/durability/readiness join, no full sheet or Story prerequisite. |
| R053 | RD-02 INFO + RD-09 LIVE normalization/currentness | CompositeR053ProofTests; positive exact-source normalization and phase-B failure truth, no LIVE disclosure owner. |
| R062 | RD-02 KNOWLEDGE/DISCLOSURE/MESSAGE + RD-03 ACTOR_CONTINUITY/EFFECT + RD-05 runtime lifecycle/evidence + RD-08 TEMPORAL_BINDING + RD-13 SEMANTIC_EVENT_HISTORY | CompositeR062ProofTests; native semantic/history authority separate from projections. |
| R087 | RD-11 RETROSPECTIVE + RD-13 SEMANTIC_EVENT_T0 + RD-14 SAVE_SESSION_MENU | CompositeR087ProofTests; conditional sparse T0 and in-band zero-extra-serial capture, not a startup dependency. |
| R122 | RD-08 CHRONOLOGY + RD-09 CURRENTNESS_SCENE + RD-11 CONTEXT + RD-12 COLLABORATION_BRIDGE | CompositeR122ProofTests; only a concrete material bridge supplies scoped evidence, no universal frontier. |

All eight require real native interface joins, negative authority-transfer assertions and `CompositeVersionImpactProofTests` reconciling sibling schemas/APIs/catalog/checkpoint/version effects once at parent closure. No slice label alone closes a parent. R099's retained-T0/T1-mutation, invalid current-pointer/hidden-reasoning rejection, bounded lookup and zero-extra-serial requirements remain explicit in the control ledger; real-target critical-path observation remains deferred. R102 retains Story-local T0, pre-LLM protected-cache exclusion, locally decidable control, content-final/control-refresh separation and no second ACL/history owner.

## 8. E1–E15 dependency and scheduling check

| Edge | Independent effective meaning / result |
|---|---|
| E1 | Family-local final shape joins RD-04 route/body/HOT. No universal schema-first or all-family barrier. |
| E2 | Actor shape feeds provisional/onboarding completion; R031/R032 proof follows RD-03/RD-14 behavior. |
| E3 | Accepted execution establishment joins durability; unrelated RD-06 planner preparation remains independent. |
| E4 | R069 HARD_PRECEDES R070. R071 completion joins all 38 duties and exact shipped consumers; F1 blocks this content closure, not unrelated LIVE work. |
| E5 | Route/HOT and current campaign publication evidence join current-native recovery. RD-09 required only for selected-LIVE recovery, not all campaign recovery. |
| E6 | R075 HARD_PRECEDES R076; R039 occurrence joins accepted execution; Procedure/Continuation and information/history duties join R077 later. F1 prevents full current CORE wording closure. |
| E7 | R078 HARD_PRECEDES R079; R040 accepted execution and R053 information joins are scoped. Phase A fence can complete before phase B normalization/absorption; CLOSED_UNABSORBED is not a reopened writer. |
| E8 | R054/R055 join R056; R056 precedes protected R057; context acceptance joins R059/R060 and eligibility. R139 ranking never grants authority. |
| E9 | Native collaboration family/input/currentness joins R082 acceptance; R124 joins disclosure/currentness/role/controlled-actor scope. RD-11 and RD-12 cores are not cyclic. |
| E10 | R099 precedes qualifying Story/Commentator use; native history remains independent. Final overlay assigns static selectors to RD-04, on-demand exact physical Story to RD-13; RD-14 does not wait for physical Story. |
| E11 | RD-13 candidate core may start independently. Retained publication/admission completion joins RD-06 publication, RD-09 access/currentness, RD-10 containment, RD-12 collaboration and exact native dependencies. Player-local shared generation required only for BOUND. |
| E12 | Native history/continuity plus bounded Context Runtime feed ordinary active-player R097; RD-14 product request exists, no Commentator transition prerequisite. |
| E13 | Confirmed R069/R070 save + R086 route precedes R098 session-local clear/menu; multiplayer non-interference only where applicable. |
| E14 | R078 + R086 join R100 creator consumer; no repository-permission/PLAYER substitution. |
| E15 | R088/R089 follow realized targets; package proof/static/hosted/empirical channels remain distinct. F1 cannot be closed by aggregate CI. |

HARD_PRECEDES, JOIN_BEFORE_INTEGRATION, INTEGRATION_COMPLETION_GATE, SHARED_FILE_CHECKPOINT, SCHEDULING_PREFERENCE, PROOF_AFTER_TARGET and CONSTRAINS_WITHOUT_ORDERING retain distinct meanings. Location RD-04→RD-02 and PC/NPC/item RD-02→RD-03 are explicit physical checkpoints. Shared STORAGE and bootstrap/launcher edits must fresh-read the prior accepted file and increment the actual material revision once per logical edit; static root work does not manufacture Story semantic ownership.

The former ROOT_SELECTOR_CUTOVER physical-Story condition and earlier unconditional BOUND wording are explicitly superseded by later current overlays. No new owner cycle or whole-wave barrier was found. F1 is missing work at an otherwise valid owner/consumer join.

## 9. Protected invariants

| Invariant | Adversarial result and evidence |
|---|---|
| No second gameplay/knowledge/history/currentness/chronology authority | Native information, Actor, execution, history and scoped currentness are separated in RD-02/03/05/08/09/13; end-to-end shipped convergence remains open under F1. |
| No global active player | Principal→PLAYER/control/operation chain in RD-09; collaboration three-family admission and recipient-scoped RD-11/12/14 joins. No current task introduces a global active-player field. |
| No generic SAVE frontier/journal/rollback | RD-06 frozen scope-native promise, generation-specific clearing and truthful partial outcomes; repaired SAVE/PERSISTENCE actions. |
| LIVE CAS separate from campaign publication | WP12-05 and WP16-8/9/15/21 retain native CAS establishment, local post-CAS adoption and forward campaign absorption; no distributed SQLite/Git/LIVE transaction. |
| Physical presence/path/index cannot create authority | New route/HOT/LIVE plans preserve the rule; current LIVE_SCENE instruction violates it and has no planned correction: F1. |
| Story noncanonical and gameplay-nonblocking | Final overlay static selector/first-materialization split, exact four-layer routes; native history/recovery wins, no Story/T0 bootstrap gate. |
| T0 sparse conditional historical basis | Fresh WP19-L29..39: qualifying material accepted decision/transition only, retained event-time value/provenance, no current T1 substitute, no raw reasoning, no extra serial call/read/publication or irrelevant-turn work. RD-13/control proof and RD-14 qualifying join preserve it. |
| Context Runtime ephemeral | RD-11 profile/request/trace/budget projection, required floors before optional ranking, no durable knowledge or context owner. |
| Dramaturg bounded retained multiplayer projection | Fresh WP-18 §6–8 matches two fixed families, native-typed basis, ABSENT/BOUND, acceptance-only generation, bounded reconcile and inactive/re-enable admission. No registry/plot graph/scheduler or durable singleplayer owner. |
| Technical sequence/Git/ref/ID order not fictional chronology | New execution/temporal/LIVE/Story/collaboration tests preserve non-equivalence. Current MULTIPLAYER global-frontier wording still needs the explicit F1 cutover. |
| No legacy v0.8 preservation constraint | Fresh clean-slate/version owners and overlays require current local schema identity without an obsolete prerelease adapter/migration project. |

Clean Architecture was used only to diagnose owner/dependency placement under AGENTS. The named runtime planners remain consumers of owner-native contracts and fixed publication adapters; no new port framework, DTO layer or subsystem is required to repair F1. A runtime import-graph/composition-root score is not asserted for code that does not yet exist.

## 10. Minimum authoritative escalation record

Additional owner/body evidence was opened only to answer a concrete duty, repaired claim or finding:

| Question capable of changing a conclusion | Minimum authoritative evidence used |
|---|---|
| Exact numeric proof semantics | WP-12 §14 and WP-13 §15 before current v2 appendix; WP-14 §15.13–25, WP-15 §13.9–17, WP-16 §15 and WP-17 §28 for the other individual rows. |
| Seven selectors and schema/compatibility consequence | WP-11 fixed route table, actual MANIFEST/schema, compact and detailed version owner, current clean-slate owner. |
| Current-conforming versus stale WP13 consumers | Targeted SAVE_CONTRACT, STORAGE, DURABILITY_GUARD and ENGINE_UPDATES body sections; LIVE_SCENE/MULTIPLAYER contradictions plus WP-16 §16 and claim law. |
| Exact Story addressing and retained-generation admission | WP-18 §3.1–3.4, §6.1/6.3/6.5, §7 and §8. No whole Story dependency corpus. |
| Bootstrap generator/no-Story law | WP19-L06..15 and L29..39; current init_campaign copy/digest code; exact BOOTSTRAP_RUNTIME/CAMPAIGN_SETUP/launcher projections and headers; SESSIONS directory metadata proving its template exists. |
| Unchanged RD owner chains | Remote changed-file comparison plus current exact readiness records/current plans; prior independent supporting evidence reused only where the brief permits it. |

No author third-pass declaration or prior Senior verdict was used to turn an unproved route into PASS. No additional document was opened merely for thematic completeness.

## 11. Publication, validation and next unit

This review publishes only:
- this independent result;
- `DEV/CURRENT_PROGRESS.md` aligned to **FAIL / REPAIR REQUIRED**, with the independent finding open.

**VERSION_IMPACT: NONE.** The actual change is a review decision and development cursor: no gameplay semantic/machine/runtime/schema/catalog/protocol owner, version carrier, module instruction, serialized contract, release identity or generated consumer changes. The future module/schema/launcher effects discussed above are review evidence, not edits or pre-bumps. System Impact: no new architecture decision; the accepted owners already determine the required author repair.

Required repair-checkpoint hosted validation was independently observed successful. The review's inventory/count/route/command checks are static planning checks; no proposed production test class was executed or represented as green. Publication uses one commit parented to the fresh reviewed HEAD, exactly these two UTF-8 blobs over its base tree and a non-force ref transition, followed by exact remote read-back and changed-path verification. Hosted validation on that new review commit is checked after publication and is not self-certified inside this document.

Next eligible work is an **author planning repair of SIRR2-001**, followed by a genuinely independent Senior re-review of the current effective package. R2.7 architectural final reconciliation remains CLOSED. Production implementation, migration, release and gameplay bootstrap remain unauthorized and unstarted. No new Product Owner semantic decision is required by the identified defect.

The only verdict of this review is **FAIL / REPAIR REQUIRED**.

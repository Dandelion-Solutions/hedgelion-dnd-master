# W05.T06-A1 — Source Manifest and Framing Evidence

Status: **STEP-1 SOURCE MANIFEST COMPLETE — DESIGN EVIDENCE, NOT ARCHITECTURE AUTHORITY**

Architecture block: `W05.T06-A1 — current-readiness and ordinary Master retrospective consumer architecture`

Target architecture checkpoint: `W05_T06_READINESS_RETROSPECTIVE_ARCHITECTURE_READY`

Current source basis: `5b7db90a36f9d5771c392f2e5119fbcd29893c03`

This manifest routes and extracts the evidence needed to frame the authorized design block. It does not select a machine architecture, authorize production changes, reopen product semantics, or advance past architecture Review Stop 1.

## 1. Authority and task state

| Source | Authority role | Why it is included / inspected scope | Current interpretation |
|---|---|---|---|
| `AGENTS.md`; `DEV/AGENT_RUNTIMES/OPENCODE.md`; `DEV/AGENT_RUNTIMES/LOCAL_MACHINE.md` | CANONICAL process/runtime policy | Current branch, artifact taxonomy, evidence rules, version gate, transport and verification surface | Work stays on the existing active ref. Design artifacts belong under `DEV/docs/superpowers/design/`. No hosted-CI claim is available from this runtime. |
| `DEV/DESIGN_PROCESS.md`; `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CANONICAL process owners | Step 1, source/evidence completeness, whole-project critic and mandatory review stops | Complete the Source Manifest, Task Brief, whole-project critic and framing repairs; stop before Step 2 unless Senior gives GO. |
| `DEV/PROJECT_MAP.md`; `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | DERIVATIVE locator/index | Reconstruct readiness, owner/current state, Story/history/context, authorization, indexing, durability, and test dependencies | These locate the owners below; they do not override them. The routing subgraph was followed into actual owner documents/code/tests. |
| `DEV/CURRENT_PROGRESS.md`; `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | CANONICAL progress; sequencing aid | Establish current work and neighboring sequence | W05.T06-A1 is the next authorized unit; safe T06-S1/S2 remain preserved. A1's target and production hold are current. |
| `DEV/docs/superpowers/design/2026-10-02-w05-t06-readiness-retrospective-system-impact-senior-ruling.md` | CANONICAL AMENDMENT / SENIOR decision | Exact System-Impact ruling, product law already settled, required architecture questions and stop sequence | Design review is authorized; product decision at entry is NO. The two implementation paths remain held. |
| `DEV/docs/superpowers/plans/implementation-wave-05-machine-bootstrap-integration.md`; `...-execution-status.md` | Accepted implementation plan / execution cursor | T06 Impact Envelope, safe slices, protected owners, system-impact evidence, required downstream tests | A1 is an architecture prerequisite, not production implementation. T06-S1/S2 are not reopened. T07/T08/W06 remain unstarted. |
| `DEV/docs/superpowers/README.md` | DERIVATIVE taxonomy locator | Confirm placement of Task Brief, Source Manifest and critic | All three are design-process/provenance artifacts and stay under `design/`. |

## 2. Product Owner intent and accepted product semantics

| Source/item | Authority role | Inspected scope and evidence | Disposition for A1 |
|---|---|---|---|
| `DEV/PRODUCT_OWNER_INPUT.md` active routing index | PRODUCT OWNER INTENT / ROUTING | PO-001, PO-002, PO-003, PO-009, PO-011 and PO-012 routes; current terminal state | PO-001/003 are direct requirements; PO-009 is a Commentator-only refinement; PO-012 is a Commentator-only eligibility law; PO-011 is a downstream visible-language constraint. PO-002 is preserved in safe T06-S1 and is not reopened. No applicable `NEEDS_PO` route is open. |
| `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md` | CANONICAL process addendum | Active-route lookup, intent/architecture distinction, whole-project critic obligations | Ledger text is evidence of intent; accepted owner specifications control runtime semantics. Deferred routes are not activated by topic overlap. |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md` | CANONICAL product decision | §§2, 2.1–2.2; ordinary active-player retrospective, no Commentator transition, current knowledge/disclosure/no-spoiler, no mutation/time advance, no duplicate history subsystem | PO-001 defines the product behavior. It does not create a Story dependency or generic memory owner. Save/exit §3 remains safe T06-S1, outside A1. |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md`; PO-003 ledger entry | CANONICAL product decision / intent evidence | §§1–7; event-time T0 basis, variable situation-specific material subset, T1/current-state non-substitution, no full psychology/per-turn snapshots/hidden reasoning, insufficiency handling, durability relationship | Ordinary Master may need accepted event-time basis for material historical motive claims; source basis is sparse, bounded and event-time. Do not infer an exact past motive from current Actor state. |
| PO-003 immutable latency amendment in `DEV/PRODUCT_OWNER_INPUT.md`; WP-19 L38/L39; WP-24-5 | PRODUCT OWNER INTENT + CANONICAL requirement | Zero additional sequential LLM calls solely for T0 capture; zero extra serial remote/tool reads solely for capture when required T0 data is already admitted; zero separate publication; zero irrelevant-turn capture work; bounded typed material items | This is a capture-path constraint. Do not silently generalize it into “no reads for a user-requested retrospective query”; analyze query-path cost separately and preserve responsiveness without inventing a numeric SLA. |
| `DEV/docs/superpowers/specs/2026-09-09-story-commentator-self-contained-corpus-owner-decision.md` (PO-009) | CANONICAL AMENDMENT / owner decision | §§2–10, 11; gameplay/Master versus Commentator corpus authority, Story-local T0 and derived control requirements for baseline Commentator, native fallback boundaries | Applies to Commentator only. It does not promote Story to Master/gameplay truth or make Story mandatory for ordinary Master retrospective. |
| `DEV/docs/superpowers/specs/2026-09-28-commentator-player-selected-pc-perspective-owner-decision.md` (PO-012) | CANONICAL AMENDMENT / owner decision | §§1–9; PUBLIC + exact current PLAYER disclosure + at most one selected currently controlled PC's exact `epistemic.known`, no multi-PC union, no full-history baseline | Explicit negative scope guard: preserve this separately for Commentator control/retrospective; do not copy its perspective formula into ordinary Master semantics. |
| `DEV/docs/superpowers/specs/2026-09-26-player-facing-response-language-owner-decision.md` (PO-011); PO-011 ledger route | CANONICAL AMENDMENT / owner decision | Transient `ResolvedResponseLanguage`, visible/internal separation, no fallback language due only to optional policy/asset absence, no persistent PLAYER language field | A1 defines recipient-safe context, not a new language owner. Any later visible Master answer consumes this existing owner; no new player-language state. |

## 3. Accepted readiness, Actor, current-state and rules owners

| Source | Authority role | Inspected scope and evidence | Framing consequence |
|---|---|---|---|
| `GAME/CORE/CHARACTER_READINESS.md` | CANONICAL runtime semantic owner | Progressive local sufficiency §§17–28; READY_PC §§30–67; authorized build sources §§69–110; no-situational-retrofit §§112–122; provisional/play boundary §§124–141; onboarding latency §§143–159; detection §§161–176; persistence/runtime precondition §§178–205 | READY_PC is a deterministic predicate over current Actor plus binding, required Assets/Effects/definitions/rules. It is not a first-play gate, 100%-filled sheet, phrase, or all-fields check. Each attempted mechanic has its own local dependency test. |
| `GAME/CORE/DIEGETIC_ONBOARDING.md` | CANONICAL runtime semantic owner | §§1–6, 7–10, 12–15; provisional gameplay, precedence, stable same-Actor identity, PROVISIONAL_IDENTITY, HOT/SOFT cadence, continuous READY_PC convergence, resume | Preserve exploratory/provisional play and same PC ID; do not turn A1 into a questionnaire or early hard phase gate. |
| `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md` | CANONICAL S6D-07 owner | Laws 1–12; reconstruction sequence; bounded Fighter/Sorcerer MVP paths; attestation fields; deferred production resolver/acceptance boundary | Existing accepted readiness architecture is not empty-slate. The current owner already defines owner-relative grants/choices, exact package context, typed readiness attestation and blocking dependencies; its production resolver is explicitly deferred. A1 must determine the runtime consumer/owner route without duplicating those laws. |
| `DEV/TOOLS/validate_character_mvp_seed.py`; `DEV/TESTS/test_s6d_07_character_mvp_seed.py`; `test_s6d_07_mvp_selector_activation.py` | IMPLEMENTATION / MACHINE-CONTRACT / TEST | `evaluate_ready_pc()` and compiler validation, exact package identity, blockers, Fighter/Sorcerer fixtures, required engine selectors/active primitives | The existing evaluator is DEV conformance tooling over one bounded package. It is not a GAME callable, not a deployable readiness service, and not permission to copy caller evidence/booleans into runtime. |
| `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/ruleset-package-manifest.json`; `character-mvp-seed.json`; `character-capabilities.json` | CANONICAL machine inputs | Manifest self-inclusion, exact package identity, supported Human/Criminal Fighter 1–2/Sorcerer 1 vertical slice, `full_srd_character_corpus=false`, unsupported content absent/nonselectable, readiness dependency classes | A1 must consume exact selected package/definition context and its admitted subset; no inferred full SRD or ambient defaults. The concrete ruleset may evolve only through its current package owner. |
| `DEV/ARCHITECTURE/ACTOR_MODEL.md` | CANONICAL model owner | §§1–1.1; §3 build state; §4 abilities; §§5–6 HP/LifeState/Resources; §7 private continuity; §9 MechanicalContext; §11–12 HOT/current and recovery | Actor remains one progressively materialized owner; sparse build anchors and derived mechanics are separated. A resolved sheet/profile is cache only. PC agency and current `world.knowledge` remain separate. |
| `DEV/ARCHITECTURE/ASSET_MODEL.md` | CANONICAL model owner | §§1–4, §§10–12; definitions versus instances, asset/resource/effect ownership, sparse state, HOT and derivation | Readiness must validate required current Assets by their natural identity and definition; Asset data is not a second flat sheet or access authority. |
| `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` | CANONICAL S6D-08 owner | Authority map, health/LifeState, resource, effect/condition/temporal boundaries, recovery and seed owner | HP/LifeState, Resources, Effects and mechanical events keep their existing owners; readiness cannot absorb their internals into a duplicate PC readiness record. |
| `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`; `ACTIVITY_MODEL.md`; `CATALOG_RESOLUTION.md` | CANONICAL model/definition owners | Engine-state versus invocation facts; exact state-view binding; registered accessors/activities; exact `ResolvedCatalogContext`, stable definition identity and fail-closed dependency resolution | The readiness predicate can use only deterministic, owner-validated, correctly bound rules/definition evidence. Prose/concept and caller assertions cannot become mechanics. |
| `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`; `RULESET_PACKAGE_MACHINE_CLOSURE.md` | CANONICAL package identity/closure owners | Exact package snapshot -> resolved lock -> typed ruleset-set identity; catalog context; natural owner projections; S6D-07 readiness evidence relationship | An assessment must bind its evidence to exact selected ruleset/package and catalog identities, not a mutable label or DEV-only tool result. |
| `GAME/SCHEMA/player.schema.yaml`; `DEV/SCHEMAS/world-player-state.schema.json`, `world-actor-state.schema.json`, `world-asset-state.schema.json`, `world-effect-state.schema.json`, `actor-archetype-data.schema.json`, `asset-definition-data.schema.json`, `effect-definition-data.schema.json`, `semantic-event-t0-basis.schema.json` | IMPLEMENTATION / MACHINE CONTRACT | Current persisted actor/player/assets/effects and event-time basis shapes | Schemas constrain carriers; none is treated as the readiness predicate or new owner. Read with their current owner and consumers. |
| `GAME/TOOLS/actor_continuity.py`; `GAME/TOOLS/information.py`; `GAME/TOOLS/catalog_runtime.py`; `GAME/TOOLS/ruleset_package.py` | IMPLEMENTATION / OWNER ADAPTERS | Actor continuity assessment scope; native information evidence validation; exact package/context binding and engine/catalog dependencies | Existing narrow callables are not assumed to implement cross-owner readiness. Inspect possible reusable owner APIs without promoting a helper into a new authority. |

## 4. Current HOT/SOFT source view, durability and resume

| Source | Authority role | Inspected scope and evidence | Framing consequence |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md` | CANONICAL | §§3, 5, 8, 17; HOT may be ahead of campaign publication; coherent read composes pinned campaign owners + accepted unpublished HOT delta + currently routed LIVE scope + required operational owners; composed view is not merged writable authority | A repository-only readiness check is incomplete whenever accepted HOT/SOFT is current; the design must compose a current owner view without a global frontier or duplicate mutation owner. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` | CANONICAL | Laws WP12-1..29, especially owner identity/source-basis separation; permitted local establishment; exact-source/LIVE distinction; currentness and cache invalidation; Context eligibility; cold recovery | HOT may be current ahead of Git only under existing owner establishment rules. Physical bytes/mtime/generation do not prove currentness or permission; LIVE prospective state stays non-current until exact CAS; local adoption after CAS cannot roll back authority. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | CANONICAL | Laws WP14-1..13 and WP14-21..24; exact current source selection, LIVE no-fallback, bounded root discovery/hydration, accepted execution resume, cache equivalence and derived rebuild | Cold resume starts from actual routed native authorities; surviving SQLite is reusable only after source-equivalence proof; index/cache absence is not semantic absence. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`; `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md` | CANONICAL | Registered `ContextNeedProfile`; bounded multi-channel discovery; owner currentness/eligibility; finite `UNSATISFIABLE`; SQLite/HOT physical authority distinction | Context is a consumer/projection, not a readiness or current-state owner. No ad hoc profile, world-graph walk, full load, broad scan or silently dropped required dependency. |
| `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`; `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md`; `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md` | CANONICAL S6D owners | Pinned state-view identity, ENGINE_STATE-only accessor/selector inputs, exact admitted selector/operation/primitive lists, transitive dependency/currentness and missing-input behavior | Readiness cannot reuse arbitrary calculation helpers or invent a selector/primitive. Any derivation stays inside exact admitted mechanical consumer contracts and typed failure boundaries. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md`; `GAME/CORE/DURABILITY_GUARD.md`; `GAME/CORE/CAMPAIGN_SETUP.md`; `GAME/CORE/RUNTIME.md` | CANONICAL | Current owner closure/durability edges; READY_PC/PLAY_READY publication boundary; combined READY_PC+PLAY_READY allowed; no save solely to inspect readiness; no active lifecycle before both | Readiness output does not force a separate commit or new lifecycle state. On a real transition, reuse the existing coherent durability/PLAY_READY closure; preserve sparse SOFT/HARD and fail-closed save semantics. |
| `GAME/TOOLS/hot_store.py`; `DEV/TESTS/test_rd04_native_routing_index_hot.py` | IMPLEMENTATION / TEST | `NativeHotStore` exact owner key, generations, atomic local batch and generation-specific dirty clearing | Repo-wide call-site search found no GAME runtime consumer beyond this module; current pytest references are its isolated tests. It is evidence for one support contract, not proof it is composed into production RuntimeHost. |
| `GAME/TOOLS/runtime_host.py`; `GAME/TOOLS/turn_runtime.py`; `GAME/TOOLS/runtime_execution.py`; `GAME/TOOLS/durability.py`; `GAME/TOOLS/recovery.py`; `GAME/TOOLS/live_state.py` | IMPLEMENTATION / OWNER CONSUMERS | RuntimeHost operation basis pins selected campaign + routed LIVE, fixed Context/History/order/publication services; TurnRuntime binds profile/bundle to one phase; recovery selects durable sources and ignores optional `hot_state` (`hot_authoritative=false`, `hot_rebuilt=true`); exact native mutation/publication boundaries | Actual callable composition and current mutation/read path must be traced. RuntimeHost currently has no HOT service. Cold resume recovers current compatible native sources and cannot recreate lost unpublished state. Re-evaluation must bind to newly validated current owners after resume/rejoin. |
| `DEV/TESTS/test_rd07_recovery.py`; `test_rd05_runtime_execution.py`; `test_rd06_durability_publication.py`; `test_runtime_host_composition.py` | IMPLEMENTATION / TEST | Current source selection/recovery, deterministic execution and publication promises, host boundaries | These are owner regressions and currentness references; they do not by themselves supply progressive readiness. |

## 5. Ordinary Master retrospective / History / Story / Context

| Source | Authority role | Inspected scope and evidence | Framing consequence |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md` | CANONICAL composition owner | L20–L23; L29–L45; L149–L205; L222–L251; L313–L384; L386–L405 | PO-001 is an ordinary Master consumer. It uses bounded candidate discovery, exact/native/SemanticEvent evidence for material claims and current disclosure/no-spoiler. Index/query failure never authorizes whole-history scan. PO-003 T0 selection is sparse/situation-specific and no extra serial capture pass is allowed. Physical index gap may use minimum derived discovery metadata under existing index ownership. |
| Step-4 canonical spec | CANONICAL | §1 six logical roles; §§2, 5, 6, 9–12; §§25–29; historical-vs-current boundaries | Six-role set remains fixed. Truth, current `world.knowledge`, human `runtime.disclosure`, LOG history, Context eligibility and Story remain distinct. Ordinary Master is not another role. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md` | CANONICAL | Laws R2.1-1..15; Story may orient, current claim resolves through current owners, no new memory authority, source-typed history/coverage and projection-absence semantics | Historical or Story orientation cannot become canonical/current truth; no generic memory/search store; exact claim needs its native evidence class. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`; `...WP-09-context-loading-resource-bounds-realization-canonical-spec.md` | CANONICAL | Need profiles, finite discovery channels and typed dependency closure; historical escalation §§15; `UNSATISFIABLE` terminal; no full preload/scan | The consumer needs an admitted, purpose-scoped profile/candidate provider/owner-resolution path. Existing `INDEX_LOOKUP` and `HISTORY_HINT` labels alone do not constitute that route. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` | CANONICAL | One user request/assistant turn/physical context; logical rebind per phase; six roles; no extra mandatory LLM calls; registered finite `UNSATISFIABLE` alternatives | The design may add/adjust only an existing-role profile/purpose when justified; model call, role, typed handoff and visible-output ownership remain current. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md`; `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md`; `GAME/CORE/SESSION.md`, `MULTIPLAYER.md`, `LIVE_SCENE.md` | CANONICAL adjacent consumer owners | Join/rejoin before mutable input, current binding/control/source refresh, no global active player, no absence-as-consent, recipient-scoped context | Readiness after resume/rejoin re-evaluates current compatible owner evidence after W03/W04 routing; join/rejoin safe T06-S2 is preserved, not redesigned. |
| `GAME/TOOLS/collaboration.py::join_participant/rejoin_participant`; `DEV/TESTS/test_rd12_collaboration.py::CollaborationJoinCatchUpTests` | IMPLEMENTATION / TEST | Current operation basis, current PLAYER/route revalidation, bounded recipient catch-up before mutable input | A1 assessment re-evaluation consumes current identity/route evidence; it does not alter collaboration admission, create a readiness cache, or reopen safe T06-S2. |
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md`; WP-15 chronology owner; `GAME/TOOLS/native_storage.py`; `GAME/SCHEMA/index.schema.yaml` | CANONICAL + IMPLEMENTATION | Direct known-ID routes; compact family indexes nominate only and cannot prove absence/authority; monolithic index baseline; exact routes and no Git/Event-ID chronology | Candidate discovery must use existing index ownership and revalidate exact native sources. IDs, storage/index order and ordinals do not imply chronology. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md` | CANONICAL | Sparse owner-anchored chronology, chronology/index non-authority, bounded current/temporal routes; WP15-34/35 and final disposition explicitly reject an arbitrary historical-query/indefinite-retention promise | Typed causal/order/metric evidence is used only when relevant. A1 does not add a global event timeline or guarantee every unanticipated historical query. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md` | CANONICAL | Semantic continuity vs selective exact, exact text protection/discharge and lawful compaction | Do not promise exact wording after lawful compaction unless exact evidence remains protected/retained. Missing exact evidence is described truthfully; semantic support still follows its native owner. |
| `GAME/CAMPAIGN/INDEX/EVENT_INDEX.yaml`; `GAME/TOOLS/init_campaign.py`; `GAME/TOOLS/runtime_host.py`; `GAME/TOOLS/history.py`; `DEV/SCHEMAS/runtime-semantic-event-state.schema.json`; `GAME/SCHEMA/event.schema.yaml` | IMPLEMENTATION / MACHINE CONTRACT | Event enrollment ordinals/paths; exact bounded History windows; current campaign pin and selected LIVE origin; native event record; existing T0 basis carrier | History is bounded by origin/ordinal window, not semantic query. Ordinary read must not substitute physical event order for chronology. **Framing discrepancy to investigate:** blank EVENT_INDEX template has only schema/entity/entries, generator copies it; current `RuntimeHost._index_entries` requires `complete:true` and `upper_ordinal`. Do not assume template absence proves an empty complete history or silently repair a later owner. |
| `GAME/TOOLS/context_runtime.py`; `GAME/TOOLS/information.py`; `GAME/TOOLS/access_control.py` | IMPLEMENTATION / current consumers | Registered six-profile table; caller candidates as untrusted nominations; exact native reload; current active PLAYER and subject/recipient checks; current knowledge/disclosure route; retrospective requests presently terminal UNSATISFIABLE | Existing Context can enforce accepted owner resolution once a registered route is supplied; it does not produce semantic retrospective candidates and currently rejects retrospective projection absent an admitted path. Commentator's selected-PC behavior is profile-specific. |
| `GAME/TOOLS/story.py`; `GAME/TOOLS/commentator.py`; PO-009; Story producer contract; Story baseline source contracts; Story growth/sharding owner decision | IMPLEMENTATION / CANONICAL owner decisions | Story is durable, noncanonical, optional/lagging for gameplay. Projection state stores per-Story-ID `entity_refs/source_refs/story_refs` and domain coverage. Story direct exact reader is private writer-internal; no public Master-safe Story reader/adapter. No read may trigger catch-up/publication. PO-009 T0 self-containment and PO-012 projection are Commentator-scoped. | Story is not presumed required or available to Master. Study native/index sufficiency first; design an optional read-only hint only if bounded discovery quality/responsiveness materially improves, with exact native proof and failure/defer to native-only retrieval. Do not couple a consumer to shard/layout. |
| `DEV/TESTS/test_rd11_context_runtime.py` | IMPLEMENTATION / TEST | `RetrospectiveContextTests` (three tests), `CommentatorControlProfileTests`, `ContextDiscoveryTests`, `ContextEligibilityTests`, `RequiredPacketClosureTests` | Existing terminal retrospective tests are explicit incomplete-route guards and must be reconciled as evidence, not weakened as a shortcut. |
| `DEV/TESTS/test_rd13_story_t0_commentator.py` | IMPLEMENTATION / TEST | `NativeHistoryWindowTests`; `T0BasisTests`; `StoryT0MaterializationTests`; `CommentatorSelfContainedTests`; `CommentatorControlEvidenceTests`; `HistoryProjectionSeparationTests`; schema/physical route tests | Supports native History, T0, Commentator PO-009/PO-012, and Story projections. This is not direct proof of an ordinary Master consumer. |
| `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief-critic.md` | HISTORICAL design provenance | PO-001/PO-003 whole-project dependency reconstruction and previous accepted owner-versus-realization dispositions | Confirms why PO-001/003 remain accepted and deferred at consumer edge; historical findings remain closed unless new current evidence contradicts them. Does not replace current owners or the present critic. |

## 6. T06 implementation and verification consumers

| Source | Authority role | Inspected scope | A1 handling |
|---|---|---|---|
| `GAME/TOOLS/bootstrap.py`; current T06 cursor in the W05 execution-status file | IMPLEMENTATION / execution evidence | Current save/exit composition, measured write gate, selection->RuntimeHost composition, creator evidence and join/rejoin delegation; S1/S2 status | Preserve published safe S1/S2. No readiness or ordinary Master retrospective callable currently exists in `GAME/TOOLS`. |
| `DEV/TESTS/test_rd14_bootstrap.py` | IMPLEMENTATION / TEST | Current class list includes selection barrier, creation identity, generator/scaffold, creator authority, multiplayer join/rejoin, save/exit and shipped bootstrap projection | `ProgressiveOnboardingTests` and `OrdinaryRetrospectiveRoutingTests` required by the accepted W05 plan are absent. They remain held until A1 has final Senior GO and the implementation plan/envelope is reconciled. |
| `DEV/TESTS/test_rd04_native_routing_index_hot.py` | IMPLEMENTATION / TEST | Native direct route, candidate owner reload, index non-authority, `NativeHotStoreTests`, atomic HOT mutation and exact generation clear | Generic HOT/index behavior is tested. Runtime integration/current-view composition is not proved by this test. |
| `DEV/TESTS/test_s6d_03_selector_metadata_contract.py`; `test_s6d_04_mechanical_context_contract.py`; `test_activity_primitive_contracts_split.py`; `test_rd05_runtime_execution.py`; `test_rd07_recovery.py`; `test_s6d_11_ruleset_package_closure.py` | IMPLEMENTATION / TEST | Exact selector/MechanicalContext admission, primitive allowlists, pinned state-view, deterministic execution/recovery and package identity closure | Existing tests constrain reuse of mechanical derivation and current-source context; no new selector, primitive, owner or recovery path is admitted by this Task Brief. |
| `DEV/TESTS/test_r2_7_wp04_actor_asset_conformance.py`; `test_rd03_actor_asset_effect_continuity.py`; `test_rd15_catalog_runtime.py`; `test_s6d_07_character_mvp_seed.py`; `test_s6d_07_mvp_selector_activation.py`; `test_s6d_11_ruleset_package_closure.py` | IMPLEMENTATION / TEST | Actor/Asset/Effect shapes, sparse provisional Actor, package identity/definition admission, bounded S6D-07 seed readiness and active selector/primitive closure | Owner-level source evidence and package-conformance references; not a production RuntimeHost readiness assessment. |
| `DEV/TESTS/test_runtime_host_composition.py`; `test_rd07_recovery.py`; `test_rd09_access_live.py`; `test_rd12_collaboration.py` | IMPLEMENTATION / TEST | Fixed service composition, bounded native event reads, no caller service replacement, exact current PLAYER/control, collaboration rejoin, cold recovery | Neighboring consumers that constrain the eventual assessment and retrospective route. Preserve existing assertions; A1 does not change S1/S2. |
| `DEV/RELEASE/VERSIONING.md`; `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` | CANONICAL version owner | Module revision, persistent schema, catalog/ruleset identity and migration classes | Step-1 documents/cursor change no semantic/machine owner. Expected `VERSION_IMPACT: NONE`, assessed again for actual changed paths before checkpoint. |

## 7. Evidence extraction and item-level accounting

### 7.1 Readiness requirements from current owners

| Item | Actual owner claim | A1 applicability/disposition |
|---|---|---|
| R-A01 | Current local sufficiency checks the proposed action's actual dependency set; it does not establish READY_PC. | Required machine concept to investigate; no bootstrap boolean or “play prohibited” gate. |
| R-A02 | Missing mechanically material choices cannot be selected after seeing the situation; a schema-valid Actor is insufficient. | Preserve fail-closed behavior and exact unresolved blockers. |
| R-A03 | READY_PC is over same current Actor + current PLAYER binding + referenced Assets/Effects + definitions/rules. | Determine owner-composed evidence input and validation path. |
| R-A04 | Normal frontier includes stable actor/player identity; accepted build/rules anchor; applicable species/origin/background; abilities; proficiency/capabilities; HP/LifeState; defense/movement; material equipment; resources/actions; spell state; persistent effects; material initial choices. | These are the explicit `CHARACTER_READINESS.md` dependency families; Step 2 must map their actual owners/derivations and applicability, not replace with a checklist/count. |
| R-A05 | Safe post-READY omissions are: uniquely derived; nonmechanical; genuine future evolution; or precommitted policy. | Preserve all four classes and the condition that later/current outcomes cannot depend on still-open choices. |
| R-A06 | Accepted initial choice precedence is player choice, deterministic inheritance, strong rules-valid concept inference, accepted default, delegated conservative default, then one targeted question if material alternatives remain. | Preserve six-step precedence; do not turn into questionnaire or infer unsupported content. |
| R-A07 | Provisional gameplay may proceed only for locally sufficient outcomes; same Actor is promoted; readiness is continuously reevaluable. | The assessment must expose local sufficiency separately from readiness and remain reusable after state refresh. |
| R-A08 | No extra SAVE solely to observe readiness; after a real READY_PC frontier, coherent persistence includes required owner closure; READY_PC may share PLAY_READY. | Reuse existing durability; do not invent a commit or readiness record. |
| R-A09 | `active` requires READY_PC and durable PLAY_READY; `initializing` can contain real provisional gameplay. | Preserve existing lifecycle; no new phase/enum. |
| R-A10 | The built-in package supports a bounded Human/Criminal Fighter 1–2 / Sorcerer 1 profile; unsupported content is absent/nonselectable. | Exact selected package is input; this scope does not expand supported content or seed. |
| R-A11 | S6D-07’s `evaluate_ready_pc()` in DEV tooling validates package/fixture evidence and exact blockers; accepted owner says it does not replace future runtime resolver/executor/publisher/repository. Its evidence binds `actor_id`, `actor_state_revision`, `catalog_generation`, `ruleset_set_digest_generation` and `ruleset_set_sha256`. | Useful conformance reference only; not a GAME runtime service or caller-minted readiness claim. Preserve exact generation-qualified identities; do not revive superseded package-content identity terminology. |
| R-A12 | WP-14 recovery rebuilds from current compatible durable native sources; WP-12 allows SQLite reuse only after source-equivalence proof; lost unpublished canon is not reconstructed by plausibility. | Resume/rejoin re-evaluates from newly current owner view; record loss of HOT as a settled recovery outcome. The open issue is acquiring the valid current HOT/SOFT basis while it survives, not deciding what to do after its loss. |

### 7.2 Retrospective/history constraints

| Item | Actual owner claim | A1 applicability/disposition |
|---|---|---|
| R-B01 | Retrospective is an ordinary active-player Master interaction; no Commentator transition and no fictional time advance. | Core product requirement. |
| R-B02 | No new generic history/memory authority; Story does not grant truth/currentness/access. | Hard non-goal. |
| R-B03 | Bounded R2.3 registered role/purpose profile binds recipient/player/PC and eligibility. | Determine narrowest existing logical role/profile/purpose; do not create a seventh `MASTER` role. |
| R-B04 | Retrieval may use entity/thread/Story orientation when useful, then a bounded historical candidate set and exact/native/SemanticEvent evidence for material claims. | Use nominations only; exact source is proof. |
| R-B05 | Native current owners, disclosure and no-spoiler rules decide what enters visible answer context. | Eligibility before semantic assembly; no repository readability, caller IDs, session cache or Story visibility as authority. |
| R-B06 | Index/Story omission does not prove semantic absence unless an explicit complete owner contract proves the requested scope. | Unknown/incomplete stays typed unresolved; no whole-history fallback. |
| R-B07 | Event-time T0 factors are variable/situation-specific, bounded and distinct from current T1. | Historical motive claims use admitted T0 or qualify insufficiency; no T1 substitution or COT. T0 source facts do not guarantee every arbitrary historical query or exact quote after owner-lawful compaction. |
| R-B08 | Story is optional/lagging for gameplay; Story reads do not catch up, mutate, or block canon. | No Master Story dependency unless material navigation gain is proven. |
| R-B09 | PO-009’s Story-local T0/control projection and PO-012’s exact single-PC/public/disclosure formula are Commentator-scoped. | Preserve separate Commentator contract; no transfer to Master. |
| R-B10 | R2.4 is one physical context/turn; logical roles rebind and role output is typed. | No additional mandatory model call or raw bundle crossing. A retrospective question can use the current turn envelope through a registered profile. |
| R-B11 | WP-24 has no universal latency/tool-call/index-size SLA. It separates structural boundedness from Class B realized benchmark and Class C supported-target experience; retrospective navigation quality under large Story is a Class-C item. | Do not invent numeric thresholds or claim empirical responsiveness from code/static tests. |
| R-B12 | WP19-L38/L39 zero-extra-serial work applies to T0 capture, not automatically to a requested read of historical material. WP-15's final disposition rejects an arbitrary historical-query promise; R2.1 and Step-5.11 distinguish semantic continuity from selective exact retention. | Preserve exact scope of the latency law; research query-path cost separately. Do not guarantee unretained exact material or all unanticipated historical queries; where retained/admitted evidence supports PO-001's examples, use it truthfully. |

### 7.3 Enumerated readiness/onboarding scenario inventory

Every enumerated case is accounted for; accounting does not make it an implementation action in Step 1.

| Cases | Item-level semantics retained | A1 disposition |
|---|---|---|
| C01 | Concept/name/class/species alone does not establish READY_PC. | Preserved. |
| C02 | `mechanics_detail: 0` affects presentation, not mechanical readiness. | Preserved. |
| C03 | Delegated bookkeeping uses accepted defaults; ask only material unresolved choices. | Preserved; no questionnaire design. |
| C04 | Missing exact mechanic may cause one bounded official/SRD setup lookup, not per-turn research. | Existing rule/package owner; outside retrospective retrieval design. |
| C05 | Fighter current-level build requires stated/derivable mechanical dependencies before activation. | Readiness semantic test vector. |
| C06 | Empty schema-shaped maps do not pass readiness. | Readiness negative test vector. |
| C07 | Spellcaster spell, resource and derived spell inputs are included where required. | Readiness semantic test vector. |
| C08 | Provisional play continues for locally sufficient outcomes; unresolved mechanics remain blocked. | Core readiness/local-sufficiency scenario. |
| C09 | READY_PC and launch may publish in one coherent PLAY_READY transaction. | Durability boundary preserved. |
| C10 | Stable READY_PC cannot cross a player-turn boundary only in RAM. | Existing durability law; not a new A1 write. |
| C11 | Semantic acceptance needs no magic phrase. | Preserved. |
| C12 | Current-sheet query reports actual stored/derived state; no fabricated “not created” for active PC. | Downstream consumer; current readiness assessment must remain truthful. |
| C13 | No uncertain combat resolution without READY_PC and correct dependencies. | Preserved. |
| C14 | Existing incomplete-campaign repair preserves identity and asks only material choices. | Current canonical repair owners; no backward compatibility extension. |
| C15 | No retrospective stat fabrication to justify unsupported earlier combat. | Critical readiness/history boundary. |
| C16 | No repeated source lookup/Git read solely because hidden mechanics detail. | Latency guard. |
| C17 | Progressive onboarding cannot bypass dependency proof; target readiness within first meaningful interactions without questionnaire. | Product latency guidance, not fixed SLA. |
| DO01 | Story-first harmless dialogue may precede READY_PC without mechanics result. | Preserved. |
| DO02 | Tentative identity alternatives do not create a write. | Preserved. |
| DO03 | Adopted stable name/identity is durable before later fiction relies on it. | Existing PROVISIONAL_IDENTITY boundary. |
| DO04 | First provisional transaction includes all already-established setup/play truth, not just name. | Existing closure; no new record. |
| DO05 | Provisional checkpoint remains `initializing`, not READY_PC. | Preserved. |
| DO06 | Same Actor ID is promoted in place. | Protected identity. |
| DO07 | No per-answer autosave. | Existing sparse durability law. |
| DO08 | Player correction supersedes compatible DM-seeded surface detail; silence is not authorship. | Preserved agency. |
| DO09 | Cosmetic gear cannot grant mechanics; actual Asset/rules dependencies apply. | Preserved. |
| DO10 | Mechanics-detail preference cannot reduce readiness. | Preserved. |
| DO11 | Resume after identity checkpoint returns to `initializing` setup. | Resume re-evaluation scenario. |
| DO12 | Explicit save during onboarding does not activate. | Existing SAVE/lifecycle owner. |
| DO13 | Stop during onboarding does not imply `paused`. | Existing lifecycle owner. |
| DO14 | Auto title is allowed only under its accepted owner and same durable transaction conditions. | Outside A1 behavior; no change. |

### 7.4 Enumerated durability boundary inventory

All `D01`–`D27` are dispositioned below so A1 does not accidentally alter neighboring durability law.

| Case | A1 disposition |
|---|---|
| D01 scaffold is not PLAY_READY | Preserve lifecycle frontier. |
| D02 PROVISIONAL_IDENTITY may be durable while `initializing` | Preserve. |
| D03 READY_PC plus launch may share coherent transaction | A7 existing batch, no separate readiness commit. |
| D04 settled READY_PC cannot cross another player turn only in RAM | Preserve owner-required durability. |
| D05 semantic acceptance has no magic phrase | Preserve. |
| D06 genuinely unresolved mechanic stays provisional | Preserve. |
| D07 mechanically capable scene requires READY_PC + PLAY_READY | Preserve. |
| D08 solo quest contract remains SOFT | No cadence redesign. |
| D09 recurring companion/relationship may remain SOFT | No cadence redesign. |
| D10 no per-turn autosave | Preserve. |
| D11 dirty-domain count is not a boundary | Preserve. |
| D12 focal-location change flushes allowed closure | Preserve. |
| D13 tactical movement does not create focal-location boundary | Preserve. |
| D14 scene/encounter completion alone is not a solo boundary | Preserve. |
| D15 valid lifecycle boundary flushes | Preserve. |
| D16 explicit save is not activation | Preserve. |
| D17 unfinished stop is not pause | Preserve. |
| D18 `active` requires READY_PC + PLAY_READY | Preserve. |
| D19 boundary/exposure check is zero-I/O | Preserve where that owner applies. |
| D20 verified context-loss risk may require safety flush | Preserve; no new A1 trigger. |
| D21 ELEVATED prioritizes safe preservation but does not block play | Preserve. |
| D22 DANGER may request one bounded attempt before same-scope growth | Preserve. |
| D23 DANGER is not HARD/corruption/timer/retry loop | Preserve. |
| D24 advisory host pressure alone cannot create gameplay DANGER | Preserve. |
| D25 clean state creates no heartbeat | Preserve. |
| D26 multiplayer may publish earlier under its owner | Preserve. |
| D27 successful persistence is invisible | Preserve. |

### 7.5 Existing runtime/test evidence and exact gaps

| Surface | Observed evidence | Scope-safe conclusion |
|---|---|---|
| `GAME/TOOLS/context_runtime.py` registered profiles | `profile.intent`, `profile.dramaturgy`, `profile.actor`, `profile.story`, `profile.narration`, `profile.commentator_control`; no Master-role profile | Existing six logical roles remain. A1 must decide whether an existing profile suffices or a narrow registered purpose/profile is needed. |
| `GAME/TOOLS/context_runtime.py` retrospective path; `DEV/TESTS/test_rd11_context_runtime.py::RetrospectiveContextTests` | `retrospective=True` is terminal `UNSATISFIABLE`; test proves no History route is called, no source read occurs and behavior remains unavailable until native route is admitted | This is a deliberate current regression boundary, not permission to bypass Context or weaken terminal failure. |
| `GAME/TOOLS/runtime_host.py::HistoryService`; `GAME/TOOLS/history.py`; `test_rd13_story_t0_commentator.py::NativeHistoryWindowTests` | Owner-issued exact History over bounded ordinal/origin `evt` pages; local path reads EVENT_INDEX then exact SemanticEvents; LIVE requires selected exact source, no local fallback | Existing native History is a proof source but not semantic retrieval by NPC/place/thread/topic. |
| `GAME/CAMPAIGN/INDEX/EVENT_INDEX.yaml`; `GAME/TOOLS/init_campaign.py`; `test_runtime_host_composition.py::test_local_semantic_events_*` | Blank template contains schema/entity/empty entries and generator copies template; current adapter requires explicit `complete:true` plus `upper_ordinal`; fixtures exercise positive exact completed index and rejection when completion proof is absent/false/mismatched | Record for Step-2 exact empty-history/index reconciliation. Do not claim missing/incomplete index proves there are no events; do not edit T05/T08 files in Step 1. |
| `GAME/TOOLS/native_storage.py`; `GAME/SCHEMA/index.schema.yaml`; `test_rd04_native_routing_index_hot.py::NativeIndexTests` | Existing family index is compact routing metadata; direct known ID bypasses index; candidate body is identity-revalidated; no Story body/privacy/current authority in entries | Any new history discovery stays bounded and nominated under existing index ownership; exact candidates are revalidated. |
| `GAME/TOOLS/story.py`; `DEV/TESTS/test_rd13_story_t0_commentator.py::StoryT0MaterializationTests` | Story state has coverage and per-Story-ID entity/source/story refs; direct read helper `_exact_story_read` is private and used inside Story writer. `GAME/TOOLS` has no public Master-safe Story navigation function; Commentator consumes separately supplied snapshot/control. | Optional hint route only if materially beneficial; no private repository access or assumed Story availability. |
| `GAME/TOOLS/runtime_host.py::RuntimeHost` / `_begin_operation`; `recovery.py::recover_current_runtime`; `turn_runtime.py::bind_phase_from_context` | Host pins campaign and exact selected LIVE per operation, composes fixed sibling services; no HOT service; cold recovery ignores `hot_state` and returns `hot_authoritative=false`, `hot_rebuilt=true`; phase binding accepts caller-supplied candidates but seals Context result | A1 must design a trustworthy accepted current-view integration rather than bootstrapping from Git alone, caller data or a false claim of existing HOT composition. |
| `GAME/TOOLS/hot_store.py`; repo-wide `NativeHotStore` call-site search; `test_rd04_native_routing_index_hot.py::NativeHotStoreTests` / `NativeAtomicityTests` | Store supports exact owner-key load/stage and atomic local batch; repo-wide GAME search has no runtime call site beyond its definition; tests exercise it directly | Existing local contract is evidence, not an integrated readiness/current-view service. |
| `DEV/TOOLS/validate_character_mvp_seed.py::evaluate_ready_pc`; `test_s6d_07_character_mvp_seed.py` | A deterministic DEV conformance evaluator returns readiness/blockers for the closed MVP fixture and checks actor revision, exact package/catalog identity, asset/proficiency/activity/selector evidence | Explicitly not a GAME runtime service or accepted owner result. The Step-2 architecture must reconcile this conformance contract with the future runtime resolver boundary. |
| `DEV/TESTS/test_rd14_bootstrap.py` current class inventory | Existing `CampaignSelectionBarrierTests`, `CreationIdentityTests`, `CreatorAuthorityTests`, `MultiplayerJoinRejoinTests`, `SaveExitMenuTests`, `ShippedBootstrapProjectionTests`, plus T05 generator/scaffold classes | Required `ProgressiveOnboardingTests` and `OrdinaryRetrospectiveRoutingTests` do not exist yet. No production implementation starts in A1. |

## 8. Versioning and publication evidence

`DEV/RELEASE/VERSIONING.md` and its detailed canonical owner were inspected. The expected Step-1 delta is limited to design-provenance Markdown and a task-local execution cursor; it does not change a semantic/machine/runtime/schema/catalog/protocol/module owner or consume/change any version namespace.

```text
VERSION_IMPACT: NONE
```

This is a prospective classification to recheck against the actual final changed-path set before publication. No version bump follows from the research/frame documents themselves.

## 9. Synthesis-completeness check for Step 1

- [x] Current remote/source basis and repository process loaded on exact current source state.
- [x] Project Map used to reconstruct both the character-readiness and history/context/index dependency subgraphs.
- [x] Actual canonical owners, accepted/superseding decisions and Product Owner routes inspected.
- [x] RuntimeHost, Context, History, Story, current mutation/read, package and recovery consumers inspected.
- [x] Relevant schemas, generator templates and existing consumer tests inspected.
- [x] Enumerated readiness, diegetic onboarding and durability cases accounted for item by item.
- [x] PO-009/PO-012 Commentator-specific semantics kept separate from ordinary Master behavior.
- [x] No numerical latency/size/SLA claim inferred from WP-24; future evidence class distinguished from structural boundedness.
- [x] A blank EVENT_INDEX versus strict native History completion-proof discrepancy recorded as an open repository-evidence question, not hidden or silently resolved.
- [x] Residual design choices are architecture research questions, not PRODUCT_OWNER_DECISION_REQUIRED at entry.

The whole-project Task-Brief critic independently rebuilt this subgraph; its findings and dispositions are in `DEV/docs/superpowers/design/2026-10-02-w05-t06-a1-task-brief-critic.md`. This manifest remains a routing/evidence aid, not architecture authority or a substitute for the actual owners.

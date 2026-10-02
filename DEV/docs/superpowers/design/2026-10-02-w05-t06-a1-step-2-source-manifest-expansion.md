# W05.T06-A1 — Step 2 Source Manifest Expansion

Status: STEP 2 EVIDENCE SET CLOSED
Repository: Dandelion-Solutions/hedgelion-dnd-master
Branch: v1/engine-rearchitecture
Evidence basis: f75809027016522af2340dde077b9412fd394b9a

This expansion refines the Step-1 Source Manifest after the mandatory Review Stop 1 GO. GitHub Connector reads are the authority for this architecture pass. No local repository state or CLS repository evidence is used as correctness authority.

## 1. Bounded dependency subgraph

Product onboarding/readiness:

    W05.T06 product onboarding
      -> READY_PC / local mechanical sufficiency
      -> current Actor + PLAYER + Asset + Effect owners
      -> admitted BoundCatalogContext / ruleset package closure
      -> accepted current owner composition
           -> pinned campaign source
           -> accepted unpublished HOT/SOFT
           -> selected LIVE source where LIVE owns the scope
      -> existing durability/publication owner for PLAY_READY

Ordinary Master retrospective:

    player natural language
      -> existing Interpreter
      -> bounded current orientation / exact nominations
      -> native History discovery
           -> EVENT_INDEX derived discovery metadata
           -> accepted unpublished HOT history helper
           -> selected LIVE history metadata where applicable
      -> exact NativeSemanticEvent / retained T0 basis / native owner evidence
      -> current PLAYER + knowledge + disclosure + source eligibility
      -> R2.3 Context Runtime, profile.narration, retrospective mode
      -> existing Narrator / ordinary Master visible output

Optional only:

    Story lookup / Story unit
      -> orientation nominations only
      -> native History / current owners still prove claims and eligibility

Runtime composition:

    compose_runtime_host
      -> operation basis
      -> current-owner read boundary
      -> ContextService
      -> HistoryService
      -> ReadinessService
      -> RetrospectiveService

## 2. Owning evidence and disposition

### Currentness / HOT / LIVE

Owners inspected:

- 2026-08-20-step-5-1-frontier-model-canonical-spec.md
- 2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md
- 2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md
- current GAME/TOOLS/hot_store.py
- current GAME/TOOLS/recovery.py
- current GAME/TOOLS/live_state.py
- current GAME/TOOLS/runtime_host.py

Established qualifier:

- accepted unpublished HOT/SOFT may be current before Git publication;
- pre-CAS LIVE prospective state is not current;
- selected LIVE source owns its admitted current scope;
- surviving local bytes after cold recovery are not authority without source-equivalence proof;
- no campaign-global scalar frontier is introduced.

Implementation evidence shows RuntimeHost currently pins campaign and LIVE but does not compose NativeHotStore into ordinary current owner reads.

### Readiness

Owners inspected:

- GAME/CORE/CHARACTER_READINESS.md
- DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md
- DEV/TOOLS/validate_character_mvp_seed.py as DEV conformance evidence only
- GAME/TOOLS/catalog_runtime.py
- GAME/TOOLS/ruleset_package.py
- current GAME/TOOLS runtime inventory

Established qualifier:

- READY_PC is a deterministic derived predicate, not a durable readiness owner;
- local mechanical sufficiency and READY_PC are distinct;
- PLAY_READY remains a durability/product state distinction;
- the production runtime may not import DEV validation tooling.

Negative evidence:

- no admitted GAME/TOOLS production READY_PC/readiness callable exists at the evidence basis;
- production BoundCatalogContext already carries exact ruleset lock, catalog generation and engine-contract evidence needed by a runtime evaluator.

### History / SemanticEvent / bounded discovery

Owners inspected:

- Step-4 truth/knowledge/role/context/Story canonical specification;
- R2.3 Context Runtime canonical specification;
- WP-19 canonical specification, especially L20-L23 and L29-L39;
- WP-11 physical routing/index canonical specification;
- GAME/TOOLS/history.py;
- DEV/SCHEMAS/runtime-semantic-event-state.schema.json;
- GAME/CAMPAIGN/INDEX/EVENT_INDEX.yaml;
- GAME/SCHEMA/index.schema.yaml and relevant native schemas.

Established qualifier:

- runtime.semantic_event is compact durable history and may preserve transition summary, causal/source refs, participant attribution, knowledge/disclosure changes, chronology and mechanical refs;
- current physical runtime semantic event is stricter and smaller: event_id, semantic_order, kind, provenance_refs, semantic_delta;
- exact History windows are bounded and owner-issued but discovery is ordinal/origin based, not semantic;
- WP19-L36 explicitly activates a minimum derived discovery projection when qualifying-event lookup otherwise requires broad history reads;
- WP11 permits derived discovery indexes but they remain non-authoritative, revalidated, and monolithic until measured WP-24 evidence triggers partitioning.

Negative evidence:

- entity/location/thread questions cannot generally be answered by EVENT_INDEX ordinal/path metadata alone;
- current last_event_id hints are not a complete historical lookup route;
- a whole-event-body scan would violate WP19/R2.3 baseline law.

### Knowledge / disclosure / access

Owners inspected:

- Step-4 canonical specification;
- GAME/TOOLS/access_control.py;
- GAME/TOOLS/information.py;
- world-knowledge, runtime-disclosure and world-lore-fact machine schemas;
- current GAME/TOOLS/context_runtime.py.

Established qualifier:

- repository readability is not gameplay eligibility;
- current world.knowledge and runtime.disclosure remain distinct current owners;
- historical visibility/exposure evidence does not itself redefine current eligibility;
- Narrator may receive only independently eligible material.

Implementation evidence:

- Context Runtime currently resolves campaign-owned PLAYER, knowledge, disclosure and world families directly from pinned repository state;
- it therefore does not observe accepted unpublished HOT current owner state;
- retrospective=True currently ends in UNSATISFIABLE rather than an admitted native historical route.

### Story

Owners inspected:

- Step-4 canonical Story model;
- R2.1 continuity/history canonical spec;
- current GAME/TOOLS/story.py;
- Story producer/source/retrospective contracts;
- PO-009/PO-012 only to prove their Commentator-specific boundary, not to import them into Master.

Established qualifier:

- Story is durable noncanonical projection, can lag or be absent, and cannot establish current truth or gameplay eligibility;
- current Story projection state has entity_refs/source_refs/story_refs lookup metadata;
- current exact persisted Story read helper is private to Story implementation.

Disposition:

- public Master Story access is not required for baseline correctness once native bounded discovery is admitted;
- Story remains a dormant optional orientation optimization with an explicit revisit trigger.

## 3. Current accepted public machine capabilities

Already present:

1. RuntimeHost operation basis with pinned campaign and selected LIVE.
2. ContextService with registered profile.narration and an existing retrospective request flag.
3. owner-issued NativeHistoryCurrentness / NativeSemanticEvent and bounded native history windows.
4. NativeHotStore current-owner storage primitives.
5. exact native routing and index contracts.
6. BoundCatalogContext and resolved ruleset/package evidence.
7. current PLAYER, knowledge, disclosure and access-control validators.
8. Story projection lookup metadata, but not a public Master read service.

## 4. Machine capabilities actually absent

1. One RuntimeHost-owned operation-scoped current-owner read boundary composing accepted campaign/HOT/LIVE currentness.
2. Production deterministic READY_PC/local-sufficiency evaluator and RuntimeHost service.
3. Native semantic-history discovery over exact typed anchors without whole-history body scanning.
4. Current history discovery that includes accepted unpublished HOT and selected LIVE where applicable.
5. A RuntimeHost-owned ordinary retrospective use-case service and a sealed Context Runtime historical-evidence route.
6. Context Runtime current-owner resolution over accepted HOT rather than repository-only state.

Absence of a public Story reader is not itself a baseline blocker.

## 5. Synthesis-completeness result

The evidence set covers every Step-1 claimed owner and the newly discovered HOT/history/currentness consumers. No unresolved external-source question changes the architecture choice. Additional research would add detail rather than change the current constraints, alternatives or recommendation.

STEP_2_SOURCE_COVERAGE: SUFFICIENT
EXTERNAL_RESEARCH_REQUIRED: NO
PRODUCT_OWNER_DECISION_DISCOVERED: NO

# W05.T06-A1 — Step 2 Research and Architecture Draft

Status: COMPLETE
Evidence basis: f75809027016522af2340dde077b9412fd394b9a

## 1. Problem restated

Two T06 product consumers are missing admitted machine boundaries:

- progressive onboarding needs deterministic READY_PC and local mechanical sufficiency against the actual accepted current view;
- ordinary Master retrospective needs bounded historical discovery and recipient-safe context without treating Story as truth.

The earlier Story-reader framing is too broad. Story access is optional. The real shared infrastructure gap is current-owner composition, because existing Context Runtime and any readiness implementation would otherwise read pinned Git while accepted unpublished HOT/SOFT can already be current.

## 2. System graph

    RuntimeHost
      |
      +-- OperationBasis
      |     +-- pinned campaign source
      |     +-- selected LIVE route/source
      |     +-- operation-scoped HOT read snapshot
      |
      +-- CurrentOwnerView
      |     +-- exact native owner route
      |     +-- accepted HOT/SOFT current owner
      |     +-- selected LIVE current owner
      |
      +-- ContextService
      |     +-- current PLAYER/knowledge/disclosure/world owners
      |     +-- profile.narration
      |
      +-- ReadinessService
      |     +-- CurrentOwnerView
      |     +-- BoundCatalogContext
      |     +-- deterministic readiness evaluator
      |
      +-- HistoryService
      |     +-- durable EVENT_INDEX
      |     +-- HOT event-discovery helper
      |     +-- selected LIVE history source
      |     +-- exact NativeSemanticEvent
      |
      +-- RetrospectiveService
            +-- current player/control orientation
            +-- HistoryService discovery/exact evidence
            +-- current knowledge/disclosure eligibility
            +-- sealed retrospective evidence
            +-- ContextService retrospective assembly
            +-- existing Narrator

    Story
      -- optional orientation only; baseline path does not depend on it

## 3. Shared current-owner boundary

### Recommendation

Add one RuntimeHost-internal CurrentOwnerView. It is an operation-scoped read capability, not a semantic owner and not a caller-supplied service.

The view selects one accepted current observation for a requested native owner identity:

1. selected LIVE source when current routing says LIVE owns that scope;
2. otherwise accepted established HOT/SOFT owner state when it is current under the operation basis;
3. otherwise the exact owner record at the pinned campaign source.

It must never select by timestamp, local generation magnitude, physical recency or convenience.

### Operation coherence

The RuntimeHost operation basis must bind a coherent HOT read snapshot or equivalent revalidation token. This is operational consistency only; it is not a campaign-global semantic frontier or global dirty generation.

If the HOT source changes incompatibly during an operation, the operation returns existing revalidation/currentness failure semantics rather than mixing generations.

Cold recovery does not resurrect stale unpublished HOT. Only source-equivalent rebuilt cache may participate after recovery.

### Consumers

- Context Runtime current families move from repository-only reads to CurrentOwnerView.
- ReadinessService uses the same view.
- RetrospectiveService uses it for current orientation/eligibility.
- HistoryService uses it for exact accepted unpublished runtime.semantic_event where applicable.

This boundary is justified by multiple existing consumers and Step-5.1 current-view law; it is not speculative generic storage infrastructure.

## 4. Production readiness design

Add a production module under GAME/TOOLS for deterministic character readiness. It independently realizes the canonical READY_PC contract and must not import DEV tooling.

RuntimeHost exposes ReadinessService with two distinct operations:

- assess_local_sufficiency: evaluate one already-derived typed immediate mechanical dependency set;
- assess_ready_pc: evaluate canonical READY_PC for one nominated Actor/current PLAYER binding and one admitted BoundCatalogContext.

The service reads current Actor/PLAYER/Asset/Effect and required native dependencies through CurrentOwnerView. Catalog/rules inputs come from an admitted BoundCatalogContext whose basis already contains catalog generation, ruleset lock and ruleset_set_sha256 evidence.

A readiness result contains:

- nominated and validated actor/player identities;
- actor state revision/currentness basis;
- ready boolean or typed status;
- deterministic blocker codes;
- exact catalog/ruleset identity;
- reconstructive provenance/attestation when ready.

It does not:

- persist a ready flag;
- mutate Actor status;
- decide PLAY_READY;
- force SAVE/publication;
- accept a bootstrap boolean as authority.

On resume/rejoin or after accepted build/current-owner change, readiness is recomputed. A previously active Actor that no longer satisfies the current predicate is an integrity/product failure to handle fail-closed, not permission to invent missing mechanics.

## 5. Native retrospective design

### Use-case owner

Add a RuntimeHost sibling RetrospectiveService. It is a use-case orchestrator, not a seventh logical LLM role and not a second history owner.

Normal path:

    Interpreter result
      -> typed retrospective request
      -> current active PLAYER / selected controlled PC validation
      -> current entity/thread/source orientation
      -> bounded History discovery
      -> exact NativeSemanticEvent / T0/native source evidence
      -> current knowledge/disclosure eligibility
      -> sealed retrospective evidence
      -> Context profile.narration with retrospective=True
      -> Narrator

No additional logical Master role is introduced.

### Why a separate service

Putting discovery, current eligibility and exact-history acquisition into HistoryService would make History own player authorization and context policy. Putting them into Context Runtime would make Context own history discovery and source traversal. RetrospectiveService keeps the product use case explicit while the existing owners retain their responsibilities.

## 6. Minimum History discovery

The trigger in WP19-L36 is satisfied: existing ordinal EVENT_INDEX metadata cannot locate qualifying events by entity/thread/session/source without broad event-body reads.

### Preferred realization

Extend the existing derived EVENT_INDEX rather than create a second durable history index.

Each accepted runtime.semantic_event may retain, inside semantic_delta, deterministic discovery_refs:

    discovery_refs:
      - owner_family: world.actor
        owner_identity: [ACTOR_x]
      - owner_family: world.location
        owner_identity: [LOCATION_y]
      - owner_family: runtime.session
        owner_identity: [SESSION_z]

Rules:

- refs are derived/validated from already accepted event inputs, source bindings or provenance; LLM text cannot invent index authority;
- they contain identifiers only, never prose, motive, T0 factor values, current knowledge or disclosure;
- the durable EVENT_INDEX copies only the subset permitted by existing index-safety policy;
- missing discovery metadata means less discoverability, never semantic absence;
- exact source evidence remains the event/native owner, never the index.

EVENT_INDEX remains the one durable event discovery projection. Existing complete/upper_ordinal enrollment semantics are retained and the campaign template must be aligned with the current History reader.

### Query forms

HistoryService gains bounded structured discovery, not free-text search:

- exact accepted event/source ref;
- current entity/thread/native owner ref;
- session ref when already established;
- recent bounded tail;
- bounded source/provenance ref supplied by already eligible current evidence.

The request carries a finite max-candidate bound. It has no regex, arbitrary predicate, embeddings, generic tags or open-ended pagination loop.

A query may scan the one accepted monolithic EVENT_INDEX artifact in memory because WP11 explicitly keeps family indexes monolithic until WP24 measured evidence says otherwise. Result cardinality stays bounded and event bodies are not scanned broadly.

### HOT and LIVE

Durable EVENT_INDEX alone is insufficient because accepted unpublished semantic events may already be current.

The local HOT transaction that establishes an unpublished runtime.semantic_event must also update a narrow derived event-discovery helper atomically. History discovery merges:

- durable EVENT_INDEX candidates at the pinned basis;
- current accepted HOT discovery rows from the operation snapshot;
- selected LIVE history discovery metadata where LIVE owns current history.

Duplicate event identities collapse to the accepted current source observation. Pre-CAS prospective LIVE state is excluded.

If a selected LIVE source lacks the required bounded discovery metadata, the service returns a typed bounded inability. It must not fall back to campaign history as current live truth or scan a remote epoch broadly.

## 7. Exact evidence and eligibility

Discovery returns only candidate references. Material claims require exact native evidence.

Exact historical records are read by HistoryService under owner-issued currentness/source basis. Current state questions are always answered from CurrentOwnerView, not from historical event bodies.

Raw private event bodies never become Narrator context merely because deterministic runtime could read them. RetrospectiveService produces a sealed evidence carrier tied to the same operation basis. Context Runtime revalidates current PLAYER/control/knowledge/disclosure and admits only eligible projections.

For retained T0 basis, availability classification and current eligibility are both enforced. If exact T0 evidence is absent or ineligible, the answer must distinguish evidence from inference under WP19-L37.

The ordinary public ContextService caller cannot forge historical evidence. Direct retrospective=True without RuntimeHost-issued retrospective evidence remains fail-closed.

## 8. Story disposition

Baseline: DEFER.

Reason:

- native History discovery is required anyway because Story may be absent or stale;
- Story lookup can only nominate candidates;
- adding a public Story reader now creates another service and current eligibility integration without closing a correctness gap.

Revisit only if measured/runtime evidence shows one of:

1. native/index discovery cannot meet bounded interaction cost without broad event-body reads; or
2. concrete product evaluation shows Story orientation materially improves retrospective navigation and native evidence still remains the proof route.

If later activated, the adapter is read-only and exposes bounded entity_refs/source_refs/story_refs orientation only. It cannot supply current truth, eligibility or final evidence by itself.

## 9. Alternatives

### A. Story-first retrospective

Benefit: existing Story lookup metadata is convenient for human episodes.

Reject for baseline: Story can lag/fail, exact read path is private, and native History/current eligibility are still required. It adds dependency without removing mandatory work.

### B. Teach Context Runtime to perform history discovery directly

Benefit: fewer named services.

Reject: it would mix retrieval orchestration with role eligibility/currentness and broaden Context into a storage/search owner.

### C. Duplicate repository/HOT selection separately in readiness and retrospective

Benefit: locally simple patches.

Reject: currentness logic diverges, Context stays stale, and future consumers repeat the same authority-sensitive composition.

### D. Preferred hybrid

One internal current-owner view + production readiness evaluator + native History discovery + thin retrospective orchestrator; Story dormant.

This is the smallest design that closes all proven consumers without a generic memory/search subsystem.

## 10. Analytical challenge

Strongest opposing case:

The preferred design adds two services and a new current-owner abstraction when T06 could be patched with direct reads. That increases machine surface and touches RuntimeHost, Context, History and HOT.

Response:

Direct patches cannot be correct because current owners can be accepted in HOT before publication and the existing Context Runtime already demonstrates the same stale-read defect. CurrentOwnerView removes duplicated authority logic rather than adding semantic authority. ReadinessService and RetrospectiveService are use-case boundaries over already separate owners; neither becomes a storage owner.

Assumptions attacked:

- If HOT is never current before publication, the shared boundary would be unnecessary. WP12 explicitly disproves that assumption.
- If Story were guaranteed current and complete, it could carry navigation. Accepted Story law explicitly disproves that assumption.
- If EVENT_INDEX already supported semantic qualification, no new metadata would be needed. Current machine evidence disproves that assumption.
- If raw event visibility were sufficient, current knowledge/disclosure could be ignored. Step-4/WP19 explicitly disprove that assumption.

Concrete failure scenarios checked:

- readiness immediately after a local accepted build delta before SAVE;
- retrospective immediately after an accepted unpublished event;
- cold restart after unpublished HOT loss;
- live-claimed state before and after CAS;
- player loses control of previously selected PC;
- invalid/stale EVENT_INDEX;
- Story unavailable;
- historical motive requested without retained T0 evidence;
- secret/private event physically retrievable but not currently eligible;
- HOT changes during multi-owner assessment.

Recommendation confidence: HIGH

What evidence would change this recommendation:

- an already accepted machine API proving coherent HOT/LIVE/current-owner reads for Context and readiness;
- an existing bounded semantic History discovery API hidden from the inspected implementation;
- a new Product Owner requirement making Story fidelity mandatory for baseline Master answers rather than optional orientation;
- proof that the required event-discovery metadata cannot be retained without violating an existing higher-authority confidentiality contract.

# RD-13 — Native History / Story / T0 / Commentator / Dramaturg — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. No production implementation begins before independent Senior plan GO.

Goal: realize native SemanticEvent/history as its own causal/history authority, deterministic noncanonical Story projection with Story-local T0 support, a self-contained baseline Commentator snapshot/control/filter path and exactly the accepted multiplayer Dramaturg retained horizons — without authority transfer or unrestricted native fallback.

RD unit: `RD-13`
Direct readiness: `R022,R051,R084,R085,R099,R102,R131`.
Composite slices: `R016.STORY,R018.STORY,R062.SEMANTIC_EVENT_HISTORY,R087.SEMANTIC_EVENT_T0`.
Canonical owners: Step-4 truth/knowledge/Story; Step-5.10 Story projection durability; Step-5.11 transcript/history retention; R2.1 continuity/history; WP-19 historical Actor decision basis; Story/Commentator self-contained corpus owner decision; Story growth/sharding decisions; Multiplayer Model; exact WP-27 records.
Dependencies/joins: RD-03 Actor continuity and accepted T0 factor evidence; RD-05 accepted execution/mechanical evidence; RD-08 temporal/chronology evidence; RD-09 access/currentness; RD-10 role/recipient containment; RD-12 collaboration; RD-02 knowledge/disclosure information owners.
Out of scope: Story as gameplay/history/ACL/currentness authority; unrestricted Commentator native fallback; hidden CoT/raw reasoning retention; single-player durable Dramaturg; writer-specific partition/rollover until R093/R094/R095/R103 trigger; generic history DB or global ACL registry.

## Implementation Impact Envelope

SPEC / APPROVED DESIGN: Step-4 Story/history separation; Step-5.10; Step-5.11; R2.1; WP-19; 2026-09-09 Commentator self-contained corpus decision; exact readiness records.
BASELINE REF: fresh branch HEAD at execution.

EXPECTED OWNERS TO CHANGE:
- native `runtime.semantic_event`/LOG machine realization;
- Story projection-local state and Story unit projections;
- Story-local T0 materialization for qualifying history;
- Commentator snapshot/control/filter and downstream read-cache contract;
- multiplayer-only Dramaturg retained horizon projections.

EXPECTED CONSUMERS TO CHANGE:
- RD-02 normalization emits SemanticEvent drafts to native history;
- RD-03 Actor material change/T0 basis emits native history evidence;
- RD-05 execution/mechanical evidence feeds native history;
- RD-11 ordinary retrospective stays native/context route and does not depend on Commentator;
- RD-12 collaboration feeds retained multiplayer horizon evidence;
- RD-14 product/bootstrap consumes Story/T0 only where qualifying/available, never as unconditional gameplay-start prerequisite.

ALLOWED INTERFACES / CONTRACTS TO CHANGE:
- Create `GAME/TOOLS/history.py`;
- create `DEV/SCHEMAS/runtime-semantic-event-state.schema.json`;
- modify/replace current `GAME/SCHEMA/event.schema.yaml` to match the accepted native history owner;
- create `GAME/TOOLS/story.py`;
- create `DEV/SCHEMAS/story-projection-state.schema.json`;
- create `DEV/SCHEMAS/story-event-unit.schema.json`;
- create `DEV/SCHEMAS/story-narrative-unit.schema.json`;
- create `DEV/SCHEMAS/story-mechanics-unit.schema.json` only for accepted mechanical projection fields;
- create `DEV/SCHEMAS/semantic-event-t0-basis.schema.json`;
- create `DEV/SCHEMAS/commentator-snapshot.schema.json`;
- create `DEV/SCHEMAS/commentator-control-projection.schema.json`;
- create `DEV/SCHEMAS/commentator-view.schema.json`;
- create `DEV/SCHEMAS/dramaturg-horizon.schema.json`;
- create `GAME/TOOLS/commentator.py`;
- create `GAME/TOOLS/dramaturg.py` only for deterministic retained-horizon projection/update/invalidation; no LLM planning authority is implied;
- create Story scaffold/root projections under `GAME/CAMPAIGN/STORY/**` as the current v1 campaign scaffold is reconstructed;
- create exactly `GAME/CAMPAIGN/DRAMATURG/SHARED.yaml` and `GAME/CAMPAIGN/DRAMATURG/PLAYERS/<player_id>.yaml` as template/runtime paths only for admitted multiplayer retained horizons;
- create/modify `DEV/TESTS/test_rd13_story_t0_commentator.py`, project-map/audit projections.

PROTECTED INVARIANTS:
- native SemanticEvent/history is causal/history authority; Story EVENTS/NARRATIVE are projections;
- transcript is communication evidence, not SemanticEvent history;
- Story may lag/fail/rebuild without changing gameplay truth/recovery;
- Story coverage is layer/source-domain local and nonfictional;
- deterministic core owns Story IDs/validation/publication/coverage; Chronicler is editorial/generative only;
- qualifying WP-19 T0 basis is bounded, event-time and Story-self-contained after projection; no current T1 substitute;
- baseline Commentator factual-support universe is imported Story corpus + self-contained eligibility/control projection; no unrestricted Master-native fallback;
- physical possession of secret data is not eligibility; filter before LLM exposure includes metadata/oracle surfaces;
- content basis and control basis are distinct; control may refresh without content rewrite;
- Dramaturg retained projections never become Story/history/ACL/canon and are multiplayer-only under current admission.

Version Impact: native event/Story/control/horizon persisted contracts require explicit Version Impact Gate at each task. No historical migration/release execution is activated here.

## Task 1 — RED: native history and projection authority boundaries

**Files**
- Create: `DEV/TESTS/test_rd13_story_t0_commentator.py`
- Inspect: `GAME/SCHEMA/event.schema.yaml` and current campaign scaffold.

**Future interfaces**
```text
validate_semantic_event_draft(draft, source_basis) -> SemanticEventValidation
append_semantic_event(hot_tx, validated_event) -> SemanticEventRecord
build_story_source_bundle(layer, source_domain_basis, coverage) -> StorySourceBundle
project_story_window(bundle) -> StoryProjectionDraft
build_commentator_snapshot(content_basis, control_basis) -> CommentatorSnapshot
filter_commentator_request(snapshot, principal_scope, request) -> EligibleCommentatorBundle
```

**RED groups**
- `NativeHistoryAuthorityTests`: current shipped event schema still mixes legacy knowledge/visibility projections and lacks final owner contract/T0 binding;
- `StoryProjectionTests`: no v1 Story producer/projection-state machine;
- `CommentatorSelfContainedTests`: no self-contained snapshot/control/filter;
- `DramaturgHorizonTests`: no exact retained horizon contracts/paths.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.NativeHistoryAuthorityTests -v
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.CommentatorSelfContainedTests -v
```
Expected RED. Do not publish RED-only completion checkpoint.

## Task 2 — GREEN: native SemanticEvent/history family (`R062.SEMANTIC_EVENT_HISTORY`)

**Files**
- Create: `GAME/TOOLS/history.py`
- Create: `DEV/SCHEMAS/runtime-semantic-event-state.schema.json`
- Replace/reconcile: `GAME/SCHEMA/event.schema.yaml`
- Modify: `DEV/TESTS/test_rd13_story_t0_commentator.py`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`

**Native contract**
```text
SemanticEventRecord {
  event_id
  kind
  participant_refs[]
  source_basis[]
  causal_predecessor_refs[]
  chronology_relation_refs[]
  affected_owner_refs[]
  player_intent_ref? / accepted input refs where material
  mechanical_evidence_refs[]
  information_transition_refs[]
  t0_basis_ref?            # qualifying WP-19 event only
  provenance
}
```
Exact field spelling follows final schema conventions; no field may make event ID/order a global chronology scalar.

**Interfaces**
```text
validate_semantic_event_draft(draft, source_basis) -> SemanticEventValidation
append_semantic_event(hot_tx, validated_event) -> SemanticEventRecord
load_semantic_event(event_id) -> SemanticEventRecord
```

**Producer contracts**
- RD-02 may supply typed Lore/Knowledge/Disclosure transition refs and SemanticEvent draft;
- RD-03 may supply accepted Actor mutation + qualifying T0 basis candidate;
- RD-05 supplies accepted execution/mechanical evidence;
- RD-08 supplies native chronology relation evidence when material;
- no producer may write event truth outside its admitted evidence.

**RED/GREEN cases**
- transcript/message wording alone cannot become truth/history without admitted event basis;
- Story output cannot be passed back as native event source for the same claim without independent native evidence;
- causal refs and chronology refs remain distinct;
- event ID allocation/order does not establish fictional chronology;
- knowledge/disclosure changes are refs to their native owners, not embedded alternate authority;
- event append is owner-valid immutable history creation under RD-04/HOT transaction;
- invalid mixed-source/currentness basis rejects before append.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.NativeHistoryAuthorityTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN.

REFACTOR: history-specific validation stays in `history.py`; no generic event bus/history DB abstraction.

Coherent checkpoint: native event schema/runtime + focused tests + project-map/audit. This checkpoint is independent of Story projection freshness.

## Task 3 — qualifying event-time T0 basis (`R099` / `R087.SEMANTIC_EVENT_T0` source side)

**Files**
- Create: `DEV/SCHEMAS/semantic-event-t0-basis.schema.json`
- Modify: `DEV/SCHEMAS/runtime-semantic-event-state.schema.json`
- Modify: `GAME/TOOLS/history.py`
- Modify: `DEV/TESTS/test_rd13_story_t0_commentator.py`
- Consume: RD-03 Actor/source evidence and RD-02 information owner refs.

**T0 contract**
For a qualifying material Actor decision/transition, retain only the bounded factors that materially affected the accepted decision:
```text
factor_identity
factor_kind
immutable event-time value/stance/equivalent meaning
source/provenance binding
availability classification
```
May include bounded knowledge/belief/suspicion/rejection, goals/commitments, directed relationship facets, resources/constraints/circumstances and causal source refs. Never full psychology/per-turn snapshot/CoT/raw prompt.

**Interfaces**
```text
build_t0_basis(qualifying_event_request, eligible_event_time_sources) -> T0BasisCandidate
validate_t0_basis(candidate, event_source_basis) -> T0BasisValidation
```

**Cases**
- ordinary nonqualifying event incurs zero T0 capture work beyond the qualifying predicate;
- qualifying material decision without required retained factors cannot claim Commentator-ready T0 support;
- current T1 Actor state cannot fill missing event-time T0;
- hidden/private factor is retained with protection metadata, not omitted merely because current reader is ineligible;
- source refs must be event-time admitted and stable;
- no hidden reasoning/raw prompt stored.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.T0BasisTests -v
```
Expected GREEN.

Coherent checkpoint: T0 schema + history binding + focused tests. No Story write yet.

## Task 4 — Story root, layer projection state and deterministic producer (`R016.STORY` / `R018.STORY`)

**Files**
- Create: `GAME/TOOLS/story.py`
- Create: `DEV/SCHEMAS/story-projection-state.schema.json`
- Create: `DEV/SCHEMAS/story-event-unit.schema.json`
- Create: `DEV/SCHEMAS/story-narrative-unit.schema.json`
- Create: `DEV/SCHEMAS/story-mechanics-unit.schema.json`
- Create scaffold/root projections for:
  - `GAME/CAMPAIGN/STORY/TRANSCRIPT/`
  - `GAME/CAMPAIGN/STORY/EVENTS/`
  - `GAME/CAMPAIGN/STORY/MECHANICS/`
  - `GAME/CAMPAIGN/STORY/NARRATIVE/`
  - layer-local projection-state location selected by the existing Story owner/scaffold convention; it must remain under Story ownership, not MANIFEST/CURRENT/checkpoint/native allocator.
- Modify: `DEV/TESTS/test_rd13_story_t0_commentator.py`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`

**Interfaces**
```text
build_story_source_bundle(layer, source_domain_basis, coverage) -> StorySourceBundle
project_story_window(bundle) -> StoryProjectionDraft
validate_story_projection(draft, bundle) -> StoryProjectionValidation
publish_story_projection(validated_draft, frozen_story_basis) -> StoryPublicationResult
```

Deterministic core owns source selection, exact basis pinning, validation, final Story ID allocation, ref/availability validation, write-set construction, publication and coverage. Optional Chronicler output is draft/editorial input only.

**Cases**
- Story source-domain coverage advances only after legal terminal disposition;
- MAY_OMIT vs MUST_MATERIALIZE obey owner contract; generation/transport/source failure cannot masquerade as omission;
- layer source cursor/order has no fictional chronology meaning;
- Story-only commits do not create source backlog;
- semantic contract generation mismatch blocks/reprojects instead of silently inheriting coverage;
- Story loss/lag cannot block gameplay or become RRC;
- native event/current owner contradiction wins over stale Story.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.StoryProjectionTests -v
```
Expected GREEN.

Coherent checkpoint: Story producer + layer schemas/root/scaffold + focused tests. Native history remains separate owner.

## Task 5 — Story EVENTS/NARRATIVE self-contained T0 materialization

**Files**
- Modify: `GAME/TOOLS/story.py`
- Modify: `DEV/SCHEMAS/story-event-unit.schema.json`
- Modify: `DEV/SCHEMAS/story-narrative-unit.schema.json`
- Modify: `DEV/TESTS/test_rd13_story_t0_commentator.py`

For every qualifying SemanticEvent with retained T0 basis:
- `STORY/EVENTS` contains or Story-locally binds complete bounded factor set with factor identity, event-time value/stance/equivalent meaning, provenance/source and availability;
- `STORY/NARRATIVE` provides readable historical/causal account and references the Story-local EVENTS basis when detailed factors are not duplicated;
- a native-only pointer is insufficient for baseline Commentator promise;
- protection metadata is preserved even when current reader cannot see factor.

**Interfaces**
```text
materialize_story_event(native_event, t0_basis, availability_basis) -> StoryEventUnit
materialize_story_narrative(event_unit, editorial_draft?) -> StoryNarrativeUnit
```

**Tests**
- after current Actor T1 changes, Story-local T0 remains sufficient for supported historical explanation;
- NARRATIVE->EVENTS linkage is deterministic/recoverable;
- secret factor exists in comprehensive Story projection but is not exposed without eligible control;
- Story copy does not become source for current Actor/knowledge mutation.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.StoryT0MaterializationTests -v
```
Expected GREEN.

Coherent checkpoint: EVENTS/NARRATIVE T0 serialization/linking + tests.

## Task 6 — self-contained Commentator snapshot and control projection (`R051`,`R084`,`R102`)

**Files**
- Create: `GAME/TOOLS/commentator.py`
- Create: `DEV/SCHEMAS/commentator-snapshot.schema.json`
- Create: `DEV/SCHEMAS/commentator-control-projection.schema.json`
- Create: `DEV/SCHEMAS/commentator-view.schema.json`
- Modify: `DEV/TESTS/test_rd13_story_t0_commentator.py`
- Consume: RD-02 knowledge/disclosure owner evidence, RD-09 principal/PLAYER/access evidence, Story availability metadata.

**Snapshot contract**
```text
CommentatorSnapshot {
  content_basis
  control_basis
  story_content_manifest
  control_projection
}
```
Content basis and control basis are logically distinct. Content may be final while access/control later refreshes.

**Interfaces**
```text
build_commentator_control_projection(owner_state, content_basis) -> CommentatorControlProjection
build_commentator_snapshot(story_content, content_basis, control_projection, control_basis) -> CommentatorSnapshot
filter_commentator_request(snapshot, principal_scope, request) -> EligibleCommentatorBundle
reconstruct_commentary(eligible_bundle, request) -> CommentatorView
refresh_commentator_control(cache, newer_control_projection) -> CommentatorCacheGeneration
```

A downstream Commentator cache is a rebuildable local read model; implementation may choose physical layout/search/index/embedding locally, but it is not Master HOT and owns no HDM semantics. The plan does not prescribe SQL/storage engine.

**Deterministic anti-oracle filter occurs before any LLM materialization** and filters not only prose but IDs, titles, entity associations, counts, chapter membership, relation labels, T0 factors, search hits, pagination/navigation metadata and existence signals.

**RED/GREEN cases**
- baseline Commentator can decide supported visibility entirely from imported Story + control projection; no Master HOT/native owner read required per request;
- missing/incompatible control data fails closed for affected material;
- secret comprehensive cache content remains absent from ineligible retrieval bundle including metadata/oracle surfaces;
- control refresh may reuse immutable compatible content generation;
- Commentator cannot widen access or grant knowledge/disclosure;
- unsupported exact motive/communication/mechanical claim reports limitation rather than native fallback or invention;
- baseline qualifying T0 explanation works after T1 changes using Story-local material only;
- `reconstruct_commentary` has no mutation/SemanticEvent/currentness/knowledge side effect.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.CommentatorSelfContainedTests -v
```
Expected GREEN.

REFACTOR: deterministic filter/control logic is separate from optional generative rendering inside `commentator.py`; no second ACL registry.

Coherent checkpoint: Commentator snapshot/control/view schemas + deterministic filter/runtime + focused tests.

## Task 7 — exact multiplayer Dramaturg retained horizons (`R085`,`R131`)

**Files**
- Create: `GAME/TOOLS/dramaturg.py`
- Create: `DEV/SCHEMAS/dramaturg-horizon.schema.json`
- Create scaffold/runtime paths exactly:
  - `GAME/CAMPAIGN/DRAMATURG/SHARED.yaml`
  - `GAME/CAMPAIGN/DRAMATURG/PLAYERS/<player_id>.yaml`
- Modify: `DEV/TESTS/test_rd13_story_t0_commentator.py`
- Consume: RD-09 access/currentness, RD-10 recipient containment, RD-12 current collaboration generation/input/handoff evidence.

**Interfaces**
```text
project_shared_dramaturg_horizon(current_multiplayer_basis) -> DramaturgHorizon
project_player_dramaturg_horizon(player_id, eligible_basis) -> DramaturgHorizon
invalidate_dramaturg_horizon(existing, changed_basis) -> KEEP | REBUILD | DROP
```

These are retained noncanonical preparation horizons only. They cannot create world truth, player knowledge/disclosure, history, collaboration obligation or execution command.

**Cases**
- shared horizon contains only facts/preparation lawful for shared retained scope;
- player-specific horizon cannot expose another player's private inputs/control/context;
- control/disclosure/currentness change invalidates/rebuilds affected horizon deterministically;
- collaboration generation change prevents stale horizon from driving dependent planning;
- single-player mode creates no durable Dramaturg path under current admission;
- no generic plot graph/registry/scheduler/background worker.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.DramaturgHorizonTests -v
```
Expected GREEN.

Coherent checkpoint: two fixed retained path contracts + deterministic projection/invalidation + privacy tests.

## Task 8 — transcript/mechanics/history separation and source suitability

**Files**
- Modify: `GAME/TOOLS/story.py`
- Modify: `GAME/TOOLS/history.py`
- Modify: `DEV/TESTS/test_rd13_story_t0_commentator.py`
- Consume Step-5.11 transcript retention and RD-05 MechanicalEvent/receipt evidence.

**Cases**
- Transcript retains accepted communication evidence but never substitutes for native SemanticEvent;
- Story TRANSCRIPT may preserve exact/near-exact participant discourse subject to retention/availability contract;
- Story MECHANICS projects only admitted mechanical evidence and does not become mechanical authority;
- derived Story/Commentator/Dramaturg material cannot silently promote into native history/current truth;
- exact quote/detail requires surviving exact evidence; summary/projection does not invent exactness.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.HistoryProjectionSeparationTests -v
```
Expected GREEN.

Coherent checkpoint: separation/source-suitability behavior + tests.

## Task 9 — `R016.STORY`,`R018.STORY`,`R062`,`R087` integration closure

**Files**
- modify integration tests only unless an exact adapter from Tasks 2–8 is missing.

`R016.STORY`: Story native projection family/root semantics exist under Story ownership.
`R018.STORY`: route/body/load integration uses RD-04 substrate only where Story owner contract requires it; Story-specific ID/coverage state remains Story-local and never canonical allocator/currentness.
`R062.SEMANTIC_EVENT_HISTORY`: closes against Task 2 native history + its producer/consumer tests independently of Story freshness.
`R087.SEMANTIC_EVENT_T0`: qualifying native event + retained T0 + Story self-contained materialization joins RD-11 retrospective and RD-14 save/session sibling slices only at parent reconciliation.

`R099` T0 precedes only qualifying Story/Commentator consumption. It is **not** an unconditional bootstrap/gameplay-start prerequisite.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.CompositeIntegrationTests -v
```
Expected GREEN.

Coherent checkpoint: integration proof only.

## Task 10 — RD-13 verification / Version Impact

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS for active deterministic/scenario obligations.

Negative stale proof searches Story-as-canon/history/ACL/currentness, transcript-as-native-history, native-only Commentator fallback for promised corpus claims, Commentator mutation, T1-for-T0 substitution, secret metadata oracle leakage, Story feedback into same envelope, single-player durable Dramaturg, generic history DB/ACL registry and ID/Git order as chronology.

Version Impact Gate: reconcile native event schema, Story layer/projection-state, T0, Commentator control/snapshot and Dramaturg horizon generations independently. Checkpoint/migration projections change only when their owners require it. System Impact Gate stops on any new history/ACL/gameplay authority, unrestricted native fallback, global Story worker dependency or changed product semantics.

Currentness fence: fresh-read Step-4, Step-5.10/5.11, R2.1, WP-19, 2026-09-09 self-contained Commentator decision, RD-02/RD-03/RD-05/RD-08/RD-09/RD-10/RD-12 and exact touched files. Owner drift stops execution.

Final coherent checkpoint: native history + Story projection/T0 + Commentator self-contained control/filter + multiplayer Dramaturg paths all green, audit/full DEV tests green and remote read-back recorded. RD-13 closes only its direct leaves/listed slices; composite/pure-proof package closure remains the package proof-ledger checkpoint.
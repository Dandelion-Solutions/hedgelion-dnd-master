# RD-03 — Actor / Asset / Effect Continuity — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. No production implementation begins before independent Senior plan GO.

Goal: realize clean v1 Actor/Asset/Effect native state plus owner-local Actor cognition/continuity behavior, replacing PC/NPC/item-era state shapes while preserving epistemic ownership, player agency, admitted history boundaries and bounded event-driven cognition.

RD unit: `RD-03`
Direct readiness: `R025..R028,R104,R108..R111,R113..R116,R126,R128..R130,R132,R136`.
Composite slices/parents: `R006.ACTOR,R016.ACTOR,R018.ACTOR,R029.ACTOR,R062.ACTOR_CONTINUITY_RELATIONS,R062.EFFECT_APPLICATION`.
Canonical owners: R2.1 continuity/history, R2.2 Actor continuity, exact Actor/Asset/Effect owners referenced by WP-27 Step-2, WP-10, WP-11.
Dependencies/joins: owner shapes feed RD-04 route/HOT; RD-14 consumes provisional Actor shape; RD-06/RD-14 join R029; RD-02 owns knowledge/disclosure normalization; RD-11 consumes Actor/history evidence but never Actor state; RD-13 owns Story/native-history projection publication where applicable.
Out of scope: persistence/publication authority, bootstrap lifecycle, Context Runtime selection/ranking, Story canon/history ownership, collaboration authority, generic memory/cognition/mutation service.

## Implementation Impact Envelope

SPEC / APPROVED DESIGN: R2.1 §§4–9/11.1; R2.2 Laws 1–28, especially 13–17; exact readiness records.
BASELINE REF: fresh branch HEAD at execution.

EXPECTED OWNERS TO CHANGE:
- `world.actor`, `world.asset`, `world.effect` machine/shipped projections;
- source-Actor-owned cognition/continuity runtime behavior;
- owner-local continuity-evidence preparation adapters.

EXPECTED CONSUMERS TO CHANGE:
- RD-04 route/HOT integration;
- RD-05 accepted execution/mutation application seam;
- RD-11 Actor/history retrieval inputs;
- RD-13 noncanonical Story/history consumers;
- RD-14 provisional Actor onboarding.

ALLOWED INTERFACES / CONTRACTS TO CHANGE:
- create `GAME/TOOLS/actor_continuity.py`;
- create `GAME/TOOLS/continuity_projection.py` for bounded R2.1 source-bundle/draft validation only; it is not a durable owner or publisher;
- create `DEV/SCHEMAS/actor-assessment-request.schema.json`;
- create `DEV/SCHEMAS/actor-delta-draft.schema.json`;
- create `DEV/SCHEMAS/continuity-projection-candidate.schema.json`;
- modify the existing Actor/Asset/Effect DEV schemas;
- create shipped Actor/Asset/Effect GAME schemas and retire PC/NPC/item schemas;
- tests/audit/project-map/storage README projections named below.

PROTECTED ARCHITECTURE INVARIANTS:
- source Actor owns only its non-epistemic private continuity;
- `world.knowledge` remains sole current proposition-stance owner;
- objective social facts remain with their native owners;
- no symmetric relationship inference;
- no engine-authored voluntary PC mental state;
- cognition is sparse/event-driven, never every Actor every turn;
- `NO_CHANGE` is successful assessment with zero semantic write;
- one assessment = one Actor + one explicit purpose + bounded eligible evidence + at most one coherent Actor-local delta;
- foundation mutation requires explicit stronger transition classification;
- transient persistence needs inspectable invalidation; no generic turn TTL/scheduler;
- Story/derived continuity is noncanonical and may orient but never establish current cognition;
- no new generic memory/history/projection authority.

ARCHITECTURE-SENSITIVE SURFACES: Actor mutation boundary, knowledge separation, accepted-source admission, foundation transitions, continuity projection publication handoff, provisional Actor identity.

Version Impact: classify actual schema/API/catalog projection changes at each checkpoint. Migration remains inactive absent its accepted trigger.

## Shared-file coordination

RD-02 first removes forbidden epistemic ownership from `pc.schema.yaml`, `npc.schema.yaml`, `item.schema.yaml`; RD-03 then retires those files in the Actor/Asset cutover. If RD-03 executes first for scheduling reasons, it must incorporate the same RD-02 epistemic-retirement assertions into the cutover checkpoint and RD-02 must rebase its remaining shared-file actions. Never publish an intermediate state that restores or preserves embedded writable knowledge/Secret authority.

## Task 1 — RED: native shape and behavioral boundary

**Files**
- Create: `DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`
- Inspect: current Actor/Asset/Effect DEV schemas and legacy GAME schemas.

**Required future interfaces**
```text
assess_actor(request, actor_state, eligible_evidence) -> ActorAssessmentResult
validate_actor_delta(actor_state, draft, eligible_evidence) -> ActorDeltaValidation
apply_actor_delta(hot_tx, validated_delta) -> ActorMutationResult
build_continuity_source_bundle(request, admitted_sources) -> ContinuitySourceBundle
validate_continuity_projection(candidate, source_bundle) -> ContinuityProjectionValidation
```

**RED groups**
- `NativeActorShapeTests`: v1 Actor/Asset/Effect owner shape and no embedded knowledge;
- `ActorAssessmentBehaviorTests`: event-trigger/purpose/NO_CHANGE/bounded delta/pre-commit validation absent;
- `ContinuitySourceAdmissionTests`: admitted-history/source validation path absent;
- `LegacyEntityProjectionTests`: old PC/NPC/item native projections still active.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity.ActorAssessmentBehaviorTests -v
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity.NativeActorShapeTests -v
```
Expected RED for absent shipped behavioral runtime and remaining projection debt. Do not publish a RED-only completion checkpoint.

## Task 2 — GREEN: reconcile native Actor / Asset / Effect contracts

**Files**
- Modify: `DEV/SCHEMAS/world-actor-state.schema.json`
- Modify only if owner-required: `DEV/SCHEMAS/world-actor-group-state.schema.json`
- Modify: `DEV/SCHEMAS/world-asset-state.schema.json`
- Modify: `DEV/SCHEMAS/world-effect-state.schema.json`
- Create: `DEV/SCHEMAS/actor-assessment-request.schema.json`
- Create: `DEV/SCHEMAS/actor-delta-draft.schema.json`
- Modify: focused tests.

**Machine requirements**
- complete native identity;
- foundation/evolving/transient lifetime classification without three artificial owners;
- sparse source-Actor-local relationship facets (`trust, affinity, fear, respect, hostility, felt_obligation`) with no auto-inverse;
- Actor continuity contains no proposition stance duplicate;
- transient item carries owner-valid invalidation basis if persisted;
- `ActorAssessmentRequest` identifies exactly one Actor, explicit purpose (`REACT|REFLECT|PLAN|RECONSIDER|RELATIONSHIP_UPDATE`), material trigger refs, current Actor revision and bounded evidence refs;
- `ActorDeltaDraft` permits `NO_CHANGE` or one coherent Actor-local delta and carries source/current-revision evidence necessary for deterministic validation.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity.NativeActorShapeTests -v
```
Expected GREEN.

REFACTOR: share structural definitions only when owner lifecycles remain distinct.

Coherent checkpoint: DEV native contracts + assessment/delta contracts + shape-focused tests. It claims schema/contract realization only, not behavioral closure.

## Task 3 — GREEN: owner-local Actor assessment and deterministic write boundary

**Files**
- Create: `GAME/TOOLS/actor_continuity.py`
- Modify: `DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`

**Interfaces**
```text
class ActorAssessmentResult:
    disposition: NO_CHANGE | DELTA_PROPOSED | REJECTED
    draft: ActorDeltaDraft | None
    reason_code: str | None

assess_actor(request, actor_state, eligible_evidence) -> ActorAssessmentResult
validate_actor_delta(actor_state, draft, eligible_evidence) -> ActorDeltaValidation
apply_actor_delta(hot_tx, validated_delta) -> ActorMutationResult
```

`assess_actor` is the bounded semantic proposal boundary. `validate_actor_delta` and `apply_actor_delta` are deterministic control. The module is Actor-owner-specific and is not a generic LLM/mutation/memory service.

**RED/GREEN cases**
- no material trigger -> assessment is not scheduled/called for dormant Actor;
- each accepted request names one explicit purpose and one source Actor;
- `NO_CHANGE` succeeds and produces no HOT dirty owner generation and no SemanticEvent merely to prove thought occurred;
- proposal touching unrelated Actor or multiple independent purposes is rejected;
- target/current revision mismatch is rejected before write;
- evidence ref outside bounded eligible request basis is rejected;
- attempted `world.knowledge` mutation is rejected/routed to RD-02 instead;
- foundation field change without explicit `FOUNDATION_TRANSITION` classification + admitted material cause is rejected;
- transient state without inspectable event/state/fictional-time/owner-revision invalidation is rejected;
- PC voluntary belief/emotion/goal/plan/speech/consent mutation without player-authored or genuine rules/world constraint is rejected;
- relationship `A -> B` write changes only A-owned relationship view; no inverse mutation;
- one accepted draft mutates one coherent source-Actor-local field set in one owner transaction.

Run RED against missing module, then GREEN:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity.ActorAssessmentBehaviorTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN.

REFACTOR: purpose-specific proposal helpers may remain private; no generalized “cognition engine”.

Coherent checkpoint: `actor_continuity.py` + behavioral tests + audit/project-map projection. Must be independently green before publication.

## Task 4 — accepted-history/source-suitability and continuity projection candidate

**Files**
- Create: `GAME/TOOLS/continuity_projection.py`
- Create: `DEV/SCHEMAS/continuity-projection-candidate.schema.json`
- Modify: `DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`

**Interfaces**
```text
build_continuity_source_bundle(request, admitted_sources) -> ContinuitySourceBundle
validate_continuity_projection(candidate, source_bundle) -> ContinuityProjectionValidation
classify_projection_compatibility(projection_basis, current_sources) -> COMPATIBLE | REPAIRABLE | OBSOLETE | UNCERTAIN
```

This module implements the R2.1 source-admission/validation seam only. It does **not** publish Story or create another continuity record family. When a durable noncanonical Story unit is warranted, the validated candidate plus its source basis is handed to RD-13's Story/Chronicler publication path.

**Behavior / tests**
- rejected generations, abandoned Narrator drafts, hidden CoT/internal prompts/private diagnostics cannot enter `ContinuitySourceBundle`;
- accepted Message/SemanticEvent/MechanicalEvent/receipt/native history may enter only for the claim semantics they actually prove;
- Story may orient but a material current claim triggers proper-source escalation rather than becoming current Actor state;
- current owner contradicting Story marks projection stale/defective, never reconciles by vote;
- derived projection absence never proves semantic absence;
- candidate retains stable source refs/source-domain coverage/projection-generation metadata;
- validation enforces shape/cardinality/source membership and forbidden-authority mutation;
- `UNCERTAIN` excludes/degrades the projection and uses stronger evidence; it never guesses;
- exact wording can be claimed only from surviving exact evidence.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity.ContinuitySourceAdmissionTests -v
```
Expected GREEN.

Coherent checkpoint: source-bundle/projection-validation adapter + contract + focused tests. Durable Story publication remains a named RD-13 join, not an RD-03 write.

## Task 5 — shipped GAME cutover to Actor / Asset / Effect

**Files**
- Create: `GAME/SCHEMA/actor.schema.yaml`
- Create: `GAME/SCHEMA/asset.schema.yaml`
- Create: `GAME/SCHEMA/effect.schema.yaml`
- Retire: `GAME/SCHEMA/pc.schema.yaml`
- Retire: `GAME/SCHEMA/npc.schema.yaml`
- Retire: `GAME/SCHEMA/item.schema.yaml`
- Modify: `GAME/SCHEMA/README.md`
- Modify: `GAME/TEMPLATE/STORAGE_README.md`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`
- Modify: focused tests.

**RED/GREEN**
- active projections reference legacy PC/NPC/item native contracts before cutover;
- after cutover, one `world.actor` family owns Actor records; PC/NPC are classifications/projections only;
- `world.asset` replaces native item family while human-facing “item” wording is presentation only;
- Effect projection preserves natural-owner application semantics;
- no epistemic fields duplicated from RD-02;
- old schemas and direct consumers disappear in the same coherent checkpoint; no compatibility wrapper.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity.LegacyEntityProjectionTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN.

Coherent checkpoint: three new shipped schemas + three retirements + README/storage/audit/project-map synchronization + tests.

## Task 6 — runtime joins: execution/HOT, knowledge and history

**Files**
- Modify: `GAME/TOOLS/actor_continuity.py`
- Consume: RD-04 `NativeHotStore.transaction(...)`;
- Consume: RD-02 information-normalization/knowledge owner API for epistemic transitions;
- Consume: RD-13 native history interface for material accepted Actor changes;
- Modify focused/integration tests.

**Join law**
```text
bounded Actor proposal
-> deterministic Actor delta validation
-> owner-local HOT transaction
-> accepted Actor mutation
-> material epistemic consequence, if any, through RD-02 only
-> material history consequence, if any, through RD-13 native SemanticEvent owner
```

Tests prove no generic transaction spans LLM/host interaction and that failed validation writes none of Actor/knowledge/history. Actor state commit does not wait for Story projection.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity.ActorMutationIntegrationTests -v
```

Coherent checkpoint: smallest owner-valid RD-03/RD-04/RD-02/RD-13 integration wiring + tests. No authority transfer.

## Task 7 — provisional Actor / onboarding and recall consumers

**Files**
- Modify focused tests only unless a concrete adapter is missing from Tasks 3–4.
- Consume later RD-14 bootstrap and RD-11 Context Runtime interfaces.

Prove:
- provisional Actor has stable native identity + structurally valid sparse state without complete-sheet prerequisite;
- same provisional identity is consumable by RD-14 and later durability branch of R029;
- RD-11 may consume current Actor/eligible history evidence but cannot mutate or rank material into Actor authority;
- broad/episodic/entity continuity views remain distinct from current Actor state and exact recall.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity.ProvisionalActorConsumerTests -v
```

Coherent checkpoint: consumer-contract proof only; no bootstrap/context ownership.

## Task 8 — RD-03 closure / direct and composite reconciliation

Required evidence:
- every direct RD-03 readiness ID maps to a named schema/runtime/consumer/test task;
- R031/R032 proof routes are not satisfied merely by schema fixtures: package proof ledger must reference Actor behavioral tests for READY_PC/lazy derivation/initial-commitment/domain behavior and retain dormant measured branches as dormant;
- `R006.ACTOR`, `R016.ACTOR`, `R018.ACTOR`, `R029.ACTOR`, `R062.ACTOR_CONTINUITY_RELATIONS`, `R062.EFFECT_APPLICATION` have exact implemented/proof surfaces without claiming sibling slices;
- no one-memory blob, duplicate knowledge owner, symmetric relation, continuous NPC simulation, generic TTL/background assessment or PC voluntary-state write survives.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd03_actor_asset_effect_continuity -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS for current deterministic/scenario obligations.

Version Impact Gate: classify Actor/Asset/Effect schema/API/catalog impacts and synchronize exact projections once. System Impact Gate stops on any need for a new cognition/memory/history authority, cross-owner mutable state or changed player-agency semantics.

Final coherent checkpoint: native contracts + Actor behavior + continuity source-validation seam + shipped cutover + owner joins + tests/audits. Story publication, bootstrap lifecycle, persistence authority and package proof closure remain with their native owners.
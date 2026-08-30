# S6D-06 — Registered Activity Primitive Contracts — Architecture Task Brief

Status: **STEP 1 COMPLETE — WHOLE-PROJECT BRIEF CRITIC PASS — STEP 2 NOT STARTED**

Date: 2026-08-26
Authoritative branch: `v1/engine-rearchitecture`
Pinned Step-1 remote ref: `35f3ec5548b6ec99033fc0f61a35c1c04c383de7`
Predecessor: S6D-05 complete and canonically owned by `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md`

## 1. Assignment

Execute only Step 1 of the S6D-06 eight-step design loop.

Frame the evidence and decision work required to close the registered `op.*` Activity primitive surface. For every current registry item, determine whether an exact supported contract is required now, the item must remain dormant/nonselectable until a named downstream trigger, or the item is stale and must be removed. For every supported primitive, require exact compile-time and deterministic-execution contracts for arguments, results, reads, mutations, RNG, bindings, exports, atomicity, failures and suspension.

After mandatory whole-project brief criticism, publish the repaired Task Brief, critic and minimal routing/status updates, verify the authoritative branch, and stop. Do not begin Step 2 or S6D-07.

## 2. Problem

`core-catalog.json` currently registers 31 Activity primitive IDs, while Activity definitions already expose `steps[].op`, `args`, `when` and `export`. Registration is not an execution contract. The repository does not yet prove item-by-item that every admitted primitive:

- has an exact closed argument and result shape;
- reads only declared authoritative inputs through accepted accessors/selectors/facts;
- can mutate only the correct semantic owner through the Step-3 commit protocol;
- handles RNG, child work, suspension, retry and failure without duplicating their owners;
- has an actual supported consumer or a justified dormant/removal disposition;
- cannot become an arbitrary query, scripting, path, file, network or generic mutation channel.

S6D-06 must close that gap without inventing seed behavior ahead of S6D-07–09 and without reopening accepted execution, MechanicalContext or portable-value architecture.

## 3. Goal

Produce an evidence-backed candidate that can eventually prove:

1. exact bidirectional accounting of every registered `op.*` ID;
2. one semantic and machine contract route for each supported primitive;
3. exact argument/result/binding/export types and validation phase;
4. exact allowed reads, dependency kinds and pinned state view;
5. exact mutation owner, transition/event evidence and segment atomicity;
6. exact RNG request/result generation and retry reuse where applicable;
7. exact child invocation, choice, reaction, scheduling and suspension behavior where applicable;
8. exact failure and no-partial-commit behavior using existing Step-3 dispositions;
9. dormant/removal treatment for primitives without current supported need;
10. preservation of S6D-01–05, Step-2 mechanics, Step-3 execution and Step-5 recovery owners;
11. no unbounded executable language or hidden query/fixed-point/workflow engine;
12. synchronization of architecture, catalogs, schemas, examples and focused verification.

## 4. In scope

### 4.1 Exact registry census

The starting registry is the current `activity_primitives` family:

`op.select_targets`, `op.roll`, `op.resolve_check`, `op.resolve_contest`, `op.resolve_save`, `op.resolve_attack`, `op.apply_damage`, `op.apply_healing`, `op.set_temporary_hp`, `op.consume_resource`, `op.restore_resource`, `op.move_entity`, `op.teleport_entity`, `op.transfer_asset`, `op.transfer_currency`, `op.create_entity`, `op.retire_entity`, `op.create_effect`, `op.update_effect`, `op.remove_effect`, `op.transform_entity`, `op.create_zone`, `op.update_zone`, `op.remove_zone`, `op.for_each_target`, `op.branch`, `op.request_choice`, `op.open_reaction_window`, `op.emit_fact`, `op.schedule_followup`, `op.advance_local_time`.

This list is a pinned starting fact, not a presumption that all 31 remain active. Step 2 must re-read current remote registry and admission ledger and reconcile exact equality.

### 4.2 Primitive contract dimensions

For every supported primitive:

- exact operation identity and contract revision/compatibility route;
- argument object, requiredness, type/cardinality and discriminators;
- actor/source/target/owner/definition bindings and role resolution;
- allowed selector/accessor/invocation-fact reads and prospective/committed view;
- result shape, export names/types and later-step visibility;
- RNG request/result contract and authoritative generation point;
- prospective transitions/deltas and exact mutation-owner class;
- MechanicalEvent and receipt/trace evidence obligations;
- atomic segment grouping, commit point and rollback/no-partial-commit rule;
- deterministic validation, missing/hydration and execution failures;
- suspension, pending child, choice/reaction, follow-up and resume currentness;
- idempotency, retry and duplicate execution prevention;
- execution bounds for iteration/branching/child depth and produced work;
- catalog-context and definition-revision pinning.

### 4.3 Primitive families to distinguish

The investigation must test rather than assume the correct grouping of:

- selection and roll/resolution primitives;
- state-changing actor/resource/location/asset primitives;
- entity/effect/zone lifecycle primitives;
- bounded control-flow primitives (`for_each_target`, `branch`);
- suspension primitives (`request_choice`, `open_reaction_window`);
- fact/event/follow-up/time primitives.

Shared metadata is permitted only where evidence proves identical semantics. Family templates must not erase item-specific arguments, mutation owners or failures.

### 4.4 Machine closure

- operation registry and admission-ledger equality;
- canonical operation-contract catalog/schema route selected from evidence;
- Activity `steps[].op/args/when/export` compilation;
- exact links to portable values, accessors/selectors/facts, transitions, events, segments, children, receipts and continuation;
- structural examples versus activated supported consumers;
- executable tests for positive, invalid, dormant, failure, suspension and recovery paths.

## 5. Out of scope

- authoring concrete species, classes, feats, spells, equipment, monsters or Activities (S6D-07–09);
- choosing balance values or supported-content breadth without evidence;
- redefining Activity parameters, Target/Area/Cost/Duration, rolls or offers already owned by S6D-05;
- redefining selector/accessor/fact semantics owned by S6D-03/04;
- defining HP/LifeState/Resource/Effect/Condition/Recovery domain semantics owned by S6D-08, except routing exact primitive dependencies to that owner;
- implementing the runtime executor/compiler;
- a generic query, expression, script, JSON-patch, object-path, reflection, file or network language;
- a general workflow/event-bus/rules fixed-point engine;
- new persistent record owners for primitive calls, Signal or StateDelta;
- reopening accepted architecture without a concrete contradiction and decision-ready superseding proposal.

## 6. Inherited invariants and owner boundaries

1. Activity definitions are declarative; `op.*` identifies a closed registered primitive, never executable code.
2. Registry presence is not activation. Unsupported items may be dormant or removed.
3. Definition compilation validates exact operation/argument/export compatibility before accepted execution.
4. S6D-04 owns mechanical reads, input authority, missing semantics, consumer permission and the hydrated bound-instance DAG.
5. S6D-05 owns portable values and their recovery equality. Primitive contracts consume those values but do not redefine them.
6. Signal and StateDelta currently have rejecting dormant roots. S6D-06 may activate only exact consumer/variant contracts proven necessary; it may not create a generic envelope or lifecycle/disposition state.
7. Cost commitment route `cost_commit.on_accept` is dormant pending an exact S6D-06 primitive/segment contract; reservation/refund/atomicity must be reconciled with Step 3 rather than inferred from its name.
8. Prospective changes exist inside evaluation/ExecutionSegment planning. Commit disposition belongs to ExecutionSegment; committed fact belongs to MechanicalEvent; outcome/evidence belongs to receipt/trace.
9. A primitive mutates only declared semantic owners through accepted transition/commit machinery; it never owns authoritative state itself.
10. One Resolution generation uses one pinned `ResolvedCatalogContext` and one permitted committed/prospective state view.
11. Authoritative RNG results are generated once and retained/reused across retry; the LLM cannot supply authoritative random outcomes.
12. Continuation retains only accepted causal inputs and pending work required for deterministic resume; no trusted prospective StateDelta is restored.
13. Child work and response currentness use existing Resolution/Continuation/PendingChild identity and generation, not a parallel queue.
14. Missing/hydration/validation/execution failures use existing owners and codes unless evidence proves a necessary extension.
15. Partial commit is forbidden unless an already accepted owner explicitly defines a committed earlier segment; failure cannot silently leave undeclared mutation.
16. Iteration, branching and follow-up production are statically bounded or deterministically runtime-bounded by accepted inputs; no recursive unbounded execution surface is admitted.
17. Exact domain mutation semantics remain with Actor/Asset/Resource/Effect/Condition/location/time owners; primitive contracts specify allowed invocation and evidence, not duplicate domain laws.
18. Human decisions are required only for material supported semantics, authority, scope, trade-offs or risk acceptance—not for evidence discovery or technically forced representation synchronization.

## 7. Mandatory Source Manifest

Step 2 must start from a fresh remote ref and record for every source: authority role, applicability, supersession, extracted item-level evidence and unresolved conflict.

### 7.1 Process, sequence and S6D anchors

- `AGENTS.md`;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`;
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`;
- `DEV/docs/superpowers/plans/2026-08-24-step-6-residual-rules-seed-debt-closure-plan.md`;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` and `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-canonicalization.md`;
- `DEV/ARCHITECTURE/CATALOG_ADMISSION.md` and `DEV/docs/superpowers/specs/2026-08-25-s6d-02-catalog-admission-gap-closure-canonicalization.md`;
- `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md` and `DEV/docs/superpowers/specs/2026-08-25-s6d-03-complete-calculation-selector-metadata-canonicalization.md`;
- `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md` and `DEV/docs/superpowers/specs/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-canonicalization.md`;
- `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md` and `DEV/docs/superpowers/specs/2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-canonicalization.md`.

### 7.2 Activity, rule and execution owners

- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`;
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-resolution-gate.md`;
- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`, `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md` and `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`;
- `DEV/ARCHITECTURE/ACTOR_MODEL.md` and `DEV/ARCHITECTURE/ASSET_MODEL.md` for Actor/Asset identity and mutable-state ownership;
- `DEV/docs/superpowers/design/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md` as the Step-1/2 assurance locator, followed to the exact Resource, HP/LifeState, Effect, Condition, location/zone and identifier model/schema owners rather than used as their detailed semantic owner;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md` and `DEV/docs/superpowers/design/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`;
- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`;
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md`;
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md`.

For each, extract exact ownership of validation, state view, mutation, commit, failure, suspension, idempotency, retention and evidence.

Historical derivation must include `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`, explicitly classified as provenance-only and non-authoritative wherever later accepted Steps 2–5 or S6D owners supersede it. It may identify old assumptions or stale vocabulary but cannot settle a current contract.

### 7.3 Catalog and schema realization

- `DEV/CATALOG/core-catalog.json` `activity_primitives`, transition/event/failure/value families;
- `DEV/CATALOG/catalog-admission-ledger.json` exact rows for every primitive;
- `DEV/CATALOG/entity-structures.json` for domain definition/state bindings;
- `DEV/CATALOG/mechanical-surfaces.json` and its schema;
- `DEV/CATALOG/portable-value-contracts.json` and `portable-value-routes.json`;
- `DEV/SCHEMAS/activity-definition-data.schema.json`;
- `runtime-command-state`, `runtime-resolution-state`, `runtime-continuation-state`, `execution-segment`, `pending-child-invocation`, `transition-request`, `resolution-receipt`, `roll-request`, `roll-result`, `choice-request`, `reaction-offer`, `signal`, `state-delta`, `invocation-fact`, `boundary-occurrence`, `mechanical-predicate` and `mechanical-accessor-ref` schemas;
- exact domain definition/state schemas reached from each candidate mutation owner;
- `DEV/SCHEMAS/condition-definition-data.schema.json`, `effect-definition-data.schema.json`, `duration-spec.schema.json` and `temporal-binding.schema.json` as exact Condition/Effect/definition-duration/concrete-temporal routes;
- `DEV/SCHEMAS/activity-parameter-binding.schema.json`, `action-request.schema.json`, `runtime-continuation-state.schema.json` and `resolution-receipt.schema.json` as the House-Rules typed-binding acceptance/recovery/evidence route;
- every direct/transitive `$ref`, inline operation branch and discriminator consumer found from these anchors.

The absent `mechanical-event.schema.json` path observed at the pinned ref must not be treated as proof that MechanicalEvent lacks an owner. Locate its actual representation in the Step-3 schemas/spec/tests before proposing any new file or record.

### 7.4 Tests and runtime consumers

- `DEV/TESTS/test_s6d_02_catalog_admission_contract.py`;
- `DEV/TESTS/test_s6d_03_selector_metadata_contract.py`;
- `DEV/TESTS/test_s6d_04_mechanical_context_contract.py`;
- `DEV/TESTS/test_s6d_05_portable_value_contract.py`;
- `DEV/TESTS/test_step2_evaluation_input_contract.py` and `DEV/TESTS/test_step2_condition_applicability.py`, followed to exact Resource/HP/LifeState/Effect/Condition state-owner tests reached by each primitive;
- `DEV/TESTS/test_step3_execution_owner_contract.py`;
- `DEV/TESTS/test_step3_resume_ordering_contract.py`;
- `DEV/TESTS/test_step3_execution_value_schemas.py`;
- `DEV/TESTS/test_step3_execution_examples.py`;
- `DEV/TESTS/test_step3_event_followup_contract.py`;
- `DEV/TESTS/test_step3_execution_catalog_contract.py`;
- `DEV/TESTS/test_house_rules_adjudicated_input_contract.py` and `DEV/TESTS/test_house_rules_policy_authority_contract.py`;
- the Step-3 tests above as the existing executable continuity/recovery contract reached by Step-5 owners; inspect the exact Step-5.2, Step-5.3, Step-5.7 and Step-5.13 canonical specs/resolution gates for any additional executable or scenario-test references and record every actual path found—do not invent a test filename when a Step-5 owner supplies only canonical scenarios;
- catalog/schema maintenance and release validation;
- `GAME/CORE/RUNTIME.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`, `ADJUDICATION.md`, `COMBAT.md`, `MAGIC.md`, `EXPLORATION.md`, `PROCESSES.md`, `CHRONOLOGY.md`, `REWARDS.md`, `ADVANCEMENT.md` and `CHARACTER_READINESS.md` as behavioral consumers, not machine-contract owners unless their headers explicitly say otherwise. For resource restoration/rest and `op.advance_local_time`, follow `ADVANCEMENT.md`/`CHARACTER_READINESS.md` into the exact Rest/Resource/TemporalBinding/BoundaryOccurrence owners above rather than treating GAME prose as mutation authority.

### 7.5 Discovery rule

Use `DEV/PROJECT_MAP.md` to build the dependency subgraph before symbol search. Then search exact primitive IDs, `steps[].op`, argument/result/export fields, transition/event kinds, pending-child and failure codes across the current tree. A zero-result code search is non-evidence until actual indexed owners/directories and canonical references have been inspected.

Classify every source/hit as canonical owner, accepted amendment, machine realization, active consumer, structural example, derivative index, historical derivation, dormant route, stale reference or downstream obligation.

External research is not presumed necessary. Use only primary/official sources if a specific technical uncertainty cannot be resolved from repository owners; public-HDM legal-conservatism rules apply.

## 8. Required Step-2 evidence products

### 8.1 Primitive admission census

One row for every registry item:

```text
Primitive ID:
Registry/ledger disposition:
Actual supported consumers:
Semantic owners touched:
Current schema/contract realization:
Required now / dormant until / stale-remove:
Activation or removal evidence:
Conflicts and destination:
```

Prove exact equality among registry, admission ledger, contract catalog and compilation schema for every active/dormant item.

### 8.2 Primitive contract matrix

One item-complete row per supported primitive:

```text
Primitive ID and family:
Argument schema and bindings:
Validation phase:
Allowed reads/dependencies/state view:
RNG request/result:
Result and export type:
Prospective outputs:
Allowed mutation owner and transition/event kinds:
Segment/atomicity/commit point:
Failure/hydration behavior:
Suspension/child/currentness behavior:
Retry/idempotency behavior:
Execution bounds:
Receipt/trace evidence:
Catalog-context requirement:
Schema/test realization:
```

Preserve item-level exceptions; do not claim family coverage from one representative primitive.

### 8.3 Binding/read/mutation graph

For each primitive, trace:

```text
Activity parameter/role
-> compiled primitive argument
-> selector/accessor/fact/portable-value input
-> prospective result/transition
-> semantic mutation owner
-> ExecutionSegment commit disposition
-> MechanicalEvent/receipt/trace evidence
-> Continuation/retry retention when applicable
```

The graph must reveal cross-owner conflicts, copied authority, undeclared reads and illegal mutation paths.

### 8.4 Control-flow and child-work matrix

For `for_each_target`, `branch`, `request_choice`, `open_reaction_window`, `schedule_followup` and any other primitive that produces or gates work, record:

- whether it is a primitive, compiler form or unsupported ID;
- exact child/work identity and generation;
- static versus runtime bounds;
- ordering, duplicate and empty-input semantics;
- suspension point and resume cursor;
- pending-child/Continuation ownership;
- cycle/depth/work-budget rejection;
- failure before/after committed segments;
- why it does not create a general workflow/event queue.

Deletion/dormancy/compilation lowering must remain valid results.

### 8.5 RNG and resolution matrix

For `op.roll`, check/save/contest/attack resolution and every indirect RNG consumer:

- request identity, purpose, expression/components and bound roles;
- selector and DC/opposed-input ownership;
- authoritative RNG generation and provenance;
- fixed result retention and retry equality;
- derived result/export versus committed mechanical event;
- unused/rejected/missing/duplicate result behavior;
- suspension interaction;
- prohibition on nested hidden rolls or LLM authoritative results.

### 8.6 Mutation and atomicity matrix

For every state-changing primitive:

- authoritative precondition reads;
- prospective change representation;
- exact owner and legal transition/event kind;
- one or multiple owner records affected;
- segment grouping and all-or-nothing boundary;
- resource cost reservation/commit/refund relationship;
- conflict detection and stale revision behavior;
- failure before commit, during publication and after an earlier committed segment;
- replay/idempotency evidence;
- whether exact domain semantics are current, downstream S6D-08/09 or unsupported.

Do not use generic JSON patch/path/value payloads.

### 8.7 Missing/failure/suspension matrix

Distinguish at least:

- unknown, dormant and stale primitive ID;
- malformed/unknown argument;
- missing required binding or invocation fact;
- hydration required versus invalid/missing reference;
- selector/accessor consumer not permitted;
- incompatible catalog context or stale native revision;
- unavailable target/resource/owner or failed domain precondition;
- RNG missing/duplicate/mismatched;
- child generation/currentness/response conflict;
- execution/cycle/depth/work limit;
- invalid prospective mutation or undeclared owner;
- failure before any commit versus after a prior segment commit;
- suspension requested from a non-suspending primitive;
- unsupported downstream domain semantics.

Map each to existing accepted failure/disposition owners; propose an extension only with evidence that no existing meaning fits.

### 8.8 Verification matrix

Require executable checks for:

- exact 31-item starting census and fresh-current equality;
- ledger/contract/schema bidirectional equality and legal dispositions;
- closed args/results and rejection of unknown fields/IDs;
- Activity step compilation and export-reference type compatibility;
- exact read/consumer permissions and pinned state view;
- exact mutation-owner/transition/event allowlists;
- RNG request/result linkage and retry reuse;
- atomic no-partial-commit behavior;
- choice/reaction/pending-child/Continuation currentness;
- bounded iteration/branching/follow-up and cycle/depth/work rejection;
- missing/hydration/failure mapping;
- dormant items nonselectable and stale items absent;
- no generic query/script/path/patch/file/network capability;
- no independent Signal/StateDelta lifecycle or trusted prospective continuation state;
- direct/transitive schema reference closure;
- representative GAME-domain traces without using prose examples as activation proof;
- synchronized owners, catalogs, schemas, tests, PROJECT_MAP and roadmap.

## 9. Questions Step 2 must answer

1. Which of the 31 registered IDs have current supported consumers, and which are dormant or stale?
2. Is a primitive contract catalog a new owner, a realization of Activity/Step-3 owners, or unnecessary duplication?
3. Which fields are common across primitives and which must remain item-specific?
4. How are Activity step arguments compiled and type-checked against parameters, roles, prior exports and definitions?
5. How are export types known and later references validated without a dynamic type system?
6. Which primitive reads are permitted through S6D-04, and which require new exact consumers rather than broader access?
7. Which primitives are pure calculation, prospective planning, state mutation or child-work orchestration?
8. What exact StateDelta variants, if any, are necessary once primitive mutation contracts are known?
9. Can those variants remain primitive-local prospective values rather than a generic shared schema?
10. What exact Signal variants, if any, have supported consumers?
11. Which transition/event kinds prove each committed primitive outcome?
12. Where is MechanicalEvent structurally realized at the pinned ref?
13. What is the smallest atomic segment for each primitive and multi-step Activity?
14. How do costs commit/refund when validation, suspension, child work or publication fails?
15. Which failures occur at compilation, acceptance, evaluation, commit, publication and resume?
16. Which values must be retained in Continuation, and which must be recomputed from accepted causal inputs?
17. Are `for_each_target` and `branch` runtime primitives or compiler forms?
18. How are iteration, branch depth, child count and follow-up chains bounded?
19. Do choice/reaction primitives suspend the current segment, create pending child work, or lower into existing Step-3 forms?
20. Does `emit_fact` produce invocation context, a MechanicalEvent, a semantic event, trace evidence or an unsupported ambiguity?
21. Does `schedule_followup` own timing, or only request existing Procedure/TemporalBinding infrastructure?
22. Does `advance_local_time` mutate canonical chronology, create a boundary occurrence, or require a downstream domain contract?
23. Which create/update/remove/transform primitives require exact S6D-08/09 semantics before activation?
24. Are any registry IDs too broad and better split, narrowed, dormant or removed?
25. Does any evidence leave a genuine product-semantic/authority/risk decision for the human architect?

## 10. Candidate approaches to evaluate

### A. Item-complete operation-contract catalog with exact owner routing — recommended starting hypothesis

One machine contract row per admitted primitive, with closed schema references and explicit reads/mutations/RNG/atomicity/failure/suspension metadata. Shared family fragments are derived only after item-level evidence.

Benefits: exact accounting, executable compilation checks and visible cross-owner authority.

Risk: catalog volume; must avoid repeating domain laws or Step-3 lifecycle state.

### B. Primitive-specific schema roots without a central contract catalog

Each `op.*` schema owns its exact arguments/results, while tests derive registry equality and common metadata.

Benefit: locally strong shapes.

Risk: cross-cutting read/mutation/failure metadata can drift or become hard to audit.

### C. Small compiler instruction set; lower broad registry IDs into it

Treat some existing IDs as authoring conveniences or stale aliases and lower supported Activities into fewer exact primitives.

Benefit: smaller executor surface.

Risk: changes accepted registry semantics and may require removals/migration decisions; evidence must prove the current broad IDs are not canonical product concepts.

### D. Generic operation envelope with arbitrary args/payload

Rejected default. It is compact but creates a dynamic scripting/mutation surface and cannot prove owner permissions or deterministic failure.

Step 2 must remain able to recommend deletion, dormancy, split, compiler lowering or a hybrid. The recommended starting hypothesis is not pre-approved architecture.

## 11. Agent/human responsibility

The agent owns repository discovery, Source Manifest completeness, per-ID evidence extraction, owner reconciliation, technically forced representation, alternatives, recommendation and executable completeness checks.

Stop for the human architect only if evidence leaves a material choice about supported gameplay semantics, authority, product scope, incompatible accepted owners or explicit risk acceptance. Documentation volume, contract placement, schema synchronization, dormant classification forced by absent consumers and technically necessary failure mapping are not human gates.

## 12. Eight-step loop

1. Architecture Task Brief plus independent whole-project brief critic.
2. Research & Architecture Draft.
3. Decision Brief.
4. Collaborative Review.
5. Candidate Specification.
6. Independent whole-project adversarial solution review.
7. Resolution Gate.
8. Canonicalization and verified publication.

Both critics must independently rebuild the relevant direct and indirect dependency graph through current `DEV/PROJECT_MAP.md`, then read actual owners, schemas, tests, consumers and accepted amendments. Reviewing only the brief or operation registry is invalid.

## 13. Step-1 exit criteria

Step 1 is complete only when:

1. all 31 pinned starting primitive IDs are accounted for without presuming activation;
2. argument/result/read/mutation/RNG/binding/export/atomicity/failure/suspension dimensions are explicit;
3. control-flow, child-work, RNG, mutation and temporal high-risk families have mandatory evidence products;
4. S6D-03/04/05, Step-2 mechanics, Step-3 execution, Step-5 recovery and domain-owner boundaries are explicit;
5. exact catalog/schema/test/GAME discovery routes are named;
6. deletion, dormancy, narrowing and compiler lowering remain valid research results;
7. whole-project critic records checked dependency routes/owners and has zero unresolved BLOCKING/SIGNIFICANT findings;
8. Task Brief, critic, PROJECT_MAP and roadmap are published and verified;
9. roadmap records S6D-06 Step 1 complete / Step 2 next;
10. Step 2 and S6D-07 remain unstarted.

## 14. Full-loop exit criteria

S6D-06 closes only when:

1. registry, admission ledger, contract catalog/schema and tests account exactly for every primitive;
2. every supported primitive has one exact machine contract and owner route;
3. every dormant primitive is nonselectable with an exact activation trigger, and every stale ID is removed;
4. Activity compilation rejects unknown/invalid args, bindings, exports, reads and operations;
5. RNG authority/retry identity is exact;
6. mutation owners, transitions/events and segment atomicity are exact;
7. failure/suspension/idempotency/recovery semantics are exact;
8. control-flow and produced-work bounds prevent recursion/workflow-engine creep;
9. Signal/StateDelta activate only exact necessary variants without lifecycle duplication;
10. no generic scripting/query/path/patch/file/network capability exists;
11. no accepted upstream/domain owner is duplicated or contradicted;
12. focused verification and maintenance checks pass;
13. adversarial whole-project critic has zero unresolved BLOCKING/SIGNIFICANT findings;
14. architecture, catalogs, schemas, tests, PROJECT_MAP and roadmap are synchronized;
15. S6D-07 Step 1 is next but not started.

## 15. Stop boundary

After brief criticism:

- repair every BLOCKING/SIGNIFICANT framing issue;
- publish only this Task Brief, its critic and minimal PROJECT_MAP/roadmap routing;
- verify exact remote HEAD and content;
- stop before Step 2.

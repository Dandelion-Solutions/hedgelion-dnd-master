# S6D-05 — Activity Parameters, Targeting, Costs and Portable Protocol Values — Architecture Task Brief

Status: **STEP 1 COMPLETE — WHOLE-PROJECT BRIEF CRITIC PASS — STEP 2 NOT STARTED**

Date: 2026-08-25
Authoritative branch: `v1/engine-rearchitecture`
Pinned Step-1 remote ref: `5a8d2c9ff8af2ab1296674c9ef5333a44a8900f2`
Predecessor: S6D-04 complete and canonically owned by `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`

## 1. Assignment

Execute only Step 1 of the S6D-05 eight-step design loop.

Frame the evidence and decision work required to finalize exact reusable embedded value contracts used by supported Activities and execution protocols:

- `TargetSpec`;
- `AreaSpec`;
- `CostSpec`;
- `DurationSpec`;
- Activity parameter declarations and invocation bindings;
- `RollRequest` / `RollResult`;
- Choice and Reaction portable payloads;
- Signal and StateDelta dispositions.

After whole-project brief criticism, publish the Task Brief, critic and minimal routing/status updates, verify the remote branch, and stop. Do not begin Step 2 or S6D-06.

## 2. Problem

The repository already contains accepted semantic owners and multiple schemas for these values, but registration, embedding, ownership and cross-protocol equality are not yet proven item-complete as one portable contract surface.

S6D-05 must prevent five failure modes:

1. the same value means different things in Activity definitions, ActionRequest, Resolution, Continuation and receipts;
2. embedded values accidentally become independent record/authority classes;
3. LLM/adjudicated bindings inject engine-owned state or bypass target/cost legality;
4. suspension/retry/reconstruction loses identity, provenance or already-authoritative rolls/choices;
5. a generic “flexible payload” becomes an unbounded query/expression/mutation channel.

This is an architecture and machine-contract closure task, not primitive implementation or seed authoring.

## 3. Goal

Produce an evidence-backed candidate that can eventually prove:

1. every required portable value has one semantic owner and one exact schema realization route;
2. every embedding site uses that contract without copying or weakening it;
3. definition-time declarations and invocation-time bindings are distinct and type-compatible;
4. target, area, cost and duration values preserve D&D semantics without encoding arbitrary executable logic;
5. rolls preserve RNG authority, formula/request identity and result provenance across retries;
6. Choice and Reaction payloads preserve eligibility, option/offer identity, responder authority, deadline/suspension and resume semantics;
7. Signal and StateDelta dispositions distinguish requests, accepted effects, rejected/ignored outcomes and committed mutation evidence;
8. no embedded value becomes an independent canonical record class;
9. S6D-04 fact/accessor authority and Step-3 execution/recovery identities remain intact;
10. all catalog/schema/test/owner contradictions are closed or routed to the exact downstream owner.

## 4. In scope

### 4.1 Value families

- exact fields, types, invariants and discriminators for all named S6D-05 families;
- stable identity needs inside a Resolution/Continuation generation;
- definition-owned versus invocation-owned fields;
- optionality, absence, null and empty collection semantics;
- canonical unit/enum/value vocabulary and normalization boundaries;
- serialization, validation and round-trip requirements;
- nested ownership and reference-versus-copy rules.

### 4.2 Activity declarations and bindings

- Activity parameter declaration identity/type/cardinality/default/requiredness;
- invocation binding source, actor/source/target roles and provenance;
- richer House-Rules adjudicated parameter bindings;
- validation before deterministic execution;
- frozen accepted bindings across suspension/retry;
- prohibition on treating arbitrary prose as a typed mechanical value.

### 4.3 Protocol embeddings

- Activity definition;
- ActionRequest and accepted RuntimeCommand/IntentPlan equivalents actually present;
- Resolution and Continuation;
- pending choice/reaction child work;
- execution segments and receipts;
- event/signal/follow-up paths;
- checkpoint/recovery and reconstruction where values remain live.

### 4.4 Machine closure

- current core-catalog portable value vocabulary;
- every schema branch and `$ref`;
- every test/example;
- exact equality/inclusion checks among owners, registries and schemas;
- dormant/embedded/nonowner disposition where no supported consumer exists.

## 5. Out of scope

- Activity primitive reads/mutations/atomicity/failure contracts (S6D-06);
- authoring seed Activities, spells, equipment or monsters (S6D-07–09);
- selecting gameplay balance, ranges, costs, durations or targets for individual seed definitions;
- valued-Condition aggregation (S6D-08);
- generic query, expression, scripting or arbitrary JSON payload languages;
- runtime executor/compiler implementation;
- new top-level record classes for embedded values;
- new scheduler/timer authority;
- reopening S6D-01–04 without a concrete contradiction.

## 6. Inherited invariants

1. Portable values are embedded typed values, not independent records or mutable authority.
2. Definition identity is referenced; authoritative world/runtime state is not copied into requests.
3. The LLM supplies intent and permitted adjudicated bindings, not engine-owned mechanical state.
4. Missing invocation fact is not false; richer adjudication uses declared Activity parameters rather than widening boolean facts.
5. One accepted invocation generation freezes causal inputs required for deterministic resume.
6. Authoritative rolls are generated once, retained and never rerolled on retry.
7. Continuation stores only the minimum accepted work needed for deterministic resumption.
8. Every embedded reference resolves through the pinned compatible `ResolvedCatalogContext`.
9. MechanicalContext/accessor/fact/query boundaries from S6D-04 remain unchanged.
10. BoundaryOccurrence is optional contextual identity only for work that actually originates at a boundary.
11. Runtime queries remain infrastructure-only and nonserializable.
12. Definition schemas are structural unless catalog-aware compilation proves admission.
13. Absence, empty, zero, false, “none” and “not yet chosen” are distinct where semantics differ.
14. Costs are declarations/commit obligations, not permission to mutate arbitrary owners.
15. StateDelta is evidence/instruction inside the owning Resolution protocol, not a second state store.
16. Signals describe closed registered occurrences/dispositions; they do not grant handler discovery or mutation authority.
17. Reaction and Choice payloads cannot self-authorize eligibility or responder identity.
18. Human decisions are required only for material supported semantics/scope/authority/risk, not deterministic representation consequences.

## 7. Current machine baseline

The current authoritative tree contains at least these exact schema owners:

- `DEV/SCHEMAS/activity-definition-data.schema.json`;
- `DEV/SCHEMAS/activity-parameter-binding.schema.json`;
- `DEV/SCHEMAS/target-spec.schema.json`;
- `DEV/SCHEMAS/area-spec.schema.json`;
- `DEV/SCHEMAS/cost-spec.schema.json`;
- `DEV/SCHEMAS/duration-spec.schema.json`;
- `DEV/SCHEMAS/roll-request.schema.json`;
- `DEV/SCHEMAS/roll-result.schema.json`;
- `DEV/SCHEMAS/choice-request.schema.json`;
- `DEV/SCHEMAS/action-request.schema.json`;
- `DEV/SCHEMAS/runtime-resolution-state.schema.json`;
- `DEV/SCHEMAS/runtime-continuation-state.schema.json`;
- `DEV/SCHEMAS/resolution-receipt.schema.json`.

The absence of standalone files named for Reaction, Signal or StateDelta is not evidence that their contracts are absent. Step 2 must locate their actual branches/owners and decide whether the current embedding is canonical, incomplete, stale or downstream. It must not create files merely to match conceptual names.

## 8. Mandatory Source Manifest

Step 2 begins from a fresh remote ref and records authority role, applicability and supersession for every source.

### 8.1 Process and sequence

- `AGENTS.md`;
- both design-process owners;
- `DEV/PROJECT_MAP.md`;
- current roadmap;
- S6D owner decision, parent Task Brief and plan;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` and `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-canonicalization.md`;
- `DEV/ARCHITECTURE/CATALOG_ADMISSION.md` and `DEV/docs/superpowers/specs/2026-08-25-s6d-02-catalog-admission-gap-closure-canonicalization.md`;
- `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md` and `DEV/docs/superpowers/specs/2026-08-25-s6d-03-complete-calculation-selector-metadata-canonicalization.md`;
- `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md` and `DEV/docs/superpowers/specs/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-canonicalization.md`.

### 8.2 Semantic owners

- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`;
- `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`;
- `DEV/ARCHITECTURE/ACTOR_MODEL.md`, `DEV/ARCHITECTURE/ASSET_MODEL.md` and `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`;
- `DEV/CATALOG/entity-structures.json`, `DEV/SCHEMAS/condition-definition-data.schema.json` and `DEV/SCHEMAS/effect-definition-data.schema.json` as the current exact Resource/Effect/Condition/LifeState structural routes;
- `DEV/SCHEMAS/duration-spec.schema.json` and `DEV/SCHEMAS/temporal-binding.schema.json` as the definition-duration/concrete-time boundary;
- `GAME/CORE/RUNTIME.md`, `GAME/CORE/MECHANICS_INTEGRITY.md`, `GAME/CORE/RANDOMNESS.md`, `GAME/CORE/ADJUDICATION.md`, `GAME/CORE/COMBAT.md`, `GAME/CORE/MAGIC.md`, `GAME/CORE/EXPLORATION.md` and `GAME/CORE/CHARACTER_READINESS.md`;
- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`, `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md` and `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md`.

### 8.3 Execution and recovery owners

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` and `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-resolution-gate.md`;
- `DEV/SCHEMAS/runtime-resolution-state.schema.json`, `runtime-continuation-state.schema.json`, `execution-segment.schema.json`, `pending-child-invocation.schema.json`, `invocation-fact.schema.json`, `resolution-receipt.schema.json` and `boundary-occurrence.schema.json`;
- `DEV/TESTS/test_step3_execution_owner_contract.py`, `test_step3_resume_ordering_contract.py`, `test_step3_execution_value_schemas.py`, `test_step3_execution_examples.py`, `test_step3_event_followup_contract.py` and `test_step3_execution_catalog_contract.py`.

For each source, state whether it owns identity, authority, retention, idempotency, mutation evidence, currentness, reachability or failure disposition.

### 8.4 Machine and verification surfaces

- `DEV/CATALOG/core-catalog.json`, `catalog-admission-ledger.json`, `mechanical-surfaces.json` and `entity-structures.json`;
- every exact schema listed in §7 plus `temporal-binding.schema.json`, `execution-segment.schema.json`, `pending-child-invocation.schema.json`, `invocation-fact.schema.json`, `boundary-occurrence.schema.json`, `mechanical-accessor-ref.schema.json`, `mechanical-predicate.schema.json` and `mechanical-surfaces.schema.json`;
- `DEV/TESTS/test_s6d_02_catalog_admission_contract.py`, `test_s6d_03_selector_metadata_contract.py`, `test_s6d_04_mechanical_context_contract.py`, `test_step2_evaluation_input_contract.py`, `test_step2_condition_applicability.py`, `test_step3_execution_value_schemas.py` and `test_house_rules_adjudicated_input_contract.py`;
- repository-wide direct/transitive `$ref` and discriminator searches, used only after the explicit anchors above;
- catalog/schema maintenance and release validation.

### 8.5 Discovery rule

Search by semantic field/discriminator and `$ref`, not filename alone. Classify each hit as canonical owner, machine realization, supported consumer, structural example, derivative, historical, stale or downstream obligation.

A schema example is not proof of current supported activation.

## 9. Required Step-2 evidence products

### 9.1 Portable-value registry census

For every relevant core-catalog `protocol_value_kinds`, targeting/range/area/duration/signal/disposition ID:

```text
Registry family / ID:
Semantic owner:
Machine owner:
Current disposition:
Exact schema branch:
Embedding consumers:
Supported-profile evidence:
Duplicate/overlap:
Decision destination:
```

Prove bidirectional equality where a registry claims exhaustive ownership.

### 9.2 Value-family ledger

One row per concrete value/discriminator:

```text
Value/discriminator:
Embedded owner:
Definition-time or invocation/runtime:
Required/optional fields:
Identity and reference fields:
Scalar/enums/units:
Absence/null/empty semantics:
Authority/provenance:
Validation phase:
Mutation authority (normally none):
Retention/retry behavior:
Allowed embedding sites:
Schema/test realization:
Disposition/downstream trigger:
Conflicts:
```

### 9.3 Declaration-binding compatibility matrix

Rows: every Activity parameter declaration kind.
Columns:

- allowed binding source;
- binding schema branch;
- exact type compatibility;
- cardinality;
- default legality and evaluation time;
- actor/source/target/choice/adjudicated authority;
- missing/invalid behavior;
- freeze/retry behavior;
- House-Rules eligibility;
- seed consumer evidence.

A binding cannot change declared type, inject undeclared fields or reinterpret engine state as adjudication.

### 9.4 Targeting and area matrix

For `TargetSpec` / `AreaSpec`:

- target kind, count/cardinality and self/source inclusion;
- range mode and units;
- point/origin/direction/shape relationships;
- creature/object/location/area roles;
- selection versus affected-set ownership;
- line-of-effect/visibility/reachability division between engine reads and adjudication;
- deterministic ordering or unordered-set semantics;
- empty/no-target behavior;
- binding and validation phase;
- downstream primitive needs without defining primitive behavior.

Do not embed world searches, geometric query languages or copied target state.

### 9.5 Cost and duration matrix

For every Cost/Duration discriminator:

- declared value and units;
- payer/owner binding;
- availability check versus reservation/commit/refund owner;
- zero/free/absent semantics;
- multiple-cost atomicity obligation routed to S6D-06/Step 3;
- fixed/instant/until/boundary/temporal variants;
- TemporalBinding and scheduled work relationship;
- concentration/recovery relationships routed to S6D-08/09;
- serializability and retry identity.

### 9.6 Roll contract ledger

For every RollRequest/Result variant:

- request identity and formula/components;
- roller/subject/target binding;
- RNG authority and generation point;
- advantage/disadvantage or equivalent normalized input;
- DC/opposed-roll ownership;
- raw dice, total and outcome separation;
- authoritative result provenance;
- reuse across retry/resume;
- receipt/trace embedding;
- rejected/unused roll handling;
- absence of LLM-supplied authoritative random results.

### 9.7 Choice and Reaction ledger

Distinguish ordinary Choice from Reaction:

- request/offer ID;
- parent Resolution and generation;
- eligible responder;
- option/offer identities;
- payload/value schemas;
- visibility and information frontier;
- deadline/decline/timeout/cancel semantics;
- pending-child/Continuation link;
- validation/currentness on resume;
- idempotency and duplicate response;
- accepted/rejected/expired dispositions;
- whether result is embedded evidence or a new authoritative record.

Do not collapse reactions into generic choices if timing/responder/currentness differs.

### 9.8 Signal and StateDelta disposition ledger

For each actual branch/discriminator:

- producer and acceptance authority;
- registered kind/disposition owner;
- causal parent/segment identity;
- payload schema;
- target/owner binding;
- proposed/applied/rejected/ignored/superseded semantics as actually supported;
- commit boundary;
- trace/receipt representation;
- retry/replay behavior;
- event/follow-up relationship;
- proof that StateDelta is not restored/cached as an independent authority.

Do not invent a universal event bus or mutation DSL.

### 9.9 Embedding/equality graph

Build a graph from each semantic value owner to every `$ref`, inline copy and protocol consumer. Prove:

- one canonical shape per semantic value;
- no weaker inline duplicate;
- no circular schema authority;
- compatible requiredness across request/resolution/continuation/receipt;
- portable identity survives every suspension/recovery route that needs it;
- embedded values never appear in world/runtime record-kind registries unless a separate accepted owner proves record status.

### 9.10 Missing/failure matrix

Distinguish at least:

- required parameter absent;
- optional parameter absent;
- explicit false/zero/empty;
- unknown declaration/binding/option/offer/value kind;
- type/cardinality mismatch;
- invalid target/range/area;
- unavailable/unpayable cost;
- stale responder/choice/reaction generation;
- missing authoritative roll;
- duplicate/replayed response;
- unsupported/dormant discriminator;
- incompatible catalog context;
- stale native revision;
- invalid StateDelta owner/mutation;
- absent boundary context where not required versus required.

Map to existing Step-3 dispositions/failures; do not mint parallel codes without evidence.

### 9.11 Verification matrix

Require executable checks for:

- registry/schema exactness and no duplicate owner;
- all direct/transitive `$ref` resolution;
- declaration-binding compatibility;
- target/area discriminator completeness and illegal combinations;
- cost/duration discriminator completeness;
- roll request/result linkage, one authoritative generation and retry reuse;
- Choice/Reaction generation/responder/option/currentness;
- Signal/StateDelta kind/disposition and owner legality;
- false/zero/empty/missing distinctions;
- catalog-context pinning;
- Continuation/receipt round-trip preservation;
- no independent record class for embedded values;
- no arbitrary query/expression/path/mutation payload;
- structural examples labeled non-authoritative;
- dormant IDs nonselectable;
- affected owner/schema/catalog/test synchronization.

## 10. Questions Step 2 must answer

1. What is the exact current registry census for all S6D-05 value and disposition IDs?
2. Which conceptual values already have a canonical schema and which are inline branches?
3. Are any inline branches weaker or divergent copies?
4. Which values need stable IDs versus only parent-relative position?
5. Which fields belong to definitions, requests, accepted work, results and receipts?
6. How is Activity parameter type compatibility expressed without a universal dynamic type system?
7. When may a default be resolved, and can exposure to later fiction change it?
8. Which adjudicated parameter kinds are richer than boolean facts and how is their authority bounded?
9. Are target selection and affected-target derivation distinct values?
10. What ordering, duplicate and empty-set semantics exist for targets?
11. Which geometry belongs in AreaSpec versus runtime geometry/query infrastructure?
12. Does CostSpec describe declaration, reservation, commitment, payment evidence or more than one with distinct discriminators?
13. Which owner handles refund/rollback across failed atomic segments?
14. How do DurationSpec and TemporalBinding divide definition intent from concrete scheduled identity?
15. Which roll fields are inputs, authoritative outputs and derived presentation?
16. How are opposed/compound rolls represented without recursion or hidden execution?
17. Are Choice and Reaction currently distinct enough in schemas and Step-3 state?
18. What exact values must survive suspension, retry and reconstruction?
19. Where do Signal and StateDelta branches actually live?
20. Are their dispositions IDs, enums or duplicated prose?
21. Can any payload authorize mutation outside the owning primitive/Resolution?
22. Do receipts preserve sufficient evidence without becoming authority?
23. Which registered values are active, dormant, embedded nonowners or stale?
24. Which gaps are S6D-05 technical closure versus S6D-06 primitive semantics or S6D-07–09 seed activation?
25. Does any finding create a genuine human product decision?

## 11. Candidate approaches to evaluate

### A. Item-complete canonical embedded-value family — recommended

One semantic contract per value family, shared through exact schema references; inline branches allowed only when they are the canonical branch under one owner. Registry and embedding equality are executable.

Benefits: deterministic, auditable, minimizes duplicate authority.

Risk: requires broad schema/reference reconciliation.

### B. Protocol-local value copies

Each request/resolution/receipt owns its own similar shape.

Benefit: local convenience.

Rejected default: drift, weakened validation and retry mismatch are likely.

### C. One universal tagged payload

All values use a generic kind + arbitrary payload envelope.

Benefit: fewer schemas.

Rejected default: becomes a dynamic type/query/mutation language and loses bounded authority.

### D. Promote values to records

Give targets/costs/rolls/choices/deltas independent record classes.

Rejected: contradicts the parent S6D-05 boundary unless an existing accepted owner proves independent lifecycle/authority.

Step 2 may refine alternatives, but must not silently select a materially different product semantics.

## 12. Agent/human responsibility

The agent owns:

- discovery and exact Source Manifest;
- field/discriminator/registry/`$ref` census;
- owner reconciliation and supersession;
- evidence-preserving ledgers and matrices;
- technical representation consequences;
- alternatives and recommendation;
- testable completeness and boundary enforcement.

Stop for the human architect only when evidence leaves a material choice about supported gameplay semantics, authority, product scope or explicit risk acceptance. Documentation volume, naming cleanup, schema placement and technically forced synchronization are not human gates.

## 13. Eight-step loop

1. Task Brief plus independent whole-project brief critic.
2. Research & Architecture Draft.
3. Decision Brief.
4. Collaborative Review.
5. Candidate Specification.
6. Independent whole-project adversarial solution review.
7. Resolution Gate.
8. Canonicalization and verified publication.

Both critics must reconstruct the full direct and indirect dependency graph through PROJECT_MAP, locate current owners and inspect pre-existing rules. Local-only schema review is insufficient.

## 14. Step-1 exit criteria

Step 1 is complete only when:

1. all named S6D-05 value families are in scope without assuming standalone files;
2. exact known schema owners and mandatory discovery routes are named;
3. Activity declaration/binding, targeting/area, cost/duration, rolls, Choice/Reaction and Signal/StateDelta evidence products are mandatory;
4. definition/request/resolution/continuation/receipt/recovery relationships are explicit;
5. embedded-value versus independent-record authority is explicit;
6. S6D-04/06/07–09 and House-Rules boundaries are explicit;
7. whole-project critic has zero unresolved BLOCKING/SIGNIFICANT;
8. brief/critic/PROJECT_MAP/roadmap are published and verified;
9. roadmap records S6D-05 Step 1 complete / Step 2 next;
10. Step 2 and S6D-06 remain unstarted.

## 15. Full-loop exit criteria

S6D-05 closes only when:

1. every registry/value/disposition item has a supported/dormant/embedded/stale disposition;
2. every semantic value has one owner and exact machine realization;
3. all embedding sites share or prove equality with that realization;
4. declaration/binding compatibility is complete;
5. target/area/cost/duration contracts are exact and bounded;
6. roll authority, identity, provenance and retry reuse are exact;
7. Choice/Reaction identities, responders, dispositions and resume behavior are exact;
8. Signal/StateDelta kinds, ownership, mutation boundary and evidence are exact;
9. missing/false/zero/empty/absent/stale behaviors are exact;
10. embedded values remain nonrecords and nonauthority;
11. no query/expression/mutation DSL appears;
12. Step-3/5 recovery and S6D-01 catalog identity are preserved;
13. S6D-04 fact/accessor boundaries remain preserved;
14. focused verification and maintenance audit pass;
15. adversarial critic has zero unresolved BLOCKING/SIGNIFICANT;
16. canonical owners, catalogs, schemas, tests, PROJECT_MAP and roadmap are synchronized;
17. S6D-06 Step 1 is next but not started.

## 16. Stop boundary

After brief criticism:

- repair every BLOCKING/SIGNIFICANT framing issue;
- publish only this Task Brief, its critic and minimal PROJECT_MAP/roadmap routing;
- verify exact remote HEAD and content;
- stop before Step 2.


# S6D-10 — Campaign Rulings / House-Rule Mechanical Boundary Integration — Architecture Task Brief

Status: **STEP 1 TASK BRIEF — WHOLE-PROJECT BRIEF-CRITIC PASS**

Date: 2026-08-27

## 1. Purpose and stage boundary

S6D-10 consumes the already approved Campaign House Rules/Rulings architecture and proves that every currently supported policy/adjudication entry into the S6D mechanical surface preserves the accepted authority split:

```text
eligible fiction + current admitted policy
    -> bounded LLM/Master semantic judgment
    -> authorized typed accepted input or typed realization reference
    -> current catalog/consumer/native-owner validation
    -> deterministic Resolution / RNG / owner mutation-or-no-mutation / evidence
```

The loop is an integration and conformance closure. It is not permission to reopen House-Rules product semantics, create a general policy engine, compile natural language into rules, broaden the supported D&D corpus, or give prose/LLM execution authority.

This artifact is Step 1 only. It frames Steps 2–8 after human approval. It does not perform the integration proof, change machine contracts, begin S6D-11/12, resume R2.7, or implement production runtime behavior.

## 2. Established decision baseline

The following are settled inputs, not open questions unless fresh owning evidence proves a contradiction or an insufficient current consumer contract:

1. House Rules is a campaign-persistent LLM-interpreted adjudication-policy layer, not a deterministic rules owner.
2. A lawful Master may make the smallest bounded one-off situational ruling needed for current play without first publishing campaign-wide policy.
3. Accepted one-off adjudication may enter mechanics only through a declared typed receiving surface. Engine-owned state, capability, legality, RNG and canonical mutation cannot be supplied as adjudication authority.
4. Registered `INVOCATION_ADJUDICATED` context facts remain boolean. Richer accepted values use declared Activity parameters whose closed value/cardinality/bounds are validated against the exact Activity declaration.
5. Accepted adjudicated inputs are causal evidence frozen with the accepted Resolution generation across retry, suspension, recovery and later policy publication.
6. Durable policy adoption is distinct from live adjudication. In multiplayer every current active PLAYER may adopt `INTERPRETIVE_POLICY`; `MECHANICAL_OVERRIDE_POLICY` requires campaign creator authority or a current active PLAYER with the explicit creator-issued grant. Singleplayer publication remains creator-only.
7. Normative policy lives in `RULES/HOUSE_RULES.md`; `RULES/HOUSE_RULES.yaml` is narrow identity/currentness/adoption/routing/realization evidence and never an executable semantic owner.
8. Formalizable policy may reference existing admitted typed capabilities through `realization_refs`. Mention is linkage only; catalog identity/currentness, exact consumer admission, deterministic validation and native-owner authority still apply.
9. Mechanically material policy whose required realization is absent, stale or incompatible stops at a finite policy-realization gap/mismatch boundary. It never falls back to stale baseline behavior or prose mutation.
10. Contextual policy may remain LLM-native indefinitely when its mechanical consequence is fully expressed by an existing bounded typed adjudication route.
11. Later policy publication is forward-looking. It does not replay RNG, reinterpret already accepted Resolution generations or rewrite committed facts.
12. No generic Signal/StateDelta lifecycle, arbitrary payload, expression/query language, background scheduler, policy frontier, notification queue or campaign scan follows from this domain.

The investigation must first classify any apparent conflict as confirmation, extension, contradiction, new consumer or insufficiency. Keyword overlap does not reopen a closed owner.

## 3. Exact S6D-10 question

The loop must determine whether the current House-Rules surfaces and the current S6D-01…09 machine contracts form a complete, non-duplicating bridge for all supported consumers.

Two routes must be proved separately.

### Route A — one-off/contextual adjudication

```text
eligible current fiction/state/policy basis
-> Master semantic judgment
-> exact declared INVOCATION_ADJUDICATED fact or parameter binding
-> binding/fact authorization + bounds + provenance + currentness validation
-> accepted Resolution generation freezes the causal input
-> deterministic exact consumer
-> native-owner mutation or honest Mechanical-Null result
-> canonical event/receipt/retry/recovery evidence owned by existing contracts
```

### Route B — durable reusable policy

```text
authorized policy adoption/publication
-> exact current Markdown + sidecar policy revision
-> applicability/conflict/currentness validation
-> contextual portion may supply only Route-A typed inputs
-> formalizable portion resolves declared realization_refs
-> selected current ResolvedCatalogContext + exact capability/consumer validation
-> same deterministic execution/native-owner boundary
-> finite conflict/realization-gap failure when the chain is incomplete
```

The result may legitimately conclude that current contracts already satisfy all required routes and only need stronger integration tests/traceability. It may also remove or narrow an unnecessary S6D-local abstraction. It must not manufacture a new record, lifecycle or subsystem merely to make S6D-10 look substantive.

## 4. Mandatory current Source Manifest and dependency route

The Step-2 investigation and both critics must fresh-read the authoritative remote ref and reconstruct the complete direct-and-indirect dependency subgraph through `DEV/PROJECT_MAP.md`. At minimum the Source Manifest must classify and inspect:

### 4.1 Process, sequencing and inherited S6D obligation

- `AGENTS.md`;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- the S6D owner decision, umbrella Task Brief and execution plan;
- the paused R2.7 WP-06 cursor as routing/history only where the current roadmap supersedes it.

### 4.2 Current House-Rules owners and accepted decision chain

- **canonical owner:** `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`;
- **research/assurance, non-owner:** `DEV/docs/superpowers/research/2026-08-25-campaign-house-rules-step-2-auditor-reopen-evidence-delta.md`;
- **decision framing:** `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-decision-brief-amended.md`;
- **explicit human owner decision:** `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md`;
- **collaborative/candidate/adversarial/resolution assurance:** `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-4-collaborative-review-v2.md`, `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-5-candidate-spec-v2.md`, `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-6-adversarial-review-v2.md` and `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-7-resolution-gate-v2.md`;
- **current closure/supersession record:** `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md`;
- **authority/runtime owners:** `DEV/ARCHITECTURE/ACCESS_CONTROL.md` and `GAME/CORE/ADJUDICATION.md`;
- **shipped normative/companion surfaces:** `GAME/CAMPAIGN/RULES/HOUSE_RULES.md` and `GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml`;
- **machine schemas:** `GAME/SCHEMA/house_rules_policy.schema.yaml`, `GAME/SCHEMA/player.schema.yaml`, `GAME/SCHEMA/campaign_manifest.schema.yaml` and `GAME/SCHEMA/session.schema.yaml`;
- **focused tests:** `DEV/TESTS/test_house_rules_adjudicated_input_contract.py` and `DEV/TESTS/test_house_rules_policy_authority_contract.py`.

### 4.3 Information eligibility, currentness, publication and recovery owners

- **base truth/knowledge/role-context canonical owner:** `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`;
- **current one-physical-chat amendment:** `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`;
- **Context Runtime canonical owner and human decision:** `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` and `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-owner-decision.md`;
- **single-context LLM/instruction canonical owner and human decision:** `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` and `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-owner-decision.md`;
- **campaign publication canonical owner:** `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`;
- **recovery canonical owner:** `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`;
- **multiplayer currentness/live ownership canonical owner:** `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`;
- **integrated Step-5 assurance/closure:** `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`;
- **runtime owners/consumers:** `GAME/CORE/RUNTIME.md`, `GAME/CORE/PERSISTENCE.md`, `GAME/CORE/DURABILITY_GUARD.md`, `GAME/CORE/SAVE_CONTRACT.md`, `GAME/CORE/MULTIPLAYER.md`, `GAME/CORE/LIVE_SCENE.md`, `GAME/CORE/SESSION.md`, `GAME/CORE/INFORMATION.md`, `GAME/CORE/AI_REASONING.md` and `GAME/CORE/RANDOMNESS.md`;
- **persistent schemas:** `GAME/SCHEMA/checkpoint.schema.yaml`, `GAME/SCHEMA/current_state.schema.yaml`, `GAME/SCHEMA/session.schema.yaml` and `GAME/SCHEMA/live_scene.schema.yaml`.

The investigation must verify that policy text is both eligible data for the exact semantic consumer and below constitutional/instruction authority. Physical visibility in the shared chat is not semantic eligibility.

### 4.4 Deterministic mechanics and current S6D machine owners

- `RULESET_PACKAGE_IDENTITY.md`, `CATALOG_RESOLUTION.md`, `CATALOG_ADMISSION.md` and selected-package identity/capability evidence;
- `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, `CALCULATION_SELECTOR_METADATA.md`, `MECHANICAL_CONTEXT.md`, `PORTABLE_ACTIVITY_VALUES.md`, `ACTIVITY_PRIMITIVE_CONTRACTS.md`, `CHARACTER_PROGRESSION_READY_PC_SEED.md`, `HEALTH_EFFECTS_RECOVERY.md` and `DOMAIN_RULES_COVERAGE.md`;
- exact S6D-01…09 machine catalogs, package members, schemas, validators and focused tests implicated by adjudicated input or policy realization;
- **Step-3 canonical/assurance:** `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` and `DEV/docs/superpowers/specs/2026-08-19-step-3-final-critical-review.md`;
- **Step-3 accepted-work schemas:** `DEV/SCHEMAS/action-request.schema.json`, `DEV/SCHEMAS/runtime-command-state.schema.json`, `DEV/SCHEMAS/runtime-resolution-state.schema.json`, `DEV/SCHEMAS/runtime-continuation-state.schema.json`, `DEV/SCHEMAS/execution-segment.schema.json` and `DEV/SCHEMAS/resolution-receipt.schema.json`, plus the exact typed MechanicalEvent schema selected by each concrete route;
- **Step-3 focused tests:** `DEV/TESTS/test_step3_command_intent_contract.py`, `DEV/TESTS/test_step3_execution_owner_contract.py`, `DEV/TESTS/test_step3_execution_value_schemas.py`, `DEV/TESTS/test_step3_resume_ordering_contract.py` and `DEV/TESTS/test_step3_event_followup_contract.py`;
- the exact Step-5 canonical and runtime surfaces enumerated in §4.3 for retry, durability, publication, currentness and recovery.

For S6D-09 in particular, the Source Manifest must read supersession in the correct order before deriving active adjudicated consumers:

1. **Decision C human owner:** `DEV/docs/superpowers/specs/2026-08-27-s6d-09-domain-rules-coverage-matrix-owner-decision.md`;
2. **earlier derivation:** `DEV/docs/superpowers/specs/2026-08-27-s6d-09-domain-rules-coverage-matrix-collaborative-review.md` and `DEV/docs/superpowers/specs/2026-08-27-s6d-09-domain-rules-coverage-matrix-candidate-spec.md`;
3. **later narrow spatial repair:** `DEV/docs/superpowers/specs/2026-08-27-s6d-09-spatial-conformance-repair-step-6-review.md`, `DEV/docs/superpowers/specs/2026-08-27-s6d-09-spatial-conformance-repair-step-7-resolution-gate.md` and `DEV/docs/superpowers/specs/2026-08-27-s6d-09-spatial-conformance-repair-step-8-canonicalization.md`;
4. **current canonical owner:** `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md`.

Where the earlier collaborative/candidate artifacts say a spatial fact remains dormant, the later repair and current canonical owner supersede that derivation for the seven exact admitted consumers.

The exact current spatial/adjudicated machine route includes `DEV/CATALOG/mechanical-surfaces.json`, `DEV/CATALOG/domain-rules-coverage.json`, `DEV/CATALOG/activity-primitive-contracts.json`, `DEV/CATALOG/catalog-admission-ledger.json`, `DEV/SCHEMAS/invocation-fact.schema.json`, `DEV/SCHEMAS/target-spec.schema.json`, `DEV/SCHEMAS/area-spec.schema.json`, `DEV/SCHEMAS/gameplay-spine-seed.schema.json`, `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json`, `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/gameplay-spine-seed.json`, `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-capabilities.json`, `DEV/TOOLS/validate_domain_rules_coverage.py` and `DEV/TESTS/test_s6d_09_domain_rules_coverage_contract.py`.

### 4.5 Exact active adjudicated consumers

Step 2 must derive these from current machine/package sources rather than from this brief. The initial known set includes:

- richer bounded DC bindings for the current generic check/save Activities;
- the exact admitted `fiction.target_reachable` boolean consumers established by the S6D-09 spatial repair;
- any other active admitted `INVOCATION_ADJUDICATED` parameter/fact consumer discovered by registry/package/consumer equality.

Every active fact and parameter consumer must enter the ledger. Every ledger consumer must resolve back to an active admitted exact package definition and machine contract. Dormant facts, quarantined primitives, conformance-only fixtures and descriptive examples remain nonselectable unless their own owner gate is separately passed.

Routing indexes, roadmaps, source summaries and prior-chat memory are locators only. Correctness-sensitive conclusions must cite actual owning artifacts and preserve qualifiers, negative findings, defer/revisit triggers and supersession.

## 5. Required evidence products

### 5.1 Boundary inventory and bidirectional equality

Construct finite source sets from current owners:

```text
ACTIVE_ADJUDICATED_CONSUMER_KEYS
    = every active exact consumer -> declared INVOCATION_ADJUDICATED parameter/fact edge

CURRENT_SUPPORTED_POLICY_REALIZATION_KEYS
    = exact current policy-realization edges proven by adopted current campaign policy
      plus identity-bound admitted package/current-consumer evidence

CONFORMANCE_ONLY_POLICY_REALIZATION_PROOF_KEYS
    = synthetic fixture-only realization edges used solely to prove contract shape,
      rejection and negative behavior

HOUSE_RULE_BOUNDARY_LEDGER_KEYS
    = every active adjudicated-consumer edge
      union every CURRENT_SUPPORTED_POLICY_REALIZATION edge
      union every explicit House-Rules mechanical-boundary obligation
```

The final ledger must prove both directions: every source edge has exactly one disposition/route; every ledger edge originates in a current source; every reference resolves through current identity/admission/consumer validation; and no dormant/quarantined item gains activation by appearing in the ledger.

`CONFORMANCE_ONLY_POLICY_REALIZATION_PROOF_KEYS` never enter the current supported set or `HOUSE_RULE_BOUNDARY_LEDGER_KEYS`. They are dispositioned separately as `CONFORMANCE_ONLY_NONSELECTABLE` and prove only contract shape and negative behavior. If the current empty campaign template legitimately contains no adopted policy/`realization_refs`, Step 2 must say that `CURRENT_SUPPORTED_POLICY_REALIZATION_KEYS` is empty and still prove the available contract through canonical positive and negative conformance fixtures without pretending that a campaign policy is currently shipped. Fixtures must not become selectable product content or a second policy owner.

### 5.2 Per-route evidence rows

Each atomic route row must record:

```text
boundary_id
route_kind = ONE_OFF_ADJUDICATION | CONTEXTUAL_POLICY_ADJUDICATION | TYPED_POLICY_REALIZATION
exact policy identity/revision basis or explicit N/A rationale
policy lifecycle/applicability/conflict state
adoption/acting-principal authority evidence or explicit N/A for one-off ruling
information-eligibility basis and exact semantic consumer
declared parameter/fact consumer ID and source class
value type/cardinality/bounds/candidate-set contract
provenance, binding and rules-context identity
policy basis linkage and exact owner of retained policy evidence
accepted-generation freeze/currentness behavior
catalog context and realization-ref resolution/admission behavior
deterministic selector/accessor/fact/Activity/primitive/native-owner route
RNG owner or explicit N/A
authoritative mutation + MechanicalEvent route, or honest Mechanical-Null route
Resolution/Continuation/ExecutionSegment/receipt ownership
typed failures for missing/invalid/unauthorized/stale/conflicting/gap cases
idempotency/retry/suspension/recovery behavior
multiplayer publication/currentness behavior or explicit N/A
positive proof
negative-space proof
gap/owner/decision trigger
```

Split rows when authority, lifecycle, information eligibility, typed input, realization, mutation or recovery semantics differ materially. A family slogan is not proof.

### 5.3 Identity and currentness proof

The investigation must distinguish and reconcile without duplication:

- stable `policy_id`;
- exact campaign revision selecting normative Markdown plus sidecar;
- sidecar lifecycle/source anchor/adoption evidence;
- `rules_context_fingerprint` and accepted binding/fact identity;
- `policy_basis_refs` where the owning accepted contract requires them;
- selected `ResolvedCatalogContext` and realization target identity;
- accepted Resolution/Continuation generation and retry identity.

It must determine, from current owners and consumers, whether each current typed fact/binding retains enough exact policy/currentness evidence. It must not assume that a string field, a fingerprint or a ref name is sufficient merely because it exists. Conversely, it must not duplicate full policy text, creator identity, current world state or catalog identity into embedded values when the existing owner plus a stable reference/fingerprint already proves the invariant.

### 5.4 Realization-reference proof

For every typed policy-realization fixture or current supported edge, prove:

1. the adopter was authorized for the semantic effect class;
2. the exact current policy revision is valid and applicable;
3. each `realization_ref` resolves in the selected compatible catalog context;
4. reference kind and target are allowed for this policy/consumer;
5. the referenced capability is currently admitted/selectable for an exact consumer;
6. Activity parameters/bindings and native-owner transitions remain independently validated;
7. mention of a capability does not invoke it, grant it new consumers or bypass player choice/target/cost/resource legality;
8. missing, stale, incompatible, dormant, quarantined or semantically divergent realization stops finitely;
9. later policy publication does not rewrite accepted work.

S6D-10 must not design a universal homebrew authoring/package system. If current policy requires a typed capability that does not exist, the route is a finite realization gap until the separately governed catalog/package architecture admits one.

### 5.5 One-off adjudication proof

For each active adjudicated input form, prove:

1. the value is genuinely fiction-dependent and cannot be safely derived from engine-owned state;
2. the exact consumer declares the input and closed bounds;
3. the producer used only information eligible for that consumer/role/purpose;
4. validation rejects engine-owned facts, undeclared fields, wrong type/cardinality/range, stale basis and unauthorized consumer/binding reuse;
5. the full accepted causal input is frozen for the Resolution generation and retained only by its canonical owner;
6. deterministic execution owns RNG, arithmetic, legality, mutation and commit;
7. absence is a typed missing/adjudication outcome, not false/default/prose fallback;
8. a valid Mechanical-Null result remains valid without artificial StateDelta/world mutation;
9. a one-off ruling is not silently promoted to durable policy by repetition or local memory.

### 5.6 Gap and amendment routing

Classify every defect as one of:

```text
HOUSE_RULES_OWNER_REGRESSION
S6D-04 FACT/AUTHORITY REGRESSION
S6D-05 BINDING/RETENTION REGRESSION
S6D-06/07/08/09 EXACT-CONSUMER OR EXECUTION REGRESSION
STEP-3/5 CURRENTNESS-RECOVERY REGRESSION
S6D-10 LOCAL INTEGRATION/TEST GAP
S6D-11 INTEGRATED MACHINE-TEST DEBT
IMPLEMENTATION-PLANNING ONLY
HUMAN PRODUCT/ARCHITECTURE DECISION
```

A completed owner may be amended only when evidence proves a contradiction, a new unsatisfied current consumer or insufficiency. Any structural repair uses RED→GREEN evidence and repeats the whole-project Step-6 review. S6D-10 cannot activate vocabulary, primitives or package content through an integration ledger.

## 6. Required questions for Steps 2–8

1. What is the exact finite set of active adjudicated parameter/fact consumer edges today?
2. Does every edge have a declared producer, exact consumer permission, closed value domain, provenance/currentness identity, missing behavior and retry/recovery owner?
3. Can any accepted input be replayed under a different consumer, binding, rules context, policy revision or catalog context?
4. When a House Rule affected an adjudication, which canonical owner proves the exact policy basis without copying policy into execution values?
5. Are `policy_basis_refs`, `rules_context_fingerprint`, invocation-fact fingerprints and catalog-context identity jointly sufficient and nonduplicating for their actual consumers?
6. Which current reusable policy mechanics can be realized by existing typed definitions/capabilities, and what exact checks turn a `realization_ref` into legal linkage rather than execution authority?
7. Does any prose, sidecar field, realization ref or LLM decision accidentally select RNG, alter engine-owned state, create a capability, bypass the exact consumer, or perform a mutation?
8. Are policy adoption authority and one-off adjudication authority kept distinct in singleplayer and multiplayer, including stale prepared writes and later revocation?
9. Are policy conflict, realization gap, missing/invalid/unauthorized/stale adjudication and catalog incompatibility finite typed outcomes with no hidden fallback?
10. Do suspension, retry, recovery and later policy publication preserve accepted causal history without replay or reinterpretation?
11. Can contextual policy remain prose-only when its downstream mechanical effect is fully represented by an existing bounded typed route?
12. Can the complete supported boundary be proved without a new policy engine, rules DSL, lifecycle record, global frontier, query system or package-authoring subsystem?

## 7. Required Steps 2–8 outputs

1. **Step 2 — Research & architecture draft:** complete Source Manifest; item-level boundary inventory; finite bidirectional equality; exact per-route evidence ledger; current contract-gap analysis; alternatives only where evidence leaves real choices; recommendation and confidence.
2. **Step 3 — Decision Brief:** present only materially different product semantics, authority, scope or risk choices. If no human choice remains, record an evidence-based no-decision result and proceed under the accepted owners.
3. **Step 4 — Collaborative review:** challenge route completeness, policy/adjudication separation, currentness identity, information eligibility, exact consumer admission, negative space and implementation-facing clarity. Include required walkthroughs below.
4. **Step 5 — Candidate specification and authorized RED→GREEN realization:** define the exact integration contract and close only proven local or explicitly gated owner regressions. Do not implement broad runtime orchestration.
5. **Step 6 — Independent whole-project adversarial solution review:** reconstruct the dependency graph independently and attack duplicate authority, prose execution, policy-as-instruction escalation, unbounded input, arbitrary refs, stale policy/catalog reuse, unauthorized adoption, consumer replay, RNG/mutation leakage, retry/recovery history rewrite, dormant activation and extra subsystems.
6. **Step 7 — Resolution Gate:** reconcile every finding with fresh owner evidence. Zero unresolved `BLOCKING` or `SIGNIFICANT` findings is mandatory before canonicalization.
7. **Step 8 — Canonicalization/publication:** update only affected owners/contracts/tests/project routing, publish/read back the complete chain and stop before S6D-11.

Both critics must begin from `DEV/PROJECT_MAP.md`, inspect actual upstream/downstream/sibling owners and report `BLOCKING`, `SIGNIFICANT` and `MINOR` findings. Module-local review is invalid.

## 8. Required architecture acceptance walkthroughs

Before canonicalization, trace at least:

1. **One-off social DC:** current eligible fiction leads to one bounded adjudicated DC for `activity.check.generic`; deterministic RNG/result is retry-safe; the result may be Mechanical-Null; no durable policy is created.
2. **Contextual durable policy:** an active interpretive policy changes how an eligible fictional factor is classified, then supplies only a bounded typed input to an existing Activity; accepted work retains the exact causal basis after a later policy revision.
3. **Formalizable mechanical override:** an authorized mechanical-override policy references an already admitted typed capability; catalog/currentness and exact-consumer validation still control execution; native owners retain cost/RNG/mutation authority.
4. **Realization gap:** a mechanically material policy has no current realization or points to a missing/stale/incompatible/dormant capability; execution stops finitely without stale baseline preference, prose execution or silent no-op.
5. **Boolean spatial judgment:** one exact admitted `fiction.target_reachable` consumer accepts true or false for its bound candidate; missing, stale and cross-consumer reuse reject; no durable spatial truth or geometry engine appears.
6. **Suspension/retry/recovery:** an accepted adjudicated input survives a genuine continuation/retry without re-asking the LLM, changing policy basis, rerolling or duplicating mutation; later policy publication is forward-looking.
7. **Unauthorized adoption:** a non-creator without the mechanical-override grant may still make a lawful bounded one-off ruling but cannot publish a reusable mechanical override; technical repository permission does not change the result.
8. **Information eligibility:** a policy/adjudication cannot use truth or NPC knowledge ineligible for the exact consumer even when physically present in the shared context.

These are architecture/machine-contract scenarios, not production runtime tests or scripted GM dialogue.

## 9. Quality attributes and failure model

The recommendation must be distinguished by:

- authority correctness and absence of duplicate semantic owners;
- deterministic replay/retry/recovery of accepted mechanics;
- exact policy, rules-context, catalog-context and consumer currentness;
- fail-closed typed behavior for missing, stale, invalid, unauthorized and conflicting inputs;
- bounded ordinary-turn work and no mandatory extra LLM/network round trip;
- compatibility with one physical chat and logical information eligibility;
- testability through strict machine contracts and negative fixtures;
- YAGNI: no generic DSL, policy engine, graph, lifecycle, scheduler or universal homebrew subsystem.

Concrete attacks must include stale prepared policy publication, grant revocation, policy supersession during suspended work, replay under a different consumer/binding, stale catalog realization, dormant/quarantined ref, policy text with imperative instruction-like wording, engine-state injection, invalid bounded value, missing fact and duplicate retry.

## 10. Non-goals

- reopening the accepted House-Rules responsibility or adoption-authority decision;
- inventing new policy classes, creator representation, grants or notification semantics;
- full natural-language rule compilation or universal semantic-value representation;
- a generic homebrew package authoring, migration or distribution subsystem;
- full SRD/PHB/DMG corpus or broad rules-content expansion;
- activating dormant facts, selectors, primitives, definitions or package content;
- embedding full policy prose or world state in ActionRequest/Resolution/Continuation;
- replacing Context Runtime, publication, recovery, catalog, Activity, Rule Element or native state owners;
- background polling, push delivery, policy frontier/cursor, global scan, arbitrary query/code/path/patch/payload surfaces;
- production gameplay runtime or UI implementation;
- S6D-11/12 or R2.7 execution.

## 11. Human decision and stop conditions

Stop for the human architect only if evidence leaves a material choice about product semantics, authority, supported scope, an expensive owner-boundary change or nontrivial risk acceptance. Before stopping, exhaust repository evidence, identify the exact affected routes/owners, present real alternatives with trade-offs and a recommendation, and ask one precise decision.

Do not stop for repository discovery, corpus volume, source classification, traceability, schema/test representation, naming, or a repair that follows unambiguously from accepted owners.

## 12. Step-1 exit gate

Step 1 closes only when:

- a distinct whole-project brief critic has reconstructed the dependency graph through the current `DEV/PROJECT_MAP.md` and inspected actual owners, decisions, schemas, tests and consumers;
- every `BLOCKING` and `SIGNIFICANT` finding is repaired or explicitly resolved;
- the final brief and critic record are published to the authoritative branch and read back;
- `DEV/PROJECT_MAP.md` routes S6D-10 through this brief and its mandatory direct-and-indirect source graph;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` records S6D-10 Step 1 complete and Step 2 next;
- no Step-2 research draft, Decision Brief, candidate, machine-contract amendment, S6D-11/12 work or R2.7 continuation has begun.


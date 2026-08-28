# S6D-12 — Adversarial Final Closure — Step 6 Whole-Project Adversarial Critic

Status: **STEP 6 MANDATORY WHOLE-PROJECT CRITIC — COMPLETE / CANDIDATE ACCEPTABLE WITH OWNER-CONFORMING CLARIFICATION**

Date: 2026-08-28

Reviewed candidate ref: `a5f064f56ed64aebdf35f9744ce4f7409cc62700`

## 1. Critic mandate

This review attacks the Step-5 final-closure candidate from the whole-project dependency subgraph required by `DEV/PROJECT_MAP.md`. It is not a module-local review and does not treat the roadmap, prior evidence summaries or schema examples as semantic authority.

The critic asks whether the candidate:

- preserves current S6D-01…11 and inherited owners;
- introduces a duplicate authority, generic escape hatch or unsupported runtime subsystem;
- weakens package/set identity, retry, RNG, persistence, cleanup, source/adoption or House-Rules boundaries;
- mistakes current realization evidence for architecture authority;
- claims machine closure without executable proof;
- or leaves a material current obligation undispositioned.

## 2. Source Manifest / dependency subgraph

### Process and current candidate chain

- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- S6D-12 Steps 1–5, including the Step-2 item-level evidence and Step-4 cross-owner review.

### Current S6D semantic owners

- `RULESET_PACKAGE_IDENTITY.md`;
- `CATALOG_ADMISSION.md`;
- `CALCULATION_SELECTOR_METADATA.md`;
- `MECHANICAL_CONTEXT.md`;
- `PORTABLE_ACTIVITY_VALUES.md`;
- `ACTIVITY_PRIMITIVE_CONTRACTS.md`;
- `CHARACTER_PROGRESSION_READY_PC_SEED.md`;
- `HEALTH_EFFECTS_RECOVERY.md`;
- `DOMAIN_RULES_COVERAGE.md`;
- `HOUSE_RULES_MECHANICAL_BOUNDARY.md`;
- `RULESET_PACKAGE_MACHINE_CLOSURE.md`;
- approved B′ owner decision.

### Inherited execution / durability / policy owners

- Step-3 deterministic execution-boundary canonical specification;
- current Resolution/Continuation, execution-segment, runtime-mechanical-event and resolution-receipt schemas;
- Step-5.11 retention/compaction and Step-5.13 cleanup owners;
- `CATALOG_CONTRACTS.md`, `CATALOG_RESOLUTION.md`, `ACCESS_CONTROL.md`, `BRANCH_MODEL.md`;
- `GAME/CORE/SOURCES.md`, `PLAY_POLICY.md`, and current runtime/mechanics/persistence consumers.

### Machine realization and focused proof

- current package manifest and declared content members;
- S6D-07…11 validators/tests and current derived identity carriers;
- `DEV/TOOLS/validate_domain_rules_coverage.py` and focused S6D-09 tests;
- `DEV/SCHEMAS/execution-segment.schema.json`;
- `DEV/SCHEMAS/runtime-mechanical-event-state.schema.json`;
- `DEV/SCHEMAS/resolution-receipt.schema.json`;
- `DEV/SCHEMAS/runtime-resolution-state.schema.json`.

## 3. Candidate-wide attack replay

| Attack | Result | Notes |
|---|---|---|
| duplicate semantic owner | PASS | candidate creates only review predicates, no runtime owner |
| LLM/prose deterministic authority | PASS | typed adjudication boundary remains intact |
| generic expression/query/path/patch escape hatch | PASS | no new executable language introduced |
| registered-but-not-active mechanics treated as active | PASS | dormant/nonselectable negative space preserved |
| package content without admission/consumer proof | PASS | existing S6D-02/06/09/11 gates remain controlling |
| unsupported state/primitive implied by product promise | PASS | atomic product evidence/negative space remains preserved |
| cycle/fixed-point fallback | PASS | MechanicalContext bounded-DAG law unchanged |
| scheduler/global queue/global scan | PASS | no new scheduler or global work introduced |
| retry/idempotency/RNG respin | PASS WITH CLARIFICATION | MRC-03 must test existing Step-3 accepted-input/fixed-RNG/idempotency law, not invent a local retry owner |
| unreconstructable accepted ruleset/catalog context | PASS SEMANTICALLY | current projection repair remains a hard machine prerequisite |
| cleanup destroys required evidence | PASS | owner-routed protection/fail-safe retention unchanged |
| changed-set compatibility bypass | PASS | S6D-11 complete compatible/additive proof unchanged |
| House-Rules/adjudication bypass | PASS | no policy/prose execution authority introduced |
| product promise broader than machine route | PASS | negative space remains non-activated |
| stale current package/set projections accepted | FAIL-CLOSED AS DESIGNED | MRC-01/MRC-02/MRC-04 remain open machine gates |
| stale/superseded evidence treated as current authority | REPAIR REQUIRED | C-01 narrow S6D-08 prose reconciliation remains due |
| pre-release migration baggage activated | PASS | released incompatible-campaign migration remains future-not-due |
| ordinary hot-path network/repository/global work | PASS | candidate requires only bounded local runtime behavior; repository reconstruction is closure-time evidence |

No attack requires a new product decision, semantic owner, runtime class, package identity algorithm or risk acceptance.

## 4. Critic finding F-01 — Mechanical-Null event ownership precision

### Severity before resolution

`SIGNIFICANT` wording/owner ambiguity in MRC-03, not an architecture contradiction.

The Step-5 candidate correctly requires a genuine `event.check.resolved` / `event.save.resolved`, but it must not be read as requiring the durable `GAME/SCHEMA/event.schema.yaml` world/semantic-event shape or a new Mechanical-Null event subsystem.

The current Step-3 owner is explicit:

```text
Resolution / direct Transition execution
    -> ExecutionSegment(s)
        -> MechanicalEvents
        -> receipts/idempotency evidence

MechanicalEvent identity = segment_id + stable event_ordinal
```

Current runtime schemas match that owner:

- `runtime-mechanical-event-state` requires `segment_id`, `event_ordinal`, `event_kind`, `root_command_id`, `causal_ref`, and payload;
- `execution-segment` owns the committed segment disposition, `event_ids`, receipt exports and `affected_revision_refs`;
- `resolution-receipt` links execution owner, segment refs, event IDs, exports and pending children;
- `runtime-resolution-state` preserves accepted ruleset/context identity, invocation facts, fixed RNG results and committed segments.

### Resolution

For S6D-12 closure, MRC-03 SHALL be interpreted and tested as follows:

1. the genuine selected check/save fact is a Step-3 `MechanicalEvent` with `event_kind == event.check.resolved` or `event.save.resolved` as selected by the admitted primitive/route;
2. event identity/linkage follows the existing Step-3 event identity and existing runtime implementation; the conformance test SHALL NOT invent or hard-code a new event-id wire encoding because exact encoding is implementation detail;
3. Mechanical-Null zero authoritative world mutation is proved concretely by the committed `ExecutionSegment.affected_revision_refs == []` together with the selected genuine MechanicalEvent and valid existing resolution receipt;
4. the receipt/segment/event linkage uses the existing `event_ids` / segment references and existing execution owner identity;
5. retry/conflict assertions use the existing accepted-input fingerprint/fixed-RNG/idempotency behavior; they do not add a Mechanical-Null-specific retry owner;
6. `GAME/SCHEMA/event.schema.yaml` is not the owner or required shape of this runtime MechanicalEvent proof.

This is an owner-conforming clarification of Step-5 MRC-03. It introduces no new schema/API/class or semantic choice.

Post-resolution severity: `RESOLVED / 0 OPEN SIGNIFICANT`.

## 5. Critic finding F-02 — zero-revision proof must be structural

### Severity before resolution

`MINOR` proof precision.

The phrase “affected world revision count is zero” is insufficient if asserted only from route prose/metadata.

### Resolution

The executable proof must inspect the committed segment result and show:

```text
ExecutionSegment.affected_revision_refs == []
```

while still proving the genuine selected MechanicalEvent and receipt. Absence of a fabricated `StateDelta` alone is not positive Mechanical-Null proof.

Post-resolution severity: `RESOLVED / 0 OPEN MINOR`.

## 6. B′ / identity attack result

The Step-5 candidate conforms exactly to the approved B′ owner decision:

- one semantic coverage contract;
- coherent v2 -> v3 physical migration;
- one seven-field strictly-derived binding companion;
- no `coverage_semantic_sha256` or equivalent;
- no sharding;
- no second package/set identity owner;
- canonical identity remains manifest -> package snapshot -> resolved lock -> `ruleset_set_sha256`;
- no partial current-projection synchronization.

The critic therefore does not reopen B′. MRC-01/MRC-02/MRC-04 remain execution/verification prerequisites only.

## 7. Stale S6D-08 wording attack result

The final Machine Owner paragraph in `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` still describes an exact closed two-file content set plus aggregate content-set digest. Later S6D-11 identity architecture supersedes that wording.

This is not a competing live identity owner because later control is explicit, but Step-5 correctly requires its removal before `SEMANTIC_ARCHITECTURE_RECONCILED == true`.

Required narrow repair:

- retain `health-effects-recovery-seed.json` as the bounded S6D-08 package member;
- state that membership is declared by the package manifest;
- route identity/reconstruction to manifest -> package snapshot -> resolved lock -> `ruleset_set_sha256`;
- state that missing/extra/modified member bytes fail canonical reconstruction/registered validation;
- do not introduce an aggregate `content_set` authority or alter health/effect semantics.

## 8. Whole-project critic classification

After applying the owner-conforming F-01/F-02 clarifications:

```text
BLOCKING:    0 semantic/candidate defects
SIGNIFICANT: 0 open critic defects
MINOR:       0 open critic defects
```

Open closure work is intentionally **not** counted as a critic defect:

```text
MRC-01  B′ coherent machine realization                   OPEN / MACHINE_REALIZATION
MRC-02  all current identity projections synchronized     OPEN / MACHINE_REALIZATION
MRC-03  Mechanical-Null executable conformance            OPEN / MACHINE_REALIZATION
MRC-04  focused integrated verification                   OPEN / MACHINE_REALIZATION
C-01    S6D-08 stale identity prose reconciliation         DUE BEFORE SEMANTIC TRUE
```

## 9. Human-decision gate

```text
NEW_SEMANTIC_ARCHITECTURE_CONTRADICTION: NONE
NEW_PRODUCT_OR_AUTHORITY_CHOICE: NONE
NEW_MATERIAL_RISK_ACCEPTANCE: NONE
S6D-11_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
```

## 10. Step-6 disposition

```text
S6D-12 STEP 6: COMPLETE
WHOLE-PROJECT CANDIDATE CRITIC: PASS AFTER OWNER-CONFORMING CLARIFICATION
SEMANTIC CANDIDATE: ACCEPTABLE FOR RESOLUTION GATE
MACHINE_REALIZATION_VERIFIED: FALSE
S6D_FINAL_CLOSURE_AUTHORIZED: FALSE
NEXT: C-01 NARROW RECONCILIATION, THEN STEP 7 — RESOLUTION GATE
```

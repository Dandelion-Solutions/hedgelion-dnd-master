# RD-15 — Catalog Runtime Binding / Unsupported-Capability Evidence — Executable Implementation Plan

Status: **AUTHOR GRAPH REPAIR — NEW BOUNDED RD / PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 11 — SIGNIFICANT**

> For implementation workers: execute only after independent Senior plan GO and under the current HDM TDD/process rules. This RD does not authorize production implementation.

## 1. Why this RD exists

The accepted catalog architecture requires every execution-facing bind to use one exact logical `ResolvedCatalogContext` and permits `runtime.catalog_gap_report` only after bounded discovery plus deterministic validation proves the requested mechanic unsupported in that same context.

Current implementation planning has a real decomposition gap:

```text
RD-10 typed InterpreterResult / semantic mapping
    -> [NO CURRENT WORKER-READY CATALOG BINDING OWNER]
    -> RD-05 executable command/mechanics acceptance
```

At the same time:

- `runtime.catalog_gap_report` is an admitted durable runtime kind;
- WP-11 gives it the native route `STATE/RUNTIME/CATALOG_GAP_REPORTS`;
- current identifier policy gives it a campaign-scoped durable identity and Finding 7 marks LIVE birth `FORBIDDEN`;
- no current RD provides its state schema, producer, publication/recovery join or proof;
- WP-27 readiness/accounting does not contain an exact `ResolvedCatalogContext` / catalog-gap readiness leaf, so preserving the original 14-RD count would silently retain an owner-to-machine gap.

This RD is therefore a planning/decomposition repair, not a new architecture decision. It realizes already-accepted catalog-resolution semantics.

## 2. Semantic boundary

RD-15 is a thin deterministic binding/admission boundary. It is **not**:

- a second ruleset-package loader;
- an online/background catalog resolver;
- a fuzzy search service;
- a rules engine;
- an LLM interpretation phase;
- a definition/currentness authority;
- a package/adoption/migration owner;
- a generic error/event bus.

It consumes the current S6D package machine closure (`GAME/TOOLS/ruleset_package.py`) and explicit natural-owner campaign/session definition frontiers. Ordinary gameplay uses an already-bound exact context; it does not scan repositories, DEV, mutable tags or arbitrary package locations.

## 3. Dependencies and joins

Upstream:

- S6D-01/S6D-11 exact package/resolved-set identity and bounded loader/comparator;
- `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md` and `CATALOG_CONTRACTS.md`;
- RD-10 typed `InterpreterResult` / registered handoff;
- RD-04 native routing/identifier-policy/HOT substrate;
- RD-09 current source/authorization where a request originates from LIVE, without transferring catalog authority into LIVE;
- explicit campaign/session definition frontiers from their natural owners when present.

Downstream:

- RD-05 receives only a deterministically validated executable binding/proposal;
- RD-06 publishes durable `runtime.catalog_gap_report` campaign-domain evidence when produced;
- RD-07 recovers retained gap evidence and reconstructs the exact catalog basis needed by accepted execution;
- RD-11 may consume bounded catalog evidence for context assembly but cannot use Context Runtime to decide capability legality;
- RD-14 bootstrap/resume binds the exact package/current catalog basis before gameplay but does not perform per-request semantic selection.

## 4. Files / impact envelope

Create:

- `GAME/TOOLS/catalog_runtime.py`
- `DEV/SCHEMAS/catalog-binding-request.schema.json`
- `DEV/SCHEMAS/catalog-binding-result.schema.json`
- `DEV/SCHEMAS/runtime-catalog-gap-report-state.schema.json`
- `DEV/TESTS/test_rd15_catalog_runtime.py`

Modify only as required by RED/currentness evidence:

- `DEV/CATALOG/identifier-policies.json` only through the shared identity-policy integration checkpoint already defined by Findings 7/8/10; keep `runtime.catalog_gap_report` campaign-scoped and `live_birth=FORBIDDEN`;
- `DEV/PROJECT_MAP.md`
- `DEV/TOOLS/audit_engine.py`
- exact package/runtime instruction consumer if a stale competing catalog-binding route is found.

Inspect/reuse, do not duplicate:

- `GAME/TOOLS/ruleset_package.py`
- current ruleset lock/package schema and S6D validators
- RD-10 InterpreterResult schema
- RD-05 execution proposal/request schemas
- current campaign/session definition-frontier owner contracts.

## 5. Runtime context contract

RD-15 materializes only an **ephemeral bound view** over natural owners.

Conceptually:

```text
BoundCatalogContext {
  engine_capability_identity
  ruleset_set_digest_generation
  ruleset_set_sha256
  campaign_definition_frontier
  session_definition_frontier | ABSENT
  catalog_context_fingerprint_generation
  catalog_context_fingerprint
  exact_definition/capability lookup maps
}
```

The fingerprint is comparison/retry evidence, not reconstruction authority. The exact natural-owner identities/frontiers remain required.

### Context construction

```text
bind_catalog_context(
    validated_ruleset_lock,
    validated_ruleset_snapshots,
    engine_contract_inventory,
    campaign_definition_frontier,
    session_definition_frontier | ABSENT,
) -> BoundCatalogContext | CatalogContextFailure
```

Rules:

1. Reuse S6D loader outputs and validators; do not recompute alternative package identity.
2. Require exact current campaign-selected ruleset-set identity to match the loaded validated set.
3. Campaign/session definitions are accepted only from explicit owner-provided frontiers; empty frontier is valid.
4. Duplicate resolved `definition_id`, namespace collision, missing required owner frontier, incompatible kind/capability or unreconstructable context fails explicitly.
5. No layer-shadowing/last-wins behavior.
6. No repository/network scan, mutable tag lookup, model memory or fuzzy result establishes context authority.
7. Ordinary per-turn binding reuses the current validated bound context until one of its natural owner/currentness dependencies changes; invalidation rebuilds from exact owners.

## 6. Execution-facing catalog binding

Conceptual interfaces:

```text
bind_interpreter_candidate(
    interpreter_result,
    bound_catalog_context,
    accepted_subject/currentness_basis,
) -> CatalogBindingResult

validate_executable_binding(
    candidate_binding,
    bound_catalog_context,
) -> SUPPORTED(ExecutableCatalogBinding)
   | UNSUPPORTED(UnsupportedCapabilityEvidence)
   | INVALID_OR_AMBIGUOUS(reason)
```

Exact flow:

```text
RD-10 typed InterpreterResult
-> bounded candidate discovery/IDs supplied by admitted semantic path where needed
-> semantic selection/adjudication only where current owner permits it
-> deterministic exact ID/kind/capability validation against SAME BoundCatalogContext
-> SUPPORTED: typed ExecutableCatalogBinding -> RD-05
-> UNSUPPORTED: durable gap-report candidate; NO RuntimeCommand
-> INVALID/AMBIGUOUS: typed clarification/failure path under existing owner; NO fabricated mechanic
```

A search miss, fuzzy low rank, unknown prose phrase or remembered model ID is never enough to emit `UNSUPPORTED`.

`ExecutableCatalogBinding` contains only the exact IDs/contracts/basis RD-05 needs. It is not a durable new owner and cannot override accepted definition/package identity.

## 7. `runtime.catalog_gap_report` machine contract

Create a strict durable state schema. Minimum worker-ready state:

```text
CatalogGapReportState {
  interaction_id
  intent_plan_id
  clause_id
  catalog_context_fingerprint_generation
  catalog_context_fingerprint
  ruleset_set_digest_generation
  ruleset_set_sha256
  requested_semantic_class
  normalized_requested_capability
  attempted_candidate_refs[]
  deterministic_failure_codes[]
  disposition = MAPPING_UNSUPPORTED
}
```

Rules:

- references the exact originating Interaction/IntentPlan/clause; does not copy raw private reasoning or arbitrary conversation text;
- retains enough exact catalog-context identity to diagnose/recover the unsupported result without pretending the fingerprint alone reconstructs context;
- `attempted_candidate_refs[]` is bounded and contains only exact typed IDs/kinds actually deterministically checked; no fuzzy ranking dump/private reasoning;
- failure codes come from a closed machine vocabulary admitted by this RD or an existing compatible typed failure registry; no free-form executable semantics;
- report is operational/evidence only — not world truth, definition authority, backlog, retry queue or capability request that auto-modifies catalog;
- one unsupported material clause may establish at most one current accepted report identity for the same accepted mapping attempt/idempotency basis; retry must not create unbounded duplicate reports;
- report creation does not create RuntimeCommand, Resolution or gameplay mutation;
- fixing/upgrading catalog content later does not retroactively rewrite the historical accepted report.

## 8. Identity / routing / LIVE disposition

`runtime.catalog_gap_report` remains:

```text
native route: <state_root>/RUNTIME/CATALOG_GAP_REPORTS/<native deterministic path>
default identity: campaign-scoped durable identity under final identifier-policy table
live_birth: FORBIDDEN
```

If an unsupported request is discovered while gameplay authority for other owners is in LIVE, the gap report still publishes through its campaign-domain runtime-evidence route. It is not packed into LIVE and does not require/authorize `EPOCH_LOCAL_CREATION(runtime.catalog_gap_report)`.

The exact report ID is frozen before its first accepted durable publication and reused on retry. It carries no fictional chronology semantics.

## 9. Publication and currentness

RD-15 produces a typed campaign-domain gap-report delta; RD-06 owns publication.

Before accepted publication:

- the exact originating Interaction/clause identity is still the same accepted mapping attempt;
- the catalog context identity/basis used to prove unsupported remains the accepted basis for that attempt;
- report identity/idempotency key remains stable.

If publication conflicts after unsupported has already been deterministically established, refresh only the publication/currentness basis. Do not rerun LLM interpretation or silently select a different mechanic solely to avoid the report.

If the catalog/current-definition basis itself moved **before** the unsupported result became accepted, invalidate/rebind and revalidate against the new current exact context rather than publishing stale unsupported evidence.

## 10. Recovery

RD-07 joins this RD as follows:

- durable gap report is retained evidence and reloads by native exact ID/path;
- it never becomes current-definition authority;
- recovery of accepted execution reconstructs the exact catalog owner basis from natural owners/S6D identities, not from the gap report;
- a report referring to unavailable exact context evidence remains diagnosable historical evidence but cannot authorize execution;
- no checkpoint/cache/index/fingerprint alone substitutes for exact catalog reconstruction.

## 11. TDD checkpoints

### Task 1 — RED: expose the missing boundary

Create `DEV/TESTS/test_rd15_catalog_runtime.py` groups:

```text
CatalogContextBindingTests
CatalogCandidateValidationTests
CatalogGapReportTests
CatalogBindingCurrentnessTests
CatalogBindingIntegrationTests
```

Initial RED proves:

- RD-10 result cannot currently be deterministically bound to the same exact context before RD-05;
- search miss cannot be treated as unsupported;
- no durable `runtime.catalog_gap_report` state contract exists;
- package identity/fingerprint cannot be reconstructed from ambient/current-looking files;
- unsupported candidate can currently fall through toward execution or untyped prose unless the new boundary exists.

No RED-only publication checkpoint.

### Task 2 — GREEN: context binder

Implement `BoundCatalogContext` and exact construction over S6D loader outputs + explicit campaign/session frontiers.

Tests:

- exact resolved-set identity match;
- empty campaign/session frontiers valid;
- duplicate definition ID, namespace collision, context mismatch fail closed;
- no layer shadowing;
- no filesystem/repository/network scan or DEV dependency;
- fingerprint changes when a natural-owner frontier changes and stays stable for same exact basis.

### Task 3 — GREEN: deterministic candidate validation

Implement `bind_interpreter_candidate` / `validate_executable_binding`.

Tests:

- exact supported ID/kind/capability yields typed executable binding;
- fuzzy candidate must still pass exact deterministic validation;
- remembered/unknown ID fails;
- wrong kind fails;
- search miss alone is not `UNSUPPORTED`;
- deterministic exhaustive/bounded admitted validation may establish `UNSUPPORTED`;
- no RuntimeCommand exists before `SUPPORTED`.

### Task 4 — GREEN: durable gap-report candidate

Create strict schema and producer.

Tests:

- exact Interaction/IntentPlan/clause + context identity captured;
- no raw private reasoning copied;
- bounded attempted candidates and closed failure codes;
- stable retry identity/idempotency;
- no RuntimeCommand/Resolution/gameplay mutation;
- LIVE-originating request still produces campaign-domain evidence only;
- later catalog change does not rewrite accepted historical report.

### Task 5 — publication/currentness/recovery joins

Integrate typed output with RD-06/RD-07 contracts without implementing their transports.

Tests:

- publication conflict does not rerun interpretation;
- pre-acceptance catalog-basis move invalidates/rebinds;
- post-acceptance publication retry preserves report identity/result;
- recovery cannot execute from report/fingerprint/cache alone;
- exact supported binding passed to RD-05 retains accepted ruleset-set/context identity.

### Task 6 — full integration proof

Prove the complete seam:

```text
RD-10 InterpreterResult
-> RD-15 same-context deterministic binding
-> SUPPORTED -> RD-05 executable acceptance
   OR
   UNSUPPORTED -> RD-15 gap evidence -> RD-06 publication
-> RD-07 recovery from natural owners/evidence
```

Negative: no direct RD-10 -> RD-05 executable path bypasses catalog binding.

Run eventually:

```bash
python3 -m unittest DEV.TESTS.test_rd15_catalog_runtime -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

## 12. Coverage / R018 consequences

This finding exposes a planning-coverage hole not represented by an exact existing WP-27 readiness leaf. Do **not** invent a fake `R27-R###` ID.

Track it as post-WP27 author graph closure:

```text
AUTHOR_GRAPH_FINDING_11
  native owners:
    CATALOG_RESOLUTION.md §§2,9-10
    CATALOG_CONTRACTS.md runtime-record/identifier laws
    RULESET_PACKAGE_IDENTITY.md / MACHINE_CLOSURE.md
  machine family:
    runtime.catalog_gap_report
  decomposition owner:
    RD-15
  R018 contribution:
    CATALOG_RUNTIME_BINDING + runtime.catalog_gap_report family closure
```

R018 family closure for `runtime.catalog_gap_report` requires:

```text
admitted kind
-> strict state schema
-> final identifier/live_birth disposition
-> WP-11 native route
-> RD-15 deterministic producer
-> RD-06 campaign publication
-> RD-07 recovery/non-authority
-> positive + negative same-context unsupported proof
```

The package's final bidirectional coverage report must explicitly show why the original 145 readiness leaves were insufficient to represent this discovered native-owner implementation consequence, without rewriting historical WP-27 evidence as though it had contained it.

## 13. Version / migration

This is unreleased v1 realization. Legacy v0.8 preservation is not a constraint. No compatibility shim/migration is required solely to retain the absence of a prior gap-report schema or runtime binder. Apply the normal Version Impact Gate to the actual schema/API change at implementation time.

## 14. Disposition

```text
AUTHOR_GRAPH_FINDING_11: REPAIRED_IN_PLANNING
NEW_RD_REQUIRED: YES — RD-15
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```

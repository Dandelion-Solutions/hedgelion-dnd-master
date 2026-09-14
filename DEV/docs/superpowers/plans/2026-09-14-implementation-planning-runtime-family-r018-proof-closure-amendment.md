# HDM Implementation Planning — R018 Runtime-Family Proof Closure Amendment

Status: **CURRENT HIGHEST-PRECEDENCE MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **F34 — SIGNIFICANT — runtime-family R018 item-bound proof gap**

## 1. Finding

`R27-R018` requires every accepted durable/runtime family to have a final schema/root or an explicit no-durable-record disposition, with **per-family schema/root validation**. Its negative law explicitly forbids false completion from catalog admission.

The current post-graph package already distributes the required runtime-family mechanisms across their natural RDs, and WP-11 already supplies the exact native roots. However, current proof routing is asymmetric:

- `2026-09-14-implementation-planning-lossless-proof-ledger-v3-post-graph.md` says that exact 17 world and 17 runtime members are checked item-by-item;
- the same closure names `R018WorldFamilyProofTests` and the separate RD-15 catalog-gap witness, but does not name an executable 17-row runtime-family proof;
- `2026-09-14-implementation-planning-post-graph-proof-witness-matrix.md` has world-family rows but no runtime-family equivalent;
- bidirectional coverage names the 17 runtime semantic/execution routes, but does not itself prove the exact final schema/root pair for every member.

A reviewer or worker could therefore accept `17+17` census/accounting while one runtime family lacks its required final machine shape/root realization. That is exactly the count-based false closure forbidden by R018.

This is a **proof/coverage closure defect**, not a new semantic architecture decision and not a new runtime subsystem.

## 2. Exact runtime-family R018 matrix

The current accepted v1 runtime-family set is exactly the following 17 members. Each row is mandatory and is independently validated; count equality alone is invalid.

| Runtime family | Final schema / machine-shape surface | WP-11 native root / exceptional route | Owning realization route |
|---|---|---|---|
| `runtime.session` | `GAME/SCHEMA/session.schema.yaml` | `SESSIONS` | RD-07 session/recovery contract |
| `runtime.message` | `DEV/SCHEMAS/runtime-message-state.schema.json` | `LOG/MESSAGES` | RD-02 retained Message owner |
| `runtime.interaction` | `DEV/SCHEMAS/runtime-interaction-state.schema.json` | `STATE/RUNTIME/INTERACTIONS` | RD-05 runtime lifecycle |
| `runtime.procedure` | `DEV/SCHEMAS/runtime-procedure-state.schema.json` plus admitted concrete Procedure-owned subtype shape where applicable | `STATE/RUNTIME/PROCEDURES` | RD-05 runtime lifecycle |
| `runtime.intent_plan` | `DEV/SCHEMAS/runtime-intent-plan-state.schema.json` | `STATE/RUNTIME/INTENT_PLANS` | RD-05 runtime lifecycle |
| `runtime.command` | `DEV/SCHEMAS/runtime-command-state.schema.json` | `STATE/RUNTIME/COMMANDS` | RD-05 runtime lifecycle; catalog-backed acceptance also consumes RD-15 |
| `runtime.resolution` | `DEV/SCHEMAS/runtime-resolution-state.schema.json` | `STATE/RUNTIME/RESOLUTIONS` | RD-05 runtime lifecycle |
| `runtime.continuation` | `DEV/SCHEMAS/runtime-continuation-state.schema.json` | `STATE/RUNTIME/CONTINUATIONS` | RD-05 runtime lifecycle / RD-07 recovery consumer |
| `runtime.mechanical_event` | `DEV/SCHEMAS/runtime-mechanical-event-state.schema.json` | `LOG/MECHANICAL_EVENTS` | RD-05 semantic/composite identity; RD-16 final shared identifier-policy integration |
| `runtime.semantic_event` | `DEV/SCHEMAS/runtime-semantic-event-state.schema.json` | `LOG/SEMANTIC_EVENTS` | RD-13 native history |
| `runtime.resolution_trace` | `DEV/SCHEMAS/runtime-resolution-trace-state.schema.json` | `STATE/RUNTIME/RESOLUTION_TRACES` | RD-05 execution evidence |
| `runtime.disclosure` | `DEV/SCHEMAS/runtime-disclosure-state.schema.json` | `STATE/RUNTIME/DISCLOSURES` | RD-02 disclosure owner |
| `runtime.collaboration_obligation` | `DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json` + shipped `GAME/SCHEMA/collaboration_obligation.schema.yaml` projection | `STATE/RUNTIME/COLLABORATION` | RD-12 collaboration owner |
| `runtime.checkpoint` | `GAME/SCHEMA/checkpoint.schema.yaml` | `CHECKPOINTS` | RD-07 checkpoint/recovery contract |
| `runtime.id_allocator` | `DEV/SCHEMAS/campaign-id-allocator-state.schema.json` + `GAME/SCHEMA/id_allocator.schema.yaml` | exceptional fixed `STATE/ID_ALLOCATOR.yaml` | RD-04 campaign allocator |
| `runtime.maintenance_audit` | `DEV/SCHEMAS/runtime-maintenance-audit-state.schema.json` | `STATE/RUNTIME/MAINTENANCE_AUDITS` | RD-07 maintenance evidence |
| `runtime.catalog_gap_report` | `DEV/SCHEMAS/runtime-catalog-gap-report-state.schema.json` | `STATE/RUNTIME/CATALOG_GAP_REPORTS` | RD-15 gap evidence -> RD-06 publication -> RD-07 recovery |

The table is a planning/proof fixture, not a runtime registry or semantic owner. The natural owners above remain authoritative for each shape and behavior.

If execution-time currentness proves that a named schema surface has been legitimately superseded by a later accepted owner, the worker must update the exact row and proof route under the normal Version/System Impact process; it may not silently drop the family or satisfy the row from catalog admission alone.

## 3. Mandatory proof witness

Add one package proof class, created only when implementation/proof execution is authorized:

```text
DEV/TESTS/test_implementation_proof_ledger.py
  R018RuntimeFamilyProofTests
```

The proof is item-bound over the exact 17-row matrix. It must prove for each family:

1. the family is in the exact accepted runtime-family set and no unowned extra runtime family is silently admitted;
2. the row resolves to its exact final schema/machine-shape surface, or to an owner-approved explicit no-durable-record disposition — none of the 17 current rows has such a no-record disposition;
3. the exact WP-11 native root/exceptional route is preserved;
4. the final schema validates the complete native identity/state contract required by its natural owner rather than only a generic untyped object envelope;
5. its identifier/live-birth disposition is compatible with the current identifier-policy integration; `runtime.id_allocator` remains exceptional and SOURCE_NATIVE_LIVE never falls back to it;
6. its owning RD has an executable producer/consumer route appropriate to that family; catalog presence alone is insufficient;
7. a missing schema, wrong root, family/schema mismatch, duplicate family, unowned extra family or generic count-only substitute fails the proof.

The proof must include exact negative cases for at least:

- deleting one row while keeping runtime count at 17 through a duplicate/extra member;
- mapping one family to another family's schema;
- wrong WP-11 root with otherwise valid body;
- treating `runtime.id_allocator` as a hashed ordinary native-record route;
- treating a catalog kind with no final schema as R018-complete;
- treating the 17-member census alone as proof.

Primary channel: `STATIC_AUDIT + INTEGRATION_SCENARIO`.

## 4. Composite R018 closure law

The current R018 composite gate is superseded only in this exact respect:

```text
R018_WORLD_FAMILY_PROOF_READY
+ R018_RUNTIME_FAMILY_PROOF_READY
+ RD15_CATALOG_GAP_BEHAVIORAL_FAMILY_WITNESS_READY
+ current route/identity/shared-integration prerequisites
    -> CompositeR018ProofTests
```

`CompositeR018ProofTests` may not close merely because:

- the world-family matrix is green;
- `runtime.catalog_gap_report` alone is green;
- `core-catalog.json` contains 17 runtime kind names;
- bidirectional coverage lists all 17 names;
- aggregate `17+17` counts match.

The RD-15 catalog-gap behavioral witness remains required in addition to its row in `R018RuntimeFamilyProofTests`; the row proves schema/root family realization, while RD-15 proves the special producer/publication/recovery mechanism already required by current proof v3.

## 5. Execution/checkpoint integration

This amendment creates **no new RD and no whole-wave execution barrier**.

Owner-local runtime-family work proceeds under its existing RD. The package proof becomes eligible only after the relevant existing GREEN checkpoints are available:

```text
RD-02 native Message/Disclosure schema checkpoint
+ RD-04 allocator/native-route checkpoint
+ RD-05 runtime lifecycle/evidence schema checkpoint
+ RD-07 Session/Checkpoint/Maintenance schema checkpoints
+ RD-12 collaboration-obligation schema checkpoint
+ RD-13 SemanticEvent schema checkpoint
+ RD-15 catalog-gap schema/mechanism checkpoint
+ RD-16 final shared identifier-policy integration checkpoint
    -> R018_RUNTIME_FAMILY_PROOF_READY
```

This is a proof dependency join. It does not serialize unrelated owner-local implementation work and transfers no semantic ownership to the proof ledger or RD-16.

Overlay 5 checkpoint-coherence law remains in force: the proof class is introduced only when the mechanisms it verifies are available in the same coherent GREEN proof checkpoint.

## 6. Coverage / proof / execution authority consequences

This amendment is later-precedence for F34 only.

Coverage:
- the runtime-family forward map in bidirectional coverage v3 remains semantically correct;
- this exact matrix adds the missing reverse machine-shape/root/proof closure.

Proof:
- proof-ledger v3's statement that runtime families are item-by-item checked is valid only together with this amendment;
- the post-graph witness matrix gains logical row `PG32`:

```text
PG32  exact 17-runtime-family R018 schema/root closure
      -> R018RuntimeFamilyProofTests
      -> STATIC_AUDIT + INTEGRATION_SCENARIO
```

Execution graph:
- no new semantic hard edge is introduced;
- only the proof checkpoint join in §5 is added;
- existing RD-01..RD-16 graph and F27–F31 execution routing remain otherwise unchanged.

## 7. Negative-authority / non-goals

This repair does not:

- create a central runtime-family registry;
- make this matrix runtime authority;
- move semantic ownership into RD-16 or the proof ledger;
- require every family to use the same schema technology or lifecycle;
- turn route/root naming into identity/currentness authority;
- activate dormant/release/empirical work;
- create a new readiness ID;
- authorize production implementation.

## 8. Disposition

```text
F34: REPAIRED_IN_PLANNING
R018_RUNTIME_FAMILY_COUNT_ONLY_CLOSURE: FORBIDDEN
R018_RUNTIME_FAMILY_ITEM_BOUND_WITNESS: R018RuntimeFamilyProofTests
R018_COMPOSITE_REQUIRES_WORLD_AND_RUNTIME_ITEM_PROOF: YES
NEW_RD: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

This repair remains author-side and independently unconfirmed. It does not unblock Senior review; the broader adversarial graph audit continues.
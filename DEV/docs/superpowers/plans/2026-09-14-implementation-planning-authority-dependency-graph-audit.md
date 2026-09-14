# HDM Implementation Planning — Authority / Dependency Graph Audit

Status: **ACTIVE AUTHOR ADVERSARIAL PLANNING AUDIT — NON-CANONICAL EVIDENCE LEDGER**
Date: 2026-09-14
Baseline: `94e416c58633912a97308c1bfa95762951f0f8a4`
Production implementation authorized: **NO**.

This artifact is an audit/traceability ledger. It does not replace canonical owners, RD plans, proof ledgers, or readiness authorities. Its purpose is to detect hidden implementation-planning defects that coarse document-by-document review can miss.

## 1. Graph model

The audit treats the planning package as a typed directed multigraph.

### Node classes

- `SEMANTIC_OWNER` — world/runtime/value owner and lifecycle.
- `POLICY_OWNER` — authorization/currentness/chronology/publication/recovery law.
- `MACHINE_KIND` — catalog/admission kind.
- `STRUCTURE` — exact machine/schema shape.
- `IDENTITY_POLICY` — allocation/derived/composite/singleton/source-native identity.
- `PHYSICAL_ROUTE` — fixed/root/route/index/storage location.
- `DERIVATIVE_ROUTE` — completeness/index/routing evidence that is not semantic authority.
- `RUNTIME_API` — deterministic producer/validator/consumer method.
- `DURABILITY_EDGE` — local atomic segment, campaign publication, LIVE exact-source CAS, Story publication, etc.
- `RECOVERY_CONSUMER` — cold hydration/currentness/rebuild path.
- `SHIPPED_CONSUMER` — CORE/setup/session/bootstrap prose or schema that directs actual behavior.
- `READINESS_DUTY` — R001..R084 item or owner-enumerated machine duty.
- `PROOF_WITNESS` — focused/integration/static/hosted/empirical proof.
- `RD_OWNER` — RD-01..RD-14 executable plan.
- `EXECUTION_EDGE` — prerequisite, constraint, bounded integration join, or currentness barrier.

### Edge classes

```text
OWNS
ADMITS
STRUCTURES
IDENTIFIES
ROUTES
DERIVES_FROM
MUTATES_WITH
PUBLISHED_BY
SELECTS_AUTHORITY
CONSUMES
RECOVERS_FROM
PROVES
IMPLEMENTS
JOINS_BEFORE_INTEGRATION
CONSTRAINS_WITHOUT_ORDERING
MUST_NOT_OWN
SUPERSEDES
```

## 2. Required closure patterns

A worker-ready family/owner path must satisfy the applicable closure, not merely contain similarly named files.

### Native durable owner

```text
SEMANTIC_OWNER
 -> MACHINE_KIND/admission
 -> STRUCTURE
 -> IDENTITY_POLICY
 -> PHYSICAL_ROUTE
 -> RD producer/mutator
 -> DURABILITY_EDGE
 -> RECOVERY_CONSUMER
 -> READINESS_DUTY
 -> item-bound PROOF_WITNESS
```

### Correctness-critical derivative routing

```text
SEMANTIC_OWNER lifecycle
 -> derivative route computation
 -> same acknowledged durability closure as owner transition
 -> bounded recovery/invalidation consumer
 -> basis/currentness validation
 -> proof of completeness + non-authority
```

### Shipped consumer cutover

```text
canonical owner law
 -> runtime/schema realization
 -> shipped CORE/setup/session consumer
 -> stale formulation negative search/test
```

### Cross-domain operation

```text
native source A exact edge
 + native source B exact edge
 -> forward owning transition
```

There is no implied distributed transaction, rollback, scalar currentness, or fictional chronology edge unless a canonical owner explicitly grants it.

## 3. Defect patterns searched

The audit marks a planning defect when it finds any of:

1. semantic owner with no admitted machine kind or explicit no-record disposition;
2. physical family/route with no semantic owner;
3. catalog kind with no exact structure or identifier policy;
4. independently addressable owner with a shorter-lived ID than its accepted durability;
5. lifecycle transition with no coherent derivative routing/index mutation;
6. derivative completeness consumer with no bounded producer;
7. proof witness whose executable mechanism is absent or underdefined;
8. shipped consumer that preserves contradicted authority/currentness guidance;
9. multiple independent writers for one physical shared file without an ordered join;
10. publishable checkpoint that commits intentional RED future tests;
11. currentness route that nominates authority but has no exact selected-source fence;
12. recovery path that can only succeed by forbidden broad scan/fallback;
13. aggregate readiness coverage that can hide a missing concrete family/item;
14. stale legacy v0.8 preservation assumption constraining the clean-slate v1.0 `GAME/**` design;
15. architecture owner contradiction where a lower-scope physical owner invents/duplicates semantic ownership.

## 4. Findings currently established

| Author finding | Graph break | Current disposition |
|---|---|---|
| 1 | Scene LIVE route shipped/schema consumer was stale relative to owner-typed currentness | mandatory scene-routing overlay published |
| 2 | Publishable RD checkpoints contained future-task intentional RED tests | package checkpoint-coherence overlay published |
| 3 | RD-01 contained another instance of the same checkpoint break | incorporated into checkpoint overlay |
| 4 | `world.thread` semantic owner had no complete catalog admission/structure/identity projection | mandatory WP-15 thread catalog overlay published |
| 5 | WP-17 shipped collaboration guidance had proof/search but no executable consumer cutover | mandatory WP-17 consumer overlay published |
| 6 | temporal owner lifecycle had Agenda/recovery consumers but no durable completeness-routing producer | mandatory temporal completeness-routing overlay published |
| 7 | WP-16 duties 12/13/15 currently claim proof closure without complete executable lifecycle/identity/multi-source mechanism | **OPEN — repair being prepared** |
| 8 | family graph shows false `world.faction` physical family and missing `world.player` machine admission | **OPEN — reconciliation repair being prepared** |

## 5. Family-level R018 graph — current evidence

Current S6D `world_record_kinds` machine admission contains 15 exact kinds:

```text
world.actor
world.actor_group
world.asset
world.location
world.connection
world.zone
world.organization
world.contract
world.mission
world.scene
world.encounter
world.hazard
world.effect
world.lore_fact
world.knowledge
```

Current later accepted deltas:

- `world.thread` — WP-15 accepted semantic owner; current machine admission absent; Author Finding 4 already makes the coordinated cutover mandatory.
- `world.player` — WP-16 accepted campaign authorization/control owner; `GAME/SCHEMA/player.schema.yaml` and identifier policy exist, but catalog kind/admission/entity structure are absent; requires coordinated catalog admission rather than an inspect-only schema disposition.
- `world.faction` — **not** a semantic owner. Current catalog owns `world.organization`; faction is `organization.faction` facet/classification. WP-11's separate `world.faction -> WORLD/FACTIONS` row is therefore a stale lower-scope physical projection and must not create a new v1 family.

The user/product-owner clean-slate constraint is now explicit:

```text
GAME/** may be rebuilt for v1.0.
legacy v0.8 is not a preservation constraint.
```

Therefore legacy `faction.schema.yaml`, old roots, or old route names do not create a compatibility reason to retain a duplicate v1 semantic family.

## 6. Runtime-family identity graph — current evidence

Current admitted runtime record kinds include:

```text
runtime.session
runtime.message
runtime.interaction
runtime.procedure
runtime.intent_plan
runtime.command
runtime.resolution
runtime.continuation
runtime.mechanical_event
runtime.semantic_event
runtime.resolution_trace
runtime.disclosure
runtime.collaboration_obligation
runtime.checkpoint
runtime.id_allocator
runtime.maintenance_audit
runtime.catalog_gap_report
```

Identity classification must distinguish:

- independently allocated externally referenceable identities;
- parent-derived identities;
- semantic composite identities;
- singletons/campaign-only owners;
- source-native LIVE identities.

WP-16 does not authorize a generic surrogate rewrite. Derived/composite identities remain derived/composite. `source_native_live` is an alternate accepted identity basis only for independently addressable records first durably accepted inside LIVE and only where per-kind LIVE-born creation/admission is explicitly allowed.

## 7. WP-16 graph status

Items 1–11: producer/currentness/lifecycle paths are present in RD-09 plus existing joins.

Items 12, 13, 15: open planning gaps.

- **12 additive activation/reactivation:** proof ledger names `LiveLifecycleTests`, but RD-09 does not define the owner-proven no-rollover decision or its negative/controller-transfer cases.
- **13 source-native identity / per-kind admission:** proof ledger claims exact per-kind projection, but RD-09/PB-04 leave the kind set and creation admission to worker discovery. Unknown family must fail closed.
- **15 multi-LIVE composition:** proof ledger claims no-distributed-rollback behavior, but RD-09 does not define exact multi-source freeze/recompose/forward-transition handling.

Items 16–21 currently have valid cross-owner joins to RD-05/RD-07/RD-08/RD-09/RD-12 as applicable and remain under audit rather than being duplicated into RD-09.

Item 22 remains `EMPIRICAL_DEFERRED` under WP-24 until a real target workload exists.

## 8. Audit queue

The graph audit remains open. Required next passes:

1. finish WP-16 Finding 7 repair and re-evaluate R080 item-level proof;
2. reconcile Finding 8 and rebuild the full R018 family matrix;
3. compare every WP-11 world/runtime physical family against semantic admission + structure + ID policy + RD owner + proof;
4. inspect orphan identifier policies and admitted kinds lacking a physical/runtime route;
5. inspect shared files touched by two or more RD/overlays for one-writer/order correctness;
6. inspect every `INSPECT_ONLY`, `PROTECT_CURRENT_CONFORMING`, compatibility, migration, preservation and shim disposition under clean-slate v1.0;
7. inspect publication/recovery companions for same-edge joins and no-scan recovery;
8. inspect all proof ledgers for witness-without-mechanism and mechanism-without-proof asymmetry;
9. rebuild execution-wave edges from the repaired dependency graph;
10. rebuild bidirectional coverage at item/family granularity rather than relying only on aggregate domain slices;
11. run final currentness/reverse-coverage sweep before author closure.

## 9. Completion condition

This audit may close only when:

```text
OPEN AUTHOR BLOCKING    = 0
OPEN AUTHOR SIGNIFICANT = 0
OPEN AUTHOR MINOR       = 0

and

all active readiness/owner duties have:
  exact current owner
  executable RD route
  physical/shared-writer disposition
  required durability/currentness/recovery joins
  item-bound proof
  reverse coverage
```

Only then may the package move to mandatory independent Senior plan review / GO. Production implementation remains forbidden until that independent gate passes.

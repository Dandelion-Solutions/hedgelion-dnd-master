# Implementation Planning — Blank Scaffold Input Checkpoint Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 40 — SIGNIFICANT**

## Finding

RD-14 Task 3 requires the selected package generator to produce the **complete current v1 campaign scaffold** from the package `CAMPAIGN/` template. Bootstrap is explicitly forbidden from repairing a partial generator result by post-generation LLM/per-file invention.

Several mandatory blank-scaffold products are owned by earlier/lateral planning repairs:

```text
STATE/ID_ALLOCATOR.yaml
STATE/RUNTIME/TEMPORAL_ROUTING.yaml
STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml
STATE/RUNTIME/LIVE_ROUTING.yaml
```

The current package already requires each of these to exist as a valid blank-campaign artifact:

- RD-04 owns the campaign allocator singleton/scaffold contract;
- Finding 6 / RD-08 owns the empty temporal-routing companion;
- Finding 9 owns the empty principal->PLAYER completeness-routing companion;
- Finding 30 / RD-09 owns the empty LIVE-routing completeness companion.

RD-14 consumes them, but the current checkpoint graph names only a later `RD-16 -> RD-14 late final topology/scaffold validation` edge plus other product joins. It does **not** provide a named checkpoint requiring these blank-scaffold producer contracts to exist before RD-14's generator/scaffold integration task executes.

Therefore a legal worker schedule can execute RD-14 Task 3 against an incomplete package template and only later discover that mandatory generated files must be added. The worker must then invent whether to rerun generation, patch output, amend the package, or treat the first scaffold as valid. That contradicts the exact-generator/complete-package law and creates an avoidable invalid intermediate implementation route.

This is a planning/checkpoint defect, not an architecture gap. The required files and their semantics are already accepted.

---

# 1. Producer-local scaffold checkpoints

The owning plans expose bounded **contract/template readiness** checkpoints. These checkpoints are intentionally narrower than whole-RD completion.

```text
RD04_ALLOCATOR_SCAFFOLD_READY
RD08_TEMPORAL_ROUTING_SCAFFOLD_READY
PRINCIPAL_PLAYER_ROUTING_SCAFFOLD_CONTRACT_READY
RD09_LIVE_ROUTING_SCAFFOLD_CONTRACT_READY
RD07_OPERATIONAL_ROOT_CONTRACT_READY
```

Meanings:

### `RD04_ALLOCATOR_SCAFFOLD_READY`

The current package template contains a schema-valid initial campaign allocator singleton at its accepted fixed route. Campaign allocation runtime/HOT integration may continue independently; this checkpoint proves only the deterministic blank scaffold material required by generation.

### `RD08_TEMPORAL_ROUTING_SCAFFOLD_READY`

The package template contains a schema-valid explicit empty `STATE/RUNTIME/TEMPORAL_ROUTING.yaml` using the accepted temporal-source-routing contract. No temporal occurrence is created and no Agenda/runtime completion is implied.

### `PRINCIPAL_PLAYER_ROUTING_SCAFFOLD_CONTRACT_READY`

The package template contains a schema-valid explicit empty `STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml`. It proves only blank completeness-routing structure. PLAYER admission/final strict schema, authorization runtime and publication/recovery joins remain independently owned.

### `RD09_LIVE_ROUTING_SCAFFOLD_CONTRACT_READY`

The package template contains a schema-valid explicit empty `STATE/RUNTIME/LIVE_ROUTING.yaml`. It proves only the blank selected-route companion contract. It does **not** wait for source-native LIVE identity, opening, CAS, packing or absorption completion and grants no LIVE authority.

### `RD07_OPERATIONAL_ROOT_CONTRACT_READY` — F58 extension

The package template contains `STATE/RUNTIME/RECOVERY_ROOTS/FORMAT.yaml`, local version 1, and the shared operational-root routing contract/path validation is GREEN under mandatory overlay 37. The generated blank active-only namespaces have no gameplay entries. The static marker distinguishes a missing contract from a valid blank format; it does not itself certify current membership completeness. This checkpoint requires neither full RD-05 lifecycle execution nor full RD-07 recovery, RD-09 LIVE identity/CAS, or RD-16 final integration.

This split is required to avoid inventing a false cycle through RD-14 campaign identity -> RD-09 source-native identity -> RD-16 -> RD-14 late topology validation.

---

# 2. RD-14 blank-scaffold input join

Add:

```text
RD04_ALLOCATOR_SCAFFOLD_READY
+ RD08_TEMPORAL_ROUTING_SCAFFOLD_READY
+ PRINCIPAL_PLAYER_ROUTING_SCAFFOLD_CONTRACT_READY
+ RD09_LIVE_ROUTING_SCAFFOLD_CONTRACT_READY
+ RD07_OPERATIONAL_ROOT_CONTRACT_READY
  JOIN_BEFORE_INTEGRATION
RD14_BLANK_SCAFFOLD_INPUTS_READY
```

Then:

```text
RD14_BLANK_SCAFFOLD_INPUTS_READY
  HARD_PRECEDES
RD14_GENERATOR_SCAFFOLD_VALIDATION_READY
```

`RD14_GENERATOR_SCAFFOLD_VALIDATION_READY` is the GREEN result of RD-14 Task 3's exact generator/scaffold validation against the selected package root.

RD-14 Task 1/2 campaign-selection and early creation-identity work remains eligible before this join when it does not execute/validate the final generated package scaffold.

The existing `RD14_CAMPAIGN_IDENTITY_CREATION_READY` checkpoint remains distinct and may continue to feed the F25 source-native identity join. F40 does not create a whole-RD ordering edge.

---

# 3. Generator law

At `RD14_GENERATOR_SCAFFOLD_VALIDATION_READY`, the selected package generator must receive a package/template that already contains all current mandatory blank-scaffold products admitted by the package.

The generated output must contain, at minimum where applicable to the final v1 package:

```text
STATE/ID_ALLOCATOR.yaml
STATE/RUNTIME/TEMPORAL_ROUTING.yaml
STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml
STATE/RUNTIME/LIVE_ROUTING.yaml
STATE/RUNTIME/RECOVERY_ROOTS/FORMAT.yaml
```

plus all other currently admitted scaffold products from their owners.

Rules:

1. Bootstrap does not create any of these files after generation merely because the package template was stale.
2. Missing mandatory scaffold input blocks generator/scaffold validation; it is not interpreted as an empty/absent semantic state.
3. Empty completeness companions are explicit validated artifacts; physical absence is not equivalent to semantic emptiness.
4. The allocator initial state is owner-defined scaffold state; it is not reconstructed by scanning maximum existing IDs.
5. No blank routing companion grants PLAYER authorization, temporal lifecycle, LIVE authority or fictional state.
6. Generator output remains one coherent package scaffold that can be published from scratch by RD-14 Task 4.
7. Story/T0 remains conditional and is not added to this mandatory blank-scaffold join.

---

# 4. Interaction with RD-16 late topology validation

F40 does not replace the existing late RD-16 -> RD-14 topology/scaffold validation join.

The two checkpoints prove different things:

```text
RD14_BLANK_SCAFFOLD_INPUTS_READY
    = fixed mandatory blank template products exist before generator validation

RD16 shared machine integration
    -> RD14 late final topology/scaffold validation
    = final 17-family/catalog/strict-schema topology consumed and projected coherently
```

The early generator may be implemented/tested once all fixed blank-scaffold contracts are ready. Final RD-14 package/product closure still waits for the later RD-16 topology integration where required.

If a later semantic repair introduces another **mandatory blank scaffold artifact**, its owner must add a producer-local scaffold checkpoint and join it into `RD14_BLANK_SCAFFOLD_INPUTS_READY`; workers may not silently extend the template outside the graph.

---

# 5. Required tests / proof

Add an RD-14 focused group conceptually:

```text
BlankScaffoldCompletenessTests
```

Required cases:

1. generated blank campaign contains schema-valid `STATE/ID_ALLOCATOR.yaml`;
2. generated blank campaign contains schema-valid explicit-empty `STATE/RUNTIME/TEMPORAL_ROUTING.yaml`;
3. generated blank campaign contains schema-valid explicit-empty `STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml`;
4. generated blank campaign contains schema-valid explicit-empty `STATE/RUNTIME/LIVE_ROUTING.yaml`;
5. absence of any mandatory blank product blocks `RD14_GENERATOR_SCAFFOLD_VALIDATION_READY` rather than being patched post-generation;
6. empty temporal/principal/LIVE companions grant no semantic authority and are distinguishable from missing/corrupt artifacts;
7. allocator singleton is generated from package owner state, never inferred from directory/index/max-ID enumeration;
8. exact campaign/package/ruleset identity propagation remains unchanged;
9. Story/T0 is not required solely to satisfy blank-scaffold completeness;
10. the early blank-scaffold join does not require RD-16 final machine integration or `RD09_SOURCE_NATIVE_ID_READY` and therefore does not create the known RD-14 -> RD-09 -> RD-16 -> RD-14 cycle;
11. F58 operational-root FORMAT.yaml survives exact generation at local version 1 with empty active-only namespaces; absence/corruption is not patched after generation, and the marker grants no root lifecycle/currentness/completeness authority.

Cross-owner proof must validate the **actual generated bytes**, not only the presence of template files in the repository.

---

# 6. Execution graph amendment

Add to Tier F product/scaffold integration:

| Producer | Join target |
|---|---|
| RD04_ALLOCATOR_SCAFFOLD_READY | RD14_BLANK_SCAFFOLD_INPUTS_READY |
| RD08_TEMPORAL_ROUTING_SCAFFOLD_READY | RD14_BLANK_SCAFFOLD_INPUTS_READY |
| PRINCIPAL_PLAYER_ROUTING_SCAFFOLD_CONTRACT_READY | RD14_BLANK_SCAFFOLD_INPUTS_READY |
| RD09_LIVE_ROUTING_SCAFFOLD_CONTRACT_READY | RD14_BLANK_SCAFFOLD_INPUTS_READY |
| RD07_OPERATIONAL_ROOT_CONTRACT_READY | RD14_BLANK_SCAFFOLD_INPUTS_READY |

`RD14_BLANK_SCAFFOLD_INPUTS_READY HARD_PRECEDES RD14_GENERATOR_SCAFFOLD_VALIDATION_READY`.

Retain separately:

```text
RD14_CAMPAIGN_IDENTITY_CREATION_READY
  -> F25/RD09 source-native identity join

RD16 SHARED_MACHINE_INTEGRATION
  -> RD14 late final topology/scaffold validation
```

No whole-RD serialization is introduced.

---

# 7. Recovery/currentness consequence

Because missing completeness companions have fail-closed semantics after campaign creation, RD-07/bootstrap resume may rely on RD-14 blank-scaffold proof only as evidence that **newly generated v1 campaigns start structurally complete**. Current runtime recovery must still load and validate the exact current companions; scaffold provenance never substitutes for current bytes.

---

# 8. Non-goals

This repair does not:

- create a global scaffold owner;
- make blank companion files semantic authority;
- require Story/T0 at New Game;
- serialize all of RD-04/RD-08/RD-09 before RD-14;
- require final LIVE implementation before blank LIVE-routing schema/template readiness;
- require final RD-16 machine integration before the early generator task;
- add a post-generation repair phase;
- authorize gameplay bootstrap or production implementation.

---

## Disposition

```text
AUTHOR_GRAPH_FINDING_40: REPAIRED_IN_PLANNING
SEVERITY: SIGNIFICANT
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```

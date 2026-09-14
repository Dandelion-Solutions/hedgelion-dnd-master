# HDM Implementation Planning — PLAYER Collaboration Strict-State Integration Amendment

Status: **CURRENT HIGHEST-PRECEDENCE MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **F35 — SIGNIFICANT — WP-17 PLAYER companion can be lost across RD-12 -> RD-16 strict machine integration**

## 1. Finding

WP-17 LAW 28–31 requires every nonterminal collaboration generation to maintain completeness-protected `PLAYER.collaboration_route_refs[]`, and requires obligation generation changes plus all affected PLAYER route refs to publish in one campaign durability closure. The PLAYER companion is routing completeness evidence only; it is not collaboration authority.

RD-12 Task 4 correctly plans the owner-local realization by modifying `GAME/SCHEMA/player.schema.yaml`, collaboration reconciliation code and focused tests.

Later RD-16 creates the final strict `DEV/SCHEMAS/world-player-state.schema.json` and makes `world-record.schema.json` dispatch `world.player` through that strict state schema. RD-16 has a general prohibition on silently omitting owner fields, but its explicit PLAYER realization/tests and `SHARED_MACHINE_INTEGRATION_JOIN` do not currently consume RD-12's collaboration companion delta. The join currently includes RD-08/RD-04/RD-05/RD-09/RD-15 inputs, not RD-12.

Therefore the current graph permits this legal execution order:

```text
RD-16 builds/finalizes strict world.player state without collaboration_route_refs
-> RD-16 reaches machine-integration GREEN
-> RD-12 later adds collaboration_route_refs only to GAME/SCHEMA/player.schema.yaml
```

That leaves two divergent PLAYER machine surfaces and can make the final strict world-record path reject, omit or fail to require the exact completeness companion required by WP-17. A broad statement that owner fields must not be omitted does not establish the missing producer-before-integrator edge.

This is a shared-schema/integration-order defect. It does not reopen PLAYER or collaboration semantics.

## 2. Authority-preserving realization

Semantic ownership remains:

- WP-16 / `world.player`: campaign PLAYER identity, membership, binding, control and authorization semantics;
- WP-17 / RD-12: collaboration routing-companion semantics and obligation relationship;
- RD-16: final physical integration of strict world-family machine schemas/shared machine files.

No new owner is created.

The exact machine realization is:

```text
RD-12 PLAYER collaboration companion delta LOCAL_SEMANTIC_READY
    -> RD-16 PLAYER_STRICT_STATE_INTEGRATION_JOIN
    -> final DEV/SCHEMAS/world-player-state.schema.json
    -> aligned shipped GAME/SCHEMA/player.schema.yaml projection
    -> world-record strict dispatch/conformance GREEN
```

RD-12 remains responsible for the meaning, producer/reconciliation behavior and same-campaign-closure rule. RD-16 only integrates that accepted delta into the final strict machine shape.

## 3. Final strict PLAYER state requirement

`DEV/SCHEMAS/world-player-state.schema.json` must include the WP-17 companion in addition to the already required PLAYER fields.

Conceptually:

```text
collaboration_route_refs: [
  {
    obligation_id: non-empty machine id/string
    generation: non-negative integer
  }, ...
]
```

Required properties/invariants:

1. The field is part of durable campaign-owned `world.player` state, not a session/cache/index field.
2. The collection has deterministic representation and no duplicate `(obligation_id,generation)` pair.
3. It carries routing identity only; it cannot carry obligation lifecycle, accepted input bodies, authorization, control transfer or closure state.
4. A nonterminal required route holder must contain the exact current `(obligation_id,generation)` ref after the coherent campaign publication that establishes that generation.
5. Terminal `RESOLVED`/`OBSOLETE` removes affected refs in the same campaign native-domain closure as the obligation terminal transition.
6. Missing/stale/mismatched refs under an otherwise current PLAYER record are integrity/repair evidence; ordinary recovery does not broaden into a scan of all collaboration records.
7. Empty collection is valid when current completeness proof establishes no matching nonterminal obligation for that PLAYER.
8. The companion is never used to grant PLAYER membership, controlled-PC authority, collaboration input authority or current opportunity authority.

Exact field spelling may follow the final machine convention, but `GAME/SCHEMA/player.schema.yaml`, `world-player-state.schema.json`, RD-12 producer/recovery code and tests must describe the same semantic data and cardinality. A worker may not choose two incompatible encodings without an explicit owner-approved translation contract.

## 4. Shared physical writer/order law

`GAME/SCHEMA/player.schema.yaml` is a shared physical surface between the existing PLAYER projection and RD-12 collaboration realization.

Use one ordered physical integration path:

```text
RD-12 prepares owner-local collaboration companion schema delta
-> RD-12 LOCAL_SEMANTIC_READY (no claim of final PLAYER machine closure)
-> RD-16 fresh-reads current GAME/SCHEMA/player.schema.yaml
-> RD-16 integrates the complete accepted PLAYER shape, including collaboration_route_refs,
   into world-player-state.schema.json and the shipped PLAYER schema projection
-> RD-16 publishes the final PLAYER schema checkpoint
```

RD-12 must not publish a later independent PLAYER-schema edit that can diverge from the RD-16 strict state generation. If implementation scheduling executes RD-12's physical GAME-schema edit before RD-16, RD-16 becomes the final physical writer and must preserve/revalidate it. If scheduling defers the physical edit, RD-12 supplies an exact delta to RD-16. Both paths result in one final generation; there are not two independently final schemas.

This is physical-writer ordering only and transfers no WP-17 semantic ownership.

## 5. Execution-graph amendment

Add the following checkpoint edge; it supersedes only the affected RD-16 PLAYER integration timing:

```text
RD12_PLAYER_COLLABORATION_ROUTE_LOCAL_SEMANTIC_READY
    -> RD16_PLAYER_STRICT_STATE_INTEGRATION_JOIN
```

The existing RD-16 shared integration join becomes:

```text
RD08 thread LOCAL_SEMANTIC_READY
+ RD04 player/faction disposition LOCAL_SEMANTIC_READY
+ RD05 MechanicalEvent identity LOCAL_SEMANTIC_READY
+ RD09/WP16 live_birth table LOCAL_SEMANTIC_READY
+ RD12 PLAYER collaboration-route companion LOCAL_SEMANTIC_READY
+ RD15 catalog-gap family policy input LOCAL_SEMANTIC_READY
+ RD16 strict world-family schemas ready
    -> RD16 SHARED_MACHINE_INTEGRATION_JOIN
```

This does not require all RD-12 collaboration behavior to finish before unrelated RD-16 quiet-family schema preparation. Only final PLAYER/shared-machine integration waits for the named owner-local delta.

No RD-16 -> RD-12 semantic dependency is introduced, so this does not create a cycle.

## 6. Required tests / proof

Extend `DEV/TESTS/test_rd16_world_family_machine_integration.py` with a focused group, conceptually:

```text
PlayerCollaborationStrictStateIntegrationTests
```

Required cases:

- final `world.player` strict state admits the exact WP-17 collaboration route-ref field;
- required/property sets do not silently omit it when the current PLAYER owner contract includes it;
- duplicate `(obligation_id,generation)` refs reject;
- invalid generation/identity shape rejects;
- strict world-record dispatch validates a PLAYER carrying current collaboration refs;
- shipped `GAME/SCHEMA/player.schema.yaml` and strict world-player schema agree on field meaning/cardinality;
- route refs cannot satisfy/close an obligation, authorize an input, grant PLAYER authority or transfer control;
- terminal collaboration transition plus ref removal is represented as one RD-06 campaign native-domain publication input, not two independently publishable closures;
- corruption/mismatch blocks or enters bounded repair handling and does not authorize broad ordinary scan fallback.

Re-run RD-12 focused owner tests after the final RD-16 integration:

```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.PlayerRouteCompanionTests -v
python3 -m unittest DEV.TESTS.test_rd16_world_family_machine_integration.PlayerCollaborationStrictStateIntegrationTests -v
python3 -m unittest DEV.TESTS.test_rd16_world_family_machine_integration.WorldStateSchemaCoverageTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

All committed tests are GREEN before the coherent final PLAYER/shared-machine checkpoint is publication-eligible.

## 7. Coverage / proof consequences

Forward route:

```text
WP17-28..31
 -> RD-12 Task 4 producer/reconciliation/same-closure semantics
 -> RD12_PLAYER_COLLABORATION_ROUTE_LOCAL_SEMANTIC_READY
 -> RD-16 strict world.player final physical integration
 -> RD-06 campaign native-domain publication
 -> RD-07/current PLAYER recovery + direct obligation dereference
 -> item-bound integration proof
```

Reverse route from final `world-player-state.schema.json` must recover both:

- WP-16 PLAYER binding/control owner fields;
- WP-17 collaboration-route completeness companion fields.

The post-graph proof witness set gains logical row `PG33`:

```text
PG33  WP-17 PLAYER collaboration companion survives final strict world.player integration
      -> PlayerCollaborationStrictStateIntegrationTests
      -> STATIC_AUDIT + INTEGRATION_SCENARIO
```

`R018WorldFamilyProofTests` for `world.player` is not complete unless this current owner field is included in the final strict schema/property comparison. Generic family presence, `status+controlled_pc_ids` alone, or the shipped PLAYER schema alone is insufficient.

## 8. Version / system impact

Implementation must classify the actual schema-version impact after fresh-reading the current unreleased schema generations. The plan does not invent a version number here.

Because the v1 tree is clean-slate/pre-release, no compatibility shim is required solely to preserve an obsolete pre-release PLAYER shape. Nevertheless all current shipped/runtime consumers of PLAYER must be updated coherently to the one final accepted shape.

System impact is bounded to existing PLAYER/collaboration/schema integration. No Product Owner decision, new readiness ID, new RD or new semantic family is required.

## 9. Disposition

```text
F35: REPAIRED_IN_PLANNING
WP17_PLAYER_ROUTE_COMPANION_IN_FINAL_STRICT_STATE: REQUIRED
RD12_TO_RD16_PLAYER_INTEGRATION_EDGE: REQUIRED
INDEPENDENT_FINAL_PLAYER_SCHEMA_WRITERS: FORBIDDEN
NEW_RD: NO
NEW_SEMANTIC_OWNER: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

This is an author-side repair and remains independently unconfirmed. The broader graph audit continues; this amendment does not authorize Senior handoff.
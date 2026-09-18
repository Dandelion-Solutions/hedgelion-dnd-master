# HDM v1 Implementation Wave 06 — Proof and Senior Handoff

Status: **PLANNED / PROOF-AFTER-TARGET + FINAL SENIOR HANDOFF**

Goal: prove the realized package at one exact remote HEAD, reconcile every active/trigger/no-work readiness disposition, validate the execution graph and version cutovers, and hand the implementation result to an independent Senior reviewer.

Use `implementation-plan-execution-contract.md`. Proof follows the mechanism it proves. A class name, file existence or green unrelated suite is not evidence by itself.

## Entry and exit

Each proof becomes eligible when its named target checkpoints are GREEN and published; there is no whole-wave entry barrier for an unrelated proof or owner-local task. W06.T01 and W06.T06 perform the complete-package checks after all required writers. Exit requires complete local and hosted evidence for the same exact HEAD plus independent Senior integration review. Until that review returns PASS / GO and `DEV/CURRENT_PROGRESS.md` records it, release/migration/gameplay bootstrap remain unauthorized.

Minimum wave impact envelope:

- owners: proof ledger, test suites, maintenance audit, execution/coverage graph projection, version witnesses, hosted result and durable handoff cursor;
- protected invariants: no proof substitutes for behavior, no stale/cached HEAD, no inferred coverage from counts, no test-name-only closure and no proof-to-target dependency cycle;
- allowed product changes: none unless validation exposes a concrete defect; repair returns to the owning wave task and repeats its RED/GREEN/checkpoint loop.

## W06.T01 — Complete owner and integration suites

Run every owner suite named by Waves 01–05 after all physical writers are complete. Confirm that the class exists, executes non-zero assertions and exercises its claimed mechanism. At minimum:

- `test_rd01_shipped_projection_repairs.py`;
- `test_rd02_information_native_contracts.py`;
- `test_rd03_actor_asset_effect_continuity.py`;
- `test_rd04_native_routing_index_hot.py`;
- `test_rd05_runtime_execution.py`;
- `test_rd06_durability_publication.py`;
- `test_rd07_recovery.py`;
- `test_rd08_temporal.py`;
- `test_rd09_access_live.py`;
- `test_rd10_role_emission.py`;
- `test_rd11_context_runtime.py`;
- `test_rd12_collaboration.py`;
- `test_rd13_story_t0_commentator.py`;
- `test_rd14_bootstrap.py`;
- `test_rd15_catalog_runtime.py`;
- `test_rd16_world_family_machine_integration.py`;
- `test_r2_7_wp03_catalog_conformance.py`.

For each suite, record command, assertion/test count, exact result and checkpoint(s) discharged. An expected empirical/supported-target trigger that remains dormant is recorded as `EMPIRICAL_DEFERRED`, not silently counted as GREEN.

Output checkpoint: `W06_OWNER_SUITES_GREEN`.

## W06.T02 — Readiness and composite proof ledger

Complete `DEV/TESTS/test_implementation_proof_ledger.py` against the realized targets. Preserve these proof classes:

`Stage3PackageProofTests`, `ActorReadinessProofTests`, `DomainCommitmentProofTests`, `ExecutionRetryProofTests`, `RoleContainmentProofTests`, `ContextBoundednessProofTests`, `Wp12HotProofTests`, `OwnerFirstReconciliationProofTests`, `ProofChannelDisciplineTests`, `Wp13DurabilityProofTests`, `Wp14RecoveryProofTests`, `Wp15TemporalProofTests`, `Wp16LiveAccessProofTests`, `Wp17CollaborationProofTests`, `T0HistoricalBasisProofTests`, `CommentatorSelfContainedProofTests`, `CompositeR006ProofTests`, `CompositeR016ProofTests`, `CompositeR018ProofTests`, `CompositeR029ProofTests`, `CompositeR053ProofTests`, `CompositeR062ProofTests`, `CompositeR087ProofTests`, `CompositeR122ProofTests`, `CompositeVersionImpactProofTests`, `R018WorldFamilyProofTests`, `R018RuntimeFamilyProofTests`, `SharedSchemaStorageReadmeIntegrationProofTests`, `CoreFrameworkModuleVersionCutoverTests`, `RetainedSchemaVersionCutoverTests`, `PostGraphPackageRoutingProofTests`, `PostGraphCheckpointCoherenceProofTests`, `PostGraphCoverageCurrentnessProofTests`, `PostGraphProofRoutingTests`, `PostGraphExecutionGraphProofTests`.

Reconcile against the canonical WP-27 ledger:

```text
145 readiness records total
133 active = 116 direct + 9 pure proof + 8 composite parents
12 trigger-gated
79 explicit no-work source terminals
R004 absent
```

Every active record points to an executed task/checkpoint and evidence channel. Every trigger-gated record retains its exact dormant trigger and cannot be activated by wave placement. Every no-work terminal retains its reason. Counts are cross-checks; item-level mapping is authority.

### Exact runtime-family proof and negative witnesses

`R018RuntimeFamilyProofTests` in `DEV/TESTS/test_implementation_proof_ledger.py` consumes the exact 17-row runtime-family realization matrix in Wave 05. Create and turn these witnesses GREEN only when their realized targets exist; do not publish future-task RED tests. Primary evidence channels: `STATIC_AUDIT + INTEGRATION_SCENARIO`.

For every row, prove all of the following against final published bytes:

1. Exact accepted family membership, with no missing, duplicate or unowned extra member.
2. Resolution to every named final schema/machine-shape surface, including shipped projections and an admitted concrete Procedure subtype where applicable. No current row has a no-durable-record exemption.
3. The exact native root/exceptional route from the matrix and current WP-11 owner, independently of a valid record body.
4. Strict validation of the complete owner-native identity/state contract, not merely a generic untyped object envelope.
5. Compatibility with the final identifier/live-birth policy: `runtime.id_allocator` stays a fixed exceptional singleton; SOURCE_NATIVE_LIVE never falls back to that allocator.
6. An executable owner-native producer/consumer realization route, with the matrix's exact checkpoints and final-schema writers. Catalog admission alone is insufficient.
7. Rejection of missing schema, family/schema mismatch, wrong root, duplicate/extra family and any count-only substitute.

Required negative fixtures, each with an assertion that the corresponding row/proof fails:

| Negative fixture | Required rejection |
|---|---|
| Delete one required row and keep the count at 17 by substituting a duplicate or unowned extra member | Exact set/row mismatch fails despite count equality; test both duplicate and extra substitutions |
| Map one runtime family to another family's schema | Family/schema binding fails even if that schema validates its own body |
| Use a wrong WP-11 root with an otherwise valid native body | Root/route proof fails |
| Route `runtime.id_allocator` as a hashed ordinary native record | Exceptional fixed `STATE/ID_ALLOCATOR.yaml` law fails |
| Admit a catalog kind whose final schema is absent | R018 realization proof fails despite catalog presence |
| Supply only a 17-member census with no per-row schema/root/realization evidence | Count-only closure fails |

The integration join is:

```text
W05_OWNER_LOCAL_STRICT_SCHEMA_WRAPPER_INPUTS_READY
    -> JOIN_BEFORE_INTEGRATION -> W05.T02
    -> RD16_SHARED_MACHINE_INTEGRATION_READY

W01_INFORMATION_OWNER_READY + W01_NATIVE_ROUTING_READY
+ W02_CATALOG_BACKED_COMMAND_READY + W02_DETERMINISTIC_EXECUTION_READY
+ W02_EXACT_RECOVERY_READY
+ W04_COLLABORATION_PUBLICATION_READY + W04_NATIVE_HISTORY_PUBLICATION_READY
+ W01_CATALOG_CONTEXT_READY + W02_DURABILITY_PUBLICATION_READY
+ SESSION_SCHEMA_FINAL_INTEGRATION_READY + W05_RETAINED_SCHEMA_CUTOVERS_READY
+ RD16_SHARED_MACHINE_INTEGRATION_READY
    -> PROOF_AFTER_TARGET -> R018_RUNTIME_FAMILY_PROOF_READY (W06.T02)
```

The world proof independently waits for its final world schemas, wrapper/identifier integration and `RD16_PLAYER_STRICT_STATE_INTEGRATION_READY`, then produces `R018_WORLD_FAMILY_PROOF_READY`. The catalog-gap behavioral chain uses W01.T08 -> W02.T05 -> W02.T06 with W05.T02's final shared binding, and produces `RD15_CATALOG_GAP_BEHAVIORAL_FAMILY_WITNESS_READY` here. Its matrix row proves schema/root realization; its separate behavioral witness must prove producer/publication/recovery and cannot be replaced by that row.

`CompositeR018ProofTests` requires `R018_WORLD_FAMILY_PROOF_READY` + `R018_RUNTIME_FAMILY_PROOF_READY` + `RD15_CATALOG_GAP_BEHAVIORAL_FAMILY_WITNESS_READY` + the current route/identity/shared-integration prerequisites. Assert that the composite fails when any required proof is missing, even if the world-only proof, catalog-gap-only witness, 17 admitted catalog names, bidirectional name list or aggregate 17+17 census is GREEN.

Final integrated 17x17/R018 evidence is produced only after the W05.T02 shared write and the affected final schema writers. It is never an input to W05.T01 or W05.T02. No semantic owner or runtime registry is introduced by this proof fixture.

Output checkpoints: `R018_WORLD_FAMILY_PROOF_READY`, `R018_RUNTIME_FAMILY_PROOF_READY`, `RD15_CATALOG_GAP_BEHAVIORAL_FAMILY_WITNESS_READY` and, after all readiness/composite obligations, `W06_READINESS_PROOF_READY`.

## W06.T03 — Post-WP27 proof matrix PG06–PG37

Execute and record the following integration rows against actual mechanisms:

| Row | Required proof |
|---|---|
| PG06 | temporal routing completeness and recovery |
| PG07 | additive LIVE, exhaustive birth and multi-LIVE transition |
| PG08 | exact world-family reconciliation |
| PG09 | principal-to-PLAYER route and no ordinary scan fallback |
| PG10 | `MechanicalEvent (segment_id,event_ordinal)` identity and allocator exclusion |
| PG11 | catalog bind and typed gap evidence |
| PG12 | strict 17 world schemas |
| PG13 | one shared catalog writer |
| PG14 | shipped adjudication catalog binding |
| PG15 | one current package router |
| PG16 | one native PLAYER key |
| PG17 | checkpoint coherence |
| PG18 | catalog-backed command acceptance requires exact catalog context basis |
| PG19 | coverage currentness: 16 owner lanes, 17+17 families and historical readiness accounting |
| PG20 | proof routing to realized targets |
| PG21 | acyclic execution graph |
| PG23 | catalog context basis and reconstruction |
| PG24 | source-native ID, cursor and encoding |
| PG25 | canonical campaign identity and immutability |
| PG26 | deterministic multiple-creation ordering |
| PG27 | LIVE epoch identity and route/body tuple |
| PG28 | opening preparation idempotency and ambiguous acknowledgement |
| PG29 | complete LIVE opening seed |
| PG30 | completeness-protected LIVE routing companion |
| PG31 | lossless native packing and idempotent absorption |
| PG32 | exact Wave-05 17-row family -> final schema/machine shape -> native root/exceptional route -> owning realization mapping, proved by W06.T02 `R018RuntimeFamilyProofTests` / `R018_RUNTIME_FAMILY_PROOF_READY`, including every named negative fixture; census/catalog presence alone cannot close the row |
| PG33 | PLAYER collaboration strict-state integration |
| PG34 | LIVE temporal handoff |
| PG35 | operational-root enrollment, publication, LIVE handoff and cold recovery |
| PG36 | access-policy mutation, collaboration reconciliation, publication and current consumers |
| PG37 | exact accepted adjudication basis resolution, acceptance, publication and historical recovery |

There is no PG22. The historical Finding 22 was a witness-routing rule, not a proof-row identifier; do not invent the missing number.

Each row records target checkpoint(s), primary evidence channel, exact test/assertion or static byte check and failure disposition. Static conformance cannot replace the behavioral chains in PG28, PG31 and PG35–PG37.

Output checkpoint: `W06_POST_WP27_PROOF_READY`.

## W06.T04 — Negative law, currentness and stale-surface audit

At the exact candidate HEAD, run static and behavioral checks for absence of:

- duplicate gameplay, history, knowledge, chronology, authorization, currentness or recovery authority;
- email identity, login-only takeover/transfer or generic PLAYER_INDEX authorization;
- broad ordinary scans, latest-looking selection or physical ordering as authority;
- visibility-to-knowledge and recipient leakage;
- accepted-mechanics replay, RNG reroll or identity reallocation;
- prepared LIVE treated as current, incomplete route companion or lossy absorption;
- global active-player, campaign clock, universal pending queue, publication journal, durability frontier or cross-owner transaction;
- old `MANIFEST.players.player_ids` consumers;
- v0.8 migration/dual-read aliases created solely for superseded pre-release shapes;
- stale references to retired implementation-plan files or a second current package router;
- force update or branch/ref deletion behavior.

All positive current routes must resolve from the repository at the tested HEAD. Record exact search scopes and explain legitimate historical/provenance occurrences rather than using an unbounded string count as proof.

Output checkpoint: `W06_NEGATIVE_CURRENTNESS_AUDIT_READY`.

## W06.T05 — Version, shared-writer and graph verification

Run `DEV/TESTS/test_implementation_package_version_cutovers.py` and the matching proof-ledger classes. Verify:

- all eleven retained schema targets in the package index;
- all sixteen material CORE targets in the package index;
- one final writer for every shared file/checkpoint in the execution contract;
- all required semantic deltas are present in actual final bytes;
- no final target is written again by a downstream task;
- dependency graph is acyclic and every consumer points to a producer checkpoint;
- proof edges are `PROOF_AFTER_TARGET` and never prerequisites of their own mechanism.

If an accepted intervening commit advanced a namespace, verify the reconciled transition and owner law rather than blindly asserting the old source number. Any unplanned breaking surface returns to the Version/System Impact gates.

Output checkpoint: `W06_VERSION_GRAPH_READY`.

## W06.T06 — Full exact-head validation and hosted evidence

On a clean view of the published candidate HEAD:

1. run the repository maintenance audit required by `AGENTS.md` and the development process;
2. run `python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'`;
3. run any current exact package/validator commands named by the canonical owners;
4. publish only through non-force compare-and-swap semantics;
5. read back remote ref, commit, tree and representative changed bytes;
6. obtain hosted CI for that exact commit where the repository provides it;
7. compare hosted commit SHA and test results with the handoff SHA.

A green run on another SHA is not evidence. Missing hosted infrastructure is recorded explicitly and cannot be silently labeled GREEN; the independent Senior decides whether the available exact-head evidence satisfies the required gate.

Output checkpoint: `W06_EXACT_HEAD_VALIDATED`.

## W06.T07 — Independent Senior integration handoff

Prepare a self-contained handoff containing:

- exact candidate SHA and parent;
- stable package entry point;
- realized checkpoint list and execution graph;
- readiness accounting and trigger-gated dispositions;
- owner/integration/full-suite and hosted results;
- PG06–PG21 and PG23–PG37 evidence;
- version and shared-writer table;
- current negative/stale-surface findings;
- any residual limitation, exact reopen trigger and responsible owner.

The reviewer fresh-reads the public branch and judges the complete integrated package independently. On findings, route each repair to the owning wave task, reproduce it with RED evidence, implement/publish/verify, and resubmit the exact new HEAD. On PASS / GO, update `DEV/CURRENT_PROGRESS.md` with the reviewed SHA and authorized next unit. Do not infer release or gameplay authorization beyond the explicit recorded decision.

Output checkpoint: `W06_INDEPENDENT_SENIOR_HANDOFF_COMPLETE`.

## Wave 06 completion evidence

This wave closes only with item-level readiness/proof evidence, all named suites and audits GREEN, remote read-back, exact-head hosted disposition and independent Senior result recorded durably. The traceability file remains consolidation provenance and cannot close an implementation or proof row.

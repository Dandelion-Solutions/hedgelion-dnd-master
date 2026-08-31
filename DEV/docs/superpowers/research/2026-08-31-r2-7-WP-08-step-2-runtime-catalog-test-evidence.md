# R2.7 WP-08 Step 2 — Runtime, Catalog and Test Reverse Evidence Slice

Status: **STEP-2 EVIDENCE SLICE COMPLETE — REVERSE RUNTIME/CATALOG/TEST RECONCILIATION**

Date: 2026-08-31

## Sources read

- `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`
- `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`
- `DEV/ARCHITECTURE/ACTOR_MODEL.md`
- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/mechanical-surfaces.json`
- `DEV/CATALOG/catalog-admission-ledger.json`
- `DEV/SCHEMAS/runtime-*.schema.json`
- `DEV/TESTS/test_s6d_04_mechanical_context_contract.py`
- `DEV/TESTS/RUNTIME_CONTEXT_RESEARCH_CASES.md`
- `DEV/TESTS/test_step_5_0_contamination.py`

All were opened on published ref
`38d057a485990b3ff8aa310df42bfd3ae3eee376`.

## Reverse findings

| ID | Actual surface and claim | WP-08 classification | Disposition |
|---|---|---|---|
| M01 | `core-catalog.json` registers `world.knowledge`, `value.actor_proposal`, `value.preparation_draft`, `value.story_projection_draft`, `value.narration_result`, Actor continuity lifetimes, cognition purposes and logical role vocabulary. | Closed vocabulary/identity carrier. A registry entry is not a role phase, RoleContextBundle, handoff authorization or execution authority. | SATISFIED vocabulary support; no authority promotion |
| M02 | `entity-structures.json` treats `world.actor.continuity` and `world.knowledge` as separate world-record structures. | Directly compatible with R2.2 source-Actor private continuity versus Step-4 proposition stance; it neither makes cognition ambient nor changes R2.3 eligibility. | SATISFIED structural separation |
| M03 | `ACTOR_MODEL.md` gives `world.actor` one sparse `continuity` block, excludes durable `transient_private`, rejects chain-of-thought/strategy DAG/every generated thought, keeps `world.knowledge` and human disclosure separate, and requires explicit registered selectors/accessors for a future mechanical continuity consumer. | This is existing R2.2/R2.7 machine alignment for Actor data. It is not a role-phase runtime or permission to use private continuity without an eligible request. | SATISFIED R2.2 data alignment; F01/F02 remain open |
| M04 | `catalog-admission-ledger.json` maps Actor continuity lifetimes/purposes/relationships to R2.2 owners and marks their downstream machine realization as retained with named R2.x/R2.7 owners. | Confirms no independent S6D owner is being invented. | NO_DUPLICATE_OWNER |
| M05 | `MECHANICAL_CONTEXT.md` is canonical S6D-04 only for bounded mechanical accessors, invocation facts and dependency graph. It explicitly makes its contexts/caches disposable and denies runtime domain-query/role-context ownership. | Similar word “context” is not a bridge to R2.3 RoleContext Runtime. Reusing it as role eligibility/trace authority would be an authority error. | OUT_OF_SCOPE for WP-08 role context; retain boundary |
| M06 | `MECHANICAL_RUNTIME_PROPOSAL.md` has status PROPOSAL and implementation not started. It says existing CORE contracts remain authoritative until later deliberate integration. | It is noncanonical proposal evidence, cannot define WP-08 owner or discharge mapping/test obligations. | HISTORICAL/PROPOSAL; no authority |
| M07 | The inspected `runtime-*.schema.json` and S6D test establish mechanical invocation-generation/context-fact contracts and structural non-execution authority. | Candidate implementation-only machinery may be considered only through a future explicit interface; no evidence maps it to RoleContextRequest, TurnEnvelope or Narrator fencing. | IMPLEMENTATION-ONLY; no false reuse |
| M08 | Current context research tests prove full CORE cache/activation/lazy campaign loading. Contamination test proves narrow catalog/schema retirement. | Existing tests do not establish R2.6 containment/lawful-later-use, phase rebind, typed handoffs, bundle/trace protection, or Narrator emission fencing. | VERIFICATION_OBLIGATION |
| M09 | No inspected catalog/schema/runtime surface is a persistent hidden-reasoning, raw private-bundle or generic role-memory authority. | Compatible negative result for R2.1/R2.3/R2.4. Scope is this exact reverse-audit set, not a claim of global textual absence. | NO_DELTA |

## Architecture-to-machine reconciliation

| WP-08 obligation | Evidence result |
|---|---|
| R2.1 source escalation / no hidden reasoning | compatible guidance and Actor data boundary; exact runtime selection/instruction route still unmapped |
| R2.2 Actor private continuity / `world.knowledge` separation | existing Actor/catalog/entity alignment is sufficient at data-owner level |
| R2.3 request/profile/bundle/trace/outcomes | no current machine authority identified; implementation obligation remains |
| R2.4 TurnEnvelope/rebind/minimum typed transport | no current runtime authority identified; implementation obligation remains |
| R2.6 explicit active-role/lawful-later instruction | CORE activation supports a destination hierarchy, but exact owner/text/test mapping remains WP-07/F06 carry-in |
| Narrator/Chronicler/EMISSION_COMMIT | existing catalog values and adjacent canonical owners exist; exact current runtime wiring and verification remain open |

## Conclusion

The reverse audit finds no contradiction and no material human decision. Existing
R2.2 data realization is compatible and must be preserved. The missing R2.3/R2.4/
R2.6 mappings are deterministic implementation/verification obligations under
existing owners, not evidence for a new architecture. Step 2 may now consolidate
the three evidence slices and produce the Step-3 Decision Brief.

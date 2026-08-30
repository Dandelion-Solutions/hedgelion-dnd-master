# S6D-03 — Complete Calculation Selector Metadata — Whole-Project Brief Critic

Status: **CRITIQUE COMPLETE — PASS AFTER REPAIR**

Date: 2026-08-25

Reviewed base ref: `v1/engine-rearchitecture@f01e30e5560e790449153ad6c7b1aeeef00b5eed`

Reviewed artifact: `2026-08-25-s6d-03-complete-calculation-selector-metadata-task-brief.md`

Reviewer stance: independent Step-1 whole-project critic under both design-process owners.

No Step-2 research, selector decision, machine-contract edit or publication was performed by the critic.

## Whole-project routes checked

The critic reconstructed the relevant dependency subgraph through `DEV/PROJECT_MAP.md`, including:

- process, roadmap, S6D owner decision, parent Task Brief and plan;
- S6D-01 package/catalog identity and S6D-02 catalog-admission owner/ledger;
- Rule Element, Activity, accepted Step-2 selector/query and assurance owners;
- execution, Resolution/Continuation, House Rules and adjudication boundaries;
- core catalog, mechanical surfaces, schemas, examples and tests;
- domain rules/seed/package and recovery consumers;
- downstream S6D-04/05/06/07–09/11 ownership.

## Findings

### BC-01 — Operations without a selector pair could escape item-level coverage

Severity: **SIGNIFICANT**

The draft required accounting for 26 `rule.*` operations, but its only operation product was a compatibility matrix for pairs already legal or claimed. Nineteen dormant operations could therefore evade owner/evidence/applicability/disposition analysis.

Required repair: add a separate per-operation evidence ledger for all 26 IDs, retain the pair matrix as a second product, and require exact registry equality in evidence, verification and exits.

Resolution: **ACCEPTED AND APPLIED.** The final brief contains the separate 26-ID ledger and exact set-equality gates.

### BC-02 — Selector-operation value contract could steal S6D-05 payload scope

Severity: **SIGNIFICANT**

“Exact value contract” was not bounded against S6D-05, allowing either portable-schema scope theft or false nominal closure.

Required repair: distinguish S6D-03 semantic compatibility from S6D-05 serialized payload realization. S6D-03 owns nominal value-kind reference, semantic/range/unit/cardinality constraints, normalization and contribution/result compatibility. Each pair names an existing portable-value owner or a precise S6D-05 obligation; payload members remain out of scope.

Resolution: **ACCEPTED AND APPLIED.** Evidence products and full-loop exits now enforce this boundary and prohibit certifying an unresolved portable shape.

## Re-review

The critic re-read the exact repaired brief and whole-project framing.

Final verdict: **PASS — zero unresolved BLOCKING or SIGNIFICANT findings.**

The repaired brief does not execute selector activation decisions, choose resolver semantics, define dependency edges, or begin S6D-04.

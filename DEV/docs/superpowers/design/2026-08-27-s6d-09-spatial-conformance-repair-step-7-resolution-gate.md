# S6D-09 Spatial Conformance Repair — Step 7 Resolution Gate

Status: **PASS — READY FOR CANONICALIZATION**

Date: 2026-08-27

## Gate result

The narrow repair satisfies the Senior Auditor HOLD without reopening Decision C or Step 3. No human product decision is required.

Accepted resolution:

- bounded target/range/area applicability is `route.spatial_target_applicability`, not `route.procedure_movement`;
- seven exact existing Activities declare their real bounded TargetSpec/AreaSpec contracts;
- fiction-dependent applicability crosses the existing S6D-04 boundary as fixed `fiction.target_reachable` facts with exact consumer, source, candidate, provenance, binding and pinned rules-context identity;
- missing, false, stale, unauthorized, duplicate, ambiguous and unbound facts fail distinctly and create no mutation/event/lifecycle/world truth;
- durable Actor location change requires a current canonical destination `world.location` snapshot;
- within-location repositioning spends Procedure movement only and never creates a micro-location;
- generic visibility/cover, geometry, pathfinding, universal coordinates, global query, campaign scan and action enumeration remain unsupported;
- no dormant primitive is activated.

## Evidence gate

- renewed whole-project critic: PASS, 0 blocking/significant/minor;
- focused S6D-06…09 conformance: 58/58 pass before final read-back run;
- package member and aggregate digests close over the repaired character/gameplay seed;
- source-set and coverage-ledger generation has zero differences, unresolved references, orphan edges or supported gaps.

Step 8 may canonicalize this exact repair. S6D-10 remains not started.



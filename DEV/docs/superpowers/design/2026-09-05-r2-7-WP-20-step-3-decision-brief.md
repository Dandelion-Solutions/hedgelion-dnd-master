# R2.7 WP-20 Step 3 — Decision Brief

Status: **STEP 3 COMPLETE — DECISION READY**

Date: 2026-09-05

Domain: **Engine update / schema evolution / migration**

Inputs:

- completed Step-1 package and mandatory Senior GO;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-step-2-research-architecture-draft.md`;
- accepted clean-slate and versioning law;
- current campaign/storage/ruleset/persistence/recovery/LIVE/access owners.

---

## 1. What are we deciding?

How HDM v1.0+ determines whether an exact released runtime/package can operate on an existing released campaign, when explicit migration is required, how a migration path is selected, which authority may execute it, and what constitutes durable success.

This decision must not collapse independent version namespaces, recreate pre-release compatibility, or introduce a second persistence/currentness authority.

## 2. Why now?

WP-20 is the first R2.7 work package whose domain explicitly owns released-campaign evolution. Later release/validation/operational work needs one finite architecture contract before implementation planning can define migration artifacts, validators and tests.

The accepted versioning normalization supplies identifiers and compatibility axes, but deliberately does not infer migration support. WP-20 must supply the missing composition law.

## 3. Distinguishing requirements

The options are distinguished by these non-negotiable requirements:

1. released v1.0+ compatibility only; no v0.8 burden;
2. independent engine/package/ruleset/catalog/schema/storage namespaces remain independent;
3. exact released asset/provenance identity is immutable evidence;
4. version/generation/Git ancestry does not create compatibility or migration support;
5. existing campaign creator, storage-owner, LIVE, recovery and CAS authority remains controlling;
6. accepted resumable work cannot be rebound to new ambient rules/RNG/context;
7. unsupported newer or insufficient-evidence state fails closed;
8. publication success must be defined by existing authoritative ref/CAS semantics;
9. reverse/downgrade support must be explicit rather than inferred;
10. the design must remain finite and package-local enough for the existing local runtime-package model.

## 4. Credible alternatives

### A — Immutable target-package compatibility envelope + explicit directed migration-edge graph

Each exact target runtime carries finite immutable compatibility/migration support data. A bounded compatibility evidence envelope is built from current campaign/storage/ruleset/schema/accepted-work/LIVE evidence. Compatibility evaluation is finite. Migration follows only declared directed edges and an unambiguous declared path. Publication reuses existing campaign-tree CAS.

**Benefits**

- preserves current ownership/currentness model;
- deterministic and auditable;
- handles multiple independent axes without scalar collapse;
- supports direct-only packages as a simple subset;
- old target releases remain self-describing and immutable;
- no external registry/service dependency.

**Costs**

- each supported released transformation requires explicit metadata/artifact ownership;
- release realization/tests must validate graph closure and ambiguity;
- support policy is visible and cannot be hand-waved from version numbers.

### B — Mutable central compatibility/migration registry

A shared registry answers compatibility and path questions at runtime.

**Benefit:** convenient discovery and centrally changeable policy.

**Costs:** introduces a new mutable authority, availability/currentness/replay problem and network dependency; contradicts the exact local package model; makes an old immutable release dependent on later registry state.

### C — Infer compatibility/path from semantic version, generation or Git ancestry

**Benefit:** minimal metadata.

**Costs:** directly contradicts the accepted versioning law; cannot represent unsupported skips, independent axes, semantic incompatibility or explicit reverse policy; turns provenance/order into accidental authority.

### D — Direct source->target transforms only, never compose edges

**Benefit:** simplest path selector.

**Cost:** forces repeated direct transforms even when two already-supported exact transformations compose safely. It is useful as an implementation/profile choice, but unnecessarily restrictive as architecture law.

## 5. Recommendation

Choose **Alternative A**.

The architecture should be expressed as:

```text
current authoritative source evidence
 + exact immutable target package support
 -> finite compatibility classification
 -> optional explicit directed migration path
 -> existing owner prerequisites
 -> prepared transform + validation
 -> existing single-ref campaign CAS publication
 -> confirmed durable success
```

The migration graph is not a new online service or campaign database. It is finite immutable target-package support data. A release that supports only direct edges remains fully compliant.

## 6. Strongest weakness

The principal weakness is maintenance overhead: released transformations and their predicates must be explicitly specified, packaged and verified. A careless implementation could overengineer this into a generic migration framework.

The mitigation is architectural restraint: no mutable global registry, no graph database, no campaign-stored migration planner, no background service and no requirement to support arbitrary paths. Only actually supported released transitions exist as edges.

## 7. Consequences versus alternatives

| Concern | A: package-scoped explicit graph | B: central registry | C: inferred order | D: direct-only |
|---|---|---|---|---|
| Determinism/replay | strong | registry-state dependent | deceptively weak | strong |
| Existing owner reuse | strong | adds owner | leaks order as authority | strong |
| Independent axes | explicit | explicit | weak | explicit |
| Offline/local package fit | strong | poor | strong | strong |
| Ambiguity handling | fail closed | registry-defined | often hidden | simple |
| Release maintenance cost | moderate | moderate/high operationally | low initially/high risk | potentially high duplication |
| YAGNI | bounded if finite | poor | superficially good but incorrect | good but too restrictive |

## 8. Remaining uncertainty

No current uncertainty changes the architectural choice.

Realization details intentionally remain later work, including:

- exact on-disk migration-edge schema;
- migration artifact language/module layout;
- release-builder validation mechanics;
- exact executable test harness and fixtures;
- support matrix for future releases that do not yet exist.

These are not required to decide the authority/path/publication model.

## 9. What would change the recommendation?

- an accepted product rule that only direct one-step migration may ever be supported;
- a future deployment model in which exact target packages cannot carry the support needed to interpret older released campaigns;
- a new requirement for one atomic transaction spanning independently authoritative repositories/stores, which existing per-owner transactions cannot compose safely.

No such condition exists in current scope.

## 10. Human decision

The accepted Product Owner clean-slate boundary, versioning law and existing authority/currentness owners mechanically determine the choice among the current alternatives. No unresolved product semantic or material trade-off remains.

```text
RECOMMENDATION: ALTERNATIVE A
RECOMMENDATION_CONFIDENCE: HIGH
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

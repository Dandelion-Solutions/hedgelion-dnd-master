# R2.7 WP-20 Step 4 — Collaborative Architecture Review

Status: **STEP 4 COMPLETE — NO ADDITIONAL HUMAN DECISION REQUIRED**

Date: 2026-09-05

Domain: **Engine update / schema evolution / migration**

Reviewed:

- completed Step-2 research/architecture draft;
- Step-3 Decision Brief recommending package-scoped explicit compatibility/migration support;
- accepted Product Owner clean-slate decision;
- current versioning, access, persistence, recovery, LIVE, ruleset and bootstrap owners;
- mandatory Senior Step-1 GO authorizing autonomous continuation through Steps 2–8 unless a genuine human-owned decision fires.

---

## 1. Review disposition

The Step-3 recommendation is accepted for candidate formalization:

> **Use an immutable exact-target-package Compatibility Evidence Envelope plus explicit directed migration-edge support, composed with existing creator/storage/LIVE/recovery/CAS owners.**

No new product choice is hidden in this acceptance. The design follows from already accepted constraints:

- released compatibility begins at v1.0;
- version/generation/source order is not compatibility proof;
- exact released assets are immutable;
- campaign adoption is creator-owned;
- storage default evolution is storage-owner-owned;
- LIVE and currentness owners already constrain safe campaign mutation;
- authoritative campaign publication already has one CAS transaction model;
- unsupported/ambiguous state fails closed.

## 2. Review clarifications incorporated before Step 5

### R4-01 — “Graph” does not imply a service or generic framework

The graph is only the mathematical model of finite directed support edges carried by an exact target package. A target may ship one direct edge, several composable edges or no migration edge at all.

No mutable global registry, graph database, remote compatibility service, background scheduler or campaign-stored planner is authorized.

### R4-02 — Support existence is not a future product promise

WP-20 defines **how** supported released transitions are represented and executed safely. It does not promise that every future released version will migrate every older release.

For any concrete source/target pair, support exists only when exact immutable target support data proves it.

### R4-03 — Storage evolution remains a separate authority axis

`storage_format_generation` may be a prerequisite to campaign work, but storage migration is not folded into creator-owned campaign-tree publication. It remains storage-owner maintenance on the storage-default authority.

If a release requires both, each operation has its own authority and success/failure. One cannot manufacture success for the other.

### R4-04 — Direct compatibility must be affirmative

The absence of a migration edge is not proof of direct compatibility. The exact target must affirmatively prove the relevant source envelope is directly supported; otherwise the result is unsupported or indeterminate.

### R4-05 — Accepted resumable work is part of compatibility, not cleanup

Frozen accepted work cannot be silently “completed by migration” or rebound to target ambient state. Target interpretation compatibility is a prerequisite. If absent, migration blocks until the existing owner supplies a lawful closure/continuation path.

### R4-06 — Reverse migration is a new transition

After an accepted migration, a rollback-by-ref-rewind would bypass chronology/currentness and erase the later authoritative transition. A downgrade must therefore be a separately declared reverse edge and a new forward publication.

### R4-07 — Derived rebuild is bounded by owner class

- authoritative native data: transform only by declared migration scope;
- required branch-persistent derived/index projections: rebuild deterministically from migrated authority inside the prepared target transaction;
- local HOT/runtime caches: invalidate/rebuild only after authoritative publication succeeds;
- owner-specific asynchronous/noncanonical projections: use their existing rebuild/catch-up owners.

## 3. Alternatives review

Alternative B (central registry) remains rejected for duplicate authority/currentness and offline package-model conflict.

Alternative C (ordering/ancestry inference) remains rejected as directly incompatible with accepted versioning law.

Alternative D (direct-only) remains a valid package profile, but not a necessary architecture restriction.

The simplest compliant realization of the accepted architecture is still small:

```text
finite target support table
+ explicit edge records
+ deterministic evaluator
+ existing publication owner
```

Nothing in the architecture requires a general-purpose migration framework.

## 4. Human/PO gate check

No unresolved question affects:

- product semantics;
- compatibility horizon;
- material authority ownership;
- explicit risk acceptance;
- future support commitment;
- hard-to-reverse infrastructure choice beyond already accepted constraints.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
STEP_5_AUTHORIZED_BY_EXISTING_GO: YES
```

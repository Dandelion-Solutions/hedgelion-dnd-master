# HDM Implementation Planning — R047 Current-Surface Reconciliation Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / INDEPENDENTLY UNCONFIRMED**
Date: 2026-09-14
Finding: **AUTHOR FINDING 44 — SIGNIFICANT**
Production implementation: **NO**.

This amendment repairs a currentness/execution defect in RD-01. It changes no accepted domain semantics and creates no replacement module.

## 1. Finding

Historical Step-2 evidence routed `R27-R047` from stale B-prime pre-realization wording in `GAME/CORE/DOMAIN_RULES_COVERAGE.md` and explicitly required repair of the **active stale text only**.

Current planning accidentally converted that historical path into a mandatory production target:

```text
RD-01 RED assertion:
  GAME/CORE/DOMAIN_RULES_COVERAGE.md does not present old blocked/not-materialized wording as current

RD-01 Task 2:
  Modify GAME/CORE/DOMAIN_RULES_COVERAGE.md
```

But the exact current branch does not contain that file. It is also absent at `PLANNING_BASELINE_SHA=85311db76be2e440c97baf0b0625177de2eb0774`.

A bounded repository search at the F44 audit basis found no current `B-prime` or old `not materialized` formulation. The historical stale surface therefore is not a current v1 shipped consumer.

Literal execution of the old RD-01 step would either fail on a nonexistent target or recreate a retired module solely to satisfy historical provenance. Both outcomes violate the package currentness rule and the clean-slate v1 rule.

## 2. Mandatory RD-01 disposition

For `R27-R047`, the current executable disposition is:

```text
CURRENT_V1_STATE: ALREADY_SATISFIED_BY_SURFACE_REMOVAL
ACTIVE_STALE_TEXT_FOUND: NO
GAME/CORE/DOMAIN_RULES_COVERAGE.md: MUST_NOT_RECREATE_FOR_R047
PRODUCTION_MUTATION: NONE
framework_module_version impact: NONE
```

This amendment supersedes only the stale path/action in RD-01. It does not change the other RD-01 direct leaves.

RD-01 Task 1 must replace the old path-existence assertion with a bounded negative/currentness assertion:

1. `GAME/CORE/DOMAIN_RULES_COVERAGE.md` is not required to exist;
2. if absent, the test passes the historical path portion and continues the bounded active shipped-consumer scan;
3. active shipped CORE projections must not contain the historical B-prime blocked/unrealized/not-materialized-as-current semantics;
4. a newly discovered **current active** contradictory consumer is repaired at its actual path and receives its normal module-version impact;
5. historical evidence/provenance documents are not rewritten merely to erase history.

RD-01 Task 2 removes `GAME/CORE/DOMAIN_RULES_COVERAGE.md` from the unconditional `Modify` list.

## 3. No replacement debt

Do not create any of the following solely for R047:

- a new `DOMAIN_RULES_COVERAGE.md`;
- a compatibility alias/path;
- a redirect stub;
- a deprecated placeholder module;
- a module-version tombstone;
- an alternate package/domain authority document.

R047 is a stale-projection obligation, not a requirement that the historical projection continue to exist.

If a future current active module materially restates the forbidden old semantics, repair that real module under its current owner and bump its `framework_module_version` exactly once for the material edit. That future case does not revive this removed path.

## 4. Proof obligation

`DomainExplorationTests` (or the exact current focused RD-01 test class) must prove:

```text
absent historical DOMAIN_RULES_COVERAGE path is accepted
AND active current CORE scan contains no R047 forbidden semantic claim
AND no compatibility/replacement module was created for the historical path
```

This is a negative/currentness proof. It must not fail merely because the retired file is absent.

The R048 `EXPLORATION.md` obligation remains independent and still requires its actual current shipped projection repair/proof if contradictory wording exists.

## 5. Versioning consequence

Because R047 now performs no material edit to a current logical module:

```text
R047 framework_module_version transition = NONE
```

Do not manufacture a Category-B revision bump for an absent module or for an inspect-only negative result.

The wider `framework_module_version` audit remains active for actual material CORE edits elsewhere in RD-01..RD-16/mandatory overlays.

## 6. Finding disposition

```text
AUTHOR_FINDING_44: SIGNIFICANT
ROOT_CAUSE: historical stale path was promoted into an unconditional current production target without exact-current path validation
R047_CURRENT_DISPOSITION: CURRENT_V1_ALREADY_SATISFIED / NEGATIVE-PROOF ONLY
REMOVED_SURFACE_RECREATION: FORBIDDEN
MIGRATION_OR_COMPATIBILITY_STUB: FORBIDDEN
MODULE_VERSION_BUMP: NONE
ARCHITECTURE_REOPEN: NO
HUMAN_DECISION_REQUIRED: NO
REPAIR_STATE: PLANNED IN THIS MANDATORY AMENDMENT
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

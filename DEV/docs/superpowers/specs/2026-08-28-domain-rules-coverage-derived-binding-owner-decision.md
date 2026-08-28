# Domain Rules Coverage Derived Binding — Owner Decision

Status: **OWNER-APPROVED POST-CANONICAL REALIZATION DECISION / IMPLEMENTATION BLOCKED**

Date: 2026-08-28

Applies to:

- `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md`;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md`;
- the current S6D-09 supported-domain coverage machine realization;
- S6D-12 final closure and the later R2.7 resume gate.

## 1. Decision

The owner approves **B′** as the physical realization amendment for supported-domain coverage identity evidence.

`DEV/CATALOG/domain-rules-coverage.json` remains one semantic coverage contract. It is not sharded.

The entire volatile package binding moves out of that semantic artifact into one small strictly-derived companion:

```text
DEV/CATALOG/domain-rules-coverage-binding.json
```

The binding contains exactly:

```text
profile_id
package_id
package_version
catalog_generation
gameplay_spine_member
package_content_sha256
ruleset_set_sha256
```

No `coverage_semantic_sha256` or equivalent coverage digest is introduced. Semantic coverage remains validated by exact equality between the checked-in semantic artifact and the fresh deterministic coverage producer.

## 2. Authority law

Canonical package/set authority remains only:

```text
manifest
-> package snapshot
-> resolved lock
-> ruleset_set_sha256
```

The derived binding is verification evidence only. It may neither select package identity nor repair a mismatch. Validation must fail closed unless the binding equals the current reconstructed package snapshot/resolved lock and the exact expected profile/package/version/catalog/member context.

This decision does not reopen S6D-11 semantic architecture, change its identity algorithm, or introduce a second identity owner.

## 3. Preserved S6D-09 semantics

The S6D-09 completeness law is unchanged:

```text
REQUIRED_COVERAGE_KEYS = union(PACKAGE_CLOSURE_KEYS,
                               ACTIVE_MACHINE_CONSUMER_KEYS,
                               PRODUCT_PROMISE_KEYS)
COVERAGE_LEDGER_KEYS == REQUIRED_COVERAGE_KEYS
```

The split changes only physical placement of volatile package identity evidence. It does not change supported mechanics, product/MVP scope, active primitives, admission, package bytes, compatibility/adoption policy, runtime behavior, or the semantic coverage ledger.

## 4. Rejected alternatives

- Keeping volatile package identity embedded in the large generated semantic artifact is rejected because it preserves the proven maintenance coupling.
- Sharding the coverage contract is rejected as YAGNI: no current partial-loading requirement justifies a distributed semantic ledger/manifest.

These alternatives are closed unless a later current requirement materially changes the evidence.

## 5. Realization checkpoint

```text
architecture decision: B′ APPROVED
architecture semantics: settled
implementation/migration: BLOCKED_BY_EXECUTION_CAPABILITY
missing capability:
  execute deterministic repository producer on verified ref
  and return generated artifact bytes
required before:
  S6D final closure / R2.7 resume
```

The missing capability blocks the one-time coherent v2 -> v3 machine-contract migration. It does not justify manual reconstruction of the large generated artifact, partial migration of the other identity carriers, CI redesign, sharding, or reopening accepted identity semantics.

Until that capability exists, do not partially migrate schemas, producer/validator code, `domain-rules-coverage.json`, or the remaining current identity projections.

## 6. S6D-12 carry-in

S6D-12 may proceed with research and architecture while this realization obligation remains open. Its Task Brief must carry the obligation explicitly and must not spend the stage re-diagnosing the already-established root cause.

S6D final closure and R2.7 WP-06 resume are forbidden until either:

1. B′ is coherently materialized and its focused conformance evidence passes; or
2. a later explicit human owner decision accepts a different disposition.

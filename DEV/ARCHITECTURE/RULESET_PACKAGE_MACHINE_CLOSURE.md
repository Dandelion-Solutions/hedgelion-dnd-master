# HDM Ruleset Package Machine Closure

Status: **CANONICAL S6D-11 ARCHITECTURE / POST-CANONICAL B′ REALIZATION AMENDMENT**

Date: 2026-08-28

## Decision

S6D-11 activates the built-in bounded ruleset package only through the single identity chain defined by RULESET_PACKAGE_IDENTITY.md: strict self-including manifest, exact semantic bytes, builder-derived package snapshot, exact resolved lock and typed `ruleset_set_digest_generation` + `ruleset_set_sha256` identity.

No transitional aggregate digest is an authority. DEV/CATALOG/ruleset-package-closure.json is the item-level migration and activation ledger; its displayed digests are derived verification evidence.

The later B′ owner decision changes only the physical placement of supported-domain coverage identity evidence. It does not reopen S6D-11 semantic architecture or alter this identity chain.

## Builder and loader

GAME/TOOLS/ruleset_package.py is the shipped bounded manifest/lock/comparator contract. DEV/TOOLS/validate_ruleset_package_closure.py is its build-time orchestration owner: it derives the closed engine-contract inventory, proves the transitional census and executes every registered S6D-07…10 package validator before release provenance/activation. It receives explicit roots and package directories and returns an exact reconstructive lock or one closed failure.catalog_context_incompatible reason. No discovery scan, network registry, fuzzy replacement or partial context is permitted.

Package-specific registered validators remain responsible for schema, cross-reference, admission and active-consumer equality. A package is usable only after both the generic loader and every applicable registered validator pass.

## Changed same-version compatibility

A changed typed resolved-set identity is compatible/additive only when the deterministic comparator proves a monotonic canonical semantic-entry superset between independently valid adopted and candidate sets.

Every adopted package identity line, namespace claim, exact dependency and owner-qualified definition/capability/active primitive/selector/accessor/fact/value/schema entry must remain present with identical kind and generation-qualified canonical semantic hash. Exact inputs are derived from both shipped package snapshots, the fixed five-family engine-contract registry and the campaign persistence owner's durable-state/accepted-work dependency frontier. The comparator derives completeness internally; no caller boolean or arbitrary entry map exists. Candidate-only additions must independently load, validate and avoid collision. Missing evidence blocks.

Only COMPATIBLE_ADDITIVE satisfies the changed-set precondition of the existing silent forward same-version runtime refresh. BLOCKED_INCOMPATIBLE and BLOCKED_INSUFFICIENT_EVIDENCE prevent context use and route to creator adoption/migration. Ancestry, package revision, compatibility family/generation, catalog generation and standalone load success are not semantic proof.

## Projections and durability

The generated runtime provenance embeds the exact resolved lock/set digest plus its digest generation and a path-neutral runtime-owned conformance inventory. Build-time DEV paths/results compile into stable family/validator IDs, semantic hashes and a digest-bound attestation; literal DEV topology never crosses the package boundary and cannot become runtime authority. Campaign MANIFEST owns sibling ruleset.created_with/current generation+digest identity; Resolution and Continuation pin the accepted set generation+digest and catalog-context fingerprint generation; checkpoint evidence is projection only. READY_PC and House-Rules realization evidence bind to the set identity through their natural projections. Runtime never reads DEV/.

Supported-domain coverage follows the approved B′ physical realization: `DEV/CATALOG/domain-rules-coverage.json` remains one semantic coverage ledger and carries no package binding after migration; `DEV/CATALOG/domain-rules-coverage-binding.json` is the small strictly-derived verification companion containing only `profile_id`, `package_id`, `package_revision`, `compatibility_family`, `compatibility_generation`, integer `catalog_generation`, `gameplay_spine_member`, `package_content_sha256`, `ruleset_set_digest_generation` and `ruleset_set_sha256`. No coverage-semantic digest is introduced. The S6D-09 validator must prove exact semantic equality to its deterministic producer separately from exact binding equality to the reconstructed package snapshot/resolved lock and fixed profile/package/catalog/member context.

The coverage binding is not an identity owner and cannot choose or repair a set. Canonical authority remains `manifest -> package snapshot -> resolved lock -> typed ruleset-set identity`. Missing or mismatched derived binding evidence fails closed.

The B′ machine migration and the 2026-09-05 version-namespace normalization are realized in the current pre-release machine state. Durable decision provenance remains recorded in `DEV/docs/superpowers/specs/2026-08-28-domain-rules-coverage-derived-binding-owner-decision.md`; historical execution blockers in that evidence remain historical and do not describe current machine status.

## Activation boundary

The current package is ACTIVE_VERIFIED_MACHINE_CONTRACT only after the Step-7 Resolution Gate verifies its exact derived identities, registered validators/tests, transitional-key absence and negative cases. This status does not activate dormant/quarantined content or implement production execution. S6D-12 remains separate.

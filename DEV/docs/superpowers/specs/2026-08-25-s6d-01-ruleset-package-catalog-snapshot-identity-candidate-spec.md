# S6D-01 — Ruleset / Package / Catalog Snapshot Identity — Candidate Specification

Status: **STEP 5 CANDIDATE / NOT YET CANONICAL**

Date: 2026-08-25

## 1. Scope and decision

HDM SHALL represent selected reusable rules definitions through content-addressed semantic package snapshots and a deterministic dependency-closed resolved-set identity. The full `ResolvedCatalogContext` remains derived from engine identity, that ruleset set, and owner-local campaign/session frontiers. No stored global catalog snapshot becomes authority.

This specification defines identity, compatibility/adoption boundaries, projection and failure laws. It does not supply S6D-02 seed content or implement S6D-11 machine closure.

## 2. Terms

### RulesetPackageManifest

Semantic declaration owned by one reusable-definition package:

```text
manifest_schema_version
package_id
package_version
compatibility_id
engine_requirement
catalog_generation
owned_namespaces[]
dependencies[]
content_files[]
```

### RulesetPackageSnapshot

One validated manifest plus exact semantic content bytes and computed `content_sha256`.

### ResolvedRulesetSnapshotSet

One closed, cycle-free set of exact package snapshots satisfying dependencies, namespace ownership and engine/catalog requirements.

### ruleset_set_sha256

Exact order-independent digest of the canonical resolved-set lock.

### catalog_context_fingerprint

Derived digest of the engine capability identity, `ruleset_set_sha256`, exact campaign-definition frontier and optional exact session-overlay frontier. It is equality/retry evidence, not a reconstructive state owner by itself.

## 3. Identity laws

### LAW S6D01-1 — IDENTITY AXES ARE NON-EQUIVALENT

Engine version, catalog generation, runtime package/source provenance, runtime ZIP digest, ruleset package version, compatibility ID, package content digest, resolved-set digest and catalog-context fingerprint SHALL NOT substitute for one another.

### LAW S6D01-2 — PACKAGE CONTENT IDENTITY IS BYTE-DERIVED

`content_sha256` is computed from a domain-separated canonical sequence of normalized package-relative paths and SHA-256 digests of exact file bytes selected by `content_files`. The manifest bytes participate. The digest is not stored inside the hashed manifest and is never inferred from source SHA/tag/version.

Paths SHALL be unique, normalized, package-relative, traversal-free and sorted by Unicode code-point order over their normalized UTF-8 representation. Symlinks and external paths are rejected unless a later explicit package contract safely admits them.

The digest preimage is UTF-8 canonical JSON with fixed member names, no insignificant whitespace and lower-case hexadecimal digests, prefixed by the ASCII domain separator `HDM_RULESET_PACKAGE_SNAPSHOT_V1\n`. YAML presentation order, filesystem enumeration order, timestamps, permissions and archive container metadata do not participate.

### LAW S6D01-3 — RESOLVED-SET IDENTITY IS ORDER-INDEPENDENT

`ruleset_set_sha256` is computed from a domain-separated canonical lock sorted by `package_id`. Loader input/discovery order has no semantic effect.

The set-digest preimage uses the same canonical JSON rules and the ASCII domain separator `HDM_RESOLVED_RULESET_SET_V1\n`.

Each lock entry contains at least:

```text
package_id
package_version
compatibility_id
content_sha256
catalog_generation
dependency package_id -> exact content_sha256
```

### LAW S6D01-4 — EXACT DEPENDENCY CLOSURE

Every declared dependency resolves to exactly one snapshot. Missing dependency, duplicate package ID, incompatible engine/catalog requirement, dependency cycle or ambiguous snapshot is a finite load failure.

### LAW S6D01-5 — NAMESPACE OWNERSHIP IS SET-VALIDATED

Every reusable definition belongs to a namespace claimed by its source package. Overlapping incompatible claims, definitions outside claims and duplicate resolved definition IDs fail admission. No last-layer-wins behavior exists.

## 4. Resolved context laws

### LAW S6D01-6 — ONE LOGICAL CONTEXT, NO GLOBAL SNAPSHOT OWNER

One loader/binder/Resolution uses one logical `ResolvedCatalogContext`. Its fingerprint composes existing owners; it does not copy or outrank them.

### LAW S6D01-7 — CAMPAIGN/SESSION FRONTIERS REMAIN OWNER-LOCAL

Campaign definitions and session overlays participate through exact owner-native revision/dependency refs. They are not silently converted into release packages, copied into the ruleset lock or shadowed by it.

### LAW S6D01-8 — FINGERPRINT IS NOT RECONSTRUCTION AUTHORITY

A `catalog_context_fingerprint` mismatch proves contexts differ. A match supports equality checking. The fingerprint alone does not locate missing package/content/frontier evidence and cannot authorize regeneration or LLM substitution.

## 5. Projection laws

### LAW S6D01-9 — RUNTIME PACKAGE ADVERTISES ITS EMBEDDED LOCK

Builder-generated runtime package provenance SHALL include the exact `ResolvedRulesetSnapshotSet` lock and `ruleset_set_sha256` for the semantic rules packages shipped in that artifact. The final ZIP SHA-256 remains external exact artifact identity.

### LAW S6D01-10 — CAMPAIGN ADOPTION RECORDS RULESET-SET IDENTITY

Campaign MANIFEST SHALL use a sibling `ruleset.created_with` / `ruleset.current` projection rather than hiding ruleset semantics inside `engine`. Each carries at least the selected `ruleset_set_sha256`; later machine realization may include bounded diagnostic package IDs when proved useful. `ruleset.created_with` remains immutable; `ruleset.current` changes only under authorized coherent adoption/refresh rules.

Engine and ruleset projections may change in one coherent adoption transaction, but neither becomes authority for the other.

### LAW S6D01-11 — ACCEPTED EXECUTION PINS EXACT RULESET SET

Accepted Resolution and Continuation generations SHALL retain `ruleset_set_sha256` plus `catalog_context_fingerprint`. Owner-local dependency refs retain any campaign/session definitions required for resume/retry.

Do not add package identity to ordinary world/definition records solely for context reconstruction.

### LAW S6D01-12 — CHECKPOINT IS NONAUTHORITATIVE

Checkpoint/diagnostic evidence may repeat package/context refs for routing, but current campaign and accepted execution owners remain authoritative. Checkpoint absence/staleness never licenses ambient reinterpretation.

## 6. Compatibility and adoption laws

### LAW S6D01-13 — COMPATIBILITY ID IS DECLARATIVE, NOT EXACT IDENTITY

`compatibility_id` identifies a publisher-declared semantic compatibility line. It does not replace `content_sha256` or `ruleset_set_sha256`, prove honest implementation by itself, or authorize silent accepted-work substitution.

Within one compatibility line, an existing definition ID may not change kind or incompatible meaning and a required definition may not disappear without an explicit migration boundary. Release/S6D-11 validation must enforce what can be mechanically proven.

### LAW S6D01-14 — SAME-VERSION REFRESH REQUIRES SAME RULESET SET

Source ancestry is provenance only. A same-engine-version/package-ID candidate is a nonsemantic silent refresh only when `ruleset_set_sha256` equals the campaign's current value.

If the set digest differs, the change is semantic ruleset adoption even if additive or on the same compatibility line:

- campaign creator authority is required;
- prepared/unaccepted work revalidates;
- accepted work retains exact prior set identity;
- non-creator use cannot advance campaign semantics;
- coherent publication updates campaign current identity.

### LAW S6D01-15 — INCOMPATIBLE LINE MIGRATION REMAINS WP-20

S6D-01 provides exact identities and finite mismatch boundaries. Future released-campaign migration across incompatible compatibility lines remains owned by R2.7 WP-20.

## 7. Recovery and retention laws

### LAW S6D01-16 — NO AMBIENT REINTERPRETATION

If accepted execution's exact ruleset snapshot set cannot be resolved, recovery blocks with a finite compatibility/prerequisite failure. It does not use model memory, current filesystem accident, current tag contents or arbitrary newer rules.

### LAW S6D01-17 — SNAPSHOT RETENTION FOLLOWS PROMISED CONSUMERS

An exact package snapshot/set required by a reachable accepted execution, campaign adoption or other protected consumer cannot retire until its owner-specific dependency is discharged or explicitly migrated. This joins Step-5.13 protection routing; it creates no universal refcount or GC frontier.

### LAW S6D01-18 — RECONSTRUCTION IS BOUNDED

Startup/adoption/recovery validates a finite declared package set and exact owner-local refs. Ordinary gameplay uses the already-bound context. No network registry, repository-wide scan, background worker or mutable-tag lookup is required.

## 8. House Rules boundary

### LAW S6D01-19 — REALIZATION LINKAGE DOES NOT FORK IDENTITY

House Rules `realization_refs` resolve against the active context and remain subject to catalog/currentness validation. Their presence does not create a package fork, override same-ID definitions or grant execution authority.

A derived/profile package is admitted only by a future explicit package adoption/migration decision when actual reusable same-ID replacement semantics require it. S6D-01 does not invent one.

## 9. Failure taxonomy

At minimum:

- `RULESET_PACKAGE_MANIFEST_INVALID`;
- `RULESET_PACKAGE_CONTENT_MISMATCH`;
- `RULESET_DEPENDENCY_MISSING`;
- `RULESET_DEPENDENCY_CYCLE`;
- `RULESET_PACKAGE_ID_AMBIGUOUS`;
- `RULESET_NAMESPACE_CONFLICT`;
- `RULESET_ENGINE_INCOMPATIBLE`;
- `RULESET_CATALOG_GENERATION_INCOMPATIBLE`;
- `RULESET_SET_MISMATCH`;
- `CATALOG_CONTEXT_UNRECONSTRUCTABLE`;
- existing `failure.catalog_context_incompatible` where the generic execution-facing failure is appropriate.

Failures are finite and diagnostic. They never cause fuzzy ID replacement, prose execution, hidden migration or partial mixed-context loading.

These names define the required semantic distinctions, not immediate registry admission. S6D-02/S6D-11 SHALL either admit exact machine failure IDs with those meanings or map them to an existing typed failure envelope without losing the distinctions.

## 10. Machine realization contract

S6D-01 canonicalization authorizes later structural realization of:

- a shipped ruleset-package manifest schema;
- generated runtime-package lock fields/schema version update;
- campaign manifest ruleset-set projections;
- Resolution/Continuation ruleset-set projections;
- deterministic digest/closure validator;
- update-policy rules based on exact set identity;
- focused tests.

Actual package instance namespaces/content depend on S6D-02. Integrated executable closure belongs to S6D-11 and must use RED→GREEN TDD.

## 11. Required verification

S6D-11 must cover:

1. deterministic content digest independent of traversal/enumeration order;
2. resolved-set digest independent of input order;
3. manifest/content tamper detection;
4. exact dependency closure and cycle rejection;
5. duplicate package ID/namespace/definition rejection;
6. engine/catalog mismatch rejection;
7. runtime package lock matches shipped files;
8. campaign creation/adoption projections;
9. same-version refresh: same set allowed, changed set requires creator adoption;
10. Resolution/Continuation preservation and mismatch blocking;
11. checkpoint cannot override accepted identity;
12. retained snapshot dependency blocks cleanup;
13. House Rules realization ref validates only through active context;
14. no per-world-record package-version proliferation;
15. reconstruct identical context from identical owners/locks and reject incomplete evidence.

## 12. Downstream ownership

- S6D-02 owns actual admitted package(s), namespaces and seed content.
- S6D-03–06 own complete registered execution metadata inside the compatible catalog generation.
- S6D-07–09 own reconstructable supported mechanics coverage.
- S6D-10 owns integrated House Rules mechanical handoff validation.
- S6D-11 owns executable structural closure.
- S6D-12 owns integrated adversarial closure.
- R2.7 WP-20 owns future incompatible released migration policy.


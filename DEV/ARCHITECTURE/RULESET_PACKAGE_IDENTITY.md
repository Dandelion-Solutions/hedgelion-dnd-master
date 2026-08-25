# HDM Ruleset Package and Resolved Catalog Identity

Status: **CANONICAL S6D-01 ARCHITECTURE**

Canonicalized: 2026-08-25

Design chain:

- `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-task-brief.md`
- `DEV/docs/superpowers/research/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-research-architecture-draft.md`
- `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-collaborative-review.md`
- `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-resolution-gate.md`

## 1. Decision

HDM identifies selected reusable rules definitions through content-addressed semantic package snapshots and an exact dependency-closed resolved-set identity.

```text
RulesetPackageManifest + exact semantic content bytes
    -> RulesetPackageSnapshot(content_sha256)

exact cycle-free dependency closure
    -> ResolvedRulesetSnapshotSet(ruleset_set_sha256)

engine capability identity
    + ruleset_set_sha256
    + exact campaign-definition frontier
    + optional exact session-overlay frontier
        -> derived catalog_context_fingerprint
```

The resolved ruleset set is exact and reconstructive. The full `ResolvedCatalogContext` remains a logical composition of natural owners. Its fingerprint is comparison/retry evidence, not a new global snapshot owner.

## 2. Identity types

### RulesetPackageManifest

One package-owned semantic declaration:

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

`content_files[]` is an explicit set of normalized package-relative semantic files. Baseline S6D-01 does not admit wildcard/root expansion, symlinks, external paths or filesystem-enumeration semantics.

### RulesetPackageSnapshot

One validated manifest plus the exact bytes of its declared semantic content and computed `content_sha256`.

### ResolvedRulesetSnapshotSet

One exact, dependency-closed, cycle-free set of snapshots satisfying engine/catalog requirements and non-overlapping namespace ownership.

### ruleset_set_sha256

Exact order-independent content identity of the resolved ruleset set.

### catalog_context_fingerprint

Derived identity of engine capability, exact resolved ruleset set and exact owner-local campaign/session definition frontiers. It is not sufficient reconstruction authority by itself.

## 3. Non-equivalent axes

The following axes SHALL NOT silently substitute for one another:

```text
engine_version                 semantic engine/capability line
catalog_generation             coordinated machine vocabulary/schema generation
runtime package_id/source SHA  built-artifact provenance
runtime ZIP SHA-256            exact complete artifact bytes
ruleset package_version        package presentation/adoption version
ruleset compatibility_id       declared semantic compatibility line
ruleset content_sha256         exact package semantic-content identity
ruleset_set_sha256             exact selected package-set identity
catalog_context_fingerprint    derived composed-context identity
```

`rules_baseline` remains human-facing baseline metadata. `catalog_version` does not identify selected reusable definitions. Source ancestry proves provenance/order, not semantic compatibility.

## 4. Deterministic digest contract

### Package digest

`content_sha256` is SHA-256 over:

```text
ASCII "HDM_RULESET_PACKAGE_SNAPSHOT_V1\n"
+ UTF-8 canonical JSON payload
```

The payload contains fixed member names and the sorted sequence of:

```text
normalized_relative_path
sha256(exact_file_bytes) as lower-case hexadecimal
```

The manifest bytes are one declared content file and therefore participate. The digest is not stored inside that hashed manifest.

Canonical JSON has no insignificant whitespace; object member ordering is fixed by the owning schema/serializer. Paths are unique, traversal-free, normalized UTF-8 package-relative paths and are ordered by Unicode code point. Timestamps, permissions, archive metadata, YAML presentation order and filesystem enumeration order do not participate.

### Resolved-set digest

`ruleset_set_sha256` is SHA-256 over:

```text
ASCII "HDM_RESOLVED_RULESET_SET_V1\n"
+ UTF-8 canonical JSON lock
```

The lock is sorted by `package_id`. Each entry contains at least package ID/version, compatibility ID, content digest, catalog generation and exact dependency `package_id -> content_sha256` edges. Discovery/input order has no meaning.

## 5. Admission and namespace laws

1. Every dependency resolves to exactly one package snapshot.
2. Missing/ambiguous package IDs, exact dependency mismatch, cycles and engine/catalog incompatibility fail loading.
3. Every reusable definition belongs to a namespace claimed by its source package.
4. Namespace overlap, definition outside a claim and duplicate resolved `definition_id` fail loading.
5. There is no last-layer-wins or same-ID shadowing.
6. Campaign/session definitions remain owner-local frontiers and follow existing promotion/collision laws; they are not silently repackaged or copied into the ruleset lock.

## 6. Natural-owner projections

### Runtime package

Builder-generated runtime package provenance SHALL advertise the exact embedded resolved ruleset lock and `ruleset_set_sha256`. The runtime ZIP SHA-256 remains its separate external artifact identity.

### Campaign

Campaign MANIFEST SHALL use a sibling ruleset projection:

```text
ruleset:
  created_with:
    ruleset_set_sha256
  current:
    ruleset_set_sha256
```

Machine realization may add bounded diagnostic package IDs only when a proved consumer needs them. `ruleset.created_with` is immutable. `ruleset.current` changes only through authorized coherent adoption/refresh. Engine and ruleset identities may update in one transaction but neither owns the other.

### Accepted execution

Accepted Resolution and Continuation generations SHALL retain:

```text
ruleset_set_sha256
catalog_context_fingerprint
```

Owner-local dependency refs retain any campaign/session definitions required for retry/resume. Ordinary world/definition records do not repeat package identity solely for reconstruction.

### Checkpoint

Checkpoint/diagnostic evidence may repeat refs for routing, but campaign and accepted execution owners remain authoritative. Checkpoint cannot repair a mismatch by selecting ambient mechanics.

## 7. Adoption and compatibility

`compatibility_id` is a declared semantic line, not exact identity. It neither replaces content digests nor authorizes silent substitution for accepted work.

Within one compatibility line, existing definition IDs cannot change incompatible kind/meaning and required definitions cannot disappear without an explicit migration boundary.

A same-engine-version/package-ID/source-descendant candidate follows the silent forward-refresh contract in `GAME/CORE/ENGINE_UPDATES.md`. An unchanged `ruleset_set_sha256` is trivially nonsemantic maintenance. A changed set digest does not by itself turn that proven compatible same-version runtime refresh into a prompted migration.

For a proven forward same-version refresh whose embedded ruleset set changes compatibly or additively:

- the runtime may use the candidate immediately without a player prompt;
- prepared/unaccepted work revalidates against the candidate set;
- accepted work retains its exact prior set identity;
- a non-creator may use the refreshed runtime and its exact embedded set for play, but cannot persist either campaign engine identity or `ruleset.current`;
- the campaign creator silently refreshes `engine.current` provenance and `ruleset.current` together at the next otherwise-valid coherent campaign persistence boundary; no standalone maintenance commit is created.

An incompatible, backward, diverged or otherwise ambiguous ruleset-set replacement is not a silent refresh. It requires explicit creator-authorized adoption/migration under the applicable migration owner.

Future migration across incompatible released compatibility lines remains owned by R2.7 WP-20.

## 8. Recovery and retention

Accepted work is never reinterpreted through model memory, mutable tag contents, arbitrary current files or a different ruleset set.

If its exact ruleset set cannot be resolved, recovery stops at a finite compatibility/prerequisite failure. Exact required snapshots remain protected while a reachable accepted execution, campaign adoption or other typed consumer needs them.

Retention joins Step-5.13 owner-specific protection routing. It creates no universal refcount, GC graph, snapshot record or frontier.

Startup/adoption/recovery validates one finite declared set plus bounded owner-local refs. Ordinary gameplay uses the already-bound context; no online registry, repository-wide scan or background resolver exists.

## 9. House Rules boundary

House Rules `realization_refs` resolve against the active context and remain subject to catalog/currentness validation. They do not create a package fork, same-ID override or execution authority.

A derived/profile package requires later explicit evidence that reusable same-ID replacement semantics are genuinely needed. None is admitted by S6D-01.

## 10. Finite failures

The architecture distinguishes:

- invalid package manifest;
- package content mismatch;
- missing/ambiguous dependency;
- dependency cycle;
- package ID ambiguity;
- namespace conflict;
- engine/catalog incompatibility;
- resolved-set mismatch;
- unreconstructable catalog context.

S6D-02/S6D-11 may admit exact machine failure IDs or map them to an existing typed failure envelope, but SHALL preserve these distinctions. No failure permits fuzzy replacement, prose execution, hidden migration or partial mixed-context loading.

## 11. Downstream machine obligations

- **S6D-02:** actual package instance(s), namespace claims, semantic content inventory and catalog failure admission.
- **S6D-03–06:** selector/accessor/value/primitive registries tied to the declared compatible catalog generation/content closure.
- **S6D-07–09:** reconstructable READY_PC and supported mechanics seed from the locked content.
- **S6D-10:** House Rules realization validation through the active context.
- **S6D-11:** RED→GREEN manifest/lock/digest/projection/adoption/recovery tests and structural realization.
- **S6D-12:** integrated identity/authority/retention adversarial closure.
- **R2.7 WP-20:** future incompatible released-campaign migration policy.

S6D-01 does not create the actual seed package before S6D-02 establishes its contents/namespaces, and it does not claim executable closure before S6D-11.

## 12. Required S6D-11 verification

At minimum:

1. deterministic package digest independent of enumeration order;
2. deterministic set digest independent of input order;
3. content tamper detection;
4. exact dependency closure/cycle rejection;
5. duplicate package/namespace/definition rejection;
6. engine/catalog mismatch rejection;
7. runtime lock matches shipped semantic files;
8. campaign creation/adoption ruleset projections;
9. same-set maintenance versus changed-set creator adoption;
10. Resolution/Continuation preservation and mismatch blocking;
11. checkpoint nonauthority;
12. typed retention blocking premature cleanup;
13. House Rules refs validate only through active context;
14. absence of per-record package-version proliferation;
15. identical-owner reconstruction and incomplete-evidence rejection.



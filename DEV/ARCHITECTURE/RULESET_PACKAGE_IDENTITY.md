# HDM Ruleset Package and Resolved Catalog Identity

Status: **CANONICAL S6D-01 ARCHITECTURE — VERSIONING REPRESENTATION AMENDED 2026-09-05**

Canonicalized: 2026-08-25

Versioning representation amendment:

- `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` supersedes the pre-release representation of ruleset package update/compatibility fields and digest-domain generation spelling;
- the identity/authority/content-addressing semantics in this document remain canonical;
- target representation separates `package_revision`, `compatibility_family`, `compatibility_generation`, integer `catalog_generation`, and typed digest/canonicalization generation;
- current pre-release machine artifacts that still use `package_version`, version-bearing `compatibility_id`, `catalog_generation: 2.0.0` or `_V1` domain literals are realization debt and do not create compatibility obligations.

Design chain:

- `DEV/docs/superpowers/design/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-task-brief.md`
- `DEV/docs/superpowers/design/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-research-architecture-draft.md`
- `DEV/docs/superpowers/design/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-decision-brief.md`
- `DEV/docs/superpowers/design/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-collaborative-review.md`
- `DEV/docs/superpowers/design/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-candidate-spec.md`
- `DEV/docs/superpowers/design/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-adversarial-review.md`
- `DEV/docs/superpowers/design/2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-resolution-gate.md`

## 1. Decision

HDM identifies selected reusable rules definitions through content-addressed semantic package snapshots and an exact dependency-closed resolved-set identity.

```text
RulesetPackageManifest + exact semantic content bytes
    -> RulesetPackageSnapshot(content_sha256)

exact cycle-free dependency closure
    -> ResolvedRulesetSnapshotSet(ruleset_set_sha256)

engine capability identity
    + ruleset_set exact typed identity
    + exact campaign-definition frontier
    + optional exact session-overlay frontier
        -> derived catalog_context_fingerprint
```

The resolved ruleset set is exact and reconstructive. The full `ResolvedCatalogContext` remains a logical composition of natural owners. Its fingerprint is comparison/retry evidence, not a new global snapshot owner.

## 2. Identity types

### RulesetPackageManifest

One package-owned semantic declaration, conceptually:

```text
manifest_schema_version
package_id
package_revision
compatibility_family
compatibility_generation
engine_requirement
catalog_generation
owned_namespaces[]
dependencies[]
content_files[]
```

`package_revision` is package-local update order only. It is not a semantic-compatibility signal.

`compatibility_family` is the stable semantic family identity. `compatibility_generation` is the integer semantic compatibility line inside that family.

The current pre-release machine manifest still carries `package_version` and version-bearing `compatibility_id`; the later normalization pass replaces those fields without preserving their legacy spelling.

`content_files[]` is an explicit set of normalized package-relative semantic files. Baseline S6D-01 does not admit wildcard/root expansion, symlinks, external paths or filesystem-enumeration semantics.

### RulesetPackageSnapshot

One validated manifest plus the exact bytes of its declared semantic content and computed exact package-content identity under the applicable typed digest/canonicalization contract generation.

### ResolvedRulesetSnapshotSet

One exact, dependency-closed, cycle-free set of snapshots satisfying engine/catalog requirements and non-overlapping namespace ownership.

### ruleset-set exact identity

The resolved-set exact identity is content-addressed and generation-aware. A bare hexadecimal digest is meaningful only under the digest/canonicalization contract that produced it.

Current field spelling `ruleset_set_sha256` remains pre-release machine realization; future released persistence MUST retain enough typed generation/context to interpret the exact identity across digest-contract evolution.

### catalog_context_fingerprint

Derived identity of engine capability, exact resolved ruleset set and exact owner-local campaign/session definition frontiers. It is not sufficient reconstruction authority by itself and likewise remains generation-aware if its canonicalization contract evolves.

## 3. Non-equivalent axes

The following axes SHALL NOT silently substitute for one another:

```text
engine_version                         semantic engine/capability line
catalog_generation                     coordinated machine vocabulary/schema generation
runtime package_id/source SHA          built-artifact provenance
runtime ZIP SHA-256                    exact complete artifact bytes
ruleset package_revision               package-local update order
ruleset compatibility_family           semantic compatibility family identity
ruleset compatibility_generation       semantic compatibility line
ruleset exact package-content identity exact package semantic-content identity
ruleset exact resolved-set identity    exact selected package-set identity
catalog_context_fingerprint            derived composed-context identity
```

`rules_baseline` remains human-facing baseline metadata. Catalog generation does not identify selected reusable definitions. Source ancestry proves provenance/order, not semantic compatibility. Package revision proves neither semantic compatibility nor exact identity.

## 4. Deterministic digest contract

### Package digest

Package snapshot exact identity is SHA-256 over one canonical payload under an explicit package-snapshot digest contract generation.

The payload contains fixed member names and the sorted sequence of:

```text
normalized_relative_path
sha256(exact_file_bytes) as lower-case hexadecimal
```

The manifest bytes are one declared content file and therefore participate. The digest is not stored inside that hashed manifest.

Canonical JSON has no insignificant whitespace; object member ordering is fixed by the owning schema/serializer. Paths are unique, traversal-free, normalized UTF-8 package-relative paths and are ordered by Unicode code point. Timestamps, permissions, archive metadata, YAML presentation order and filesystem enumeration order do not participate.

The current pre-release implementation spells its domain generation inside an `_V1` byte literal. That spelling is superseded as architecture: digest/canonicalization generation must be explicit/typed under the canonical versioning policy and may be implied by an enclosing schema only when unambiguous.

### Resolved-set digest

The resolved-set exact identity is SHA-256 over the canonical resolved lock under an explicit resolved-set digest contract generation.

The lock is sorted by `package_id`. Each entry contains at least package ID/revision, compatibility family/generation, exact content identity, catalog generation and exact dependency `package_id -> exact content identity` edges. Discovery/input order has no meaning.

A digest generated under a different digest-contract generation is a different exact-identity domain and is not directly compared as if both values came from one canonicalization contract.

## 5. Admission and namespace laws

1. Every dependency resolves to exactly one package snapshot.
2. Missing/ambiguous package IDs, exact dependency mismatch, cycles and engine/catalog incompatibility fail loading.
3. Every reusable definition belongs to a namespace claimed by its source package.
4. Namespace overlap, definition outside a claim and duplicate resolved `definition_id` fail loading.
5. There is no last-layer-wins or same-ID shadowing.
6. Campaign/session definitions remain owner-local frontiers and follow existing promotion/collision laws; they are not silently repackaged or copied into the ruleset lock.
7. All coordinated catalog-generation projections in one admitted runtime/ruleset closure MUST equal the canonical catalog generation; mixed generations fail admission.

## 6. Natural-owner projections

### Runtime package

Builder-generated runtime package provenance SHALL advertise the exact embedded resolved ruleset lock and exact typed resolved-set identity. The runtime ZIP SHA-256 remains its separate external artifact identity over complete archive bytes.

### Campaign

Campaign MANIFEST SHALL use a sibling ruleset projection carrying immutable creation identity and mutable current adopted identity.

Conceptually:

```text
ruleset:
  created_with:
    exact resolved-set identity + required identity-generation context
  current:
    exact resolved-set identity + required identity-generation context
```

Machine realization may add bounded diagnostic package IDs only when a proved consumer needs them. `ruleset.created_with` is immutable. `ruleset.current` changes only through authorized coherent adoption/refresh. Engine and ruleset identities may update in one transaction but neither owns the other.

### Accepted execution

Accepted Resolution and Continuation generations SHALL retain the exact resolved ruleset-set identity and catalog-context fingerprint with enough typed generation/context to interpret them across released digest-contract evolution.

Owner-local dependency refs retain any campaign/session definitions required for retry/resume. Ordinary world/definition records do not repeat package identity solely for reconstruction.

### Checkpoint

Checkpoint/diagnostic evidence may repeat refs for routing, but campaign and accepted execution owners remain authoritative. Checkpoint cannot repair a mismatch by selecting ambient mechanics.

## 7. Adoption and compatibility

`compatibility_generation` is a declared semantic line inside one `compatibility_family`; it is not exact identity. It neither replaces content digests nor authorizes silent substitution for accepted work.

Within one compatibility generation, existing definition IDs cannot change incompatible kind/meaning and required definitions cannot disappear without an explicit migration boundary.

Same compatibility generation makes a candidate eligible for the accepted semantic compatibility proof. It does not prove compatibility by itself.

A same-engine-version/package-ID/source-descendant candidate follows the silent forward-refresh contract in `GAME/CORE/ENGINE_UPDATES.md` only when the required exact and monotonic semantic compatibility proof succeeds. An unchanged exact resolved-set identity is trivially nonsemantic maintenance. A changed exact set identity does not by itself turn a proven compatible same-version runtime refresh into a prompted migration.

For a proven forward same-version refresh whose embedded ruleset set changes compatibly or additively:

- the runtime may use the candidate immediately without a player prompt;
- prepared/unaccepted work revalidates against the candidate set;
- accepted work retains its exact prior set identity and typed identity generation/context;
- a non-creator may use the refreshed runtime and its exact embedded set for play, but cannot persist either campaign engine identity or `ruleset.current`;
- the campaign creator silently refreshes `engine.current` provenance and `ruleset.current` together at the next otherwise-valid coherent campaign persistence boundary; no standalone maintenance commit is created.

Different compatibility generation, incompatible semantic comparison, backward/diverged source relation or otherwise ambiguous ruleset-set replacement is not a silent refresh. It requires explicit creator-authorized adoption/migration under the applicable migration owner or fails unsupported.

Future migration across incompatible released compatibility generations remains owned by R2.7 WP-20.

## 8. Recovery and retention

Accepted work is never reinterpreted through model memory, mutable tag contents, arbitrary current files or a different ruleset set.

If its exact typed ruleset-set identity cannot be resolved, recovery stops at a finite compatibility/prerequisite failure. Exact required snapshots remain protected while a reachable accepted execution, campaign adoption or other typed consumer needs them.

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
- **R2.7 WP-20:** incompatible released-campaign migration policy plus canonical versioning/compatibility law.

S6D-01 does not create the actual seed package before S6D-02 establishes its contents/namespaces, and it does not claim executable closure before S6D-11.

Current machine realization predates the 2026-09-05 versioning-representation amendment. The later separately authorized normalization pass must update manifest/lock/result schemas, field names, typed digest-generation context and all affected hashes/fixtures atomically enough for audit/build to reject mixed representations.

## 12. Required S6D-11 verification semantics retained

At minimum, the realized architecture continues to require:

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

The versioning normalization pass must preserve these semantics while replacing obsolete pre-release field/value spelling.

## 13. S6D-11 machine realization status

S6D-11 originally closed this owner through `RULESET_PACKAGE_MACHINE_CLOSURE.md`, strict package manifest/lock/result schemas and `validate_ruleset_package_closure.py`.

Those machine artifacts are now **semantically accepted but version-representation stale** relative to the 2026-09-05 canonical amendment. Their current pre-release `package_version`, version-bearing `compatibility_id`, `2.0.0` catalog spelling and `_V1` digest-domain representation are not future architecture authority.

The accepted compatibility principle remains: a changed same-engine-version set is eligible for silent forward use only after independent adopted/candidate loading and a COMPLETE monotonic canonical semantic-entry comparison returns compatible/additive. Every adopted package line, namespace, exact dependency and definition/capability/active primitive/selector/accessor/fact/value/schema entry must remain present with identical kind and semantic hash under the applicable typed digest contract. Candidate-only entries must independently validate and avoid collisions. Incompatible or insufficient evidence prevents context use. Ancestry, labels and standalone load success are not this proof.

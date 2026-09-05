# HDM Versioning Namespace and Compatibility Policy

Status: **CANONICAL — HUMAN-APPROVED ARCHITECTURE AMENDMENT / MACHINE REALIZATION DEFERRED**

Date: 2026-09-05

This specification defines the canonical HDM-owned versioning taxonomy, compatibility meaning and migration obligations. It is implementation-facing architecture. It does not itself renumber tracked machine artifacts, rewrite persistent templates, recalculate digests, create migration scripts or authorize WP-20 Step 2.

The Product Owner / human architect approved this architecture after reviewing the versioning inventory preserved in:

- `DEV/docs/superpowers/research/2026-09-05-versioning-namespace-inventory-and-analysis.md`.

This amendment refines and extends `DEV/RELEASE/VERSIONING.md`. Where older accepted documents encode version/generation information in a representation that conflicts with this specification, their underlying identity/authority semantics remain in force but the older version-field representation is superseded by this specification.

## 1. Scope

This policy governs HDM-owned version and revision namespaces, including:

- engine release identity;
- CORE/runtime module versions;
- development bookkeeping revisions;
- persistent record schemas;
- campaign-wide persistent-contract generation;
- storage-format generation;
- runtime/package/protocol schemas;
- catalog generation;
- ruleset package revision and compatibility generation;
- HDM-owned exact-digest canonicalization generations;
- domain-local runtime/currentness revisions where version taxonomy applies.

External version namespaces are outside this policy and remain owned externally. Examples include D&D/SRD release numbering, JSON Schema draft identity, Git object identity, third-party dependency versions and other externally owned standards/products.

## 2. Clean-slate realization boundary

Current development is pre-release for HDM v1.0. Under the accepted clean-slate compatibility decision, no v0.8/pre-release compatibility obligation exists.

Therefore the later machine-realization pass for this policy MAY:

- rename version fields;
- replace invalid or ambiguous pre-release numbering;
- normalize catalog/ruleset/protocol representations;
- recalculate all derived HDM-owned hashes/fingerprints affected by canonicalization changes;
- recreate pre-release schemas/templates/fixtures/contracts rather than preserving obsolete shapes;
- delete obsolete compatibility shims rather than carrying them forward.

It MUST NOT create compatibility adapters or migration debt solely to preserve current pre-release machine shapes.

Released v1.0+ data/assets are governed by the compatibility and migration laws below.

## 3. Three numbering categories

Every HDM-owned version/revision field MUST belong to exactly one of these categories.

### Category A — engine release identity

Format:

```text
MAJOR.MINOR[-prerelease]
```

Canonical field:

```text
engine_version
```

Meaning: semantic HDM engine release/capability line.

A prerelease suffix belongs only to engine release/tag identity. It is not copied into component versions, schema versions, generations or revisions.

### Category B — engine-bound component/module version

Format:

```text
ENGINE_MAJOR.ENGINE_MINOR.REVISION
```

Canonical module field:

```text
framework_module_version
```

Meaning:

- `ENGINE_MAJOR.ENGINE_MINOR` identifies the engine release line in which that component was last materially changed;
- `REVISION` is the monotonically increasing revision counter owned by that component.

A pure engine release bump does not change an untouched component. On the next material component change, the prefix moves to the then-current engine major/minor and the component-local revision increments exactly once.

### Category C — independent counter

Format:

```text
integer N
```

Category C counters do not inherit or copy engine major/minor merely for visual uniformity.

Category C has distinct semantic subtypes:

- `*_revision` — local monotonic change/currentness/bookkeeping counter; does not by itself define a compatibility boundary;
- `*_schema_version` or artifact-local `schema_version` — version of one explicitly typed serialized contract;
- `*_generation` — semantic/compatibility generation for a coordinated contract family or format;
- domain-local runtime/currentness ordinal — state mutation/currentness order within its named owner/domain.

The shared integer representation does not make these subtypes interchangeable.

## 4. Naming law

Version semantics MUST be visible from the field/type name rather than inferred from a visually familiar number.

Normative naming rules:

```text
engine_version                    -> Category A release identity
framework_module_version          -> Category B engine-bound component
*_revision                        -> Category C local revision/ordinal
*_schema_version / schema_version -> Category C serialized-contract schema
*_generation                      -> Category C semantic/compatibility generation
```

HDM-owned compatibility generations SHOULD NOT be hidden only inside opaque identifiers such as a trailing `.v1` when a stable family identifier plus an explicit typed generation can represent the semantics.

Legacy identifiers that contain version-looking text but whose text is genuinely part of immutable semantic identity rather than a version namespace are not mechanically rewritten merely because they contain `vN`; the normalization pass must classify them first.

## 5. Cross-namespace laws

### V-01 — equality is namespace-local

Numeric equality across different namespaces has no semantic meaning.

For example:

```text
campaign_contract_generation = 2
catalog_generation = 2
checkpoint.schema_version = 2
```

are unrelated facts.

### V-02 — ordering is namespace-local

`3 > 2` establishes ordering only inside one explicitly defined ordered namespace. It never proves compatibility.

Timestamps, commit ancestry, SHA magnitude, filename ordering and lexical version-string ordering cannot substitute for a declared compatibility relation.

### V-03 — same generation means eligibility, not proof

Where a generation represents a compatibility line, equality permits the applicable compatibility proof to run; it does not itself prove exact or semantic compatibility.

Exact content identity, required semantic comparisons and owner-specific invariants remain authoritative.

### V-04 — unknown newer contract fails closed

A consumer encountering an unsupported newer schema/generation MUST reject, require an admitted migration/adoption path, or report unsupported/insufficient evidence. It MUST NOT optimistically interpret unknown fields or fuzzy-match the nearest version.

### V-05 — migration is an explicit directed graph edge

Migration/adoption is selected through declared source/target predicates and immutable implementation identity/provenance. Integer arithmetic never manufactures migration paths.

A source generation `2` and target `5` do not imply legal `2->3->4->5` migration. The graph must explicitly contain one valid path.

Reverse/downgrade migration is not guaranteed. A reverse transformation exists only when an explicit reverse edge is separately declared, supported and verified.

### V-06 — owner and projection must agree

Every version/generation has exactly one semantic owner. A repeated copy elsewhere is a projection.

When a coordinated closure requires the same generation on several artifacts, all projections MUST equal the owner. Mixed-generation closure is invalid, not temporarily compatible.

### V-07 — version identity does not replace exact identity

Semantic version/generation/revision fields do not replace exact package/content/provenance identities such as ZIP SHA-256, content-addressed ruleset identities or immutable source commit identity.

### V-08 — release assets are immutable

Released runtime/package assets are never rewritten into a newer schema/generation. A newer consumer may explicitly support an older released asset or reject it. A new release creates a new asset.

## 6. Engine release policy

Canonical representation:

```yaml
engine_version: 1.0-alpha
recommended_tag: v1.0-alpha
```

`recommended_tag` is a projection of `engine_version` and MUST remain exactly `v<engine_version>` under the current release policy.

Engine-version ordering alone does not prove that an existing campaign can run unchanged. Released campaign compatibility is multi-axis and includes the applicable campaign contract generation, persistent family schemas, storage generation, exact runtime/package provenance, catalog/ruleset compatibility and accepted-work interpretation dependencies where material.

An engine release bump by itself does not imply a campaign migration.

## 7. CORE/runtime module version policy

All versioned shipped CORE/runtime instruction modules use:

```text
framework_module_version: ENGINE_MAJOR.ENGINE_MINOR.REVISION
```

The prefix identifies the engine major/minor line of the module's last material contract change.

Rules:

1. a new module starts at local revision `1`;
2. every later material logical edit increments its local revision exactly once;
3. an engine release change without a module change does not rewrite the module version;
4. on the next material edit, move the prefix to the current engine major/minor and increment the existing local revision;
5. prerelease suffixes are never placed in module versions;
6. all version-bearing CORE/runtime modules use the same field name unless an owning specification proves a genuinely different version type;
7. current CORE documentation that is intentionally not a versioned module must be explicitly classified as such rather than accidentally omitted from validation.

Module versions are package metadata/history and are not independently migrated inside campaigns. A campaign consumes an exact validated runtime package; it does not assemble arbitrary module versions from different releases.

## 8. Development bookkeeping revisions

Development-only counters such as `persistence_revision`, `storage_format_revision`, `consistency_audit_revision` and similar `*_revision` fields remain independent integers.

They are bookkeeping/review-change counters, not runtime compatibility versions.

Rules:

- increment only when the owning concern materially changes under its existing bookkeeping law;
- do not prefix with engine major/minor;
- do not leak into runtime metadata merely for observability;
- never use them as campaign migration selectors unless a future explicit owner changes their semantics and name.

No campaign migration is caused by a development-only revision change.

## 9. Persistent family schema policy

Each independently serialized persistent record family owns its local schema version.

Canonical form inside a typed schema/record remains an integer:

```yaml
schema_version: N
```

or an explicitly qualified `*_schema_version` when the enclosing artifact is not sufficiently self-typing.

Rules:

1. compatible optional/additive changes MAY remain on the same schema version when the owning schema says old and new records remain semantically valid;
2. an incompatible required-field/type/meaning change MUST bump the affected family schema version;
3. an old reader encountering an unsupported newer family schema fails closed;
4. a new reader may read an older family schema only when support is explicit;
5. persisted instances requiring conversion use an explicit migration edge;
6. schema arithmetic never implies migration support.

Local family schema versions remain independent across families. It is valid for manifest, checkpoint and NPC records to have different schema versions simultaneously.

## 10. Campaign-wide persistent contract generation

The current ambiguous shared `ENGINE_VERSION.schema_version` concept is superseded by a clearly named aggregate compatibility axis:

```text
campaign_contract_generation
```

### 10.1 Runtime/development projection

The target runtime/development version manifests carry:

```yaml
campaign_contract_generation: N
```

This means: the released aggregate persistent campaign contract generation the runtime is capable of adopting/producing under the current architecture.

It is not a replacement for local record-family schema versions.

### 10.2 Campaign projection

A released campaign MUST carry immutable creation provenance plus mutable current adoption for the aggregate contract generation, conceptually:

```yaml
campaign_contract:
  created_with: N
  current: N
```

`created_with` is immutable. `current` changes only through a confirmed authorized compatible adoption/migration publication.

Exact final machine placement/naming may be structurally adapted only if it preserves these two semantics without creating duplicate authority.

### 10.3 Bump law

`campaign_contract_generation` MUST bump when a released change requires coherent migration of existing campaign persistent semantics, including:

- any breaking local persistent-family schema change that requires campaign migration;
- a persistent semantic interpretation change requiring migration even if file shape remains unchanged;
- a coordinated set of persistent-family changes that must be adopted atomically.

A purely compatible additive change that requires no migration does not by itself bump campaign contract generation.

A local schema bump that is breaking/migration-required MUST be accompanied by a campaign contract generation bump. The converse is not required: aggregate generation may bump for a semantic contract change without a physical local-schema shape change.

### 10.4 Compatibility/migration

Equal campaign-contract generation is necessary for direct no-migration use but is not sufficient to prove the complete compatibility envelope.

Different released campaign-contract generations require an explicit migration/adoption path or produce an unsupported result. No implicit backward compatibility exists.

## 11. Storage format generation

The storage marker/layout compatibility axis is an independent generation:

```text
storage_format_generation: N
```

This supersedes ambiguous `storage_format_version` wording as the target naming convention.

Bump the generation when storage repository marker/layout/authority semantics change incompatibly.

Storage-format migration is distinct from campaign-data migration. Either may change without the other.

A runtime may support an older storage generation only explicitly. An unsupported newer generation fails closed. A storage migration uses its own explicit source/target edge and authority/publication contract.

## 12. Runtime package and other package/protocol schemas

Runtime/package/protocol artifact schemas remain independent integer schema versions.

Examples include:

- runtime package manifest schema;
- ruleset package manifest schema;
- resolved-set lock schema;
- engine-contract inventory schema;
- compatibility-result schema;
- conformance-attestation schema.

These versions describe the serialized/protocol contract of that artifact, not the HDM engine release.

Released package assets are immutable. Schema evolution uses reader support/rejection and newly generated target-schema assets; old ZIPs/locks/attestations are not rewritten in place.

Derived lock/inventory/attestation objects may be regenerated under a new schema when their natural authoritative inputs remain available. Regeneration is not campaign migration unless a persisted campaign/accepted-work owner stores compatibility-bearing identity whose meaning changes.

## 13. Launcher revision

The launcher uses an independent local revision:

```text
launcher_revision: N
```

This supersedes `launcher_version` as the target naming convention because the value is not an engine release or compatibility generation.

A launcher revision bump alone requires no campaign/storage migration.

## 14. Catalog generation

Catalog uses one coordinated independent integer generation:

```text
catalog_generation: N
```

The current clean-slate catalog generation represented in pre-release machine artifacts as `2.0.0` is normalized conceptually to generation `2`.

### 14.1 Coordinated closure law

All machine artifacts that project the current coordinated catalog generation MUST equal the canonical catalog owner generation.

A source tree/runtime package containing mixed coordinated catalog generations is invalid. For example, catalog owner/core at generation `3` while a required coordinated registry/projection/ruleset requirement remains generation `2` MUST fail audit/build/admission.

Local structural `schema_version` values of individual catalog artifacts are independent and need not equal `catalog_generation`.

### 14.2 Bump law

Bump `catalog_generation` only for an incompatible coordinated change in machine vocabulary/schema/contract semantics that cannot remain inside the existing compatibility generation.

Compatible/additive catalog content changes MAY remain within the same generation; exact content/semantic identities still distinguish the changed snapshot.

A generation is not a build counter.

### 14.3 Compatibility/migration

Different catalog generations are not silently compatible. A runtime/ruleset built against one generation cannot be reinterpreted against another merely because IDs look similar.

Cross-generation movement requires an explicit admitted adoption/migration/translation boundary or fails unsupported.

## 15. Ruleset package revision and semantic compatibility generation

Ruleset package identity keeps exact content addressing and separates presentation/update order from semantic compatibility.

Target conceptual manifest fields include:

```yaml
package_id: <stable package identity>
package_revision: N
compatibility_family: <stable semantic compatibility family>
compatibility_generation: N
manifest_schema_version: N
engine_requirement: <engine release constraint/identity as defined by owner>
catalog_generation: N
```

### 15.1 Package revision

`package_revision` is a monotonically increasing local revision within one `package_id` lineage.

It records package update order only. It does not prove compatibility and is not a migration selector by itself.

### 15.2 Compatibility family and generation

`compatibility_family` names the stable semantic compatibility family. `compatibility_generation` is the integer semantic line within that family.

Same compatibility generation means a candidate is eligible for the existing semantic compatibility proof. It does not authorize silent substitution by itself.

The accepted exact/monotonic semantic comparison remains required for compatible same-generation refresh where applicable.

Changing `compatibility_generation` defines an incompatible semantic boundary. Existing released campaigns require explicit creator-authorized adoption/migration or fail unsupported under WP-20 policy.

### 15.3 Legacy representation supersession

The current pre-release representation using `package_version: 0.1.0-mvp` and a version-bearing `compatibility_id: ...v1` is superseded as the target representation by package revision plus compatibility family/generation.

This representational amendment does not remove the underlying non-equivalence of package order, semantic compatibility and exact content identity established by `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`.

## 16. Exact digest and fingerprint contract generations

HDM-owned custom canonical hashes/fingerprints are exact identities under a specific digest/canonicalization contract.

The generation of that contract MUST be explicit in architecture and machine validation. It MUST NOT exist only as an unexplained `_V1` suffix embedded in a magic byte string or opaque identifier.

A digest contract generation changes when any identity-defining rule changes, including:

- participating fields/content;
- canonical serialization;
- ordering;
- path/string normalization;
- domain-separation semantics;
- digest algorithm.

### 16.1 Enclosing-schema rule

A digest contract generation MAY be implied by an enclosing typed protocol/schema generation only when that enclosing contract unambiguously fixes the complete digest semantics.

If an exact digest escapes that enclosing context and is persisted/referenced independently across releases, its typed identity MUST carry enough generation/type information to determine the digest contract used.

In particular, a bare persisted ruleset-set hash or context fingerprint must not become ambiguous after a future digest-contract change.

### 16.2 Comparison law

Digest values produced under different digest-contract generations are not directly comparable as one identity space.

A generation change does not by itself prove semantic content mismatch; it means exact identity must be interpreted/recomputed under the applicable contract.

### 16.3 Pre-release normalization

During the current pre-release realization, all HDM-owned derived hashes/fingerprints affected by the new canonicalization representation MAY be recomputed and all fixtures/locks/attestations updated. No legacy hash compatibility shim is required.

After v1.0 release, persisted accepted-work/campaign identities from an older digest generation remain meaningful historical/exact evidence in their original typed context. A migration may recompute target identities only from admitted source bytes/evidence; it MUST NOT guess equivalence from matching labels.

## 17. Dynamic state revisions and currentness ordinals

Domain-local values such as `state_revision`, live revision/frontier or other runtime currentness counters remain owner-local integer ordinals.

They are not release versions, schema versions or migration generations and MUST NOT be mass-renumbered by version normalization.

Their existing owner-specific currentness/CAS semantics remain unchanged.

## 18. Migration direction and rollback semantics

### 18.1 Directed explicit edges

Released migrations form a directed graph of explicit edges. Baseline support is forward migration where a declared edge exists.

Downgrade/reverse migration is not a baseline promise. It requires an explicit separately designed reverse edge.

### 18.2 No arithmetic path invention

A migration runner may compose multiple edges only when each edge is explicit, compatible with the exact current state/evidence and the graph/path-selection law admits that composition.

### 18.3 Publication and failure

Local transformation does not change campaign/storage authority.

Authoritative migration/adoption occurs only at the existing confirmed authority-changing publication boundary under current persistence/CAS/currentness/authorization owners.

- before publication: abort discards target scratch and leaves old authority unchanged;
- confirmed publication rejection: old authoritative state remains current; no reverse migration is needed;
- indeterminate publication: resolve the existing publication outcome before retrying or claiming rollback;
- after confirmed accepted migration: returning to an older representation is a new reverse migration and exists only if an explicit reverse edge is supported.

Checkpoint existence never creates generic rollback support.

## 19. Compatibility and migration matrix

| Namespace/entity | Compatibility meaning | Backward compatibility default | Migration/adoption rule |
|---|---|---|---|
| `engine_version` | semantic engine release/capability line | none implied by version number | evaluate full compatibility envelope; engine bump alone does not require migration |
| CORE module version | module history inside exact runtime package | not independently relevant | no campaign migration; consume exact validated runtime package |
| DEV `*_revision` | development bookkeeping | not applicable | none |
| persistent family `schema_version` | one serialized record contract | explicit support only | breaking persisted change requires explicit migration edge |
| `campaign_contract_generation` | aggregate persistent campaign compatibility epoch | no implicit cross-generation compatibility | mismatch requires explicit campaign migration/adoption or unsupported |
| `storage_format_generation` | storage marker/layout contract | explicit support only | explicit storage migration edge; independent of campaign migration |
| runtime/package/protocol schema | serialized asset/protocol contract | explicit reader support only | released asset remains immutable; regenerate/new asset or reject |
| `launcher_revision` | launcher change counter | not applicable | none |
| `catalog_generation` | coordinated machine-contract compatibility generation | none across generations by default | explicit adoption/translation/migration or unsupported |
| ruleset `package_revision` | package update order | not a compatibility signal | semantic comparison decides same-generation refresh; revision alone does nothing |
| ruleset `compatibility_generation` | semantic compatibility line | same generation only makes proof eligible | different generation requires explicit adoption/migration or unsupported |
| ruleset/protocol schema versions | wire/serialized contract | explicit support only | regenerate derived artifacts or reject; migrate persisted owners only when affected |
| digest/fingerprint contract generation | exact identity canonicalization domain | no raw cross-generation equality | recompute from admitted source evidence; migrate/retain persisted typed identities as required |
| dynamic state/currentness revision | owner-local ordering/currentness | owner-specific | no generic migration/version normalization |

## 20. Version-owner projection law for release/build/audit

Builder/audit/validation MUST eventually enforce the following after machine realization:

1. every version-bearing field is classified into Category A, B or C and its subtype is known;
2. version field names match their semantics;
3. coordinated projections equal their canonical owner;
4. mixed catalog generation closure fails;
5. unsupported future schemas/generations fail closed;
6. CORE version fields follow the engine-bound module law and use the canonical field name;
7. no current CORE module declares a future engine major/minor line;
8. runtime metadata does not leak development-only revisions;
9. package/ruleset semantic compatibility is not inferred from package revision alone;
10. custom digest canonicalization generation is known and validated;
11. ambiguous obsolete fields such as the current aggregate `ENGINE_VERSION.schema_version` are removed/superseded in machine realization;
12. pre-release legacy representations are not retained solely for backward compatibility.

## 21. Deferred machine-realization obligations

This architecture does not authorize implementation in the current gate.

The later approved realization pass must at minimum reconcile:

- `DEV/RELEASE/VERSIONING.md` implementation checks;
- `DEV/ENGINE_DEVELOPMENT.yaml` and `GAME/ENGINE_VERSION.yaml`;
- campaign manifest/schema/template projections for campaign contract generation;
- storage marker/schema naming;
- runtime package schema/metadata consumers;
- all CORE module version headers and header-name consistency;
- catalog machine artifacts/schemas/admission/closure projections from `2.0.0` representation to integer generation `2`;
- ruleset manifest/lock/result/attestation representations;
- package revision and compatibility family/generation;
- custom digest-domain constants/canonicalization and all affected generated hashes/fixtures;
- stale documentation references such as the old catalog `1.2.0` claim;
- loaders/builders/validators/tests/audits/release checks;
- migration/update documentation and future migration graph realization.

No prompt or implementation plan for this realization is created by this specification.

## 22. WP-20 relationship

This amendment becomes an accepted architecture input to R2.7 WP-20 engine update / schema evolution / migration.

It resolves the version-taxonomy portion of WP-20 framing, especially the relation among engine release, persistent schema, aggregate campaign contract generation, catalog generation, ruleset compatibility generation and package/protocol schema identities.

It does not authorize WP-20 Step 2. The mandatory Senior review of the complete Step-1 package must include this amendment and its source research before any Step-2 work begins.

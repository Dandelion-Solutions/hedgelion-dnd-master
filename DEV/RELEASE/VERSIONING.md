# Versioning

This policy is for engine/framework development. It is not a gameplay rule.

Canonical detailed owner for HDM-owned version namespaces, compatibility meaning and migration obligations:

- `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md`.

This file is the compact release/versioning policy projection. If it conflicts with that canonical amendment, the canonical amendment wins.

## 1. Three HDM-owned numbering categories

Every HDM-owned version/revision field belongs to exactly one category.

### A — Engine release identity

Format:

```text
MAJOR.MINOR[-prerelease]
```

Canonical field:

```text
engine_version
```

### B — Engine-bound component/module version

Format:

```text
ENGINE_MAJOR.ENGINE_MINOR.REVISION
```

Canonical CORE/runtime module field:

```text
framework_module_version
```

`ENGINE_MAJOR.ENGINE_MINOR` is the engine line in which the module was last materially changed. `REVISION` is the module-local monotonically increasing revision.

### C — Independent integer counter

Format:

```text
integer N
```

Subtypes are semantically distinct:

- `*_revision` — local bookkeeping/currentness/change counter; not a compatibility boundary by itself;
- `*_schema_version` or artifact-local `schema_version` — one typed serialized-contract schema;
- `*_generation` — semantic/compatibility generation for a coordinated contract family or format;
- domain-local runtime/currentness ordinals — owner-local ordering/currentness only.

These subtypes are not interchangeable merely because all are integers.

## 2. Engine releases

The engine release version uses two numeric components with an optional prerelease suffix, for example `v0.8`, `v1.0-alpha`, or `v1.5`.

`DEV/ENGINE_DEVELOPMENT.yaml` is the canonical development/release bookkeeping record. `GAME/ENGINE_VERSION.yaml` is the installed-package projection; all shared fields must match and are enforced by builder/audit.

Git tags are immutable release/reference points and use the exact `recommended_tag` spelling. Untagged commits on `main` are development state and MUST NOT be offered to campaigns as normal updates.

`release_status` remains meaningful development-package bookkeeping, but it is not a tag-publication gate. For an untagged build, `release_status: development` produces development package identity `dev-v<engine_version>` and runtime use remains subject to the development-package authorization gate. A tag-mode build is authorized by the tag itself: it must be a valid version tag, equal `recommended_tag`, correspond to `v<engine_version>`, resolve to the exact checked-out commit, and satisfy release-lineage validation. No manual `ready-for-tag` transition is required.

A correctly tagged package has release provenance from the immutable tag even when the source-tree status remains `development`; this does not weaken the separate authorization rules for untagged development packages.

Published provenance comes from exact tag identity/commit resolution. The tagged tree is not mutated afterward merely to change release status.

A release intended for campaign integration declares `campaign_update.compatibility` in both version manifests:

- `compatible` — normal automatic integration may proceed only when the full applicable compatibility proof passes;
- `maintenance_required` — bounded campaign maintenance/migration is required or exact compatibility has not been proved.

Missing/unknown compatibility metadata is treated conservatively as maintenance-required.

Semantic `engine_version` is only one compatibility axis. It MUST NOT substitute for campaign-contract generation, local persistent schemas, storage generation, catalog/ruleset compatibility, exact runtime/package provenance or accepted-work interpretation evidence where those axes are material.

An engine release bump alone does not imply campaign migration.

## 3. CORE/runtime module versions

CORE/runtime modules use `ENGINE_MAJOR.ENGINE_MINOR.REVISION` in the canonical field `framework_module_version`.

- `ENGINE_MAJOR.ENGINE_MINOR` records the engine major/minor version in which that module was last materially changed.
- `REVISION` is a monotonically increasing counter belonging only to that module.
- A new module starts at revision `1` under the current engine major/minor.
- Each later logical/material change increments its revision exactly once.
- If the engine version changes but the module does not, the module version does not change.
- On the next module change, update the prefix to current engine major/minor and increment the existing revision.
- Updating the version header as part of the same logical edit is metadata, not an additional revision.
- Prerelease suffixes belong to the engine release/tag, not module versions.
- A versioned CORE/runtime module MUST NOT claim a future engine major/minor line.
- Shipped CORE/runtime modules that are intentionally non-versioned documentation must be explicitly classified as such rather than accidentally omitted from validation.

A campaign never migrates individual module versions. It consumes one exact validated runtime package.

## 4. Independent revisions, schemas and generations

Independent compatibility/bookkeeping counters remain integers. Do not prefix them with engine major/minor for visual uniformity.

### Development revisions

Development-only `*_revision` counters remain independent integers in `DEV/ENGINE_DEVELOPMENT.yaml` and other owning development artifacts.

They do not define runtime compatibility and do not cause campaign migration.

### Persistent family schemas

Each independently serialized persistent record family owns its own integer `schema_version` (or explicitly qualified `*_schema_version`).

Breaking persisted changes require a local schema bump and an explicit migration edge. Compatible optional/additive changes may remain on the same schema version when the owning schema preserves semantics.

Old consumers do not optimistically read unsupported newer schemas. New consumers read older schemas only when support is explicit.

### Campaign-wide persistent contract generation

The aggregate persistent campaign compatibility axis is:

```text
campaign_contract_generation: N
```

This is the aggregate persistent campaign compatibility epoch; it is not a replacement for local family schema versions.

A breaking local persistent-family schema change that requires campaign migration MUST bump campaign contract generation. Campaign contract generation may also bump for a persistent semantic interpretation change requiring coherent migration even when local file shape does not change.

A released campaign retains immutable creation generation and mutable current adopted generation under the canonical versioning amendment.

Different released campaign-contract generations require an explicit migration/adoption path or are unsupported.

### Storage format generation

The storage compatibility field is:

```text
storage_format_generation: N
```

It is independent of campaign-contract generation. Incompatible storage marker/layout semantics bump storage generation and use an explicit storage migration edge.

### Launcher revision

The launcher uses an independent local counter:

```text
launcher_revision: N
```

A launcher revision change alone causes no campaign migration.

## 5. Catalog generation

Catalog uses one coordinated independent integer:

```text
catalog_generation: N
```

The current coordinated machine-contract generation is integer generation `2`.

All coordinated catalog projections MUST equal the canonical catalog generation. Mixed coordinated generations are invalid and fail build/audit/admission.

Local structural `schema_version` values of catalog artifacts remain independent and need not equal `catalog_generation`.

Bump catalog generation only for an incompatible coordinated machine-vocabulary/contract change. Compatible/additive content changes may stay within the same generation and remain distinguishable by exact content/semantic identity.

Different catalog generations are not silently compatible; cross-generation movement requires an explicit admitted adoption/translation/migration boundary or fails unsupported.

## 6. Ruleset package/version namespaces

Ruleset package update order, semantic compatibility and exact content identity are distinct axes.

The current representation separates them as:

```text
package_revision: N
compatibility_family: <stable family identity>
compatibility_generation: N
manifest_schema_version: N
catalog_generation: N
content_sha256 / ruleset_set_sha256: exact identities under their owning digest contracts
```

`package_revision` records package update order only and never proves compatibility.

`compatibility_generation` is the semantic compatibility line. Same generation makes a candidate eligible for the applicable semantic compatibility proof; it does not prove compatibility by itself. Different generation requires explicit adoption/migration or is unsupported.

The normalized pre-release machine representation uses package revision plus compatibility family/generation and integer catalog generation. Exact ruleset identity semantics remain owned by `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` and the canonical versioning amendment.

## 7. Package/protocol schema versions

Runtime-package schema, ruleset-manifest schema, resolved-lock schema, inventory schema, compatibility-result schema, attestation schema and similar typed protocol schemas remain independent integer schema versions.

Released assets are immutable. A new consumer may explicitly support an older schema or reject it; old release assets are not rewritten in place.

Derived package/lock/inventory/attestation data may be regenerated under a new schema from admitted natural-owner inputs. That regeneration is not campaign migration unless a persisted campaign/accepted-work owner stores compatibility-bearing identity whose meaning changes.

## 8. Digest/canonicalization generations

HDM-owned custom hashes/fingerprints are exact identities under one explicit digest/canonicalization contract generation.

A generation change is required when participating fields, canonical serialization, ordering, normalization, domain separation or digest algorithm changes.

Digest-contract generation MUST NOT exist only as an unexplained suffix hidden inside a magic byte string/opaque ID.

A digest generation may be implied by an enclosing typed schema/generation only when that enclosing contract unambiguously fixes the full digest semantics. A digest persisted independently across releases must carry enough typed context to identify its digest contract.

Hashes produced under different digest-contract generations are not directly comparable as the same exact-identity space.

The current HDM-owned ruleset digest/canonicalization domains use explicit generation `1`. Escaping resolved-set and catalog-context identities carry `ruleset_set_digest_generation` and `catalog_context_fingerprint_generation` respectively. Named producer constants and generation-qualified domain separators make the generation mechanically visible.

Current pre-release normalization recomputed all affected HDM-owned derived hashes/fingerprints without compatibility shims. After v1.0 release, old typed exact identities remain meaningful evidence and are migrated/recomputed only from admitted source bytes/evidence.

## 9. Global compatibility/migration laws

1. **Equality is namespace-local.** Numeric equality across unrelated version namespaces has no meaning.
2. **Ordering is namespace-local.** A higher version/generation does not prove compatibility.
3. **Same generation means eligibility, not proof.** Owner-specific semantic/exact checks still apply.
4. **Unknown newer contract fails closed.** No fuzzy or optimistic interpretation.
5. **Migration is an explicit directed graph edge.** Integer arithmetic never manufactures a path.
6. **Reverse/downgrade migration is not guaranteed.** It exists only as an explicit separately supported reverse edge.
7. **One semantic owner per version/generation.** Repeated values are projections and must equal their owner.
8. **Version identity never replaces exact identity/provenance.** Exact package/content/source identities remain distinct.
9. **Released assets are immutable.** Compatibility is expressed by support, migration/adoption or rejection, not by rewriting old release artifacts.

## 10. Publication and rollback boundary

A migration/local transform does not become authoritative merely because target-form bytes were produced.

Authority changes only through the existing confirmed publication/CAS/currentness/authorization boundary.

- abort before publication leaves old authority unchanged;
- confirmed publication rejection leaves old authority unchanged and needs no reverse migration;
- indeterminate publication must be resolved before retry or rollback claims;
- after confirmed accepted migration, returning to an older representation requires an explicit reverse migration edge if one exists.

Checkpoint existence never creates generic rollback support.

## 11. Machine enforcement obligation

Builder/audit/validators enforce:

- every HDM-owned version field is classified and correctly named;
- CORE module versions obey engine-bound component rules and never claim future engine lines;
- shared DEV/GAME `campaign_contract_generation` is equal and the engine manifests carry no aggregate local-schema alias;
- coordinated catalog generation projections are equal integer values;
- unsupported newer schemas/generations fail closed;
- package revision is never treated as semantic compatibility;
- ruleset package/compatibility fields use revision plus stable family/generation axes;
- digest/canonicalization generation is explicit and validated for escaping exact identities;
- development-only revisions do not leak into runtime metadata;
- runtime-package, campaign, storage, ruleset-lock/inventory/comparison/attestation schemas match their normalized shapes;
- pre-release legacy representations are rejected rather than preserved solely for backward compatibility.

The current pre-release machine tree is normalized to this policy. Maintenance audit and focused version-policy tests guard against reintroducing the superseded namespace spellings or mixed generation representations.

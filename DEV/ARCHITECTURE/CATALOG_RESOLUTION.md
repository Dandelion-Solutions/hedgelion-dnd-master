# HDM Catalog Resolution, Identity, and Evolution Contract

Status: **AGREED STEP-1 ARCHITECTURE — RETROSPECTIVE ASSURANCE AMENDMENT**

Related contracts:

- `ARCHITECTURE/CATALOG_MODEL.md`
- `ARCHITECTURE/CATALOG_INVENTORY.md`
- `ARCHITECTURE/CATALOG_CONTRACTS.md`
- `CATALOG/core-catalog.json`
- `CATALOG/identifier-policies.json`

## 1. Purpose

This document closes the definition-resolution semantics that were previously
implicit in the catalog strata model. It defines how stable plain
`definition_id` references remain deterministic across engine/ruleset/campaign/
session sources without per-record version fields or ambient shadowing.

## 2. One ResolvedCatalogContext

Every typed loader, binder, MechanicalContext builder, and Resolution operates
against one logical `ResolvedCatalogContext`.

Conceptually:

```text
ResolvedCatalogContext
    engine capability contract identity
    selected ruleset package identity/set
    campaign-definition frontier
    optional session overlay frontier
```

This is a logical context/authority boundary, not a new world entity. Step 6
owns the concrete ruleset-package manifest and migration/packaging format; Step
5 owns durable checkpoint/publication transport where applicable.

A durable state/checkpoint frontier must retain enough package/frontier identity
to reconstruct a compatible durable ResolvedCatalogContext. The LLM's memory,
current filesystem accident, search result order, or a mutable remote tag is not
catalog authority.

## 3. Definition IDs are unique inside the resolved context

For one ResolvedCatalogContext:

```text
one definition_id -> at most one reusable definition
```

Duplicate definition IDs across loaded ruleset, campaign, or session sources are
validation errors. There is no generic last-layer-wins behavior.

The historical catalog-strata arrow:

```text
engine capability registry
  -> selected ruleset definitions
  -> campaign definitions
  -> session-local definitions
```

means **assembly/dependency/discovery order**, not override or shadowing
precedence.

This preserves stable semantic meaning for plain durable `definition_id`
references.

## 4. No implicit same-ID override

A campaign/session definition must not silently replace a loaded definition by
reusing its ID.

Ordinary new campaign content receives a distinct campaign-owned semantic ID.
When an existing standard mechanic can express a house rule through a Feature,
Rule Element, Activity, policy, or another already-typed campaign mechanism,
use that mechanism rather than mutating catalog identity.

A true modification of an existing reusable ruleset definition is a ruleset
profile/package concern. Step 6 may introduce an explicit derived/forked ruleset
package or migration mechanism. Even then, only one definition for each ID is
present in the resulting ResolvedCatalogContext; runtime layer shadowing remains
forbidden.

## 5. Package/namespace ownership

Definition IDs are semantic namespaced IDs. Namespace ownership belongs at the
loaded package/context level rather than being repeated in every definition.

A future ruleset/campaign package manifest must be able to declare the namespace
or namespaces it owns. Loader validation must reject:

- a definition outside its source's permitted namespace;
- two loaded sources claiming the same resolved definition ID;
- a package combination whose namespace ownership is incompatible.

This contract does not require a global internet namespace registry. It only
requires deterministic ownership inside the selected HDM package set.

## 6. Ruleset package identity and snapshot requirement

`catalog_version` identifies the engine machine-catalog contract. It does not by
itself identify the complete reusable definition set selected for a campaign.
Likewise, a human-readable rules-baseline string is not sufficient package
identity.

When independently versioned ruleset definition packages become executable,
the ResolvedCatalogContext must identify them with stable package-level
metadata sufficient for compatibility/restoration, conceptually including:

```text
package_id
package_version
content identity/digest or equivalent immutable snapshot identity
compatibility identity when distinct from presentation version
```

Exact fields, storage paths, package derivation, and migration tooling are Step
6 concerns. Do not add package version fields to every definition/world record.

Until a separately versioned ruleset package exists, shipped definitions may be
covered by the adopted engine/runtime package identity, provided the release
compatibility contract below is enforced.

## 7. Same-version runtime refresh cannot change catalog meaning incompatibly

Source ancestry proves provenance/order, not semantic compatibility.

A same-semantic-version forward runtime refresh is valid only within the same
declared capability/catalog compatibility line. It may make backward-compatible
or additive catalog changes, but it must not silently:

- repurpose an existing capability/definition ID;
- change an existing definition to an incompatible kind/meaning;
- remove a definition required by accepted durable state;
- invalidate accepted embedded mechanical content without migration.

An incompatible change requires explicit semantic adoption/migration rather than
being treated as cosmetic same-version maintenance.

Release/migration tooling owns the concrete compatibility check in Step 6.
`ENGINE_UPDATES.md` ancestry checks remain necessary provenance evidence but are
not, by themselves, proof of catalog semantic compatibility.

## 8. Session definition promotion

Reusable definitions and world records have different promotion identity rules.

A session-local **definition** already uses semantic identity. Promotion to
campaign scope normally:

```text
preserves definition_id
changes owning storage/layer
publishes required dependency closure
```

Promotion fails if the ID collides in the target ResolvedCatalogContext or if
its namespace is not permitted for campaign durability. Such a case needs an
explicit new definition/migration; runtime must not silently rewrite definition
references.

A session-local **world record** continues to use the allocator/rekey promotion
contract in `CATALOG_CONTRACTS.md` because local world identity and durable
campaign identity are intentionally different.

Durable publication may not leave a durable world/definition reference pointing
to an unpublished session-only dependency.

## 9. Discovery is not authority

Catalog discovery may search/rank reusable definitions and capabilities using
kind, localized names, tags, facets, semantic text, applicability metadata, and
bounded current context.

Search returns candidates. It does not grant capability or prove mechanical
validity.

The execution-facing contract is:

```text
bounded discovery
    -> typed candidate IDs/kinds
    -> LLM semantic selection/adjudication where permitted
    -> deterministic validation against the SAME ResolvedCatalogContext
```

Model memory, a remembered old ID, fuzzy rank, or an unvalidated text match may
never substitute for loaded-catalog validation.

A search miss is not automatically a catalog gap. `unsupported`/
`runtime.catalog_gap_report` is appropriate only after bounded discovery and
deterministic capability validation establish that the requested mechanic is
not expressible in the loaded context.

Exact candidate payload/ranking and knowledge-sensitive filtering belong to
Steps 3–4.

## 10. Migration and failure semantics

Loading/adopting a catalog context fails explicitly when, after the applicable
migration process, any durable reference has:

- missing definition ID;
- incompatible definition kind;
- incompatible capability contract;
- ambiguous duplicate definition ID;
- unresolved unpublished dependency.

The LLM must not regenerate a plausible replacement to make the load succeed.

Compatible additive package changes need not force per-record migration.
Incompatible semantic changes are handled at package/campaign migration scope,
consistent with HDM's coherent-snapshot model.

## 11. S6D package-identity closure

S6D-01 has closed the package/snapshot identity architecture in:

- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`

That owner defines content-addressed `RulesetPackageSnapshot` values, exact
dependency-closed `ResolvedRulesetSnapshotSet` identity, natural-owner
campaign/execution projections, adoption boundaries and reconstruction laws.

Remaining downstream ownership is explicit:

- S6D-02 supplies actual ruleset package instances, namespace claims and seed content;
- S6D-11 supplies manifest/lock schemas, builder/loader realization and RED→GREEN verification;
- R2.7 WP-20 owns future incompatible released-campaign migration policy.

A derived/profile package remains dormant unless a proven reusable same-ID
replacement consumer requires it. House Rules `realization_refs` do not create
such a package implicitly.
